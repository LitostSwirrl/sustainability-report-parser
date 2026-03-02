# Group B: 碳排放 (GHG Emissions — Scope 1, 2, 3 + ISO Categories 3-6)

**Fields:** 9-15
**Focus:** Scope 1, Scope 2, Scope 3 totals; ISO/CNS 14064-1 Categories 3-6; domestic facilities only

---

## PDF Reading Strategy

Read these sections in order:

1. **GRI appendix / GRI index** — search GRI 305-1 (Scope 1), 305-2 (Scope 2), 305-3 (Scope 3) for page cross-references
2. **SASB appendix** — often contains a consolidated GHG table by scope
3. **Environmental performance data table** — usually in the back appendix; look for a table with 類別一、類別二、類別三 columns
4. **GHG inventory chapter** — narrows down if the company splits emissions by facility
5. **Notes/footnotes below GHG tables** — confirms whether overseas facilities are included or excluded

Search keywords: 溫室氣體、碳排放、範疇一、範疇二、範疇三、類別一、類別二、類別三、類別四、類別五、類別六、直接排放、間接排放、GHG盤查、GRI 305

---

## Critical Terminology: Two Classification Systems

Taiwanese sustainability reports use **two different GHG categorization systems**. You must distinguish them carefully.

### System 1: ISO/CNS 14064-1 (類別 1-6)
This is the **Taiwanese national standard** (CNS 14064-1) used by most listed companies in Taiwan.

| 類別 | Description |
|------|-------------|
| 類別一 | 直接溫室氣體排放（燃燒、製程）= Scope 1 |
| 類別二 | 輸入能源的間接溫室氣體排放（外購電力/熱）= Scope 2 |
| 類別三 | 運輸的間接溫室氣體排放（原料/產品運輸）|
| 類別四 | 組織使用的產品所產生的間接溫室氣體排放 |
| 類別五 | 與組織產品使用相關聯的間接溫室氣體排放 |
| 類別六 | 由其他來源產生的間接溫室氣體排放 |

**類別一 = Scope 1, 類別二 = Scope 2. 類別三 through 類別六 collectively correspond to Scope 3.**

### System 2: GHG Protocol (類別 1-15, often written as "Category" or "Cat.")
This is the international standard used by some companies (especially those following GRI 305-3 fully).
- Category 1 = Purchased goods and services
- Category 2 = Capital goods
- Category 3 = Fuel- and energy-related activities
- ... through Category 15 = Investments

**GHG Protocol Categories 1-15 are covered in Group C (fields 16-30), not in this group.**

### Mapping for fields 9-15
- Field 9 → ISO 類別一 (= Scope 1)
- Field 10 → ISO 類別二 (= Scope 2)
- Field 11 → Scope 3 total (= sum of ISO 類別三+四+五+六, or GHG Protocol Cat.1-15 total if the company uses that system)
- Field 12 → ISO 類別三
- Field 13 → ISO 類別四
- Field 14 → ISO 類別五
- Field 15 → ISO 類別六

---

## Field Definitions

### 欄位 9: 範疇一/類別一（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** 溫室氣體排放量中，範疇一（直接排放）的值。若公司有加總值，請填寫總額，**不含海外廠**。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。若沒有2024年資料，請於補充說明註記。
- **Example output:** `123456.7890`

### 欄位 10: 範疇二/類別二（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** 溫室氣體排放量中，範疇二（間接排放/外購電力）的值。若公司有加總值，請填寫總額，不含海外廠。注意：某些公司同時揭露「市場法」(market-based) 和「地點法」(location-based) 數值，請優先採用市場法數值，並在補充說明中說明。
- **Example output:** `89000.1234`

### 欄位 11: 範疇三（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** 溫室氣體排放量中，範疇三（其他間接排放）的總值。**使用報告書揭露的合計值，不限台灣廠區。** 計算優先順序：
  1. 若公司直接給出範疇三總值，使用該數值
  2. 若公司給的是ISO類別三到類別六，請協助加總
  3. 若公司給的是GHG Protocol類別1到15，請協助加總
  若沒有2024年資料，請於補充說明註記並嘗試填入最近年度數值。
- **Example output:** `450000.0000`

### 欄位 12: 類別三（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** ISO/CNS 14064-1**類別三**（運輸的間接溫室氣體排放）的值。此為台灣本土分類中的「類別三」，對應原料及產品的上下游運輸排放。使用報告書揭露的合計值，不限台灣廠區。若公司未採用ISO分類，請留空。
- **Note:** ISO 類別三 ≠ GHG Protocol Category 3。兩者意義不同，請勿混淆。

### 欄位 13: 類別四（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** ISO/CNS 14064-1**類別四**（組織使用的產品所產生的間接溫室氣體排放）的值。使用報告書揭露的合計值，不限台灣廠區。若公司未採用ISO分類，或報告書未揭露，請留空（大多數公司未揭露此類別）。

### 欄位 14: 類別五（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** ISO/CNS 14064-1**類別五**（與組織的產品使用相關聯的間接溫室氣體排放）的值。使用報告書揭露的合計值，不限台灣廠區。若公司未採用ISO分類，或報告書未揭露，請留空。

