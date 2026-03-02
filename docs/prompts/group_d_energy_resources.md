# Group D: 能源、透明度、氣候行動、燃煤、再生能源、勞動、水資源

**Fields:** 31-72
**Focus:** Data transparency, energy use, coal/fossil fuels, electricity, renewables, climate action targets, low-carbon products, labor safety, water resources

This is the largest group. Work through each sub-section systematically.

---

## Scope Boundary Rules

Different sub-groups may have different reporting boundaries. Follow these rules:

| Sub-Group | Fields | Boundary Rule |
|-----------|--------|---------------|
| 能源 (Energy) | F34-38, F42-43 | Company-wide reported total (all sites globally) |
| 氣候行動 (Climate targets) | F48-55 | Company-wide |
| 勞動 (Labor safety) | F58-65 | Taiwan operations preferred; if overseas data is included, note it in 補充說明 |
| 水資源 (Water) | F66-72 | Taiwan operations preferred; if overseas data is included, note it in 補充說明 |

When the report provides both Taiwan-only and consolidated figures, prefer Taiwan-only for labor/water fields unless only the consolidated figure is available. Always note the scope in 補充說明.

---

## PDF Reading Strategy

Use the GRI index to locate all sections before reading body text:

| Topic | GRI reference | Search keywords |
|-------|---------------|-----------------|
| GHG history | GRI 305-1/2/3 | 三年排放、近三年 |
| Energy total | GRI 302-1 | 總能源、能源使用量、GJ、MJ |
| Energy breakdown | GRI 302-1 | 天然氣、柴油、電力使用量 |
| Coal | GRI 302-1 | 燃煤、煤炭、煙煤、無煙煤 |
| Fossil fuels | climate/energy chapter | 化石燃料、能源轉型 |
| Electricity | GRI 302-1 | 用電量、外購電力 |
| Renewables | GRI 302-1 | 再生能源、太陽能、風電 |
| RE targets | climate chapter | RE100、用電大戶、再生能源目標 |
| Energy saving | climate/energy chapter | 節能目標、節電目標 |
| Climate strategies | climate chapter | 減碳策略、低碳轉型 |
| Low-carbon products | product/business chapter | 低碳產品、綠色產品、轉型活動 |
| Labor safety | GRI 403 | 職業安全、失能傷害、LTIFR、GRI 403-9 |
| Water | GRI 303-3/4/5 | 取水量、排水量、耗水量 |

---

## Sub-Group D1: 資料透明度 (Fields 31-33)

### 欄位 31: 是否揭露近三年溫室氣體排放資料
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 企業是否有逐年揭露溫室氣體排放狀況（2022-2024年）。通常可於最後附錄查詢。若報告書只揭露兩年，則為 False。
- **Example output:** `True`

### 欄位 32: 是否設定範疇三減量目標
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 判斷公司是否針對範疇三（Scope 3）設定減量目標或規劃。有設定=True；明確表示沒有=False；未提及=留空。

### 欄位 33: 範疇三減量目標實際作為
- **Data Format:** string
- **Unit:** NA
- **Description:** 範疇三的具體減碳作為（限3項）。**固定格式**：「作為1、作為2、作為3」。每項必須是4-10字的名詞短語。若無具體作為或僅有宣示性文字，留空。
- **Example output:** `供應商減碳輔導、綠色採購、物流優化`
- **Wrong format:** full sentences, 或超過10字的描述

---

## Sub-Group D2: 能源 (Fields 34-38)

### 欄位 34: 2024年度總能源使用量
- **Data Format:** decimal
- **Unit:** MJ
- **Precision:** 0.0001
- **Description:** 通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用（電力換算為熱量後一併計入）。通常可於最後面的附錄查詢得到。
- **Unit note:** The field unit is **MJ**. If the report uses GJ, multiply by 1,000. If report uses TJ, multiply by 1,000,000.
- **Example output:** `8234567.0000` (in MJ)

### 欄位 35: 2023年度總能源使用量
- **Data Format:** decimal
- **Unit:** MJ
- **Precision:** 0.0001
- **Description:** 同上，2023年度數值。

### 欄位 36: 2022年度總能源使用量
- **Data Format:** decimal
- **Unit:** MJ
- **Precision:** 0.0001
- **Description:** 同上，2022年度數值。

