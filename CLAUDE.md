# ESG 永續報告書解析器 — Agentic Workflow

## Overview

This project extracts 72-140 ESG fields from sustainability reports (永續報告書).
**Claude Code reads PDFs directly**, extracts structured data following documented
guidelines, and writes results to a local xlsx spreadsheet via utility scripts.

## Quick Start (for a Claude Code session)

```bash
# 1. Check what's been done
python scripts/check_progress.py

# 2. Pick a company
python scripts/list_companies.py --format table

# 3. Read the PDF (place PDFs in analysis/pdfs/)
#    Claude Code reads PDFs directly — no API calls needed

# 4. Extract fields following group prompts (see below)

# 5. Save results as JSON
#    → output/results/{company_code}_{year}_group_{X}.json

# 6. Write to xlsx
python scripts/write_group_results.py output/results/2330_2024_group_a.json

# 7. Merge all groups for a company
python scripts/merge_groups.py 2330 2024
```

## Field Groups

Every company gets **base fields 1-72**. Industry-specific fields are added on top.

| Group | Fields | Focus | Prompt File |
|-------|--------|-------|-------------|
| **A** | 1-8 | 氣候承諾 (Net-zero, SBT, mid-term targets) | `docs/prompts/group_a_climate_commitments.md` |
| **B** | 9-15 | 碳排放 (Scope 1/2/3, Categories 3-6) | `docs/prompts/group_b_ghg_emissions.md` |
| **C** | 16-30 | Scope 3 細項 (GHG Protocol 15 categories) | `docs/prompts/group_c_scope3_detail.md` |
| **D** | 31-72 | 能源/再生能源/氣候行動/勞動/水資源 | `docs/prompts/group_d_energy_resources.md` |
| **E** | (V1 ref) | 勞動安全 V1 reference | `docs/prompts/group_e_labor_safety.md` |
| **F** | (V1 ref) | 水資源 GRI 303 V1 reference | `docs/prompts/group_f_water.md` |
| **G** | 101-110 | 製造業共通 (sustainable activity, BAT, GHG intensity) | `docs/prompts/group_g_manufacturing.md` |
| **H** | 201-295 | 產業專屬 (per-industry, see routing) | `docs/prompts/group_h_industry_specific.md` |
| **I** | 101-104, 401-432 | 金融業 (PCAF, NZBA, PRB) | `docs/prompts/group_i_finance.md` |

## Industry Routing

See `docs/field_definitions/industry_routing.md` for full details.

| Industry | Keywords | Extra Fields |
|----------|----------|-------------|
| 金融 | 金融, 銀行, 保險, 證券, 金控 | Groups A-D + I |
| 水泥 | 水泥, cement, 熟料 | Groups A-D + G + H (201-210) |
| 玻璃 | 玻璃, glass | Groups A-D + G + H (211-220) |
| 石油化學 | 石化, 乙烯, 丙烯 | Groups A-D + G + H (221-235) |
| 鋼鐵 | 鋼鐵, steel | Groups A-D + G + H (236-245) |
| 紡織 | 紡織, textile, 纖維 | Groups A-D + G + H (246-255) |
| 造紙 | 造紙, paper, 紙漿 | Groups A-D + G + H (256-265) |
| 半導體 | 半導體, 晶圓, IC | Groups A-D + G + H (266-275) |
| 平面顯示器 | 面板, LCD, OLED | Groups A-D + G + H (276-285) |
| 電腦設備 | 電腦, computer, 筆電 | Groups A-D + G + H (286-295) |
| 一般製造 | (default) | Groups A-D + G |

## PDF Reading Strategy

Read the entire PDF sequentially in 20-page chunks:
1. Pages 1-20, 21-40, 41-60, etc.
2. Accumulate context across chunks
3. After reading all pages, extract fields per group
4. Start from GRI/SASB appendix when looking for specific data points

## Key Rules

