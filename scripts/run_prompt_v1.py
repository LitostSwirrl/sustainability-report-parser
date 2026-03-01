#!/usr/bin/env python3
"""
Run extraction with prompt ver. 5 on verification PDFs.

Processes all 10 companies from verification_pdfs/ and writes results
to a new Google Sheets tab. Ver. 5 includes:
- Water fields (301-310)
- Finance extended fields (401-420) for financial sector

Usage:
    python scripts/run_prompt_v1.py
    python scripts/run_prompt_v1.py --dry-run
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
from src.pdf_processor import PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


# New sheet name for prompt ver. 5 results (with water 301-310 + finance extended 401-420)
NEW_SHEET_NAME = "欄位蒐集結果 26-02-05（prompt ver. 5)"

# Verification PDFs directory
VERIFICATION_DIR = Path(__file__).parent.parent / "verification_pdfs"

# Company info mapping (code -> industry)
COMPANY_INDUSTRIES = {
    "1216": "食品工業",
    "1409": "紡織纖維",
    "1444": "紡織纖維",
    "1451": "紡織纖維",
    "1563": "汽車工業",
    "2023": "鋼鐵工業",
    "2101": "橡膠工業",
    "2313": "電子零組件業",
    "5425": "半導體業",
    "6443": "光電業",
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


def parse_pdf_filename(filename: str) -> dict:
    """
    Parse company info from PDF filename.

    Expected format: {code}_{name}_{year}_永續報告書.pdf
    Example: 1216_統一_2024_永續報告書.pdf
    """
    parts = filename.replace('.pdf', '').split('_')
    if len(parts) >= 3:
        code = parts[0]
        name = parts[1]
        year = parts[2]
        return {
            'company_code': code,
            'company_name': name,
            'year': year,
            'industry': COMPANY_INDUSTRIES.get(code, '未知')
        }
    return None


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
        # Create with instruction row structure
        worksheet = sheet.add_worksheet(title=sheet_name, rows=2000, cols=20)

        # Add instruction row
        worksheet.update_cell(1, 1, "說明：此表格為 prompt ver. 5 的提取結果（含水資源 301-310 + 金融業延伸 401-420）")

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


def run_extraction(dry_run: bool = False) -> None:
    """Run extraction on all verification PDFs."""
    logger = get_logger()

    # Get all PDF files
    pdf_files = sorted(VERIFICATION_DIR.glob("*.pdf"))

    if not pdf_files:
        logger.error(f"No PDF files found in {VERIFICATION_DIR}")
        return

    print(f"\n{'='*60}")
    print("Prompt Ver. 5 Extraction Plan")
    print("(Water 301-310 + Finance Extended 401-420)")
    print(f"{'='*60}")
    print(f"PDF Directory: {VERIFICATION_DIR}")
    print(f"Companies: {len(pdf_files)}")
    print(f"Target Sheet: {NEW_SHEET_NAME}")
    print(f"{'='*60}\n")

    for pdf_file in pdf_files:
        info = parse_pdf_filename(pdf_file.name)
        if info:
            print(f"  - {info['company_name']} ({info['company_code']}) - {info['industry']}")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(pdf_files)} extractions? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Setup Google auth
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    # Create/get worksheet
    worksheet = create_or_get_worksheet(gc, NEW_SHEET_NAME)

    # Initialize analyzer (no cache for fresh extraction)
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None  # Disable cache

    # Process each PDF
    successful = 0
    failed = 0

    for pdf_file in tqdm(pdf_files, desc="Processing"):
        company_info = parse_pdf_filename(pdf_file.name)
        if not company_info:
            logger.warning(f"Could not parse filename: {pdf_file.name}")
            failed += 1
            continue

        logger.info(f"Processing: {company_info['company_name']} ({company_info['company_code']})")

        try:
            start_time = datetime.now()

            # Upload PDF to Gemini
            pdf_gemini = PDFProcessor.upload_pdf_to_gemini(str(pdf_file))
            if not pdf_gemini:
                logger.error(f"Failed to upload: {pdf_file.name}")
                failed += 1
                continue

            try:
                # Get fields for this industry
                final_fields = get_final_fields(company_info['industry'])

                # Build prompt and call API
                prompt = analyzer._build_field_collection_prompt(company_info, final_fields)

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
                    logger.info(f"Completed {company_info['company_name']}: {count} fields in {elapsed:.1f}s")
                    successful += 1
                else:
                    logger.error(f"No response for {company_info['company_name']}")
                    failed += 1

            finally:
                # Clean up Gemini file
                PDFProcessor.delete_gemini_file(pdf_gemini.name)

        except Exception as e:
            logger.error(f"Error processing {company_info['company_name']}: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print("Extraction Complete")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run prompt ver. 5 extraction on verification PDFs (water + finance extended)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )

    args = parser.parse_args()

    setup_logging(session_name="prompt_v1")

    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        run_extraction(dry_run=args.dry_run)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