### 欄位 37: 是否揭露各項能源使用細項
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 是否揭露2024年使用的各種能源細項（如電力、天然氣、柴油等分項數值）。有揭露=True；無揭露或只有總量=False；未提及=留空。

### 欄位 38: 2024年度使用的各種能源項目
- **Data Format:** string
- **Unit:** 依報告書原始格式
- **Description:** 列出各能源使用量。**固定格式**：「能源: 數值 單位; 」（冒號後有空格，分號後有空格）。
- **排列順序**：電力 > 天然氣 > 柴油 > 汽油 > 液化石油氣 > 燃料油 > 其他
- **Rules**:
  - 數值不含千分位符號
  - 只列出報告書中有記載的項目
  - 零值不列出
- **Example output:** `電力: 206234 千度; 天然氣: 25283 千立方公尺; 柴油: 634 公秉; `
- **Note:** Preserve original units from the report (千度, GJ, 公秉 etc.) — do not convert

---

## Sub-Group D3: 燃煤 (Fields 39-41)

### 欄位 39: 燃煤使用量
- **Data Format:** string
- **Unit:** 依報告書原始格式
- **Description:** 報告年度的燃煤使用量。燃煤包含煙煤、無煙煤、褐煤等。若公司明確表示不使用燃煤（如「本公司無煤炭」或能源表完整列舉所有來源且無燃煤），填 `0`。若報告書未提及燃煤，留空。數值通常可在能源使用細項表格中找到。
- **Example output:** `12500 公噸` or `0`

### 欄位 40: 燃煤淘汰計劃
- **Data Format:** string
- **Unit:** NA
- **Description:** 公司是否有燃煤淘汰或減量計劃？若有，請說明目標年份與減量目標。若不使用燃煤，請填「不適用」。若使用燃煤但無計劃，填「無」。
- **Example output:** `預計2030年前完全淘汰燃煤使用`

### 欄位 41: 化石燃料轉型計劃
- **Data Format:** string
- **Unit:** NA
- **Description:** 公司是否有化石燃料整體轉型計劃？化石燃料包含煤炭、天然氣、石油。請說明轉型目標與時程。若無相關計劃請填「無」。
- **Example output:** `2035年前以天然氣替代燃煤、2040年前轉為再生能源`

---

## Sub-Group D4: 用電 (Fields 42-43)

### 欄位 42: 當年度總用電量
- **Data Format:** decimal
- **Unit:** 度（KWh）
- **Precision:** 0.0001
- **Description:** 只看該公司使用電力或外購電力的數值，自行使用再生能源發電不計入。以報告書原記錄單位為主（可能為度、千度、萬度、GJ等）。
- **Unit note:** The field unit is 度（KWh）. If the report uses GJ, apply: 1 GJ = 277.778 KWh. If it uses MWh, multiply by 1,000. If it uses 千度, multiply by 1,000.
- **Example output:** `206234000` (in KWh, converted from 206,234 千度)

### 欄位 43: 再生能源使用佔總發電量（百分比）
- **Data Format:** decimal
- **Unit:** NA (以小數表示)
- **Precision:** 0.0001
- **Description:** 透過利用再生能源所產生之發電量，佔總發電量的比例。以小數表示（38%→0.38）。通常可於最後面附錄查詢得到。

---

## Sub-Group D5: 再生能源 (Fields 44-47)

### 欄位 44: 再生能源裝置容量
- **Data Format:** decimal
- **Unit:** 瓩（KW）
- **Precision:** 0.001
- **Description:** 僅收公司自行建置的再生能源（太陽光電、風電、地熱等）。只收**確定建置完成**的容量，不收規劃/預計/施工中的數值。
- **Note:** If the report gives capacity in MW, multiply by 1,000 to convert to KW.

### 欄位 45: 再生能源使用來源（自發自用、購電協議、再生能源憑證）
- **Data Format:** string
- **Unit:** NA
- **Description:** 公司使用的再生能源來源。常見來源：自發自用（Self-generated）、購電協議（PPA/Power Purchase Agreement）、再生能源憑證（T-REC/I-REC）。列出所有使用的來源。
- **Example output:** `自發自用、再生能源憑證(T-REC)、購電協議(PPA)`

