# 永續報告書解析器 (Sustainability Report Parser)

## Project Overview
Local Python tool to parse sustainability reports using Gemini API, extracting 60 standardized fields and storing results in Google Sheets.

## Stack
- **Runtime:** Python 3.10+
- **AI:** Google Gemini API (gemini-3.0-pro preferred)
- **Storage:** Google Sheets API, local CSV backup
- **PDF:** pdfplumber, PyPDF2, Google Drive integration

## Key Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis (limited)
python scripts/run_analysis.py --limit 5

# Test single company
python scripts/test_single.py --company 2330

# Full batch processing
python scripts/batch_process.py

# Dry run (preview without API calls)
python scripts/run_analysis.py --limit 10 --dry-run
```

## Code Style
- Type hints required (no `Any` unless unavoidable)
- All functions must have docstrings
- Use `logging` module, never `print()` for status messages
- Early returns, flat code structure
- Chinese comments are acceptable for domain-specific terms

## Critical Rules
- **NEVER commit API keys** - use .env files
- **ALWAYS log** before/after API calls with timing
- Handle rate limits with exponential backoff
- Validate field extraction results before saving
- Generate summary statistics after each run
- Commit frequently to track progress

## Project Structure
```
src/
├── config.py           # Centralized configuration
├── field_definitions.py # 60 field definitions
├── pdf_processor.py    # PDF upload to Gemini
├── analyzer.py         # Field extraction logic
├── sheets_manager.py   # Google Sheets I/O
└── utils.py            # Logging, retry, helpers

scripts/
├── run_analysis.py     # Main CLI entry point
├── test_single.py      # Single company test
└── batch_process.py    # Full batch processing
```

## Field Definitions
- Fields 1-41: Base fields (報告邊界, 溫室氣體, 能源, 水資源, 廢棄物)
- Fields 42-51: Scope 3 breakdown (15 GHG Protocol categories)
- Fields 52-60: Industry-specific extensions (SASB sectors)

## Logging Requirements
Every run must log:
1. Session start timestamp and configuration
2. Each company processing: start, PDF upload, API call, result
3. Field extraction success/failure counts
4. Any errors with full traceback
5. Session end with duration and summary statistics

## Google Drive Integration
- PDFs are stored in Google Drive
- Use gspread for Sheets access
- Authenticate via service account or OAuth

## Error Handling
- Retry API calls up to 3 times with exponential backoff
- Log all errors but continue batch processing
- Mark failed companies for re-processing
- Save partial results to prevent data loss
