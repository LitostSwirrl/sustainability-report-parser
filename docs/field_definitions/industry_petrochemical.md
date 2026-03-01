# 石油化學產業欄位 (Petrochemical Industry) — 欄位 221-235

> Source: `src/field_definitions.py` → `PETROCHEMICAL_FIELDS`
> Applicable to: Petrochemical industry companies (石化業，如乙烯、丙烯、聚乙烯、聚丙烯、PVC等生產商). Appended after base fields and manufacturing common fields. Reference standard: 附表6 — 永續經濟活動認定參考指引。Each product type has its own GHG intensity threshold.

---

### 欄位 221: 主要石化產品類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 列舉企業主要生產的石化產品類別（如：乙烯、丙烯、聚乙烯等）。

---

### 欄位 222: 乙烯/丙烯/丁二烯年產量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產乙烯、丙烯或丁二烯，請填寫年產量（可列舉多項）。

---

### 欄位 223: 乙烯/丙烯/丁二烯單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 乙烯、丙烯、丁二烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 0.9400 公噸CO2e/公噸**

---

### 欄位 224: 苯乙烯年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產苯乙烯(Styrene)，請填寫年產量。

---

### 欄位 225: 苯乙烯單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 苯乙烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 1.0551 公噸CO2e/公噸**

---

### 欄位 226: 氯乙烯年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產氯乙烯(Vinyl Chloride)，請填寫年產量。

---

### 欄位 227: 氯乙烯單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 氯乙烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 0.5026 公噸CO2e/公噸**

---

### 欄位 228: 聚乙烯(PE)年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產聚乙烯，請填寫年產量。

---

### 欄位 229: 聚乙烯(PE)單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 聚乙烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 1.0823 公噸CO2e/公噸**

---

### 欄位 230: 聚丙烯(PP)年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產聚丙烯，請填寫年產量。

---

### 欄位 231: 聚丙烯(PP)單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 聚丙烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 0.4374 公噸CO2e/公噸**

---

### 欄位 232: 聚氯乙烯(PVC)年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若生產PVC，請填寫年產量。

---

### 欄位 233: 聚氯乙烯(PVC)單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 聚氯乙烯的單位GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表6):** **≤ 0.4544 公噸CO2e/公噸**

---

### 欄位 234: 其他石化產品（乙二醇/酚/丙酮/丙烯腈）資訊

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 若生產乙二醇、酚/丙酮、丙烯腈，請說明產量與排放強度。

**技術篩選標準 (附表6):**
- 乙二醇 **≤ 2.0750 公噸CO2e/公噸**
- 酚/丙酮 **≤ 0.8741 公噸CO2e/公噸**
- 丙烯腈 **≤ 1.0570 公噸CO2e/公噸**

---

### 欄位 235: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表6判斷：各產品單位GHG排放量是否符合對應閾值。各產品閾值如下——乙烯/丙烯/丁二烯 ≤ 0.9400、苯乙烯 ≤ 1.0551、氯乙烯 ≤ 0.5026、PE ≤ 1.0823、PP ≤ 0.4374、PVC ≤ 0.4544。
