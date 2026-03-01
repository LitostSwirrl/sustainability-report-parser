#!/usr/bin/env python3
"""
Fill 檢查欄 (columns L:P) in Google Sheets with assessment results.

Reads comparison_report.csv and updates the Google Sheet with:
- L: 答案正確性 (0%, 25%, 50%, 75%, 100%) - intelligent assessment
- M: 正確數值 - the most common value from multiple runs
- N: 判斷說明/備註 - explains why answer matches or doesn't match original
- O: 實際參考頁數 - the most consistent page reference
- P: 參考頁數正確 - TRUE or empty

Usage:
    python scripts/fill_review_columns.py
    python scripts/fill_review_columns.py --dry-run
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from src.config import OUTPUT_SHEET_ID
from src.utils import setup_logging, get_logger

# Sheet name for the validation results (gid=12346745)
VALIDATION_SHEET_NAME = "欄位蒐集結果 26-01-30（prompt ver. 0)"


def setup_google_auth() -> gspread.Client:
    """Setup Google Sheets authentication."""
    import os
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    creds_path = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS',
        Path(__file__).parent.parent / 'credentials.json'
    )
    if not Path(creds_path).exists():
        raise FileNotFoundError(f"Google credentials not found at {creds_path}")
    creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
    return gspread.authorize(creds)


def load_comparison_report(validation_dir: Path) -> pd.DataFrame:
    """Load comparison report CSV."""
    report_path = validation_dir / "comparison_report.csv"

    if not report_path.exists():
        raise FileNotFoundError(
            f"Comparison report not found: {report_path}\n"
            "Please run compare_results.py first"
        )

    return pd.read_csv(report_path)


def get_sheet_row_mapping(worksheet) -> dict:
    """
    Create mapping of (company_code, field_id) -> row_number.

    Note: This sheet has row 1 as instructions, row 2 as headers, data starts at row 3.

    Returns:
        Dict mapping (code, field_id) to 1-based row number
    """
    logger = get_logger()

    # Get all data (skip first row which is instructions)
    # Row 2 is headers, data starts at row 3
    all_values = worksheet.get_all_values()

    # Row 2 (index 1) is headers
    headers = all_values[1] if len(all_values) > 1 else []
    col_indices = {h: i for i, h in enumerate(headers)}

    code_col = col_indices.get('公司代碼', 1)  # B
    field_col = col_indices.get('欄位編號', 3)  # D

    mapping = {}
    for idx, row in enumerate(all_values[2:], start=3):  # Data starts at row 3
        if len(row) > max(code_col, field_col):
            code = str(row[code_col])
            field_id = str(row[field_col])

            if code and field_id:
                mapping[(code, field_id)] = idx

    logger.info(f"Created mapping for {len(mapping)} rows")
    return mapping


def fill_review_columns(
    gc: gspread.Client,
    comparison_df: pd.DataFrame,
    dry_run: bool = False
) -> int:
    """
    Fill columns L:P in Google Sheets with assessment results.

    Columns (L=12, M=13, N=14, O=15, P=16):
    - L (12): 答案正確性 (0%, 25%, 50%, 75%, 100%)
    - M (13): 正確數值 (most common value from runs)
    - N (14): 判斷說明/備註 (assessment notes)
    - O (15): 實際參考頁數 (most common page reference)
    - P (16): 參考頁數正確 (TRUE or empty)

    Args:
        gc: Authenticated gspread client
        comparison_df: DataFrame with comparison results
        dry_run: If True, show updates without writing

    Returns:
        Number of rows updated
    """
    logger = get_logger()

    # Open sheet
    sheet = gc.open_by_key(OUTPUT_SHEET_ID)
    worksheet = sheet.worksheet(VALIDATION_SHEET_NAME)

    # Get current headers (row 2 is headers in this sheet)
    headers = worksheet.row_values(2)
    logger.info(f"Current headers (row 2): {headers[:20]}")

    # Ensure sheet has enough columns (need at least 16 for P)
    sheet_cols = worksheet.col_count
    if sheet_cols < 17:
        logger.info(f"Expanding sheet from {sheet_cols} to 17 columns...")
        if not dry_run:
            worksheet.resize(cols=17)
            logger.info("Sheet expanded")

    # Add header for column P if missing
    if len(headers) < 16 or headers[15] != '參考頁數正確':
        logger.info("Adding '參考頁數正確' header to column P...")
        if not dry_run:
            worksheet.update_cell(2, 16, '參考頁數正確')
            logger.info("Header added")

    # Get row mapping
    row_mapping = get_sheet_row_mapping(worksheet)

    # Prepare batch update
    updates = []
    updated_count = 0

    for _, row in comparison_df.iterrows():
        code = str(row['公司代碼'])
        field_id = str(row['欄位編號'])
        key = (code, field_id)

        if key not in row_mapping:
            logger.warning(f"Row not found for {code} field {field_id}")
            continue

        sheet_row = row_mapping[key]

        # Get values, handling NaN
        correctness = str(row.get('答案正確性', ''))
        correct_value = str(row.get('正確數值', '')) if pd.notna(row.get('正確數值')) else ''
        assessment = str(row.get('判斷說明', '')) if pd.notna(row.get('判斷說明')) else ''
        page_ref = str(row.get('實際參考頁數', '')) if pd.notna(row.get('實際參考頁數')) else ''
        page_correct = str(row.get('參考頁數正確', '')) if pd.notna(row.get('參考頁數正確')) else ''

        # Clean up 'nan' strings
        if correct_value == 'nan':
            correct_value = ''
        if assessment == 'nan':
            assessment = ''
        if page_ref == 'nan':
            page_ref = ''
        if page_correct == 'nan':
            page_correct = ''

        # Prepare cell values for columns L, M, N, O, P
        values = [
            correctness,    # L: 答案正確性
            correct_value,  # M: 正確數值
            assessment,     # N: 判斷說明/備註
            page_ref,       # O: 實際參考頁數
            page_correct,   # P: 參考頁數正確
        ]

        for i, value in enumerate(values):
            updates.append({
                'range': f"{chr(76 + i)}{sheet_row}",  # L, M, N, O, P
                'values': [[value]]
            })

        updated_count += 1

    logger.info(f"Prepared {len(updates)} cell updates for {updated_count} rows")

    if dry_run:
        print(f"\n[DRY RUN] Would update {updated_count} rows")
        print("Sample updates:")
        for update in updates[:20]:
            print(f"  {update['range']}: {update['values'][0][0][:50] if update['values'][0][0] else ''}")
        return 0

    # Execute batch update
    if updates:
        # gspread batch_update expects list of dicts with 'range' and 'values'
        worksheet.batch_update(updates)
        logger.info(f"Updated {updated_count} rows in Google Sheets")

    return updated_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fill review columns (K:O) in Google Sheets"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be updated without writing"
    )
    parser.add_argument(
        "--validation-dir",
        type=str,
        help="Path to validation directory"
    )

    args = parser.parse_args()

    setup_logging(session_name="fill_review")
    logger = get_logger()

    validation_dir = Path(args.validation_dir) if args.validation_dir else \
        Path(__file__).parent.parent / "validation"

    try:
        # Load comparison report
        print("Loading comparison report...")
        comparison_df = load_comparison_report(validation_dir)
        print(f"Loaded {len(comparison_df)} comparison records")

        # Setup Google auth
        print("\nSetting up Google authentication...")
        gc = setup_google_auth()
        print("Authentication successful")

        # Summary
        print(f"\n{'='*60}")
        print("Assessment Column Fill Plan")
        print(f"{'='*60}")
        print(f"Companies: {comparison_df['公司代碼'].nunique()}")
        print(f"Fields per company: ~{len(comparison_df) // comparison_df['公司代碼'].nunique()}")
        print(f"Total rows to update: {len(comparison_df)}")
        print(f"Target sheet: {VALIDATION_SHEET_NAME}")
        print(f"Columns: L:P (答案正確性, 正確數值, 判斷說明, 實際參考頁數, 參考頁數正確)")
        print(f"{'='*60}\n")

        if not args.dry_run:
            confirm = input("Proceed with updating Google Sheets? (y/n): ")
            if confirm.lower() != 'y':
                print("Cancelled")
                return

        # Fill columns
        updated = fill_review_columns(gc, comparison_df, args.dry_run)

        if not args.dry_run:
            print(f"\nSuccessfully updated {updated} rows")
            print(f"Check: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")

    except FileNotFoundError as e:
        logger.error(str(e))
        print("\nPlease run comparison first:")
        print("  python scripts/compare_results.py")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
