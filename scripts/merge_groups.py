#!/usr/bin/env python3
"""
Merge all group JSON results for a company into a single CSV.
Optionally push the merged data to the local xlsx spreadsheet.

Usage:
    python scripts/merge_groups.py 2330 2024
    python scripts/merge_groups.py 2330 2024 --write-sheets
    python scripts/merge_groups.py 2330 2024 --write-sheets --tab-name "2330合併結果"
    python scripts/merge_groups.py 2330 2024 --results-dir /path/to/results
"""

import sys
import csv
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR, OUTPUT_SHEET_NAME
from src.utils import setup_logging, get_logger
from src.xlsx_manager import XlsxManager

# Results directory where group JSON files are stored
RESULTS_DIR = Path(OUTPUT_DIR) / "results"

# Column order matching xlsx output format (same as XlsxManager)
SHEET_HEADERS = [
    "西元年份",
    "公司代碼",
    "公司簡稱",
    "欄位編號",
    "欄位名稱",
    "欄位數值",
    "欄位單位",
    "補充說明",
    "參考頁數",
    "處理時間",
]


def find_group_files(
    results_dir: Path,
    company_code: str,
    year: str,
) -> list[tuple[str, Path]]:
    """
    Find all group JSON files for a company/year pair.

    Matches files with the pattern: {company_code}_{year}_group_{label}.json

    Args:
        results_dir: Directory to search.
        company_code: Company stock code to match.
        year: Report year to match.

    Returns:
        List of (group_label, file_path) tuples, sorted by group label.
    """
    import re

    logger = get_logger()
    pattern = re.compile(
        rf"^{re.escape(company_code)}_{re.escape(year)}_group_(.+)\.json$",
        re.IGNORECASE,
    )

    results = []
    if not results_dir.exists():
        logger.warning(f"Results directory not found: {results_dir}")
        return results

    for json_file in sorted(results_dir.glob(f"{company_code}_{year}_group_*.json")):
        match = pattern.match(json_file.name)
        if match:
            group_label = match.group(1)
            results.append((group_label, json_file))
            logger.debug(f"Found group file: {json_file.name}")

    return results


def load_group_file(
    json_path: Path,
) -> tuple[Optional[dict], Optional[str]]:
    """
    Load a single group JSON file.

    Args:
        json_path: Path to the JSON file.

    Returns:
        Tuple of (data_dict, error_message). error_message is None on success.
    """
    try:
        with open(json_path, encoding="utf-8") as fh:
            data = json.load(fh)

        if not isinstance(data.get("fields"), list):
            return None, f"'fields' is not a list in {json_path.name}"

        return data, None
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error in {json_path.name}: {exc}"
    except Exception as exc:
        return None, f"Failed to read {json_path.name}: {exc}"


def convert_field_to_row(
    field: dict,
    company_code: str,
    company_name: str,
    year: str,
    processed_at: str,
) -> list[str]:
    """
    Convert a single field dict to a sheet row list.

    Args:
        field: Field dict with keys: field_id, field_name, value, unit, notes, page_refs.
        company_code: Company stock code.
        company_name: Company short name.
        year: Report year.
        processed_at: ISO timestamp string.

    Returns:
        List of string values matching SHEET_HEADERS order.
    """
    return [
        year,                                           # 西元年份
        company_code,                                   # 公司代碼
        company_name,                                   # 公司簡稱
        str(field.get("field_id", "")).strip(),         # 欄位編號
        str(field.get("field_name", "")).strip(),       # 欄位名稱
        str(field.get("value", "")).strip(),            # 欄位數值
        str(field.get("unit", "")).strip(),             # 欄位單位
        str(field.get("notes", "")).strip(),            # 補充說明
        str(field.get("page_refs", "")).strip(),        # 參考頁數
        processed_at,                                   # 處理時間
    ]


