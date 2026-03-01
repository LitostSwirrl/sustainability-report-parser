#!/usr/bin/env python3
"""
Financial indicators validation script.

Runs extraction with updated finance fields (421-432) and reordered GHG emissions
on the 10 validation companies, outputting to a new Google Sheets tab.

Usage:
    python scripts/run_financial_validation.py --dry-run
    python scripts/run_financial_validation.py --company 1216
    python scripts/run_financial_validation.py
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

# Output tab name with today's date
OUTPUT_TAB_NAME = f"財務指標更新驗證_{datetime.now().strftime('%Y%m%d')}"


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


class FinanceValidationAnalyzer:
    """Analyzer for financial indicator validation runs."""

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

        self.logger.info(f"Running extraction for {company_name}")

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

            # Log field count by category
            ghg_fields = [f for f in final_fields if f in [str(i) for i in range(27, 34)]]
            scope3_fields = [f for f in final_fields if f in [str(i) for i in range(42, 57)]]
            finance_fields = [f for f in final_fields if int(f) >= 400]

            self.logger.info(
                f"Field breakdown: GHG={len(ghg_fields)}, Scope3={len(scope3_fields)}, "
                f"Finance={len(finance_fields)}, Total={len(final_fields)}"
            )

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
    target_companies: list = None,
    dry_run: bool = False,
    skip_sheets: bool = False
) -> None:
    """
    Run validation extractions for specified companies.

    Args:
        sheets_manager: SheetsManager instance
        target_companies: List of company codes to process
        dry_run: If True, show plan without executing
        skip_sheets: If True, skip writing to Google Sheets
    """
    logger = get_logger()
    output_dir = Path(__file__).parent.parent / "validation_finance"
    output_dir.mkdir(exist_ok=True)

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
    print(f"Financial Indicators Validation Plan")
    print(f"{'='*60}")
    print(f"Companies: {len(company_df)}")
    print(f"Output tab: {OUTPUT_TAB_NAME}")
    print(f"Total API calls: {len(company_df)}")
    print(f"Estimated time: ~{len(company_df) * 2} minutes")
    print(f"{'='*60}")
    print(f"\nNew fields (421-432):")
    print(f"  - UN永續原則第三方確信")
    print(f"  - 永續金融人才認證比例")
    print(f"  - 氣候實體風險揭露")
    print(f"  - 高碳產業放款佔比/減量目標")
    print(f"  - 生物多樣性風險評估")
    print(f"  - ...etc (12 new fields)")
    print(f"\nGHG Field Order:")
    print(f"  類別一 → 類別二 → 類別三 → 範疇三 → 類別四 → 類別五 → 類別六")
    print(f"  → Scope 3 類別 1-15")
    print(f"{'='*60}\n")
    print("Target companies:")
    for _, row in company_df.iterrows():
        print(f"  - {row['公司簡稱']} ({row['公司代碼']})")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")

        # Show field order for a sample industry
        sample_fields = get_final_fields("金融業")

        # Sort by display_order
        def sort_key(field_id: str) -> tuple:
            field_info = sample_fields[field_id]
            display_order = field_info.get('display_order')
            if display_order is not None:
                return (0, display_order, int(field_id))
            return (1, 0, int(field_id))

        sorted_ids = sorted(sample_fields.keys(), key=sort_key)

        print(f"\nField order preview (first 30 for 金融業):")
        for i, fid in enumerate(sorted_ids[:30]):
            f = sample_fields[fid]
            order_info = f" [order={f.get('display_order', 'N/A')}]" if 'display_order' in f else ""
            print(f"  {i+1}. [{fid}] {f['name']}{order_info}")

        # Show new finance fields
        print(f"\nNew finance fields (421-432):")
        for fid in [str(i) for i in range(421, 433)]:
            if fid in sample_fields:
                f = sample_fields[fid]
                print(f"  [{fid}] {f['name']}")

        return

    # Confirm
    confirm = input(f"\nProceed with {len(company_df)} API calls? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Initialize validator
    validator = FinanceValidationAnalyzer()
    all_results = []

    # Run extractions
    print(f"\n{'='*60}")
    print(f"Running Extractions")
    print(f"{'='*60}")

    for idx, row in tqdm(company_df.iterrows(), total=len(company_df), desc="Processing"):
        company_code = str(row['公司代碼'])
        company_name = row['公司簡稱']
        year = str(row['年度'])

        output_file = output_dir / f"{company_code}_{year}.json"

        try:
            logger.info(f"Processing {company_name} ({company_code})")
            start_time = datetime.now()

            results = validator.run_extraction(row.to_dict())

            elapsed = (datetime.now() - start_time).total_seconds()

            # Save to local JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'company_code': company_code,
                    'company_name': company_name,
                    'year': year,
                    'processed_at': datetime.now().isoformat(),
                    'elapsed_seconds': elapsed,
                    'output_tab': OUTPUT_TAB_NAME,
                    'field_count': len(results),
                    'results': results
                }, f, ensure_ascii=False, indent=2)

            # Collect results for Google Sheets
            all_results.extend(results)

            logger.info(f"Completed {company_name}: {len(results)} fields in {elapsed:.1f}s")

        except Exception as e:
            logger.error(f"Failed {company_name}: {e}")

            # Save error record
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'company_code': company_code,
                    'company_name': company_name,
                    'year': year,
                    'processed_at': datetime.now().isoformat(),
                    'error': str(e),
                    'results': []
                }, f, ensure_ascii=False, indent=2)

    # Write all results to Google Sheets
    if all_results and not skip_sheets:
        print(f"\nWriting {len(all_results)} results to Google Sheets tab: {OUTPUT_TAB_NAME}")
        try:
            sheets_manager.append_results(all_results, tab_name=OUTPUT_TAB_NAME)
            print(f"Successfully wrote to Google Sheets")
        except Exception as e:
            logger.error(f"Failed to write to Google Sheets: {e}")
            print(f"ERROR: Failed to write to Google Sheets: {e}")
            print(f"Results are saved locally in: {output_dir}")

    print(f"\nValidation complete!")
    print(f"Local results: {output_dir}")
    print(f"Google Sheets tab: {OUTPUT_TAB_NAME}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run financial indicators validation on 10 sample companies"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Process specific company by stock code"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan and field order without executing"
    )
    parser.add_argument(
        "--skip-sheets",
        action="store_true",
        help="Skip writing to Google Sheets (local JSON only)"
    )

    args = parser.parse_args()

    # Setup
    setup_logging(session_name="finance_validation")
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

        target_companies = [args.company] if args.company else None

        run_validation(
            sheets_manager=sheets_manager,
            target_companies=target_companies,
            dry_run=args.dry_run,
            skip_sheets=args.skip_sheets
        )

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
