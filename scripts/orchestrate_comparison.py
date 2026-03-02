#!/usr/bin/env python3
"""
Orchestrate Comparison — Orchestration Agent

Loads both CSV result files, identifies overlapping companies,
batches work by company, and runs the comparison engine + verification
reviewer pipeline. Writes all output files.

Usage:
    python scripts/orchestrate_comparison.py
    python scripts/orchestrate_comparison.py --company 1216
    python scripts/orchestrate_comparison.py --output output/comparison
"""

import csv
import sys
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import PROJECT_ROOT, OUTPUT_DIR
from src.utils import setup_logging, get_logger
from scripts.comparison_engine import (
    ComparisonRecord,
    DiscrepancyType,
    Severity,
    compare_company_batch,
)
from scripts.verification_reviewer import review_batch


# ── Default file paths ───────────────────────────────────────────────────

DEFAULT_GOOGLE_CSV = PROJECT_ROOT / "欄位蒐集結果 26-02-11（prompt ver. 5）.csv"
DEFAULT_AGENTIC_CSV = PROJECT_ROOT / "LLM 解析結果 - 欄位蒐集結果.csv"
DEFAULT_OUTPUT_DIR = OUTPUT_DIR / "comparison"


# ── CSV Loading ──────────────────────────────────────────────────────────


def load_csv(path: Path) -> list[dict]:
    """Load a CSV file into a list of dicts."""
    logger = get_logger()

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    logger.info(f"Loaded {len(rows)} rows from {path.name}")
    return rows


