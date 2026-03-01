# Group F: 水資源 (Water Resources — GRI 303) — V1 Reference

**Fields:** V1 301-310
**Note:** In V2, water fields are 66-72 in `BASE_FIELDS_V2` with a simplified structure (disaggregated by source). This document covers the V1 definitions for backward compatibility and provides GRI 303 extraction guidance applicable to both versions.

---

## Version Comparison

| Dimension | V1 (欄位 301-310) | V2 (欄位 66-72) |
|-----------|-------------------|------------------|
| Withdrawal | 總取水量 (single total, 301-302) | Split by source: 自來水(66)、地表水(67)、地下水(68)、其他(69) |
| Recycled water | 用水回收率 (307, ratio only) | 回收水量 (70, absolute volume) |
| Discharge | 總排水量 (304) | 排放水量 (71) |
| Consumption | 耗水量 (306) | 耗用水量 (72) |
| Discharge breakdown | 排水去向 (305) | Not separately tracked in V2 |
| Stress area | 是否位於水資源壓力區 (308) | Not in V2 base fields |
| Reduction target | 用水減量目標 (309-310) | Not in V2 base fields |
| Source breakdown | 取水來源分布 (303) | Disaggregated into separate fields (66-69) |

---

## V1 Water Fields (301-310)

### 欄位 301: 2024年度總取水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 報告年度的總取水量 (Water Withdrawal)，包含所有水源。單位通常為百萬公升 (ML) 或公噸。若報告書使用立方公尺 (m³)，請換算為公噸 (1 m³ = 1 公噸)。若公司有多個廠區，請加總所有國內廠區數據。通常可於 GRI 303-3 或環境績效表中找到。

**Extraction rules:**
- Primary keyword search: "總取水量", "取水量", "Water Withdrawal", "GRI 303-3"
- Always use the annual total, not a daily or monthly average
- Scope: domestic Taiwan operations only unless the report boundary explicitly includes overseas
- If the report uses ML (megalitres): 1 ML = 1,000 m³ = 1,000 公噸
- If the report uses 萬噸: multiply by 10,000 to get 公噸

**Common pitfalls:**
- "Water use" (用水量) and "water withdrawal" (取水量) may differ if the report tracks recycled water separately
- Some reports show "fresh water" only, excluding seawater — note this in 補充說明
- Do not sum across multiple years; extract only the most recent year (2024)

---

### 欄位 302: 2023年度總取水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 前一年度 (2023年) 的總取水量，用於比較年度變化。若報告書使用立方公尺 (m³)，請換算為公噸。

**Extraction rules:**
- Same methodology as 欄位 301, but for the prior-year column
- Many reports present a three-year table; pick the 2023 column
- If 2023 data is absent, leave blank and note in 補充說明

---

### 欄位 303: 取水來源分布

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 依報告書原始格式 |
| Precision | NA |
| Category | 水資源 |

**Description:** 取水來源的細項分布。固定格式：「來源: 數值 單位; 」（冒號後空格，分號後空格）。常見來源：自來水（第三方水源）、地下水、地表水（河川/湖泊）、海水、雨水收集、再生水。範例：「自來水: 1500000 公噸; 地下水: 50000 公噸; 」。若只揭露總量未分類，請在補充說明中註記。

**Extraction rules:**
- Keywords: "取水來源", "Water Sources", "GRI 303-3 (by source)"
- Record all sources listed in the report with their respective volumes
- Use the exact unit the report uses; do not convert
- If the report only gives percentages without absolute values, record the percentages and note the absence of absolute figures

**V2 mapping:** This field maps to V2 fields 66 (自來水), 67 (地表水), 68 (地下水), 69 (其他) where each source has its own field.

---

### 欄位 304: 2024年度總排水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 報告年度的總排水量 (Water Discharge)。單位通常為百萬公升 (ML) 或公噸。若報告書使用立方公尺 (m³)，請換算為公噸。排水量通常小於取水量，差額為耗水量。

**Extraction rules:**
- Keywords: "排水量", "廢水排放量", "放流水量", "Water Discharge", "GRI 303-4"
- If the report separates treated wastewater and untreated discharge, sum them
- Verify: withdrawal (301) - discharge (304) should approximately equal consumption (306); flag anomalies in 補充說明

**V2 mapping:** Maps to V2 field 71 (排放水量).

---

### 欄位 305: 排水去向分布

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 依報告書原始格式 |
| Precision | NA |
| Category | 水資源 |

**Description:** 排水去向的細項分布。固定格式：「去向: 數值 單位; 」。常見去向：污水處理廠、地表水體、海洋、地下滲透、其他第三方。範例：「污水處理廠: 1200000 公噸; 地表水體: 100000 公噸; 」。若只揭露總量，請在補充說明中註記。

**Extraction rules:**
- Keywords: "排放去向", "廢水去向", GRI 303-4 destination breakdown
- Common destinations (中文/English pairs): 公共污水下水道/municipal sewer, 河川/river, 海洋/ocean, 再利用/reuse, 工業區污水廠/industrial wastewater plant
- Record in the format specified above

---

### 欄位 306: 2024年度耗水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 報告年度的耗水量 (Water Consumption) = 取水量 - 排水量。耗水量代表被蒸發、納入產品、或無法回收的水量。若報告書未直接提供，但有取水量與排水量，請協助計算並在補充說明中註記計算方式。

**Extraction rules:**
- Keywords: "耗水量", "Water Consumption", "GRI 303-5"
- If the report explicitly states a consumption figure, use it
- If not stated, calculate: consumption = withdrawal (301) - discharge (304)
- Always note in 補充說明 whether this was directly reported or calculated

