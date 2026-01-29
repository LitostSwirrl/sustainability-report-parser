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
from typing import Dict, Optional, List

import requests
import pandas as pd
import gspread
from google import genai

from .config import (
    CACHE_DIR, OUTPUT_DIR, COMPANY_LIST_SHEET_ID, OUTPUT_SHEET_ID,
    COMPANY_LIST_SHEET_NAME, OUTPUT_SHEET_NAME, GEMINI_API_KEY
)
from .utils import get_logger


class PDFProcessor:
    """PDF processing class - uploads PDFs to Gemini for analysis."""

    _client = None

    @classmethod
    def get_client(cls):
        """Get or create Gemini client."""
        if cls._client is None:
            cls._client = genai.Client(api_key=GEMINI_API_KEY)
        return cls._client

    @staticmethod
    def upload_pdf_to_gemini(pdf_path: str):
        """
        Upload PDF file to Gemini.

        Args:
            pdf_path: Local path to the PDF file

        Returns:
            Gemini file object or None if upload fails
        """
        import shutil
        import tempfile

        logger = get_logger()
        temp_path = None
        try:
            client = PDFProcessor.get_client()

            # Handle non-ASCII filenames by copying to temp file with ASCII name
            original_name = os.path.basename(pdf_path)
            try:
                original_name.encode('ascii')
                # Filename is ASCII-safe, upload directly
                pdf_file = client.files.upload(file=pdf_path)
            except UnicodeEncodeError:
                # Filename has non-ASCII chars, copy to temp file
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, "upload.pdf")
                shutil.copy2(pdf_path, temp_path)
                pdf_file = client.files.upload(file=temp_path)

            logger.info(f"PDF uploaded successfully: {pdf_file.display_name}")
            return pdf_file
        except Exception as e:
            logger.error(f"PDF upload failed: {e}")
            return None
        finally:
            # Clean up temp file if created
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    os.rmdir(os.path.dirname(temp_path))
                except Exception:
                    pass

    @staticmethod
    def delete_gemini_file(file_name: str) -> bool:
        """Delete uploaded file from Gemini."""
        logger = get_logger()
        try:
            client = PDFProcessor.get_client()
            client.files.delete(name=file_name)
            logger.info(f"Cleaned up Gemini file: {file_name}")
            return True
        except Exception:
            return False

    @staticmethod
    def delete_local_pdf(pdf_path: str) -> bool:
        """Delete local PDF file after processing to save space."""
        logger = get_logger()
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                logger.info(f"Deleted local PDF: {pdf_path}")
                return True
            return False
        except Exception as e:
            logger.warning(f"Could not delete local PDF: {e}")
            return False

    @staticmethod
    def get_company_info_from_filename(filename: str) -> Dict[str, str]:
        """
        Parse company info from filename (backwards compatible).

        Expected format: 產業類別_公司代碼_公司簡稱_永續報告書_西元年份.pdf
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
        """Parse company info from sheet data."""
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
        """Extract file ID from Google Drive URL."""
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
        Note: Files are temporary and will be deleted after processing.
        """
        logger = get_logger()
        cache_dir = cache_dir or str(CACHE_DIR)

        try:
            filename = (
                f"{company_info['industry']}_{company_info['company_code']}_"
                f"{company_info['company_name']}_永續報告書_{company_info['year']}.pdf"
            )
            local_path = os.path.join(cache_dir, filename)

            # Always re-download (since we delete after processing)
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

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
    """Local cache manager for analysis results (JSON cache, not PDFs)."""

    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir or CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_path(self, company_code: str, year: str) -> Path:
        return self.cache_dir / f"{company_code}_{year}_analysis.json"

    def is_cached(self, company_code: str, year: str) -> bool:
        return self.get_cache_path(company_code, year).exists()

    def save_cache(self, company_code: str, year: str, data: Dict) -> None:
        logger = get_logger()
        cache_path = self.get_cache_path(company_code, year)

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Cache saved: {cache_path}")

    def load_cache(self, company_code: str, year: str) -> Optional[Dict]:
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
        self.gc = gc
        self._combined_csv_path = None

    def get_company_list(self, filter_to_analyze: bool = True) -> pd.DataFrame:
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
        if existing_results is None:
            existing_results = self.get_existing_results()

        if existing_results.empty:
            return 'not_processed'

        company_results = existing_results[
            (existing_results['公司代碼'].astype(str) == str(company_code)) &
            (existing_results['西元年份'].astype(str) == str(year))
        ]

        if company_results.empty:
            return 'not_processed'

        failed_conditions = (
            company_results['補充說明'].str.contains('解析失敗', na=False) |
            company_results['欄位數值'].str.contains('解析失敗', na=False)
        )

        if failed_conditions.any():
            return 'failed'

        if len(company_results) < 60:
            return 'incomplete'

        return 'completed'

    def delete_company_results(self, company_code: str, year: str) -> None:
        logger = get_logger()
        try:
            sheet = self.gc.open_by_key(OUTPUT_SHEET_ID)
            worksheet = sheet.worksheet(OUTPUT_SHEET_NAME)

            all_data = worksheet.get_all_records()

            headers = [
                '西元年份', '公司代碼', '公司簡稱', '欄位編號', '欄位名稱',
                '欄位數值', '欄位單位', '補充說明', '參考頁數', '處理時間'
            ]

            filtered_data = []
            for row in all_data:
                if not (str(row.get('公司代碼', '')) == str(company_code) and
                        str(row.get('西元年份', '')) == str(year)):
                    filtered_data.append([row.get(h, '') for h in headers])

            worksheet.clear()
            worksheet.append_row(headers)
            if filtered_data:
                worksheet.append_rows(filtered_data)

            logger.info(f"Deleted results for {company_code} ({year})")

        except Exception as e:
            logger.error(f"Failed to delete results: {e}")

    def append_results(self, results: List[Dict]) -> None:
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
                logger.info(f"Appended {len(rows_to_add)} results to Google Sheets")

        except Exception as e:
            logger.error(f"Failed to write results: {e}")

    def save_results_to_csv(
        self,
        results: List[Dict],
        company_code: str,
        company_name: str,
        year: str
    ) -> tuple:
        """
        Save results to TWO CSV files:
        1. Per-company CSV: output/{company_code}_{company_name}_{year}.csv
        2. Combined CSV: output/combined_results.csv (appends)

        Returns:
            Tuple of (company_csv_path, combined_csv_path)
        """
        logger = get_logger()
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)

        # 1. Per-company CSV
        company_csv = output_dir / f"{company_code}_{company_name}_{year}.csv"
        df = pd.DataFrame(results)
        df.to_csv(company_csv, index=False, encoding='utf-8-sig')
        logger.info(f"Company CSV saved: {company_csv}")

        # 2. Combined CSV (append mode)
        combined_csv = output_dir / "combined_results.csv"

        if combined_csv.exists():
            # Append without header
            df.to_csv(combined_csv, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            # Create with header
            df.to_csv(combined_csv, index=False, encoding='utf-8-sig')

        logger.info(f"Combined CSV updated: {combined_csv}")

        return str(company_csv), str(combined_csv)