def merge_group_files(
    group_files: list[tuple[str, Path]],
) -> tuple[list[list[str]], dict]:
    """
    Load and merge all group JSON files into a flat list of rows.

    Duplicate field_ids across groups are allowed (the last group wins when
    deduplication is used, but here we preserve all rows).

    Args:
        group_files: List of (group_label, file_path) from find_group_files.

    Returns:
        Tuple of:
            - all_rows: Flat list of sheet rows (list of lists).
            - stats: Dict with keys: groups_loaded, groups_failed, total_fields,
                     company_code, company_name, year, failed_groups, loaded_groups.
    """
    logger = get_logger()
    all_rows: list[list[str]] = []
    stats = {
        "groups_loaded": 0,
        "groups_failed": 0,
        "total_fields": 0,
        "company_code": "",
        "company_name": "",
        "year": "",
        "loaded_groups": [],
        "failed_groups": [],
    }

    for group_label, json_path in group_files:
        data, error = load_group_file(json_path)
        if error:
            logger.error(f"Skipping group '{group_label}': {error}")
            stats["groups_failed"] += 1
            stats["failed_groups"].append(group_label)
            continue

        company_code = str(data.get("company_code", "")).strip()
        company_name = str(data.get("company_name", "")).strip()
        year = str(data.get("year", "")).strip()
        processed_at = data.get("processed_at") or datetime.now().isoformat()

        # Capture metadata from first valid group
        if not stats["company_code"]:
            stats["company_code"] = company_code
            stats["company_name"] = company_name
            stats["year"] = year

        fields = data.get("fields", [])
        group_rows = [
            convert_field_to_row(f, company_code, company_name, year, processed_at)
            for f in fields
        ]
        all_rows.extend(group_rows)
        stats["groups_loaded"] += 1
        stats["total_fields"] += len(fields)
        stats["loaded_groups"].append(group_label)
        logger.info(
            f"Loaded group '{group_label}': {len(fields)} fields from {json_path.name}"
        )

    return all_rows, stats


def write_combined_csv(
    rows: list[list[str]],
    company_code: str,
    year: str,
    output_dir: Path,
) -> str:
    """
    Write merged rows to a single combined CSV file.

    Output filename: {company_code}_{year}_combined.csv

    Args:
        rows: List of sheet rows to write.
        company_code: Company stock code.
        year: Report year.
        output_dir: Directory to write the CSV into.

    Returns:
        Absolute path to the written CSV file.
    """
    logger = get_logger()
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / f"{company_code}_{year}_combined.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(SHEET_HEADERS)
        writer.writerows(rows)

    logger.info(f"Combined CSV written: {csv_path} ({len(rows)} rows)")
    return str(csv_path)


def determine_missing_groups(
    expected_groups: Optional[list[str]],
    found_groups: list[str],
) -> list[str]:
    """
    Determine which expected groups are missing from found groups.

    If no expected_groups provided, uses a heuristic based on the last loaded
    group label to guess the expected set (a-z sequence).

    Args:
        expected_groups: Explicit list of expected group labels, or None.
        found_groups: List of group labels that were successfully loaded.

    Returns:
        List of missing group labels.
    """
    if expected_groups:
        return [g for g in expected_groups if g not in found_groups]

    # Heuristic: if groups are single letters, infer the expected set
    # from the last letter found
    if not found_groups:
        return []

    single_letter_groups = [g for g in found_groups if len(g) == 1 and g.isalpha()]
    if len(single_letter_groups) == len(found_groups) and single_letter_groups:
        last_letter = max(single_letter_groups)
        expected = [chr(c) for c in range(ord("a"), ord(last_letter) + 1)]
        return [g for g in expected if g not in found_groups]

    return []