### 欄位 15: 類別六（值）
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** ISO/CNS 14064-1**類別六**（由其他來源產生的間接溫室氣體排放）的值。使用報告書揭露的合計值，不限台灣廠區。若公司未採用ISO分類，或報告書未揭露，請留空。

---

## Extraction Rules (for this group)

### Boundary Scope by Field

| Fields | Scope | Rule |
|--------|-------|------|
| 9-10 (Scope 1, 2) | **Domestic (Taiwan) only** | Sum only 台灣廠區; exclude 海外廠 |
| 11 (Scope 3 total) | **Reported total (no geographic restriction)** | Use the company's disclosed Scope 3 total as-is |
| 12-15 (ISO 類別三~六) | **Reported total (no geographic restriction)** | Use the company's disclosed category values as-is |

### Domestic vs. overseas facilities (Fields 9-10 only)
- Fields 9-10 collect **domestic (Taiwan) data only**
- If the company provides a combined global total for Scope 1/2, check footnotes or table headers for whether it includes overseas
- If the table clearly separates 台灣 vs. 海外, sum only the 台灣 rows for fields 9-10
- If the report only provides a global figure with no breakdown, use it and note in 補充說明 that overseas may be included

### Fields 11-15: Use reported totals
- Fields 11-15 use the **company's reported total values** without geographic restriction
- Do NOT attempt to subtract overseas facilities from these fields
- If the report provides a Scope 3 total or ISO category totals, use them directly

### How to handle companies using GHG Protocol (not ISO 14064-1)
- Fields 9-10 (Scope 1, Scope 2) apply under both systems — fill directly
- Field 11 (Scope 3 total) — sum GHG Protocol Categories 1-15 if given
- Fields 12-15 (ISO 類別三~六) — these are ISO-specific; if the company only uses GHG Protocol, leave fields 12-15 blank and note in 補充說明

### Market-based vs. location-based Scope 2
- When both are reported, prefer **market-based** for field 10
- Note the methodology used in 補充說明

### Scope 3 calculation when only partial categories are given
- If the company discloses only ISO 類別三 and 類別六 (skipping 4 and 5), sum what is disclosed for field 11
- Note which categories were included in the sum in 補充說明

### Units and conversion
- Standard unit for all fields 9-15 is **公噸CO2e**
- Common conversions needed:
  - 千公噸CO2e (kt CO2e) × 1,000 = 公噸CO2e
  - 百萬公噸CO2e (Mt CO2e) × 1,000,000 = 公噸CO2e
- Do NOT apply any conversion factors yourself to activity data — only convert between CO2e mass units

### Numeric format
- No thousand separators: `1234567.89`, not `1,234,567.89`
- Zero values: if the company explicitly reports 0, fill `0`; if not reported at all, leave blank

---

## Output Format

```
---欄位9開始---
欄位數值: [value or empty]
欄位單位: 公噸CO2e
補充說明: [source section, whether summed/converted, overseas exclusion note — max 200 chars]
參考頁數: [p.X or NA]
---欄位9結束---
```

Example for a company using ISO 14064-1 with facility-level breakdown:

```
---欄位9開始---
欄位數值: 185432.1200
欄位單位: 公噸CO2e
補充說明: GRI附錄溫室氣體盤查表類別一，加總台南廠+桃園廠+新竹廠，已排除越南廠
參考頁數: p.98
---欄位9結束---

---欄位10開始---
欄位數值: 62310.5000
欄位單位: 公噸CO2e
補充說明: 類別二，採市場法計算，使用再生能源憑證折抵後數值
參考頁數: p.98
---欄位10結束---

---欄位11開始---
欄位數值: 89200.0000
欄位單位: 公噸CO2e
補充說明: 範疇三，加總類別三+類別六（類別四、五未揭露），來自p.99環境績效附錄
參考頁數: p.99
---欄位11結束---
```

---

## Common Pitfalls

1. **Confusing ISO categories with GHG Protocol categories**: the most critical mistake. ISO 類別三 (transportation) is NOT the same as GHG Protocol Category 3 (fuel and energy activities). Always determine which system the report uses before mapping numbers to fields.

2. **Including overseas emissions**: many large Taiwanese companies operate globally. Tables that say 「合併報告邊界」often include overseas facilities. Check footnotes for explicit statements like 「含海外廠」or 「台灣廠區」.

3. **Mistaking Scope 2 location-based for market-based**: when a company shows two Scope 2 rows, the lower number is usually market-based (after renewable energy certificates). Use that one.

4. **Treating Scope 3 as zero when only partial categories are disclosed**: if only 類別三 is disclosed, field 11 should equal 類別三, not zero. Note the incomplete disclosure in 補充說明.

5. **Unit confusion at the table level**: some GHG tables use 公噸CO2e in one column and GJ in another. Verify the unit header of the specific column you are reading before recording the value.

6. **2023 vs. 2024 data**: some reports released in 2025 may present 2024 as preliminary and 2023 as the verified figure. Use 2024 data; if not available, use 2023 and note it.

7. **Carbon offset / removal credits**: some Scope 1 figures are shown both gross (before offsets) and net (after offsets). Use the gross figure and note if the report provides net values as well.
