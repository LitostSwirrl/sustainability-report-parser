#!/usr/bin/env python3
"""
Check extraction progress across Claude Code sessions.
Reads output/results/ directory and the local xlsx spreadsheet to show status.

Usage:
    python scripts/check_progress.py
    python scripts/check_progress.py --year 2024
    python scripts/check_progress.py --company 2330
    python scripts/check_progress.py --format json
"""

import sys
import re
import json
import argparse
import logging
from pathlib import Path
from typing import Optional
from collections import defaultdict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR
from src.utils import setup_logging, get_logger
from src.xlsx_manager import XlsxManager

# Where group JSON results are stored
RESULTS_DIR = Path(OUTPUT_DIR) / "results"

# Pattern for group result filenames: {code}_{year}_group_{label}.json
# label can be letters (a, b, c) or longer identifiers (group_1, group_2)
RESULT_FILENAME_RE = re.compile(
    r"^(?P<code>[^_]+)_(?P<year>\d{4})_group_(?P<group>.+)\.json$",
    re.IGNORECASE,
)


def scan_result_files(
    results_dir: Path,
    company_filter: Optional[str] = None,
    year_filter: Optional[str] = None,
) -> dict[tuple[str, str], list[str]]:
    """
    Scan the results directory for group JSON files.

    Args:
        results_dir: Path to the results directory.
        company_filter: Optional company code to restrict scan.
        year_filter: Optional year string to restrict scan.

    Returns:
        Dict mapping (company_code, year) -> list of group labels found.
    """
    logger = get_logger()
    found: dict[tuple[str, str], list[str]] = defaultdict(list)

    if not results_dir.exists():
        logger.warning(f"Results directory does not exist: {results_dir}")
        return found

    for json_file in sorted(results_dir.glob("*.json")):
        match = RESULT_FILENAME_RE.match(json_file.name)
        if not match:
            logger.debug(f"Skipping unrecognised filename: {json_file.name}")
            continue

        code = match.group("code")
        year = match.group("year")
        group = match.group("group")

        if company_filter and code != company_filter:
            continue
        if year_filter and year != year_filter:
            continue

        found[(code, year)].append(group)

    return found


def read_group_json_summary(json_path: Path) -> dict:
    """
    Read a group JSON file and return a lightweight summary.

    Args:
        json_path: Path to the group JSON file.

    Returns:
        Dict with keys: field_count, processed_at, has_errors.
    """
    try:
        with open(json_path, encoding="utf-8") as fh:
            data = json.load(fh)
        fields = data.get("fields", [])
        field_count = len(fields)
        # Detect any field where value indicates failure
        has_errors = any(
            "解析失敗" in str(f.get("value", "")) or
            "解析失敗" in str(f.get("notes", ""))
            for f in fields
        )
        return {
            "field_count": field_count,
            "processed_at": data.get("processed_at", ""),
            "has_errors": has_errors,
        }
    except Exception:
        return {"field_count": 0, "processed_at": "", "has_errors": True}


def build_progress_report(
    found: dict[tuple[str, str], list[str]],
    company_list: list[dict],
    results_dir: Path,
) -> list[dict]:
    """
    Cross-reference found result files with the company list to build a progress report.

    Args:
        found: Dict from scan_result_files - (code, year) -> [group labels].
        company_list: List of company dicts from Sheets or empty.
        results_dir: Path to results directory.

    Returns:
        List of progress dicts sorted by company_code, year.
    """
    # Build a lookup from the company list
    company_lookup: dict[tuple[str, str], dict] = {}
    for c in company_list:
        company_lookup[(c["company_code"], c["year"])] = c

    # Collect all (code, year) keys from both sources
    all_keys: set[tuple[str, str]] = set(found.keys()) | set(company_lookup.keys())

    rows = []
    for code, year in sorted(all_keys):
        groups_completed = sorted(found.get((code, year), []))
        company_info = company_lookup.get((code, year), {})

        # Gather per-group summaries
        group_summaries = []
        total_fields = 0
        any_errors = False
        for group in groups_completed:
            fname = f"{code}_{year}_group_{group}.json"
            fpath = results_dir / fname
            summary = read_group_json_summary(fpath)
            group_summaries.append(
                {
                    "group": group,
                    "field_count": summary["field_count"],
                    "processed_at": summary["processed_at"],
                    "has_errors": summary["has_errors"],
                }
            )
            total_fields += summary["field_count"]
            if summary["has_errors"]:
                any_errors = True

        in_company_list = (code, year) in company_lookup
        status: str
        if not groups_completed:
            status = "pending"
        elif any_errors:
            status = "completed_with_errors"
        else:
            status = "completed"

        rows.append(
            {
                "company_code": code,
                "company_name": company_info.get("company_name", ""),
                "industry": company_info.get("industry", ""),
                "year": year,
                "in_company_list": in_company_list,
                "groups_completed": groups_completed,
                "groups_completed_count": len(groups_completed),
                "total_fields_extracted": total_fields,
                "any_errors": any_errors,
                "status": status,
                "group_details": group_summaries,
            }
        )

    return rows


