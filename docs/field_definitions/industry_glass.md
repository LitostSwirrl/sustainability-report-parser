# 玻璃產業欄位 (Glass Industry) — 欄位 211-220

> Source: `src/field_definitions.py` → `GLASS_FIELDS`
> Applicable to: Glass industry companies (玻璃業). Appended after base fields and manufacturing common fields. Reference standard: 附表5 — 永續經濟活動認定參考指引。Technical screening threshold applies to field 213.

---

### 欄位 211: 主要玻璃產品類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 說明主要生產的玻璃產品類型：平板玻璃、板狀玻璃、浮法玻璃、或其他玻璃製品。

---

### 欄位 212: 平板玻璃年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 2024年平板玻璃（Flat Glass）總產量。

---

### 欄位 213: 平板玻璃單位溫室氣體排放量 (範疇一+範疇二)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 單位產品GHG排放量。

**技術篩選標準 (附表5):** 平板玻璃單位GHG排放量 **≤ 1.0121 公噸CO2e/公噸**

---

### 欄位 214: 玻璃碎片（廢玻璃）使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 生產過程中使用回收玻璃碎片（Cullet）佔總原料投入之比例。

---

### 欄位 215: 玻璃窯爐製程能源消耗量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | GJ/公噸 |
| Precision | 0.0001 |
| Category | 能源效率 |

**Description:** 單位產品能源消耗量（熔爐能源效率）。

---

### 欄位 216: 窯爐類型與技術

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 技術資訊 |

**Description:** 說明採用的窯爐技術類型（如：浮法窯、電熔窯、純氧燃燒技術等）。

---

### 欄位 217: 替代燃料使用情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 循環經濟 |

**Description:** 是否使用替代燃料（如：生質能、廢棄物衍生燃料）及使用比例。

---

### 欄位 218: 產品碳足跡驗證情形

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 是否取得產品碳足跡標籤或環保標章認證。

---

### 欄位 219: 製程NOx或SOx減量措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 環境管理 |

**Description:** 空氣污染物減量技術採用情形（如：脫硝、脫硫設備）。

---

### 欄位 220: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表5判斷：平板玻璃單位GHG排放量 **≤ 1.0121 公噸CO2e/公噸**。
