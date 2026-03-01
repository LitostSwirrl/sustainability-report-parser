# Group H: 產業專屬欄位 (Industry-Specific Fields)

**Fields:** Vary by industry (201-295)
**Applicable to:** Manufacturing companies classified into specific industries
**Source:** `src/field_definitions.py` → `classify_industry()`, `_get_industry_specific_guidance()`

This document is a routing guide. It directs you to the correct industry field module based on the company's sector classification, and provides the extraction guidance for each industry's technical screening criteria.

---

## Industry Detection

The system classifies companies using `classify_industry(company_industry: str)` which matches against keyword lists. If no match is found, the company defaults to "一般製造" and only fields 101-110 (Group G) apply.

| Industry | Keywords (any match triggers classification) |
|----------|---------------------------------------------|
| 水泥 | 水泥, cement, 熟料, clinker, 水泥工業 |
| 玻璃 | 玻璃, glass, 平板玻璃, 玻璃陶瓷 |
| 石油化學 | 石化, petrochemical, 乙烯, 丙烯, 聚乙烯, 聚丙烯, 塑膠工業, 化學工業 |
| 鋼鐵 | 鋼鐵, steel, 煉鋼, 鋼材, 鋼鐵工業 |
| 紡織 | 紡織, textile, 纖維, 紡紗, 織布, 染整, 紡織纖維 |
| 造紙 | 造紙, paper, 紙漿, 紙板, 造紙工業 |
| 半導體 | 半導體, semiconductor, 晶圓, IC, 半導體業 |
| 平面顯示器 | 面板, display, TFT, LCD, OLED, 顯示器, 光電業 |
| 電腦設備 | 電腦, computer, 筆電, 伺服器, 週邊, 電腦及週邊設備業 |

---

## Industry to Field File Mapping

| Industry | Fields | Technical Standard |
|----------|--------|--------------------|
| 水泥 | 201-210 | 附表4 |
| 玻璃 | 211-220 | 附表5 |
| 石油化學 | 221-235 | 附表6 |
| 鋼鐵 | 236-245 | 附表7 |
| 紡織 | 246-255 | 附表8 |
| 造紙 | 256-265 | 附表9 |
| 半導體 | 266-275 | 附表10 |
| 平面顯示器 | 276-285 | 附表11 |
| 電腦設備 | 286-295 | 附表12 |

---

## How to Use

1. Determine the company's industry (from the company list metadata or the report's "主要業務" section)
2. Apply the corresponding field module below
3. Extract only the fields applicable to that industry
4. Pay special attention to the technical screening thresholds — the final boolean field of each module (`210`, `220`, `235`, `245`, `255`, `265`, `275`, `285`, `295`) asks whether the company meets the sustainable economic activity criteria

---

## Water泥産業 (Cement) — 欄位 201-210

**Technical Standard:** 《永續經濟活動認定參考指引第二版》附表4

### Core Technical Screening Criteria:
- Water cement clinker (水泥熟料) unit GHG emissions (Scope 1 + Scope 2) <= 0.90 tCO2e/tonne
- Finished cement (水泥成品) unit GHG emissions (Scope 1 + Scope 2) <= 0.87 tCO2e/tonne

### Field Definitions:

**欄位 201: 水泥熟料年產量**
- Format: decimal, unit: 公噸
- 2024年水泥熟料 (Clinker) 生產量。Search for "熟料產量", "Clinker production".

**欄位 202: 水泥熟料單位溫室氣體排放量 (範疇一+範疇二)**
- Format: decimal, unit: 公噸CO2e/公噸, precision: 0.0001
- Technical screening threshold: <= 0.90 公噸CO2e/公噸
- Search for "熟料排放強度", "Clinker emission intensity", "單位熟料碳排"

**欄位 203: 水泥成品年產量**
- Format: decimal, unit: 公噸
- 2024年水泥成品（包含各種類型水泥）生產量。

**欄位 204: 水泥成品單位溫室氣體排放量 (範疇一+範疇二)**
- Format: decimal, unit: 公噸CO2e/公噸, precision: 0.0001
- Technical screening threshold: <= 0.87 公噸CO2e/公噸
- Search for "水泥排放強度", "Cement emission intensity"

**欄位 205: 替代原料使用比例**
- Format: decimal, unit: 百分比, precision: 0.01
- 使用廢棄物、副產品等替代原料佔總原料使用量之比例。
- Search for "替代原料", "廢棄物替代", "原料替代率"