- See `docs/extraction_guidelines.md` for ALL formatting rules
- See `docs/output_format.md` for result structure
- Page references use **printed page number from the PDF footer/header** (the number visible on the page), NOT the PDF viewer position. If a page has no printed number (e.g., cover), use PDF viewer position and note it.
- Numbers: no thousands separator, percentages as decimals
- Empty fields: leave blank, never write 「無」or 「NA」or 「不適用」or 「未揭露」
- Prefer directly reported values over self-calculation from component data

## Output JSON Format

```json
{
  "company_code": "2330",
  "company_name": "台積電",
  "year": "2024",
  "group": "A",
  "fields": [
    {
      "field_id": "1",
      "field_name": "是否承諾淨零排放／碳中和",
      "value": "承諾2050年達成淨零排放",
      "unit": "NA",
      "notes": "報告書p.15明確承諾",
      "page_refs": "p.15"
    }
  ],
  "processed_at": "2026-03-02T10:00:00"
}
```

## Batch Strategy (across sessions)

- Each session processes 3-5 companies
- `scripts/check_progress.py` tracks completion
- Any session can resume where the last left off
- Results are saved incrementally per group

## Project Structure

```
├── CLAUDE.md                              # This file
├── docs/
│   ├── extraction_guidelines.md           # All extraction rules
│   ├── output_format.md                   # Result structure spec
│   ├── field_definitions/                 # Field reference docs
│   │   ├── base_fields.md                 # Fields 1-72
│   │   ├── manufacturing_common_fields.md # Fields 101-110
│   │   ├── finance_fields.md              # Fields 101-104 + 401-432
│   │   ├── industry_*.md                  # Per-industry fields
│   │   └── industry_routing.md            # Classification logic
│   └── prompts/                           # Group extraction prompts
│       ├── group_a_climate_commitments.md
│       ├── group_b_ghg_emissions.md
│       ├── group_c_scope3_detail.md
│       ├── group_d_energy_resources.md
│       ├── group_e_labor_safety.md
│       ├── group_f_water.md
│       ├── group_g_manufacturing.md
│       ├── group_h_industry_specific.md
│       └── group_i_finance.md
├── src/                                   # Core modules (legacy + utils)
│   ├── config.py
│   ├── xlsx_manager.py                    # Local xlsx read/write (active workflow)
│   ├── field_definitions.py               # Source of truth (125KB)
│   ├── analyzer.py                        # Legacy Gemini analyzer
│   ├── pdf_processor.py                   # Sheets/Cache/PDF utils (legacy)
│   └── utils.py
├── scripts/
│   ├── list_companies.py                  # List companies from xlsx
│   ├── check_progress.py                  # Show extraction progress
│   ├── publish_to_xlsx.py                 # Publish CSV results → xlsx
│   ├── write_group_results.py             # Write JSON → xlsx
│   ├── merge_groups.py                    # Merge group JSONs
│   ├── publish_to_sheets.py              # Legacy: publish to Google Sheets
│   └── run_analysis.py                    # Legacy Gemini batch
├── analysis/pdfs/                         # Place PDFs here
├── output/results/                        # Per-company group JSONs
└── validation/                            # Historical validation data
```

## Legacy System

The Gemini-based pipeline (`src/analyzer.py`, `scripts/run_analysis.py`) is preserved
as a fallback. Tag `pre-revamp-backup` marks the last full Gemini-era state.

## Code Style

- Type hints required (no `Any` unless unavoidable)
- Use `logging` module, never `print()` for status
- Early returns, flat code structure
- Chinese comments acceptable for domain terms
- **NEVER commit API keys** — use .env files

## Stack

- **Runtime:** Python 3.10+
- **AI:** Claude Code (agentic) + Gemini API (legacy fallback)
- **Storage:** Local xlsx (`LLM 解析結果.xlsx` via openpyxl), local JSON/CSV
- **PDF:** Claude Code reads PDFs directly
- **Legacy:** Google Sheets API (gspread) — used by legacy scripts only
