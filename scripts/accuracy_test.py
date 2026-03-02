#!/usr/bin/env python3
"""
Accuracy Test — Self-test harness for agentic extraction quality.

Compares the latest agentic extraction results against PDF-verified ground truth
to measure accuracy and identify remaining errors by root cause.

Usage:
    python scripts/accuracy_test.py
    python scripts/accuracy_test.py --company 1216
    python scripts/accuracy_test.py --verbose
"""

import csv
import json
import re
import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR
from src.utils import setup_logging, get_logger

GROUND_TRUTH_PATH = OUTPUT_DIR / "verification" / "ground_truth.json"
AGENTIC_CSV_PATH = (
    Path(__file__).parent.parent
    / "LLM 解析結果 - 欄位蒐集結果.csv"
)


def load_ground_truth(path: Path) -> list[dict]:
    """Load ground truth fields."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["fields"]


def load_agentic_results(csv_path: Path) -> dict[tuple[str, str], str]:
    """Load agentic CSV into a lookup dict keyed by (company_code, field_id)."""
    lookup: dict[tuple[str, str], str] = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            company_code = row.get("公司代碼", "").strip()
            field_id = row.get("欄位編號", "").strip()
            value = row.get("欄位數值", "").strip()
            if company_code and field_id:
                lookup[(company_code, field_id)] = value
    return lookup


def normalize_for_comparison(value: str) -> str:
    """Normalize a value for fuzzy comparison."""
    if not value:
        return ""
    s = str(value).strip()
    # Remove thousand separators
    s = s.replace(",", "")
    # Normalize whitespace
    s = re.sub(r"\s+", " ", s)
    # Strip trailing zeros after decimal
    try:
        f = float(s)
        # Represent as clean float
        if f == int(f):
            return str(int(f))
        return f"{f:.10f}".rstrip("0").rstrip(".")
    except (ValueError, OverflowError):
        pass
    return s


def values_match(agentic_val: str, truth_val: str) -> bool:
    """Check if agentic value matches ground truth (fuzzy)."""
    a = normalize_for_comparison(agentic_val)
    t = normalize_for_comparison(truth_val)

    # Forbidden tokens that should never appear in extraction output
    forbidden = {"不適用", "未揭露", "無", "無資料", "無法填答", "na", "n/a", "-"}

    if not t:
        # Truth is blank — agentic should also be blank
        return a == ""

    if a == t:
        return True

    # Numeric comparison with tolerance
    try:
        a_num = float(a)
        t_num = float(t)
        if t_num == 0:
            return a_num == 0
        ratio = abs(a_num - t_num) / abs(t_num)
        return ratio < 0.01  # 1% tolerance
    except (ValueError, OverflowError):
        pass

    # Boolean comparison
    bool_map = {"true": "True", "false": "False"}
    if a.lower() in bool_map and t.lower() in bool_map:
        return a.lower() == t.lower()

    # Text containment check (for text fields where agentic may be more/less verbose)
    if len(t) > 10 and len(a) > 10:
        # Check significant keyword overlap using Chinese characters and words
        t_words = set(re.findall(r"[\w\u4e00-\u9fff]+", t))
        a_words = set(re.findall(r"[\w\u4e00-\u9fff]+", a))
        if t_words and a_words:
            overlap = len(t_words & a_words) / max(len(t_words), len(a_words))
            if overlap > 0.5:
                return True

    return False


def run_accuracy_test(
    ground_truth: list[dict],
    agentic_lookup: dict[tuple[str, str], str],
    company_filter: str | None = None,
) -> dict:
    """Run accuracy test and return results."""

    results: list[dict] = []
    for gt in ground_truth:
        company = gt["company_code"]
        if company_filter and company != company_filter:
            continue

        field_id = gt["field_id"]
        truth_val = gt["verified_value"]
        agentic_val = agentic_lookup.get((company, field_id), "")

        match = values_match(agentic_val, truth_val)
        root_cause = gt.get("root_cause_if_agentic_wrong")

        results.append({
            "company_code": company,
            "company_name": gt["company_name"],
            "field_id": field_id,
            "field_name": gt["field_name"],
            "truth_value": truth_val,
            "agentic_value": agentic_val,
            "match": match,
            "root_cause": root_cause if not match else None,
            "pdf_page": gt.get("pdf_page", ""),
        })

    # Compute metrics
    total = len(results)
    correct = sum(1 for r in results if r["match"])
    wrong = total - correct

    # Root cause breakdown for wrong answers
    root_causes = Counter(
        r["root_cause"] for r in results
        if not r["match"] and r["root_cause"]
    )

    # Per-company breakdown
    by_company: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_company[f"{r['company_code']} {r['company_name']}"].append(r)

    company_scores = {}
    for company, fields in sorted(by_company.items()):
        c = sum(1 for f in fields if f["match"])
        company_scores[company] = {
            "total": len(fields),
            "correct": c,
            "pct": f"{c / len(fields) * 100:.1f}%" if fields else "0%",
        }

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "accuracy_pct": f"{correct / total * 100:.1f}%" if total else "0%",
        "root_causes": dict(root_causes.most_common()),
        "company_scores": company_scores,
        "details": results,
    }


def print_report(metrics: dict, verbose: bool = False) -> None:
    """Print accuracy report to console."""
    print(f"\n{'='*60}")
    print("AGENTIC EXTRACTION ACCURACY TEST")
    print(f"{'='*60}")
    print(f"Total verified fields:  {metrics['total']}")
    print(f"Correct:                {metrics['correct']}/{metrics['total']} ({metrics['accuracy_pct']})")
    print(f"Wrong:                  {metrics['wrong']}/{metrics['total']}")

    if metrics["root_causes"]:
        print(f"\n{'─'*40}")
        print("Root Cause Breakdown (remaining errors):")
        for cause, count in metrics["root_causes"].items():
            print(f"  {cause or 'UNKNOWN'}: {count}")

    print(f"\n{'─'*40}")
    print("Per-Company Scores:")
    for company, scores in metrics["company_scores"].items():
        print(f"  {company}: {scores['correct']}/{scores['total']} ({scores['pct']})")

    if verbose:
        wrong_fields = [r for r in metrics["details"] if not r["match"]]
        if wrong_fields:
            print(f"\n{'─'*40}")
            print("Remaining Errors:")
            for r in wrong_fields:
                print(
                    f"\n  [{r['company_code']}] Field {r['field_id']} ({r['field_name']})"
                )
                print(f"    Truth:   {str(r['truth_value'])[:80]}")
                print(f"    Agentic: {str(r['agentic_value'])[:80]}")
                print(f"    Cause:   {r['root_cause'] or 'UNKNOWN'}")
                print(f"    Page:    {r['pdf_page']}")

    print(f"\n{'='*60}")


def main():
    parser = ArgumentParser(description="Test agentic extraction accuracy against ground truth")
    parser.add_argument("--company", help="Filter to specific company code")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show error details")
    parser.add_argument("--ground-truth", type=Path, default=GROUND_TRUTH_PATH,
                        help="Path to ground truth JSON")
    parser.add_argument("--agentic-csv", type=Path, default=AGENTIC_CSV_PATH,
                        help="Path to agentic results CSV")
    parser.add_argument("--json-output", type=Path, help="Write results as JSON to this path")
    args = parser.parse_args()

    setup_logging(session_name="accuracy_test")
    logger = get_logger()

    if not args.ground_truth.exists():
        logger.error(f"Ground truth not found: {args.ground_truth}")
        sys.exit(1)

    if not args.agentic_csv.exists():
        logger.error(f"Agentic CSV not found: {args.agentic_csv}")
        sys.exit(1)

    ground_truth = load_ground_truth(args.ground_truth)
    logger.info(f"Loaded {len(ground_truth)} ground truth fields")

    agentic_lookup = load_agentic_results(args.agentic_csv)
    logger.info(f"Loaded {len(agentic_lookup)} agentic extraction values")

    metrics = run_accuracy_test(
        ground_truth, agentic_lookup,
        company_filter=args.company,
    )

    print_report(metrics, verbose=args.verbose)

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
        logger.info(f"Results written to {args.json_output}")


if __name__ == "__main__":
    main()
