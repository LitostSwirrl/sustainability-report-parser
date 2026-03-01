# 產業分類與欄位路由 (Industry Routing)

> Source: `src/field_definitions.py` → `classify_industry()`, `get_final_fields()`, `_get_final_fields_v2()`

---

## Industry Classification

`classify_industry(company_industry: str) -> str`

The function lowercases the input string and checks it against each entry in `INDUSTRY_CLASSIFICATIONS`. The first matching keyword wins. If no keyword matches, the function returns `"一般製造"` as the default.

| Industry | Keywords | Field Module | 永續經濟活動認定附表 |
|----------|----------|--------------|---------------------|
| 水泥 | 水泥, cement, 熟料, clinker, 水泥工業 | CEMENT_FIELDS (201-210) | 附表4 |
| 玻璃 | 玻璃, glass, 平板玻璃, 玻璃陶瓷 | GLASS_FIELDS (211-220) | 附表5 |
| 石油化學 | 石化, petrochemical, 乙烯, 丙烯, 聚乙烯, 聚丙烯, 塑膠工業, 化學工業 | PETROCHEMICAL_FIELDS (221-235) | 附表6 |
| 鋼鐵 | 鋼鐵, steel, 煉鋼, 鋼材, 鋼鐵工業 | STEEL_FIELDS (236-245) | 附表7 |
| 紡織 | 紡織, textile, 纖維, 紡紗, 織布, 染整, 紡織纖維 | TEXTILE_FIELDS (246-255) | 附表8 |
| 造紙 | 造紙, paper, 紙漿, 紙板, 造紙工業 | PAPER_FIELDS (256-265) | 附表9 |
| 半導體 | 半導體, semiconductor, 晶圓, IC, 半導體業 | SEMICONDUCTOR_FIELDS (266-275) | 附表10 |
| 平面顯示器 | 面板, display, TFT, LCD, OLED, 顯示器, 光電業 | DISPLAY_PANEL_FIELDS (276-285) | 附表11 |
| 電腦設備 | 電腦, computer, 筆電, 伺服器, 週邊, 電腦及週邊設備業 | COMPUTER_EQUIPMENT_FIELDS (286-295) | 附表12 |
| 金融 | 金融, 銀行, 保險, 證券, 金控, 金融保險業, 金融業, 期貨商 | FINANCE_FIELDS_V2 (101-104) + FINANCE_EXTENDED_FIELDS (401-432) | N/A |
| 一般製造 (default) | _(no keyword match)_ | MANUFACTURING_COMMON_FIELDS_V2 (101-110) only | N/A |

---

## Field Composition by Industry (V2)

`_get_final_fields_v2(company_industry: str) -> Dict`

Every company starts with **BASE_FIELDS_V2** (fields 1-72, the universal 2026 verification indicators). Industry-specific fields are then merged on top.

### BASE_FIELDS_V2 structure (fields 1-72, all companies)

| Range | Category |
|-------|----------|
| 1-8 | 氣候承諾 (Climate commitments) |
| 9-30 | 碳排放 (GHG emissions: Scope 1, 2, 3 + ISO categories) |
| 31-33 | 資料透明度 (Data transparency) |
| 34-38 | 能源 (Total energy use, 3-year history, breakdown) |
| 39-41 | 燃煤 (Coal use, phase-out plan, fossil fuel transition) |
| 42-43 | 用電 (Electricity use + RE share) |
| 44-47 | 再生能源 (RE capacity, sources, obligations, RE100) |
| 48-55 | 氣候行動 (RE targets, energy saving targets, key reduction strategies) |
| 56-57 | 低碳產品 (Low-carbon products/services + revenue share) |
| 58-65 | 勞動 (LTIFR, injury counts, lost days, major incidents, violations, subsidies, IR/FR, occupational disease) |
| 66-72 | 水資源 (Tap water, surface water, groundwater, other sources, recycled, discharged, consumed) |