def group_by_company(rows: list[dict]) -> dict[str, list[dict]]:
    """Group rows by company code."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        code = row.get("公司代碼", "")
        if code:
            groups[code].append(row)
    return dict(groups)


def get_company_name(rows: list[dict]) -> str:
    """Get company name from a list of rows."""
    for row in rows:
        name = row.get("公司簡稱", "")
        if name:
            return name
    return ""


# ── Output Writers ───────────────────────────────────────────────────────


def write_comparison_csv(records: list[ComparisonRecord], path: Path) -> None:
    """Write comparison records to CSV."""
    if not records:
        get_logger().warning(f"No records to write to {path.name}, skipping")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(records[0].to_dict().keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())


def write_summary_markdown(
    all_records: list[ComparisonRecord],
    google_total: int,
    agentic_total: int,
    overlap_companies: list[str],
    only_google: list[str],
    only_agentic: list[str],
    output_path: Path,
) -> None:
    """Generate a human-readable summary in Markdown."""
    total = len(all_records)
    matches = [r for r in all_records if r.discrepancy_type == DiscrepancyType.MATCH]
    mismatches = [r for r in all_records if r.discrepancy_type != DiscrepancyType.MATCH]

    # Count by type
    type_counts: dict[str, int] = defaultdict(int)
    for r in mismatches:
        type_counts[r.discrepancy_type.value] += 1

    # Count by severity
    severity_counts: dict[str, int] = defaultdict(int)
    for r in mismatches:
        severity_counts[r.severity.value] += 1

    # Count recommendations
    rec_counts: dict[str, int] = defaultdict(int)
    for r in all_records:
        rec_counts[r.recommendation_source] += 1

    # Per-company stats
    company_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "match": 0, "mismatch": 0})
    for r in all_records:
        key = f"{r.company_code} {r.company_name}"
        company_stats[key]["total"] += 1
        if r.discrepancy_type == DiscrepancyType.MATCH:
            company_stats[key]["match"] += 1
        else:
            company_stats[key]["mismatch"] += 1

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# ESG Extraction Comparison Report",
        f"",
        f"Generated: {now}",
        f"",
        f"## Dataset Overview",
        f"",
        f"| Source | Rows | Companies |",
        f"|--------|------|-----------|",
        f"| Google API (prompt ver. 5) | {google_total} | {google_total // 80}+ |",
        f"| Agentic Workflow (Claude Code) | {agentic_total} | {agentic_total // 80}+ |",
        f"",
        f"**Overlapping companies**: {', '.join(overlap_companies)} ({len(overlap_companies)})",
        f"**Only in Google API**: {', '.join(only_google) if only_google else 'none'}",
        f"**Only in Agentic**: {', '.join(only_agentic) if only_agentic else 'none'}",
        f"",
        f"## Comparison Summary",
        f"",
        f"| Metric | Count | % |",
        f"|--------|-------|---|",
        f"| Total field pairs | {total} | 100% |",
        f"| Match | {len(matches)} | {len(matches)/total*100:.1f}% |",
        f"| Mismatch | {len(mismatches)} | {len(mismatches)/total*100:.1f}% |",
        f"",
        f"## Discrepancy Types",
        f"",
        f"| Type | Count | Description |",
        f"|------|-------|-------------|",
    ]

    type_descriptions = {
        "UNIT_CONVERSION": "GJ/MJ unit mismatch (x1000 factor)",
        "BOOLEAN_DIFF": "True/False/blank disagreement",
        "NUMERIC_DIFF": "Different numbers entirely",
        "TEXT_DIFF": "Different phrasing, possibly same meaning",
        "COVERAGE_GAP": "One has data, other is blank",
        "FORMAT_DIFF": "Same data, different format",
    }

    for dtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        desc = type_descriptions.get(dtype, "")
        lines.append(f"| {dtype} | {count} | {desc} |")

    lines.extend([
        f"",
        f"## Severity Distribution (mismatches only)",
        f"",
        f"| Severity | Count |",
        f"|----------|-------|",
    ])
    for sev in ["high", "medium", "low"]:
        lines.append(f"| {sev} | {severity_counts.get(sev, 0)} |")

    lines.extend([
        f"",
        f"## Recommendations",
        f"",
        f"| Source | Count | Meaning |",
        f"|--------|-------|---------|",
        f"| both | {rec_counts.get('both', 0)} | Values agree |",
        f"| google | {rec_counts.get('google', 0)} | Google API value preferred |",
        f"| agentic | {rec_counts.get('agentic', 0)} | Agentic workflow value preferred |",
        f"| human_review | {rec_counts.get('human_review', 0)} | Needs manual verification |",
        f"",
        f"## Per-Company Breakdown",
        f"",
        f"| Company | Total | Match | Mismatch | Match Rate |",
        f"|---------|-------|-------|----------|------------|",
    ])

    for company, stats in sorted(company_stats.items()):
        rate = stats["match"] / stats["total"] * 100 if stats["total"] else 0
        lines.append(
            f"| {company} | {stats['total']} | {stats['match']} | "
            f"{stats['mismatch']} | {rate:.1f}% |"
        )

    # High-severity items
    high_severity = [r for r in mismatches if r.severity == Severity.HIGH]
    if high_severity:
        lines.extend([
            f"",
            f"## High-Severity Discrepancies ({len(high_severity)} items)",
            f"",
        ])
        for r in high_severity[:30]:
            lines.append(
                f"- **{r.company_code} {r.company_name}** Field {r.field_id} "
                f"({r.field_name}): {r.discrepancy_type.value} — "
                f"Google=`{r.google_value[:50]}` vs Agentic=`{r.agentic_value[:50]}`"
            )
        if len(high_severity) > 30:
            lines.append(f"- ... and {len(high_severity) - 30} more")

    content = "\n".join(lines) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Main Pipeline ────────────────────────────────────────────────────────


def run_pipeline(
    google_csv: Path,
    agentic_csv: Path,
    output_dir: Path,
    target_company: str | None = None,
) -> list[ComparisonRecord]:
    """
    Run the full comparison pipeline.

    1. Load CSVs
    2. Find overlapping companies
    3. Compare field-by-field per company (comparison engine)
    4. Review discrepancies (verification reviewer)
    5. Write outputs
    """
    logger = get_logger()

    # ── Step 1: Load ──
    logger.info("Loading CSV files...")
    google_rows = load_csv(google_csv)
    agentic_rows = load_csv(agentic_csv)

    # ── Step 2: Find overlap ──
    google_by_co = group_by_company(google_rows)
    agentic_by_co = group_by_company(agentic_rows)

    google_codes = set(google_by_co.keys())
    agentic_codes = set(agentic_by_co.keys())
    overlap_codes = sorted(google_codes & agentic_codes)
    only_google_codes = sorted(google_codes - agentic_codes)
    only_agentic_codes = sorted(agentic_codes - google_codes)

    logger.info(
        f"Overlap: {len(overlap_codes)} companies ({', '.join(overlap_codes)}), "
        f"Only Google: {len(only_google_codes)}, Only Agentic: {len(only_agentic_codes)}"
    )

    # Filter if specific company requested
    if target_company:
        if target_company not in overlap_codes:
            logger.error(f"Company {target_company} not in overlap set: {overlap_codes}")
            sys.exit(1)
        overlap_codes = [target_company]

    # ── Step 3 & 4: Compare + Review per company ──
    all_records: list[ComparisonRecord] = []
    per_company_dir = output_dir / "per_company"
    per_company_dir.mkdir(parents=True, exist_ok=True)

    for code in overlap_codes:
        g_rows = google_by_co[code]
        a_rows = agentic_by_co[code]
        company_name = get_company_name(g_rows) or get_company_name(a_rows)

        logger.info(f"Processing {code} {company_name}...")

        # Comparison engine
        records = compare_company_batch(code, company_name, g_rows, a_rows)

        # Verification reviewer
        records = review_batch(records)

        # Write per-company CSV
        company_csv = per_company_dir / f"{code}_{company_name}_comparison.csv"
        write_comparison_csv(records, company_csv)
        logger.info(f"  Written: {company_csv}")

        all_records.extend(records)

    # ── Step 5: Write aggregated outputs ──
    output_dir.mkdir(parents=True, exist_ok=True)

    # Full detail CSV
    detail_path = output_dir / "comparison_detail.csv"
    write_comparison_csv(all_records, detail_path)
    logger.info(f"Written: {detail_path}")

    # Discrepancies only
    discrepancies = [r for r in all_records if r.discrepancy_type != DiscrepancyType.MATCH]
    disc_path = output_dir / "discrepancies_only.csv"
    write_comparison_csv(discrepancies, disc_path)
    logger.info(f"Written: {disc_path} ({len(discrepancies)} records)")

    # Verification report (same as detail but focused on recommendations)
    report_path = output_dir / "verification_report.csv"
    write_comparison_csv(all_records, report_path)
    logger.info(f"Written: {report_path}")

    # Summary markdown
    # Build overlap labels with names
    overlap_labels = []
    for code in overlap_codes:
        name = get_company_name(google_by_co.get(code, []) or agentic_by_co.get(code, []))
        overlap_labels.append(f"{code} {name}")

    summary_path = output_dir / "summary.md"
    write_summary_markdown(
        all_records=all_records,
        google_total=len(google_rows),
        agentic_total=len(agentic_rows),
        overlap_companies=overlap_labels,
        only_google=only_google_codes,
        only_agentic=only_agentic_codes,
        output_path=summary_path,
    )
    logger.info(f"Written: {summary_path}")

    return all_records


# ── Console Summary ──────────────────────────────────────────────────────


def print_console_summary(records: list[ComparisonRecord]) -> None:
    """Print a compact summary to the console."""
    total = len(records)
    if total == 0:
        print("\nNo records to compare.")
        return

    matches = sum(1 for r in records if r.discrepancy_type == DiscrepancyType.MATCH)
    mismatches = total - matches

    print(f"\n{'='*60}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*60}")
    print(f"Total field pairs:   {total}")
    print(f"Matches:             {matches} ({matches/total*100:.1f}%)")
    print(f"Mismatches:          {mismatches} ({mismatches/total*100:.1f}%)")

    # By type
    type_counts: dict[str, int] = defaultdict(int)
    for r in records:
        if r.discrepancy_type != DiscrepancyType.MATCH:
            type_counts[r.discrepancy_type.value] += 1

    if type_counts:
        print(f"\nDiscrepancy breakdown:")
        for dtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {dtype:20s}  {count:3d}")

    # Recommendations
    rec_counts: dict[str, int] = defaultdict(int)
    for r in records:
        if r.discrepancy_type != DiscrepancyType.MATCH:
            rec_counts[r.recommendation_source] += 1

    if rec_counts:
        print(f"\nRecommendations for mismatches:")
        for src, count in sorted(rec_counts.items(), key=lambda x: -x[1]):
            print(f"  {src:20s}  {count:3d}")

    print(f"{'='*60}")


# ── CLI ──────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Compare ESG extraction results: Google API vs Agentic Workflow"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Compare specific company only (stock code)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output directory (default: output/comparison)"
    )
    parser.add_argument(
        "--google-csv",
        type=str,
        help="Path to Google API results CSV"
    )
    parser.add_argument(
        "--agentic-csv",
        type=str,
        help="Path to Agentic workflow results CSV"
    )

    args = parser.parse_args()

    setup_logging(session_name="comparison")
    logger = get_logger()

    google_csv = Path(args.google_csv) if args.google_csv else DEFAULT_GOOGLE_CSV
    agentic_csv = Path(args.agentic_csv) if args.agentic_csv else DEFAULT_AGENTIC_CSV
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR

    # Validate inputs
    for csv_path in [google_csv, agentic_csv]:
        if not csv_path.exists():
            logger.error(f"CSV file not found: {csv_path}")
            sys.exit(1)

    logger.info(f"Google CSV:  {google_csv}")
    logger.info(f"Agentic CSV: {agentic_csv}")
    logger.info(f"Output dir:  {output_dir}")

    # Run pipeline
    records = run_pipeline(
        google_csv=google_csv,
        agentic_csv=agentic_csv,
        output_dir=output_dir,
        target_company=args.company,
    )

    # Console summary
    print_console_summary(records)

    print(f"\nOutput files written to: {output_dir}/")
    print(f"  - comparison_detail.csv    (all {len(records)} field pairs)")
    disc_count = sum(1 for r in records if r.discrepancy_type != DiscrepancyType.MATCH)
    print(f"  - discrepancies_only.csv   ({disc_count} mismatches)")
    print(f"  - verification_report.csv  (with recommendations)")
    print(f"  - summary.md               (human-readable report)")
    print(f"  - per_company/             (per-company breakdowns)")


if __name__ == "__main__":
    main()
