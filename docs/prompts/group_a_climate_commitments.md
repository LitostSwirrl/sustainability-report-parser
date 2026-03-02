# Group A: 氣候承諾 (Climate Commitments)

**Fields:** 1-8
**Focus:** Net-zero targets, mid-term GHG absolute reduction goals, SBT certification

---

## PDF Reading Strategy

Read these sections of the report in order:

1. **Table of contents** — identify which chapters cover climate strategy, carbon management, TCFD
2. **Chairman's message / CEO letter** — often contains top-level commitment statements with target years
3. **Climate strategy / TCFD chapter** — detailed target descriptions, base years, reduction percentages
4. **GHG inventory or appendix** — base year emission quantities, historical data
5. **GRI appendix / index** — use GRI 305 cross-reference to locate GHG commitment pages quickly

Search keywords: 淨零、碳中和、2050、中期目標、SBT、SBTi、科學基礎、基準年、減量目標

---

## Field Definitions

### 欄位 1: 是否承諾淨零排放／碳中和
- **Data Format:** string
- **Unit:** NA
- **Description:** 若有淨零/碳中和承諾，請節錄關鍵句（50字以內），包含目標年份。若無明確承諾，填「無承諾」。不需完整引用，只需核心內容。
- **Example output:** `2050年達成淨零排放，以2018年為基準年` or `無承諾`

### 欄位 2: 預計達成淨零排放／碳中和年份
- **Data Format:** integer
- **Unit:** NA
- **Description:** 請只填入西元年份。若沒有明確承諾，請留空。若原始資料為民國年份，請協助轉換（民國年+1911=西元年）。
- **Example output:** `2050`

### 欄位 3: 是否設定中期溫室氣體絕對減量目標
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 企業是否設定了在達到淨零前的中期減量檢核點？True=有設定；False=明確表示無；留空=報告書完全未提及。
- **Note:** 中期目標通常以 2025、2030 為目標年，並設定相對基準年的絕對減量百分比。

### 欄位 4: 中期減量目標年設定
- **Data Format:** integer
- **Unit:** NA
- **Description:** 請只填入年份（西元年）。若沒有明確設定，請留空。若有多個目標年，填最近的一個，並在補充說明中敘明所有目標年。
- **Example output:** `2030`

### 欄位 5: 中期溫室氣體絕對減量目標值（百分比）
- **Data Format:** decimal
- **Unit:** NA (以小數表示)
- **Precision:** 0.0001
- **Description:** 以小數表示，如30%填0.3。以下情況**不算**中期絕對減量目標，請留空：
  - 「單位產品碳排放係數」降低（intensity-based，非絕對量）
  - 「xx年的溫室氣體總排放量回到xx年水準」（無明確減量幅度）
  - 「僅針對特定廠有設定減排目標」（非公司整體）
- **Example output:** `0.3` (代表目標減量30%)

### 欄位 6: 中期減量基準年設定
- **Data Format:** integer
- **Unit:** NA
- **Description:** 中期目標對應的基準年西元年份。若未提供明確基準年，則留空。
- **Example output:** `2018`

### 欄位 7: 中期減量基準年排放量
- **Data Format:** decimal
- **Unit:** 公噸CO2e
- **Precision:** 0.0001
- **Description:** 中期目標的基準年碳排放量。若未提供明確基準年數據，則留空。通常在GHG盤查附錄的歷年趨勢表可找到。
- **Example output:** `1705790`

### 欄位 8: 中期目標是否取得SBT認證
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 中期減量目標是否取得科學基礎減量目標認證（SBT/SBTi）。True=已取得認證；False=明確表示未取得；留空=報告書未提及。
- **Key distinction:** SBTi「已承諾」(Committed) ≠ SBTi「已通過認證」(Approved/Validated)。只有已通過認證才填True。

---

## Extraction Rules (for this group)

