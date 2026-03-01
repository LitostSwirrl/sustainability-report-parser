# Group E: 勞動安全與排碳 (Labor Safety & Emissions) — V1 Reference

**Fields:** V1 201-209 (mapped to V2 fields 39-41, 58-65)
**Note:** In V2, these fields are integrated into the base fields. This document is a supplementary reference for V1-era labor and coal/fossil-fuel fields. When running the V2 extraction pipeline, use `base_fields.md` sections 39-41 and 58-65 instead.

---

## V1 to V2 Mapping

| V1 Field | V2 Field | Name |
|----------|----------|------|
| 201 (LTIFR) | 58 | 失能傷害頻率 (LTIFR) |
| 202 (職災件數) | 59 | 職業傷害件數 |
| 204 (損失工時) | 60 | 損失工作日數 |
| 203 (重大事件) | 61 | 重大職業安全意外事件 |
| 205 (勞動法規) | 62 | 勞動法規違規與裁罰 |
| 206 (政府補貼) | 63 | 政府補貼或獎勵 |
| 207 (燃煤) | 39 | 燃煤使用量 |
| 208 (燃煤淘汰) | 40 | 燃煤淘汰計劃 |
| 209 (化石燃料) | 41 | 化石燃料轉型計劃 |

---

## V1 Field Definitions (201-209)

### 欄位 201: 失能傷害頻率 (LTIFR)

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職業安全 |

**Description:** 報告年度的失能傷害頻率 (Lost Time Injury Frequency Rate)。計算公式：(失能傷害件數 × 1,000,000) / 總工時。請分別列出男性與女性數值，若報告書僅提供整體數值，請填寫整體數值並在補充說明中註記。

**Extraction rules:**
- Look for "失能傷害頻率", "LTIFR", "Lost Time Injury Frequency Rate"
- May appear in GRI 403-9 disclosure or the occupational safety statistics table
- If only an overall figure is provided (no gender breakdown), record it and note the limitation
- Formula verification: value = (incidents × 1,000,000) / total working hours

**Common pitfalls:**
- Do not confuse LTIFR with TRIFR (Total Recordable Injury Frequency Rate)
- Some reports use 200,000 hours (OSHA standard) instead of 1,000,000; note which base was used
- Zero is a valid answer — do not leave blank if the report explicitly states zero injuries

---

### 欄位 202: 職業傷害件數

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職業安全 |

**Description:** 報告年度發生的職業傷害總件數。請分別列出死亡、永久失能、暫時失能件數。格式範例：「死亡0件、永久失能0件、暫時失能5件」。若報告書有依性別分類，請一併列出。

**Extraction rules:**
- Look for "職業傷害", "職業災害", "工安事故", GRI 403-9
- Breakdown expected: 死亡 (fatalities) / 永久失能 (permanent disability) / 暫時失能 (temporary disability)
- Report scope: Taiwan domestic operations only (exclude overseas unless the report explicitly includes them in the boundary)

**Common pitfalls:**
- "工安事故件數" may include near-miss events; ensure you are counting confirmed injuries only
- Separate contractor (承攬商) figures from employee figures if both are provided
- If only a total is given without breakdown, record the total and note the lack of breakdown in 補充說明

---

### 欄位 203: 重大職業安全意外事件

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職業安全 |

**Description:** 報告年度是否有發生重大職業安全意外事件？重大事件包含：造成死亡、永久失能、多人受傷之事故，以及火災、爆炸等工安事故。若有發生，請填入傷亡人數與說明文字（如：「死亡1人，因鍋爐爆炸事故」）；若無請填「無」。

**Extraction rules:**
- Search for dedicated "重大事故" or "重大工安事件" sections
- GRI 403-9 and 403-10 may contain this information
- Include fire (火災), explosion (爆炸), chemical leak (化學品洩漏), and structural collapse (坍塌)
- If the report explicitly states no major incidents occurred, fill "無"

**Common pitfalls:**
- Do not conflate "important" (重要) safety initiatives with "major" (重大) incidents
- Near-misses (虛驚事件) do not qualify unless they led to actual harm

---

### 欄位 204: 損失工作日數

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 日 |
| Precision | 0.01 |
| Category | 職業安全 |

**Description:** 報告年度因職業傷害造成的損失工作日數 (Lost Days / Lost Workdays)。此數值通常出現在職業安全統計表格中。

**Extraction rules:**
- Keywords: "損失工作日", "損失日數", "失能日數", "Lost Days", "Lost Workdays"
- Typically found in the occupational safety data table in the appendix (附錄)
- Some reports express this as "severity rate" — if so, record the raw lost-days figure, not the rate
- Zero is valid if the report states no lost time occurred

**Common pitfalls:**
- Do not include sick leave (病假) unless it was caused by a work-related injury
- "Restricted work days" and "transferred work days" are sometimes counted separately; include only "lost days" unless the report uses a combined figure

---

### 欄位 205: 勞動法規違規與裁罰

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 法規遵循 |

