#!/usr/bin/env python3
"""
List companies from Google Sheets for Claude Code workflow.
Outputs JSON with company info: code, name, industry, year, file link, status.

Usage:
    python scripts/list_companies.py
    python scripts/list_companies.py --year 2024
    python scripts/list_companies.py --industry 金融業
    python scripts/list_companies.py --all
    python scripts/list_companies.py --format table
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import (
    COMPANY_LIST_SHEET_ID,
    COMPANY_LIST_SHEET_NAME,
    OUTPUT_SHEET_ID,
    OUTPUT_SHEET_NAME,
    OUTPUT_DIR,
)
from src.utils import setup_logging, get_logger

# Fallback CSV paths to check when Sheets is unavailable
CACHE_CSV_CANDIDATES = [
    Path(__file__).parent.parent / "cache" / "company_list.csv",
    Path(__file__).parent.parent / "output" / "company_list.csv",
]


def setup_google_auth():
    """
    Setup Google Sheets authentication using service account credentials.

    Returns:
        Authenticated gspread client, or None if credentials are missing.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        creds_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            str(Path(__file__).parent.parent / "credentials.json"),
        )
        if not Path(creds_path).exists():
            return None
        creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
        return gspread.authorize(creds)
    except ImportError:
        return None
    except Exception:
        return None


def load_companies_from_sheets(
    gc,
    filter_to_analyze: bool = True,
    year: Optional[str] = None,
    industry: Optional[str] = None,
) -> list[dict]:
    """
    Load company list from Google Sheets and apply optional filters.

    Args:
        gc: Authenticated gspread client.
        filter_to_analyze: If True, only return rows where 待分析 == TRUE.
        year: Filter by 年度 value (e.g. "2024").
        industry: Filter by 產業別 value (e.g. "金融業").

    Returns:
        List of company dicts with normalized keys.
    """
    logger = get_logger()
    try:
        sheet = gc.open_by_key(COMPANY_LIST_SHEET_ID)
        worksheet = sheet.worksheet(COMPANY_LIST_SHEET_NAME)
        data = worksheet.get_all_records()
        logger.info(f"Loaded {len(data)} rows from Sheets")
    except Exception as exc:
        logger.error(f"Failed to read from Google Sheets: {exc}")
        return []

    companies = []
    for row in data:
        if filter_to_analyze:
            flag = str(row.get("待分析", "")).strip().upper()
            if flag not in ("TRUE", "1", "YES", "Y"):
                continue

        year_val = str(row.get("年度", "")).strip()
        industry_val = str(row.get("產業別", "")).strip()

        if year and year_val != str(year):
            continue
        if industry and industry_val != industry:
            continue

        companies.append(
            {
                "company_code": str(row.get("公司代碼", "")).strip(),
                "company_name": str(row.get("公司簡稱", "")).strip(),
                "full_name": str(row.get("公司全名", "")).strip(),
                "industry": industry_val,
                "market": str(row.get("市場別", "")).strip(),
                "year": year_val,
                "file_link": str(row.get("檔案連結", "")).strip(),
                "file_size_mb": str(row.get("檔案大小(MB)", "")).strip(),
                "download_status": str(row.get("下載狀態", "")).strip(),
                "to_analyze": str(row.get("待分析", "")).strip(),
                "notes": str(row.get("備註", "")).strip(),
                "last_updated": str(row.get("最後更新時間", "")).strip(),
            }
        )

    return companies


def load_companies_from_csv(
    csv_path: Path,
    filter_to_analyze: bool = True,
    year: Optional[str] = None,
    industry: Optional[str] = None,
) -> list[dict]:
    """
    Load company list from a cached CSV file as a fallback.

    Args:
        csv_path: Path to the CSV file.
        filter_to_analyze: If True, only return rows where 待分析 == TRUE.
        year: Optional year filter.
        industry: Optional industry filter.

    Returns:
        List of company dicts with normalized keys.
    """
    logger = get_logger()
    try:
        import pandas as pd

        df = pd.read_csv(csv_path, dtype=str, encoding="utf-8-sig")
        logger.info(f"Loaded {len(df)} rows from cached CSV: {csv_path}")
    except Exception as exc:
        logger.error(f"Failed to read cached CSV {csv_path}: {exc}")
        return []

    companies = []
    for _, row in df.iterrows():
        if filter_to_analyze and "待分析" in df.columns:
            flag = str(row.get("待分析", "")).strip().upper()
            if flag not in ("TRUE", "1", "YES", "Y"):
                continue

        year_val = str(row.get("年度", "")).strip()
        industry_val = str(row.get("產業別", "")).strip()

        if year and year_val != str(year):
            continue
        if industry and industry_val != industry:
            continue

        companies.append(
            {
                "company_code": str(row.get("公司代碼", "")).strip(),
                "company_name": str(row.get("公司簡稱", "")).strip(),
                "full_name": str(row.get("公司全名", "")).strip(),
                "industry": industry_val,
                "market": str(row.get("市場別", "")).strip(),
                "year": year_val,
                "file_link": str(row.get("檔案連結", "")).strip(),
                "file_size_mb": str(row.get("檔案大小(MB)", "")).strip(),
                "download_status": str(row.get("下載狀態", "")).strip(),
                "to_analyze": str(row.get("待分析", "")).strip(),
                "notes": str(row.get("備註", "")).strip(),
                "last_updated": str(row.get("最後更新時間", "")).strip(),
            }
        )

    return companies


