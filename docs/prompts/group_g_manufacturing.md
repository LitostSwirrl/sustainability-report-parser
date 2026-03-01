# Group G: 製造業共通欄位 (Manufacturing Common Fields) — V2

**Fields:** MANUFACTURING_COMMON_FIELDS_V2 (欄位 101-110)
**Applicable to:** All manufacturing companies (non-financial sector), including general manufacturers and all specific industry sub-groups (水泥, 玻璃, 石油化學, 鋼鐵, 紡織, 造紙, 半導體, 平面顯示器, 電腦設備)
**Source:** `src/field_definitions.py` → `MANUFACTURING_COMMON_FIELDS_V2`

These 10 fields are appended after the base fields (1-72) for every manufacturing company. They capture sustainable economic activity ratios (Turnover/CapEx/OpEx), product-level GHG intensity, technology adoption, and intensity improvement targets.

---

## Field Definitions

### 欄位 101: 符合永續指引之營收 (Turnover) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |
| Aspect | 營運 |

**Description:** 辨識企業的營收有多少比例來自於合格的永續經濟活動。若未揭露請留空。

**What qualifies as "永續經濟活動":**
Revenues from products or services aligned with Taiwan's "永續經濟活動認定參考指引" (Taiwan Taxonomy). This includes:
- Renewable energy products / equipment
- Energy-efficient buildings, transport, or industrial equipment
- Low-carbon manufacturing products that meet the technical screening thresholds (附表4-12)
- Waste treatment and recycling services classified as sustainable

**Extraction rules:**
- Keywords: "永續經濟活動營收", "永續指引營收", "綠色產品營收", "ESG營收", "低碳產品比例"
- If the report explicitly states a percentage, use it as-is (convert to decimal, e.g., 15% → 0.15)
- If the report discloses the absolute revenue but not the percentage, calculate: sustainable revenue / total revenue (field 13 in base fields)
- Some reports reference EU Taxonomy or GRI — only count figures explicitly aligned with Taiwan's sustainable economic activity guidelines unless the company's definition is explicitly broader

**Common pitfalls:**
- "Green product revenue" (綠色產品營收) may or may not follow the official taxonomy definition — note in 補充說明 which definition is used
- Do not confuse with "ESG-related initiatives spending" (ESG相關支出) which is an expense, not revenue
- If undisclosed, leave blank — do NOT estimate or proxy from other figures

---

### 欄位 102: 符合永續指引之資本支出 (CapEx) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |
| Aspect | 營運 |

**Description:** 通常指投入於製程改善、節能設備的投資比例。

**What counts as qualifying CapEx:**
Capital expenditures directed toward:
- Energy efficiency upgrades (節能設備)
- Renewable energy installations (再生能源裝置)
- Pollution abatement equipment (污染防治)
- Process decarbonization investments (製程低碳化)
- Circular economy infrastructure (循環經濟)

**Extraction rules:**
- Keywords: "永續資本支出", "永續CapEx", "節能投資", "環保投資占比", "低碳轉型資本支出"
- Decimal format: e.g., 5.3% → 0.053
- Denominator is total capital expenditure for the reporting year
- If only the absolute amount is given (not the ratio), check if total CapEx is disclosed elsewhere to compute the ratio; note the calculation in 補充說明

**Common pitfalls:**
- R&D spending on sustainable products is sometimes bundled with CapEx — flag if definition is ambiguous
- Maintenance CapEx (維護性資本支出) is generally not qualifying unless it specifically replaces high-emission equipment

---

### 欄位 103: 符合永續指引之營運費用 (OpEx) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |
| Aspect | 營運 |

**Description:** 針對永續設備維護、研發等費用比例。

**What counts as qualifying OpEx:**
- Operating costs for maintaining sustainable energy and emission-reduction equipment
- Environmental compliance costs (環境合規費用)
- ESG-related R&D expenditure (永續研發費用)
- Costs for certified green manufacturing processes

**Extraction rules:**
- Keywords: "永續營運費用", "OpEx佔比", "環保費用占比", "ESG費用", "低碳製程費用"
- Same decimal format convention as fields 101-102
- If only an absolute figure is given, divide by total operating costs to compute the ratio

**Common pitfalls:**
- Employee training costs for ESG awareness are rarely qualifying OpEx under strict taxonomy definitions — note if included
- Waste treatment fees (廢棄物處理費) may qualify if linked to circular economy activities

---

