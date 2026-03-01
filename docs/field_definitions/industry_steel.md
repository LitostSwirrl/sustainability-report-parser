# 鋼鐵產業欄位 (Steel Industry) — 欄位 236-245

> Source: `src/field_definitions.py` → `STEEL_FIELDS`
> Applicable to: Steel industry companies (鋼鐵業). Appended after base fields and manufacturing common fields. Reference standard: 附表7 — 永續經濟活動認定參考指引。Technical screening thresholds vary by production process (EAF vs. integrated) and steel grade (carbon steel vs. high-alloy steel).

---

### 欄位 236: 鋼鐵生產製程類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 製程資訊 |

**Description:** 說明主要採用的製程類型：電弧爐(EAF)、一貫製程(高爐+煉鋼爐)、或其他製程。

---

### 欄位 237: 鋼品類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 主要生產的鋼材類型：碳鋼、高合金鋼、或兩者兼有。

---

### 欄位 238: 粗鋼年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 2024年粗鋼（crude steel）總產量。

---

### 欄位 239: 電弧爐鋼品單位溫室氣體排放量 (範疇一+範疇二)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 若採用電弧爐製程，請填寫單位產品GHG排放量。

**技術篩選標準 (附表7 — 電弧爐製程):**
- 高合金鋼 **≤ 0.620 公噸CO2e/公噸**
- 碳鋼 **≤ 0.476 公噸CO2e/公噸**

---

### 欄位 240: 廢鋼使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 廢鋼投入量佔總鋼鐵原料投入量之比例。

**技術篩選標準 (附表7):**
- 高合金鋼 **≥ 70%**
- 碳鋼 **≥ 90%**

---

### 欄位 241: 鐵水年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 若採用一貫製程（高爐煉鐵），請填寫鐵水(hot metal/molten iron)年產量。

---

### 欄位 242: 鐵水單位溫室氣體排放量 (範疇一+範疇二)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 若採用一貫製程，請填寫鐵水單位GHG排放量。

**技術篩選標準 (附表7 — 一貫製程):** **≤ 1.443 公噸CO2e/公噸**

---

### 欄位 243: 燒結礦單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 若生產燒結礦，請填寫單位GHG排放量。

**技術篩選標準 (附表7):** **≤ 0.242 公噸CO2e/公噸**

---

### 欄位 244: 焦炭單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 若生產焦炭（不包括褐煤焦炭），請填寫單位GHG排放量。

**技術篩選標準 (附表7):** **≤ 0.237 公噸CO2e/公噸**

---

### 欄位 245: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表7判斷：依製程類型（EAF或一貫）及產品類型（碳鋼或高合金鋼）對應標準。EAF碳鋼須同時滿足單位GHG ≤ 0.476 及廢鋼比例 ≥ 90%；EAF高合金鋼須 ≤ 0.620 及 ≥ 70%；一貫製程鐵水須 ≤ 1.443。