### 欄位 46: 是否達成政府用電大戶再生能源建置義務
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 如果有達到，通常報告書會寫「已達到/遠高於政府用電大戶條款所規定的10%」。判斷標準：True 表示已明確達成義務，False 表示公司明確表示未達成，留空表示報告書未提及或僅描述法規背景而未說明是否達成。注意：僅描述用電大戶條款內容（法規介紹）不等於已達成義務。

### 欄位 47: 是否取得RE100認證
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 請判斷企業之再生能源目標，是否取得RE100目標認證。RE100是全球再生能源倡議，要求企業承諾100%使用再生能源。True=已加入RE100；False=明確未加入；留空=未提及。

---

## Sub-Group D6: 氣候行動 (Fields 48-55)

### 欄位 48: 是否設定再生能源使用目標
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 是否設定要於何時達到再生能源使用率幾%。有設定=True；明確無=False；未提及=留空。

### 欄位 49: 再生能源目標年設定
- **Data Format:** integer
- **Unit:** NA
- **Description:** 請只填入目標年份（西元年）。若未提及或未設定，請留空。若目標年為2050，請視為沒有具體中期目標並留空。

### 欄位 50: 再生能源目標值（百分比）
- **Data Format:** decimal
- **Unit:** NA (以小數表示)
- **Precision:** 0.0001
- **Description:** 請填入目標值的數字，以小數表示（如目標使用率50%，填0.5）。

### 欄位 51: 是否設定節能目標
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 節能、節電等皆可算入。僅處理**明確寫出節能目標設定**的內容（有具體目標值或目標年）。有設定=True；明確無=False；未提及=留空。

### 欄位 52: 節能目標年設定
- **Data Format:** integer
- **Unit:** NA
- **Description:** 請只填入年份（西元年）。若沒有明確承諾，請留空。

### 欄位 53: 節能目標值（百分比）
- **Data Format:** decimal
- **Unit:** NA (以小數表示)
- **Precision:** 0.0001
- **Description:** 請填入節能目標值，以小數表示（如節能30%填0.3）。

### 欄位 54: 節電目標值設定（百分比）
- **Data Format:** decimal
- **Unit:** NA (以小數表示)
- **Precision:** 0.0001
- **Description:** 填入公司設定的節電目標值（以小數表示，例如節電2%請填0.02）。並非實際節電量，而是設定的目標。無法填答時請留空。
- **Note:** Field 53 is an energy-saving target (general); field 54 is a specific electricity-saving target. Both may exist simultaneously.

### 欄位 55: 是否說明關鍵減量策略
- **Data Format:** string
- **Unit:** NA
- **Description:** 列舉公司主要減碳策略（限5項）。**固定格式**：「策略1、策略2、策略3」。每項必須是4-8字的名詞短語。
- **Example output:** `燃煤改天然氣、太陽能發電、設備汰換、製程優化、採購再生能源`
- **Wrong format:** complete sentences, descriptions longer than 8 characters per item

---

## Sub-Group D7: 資料透明度-低碳產品 (Fields 56-57)

### 欄位 56: 是否生產支持轉型至低碳經濟之產品/服務
- **Data Format:** boolean
- **Unit:** NA
- **Description:** 公司是否說明有生產或進行低碳經濟相關的產品或服務內容，如依特定標準或指引（EU Taxonomy, 永續經濟活動認定參考指引等）定義低碳產品。
- **Note:** Simply selling solar panels or EVs does not auto-qualify; the company needs to explicitly identify and describe such products in the report.

### 欄位 57: 支持轉型至低碳經濟之產品/服務產生的營收或營收占比
- **Data Format:** decimal
- **Unit:** 元
- **Precision:** 0.0001
- **Description:** 揭露公司2024年「支持轉型至低碳經濟之產品/服務」之收入佔總營收之比例，或絕對營收金額。公司須說明該低碳產品與服務之定義。
- **Note:** If the report gives a percentage, fill the decimal (e.g., 0.35 for 35%). If it gives an absolute revenue figure in 元, fill that. Note which in 補充說明.

---

## Sub-Group D8: 勞動 (Fields 58-65)

### 欄位 58: 失能傷害頻率(LTIFR)
- **Data Format:** decimal
- **Unit:** NA
- **Precision:** 0.0001
- **Description:** 報告年度的失能傷害頻率（Lost Time Injury Frequency Rate）。計算公式：(失能傷害件數 × 1,000,000) / 總工時。請提供整體數值；若只有男/女分開，在補充說明中列出並填整體值。
- **Common location:** GRI 403-9 appendix

