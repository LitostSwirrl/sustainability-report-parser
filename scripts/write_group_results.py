#!/usr/bin/env python3
"""
Write extraction results from a group JSON file to the local xlsx and CSV backup.

Usage:
    python scripts/write_group_results.py output/results/2330_2024_group_a.json
    python scripts/write_group_results.py output/results/2330_2024_group_a.json --dry-run
    python scripts/write_group_results.py output/results/2330_2024_group_a.json --tab-name "2024結果"
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

# Expected output column order matching XlsxManager.append_rows_to_tab
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


def load_group_json(json_path: Path) -> dict:
    """
    Load and validate a group JSON file.

    Expected top-level keys:
        company_code, company_name, year, group, fields, processed_at

    Args:
        json_path: Path to the group JSON file.

    Returns:
        Parsed dict.

    Raises:
        ValueError: If required keys are missing or fields is not a list.
        FileNotFoundError: If the file does not exist.
    """
    if not json_path.exists():
        raise FileNotFoundError(f"Group JSON file not found: {json_path}")

    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)

    required_keys = {"company_code", "company_name", "year", "group", "fields"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(
            f"Group JSON is missing required keys: {sorted(missing)}"
        )

    if not isinstance(data["fields"], list):
        raise ValueError("'fields' must be a list in the group JSON")

    return data


def convert_fields_to_sheet_rows(
    data: dict,
    processed_at: Optional[str] = None,
) -> list[list[str]]:
    """
    Convert group JSON data into rows matching the xlsx output column order.

    Args:
        data: Parsed group JSON dict.
        processed_at: Timestamp string to use for 處理時間. Defaults to now.

    Returns:
        List of rows, each row is a list of strings aligned to SHEET_HEADERS.
    """
    timestamp = processed_at or data.get("processed_at") or datetime.now().isoformat()
    company_code = str(data["company_code"]).strip()
    company_name = str(data["company_name"]).strip()
    year = str(data["year"]).strip()

    rows = []
    for field in data["fields"]:
        row = [
            year,                                           # 西元年份
            company_code,                                   # 公司代碼
            company_name,                                   # 公司簡稱
            str(field.get("field_id", "")).strip(),         # 欄位編號
            str(field.get("field_name", "")).strip(),       # 欄位名稱
            str(field.get("value", "")).strip(),            # 欄位數值
            str(field.get("unit", "")).strip(),             # 欄位單位
            str(field.get("notes", "")).strip(),            # 補充說明
            str(field.get("page_refs", "")).strip(),        # 參考頁數
            timestamp,                                      # 處理時間
        ]
        rows.append(row)

    return rows


def write_to_csv(
    rows: list[list[str]],
    company_code: str,
    company_name: str,
    year: str,
    group: str,
) -> tuple[str, str]:
    """
    Save rows to a per-group CSV and append to the combined results CSV.

    File locations:
        Per-group:  output/{code}_{name}_{year}_group_{group}.csv
        Combined:   output/combined_results.csv

    Args:
        rows: List of row lists to write.
        company_code: Company stock code.
        company_name: Company short name.
        year: Report year.
        group: Group label (e.g. "a", "b").

    Returns:
        Tuple of (per_group_csv_path, combined_csv_path).
    """
    logger = get_logger()
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Per-group CSV
    group_csv = output_dir / f"{company_code}_{company_name}_{year}_group_{group}.csv"
    with open(group_csv, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(SHEET_HEADERS)
        writer.writerows(rows)
    logger.info(f"Per-group CSV saved: {group_csv}")

    # Combined CSV (append)
    combined_csv = output_dir / "combined_results.csv"
    write_header = not combined_csv.exists()
    with open(combined_csv, "a", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        if write_header:
            writer.writerow(SHEET_HEADERS)
        writer.writerows(rows)
    logger.info(f"Combined CSV updated: {combined_csv}")

    return str(group_csv), str(combined_csv)


def preview_rows(rows: list[list[str]], max_rows: int = 5) -> None:
    """
    Print a preview of the rows that would be written (for --dry-run).

    Args:
        rows: List of row lists.
        max_rows: Maximum rows to display.
    """
    print(f"\n[DRY RUN] Would write {len(rows)} rows to xlsx and CSV.")
    print(f"Headers: {SHEET_HEADERS}")
    print(f"\nFirst {min(max_rows, len(rows))} rows:")
    for i, row in enumerate(rows[:max_rows]):
        print(f"  [{i + 1}] {row}")
    if len(rows) > max_rows:
        print(f"  ... and {len(rows) - max_rows} more rows")


def main() -> None:
    """Main entry point for write_group_results script."""
    parser = argparse.ArgumentParser(
        description="Write group JSON extraction results to xlsx and CSV"
    )
    parser.add_argument(
        "json_file",
        type=str,
        help="Path to the group JSON file (e.g. output/results/2330_2024_group_a.json)",
    )
    parser.add_argument(
        "--tab-name",
        "-t",
        type=str,
        default=None,
        help=f"xlsx tab name (default: {OUTPUT_SHEET_NAME})",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Preview rows without writing to Sheets or CSV",
    )
    parser.add_argument(
        "--no-sheets",
        action="store_true",
        help="Skip xlsx write; only write the CSV backup",
    )
    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Skip CSV backup; only write to xlsx",
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
    setup_logging(session_name="write_group_results")
    logger = get_logger()

    json_path = Path(args.json_file)

    # Load and validate the JSON
    try:
        data = load_group_json(json_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        logger.error(f"Failed to load group JSON: {exc}")
        sys.exit(1)

    company_code = str(data["company_code"]).strip()
    company_name = str(data["company_name"]).strip()
    year = str(data["year"]).strip()
    group = str(data["group"]).strip()
    field_count = len(data["fields"])

    logger.info(
        f"Loaded group JSON: {company_code} {company_name} {year} "
        f"group={group}, {field_count} fields"
    )

    # Convert to sheet rows
    rows = convert_fields_to_sheet_rows(data)

    if args.dry_run:
        preview_rows(rows)
        print(
            f"\nTarget tab: {args.tab_name or OUTPUT_SHEET_NAME}"
        )
        print(f"JSON source: {json_path}")
        sys.exit(0)

    if not rows:
        logger.warning("No fields found in group JSON. Nothing to write.")
        sys.exit(0)

    xlsx_written = 0
    csv_written = False
    errors: list[str] = []

    # Write to xlsx
    if not args.no_sheets:
        try:
            manager = XlsxManager()
            target_tab = args.tab_name or OUTPUT_SHEET_NAME
            xlsx_written = manager.append_rows_to_tab(target_tab, SHEET_HEADERS, rows)
        except Exception as exc:
            msg = f"Failed to write to xlsx: {exc}"
            logger.error(msg)
            errors.append(msg)

    # Write to CSV backup
    if not args.no_csv:
        try:
            group_csv, combined_csv = write_to_csv(
                rows, company_code, company_name, year, group
            )
            csv_written = True
        except Exception as exc:
            msg = f"Failed to write CSV: {exc}"
            logger.error(msg)
            errors.append(msg)
    else:
        group_csv = "(skipped)"
        combined_csv = "(skipped)"

    # Summary output
    print(f"\n{'='*60}")
    print("Write Group Results - Summary")
    print(f"{'='*60}")
    print(f"Source file:    {json_path}")
    print(f"Company:        {company_name} ({company_code})")
    print(f"Year:           {year}")
    print(f"Group:          {group}")
    print(f"Fields:         {field_count}")
    print(f"Rows prepared:  {len(rows)}")
    if not args.no_sheets:
        print(f"xlsx written:   {xlsx_written} rows -> tab '{args.tab_name or OUTPUT_SHEET_NAME}'")
    if not args.no_csv and csv_written:
        print(f"CSV (per-group):  {group_csv}")
        print(f"CSV (combined):   {combined_csv}")
    if errors:
        print(f"\nWarnings/Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    print(f"{'='*60}")

    if errors and xlsx_written == 0 and not csv_written:
        sys.exit(1)


if __name__ == "__main__":
    main()