**欄位 206: 替代燃料使用比例**
- Format: decimal, unit: 百分比, precision: 0.01
- 使用廢棄物衍生燃料等替代燃料佔總燃料使用量之比例。
- Search for "替代燃料", "廢棄物衍生燃料", "Refuse Derived Fuel (RDF)"

**欄位 207: 水泥窯協同處理廢棄物量**
- Format: decimal, unit: 公噸, precision: 0.0001
- 利用水泥窯協同處理廢棄物的年處理量。
- Search for "協同處理", "水泥窯廢棄物", "co-processing"

**欄位 208: 熟料/水泥比 (Clinker Factor)**
- Format: decimal, unit: 百分比, precision: 0.01
- 水泥產品中熟料含量佔比，數值越低表示使用更多替代性膠凝材料。
- Search for "熟料係數", "Clinker Factor", "熟料比"

**欄位 209: CCUS技術應用情形**
- Format: string
- 是否應用碳捕捉、利用與封存技術，以及年碳捕捉量。
- Search for "CCUS", "碳捕捉", "CCS", "Carbon Capture"

**欄位 210: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if: 熟料 <= 0.90 AND 水泥成品 <= 0.87 公噸CO2e/公噸
- Derive from fields 202 and 204

### Key Search Terms: 水泥熟料 (Clinker), 熟料係數 (Clinker Factor), 替代原料, CCUS
### Data Locations: 環境永續/氣候變遷章節, 產品碳足跡, GRI 305, 附錄環境數據統計表

---

## 玻璃産業 (Glass) — 欄位 211-220

**Technical Standard:** 附表5

### Core Technical Screening Criterion:
- Flat glass (平板玻璃) unit GHG emissions (Scope 1 + Scope 2) <= 1.0121 tCO2e/tonne

### Field Definitions:

**欄位 211: 主要玻璃產品類型**
- Format: string
- 說明主要生產的玻璃產品類型：平板玻璃、板狀玻璃、浮法玻璃、或其他玻璃製品。

**欄位 212: 平板玻璃年產量**
- Format: decimal, unit: 公噸, precision: 0.0001
- 2024年平板玻璃 (Flat Glass) 總產量。

**欄位 213: 平板玻璃單位溫室氣體排放量 (範疇一+範疇二)**
- Format: decimal, unit: 公噸CO2e/公噸, precision: 0.0001
- Technical screening threshold: <= 1.0121 公噸CO2e/公噸

**欄位 214: 玻璃碎片（廢玻璃）使用比例**
- Format: decimal, unit: 百分比, precision: 0.01
- 回收玻璃碎片 (Cullet) 佔總原料投入之比例。

**欄位 215: 玻璃窯爐製程能源消耗量**
- Format: decimal, unit: GJ/公噸, precision: 0.0001
- 單位產品能源消耗量（熔爐能源效率）。

**欄位 216: 窯爐類型與技術**
- Format: string
- 浮法窯、電熔窯、純氧燃燒技術等。

**欄位 217: 替代燃料使用情形**
- Format: string
- 是否使用替代燃料（如：生質能、廢棄物衍生燃料）及使用比例。

**欄位 218: 產品碳足跡驗證情形**
- Format: boolean
- 是否取得產品碳足跡標籤或環保標章認證。

**欄位 219: 製程NOx或SOx減量措施**
- Format: string
- 空氣污染物減量技術採用情形（如：脫硝、脫硫設備）。

**欄位 220: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if: 平板玻璃單位GHG排放量 <= 1.0121 公噸CO2e/公噸

### Key Search Terms: 平板玻璃, 浮法玻璃, 窯爐, Cullet (廢玻璃), 能源效率
### Data Locations: 環境績效數據章節, 產品碳足跡資訊, 循環經濟章節

---

## 石油化學産業 (Petrochemical) — 欄位 221-235

**Technical Standard:** 附表6

### Core Technical Screening Criteria (by product):

| Product | Threshold (公噸CO2e/公噸) |
|---------|---------------------------|
| 乙烯、丙烯、丁二烯 | <= 0.9400 |
| 苯乙烯 | <= 1.0551 |
| 氯乙烯 (VCM) | <= 0.5026 |
| 乙二醇 | <= 2.0750 |
| 酚/丙酮 | <= 0.8741 |
| 聚氯乙烯 (PVC) | <= 0.4544 |
| 聚乙烯 (PE) | <= 1.0823 |
| 聚丙烯 (PP) | <= 0.4374 |
| 丙烯腈 | <= 1.0570 |

### Field Definitions:

