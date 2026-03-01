#!/usr/bin/env python3
"""
Validation script for running multiple extraction rounds.

Runs extractions multiple times per company to assess consistency.
Results are stored in validation/ directory for later comparison.

Usage:
    python scripts/run_validation.py --runs 5
    python scripts/run_validation.py --runs 5 --company 1216
    python scripts/run_validation.py --dry-run
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from tqdm import tqdm

from src.config import validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import SheetsManager, PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


# Validation target companies (10 companies from initial batch)
VALIDATION_COMPANIES = [
    "1216", "1409", "1444", "1451", "1563",
    "2023", "2101", "2313", "5425", "6443"
]


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


def download_original_results(
    sheets_manager: SheetsManager,
    validation_dir: Path
) -> None:
    """Download original extraction results from Google Sheets."""
    logger = get_logger()
    original_dir = validation_dir / "original"
    original_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading original results from Google Sheets...")
    existing_results = sheets_manager.get_existing_results()

    if existing_results.empty:
        logger.warning("No existing results found in Google Sheets")
        return

    for company_code in VALIDATION_COMPANIES:
        company_results = existing_results[
            existing_results['公司代碼'].astype(str) == str(company_code)
        ]

        if company_results.empty:
            logger.warning(f"No results found for {company_code}")
            continue

        year = company_results['西元年份'].iloc[0]
        output_file = original_dir / f"{company_code}_{year}.json"

        # Convert to list of dicts
        results_list = company_results.to_dict('records')

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'company_code': company_code,
                'year': str(year),
                'source': 'google_sheets',
                'downloaded_at': datetime.now().isoformat(),
                'results': results_list
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved original results: {output_file} ({len(results_list)} fields)")


class ValidationAnalyzer:
    """Modified analyzer that bypasses cache for validation runs."""

    def __init__(self):
        self.logger = get_logger()
        self.analyzer = FieldCollectionAnalyzer()
        # Disable cache for fresh extractions
        self.analyzer.cache_manager = None

    def run_extraction(self, company_data: dict) -> list:
        """
        Run fresh extraction without cache.

        Args:
            company_data: Company data from sheets

        Returns:
            List of field results
        """
        company_info = PDFProcessor.get_company_info_from_sheet_data(company_data)
        company_name = company_info['company_name']

        self.logger.info(f"Running fresh extraction for {company_name}")

        # Download PDF
        file_id = PDFProcessor.extract_drive_file_id(company_info['file_link'])
        if not file_id:
            self.logger.error(f"Could not extract file ID: {company_info['file_link']}")
            return []

        pdf_path = PDFProcessor.download_from_drive(file_id, company_info)
        if not pdf_path:
            self.logger.error(f"PDF download failed: {company_name}")
            return []

        try:
            # Run analysis without caching
            results = self._analyze_without_cache(pdf_path, company_info)
            return results
        finally:
            PDFProcessor.delete_local_pdf(pdf_path)

    def _analyze_without_cache(self, pdf_path: str, company_info: dict) -> list:
        """Analyze report without using or saving cache."""
        from google import genai
        from google.genai import types
        from src.config import MODEL_NAME, GEMINI_API_KEY

        # Upload PDF
        pdf_file = PDFProcessor.upload_pdf_to_gemini(pdf_path)
        if not pdf_file:
            return []

        try:
            # Get fields and build prompt
            final_fields = get_final_fields(company_info.get('industry', ''))
            prompt = self.analyzer._build_field_collection_prompt(company_info, final_fields)

            # Make API call
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=prompt),
                            types.Part.from_uri(
                                file_uri=pdf_file.uri,
                                mime_type="application/pdf"
                            )
                        ]
                    )
                ]
            )

            if response and response.text:
                return self.analyzer._parse_field_collection_response(
                    response.text, company_info, final_fields
                )
            return []

        finally:
            PDFProcessor.delete_gemini_file(pdf_file.name)


def run_validation(
    sheets_manager: SheetsManager,
    num_runs: int = 5,
    target_companies: list = None,
    dry_run: bool = False
) -> None:
    """
    Run validation extractions for specified companies.

    Args:
        sheets_manager: SheetsManager instance
        num_runs: Number of extraction runs per company
        target_companies: List of company codes to process
        dry_run: If True, show plan without executing
    """
    logger = get_logger()
    validation_dir = Path(__file__).parent.parent / "validation"
    validation_dir.mkdir(exist_ok=True)

    # Default to all validation companies
    if not target_companies:
        target_companies = VALIDATION_COMPANIES

    # Get company list from sheets
    company_df = sheets_manager.get_company_list(filter_to_analyze=True)
    company_df = company_df[
        company_df['公司代碼'].astype(str).isin(target_companies)
    ]

    if company_df.empty:
        logger.error("No matching companies found")
        return

    # Show plan
    print(f"\n{'='*60}")
    print(f"Validation Plan")
    print(f"{'='*60}")
    print(f"Companies: {len(company_df)}")
    print(f"Runs per company: {num_runs}")
    print(f"Total API calls: {len(company_df) * num_runs}")
    print(f"Estimated time: ~{len(company_df) * num_runs * 2} minutes")
    print(f"{'='*60}\n")

    for _, row in company_df.iterrows():
        print(f"  - {row['公司簡稱']} ({row['公司代碼']})")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(company_df) * num_runs} API calls? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Download original results first
    download_original_results(sheets_manager, validation_dir)

    # Initialize validator
    validator = ValidationAnalyzer()

    # Run extractions
    for run_num in range(1, num_runs + 1):
        run_dir = validation_dir / f"run_{run_num}"
        run_dir.mkdir(exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Run {run_num}/{num_runs}")
        print(f"{'='*60}")

        for idx, row in tqdm(company_df.iterrows(), total=len(company_df), desc=f"Run {run_num}"):
            company_code = str(row['公司代碼'])
            company_name = row['公司簡稱']
            year = str(row['年度'])

            output_file = run_dir / f"{company_code}_{year}.json"

            # Skip if already processed
            if output_file.exists():
                logger.info(f"Skipping {company_name}: already processed in run {run_num}")
                continue

            try:
                logger.info(f"Processing {company_name} ({company_code}) - Run {run_num}")
                start_time = datetime.now()

                results = validator.run_extraction(row.to_dict())

                elapsed = (datetime.now() - start_time).total_seconds()

                # Save results
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'company_code': company_code,
                        'company_name': company_name,
                        'year': year,
                        'run_number': run_num,
                        'processed_at': datetime.now().isoformat(),
                        'elapsed_seconds': elapsed,
                        'results': results
                    }, f, ensure_ascii=False, indent=2)

                logger.info(f"Completed {company_name}: {len(results)} fields in {elapsed:.1f}s")

            except Exception as e:
                logger.error(f"Failed {company_name}: {e}")

                # Save error record
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'company_code': company_code,
                        'company_name': company_name,
                        'year': year,
                        'run_number': run_num,
                        'processed_at': datetime.now().isoformat(),
                        'error': str(e),
                        'results': []
                    }, f, ensure_ascii=False, indent=2)

    print(f"\nValidation complete! Results saved to: {validation_dir}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run validation extractions for consistency testing"
    )
    parser.add_argument(
        "--runs", "-r",
        type=int,
        default=5,
        help="Number of extraction runs per company (default: 5)"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Process specific company by stock code"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download original results from Google Sheets"
    )

    args = parser.parse_args()

    # Setup
    setup_logging(session_name="validation")
    logger = get_logger()

    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        print("\nSetting up Google authentication...")
        gc = setup_google_auth()
        sheets_manager = SheetsManager(gc)
        print("Authentication successful")

        if args.download_only:
            validation_dir = Path(__file__).parent.parent / "validation"
            validation_dir.mkdir(exist_ok=True)
            download_original_results(sheets_manager, validation_dir)
            return

        target_companies = [args.company] if args.company else None

        run_validation(
            sheets_manager=sheets_manager,
            num_runs=args.runs,
            target_companies=target_companies,
            dry_run=args.dry_run
        )

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
