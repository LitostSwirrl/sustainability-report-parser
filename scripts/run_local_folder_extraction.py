#!/usr/bin/env python3
"""
Run extraction on all PDFs in a local folder.

Processes all PDFs from the specified local folder and writes results to Google Sheets.

Usage:
    python scripts/run_local_folder_extraction.py --folder "/path/to/pdfs"
    python scripts/run_local_folder_extraction.py --folder "/path/to/pdfs" --tab-name "結果" --dry-run
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

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


def parse_filename_to_company_info(filename: str) -> Optional[Dict]:
    """
    Parse company info from PDF filename.

    Supported formats:
    1. Standard: {year}_{code}_{industry}_{full_name}_{short_name}_永續報告書.pdf
       Example: 2024_1101_水泥工業_臺灣水泥股份有限公司_台泥_永續報告書.pdf

    2. Non-standard: {tax_id}-{company_name}-Report-{year}.pdf
       Example: 84149786-晶元光電股份有限公司-Report-2024.pdf
       These are treated as 一般製造業.
    """
    try:
        name_without_ext = filename.replace('.pdf', '')

        # Try standard format first (underscore-separated)
        if '_永續報告書' in name_without_ext:
            parts = name_without_ext.split('_')
            if len(parts) >= 5:
                year = parts[0]
                code = parts[1]
                industry = parts[2]
                short_name = parts[-2]  # Before 永續報告書

                return {
                    'year': year,
                    'company_code': code,
                    'industry': industry,
                    'company_name': short_name
                }

        # Try non-standard format (dash-separated with -Report-)
        if '-Report-' in name_without_ext:
            parts = name_without_ext.split('-')
            if len(parts) >= 3:
                tax_id = parts[0]
                # Company name may contain dashes, so join everything between first and last parts
                company_name = '-'.join(parts[1:-2]) if len(parts) > 3 else parts[1]
                # Remove common suffixes from company name
                company_name = company_name.replace('股份有限公司', '').replace('有限公司', '')
                year = parts[-1]  # Last part after "Report-"

                return {
                    'year': year,
                    'company_code': tax_id,
                    'industry': '一般製造業',
                    'company_name': company_name
                }

    except Exception:
        pass

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
        worksheet = sheet.add_worksheet(title=sheet_name, rows=15000, cols=15)

        # Add headers
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


def run_extraction(
    folder_paths: list,
    tab_name: str,
    dry_run: bool = False,
    limit: int = None
) -> None:
    """Run extraction on all PDFs in the local folders."""
    logger = get_logger()

    # Collect PDFs from all folders
    pdf_files = []
    for folder_path in folder_paths:
        folder = Path(folder_path)
        if not folder.exists():
            logger.error(f"Folder not found: {folder_path}")
            continue
        pdf_files.extend(sorted(folder.glob("*.pdf")))

    pdf_files = sorted(pdf_files, key=lambda x: x.name)

    if not pdf_files:
        logger.error(f"No PDF files found in {folder_path}")
        return

    # Parse company info and filter valid files
    companies_to_process = []
    for pdf in pdf_files:
        info = parse_filename_to_company_info(pdf.name)
        if info:
            companies_to_process.append({
                'file_path': str(pdf),
                'filename': pdf.name,
                **info
            })
        else:
            logger.warning(f"Could not parse filename: {pdf.name}")

    # Sort by company code
    companies_to_process.sort(key=lambda x: x['company_code'])

    # Apply limit if specified
    if limit:
        companies_to_process = companies_to_process[:limit]

    print(f"\n{'='*60}")
    print("Local Folder Extraction Plan")
    print(f"{'='*60}")
    print(f"Folders: {len(folder_paths)}")
    for fp in folder_paths:
        print(f"  - {fp}")
    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Valid companies: {len(companies_to_process)}")
    print(f"Target Sheet Tab: {tab_name}")
    print(f"{'='*60}\n")

    # Show company list
    print("Companies to process:")
    for i, company in enumerate(companies_to_process, 1):
        fields = get_final_fields(company['industry'])
        print(f"{i:3d}. {company['company_name']} ({company['company_code']}) - {company['industry']} ({len(fields)} fields)")

    print(f"{'='*60}")

    if dry_run:
        print(f"\n[DRY RUN] Would process {len(companies_to_process)} companies")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(companies_to_process)} extractions? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Setup Google auth
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    # Create/get worksheet
    worksheet = create_or_get_worksheet(gc, tab_name)

    # Initialize analyzer (no cache for fresh extraction)
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None  # Disable cache

    # Process each PDF
    successful = 0
    failed = 0

    for company in tqdm(companies_to_process, desc="Processing"):
        logger.info(f"Processing: {company['company_name']} ({company['company_code']})")

        try:
            start_time = datetime.now()

            # Upload PDF to Gemini
            pdf_gemini = PDFProcessor.upload_pdf_to_gemini(company['file_path'])
            if not pdf_gemini:
                logger.error(f"Failed to upload to Gemini: {company['filename']}")
                failed += 1
                continue

            try:
                # Get fields for this industry
                company_info = {
                    'company_code': company['company_code'],
                    'company_name': company['company_name'],
                    'year': company['year'],
                    'industry': company['industry']
                }
                final_fields = get_final_fields(company['industry'])

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
                    logger.info(f"Completed {company['company_name']}: {count} fields in {elapsed:.1f}s")
                    successful += 1
                else:
                    logger.error(f"No response for {company['company_name']}")
                    failed += 1

            finally:
                # Clean up Gemini file
                PDFProcessor.delete_gemini_file(pdf_gemini.name)

        except Exception as e:
            logger.error(f"Error processing {company['company_name']}: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print("Extraction Complete")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")
    print(f"Tab: {tab_name}")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run extraction on all PDFs in a local folder"
    )
    parser.add_argument(
        "--folder", "-f",
        type=str,
        action="append",
        required=True,
        help="Path to local folder containing PDFs (can specify multiple times)"
    )
    parser.add_argument(
        "--tab-name", "-t",
        type=str,
        default="欄位蒐集結果",
        help="Target Google Sheets tab name"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show plan without executing"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of companies to process"
    )

    args = parser.parse_args()

    setup_logging(session_name="local_folder_extraction")

    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        run_extraction(
            folder_paths=args.folder,
            tab_name=args.tab_name,
            dry_run=args.dry_run,
            limit=args.limit
        )
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
