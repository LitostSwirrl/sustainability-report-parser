#!/usr/bin/env python3
"""
Run extraction on manufacturing company PDFs using V2 field structure (2026年驗證指標).

Reads companies from Google Sheets where 待分析=TRUE and industry != 金融業,
then processes them and writes results to a new dated tab.

Usage:
    python scripts/run_manufacturing_extraction.py
    python scripts/run_manufacturing_extraction.py --dry-run
    python scripts/run_manufacturing_extraction.py --limit 5
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from tqdm import tqdm

from src.config import OUTPUT_SHEET_ID, validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import PDFProcessor, SheetsManager
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields, classify_industry


# Sheet name for manufacturing extraction results
SHEET_NAME = "製造業蒐集結果 2026-02-09"


def setup_google_auth() -> gspread.Client:
    """Setup Google Sheets authentication."""
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


def create_or_get_worksheet(gc: gspread.Client, sheet_name: str):
    """Create new worksheet or get existing one."""
    logger = get_logger()
    sheet = gc.open_by_key(OUTPUT_SHEET_ID)

    try:
        worksheet = sheet.worksheet(sheet_name)
        logger.info(f"Found existing worksheet: {sheet_name}")
        return worksheet
    except gspread.WorksheetNotFound:
        logger.info(f"Creating new worksheet: {sheet_name}")
        worksheet = sheet.add_worksheet(title=sheet_name, rows=5000, cols=20)

        # Add instruction row
        worksheet.update_cell(1, 1, "說明：製造業 V2 欄位結構提取結果（2026年驗證指標）")

        # Add headers in row 2
        headers = [
            '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
            '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間'
        ]
        worksheet.append_row(headers)

        return worksheet


def append_results_to_worksheet(worksheet, results: list) -> int:
    """Append results to worksheet."""
    logger = get_logger()

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
            result.get('處理時間', '')
        ]
        rows_to_add.append(row)

    if rows_to_add:
        worksheet.append_rows(rows_to_add)
        logger.info(f"Appended {len(rows_to_add)} results")

    return len(rows_to_add)


def get_manufacturing_companies(sheets_manager: SheetsManager) -> list:
    """Get list of manufacturing companies to process (待分析=TRUE, not finance)."""
    logger = get_logger()

    # Get all companies marked for analysis
    company_df = sheets_manager.get_company_list(filter_to_analyze=True)

    if company_df.empty:
        logger.warning("No companies found with 待分析=TRUE")
        return []

    # Filter out finance companies
    manufacturing_companies = []
    for _, row in company_df.iterrows():
        industry = row.get('產業別', '')
        industry_category = classify_industry(industry)

        if industry_category != "金融":
            manufacturing_companies.append(row.to_dict())

    logger.info(f"Found {len(manufacturing_companies)} manufacturing companies to process")
    return manufacturing_companies


def run_extraction(dry_run: bool = False, limit: int = None) -> None:
    """Run extraction on manufacturing companies."""
    logger = get_logger()

    # Setup Google auth
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    sheets_manager = SheetsManager(gc)
    print("Authentication successful")

    # Get manufacturing companies
    companies = get_manufacturing_companies(sheets_manager)

    if not companies:
        logger.error("No manufacturing companies found to process")
        return

    if limit:
        companies = companies[:limit]

    print(f"\n{'='*60}")
    print("Manufacturing Sector Extraction Plan (V2 - 2026年驗證指標)")
    print(f"{'='*60}")
    print(f"Companies: {len(companies)}")
    print(f"Target Sheet: {SHEET_NAME}")
    print(f"Field Version: V2 (70 base fields)")
    print(f"{'='*60}\n")

    for company in companies:
        industry = company.get('產業別', '')
        industry_category = classify_industry(industry)
        fields = get_final_fields(industry, version="v2")
        print(f"  - {company.get('公司簡稱')} ({company.get('公司代碼')}) - {industry_category} ({len(fields)} fields)")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(companies)} extractions? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Create/get worksheet
    worksheet = create_or_get_worksheet(gc, SHEET_NAME)

    # Initialize analyzer (no cache for fresh extraction)
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None  # Disable cache

    # Process each company
    successful = 0
    failed = 0

    for company in tqdm(companies, desc="Processing"):
        company_code = str(company.get('公司代碼', ''))
        company_name = company.get('公司簡稱', '')
        year = str(company.get('年度', ''))
        industry = company.get('產業別', '')

        logger.info(f"Processing: {company_name} ({company_code})")

        try:
            start_time = datetime.now()

            # Get company info
            company_info = PDFProcessor.get_company_info_from_sheet_data(company)

            # Download PDF
            file_id = PDFProcessor.extract_drive_file_id(company_info['file_link'])
            if not file_id:
                logger.error(f"Could not extract file ID: {company_info['file_link']}")
                failed += 1
                continue

            pdf_path = PDFProcessor.download_from_drive(file_id, company_info)
            if not pdf_path:
                logger.error(f"PDF download failed: {company_name}")
                failed += 1
                continue

            try:
                # Upload PDF to Gemini
                pdf_gemini = PDFProcessor.upload_pdf_to_gemini(pdf_path)
                if not pdf_gemini:
                    logger.error(f"Failed to upload: {pdf_path}")
                    failed += 1
                    continue

                try:
                    # Get fields for this industry (V2 structure)
                    final_fields = get_final_fields(industry, version="v2")

                    # Build prompt and call API
                    prompt = analyzer._build_field_collection_prompt(
                        company_info, final_fields, use_v2_sorting=True
                    )

                    from google import genai
                    from google.genai import types
                    from src.config import MODEL_NAME, GEMINI_API_KEY

                    client = genai.Client(api_key=GEMINI_API_KEY)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[
                            types.Content(
                                role="user",
                                parts=[
                                    types.Part.from_text(text=prompt),
                                    types.Part.from_uri(
                                        file_uri=pdf_gemini.uri,
                                        mime_type="application/pdf"
                                    )
                                ]
                            )
                        ]
                    )

                    if response and response.text:
                        results = analyzer._parse_field_collection_response(
                            response.text, company_info, final_fields
                        )

                        # Append to worksheet
                        count = append_results_to_worksheet(worksheet, results)

                        elapsed = (datetime.now() - start_time).total_seconds()
                        logger.info(f"Completed {company_name}: {count} fields in {elapsed:.1f}s")
                        successful += 1
                    else:
                        logger.error(f"No response for {company_name}")
                        failed += 1

                finally:
                    # Clean up Gemini file
                    PDFProcessor.delete_gemini_file(pdf_gemini.name)

            finally:
                # Clean up local PDF
                PDFProcessor.delete_local_pdf(pdf_path)

        except Exception as e:
            logger.error(f"Error processing {company_name}: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print("Manufacturing Extraction Complete")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run manufacturing sector extraction with V2 field structure"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Limit number of companies to process"
    )

    args = parser.parse_args()

    setup_logging(session_name="manufacturing_extraction")

    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        run_extraction(dry_run=args.dry_run, limit=args.limit)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