### 欄位 59: 職業傷害件數
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度發生的職業傷害總件數。**固定格式**：「死亡X件、永久失能X件、暫時失能X件」。若報告書有依性別分類，請一併列出。
- **Example output:** `死亡0件、永久失能0件、暫時失能12件`

### 欄位 60: 損失工作日數
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度因職業傷害造成的損失工作日數（Lost Days）。此數值通常出現在職業安全統計表格中。若只有一個數值，直接填入；若分男/女，列出格式「男X日、女X日」。
- **Example output:** `248` or `男198日、女50日`
- **搜尋清單:** ① GRI 403-9 表格中「損失天數」「損失日數」欄位 ② 職業安全統計表 ③ ESG 績效數據附錄中的安全指標表。注意：此欄位要的是**絕對損失天數**，不是嚴重度（Severity Rate）。

### 欄位 61: 重大職業安全意外事件
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度是否有發生重大職業安全意外事件？重大事件包含：造成死亡、永久失能、多人受傷之事故，以及火災、爆炸等工安事故。若有發生，請填入傷亡人數與說明文字；若無請填「無」。
- **Example output:** `死亡1人，因高空墜落意外` or `無`

### 欄位 62: 勞動法規違規與裁罰
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度是否有違反勞動相關法規之情事（職業安全衛生法、勞動基準法、性別工作平等法等）？若有請列出違規法條、違規內容與裁罰金額。若公司明確表示無違規事件，填 `0`。若報告書未提及，留空。
- **搜尋清單（務必逐一檢查）:** ① GRI 2-27 揭露 ② 法規遵循/合規章節 ③ 合規事件表/重大裁罰表 ④ SASB 附錄 ⑤ 職業安全衛生章節。**注意：此欄位通常不在環境章節。**
- **Example output:** `違反職業安全衛生法第6條，罰款新台幣10萬元` or `0`

### 欄位 63: 政府補貼或獎勵
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度是否接受政府補貼或獎勵計劃？若有，請說明計劃名稱與補貼金額。若未揭露，留空。
- **搜尋清單（務必逐一檢查）:** ① GRI 201-4 揭露 ② 治理章節「取自政府之財務援助」表格 ③ 財務報表附註（IAS 20 政府補助） ④ SASB 附錄 ⑤ 公司治理章節。**注意：此欄位通常不在環境章節，而在治理或財務章節。**
- **Example output:** `經濟部能源局節能補助計劃，補助金額新台幣300萬元`

### 欄位 64: 受傷、死亡比率
- **Data Format:** string
- **Unit:** NA
- **Description:** 報告年度的職業傷害率(IR)與死亡率(FR)。傷害率計算公式：(傷害件數 × 200,000) / 總工時。死亡率計算公式：(死亡人數 × 200,000) / 總工時。**固定格式**：「傷害率X.X、死亡率X」。若報告書未揭露請留空。
- **Example output:** `傷害率0.52、死亡率0`

### 欄位 65: 職業病
- **Data Format:** string
- **Unit:** NA
- **Description:** 該公司當年度是否發生職業病？若有，請填入人數與說明文字（如：「3人，塵肺症」）。職業病包含職業性癌症、呼吸系統疾病、皮膚病、聽力損失等。若無請填「無」。
- **Example output:** `無` or `2人，噪音性聽力損失`

---

## Sub-Group D9: 水資源 (Fields 66-72)

Water data appears under GRI 303-3 (withdrawal), GRI 303-4 (discharge), GRI 303-5 (consumption). Check the GRI index first.

All water fields use unit **噸 (公噸)**. Common conversions:
- 1 立方公尺 (m³) = 1 公噸 (water density ≈ 1 kg/L)
- 1 百萬公升 (ML) = 1,000 公噸
- 1 千公升 (kL) = 1 公噸
- 「度」(in water context) = 1 立方公尺 = 1 公噸

### 欄位 66: 取水量-自來水
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司用水量中，取自自來水廠的水（自來水、水庫水等第三方供水）。若公司僅寫總用水量而未分來源，請留空。

### 欄位 67: 取水量-地表水
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司用水量中，取自自然河川的水（溪流、攔河堰等地表水體）。若公司僅寫總用水量，請留空。