def format_table(rows: list[dict]) -> str:
    """
    Render a progress report as a human-readable table.

    Args:
        rows: List of progress dicts from build_progress_report.

    Returns:
        Multi-line string table.
    """
    if not rows:
        return "(no results found)"

    col = {
        "code": 8,
        "name": 12,
        "industry": 14,
        "year": 6,
        "groups": 20,
        "fields": 8,
        "status": 24,
    }
    header = (
        f"{'Code':<{col['code']}} "
        f"{'Name':<{col['name']}} "
        f"{'Industry':<{col['industry']}} "
        f"{'Year':<{col['year']}} "
        f"{'Groups Done':<{col['groups']}} "
        f"{'Fields':<{col['fields']}} "
        f"{'Status':<{col['status']}}"
    )
    sep = "-" * len(header)
    lines = [sep, header, sep]

    pending_count = 0
    completed_count = 0
    error_count = 0

    for r in rows:
        groups_str = ",".join(r["groups_completed"]) if r["groups_completed"] else "(none)"
        status = r["status"]
        if status == "pending":
            pending_count += 1
        elif status == "completed":
            completed_count += 1
        else:
            error_count += 1

        lines.append(
            f"{r['company_code']:<{col['code']}} "
            f"{r['company_name']:<{col['name']}} "
            f"{r['industry']:<{col['industry']}} "
            f"{r['year']:<{col['year']}} "
            f"{groups_str:<{col['groups']}} "
            f"{r['total_fields_extracted']:<{col['fields']}} "
            f"{status:<{col['status']}}"
        )

    lines.append(sep)
    lines.append(
        f"Total: {len(rows)} | Completed: {completed_count} | "
        f"Errors: {error_count} | Pending: {pending_count}"
    )
    return "\n".join(lines)


def main() -> None:
    """Main entry point for check_progress script."""
    parser = argparse.ArgumentParser(
        description="Check extraction progress across Claude Code sessions"
    )
    parser.add_argument(
        "--year",
        "-y",
        type=str,
        help="Filter by report year (e.g. 2024)",
    )
    parser.add_argument(
        "--company",
        "-c",
        type=str,
        help="Filter by company code (e.g. 2330)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["table", "json"],
        default="table",
        help="Output format: table (default, human-readable) or json",
    )
    parser.add_argument(
        "--no-sheets",
        action="store_true",
        help="Skip xlsx company list lookup (use local result files only)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=str(RESULTS_DIR),
        help=f"Path to results directory (default: {RESULTS_DIR})",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        stream=sys.stderr,
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    setup_logging(session_name="check_progress")
    logger = get_logger()

    results_dir = Path(args.results_dir)

    # 1. Scan local result files
    found = scan_result_files(
        results_dir,
        company_filter=args.company,
        year_filter=args.year,
    )
    logger.info(f"Found {len(found)} (company, year) pairs in {results_dir}")

    # 2. Optionally load company list from xlsx for cross-referencing
    company_list: list[dict] = []
    if not args.no_sheets:
        try:
            manager = XlsxManager()
            full_list = manager.get_company_list(
                filter_to_analyze=True,
                year=args.year,
            )
            # Map to the minimal shape expected by build_progress_report
            company_list = [
                {
                    "company_code": c["company_code"],
                    "company_name": c["company_name"],
                    "year": c["year"],
                    "industry": c["industry"],
                }
                for c in full_list
            ]
            if args.company:
                company_list = [c for c in company_list if c["company_code"] == args.company]
            logger.info(f"Loaded {len(company_list)} companies from xlsx")
        except (FileNotFoundError, ValueError) as exc:
            logger.warning(
                f"xlsx company list unavailable: {exc}. Cross-referencing skipped. "
                "Use --no-sheets to suppress this warning."
            )

    # 3. Build progress report
    rows = build_progress_report(found, company_list, results_dir)

    # 4. Output
    if args.format == "json":
        summary = {
            "results_dir": str(results_dir),
            "filters": {"year": args.year, "company": args.company},
            "total": len(rows),
            "completed": sum(1 for r in rows if r["status"] == "completed"),
            "completed_with_errors": sum(
                1 for r in rows if r["status"] == "completed_with_errors"
            ),
            "pending": sum(1 for r in rows if r["status"] == "pending"),
            "rows": rows,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_table(rows))
        print(f"\nResults directory: {results_dir}")
        if not company_list and not args.no_sheets:
            print(
                "Note: Company list from xlsx not available. "
                "Run with --no-sheets to suppress xlsx lookup."
            )


if __name__ == "__main__":
    main()
