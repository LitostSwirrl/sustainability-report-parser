# Group I: 金融業專屬欄位 (Finance Industry Fields)

**Fields:** FINANCE_FIELDS_V2 (欄位 101-104) + FINANCE_EXTENDED_FIELDS (欄位 401-432)
**Applicable to:** Financial sector companies only — banks (銀行), insurance (保險), securities (證券), holding companies (金控), futures dealers (期貨商)
**Source:** `src/field_definitions.py` → `FINANCE_FIELDS_V2`, `FINANCE_EXTENDED_FIELDS`
**Total additional fields:** 36 (4 basic + 32 extended)

These fields are appended after the base fields (1-72) for all financial sector companies. They cover sustainable finance products, financed emissions (PCAF), climate scenario analysis, sustainable finance initiative memberships, and regulatory evaluation participation.

---

## Finance-Specific Search Guidance

### Primary Document Locations

1. **TCFD Report (氣候相關財務揭露報告)**: Climate scenario analysis, financed emission disclosures, transition risk assessments, physical risk evaluations
2. **Sustainability Report Appendix (永續報告書附錄)**: Sustainable finance product statistics, ESG investment data, loan portfolio analysis, sustainable finance KPI tables
3. **Risk Management Chapter (風險管理章節)**: Climate risk management framework, financed emission inventory methodology
4. **Board and Governance Chapter**: ESG committee disclosures, sustainability-linked executive compensation

### International Sustainability Finance Initiative Abbreviations

| Abbreviation | Full Name | Description |
|-------------|-----------|-------------|
| PRB | Principles for Responsible Banking | 責任銀行原則 (UNEP FI) |
| PRI | Principles for Responsible Investment | 責任投資原則 |
| PSI | Principles for Sustainable Insurance | 永續保險原則 (UNEP FI) |
| NZBA | Net-Zero Banking Alliance | 淨零銀行聯盟 |
| NZAMI | Net-Zero Asset Managers Initiative | 淨零資產管理倡議 |
| PCAF | Partnership for Carbon Accounting Financials | 金融業碳核算夥伴關係 |
| 赤道原則 | Equator Principles | 專案融資環境社會風險評估框架 |
| TCFD | Task Force on Climate-related Financial Disclosures | 氣候相關財務揭露工作小組 |
| TNFD | Taskforce on Nature-related Financial Disclosures | 自然相關財務揭露工作小組 |
| SBTN | Science Based Targets for Nature | 自然科學基礎目標網絡 |
| NGFS | Network for Greening the Financial System | 央行與監管機構綠化金融網絡 |

### PCAF Data Quality Scores (數據品質分數)

PCAF scores range from 1 (best) to 5 (worst) based on the data source used to calculate financed emissions:

| Score | Data Source | Quality Level |
|-------|-------------|---------------|
| 1 | Client-reported and verified GHG data | 最高品質：使用客戶經查證的排放數據 |
| 2 | Client-reported but unverified GHG data | 使用客戶未經查證的排放數據 |
| 3 | Industry average intensity × actual production data | 使用產業平均排放強度 × 實際生產數據 |
| 4 | Industry average intensity × revenue data | 使用產業平均排放強度 × 營收數據 |
| 5 | Industry average intensity × total assets | 最低品質：使用產業平均排放強度 × 資產數據 |

A single institution may report different scores for different asset classes. Look for "PCAF data quality score", "數據品質分數", or a scoring table in the financed emissions methodology section.

### Sustainable Finance Product Categories (永續金融商品分類)

| Product | Chinese | Description |
|---------|---------|-------------|
| Sustainability-Linked Loans (SLL) | 永續連結貸款 | Interest rate tied to borrower's ESG KPIs |
| Green Loans | 綠色貸款 | Proceeds restricted to green projects |
| Green Bonds | 綠色債券 | Debt proceeds restricted to environmental projects |
| Social Bonds | 社會債券 | Debt proceeds for social impact projects |
| Sustainability Bonds | 永續發展債券 | Combined green + social use of proceeds |
| Sustainability-Linked Bonds (SLB) | 永續發展連結債券 | Coupon linked to ESG targets |
| ESG Funds | ESG主題基金 | Investment products integrating ESG factors |
| Responsible Investment | 責任投資 | Portfolio management using ESG criteria |

---

## FINANCE_FIELDS_V2 (欄位 101-104)