### Field Composition per Industry

| Industry | Base Fields | Additional Fields | Approx. Total |
|----------|-------------|-------------------|---------------|
| 金融 | BASE_FIELDS_V2 (1-72) | FINANCE_FIELDS_V2 (101-104) + FINANCE_EXTENDED_FIELDS (401-432) | ~108 fields |
| 水泥 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + CEMENT_FIELDS (201-210) | ~92 fields |
| 玻璃 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + GLASS_FIELDS (211-220) | ~92 fields |
| 石油化學 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + PETROCHEMICAL_FIELDS (221-235) | ~97 fields |
| 鋼鐵 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + STEEL_FIELDS (236-245) | ~92 fields |
| 紡織 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + TEXTILE_FIELDS (246-255) | ~92 fields |
| 造紙 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + PAPER_FIELDS (256-265) | ~92 fields |
| 半導體 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + SEMICONDUCTOR_FIELDS (266-275) | ~92 fields |
| 平面顯示器 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + DISPLAY_PANEL_FIELDS (276-285) | ~92 fields |
| 電腦設備 | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) + COMPUTER_EQUIPMENT_FIELDS (286-295) | ~92 fields |
| 一般製造 (default) | BASE_FIELDS_V2 (1-72) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) | ~82 fields |

---

## Industry-Specific Field Modules (detail)

### FINANCE_FIELDS_V2 (101-104)
Basic sustainable finance metrics for financial institutions.

| Field | Name |
|-------|------|
| 101 | 綠色/永續放款餘額 |
| 102 | 永續經濟活動放款佔比 |
| 103 | 綠色/永續投資餘額 |
| 104 | 適用赤道原則專案融資件數/金額 |

### FINANCE_EXTENDED_FIELDS (401-432)
Extended financial sector fields based on Taiwan Sustainable Finance Evaluation, WBA Financial System Benchmark, and PCAF Standard.

| Field | Name | Category |
|-------|------|----------|
| 401 | 投融資組合碳排放量 | 投融資碳排放 |
| 402 | 投融資碳排放揭露範圍 | 投融資碳排放 |
| 403 | 投融資碳排放基準年 | 投融資碳排放 |
| 404 | 投融資碳排放減量目標 | 投融資碳排放 |
| 405 | 是否執行氣候情境分析 | 氣候風險 |
| 406 | 氣候情境分析範圍說明 | 氣候風險 |
| 407 | 永續連結貸款餘額 | 永續金融商品 |
| 408 | 永續連結貸款佔總放款比例 | 永續金融商品 |
| 409 | ESG主題基金資產規模 | 永續金融商品 |
| 410 | 是否訂定化石燃料融資政策 | 氣候行動 |
| 411 | 化石燃料融資政策說明 | 氣候行動 |
| 412 | 是否簽署國際永續金融倡議 | 永續承諾 |
| 413 | 簽署的永續金融倡議 | 永續承諾 |
| 414 | 是否採用雙重重大性概念 | 報告品質 |
| 415 | 金融包容性措施 | 金融包容 |
| 416 | 防漂綠措施說明 | 報告品質 |
| 417 | 客戶ESG議合件數 | 客戶議合 |
| 418 | 是否參與永續金融評鑑 | 外部評鑑 |
| 419 | 永續金融評鑑排名 | 外部評鑑 |
| 420 | PCAF數據品質分數 | 投融資碳排放 |
| 421 | UN永續原則第三方確信 | 外部確信 |
| 422 | 永續金融人才認證比例 | 人才發展 |
| 423 | 氣候實體風險揭露 | 氣候風險 |
| 424 | 高碳產業放款佔比 | 氣候行動 |
| 425 | 高碳產業放款減量目標 | 氣候行動 |
| 426 | 永續經濟活動放款類別 | 永續金融商品 |
| 427 | 綠色債券承銷金額 | 永續金融商品 |
| 428 | 責任投資策略說明 | 責任投資 |
| 429 | 生物多樣性風險評估 | 自然相關風險 |
| 430 | 微型/小型企業放款比例 | 金融包容 |
| 431 | 氣候轉型風險評估 | 氣候風險 |
| 432 | 永續績效連結薪酬 | 薪酬治理 |

