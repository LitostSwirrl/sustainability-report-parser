"""
Field definitions for Sustainability Report Parser.

Contains 100+ field definitions organized by:
- BASE_FIELDS (1-41): Universal fields for all companies (V1)
- BASE_FIELDS_V2 (1-72): Universal fields for all companies (V2, 2026年驗證指標)
- SCOPE3_FIELDS (42-56): GRI Scope 3 expansion
- LABOR_EMISSIONS_FIELDS (201-209): Labor safety and emissions (V1)
- WATER_FIELDS (301-310): GRI 303 water metrics
- FINANCE_EXTENDED_FIELDS (401-420): Taiwan Sustainable Finance Evaluation + WBA + PCAF
- Industry-specific fields (201-295): Based on Taiwan's Sustainable Finance guidelines

Industry modules:
- FINANCE_FIELDS (57-60): Financial sector basic fields (V1)
- FINANCE_FIELDS_V2 (101-104): Financial sector basic fields (V2)
- FINANCE_EXTENDED_FIELDS (401-420): Financial sector extended (financed emissions, climate scenario, ESG)
- MANUFACTURING_FIELDS (57-60): General manufacturing (V1)
- MANUFACTURING_COMMON_FIELDS_V2 (101-110): Manufacturing common fields (V2)
- CEMENT_FIELDS (201-210): Cement industry
- GLASS_FIELDS (211-220): Glass industry
- PETROCHEMICAL_FIELDS (221-235): Petrochemical industry
- STEEL_FIELDS (236-245): Steel industry
- TEXTILE_FIELDS (246-255): Textile industry
- PAPER_FIELDS (256-265): Paper industry
- SEMICONDUCTOR_FIELDS (266-275): Semiconductor industry
- DISPLAY_PANEL_FIELDS (276-285): Display panel industry
- COMPUTER_EQUIPMENT_FIELDS (286-295): Computer equipment industry
"""

from typing import Dict

# ==========================================
# 1. 基礎欄位定義 (通用 1-41)
# ==========================================

