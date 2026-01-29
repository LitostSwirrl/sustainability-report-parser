"""
PDF processing and data management classes.

Includes:
- PDFProcessor: Handles PDF upload to Gemini and file parsing
- CacheManager: Local caching for analysis results
- SheetsManager: Google Sheets read/write operations
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Optional, List, Any

import requests
import pandas as pd
import gspread
import google.generativeai as genai

from .config import (
    CACHE_DIR, COMPANY_LIST_SHEET_ID, OUTPUT_SHEET_ID,
    COMPANY_LIST_SHEET_NAME, OUTPUT_SHEET_NAME
)
from .utils import get_logger


class PDFProcessor:
    """PDF processing class - uploads PDFs to Gemini for analysis."""

    @staticmethod
    def upload_pdf_to_gemini(pdf_path: str) -> Optional[Any]:
        """
        Upload PDF file to Gemini.

        Args:
            pdf_path: Local path to the PDF file

        Returns:
            Gemini file object or None if upload fails
        """
        logger = get_logger()
        try:
            pdf_file = genai.upload_file(pdf_path)
            logger.info(f"PDF uploaded successfully: {pdf_file.display_name}")
            return pdf_file
        except Exception as e:
            logger.error(f"PDF upload failed: {e}")
            return None

    @staticmethod
    def get_company_info_from_filename(filename: str) -> Dict[str, str]:
        """
        Parse company info from filename (backwards compatible).

        Expected format: 產業類別_公司代碼_公司簡稱_永續報告書_西元年份.pdf

        Args:
            filename: PDF filename

        Returns:
            Dictionary with company info or empty dict if parsing fails
        """
        logger = get_logger()
        try:
            name_without_ext = filename.replace('.pdf', '')
            parts = name_without_ext.split('_')

            if len(parts) >= 5:
                return {
                    'industry': parts[0],
                    'company_code': parts[1],
                    'company_name': parts[2],
                    'year': parts[4]
                }
            else:
                logger.warning(f"Filename format mismatch: {filename}")
                return {}
        except Exception as e:
            logger.error(f"Failed to parse filename: {e}")
            return {}

    @staticmethod
    def get_company_info_from_sheet_data(row_data: Dict) -> Dict[str, str]:
        """
        Parse company info from sheet data.

        Args:
            row_data: Dictionary containing row data from Google Sheets

        Returns:
            Dictionary with standardized company info
        """
        return {
            'company_code': str(row_data.get('公司代碼', '')),
            'company_name': str(row_data.get('公司簡稱', '')),
            'full_name': str(row_data.get('公司全名', '')),
            'industry': str(row_data.get('產業別', '')),
            'market': str(row_data.get('市場別', '')),
            'year': str(row_data.get('年度', '')),
            'download_status': str(row_data.get('下載狀態', '')),
            'file_link': str(row_data.get('檔案連結', '')),
            'file_size': str(row_data.get('檔案大小(MB)', '')),
            'last_updated': str(row_data.get('最後更新時間', '')),
            'notes': str(row_data.get('備註', '')),
            'to_analyze': str(row_data.get('待分析', ''))
        }

    @staticmethod
    def extract_drive_file_id(drive_url: str) -> Optional[str]:
        """
        Extract file ID from Google Drive URL.

        Args:
            drive_url: Google Drive sharing URL

        Returns:
            File ID string or None if extraction fails
        """
        logger = get_logger()
        try:
            patterns = [
                r'/file/d/([a-zA-Z0-9-_]+)',
                r'id=([a-zA-Z0-9-_]+)',
                r'/d/([a-zA-Z0-9-_]+)'
            ]

            for pattern in patterns:
                match = re.search(pattern, drive_url)
                if match:
                    return match.group(1)

            logger.warning(f"Could not extract file ID from URL: {drive_url}")
            return None
        except Exception as e:
            logger.error(f"Failed to extract file ID: {e}")
            return None

    @staticmethod
    def download_from_drive(
        file_id: str,
        company_info: Dict[str, str],
        cache_dir: str = None
    ) -> Optional[str]:
        """
        Download PDF file from Google Drive.

        Args:
            file_id: Google Drive file ID
            company_info: Company information dictionary
            cache_dir: Directory to save downloaded file

        Returns:
            Local file path or None if download fails
        """
        logger = get_logger()
        cache_dir = cache_dir or str(CACHE_DIR)

        try:
            # Build filename
            filename = (
                f"{company_info['industry']}_{company_info['company_code']}_"
                f"{company_info['company_name']}_永續報告書_{company_info['year']}.pdf"
            )
            local_path = os.path.join(cache_dir, filename)

            # If file exists and has reasonable size, use it
            if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
                logger.info(f"File already exists, using cached: {filename}")
                return local_path

            # Build download URL
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

            # Download file
            response = requests.get(download_url, stream=True, timeout=120)

            if response.status_code == 200:
                os.makedirs(cache_dir, exist_ok=True)
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                logger.info(
                    f"File downloaded: {filename} ({os.path.getsize(local_path)} bytes)"
                )
                return local_path
            else:
                logger.error(f"Download failed, HTTP status: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"File download failed: {e}")
            return None


class CacheManager:
    """Local cache manager for analysis results."""

    def __init__(self, cache_dir: str = None):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = Path(cache_dir or CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_path(self, company_code: str, year: str) -> Path:
        """Get cache file path for a company/year combination."""
        return self.cache_dir / f"{company_code}_{year}_analysis.json"

    def is_cached(self, company_code: str, year: str) -> bool:
        """Check if analysis result is cached."""
        return self.get_cache_path(company_code, year).exists()

    def save_cache(self, company_code: str, year: str, data: Dict) -> None:
        """
        Save analysis result to cache.

        Args:
            company_code: Company stock code
            year: Report year
            data: Analysis result data
        """
        logger = get_logger()
        cache_path = self.get_cache_path(company_code, year)

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Cache saved: {cache_path}")

    def load_cache(self, company_code: str, year: str) -> Optional[Dict]:
        """
        Load analysis result from cache.

        Args:
            company_code: Company stock code
            year: Report year

        Returns:
            Cached data dictionary or None if not found
        """
        logger = get_logger()
        cache_path = self.get_cache_path(company_code, year)

        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cache: {e}")

        return None

    def clear_cache(self, company_code: str = None, year: str = None) -> int:
        """
        Clear cache files.

        Args:
            company_code: Optional - clear only this company's cache
            year: Optional - clear only this year's cache

        Returns:
            Number of files deleted
        """
        logger = get_logger()
        deleted = 0

        if company_code and year:
            cache_path = self.get_cache_path(company_code, year)
            if cache_path.exists():
                cache_path.unlink()
                deleted = 1
        else:
            pattern = "*_*_analysis.json"
            for cache_file in self.cache_dir.glob(pattern):
                if company_code and company_code not in cache_file.name:
                    continue
                if year and year not in cache_file.name:
                    continue
                cache_file.unlink()
                deleted += 1

        logger.info(f"Cleared {deleted} cache files")
        return deleted


class SheetsManager:
    """Google Sheets manager for field collection format."""

    def __init__(self, gc: gspread.Client):
        """
        Initialize sheets manager.

        Args:
            gc: Authenticated gspread client
        """
        self.gc = gc

    def get_company_list(self, filter_to_analyze: bool = True) -> pd.DataFrame:
        """
        Get company list from Google Sheets.

        Args:
            filter_to_analyze: If True, only return companies marked for analysis

        Returns:
            DataFrame with company data
        """
        logger = get_logger()
        try:
            sheet = self.gc.open_by_key(COMPANY_LIST_SHEET_ID)
            worksheet = sheet.worksheet(COMPANY_LIST_SHEET_NAME)
            data = worksheet.get_all_records()

            df = pd.DataFrame(data)
            logger.info(f"Loaded {len(df)} companies")

            if filter_to_analyze and '待分析' in df.columns:
                df_filtered = df[df['待分析'].astype(str).str.upper() == 'TRUE']
                logger.info(f"Filtered to {len(df_filtered)} companies for analysis")
                return df_filtered

            return df

        except Exception as e:
            logger.error(f"Failed to get company list: {e}")
            return pd.DataFrame()

    def get_existing_results(self) -> pd.DataFrame:
        """
        Get existing analysis results from Google Sheets.

        Returns:
            DataFrame with existing results
        """
        logger = get_logger()
        try:
            sheet = self.gc.open_by_key(OUTPUT_SHEET_ID)
            try:
                worksheet = sheet.worksheet(OUTPUT_SHEET_NAME)
                data = worksheet.get_all_records()
                return pd.DataFrame(data)
            except gspread.WorksheetNotFound:
                logger.info("Output worksheet not found, returning empty DataFrame")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Failed to get existing results: {e}")
            return pd.DataFrame()

    def check_company_processing_status(
        self,
        company_code: str,
        year: str,
        existing_results: pd.DataFrame = None
    ) -> str:
        """
        Check company processing status.

        Args:
            company_code: Company stock code
            year: Report year
            existing_results: Pre-loaded results DataFrame (recommended)

        Returns:
            Status string: 'not_processed', 'incomplete', 'failed', or 'completed'
        """
        if existing_results is None:
            existing_results = self.get_existing_results()

        if existing_results.empty:
            return 'not_processed'

        # Filter for this company and year
        company_results = existing_results[
            (existing_results['公司代碼'].astype(str) == str(company_code)) &
            (existing_results['西元年份'].astype(str) == str(year))
        ]

        if company_results.empty:
            return 'not_processed'

        # Check for parsing failures
        failed_conditions = (
            company_results['補充說明'].str.contains('解析失敗', na=False) |
            company_results['欄位數值'].str.contains('解析失敗', na=False)
        )

        if failed_conditions.any():
            return 'failed'

        # Check field count (should have 60 fields)
        if len(company_results) < 60:
            return 'incomplete'

        return 'completed'

    def delete_company_results(self, company_code: str, year: str) -> None:
        """
        Delete existing results for a company.

        Args:
            company_code: Company stock code
            year: Report year
        """
        logger = get_logger()
        try:
            sheet = self.gc.open_by_key(OUTPUT_SHEET_ID)
            worksheet = sheet.worksheet(OUTPUT_SHEET_NAME)

            all_data = worksheet.get_all_records()

            # Filter out rows for this company/year
            headers = [
                '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
                '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間'
            ]

            filtered_data = []
            for row in all_data:
                if not (str(row.get('公司代碼', '')) == str(company_code) and
                        str(row.get('西元年份', '')) == str(year)):
                    filtered_data.append([row.get(h, '') for h in headers])

            # Clear and rewrite
            worksheet.clear()
            worksheet.append_row(headers)
            if filtered_data:
                worksheet.append_rows(filtered_data)

            logger.info(f"Deleted results for {company_code} ({year})")

        except Exception as e:
            logger.error(f"Failed to delete results: {e}")

    def append_results(self, results: List[Dict]) -> None:
        """
        Append analysis results to Google Sheets.

        Args:
            results: List of field result dictionaries
        """
        logger = get_logger()
        try:
            sheet = self.gc.open_by_key(OUTPUT_SHEET_ID)

            try:
                worksheet = sheet.worksheet(OUTPUT_SHEET_NAME)
            except gspread.WorksheetNotFound:
                worksheet = sheet.add_worksheet(
                    title=OUTPUT_SHEET_NAME, rows=2000, cols=15
                )
                headers = [
                    '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
                    '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間'
                ]
                worksheet.append_row(headers)

            # Convert results to rows
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

        except Exception as e:
            logger.error(f"Failed to write results: {e}")

    def save_results_to_csv(
        self,
        results: List[Dict],
        output_path: str = None
    ) -> str:
        """
        Save results to local CSV file.

        Args:
            results: List of field result dictionaries
            output_path: Output file path (optional)

        Returns:
            Path to saved CSV file
        """
        logger = get_logger()
        from .config import OUTPUT_DIR
        from datetime import datetime

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"results_{timestamp}.csv"

        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"Results saved to: {output_path}")

        return str(output_path)
