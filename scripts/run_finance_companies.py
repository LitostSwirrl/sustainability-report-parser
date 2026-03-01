#!/usr/bin/env python3
"""
Run extraction on 10 financial companies to validate new finance fields (421-432).

Usage:
    python scripts/run_finance_companies.py --dry-run
    python scripts/run_finance_companies.py
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from tqdm import tqdm

from src.config import validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import SheetsManager, PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


# 10 Financial companies for validation
FINANCE_COMPANIES = [
    "2801", "2812", "2816", "2820", "2832",
    "2834", "2836", "2838", "2845", "2849"
]

OUTPUT_TAB_NAME = f"金融業欄位驗證_{datetime.now().strftime('%Y%m%d')}"


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


class FinanceAnalyzer:
    """Analyzer for financial company extraction."""

    def __init__(self):
        self.logger = get_logger()
        self.analyzer = FieldCollectionAnalyzer()
        self.analyzer.cache_manager = None  # Disable cache

    def run_extraction(self, company_data: dict) -> list:
        """Run fresh extraction without cache."""
        company_info = PDFProcessor.get_company_info_from_sheet_data(company_data)
        company_name = company_info['company_name']

        self.logger.info(f"Running extraction for {company_name}")

        file_id = PDFProcessor.extract_drive_file_id(company_info['file_link'])
        if not file_id:
            self.logger.error(f"Could not extract file ID: {company_info['file_link']}")
            return []

        pdf_path = PDFProcessor.download_from_drive(file_id, company_info)
        if not pdf_path:
            self.logger.error(f"PDF download failed: {company_name}")
            return []

        try:
            results = self._analyze(pdf_path, company_info)
            return results
        finally:
            PDFProcessor.delete_local_pdf(pdf_path)

    def _analyze(self, pdf_path: str, company_info: dict) -> list:
        """Analyze report."""
        from google import genai
        from google.genai import types
        from src.config import MODEL_NAME, GEMINI_API_KEY

        pdf_file = PDFProcessor.upload_pdf_to_gemini(pdf_path)
        if not pdf_file:
            return []

        try:
            final_fields = get_final_fields(company_info.get('industry', ''))

            # Count finance fields
            finance_fields = [f for f in final_fields if int(f) >= 400]
            self.logger.info(
                f"Field breakdown: Finance={len(finance_fields)}, Total={len(final_fields)}"
            )

            prompt = self.analyzer._build_field_collection_prompt(company_info, final_fields)

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


def run_finance_validation(
    sheets_manager: SheetsManager,
    dry_run: bool = False
) -> None:
    """Run validation on financial companies."""
    logger = get_logger()
    output_dir = Path(__file__).parent.parent / "validation_finance"
    output_dir.mkdir(exist_ok=True)

    # Get company list (without filter_to_analyze restriction)
    company_df = sheets_manager.get_company_list(filter_to_analyze=False)
    company_df = company_df[
        company_df['公司代碼'].astype(str).isin(FINANCE_COMPANIES)
    ]

    if company_df.empty:
        logger.error("No matching financial companies found")
        return

    print(f"\n{'='*60}")
    print(f"Financial Companies Validation Plan")
    print(f"{'='*60}")
    print(f"Companies: {len(company_df)}")
    print(f"Output tab: {OUTPUT_TAB_NAME}")
    print(f"New finance fields: 421-432 (12 fields)")
    print(f"{'='*60}\n")
    print("Target companies:")
    for _, row in company_df.iterrows():
        print(f"  - {row['公司簡稱']} ({row['公司代碼']}) - {row['產業別']}")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")

        # Show finance field details
        sample_fields = get_final_fields("金融業")
        print(f"\nFinance fields loaded: {len([f for f in sample_fields if int(f) >= 400])}")
        print(f"Total fields for 金融業: {len(sample_fields)}")

        print("\nNew finance fields (421-432):")
        for fid in [str(i) for i in range(421, 433)]:
            if fid in sample_fields:
                print(f"  [{fid}] {sample_fields[fid]['name']}")
        return

    confirm = input(f"\nProceed with {len(company_df)} API calls? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    analyzer = FinanceAnalyzer()
    all_results = []

    print(f"\n{'='*60}")
    print(f"Running Extractions")
    print(f"{'='*60}")

    for idx, row in tqdm(company_df.iterrows(), total=len(company_df), desc="Processing"):
        company_code = str(row['公司代碼'])
        company_name = row['公司簡稱']
        year = str(row['年度'])

        output_file = output_dir / f"finance_{company_code}_{year}.json"

        try:
            logger.info(f"Processing {company_name} ({company_code})")
            start_time = datetime.now()

            results = analyzer.run_extraction(row.to_dict())
            elapsed = (datetime.now() - start_time).total_seconds()

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'company_code': company_code,
                    'company_name': company_name,
                    'year': year,
                    'industry': row['產業別'],
                    'processed_at': datetime.now().isoformat(),
                    'elapsed_seconds': elapsed,
                    'field_count': len(results),
                    'results': results
                }, f, ensure_ascii=False, indent=2)

            all_results.extend(results)
            logger.info(f"Completed {company_name}: {len(results)} fields in {elapsed:.1f}s")

        except Exception as e:
            logger.error(f"Failed {company_name}: {e}")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'company_code': company_code,
                    'company_name': company_name,
                    'year': year,
                    'error': str(e),
                    'results': []
                }, f, ensure_ascii=False, indent=2)

    # Write to Google Sheets
    if all_results:
        print(f"\nWriting {len(all_results)} results to Google Sheets tab: {OUTPUT_TAB_NAME}")
        try:
            sheets_manager.append_results(all_results, tab_name=OUTPUT_TAB_NAME)
            print("Successfully wrote to Google Sheets")
        except Exception as e:
            logger.error(f"Failed to write to Google Sheets: {e}")

    print(f"\nValidation complete!")
    print(f"Local results: {output_dir}")
    print(f"Google Sheets tab: {OUTPUT_TAB_NAME}")


def main():
    parser = argparse.ArgumentParser(
        description="Run extraction on 10 financial companies"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )
    args = parser.parse_args()

    setup_logging(session_name="finance_companies")
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

        run_finance_validation(
            sheets_manager=sheets_manager,
            dry_run=args.dry_run
        )

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