### MANUFACTURING_COMMON_FIELDS_V2 (101-110)
Common fields for all manufacturing industries.

| Field | Name |
|-------|------|
| 101 | 符合永續指引之營收 (Turnover) 佔比 |
| 102 | 符合永續指引之資本支出 (CapEx) 佔比 |
| 103 | 符合永續指引之營運費用 (OpEx) 佔比 |
| 104 | 單位產品溫室氣體排放強度 (特定製程) |
| 105 | 產品製程類別或代表性產品名稱 |
| 106 | 產品年產量 |
| 107 | 是否採用最佳可行技術 (BAT) |
| 108 | 碳排放強度改善目標年 |
| 109 | 碳排放強度改善目標值 |
| 110 | 製程能源效率指標 |

### Industry-Specific Field Ranges

| Industry | Field IDs | Key Metrics |
|----------|-----------|-------------|
| 水泥 (CEMENT) | 201-210 | 熟料/成品年產量、單位GHG排放量、替代原料/燃料比例、熟料係數、CCUS |
| 玻璃 (GLASS) | 211-220 | 平板玻璃產量、單位GHG、廢玻璃使用比例、窯爐類型與能源消耗 |
| 石油化學 (PETROCHEMICAL) | 221-235 | 乙烯/丙烯/苯乙烯/氯乙烯/PE/PP/PVC 各產品產量與單位GHG |
| 鋼鐵 (STEEL) | 236-245 | EAF/一貫製程類型、粗鋼產量、廢鋼使用比例、鐵水/燒結礦/焦炭排放強度 |
| 紡織 (TEXTILE) | 246-255 | 人造纖維/紡紗/染整各製程產量與單位GHG、再生原料比例、永續認證 |
| 造紙 (PAPER) | 256-265 | 各紙類產量(Adt)與單位GHG、廢紙回收比例、COD、FSC/PEFC認證 |
| 半導體 (SEMICONDUCTOR) | 266-275 | IC製造/封測類型、晶圓尺寸/製程節點、單位面積GHG、PFC減排措施 |
| 平面顯示器 (DISPLAY_PANEL) | 276-285 | 面板世代、基板投入面積、單位GHG/單位能源、含氟GHG減量措施 |
| 電腦設備 (COMPUTER_EQUIPMENT) | 286-295 | EPEAT/Energy Star/ISO 14024/ISO 14021認證取得情形、循環設計 |

---

## V1 vs V2 Comparison

The system supports two versions via `get_final_fields(company_industry, version="v2")`.

| Aspect | V1 (legacy) | V2 (2026 verification) |
|--------|-------------|------------------------|
| Base fields | BASE_FIELDS (1-41) + SCOPE3_FIELDS (42-56) + LABOR_EMISSIONS_FIELDS (201-209) + WATER_FIELDS (301-310) | BASE_FIELDS_V2 (1-72, unified numbering) |
| Finance industry fields | FINANCE_FIELDS (57-60) + FINANCE_EXTENDED_FIELDS (401-420) | FINANCE_FIELDS_V2 (101-104) + FINANCE_EXTENDED_FIELDS (401-432) |
| Manufacturing common | MANUFACTURING_COMMON_FIELDS (61-70) | MANUFACTURING_COMMON_FIELDS_V2 (101-110) |
| Industry-specific | Same CEMENT/GLASS/etc. field modules | Same modules (201-295), plus MANUFACTURING_COMMON above |
| Sorting in prompt | Uses `display_order` for custom GHG field ordering | Simple numeric sort (fields already in correct sequence) |
