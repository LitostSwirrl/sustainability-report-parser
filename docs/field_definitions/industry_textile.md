# 紡織產業欄位 (Textile Industry) — 欄位 246-255

> Source: `src/field_definitions.py` → `TEXTILE_FIELDS`
> Applicable to: Textile industry companies (紡織業), including man-made fiber producers, spinning/weaving, and dyeing/finishing operations. Appended after base fields and manufacturing common fields. Reference standard: 附表8 — 永續經濟活動認定參考指引. Technical screening thresholds vary by process type and fiber product.

---

### 欄位 246: 主要紡織製程類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 製程資訊 |

**Description:** 說明企業主要從事的製程：人造纖維製造、紡紗織布、染整、或多製程整合。

---

### 欄位 247: 人造纖維產品類型與年產量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸 |
| Precision | NA |
| Category | 產量 |

**Description:** 若生產人造纖維，請列舉產品類型（聚酯粒/短纖/長纖/加工絲、尼龍粒/長纖/加工絲）及年產量。

---

### 欄位 248: 人造纖維單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸CO2e/公噸 |
| Precision | NA |
| Category | GHG強度 |

**Description:** 各產品類型單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表8):**
| 產品 | 閾值 |
|------|------|
| 聚酯粒 | **≤ 0.2275 公噸CO2e/公噸** |
| 聚酯短纖 | **≤ 0.5661 公噸CO2e/公噸** |
| 聚酯長纖 | **≤ 1.1020 公噸CO2e/公噸** |
| 聚酯加工絲 | **≤ 0.8503 公噸CO2e/公噸** |
| 尼龍粒 | **≤ 1.0425 公噸CO2e/公噸** |
| 尼龍長纖 | **≤ 1.5420 公噸CO2e/公噸** |
| 尼龍加工絲 | **≤ 0.7484 公噸CO2e/公噸** |

---

### 欄位 249: 紡紗織布年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若從事紡紗織布製程，請填寫年產量。

---

### 欄位 250: 紡紗織布單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 紡紗織布製程的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表8):** **≤ 2.2 公噸CO2e/公噸**

---

### 欄位 251: 染整加工年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若從事染整製程，請填寫年加工量。

---

### 欄位 252: 染整加工單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 染整製程的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表8):** **≤ 2.7 公噸CO2e/公噸**

---

### 欄位 253: 再生原料使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 使用回收材料或再生原料佔總原料投入之比例。

---

### 欄位 254: 永續紡織認證取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 是否取得GRS（全球回收標準）、RCS（回收材料標準）或其他永續認證。

---

### 欄位 255: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表8判斷：依製程類型對應相應GHG排放標準。人造纖維依產品類型對應各自閾值；紡紗織布 ≤ 2.2；染整 ≤ 2.7（單位均為公噸CO2e/公噸）。