### 欄位 101: 綠色/永續放款餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融 |
| Aspect | 金融 |

**Description:** 請註明是綠色放款、永續連結貸款或符合指引之放款總額。

**Extraction rules:**
- Keywords: "綠色放款餘額", "永續放款", "永續連結貸款餘額", "Green Loan", "Sustainable Finance Outstanding"
- Record the year-end outstanding balance (期末餘額), not origination volume
- Include: green loans (綠色貸款), sustainability-linked loans (永續連結貸款), sustainable project finance
- Exclude: conventional loans that happen to be to green industries — only count if explicitly classified under a green/sustainable label
- Unit: NTD (新台幣元); if reported in 億元, multiply by 100,000,000

**Common pitfalls:**
- Distinguish between "committed" (承諾) and "outstanding" (餘額) amounts — use outstanding
- Some institutions report "cumulative issuance" (累計發行) vs. "outstanding balance" — use outstanding

---

### 欄位 102: 永續經濟活動放款佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比(%) |
| Precision | 0.01 |
| Category | 永續金融 |
| Aspect | 金融 |

**Description:** 分子為符合永續指引之放款，分母為總放款，若無明確佔比請留空。

**Extraction rules:**
- Numerator: 欄位 101 (qualifying sustainable loans)
- Denominator: total loan portfolio (總放款餘額)
- If both numerator and denominator are disclosed but ratio is not stated, compute: 101 / total loans
- Format: decimal (e.g., 3.5% → 0.035)

---

### 欄位 103: 綠色/永續投資餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融 |
| Aspect | 金融 |

**Description:** 包含綠色債券、永續債券或投資電廠等金額。

**Extraction rules:**
- Keywords: "綠色債券投資", "永續債券持有", "ESG投資", "再生能源投資", "Green Bond Portfolio"
- Include: green bonds, sustainability bonds, direct investments in renewable energy projects
- This is the institution's own investment portfolio, not loans extended to clients
- Record as outstanding balance, not annual new purchases

---

### 欄位 104: 適用赤道原則專案融資件數/金額

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 件/元 |
| Precision | NA |
| Category | 永續金融 |
| Aspect | 金融 |

**Description:** 請同時列出件數與金額，如：「5件 / 20億元」。

**Extraction rules:**
- Keywords: "赤道原則", "Equator Principles", "EP", "專案融資", "Project Finance"
- Format: "[件數]件 / [金額]" (e.g., "3件 / 15億元")
- If only one of the two is available, record what is available and note the other is undisclosed
- Equator Principles apply to project finance above USD 10 million with significant environmental/social risks

---

## FINANCE_EXTENDED_FIELDS (欄位 401-432)

### 欄位 401: 投融資組合碳排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.01 |
| Category | 投融資碳排放 |
| Aspect | 金融 |

**Description:** 依據PCAF標準計算的投融資組合碳排放量 (Scope 3 Category 15)。包含企業貸款、專案融資、投資等資產類別的 financed emissions。通常可於TCFD報告或永續報告書的氣候風險章節找到。

**Extraction rules:**
- Keywords: "投融資組合碳排放", "Financed Emissions", "PCAF", "Scope 3 類別15", "Category 15"
- This is the aggregate of all asset-class financed emissions
- If only partial coverage is disclosed (e.g., corporate loans only), record the disclosed figure and note the coverage in 補充說明
- Some institutions express this as "weighted average carbon intensity (WACI)" rather than absolute emissions — record the absolute figure; note WACI separately in 補充說明
- Check the base fields: this value should match or be consistent with base field V2-30 (Scope 3 Category 15)

---

### 欄位 402: 投融資碳排放揭露範圍

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |
| Aspect | 金融 |

**Description:** 列出已揭露 financed emissions 的資產類別。格式：「資產類別1; 資產類別2;」。常見類別：企業貸款 (Corporate loans)、專案融資 (Project finance)、商業不動產 (Commercial real estate)、房貸 (Mortgages)、上市股票 (Listed equity)、公司債 (Corporate bonds)。

**Extraction rules:**
- List all PCAF asset classes for which emissions have been calculated
- PCAF defines 7 asset classes: listed equity & corporate bonds (上市股票和公司債), business loans & unlisted equity (企業貸款和非上市股票), project finance (專案融資), commercial real estate (商業不動產), mortgages (房屋貸款), motor vehicle loans (車貸), sovereign bonds (主權債)
- Record only the ones the institution has actually calculated and disclosed

