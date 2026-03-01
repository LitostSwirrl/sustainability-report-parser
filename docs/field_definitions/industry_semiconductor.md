# 半導體產業欄位 (Semiconductor Industry) — 欄位 266-275

> Source: `src/field_definitions.py` → `SEMICONDUCTOR_FIELDS`
> Applicable to: Semiconductor companies (半導體業), including IC fabrication (晶圓廠) and IC packaging/testing (封裝測試). Appended after base fields and manufacturing common fields. Reference standard: 附表10 — 永續經濟活動認定參考指引. GHG thresholds differ by wafer size and process node; packaging thresholds are measured in electricity consumption per unit.

---

### 欄位 266: 主要業務類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 製程資訊 |

**Description:** IC製造（晶圓廠）或IC封裝測試。

---

### 欄位 267: 晶圓尺寸與年產量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 萬片（約當8吋） |
| Precision | NA |
| Category | 產量 |

**Description:** 若為IC製造，請說明晶圓尺寸（6吋/8吋/12吋）及年產量（萬片約當8吋）。

---

### 欄位 268: 製程節點技術

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 技術資訊 |

**Description:** 若為12吋晶圓，請說明主要製程節點（成熟製程 ≥ 10nm 或先進製程 < 10nm）。

---

### 欄位 269: IC製造單位面積溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公斤CO2e/平方公分 |
| Precision | 0.01 |
| Category | GHG強度 |

**Description:** 晶圓單位面積GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表10 — IC製造):**
| 晶圓規格 | 閾值 |
|----------|------|
| 6吋以下 | **≤ 2.18 公斤CO2e/平方公分** |
| 8吋 | **≤ 2.51 公斤CO2e/平方公分** |
| 12吋（成熟製程 ≥ 10nm） | **≤ 1.31 公斤CO2e/平方公分** |
| 12吋（先進製程 < 10nm） | **≤ 9.58 公斤CO2e/平方公分** |

---

### 欄位 270: IC封測年產量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 千個 |
| Precision | NA |
| Category | 產量 |

**Description:** 若為封測業務，請說明年封裝或測試產量。

---

### 欄位 271: IC封測單位產品用電量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | kWh/千個 |
| Precision | NA |
| Category | 能源效率 |

**Description:** 封測製程單位產品用電量。

**技術篩選標準 (附表10 — IC封測):**
| 封測類型 | 閾值 |
|----------|------|
| 導線架 | **≤ 55 kWh/千個** |
| BGA | **≤ 22 kWh/千個** |
| FlipChip | **≤ 230 kWh/千個** |
| Bumping | **≤ 85 kWh/千個** |
| 測試 | **≤ 12 kWh/千個** |

---

### 欄位 272: PFC（全氟化物）減排措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 技術採用 |

**Description:** 針對含氟溫室氣體的減量技術或設備使用情形。

---

### 欄位 273: 製程用水回收率

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 製程用水回收再利用比例。

---

### 欄位 274: 綠色製造或責任商業聯盟(RBA)認證

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 是否取得RBA、ISO 14001或其他綠色製造相關認證。

---

### 欄位 275: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表10判斷：依晶圓尺寸/製程節點或封測類型對應標準。IC製造依晶圓規格對應單位面積GHG閾值；IC封測依封測類型對應單位用電量閾值。