**欄位 221: 主要石化產品類型** — Format: string. List key products produced.

**欄位 222: 乙烯/丙烯/丁二烯年產量** — Format: string, unit: 公噸. List volumes for each if produced.

**欄位 223: 乙烯/丙烯/丁二烯單位溫室氣體排放量** — Format: decimal, unit: 公噸CO2e/公噸. Threshold: <= 0.9400.

**欄位 224: 苯乙烯年產量** — Format: decimal, unit: 公噸.

**欄位 225: 苯乙烯單位溫室氣體排放量** — Format: decimal, threshold: <= 1.0551 公噸CO2e/公噸.

**欄位 226: 氯乙烯年產量** — Format: decimal, unit: 公噸.

**欄位 227: 氯乙烯單位溫室氣體排放量** — Format: decimal, threshold: <= 0.5026 公噸CO2e/公噸.

**欄位 228: 聚乙烯(PE)年產量** — Format: decimal, unit: 公噸.

**欄位 229: 聚乙烯(PE)單位溫室氣體排放量** — Format: decimal, threshold: <= 1.0823 公噸CO2e/公噸.

**欄位 230: 聚丙烯(PP)年產量** — Format: decimal, unit: 公噸.

**欄位 231: 聚丙烯(PP)單位溫室氣體排放量** — Format: decimal, threshold: <= 0.4374 公噸CO2e/公噸.

**欄位 232: 聚氯乙烯(PVC)年產量** — Format: decimal, unit: 公噸.

**欄位 233: 聚氯乙烯(PVC)單位溫室氣體排放量** — Format: decimal, threshold: <= 0.4544 公噸CO2e/公噸.

**欄位 234: 其他石化產品（乙二醇/酚/丙酮/丙烯腈）資訊**
- Format: string
- If produced: 乙二醇 (threshold <= 2.0750), 酚/丙酮 (threshold <= 0.8741), 丙烯腈 (threshold <= 1.0570)
- Describe production volume and emission intensity for each

**欄位 235: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if: at least one produced product meets its respective threshold in the table above

### Key Search Terms: 石化產品產量, 輕裂解 (Naphtha Cracking), 產品碳足跡, 排放強度
### Data Locations: 製程環境績效章節, 產品產量統計表, 產品碳足跡報告

---

## 鋼鐵産業 (Steel) — 欄位 236-245

**Technical Standard:** 附表7

### Core Technical Screening Criteria:

**Electric Arc Furnace (EAF — 電弧爐) Route:**

Option 1 — GHG emission intensity (Scope 1 + Scope 2):
- High-alloy steel (高合金鋼): <= 0.620 tCO2e/tonne
- Carbon steel (碳鋼): <= 0.476 tCO2e/tonne

Option 2 — Scrap steel use ratio (廢鋼使用比例):
- High-alloy steel: >= 70%
- Carbon steel: >= 90%

**Integrated Process (一貫製程 — Blast Furnace + BOF):**
- Hot metal (鐵水): <= 1.443 tCO2e/tonne
- Sinter (燒結礦): <= 0.242 tCO2e/tonne
- Coke (焦炭, excluding lignite coke): <= 0.237 tCO2e/tonne

### Field Definitions:

**欄位 236: 鋼鐵生產製程類型**
- Format: string
- 電弧爐(EAF)、一貫製程(高爐+煉鋼爐)、或兩者兼有

**欄位 237: 鋼品類型**
- Format: string
- 碳鋼、高合金鋼、或兩者兼有

**欄位 238: 粗鋼年產量**
- Format: decimal, unit: 公噸, precision: 0.0001
- 2024年粗鋼 (crude steel) 總產量

**欄位 239: 電弧爐鋼品單位溫室氣體排放量 (範疇一+範疇二)**
- Format: decimal, unit: 公噸CO2e/公噸, precision: 0.0001
- Only fill if EAF process is used
- Thresholds: 高合金鋼 <= 0.620, 碳鋼 <= 0.476

**欄位 240: 廢鋼使用比例**
- Format: decimal, unit: 百分比, precision: 0.01
- Required for EAF Option 2 screening: 高合金鋼 >= 70%, 碳鋼 >= 90%
- Search for "廢鋼比例", "廢鋼投入率", "scrap ratio"

**欄位 241: 鐵水年產量**
- Format: decimal, unit: 公噸
- Fill only if integrated process (一貫製程/高爐) is used

**欄位 242: 鐵水單位溫室氣體排放量 (範疇一+範疇二)**
- Format: decimal, unit: 公噸CO2e/公噸, threshold: <= 1.443

