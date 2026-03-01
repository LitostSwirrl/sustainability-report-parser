#!/usr/bin/env python3
"""
Analyze extraction failures from Google Sheets.

Identifies which fields have "解析失敗" and shows patterns.

Usage:
    python scripts/analyze_failures.py
    python scripts/analyze_failures.py --sheet "金融業10家驗證 26-02-05（prompt ver. 5）"
"""

import sys
import os
import argparse
from pathlib import Path
from collections import defaultdict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

from src.config import OUTPUT_SHEET_ID


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


def analyze_failures(sheet_name: str) -> None:
    """Analyze extraction failures from the specified sheet."""
    print(f"\n{'='*60}")
    print(f"Analyzing Failures in: {sheet_name}")
    print(f"{'='*60}\n")

    # Connect to Google Sheets
    print("Connecting to Google Sheets...")
    gc = setup_google_auth()
    sheet = gc.open_by_key(OUTPUT_SHEET_ID)

    try:
        worksheet = sheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        print(f"ERROR: Worksheet '{sheet_name}' not found")
        print("\nAvailable worksheets:")
        for ws in sheet.worksheets():
            print(f"  - {ws.title}")
        return

    # Get all data
    print("Loading data...")
    data = worksheet.get_all_values()

    # Find header row (skip instruction row if exists)
    # Check first few rows to find headers
    header_row_idx = 0
    for idx, row in enumerate(data[:3]):
        if '欄位數值' in row or '公司代碼' in row:
            header_row_idx = idx
            break

    headers = data[header_row_idx]
    rows = data[header_row_idx + 1:]

    print(f"Headers found at row {header_row_idx + 1}: {headers[:5]}...")

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Check for failures
    failures = df[
        (df['欄位數值'].str.contains('解析失敗', na=False)) |
        (df['補充說明'].str.contains('解析失敗', na=False))
    ]

    total_rows = len(df)
    total_failures = len(failures)

    print(f"\nTotal records: {total_rows}")
    print(f"Failures: {total_failures} ({total_failures/total_rows*100:.1f}%)")

    if total_failures == 0:
        print("\n No failures found!")
        return

    # Analyze by company
    print(f"\n{'='*60}")
    print("Failures by Company")
    print(f"{'='*60}")

    company_failures = failures.groupby('公司簡稱').size().sort_values(ascending=False)
    company_totals = df.groupby('公司簡稱').size()

    for company in company_failures.index:
        failed = company_failures[company]
        total = company_totals.get(company, 99)
        print(f"  {company}: {failed}/{total} failures ({failed/total*100:.1f}%)")

    # Analyze by field
    print(f"\n{'='*60}")
    print("Failures by Field (most common)")
    print(f"{'='*60}")

    field_failures = failures.groupby(['欄位編號', '欄位名稱']).size().sort_values(ascending=False)

    for (field_id, field_name), count in field_failures.head(20).items():
        print(f"  欄位 {field_id}: {field_name} - {count} failures")

    # Show field range analysis
    print(f"\n{'='*60}")
    print("Failures by Field Range")
    print(f"{'='*60}")

    field_ranges = defaultdict(int)
    for field_id in failures['欄位編號'].values:
        try:
            fid = int(field_id)
            if fid <= 41:
                field_ranges['基礎欄位 (1-41)'] += 1
            elif fid <= 56:
                field_ranges['Scope 3 欄位 (42-56)'] += 1
            elif fid <= 60:
                field_ranges['金融專屬 (57-60)'] += 1
            elif fid <= 200:
                field_ranges['產業特定 (100-200)'] += 1
            elif fid <= 210:
                field_ranges['勞工安全 (201-210)'] += 1
            elif fid <= 310:
                field_ranges['水資源 (301-310)'] += 1
            elif fid <= 420:
                field_ranges['金融延伸 (401-420)'] += 1
            else:
                field_ranges['其他'] += 1
        except ValueError:
            field_ranges['無法解析'] += 1

    for range_name, count in sorted(field_ranges.items(), key=lambda x: -x[1]):
        print(f"  {range_name}: {count} failures")

    # Export failed fields for reference
    if total_failures > 0:
        output_file = Path(__file__).parent.parent / 'validation' / 'failures_analysis.csv'
        output_file.parent.mkdir(exist_ok=True)
        failures.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n Failure details exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze extraction failures")
    parser.add_argument(
        "--sheet", "-s",
        default="金融業10家驗證 26-02-05（prompt ver. 5）",
        help="Sheet name to analyze"
    )

    args = parser.parse_args()
    analyze_failures(args.sheet)


if __name__ == "__main__":
    main()