def format_as_table(companies: list[dict]) -> str:
    """
    Format company list as a human-readable table.

    Args:
        companies: List of company dicts.

    Returns:
        Formatted table string.
    """
    if not companies:
        return "(no companies found)"

    col_widths = {
        "company_code": 8,
        "company_name": 12,
        "industry": 14,
        "year": 6,
        "download_status": 14,
        "file_size_mb": 10,
    }
    header = (
        f"{'Code':<{col_widths['company_code']}} "
        f"{'Name':<{col_widths['company_name']}} "
        f"{'Industry':<{col_widths['industry']}} "
        f"{'Year':<{col_widths['year']}} "
        f"{'DL Status':<{col_widths['download_status']}} "
        f"{'Size(MB)':<{col_widths['file_size_mb']}}"
    )
    separator = "-" * len(header)
    lines = [separator, header, separator]

    for c in companies:
        lines.append(
            f"{c['company_code']:<{col_widths['company_code']}} "
            f"{c['company_name']:<{col_widths['company_name']}} "
            f"{c['industry']:<{col_widths['industry']}} "
            f"{c['year']:<{col_widths['year']}} "
            f"{c['download_status']:<{col_widths['download_status']}} "
            f"{c['file_size_mb']:<{col_widths['file_size_mb']}}"
        )

    lines.append(separator)
    lines.append(f"Total: {len(companies)} companies")
    return "\n".join(lines)


def main() -> None:
    """Main entry point for list_companies script."""
    parser = argparse.ArgumentParser(
        description="List companies from Google Sheets for Claude Code workflow"
    )
    parser.add_argument(
        "--year",
        "-y",
        type=str,
        help="Filter by report year (e.g. 2024)",
    )
    parser.add_argument(
        "--industry",
        "-i",
        type=str,
        help="Filter by industry (e.g. 金融業, 製造業)",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Include all companies, not just those marked 待分析=TRUE",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "table"],
        default="json",
        help="Output format: json (default, machine-readable) or table (human-readable)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging to stderr",
    )

    args = parser.parse_args()

    # Logging: only write to stderr so stdout stays clean for JSON output
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        stream=sys.stderr,
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    setup_logging(session_name="list_companies")
    logger = get_logger()

    filter_to_analyze = not args.all
    companies: list[dict] = []
    source = "unknown"

    # 1. Try Google Sheets
    gc = setup_google_auth()
    if gc is not None:
        logger.info("Google authentication successful, loading from Sheets")
        companies = load_companies_from_sheets(
            gc,
            filter_to_analyze=filter_to_analyze,
            year=args.year,
            industry=args.industry,
        )
        source = "google_sheets"
    else:
        logger.warning("Google Sheets unavailable, falling back to cached CSV")

    # 2. Fallback to cached CSV
    if not companies:
        for csv_path in CACHE_CSV_CANDIDATES:
            if csv_path.exists():
                logger.info(f"Using cached CSV: {csv_path}")
                companies = load_companies_from_csv(
                    csv_path,
                    filter_to_analyze=filter_to_analyze,
                    year=args.year,
                    industry=args.industry,
                )
                source = f"csv:{csv_path}"
                if companies:
                    break

    if not companies:
        logger.error("No company data available from Sheets or cached CSV")
        # Still output valid JSON so callers can detect the empty state
        output = {
            "source": source,
            "count": 0,
            "filters": {"year": args.year, "industry": args.industry, "all": args.all},
            "companies": [],
            "error": "No data source available. Ensure credentials.json exists or a cached CSV is present.",
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.format == "table":
        print(format_as_table(companies))
        print(f"\nSource: {source}")
    else:
        output = {
            "source": source,
            "count": len(companies),
            "filters": {"year": args.year, "industry": args.industry, "all": args.all},
            "companies": companies,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