### 欄位 104: 單位產品溫室氣體排放強度 (特定製程)

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸CO2e/單位產品 |
| Precision | 0.01 |
| Category | GHG強度 |
| Aspect | 環境 |

**Description:** 選擇報告書中明確標示為「代表性產品」或「主要產品」的碳排放強度數值。若有多項產品，選營收佔比最高者。格式：「數值 單位 (產品名)」。

**Extraction rules:**
- This is a string field; preserve the unit and product name from the report
- Priority: choose the product the company labels as its "主要產品" or "代表性產品"
- If the company provides GHG intensity for multiple products with no priority label, select the product with the highest revenue share (check the products/services chapter)
- Scope: Scope 1 + Scope 2 combined intensity is standard; note if Scope 1-only is used
- Format examples:
  - `"0.45 公噸CO2e/公噸 (鋼筋)"`
  - `"1.23 公斤CO2e/平方公分 (12吋晶圓)"`
  - `"0.89 公噸CO2e/Adt (瓦楞紙板)"`

**Common pitfalls:**
- Do not fill this with an absolute emission figure (e.g., total Scope 1+2 in tCO2e); this must be an intensity per unit product
- Some companies only report energy intensity (GJ/unit), not GHG intensity — if so, leave blank and note in 補充說明
- Industry-specific thresholds for this metric are defined in fields 201-295 (industry-specific modules)

---

### 欄位 105: 產品製程類別或代表性產品名稱

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |
| Aspect | 營運 |

**Description:** 公司主要產品類別，限3項以內。格式：「產品1、產品2、產品3」。使用報告書中的原始名稱，不需加註解說明。

**Extraction rules:**
- Source: company overview, products/services section, or the "主要業務" chapter
- List a maximum of 3 items; choose by revenue contribution (highest first)
- Use the exact product names as written in the report — do not translate or abbreviate
- If only one main product exists, fill with that single item

**Output examples:**
- `"晶圓代工、IC封裝測試"`
- `"水泥熟料、水泥成品、預拌混凝土"`
- `"聚酯短纖、聚酯長纖、回收聚酯"`

**Common pitfalls:**
- Business segments (業務部門) are not the same as products; prefer specific product names
- Avoid generic labels like "製造業", "工業產品" — be specific to the actual output

---

### 欄位 106: 產品年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 依產品單位（公噸、平方公尺等）|
| Precision | 0.0001 |
| Category | 產品資訊 |
| Aspect | 營運 |

**Description:** 2024年該代表性產品的年產量。

**Extraction rules:**
- Record the production volume for the same product named in 欄位 105
- Use the unit from the report (公噸, 萬片, 平方公尺, Adt, etc.)
- If multiple products are listed in 欄位 105, record the production volume for the primary (first-listed) product
- If 2024 data is not yet available (report covers fiscal year not matching calendar year), use the most recent year available and note in 補充說明

**Common pitfalls:**
- "Installed capacity" (設計產能) is not the same as actual production — use actual output
- Some reports express production in value (NTD) rather than physical volume — leave blank if only value-based data is available and note accordingly

---

### 欄位 107: 是否採用最佳可行技術 (BAT)

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 技術採用 |
| Aspect | 環境 |

**Description:** 企業是否採用或規劃採用最佳可行技術來降低碳排放。

**What counts as BAT (Best Available Techniques):**
BAT refers to the most effective techniques for preventing or reducing emissions while remaining economically viable. In the context of Taiwan's Sustainable Finance Guidelines, it appears in manufacturing decarbonization technology adoption:
- Low-temperature calcination for cement
- Electric arc furnace (EAF) for steelmaking
- Pure-oxygen combustion (富氧燃燒) for glass
- Advanced process control (APC) systems
- Carbon capture and utilization (CCU/CCUS)
- Heat recovery / waste heat utilization

**Extraction rules:**
- True if: the report explicitly mentions adopting or planning to adopt best available/advanced techniques for emission reduction
- False if: the report's technology section shows only conventional processes with no mention of BAT or equivalent
- Look in: technology investment section, R&D chapter, energy efficiency measures, climate action plan
- Industry-specific BAT references appear in 附表4-12 of the Taiwan Taxonomy

---

### 欄位 108: 碳排放強度改善目標年

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | 西元年 |
| Precision | NA |
| Category | 氣候行動 |
| Aspect | 氣候指標 |

**Description:** 企業設定達成特定碳排放強度目標的年份。