---

### 欄位 403: 投融資碳排放基準年

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |
| Aspect | 金融 |

**Description:** 投融資組合碳排放減量目標的基準年份。若未設定減量目標或未揭露基準年，請留空。

---

### 欄位 404: 投融資碳排放減量目標

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 投融資碳排放 |
| Aspect | 金融 |

**Description:** 投融資組合的碳排放減量目標說明（限50字）。格式範例：「2030年投融資碳排放較2021年降低50%」。若無目標請留空。

**Extraction rules:**
- This refers specifically to financed emissions reduction targets, not the institution's own operational emissions target
- NZBA members are required to set such targets; check for NZBA commitment disclosures
- Include: target year, reduction percentage, base year, and scope of coverage (which asset classes)

---

### 欄位 405: 是否執行氣候情境分析

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |
| Aspect | 金融 |

**Description:** 金融機構是否針對投融資組合執行氣候情境分析 (Climate Scenario Analysis)？常見情境包含：IEA NZE、NGFS情境、RCP情境等。填答只有 True/False 兩種可能性。

**Extraction rules:**
- True if: any quantitative scenario analysis was conducted on the loan or investment portfolio
- False if: only qualitative descriptions of climate risk are provided without scenario modeling
- Keywords: "氣候情境分析", "Scenario Analysis", "NGFS", "IEA NZE", "1.5°C scenario", "2°C scenario", "RCP 2.6"
- Primarily in: TCFD report, Risk Management chapter

---

### 欄位 406: 氣候情境分析範圍說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |
| Aspect | 金融 |

**Description:** 氣候情境分析的涵蓋範圍說明（限100字）。包含：使用的情境（如NGFS、IEA NZE）、分析的資產類別、時間範圍等。若欄位405為False，請留空。

---

### 欄位 407: 永續連結貸款餘額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |
| Aspect | 金融 |

**Description:** 永續連結貸款 (Sustainability-Linked Loans, SLL) 的餘額，即貸款利率與借款人ESG績效掛鉤的貸款。單位為新台幣元。

**Extraction rules:**
- SLL must have explicit KPI targets linked to the interest rate (e.g., borrower must reduce GHG by X% or rate steps up)
- Distinguish from "green loans" (use of proceeds restricted) vs. "SLL" (rate linked to KPIs)
- Some reports present a combined "green + SLL" figure — extract the SLL component if separately stated

---

### 欄位 408: 永續連結貸款佔總放款比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 永續金融商品 |
| Aspect | 金融 |

**Description:** 永續連結貸款餘額佔總放款餘額的比例。以小數表示，例如5%請填0.05。

---

### 欄位 409: ESG主題基金資產規模

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |
| Aspect | 金融 |

**Description:** 管理的ESG主題基金或永續投資基金的總資產規模。單位為新台幣元。適用於投信業或有基金管理業務的金融機構。

**Extraction rules:**
- Keywords: "ESG基金", "永續基金", "ESG投資", "責任投資規模"
- Record assets under management (AUM), not annual subscription volume
- If only foreign currency amounts are given, convert to NTD using the year-end exchange rate and note in 補充說明

---

### 欄位 410: 是否訂定化石燃料融資政策

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |
| Aspect | 金融 |

**Description:** 金融機構是否訂定針對化石燃料（煤炭、石油、天然氣）產業的融資限制或退出政策？

**Extraction rules:**
- True if: a formal, written policy document restricts or phases out lending to coal, oil, or gas sectors
- False if: no formal policy exists, only general ESG consideration statements
- Look in: "敏感產業融資政策", "化石燃料政策", "煤炭退出政策", "Coal Financing Policy"

---

### 欄位 411: 化石燃料融資政策說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |
| Aspect | 金融 |

**Description:** 化石燃料融資政策的具體內容（限100字）。包含：限制的產業類別、退出時程、例外條款等。若欄位410為False，請留空。

---

### 欄位 412: 是否簽署國際永續金融倡議

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續承諾 |
| Aspect | 金融 |

**Description:** 是否簽署國際永續金融倡議？常見倡議包含：PRB、PRI、PSI、NZBA、NZAMI等。

---

### 欄位 413: 簽署的永續金融倡議

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 永續承諾 |
| Aspect | 金融 |

**Description:** 列出已簽署的國際永續金融倡議。格式：「倡議1、倡議2、倡議3」。若欄位412為False，請留空。