**V2 mapping:** Maps to V2 field 72 (耗用水量). Note: V2 guidance instructs NOT to calculate if not directly reported.

**Common pitfalls:**
- Some companies report "net water use" which may already be consumption; verify the definition
- Recycled water that is reused internally should not inflate the withdrawal figure — check if recycled water is counted in both withdrawal and internal use

---

### 欄位 307: 用水回收率

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 水資源 |

**Description:** 製程用水或總用水的回收再利用比例。以小數表示，例如回收率85%請填0.85。此數值可能出現在水資源管理章節或環境績效統計表中。若報告書提供回收水量而非比例，請協助計算比例（回收水量 / 總用水量）。

**Extraction rules:**
- Keywords: "回收率", "水回收", "廢水回收再利用", "Water Recovery Rate", "Recycling Rate"
- If given as a percentage string (e.g., "85%"), convert to decimal (0.85)
- If only volume is provided: rate = recycled volume / total withdrawal
- Note the denominator used (total withdrawal vs. total process water) in 補充說明

**V2 mapping:** V2 uses an absolute volume (field 70: 回收水量) instead of a ratio.

---

### 欄位 308: 是否位於水資源壓力區

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 水資源 |

**Description:** 公司營運據點是否位於水資源壓力區域 (Water-stressed Areas)？報告書可能引用 WRI Aqueduct 或 WWF Water Risk Filter 等工具評估。填答只有 True/False 兩種可能性，若報告書未提及水資源壓力風險評估，請留空。

**Extraction rules:**
- Keywords: "水資源壓力", "缺水風險", "Water Stress", "WRI Aqueduct", "WWF Water Risk Filter"
- True if: the report confirms any facility is in a high/extremely high water stress area
- False if: the report explicitly states no facilities are in water-stressed areas
- Leave blank if: the report is entirely silent on this topic

---

### 欄位 309: 是否設定用水減量目標

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 水資源 |

**Description:** 公司是否設定用水減量或水資源管理目標？例如：「2030年用水強度降低20%」或「2025年水回收率達90%」。填答只有 True/False 兩種可能性，無法判斷時請留空。

**Extraction rules:**
- Keywords: "節水目標", "用水目標", "水資源目標", "Water Reduction Target"
- A quantified target with a year counts as True
- A vague statement like "持續改善用水效率" without a specific target counts as False
- Leave blank only when the report contains insufficient information to judge

---

### 欄位 310: 用水減量目標說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 水資源 |

**Description:** 若有設定用水減量目標，請簡要說明目標內容（限50字）。包含目標年份、目標值、基準年。格式範例：「2030年用水強度較2020年降低20%」。若無目標或欄位309為False，請留空。

**Extraction rules:**
- Only fill if 欄位 309 = True
- Concise format: target year + metric + reduction percentage + base year (if given)
- If multiple targets exist, describe the most quantitatively specific one; mention others in 補充說明

---

## V2 Water Fields Reference (欄位 66-72)

These are the V2 counterparts in `BASE_FIELDS_V2`. Refer to `docs/field_definitions/base_fields.md` for full definitions.

| V2 Field | Name | Unit | Notes |
|----------|------|------|-------|
| 66 | 取水量-自來水 | 噸 | Third-party water supply only |
| 67 | 取水量-地表水 | 噸 | Rivers, streams, weirs |
| 68 | 取水量-地下水 | 噸 | Groundwater extraction |
| 69 | 取水量-其他來源 | 噸 | Seawater, condensate, rainwater, recycled water from external sources |
| 70 | 回收水量 | 噸 | Internal reuse; may exceed withdrawal due to multiple circulation cycles |
| 71 | 排放水量 | 噸 | Final wastewater discharged off-site |
| 72 | 耗用水量 | 噸 | Only fill if explicitly stated; do NOT calculate in V2 |

---

## GRI 303 Search Guide

### Standard reference points:
- **GRI 303-3**: Water withdrawal — total and by source
- **GRI 303-4**: Water discharge — total and by destination
- **GRI 303-5**: Water consumption — net consumption

### Typical document locations:
1. GRI Content Index (cross-reference table at back of report)
2. Environmental performance data appendix (環境績效附錄)
3. Water management chapter (水資源管理章節)
4. CSR / ESG data summary table

### Unit conversion reference:
| From | To | Factor |
|------|----|--------|
| 1 ML (megalitre) | 公噸 | × 1,000 |
| 1 m³ | 公噸 | × 1 |
| 1 萬噸 | 公噸 | × 10,000 |
| 1 千度 (kL) | 公噸 | × 1 |
| 1 億噸 | 公噸 | × 100,000,000 |

---

## Output Format

For each field, output:

```
欄位 [ID]: [Value]
補充說明: [Unit conversion method, scope notes, whether calculated or directly reported, any data gaps]
```

If the value cannot be determined:
```
欄位 [ID]: 無法填答
補充說明: [Reason — not disclosed, report scope mismatch, ambiguous units, etc.]
```

---

## Common Pitfalls

1. **Unit confusion**: Reports may mix ML, m³, 公噸, and 萬噸 in the same table — always check unit headers carefully
2. **Recycled water double-counting**: If recycled water is counted as both a "source" and a "withdrawal", the total withdrawal figure may be inflated
3. **Scope mismatch**: Some companies report global figures in the main body but Taiwan-only figures in the appendix — use the figure that matches the report boundary
4. **Missing discharge data**: Many companies report withdrawal but omit discharge; do not calculate discharge from other fields — leave blank and note
5. **"Water intensity" vs. absolute volume**: Intensity metrics (m³ per unit output) cannot be used to fill these fields; absolute volumes are required
