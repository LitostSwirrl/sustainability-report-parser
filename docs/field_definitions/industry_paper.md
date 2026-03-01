# 造紙產業欄位 (Paper Industry) — 欄位 256-265

> Source: `src/field_definitions.py` → `PAPER_FIELDS`
> Applicable to: Paper industry companies (造紙業), including pulp, paperboard, corrugated, tissue, printing/writing paper, and specialty paper producers. Appended after base fields and manufacturing common fields. Reference standard: 附表9 — 永續經濟活動認定參考指引. GHG thresholds vary by paper product type; the standard unit is Air Dry Ton (Adt).

---

### 欄位 256: 主要紙類產品類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 列舉主要生產的紙類：漂白硫酸鹽漿、紙板、紙箱用紙(裱面紙板/瓦楞芯紙)、家庭用紙、印刷書寫用紙、特殊紙。

---

### 欄位 257: 紙類年產量（氣乾噸Adt）

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | Adt |
| Precision | NA |
| Category | 產量 |

**Description:** 各類紙品年產量，以氣乾噸(Air Dry Ton, Adt)為單位。

---

### 欄位 258: 紙類產品單位溫室氣體排放量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 公噸CO2e/Adt |
| Precision | NA |
| Category | GHG強度 |

**Description:** 各紙類GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表9):**
| 產品類型 | 閾值 |
|----------|------|
| 漂白硫酸鹽漿 | **≤ 0.70 公噸CO2e/Adt** |
| 紙板 | **≤ 0.90 公噸CO2e/Adt** |
| 裱面紙板 | **≤ 0.90 公噸CO2e/Adt** |
| 瓦楞芯紙 | **≤ 0.90 公噸CO2e/Adt** |
| 家庭用紙 | **≤ 1.60 公噸CO2e/Adt** |
| 印刷書寫用紙 | **≤ 0.90 公噸CO2e/Adt** |
| 特殊紙 | **≤ 2.20 公噸CO2e/Adt** |

---

### 欄位 259: 單位產品能源消耗量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | Mcal/Adt |
| Precision | 0.01 |
| Category | 能源效率 |

**Description:** 紙類生產能源消耗強度。

---

### 欄位 260: 廢紙回收使用比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 使用廢紙或再生原料佔總原料投入之比例。

---

### 欄位 261: 事業廢棄物回收再利用率

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 循環經濟 |

**Description:** 製程產生的事業廢棄物回收再利用比例。

---

### 欄位 262: COD（化學需氧量）產生量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公斤/Adt |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 單位產品COD產生量或排放量。

---

### 欄位 263: FSC/PEFC森林認證情形

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 是否取得FSC或PEFC等森林管理認證。

---

### 欄位 264: 綠色產品或環保標章取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得環保標章或綠色產品認證。

---

### 欄位 265: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表9判斷：各紙類產品GHG排放量是否符合對應閾值。各產品閾值見欄位258說明。