**Extraction rules:**
- Common initiatives: PRB, PRI, PSI, NZBA, NZAMI, PCAF, 赤道原則 (Equator Principles)
- Look in: "倡議承諾", "永續倡議", "簽署宣言", sustainability commitments section
- Use the standard abbreviations listed in the Search Guidance section above

---

### 欄位 414: 是否採用雙重重大性概念

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 報告品質 |
| Aspect | 金融 |

**Description:** 永續報告書是否納入雙重重大性 (Double Materiality) 概念？雙重重大性同時考量企業對環境社會的影響 (impact materiality) 與ESG議題對企業財務的影響 (financial materiality)。

**Extraction rules:**
- True if: the materiality assessment section explicitly mentions "雙重重大性" or "Double Materiality" as a methodology
- EU CSRD / ESRS adopters typically use double materiality — look for ESRS references
- GRI-only reporters may use "impact materiality" — this does NOT automatically qualify as double materiality
- False if only financial materiality (TCFD/SASB approach) is used

---

### 欄位 415: 金融包容性措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 金融包容 |
| Aspect | 社會 |

**Description:** 針對弱勢族群或偏鄉地區提供的金融包容性措施說明（限100字）。例如：原住民族金融服務、偏鄉ATM佈建、微型保險、小額貸款等。

---

### 欄位 416: 防漂綠措施說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 報告品質 |
| Aspect | 治理 |

**Description:** 參考金管會「金融機構防漂綠參考指引」訂定的防漂綠措施說明（限100字）。包含：永續金融商品審查機制、ESG資訊驗證程序、行銷宣傳規範等。

**Extraction rules:**
- Keywords: "防漂綠", "Anti-greenwashing", "永續金融商品審查", "ESG驗證", "綠色標籤審查"
- Taiwan's FSC published "金融機構防漂綠參考指引" (Anti-Greenwashing Guidelines) — look for explicit references
- Describe the mechanism, not just the policy intent

---

### 欄位 417: 客戶ESG議合件數

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | 件 |
| Precision | NA |
| Category | 客戶議合 |
| Aspect | 金融 |

**Description:** 報告年度與客戶進行ESG議合 (Engagement) 的件數。議合包含：引導客戶設定減碳目標、提供永續轉型諮詢、要求改善ESG績效等。

**Extraction rules:**
- Keywords: "客戶議合", "ESG議合件數", "永續轉型輔導件數", "Client Engagement"
- Count formal engagement activities, not general customer communications
- If both "engagement on ESG" and "shareholder engagement" are reported, use the loan/banking client engagement figure for banks; use shareholder engagement for asset managers

---

### 欄位 418: 是否參與永續金融評鑑

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 外部評鑑 |
| Aspect | 金融 |

**Description:** 是否參與金管會主辦的永續金融評鑑？

**Extraction rules:**
- The Taiwan FSC (金融監督管理委員會) conducts an annual 永續金融評鑑 (Sustainable Finance Evaluation)
- True if: the report mentions participating in or receiving a rating from this evaluation
- Keywords: "永續金融評鑑", "金管會評鑑", "FSC Sustainable Finance Evaluation"

---

### 欄位 419: 永續金融評鑑排名

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 外部評鑑 |
| Aspect | 金融 |

**Description:** 最近一屆永續金融評鑑的排名結果。填寫格式：「前25%」「26%-50%」「51%-75%」「76%-100%」。若未參與或未公布請留空。

**Extraction rules:**
- The FSC Sustainable Finance Evaluation ranks participants in quartiles
- Look for: "前25%", "傑出", "優良", or the percentile band described in the report
- If the exact quartile is not stated, note the description and leave the field blank if you cannot map it

---

### 欄位 420: PCAF數據品質分數

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.1 |
| Category | 投融資碳排放 |
| Aspect | 金融 |

**Description:** 投融資碳排放計算所使用的PCAF數據品質分數 (Data Quality Score)。分數範圍1-5，1為最高品質，5為最低品質。

**Extraction rules:**
- Many institutions report a weighted average score across asset classes
- If scores differ by asset class, record the weighted average; list individual scores in 補充說明
- Refer to the PCAF Data Quality Score table in the Search Guidance section above
- Look in: PCAF methodology section, financed emissions disclosure appendix

---

### 欄位 421: UN永續原則第三方確信

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 外部確信 |
| Aspect | 金融 |

