#!/usr/bin/env python3
"""
Comparison Engine — Discrepancy Agent

Compares field-by-field values between two ESG extraction methods
(Google API vs Agentic Workflow) and classifies discrepancies.

Used as a module by orchestrate_comparison.py.
"""

import re
import sys
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import get_logger


class DiscrepancyType(str, Enum):
    MATCH = "MATCH"
    UNIT_CONVERSION = "UNIT_CONVERSION"
    BOOLEAN_DIFF = "BOOLEAN_DIFF"
    NUMERIC_DIFF = "NUMERIC_DIFF"
    TEXT_DIFF = "TEXT_DIFF"
    COVERAGE_GAP = "COVERAGE_GAP"
    FORMAT_DIFF = "FORMAT_DIFF"


class Severity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ComparisonRecord:
    company_code: str
    company_name: str
    field_id: str
    field_name: str
    google_value: str
    agentic_value: str
    google_notes: str
    agentic_notes: str
    google_page_refs: str
    agentic_page_refs: str
    match_status: str  # "match" or "mismatch"
    discrepancy_type: DiscrepancyType
    severity: Severity
    # Filled by verification reviewer
    recommended_value: str = ""
    recommendation_source: str = ""
    confidence: str = ""
    review_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "公司代碼": self.company_code,
            "公司簡稱": self.company_name,
            "欄位編號": self.field_id,
            "欄位名稱": self.field_name,
            "google_value": self.google_value,
            "agentic_value": self.agentic_value,
            "google_notes": self.google_notes,
            "agentic_notes": self.agentic_notes,
            "google_page_refs": self.google_page_refs,
            "agentic_page_refs": self.agentic_page_refs,
            "match_status": self.match_status,
            "discrepancy_type": self.discrepancy_type.value,
            "severity": self.severity.value,
            "recommended_value": self.recommended_value,
            "recommendation_source": self.recommendation_source,
            "confidence": self.confidence,
            "review_notes": self.review_notes,
        }


# ── Normalization (adapted from compare_results.py) ──────────────────────


def normalize_value(value: str) -> str:
    """Normalize a value for comparison: strip, empty→'', booleans, numeric trailing zeros."""
    if value is None:
        return ""

    value = str(value).strip()

    # Normalize empty-like values
    if value.lower() in ("", "無", "無資料", "無法填答", "na", "n/a", "none", "-", "不適用"):
        return ""

    # Normalize booleans
    if value.lower() in ("true", "yes", "是"):
        return "True"
    if value.lower() in ("false", "no", "否"):
        return "False"

    # Normalize numeric strings
    try:
        num = float(value.replace(",", ""))
        if num == int(num):
            return str(int(num))
        return f"{num:.10f}".rstrip("0").rstrip(".")
    except ValueError:
        pass

    return value


def _try_float(value: str) -> Optional[float]:
    """Try to parse a string as float, return None on failure."""
    if not value or not isinstance(value, str):
        return None
    try:
        return float(value.replace(",", "").strip())
    except ValueError:
        return None


def _is_boolean(value: str) -> bool:
    """Check if a normalized value is boolean-like."""
    return normalize_value(value) in ("True", "False", "")


# ── Discrepancy Classification ───────────────────────────────────────────


def classify_discrepancy(
    google_raw: str,
    agentic_raw: str,
    field_id: str,
) -> tuple[DiscrepancyType, Severity]:
    """
    Classify the type and severity of a discrepancy between two values.

    Returns (DiscrepancyType, Severity).
    """
    g_norm = normalize_value(google_raw)
    a_norm = normalize_value(agentic_raw)

    # ── Exact match after normalization ──
    if g_norm == a_norm:
        return DiscrepancyType.MATCH, Severity.NONE

    g_empty = g_norm == ""
    a_empty = a_norm == ""

    # ── Coverage gap: one has data, other is blank ──
    if g_empty != a_empty:
        # Check if the non-empty value is just "False" for a boolean field
        non_empty = a_norm if g_empty else g_norm
        if non_empty == "False":
            return DiscrepancyType.BOOLEAN_DIFF, Severity.MEDIUM
        return DiscrepancyType.COVERAGE_GAP, Severity.HIGH

    # ── Both have values: try numeric comparison ──
    g_num = _try_float(g_norm)
    a_num = _try_float(a_norm)

    if g_num is not None and a_num is not None:
        # Check unit conversion (×1000 factor, GJ↔MJ)
        if g_num != 0 and a_num != 0:
            ratio = a_num / g_num
            if abs(ratio - 1000) < 1 or abs(ratio - 0.001) < 0.000001:
                return DiscrepancyType.UNIT_CONVERSION, Severity.MEDIUM

        # Check if values are very close (floating point tolerance)
        if g_num != 0 and abs(g_num - a_num) / abs(g_num) < 0.001:
            return DiscrepancyType.MATCH, Severity.NONE

        # Genuinely different numbers
        return DiscrepancyType.NUMERIC_DIFF, Severity.HIGH

    # ── Boolean comparison ──
    g_bool = g_norm in ("True", "False")
    a_bool = a_norm in ("True", "False")

    if g_bool or a_bool:
        return DiscrepancyType.BOOLEAN_DIFF, Severity.HIGH

    # ── Text comparison ──
    # Format diff: same core info, different representation (e.g., "0" vs "不適用")
    # We already normalized "不適用" to "" above, so remaining format diffs are subtler
    if _is_format_variation(google_raw, agentic_raw):
        return DiscrepancyType.FORMAT_DIFF, Severity.LOW

    # Text diff: different phrasing, potentially same meaning
    return DiscrepancyType.TEXT_DIFF, _score_text_severity(g_norm, a_norm)


