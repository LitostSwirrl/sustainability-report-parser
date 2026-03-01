# 輸出格式規範 (Output Format Specification)

> Source: `src/analyzer.py` → `_build_field_collection_prompt()`, `_parse_field_section()`, `_create_empty_field_result()`

---

## 欄位萃取輸出格式

每個欄位的輸出必須使用以下標記格式。The start/end markers are parsed by `_parse_field_collection_response()` using exact string matching.

```
---欄位{N}開始---
欄位數值: [value or empty]
欄位單位: [unit or NA]
補充說明: [source, calculation, max 200 chars]
參考頁數: [p.X, p.Y or NA]
---欄位{N}結束---
```

The markers use the exact field ID as it appears in the field definitions dictionary (e.g., `欄位1`, `欄位101`, `欄位401`).

### Example (with data):

```
---欄位3開始---
欄位數值: 1705790
欄位單位: 公噸CO2e
補充說明: 數據來自GRI 305-1揭露，範疇一與範疇二合計，已包含六種溫室氣體
參考頁數: p.45
---欄位3結束---
```

### Example (no data):

```
---欄位9開始---
欄位數值:
欄位單位: NA
補充說明: 報告書未提及是否取得科學基礎減碳目標(SBT)認證
參考頁數: NA
---欄位9結束---
```

### Parsing behavior (in `_parse_field_section()`):

- `欄位數值:` — value after the colon is trimmed. If the value is `無法填答`, `無`, or `無資料`, it is normalized to empty string `''`.
- `欄位單位:` — stored as-is; defaults to `'NA'` if line is missing.
- `補充說明:` — stored as-is; truncated to 200 characters when saved.
- `參考頁數:` — stored as-is.

If the start/end markers for a field are not found in the response, `_create_empty_field_result()` is called, which fills `欄位數值` with `'解析失敗'` and `補充說明` with `'解析失敗，未找到相關資訊'`.

---

## Google Sheets 輸出格式

Each field result maps to one row in Google Sheets. The column structure is defined by `_parse_field_section()`:

| Column | Python Key | Description |
|--------|-----------|-------------|
| 年份 | `年份` | Report year (e.g., `2024`) |
| 公司代碼 | `公司代碼` | Company stock code (e.g., `2330`) |
| 公司簡稱 | `公司簡稱` | Company short name (e.g., `台積電`) |
| 欄位編號 | `欄位編號` | Field number as string (e.g., `"9"`, `"101"`) |
| 欄位名稱 | `欄位名稱` | Field name from field definitions |
| 欄位數值 | `欄位數值` | Extracted value (empty string if not found) |
| 欄位單位 | `欄位單位` | Unit string |
| 補充說明 | `補充說明` | Notes, truncated to 200 characters |
| 參考頁數 | `參考頁數` | Page references in `p.X` format |
| 處理時間 | `處理時間` | Processing timestamp (`YYYY-MM-DD HH:MM:SS`) |

---

## JSON Output Format (for agentic workflow)

When results are cached to disk via `CacheManager`, the structure is:

```json
{
  "company_info": {
    "company_code": "2330",
    "company_name": "台積電",
    "year": "2024",
    "industry": "半導體",
    "file_link": "https://drive.google.com/..."
  },
  "analysis_results": [
    {
      "年份": "2024",
      "公司代碼": "2330",
      "公司簡稱": "台積電",
      "欄位編號": "1",
      "欄位名稱": "是否承諾淨零排放／碳中和",
      "欄位數值": "承諾2050年達成淨零排放",
      "欄位單位": "NA",
      "補充說明": "報告書p.15明確承諾2050年淨零目標",
      "參考頁數": "p.15",
      "處理時間": "2026-03-02 10:00:00"
    }
  ],
  "processed_at": "2026-03-02T10:00:00.000000",
  "pdf_file_name": "2330_台積電_2024.pdf"
}
```

### Normalized representation for agentic workflow:

```json
{
  "company_code": "2330",
  "company_name": "台積電",
  "year": "2024",
  "industry": "半導體",
  "fields": [
    {
      "field_id": "1",
      "field_name": "是否承諾淨零排放／碳中和",
      "value": "承諾2050年達成淨零排放",
      "unit": "NA",
      "notes": "報告書p.15明確承諾2050年淨零目標",
      "page_refs": "p.15"
    },
    {
      "field_id": "9",
      "field_name": "範疇一/類別一（值）",
      "value": "1234567.8901",
      "unit": "公噸CO2e",
      "notes": "數據來自GRI 305-1揭露，已合併子公司排放量",
      "page_refs": "p.78, p.82"
    }
  ],
  "processed_at": "2026-03-02T10:00:00"
}
```

---

## Field Ordering in Output

Fields appear in the response in the order specified by the prompt. The prompt sorts fields using:

- **V2 (default):** Simple numeric sort — `sorted(keys, key=lambda x: int(x))`. Fields 1, 2, 3 ... 72, 101, 102 ... 110, 201 ... 210 etc.
- **V1 (legacy):** Sort by `display_order` attribute first (for custom GHG field ordering), then by numeric field ID. This allows ISO category fields to be interleaved with Scope 3 categories in a specific logical sequence.

The response parser in `_parse_field_collection_response()` always uses `display_order`-first sorting regardless of version, to ensure consistent output row ordering when writing to Google Sheets.

---

## Value Normalization Rules

These rules apply during parsing (`_parse_field_section()`):

| Raw value | Normalized to |
|-----------|---------------|
| `無法填答` | `''` (empty) |
| `無` | `''` (empty) |
| `無資料` | `''` (empty) |
| _(blank after colon)_ | `''` (empty) |
| Any other value | kept as-is |

The 補充說明 field is hard-truncated at 200 characters before being stored.
