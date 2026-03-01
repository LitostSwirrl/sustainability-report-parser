#!/usr/bin/env python3
"""
Run extraction on all PDFs in a Google Drive folder.

Processes all PDFs from the specified Drive folder and writes results to Google Sheets.

Usage:
    python scripts/run_drive_folder_extraction.py --folder-id "1VrNNXjLq6KDEOTIExx4K_lenGCWeDzx8"
    python scripts/run_drive_folder_extraction.py --folder-id "..." --tab-name "結果" --dry-run
"""

import sys
import os
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from tqdm import tqdm
import io

from src.config import OUTPUT_SHEET_ID, CACHE_DIR, validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


def setup_google_auth():
    """Setup Google authentication for both Sheets and Drive."""
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
    gc = gspread.authorize(creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return gc, drive_service


def list_pdfs_in_folder(drive_service, folder_id: str, recursive: bool = True) -> List[Dict]:
    """
    List all PDF files in a Google Drive folder.

    Args:
        drive_service: Google Drive API service
        folder_id: Google Drive folder ID
        recursive: If True, search subfolders too

    Returns:
        List of file metadata dicts with id, name, parents
    """
    logger = get_logger()
    all_files = []

    def search_folder(fid: str):
        query = f"'{fid}' in parents and trashed = false"
        page_token = None

        while True:
            results = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, parents)',
                pageToken=page_token,
                pageSize=100
            ).execute()

            items = results.get('files', [])

            for item in items:
                if item['mimeType'] == 'application/pdf':
                    all_files.append(item)
                elif item['mimeType'] == 'application/vnd.google-apps.folder' and recursive:
                    # Recurse into subfolder
                    search_folder(item['id'])

            page_token = results.get('nextPageToken')
            if not page_token:
                break

    search_folder(folder_id)
    logger.info(f"Found {len(all_files)} PDF files in folder")
    return all_files


def parse_filename_to_company_info(filename: str) -> Optional[Dict]:
    """
    Parse company info from PDF filename.

    Expected format: {year}_{industry}_{code}_{full_name}_{short_name}_永續報告書.pdf
    Example: 2024_水泥工業_1101_臺灣水泥股份有限公司_台泥_永續報告書.pdf
    """
    try:
        name_without_ext = filename.replace('.pdf', '')
        parts = name_without_ext.split('_')

        if len(parts) >= 5:
            year = parts[0]
            industry = parts[1]
            code = parts[2]
            # Full name might have underscores, short name is second to last
            short_name = parts[-2]  # Before 永續報告書

            return {
                'year': year,
                'industry': industry,
                'company_code': code,
                'company_name': short_name
            }
    except Exception:
        pass

    return None


def download_file_from_drive(drive_service, file_id: str, filename: str, cache_dir: str) -> Optional[str]:
    """Download a file from Google Drive to local cache."""
    logger = get_logger()

    try:
        # Create safe filename
        safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
        local_path = os.path.join(cache_dir, safe_filename)

        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Write to file
        os.makedirs(cache_dir, exist_ok=True)
        with open(local_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

        logger.info(f"Downloaded: {filename} ({os.path.getsize(local_path)} bytes)")
        return local_path

    except Exception as e:
        logger.error(f"Failed to download {filename}: {e}")
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
    folder_id: str,
    tab_name: str,
    dry_run: bool = False,
    limit: int = None
) -> None:
    """Run extraction on all PDFs in the Drive folder."""
    logger = get_logger()

    print(f"\nSetting up Google authentication...")
    gc, drive_service = setup_google_auth()
    print("Authentication successful")

    # List all PDFs in folder
    print(f"\nScanning Google Drive folder...")
    pdf_files = list_pdfs_in_folder(drive_service, folder_id)

    if not pdf_files:
        logger.error(f"No PDF files found in folder {folder_id}")
        return

    # Parse company info and filter valid files
    companies_to_process = []
    for pdf in pdf_files:
        info = parse_filename_to_company_info(pdf['name'])
        if info:
            companies_to_process.append({
                'file_id': pdf['id'],
                'filename': pdf['name'],
                **info
            })
        else:
            logger.warning(f"Could not parse filename: {pdf['name']}")

    # Sort by company code
    companies_to_process.sort(key=lambda x: x['company_code'])

    # Apply limit if specified
    if limit:
        companies_to_process = companies_to_process[:limit]

    print(f"\n{'='*60}")
    print("Drive Folder Extraction Plan")
    print(f"{'='*60}")
    print(f"Folder ID: {folder_id}")
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

    # Create/get worksheet
    worksheet = create_or_get_worksheet(gc, tab_name)

    # Initialize analyzer (no cache for fresh extraction)
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None  # Disable cache

    # Process each PDF
    successful = 0
    failed = 0
    cache_dir = str(CACHE_DIR)

    for company in tqdm(companies_to_process, desc="Processing"):
        logger.info(f"Processing: {company['company_name']} ({company['company_code']})")

        local_path = None
        try:
            start_time = datetime.now()

            # Download PDF from Drive
            local_path = download_file_from_drive(
                drive_service,
                company['file_id'],
                company['filename'],
                cache_dir
            )

            if not local_path:
                logger.error(f"Failed to download: {company['filename']}")
                failed += 1
                continue

            # Upload PDF to Gemini
            pdf_gemini = PDFProcessor.upload_pdf_to_gemini(local_path)
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

        finally:
            # Clean up local file
            if local_path and os.path.exists(local_path):
                try:
                    os.remove(local_path)
                except Exception:
                    pass

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
        description="Run extraction on all PDFs in a Google Drive folder"
    )
    parser.add_argument(
        "--folder-id", "-f",
        type=str,
        required=True,
        help="Google Drive folder ID"
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

    setup_logging(session_name="drive_folder_extraction")

    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        run_extraction(
            folder_id=args.folder_id,
            tab_name=args.tab_name,
            dry_run=args.dry_run,
            limit=args.limit
        )
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