**Description:** 是否針對簽署的UN永續原則（PRB/PRI/PSI）執行情形取得第三方確信 (Assurance)？若未簽署任何UN永續原則請留空。

**Extraction rules:**
- True if: an independent assurance provider has verified the institution's implementation of PRB, PRI, or PSI
- Look for assurance statements from Big 4 accounting firms or specialist ESG assurance providers
- Distinguish from: sustainability report assurance (報告書查驗) vs. specific UN Principle implementation assurance

---

### 欄位 422: 永續金融人才認證比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 人才發展 |
| Aspect | 金融 |

**Description:** 取得永續金融相關證照的員工人數佔總員工人數的比例。以小數表示，例如5%請填0.05。若未揭露請留空。

**Extraction rules:**
- Keywords: "永續金融認證", "ESG證照", "永續金融基礎能力測驗", "綠色金融人才"
- Taiwan's Securities Investment Trust and Consulting Association (SITCA) and others issue sustainable finance certificates
- Compute: certified employees / total employees; note the denominator used

---

### 欄位 423: 氣候實體風險揭露

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |
| Aspect | 金融 |

**Description:** 是否揭露氣候實體風險（颱風、洪水、乾旱、海平面上升等）對投融資組合的影響評估？請簡述評估範圍與主要風險類型（限100字）。若未評估請填「無」。

**Extraction rules:**
- Physical risks include: extreme weather events (颱風/洪水), chronic risks (乾旱/海平面上升/氣溫上升)
- Look in: TCFD report, risk management chapter, climate scenario analysis section
- If the institution has assessed physical risk to its loan collateral, real estate, or equity portfolio, describe the coverage and methodology

---

### 欄位 424: 高碳產業放款佔比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 氣候行動 |
| Aspect | 金融 |

**Description:** 對高碳排產業（煤炭開採、石油天然氣、火力發電等）的放款餘額佔總放款餘額的比例。以小數表示，例如10%請填0.10。高碳產業定義依報告書揭露為準。

**Extraction rules:**
- Keywords: "高碳產業放款", "碳密集產業", "化石燃料放款佔比", "Fossil Fuel Exposure"
- Definition of "high carbon" varies by institution — note their definition in 補充說明
- Common inclusions: coal mining (煤炭開採), oil & gas extraction (石油天然氣), thermal power generation (火力發電), petrochemicals (石化)

---

### 欄位 425: 高碳產業放款減量目標

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |
| Aspect | 金融 |

**Description:** 是否設定高碳排產業放款減量或退出目標？請說明目標年份與減量目標（限50字）。例如：「2030年前煤炭融資歸零」。若無目標請填「無」。

---

### 欄位 426: 永續經濟活動放款類別

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 永續金融商品 |
| Aspect | 金融 |

**Description:** 列出符合《永續經濟活動認定參考指引》的主要放款類別。格式：「類別1; 類別2;」。常見類別：再生能源專案融資、綠建築貸款、電動車貸款、循環經濟產業等。若無相關放款請留空。

**Extraction rules:**
- This specifically refers to lending aligned with Taiwan's "永續經濟活動認定參考指引" (Taiwan Taxonomy)
- Look for explicit taxonomy alignment disclosures
- Common qualifying categories: renewable energy project loans (再生能源專案), green building mortgages (綠建築), EV loans (電動車), waste-to-energy projects

---

### 欄位 427: 綠色債券承銷金額

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 1 |
| Category | 永續金融商品 |
| Aspect | 金融 |

**Description:** 報告年度承銷或發行的綠色債券、永續債券、社會債券總金額。單位為新台幣元。若為證券業請填承銷金額，若為銀行業可填發行金額。

**Extraction rules:**
- For securities firms (證券商): record underwriting volume (承銷金額)
- For banks issuing their own green bonds: record issuance amount
- Include all labeled bond types: green, social, sustainability, sustainability-linked
- Keywords: "綠色債券承銷", "永續債券發行", "標籤債券"

---

### 欄位 428: 責任投資策略說明

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 責任投資 |
| Aspect | 金融 |

**Description:** 採用的責任投資策略類型。格式：「策略1、策略2」。常見策略：ESG整合 (ESG Integration)、負面排除 (Exclusion)、正向篩選 (Best-in-class)、主題投資、議合與投票 (Engagement)、影響力投資。