**欄位 243: 燒結礦單位溫室氣體排放量**
- Format: decimal, unit: 公噸CO2e/公噸, threshold: <= 0.242

**欄位 244: 焦炭單位溫室氣體排放量**
- Format: decimal, unit: 公噸CO2e/公噸, threshold: <= 0.237
- Note: excludes lignite coke (褐煤焦炭)

**欄位 245: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- Evaluate per the applicable process type (EAF Option 1 or 2; or integrated process thresholds)

### Key Search Terms: 電弧爐(EAF), 高爐, 廢鋼使用率, 鐵水, 燒結礦, 焦炭
### Data Locations: 生產製程說明, 環境績效統計表, 循環經濟章節

---

## 紡織産業 (Textile) — 欄位 246-255

**Technical Standard:** 附表8

### Core Technical Screening Criteria:

**Man-made fibers (人造纖維) — Scope 1 + Scope 2 intensity:**
| Product | Threshold (公噸CO2e/公噸) |
|---------|---------------------------|
| 聚酯粒 | <= 0.2275 |
| 聚酯短纖 | <= 0.5661 |
| 聚酯長纖 | <= 1.1020 |
| 聚酯加工絲 | <= 0.8503 |
| 尼龍粒 | <= 1.0425 |
| 尼龍長纖 | <= 1.5420 |
| 尼龍加工絲 | <= 0.7484 |

**Yarn / Weaving (紡紗織布):** <= 2.2 tCO2e/tonne
**Dyeing / Finishing (染整):** <= 2.7 tCO2e/tonne

### Field Definitions:

**欄位 246: 主要紡織製程類型** — Format: string. 人造纖維製造、紡紗織布、染整、或多製程整合

**欄位 247: 人造纖維產品類型與年產量**
- Format: string, unit: 公噸
- List fiber types (聚酯粒/短纖/長纖/加工絲, 尼龍粒/長纖/加工絲) and volumes if produced

**欄位 248: 人造纖維單位溫室氣體排放量**
- Format: string (multiple products may be listed)
- Match each product against the thresholds table above

**欄位 249: 紡紗織布年產量** — Format: decimal, unit: 公噸

**欄位 250: 紡紗織布單位溫室氣體排放量** — Format: decimal, threshold: <= 2.2 公噸CO2e/公噸

**欄位 251: 染整加工年產量** — Format: decimal, unit: 公噸

**欄位 252: 染整加工單位溫室氣體排放量** — Format: decimal, threshold: <= 2.7 公噸CO2e/公噸

**欄位 253: 再生原料使用比例**
- Format: decimal, unit: 百分比
- 使用回收材料或再生原料佔總原料投入之比例

**欄位 254: 永續紡織認證取得情形**
- Format: string
- GRS (Global Recycled Standard), RCS (Recycled Claimed Standard), 或其他永續認證

**欄位 255: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- Evaluate per the applicable process type and product type thresholds

### Key Search Terms: 聚酯, 尼龍, 紡紗, 染整, GRS, RCS, 再生纖維
### Data Locations: 製程產量統計, 環境績效數據, 循環經濟/永續材料章節, 產品認證資訊

---

## 造紙産業 (Paper) — 欄位 256-265

**Technical Standard:** 附表9

### Core Technical Screening Criteria (Scope 1 + Scope 2, in tCO2e/Adt):

| Paper Type | Threshold |
|------------|-----------|
| 漂白硫酸鹽漿 (Bleached kraft pulp) | <= 0.70 |
| 紙板 (Paperboard) | <= 0.90 |
| 裱面紙板 (Liner board) | <= 0.90 |
| 瓦楞芯紙 (Corrugating medium) | <= 0.90 |
| 家庭用紙 (Tissue) | <= 1.60 |
| 印刷書寫用紙 (Printing & writing) | <= 0.90 |
| 特殊紙 (Specialty paper) | <= 2.20 |

Unit: Adt = Air Dry Tonne (氣乾噸)

### Field Definitions:

**欄位 256: 主要紙類產品類型** — Format: string. List the paper types produced.

**欄位 257: 紙類年產量（氣乾噸Adt）**
- Format: string (may list multiple products)
- Unit: Adt (Air Dry Ton, 氣乾噸)

**欄位 258: 紙類產品單位溫室氣體排放量**
- Format: string (list per-product emission intensities)
- Unit: 公噸CO2e/Adt
- Match against the threshold table above

**欄位 259: 單位產品能源消耗量**
- Format: decimal, unit: Mcal/Adt, precision: 0.01

