#!/usr/bin/env python3
"""
Verification Reviewer — Review Agent

Applies domain-specific extraction rules to each discrepancy
and recommends which value is more likely correct.

Rules encoded from docs/extraction_guidelines.md.
Used as a module by orchestrate_comparison.py.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import get_logger
from scripts.comparison_engine import (
    ComparisonRecord,
    DiscrepancyType,
    Severity,
    normalize_value,
    _try_float,
)

# ── Energy fields that should be in MJ ───────────────────────────────────

ENERGY_MJ_FIELDS = {"34", "35", "36"}  # 2024/2023/2022 年度總能源使用量

# ── Boolean fields ───────────────────────────────────────────────────────

BOOLEAN_FIELDS = {
    "3", "8", "31", "32", "37", "46", "47", "48",
    "51", "55", "58", "62", "66", "70",
    "101", "102",
}

# ── Fields where blank = "not mentioned" (not False) ─────────────────────
# Per extraction guidelines: 「未揭露」「無資料」應視為「留空」而非 False


def review_discrepancy(record: ComparisonRecord) -> ComparisonRecord:
    """
    Apply domain rules to a single discrepancy and fill recommendation fields.

    Mutates the record in-place and returns it.
    """
    if record.discrepancy_type == DiscrepancyType.MATCH:
        record.recommended_value = record.google_value or record.agentic_value
        record.recommendation_source = "both"
        record.confidence = "high"
        record.review_notes = "Values match after normalization"
        return record

    # Dispatch by discrepancy type
    handler = _HANDLERS.get(record.discrepancy_type, _review_default)
    return handler(record)


# ── Type-specific handlers ───────────────────────────────────────────────


def _review_unit_conversion(record: ComparisonRecord) -> ComparisonRecord:
    """Handle UNIT_CONVERSION: energy fields should be in MJ per guidelines."""
    g_num = _try_float(record.google_value)
    a_num = _try_float(record.agentic_value)

    if record.field_id in ENERGY_MJ_FIELDS:
        # Extraction guidelines: energy should be in MJ
        # The larger value is likely MJ (×1000 of GJ)
        if g_num is not None and a_num is not None:
            if a_num > g_num:
                record.recommended_value = record.agentic_value
                record.recommendation_source = "agentic"
                record.confidence = "high"
                record.review_notes = (
                    f"Agentic value ({a_num:,.0f}) is MJ (correct unit per guidelines). "
                    f"Google value ({g_num:,.0f}) appears to be in GJ."
                )
            else:
                record.recommended_value = record.google_value
                record.recommendation_source = "google"
                record.confidence = "high"
                record.review_notes = (
                    f"Google value ({g_num:,.0f}) is MJ (correct unit per guidelines). "
                    f"Agentic value ({a_num:,.0f}) appears to be in GJ."
                )
        else:
            record.recommended_value = ""
            record.recommendation_source = "human_review"
            record.confidence = "low"
            record.review_notes = "Unit conversion detected but cannot determine correct unit."
    else:
        # Non-energy field with ×1000 factor: needs human review
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "medium"
        record.review_notes = (
            f"×1000 factor difference. "
            f"Google: {record.google_value}, Agentic: {record.agentic_value}. "
            f"Check report for correct unit."
        )

    return record


def _review_boolean_diff(record: ComparisonRecord) -> ComparisonRecord:
    """Handle BOOLEAN_DIFF: apply blank ≠ False rule from extraction guidelines."""
    g_norm = normalize_value(record.google_value)
    a_norm = normalize_value(record.agentic_value)

    g_is_blank = g_norm == ""
    a_is_blank = a_norm == ""

    # Rule: blank means "not mentioned", False means "explicitly denied"
    # If one says blank and other says False, the one saying False is more informative
    # BUT only if the report actually explicitly denies it

    if g_is_blank and a_norm == "False":
        # Agentic explicitly found a "no" — check if notes support it
        if _notes_support_explicit_denial(record.agentic_notes):
            record.recommended_value = "False"
            record.recommendation_source = "agentic"
            record.confidence = "medium"
            record.review_notes = (
                "Agentic found explicit denial (False) supported by notes. "
                "Google left blank (not mentioned). Agentic appears more precise."
            )
        else:
            record.recommended_value = ""
            record.recommendation_source = "human_review"
            record.confidence = "low"
            record.review_notes = (
                "Google blank vs Agentic False. Per guidelines, blank = not mentioned. "
                "Agentic notes don't clearly indicate explicit denial. Needs human check."
            )
    elif a_is_blank and g_norm == "False":
        if _notes_support_explicit_denial(record.google_notes):
            record.recommended_value = "False"
            record.recommendation_source = "google"
            record.confidence = "medium"
            record.review_notes = (
                "Google found explicit denial (False) supported by notes. "
                "Agentic left blank."
            )
        else:
            record.recommended_value = ""
            record.recommendation_source = "human_review"
            record.confidence = "low"
            record.review_notes = (
                "Agentic blank vs Google False. Needs human review to determine "
                "if report explicitly denies or simply doesn't mention."
            )
    elif g_norm == "True" and a_norm == "False":
        # Direct contradiction — high severity, always human review
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"Direct contradiction: Google=True, Agentic=False. "
            f"Google notes: {_truncate(record.google_notes, 80)} | "
            f"Agentic notes: {_truncate(record.agentic_notes, 80)}"
        )
    elif g_norm == "False" and a_norm == "True":
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"Direct contradiction: Google=False, Agentic=True. "
            f"Google notes: {_truncate(record.google_notes, 80)} | "
            f"Agentic notes: {_truncate(record.agentic_notes, 80)}"
        )
    else:
        # Other boolean-adjacent mismatches (e.g., "無承諾" vs blank)
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"Boolean-like mismatch: Google='{record.google_value}' vs "
            f"Agentic='{record.agentic_value}'. Check extraction guidelines."
        )

    return record


def _review_numeric_diff(record: ComparisonRecord) -> ComparisonRecord:
    """Handle NUMERIC_DIFF: significantly different numbers."""
    g_num = _try_float(record.google_value)
    a_num = _try_float(record.agentic_value)

    # Check if one has more page references (more thorough extraction)
    g_pages = _count_page_refs(record.google_page_refs)
    a_pages = _count_page_refs(record.agentic_page_refs)

    # Check if notes explain the source
    g_has_source = _notes_cite_source(record.google_notes)
    a_has_source = _notes_cite_source(record.agentic_notes)

    # Heuristic: more page refs + source citation = more reliable
    g_score = g_pages + (1 if g_has_source else 0)
    a_score = a_pages + (1 if a_has_source else 0)

    if g_score > a_score + 1:
        record.recommended_value = record.google_value
        record.recommendation_source = "google"
        record.confidence = "low"
        record.review_notes = (
            f"Google has better source documentation "
            f"({g_pages} page refs, source cited: {g_has_source}) vs "
            f"Agentic ({a_pages} page refs, source cited: {a_has_source}). "
            f"Still needs human verification."
        )
    elif a_score > g_score + 1:
        record.recommended_value = record.agentic_value
        record.recommendation_source = "agentic"
        record.confidence = "low"
        record.review_notes = (
            f"Agentic has better source documentation "
            f"({a_pages} page refs, source cited: {a_has_source}) vs "
            f"Google ({g_pages} page refs, source cited: {g_has_source}). "
            f"Still needs human verification."
        )
    else:
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"Numbers differ significantly: Google={record.google_value} vs "
            f"Agentic={record.agentic_value}. Similar source quality. Must verify against report."
        )

    return record


def _review_coverage_gap(record: ComparisonRecord) -> ComparisonRecord:
    """Handle COVERAGE_GAP: one has data, other is blank."""
    g_norm = normalize_value(record.google_value)
    a_norm = normalize_value(record.agentic_value)

    has_data_source = "google" if g_norm else "agentic"
    data_value = g_norm if g_norm else a_norm
    data_notes = record.google_notes if g_norm else record.agentic_notes
    blank_notes = record.agentic_notes if g_norm else record.google_notes

    # Per guidelines: empty = not found. If one method found data, check if notes
    # from the blank method explain why it was left blank
    blank_explains = _notes_explain_absence(blank_notes)

    if blank_explains:
        # Blank method actively searched and didn't find it — conflict
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"{has_data_source.title()} found '{_truncate(data_value, 50)}' but "
            f"other method notes: '{_truncate(blank_notes, 80)}'. "
            f"Need to verify which is correct."
        )
    else:
        # Blank method may have simply missed it
        record.recommended_value = record.google_value if g_norm else record.agentic_value
        record.recommendation_source = has_data_source
        record.confidence = "medium"
        record.review_notes = (
            f"Only {has_data_source} extracted a value. "
            f"Other method left blank without explanation. "
            f"Tentatively accepting {has_data_source}'s value."
        )

    return record


def _review_text_diff(record: ComparisonRecord) -> ComparisonRecord:
    """Handle TEXT_DIFF: different text phrasing."""
    # For text fields, the more detailed answer with page refs is preferred
    g_len = len(record.google_value.strip())
    a_len = len(record.agentic_value.strip())
    g_pages = _count_page_refs(record.google_page_refs)
    a_pages = _count_page_refs(record.agentic_page_refs)

    # Prefer the more detailed, better-sourced version
    if a_pages > g_pages and a_len >= g_len * 0.7:
        record.recommended_value = record.agentic_value
        record.recommendation_source = "agentic"
        record.confidence = "medium"
        record.review_notes = "Agentic has more page references and comparable detail."
    elif g_pages > a_pages and g_len >= a_len * 0.7:
        record.recommended_value = record.google_value
        record.recommendation_source = "google"
        record.confidence = "medium"
        record.review_notes = "Google has more page references and comparable detail."
    else:
        # Similar quality — prefer the more detailed one
        record.recommended_value = ""
        record.recommendation_source = "human_review"
        record.confidence = "low"
        record.review_notes = (
            f"Text differs but similar quality. "
            f"Google ({g_len} chars, {g_pages} pages) vs "
            f"Agentic ({a_len} chars, {a_pages} pages)."
        )

    return record


def _review_format_diff(record: ComparisonRecord) -> ComparisonRecord:
    """Handle FORMAT_DIFF: same data, different representation."""
    record.recommended_value = record.agentic_value or record.google_value
    record.recommendation_source = "agentic" if record.agentic_value else "google"
    record.confidence = "high"
    record.review_notes = (
        f"Format variation only. Google='{_truncate(record.google_value, 40)}' vs "
        f"Agentic='{_truncate(record.agentic_value, 40)}'."
    )
    return record


def _review_default(record: ComparisonRecord) -> ComparisonRecord:
    """Default handler for unknown discrepancy types."""
    record.recommended_value = ""
    record.recommendation_source = "human_review"
    record.confidence = "low"
    record.review_notes = "Unclassified discrepancy. Needs manual review."
    return record


_HANDLERS = {
    DiscrepancyType.UNIT_CONVERSION: _review_unit_conversion,
    DiscrepancyType.BOOLEAN_DIFF: _review_boolean_diff,
    DiscrepancyType.NUMERIC_DIFF: _review_numeric_diff,
    DiscrepancyType.COVERAGE_GAP: _review_coverage_gap,
    DiscrepancyType.TEXT_DIFF: _review_text_diff,
    DiscrepancyType.FORMAT_DIFF: _review_format_diff,
}


# ── Helper functions ─────────────────────────────────────────────────────


def _truncate(text: str, max_len: int = 50) -> str:
    if not text:
        return "(empty)"
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def _count_page_refs(page_str: str) -> int:
    """Count the number of page references in a string like 'p.10, p.12'."""
    if not page_str or page_str.strip().upper() == "NA":
        return 0
    return len(re.findall(r"p\.\d+", page_str, re.IGNORECASE))


def _notes_cite_source(notes: str) -> bool:
    """Check if notes cite a specific data source (GRI, SASB, table reference)."""
    if not notes:
        return False
    source_patterns = [
        r"GRI\s*\d+",
        r"SASB",
        r"附錄",
        r"表\d+|表格",
        r"揭露",
        r"數據來自",
    ]
    return any(re.search(p, notes) for p in source_patterns)


def _notes_support_explicit_denial(notes: str) -> bool:
    """Check if notes contain evidence of explicit denial/negative finding."""
    if not notes:
        return False
    denial_patterns = [
        r"未取得",
        r"未達成",
        r"未設定",
        r"無.*認證",
        r"否",
        r"尚未",
        r"未提及.*取得",
        r"明確表示.*否",
        r"未加入",
    ]
    return any(re.search(p, notes) for p in denial_patterns)


def _notes_explain_absence(notes: str) -> bool:
    """Check if notes explain why a value was left blank."""
    if not notes:
        return False
    absence_patterns = [
        r"未提及",
        r"未揭露",
        r"未.*相關",
        r"無.*資訊",
        r"報告書[中未]",
        r"找不到",
        r"無法",
    ]
    return any(re.search(p, notes) for p in absence_patterns)


# ── Batch review ─────────────────────────────────────────────────────────


def review_batch(records: list[ComparisonRecord]) -> list[ComparisonRecord]:
    """
    Review all comparison records and fill recommendation fields.

    Args:
        records: List of ComparisonRecords from comparison engine

    Returns:
        Same list with recommendation fields populated
    """
    logger = get_logger()

    for record in records:
        review_discrepancy(record)

    # Log summary
    total = len(records)
    matches = sum(1 for r in records if r.discrepancy_type == DiscrepancyType.MATCH)
    human_review = sum(1 for r in records if r.recommendation_source == "human_review")
    google_rec = sum(1 for r in records if r.recommendation_source == "google")
    agentic_rec = sum(1 for r in records if r.recommendation_source == "agentic")

    logger.info(
        f"Review complete: {total} fields — "
        f"{matches} match, {google_rec} rec. Google, {agentic_rec} rec. Agentic, "
        f"{human_review} need human review"
    )

    return records
