# 水泥產業欄位 (Cement Industry) — 欄位 201-210

> Source: `src/field_definitions.py` → `CEMENT_FIELDS`
> Applicable to: Cement industry companies (水泥業). Appended after base fields and manufacturing common fields. Reference standard: 附表4 — 永續經濟活動認定參考指引。Technical screening thresholds apply to fields 202 and 204.

---

### 欄位 201: 水泥熟料年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 2024年水泥熟料 (Clinker) 生產量。

---

### 欄位 202: 水泥熟料單位溫室氣體排放量 (範疇一+範疇二)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 最近一年單位產品溫室氣體排放量（範疇一+範疇二），扣除分配給廢氣生產之溫室氣體排放量。

**技術篩選標準 (附表4):** 水泥熟料單位GHG排放量 **≤ 0.90 公噸CO2e/公噸**

---

### 欄位 203: 水泥成品年產量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 產量 |

**Description:** 2024年水泥成品生產量（包含各種類型水泥）。

---

### 欄位 204: 水泥成品單位溫室氣體排放量 (範疇一+範疇二)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/公噸 |
| Precision | 0.0001 |
| Category | GHG強度 |

**Description:** 最近一年單位產品溫室氣體排放量（範疇一+範疇二）。

**技術篩選標準 (附表4):** 水泥成品單位GHG排放量 **≤ 0.87 公噸CO2e/公噸**

---

### 欄位 205: 替代原料使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 使用廢棄物、副產品等替代原料佔總原料使用量之比例。

---

### 欄位 206: 替代燃料使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 使用廢棄物衍生燃料等替代燃料佔總燃料使用量之比例。

---

### 欄位 207: 水泥窯協同處理廢棄物量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.0001 |
| Category | 循環經濟 |

**Description:** 利用水泥窯協同處理廢棄物的年處理量。

---

### 欄位 208: 熟料／水泥比 (Clinker Factor)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 技術指標 |

**Description:** 水泥產品中熟料含量佔比，數值越低表示使用更多替代性膠凝材料。

---

### 欄位 209: CCUS技術應用情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 技術採用 |

**Description:** 是否應用碳捕捉、利用與封存技術，以及年碳捕捉量。

---

### 欄位 210: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表4判斷：水泥熟料 ≤ 0.90 且水泥成品 ≤ 0.87 公噸CO2e/公噸。兩項條件須同時符合方可判定為 True。
