"""
Field Collection Analyzer for Sustainability Reports.

Uses Google Gemini API (google.genai) to extract structured data from PDF reports.
"""

import os
import time
import random
from datetime import datetime
from typing import Dict, List

from google import genai
from google.genai import types

from .config import MODEL_NAME, GEMINI_API_KEY, MAX_RETRIES, BASE_RETRY_DELAY
from .utils import get_logger, log_timing, SessionSummary
from .pdf_processor import PDFProcessor, CacheManager
from .field_definitions import get_final_fields


class FieldCollectionAnalyzer:
    """
    Sustainability report field collection analyzer.

    Extracts 60+ standardized fields from sustainability reports
    using Google Gemini API.
    """

    def __init__(self, cache_manager: CacheManager = None):
        """
        Initialize the analyzer.

        Args:
            cache_manager: Optional CacheManager instance for caching results
        """
        self.logger = get_logger()

        # Configure Gemini API
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.cache_manager = cache_manager or CacheManager()
        self.session_summary = SessionSummary()

        self.logger.info(f"Analyzer initialized with model: {MODEL_NAME}")

    def analyze_company_report_from_drive_with_retry(
        self,
        company_data: Dict,
        max_retries: int = MAX_RETRIES
    ) -> List[Dict]:
        """
        Analyze company report from Google Drive link with retry mechanism.

        Args:
            company_data: Company data dictionary from Google Sheets
            max_retries: Maximum retry attempts

        Returns:
            List of field result dictionaries
        """
        for attempt in range(max_retries + 1):
            try:
                return self.analyze_company_report_from_drive(company_data)
            except Exception as e:
                error_str = str(e)

                # Check for quota/rate limit errors
                is_quota_error = (
                    "429" in error_str or
                    "Resource has been exhausted" in error_str or
                    "quota" in error_str.lower()
                )

                if is_quota_error and attempt < max_retries:
                    delay = BASE_RETRY_DELAY * (2 ** attempt) + random.uniform(0, 10)
                    self.logger.warning(
                        f"API quota limit, attempt {attempt + 1}/{max_retries}. "
                        f"Waiting {delay:.1f}s..."
                    )
                    time.sleep(delay)
                    continue
                elif attempt < max_retries:
                    delay = BASE_RETRY_DELAY + random.uniform(0, 5)
                    self.logger.warning(
                        f"Error, attempt {attempt + 1}/{max_retries}. "
                        f"Retrying in {delay:.1f}s... Error: {e}"
                    )
                    time.sleep(delay)
                    continue
                else:
                    self.logger.error(f"Failed after {max_retries} retries: {e}")
                    company_code = company_data.get('公司代碼', 'unknown')
                    self.session_summary.record_failure(company_code, str(e))
                    return []

        return []

    @log_timing
    def analyze_company_report_from_drive(self, company_data: Dict) -> List[Dict]:
        """
        Analyze company report from Google Drive link.

        Args:
            company_data: Company data dictionary from Google Sheets

        Returns:
            List of field result dictionaries
        """
        company_name = company_data.get('公司簡稱', 'Unknown')
        year = company_data.get('年度', 'Unknown')
        self.logger.info(f"Starting analysis: {company_name} ({year})")

        # Parse company info
        company_info = PDFProcessor.get_company_info_from_sheet_data(company_data)

        # Check cache
        if self.cache_manager.is_cached(company_info['company_code'], company_info['year']):
            self.logger.info(
                f"Loading cached result: {company_info['company_code']}_{company_info['year']}"
            )
            cached_result = self.cache_manager.load_cache(
                company_info['company_code'],
                company_info['year']
            )
            if cached_result:
                results = cached_result.get('analysis_results', [])
                self.session_summary.record_success(
                    company_info['company_code'],
                    len(results)
                )
                return results

        # Download PDF from Google Drive
        file_id = PDFProcessor.extract_drive_file_id(company_info['file_link'])
        if not file_id:
            self.logger.error(f"Could not extract file ID: {company_info['file_link']}")
            return []

        pdf_path = PDFProcessor.download_from_drive(file_id, company_info)
        if not pdf_path:
            self.logger.error(f"PDF download failed: {company_info['company_name']}")
            return []

        try:
            return self.analyze_company_report(pdf_path, company_info)
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise
        finally:
            # Always delete local PDF after processing to save space
            PDFProcessor.delete_local_pdf(pdf_path)

    def analyze_company_report(
        self,
        pdf_path: str,
        company_info: Dict = None
    ) -> List[Dict]:
        """
        Analyze sustainability report and collect field data.

        Args:
            pdf_path: Local path to PDF file
            company_info: Optional company info dictionary

        Returns:
            List of field result dictionaries
        """
        if company_info is None:
            filename = os.path.basename(pdf_path)
            company_info = PDFProcessor.get_company_info_from_filename(filename)

            if not company_info:
                self.logger.error(f"Could not parse company info: {filename}")
                return []

        # Upload PDF to Gemini
        pdf_file = PDFProcessor.upload_pdf_to_gemini(pdf_path)
        if not pdf_file:
            self.logger.error(f"PDF upload failed: {pdf_path}")
            return []

        try:
            # Get field definitions for this company's industry
            final_fields = get_final_fields(company_info.get('industry', ''))

            # Build analysis prompt
            prompt = self._build_field_collection_prompt(company_info, final_fields)

            # Make API call using google.genai
            self.session_summary.record_api_call()
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_uri(
                                file_uri=pdf_file.uri,
                                mime_type="application/pdf"
                            ),
                            types.Part.from_text(text=prompt)
                        ]
                    )
                ]
            )

            if response and response.text:
                results = self._parse_field_collection_response(
                    response.text,
                    company_info,
                    final_fields
                )

                # Save to cache
                cache_data = {
                    'company_info': company_info,
                    'analysis_results': results,
                    'processed_at': datetime.now().isoformat(),
                    'pdf_file_name': os.path.basename(pdf_path)
                }
                self.cache_manager.save_cache(
                    company_info['company_code'],
                    company_info['year'],
                    cache_data
                )

                self.logger.info(
                    f"Analysis complete: {company_info['company_code']} "
                    f"({len(results)} fields)"
                )
                self.session_summary.record_success(
                    company_info['company_code'],
                    len(results)
                )
                return results
            else:
                self.logger.error("API returned no valid response")
                return []

        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise

        finally:
            # Clean up uploaded file from Gemini
            try:
                PDFProcessor.delete_gemini_file(pdf_file.name)
            except Exception:
                pass

    def _build_field_collection_prompt(
        self,
        company_info: Dict[str, str],
        final_fields: Dict
    ) -> str:
        """Build the field collection analysis prompt - IDENTICAL to original notebook."""
        # Build field details
        fields_detail = ""
        sorted_keys = sorted(final_fields.keys(), key=lambda x: int(x))

        for field_id in sorted_keys:
            field_info = final_fields[field_id]
            unit_display = field_info['unit'] if field_info['unit'] != 'NA' else '無單位'

            fields_detail += f"""
### 欄位 {field_id}: {field_info['name']}
- **定義/描述：** {field_info['description']}
- **資料格式：** {field_info['data_format']}
- **單位：** {unit_display}
- **精確度：** {field_info.get('precision', 'NA')}
"""

        total_count = len(final_fields)

        return f"""
你是一位專業的ESG資料分析專家，負責從企業永續報告書中蒐集特定欄位的數據資料。請仔細分析這份{company_info.get('company_name', '企業')}的{company_info.get('year', '')}年永續報告書PDF文件，蒐集以下 {total_count} 個欄位的資料。

## 企業資訊
- **公司名稱：** {company_info.get('company_name', '未知')}
- **公司代號：** {company_info.get('company_code', '未知')}
- **年度：** {company_info.get('year', '未知')}
- **產業別：** {company_info.get('industry', '未知')}

## 🎯 欄位定義與資料蒐集要求
(注意：已包含基礎欄位、GRI Scope 3 擴充欄位，以及依據《永續經濟活動認定參考指引》的產業特定欄位)

{fields_detail}

## 📋 重要分析指引

### 資料蒐集原則：
1. **精確提取：** 如果有換算、加總相關數據，請統一在備註中說明。
2. **數據為主：** 專注於數值、事實的蒐集。
3. **完整搜尋：** 仔細瀏覽報告書所有頁面，包括表格、圖表、附錄、註腳。
4. **準確計算：** 當需要換算或加總時，請確保單位一致、計算正確。
5. 若所需要的數據在最後的 SASB / GRI 準則表就可以查得到，請直接引用。

### 資料格式要求：
## 務必按照所指定的格式紀錄資料
- **String：** 按照個別欄位的說明，輸出原文或者摘要
- **Integer：** 整數數值，年份請轉換為西元年
- **Decimal：** 小數數值，按指定精確度
- **Boolean：** True/False

### 特別注意事項：
## 務必先從最後的 GRI 附錄、SASB 附錄尋找相關資料的頁數，再進行定位
1. **單位統一：** 按照欄位定義的單位格式輸出
2. **數據計算：** 需要加總或換算時，請在補充說明中註明
3. **無資料處理：** 找不到資料時留空 (blank value)，不要填「無」或「無資料」。
4. **頁碼記錄：** 務必記錄資料來源的頁碼（p.1, p.2, p.3...）
5. **溫室氣體分類：**
   - 類別 3 ～ 類別 6 是 ISO/CNS 14064-1 的分類方式。
   - 類別 1 ～ 15 是 GHG Protocol 的分類方式，請特別區分。
   - 若所需要的數據在最後的 SASB / GRI 準則表就可以查得到，請直接引用。

## 🔍 輸出格式要求

請嚴格按照以下格式回答，每個欄位都要有明確的開始和結束標記：

---欄位1開始---
欄位數值: [對應數值]
欄位單位: [對應單位]
補充說明: [相關說明]
參考頁數: [頁碼]
---欄位1結束---

... (依此類推到欄位 {total_count})

## ⚠️ 重要提醒
1. 必須處理全部 {total_count} 個欄位，不可遺漏。
2. 數值要準確，單位要統一。例如指定 GJ 時，就應該主動換算原始資料中為 TJ 或 MJ 的數值。
3. 若「欄位數值」沒有資料，請留空 (blank value)，不要填「無」或「無資料」。
4. 頁碼請統一寫成「p.10, p.12」格式。

請開始分析並按順序輸出欄位的蒐集結果：
"""

    def _parse_field_collection_response(
        self,
        response_text: str,
        company_info: Dict[str, str],
        final_fields: Dict
    ) -> List[Dict]:
        """Parse field collection response from Gemini."""
        results = []
        sorted_keys = sorted(final_fields.keys(), key=lambda x: int(x))

        for field_id in sorted_keys:
            start_marker = f"---欄位{field_id}開始---"
            end_marker = f"---欄位{field_id}結束---"

            start_idx = response_text.find(start_marker)
            end_idx = response_text.find(end_marker)

            if start_idx != -1 and end_idx != -1:
                field_text = response_text[start_idx + len(start_marker):end_idx].strip()
                result = self._parse_field_section(
                    field_text, field_id, company_info, final_fields
                )
                results.append(result)
            else:
                results.append(
                    self._create_empty_field_result(field_id, company_info, final_fields)
                )

        return results

    def _parse_field_section(
        self,
        text: str,
        field_id: str,
        company_info: Dict[str, str],
        final_fields: Dict
    ) -> Dict:
        """Parse a single field section."""
        lines = text.split('\n')

        field_value = ''
        field_unit = 'NA'
        additional_notes = ''
        page_refs = ''

        for line in lines:
            line = line.strip()
            if line.startswith('欄位數值:'):
                field_value = line.replace('欄位數值:', '').strip()
                if field_value in ['無法填答', '無', '無資料']:
                    field_value = ''
            elif line.startswith('欄位單位:'):
                field_unit = line.replace('欄位單位:', '').strip()
            elif line.startswith('補充說明:'):
                additional_notes = line.replace('補充說明:', '').strip()
            elif line.startswith('參考頁數:'):
                page_refs = line.replace('參考頁數:', '').strip()

        field_def = final_fields.get(field_id, {})
        field_name = field_def.get('name', f'未知欄位{field_id}')

        return {
            '年份': company_info.get('year', ''),
            '公司代碼': company_info.get('company_code', ''),
            '公司簡稱': company_info.get('company_name', ''),
            '欄位編號': field_id,
            '欄位名稱': field_name,
            '欄位數值': field_value,
            '欄位單位': field_unit,
            '補充說明': additional_notes[:200],
            '參考頁數': page_refs,
            '處理時間': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _create_empty_field_result(
        self,
        field_id: str,
        company_info: Dict[str, str],
        final_fields: Dict
    ) -> Dict:
        """Create an empty field result for parsing failures."""
        field_def = final_fields.get(field_id, {})
        field_name = field_def.get('name', f'未知欄位{field_id}')

        return {
            '年份': company_info.get('year', ''),
            '公司代碼': company_info.get('company_code', ''),
            '公司簡稱': company_info.get('company_name', ''),
            '欄位編號': field_id,
            '欄位名稱': field_name,
            '欄位數值': '解析失敗',
            '欄位單位': 'NA',
            '補充說明': '解析失敗，未找到相關資訊',
            '參考頁數': '',
            '處理時間': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_session_summary(self) -> str:
        """Get the current session summary."""
        return self.session_summary.get_summary()
