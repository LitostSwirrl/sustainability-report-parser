#!/usr/bin/env python3
"""
Run analysis on random companies and export to a specific Google Sheets tab.
Includes PDF Drive link as an additional column.
"""

import sys
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from tqdm import tqdm

from src.config import validate_config, print_config, OUTPUT_SHEET_ID
from src.utils import setup_logging, get_logger
from src.pdf_processor import CacheManager, SheetsManager
from src.analyzer import FieldCollectionAnalyzer


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

    creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
    return gspread.authorize(creds)


def append_results_to_custom_sheet(
    gc: gspread.Client,
    results: list,
    sheet_name: str,
    drive_link: str
) -> None:
    """
    Append results to a custom worksheet with Drive link column.
    """
    logger = get_logger()
    try:
        sheet = gc.open_by_key(OUTPUT_SHEET_ID)

        try:
            worksheet = sheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(
                title=sheet_name, rows=5000, cols=15
            )
            headers = [
                '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
                '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間',
                '報告書連結'
            ]
            worksheet.append_row(headers)
            logger.info(f"Created new worksheet: {sheet_name}")

        rows_to_add = []
        for result in results:
            row = [
                result.get('年份', ''),
                result.get('公司代碼', ''),
                result.get('公司簡稱', ''),
                result.get('欄位編號', ''),
                result.get('欄位名稱', ''),
                result.get('欄位數值', ''),
                result.get('欄位單位', ''),
                result.get('補充說明', ''),
                result.get('參考頁數', ''),
                result.get('處理時間', ''),
                drive_link
            ]
            rows_to_add.append(row)

        if rows_to_add:
            worksheet.append_rows(rows_to_add)
            logger.info(f"Appended {len(rows_to_add)} results to {sheet_name}")

    except Exception as e:
        logger.error(f"Failed to write results: {e}")
        raise


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run random company analysis with custom export")
    parser.add_argument("--count", "-n", type=int, default=10, help="Number of random companies")
    parser.add_argument("--seed", "-s", type=int, help="Random seed for reproducibility")
    parser.add_argument("--companies", "-c", type=str, help="Comma-separated company codes (overrides random)")
    parser.add_argument("--sheet-name", type=str,
                        default="欄位蒐集結果 26-02-04（prompt ver. 2）",
                        help="Target worksheet name")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without running")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    setup_logging(session_name="random_export")
    logger = get_logger()

    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    # Setup
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    # Initialize managers
    cache_manager = CacheManager()
    sheets_manager = SheetsManager(gc)
    analyzer = FieldCollectionAnalyzer(cache_manager)

    # Get all companies marked for analysis
    print("\nLoading company list...")
    company_df = sheets_manager.get_company_list(filter_to_analyze=True)

    if company_df.empty:
        print("No companies found for analysis")
        return

    print(f"Found {len(company_df)} companies marked for analysis")

    # Selection: specific companies or random
    if args.companies:
        # Use specific company codes
        company_codes = [c.strip() for c in args.companies.split(",")]
        selected_companies = company_df[
            company_df['公司代碼'].astype(str).isin(company_codes)
        ]
        if selected_companies.empty:
            print(f"No matching companies found for codes: {company_codes}")
            return
        count = len(selected_companies)
        print(f"\nSelected {count} specific companies:")
    else:
        # Random selection
        if args.seed:
            random.seed(args.seed)
            print(f"Using random seed: {args.seed}")

        count = min(args.count, len(company_df))
        random_indices = random.sample(range(len(company_df)), count)
        selected_companies = company_df.iloc[random_indices]
        print(f"\nRandomly selected {count} companies:")
    print("=" * 60)
    for idx, (_, row) in enumerate(selected_companies.iterrows(), 1):
        link = row.get('檔案連結', 'No link')[:50]
        print(f"{idx:2d}. {row['公司簡稱']} ({row['公司代碼']}) - {row['產業別']}")
        print(f"    Link: {link}...")
    print("=" * 60)

    if args.dry_run:
        print(f"\nDRY RUN - Would export to sheet: '{args.sheet_name}'")
        return

    # Confirm
    if not args.yes:
        confirm = input(f"\nProcess {count} companies and export to '{args.sheet_name}'? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
    else:
        print(f"\nProcessing {count} companies (auto-confirmed with -y flag)")

    # Process
    successful = 0
    failed = 0

    for _, row in tqdm(selected_companies.iterrows(), total=count, desc="Processing"):
        try:
            code = str(row['公司代碼'])
            year = str(row['年度'])
            drive_link = str(row.get('檔案連結', ''))

            if not drive_link or drive_link.strip() == '':
                logger.warning(f"Skipping {row['公司簡稱']}: No file link")
                failed += 1
                continue

            results = analyzer.analyze_company_report_from_drive_with_retry(row.to_dict())

            if results:
                # Export to custom sheet with drive link
                append_results_to_custom_sheet(
                    gc=gc,
                    results=results,
                    sheet_name=args.sheet_name,
                    drive_link=drive_link
                )
                successful += 1
                logger.info(f"Completed: {row['公司簡稱']}")
            else:
                failed += 1
                logger.error(f"Failed: {row['公司簡稱']}")

        except Exception as e:
            failed += 1
            logger.error(f"Error {row['公司簡稱']}: {e}")

    # Summary
    print(analyzer.get_session_summary())
    print(f"\nSuccessful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nResults exported to: '{args.sheet_name}'")


if __name__ == "__main__":
    main()
