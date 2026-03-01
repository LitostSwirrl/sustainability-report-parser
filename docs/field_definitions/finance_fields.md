# 金融業欄位 (Finance Fields) — 欄位 101-104 + 401-432

> Source: `src/field_definitions.py` → `FINANCE_FIELDS_V2` (欄位 101-104) + `FINANCE_EXTENDED_FIELDS` (欄位 401-432)
> Applicable to: Financial sector companies (銀行、保險、證券、金控、期貨商). In V2 (2026 驗證指標), these fields are appended after the 72 base fields. The extended fields (401-432) cover PCAF financed emissions, climate scenario analysis, sustainable finance products, and WBA Financial System Benchmark indicators.

---

## 基礎金融欄位 (FINANCE_FIELDS_V2) — 欄位 101-104

### 欄位 101: 綠色/永續放款餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融 |

**Description:** 請註明是綠色放款、永續連結貸款或符合指引之放款總額。

---

### 欄位 102: 永續經濟活動放款佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續金融 |

**Description:** 分子為符合永續指引之放款，分母為總放款，若無明確佔比請留空。

---

### 欄位 103: 綠色/永續投資餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融 |

**Description:** 包含綠色債券、永續債券或投資電廠等金額。

---

### 欄位 104: 適用赤道原則專案融資件數/金額

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 件/元 |
| Precision | NA |
| Category | 永續金融 |

**Description:** 請同時列出件數與金額，如：5件 / 20億元。

---

## 金融業延伸欄位 (FINANCE_EXTENDED_FIELDS) — 欄位 401-432

> 依據：永續金融評鑑、WBA Financial System Benchmark、PCAF Standard

### 欄位 401: 投融資組合碳排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.01 |
| Category | 投融資碳排放 |

**Description:** 依據PCAF標準計算的投融資組合碳排放量（Scope 3 Category 15）。包含企業貸款、專案融資、投資等資產類別的financed emissions。通常可於TCFD報告或永續報告書的氣候風險章節找到。

---

### 欄位 402: 投融資碳排放揭露範圍

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |

**Description:** 列出已揭露financed emissions的資產類別。格式：「資產類別1; 資產類別2;」。常見類別：企業貸款(Corporate loans)、專案融資(Project finance)、商業不動產(Commercial real estate)、房貸(Mortgages)、上市股票(Listed equity)、公司債(Corporate bonds)。

---

### 欄位 403: 投融資碳排放基準年

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |

**Description:** 投融資組合碳排放減量目標的基準年份。若未設定減量目標或未揭露基準年，請留空。

---

### 欄位 404: 投融資碳排放減量目標

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |

**Description:** 投融資組合的碳排放減量目標說明（限50字）。格式範例：「2030年投融資碳排放較2021年降低50%」。若無目標請留空。

---

### 欄位 405: 是否執行氣候情境分析

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |

**Description:** 金融機構是否針對投融資組合執行氣候情境分析（Climate Scenario Analysis）？常見情境包含：IEA NZE、NGFS情境、RCP情境等。填答只有 True/False 兩種可能性。

---

### 欄位 406: 氣候情境分析範圍說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |

**Description:** 氣候情境分析的涵蓋範圍說明（限100字）。包含：使用的情境（如NGFS、IEA NZE）、分析的資產類別、時間範圍等。若欄位405為False，請留空。

---

### 欄位 407: 永續連結貸款餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |

**Description:** 永續連結貸款（Sustainability-Linked Loans, SLL）的餘額，即貸款利率與借款人ESG績效掛鉤的貸款。單位為新台幣元。

---

### 欄位 408: 永續連結貸款佔總放款比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 永續金融商品 |

**Description:** 永續連結貸款餘額佔總放款餘額的比例。以小數表示，例如5%請填0.05。

---

### 欄位 409: ESG主題基金資產規模

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |

**Description:** 管理的ESG主題基金或永續投資基金的總資產規模。單位為新台幣元。適用於投信業或有基金管理業務的金融機構。

---

### 欄位 410: 是否訂定化石燃料融資政策

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 金融機構是否訂定針對化石燃料（煤炭、石油、天然氣）產業的融資限制或退出政策？填答只有 True/False 兩種可能性。

---

### 欄位 411: 化石燃料融資政策說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 化石燃料融資政策的具體內容（限100字）。包含：限制的產業類別、退出時程、例外條款等。若欄位410為False，請留空。

---

### 欄位 412: 是否簽署國際永續金融倡議

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續承諾 |

**Description:** 是否簽署國際永續金融倡議？常見倡議包含：PRB(責任銀行原則)、PRI(責任投資原則)、PSI(永續保險原則)、NZBA(淨零銀行聯盟)、NZAMI(淨零資產管理倡議)等。

---

### 欄位 413: 簽署的永續金融倡議

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 永續承諾 |

**Description:** 列出已簽署的國際永續金融倡議。格式：「倡議1、倡議2、倡議3」。常見倡議：PRB、PRI、PSI、NZBA、NZAMI、PCAF、赤道原則。若欄位412為False，請留空。

---

### 欄位 414: 是否採用雙重重大性概念

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 報告品質 |