**Extraction rules:**
- Only fill if the institution has an asset management or proprietary investment arm
- Record strategy names as used in the report; use the standard names above as reference
- If all 6 strategies are mentioned, list them all
- Look in: "責任投資", "ESG投資策略", investment policy sections

---

### 欄位 429: 生物多樣性風險評估

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 自然相關風險 |
| Aspect | 金融 |

**Description:** 是否評估投融資組合對生物多樣性的影響或依賴風險？參考框架可能包含TNFD、SBTN、ENCORE等。若報告書未提及生物多樣性風險請留空。

**Extraction rules:**
- True if: the institution has conducted formal assessment of biodiversity risk in its portfolio
- Frameworks to look for: TNFD (Taskforce on Nature-related Financial Disclosures), SBTN (Science Based Targets for Nature), ENCORE (Exploring Natural Capital Opportunities, Risks and Exposure)
- Keywords: "生物多樣性", "自然相關風險", "TNFD", "SBTN", "ENCORE"
- Leave blank (not False) if the report is entirely silent on biodiversity

---

### 欄位 430: 微型/小型企業放款比例

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 百分比 |
| Precision | 0.01 |
| Category | 金融包容 |
| Aspect | 金融 |

**Description:** 對微型企業及小型企業（依中小企業認定標準）的放款餘額佔總放款餘額的比例。以小數表示。

**Extraction rules:**
- Keywords: "中小企業放款佔比", "微型企業", "SME loan ratio", "小微企業"
- Taiwan's "中小企業認定標準" defines SME thresholds — note if the institution uses a different definition
- This reflects financial inclusion performance

---

### 欄位 431: 氣候轉型風險評估

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候風險 |
| Aspect | 金融 |

**Description:** 是否針對投融資組合執行氣候轉型風險評估（政策、技術、市場、聲譽風險）？請簡述評估範圍與方法（限100字）。若未評估請填「無」。

**Extraction rules:**
- Transition risks cover: policy/regulatory risk (政策法規), technology risk (技術), market risk (市場), reputational risk (聲譽)
- Distinct from physical risk (欄位 423) — this covers risks from the transition to a low-carbon economy
- Look in: TCFD report, risk management chapter, climate scenario analysis

---

### 欄位 432: 永續績效連結薪酬

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 薪酬治理 |
| Aspect | 治理 |

**Description:** 高階主管薪酬是否與永續/ESG績效指標連結？若有，請說明連結的指標類型。若無連結請填「無」。

**Extraction rules:**
- Keywords: "永續績效薪酬", "ESG連結薪酬", "永續KPI薪酬", "氣候目標薪酬", "Sustainability-linked Compensation"
- Describe the specific ESG metrics used (e.g., 碳排放減量目標、ESG評鑑排名、永續金融業務目標)
- Note: which executives are included (CEO only? All C-suite? All managers?)
- Look in: corporate governance chapter, board compensation report, remuneration policy section

---

## Output Format

For each field, output:

```
欄位 [ID]: [Value]
補充說明: [Data source (report name, chapter, page), scope notes, methodology notes, any limitations]
```

If the value cannot be determined:
```
欄位 [ID]: 無法填答
補充說明: [Reason — not disclosed, information found in different format, section missing, etc.]
```

---

## Common Pitfalls for Finance Fields

1. **Cumulative vs. outstanding**: Many sustainable finance metrics report both cumulative issuance (since inception) and current outstanding balance — always use outstanding balance for stock metrics (101, 103, 407, 409)

2. **Institutional vs. client emissions**: Field 401 (financed emissions) is about the PORTFOLIO'S carbon footprint — not the institution's own operational emissions (which belong in base fields 9-11)

3. **Commitment vs. implementation**: Signing a pledge (PRB, NZBA) is different from having fully implemented it — for boolean fields, True means the commitment/signature exists, not full implementation

4. **TCFD vs. sustainability report**: Many financial institutions publish TCFD reports separately from their sustainability reports — check both documents

5. **Asset class coverage gaps**: PCAF financed emissions often cover only a subset of asset classes; always note what is covered vs. what is excluded

6. **Currency conversion**: Finance fields with monetary values may appear in USD, EUR, or other currencies in international reports — convert to NTD and note the exchange rate and date used

7. **Greenwashing risk in product classification**: Only count loans/investments as "sustainable" if explicitly classified under a recognized green/sustainable label; do not infer based on borrower industry