**Extraction rules:**
- This is specifically for product-level GHG intensity reduction targets, not absolute emission targets
- Keywords: "碳排放強度目標", "排放強度改善", "單位產品排碳目標", "intensity target year"
- If only an absolute emission reduction target year is available, do NOT fill this field — leave blank
- Record the western calendar year (西元年) as an integer (e.g., 2030)

**Common pitfalls:**
- Distinguish between "absolute reduction target year" (absolute) and "intensity reduction target year" (per-unit) — this field is for intensity only
- If multiple intensity targets exist for different products, record the earliest target year and note the others in 補充說明

---

### 欄位 109: 碳排放強度改善目標值

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/單位產品 |
| Precision | 0.0001 |
| Category | 氣候行動 |
| Aspect | 氣候指標 |

**Description:** 企業設定的碳排放強度目標值。

**Extraction rules:**
- Record the target intensity value (not the reduction percentage, but the absolute target intensity)
- If the report only states a reduction percentage (e.g., "reduce by 20% from 2020 level"), and the 2020 baseline intensity is known, calculate the target: baseline × (1 - reduction rate). Note the calculation in 補充說明
- Match the unit to 欄位 104 (same product, same unit denominator)
- If the target is expressed in different units, convert and note the conversion

**Common pitfalls:**
- "20% reduction" is NOT a target value — it is a reduction rate; you must know the baseline to compute the target value
- If the baseline is not disclosed, leave this field blank and record only the reduction rate in 補充說明

---

### 欄位 110: 製程能源效率指標

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | GJ/公噸 |
| Precision | 0.0001 |
| Category | 能源效率 |
| Aspect | 環境 |

**Description:** 單位產品能源消耗量 (GJ/公噸產品)。

**Extraction rules:**
- Keywords: "製程能源效率", "單位能耗", "能源強度", "Energy Intensity", "GJ/tonne", "GJ/公噸"
- Convert to GJ/公噸 if needed:
  - If reported in MJ/公噸: divide by 1,000
  - If reported in kWh/公噸: multiply by 0.0036
  - If reported in Mcal/公噸: multiply by 0.004184
- Choose the same representative product as in 欄位 104-106

**Common pitfalls:**
- Total site energy intensity (GJ/NTD or GJ/employee) is not the same as process energy intensity (GJ/公噸 product) — use process-level data
- If the unit is per square metre or per piece (for electronics), record as-is and note the unit difference in 補充說明 since the field assumes GJ/公噸

---

## Output Format

```
欄位 101: [Value]
補充說明: [Definition used, data source, any calculation notes]

欄位 102: [Value]
補充說明: [...]

...

欄位 110: [Value]
補充說明: [...]
```

If a field cannot be filled:
```
欄位 [ID]: 無法填答
補充說明: [Reason — not disclosed, wrong unit, scope mismatch, etc.]
```

---

## Common Search Locations

| Field | Primary Location | Secondary Location |
|-------|------------------|--------------------|
| 101-103 | Sustainability performance summary / ESG KPI table | Financial report MD&A section, green finance chapter |
| 104, 109-110 | Product carbon footprint section | Environmental data appendix, GRI 305/302 disclosure |
| 105-106 | Company overview / business description | Annual report operations section |
| 107 | Technology investment / R&D chapter | Climate action / decarbonization roadmap |
| 108-109 | Climate targets section | TCFD report, sustainability goals table |

---

## Relationship to Industry-Specific Fields

Fields 101-110 are the **common** manufacturing layer. For companies in specific industries, additional fields (201-295) provide more granular product-level data:

- 水泥: 欄位 201-210 (CEMENT_FIELDS) — see `docs/field_definitions/industry_routing.md`
- 玻璃: 欄位 211-220 (GLASS_FIELDS)
- 石油化學: 欄位 221-235 (PETROCHEMICAL_FIELDS)
- 鋼鐵: 欄位 236-245 (STEEL_FIELDS)
- 紡織: 欄位 246-255 (TEXTILE_FIELDS)
- 造紙: 欄位 256-265 (PAPER_FIELDS)
- 半導體: 欄位 266-275 (SEMICONDUCTOR_FIELDS)
- 平面顯示器: 欄位 276-285 (DISPLAY_PANEL_FIELDS)
- 電腦設備: 欄位 286-295 (COMPUTER_EQUIPMENT_FIELDS)

For industry-specific field extraction guidance, see `docs/prompts/group_h_industry_specific.md`.