### 欄位 68: 取水量-地下水
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司用水量中，取自地下水的水。若公司僅寫總用水量，請留空。

### 欄位 69: 取水量-其他來源（海水、冷凝水、雨水、再生水）
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司用水量中，取自其他來源的水（海水淡化、雨水收集、再生水等）。若公司僅寫總用水量，請留空。若有多種其他來源，加總後填入並在補充說明說明各來源。

### 欄位 70: 回收水量
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司在生產過程中回收的水資源。注意：回收水量有時會高於取水量，因為一滴水可被重複利用多次（循環用水）。

### 欄位 71: 排放水量
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 公司最後排放掉的廢污水（廢水、排放水、放流水）。排水量通常小於取水量，差額約為耗水量。

### 欄位 72: 耗用水量
- **Data Format:** decimal
- **Unit:** 噸
- **Precision:** 0.0001
- **Description:** 生產過程中消耗掉，沒有回到自然界的水。**若報告書有明確揭露耗用水量請填入，若無明確資料請留空，無須協助公司計算。**
- **Note:** This field is strictly as-reported. Do not calculate it as (field 66+67+68+69) - field 71.

---

## Extraction Rules (for this group)

### Energy unit conversions (fields 34-36)
The field unit is MJ. Apply these conversions if the report uses other units:
- GJ → MJ: multiply by 1,000
- TJ → MJ: multiply by 1,000,000
- kWh → MJ: multiply by 3.6
- MWh → MJ: multiply by 3,600
- GWh → MJ: multiply by 3,600,000

Always note the original unit and conversion in 補充說明.

### Electricity unit conversions (field 42)
The field unit is 度（KWh）. Apply these conversions:
- 千度 (kKWh) → KWh: multiply by 1,000
- MWh → KWh: multiply by 1,000
- GWh → KWh: multiply by 1,000,000
- GJ → KWh: multiply by 277.778

### Energy item format (field 38)
Strict format requirement: `能源: 數值 單位; ` (colon then space, semicolon then space)

The reported unit must be preserved exactly as it appears in the report:
- If the report says「電力: 206,234 千度」→ write `電力: 206234 千度; ` (remove thousand separator)
- If the report says「天然氣: 25.3 百萬立方公尺」→ write `天然氣: 25.3 百萬立方公尺; `
- Do NOT convert these to a common unit — keep original units per item

### Boolean judgment for energy fields
- Field 46 (政府用電大戶): True if the report explicitly states the company has met the obligation. False if the report explicitly states the company has not met it. Blank if the report only describes the regulation without stating compliance. Merely describing the 用電大戶條款 content is NOT evidence of meeting the obligation.
- Field 47 (RE100): True if the company is a confirmed RE100 member. False if the report discusses RE100 in a scenario/hypothetical context but the company is clearly not a member. Blank if RE100 is not mentioned at all.

### 認證/倡議布林值例外規則 (Certification Boolean Exceptions)

以下欄位若報告書**完全未提及**，應填 `False`（非留空），因為已達成者必會揭露：

| 欄位 | 邏輯 |
|------|------|
| F32 (範疇三減量目標) | 已設定者必會揭露 → 未提及 = 未設定 = `False` |
| F47 (RE100) | 已加入者必會揭露 → 未提及 = 未加入 = `False` |
| F48 (再生能源使用目標) | 已設定者必會揭露 → 未提及 = 未設定 = `False` |

注意：F51（節能目標）不適用此規則，因公司可能有節能目標但未在報告書中明確揭露。

### Numeric format for all fields
- No thousand separators
- Percentages as decimals
- Leave blank when absent (do not write 0, 無, NA for data fields)

### 補充說明 for labor fields
Always note:
- Whether data covers employees only or includes contractors
- Whether LTIFR uses 1,000,000 or 200,000 work-hour base
- Source section (GRI 403-9, safety appendix table, etc.)

### Water: what to do when only total is given
- If the report only gives total withdrawal without source breakdown, leave fields 66-69 blank
- Note in 補充說明 that total withdrawal is disclosed but source breakdown is not

---

## Output Format

```
---欄位N開始---
欄位數值: [value or empty]
欄位單位: [unit or NA]
補充說明: [source, conversion, caveats — max 200 chars]
參考頁數: [p.X or NA]
---欄位N結束---
```

