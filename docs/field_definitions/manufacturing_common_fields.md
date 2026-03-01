# 製造業共通欄位 (Manufacturing Common Fields) — 欄位 101-110

> Source: `src/field_definitions.py` → `MANUFACTURING_COMMON_FIELDS_V2`
> Applicable to: All manufacturing companies (non-financial sector). These fields capture sustainable economic activity ratios (Turnover/CapEx/OpEx), product-level GHG intensity, and technology adoption metrics. Used in V2 (2026 驗證指標) as the standard manufacturing module appended after base fields 1-72.

---

### 欄位 101: 符合永續指引之營收 (Turnover) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |

**Description:** 辨識企業的營收有多少比例來自於合格的永續經濟活動。若未揭露請留空。

---

### 欄位 102: 符合永續指引之資本支出 (CapEx) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |

**Description:** 通常指投入於製程改善、節能設備的投資比例。

---

### 欄位 103: 符合永續指引之營運費用 (OpEx) 佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續經濟活動 |

**Description:** 針對永續設備維護、研發等費用比例。

---

### 欄位 104: 單位產品溫室氣體排放強度 (特定製程)

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸CO2e/單位產品 |
| Precision | 0.01 |
| Category | GHG強度 |

**Description:** 選擇報告書中明確標示為「代表性產品」或「主要產品」的碳排放強度數值。若有多項產品，選營收佔比最高者。格式：「數值 單位 (產品名)」。

---

### 欄位 105: 產品製程類別或代表性產品名稱

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 公司主要產品類別，限3項以內。格式：「產品1、產品2、產品3」。使用報告書中的原始名稱，不需加註解說明。

---

### 欄位 106: 產品年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 依產品單位 |
| Precision | 0.0001 |
| Category | 產品資訊 |

**Description:** 2024年該代表性產品的年產量。

---

### 欄位 107: 是否採用最佳可行技術 (BAT)

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 技術採用 |

**Description:** 企業是否採用或規劃採用最佳可行技術來降低碳排放。

---

### 欄位 108: 碳排放強度改善目標年

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | 西元年 |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 企業設定達成特定碳排放強度目標的年份。

---

### 欄位 109: 碳排放強度改善目標值

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/單位產品 |
| Precision | 0.0001 |
| Category | 氣候行動 |

**Description:** 企業設定的碳排放強度目標值。

---

### 欄位 110: 製程能源效率指標

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | GJ/公噸 |
| Precision | 0.0001 |
| Category | 能源效率 |

**Description:** 單位產品能源消耗量 (GJ/公噸產品)。
