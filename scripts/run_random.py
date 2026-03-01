#!/usr/bin/env python3
"""
Run analysis on random companies.
Clears existing results and processes N random companies marked for analysis.
"""

import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials

from src.config import validate_config, print_config, OUTPUT_SHEET_ID, OUTPUT_SHEET_NAME
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


def clear_output_sheet(gc: gspread.Client):
    """Clear output sheet but keep headers."""
    logger = get_logger()
    try:
        sheet = gc.open_by_key(OUTPUT_SHEET_ID)
        worksheet = sheet.worksheet(OUTPUT_SHEET_NAME)

        # Get all data
        all_values = worksheet.get_all_values()

        if len(all_values) > 1:
            # Keep only header row
            headers = all_values[0]
            worksheet.clear()
            worksheet.append_row(headers)
            logger.info(f"Cleared {len(all_values) - 1} rows from output sheet, kept headers")
        else:
            logger.info("Output sheet already empty (only headers)")

    except gspread.WorksheetNotFound:
        logger.info("Output worksheet not found, will be created on first write")
    except Exception as e:
        logger.error(f"Failed to clear output sheet: {e}")
        raise


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run random company analysis")
    parser.add_argument("--count", "-n", type=int, default=10, help="Number of random companies")
    parser.add_argument("--seed", "-s", type=int, help="Random seed for reproducibility")
    parser.add_argument("--clear-only", action="store_true", help="Only clear sheets, don't process")
    args = parser.parse_args()

    setup_logging(session_name="random_run")
    logger = get_logger()

    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    # Setup
    print("\n🔐 Setting up Google authentication...")
    gc = setup_google_auth()
    print("✅ Authentication successful")

    # Clear output sheet
    print("\n🗑️ Clearing output sheet...")
    clear_output_sheet(gc)
    print("✅ Output sheet cleared")

    if args.clear_only:
        print("\n✅ Clear complete. Exiting (--clear-only mode)")
        return

    # Initialize managers
    cache_manager = CacheManager()
    sheets_manager = SheetsManager(gc)
    analyzer = FieldCollectionAnalyzer(cache_manager)

    # Get all companies marked for analysis
    print("\n📋 Loading company list...")
    company_df = sheets_manager.get_company_list(filter_to_analyze=True)

    if company_df.empty:
        print("❌ No companies found for analysis")
        return

    print(f"Found {len(company_df)} companies marked for analysis")

    # Random selection
    if args.seed:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")

    count = min(args.count, len(company_df))
    random_indices = random.sample(range(len(company_df)), count)
    selected_companies = company_df.iloc[random_indices]

    print(f"\n🎲 Randomly selected {count} companies:")
    print("=" * 50)
    for idx, (_, row) in enumerate(selected_companies.iterrows(), 1):
        print(f"{idx:2d}. {row['公司簡稱']} ({row['公司代碼']}) - {row['產業別']}")
    print("=" * 50)

    # Confirm
    confirm = input(f"\n⚠️ Process these {count} companies? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    # Process
    from tqdm import tqdm

    successful = 0
    failed = 0

    for _, row in tqdm(selected_companies.iterrows(), total=count, desc="Processing"):
        try:
            code = str(row['公司代碼'])
            year = str(row['年度'])

            if not row.get('檔案連結') or str(row['檔案連結']).strip() == '':
                logger.warning(f"Skipping {row['公司簡稱']}: No file link")
                failed += 1
                continue

            results = analyzer.analyze_company_report_from_drive_with_retry(row.to_dict())

            if results:
                sheets_manager.append_results(results)
                sheets_manager.save_results_to_csv(results, code, row['公司簡稱'], year)
                successful += 1
                logger.info(f"✅ {row['公司簡稱']}")
            else:
                failed += 1
                logger.error(f"❌ {row['公司簡稱']}")

        except Exception as e:
            failed += 1
            logger.error(f"❌ {row['公司簡稱']}: {e}")

    # Summary
    print(analyzer.get_session_summary())
    print(f"\n✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")


if __name__ == "__main__":
    main()