**Description:** 報告年度是否有違反勞動相關法規之情事？若有，請列出違規法條、違規內容與裁罰金額。相關法規包含：職業安全衛生法、勞動基準法、性別工作平等法等。格式範例：「違反職業安全衛生法第6條，罰款新台幣10萬元」。若無違規請填「無」。

**Extraction rules:**
- Search for "勞動法規", "裁罰", "罰款", "違規", "行政裁處"
- Check the compliance / legal section and the GRI 419 disclosure
- Include all violations: fines, warnings, mandatory improvement orders (改善通知)
- Record the law name, article number (if given), nature of violation, and penalty amount

**Common pitfalls:**
- An "improvement order" with no monetary fine is still a violation — record it
- Environmental fines (環保裁罰) are separate from labor fines — include only labor-related penalties here
- If the report is silent on violations, do not assume "無"; note "未揭露" instead

---

### 欄位 206: 政府補貼或獎勵

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 政府互動 |

**Description:** 報告年度是否接受政府補貼或獎勵計劃？若有，請說明計劃名稱與補貼金額。範例：「經濟部工業局智慧製造補助計劃，補助金額新台幣500萬元」。若無或未揭露請填「無」或「未揭露」。

**Extraction rules:**
- Keywords: "政府補助", "政府獎勵", "補貼", "補助款", "研究計劃補助"
- Check government relations / public policy sections and financial statement notes
- Include central government and local government subsidies
- Format: scheme name + amount (if disclosed)

**Common pitfalls:**
- Tax incentives (稅捐減免) are a form of government subsidy; include them if disclosed with a monetary value
- Award certificates (獎牌/表揚) without monetary value do not qualify as "補貼或獎勵" for this field
- If no amount is disclosed, still record the scheme name and note the amount as "未揭露"

---

### 欄位 207: 燃煤使用量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 依報告書原始格式 |
| Precision | NA |
| Category | 能源使用 |

**Description:** 報告年度的燃煤使用量。燃煤包含煙煤 (bituminous coal)、無煙煤 (anthracite)、褐煤 (lignite) 等。若公司不使用燃煤請填「0」或「不適用」。數值通常可在能源使用細項表格中找到。

**V2 Note:** In V2 this maps to field 39. The extraction logic is identical.

**Extraction rules:**
- Keywords: "燃煤", "煤炭", "煤", "coal", "無煙煤", "褐煤"
- Record the value in the unit reported (公噸, 千公噸, GJ, etc.)
- If the energy breakdown table shows zero for coal, fill "0"
- If coal is not listed at all in the energy table, fill "不適用"

**Common pitfalls:**
- Coke (焦炭) used in steel production may be listed separately — include it only if the report groups it under "燃煤"
- Do not convert units; record in original format

---

### 欄位 208: 燃煤淘汰計劃

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 公司是否有燃煤淘汰或減量計劃？若有，請說明目標年份與減量目標。範例：「預計於2030年前完全淘汰燃煤使用」。若不使用燃煤或無相關計劃請填「不適用」或「無」。

**V2 Note:** In V2 this maps to field 40.

**Extraction rules:**
- Keywords: "燃煤淘汰", "煤炭退出", "去煤", "coal phase-out", "coal-free"
- Look in climate action / decarbonization strategy sections
- Record target year and scope of phase-out (complete vs. partial reduction)
- If the company already reports zero coal usage, fill "不適用"

---

### 欄位 209: 化石燃料轉型計劃

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 公司是否有化石燃料整體轉型計劃？若有，請說明轉型目標與時程。化石燃料包含：煤炭、天然氣、石油及其衍生燃料。請說明公司如何減少對化石燃料的依賴，例如：提高再生能源佔比、改用低碳燃料等。若無相關計劃請填「無」。

**V2 Note:** In V2 this maps to field 41.

**Extraction rules:**
- Keywords: "化石燃料", "fossil fuel", "能源轉型", "低碳燃料", "燃料替換"
- Look in energy strategy and climate action chapters
- Distinguish between coal phase-out (欄位208) and broader fossil fuel transition (此欄位)
- Record the transition strategy type (e.g., 提高再生能源比例、改用天然氣、切換生質能) and timeline

**Common pitfalls:**
- A general net-zero commitment is not the same as a fossil fuel transition plan; require specific fuel-switching actions
- If the report only mentions coal phase-out but is silent on natural gas / oil, note that limitation

---

## Output Format

For each field, output the extracted value in the following structure:

```
欄位 [ID]: [Value]
補充說明: [Any caveats, unit conversions, scope notes, or data gaps]
```

If the value cannot be determined from the report, output:
```
欄位 [ID]: 無法填答
補充說明: [Reason — e.g., not disclosed, section missing, ambiguous data]
```

---

## Common Search Locations (V1 era)

1. **Appendix / 附錄** — occupational safety statistics tables (GRI 403-9, 403-10)
2. **Labor / HR chapter** — 人力資源、員工關係、職業安全衛生 sections
3. **Environmental chapter** — energy breakdown tables for coal usage (欄位207)
4. **Climate strategy section** — phase-out and transition plans (欄位208-209)
5. **GRI Content Index** — cross-reference GRI 403 (occupational H&S) and GRI 302 (energy)
