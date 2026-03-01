#!/usr/bin/env python3
"""Export all field definitions and prompts to a consolidated CSV file."""

import csv
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from field_definitions import (
    BASE_FIELDS,
    SCOPE3_FIELDS,
    MANUFACTURING_FIELDS,
    FINANCE_FIELDS,
    CEMENT_FIELDS,
    GLASS_FIELDS,
    PETROCHEMICAL_FIELDS,
    STEEL_FIELDS,
    TEXTILE_FIELDS,
    PAPER_FIELDS,
    SEMICONDUCTOR_FIELDS,
    DISPLAY_PANEL_FIELDS,
    COMPUTER_EQUIPMENT_FIELDS,
)

OUTPUT_PATH = Path(__file__).parent.parent / "verification_questions.csv"

def main():
    rows = []

    # Define field categories
    field_categories = [
        ("通用 (1-41)", BASE_FIELDS),
        ("Scope 3 (42-56)", SCOPE3_FIELDS),
        ("金融業 (57-60)", FINANCE_FIELDS),
        ("製造業共通 (61-70)", MANUFACTURING_FIELDS),
        ("水泥業 (71-80)", CEMENT_FIELDS),
        ("玻璃業 (81-90)", GLASS_FIELDS),
        ("石化業 (91-105)", PETROCHEMICAL_FIELDS),
        ("鋼鐵業 (106-115)", STEEL_FIELDS),
        ("紡織業 (116-125)", TEXTILE_FIELDS),
        ("造紙業 (126-135)", PAPER_FIELDS),
        ("半導體業 (136-145)", SEMICONDUCTOR_FIELDS),
        ("面板業 (146-155)", DISPLAY_PANEL_FIELDS),
        ("電腦設備業 (156-165)", COMPUTER_EQUIPMENT_FIELDS),
    ]

    for category_name, fields in field_categories:
        for field_id, field_def in sorted(fields.items(), key=lambda x: int(x[0])):
            rows.append({
                '欄位編號': field_id,
                '欄位名稱': field_def['name'],
                '定義描述': field_def['description'],
                '資料格式': field_def['data_format'],
                '單位': field_def['unit'],
                '精確度': field_def.get('precision', 'NA'),
                '產業類別': category_name,
                '面向': field_def.get('aspect', ''),
                '分類': field_def.get('category', ''),
            })

    # Write CSV
    fieldnames = ['欄位編號', '欄位名稱', '定義描述', '資料格式', '單位', '精確度', '產業類別', '面向', '分類']

    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Exported {len(rows)} field definitions to {OUTPUT_PATH}")
    print(f"  File size: {OUTPUT_PATH.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
