#!/usr/bin/env python3
"""
Validation script for prompt ver. 1 results.

Runs extractions multiple times per company using local PDFs from verification_pdfs/.
Results are stored in validation_v1/ directory for comparison.

Usage:
    python scripts/run_validation_v1.py --runs 5
    python scripts/run_validation_v1.py --dry-run
    python scripts/run_validation_v1.py --download-only
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

from src.config import OUTPUT_SHEET_ID, MODEL_NAME, GEMINI_API_KEY, validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields


# Sheet name for prompt ver. 1 results
PROMPT_V1_SHEET_NAME = "欄位蒐集結果 26-02-04（prompt ver. 1)"

# Verification PDFs directory
VERIFICATION_DIR = Path(__file__).parent.parent / "verification_pdfs"

# Validation output directory
VALIDATION_DIR = Path(__file__).parent.parent / "validation_v1"

# Company info mapping (code -> industry and name)
COMPANY_INFO = {
    "1216": {"name": "統一", "industry": "食品工業"},
    "1409": {"name": "新纖", "industry": "紡織纖維"},
    "1444": {"name": "力麗", "industry": "紡織纖維"},
    "1451": {"name": "年興", "industry": "紡織纖維"},
    "1563": {"name": "巧新", "industry": "汽車工業"},
    "2023": {"name": "燁輝", "industry": "鋼鐵工業"},
    "2101": {"name": "南港", "industry": "橡膠工業"},
    "2313": {"name": "華通", "industry": "電子零組件業"},
    "5425": {"name": "台半", "industry": "半導體業"},
    "6443": {"name": "元晶", "industry": "光電業"},
}


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
        info = COMPANY_INFO.get(code, {"name": name, "industry": "未知"})
        return {
            'company_code': code,
            'company_name': info['name'],
            'year': year,
            'industry': info['industry']
        }
    return None


def download_original_from_sheets(gc: gspread.Client, output_dir: Path) -> None:
    """Download original extraction results from Google Sheets prompt v1 tab."""
    logger = get_logger()
    original_dir = output_dir / "original"
    original_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading original results from {PROMPT_V1_SHEET_NAME}...")

    try:
        sheet = gc.open_by_key(OUTPUT_SHEET_ID)
        worksheet = sheet.worksheet(PROMPT_V1_SHEET_NAME)

        # Get all values as list of lists to avoid header issues
        all_values = worksheet.get_all_values()

        if len(all_values) < 3:  # Need at least instruction row, header row, and data
            logger.warning("No data found in sheet")
            return

        # Row 1 is instruction row, row 2 is header row
        headers = all_values[1]  # Header row (0-indexed position 1)
        data_rows = all_values[2:]  # Data starts from row 3

        # Create records from data
        all_data = []
        for row in data_rows:
            if not any(row):  # Skip empty rows
                continue
            record = {}
            for i, header in enumerate(headers):
                if header and i < len(row):  # Only use non-empty headers
                    record[header] = row[i]
            if record:
                all_data.append(record)

        if not all_data:
            logger.warning("No data found in sheet")
            return

        # Group by company code
        from collections import defaultdict
        companies = defaultdict(list)

        for row in all_data:
            code = str(row.get('公司代碼', ''))
            if code in COMPANY_INFO:
                companies[code].append(row)

        # Save each company's results
        for code, results in companies.items():
            if not results:
                continue

            year = str(results[0].get('西元年份', '2024'))
            output_file = original_dir / f"{code}_{year}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'company_code': code,
                    'company_name': COMPANY_INFO[code]['name'],
                    'year': year,
                    'source': 'google_sheets_v1',
                    'downloaded_at': datetime.now().isoformat(),
                    'results': results
                }, f, ensure_ascii=False, indent=2)

            logger.info(f"Saved original results: {output_file} ({len(results)} fields)")

    except gspread.WorksheetNotFound:
        logger.error(f"Worksheet not found: {PROMPT_V1_SHEET_NAME}")
        raise


def run_fresh_extraction(pdf_path: Path, company_info: dict, analyzer: FieldCollectionAnalyzer) -> list:
    """Run fresh extraction on a PDF without cache."""
    logger = get_logger()
    from google import genai
    from google.genai import types

    # Upload PDF to Gemini
    pdf_file = PDFProcessor.upload_pdf_to_gemini(str(pdf_path))
    if not pdf_file:
        logger.error(f"Failed to upload: {pdf_path.name}")
        return []

    try:
        # Get fields for this industry
        final_fields = get_final_fields(company_info['industry'])

        # Build prompt
        prompt = analyzer._build_field_collection_prompt(company_info, final_fields)

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
            return analyzer._parse_field_collection_response(
                response.text, company_info, final_fields
            )
        return []

    finally:
        PDFProcessor.delete_gemini_file(pdf_file.name)


def run_validation(num_runs: int = 5, dry_run: bool = False) -> None:
    """
    Run validation extractions for prompt v1.

    Args:
        num_runs: Number of extraction runs per company
        dry_run: If True, show plan without executing
    """
    logger = get_logger()
    VALIDATION_DIR.mkdir(exist_ok=True)

    # Get all PDF files
    pdf_files = sorted(VERIFICATION_DIR.glob("*.pdf"))

    if not pdf_files:
        logger.error(f"No PDF files found in {VERIFICATION_DIR}")
        return

    # Parse company info
    companies = []
    for pdf_file in pdf_files:
        info = parse_pdf_filename(pdf_file.name)
        if info:
            info['pdf_path'] = pdf_file
            companies.append(info)

    # Show plan
    print(f"\n{'='*60}")
    print(f"Prompt v1 Validation Plan")
    print(f"{'='*60}")
    print(f"PDF Directory: {VERIFICATION_DIR}")
    print(f"Companies: {len(companies)}")
    print(f"Runs per company: {num_runs}")
    print(f"Total API calls: {len(companies) * num_runs}")
    print(f"Output directory: {VALIDATION_DIR}")
    print(f"{'='*60}\n")

    for company in companies:
        print(f"  - {company['company_name']} ({company['company_code']}) - {company['industry']}")

    if dry_run:
        print("\n[DRY RUN] No extractions will be performed")
        return

    # Confirm
    confirm = input(f"\nProceed with {len(companies) * num_runs} API calls? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return

    # Setup Google auth and download original
    print("\nSetting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    # Download original results
    download_original_from_sheets(gc, VALIDATION_DIR)

    # Initialize analyzer (no cache)
    analyzer = FieldCollectionAnalyzer()
    analyzer.cache_manager = None

    # Run extractions
    for run_num in range(1, num_runs + 1):
        run_dir = VALIDATION_DIR / f"run_{run_num}"
        run_dir.mkdir(exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Run {run_num}/{num_runs}")
        print(f"{'='*60}")

        for company in tqdm(companies, desc=f"Run {run_num}"):
            code = company['company_code']
            name = company['company_name']
            year = company['year']
            pdf_path = company['pdf_path']

            output_file = run_dir / f"{code}_{year}.json"

            # Skip if already processed
            if output_file.exists():
                logger.info(f"Skipping {name}: already processed in run {run_num}")
                continue

            try:
                logger.info(f"Processing {name} ({code}) - Run {run_num}")
                start_time = datetime.now()

                results = run_fresh_extraction(pdf_path, company, analyzer)

                elapsed = (datetime.now() - start_time).total_seconds()

                # Save results
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'company_code': code,
                        'company_name': name,
                        'year': year,
                        'run_number': run_num,
                        'processed_at': datetime.now().isoformat(),
                        'elapsed_seconds': elapsed,
                        'results': results
                    }, f, ensure_ascii=False, indent=2)

                logger.info(f"Completed {name}: {len(results)} fields in {elapsed:.1f}s")

            except Exception as e:
                logger.error(f"Failed {name}: {e}")

                # Save error record
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'company_code': code,
                        'company_name': name,
                        'year': year,
                        'run_number': run_num,
                        'processed_at': datetime.now().isoformat(),
                        'error': str(e),
                        'results': []
                    }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("Validation Complete!")
    print(f"{'='*60}")
    print(f"Results saved to: {VALIDATION_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Run comparison: python scripts/compare_results.py --source validation_v1")
    print(f"  2. Review: validation_v1/comparison_report_v1.csv")
    print(f"{'='*60}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run validation extractions for prompt v1"
    )
    parser.add_argument(
        "--runs", "-r",
        type=int,
        default=5,
        help="Number of extraction runs per company (default: 5)"
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
    setup_logging(session_name="validation_v1")
    logger = get_logger()

    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    try:
        if args.download_only:
            print("\nSetting up Google authentication...")
            gc = setup_google_auth()
            print("Authentication successful")
            VALIDATION_DIR.mkdir(exist_ok=True)
            download_original_from_sheets(gc, VALIDATION_DIR)
            return

        run_validation(
            num_runs=args.runs,
            dry_run=args.dry_run
        )

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