### Boolean judgment
- **True**: report explicitly states 「是」「有」「已取得」「已達成」「已認證」
- **False**: report explicitly states 「否」「無」「未取得」「未達成」
- **留空**: report does not mention the topic at all — do NOT write False just because it is absent

**例外 — 欄位 8 (SBTi認證)**：若報告書完全未提及 SBT/SBTi，應填 `False`（非留空）。
已取得 SBTi 認證的公司必然會在報告書中揭露此成就，因此未提及即代表未取得。
此規則僅適用於 F8，不適用於 F3（中期目標）。

### Numeric format
- All values without thousand separators: write `1705790`, not `1,705,790`
- Percentages as decimals: 42% → `0.42`
- Do not fill zero when data is absent — leave blank

### 民國 to 西元 conversion
- 民國 109 年 → 2020; 民國 114 年 → 2025; 民國 139 年 → 2050

### Absolute vs. intensity-based targets
- **Absolute**: 「相較基準年減少30%」— qualifies for field 5
- **Intensity**: 「單位產品碳排強度降低30%」or 「每度電排碳降低30%」— does NOT qualify for field 5

### Source page documentation
- Always record page numbers in format `p.45` or `p.45, p.67`
- Write `NA` only if genuinely no page can be identified
- Check GRI appendix first (GRI 305) for page cross-references

### 補充說明 rules
- Every field must have a 補充說明, even if the field is blank
- When data found: note the source, whether figures were converted or summed, any caveats
- When data absent: describe what was searched and why the field is blank

---

## Output Format

For each field, output exactly in this format:

```
---欄位1開始---
欄位數值: [value or empty]
欄位單位: [unit or NA]
補充說明: [source, calculation method, or reason for blank — max 200 chars]
參考頁數: [p.X, p.Y or NA]
---欄位1結束---
```

Full example for a company with a commitment:

```
---欄位1開始---
欄位數值: 2050年達成供應鏈淨零排放，以2018年為基準
欄位單位: NA
補充說明: 來自董事長致詞及氣候策略章節，承諾範圍含範疇一、二、三
參考頁數: p.12, p.45
---欄位1結束---

---欄位2開始---
欄位數值: 2050
欄位單位: NA
補充說明: 明確揭露2050年達成淨零目標
參考頁數: p.12
---欄位2結束---

---欄位3開始---
欄位數值: True
欄位單位: NA
補充說明: 公司設定2030年中期減量目標，相較2018年絕對減量46%
參考頁數: p.47
---欄位3結束---
```

---

## Common Pitfalls

1. **Product carbon neutral ≠ company-wide net-zero**: a product-level carbon neutral claim (e.g., a specific server model) does not count as a company-wide net-zero commitment for field 1.

2. **Aspirational statements ≠ formal commitments**: phrases like 「努力邁向」「朝向淨零目標前進」without a specific year are NOT a commitment. Field 1 should be blank or note the aspirational language only.

3. **SBTi Committed ≠ SBTi Approved**: the SBTi website lists companies as "Committed" when they have pledged to submit targets, and "Targets Set" or "Approved" after validation. Field 8 is True only when the report confirms targets have been approved/validated.

4. **Multiple mid-term targets**: a company may have 2025, 2030, and 2035 targets. Field 4 takes the nearest future year; list all years in 補充說明.

5. **Scope 1+2 only vs. all scopes**: some companies set mid-term targets only for Scope 1+2. This still qualifies for field 3/5, but note the scope limitation in 補充說明.

6. **民國 year confusion**: older sections of Taiwanese reports may quote targets in 民國 years. Always convert to 西元 before filling field 2, 4, or 6.

7. **Intensity target masquerading as absolute**: watch for phrases like 「相較基準年減少單位產值排碳30%」— the word 「單位」indicates intensity, not absolute.

8. **Base year emission in different units**: if the base year emission is given in kt CO2e or Mt CO2e, convert to 公噸CO2e before filling field 7 (1 kt = 1,000 公噸; 1 Mt = 1,000,000 公噸).