**欄位 260: 廢紙回收使用比例**
- Format: decimal, unit: 百分比
- 廢紙或再生原料佔總原料投入之比例

**欄位 261: 事業廢棄物回收再利用率**
- Format: decimal, unit: 百分比

**欄位 262: COD（化學需氧量）產生量**
- Format: decimal, unit: 公斤/Adt
- 單位產品COD產生量或排放量

**欄位 263: FSC/PEFC森林認證情形**
- Format: boolean
- FSC (Forest Stewardship Council), PEFC (Programme for the Endorsement of Forest Certification)

**欄位 264: 綠色產品或環保標章取得情形**
- Format: string

**欄位 265: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if: at least one paper product meets its corresponding Adt threshold

### Key Search Terms: 氣乾噸 (Adt), 廢紙回收率, 能源消耗強度, FSC, PEFC, COD
### Data Locations: 產品產量統計表, 環境績效章節, 循環經濟數據, 製程能源使用統計

---

## 半導體産業 (Semiconductor) — 欄位 266-275

**Technical Standard:** 附表10

### Core Technical Screening Criteria:

**IC Manufacturing (IC製造) — Scope 1 + Scope 2 per unit area:**
| Wafer Size | Threshold (公斤CO2e/cm²) |
|------------|---------------------------|
| 6吋以下 | <= 2.18 |
| 8吋 | <= 2.51 |
| 12吋 成熟製程 (>= 10nm) | <= 1.31 |
| 12吋 先進製程 (< 10nm) | <= 9.58 |

**IC Packaging & Testing (IC封測) — electricity per unit:**
| Package Type | Threshold (kWh/千個) |
|-------------|----------------------|
| 導線架 (Lead Frame) | <= 55 |
| 球型陣列封裝 (BGA) | <= 22 |
| 覆晶封裝 (Flip Chip) | <= 230 |
| 晶圓凸塊 (Bumping) | <= 85 |
| 測試 (Testing) | <= 12 |

### Field Definitions:

**欄位 266: 主要業務類型**
- Format: string
- IC製造（晶圓廠）或 IC封裝測試

**欄位 267: 晶圓尺寸與年產量**
- Format: string, unit: 萬片（約當8吋）
- If IC manufacturing: specify wafer sizes and annual production

**欄位 268: 製程節點技術**
- Format: string
- For 12-inch wafers: specify dominant process node (成熟製程 >= 10nm or 先進製程 < 10nm)

**欄位 269: IC製造單位面積溫室氣體排放量**
- Format: decimal, unit: 公斤CO2e/平方公分 (kg CO2e/cm²)
- Only fill for IC manufacturing companies
- Match against the wafer-size threshold table above

**欄位 270: IC封測年產量**
- Format: string, unit: 千個
- Only fill for packaging & testing companies; specify by package type

**欄位 271: IC封測單位產品用電量**
- Format: string, unit: kWh/千個
- Match against the packaging type threshold table above

**欄位 272: PFC（全氟化物）減排措施**
- Format: string
- 含氟溫室氣體 (SF6, NF3, CF4, C2F6, C3F8, CHF3, etc.) 減量技術或設備
- Search for "PFC減排", "含氟溫室氣體", "全氟化物"

**欄位 273: 製程用水回收率**
- Format: decimal, unit: 百分比

**欄位 274: 綠色製造或責任商業聯盟(RBA)認證**
- Format: string
- RBA, ISO 14001, 或其他綠色製造認證

**欄位 275: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- Evaluate per business type (IC manufacturing thresholds by wafer size, or encapsulation thresholds by package type)

### Key Search Terms: 晶圓尺寸(6吋/8吋/12吋), 製程節點(nm), PFC減排, 單位面積排放強度, RBA
### Data Locations: 製程技術說明, 溫室氣體管理專章(含PFC), 廠區環境績效數據, 綠色製造章節

---

## 平面顯示器面板産業 (Display Panel) — 欄位 276-285

**Technical Standard:** 附表11

### Core Technical Screening Criteria:

Option 1 — GHG emission intensity (Scope 1 + Scope 2, tCO2e/m²):
- 3.5代以下 (Gen 3.5 and below): <= 0.600 tCO2e/m²
- 4代以上 (Gen 4 and above): <= 0.150 tCO2e/m²

Option 2 — Energy consumption (kWh/m²):
- 3.5代以下: <= 600 kWh/m²
- 4代以上: <= 120 kWh/m²

### Field Definitions:

