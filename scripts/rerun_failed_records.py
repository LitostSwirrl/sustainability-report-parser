#!/usr/bin/env python3
"""Rerun companies with 解析失敗 records."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from google import genai
from google.genai import types

from src.config import OUTPUT_SHEET_ID, MODEL_NAME, GEMINI_API_KEY
from src.utils import setup_logging, get_logger
from src.pdf_processor import PDFProcessor
from src.analyzer import FieldCollectionAnalyzer
from src.field_definitions import get_final_fields

setup_logging(session_name="rerun_failed_records")
logger = get_logger()

# Companies with 解析失敗
failed_companies = [
    ('1605', '華新'),
    ('1710', '東聯'),
    ('2029', '盛餘'),
    ('2101', '南港'),
    ('2303', '聯電'),
    ('2327', '國巨'),
    ('2409', '友達'),
    ('3049', '精金'),
    ('3711', '日月光投控'),
    ('5347', '世界'),
    ('6116', '彩晶'),
    ('6239', '力成'),
    ('6581', '鋼聯'),
    ('6770', '力積電'),
    ('36550632', '國聯矽業化學'),
    ('84149786', '晶元光電'),
    ('96971313', '中鋼鋁業'),
]

# Find PDFs
folders = [
    Path('/Users/jinsoon/Downloads/排碳大戶要收集的永續報告書'),
    Path('/Users/jinsoon/Downloads/排碳大戶要收集的永續報告書 2')
]

def find_pdf(code, name):
    for folder in folders:
        for pdf in folder.glob('*.pdf'):
            if f'_{code}_' in pdf.name or pdf.name.startswith(f'{code}-'):
                return pdf
    return None

def parse_pdf_info(pdf_path):
    """Parse company info from filename."""
    name = pdf_path.name.replace('.pdf', '')

    if '_永續報告書' in name:
        parts = name.split('_')
        return {
            'year': parts[0],
            'company_code': parts[1],
            'industry': parts[2],
            'company_name': parts[-2]
        }
    elif '-Report-' in name:
        parts = name.split('-')
        company_name = '-'.join(parts[1:-2]) if len(parts) > 3 else parts[1]
        company_name = company_name.replace('股份有限公司', '').replace('有限公司', '')
        return {
            'year': parts[-1],
            'company_code': parts[0],
            'industry': '一般製造業',
            'company_name': company_name
        }
    return None

TAB_NAME = "欄位蒐集結果 26-02-12（prompt ver. 5）"

# Setup Google auth
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']
creds_path = Path(__file__).parent.parent / 'credentials.json'
creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(OUTPUT_SHEET_ID)
worksheet = sheet.worksheet(TAB_NAME)

# Initialize analyzer
analyzer = FieldCollectionAnalyzer()
analyzer.cache_manager = None

# Find and process each company
files_to_process = []
for code, name in failed_companies:
    pdf = find_pdf(code, name)
    if pdf:
        info = parse_pdf_info(pdf)
        if info:
            info['path'] = str(pdf)
            files_to_process.append(info)
            print(f"Found: {info['company_name']} ({info['company_code']})", flush=True)
    else:
        print(f"NOT FOUND: {name} ({code})", flush=True)

print(f"\nReprocessing {len(files_to_process)} companies...", flush=True)

successful = 0
failed = 0

for company in files_to_process:
    print(f"\nProcessing: {company['company_name']} ({company['company_code']})", flush=True)

    try:
        start_time = datetime.now()

        # Upload PDF to Gemini
        pdf_gemini = PDFProcessor.upload_pdf_to_gemini(company['path'])
        if not pdf_gemini:
            print(f"  Failed to upload PDF", flush=True)
            failed += 1
            continue

        try:
            # Get fields
            company_info = {
                'company_code': company['company_code'],
                'company_name': company['company_name'],
                'year': company['year'],
                'industry': company['industry']
            }
            final_fields = get_final_fields(company['industry'])

            # Build prompt and call API
            prompt = analyzer._build_field_collection_prompt(company_info, final_fields)

            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=prompt),
                            types.Part.from_uri(
                                file_uri=pdf_gemini.uri,
                                mime_type="application/pdf"
                            )
                        ]
                    )
                ]
            )

            if response and response.text:
                results = analyzer._parse_field_collection_response(
                    response.text, company_info, final_fields
                )

                # Append to worksheet
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

                worksheet.append_rows(rows_to_add)
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"  ✅ Completed: {len(results)} fields in {elapsed:.1f}s", flush=True)
                successful += 1
            else:
                print(f"  ❌ No response from API", flush=True)
                failed += 1

        finally:
            PDFProcessor.delete_gemini_file(pdf_gemini.name)

    except Exception as e:
        print(f"  ❌ Error: {e}", flush=True)
        failed += 1

print(f"\n{'='*50}", flush=True)
print(f"Reprocessing Complete", flush=True)
print(f"{'='*50}", flush=True)
print(f"Successful: {successful}", flush=True)
print(f"Failed: {failed}", flush=True)
