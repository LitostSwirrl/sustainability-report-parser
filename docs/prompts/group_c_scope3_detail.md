# Group C: GHG Protocol 範疇三細項 (Scope 3 Detail — Categories 1-15)

**Fields:** 16-30
**Focus:** GHG Protocol's 15 Scope 3 categories; many may be empty — that is normal

---

## PDF Reading Strategy

Read these sections in order:

1. **GRI appendix / GRI index** — search GRI 305-3 cross-reference for page numbers
2. **SASB appendix** — check if a Scope 3 breakdown table appears there
3. **Supply chain / value chain chapter** — Category 1 (purchased goods) is often discussed here
4. **Climate / TCFD chapter** — some companies include a Scope 3 breakdown table in the TCFD section
5. **ESG data appendix** — look for a table with columns labeled "類別1" through "類別15" or "Category 1" through "Category 15"

Search keywords: 範疇三、Scope 3、類別1、類別2、購買商品、資本商品、員工通勤、商務旅行、下游運輸、投資排放、GRI 305-3、supply chain emissions、value chain

---

## Critical Distinction: GHG Protocol vs. ISO 14064-1

This group covers **GHG Protocol Scope 3 Categories 1-15 only**.

Do NOT confuse with ISO/CNS 14064-1 類別三～六 (which were covered in Group B, fields 12-15).

| GHG Protocol Category | Chinese name |
|------------------------|--------------|
| Category 1 | 購買商品或服務 |
| Category 2 | 資本商品 |
| Category 3 | 燃料與能源相關活動 |
| Category 4 | 上游運輸和配送 |
| Category 5 | 營運廢棄物 |
| Category 6 | 商務旅行 |
| Category 7 | 員工通勤 |
| Category 8 | 上游租賃資產 |
| Category 9 | 下游運輸和配送 |
| Category 10 | 銷售產品的加工 |
| Category 11 | 使用銷售產品 |
| Category 12 | 銷售產品廢棄處理 |
| Category 13 | 下游租賃資產 |
| Category 14 | 特許經營 |
| Category 15 | 投資 |

---

## Field Definitions

### 欄位 16: Scope 3 類別 1 (購買商品或服務)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別1。包含供應鏈上游採購的商品與服務在其生命週期中產生的排放。這是多數製造業最大的 Scope 3 類別。
- **Note:** This is typically the largest Scope 3 category for manufacturers. If a company discloses only one Scope 3 number without breaking it into categories, do not assume it is Category 1.

### 欄位 17: Scope 3 類別 2 (資本商品)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別2。公司購買或取得的資本財（如機器設備、建築）在製造過程中產生的排放。若報告書未揭露，請留空。

### 欄位 18: Scope 3 類別 3 (燃料與能源相關活動)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別3（非範疇一二之排放）。包含燃料開採、處理、運輸至公司所產生的排放，以及外購電力的上游排放（transmission and distribution losses）。若報告書未揭露，請留空。
- **Caution:** GHG Protocol Category 3 ≠ ISO 14064-1 類別三。Do not cross-fill from Group B.

### 欄位 19: Scope 3 類別 4 (上游運輸和配送)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別4。從供應商到公司廠區的原物料及零件運輸排放。若報告書未揭露，請留空。

### 欄位 20: Scope 3 類別 5 (營運廢棄物)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別5。公司營運過程中產生廢棄物的處理排放（廢棄物最終處置）。若報告書未揭露，請留空。

### 欄位 21: Scope 3 類別 6 (商務旅行)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別6。員工因公出差（搭乘飛機、火車等）產生的排放。若報告書未揭露，請留空。

### 欄位 22: Scope 3 類別 7 (員工通勤)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別7。員工每日上下班通勤所產生的排放。若報告書未揭露，請留空。

### 欄位 23: Scope 3 類別 8 (上游租賃資產)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別8。公司租用的資產（非自有）中，其資產運作產生的排放（如租用辦公室的能源）。若報告書未揭露，請留空。

### 欄位 24: Scope 3 類別 9 (下游運輸和配送)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別9。從公司出貨到客戶及最終消費者的運輸排放。若報告書未揭露，請留空。

### 欄位 25: Scope 3 類別 10 (銷售產品的加工)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別10。下游客戶對公司售出產品進行進一步加工所產生的排放。通常只適用於半成品製造商。若報告書未揭露，請留空。

### 欄位 26: Scope 3 類別 11 (使用銷售產品)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別11。消費者使用公司所售商品的生命週期排放。對電子產品、汽車等產業往往是最大的Scope 3類別。若報告書未揭露，請留空。

### 欄位 27: Scope 3 類別 12 (銷售產品廢棄處理)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別12。消費者使用後，廢棄商品的處理排放（如廢電子產品回收）。若報告書未揭露，請留空。

### 欄位 28: Scope 3 類別 13 (下游租賃資產)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別13。公司出租給他人的資產所產生的排放。若報告書未揭露，請留空。

### 欄位 29: Scope 3 類別 14 (特許經營)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別14。連鎖加盟業者（Franchisor）因加盟店運營產生的排放。僅適用於有加盟體系的企業。若報告書未揭露，請留空。

### 欄位 30: Scope 3 類別 15 (投資)
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** GHG Protocol 範疇三類別15。公司持有股權或債權的被投資企業之排放。**金融業請特別注意此欄位**，通常為投融資組合排放（Financed Emissions，依PCAF標準計算）。製造業的控股公司若有大量轉投資，也可能揭露此類別。若報告書未揭露，請留空。

