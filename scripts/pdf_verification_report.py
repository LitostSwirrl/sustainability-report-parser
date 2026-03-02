#!/usr/bin/env python3
"""
PDF Verification Report — Review & Aggregation Agent

Reads verification result JSONs from PDF agents and generates:
- Accuracy scorecard per method
- Error pattern analysis
- Final verified CSV
- Summary markdown

Usage:
    python scripts/pdf_verification_report.py
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR
from src.utils import setup_logging, get_logger

VERIFICATION_DIR = OUTPUT_DIR / "verification"
RESULTS_DIR = VERIFICATION_DIR / "results"


def load_verification_results(results_dir: Path) -> list[dict]:
    """Load all verification result JSONs."""
    logger = get_logger()
    all_fields: list[dict] = []

    for json_path in sorted(results_dir.glob("*_verified.json")):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        company_code = data["company_code"]
        company_name = data["company_name"]

        for field in data["fields"]:
            field["company_code"] = company_code
            field["company_name"] = company_name
            all_fields.append(field)

        logger.info(
            f"Loaded {len(data['fields'])} verified fields from {json_path.name}"
        )

    return all_fields


def write_verified_csv(fields: list[dict], output_path: Path) -> None:
    """Write verified comparison CSV."""
    fieldnames = [
        "company_code", "company_name", "field_id", "field_name",
        "google_value", "agentic_value", "verified_value",
        "correct_source", "verification_notes", "pdf_page",
    ]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for field in fields:
            writer.writerow(field)


def write_accuracy_csv(fields: list[dict], output_path: Path) -> None:
    """Write per-method accuracy breakdown."""
    # Overall
    total = len(fields)
    correct_source_counts = Counter(f["correct_source"] for f in fields)

    google_correct = correct_source_counts.get("google", 0) + correct_source_counts.get("both", 0)
    agentic_correct = correct_source_counts.get("agentic", 0) + correct_source_counts.get("both", 0)
    both_correct = correct_source_counts.get("both", 0)
    neither_correct = correct_source_counts.get("neither", 0)

    # Per company
    by_company: dict[str, list[dict]] = defaultdict(list)
    for f in fields:
        by_company[f"{f['company_code']} {f['company_name']}"].append(f)

    rows = []

    # Overall row
    rows.append({
        "scope": "OVERALL",
        "total": total,
        "google_correct": google_correct,
        "google_pct": f"{google_correct / total * 100:.1f}%" if total else "0%",
        "agentic_correct": agentic_correct,
        "agentic_pct": f"{agentic_correct / total * 100:.1f}%" if total else "0%",
        "both_correct": both_correct,
        "neither_correct": neither_correct,
    })

    # Per-company rows
    for company, company_fields in sorted(by_company.items()):
        ct = len(company_fields)
        cc = Counter(f["correct_source"] for f in company_fields)
        gc = cc.get("google", 0) + cc.get("both", 0)
        ac = cc.get("agentic", 0) + cc.get("both", 0)
        rows.append({
            "scope": company,
            "total": ct,
            "google_correct": gc,
            "google_pct": f"{gc / ct * 100:.1f}%" if ct else "0%",
            "agentic_correct": ac,
            "agentic_pct": f"{ac / ct * 100:.1f}%" if ct else "0%",
            "both_correct": cc.get("both", 0),
            "neither_correct": cc.get("neither", 0),
        })

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_summary_markdown(fields: list[dict], output_path: Path) -> None:
    """Generate human-readable verification summary."""
    total = len(fields)
    cc = Counter(f["correct_source"] for f in fields)

    google_correct = cc.get("google", 0) + cc.get("both", 0)
    agentic_correct = cc.get("agentic", 0) + cc.get("both", 0)
    both_correct = cc.get("both", 0)
    neither = cc.get("neither", 0)
    google_only = cc.get("google", 0)
    agentic_only = cc.get("agentic", 0)

    # Per company
    by_company: dict[str, list[dict]] = defaultdict(list)
    for f in fields:
        by_company[f"{f['company_code']} {f['company_name']}"].append(f)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# PDF-Verified Comparison Report",
        "",
        f"Generated: {now}",
        f"Discrepancies verified: {total}",
        "",
        "## Overall Accuracy (across discrepancies only)",
        "",
        "| Method | Correct | % | Interpretation |",
        "|--------|---------|---|----------------|",
        f"| Google API (prompt ver. 5) | {google_correct}/{total} | "
        f"{google_correct / total * 100:.1f}% | Google got it right |",
        f"| Agentic Workflow (Claude Code) | {agentic_correct}/{total} | "
        f"{agentic_correct / total * 100:.1f}% | Agentic got it right |",
        f"| Both correct | {both_correct}/{total} | "
        f"{both_correct / total * 100:.1f}% | Same meaning, different wording |",
        f"| Neither correct | {neither}/{total} | "
        f"{neither / total * 100:.1f}% | Both methods got it wrong |",
        "",
        "Note: Google + Agentic percentages can exceed 100% since 'both correct' "
        "counts for each method.",
        "",
        "## Exclusive Wins",
        "",
        f"- **Google-only correct**: {google_only} fields ({google_only / total * 100:.1f}%)",
        f"- **Agentic-only correct**: {agentic_only} fields ({agentic_only / total * 100:.1f}%)",
        "",
        "## Per-Company Breakdown",
        "",
        "| Company | Total | Google % | Agentic % | Both | Neither |",
        "|---------|-------|----------|-----------|------|---------|",
    ]

    for company, company_fields in sorted(by_company.items()):
        ct = len(company_fields)
        c = Counter(f["correct_source"] for f in company_fields)
        gc = c.get("google", 0) + c.get("both", 0)
        ac = c.get("agentic", 0) + c.get("both", 0)
        lines.append(
            f"| {company} | {ct} | {gc / ct * 100:.1f}% | "
            f"{ac / ct * 100:.1f}% | {c.get('both', 0)} | {c.get('neither', 0)} |"
        )

    # Error details by source
    for source_label, source_key in [
        ("Google got wrong (Agentic was right)", "agentic"),
        ("Agentic got wrong (Google was right)", "google"),
        ("Both got wrong", "neither"),
    ]:
        source_fields = [f for f in fields if f["correct_source"] == source_key]
        if source_fields:
            lines.extend([
                "",
                f"## {source_label} ({len(source_fields)} fields)",
                "",
            ])
            for f in source_fields:
                notes = f.get("verification_notes", "")[:100]
                lines.append(
                    f"- **{f['company_code']} {f['company_name']}** "
                    f"Field {f['field_id']} ({f['field_name']}): "
                    f"verified=`{str(f.get('verified_value', ''))[:60]}` — {notes}"
                )

    content = "\n".join(lines) + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    setup_logging(session_name="pdf_verification_report")
    logger = get_logger()

    if not RESULTS_DIR.exists() or not list(RESULTS_DIR.glob("*_verified.json")):
        logger.error(f"No verification results found in {RESULTS_DIR}")
        logger.error("Run PDF verification agents first.")
        sys.exit(1)

    fields = load_verification_results(RESULTS_DIR)
    logger.info(f"Total verified fields: {len(fields)}")

    # Write outputs
    verified_csv = VERIFICATION_DIR / "verified_comparison.csv"
    write_verified_csv(fields, verified_csv)
    logger.info(f"Written: {verified_csv}")

    accuracy_csv = VERIFICATION_DIR / "accuracy_report.csv"
    write_accuracy_csv(fields, accuracy_csv)
    logger.info(f"Written: {accuracy_csv}")

    summary_path = VERIFICATION_DIR / "verification_summary.md"
    write_summary_markdown(fields, summary_path)
    logger.info(f"Written: {summary_path}")

    # Console summary
    total = len(fields)
    cc = Counter(f["correct_source"] for f in fields)
    google_correct = cc.get("google", 0) + cc.get("both", 0)
    agentic_correct = cc.get("agentic", 0) + cc.get("both", 0)

    print(f"\n{'='*60}")
    print("PDF VERIFICATION RESULTS")
    print(f"{'='*60}")
    print(f"Total discrepancies verified: {total}")
    print(f"Google API correct:           {google_correct}/{total} ({google_correct / total * 100:.1f}%)")
    print(f"Agentic Workflow correct:     {agentic_correct}/{total} ({agentic_correct / total * 100:.1f}%)")
    print(f"Both correct:                 {cc.get('both', 0)}/{total}")
    print(f"Neither correct:              {cc.get('neither', 0)}/{total}")
    print(f"{'='*60}")
    print(f"\nFull report: {summary_path}")


if __name__ == "__main__":
    main()