Example for energy fields:

```
---欄位34開始---
欄位數值: 8234567000.0000
欄位單位: MJ
補充說明: 報告書原始數值8234567 GJ，乘以1000換算為MJ，來自GRI 302-1附錄，含電力及燃料
參考頁數: p.112
---欄位34結束---

---欄位38開始---
欄位數值: 電力: 206234 千度; 天然氣: 25283 千立方公尺; 柴油: 634 公秉; 液化石油氣: 120 公噸;
欄位單位: 依報告書原始格式
補充說明: 各項能源數值來自GRI 302-1能源使用細項表，單位保留原始格式
參考頁數: p.113
---欄位38結束---
```

Example for labor fields:

```
---欄位58開始---
欄位數值: 0.47
欄位單位: NA
補充說明: 失能傷害頻率LTIFR，計算基礎百萬工時，涵蓋正職員工及外包人員，來自GRI 403-9
參考頁數: p.134
---欄位58結束---

---欄位59開始---
欄位數值: 死亡0件、永久失能0件、暫時失能8件
欄位單位: NA
補充說明: 職業傷害件數，來自職業安全統計表，包含正職員工及承攬商
參考頁數: p.134
---欄位59結束---
```

Example for water fields:

```
---欄位66開始---
欄位數值: 1250000.0000
欄位單位: 噸
補充說明: 自來水取水量，原始數據1250000 m³，1 m³=1噸換算，來自GRI 303-3
參考頁數: p.148
---欄位66結束---

---欄位72開始---
欄位數值:
欄位單位: 噸
補充說明: 報告書未揭露耗用水量，僅有取水量與排放水量，不自行計算
參考頁數: NA
---欄位72結束---
```

---

## Common Pitfalls

### Energy pitfalls
1. **GJ vs. MJ confusion**: field 34-36 require MJ. If the report shows 8,234 GJ, fill `8234000` MJ — do not fill `8234`.
2. **Excluding electricity from total energy**: the total energy in fields 34-36 should include electricity (converted to heat equivalent). Do not subtract it.
3. **Energy breakdown units mixed**: field 38 preserves original per-item units. Do not force everything into GJ.
4. **Planned renewable capacity counted**: field 44 only counts capacity already built and operational. Exclude anything labeled 「規劃」「施工中」「預計完工」.

### Renewable energy pitfalls
5. **RE100 vs. government obligation**: field 46 is the government's 用電大戶 10% obligation (mandatory). Field 47 is RE100 (voluntary). These are completely different and should not be confused.
6. **RE percentage vs. capacity**: field 43 is a percentage of total electricity; field 44 is an installed capacity in KW. Do not fill one into the other.

### Climate action pitfalls
7. **Aspirational vs. target**: field 51 (節能目標) requires a specific numeric target or year. Phrases like 「持續推動節能措施」without a figure do not qualify.
8. **Strategies field format**: field 55 requires 4-8 character noun phrases separated by 、. A complete sentence like 「推動製程優化以降低能源消耗」should be compressed to 「製程優化」.

### Labor pitfalls
9. **LTIFR base rate confusion**: some companies calculate LTIFR using 200,000 hours (US OSHA standard) instead of 1,000,000 hours. Note which base the company used in 補充說明.
10. **Contractor vs. employee data**: GRI 403 may report injury data separately for employees and contractors. Fill the combined figure in field 58; note coverage in 補充說明.
11. **Lost Days vs. Lost Day Rate**: field 60 is an absolute count of lost days, not a rate. Do not fill in a rate.

### Water pitfalls
12. **Recycled water double-counting**: field 70 (回收水量) may appear larger than total intake (fields 66-69) because recycled water is counted each time it circulates. This is expected — do not flag it as an error.
13. **Do not calculate 耗用水量**: field 72 must only be filled if the report explicitly discloses the consumption figure. Never calculate it as (withdrawal - discharge).
14. **Unit confusion in water tables**: Taiwanese reports sometimes mix 公噸, m³, and 千公升 in the same table. Verify each row's unit header before converting.
15. **Tap water vs. river water distinction**: 自來水 (field 66) is water supplied by a utility company; 地表水 (field 67) is water drawn directly from rivers or reservoirs by the company. Make sure to distinguish them correctly.