---

## Extraction Rules (for this group)

### Empty categories are expected and normal
Most companies only disclose a subset of the 15 categories. Do not fill in zeros for undisclosed categories. Leave them blank.

Industry-typical disclosed categories:
- **Manufacturing**: Usually Categories 1, 4, 5, 6, 7 (sometimes also 11, 12)
- **Financial institutions**: Usually Category 15 (financed emissions); may also disclose 6, 7
- **Retailers / logistics**: Usually Categories 1, 4, 9

### How to find Scope 3 data in reports

Most common locations (in order of reliability):

1. **GRI 305-3 page**: the GRI index will link directly to the Scope 3 disclosure page. Go there first.
2. **Separate Scope 3 inventory table**: look for a table with rows labeled by category number.
3. **Climate / sustainability strategy chapter**: the Scope 3 figure may appear embedded in narrative text.
4. **TCFD appendix**: some companies only put Scope 3 data in their TCFD disclosure rather than the main report.

Common table heading variants in Taiwanese reports:
- 「類別1(購買商品)」, 「Cat.1 Purchased Goods」
- 「GHG Protocol Category 1」
- English-only tables use "Category 1" through "Category 15"

### Distinguishing GHG Protocol categories from ISO categories in ambiguous tables
If a table only says 「類別一」「類別二」「類別三」without further description, determine the system from context:
- If 類別一 and 類別二 are large numbers (the company's main direct and indirect emissions), it is using ISO 14064-1 → do NOT use for fields 16-30
- If 類別一 is labeled as 「購買商品」or the values are all in the Scope 3 section of the table, it is using GHG Protocol → use for fields 16-30

### Unit conversion
- Standard unit is 公噸CO2e
- Convert kt CO2e × 1,000; Mt CO2e × 1,000,000
- Do not convert raw activity data into CO2e — only convert between CO2e mass units

### Financial sector: Category 15 (Financed Emissions) — special handling
- Category 15 for banks/insurers often appears in a TCFD report or dedicated section, not the main GHG table
- The value may be labelled 「投融資組合排放」「被投資企業排放」「Financed Emissions」
- The unit should still be 公噸CO2e; if the report gives it in 千公噸CO2e (kt), convert before filling
- Note the PCAF data quality score in 補充說明 if disclosed

---

## Output Format

```
---欄位16開始---
欄位數值: [value or empty]
欄位單位: 公噸CO2e
補充說明: [source section, category description, or reason for blank — max 200 chars]
參考頁數: [p.X or NA]
---欄位16結束---
```

Example for a semiconductor company that discloses Categories 1, 4, 5, 6, 7:

```
---欄位16開始---
欄位數值: 8234567.0000
欄位單位: 公噸CO2e
補充說明: GRI 305-3附錄Scope 3 Category 1，購買商品與服務，來自供應商盤查數據
參考頁數: p.145
---欄位16結束---

---欄位17開始---
欄位數值:
欄位單位: 公噸CO2e
補充說明: 報告書未揭露Category 2（資本商品）排放數值
參考頁數: NA
---欄位17結束---

---欄位21開始---
欄位數值: 12450.0000
欄位單位: 公噸CO2e
補充說明: Category 6商務旅行，以航班里程數計算，包含長途與短途飛行
參考頁數: p.146
---欄位21結束---
```

Example for a financial institution (Category 15 key):

```
---欄位30開始---
欄位數值: 45678900.0000
欄位單位: 公噸CO2e
補充說明: Financed Emissions依PCAF標準計算，涵蓋企業放款及專案融資，PCAF品質分數3.2，來自TCFD報告
參考頁數: p.23
---欄位30結束---
```

---

## Common Pitfalls

1. **Confusing ISO 類別三 with GHG Protocol Category 3**: the most critical error in this group. ISO 類別三 (transportation of goods to/from the company) is NOT the same as GHG Protocol Category 3 (upstream fuel/energy activities). If the report uses ISO categories for its Scope 3, fields 16-30 should all be blank (those numbers belong in Group B, fields 12-15).

2. **Filling zeros for undisclosed categories**: if a category is not in the report, leave the field blank. Do not fill `0`. A blank means "not disclosed"; `0` means "zero emissions," which would be incorrect.

3. **Double-counting with Group B fields**: field 11 in Group B is the Scope 3 total. Fields 16-30 here are the breakdown. They should sum to field 11. Do not count a single number in both places as if they were separate.

4. **Financed Emissions (Category 15) in wrong unit**: some financial institutions report financed emissions in 「百萬公噸CO2e」or 「千噸」. Convert to 公噸CO2e before filling field 30.

5. **Partial tables**: a company may show a Scope 3 table where some category rows say 「not applicable」or 「N/A」. Treat these as blank (do not fill 0 or any value).

6. **Aggregated Scope 3 with no category breakdown**: if the report gives only one Scope 3 total with no category detail, fill that total in Group B field 11 and leave all fields 16-30 blank.

7. **Different Scope 3 bases across report sections**: the main chapter may show a rounded figure while the GRI appendix shows the precise figure. Use the GRI appendix figure as it is the formal disclosure.

8. **Category 15 for non-financial companies**: a manufacturing holding company with significant equity investments may disclose Category 15 emissions. This is valid — fill field 30 if found.
