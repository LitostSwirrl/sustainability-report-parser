# 平面顯示器面板產業欄位 (Display Panel Industry) — 欄位 276-285

> Source: `src/field_definitions.py` → `DISPLAY_PANEL_FIELDS`
> Applicable to: Display panel industry companies (平面顯示器面板業，含LCD、OLED等光電業). Appended after base fields and manufacturing common fields. Reference standard: 附表11 — 永續經濟活動認定參考指引. Technical screening can be met via either an emissions-based threshold (Option 1) or an energy consumption threshold (Option 2), depending on panel generation.

---

### 欄位 276: 面板技術類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 主要生產的面板技術：LCD、OLED、或其他。

---

### 欄位 277: 面板世代與產線規格

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 製程資訊 |

**Description:** 說明主要產線的面板世代（如G3.5、G4、G6、G8.5等）。

---

### 欄位 278: 年基板投入面積

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 平方公尺 |
| Precision | 0.01 |
| Category | 產量 |

**Description:** 2024年基板投入總面積。

---

### 欄位 279: 單位基板溫室氣體排放量（範疇一+範疇二）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e/平方公尺 |
| Precision | 0.001 |
| Category | GHG強度 |

**Description:** 單位基板GHG排放量（範疇一+範疇二）。

**技術篩選標準 (附表11 — 選項1，排放量):**
| 面板世代 | 閾值 |
|----------|------|
| 3.5代以下 | **≤ 0.600 公噸CO2e/平方公尺** |
| 4代以上 | **≤ 0.150 公噸CO2e/平方公尺** |

---

### 欄位 280: 單位基板能源消耗量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | kWh/平方公尺 |
| Precision | 0.01 |
| Category | 能源效率 |

**Description:** 單位基板能源消耗量。

**技術篩選標準 (附表11 — 選項2，能源消耗量):**
| 面板世代 | 閾值 |
|----------|------|
| 3.5代以下 | **≤ 600 kWh/平方公尺** |
| 4代以上 | **≤ 120 kWh/平方公尺** |

---

### 欄位 281: 顯示器能效等級或認證

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品能效等級（如Energy Star）或相關認證。

---

### 欄位 282: 含氟溫室氣體減量措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 技術採用 |

**Description:** 製程使用SF6、NF3等氣體的減量或處理技術。

---

### 欄位 283: 製程廢液回收處理率

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 環境管理 |

**Description:** 製程產生的化學廢液回收處理比例。

---

### 欄位 284: 綠色產品或環境標章取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得環保標章或綠色產品相關認證。

---

### 欄位 285: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表11判斷：依面板世代選擇排放量（選項1）或能源消耗量（選項2）標準。3.5代以下：GHG ≤ 0.600 公噸CO2e/平方公尺 或 能耗 ≤ 600 kWh/平方公尺；4代以上：GHG ≤ 0.150 或能耗 ≤ 120 kWh/平方公尺。滿足任一選項即符合標準。
