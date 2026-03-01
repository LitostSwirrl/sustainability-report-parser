#!/usr/bin/env python3
"""
Re-run extraction for specific companies that had failures.

Usage:
    python scripts/rerun_failed_companies.py 2891 2884
    python scripts/rerun_failed_companies.py --dry-run 2891 2884
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

from src.config import OUTPUT_SHEET_ID, MODEL_NAME, GEMINI_API_KEY, validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


# Sheet name for re-extraction results (new tab to avoid rate limits)
SHEET_NAME = "金融業重跑 26-02-05（中信金+玉山金）"

# Finance PDFs directory
FINANCE_DIR = Path(__file__).parent.parent / "finance_pdfs"

# Company info mapping
FINANCE_COMPANIES = {
    "2881": {"name": "富邦金", "industry": "金融業"},
    "2882": {"name": "國泰金", "industry": "金融業"},
    "2884": {"name": "玉山金", "industry": "金融業"},
    "2885": {"name": "元大投信", "industry": "金融業"},
    "2886": {"name": "兆豐金", "industry": "金融業"},
    "2890": {"name": "永豐金", "industry": "金融業"},
    "2891": {"name": "中信金", "industry": "金融業"},
    "2892": {"name": "第一金", "industry": "金融業"},
    "5880": {"name": "合庫金", "industry": "金融業"},
    "6005": {"name": "元大證", "industry": "金融業"},
}


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


def find_pdf_for_company(company_code: str) -> Path:
    """Find the PDF file for a company code."""
    for pdf_file in FINANCE_DIR.glob("*.pdf"):
        if pdf_file.name.startswith(f"{company_code}_"):
            return pdf_file
    return None


def delete_company_rows(worksheet, company_code: str) -> int:
    """Delete existing rows for a company."""
    logger = get_logger()

    # Get all data
    data = worksheet.get_all_values()

    # Find header row
    header_row_idx = 0
    for idx, row in enumerate(data[:3]):
        if '公司代碼' in row:
            header_row_idx = idx
            break

    headers = data[header_row_idx]
    code_col_idx = headers.index('公司代碼')

    # Find rows to delete (in reverse order to avoid index shifting)
    rows_to_delete = []
    for row_idx, row in enumerate(data[header_row_idx + 1:], start=header_row_idx + 2):
        if len(row) > code_col_idx and row[code_col_idx] == company_code:
            rows_to_delete.append(row_idx)

    # Delete in reverse order
    for row_idx in reversed(rows_to_delete):
        worksheet.delete_rows(row_idx)

    logger.info(f"Deleted {len(rows_to_delete)} existing rows for {company_code}")
    return len(rows_to_delete)


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


def run_reextraction(company_codes: list, dry_run: bool = False) -> None:
    """Re-run extraction for specific companies."""
    logger = get_logger()

    # Validate company codes
    valid_companies = []
    for code in company_codes:
        if code not in FINANCE_COMPANIES:
            logger.warning(f"Unknown company code: {code}")
            continue

        pdf_file = find_pdf_for_company(code)
        if not pdf_file:
            logger.warning(f"PDF not found for {code}")
            continue

        valid_companies.append({
            'code': code,
            'name': FINANCE_COMPANIES[code]['name'],
            'industry': FINANCE_COMPANIES[code]['industry'],
            'pdf': pdf_file
        })

    if not valid_companies:
        logger.error("No valid companies to process")
        return

    print(f"\n{'='*60}")
    print("Re-extraction Plan")
    print(f"{'='*60}")
    print(f"Companies to re-extract: {len(valid_companies)}")
    print(f"Target Sheet: {SHEET_NAME}")
    print(f"{'='*60}\n")

    for company in valid_companies:
        fields = get_final_fields(company['industry'])
        print(f"  - {company['name']} ({company['code']}) - {len(fields)} fields")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(valid_companies)} re-extractions? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Setup Google auth
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    # Get or create worksheet
    sheet = gc.open_by_key(OUTPUT_SHEET_ID)
    try:
        worksheet = sheet.worksheet(SHEET_NAME)
        logger.info(f"Found existing worksheet: {SHEET_NAME}")
    except gspread.WorksheetNotFound:
        logger.info(f"Creating new worksheet: {SHEET_NAME}")
        worksheet = sheet.add_worksheet(title=SHEET_NAME, rows=500, cols=20)
        # Add headers
        headers = [
            '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
            '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間'
        ]
        worksheet.append_row(headers)

    # Initialize analyzer
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None  # Disable cache

    # Process each company
    successful = 0
    failed = 0

    for company in tqdm(valid_companies, desc="Processing"):
        company_info = {
            'company_code': company['code'],
            'company_name': company['name'],
            'year': '2024',  # Assuming 2024 reports
            'industry': company['industry']
        }

        logger.info(f"Processing: {company['name']} ({company['code']})")

        try:
            start_time = datetime.now()

            # Upload PDF to Gemini
            pdf_gemini = PDFProcessor.upload_pdf_to_gemini(str(company['pdf']))
            if not pdf_gemini:
                logger.error(f"Failed to upload: {company['pdf'].name}")
                failed += 1
                continue

            try:
                # Get fields for this industry
                final_fields = get_final_fields(company_info['industry'])

                # Build prompt and call API
                prompt = analyzer._build_field_collection_prompt(company_info, final_fields)

                from google import genai
                from google.genai import types

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

                    # Count failures in new results
                    failure_count = sum(
                        1 for r in results
                        if r.get('欄位數值') == '解析失敗' or '解析失敗' in r.get('補充說明', '')
                    )

                    # Append to worksheet
                    count = append_results_to_worksheet(worksheet, results)

                    elapsed = (datetime.now() - start_time).total_seconds()
                    logger.info(
                        f"Completed {company['name']}: {count} fields "
                        f"({failure_count} failures) in {elapsed:.1f}s"
                    )
                    successful += 1
                else:
                    logger.error(f"No response for {company['name']}")
                    failed += 1

            finally:
                # Clean up Gemini file
                PDFProcessor.delete_gemini_file(pdf_gemini.name)

        except Exception as e:
            logger.error(f"Error processing {company['name']}: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print("Re-extraction Complete")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Re-run extraction for specific companies"
    )
    parser.add_argument(
        "companies",
        nargs='+',
        help="Company codes to re-extract (e.g., 2891 2884)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )

    args = parser.parse_args()

    setup_logging(session_name="rerun_failed")

    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        run_reextraction(args.companies, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
