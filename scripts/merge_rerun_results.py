#!/usr/bin/env python3
"""
Merge re-run results back into the main sheet.

Replaces failed company rows with corrected data from the re-run sheet.

Usage:
    python scripts/merge_rerun_results.py
"""

import sys
import os
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials

from src.config import OUTPUT_SHEET_ID


MAIN_SHEET = "金融業10家驗證 26-02-05（prompt ver. 5）"
RERUN_SHEET = "金融業重跑 26-02-05（中信金+玉山金）"
COMPANIES_TO_REPLACE = ["2891", "2884"]  # 中信金, 玉山金


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


def merge_results():
    """Merge re-run results into main sheet."""
    print(f"\n{'='*60}")
    print("Merging Re-run Results")
    print(f"{'='*60}")
    print(f"Main sheet: {MAIN_SHEET}")
    print(f"Re-run sheet: {RERUN_SHEET}")
    print(f"Companies to replace: {COMPANIES_TO_REPLACE}")
    print(f"{'='*60}\n")

    # Connect
    print("Connecting to Google Sheets...")
    gc = setup_google_auth()
    spreadsheet = gc.open_by_key(OUTPUT_SHEET_ID)

    main_ws = spreadsheet.worksheet(MAIN_SHEET)
    rerun_ws = spreadsheet.worksheet(RERUN_SHEET)

    # Get all data from main sheet
    print("Loading main sheet data...")
    main_data = main_ws.get_all_values()

    # Find header row
    header_idx = 0
    for idx, row in enumerate(main_data[:3]):
        if '公司代碼' in row:
            header_idx = idx
            break

    headers = main_data[header_idx]
    code_col = headers.index('公司代碼')

    # Find rows to delete (companies to replace)
    rows_to_delete = []
    for row_idx, row in enumerate(main_data[header_idx + 1:], start=header_idx + 2):
        if len(row) > code_col and row[code_col] in COMPANIES_TO_REPLACE:
            rows_to_delete.append(row_idx)

    print(f"Found {len(rows_to_delete)} rows to replace")

    # Delete old rows in batches (reverse order to avoid index shifting)
    print("Deleting old rows...")
    batch_size = 50
    for i in range(0, len(rows_to_delete), batch_size):
        batch = sorted(rows_to_delete[i:i+batch_size], reverse=True)
        for row_idx in batch:
            main_ws.delete_rows(row_idx)
        print(f"  Deleted batch {i//batch_size + 1}")
        time.sleep(2)  # Rate limit

    # Get re-run data
    print("Loading re-run data...")
    rerun_data = rerun_ws.get_all_values()

    # Skip header row in re-run sheet
    rerun_rows = rerun_data[1:]  # Skip header

    # Append new rows
    print(f"Appending {len(rerun_rows)} corrected rows...")
    if rerun_rows:
        main_ws.append_rows(rerun_rows)

    print(f"\n{'='*60}")
    print("Merge Complete!")
    print(f"{'='*60}")
    print(f"Deleted: {len(rows_to_delete)} old rows")
    print(f"Added: {len(rerun_rows)} corrected rows")
    print(f"Sheet: https://docs.google.com/spreadsheets/d/{OUTPUT_SHEET_ID}")
    print(f"{'='*60}")


if __name__ == "__main__":
    merge_results()
