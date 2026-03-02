#!/usr/bin/env python3
"""
Build Agentic CSV — Concatenate per-company combined CSVs into one.

Reads all *_combined.csv files from a results directory and concatenates
them into a single CSV matching the agentic extraction output format.

Usage:
    python scripts/build_agentic_csv.py --input-dir output/results --output output/agentic_v2.csv
    python scripts/build_agentic_csv.py  # uses defaults
"""

import csv
import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR

SHEET_HEADERS = [
    "西元年份",
    "公司代碼",
    "公司簡稱",
    "欄位編號",
    "欄位名稱",
    "欄位數值",
    "欄位單位",
    "補充說明",
    "參考頁數",
    "處理時間",
]


def find_combined_csvs(input_dir: Path) -> list[Path]:
    """Find all *_combined.csv files in the input directory."""
    return sorted(input_dir.glob("*_combined.csv"))


def main():
    parser = ArgumentParser(description="Concatenate per-company CSVs into one agentic CSV")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=OUTPUT_DIR / "results",
        help="Directory containing *_combined.csv files (default: output/results)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR / "agentic_combined.csv",
        help="Output CSV path (default: output/agentic_combined.csv)",
    )
    args = parser.parse_args()

    csv_files = find_combined_csvs(args.input_dir)
    if not csv_files:
        print(f"No *_combined.csv files found in {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    with open(args.output, "w", newline="", encoding="utf-8-sig") as out_fh:
        writer = csv.writer(out_fh)
        writer.writerow(SHEET_HEADERS)

        for csv_path in csv_files:
            with open(csv_path, "r", encoding="utf-8-sig") as in_fh:
                reader = csv.DictReader(in_fh)
                for row in reader:
                    writer.writerow([row.get(h, "") for h in SHEET_HEADERS])
                    total_rows += 1

            print(f"  Added: {csv_path.name}", file=sys.stderr)

    print(f"Written {total_rows} rows from {len(csv_files)} files to {args.output}")


if __name__ == "__main__":
    main()