**Description:** 永續報告書是否納入雙重重大性（Double Materiality）概念？雙重重大性同時考量企業對環境社會的影響（impact materiality）與ESG議題對企業財務的影響（financial materiality）。

---

### 欄位 415: 金融包容性措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 金融包容 |

**Description:** 針對弱勢族群或偏鄉地區提供的金融包容性措施說明（限100字）。例如：原住民族金融服務、偏鄉ATM佈建、微型保險、小額貸款等。

---

### 欄位 416: 防漂綠措施說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 報告品質 |

**Description:** 參考金管會「金融機構防漂綠參考指引」訂定的防漂綠措施說明（限100字）。包含：永續金融商品審查機制、ESG資訊驗證程序、行銷宣傳規範等。

---

### 欄位 417: 客戶ESG議合件數

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | 件 |
| Precision | NA |
| Category | 客戶議合 |

**Description:** 報告年度與客戶進行ESG議合（Engagement）的件數。議合包含：引導客戶設定減碳目標、提供永續轉型諮詢、要求改善ESG績效等。

---

### 欄位 418: 是否參與永續金融評鑑

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 外部評鑑 |

**Description:** 是否參與金管會主辦的永續金融評鑑？填答只有 True/False 兩種可能性。

---

### 欄位 419: 永續金融評鑑排名

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 外部評鑑 |

**Description:** 最近一屆永續金融評鑑的排名結果。填寫格式：「前25%」「26%-50%」「51%-75%」「76%-100%」。若未參與或未公布請留空。

---

### 欄位 420: PCAF數據品質分數

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.1 |
| Category | 投融資碳排放 |

**Description:** 投融資碳排放計算所使用的PCAF數據品質分數（Data Quality Score）。分數範圍1-5，1為最高品質（使用客戶實際排放數據），5為最低品質（使用產業平均估算）。

---

### 欄位 421: UN永續原則第三方確信

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 外部確信 |

**Description:** 是否針對簽署的UN永續原則（PRB/PRI/PSI）執行情形取得第三方確信（Assurance）？填答只有 True/False 兩種可能性。若未簽署任何UN永續原則請留空。

---

### 欄位 422: 永續金融人才認證比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 人才發展 |

**Description:** 取得永續金融相關證照（如：永續金融基礎能力測驗、ESG投資分析師等）的員工人數佔總員工人數的比例。以小數表示，例如5%請填0.05。若未揭露請留空。

---

### 欄位 423: 氣候實體風險揭露

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |

**Description:** 是否揭露氣候實體風險（颱風、洪水、乾旱、海平面上升等）對投融資組合的影響評估？請簡述評估範圍與主要風險類型（限100字）。若未評估請填「無」。

---

### 欄位 424: 高碳產業放款佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 氣候行動 |

**Description:** 對高碳排產業（煤炭開採、石油天然氣、火力發電等）的放款餘額佔總放款餘額的比例。以小數表示，例如10%請填0.10。高碳產業定義依報告書揭露為準。

---

### 欄位 425: 高碳產業放款減量目標

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 是否設定高碳排產業放款減量或退出目標？請說明目標年份與減量目標（限50字）。例如：「2030年前煤炭融資歸零」。若無目標請填「無」。

---

### 欄位 426: 永續經濟活動放款類別

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 永續金融商品 |

**Description:** 列出符合《永續經濟活動認定參考指引》的主要放款類別。格式：「類別1; 類別2;」。常見類別：再生能源專案融資、綠建築貸款、電動車貸款、循環經濟產業等。若無相關放款請留空。

---

### 欄位 427: 綠色債券承銷金額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |

**Description:** 報告年度承銷或發行的綠色債券、永續債券、社會債券總金額。單位為新台幣元。若為證券業請填承銷金額，若為銀行業可填發行金額。

---

### 欄位 428: 責任投資策略說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 責任投資 |

**Description:** 採用的責任投資策略類型。格式：「策略1、策略2」。常見策略：ESG整合（ESG Integration）、負面排除（Exclusion）、正向篩選（Best-in-class）、主題投資、議合與投票（Engagement）、影響力投資。

---

### 欄位 429: 生物多樣性風險評估

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 自然相關風險 |

**Description:** 是否評估投融資組合對生物多樣性的影響或依賴風險？參考框架可能包含TNFD、SBTN、ENCORE等。填答只有 True/False 兩種可能性。若報告書未提及生物多樣性風險請留空。

---

### 欄位 430: 微型/小型企業放款比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 金融包容 |

**Description:** 對微型企業及小型企業（依中小企業認定標準）的放款餘額佔總放款餘額的比例。以小數表示，例如15%請填0.15。此指標反映金融包容性。

---

### 欄位 431: 氣候轉型風險評估

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |

**Description:** 是否針對投融資組合執行氣候轉型風險評估（政策、技術、市場、聲譽風險）？請簡述評估範圍與方法（限100字）。若未評估請填「無」。

---

### 欄位 432: 永續績效連結薪酬

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 薪酬治理 |

**Description:** 高階主管薪酬是否與永續/ESG績效指標連結？若有，請說明連結的指標類型（如：碳排放減量、ESG評鑑排名、永續金融業務目標等）。若無連結請填「無」。
