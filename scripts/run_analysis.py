#!/usr/bin/env python3
"""
Main CLI entry point for Sustainability Report Parser.

Usage:
    python scripts/run_analysis.py --limit 5
    python scripts/run_analysis.py --company 2330
    python scripts/run_analysis.py --dry-run
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from tqdm import tqdm

from src.config import validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import CacheManager, SheetsManager
from src.analyzer import FieldCollectionAnalyzer


def setup_google_auth() -> gspread.Client:
    """
    Setup Google Sheets authentication.

    For local use, expects a service account JSON file at:
    - credentials.json in project root, or
    - GOOGLE_APPLICATION_CREDENTIALS environment variable

    Returns:
        Authenticated gspread client
    """
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
        raise FileNotFoundError(
            f"Google credentials file not found at {creds_path}. "
            "Please place your service account JSON file at 'credentials.json' "
            "or set GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )

    creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
    return gspread.authorize(creds)


def process_companies(
    sheets_manager: SheetsManager,
    analyzer: FieldCollectionAnalyzer,
    limit: int = None,
    company_code: str = None,
    dry_run: bool = False
) -> None:
    """
    Process companies from Google Sheets.

    Args:
        sheets_manager: SheetsManager instance
        analyzer: FieldCollectionAnalyzer instance
        limit: Maximum number of companies to process
        company_code: Specific company code to process
        dry_run: If True, show what would be processed without making API calls
    """
    logger = get_logger()

    logger.info("Starting smart batch processing...")

    # Get company list
    company_df = sheets_manager.get_company_list(filter_to_analyze=True)

    if company_df.empty:
        logger.warning("No companies found for analysis")
        return

    # Filter for specific company if requested
    if company_code:
        company_df = company_df[
            company_df['公司代碼'].astype(str) == str(company_code)
        ]
        if company_df.empty:
            logger.error(f"Company {company_code} not found in list")
            return

    # Load existing results once
    logger.info("Loading existing results...")
    existing_results_df = sheets_manager.get_existing_results()
    logger.info(f"Loaded {len(existing_results_df)} existing results")

    # Analyze processing needs
    companies_to_process = []

    print("\n🔍 Checking company processing status...")
    for idx, row in company_df.iterrows():
        code = str(row['公司代碼'])
        year = str(row['年度'])
        name = row['公司簡稱']

        status = sheets_manager.check_company_processing_status(
            code, year, existing_results_df
        )

        if status == 'completed':
            logger.info(f"✅ {name} ({code}): Already processed")
        else:
            companies_to_process.append((row, status))
            status_emoji = {
                'not_processed': '🆕',
                'incomplete': '⚠️',
                'failed': '❌'
            }
            logger.info(f"{status_emoji.get(status, '❓')} {name} ({code}): {status}")

    if not companies_to_process:
        print("\n🎉 All companies have been successfully processed!")
        return

    # Apply limit
    if limit and len(companies_to_process) > limit:
        companies_to_process = companies_to_process[:limit]
        logger.info(f"Limited to {limit} companies")

    total_companies = len(companies_to_process)
    print(f"\n📊 Companies to process: {total_companies}")

    # Show company list
    print("\n=== Companies to Process ===")
    for idx, (row, status) in enumerate(companies_to_process, 1):
        status_emoji = {
            'not_processed': '🆕 New',
            'incomplete': '⚠️ Incomplete',
            'failed': '❌ Failed'
        }
        print(f"{idx:2d}. {status_emoji[status]}: {row['公司簡稱']} ({row['公司代碼']}) - {row['年度']}")
        print(f"    File size: {row.get('檔案大小(MB)', 'Unknown')}MB")

    print("=" * 50)

    if dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
        print(f"Would process {total_companies} companies")
        return

    # Confirm before processing
    confirm = input(f"\n⚠️ Process {total_companies} companies? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    # Process companies
    successful_count = 0
    failed_count = 0

    for idx, (row, status) in enumerate(tqdm(companies_to_process, desc="Processing"), 1):
        try:
            code = str(row['公司代碼'])
            year = str(row['年度'])

            logger.info(f"Processing {idx}/{total_companies}: {row['公司簡稱']} (status: {status})")

            # Check for file link
            if not row.get('檔案連結') or str(row['檔案連結']).strip() == '':
                logger.warning(f"Skipping {row['公司簡稱']}: No file link")
                failed_count += 1
                continue

            # Delete old results if reprocessing
            if status in ['incomplete', 'failed']:
                logger.info(f"Deleting old results for {row['公司簡稱']}")
                sheets_manager.delete_company_results(code, year)

            # Analyze report
            results = analyzer.analyze_company_report_from_drive_with_retry(row.to_dict())

            if results:
                # Save to sheets
                sheets_manager.append_results(results)

                # Also save to local CSV backup
                sheets_manager.save_results_to_csv(results)

                successful_count += 1
                logger.info(f"✅ Successfully processed: {row['公司簡稱']}")
            else:
                failed_count += 1
                logger.error(f"❌ Failed to process: {row['公司簡稱']}")

        except Exception as e:
            failed_count += 1
            logger.error(f"❌ Error processing {row['公司簡稱']}: {e}")

    # Print summary
    print(analyzer.get_session_summary())
    print(f"\n✅ Successful: {successful_count}")
    print(f"❌ Failed: {failed_count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sustainability Report Parser - Extract structured data from ESG reports"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of companies to process"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Process specific company by stock code"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be processed without making changes"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(session_name="analysis")
    logger = get_logger()

    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        # Setup Google auth
        print("\n🔐 Setting up Google authentication...")
        gc = setup_google_auth()
        print("✅ Authentication successful")

        # Initialize managers
        cache_manager = CacheManager()
        sheets_manager = SheetsManager(gc)
        analyzer = FieldCollectionAnalyzer(cache_manager)

        # Run processing
        process_companies(
            sheets_manager=sheets_manager,
            analyzer=analyzer,
            limit=args.limit,
            company_code=args.company,
            dry_run=args.dry_run
        )

    except FileNotFoundError as e:
        logger.error(str(e))
        print("\n💡 Tip: Create a service account at Google Cloud Console and download the JSON key file")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