BASE_FIELDS = {
    "1": {"name": "此份永續報告的邊界", "description": "報告書的資料範圍。請簡潔列出：1) 主體公司名稱 2) 涵蓋廠區/據點（若有列出）。限50字以內，不需包含時間範圍。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "報告書邊界", "category": "報告書邊界"},
    "2": {"name": "是否承諾淨零排放或碳中和", "description": "若有淨零/碳中和承諾，請節錄關鍵句（50字以內），包含目標年份。若無明確承諾，填「無承諾」。不需完整引用，只需核心內容。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "3": {"name": "預計達成淨零排放／碳中和年份", "description": "請只填入西元年份，若沒有明確承諾，請留空。若原始資料為民國年份，請協助轉換。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "4": {"name": "是否設定中期溫室氣體絕對減量目標", "description": "企業是否設定了在 2030 年的中期減量目標或檢核點？", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "5": {"name": "中期減量目標年設定", "description": "企業設定的中期（無論是否 2030）減量年份？請只填入年份，若沒有明確設定，請留空。若有多個目標年，這裏填最近的目標年，並在 [補充說明] 中敘明所有目標年。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "6": {"name": "中期溫室氣體絕對減量目標值（百分比）", "description": "以下不算：「單位產品碳排放係數」降低，或是「xx年的溫室氣體總排放量回到xx年水準，或是「僅針對特定廠有設定減排目標」。若關於中期溫室氣體減量目標，只找得到以上相關數據或描述，請留空。", "data_format": "decimal", "unit": "依報告書原始格式", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候承諾"},
    "7": {"name": "中期減量基準年設定", "description": "請判斷企業之中期減量目標，其參照的基準年之西元年份。若未提供明確基準年計算標準，則留空。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "8": {"name": "中期減量基準年排放量", "description": "請判斷企業之中期減量目標，其參照的基準年之碳排放量。若未提供明確基準年計算標準，則留空。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候承諾"},
    "9": {"name": "中期目標是否取得SBT認證", "description": "請判斷企業之中期減量目標，是否取得科學基礎減量目標認證（SBT / SBTi）。填答只有 True/False 兩種可能性，無法判斷時請留空。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "10": {"name": "2024年度總能源使用量", "description": "通常會以熱量（GJ）作為單位，計算時不需排除電力使用，以一家公司的總能源使用數值來收錄。通常可於最後面的附錄查詢得到", "data_format": "decimal", "unit": "GJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "11": {"name": "2023年度總能源使用量", "description": "通常會以熱量（GJ）作為單位，計算時不需排除電力使用，以一家公司的總能源使用數值來收錄。通常可於最後面的附錄查詢得到", "data_format": "decimal", "unit": "GJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "12": {"name": "2022年度總能源使用量", "description": "通常會以熱量（GJ）作為單位，計算時不需排除電力使用，以一家公司的總能源使用數值來收錄。通常可於最後面的附錄查詢得到", "data_format": "decimal", "unit": "GJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "13": {"name": "2024營收資料", "description": "看公司總營收，通常可能在「營運概況」或類似章節中出現，請以新台幣（元）表示，若和報告邊界範圍不同，請在補充說明", "data_format": "integer", "unit": "NTD", "precision": "1", "aspect": "財報", "category": "營收"},
    "14": {"name": "2024總用電量", "description": "只看該公司使用電力或外購電力的數值，自行使用再生能源發電、其他化石燃料的使用不計入。<br>以報告書原記錄單位為主（可能為度或 GJ 等等）", "data_format": "decimal", "unit": "按照報告書原始格式", "precision": "0.0001", "aspect": "環境", "category": "能源使用"},
    "15": {"name": "是否設定節能目標？", "description": "節能、節電等皆可算入，公司是否提出能源效率進步的目標設定，數值為 True or False", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "16": {"name": "節能目標年設定", "description": "請只填入年份，若沒有明確承諾，請留空", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "17": {"name": "節能目標值（百分比）", "description": "請填入目標值的數字，可包含小數點。如節點目標為 30%，則填寫 0.3。", "data_format": "decimal", "unit": "", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "18": {"name": "年節電率目標", "description": "請填入公司2024年度的節電率目標設定（以小數表示，例如 2% 請填 0.02）。並非實際節電量而是設定的目標。無法填答時請留空。", "data_format": "decimal", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "19": {"name": "是否達成政府用電大戶再生能源建置義務", "description": "如果有達到，通常會寫：「已達到/遠高於政府用電大戶條款所規定的10%」。若無法找到相關描述，則判斷為 False。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "再生能源"},
    "20": {"name": "再生能源裝置容量", "description": "僅收公司自行建置的再生能源，範疇為太陽光電、風電、地熱等。<br>請注意不收規劃的數值，只收確定建置完成的容量。", "data_format": "decimal", "unit": "瓩（KW）", "precision": "0.001", "aspect": "環境", "category": "再生能源"},
    "21": {"name": "是否設定再生能源使用目標？", "description": "判斷公司是否設定再生能源使用目標（例如：2030年再生能源使用率達到X%）。填答只有 True/False 兩種可能性，無法判斷時請留空。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "22": {"name": "再生能源目標年設定", "description": "請只填入目標年份（西元年）。若未提及或未設定，請留空。若目標年為 2050，請視為沒有設定目標並留空。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "23": {"name": "再生能源目標值（百分比）", "description": "請填入目標值的數字，可包含小數點", "data_format": "decimal", "unit": "瓩（KW）", "precision": "0.001", "aspect": "氣候指標", "category": "氣候行動"},
    "24": {"name": "是否取得RE100認證？", "description": "請判斷企業之再生能源目標，是否取得RE100目標認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "25": {"name": "是否說明關鍵減量策略", "description": "列舉公司主要減碳策略（限5項）。輸出格式：「策略1、策略2、策略3」。規則：每項策略必須是4-8字的名詞短語。範例：「燃煤改天然氣、太陽能發電、設備汰換、製程優化」。錯誤示範：完整句子、詳細說明、超過8字的描述。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "26": {"name": "是否揭露 2022 - 2024 年溫室氣體排放資料", "description": "通常可於最後面的附錄查詢得到", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "27": {"name": "類別一（值）", "description": "此欄位收集溫室氣體排放量中，範疇一（直接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 1},
    "28": {"name": "類別二（值）", "description": "此欄位收集溫室氣體排放量中，範疇二（輸入能源的間接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 2},
    "29": {"name": "類別三（值）", "description": "此欄位收集溫室氣體排放量中，類別三（運輸的間接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 3},
    "30": {"name": "類別四（值）", "description": "此欄位收集溫室氣體排放量中，類別四的值。（組織使用的產品所產生的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 5},
    "31": {"name": "類別五（值）", "description": "此欄位收集溫室氣體排放量中，類別五的值。（與組織的產品使用相關聯的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 6},
    "32": {"name": "類別六（值）", "description": "此欄位收集溫室氣體排放量中，類別六的值。（由其他來源產生的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 7},
    "33": {"name": "範疇三（值）", "description": "此欄位收集溫室氣體排放量中，範疇三（其他間接溫室氣體排放）的值。<br>若公司有給範疇三直接加總值，請直接填寫總額，但請注意不包含國外／海外廠。<br>若公司給的是類別三到類別六，請協助加總類別三到類別六。<br>若公司寫到類別十五，請協助加總類別三到類別十五。<br>若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度", "display_order": 4},
    "34": {"name": "是否設定範疇三減量目標", "description": "判斷公司是否針對範疇三（Scope 3）設定減量目標或規劃。填答只有 True/False 兩種可能性，無法判斷時請留空。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "35": {"name": "範疇三減量目標實際作為", "description": "範疇三的具體減碳作為（限3項）。輸出格式：「作為1、作為2、作為3」。規則：每項作為必須是4-10字的名詞短語。範例：「供應商減碳輔導、綠色採購、物流優化」。若無具體作為或僅有宣示性文字，留空。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "36": {"name": "是否揭露各項能源使用細項", "description": "是否揭露 2024 年用的各種能源，數值為 True or False", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "37": {"name": "2024年度使用的各種能源項目", "description": "列出2024年各能源使用量。固定格式：「能源: 數值 單位; 」（冒號後空格，分號後空格）。排列順序：電力 > 天然氣 > 柴油 > 汽油 > 液化石油氣 > 燃料油 > 其他。規則：數值不含千分位、只列出報告書中有記載的項目、零值不列出。範例：「電力: 206234 千度; 天然氣: 25283 千立方公尺; 柴油: 634 公秉; 」", "data_format": "string", "unit": "以報告書原始格式", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "38": {"name": "再生能源使用佔總發電量（百分比）", "description": "意指透過利用再生能源所產生之發電量，佔總發電量的比例。通常可於最後面附錄查詢得到", "data_format": "decimal", "unit": "", "precision": "0.000001", "aspect": "氣候指標", "category": "氣候行動"},
    "39": {"name": "再生能源使用來源（自發自用、購電協議、再生能源憑證）", "description": "公司使用的再生能源來源是什麼？", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "40": {"name": "是否生產支持轉型至低碳經濟之產品/服務", "description": "公司是否說明有生產或進行低碳經濟相關的產品或服務內容，如按照特定標準或指引定義低碳產品或服務，請在補充說明中註明", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "41": {"name": "支持轉型至低碳經濟之產品/服務產生的營收或營收占比", "description": "揭露公司2024年「支持轉型至低碳經濟之產品/服務」之收入佔總營收之比例。公司須說明該低碳產品與服務之定義", "data_format": "decimal", "unit": "", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"}
}

# ==========================================
# 2. 模組 A：GRI Scope 3 擴充 (42-56)
# ==========================================

SCOPE3_FIELDS = {
    "42": {"name": "Scope 3 類別 1 (購買商品或服務)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 1 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 8},
    "43": {"name": "Scope 3 類別 2 (資本商品)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 2 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 9},
    "44": {"name": "Scope 3 類別 3 (燃料與能源相關活動)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 3 (非範疇一二之排放) 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 10},
    "45": {"name": "Scope 3 類別 4 (上游運輸和配送)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 4 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 11},
    "46": {"name": "Scope 3 類別 5 (營運廢棄物)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 5 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 12},
    "47": {"name": "Scope 3 類別 6 (商務旅行)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 6 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 13},
    "48": {"name": "Scope 3 類別 7 (員工通勤)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 7 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 14},
    "49": {"name": "Scope 3 類別 8 (上游租賃資產)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 8 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 15},
    "50": {"name": "Scope 3 類別 9 (下游運輸和配送)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 9 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 16},
    "51": {"name": "Scope 3 類別 10 (銷售產品的加工)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 10 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 17},
    "52": {"name": "Scope 3 類別 11 (使用銷售產品)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 11 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 18},
    "53": {"name": "Scope 3 類別 12 (銷售產品廢棄處理)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 12 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 19},
    "54": {"name": "Scope 3 類別 13 (下游租賃資產)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 13 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 20},
    "55": {"name": "Scope 3 類別 14 (特許經營)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 14 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 21},
    "56": {"name": "Scope 3 類別 15 (投資)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 15 進行數值萃取。金融業請特別注意此欄位，通常為投融資組合排放。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3", "display_order": 22}
}

# ==========================================
# 2.5 新增：勞動安全與排碳欄位 (201-209)
# ==========================================

LABOR_EMISSIONS_FIELDS = {
    "201": {
        "name": "失能傷害頻率(LTIFR)",
        "description": "報告年度的失能傷害頻率(Lost Time Injury Frequency Rate)為何？請分別列出男性與女性數值。計算公式通常為：(失能傷害件數 × 1,000,000) / 總工時。若報告書僅提供整體數值，請填寫整體數值並在補充說明中註記。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "勞動安全",
        "category": "職業安全"
    },
    "202": {
        "name": "職業傷害件數",
        "description": "報告年度發生的職業傷害總件數為何？請分別列出死亡、永久失能、暫時失能件數。格式範例：死亡0件、永久失能0件、暫時失能5件。若報告書有依性別分類，請一併列出。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "勞動安全",
        "category": "職業安全"
    },
    "203": {
        "name": "重大職業安全意外事件",
        "description": "報告年度是否有發生重大職業安全意外事件？重大事件包含：造成死亡、永久失能、多人受傷之事故，以及火災、爆炸等工安事故。若有發生，請填入傷亡人數與說明文字（如：死亡1人，因鍋爐爆炸事故）；若無請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "勞動安全",
        "category": "職業安全"
    },
    "204": {
        "name": "損失工作日數",
        "description": "報告年度因職業傷害造成的損失工作日數(Lost Days)為何？此數值通常出現在職業安全統計表格中。",
        "data_format": "decimal",
        "unit": "日",
        "precision": "0.01",
        "aspect": "勞動安全",
        "category": "職業安全"
    },
    "205": {
        "name": "勞動法規違規與裁罰",
        "description": "報告年度是否有違反勞動相關法規之情事？若有，請列出違規法條、違規內容與裁罰金額。相關法規包含：職業安全衛生法、勞動基準法、性別工作平等法等。格式範例：違反職業安全衛生法第6條，罰款新台幣10萬元。若無違規請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "勞動安全",
        "category": "法規遵循"
    },
    "206": {
        "name": "政府補貼或獎勵",
        "description": "報告年度是否接受政府補貼或獎勵計劃？若有，請說明計劃名稱與補貼金額。範例：經濟部工業局智慧製造補助計劃，補助金額新台幣500萬元。若無或未揭露請填「無」或「未揭露」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "政府關係",
        "category": "政府互動"
    },
    "207": {
        "name": "燃煤使用量",
        "description": "報告年度的燃煤使用量為何？請填寫數值與單位。燃煤包含煙煤、無煙煤、褐煤等。若公司不使用燃煤請填「0」或「不適用」。數值通常可在能源使用細項表格中找到。",
        "data_format": "string",
        "unit": "依報告書原始格式",
        "precision": "NA",
        "aspect": "環境",
        "category": "能源使用"
    },
    "208": {
        "name": "燃煤淘汰計劃",
        "description": "公司是否有燃煤淘汰或減量計劃？若有，請說明目標年份與減量目標。範例：預計於2030年前完全淘汰燃煤使用。若不使用燃煤或無相關計劃請填「不適用」或「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "氣候指標",
        "category": "氣候行動"
    },
    "209": {
        "name": "化石燃料轉型計劃",
        "description": "公司是否有化石燃料整體轉型計劃？若有，請說明轉型目標與時程。化石燃料包含：煤炭、天然氣、石油及其衍生燃料。請說明公司如何減少對化石燃料的依賴，例如：提高再生能源佔比、改用低碳燃料等。若無相關計劃請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "氣候指標",
        "category": "氣候行動"
    }
}

# ==========================================
# 3. 水資源欄位 (301-310) - GRI 303 通用
# ==========================================

WATER_FIELDS = {
    "301": {
        "name": "2024年度總取水量",
        "description": "報告年度的總取水量（Water Withdrawal），包含所有水源。單位通常為百萬公升（ML）或公噸。若報告書使用立方公尺（m³），請換算為公噸（1 m³ = 1 公噸）。若公司有多個廠區，請加總所有國內廠區數據。通常可於 GRI 303-3 或環境績效表中找到。",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.01",
        "aspect": "環境",
        "category": "水資源"
    },
    "302": {
        "name": "2023年度總取水量",
        "description": "前一年度（2023年）的總取水量，用於比較年度變化。若報告書使用立方公尺（m³），請換算為公噸（1 m³ = 1 公噸）。",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.01",
        "aspect": "環境",
        "category": "水資源"
    },
    "303": {
        "name": "取水來源分布",
        "description": "取水來源的細項分布。固定格式：「來源: 數值 單位; 」（冒號後空格，分號後空格）。常見來源包含：自來水（第三方水源）、地下水、地表水（河川/湖泊）、海水、雨水收集、再生水。範例：「自來水: 1500000 公噸; 地下水: 50000 公噸; 」。若只揭露總量未分類，請在補充說明中註記。",
        "data_format": "string",
        "unit": "依報告書原始格式",
        "precision": "NA",
        "aspect": "環境",
        "category": "水資源"
    },
    "304": {
        "name": "2024年度總排水量",
        "description": "報告年度的總排水量（Water Discharge）。單位通常為百萬公升（ML）或公噸。若報告書使用立方公尺（m³），請換算為公噸。排水量通常小於取水量，差額為耗水量。",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.01",
        "aspect": "環境",
        "category": "水資源"
    },
    "305": {
        "name": "排水去向分布",
        "description": "排水去向的細項分布。固定格式：「去向: 數值 單位; 」。常見去向包含：污水處理廠、地表水體、海洋、地下滲透、其他第三方。範例：「污水處理廠: 1200000 公噸; 地表水體: 100000 公噸; 」。若只揭露總量，請在補充說明中註記。",
        "data_format": "string",
        "unit": "依報告書原始格式",
        "precision": "NA",
        "aspect": "環境",
        "category": "水資源"
    },
    "306": {
        "name": "2024年度耗水量",
        "description": "報告年度的耗水量（Water Consumption）= 取水量 - 排水量。耗水量代表被蒸發、納入產品、或無法回收的水量。若報告書未直接提供，但有取水量與排水量，請協助計算並在補充說明中註記計算方式。",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.01",
        "aspect": "環境",
        "category": "水資源"
    },
    "307": {
        "name": "用水回收率",
        "description": "製程用水或總用水的回收再利用比例。以小數表示，例如回收率85%請填0.85。此數值可能出現在水資源管理章節或環境績效統計表中。若報告書提供回收水量而非比例，請協助計算比例（回收水量/總用水量）。",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "水資源"
    },
    "308": {
        "name": "是否位於水資源壓力區",
        "description": "公司營運據點是否位於水資源壓力區域（Water-stressed Areas）？報告書可能引用WRI Aqueduct或WWF Water Risk Filter等工具評估。填答只有 True/False 兩種可能性，若報告書未提及水資源壓力風險評估，請留空。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "水資源"
    },
    "309": {
        "name": "是否設定用水減量目標",
        "description": "公司是否設定用水減量或水資源管理目標？例如：「2030年用水強度降低20%」或「2025年水回收率達90%」。填答只有 True/False 兩種可能性，無法判斷時請留空。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "氣候指標",
        "category": "水資源"
    },
    "310": {
        "name": "用水減量目標說明",
        "description": "若有設定用水減量目標，請簡要說明目標內容（限50字）。包含目標年份、目標值、基準年。格式範例：「2030年用水強度較2020年降低20%」。若無目標或欄位309為False，請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "氣候指標",
        "category": "水資源"
    }
}

# ==========================================
# 4. 模組 B-1：金融業專用 (57-60)
# ==========================================

FINANCE_FIELDS = {
    "57": {"name": "綠色/永續放款餘額", "description": "請註明是綠色放款、永續連結貸款或符合指引之放款總額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "58": {"name": "永續經濟活動放款佔比", "description": "分子為符合永續指引之放款，分母為總放款，若無明確佔比請留空", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "金融", "category": "永續金融"},
    "59": {"name": "綠色/永續投資餘額", "description": "包含綠色債券、永續債券或投資電廠等金額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "60": {"name": "適用赤道原則專案融資件數/金額", "description": "請同時列出件數與金額，如：5件 / 20億元", "data_format": "string", "unit": "件/元", "precision": "NA", "aspect": "金融", "category": "永續金融"}
}

# ==========================================
# 4.1 模組 B-1 延伸：金融業延伸欄位 (401-420)
# 依據：永續金融評鑑、WBA Financial System Benchmark、PCAF Standard
# ==========================================

FINANCE_EXTENDED_FIELDS = {
    "401": {
        "name": "投融資組合碳排放量",
        "description": "依據PCAF標準計算的投融資組合碳排放量（Scope 3 Category 15）。包含企業貸款、專案融資、投資等資產類別的financed emissions。通常可於TCFD報告或永續報告書的氣候風險章節找到。",
        "data_format": "decimal",
        "unit": "公噸CO2e",
        "precision": "0.01",
        "aspect": "金融",
        "category": "投融資碳排放"
    },
    "402": {
        "name": "投融資碳排放揭露範圍",
        "description": "列出已揭露financed emissions的資產類別。格式：「資產類別1; 資產類別2;」。常見類別：企業貸款(Corporate loans)、專案融資(Project finance)、商業不動產(Commercial real estate)、房貸(Mortgages)、上市股票(Listed equity)、公司債(Corporate bonds)。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "投融資碳排放"
    },
    "403": {
        "name": "投融資碳排放基準年",
        "description": "投融資組合碳排放減量目標的基準年份。若未設定減量目標或未揭露基準年，請留空。",
        "data_format": "integer",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "投融資碳排放"
    },
    "404": {
        "name": "投融資碳排放減量目標",
        "description": "投融資組合的碳排放減量目標說明（限50字）。格式範例：「2030年投融資碳排放較2021年降低50%」。若無目標請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "投融資碳排放"
    },
    "405": {
        "name": "是否執行氣候情境分析",
        "description": "金融機構是否針對投融資組合執行氣候情境分析（Climate Scenario Analysis）？常見情境包含：IEA NZE、NGFS情境、RCP情境等。填答只有 True/False 兩種可能性。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候風險"
    },
    "406": {
        "name": "氣候情境分析範圍說明",
        "description": "氣候情境分析的涵蓋範圍說明（限100字）。包含：使用的情境（如NGFS、IEA NZE）、分析的資產類別、時間範圍等。若欄位405為False，請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候風險"
    },
    "407": {
        "name": "永續連結貸款餘額",
        "description": "永續連結貸款（Sustainability-Linked Loans, SLL）的餘額，即貸款利率與借款人ESG績效掛鉤的貸款。單位為新台幣元。",
        "data_format": "decimal",
        "unit": "元",
        "precision": "1",
        "aspect": "金融",
        "category": "永續金融商品"
    },
    "408": {
        "name": "永續連結貸款佔總放款比例",
        "description": "永續連結貸款餘額佔總放款餘額的比例。以小數表示，例如5%請填0.05。",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "金融",
        "category": "永續金融商品"
    },
    "409": {
        "name": "ESG主題基金資產規模",
        "description": "管理的ESG主題基金或永續投資基金的總資產規模。單位為新台幣元。適用於投信業或有基金管理業務的金融機構。",
        "data_format": "decimal",
        "unit": "元",
        "precision": "1",
        "aspect": "金融",
        "category": "永續金融商品"
    },
    "410": {
        "name": "是否訂定化石燃料融資政策",
        "description": "金融機構是否訂定針對化石燃料（煤炭、石油、天然氣）產業的融資限制或退出政策？填答只有 True/False 兩種可能性。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候行動"
    },
    "411": {
        "name": "化石燃料融資政策說明",
        "description": "化石燃料融資政策的具體內容（限100字）。包含：限制的產業類別、退出時程、例外條款等。若欄位410為False，請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候行動"
    },
    "412": {
        "name": "是否簽署國際永續金融倡議",
        "description": "是否簽署國際永續金融倡議？常見倡議包含：PRB(責任銀行原則)、PRI(責任投資原則)、PSI(永續保險原則)、NZBA(淨零銀行聯盟)、NZAMI(淨零資產管理倡議)等。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "永續承諾"
    },
    "413": {
        "name": "簽署的永續金融倡議",
        "description": "列出已簽署的國際永續金融倡議。格式：「倡議1、倡議2、倡議3」。常見倡議：PRB、PRI、PSI、NZBA、NZAMI、PCAF、赤道原則。若欄位412為False，請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "永續承諾"
    },
    "414": {
        "name": "是否採用雙重重大性概念",
        "description": "永續報告書是否納入雙重重大性（Double Materiality）概念？雙重重大性同時考量企業對環境社會的影響（impact materiality）與ESG議題對企業財務的影響（financial materiality）。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "報告品質"
    },
    "415": {
        "name": "金融包容性措施",
        "description": "針對弱勢族群或偏鄉地區提供的金融包容性措施說明（限100字）。例如：原住民族金融服務、偏鄉ATM佈建、微型保險、小額貸款等。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "社會",
        "category": "金融包容"
    },
    "416": {
        "name": "防漂綠措施說明",
        "description": "參考金管會「金融機構防漂綠參考指引」訂定的防漂綠措施說明（限100字）。包含：永續金融商品審查機制、ESG資訊驗證程序、行銷宣傳規範等。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "治理",
        "category": "報告品質"
    },
    "417": {
        "name": "客戶ESG議合件數",
        "description": "報告年度與客戶進行ESG議合（Engagement）的件數。議合包含：引導客戶設定減碳目標、提供永續轉型諮詢、要求改善ESG績效等。",
        "data_format": "integer",
        "unit": "件",
        "precision": "NA",
        "aspect": "金融",
        "category": "客戶議合"
    },
    "418": {
        "name": "是否參與永續金融評鑑",
        "description": "是否參與金管會主辦的永續金融評鑑？填答只有 True/False 兩種可能性。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "外部評鑑"
    },
    "419": {
        "name": "永續金融評鑑排名",
        "description": "最近一屆永續金融評鑑的排名結果。填寫格式：「前25%」「26%-50%」「51%-75%」「76%-100%」。若未參與或未公布請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "外部評鑑"
    },
    "420": {
        "name": "PCAF數據品質分數",
        "description": "投融資碳排放計算所使用的PCAF數據品質分數（Data Quality Score）。分數範圍1-5，1為最高品質（使用客戶實際排放數據），5為最低品質（使用產業平均估算）。",
        "data_format": "decimal",
        "unit": "NA",
        "precision": "0.1",
        "aspect": "金融",
        "category": "投融資碳排放"
    },
    # --- 新增欄位 421-432：永續金融評鑑 + WBA Financial System Benchmark ---
    "421": {
        "name": "UN永續原則第三方確信",
        "description": "是否針對簽署的UN永續原則（PRB/PRI/PSI）執行情形取得第三方確信（Assurance）？填答只有 True/False 兩種可能性。若未簽署任何UN永續原則請留空。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "外部確信"
    },
    "422": {
        "name": "永續金融人才認證比例",
        "description": "取得永續金融相關證照（如：永續金融基礎能力測驗、ESG投資分析師等）的員工人數佔總員工人數的比例。以小數表示，例如5%請填0.05。若未揭露請留空。",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "金融",
        "category": "人才發展"
    },
    "423": {
        "name": "氣候實體風險揭露",
        "description": "是否揭露氣候實體風險（颱風、洪水、乾旱、海平面上升等）對投融資組合的影響評估？請簡述評估範圍與主要風險類型（限100字）。若未評估請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候風險"
    },
    "424": {
        "name": "高碳產業放款佔比",
        "description": "對高碳排產業（煤炭開採、石油天然氣、火力發電等）的放款餘額佔總放款餘額的比例。以小數表示，例如10%請填0.10。高碳產業定義依報告書揭露為準。",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "金融",
        "category": "氣候行動"
    },
    "425": {
        "name": "高碳產業放款減量目標",
        "description": "是否設定高碳排產業放款減量或退出目標？請說明目標年份與減量目標（限50字）。例如：「2030年前煤炭融資歸零」。若無目標請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候行動"
    },
    "426": {
        "name": "永續經濟活動放款類別",
        "description": "列出符合《永續經濟活動認定參考指引》的主要放款類別。格式：「類別1; 類別2;」。常見類別：再生能源專案融資、綠建築貸款、電動車貸款、循環經濟產業等。若無相關放款請留空。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "永續金融商品"
    },
    "427": {
        "name": "綠色債券承銷金額",
        "description": "報告年度承銷或發行的綠色債券、永續債券、社會債券總金額。單位為新台幣元。若為證券業請填承銷金額，若為銀行業可填發行金額。",
        "data_format": "decimal",
        "unit": "元",
        "precision": "1",
        "aspect": "金融",
        "category": "永續金融商品"
    },
    "428": {
        "name": "責任投資策略說明",
        "description": "採用的責任投資策略類型。格式：「策略1、策略2」。常見策略：ESG整合（ESG Integration）、負面排除（Exclusion）、正向篩選（Best-in-class）、主題投資、議合與投票（Engagement）、影響力投資。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "責任投資"
    },
    "429": {
        "name": "生物多樣性風險評估",
        "description": "是否評估投融資組合對生物多樣性的影響或依賴風險？參考框架可能包含TNFD、SBTN、ENCORE等。填答只有 True/False 兩種可能性。若報告書未提及生物多樣性風險請留空。",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "自然相關風險"
    },
    "430": {
        "name": "微型/小型企業放款比例",
        "description": "對微型企業及小型企業（依中小企業認定標準）的放款餘額佔總放款餘額的比例。以小數表示，例如15%請填0.15。此指標反映金融包容性。",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "金融",
        "category": "金融包容"
    },
    "431": {
        "name": "氣候轉型風險評估",
        "description": "是否針對投融資組合執行氣候轉型風險評估（政策、技術、市場、聲譽風險）？請簡述評估範圍與方法（限100字）。若未評估請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "金融",
        "category": "氣候風險"
    },
    "432": {
        "name": "永續績效連結薪酬",
        "description": "高階主管薪酬是否與永續/ESG績效指標連結？若有，請說明連結的指標類型（如：碳排放減量、ESG評鑑排名、永續金融業務目標等）。若無連結請填「無」。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "治理",
        "category": "薪酬治理"
    }
}

# ==========================================
# 4. 模組 B-2：一般產業/製造業專用 (57-60)
# ==========================================

MANUFACTURING_FIELDS = {
    "57": {"name": "符合永續指引之營收 (Turnover) 佔比", "description": "辨識企業的營收有多少比例來自於合格的永續經濟活動。若未揭露請留空，或說明是否揭露綠色產品營收佔比", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "58": {"name": "符合永續指引之資本支出 (CapEx) 佔比", "description": "通常指投入於製程改善、節能設備的投資比例", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "59": {"name": "符合永續指引之營運費用 (OpEx) 佔比", "description": "針對永續設備維護、研發等費用比例", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "60": {"name": "單位產品溫室氣體排放強度 (特定製程)", "description": "針對高碳排產業(如水泥、鋼鐵、石化)，請擷取其關鍵產品(如乙烯、水泥熟料)的排放強度數據，若有多項產品請列舉", "data_format": "string", "unit": "公噸CO2e/單位產品", "precision": "0.01", "aspect": "環境", "category": "GHG強度"}
}

# ==========================================
# 5. 模組 C：製造業共通欄位 (61-70)
# ==========================================

MANUFACTURING_COMMON_FIELDS = {
    "61": {
        "name": "符合永續指引之營收 (Turnover) 佔比",
        "description": "辨識企業的營收有多少比例來自於合格的永續經濟活動。若未揭露請留空，或說明是否揭露綠色產品營收佔比",
        "data_format": "decimal",
        "unit": "百分比(%)",
        "precision": "0.01",
        "aspect": "營運",
        "category": "永續經濟活動"
    },
    "62": {
        "name": "符合永續指引之資本支出 (CapEx) 佔比",
        "description": "通常指投入於製程改善、節能設備的投資比例",
        "data_format": "decimal",
        "unit": "百分比(%)",
        "precision": "0.01",
        "aspect": "營運",
        "category": "永續經濟活動"
    },
    "63": {
        "name": "符合永續指引之營運費用 (OpEx) 佔比",
        "description": "針對永續設備維護、研發等費用比例",
        "data_format": "decimal",
        "unit": "百分比(%)",
        "precision": "0.01",
        "aspect": "營運",
        "category": "永續經濟活動"
    },
    "64": {
        "name": "單位產品溫室氣體排放強度 (特定製程)",
        "description": "選擇報告書中明確標示為「代表性產品」或「主要產品」的碳排放強度數值。若有多項產品，選營收佔比最高者。格式：「數值 單位 (產品名)」",
        "data_format": "string",
        "unit": "公噸CO2e/單位產品",
        "precision": "0.01",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "65": {
        "name": "產品製程類別或代表性產品名稱",
        "description": "公司主要產品類別，限3項以內。格式：「產品1、產品2、產品3」。使用報告書中的原始名稱，不需加註解說明。",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "66": {
        "name": "產品年產量",
        "description": "2024年該代表性產品的年產量",
        "data_format": "decimal",
        "unit": "依產品單位（公噸、平方公尺等）",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "67": {
        "name": "是否採用最佳可行技術 (BAT)",
        "description": "企業是否採用或規劃採用最佳可行技術來降低碳排放",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "技術採用"
    },
    "68": {
        "name": "碳排放強度改善目標年",
        "description": "企業設定達成特定碳排放強度目標的年份",
        "data_format": "integer",
        "unit": "西元年",
        "precision": "NA",
        "aspect": "氣候指標",
        "category": "氣候行動"
    },
    "69": {
        "name": "碳排放強度改善目標值",
        "description": "企業設定的碳排放強度目標值",
        "data_format": "decimal",
        "unit": "公噸CO2e/單位產品",
        "precision": "0.0001",
        "aspect": "氣候指標",
        "category": "氣候行動"
    },
    "70": {
        "name": "製程能源效率指標",
        "description": "單位產品能源消耗量 (GJ/公噸產品)",
        "data_format": "decimal",
        "unit": "GJ/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "能源效率"
    }
}
# ==========================================
# 4. 水泥產業專屬欄位 (201-210)
# ==========================================

CEMENT_FIELDS = {
    "201": {
        "name": "水泥熟料年產量",
        "description": "2024年水泥熟料 (Clinker) 生產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "202": {
        "name": "水泥熟料單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "最近一年單位產品溫室氣體排放量（範疇一+範疇二），扣除分配給廢氣生產之溫室氣體排放量。永續經濟活動認定標準：≤0.90 公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "203": {
        "name": "水泥成品年產量",
        "description": "2024年水泥成品生產量（包含各種類型水泥）",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "204": {
        "name": "水泥成品單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "最近一年單位產品溫室氣體排放量（範疇一+範疇二）。永續經濟活動認定標準：≤0.87 公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "205": {
        "name": "替代原料使用比例",
        "description": "使用廢棄物、副產品等替代原料佔總原料使用量之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "206": {
        "name": "替代燃料使用比例",
        "description": "使用廢棄物衍生燃料等替代燃料佔總燃料使用量之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "207": {
        "name": "水泥窯協同處理廢棄物量",
        "description": "利用水泥窯協同處理廢棄物的年處理量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "208": {
        "name": "熟料／水泥比 (Clinker Factor)",
        "description": "水泥產品中熟料含量佔比，數值越低表示使用更多替代性膠凝材料",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "技術指標"
    },
    "209": {
        "name": "CCUS技術應用情形",
        "description": "是否應用碳捕捉、利用與封存技術，以及年碳捕捉量",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "技術採用"
    },
    "210": {
        "name": "是否符合永續經濟活動技術篩選標準",
        "description": "根據附表4判斷：水泥熟料≤0.90且水泥成品≤0.87公噸CO2e/公噸",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "合規性",
        "category": "永續經濟活動"
    }
}
# ==========================================
# 5. 玻璃產業專屬欄位 (211-220)
# ==========================================

GLASS_FIELDS = {
    "211": {
        "name": "主要玻璃產品類型",
        "description": "說明主要生產的玻璃產品類型：平板玻璃、板狀玻璃、浮法玻璃、或其他玻璃製品",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "212": {
        "name": "平板玻璃年產量",
        "description": "2024年平板玻璃（Flat Glass）總產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "213": {
        "name": "平板玻璃單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "單位產品GHG排放量。技術篩選標準：≤1.0121公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "214": {
        "name": "玻璃碎片（廢玻璃）使用比例",
        "description": "生產過程中使用回收玻璃碎片（Cullet）佔總原料投入之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "215": {
        "name": "玻璃窯爐製程能源消耗量",
        "description": "單位產品能源消耗量（熔爐能源效率）",
        "data_format": "decimal",
        "unit": "GJ/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "能源效率"
    },
    "216": {
        "name": "窯爐類型與技術",
        "description": "說明採用的窯爐技術類型（如：浮法窯、電熔窯、純氧燃燒技術等）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "技術資訊"
    },
    "217": {
        "name": "替代燃料使用情形",
        "description": "是否使用替代燃料（如：生質能、廢棄物衍生燃料）及使用比例",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "218": {
        "name": "產品碳足跡驗證情形",
        "description": "是否取得產品碳足跡標籤或環保標章認證",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "產品認證"
    },
    "219": {
        "name": "製程NOx或SOx減量措施",
        "description": "空氣污染物減量技術採用情形（如：脫硝、脫硫設備）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "環境管理"
    },
    "220": {
        "name": "是否符合永續經濟活動技術篩選標準",
        "description": "根據附表5判斷：平板玻璃單位GHG排放量≤1.0121公噸CO2e/公噸",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "合規性",
        "category": "永續經濟活動"
    }
}


# ==========================================
# 6. 石油化學產業專屬欄位 (221-235)
# ==========================================

PETROCHEMICAL_FIELDS = {
    "221": {
        "name": "主要石化產品類型",
        "description": "列舉企業主要生產的石化產品類別（如：乙烯、丙烯、聚乙烯等）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "222": {
        "name": "乙烯/丙烯/丁二烯年產量",
        "description": "若生產乙烯、丙烯或丁二烯，請填寫年產量（可列舉多項）",
        "data_format": "string",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "223": {
        "name": "乙烯/丙烯/丁二烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.9400公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "224": {
        "name": "苯乙烯年產量",
        "description": "若生產苯乙烯(Styrene)，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "225": {
        "name": "苯乙烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤1.0551公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "226": {
        "name": "氯乙烯年產量",
        "description": "若生產氯乙烯(Vinyl Chloride)，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "227": {
        "name": "氯乙烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.5026公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "228": {
        "name": "聚乙烯(PE)年產量",
        "description": "若生產聚乙烯，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "229": {
        "name": "聚乙烯(PE)單位溫室氣體排放量",
        "description": "技術篩選標準：≤1.0823公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "230": {
        "name": "聚丙烯(PP)年產量",
        "description": "若生產聚丙烯，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "231": {
        "name": "聚丙烯(PP)單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.4374公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "232": {
        "name": "聚氯乙烯(PVC)年產量",
        "description": "若生產PVC，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "233": {
        "name": "聚氯乙烯(PVC)單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.4544公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "234": {
        "name": "其他石化產品（乙二醇/酚/丙酮/丙烯腈）資訊",
        "description": "若生產乙二醇(≤2.0750)、酚/丙酮(≤0.8741)、丙烯腈(≤1.0570)，請說明產量與排放強度",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "產品資訊"
    },
    "235": {
        "name": "是否符合永續經濟活動技術篩選標準",
        "description": "根據附表6判斷：各產品單位GHG排放量是否符合對應閾值",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "合規性",
        "category": "永續經濟活動"
    }
}


# ==========================================
# 5. 鋼鐵產業專屬欄位 (236-245)
# ==========================================

STEEL_FIELDS = {
    "236": {
        "name": "鋼鐵生產製程類型",
        "description": "說明主要採用的製程類型：電弧爐(EAF)、一貫製程(高爐+煉鋼爐)、或其他製程",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "製程資訊"
    },
    "237": {
        "name": "鋼品類型",
        "description": "主要生產的鋼材類型：碳鋼、高合金鋼、或兩者兼有",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "238": {
        "name": "粗鋼年產量",
        "description": "2024年粗鋼（crude steel）總產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "239": {
        "name": "電弧爐鋼品單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "若採用電弧爐製程，請填寫單位產品GHG排放量。技術篩選標準：高合金鋼≤0.620、碳鋼≤0.476公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "240": {
        "name": "廢鋼使用比例",
        "description": "廢鋼投入量佔總鋼鐵原料投入量之比例。技術篩選標準：高合金鋼≥70%、碳鋼≥90%",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "241": {
        "name": "鐵水年產量",
        "description": "若採用一貫製程（高爐煉鐵），請填寫鐵水(hot metal/molten iron)年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "242": {
        "name": "鐵水單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "若採用一貫製程，請填寫鐵水單位GHG排放量。技術篩選標準：≤1.443公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "243": {
        "name": "燒結礦單位溫室氣體排放量",
        "description": "若生產燒結礦，請填寫單位GHG排放量。技術篩選標準：≤0.242公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "244": {
        "name": "焦炭單位溫室氣體排放量",
        "description": "若生產焦炭（不包括褐煤焦炭），請填寫單位GHG排放量。技術篩選標準：≤0.237公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "245": {
        "name": "是否符合永續經濟活動技術篩選標準",
        "description": "根據附表7判斷：依製程類型（EAF或一貫）及產品類型（碳鋼或高合金鋼）對應標準",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "合規性",
        "category": "永續經濟活動"
    }
}

# ==========================================
# 7. 紡織產業專屬欄位 (246-255)
# ==========================================

TEXTILE_FIELDS = {
    "246": {"name": "主要紡織製程類型", "description": "說明企業主要從事的製程：人造纖維製造、紡紗織布、染整、或多製程整合", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "247": {"name": "人造纖維產品類型與年產量", "description": "若生產人造纖維，請列舉產品類型（聚酯粒/短纖/長纖/加工絲、尼龍粒/長纖/加工絲）及年產量", "data_format": "string", "unit": "公噸", "precision": "NA", "aspect": "營運", "category": "產量"},
    "248": {"name": "人造纖維單位溫室氣體排放量", "description": "各產品類型單位GHG排放量（範疇一+範疇二）。技術標準：聚酯粒≤0.2275、聚酯短纖≤0.5661、聚酯長纖≤1.1020、聚酯加工絲≤0.8503、尼龍粒≤1.0425、尼龍長纖≤1.5420、尼龍加工絲≤0.7484", "data_format": "string", "unit": "公噸CO2e/公噸", "precision": "NA", "aspect": "環境", "category": "GHG強度"},
    "249": {"name": "紡紗織布年產量", "description": "若從事紡紗織布製程，請填寫年產量", "data_format": "decimal", "unit": "公噸", "precision": "0.0001", "aspect": "營運", "category": "產量"},
    "250": {"name": "紡紗織布單位溫室氣體排放量", "description": "技術篩選標準：≤2.2公噸CO2e/公噸", "data_format": "decimal", "unit": "公噸CO2e/公噸", "precision": "0.0001", "aspect": "環境", "category": "GHG強度"},
    "251": {"name": "染整加工年產量", "description": "若從事染整製程，請填寫年加工量", "data_format": "decimal", "unit": "公噸", "precision": "0.0001", "aspect": "營運", "category": "產量"},
    "252": {"name": "染整加工單位溫室氣體排放量", "description": "技術篩選標準：≤2.7公噸CO2e/公噸", "data_format": "decimal", "unit": "公噸CO2e/公噸", "precision": "0.0001", "aspect": "環境", "category": "GHG強度"},
    "253": {"name": "再生原料使用比例", "description": "使用回收材料或再生原料佔總原料投入之比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "254": {"name": "永續紡織認證取得情形", "description": "是否取得GRS（全球回收標準）、RCS（回收材料標準）或其他永續認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "255": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表8判斷：依製程類型對應相應GHG排放標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 8. 造紙產業專屬欄位 (256-265)
# ==========================================

PAPER_FIELDS = {
    "256": {"name": "主要紙類產品類型", "description": "列舉主要生產的紙類：漂白硫酸鹽漿、紙板、紙箱用紙(裱面紙板/瓦楞芯紙)、家庭用紙、印刷書寫用紙、特殊紙", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "257": {"name": "紙類年產量（氣乾噸Adt）", "description": "各類紙品年產量，以氣乾噸(Air Dry Ton, Adt)為單位", "data_format": "string", "unit": "Adt", "precision": "NA", "aspect": "營運", "category": "產量"},
    "258": {"name": "紙類產品單位溫室氣體排放量", "description": "各紙類GHG排放量（範疇一+範疇二）。技術標準：漂白硫酸鹽漿≤0.70、紙板≤0.90、裱面紙板≤0.90、瓦楞芯紙≤0.90、家庭用紙≤1.60、印刷書寫用紙≤0.90、特殊紙≤2.20 公噸CO2e/Adt", "data_format": "string", "unit": "公噸CO2e/Adt", "precision": "NA", "aspect": "環境", "category": "GHG強度"},
    "259": {"name": "單位產品能源消耗量", "description": "紙類生產能源消耗強度", "data_format": "decimal", "unit": "Mcal/Adt", "precision": "0.01", "aspect": "環境", "category": "能源效率"},
    "260": {"name": "廢紙回收使用比例", "description": "使用廢紙或再生原料佔總原料投入之比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "261": {"name": "事業廢棄物回收再利用率", "description": "製程產生的事業廢棄物回收再利用比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "262": {"name": "COD（化學需氧量）產生量", "description": "單位產品COD產生量或排放量", "data_format": "decimal", "unit": "公斤/Adt", "precision": "0.01", "aspect": "環境", "category": "水資源"},
    "263": {"name": "FSC/PEFC森林認證情形", "description": "是否取得FSC或PEFC等森林管理認證", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "264": {"name": "綠色產品或環保標章取得情形", "description": "產品是否取得環保標章或綠色產品認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "265": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表9判斷：各紙類產品GHG排放量是否符合對應閾值", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 9. 半導體產業專屬欄位 (266-275)
# ==========================================

SEMICONDUCTOR_FIELDS = {
    "266": {"name": "主要業務類型", "description": "IC製造（晶圓廠）或IC封裝測試", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "267": {"name": "晶圓尺寸與年產量", "description": "若為IC製造，請說明晶圓尺寸（6吋/8吋/12吋）及年產量（萬片約當8吋）", "data_format": "string", "unit": "萬片（約當8吋）", "precision": "NA", "aspect": "營運", "category": "產量"},
    "268": {"name": "製程節點技術", "description": "若為12吋晶圓，請說明主要製程節點（成熟製程≥10nm或先進製程<10nm）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "技術資訊"},
    "269": {"name": "IC製造單位面積溫室氣體排放量", "description": "晶圓單位面積GHG排放量（範疇一+範疇二）。技術標準：6吋以下≤2.18、8吋≤2.51、12吋成熟製程≤1.31、12吋先進製程≤9.58 公斤CO2e/平方公分", "data_format": "decimal", "unit": "公斤CO2e/平方公分", "precision": "0.01", "aspect": "環境", "category": "GHG強度"},
    "270": {"name": "IC封測年產量", "description": "若為封測業務，請說明年封裝或測試產量", "data_format": "string", "unit": "千個", "precision": "NA", "aspect": "營運", "category": "產量"},
    "271": {"name": "IC封測單位產品用電量", "description": "封測製程單位產品用電量。技術標準：導線架≤55、BGA≤22、FlipChip≤230、Bumping≤85、測試≤12 kWh/千個", "data_format": "string", "unit": "kWh/千個", "precision": "NA", "aspect": "環境", "category": "能源效率"},
    "272": {"name": "PFC（全氟化物）減排措施", "description": "針對含氟溫室氣體的減量技術或設備使用情形", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "技術採用"},
    "273": {"name": "製程用水回收率", "description": "製程用水回收再利用比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "水資源"},
    "274": {"name": "綠色製造或責任商業聯盟(RBA)認證", "description": "是否取得RBA、ISO 14001或其他綠色製造相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "275": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表10判斷：依晶圓尺寸/製程節點或封測類型對應標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 10. 平面顯示器面板產業專屬欄位 (276-285)
# ==========================================

DISPLAY_PANEL_FIELDS = {
    "276": {"name": "面板技術類型", "description": "主要生產的面板技術：LCD、OLED、或其他", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "277": {"name": "面板世代與產線規格", "description": "說明主要產線的面板世代（如G3.5、G4、G6、G8.5等）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "278": {"name": "年基板投入面積", "description": "2024年基板投入總面積", "data_format": "decimal", "unit": "平方公尺", "precision": "0.01", "aspect": "營運", "category": "產量"},
    "279": {"name": "單位基板溫室氣體排放量（範疇一+範疇二）", "description": "技術標準（選項1-排放量）：3.5代以下≤0.600、4代以上≤0.150 公噸CO2e/平方公尺", "data_format": "decimal", "unit": "公噸CO2e/平方公尺", "precision": "0.001", "aspect": "環境", "category": "GHG強度"},
    "280": {"name": "單位基板能源消耗量", "description": "技術標準（選項2-能源）：3.5代以下≤600、4代以上≤120 kWh/平方公尺", "data_format": "decimal", "unit": "kWh/平方公尺", "precision": "0.01", "aspect": "環境", "category": "能源效率"},
    "281": {"name": "顯示器能效等級或認證", "description": "產品能效等級（如Energy Star）或相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "282": {"name": "含氟溫室氣體減量措施", "description": "製程使用SF6、NF3等氣體的減量或處理技術", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "技術採用"},
    "283": {"name": "製程廢液回收處理率", "description": "製程產生的化學廢液回收處理比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "環境管理"},
    "284": {"name": "綠色產品或環境標章取得情形", "description": "產品是否取得環保標章或綠色產品相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "285": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表11判斷：依面板世代選擇排放量或能源消耗量標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 11. 電腦及週邊設備產業專屬欄位 (286-295)
# ==========================================

COMPUTER_EQUIPMENT_FIELDS = {
    "286": {"name": "主要產品類型", "description": "列舉主要生產的電腦及週邊設備（如：桌上型電腦、筆記型電腦、伺服器、顯示器、印表機等）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "287": {"name": "EPEAT標章取得情形", "description": "產品是否取得EPEAT（電子產品環境評估工具）標章及等級（金牌/銀牌/銅牌）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "288": {"name": "Energy Star或節能標章取得情形", "description": "產品是否取得Energy Star或台灣節能標章認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "289": {"name": "ISO 14024第一類環保標章取得情形", "description": "產品是否取得經ISO 14024認定的第一類環保標章", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "290": {"name": "ISO 14021第二類環境宣告情形", "description": "是否依ISO 14021規範自行宣告環境訴求，並經第三方查驗證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "291": {"name": "產品能源效率等級", "description": "產品能源效率分級或耗電量資訊", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "能源效率"},
    "292": {"name": "產品碳足跡標籤取得情形", "description": "產品是否取得碳足跡標籤或產品碳足跡認證", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "293": {"name": "產品可回收設計或循環經濟措施", "description": "產品設計是否考慮易拆解、模組化、使用再生材料等循環經濟原則", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "循環經濟"},
    "294": {"name": "產品維修服務或延長保固措施", "description": "是否提供延長保固、維修服務或升級方案以延長產品生命週期", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "社會", "category": "產品責任"},
    "295": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表12判斷：產品是否取得EPEAT、ISO 14024環保標章、Energy Star/節能標章、或ISO 14021第三方查驗證的環境宣告（任一項即可）", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}




# ==========================================
# V2 欄位定義 (2026年驗證指標)
# 依據 ESG檢測儀欄位收集一覽表 重新編號
# ==========================================

# Field ID mapping: V1 (old) -> V2 (new)
FIELD_MAPPING_V1_TO_V2 = {
    # Climate commitments (old 2-9 -> new 1-8)
    "2": "1", "3": "2", "4": "3", "5": "4", "6": "5", "7": "6", "8": "7", "9": "8",
    # Emissions (old 27,28,33,29,30,31,32 -> new 9-15)
    "27": "9", "28": "10", "33": "11", "29": "12", "30": "13", "31": "14", "32": "15",
    # Scope 3 categories (old 42-56 -> new 16-30)
    "42": "16", "43": "17", "44": "18", "45": "19", "46": "20", "47": "21", "48": "22",
    "49": "23", "50": "24", "51": "25", "52": "26", "53": "27", "54": "28", "55": "29", "56": "30",
    # Data transparency (old 26,34,35 -> new 31-33)
    "26": "31", "34": "32", "35": "33",
    # Energy (old 10-12,36,37 -> new 34-38)
    "10": "34", "11": "35", "12": "36", "36": "37", "37": "38",
    # Coal/fossil fuel (old 207-209 -> new 39-41)
    "207": "39", "208": "40", "209": "41",
    # Electricity (old 14,38 -> new 42-43)
    "14": "42", "38": "43",
    # Renewable energy (old 20,39,19,24 -> new 44-47)
    "20": "44", "39": "45", "19": "46", "24": "47",
    # Climate action (old 21-23,15-18,25 -> new 48-55)
    "21": "48", "22": "49", "23": "50", "15": "51", "16": "52", "17": "53", "18": "54", "25": "55",
    # Low carbon products (old 40-41 -> new 56-57)
    "40": "56", "41": "57",
    # Labor (old 201-205 -> new 58-61, 64) - 注意：新欄位 62 (受傷死亡比率) 和 63 (職業病) 無 V1 對應
    "201": "58", "202": "59", "204": "60", "203": "61", "205": "64",
    # Government subsidies (old 206 -> new 65)
    "206": "65",
    # Water fields 66-72 are new structure (原 64-70 重新編號)
}

FIELD_MAPPING_V2_TO_V1 = {v: k for k, v in FIELD_MAPPING_V1_TO_V2.items()}

BASE_FIELDS_V2 = {
    # === 氣候承諾 (1-8) ===
    "1": {"name": "是否承諾淨零排放／碳中和", "description": "若有淨零/碳中和承諾，請節錄關鍵句（50字以內），包含目標年份。若無明確承諾，填「無承諾」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "2": {"name": "預計達成淨零排放／碳中和年份", "description": "請只填入西元年份，若沒有明確承諾，請留空。若原始資料為民國年份，請協助轉換。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "3": {"name": "是否設定中期溫室氣體絕對減量目標", "description": "企業是否設定了在達到淨零前的中期減量檢核點？", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "4": {"name": "中期減量目標年設定", "description": "請只填入年份，若沒有明確設定，請留空。若有多個目標年，填最近的目標年，並在補充說明中敘明所有目標年。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "5": {"name": "中期溫室氣體絕對減量目標值（百分比）", "description": "若僅有「單位產品碳排放係數降低」或「特定廠減排目標」，請留空。以小數表示（如30%填0.3）。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候承諾"},
    "6": {"name": "中期減量基準年設定", "description": "中期目標對應的基準年西元年份。若未提供明確基準年，則留空。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
    "7": {"name": "中期減量基準年排放量", "description": "中期目標的基準年碳排放量。若未提供明確基準年數據，則留空。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候承諾"},
    "8": {"name": "中期目標是否取得SBT認證", "description": "中期減量目標是否取得科學基礎減量目標認證（SBT/SBTi）。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},

    # === 碳排放 (9-30) ===
    "9": {"name": "範疇一/類別一（值）", "description": "溫室氣體排放量中，範疇一（直接排放）的值。若公司有加總值，請填寫總額，不含海外廠。若沒有2024年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "10": {"name": "範疇二/類別二（值）", "description": "溫室氣體排放量中，範疇二（間接排放/外購電力）的值。若公司有加總值，請填寫總額，不含海外廠。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "11": {"name": "範疇三（值）", "description": "溫室氣體排放量中，範疇三（其他間接排放）的總值。若公司給的是類別三到六或類別三到十五，請協助加總。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "12": {"name": "類別三（值）", "description": "ISO/CNS 14064-1類別三（運輸的間接溫室氣體排放）的值。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "13": {"name": "類別四（值）", "description": "ISO/CNS 14064-1類別四（組織使用的產品所產生的間接溫室氣體排放）的值。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "14": {"name": "類別五（值）", "description": "ISO/CNS 14064-1類別五（與組織產品使用相關聯的間接溫室氣體排放）的值。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "15": {"name": "類別六（值）", "description": "ISO/CNS 14064-1類別六（由其他來源產生的間接溫室氣體排放）的值。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "16": {"name": "Scope 3 類別 1 (購買商品或服務)", "description": "GHG Protocol 範疇三類別1。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "17": {"name": "Scope 3 類別 2 (資本商品)", "description": "GHG Protocol 範疇三類別2。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "18": {"name": "Scope 3 類別 3 (燃料與能源相關活動)", "description": "GHG Protocol 範疇三類別3（非範疇一二之排放）。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "19": {"name": "Scope 3 類別 4 (上游運輸和配送)", "description": "GHG Protocol 範疇三類別4。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "20": {"name": "Scope 3 類別 5 (營運廢棄物)", "description": "GHG Protocol 範疇三類別5。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "21": {"name": "Scope 3 類別 6 (商務旅行)", "description": "GHG Protocol 範疇三類別6。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "22": {"name": "Scope 3 類別 7 (員工通勤)", "description": "GHG Protocol 範疇三類別7。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "23": {"name": "Scope 3 類別 8 (上游租賃資產)", "description": "GHG Protocol 範疇三類別8。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "24": {"name": "Scope 3 類別 9 (下游運輸和配送)", "description": "GHG Protocol 範疇三類別9。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "25": {"name": "Scope 3 類別 10 (銷售產品的加工)", "description": "GHG Protocol 範疇三類別10。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "26": {"name": "Scope 3 類別 11 (使用銷售產品)", "description": "GHG Protocol 範疇三類別11。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "27": {"name": "Scope 3 類別 12 (銷售產品廢棄處理)", "description": "GHG Protocol 範疇三類別12。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "28": {"name": "Scope 3 類別 13 (下游租賃資產)", "description": "GHG Protocol 範疇三類別13。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "29": {"name": "Scope 3 類別 14 (特許經營)", "description": "GHG Protocol 範疇三類別14。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},
    "30": {"name": "Scope 3 類別 15 (投資)", "description": "GHG Protocol 範疇三類別15。金融業請特別注意，通常為投融資組合排放。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "碳排放"},

    # === 資料透明度 (31-33) ===
    "31": {"name": "是否揭露近三年溫室氣體排放資料", "description": "企業是否有逐年揭露溫室氣體排放狀況（2022-2024年）。通常可於最後附錄查詢。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "32": {"name": "是否設定範疇三減量目標", "description": "判斷公司是否針對範疇三（Scope 3）設定減量目標或規劃。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "33": {"name": "範疇三減量目標實際作為", "description": "範疇三的具體減碳作為（限3項）。格式：「作為1、作為2、作為3」。若無具體作為或僅有宣示性文字，留空。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},

    # === 能源 (34-38) ===
    "34": {"name": "2024年度總能源使用量", "description": "通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。", "data_format": "decimal", "unit": "MJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "35": {"name": "2023年度總能源使用量", "description": "通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。", "data_format": "decimal", "unit": "MJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "36": {"name": "2022年度總能源使用量", "description": "通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。", "data_format": "decimal", "unit": "MJ", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "37": {"name": "是否揭露各項能源使用細項", "description": "是否揭露2024年使用的各種能源細項。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "能源"},
    "38": {"name": "2024年度使用的各種能源項目", "description": "列出各能源使用量。格式：「能源: 數值 單位; 」。排序：電力>天然氣>柴油>汽油>其他。", "data_format": "string", "unit": "依報告書原始格式", "precision": "NA", "aspect": "環境", "category": "能源"},

    # === 燃煤 (39-41) ===
    "39": {"name": "燃煤使用量", "description": "報告年度的燃煤使用量。燃煤包含煙煤、無煙煤、褐煤等。若公司不使用燃煤請填「0」或「不適用」。", "data_format": "string", "unit": "依報告書原始格式", "precision": "NA", "aspect": "環境", "category": "燃煤"},
    "40": {"name": "燃煤淘汰計劃", "description": "公司是否有燃煤淘汰或減量計劃？若有，請說明目標年份與減量目標。若不使用燃煤請填「不適用」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "燃煤"},
    "41": {"name": "化石燃料轉型計劃", "description": "公司是否有化石燃料整體轉型計劃？請說明轉型目標與時程。化石燃料包含煤炭、天然氣、石油。若無相關計劃請填「無」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "燃煤"},

    # === 用電 (42-43) ===
    "42": {"name": "當年度總用電量", "description": "只看該公司使用電力或外購電力的數值，自行使用再生能源發電不計入。以報告書原記錄單位為主。", "data_format": "decimal", "unit": "度（KWh）", "precision": "0.0001", "aspect": "環境", "category": "能源"},
    "43": {"name": "再生能源使用佔總發電量（百分比）", "description": "透過利用再生能源所產生之發電量，佔總發電量的比例。以小數表示。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "環境", "category": "能源"},

    # === 再生能源 (44-47) ===
    "44": {"name": "再生能源裝置容量", "description": "僅收公司自行建置的再生能源（太陽光電、風電、地熱等）。只收確定建置完成的容量，不收規劃數值。", "data_format": "decimal", "unit": "瓩（KW）", "precision": "0.001", "aspect": "環境", "category": "再生能源"},
    "45": {"name": "再生能源使用來源（自發自用、購電協議、再生能源憑證）", "description": "公司使用的再生能源來源是什麼？", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "再生能源"},
    "46": {"name": "是否達成政府用電大戶再生能源建置義務", "description": "如果有達到，通常會寫「已達到/遠高於政府用電大戶條款所規定的10%」。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "再生能源"},
    "47": {"name": "是否取得RE100認證", "description": "請判斷企業之再生能源目標，是否取得RE100目標認證。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "再生能源"},

    # === 氣候行動 (48-55) ===
    "48": {"name": "是否設定再生能源使用目標", "description": "是否設定要於何時達到再生能源使用率幾%。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "49": {"name": "再生能源目標年設定", "description": "請只填入目標年份（西元年）。若未提及或目標年為2050，請留空。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "50": {"name": "再生能源目標值（百分比）", "description": "請填入目標值的數字，可包含小數點。以小數表示。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "51": {"name": "是否設定節能目標", "description": "節能、節電等皆可算入。僅處理明確寫出節能目標設定的內容。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "52": {"name": "節能目標年設定", "description": "請只填入年份，若沒有明確承諾，請留空。", "data_format": "integer", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "53": {"name": "節能目標值（百分比）", "description": "請填入目標值的數字，可包含小數點。如30%則填0.3。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "54": {"name": "節電目標值設定（百分比）", "description": "請填入公司設定的節電目標值（以小數表示，例如2%請填0.02）。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "55": {"name": "是否說明關鍵減量策略", "description": "列舉公司主要減碳策略（限5項）。格式：「策略1、策略2、策略3」。每項4-8字名詞短語。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},

    # === 資料透明度-低碳產品 (56-57) ===
    "56": {"name": "是否生產支持轉型至低碳經濟之產品/服務", "description": "公司是否說明有生產或進行低碳經濟相關的產品或服務內容。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "57": {"name": "支持轉型至低碳經濟之產品/服務產生的營收或營收占比", "description": "揭露公司2024年低碳產品/服務之收入佔總營收之比例。公司須說明該低碳產品與服務之定義。", "data_format": "decimal", "unit": "元", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},

    # === 勞動 (58-62) ===
    "58": {"name": "失能傷害頻率(LTIFR)", "description": "報告年度的失能傷害頻率(Lost Time Injury Frequency Rate)。請提供整體數值。", "data_format": "decimal", "unit": "NA", "precision": "0.0001", "aspect": "勞動", "category": "職災"},
    "59": {"name": "職業傷害件數", "description": "報告年度發生的職業傷害總件數。格式：死亡X件、永久失能X件、暫時失能X件。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "職災"},
    "60": {"name": "損失工作日數", "description": "報告年度因職業傷害造成的損失工作日數(Lost Days)。此數值通常出現在職業安全統計表格中。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "職災"},
    "61": {"name": "重大職業安全意外事件", "description": "報告年度是否有發生重大職業安全意外事件？重大事件包含：造成死亡、永久失能、多人受傷之事故，以及火災、爆炸等工安事故。若有發生，請填入傷亡人數與說明文字（如：死亡1人，因鍋爐爆炸事故）；若無請填「無」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "工安"},
    "62": {"name": "勞動法規違規與裁罰", "description": "報告年度是否有違反勞動法規？若有請列出違規內容與裁罰金額。若無請填「無」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "勞動裁罰"},

    # === 治理 (63) ===
    "63": {"name": "政府補貼或獎勵", "description": "報告年度是否接受政府補貼或獎勵計劃？若有請說明計劃名稱與金額。若無請填「無」或「未揭露」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "治理", "category": "補貼"},

    # === 勞動延伸 (64-65) 新增 ===
    "64": {"name": "受傷、死亡比率", "description": "報告年度的職業傷害率(IR)與死亡率(FR)。傷害率計算公式：(傷害件數 × 200,000) / 總工時。死亡率計算公式：(死亡人數 × 200,000) / 總工時。格式範例：傷害率0.5、死亡率0。若報告書未揭露請留空。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "職災"},
    "65": {"name": "職業病", "description": "該公司當年度是否發生職業病？若有，請填入人數與說明文字（如：3人，塵肺症）。職業病包含：職業性癌症、呼吸系統疾病、皮膚病、聽力損失、肌肉骨骼疾病等經認定之職業病。若無請填「無」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "勞動", "category": "職災"},

    # === 水資源 (66-72) ===
    "66": {"name": "取水量-自來水", "description": "公司用水量中，取自自來水廠的水（如自來水、水庫水等）。若公司僅寫總用水量，請留空。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "67": {"name": "取水量-地表水", "description": "公司用水量中，取自自然河川的水（如溪流、攔河堰等）。若公司僅寫總用水量，請留空。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "68": {"name": "取水量-地下水", "description": "公司用水量中，取自地下水的水。若公司僅寫總用水量，請留空。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "69": {"name": "取水量-其他來源（海水、冷凝水、雨水、再生水）", "description": "公司用水量中，取自其他來源的水（如海水淡化、雨水等）。若公司僅寫總用水量，請留空。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "70": {"name": "回收水量", "description": "公司在生產過程中回收的水資源。通常回收水量會比取水量高，因為一滴水會被重複利用。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "71": {"name": "排放水量", "description": "公司在生產過程最後排放掉的廢污水（廢水、排放水、放流水同概念）。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
    "72": {"name": "耗用水量", "description": "生產過程中消耗掉，沒有回到自然界的水。若報告書有明確揭露耗用水量請填入，若無明確資料請留空，無須協助公司計算。", "data_format": "decimal", "unit": "噸", "precision": "0.0001", "aspect": "環境", "category": "水資源"},
}

# Industry-specific fields for V2 (renumbered to 101+ to avoid conflict with base 1-70)
FINANCE_FIELDS_V2 = {
    "101": {"name": "綠色/永續放款餘額", "description": "請註明是綠色放款、永續連結貸款或符合指引之放款總額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "102": {"name": "永續經濟活動放款佔比", "description": "分子為符合永續指引之放款，分母為總放款，若無明確佔比請留空", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "金融", "category": "永續金融"},
    "103": {"name": "綠色/永續投資餘額", "description": "包含綠色債券、永續債券或投資電廠等金額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "104": {"name": "適用赤道原則專案融資件數/金額", "description": "請同時列出件數與金額，如：5件 / 20億元", "data_format": "string", "unit": "件/元", "precision": "NA", "aspect": "金融", "category": "永續金融"}
}

MANUFACTURING_COMMON_FIELDS_V2 = {
    "101": {"name": "符合永續指引之營收 (Turnover) 佔比", "description": "辨識企業的營收有多少比例來自於合格的永續經濟活動。若未揭露請留空。", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "102": {"name": "符合永續指引之資本支出 (CapEx) 佔比", "description": "通常指投入於製程改善、節能設備的投資比例", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "103": {"name": "符合永續指引之營運費用 (OpEx) 佔比", "description": "針對永續設備維護、研發等費用比例", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "營運", "category": "永續經濟活動"},
    "104": {"name": "單位產品溫室氣體排放強度 (特定製程)", "description": "選擇報告書中明確標示為「代表性產品」或「主要產品」的碳排放強度數值。", "data_format": "string", "unit": "公噸CO2e/單位產品", "precision": "0.01", "aspect": "環境", "category": "GHG強度"},
    "105": {"name": "產品製程類別或代表性產品名稱", "description": "公司主要產品類別，限3項以內。格式：「產品1、產品2、產品3」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "106": {"name": "產品年產量", "description": "2024年該代表性產品的年產量", "data_format": "decimal", "unit": "依產品單位", "precision": "0.0001", "aspect": "營運", "category": "產品資訊"},
    "107": {"name": "是否採用最佳可行技術 (BAT)", "description": "企業是否採用或規劃採用最佳可行技術來降低碳排放", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "技術採用"},
    "108": {"name": "碳排放強度改善目標年", "description": "企業設定達成特定碳排放強度目標的年份", "data_format": "integer", "unit": "西元年", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "109": {"name": "碳排放強度改善目標值", "description": "企業設定的碳排放強度目標值", "data_format": "decimal", "unit": "公噸CO2e/單位產品", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "110": {"name": "製程能源效率指標", "description": "單位產品能源消耗量 (GJ/公噸產品)", "data_format": "decimal", "unit": "GJ/公噸", "precision": "0.0001", "aspect": "環境", "category": "能源效率"},
}


# ==========================================
# 產業分類系統 (Industry Classification)
# ==========================================

INDUSTRY_CLASSIFICATIONS = {
    "水泥": {
        "keywords": ["水泥", "cement", "熟料", "clinker", "水泥工業"],
        "field_module": "CEMENT",
        "field_range": (71, 80),
        "附表編號": "附表4"
    },
    "玻璃": {
        "keywords": ["玻璃", "glass", "平板玻璃", "玻璃陶瓷"],
        "field_module": "GLASS",
        "field_range": (81, 90),
        "附表編號": "附表5"
    },
    "石油化學": {
        "keywords": ["石化", "petrochemical", "乙烯", "丙烯", "聚乙烯", "聚丙烯", "塑膠工業", "化學工業"],
        "field_module": "PETROCHEMICAL",
        "field_range": (91, 105),
        "附表編號": "附表6"
    },
    "鋼鐵": {
        "keywords": ["鋼鐵", "steel", "煉鋼", "鋼材", "鋼鐵工業"],
        "field_module": "STEEL",
        "field_range": (106, 115),
        "附表編號": "附表7"
    },
    "紡織": {
        "keywords": ["紡織", "textile", "纖維", "紡紗", "織布", "染整", "紡織纖維"],
        "field_module": "TEXTILE",
        "field_range": (116, 125),
        "附表編號": "附表8"
    },
    "造紙": {
        "keywords": ["造紙", "paper", "紙漿", "紙板", "造紙工業"],
        "field_module": "PAPER",
        "field_range": (126, 135),
        "附表編號": "附表9"
    },
    "半導體": {
        "keywords": ["半導體", "semiconductor", "晶圓", "IC", "半導體業"],
        "field_module": "SEMICONDUCTOR",
        "field_range": (136, 145),
        "附表編號": "附表10"
    },
    "平面顯示器": {
        "keywords": ["面板", "display", "TFT", "LCD", "OLED", "顯示器", "光電業"],
        "field_module": "DISPLAY_PANEL",
        "field_range": (146, 155),
        "附表編號": "附表11"
    },
    "電腦設備": {
        "keywords": ["電腦", "computer", "筆電", "伺服器", "週邊", "電腦及週邊設備業"],
        "field_module": "COMPUTER_EQUIPMENT",
        "field_range": (156, 165),
        "附表編號": "附表12"
    },
    "金融": {
        "keywords": ["金融", "銀行", "保險", "證券", "金控", "金融保險業", "金融業", "期貨商"],
        "field_module": "FINANCE",
        "field_range": (57, 60),
        "附表編號": None
    }
}

def classify_industry(company_industry: str) -> str:
    """
    Classify company into specific industry category.
    Returns industry key or "一般製造" as default.
    """
    if not company_industry:
        return "一般製造"

    industry_lower = company_industry.lower()

    for industry_key, industry_info in INDUSTRY_CLASSIFICATIONS.items():
        for keyword in industry_info["keywords"]:
            if keyword in industry_lower or keyword.lower() in industry_lower:
                return industry_key

    return "一般製造"  # Default to general manufacturing


def get_final_fields(company_industry: str, version: str = "v2") -> Dict:
    """
    根據產業別合併基礎欄位與特定欄位

    Args:
        company_industry: 產業類別字串
        version: 欄位版本 ("v1" 舊版 | "v2" 2026年驗證指標)

    Returns:
        合併後的欄位定義字典
    """
    if version == "v2":
        return _get_final_fields_v2(company_industry)
    else:
        return _get_final_fields_v1(company_industry)


def _get_final_fields_v2(company_industry: str) -> Dict:
    """
    V2 欄位組合 - 使用新的70欄位基礎結構 (2026年驗證指標)
    """
    # 1. 基礎欄位 (1-70)
    final_fields = BASE_FIELDS_V2.copy()

    # 2. 分類產業
    industry_category = classify_industry(company_industry)

    # 3. 加入產業專屬欄位
    if industry_category == "金融":
        final_fields.update(FINANCE_FIELDS_V2)
        final_fields.update(FINANCE_EXTENDED_FIELDS)
        print(f"[V2] 偵測到金融產業：{company_industry}，載入金融業欄位（欄位101-104）+ 金融業延伸欄位（欄位401-432）。共 {len(final_fields)} 個欄位。")

    elif industry_category in ["水泥", "玻璃", "石油化學", "鋼鐵", "紡織",
                                "造紙", "半導體", "平面顯示器", "電腦設備"]:
        final_fields.update(MANUFACTURING_COMMON_FIELDS_V2)
        # Industry-specific fields use original numbering (71+)
        industry_info = INDUSTRY_CLASSIFICATIONS[industry_category]
        field_module_name = f"{industry_info['field_module']}_FIELDS"
        field_module = globals()[field_module_name]
        final_fields.update(field_module)

        print(f"[V2] 偵測到{industry_category}產業：{company_industry}")
        print(f"載入製造業共通欄位（欄位101-110）+ {industry_category}專屬欄位。共 {len(final_fields)} 個欄位。")

    else:
        final_fields.update(MANUFACTURING_COMMON_FIELDS_V2)
        print(f"[V2] 偵測到一般製造產業：{company_industry}，載入製造業共通欄位（欄位101-110）。共 {len(final_fields)} 個欄位。")

    return final_fields


def _get_final_fields_v1(company_industry: str) -> Dict:
    """
    V1 欄位組合 - 舊版結構 (向後相容)
    """
    # 1. Base fields (universal)
    final_fields = BASE_FIELDS.copy()

    # 2. Scope 3 fields (universal)
    final_fields.update(SCOPE3_FIELDS)

    # 2.5. Labor & Emissions fields (universal)
    final_fields.update(LABOR_EMISSIONS_FIELDS)

    # 3. Water fields (universal - GRI 303)
    final_fields.update(WATER_FIELDS)

    # 5. Classify industry
    industry_category = classify_industry(company_industry)

    # 6. Add industry-specific fields
    if industry_category == "金融":
        final_fields.update(FINANCE_FIELDS)
        final_fields.update(FINANCE_EXTENDED_FIELDS)
        print(f"[V1] 偵測到金融產業：{company_industry}，載入金融業專屬欄位（欄位57-60）+ 金融業延伸欄位（欄位401-420）。")

    elif industry_category in ["水泥", "玻璃", "石油化學", "鋼鐵", "紡織",
                                "造紙", "半導體", "平面顯示器", "電腦設備"]:
        # Add common manufacturing fields
        final_fields.update(MANUFACTURING_COMMON_FIELDS)

        # Add specific industry fields
        industry_info = INDUSTRY_CLASSIFICATIONS[industry_category]
        field_module_name = f"{industry_info['field_module']}_FIELDS"
        field_module = globals()[field_module_name]
        final_fields.update(field_module)

        print(f"[V1] 偵測到{industry_category}產業：{company_industry}")
        print(f"載入製造業共通欄位（欄位61-70）+ {industry_category}專屬欄位（欄位{industry_info['field_range'][0]}-{industry_info['field_range'][1]}）")
        print(f"參考：永續經濟活動認定參考指引 {industry_info['附表編號']}")

    else:
        # General manufacturing - only common fields
        final_fields.update(MANUFACTURING_COMMON_FIELDS)
        print(f"[V1] 偵測到一般製造產業：{company_industry}，載入製造業共通欄位（欄位61-70）。")

    return final_fields


def _get_industry_specific_guidance(industry_category: str, company_info: dict = None) -> str:
    """Generate industry-specific guidance for prompt"""

    if company_info is None:
        company_info = {}

    if industry_category == "金融":
        return ""

    guidance_map = {
        "水泥": """
## 🏭 水泥產業特定指引

根據《永續經濟活動認定參考指引第二版》附表4，水泥產業的關鍵永續指標：

### 核心技術篩選標準（氣候變遷減緩）：
1. **水泥熟料** 單位產品溫室氣體排放量（範疇一+範疇二）≤ 0.90 公噸CO2e/公噸
2. **水泥成品** 單位產品溫室氣體排放量（範疇一+範疇二）≤ 0.87 公噸CO2e/公噸

### 重點搜尋關鍵字：
- 水泥熟料 (Clinker)、水泥成品
- 單位產品碳排放、排放強度
- 替代原料（廢棄物、副產品）、替代燃料
- 水泥窯協同處理
- 熟料係數 (Clinker Factor)
- CCUS（碳捕捉利用與封存）

### 資料可能出現位置：
- 「環境永續」或「氣候變遷」章節的製程排放數據
- 產品碳足跡專章
- GRI 305排放量揭露
- 附錄的環境數據統計表
""",
        "玻璃": """
## 🪟 玻璃產業特定指引

根據《永續經濟活動認定參考指引第二版》附表5，玻璃產業的關鍵永續指標：

### 核心技術篩選標準（氣候變遷減緩）：
- **平板玻璃製造** 單位產品溫室氣體排放量（範疇一+範疇二）≤ 1.0121 公噸CO2e/公噸

### 重點搜尋關鍵字：
- 平板玻璃、板狀玻璃、浮法玻璃
- 單位產品碳排放強度
- 玻璃製品、資源再生綠色產品認定

### 資料可能出現位置：
- 環境績效數據章節
- 產品碳足跡資訊
- 循環經濟相關章節（再生玻璃使用）
""",
        "石油化學": """
## ⚗️ 石油化學產業特定指引

根據《永續經濟活動認定參考指引第二版》附表6，石化產業涵蓋9種主要產品：

### 核心技術篩選標準（各產品排放閾值）：
1. 乙烯、丙烯、丁二烯 ≤ 0.9400 公噸CO2e/公噸
2. 苯乙烯 ≤ 1.0551 公噸CO2e/公噸
3. 氯乙烯 ≤ 0.5026 公噸CO2e/公噸
4. 乙二醇 ≤ 2.0750 公噸CO2e/公噸
5. 酚/丙酮 ≤ 0.8741 公噸CO2e/公噸
6. 聚氯乙烯(PVC) ≤ 0.4544 公噸CO2e/公噸
7. 聚乙烯(PE) ≤ 1.0823 公噸CO2e/公噸
8. 聚丙烯(PP) ≤ 0.4374 公噸CO2e/公噸
9. 丙烯腈 ≤ 1.0570 公噸CO2e/公噸

### 重點搜尋關鍵字：
- 產品別產量與排放強度數據
- 輕裂解 (Naphtha Cracking)
- 石化產品碳足跡

### 資料可能出現位置：
- 產品產量統計表
- 製程環境績效章節
- 產品碳足跡報告
""",
        "鋼鐵": """
## 🏗️ 鋼鐵產業特定指引

根據《永續經濟活動認定參考指引第二版》附表7，鋼鐵產業區分製程與產品類型：

### 核心技術篩選標準：

#### 電弧爐製程 (EAF)：
**選項1 - 排放量標準：**
- 高合金鋼 ≤ 0.620 公噸CO2e/公噸
- 碳鋼 ≤ 0.476 公噸CO2e/公噸

**選項2 - 廢鋼使用比例：**
- 高合金鋼 ≥ 70%
- 碳鋼 ≥ 90%

#### 一貫製程：
- 鐵水 ≤ 1.443 公噸CO2e/公噸
- 燒結礦 ≤ 0.242 公噸CO2e/公噸
- 焦炭（不包括褐煤焦炭）≤ 0.237 公噸CO2e/公噸

### 重點搜尋關鍵字：
- 電弧爐 (EAF)、一貫廠、高爐
- 廢鋼使用率、廢鋼比例
- 鐵水、燒結礦、焦炭產量
- 高合金鋼、碳鋼

### 資料可能出現位置：
- 生產製程說明章節
- 環境績效統計表
- 循環經濟章節（廢鋼再利用）
""",
        "紡織": """
## 🧵 紡織產業特定指引

根據《永續經濟活動認定參考指引第二版》附表8，紡織產業涵蓋多個製程階段：

### 核心技術篩選標準：

#### 1. 人造纖維製造 - 溫室氣體排放量標準（範疇一+範疇二）：
- 聚酯粒 ≤ 0.2275 公噸CO2e/公噸
- 聚酯短纖 ≤ 0.5661 公噸CO2e/公噸
- 聚酯長纖 ≤ 1.1020 公噸CO2e/公噸
- 聚酯加工絲 ≤ 0.8503 公噸CO2e/公噸
- 尼龍粒 ≤ 1.0425 公噸CO2e/公噸
- 尼龍長纖 ≤ 1.5420 公噸CO2e/公噸
- 尼龍加工絲 ≤ 0.7484 公噸CO2e/公噸

#### 2. 紡紗織布 - 溫室氣體排放量標準：
≤ 2.2 公噸CO2e/公噸

#### 3. 染整 - 溫室氣體排放量標準：
≤ 2.7 公噸CO2e/公噸

### 重點搜尋關鍵字：
- 人造纖維、聚酯、尼龍
- 紡紗、織布、染整
- 單位產品用電量
- 能源消耗量
- 再生料、回收材料
- GRS (Global Recycled Standard)、RCS (Recycled Claimed Standard)

### 資料可能出現位置：
- 製程產量統計
- 環境績效數據
- 循環經濟或永續材料章節
- 產品認證資訊
""",
        "造紙": """
## 📄 造紙產業特定指引

根據《永續經濟活動認定參考指引第二版》附表9，造紙產業涵蓋7種紙類：

### 核心技術篩選標準（溫室氣體排放量，範疇一+範疇二）：
1. 漂白硫酸鹽漿 ≤ 0.70 公噸CO2e/氣乾噸(Adt)
2. 紙板 ≤ 0.90 公噸CO2e/Adt
3. 紙箱用紙-裱面紙板 ≤ 0.90 公噸CO2e/Adt
4. 紙箱用紙-瓦楞芯紙 ≤ 0.90 公噸CO2e/Adt
5. 家庭用紙 ≤ 1.60 公噸CO2e/Adt
6. 印刷書寫用紙 ≤ 0.90 公噸CO2e/Adt
7. 特殊紙 ≤ 2.20 公噸CO2e/Adt

### 其他重要指標：
- 單位產品能源消耗量 (Mcal/Adt)
- 原料及再生原料使用量
- 事業廢棄物回收再利用率
- COD（化學需氧量）產生量

### 重點搜尋關鍵字：
- 紙漿、紙板、瓦楞紙
- 氣乾噸 (Adt - Air Dry Ton)
- 廢紙回收率、再生紙
- 能源消耗強度

### 資料可能出現位置：
- 產品產量統計表（依紙類分類）
- 環境績效章節
- 循環經濟數據（廢紙利用率）
- 製程能源使用統計
""",
        "半導體": """
## 💻 半導體產業特定指引

根據《永續經濟活動認定參考指引第二版》附表10，半導體產業區分IC製造與封測：

### 核心技術篩選標準：

#### IC製造 - 單位產品溫室氣體排放量（範疇一+範疇二）：
1. 6吋以下晶圓 ≤ 2.18 公斤CO2e/平方公分
2. 8吋晶圓 ≤ 2.51 公斤CO2e/平方公分
3. 12吋晶圓（成熟製程 ≥10nm）≤ 1.31 公斤CO2e/平方公分
4. 12吋晶圓（先進製程 <10nm）≤ 9.58 公斤CO2e/平方公分

#### IC測試封裝 - 單位產品用電量：
1. 導線架 (Lead Frame) ≤ 55 kWh/千個
2. 球型陣列封裝 (BGA) ≤ 22 kWh/千個
3. 覆晶封裝 (Flip Chip) ≤ 230 kWh/千個
4. 晶圓凸塊 (Bumping) ≤ 85 kWh/千個
5. 測試 ≤ 12 kWh/千個

### 重點搜尋關鍵字：
- 晶圓尺寸（6吋、8吋、12吋）
- 製程節點（nm）
- 封裝技術
- 單位面積排放強度
- PFC減排（全氟化物）

### 資料可能出現位置：
- 製程技術說明章節
- 溫室氣體管理專章（含PFC排放）
- 廠區環境績效數據
- 綠色製造章節
""",
        "平面顯示器": """
## 🖥️ 平面顯示器面板產業特定指引

根據《永續經濟活動認定參考指引第二版》附表11：

### 核心技術篩選標準：

#### 選項1 - 溫室氣體排放量（範疇一+範疇二）：
- 3.5代以下 ≤ 0.600 公噸CO2e/平方公尺
- 4代以上 ≤ 0.150 公噸CO2e/平方公尺

#### 選項2 - 能源消耗量：
- 3.5代以下 ≤ 600 kWh/平方公尺
- 4代以上 ≤ 120 kWh/平方公尺

### 重點搜尋關鍵字：
- 面板世代（G3.5, G4, G6, G8.5等）
- 基板面積、投入面積
- LCD、OLED
- 單位基板排放強度
- 單位基板能源消耗

### 資料可能出現位置：
- 產品技術與產線說明
- 環境績效數據
- 能源管理章節
""",
        "電腦設備": """
## 💻 電腦及週邊設備產業特定指引

根據《永續經濟活動認定參考指引第二版》附表12：

### 核心技術篩選標準（任一項即可）：
1. 產品取得 **EPEAT標章**
2. 產品取得經由 **ISO 14024** 認定之第一類環保標章
3. 產品取得 **Energy Star** 或 **台灣節能標章**
4. 透過遵循 **ISO 14021** 規範，自行宣告環境訴求（第二類環境標誌），且經第三方查驗證

### 重點搜尋關鍵字：
- EPEAT認證
- Energy Star
- 節能標章
- 環保標章、綠色產品
- 能源效率分級
- ISO 14021 環境宣告

### 資料可能出現位置：
- 產品責任或永續產品章節
- 綠色產品認證清單
- 環境標章取得情形
- 產品能源效率資訊
""",
        "一般製造": """
## 🏭 一般製造業指引

針對一般製造業，請特別注意以下通用指標：

### 重點搜尋關鍵字：
- 能源使用與管理
- 溫室氣體排放數據
- 廢棄物管理與資源循環
- 生產效率與技術創新

### 資料可能出現位置：
- 環境永續章節
- 氣候變遷管理章節
- 能源管理專章
- 循環經濟相關章節
"""
    }

    return guidance_map.get(industry_category, "")