def main() -> None:
    """Main entry point for merge_groups script."""
    parser = argparse.ArgumentParser(
        description="Merge all group JSON results for a company into a single CSV"
    )
    parser.add_argument(
        "company_code",
        type=str,
        help="Company stock code (e.g. 2330)",
    )
    parser.add_argument(
        "year",
        type=str,
        help="Report year (e.g. 2024)",
    )
    parser.add_argument(
        "--write-sheets",
        "-s",
        action="store_true",
        help="Also push merged results to the local xlsx spreadsheet",
    )
    parser.add_argument(
        "--tab-name",
        "-t",
        type=str,
        default=None,
        help=f"xlsx tab name for --write-sheets (default: {OUTPUT_SHEET_NAME})",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=str(RESULTS_DIR),
        help=f"Directory containing group JSON files (default: {RESULTS_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUTPUT_DIR),
        help=f"Directory for the merged CSV output (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--expected-groups",
        "-e",
        type=str,
        nargs="+",
        default=None,
        help="Expected group labels (e.g. a b c). Used to report missing groups.",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Preview merge without writing any files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        stream=sys.stderr,
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    setup_logging(session_name="merge_groups")
    logger = get_logger()

    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    company_code = args.company_code.strip()
    year = args.year.strip()

    # 1. Find all group files for this company/year
    group_files = find_group_files(results_dir, company_code, year)

    if not group_files:
        logger.error(
            f"No group JSON files found for {company_code} {year} in {results_dir}"
        )
        print(
            f"Error: No group files matching '{company_code}_{year}_group_*.json' "
            f"found in {results_dir}"
        )
        sys.exit(1)

    logger.info(f"Found {len(group_files)} group file(s) for {company_code} {year}")

    # 2. Report which groups are found and which may be missing
    found_group_labels = [label for label, _ in group_files]
    missing_groups = determine_missing_groups(args.expected_groups, found_group_labels)

    print(f"\n{'='*60}")
    print(f"Merge Groups: {company_code} / {year}")
    print(f"{'='*60}")
    print(f"Results directory: {results_dir}")
    print(f"Groups found ({len(group_files)}): {', '.join(found_group_labels)}")

    if missing_groups:
        print(f"Groups MISSING ({len(missing_groups)}): {', '.join(missing_groups)}")
    else:
        print("Groups missing: (none detected)")

    # 3. Merge group files
    all_rows, stats = merge_group_files(group_files)

    print(f"\nMerge results:")
    print(f"  Groups successfully loaded: {stats['groups_loaded']}")
    if stats["failed_groups"]:
        print(f"  Groups failed to load:     {stats['groups_failed']} -> {stats['failed_groups']}")
    print(f"  Total fields (rows):       {stats['total_fields']}")

    if args.dry_run:
        print(f"\n[DRY RUN] Would write {len(all_rows)} rows to:")
        print(f"  CSV: {output_dir / f'{company_code}_{year}_combined.csv'}")
        if args.write_sheets:
            print(f"  Sheets tab: '{args.tab_name or OUTPUT_SHEET_NAME}'")
        print("\nFirst 3 rows preview:")
        for i, row in enumerate(all_rows[:3]):
            print(f"  [{i + 1}] {row}")
        sys.exit(0)

    if not all_rows:
        logger.error("No rows to write after merging all groups")
        print("\nError: Nothing to merge. All group files may have failed to load.")
        sys.exit(1)

    errors: list[str] = []

    # 4. Write combined CSV
    try:
        csv_path = write_combined_csv(all_rows, company_code, year, output_dir)
        print(f"\nCombined CSV written: {csv_path}")
    except Exception as exc:
        msg = f"Failed to write combined CSV: {exc}"
        logger.error(msg)
        errors.append(msg)
        csv_path = None

    # 5. Optionally write to xlsx
    xlsx_written = 0
    if args.write_sheets:
        try:
            manager = XlsxManager()
            target_tab = args.tab_name or OUTPUT_SHEET_NAME
            xlsx_written = manager.append_rows_to_tab(
                target_tab, SHEET_HEADERS, all_rows
            )
            print(
                f"xlsx written: {xlsx_written} rows -> "
                f"tab '{target_tab}'"
            )
        except Exception as exc:
            msg = f"Failed to write to xlsx: {exc}"
            logger.error(msg)
            errors.append(msg)

    # 6. Final summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"Company:          {stats['company_name']} ({company_code})")
    print(f"Year:             {year}")
    print(f"Groups merged:    {stats['groups_loaded']}")
    print(f"Total rows:       {len(all_rows)}")
    if csv_path:
        print(f"Output CSV:       {csv_path}")
    if args.write_sheets:
        print(f"xlsx rows:        {xlsx_written}")
    if missing_groups:
        print(f"Missing groups:   {', '.join(missing_groups)} (data may be incomplete)")
    if stats["failed_groups"]:
        print(f"Failed groups:    {', '.join(stats['failed_groups'])}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    print(f"{'='*60}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
