# Prompt Version Changelog

This document tracks all changes made to the field extraction prompt for the Sustainability Report Parser.

---

## Version 1 (2026-02-04)

**Sheet Tab**: `欄位蒐集結果 26-02-04（prompt ver. 1)`

### Changes Made

#### A. Global Prompt Additions (`src/analyzer.py`)

Added four new sections after "資料格式要求":

1. **數值格式標準化規則**
   ```
   1. 所有數值不使用千分位符號：寫 1705790，不寫 1,705,790
   2. 小數點保留規定精確度：依各欄位定義的精確度輸出
   3. 百分比以小數表示：38% 應寫為 0.38
   4. 空值處理：找不到資料時完全留空，不寫「無」「無資料」「NA」「0」
   ```

2. **布林值判斷規則**
   ```
   - True: 報告書中明確表示「是」「有」「已取得」「已達成」
   - False: 報告書中明確表示「否」「無」「未取得」「未達成」
   - 留空: 報告書中完全未提及該項目
   - 特別注意：「未揭露」「無資料」應視為「留空」而非 False
   ```

3. **文字欄位輸出規則**
   ```
   - 短文字欄位 (報告邊界、產品類別等): 控制在 50 字以內
   - 中等文字欄位 (減量策略、承諾說明): 控制在 100 字以內
   - 列表欄位 (能源項目、認證): 使用標準格式「項目1: 數值1; 項目2: 數值2;」
   ```

4. **參考頁數標準**
   ```
   1. 優先順序:
      - 首選：GRI 對照表/附錄中的頁碼
      - 次選：SASB 附錄中的頁碼
      - 備選：正文中的頁碼
   2. 格式規範: 統一寫成「p.10」或「p.10, p.12」（單頁或多頁）
   3. 不可缺漏: 每個欄位必須提供參考頁數，若真的找不到寫「NA」
   ```

#### B. Field Definition Changes (`src/field_definitions.py`)

| Field ID | Field Name | Previous Description | New Description |
|----------|------------|---------------------|-----------------|
| 1 | 此份永續報告的邊界 | 主要用來判斷報告書的資料範圍，可能包含統計廠區、事業單位、年份等範圍資訊，以文字紀錄即可 | 報告書的資料範圍。請簡潔列出：1) 主體公司名稱 2) 涵蓋廠區/據點（若有列出）。限50字以內，不需包含時間範圍。 |
| 2 | 是否承諾淨零排放或碳中和 | 請將企業針對淨零承諾的文字敘述重點節錄並輸出，請勿改寫。若無明確承諾，請填「無承諾」。 | 若有淨零/碳中和承諾，請節錄關鍵句（50字以內），包含目標年份。若無明確承諾，填「無承諾」。不需完整引用，只需核心內容。 |
| 25 | 是否說明關鍵減量策略 | 通常會製圖/表說明特定年區間的減碳策略，甚至寫出該策略的減碳預估比例 | 列舉公司主要減碳策略（限5項以內）。格式：「策略1、策略2、策略3」。每項策略用最簡短的名詞描述（如「燃煤改天然氣」「太陽能發電」），不需詳細說明。 |
| 35 | 範疇三減量目標實際作為 | 公司以什麼方式進行範疇三的溫室氣體排放減量 | 公司針對範疇三的減碳作為（限3項以內）。格式：「作為1、作為2、作為3」。若無具體作為，留空。 |
| 37 | 2024年度使用的各種能源項目 | 2024 年用的各種能源，通常可在最後面的附錄查詢得到，請寫出各細項數值。 | 列出2024年各能源使用量。固定格式：「電力: X度; 天然氣: X立方公尺; 柴油: X公秉」依此類推。數值不含千分位。按照報告書中出現的順序列出。 |
| 64 | 單位產品溫室氣體排放強度 | 針對高碳排產業...若有多項產品請列舉 | 選擇報告書中明確標示為「代表性產品」或「主要產品」的碳排放強度數值。若有多項產品，選營收佔比最高者。格式：「數值 單位 (產品名)」 |
| 65 | 產品製程類別或代表性產品名稱 | 請明確填寫企業主要產品的製程類別... | 公司主要產品類別，限3項以內。格式：「產品1、產品2、產品3」。使用報告書中的原始名稱，不需加註解說明。 |

### Motivation

Based on validation analysis of 10 companies × 6 extraction runs (original + 5 re-runs):

| Issue Category | Problem | Solution |
|---------------|---------|----------|
| Numeric Format | Same number appears as "1,705,790" or "1705790" | Added "no thousands separators" rule |
| Text Length | Varying detail levels in text summaries | Added character limits (50/100 chars) |
| List Format | Different delimiters and orderings | Specified exact format with semicolons |
| Boolean/Empty | False vs empty confusion | Clarified True/False/Empty criteria |
| Page References | Different runs cite different pages | Added priority order (GRI → SASB → main text) |

### Expected Improvements

| Metric | Baseline (Ver. 0) | Target (Ver. 1) |
|--------|-------------------|-----------------|
| 100% consistency rate | ~67% | >80% |
| Low consistency (<67%) | ~11% | <5% |
| Page reference consistency | ~33% | >70% |
| Numeric format issues | ~14% | 0% |

---

## Version 0 (2026-01-30)

**Sheet Tab**: `欄位蒐集結果 26-01-30（prompt ver. 0)`

### Description
Initial production version of the extraction prompt.

### Key Features
- 60+ field definitions covering: 報告邊界, 溫室氣體, 能源, 水資源, 廢棄物
- Fields 1-41: Base fields
- Fields 42-56: GRI Scope 3 breakdown
- Fields 57-165: Industry-specific extensions (SASB sectors)

### Known Issues (Discovered in Validation)
- Numeric values sometimes include thousands separators
- Text field lengths vary significantly between runs
- Boolean fields sometimes return empty instead of False
- Page references inconsistent across runs
- List fields use inconsistent delimiters

---

## Future Versions

### Planned Improvements
1. Add field-level examples in prompt
2. Consider two-pass extraction (locate data first, then extract)
3. Add confidence scoring for each extracted value
4. Implement multi-page table handling

### Validation Process
After each prompt change:
1. Run extraction on 3-10 sample companies
2. Run 3-5 times per company to measure consistency
3. Compare against previous version
4. Document improvements/regressions

---

## Assessment Explanation Improvements (2026-02-04)

### Changed File: `scripts/compare_results.py`

The `assess_correctness()` function was updated to provide more detailed explanations in the 判斷說明/備註 column.

### Before (Generic Explanations)
```
"全部6次與原始值一致"
"原始值為空，3/6次提取到值"
"原始有值但5/6次提取為空"
```

### After (Detailed Explanations with Values)
```
"6次提取結果完全一致：「無承諾」"
"原始未填值，3/6次提取到值「236000」，需確認報告書是否有此資料"
"原始值「False」，但5/6次提取為空，可能報告書中難以定位此資料"
"原始值「True」與5/6次提取值「False」不同，多數結果可能更正確"
```

### Key Improvements
1. Shows actual values being compared (truncated to 30 chars for readability)
2. Explains the discrepancy between original and new extractions
3. Provides actionable guidance (e.g., "需確認報告書是否有此資料")
4. Indicates which value might be more correct based on consistency