**欄位 276: 面板技術類型** — Format: string. LCD, OLED, 或其他

**欄位 277: 面板世代與產線規格**
- Format: string
- 主要產線的面板世代 (G3.5, G4, G6, G8.5等)

**欄位 278: 年基板投入面積**
- Format: decimal, unit: 平方公尺, precision: 0.01
- 2024年基板投入總面積

**欄位 279: 單位基板溫室氣體排放量（範疇一+範疇二）**
- Format: decimal, unit: 公噸CO2e/平方公尺, precision: 0.001
- Match against generation-based thresholds

**欄位 280: 單位基板能源消耗量**
- Format: decimal, unit: kWh/平方公尺, precision: 0.01
- Match against generation-based energy thresholds (Option 2)

**欄位 281: 顯示器能效等級或認證** — Format: string. Energy Star, 台灣節能標章, etc.

**欄位 282: 含氟溫室氣體減量措施**
- Format: string
- SF6, NF3 等氣體的減量或尾氣處理技術

**欄位 283: 製程廢液回收處理率**
- Format: decimal, unit: 百分比

**欄位 284: 綠色產品或環境標章取得情形** — Format: string

**欄位 285: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if the company satisfies Option 1 OR Option 2 threshold for its panel generation

### Key Search Terms: 面板世代(G3.5/G4/G6/G8.5), 基板面積, 含氟溫室氣體, 單位基板排放強度
### Data Locations: 產品技術與產線說明, 環境績效數據, 能源管理章節

---

## 電腦及週邊設備産業 (Computer Equipment) — 欄位 286-295

**Technical Standard:** 附表12

### Core Technical Screening Criteria (any ONE of the following qualifies):
1. Product holds **EPEAT** certification (any tier: Gold, Silver, Bronze)
2. Product holds a **ISO 14024 Type I** environmental label
3. Product holds **Energy Star** or Taiwan **節能標章** (Energy Conservation Label)
4. Product holds a **ISO 14021 Type II** self-declared environmental claim that has been **third-party verified**

### Field Definitions:

**欄位 286: 主要產品類型**
- Format: string
- 桌上型電腦、筆記型電腦、伺服器、顯示器、印表機等

**欄位 287: EPEAT標章取得情形**
- Format: string
- Specify tier: 金牌(Gold), 銀牌(Silver), 銅牌(Bronze); and product categories

**欄位 288: Energy Star或節能標章取得情形**
- Format: string
- Specify which products hold the certification

**欄位 289: ISO 14024第一類環保標章取得情形**
- Format: string
- Any government-backed Type I eco-label recognized under ISO 14024

**欄位 290: ISO 14021第二類環境宣告情形**
- Format: string
- Self-declared environmental claims per ISO 14021; must be third-party verified to count

**欄位 291: 產品能源效率等級**
- Format: string
- Energy efficiency rating or power consumption information

**欄位 292: 產品碳足跡標籤取得情形** — Format: boolean

**欄位 293: 產品可回收設計或循環經濟措施**
- Format: string
- 易拆解設計、模組化、使用再生材料等

**欄位 294: 產品維修服務或延長保固措施**
- Format: string
- 延長保固、維修服務、升級方案

**欄位 295: 是否符合永續經濟活動技術篩選標準**
- Format: boolean
- True if ANY of fields 287, 288, 289, or 290 shows a valid certification (for 290, third-party verification is required)

### Key Search Terms: EPEAT, Energy Star, 節能標章, ISO 14024, ISO 14021, 環保標章, 綠色產品
### Data Locations: 產品責任/永續產品章節, 綠色產品認證清單, 環境標章取得情形

---

## Common Extraction Rules (All Industries)

1. **Scope boundary**: Only include domestic Taiwan facilities unless the report boundary explicitly extends to overseas operations
2. **Year**: Extract 2024 figures; if not yet available, use the most recent year and note in 補充說明
3. **Units**: Always preserve the original unit from the report; convert only when necessary and document the conversion
4. **"符合技術篩選標準" boolean**: Derive from the quantitative fields in the same module — do not rely solely on the company's self-declaration
5. **Missing data**: If a product field is not applicable (e.g., a steel company does not produce sinter), leave it blank; do not fill "N/A" unless explicitly instructed

---

## Output Format

```
欄位 [ID]: [Value]
補充說明: [Notes on units, scope, calculations, or data gaps]
```

For inapplicable fields (wrong product type for this company):
```
欄位 [ID]: 不適用
補充說明: [Reason — e.g., company does not produce this product]
```