def _is_format_variation(val1: str, val2: str) -> bool:
    """Check if two values are format variations of the same info."""
    v1, v2 = val1.strip(), val2.strip()

    # One is "0" and other is a non-applicable marker
    non_applicable = {"0", "不適用", "無", "NA", "N/A", "-"}
    if v1 in non_applicable and v2 in non_applicable:
        return True

    # Numeric with/without units embedded
    # e.g., "9895 TJ" vs "9895"
    nums1 = re.findall(r"[\d.]+", v1)
    nums2 = re.findall(r"[\d.]+", v2)
    if nums1 and nums2 and nums1[0] == nums2[0] and len(nums1) == 1 and len(nums2) == 1:
        return True

    return False


def _score_text_severity(val1: str, val2: str) -> Severity:
    """Score severity of text differences based on overlap."""
    # Short texts with little overlap → high severity
    if len(val1) < 20 or len(val2) < 20:
        return Severity.MEDIUM

    # Check token overlap
    tokens1 = set(val1.replace("、", " ").replace("，", " ").replace(";", " ").split())
    tokens2 = set(val2.replace("、", " ").replace("，", " ").replace(";", " ").split())

    max_tokens = max(len(tokens1), len(tokens2))
    if max_tokens == 0:
        return Severity.MEDIUM

    overlap = len(tokens1 & tokens2) / max_tokens
    if overlap >= 0.5:
        return Severity.LOW
    return Severity.MEDIUM


# ── Main comparison function ─────────────────────────────────────────────


def compare_field_pair(
    company_code: str,
    company_name: str,
    field_id: str,
    field_name: str,
    google_row: dict,
    agentic_row: dict,
) -> ComparisonRecord:
    """Compare a single field between Google API and Agentic results."""
    g_val = google_row.get("欄位數值", "")
    a_val = agentic_row.get("欄位數值", "")

    disc_type, severity = classify_discrepancy(g_val, a_val, field_id)

    return ComparisonRecord(
        company_code=company_code,
        company_name=company_name,
        field_id=field_id,
        field_name=field_name,
        google_value=g_val,
        agentic_value=a_val,
        google_notes=google_row.get("補充說明", ""),
        agentic_notes=agentic_row.get("補充說明", ""),
        google_page_refs=google_row.get("參考頁數", ""),
        agentic_page_refs=agentic_row.get("參考頁數", ""),
        match_status="match" if disc_type == DiscrepancyType.MATCH else "mismatch",
        discrepancy_type=disc_type,
        severity=severity,
    )


def compare_company_batch(
    company_code: str,
    company_name: str,
    google_rows: list[dict],
    agentic_rows: list[dict],
) -> list[ComparisonRecord]:
    """
    Compare all fields for a single company across both methods.

    Args:
        company_code: Company stock code
        company_name: Company short name
        google_rows: List of row dicts from Google API CSV
        agentic_rows: List of row dicts from Agentic CSV

    Returns:
        List of ComparisonRecords
    """
    logger = get_logger()

    # Build lookups by field_id
    g_by_field = {r["欄位編號"]: r for r in google_rows}
    a_by_field = {r["欄位編號"]: r for r in agentic_rows}

    # Find common fields
    common_fields = sorted(
        set(g_by_field.keys()) & set(a_by_field.keys()),
        key=lambda x: int(x) if x.isdigit() else 9999,
    )

    records: list[ComparisonRecord] = []
    for fid in common_fields:
        g_row = g_by_field[fid]
        a_row = a_by_field[fid]
        field_name = g_row.get("欄位名稱", f"欄位{fid}")

        record = compare_field_pair(
            company_code, company_name, fid, field_name, g_row, a_row,
        )
        records.append(record)

    matches = sum(1 for r in records if r.match_status == "match")
    mismatches = len(records) - matches
    logger.info(
        f"[{company_code} {company_name}] {len(records)} fields compared: "
        f"{matches} match, {mismatches} mismatch"
    )

    return records
