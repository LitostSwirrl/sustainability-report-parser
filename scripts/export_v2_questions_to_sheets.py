#!/usr/bin/env python3
"""
Export V2 field definitions to Google Sheets as a questions overview tab.
Outputs to: 問題與說明 26-02-11 (prompt ver. 5)
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import gspread
from google.oauth2.service_account import Credentials

from src.config import OUTPUT_SHEET_ID
from src.field_definitions import (
    BASE_FIELDS_V2,
    FINANCE_FIELDS_V2,
    MANUFACTURING_COMMON_FIELDS_V2,
    CEMENT_FIELDS,
    GLASS_FIELDS,
    PETROCHEMICAL_FIELDS,
    STEEL_FIELDS,
    TEXTILE_FIELDS,
    PAPER_FIELDS,
    SEMICONDUCTOR_FIELDS,
    DISPLAY_PANEL_FIELDS,
    COMPUTER_EQUIPMENT_FIELDS,
    FINANCE_EXTENDED_FIELDS,
)


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

    creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
    return gspread.authorize(creds)


def export_to_sheets(gc: gspread.Client, sheet_name: str):
    """Export V2 field definitions to a Google Sheets worksheet."""

    # Define field categories for V2
    field_categories = [
        ("通用欄位 (1-72)", BASE_FIELDS_V2),
        ("金融業 (101-104)", FINANCE_FIELDS_V2),
        ("製造業共通 (101-110)", MANUFACTURING_COMMON_FIELDS_V2),
        ("水泥業 (201-210)", CEMENT_FIELDS),
        ("玻璃業 (211-220)", GLASS_FIELDS),
        ("石化業 (221-235)", PETROCHEMICAL_FIELDS),
        ("鋼鐵業 (236-245)", STEEL_FIELDS),
        ("紡織業 (246-255)", TEXTILE_FIELDS),
        ("造紙業 (256-265)", PAPER_FIELDS),
        ("半導體業 (266-275)", SEMICONDUCTOR_FIELDS),
        ("面板業 (276-285)", DISPLAY_PANEL_FIELDS),
        ("電腦設備業 (286-295)", COMPUTER_EQUIPMENT_FIELDS),
        ("金融業延伸 (401-432)", FINANCE_EXTENDED_FIELDS),
    ]

    rows = []
    for category_name, fields in field_categories:
        for field_id, field_def in sorted(fields.items(), key=lambda x: int(x[0])):
            rows.append([
                field_id,
                field_def['name'],
                field_def['description'],
                field_def['data_format'],
                field_def['unit'],
                field_def.get('precision', 'NA'),
                category_name,
                field_def.get('aspect', ''),
                field_def.get('category', ''),
            ])

    # Connect to sheet
    sheet = gc.open_by_key(OUTPUT_SHEET_ID)

    # Create or get worksheet
    try:
        worksheet = sheet.worksheet(sheet_name)
        # Clear existing data
        worksheet.clear()
        print(f"Cleared existing worksheet: {sheet_name}")
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=sheet_name, rows=500, cols=15)
        print(f"Created new worksheet: {sheet_name}")

    # Write headers
    headers = [
        '欄位編號', '欄位名稱', '定義描述', '資料格式', '單位',
        '精確度', '產業類別', '面向', '分類'
    ]
    worksheet.append_row(headers)

    # Write data
    worksheet.append_rows(rows)

    print(f"Exported {len(rows)} field definitions to '{sheet_name}'")
    return len(rows)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export V2 field definitions to Google Sheets")
    parser.add_argument(
        "--sheet-name",
        type=str,
        default="問題與說明 26-02-11 (prompt ver. 5)",
        help="Target worksheet name"
    )
    args = parser.parse_args()

    print("Setting up Google authentication...")
    gc = setup_google_auth()
    print("Authentication successful")

    print(f"\nExporting to worksheet: {args.sheet_name}")
    count = export_to_sheets(gc, args.sheet_name)

    print(f"\nDone! Exported {count} fields.")


if __name__ == "__main__":
    main()
