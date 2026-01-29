"""
Field definitions for Sustainability Report Parser.

Contains 60+ field definitions organized by:
- BASE_FIELDS (1-41): Universal fields for all companies
- SCOPE3_FIELDS (42-56): GRI Scope 3 expansion
- Industry-specific fields (57-165): Based on Taiwan's Sustainable Finance guidelines

Industry modules:
- FINANCE_FIELDS (57-60): Financial sector
- MANUFACTURING_FIELDS (57-60): General manufacturing
- CEMENT_FIELDS (71-80): Cement industry
- GLASS_FIELDS (81-90): Glass industry
- PETROCHEMICAL_FIELDS (91-105): Petrochemical industry
- STEEL_FIELDS (106-115): Steel industry
- TEXTILE_FIELDS (116-125): Textile industry
- PAPER_FIELDS (126-135): Paper industry
- SEMICONDUCTOR_FIELDS (136-145): Semiconductor industry
- DISPLAY_PANEL_FIELDS (146-155): Display panel industry
- COMPUTER_EQUIPMENT_FIELDS (156-165): Computer equipment industry
"""

from typing import Dict

# ==========================================
# 1. 基礎欄位定義 (通用 1-41)
# ==========================================

BASE_FIELDS = {
    "1": {"name": "此份永續報告的邊界", "description": "主要用來判斷報告書的資料範圍，可能包含統計廠區、事業單位、年份等範圍資訊，以文字紀錄即可", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "報告書邊界", "category": "報告書邊界"},
    "2": {"name": "是否承諾淨零排放或碳中和", "description": "請將企業針對淨零承諾的文字敘述重點節錄並輸出，請勿改寫。若無明確承諾，請填「無承諾」。", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候承諾"},
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
    "25": {"name": "是否說明關鍵減量策略", "description": "通常會製圖/表說明特定年區間的減碳策略，甚至寫出該策略的減碳預估比例", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "26": {"name": "是否揭露 2022 - 2024 年溫室氣體排放資料", "description": "通常可於最後面的附錄查詢得到", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "27": {"name": "類別一（值）", "description": "此欄位收集溫室氣體排放量中，範疇一（直接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "28": {"name": "類別二（值）", "description": "此欄位收集溫室氣體排放量中，範疇二（輸入能源的間接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "29": {"name": "類別三（值）", "description": "此欄位收集溫室氣體排放量中，類別三（運輸的間接溫室氣體排放）的值。<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "30": {"name": "類別四（值）", "description": "此欄位收集溫室氣體排放量中，類別四的值。（組織使用的產品所產生的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "31": {"name": "類別五（值）", "description": "此欄位收集溫室氣體排放量中，類別五的值。（與組織的產品使用相關聯的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "32": {"name": "類別六（值）", "description": "此欄位收集溫室氣體排放量中，類別六的值。（由其他來源產生的間接溫室氣體排放）的值<br>若公司有給加總值，請直接填寫總額，但請注意不包含國外／海外廠。若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。<br>因目前多數公司並未採用新版的碳排分類方式，所以若沒有找到，可以直接選[無法填答]", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "33": {"name": "範疇三（值）", "description": "此欄位收集溫室氣體排放量中，範疇三（其他間接溫室氣體排放）的值。<br>若公司有給範疇三直接加總值，請直接填寫總額，但請注意不包含國外／海外廠。<br>若公司給的是類別三到類別六，請協助加總類別三到類別六。<br>若公司寫到類別十五，請協助加總類別三到類別十五。<br>若公司給的是個別工廠，請協助進行加總（國外／海外工廠不計）。<br>若沒有 2024 年資料，請於補充說明註記。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"},
    "34": {"name": "是否設定範疇三減量目標", "description": "判斷公司是否針對範疇三（Scope 3）設定減量目標或規劃。填答只有 True/False 兩種可能性，無法判斷時請留空。", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "35": {"name": "範疇三減量目標實際作為", "description": "公司以什麼方式進行範疇三的溫室氣體排放減量", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "36": {"name": "是否揭露各項能源使用細項", "description": "是否揭露 2024 年用的各種能源，數值為 True or False", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "37": {"name": "2024年度使用的各種能源項目", "description": "2024 年用的各種能源，通常可在最後面的附錄查詢得到，請寫出各細項數值。", "data_format": "string", "unit": "以報告書原始格式", "precision": "0.0001", "aspect": "氣候指標", "category": "氣候行動"},
    "38": {"name": "再生能源使用佔總發電量（百分比）", "description": "意指透過利用再生能源所產生之發電量，佔總發電量的比例。通常可於最後面附錄查詢得到", "data_format": "decimal", "unit": "", "precision": "0.000001", "aspect": "氣候指標", "category": "氣候行動"},
    "39": {"name": "再生能源使用來源（自發自用、購電協議、再生能源憑證）", "description": "公司使用的再生能源來源是什麼？", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "氣候行動"},
    "40": {"name": "是否生產支持轉型至低碳經濟之產品/服務", "description": "公司是否說明有生產或進行低碳經濟相關的產品或服務內容，如按照特定標準或指引定義低碳產品或服務，請在補充說明中註明", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "氣候指標", "category": "資料透明度"},
    "41": {"name": "支持轉型至低碳經濟之產品/服務產生的營收或營收占比", "description": "揭露公司2024年「支持轉型至低碳經濟之產品/服務」之收入佔總營收之比例。公司須說明該低碳產品與服務之定義", "data_format": "decimal", "unit": "", "precision": "0.0001", "aspect": "氣候指標", "category": "資料透明度"}
}

# ==========================================
# 2. 模組 A：GRI Scope 3 擴充 (42-56)
# ==========================================

SCOPE3_FIELDS = {
    "42": {"name": "Scope 3 類別 1 (購買商品或服務)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 1 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "43": {"name": "Scope 3 類別 2 (資本商品)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 2 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "44": {"name": "Scope 3 類別 3 (燃料與能源相關活動)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 3 (非範疇一二之排放) 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "45": {"name": "Scope 3 類別 4 (上游運輸和配送)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 4 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "46": {"name": "Scope 3 類別 5 (營運廢棄物)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 5 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "47": {"name": "Scope 3 類別 6 (商務旅行)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 6 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "48": {"name": "Scope 3 類別 7 (員工通勤)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 7 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "49": {"name": "Scope 3 類別 8 (上游租賃資產)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 8 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "50": {"name": "Scope 3 類別 9 (下游運輸和配送)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 9 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "51": {"name": "Scope 3 類別 10 (銷售產品的加工)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 10 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "52": {"name": "Scope 3 類別 11 (使用銷售產品)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 11 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "53": {"name": "Scope 3 類別 12 (銷售產品廢棄處理)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 12 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "54": {"name": "Scope 3 類別 13 (下游租賃資產)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 13 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "55": {"name": "Scope 3 類別 14 (特許經營)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 14 進行數值萃取。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"},
    "56": {"name": "Scope 3 類別 15 (投資)", "description": "請搜尋報告書中關於溫室氣體盤查的章節，針對 GHG Protocol 定義的類別 15 進行數值萃取。金融業請特別注意此欄位，通常為投融資組合排放。", "data_format": "decimal", "unit": "公噸CO2e", "precision": "0.0001", "aspect": "環境", "category": "Scope 3"}
}

# ==========================================
# 3. 模組 B-1：金融業專用 (57-60)
# ==========================================

FINANCE_FIELDS = {
    "57": {"name": "綠色/永續放款餘額", "description": "請註明是綠色放款、永續連結貸款或符合指引之放款總額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "58": {"name": "永續經濟活動放款佔比", "description": "分子為符合永續指引之放款，分母為總放款，若無明確佔比請留空", "data_format": "decimal", "unit": "百分比(%)", "precision": "0.01", "aspect": "金融", "category": "永續金融"},
    "59": {"name": "綠色/永續投資餘額", "description": "包含綠色債券、永續債券或投資電廠等金額", "data_format": "decimal", "unit": "元", "precision": "1", "aspect": "金融", "category": "永續金融"},
    "60": {"name": "適用赤道原則專案融資件數/金額", "description": "請同時列出件數與金額，如：5件 / 20億元", "data_format": "string", "unit": "件/元", "precision": "NA", "aspect": "金融", "category": "永續金融"}
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
        "description": "針對高碳排產業(如水泥、鋼鐵、石化)，請擷取其關鍵產品(如乙烯、水泥熟料)的排放強度數據，若有多項產品請列舉",
        "data_format": "string",
        "unit": "公噸CO2e/單位產品",
        "precision": "0.01",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "65": {
        "name": "產品製程類別或代表性產品名稱",
        "description": "請明確填寫企業主要產品的製程類別或代表性產品名稱，例如：水泥（熟料、水泥成品）、玻璃（平板玻璃）、石化（乙烯、丙烯）等",
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
# 4. 水泥產業專屬欄位 (71-80)
# ==========================================

CEMENT_FIELDS = {
    "71": {
        "name": "水泥熟料年產量",
        "description": "2024年水泥熟料 (Clinker) 生產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "72": {
        "name": "水泥熟料單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "最近一年單位產品溫室氣體排放量（範疇一+範疇二），扣除分配給廢氣生產之溫室氣體排放量。永續經濟活動認定標準：≤0.90 公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "73": {
        "name": "水泥成品年產量",
        "description": "2024年水泥成品生產量（包含各種類型水泥）",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "74": {
        "name": "水泥成品單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "最近一年單位產品溫室氣體排放量（範疇一+範疇二）。永續經濟活動認定標準：≤0.87 公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "75": {
        "name": "替代原料使用比例",
        "description": "使用廢棄物、副產品等替代原料佔總原料使用量之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "76": {
        "name": "替代燃料使用比例",
        "description": "使用廢棄物衍生燃料等替代燃料佔總燃料使用量之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "77": {
        "name": "水泥窯協同處理廢棄物量",
        "description": "利用水泥窯協同處理廢棄物的年處理量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "78": {
        "name": "熟料／水泥比 (Clinker Factor)",
        "description": "水泥產品中熟料含量佔比，數值越低表示使用更多替代性膠凝材料",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "技術指標"
    },
    "79": {
        "name": "CCUS技術應用情形",
        "description": "是否應用碳捕捉、利用與封存技術，以及年碳捕捉量",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "技術採用"
    },
    "80": {
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
# 5. 玻璃產業專屬欄位 (81-90)
# ==========================================

GLASS_FIELDS = {
    "81": {
        "name": "主要玻璃產品類型",
        "description": "說明主要生產的玻璃產品類型：平板玻璃、板狀玻璃、浮法玻璃、或其他玻璃製品",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "82": {
        "name": "平板玻璃年產量",
        "description": "2024年平板玻璃（Flat Glass）總產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "83": {
        "name": "平板玻璃單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "單位產品GHG排放量。技術篩選標準：≤1.0121公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "84": {
        "name": "玻璃碎片（廢玻璃）使用比例",
        "description": "生產過程中使用回收玻璃碎片（Cullet）佔總原料投入之比例",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "85": {
        "name": "玻璃窯爐製程能源消耗量",
        "description": "單位產品能源消耗量（熔爐能源效率）",
        "data_format": "decimal",
        "unit": "GJ/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "能源效率"
    },
    "86": {
        "name": "窯爐類型與技術",
        "description": "說明採用的窯爐技術類型（如：浮法窯、電熔窯、純氧燃燒技術等）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "技術資訊"
    },
    "87": {
        "name": "替代燃料使用情形",
        "description": "是否使用替代燃料（如：生質能、廢棄物衍生燃料）及使用比例",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "88": {
        "name": "產品碳足跡驗證情形",
        "description": "是否取得產品碳足跡標籤或環保標章認證",
        "data_format": "boolean",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "產品認證"
    },
    "89": {
        "name": "製程NOx或SOx減量措施",
        "description": "空氣污染物減量技術採用情形（如：脫硝、脫硫設備）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "環境管理"
    },
    "90": {
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
# 6. 石油化學產業專屬欄位 (91-105)
# ==========================================

PETROCHEMICAL_FIELDS = {
    "91": {
        "name": "主要石化產品類型",
        "description": "列舉企業主要生產的石化產品類別（如：乙烯、丙烯、聚乙烯等）",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "92": {
        "name": "乙烯/丙烯/丁二烯年產量",
        "description": "若生產乙烯、丙烯或丁二烯，請填寫年產量（可列舉多項）",
        "data_format": "string",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "93": {
        "name": "乙烯/丙烯/丁二烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.9400公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "94": {
        "name": "苯乙烯年產量",
        "description": "若生產苯乙烯(Styrene)，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "95": {
        "name": "苯乙烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤1.0551公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "96": {
        "name": "氯乙烯年產量",
        "description": "若生產氯乙烯(Vinyl Chloride)，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "97": {
        "name": "氯乙烯單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.5026公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "98": {
        "name": "聚乙烯(PE)年產量",
        "description": "若生產聚乙烯，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "99": {
        "name": "聚乙烯(PE)單位溫室氣體排放量",
        "description": "技術篩選標準：≤1.0823公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "100": {
        "name": "聚丙烯(PP)年產量",
        "description": "若生產聚丙烯，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "101": {
        "name": "聚丙烯(PP)單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.4374公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "102": {
        "name": "聚氯乙烯(PVC)年產量",
        "description": "若生產PVC，請填寫年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "103": {
        "name": "聚氯乙烯(PVC)單位溫室氣體排放量",
        "description": "技術篩選標準：≤0.4544公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "104": {
        "name": "其他石化產品（乙二醇/酚/丙酮/丙烯腈）資訊",
        "description": "若生產乙二醇(≤2.0750)、酚/丙酮(≤0.8741)、丙烯腈(≤1.0570)，請說明產量與排放強度",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "環境",
        "category": "產品資訊"
    },
    "105": {
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
# 5. 鋼鐵產業專屬欄位 (106-115)
# ==========================================

STEEL_FIELDS = {
    "106": {
        "name": "鋼鐵生產製程類型",
        "description": "說明主要採用的製程類型：電弧爐(EAF)、一貫製程(高爐+煉鋼爐)、或其他製程",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "製程資訊"
    },
    "107": {
        "name": "鋼品類型",
        "description": "主要生產的鋼材類型：碳鋼、高合金鋼、或兩者兼有",
        "data_format": "string",
        "unit": "NA",
        "precision": "NA",
        "aspect": "營運",
        "category": "產品資訊"
    },
    "108": {
        "name": "粗鋼年產量",
        "description": "2024年粗鋼（crude steel）總產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "109": {
        "name": "電弧爐鋼品單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "若採用電弧爐製程，請填寫單位產品GHG排放量。技術篩選標準：高合金鋼≤0.620、碳鋼≤0.476公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "110": {
        "name": "廢鋼使用比例",
        "description": "廢鋼投入量佔總鋼鐵原料投入量之比例。技術篩選標準：高合金鋼≥70%、碳鋼≥90%",
        "data_format": "decimal",
        "unit": "百分比",
        "precision": "0.01",
        "aspect": "環境",
        "category": "循環經濟"
    },
    "111": {
        "name": "鐵水年產量",
        "description": "若採用一貫製程（高爐煉鐵），請填寫鐵水(hot metal/molten iron)年產量",
        "data_format": "decimal",
        "unit": "公噸",
        "precision": "0.0001",
        "aspect": "營運",
        "category": "產量"
    },
    "112": {
        "name": "鐵水單位溫室氣體排放量 (範疇一+範疇二)",
        "description": "若採用一貫製程，請填寫鐵水單位GHG排放量。技術篩選標準：≤1.443公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "113": {
        "name": "燒結礦單位溫室氣體排放量",
        "description": "若生產燒結礦，請填寫單位GHG排放量。技術篩選標準：≤0.242公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "114": {
        "name": "焦炭單位溫室氣體排放量",
        "description": "若生產焦炭（不包括褐煤焦炭），請填寫單位GHG排放量。技術篩選標準：≤0.237公噸CO2e/公噸",
        "data_format": "decimal",
        "unit": "公噸CO2e/公噸",
        "precision": "0.0001",
        "aspect": "環境",
        "category": "GHG強度"
    },
    "115": {
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
# 7. 紡織產業專屬欄位 (116-125)
# ==========================================

TEXTILE_FIELDS = {
    "116": {"name": "主要紡織製程類型", "description": "說明企業主要從事的製程：人造纖維製造、紡紗織布、染整、或多製程整合", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "117": {"name": "人造纖維產品類型與年產量", "description": "若生產人造纖維，請列舉產品類型（聚酯粒/短纖/長纖/加工絲、尼龍粒/長纖/加工絲）及年產量", "data_format": "string", "unit": "公噸", "precision": "NA", "aspect": "營運", "category": "產量"},
    "118": {"name": "人造纖維單位溫室氣體排放量", "description": "各產品類型單位GHG排放量（範疇一+範疇二）。技術標準：聚酯粒≤0.2275、聚酯短纖≤0.5661、聚酯長纖≤1.1020、聚酯加工絲≤0.8503、尼龍粒≤1.0425、尼龍長纖≤1.5420、尼龍加工絲≤0.7484", "data_format": "string", "unit": "公噸CO2e/公噸", "precision": "NA", "aspect": "環境", "category": "GHG強度"},
    "119": {"name": "紡紗織布年產量", "description": "若從事紡紗織布製程，請填寫年產量", "data_format": "decimal", "unit": "公噸", "precision": "0.0001", "aspect": "營運", "category": "產量"},
    "120": {"name": "紡紗織布單位溫室氣體排放量", "description": "技術篩選標準：≤2.2公噸CO2e/公噸", "data_format": "decimal", "unit": "公噸CO2e/公噸", "precision": "0.0001", "aspect": "環境", "category": "GHG強度"},
    "121": {"name": "染整加工年產量", "description": "若從事染整製程，請填寫年加工量", "data_format": "decimal", "unit": "公噸", "precision": "0.0001", "aspect": "營運", "category": "產量"},
    "122": {"name": "染整加工單位溫室氣體排放量", "description": "技術篩選標準：≤2.7公噸CO2e/公噸", "data_format": "decimal", "unit": "公噸CO2e/公噸", "precision": "0.0001", "aspect": "環境", "category": "GHG強度"},
    "123": {"name": "再生原料使用比例", "description": "使用回收材料或再生原料佔總原料投入之比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "124": {"name": "永續紡織認證取得情形", "description": "是否取得GRS（全球回收標準）、RCS（回收材料標準）或其他永續認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "125": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表8判斷：依製程類型對應相應GHG排放標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 8. 造紙產業專屬欄位 (126-135)
# ==========================================

PAPER_FIELDS = {
    "126": {"name": "主要紙類產品類型", "description": "列舉主要生產的紙類：漂白硫酸鹽漿、紙板、紙箱用紙(裱面紙板/瓦楞芯紙)、家庭用紙、印刷書寫用紙、特殊紙", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "127": {"name": "紙類年產量（氣乾噸Adt）", "description": "各類紙品年產量，以氣乾噸(Air Dry Ton, Adt)為單位", "data_format": "string", "unit": "Adt", "precision": "NA", "aspect": "營運", "category": "產量"},
    "128": {"name": "紙類產品單位溫室氣體排放量", "description": "各紙類GHG排放量（範疇一+範疇二）。技術標準：漂白硫酸鹽漿≤0.70、紙板≤0.90、裱面紙板≤0.90、瓦楞芯紙≤0.90、家庭用紙≤1.60、印刷書寫用紙≤0.90、特殊紙≤2.20 公噸CO2e/Adt", "data_format": "string", "unit": "公噸CO2e/Adt", "precision": "NA", "aspect": "環境", "category": "GHG強度"},
    "129": {"name": "單位產品能源消耗量", "description": "紙類生產能源消耗強度", "data_format": "decimal", "unit": "Mcal/Adt", "precision": "0.01", "aspect": "環境", "category": "能源效率"},
    "130": {"name": "廢紙回收使用比例", "description": "使用廢紙或再生原料佔總原料投入之比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "131": {"name": "事業廢棄物回收再利用率", "description": "製程產生的事業廢棄物回收再利用比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "循環經濟"},
    "132": {"name": "COD（化學需氧量）產生量", "description": "單位產品COD產生量或排放量", "data_format": "decimal", "unit": "公斤/Adt", "precision": "0.01", "aspect": "環境", "category": "水資源"},
    "133": {"name": "FSC/PEFC森林認證情形", "description": "是否取得FSC或PEFC等森林管理認證", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "134": {"name": "綠色產品或環保標章取得情形", "description": "產品是否取得環保標章或綠色產品認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "135": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表9判斷：各紙類產品GHG排放量是否符合對應閾值", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 9. 半導體產業專屬欄位 (136-145)
# ==========================================

SEMICONDUCTOR_FIELDS = {
    "136": {"name": "主要業務類型", "description": "IC製造（晶圓廠）或IC封裝測試", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "137": {"name": "晶圓尺寸與年產量", "description": "若為IC製造，請說明晶圓尺寸（6吋/8吋/12吋）及年產量（萬片約當8吋）", "data_format": "string", "unit": "萬片（約當8吋）", "precision": "NA", "aspect": "營運", "category": "產量"},
    "138": {"name": "製程節點技術", "description": "若為12吋晶圓，請說明主要製程節點（成熟製程≥10nm或先進製程<10nm）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "技術資訊"},
    "139": {"name": "IC製造單位面積溫室氣體排放量", "description": "晶圓單位面積GHG排放量（範疇一+範疇二）。技術標準：6吋以下≤2.18、8吋≤2.51、12吋成熟製程≤1.31、12吋先進製程≤9.58 公斤CO2e/平方公分", "data_format": "decimal", "unit": "公斤CO2e/平方公分", "precision": "0.01", "aspect": "環境", "category": "GHG強度"},
    "140": {"name": "IC封測年產量", "description": "若為封測業務，請說明年封裝或測試產量", "data_format": "string", "unit": "千個", "precision": "NA", "aspect": "營運", "category": "產量"},
    "141": {"name": "IC封測單位產品用電量", "description": "封測製程單位產品用電量。技術標準：導線架≤55、BGA≤22、FlipChip≤230、Bumping≤85、測試≤12 kWh/千個", "data_format": "string", "unit": "kWh/千個", "precision": "NA", "aspect": "環境", "category": "能源效率"},
    "142": {"name": "PFC（全氟化物）減排措施", "description": "針對含氟溫室氣體的減量技術或設備使用情形", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "技術採用"},
    "143": {"name": "製程用水回收率", "description": "製程用水回收再利用比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "水資源"},
    "144": {"name": "綠色製造或責任商業聯盟(RBA)認證", "description": "是否取得RBA、ISO 14001或其他綠色製造相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "145": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表10判斷：依晶圓尺寸/製程節點或封測類型對應標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 10. 平面顯示器面板產業專屬欄位 (146-155)
# ==========================================

DISPLAY_PANEL_FIELDS = {
    "146": {"name": "面板技術類型", "description": "主要生產的面板技術：LCD、OLED、或其他", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "147": {"name": "面板世代與產線規格", "description": "說明主要產線的面板世代（如G3.5、G4、G6、G8.5等）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "製程資訊"},
    "148": {"name": "年基板投入面積", "description": "2024年基板投入總面積", "data_format": "decimal", "unit": "平方公尺", "precision": "0.01", "aspect": "營運", "category": "產量"},
    "149": {"name": "單位基板溫室氣體排放量（範疇一+範疇二）", "description": "技術標準（選項1-排放量）：3.5代以下≤0.600、4代以上≤0.150 公噸CO2e/平方公尺", "data_format": "decimal", "unit": "公噸CO2e/平方公尺", "precision": "0.001", "aspect": "環境", "category": "GHG強度"},
    "150": {"name": "單位基板能源消耗量", "description": "技術標準（選項2-能源）：3.5代以下≤600、4代以上≤120 kWh/平方公尺", "data_format": "decimal", "unit": "kWh/平方公尺", "precision": "0.01", "aspect": "環境", "category": "能源效率"},
    "151": {"name": "顯示器能效等級或認證", "description": "產品能效等級（如Energy Star）或相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "152": {"name": "含氟溫室氣體減量措施", "description": "製程使用SF6、NF3等氣體的減量或處理技術", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "技術採用"},
    "153": {"name": "製程廢液回收處理率", "description": "製程產生的化學廢液回收處理比例", "data_format": "decimal", "unit": "百分比", "precision": "0.01", "aspect": "環境", "category": "環境管理"},
    "154": {"name": "綠色產品或環境標章取得情形", "description": "產品是否取得環保標章或綠色產品相關認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "155": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表11判斷：依面板世代選擇排放量或能源消耗量標準", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
}

# ==========================================
# 11. 電腦及週邊設備產業專屬欄位 (156-165)
# ==========================================

COMPUTER_EQUIPMENT_FIELDS = {
    "156": {"name": "主要產品類型", "description": "列舉主要生產的電腦及週邊設備（如：桌上型電腦、筆記型電腦、伺服器、顯示器、印表機等）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "營運", "category": "產品資訊"},
    "157": {"name": "EPEAT標章取得情形", "description": "產品是否取得EPEAT（電子產品環境評估工具）標章及等級（金牌/銀牌/銅牌）", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "158": {"name": "Energy Star或節能標章取得情形", "description": "產品是否取得Energy Star或台灣節能標章認證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "159": {"name": "ISO 14024第一類環保標章取得情形", "description": "產品是否取得經ISO 14024認定的第一類環保標章", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "160": {"name": "ISO 14021第二類環境宣告情形", "description": "是否依ISO 14021規範自行宣告環境訴求，並經第三方查驗證", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "161": {"name": "產品能源效率等級", "description": "產品能源效率分級或耗電量資訊", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "能源效率"},
    "162": {"name": "產品碳足跡標籤取得情形", "description": "產品是否取得碳足跡標籤或產品碳足跡認證", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "產品認證"},
    "163": {"name": "產品可回收設計或循環經濟措施", "description": "產品設計是否考慮易拆解、模組化、使用再生材料等循環經濟原則", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "環境", "category": "循環經濟"},
    "164": {"name": "產品維修服務或延長保固措施", "description": "是否提供延長保固、維修服務或升級方案以延長產品生命週期", "data_format": "string", "unit": "NA", "precision": "NA", "aspect": "社會", "category": "產品責任"},
    "165": {"name": "是否符合永續經濟活動技術篩選標準", "description": "根據附表12判斷：產品是否取得EPEAT、ISO 14024環保標章、Energy Star/節能標章、或ISO 14021第三方查驗證的環境宣告（任一項即可）", "data_format": "boolean", "unit": "NA", "precision": "NA", "aspect": "合規性", "category": "永續經濟活動"}
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


def get_final_fields(company_industry: str) -> Dict:
    """
    根據產業別合併基礎欄位與特定欄位 (Enhanced version)
    """
    # 1. Base fields (universal)
    final_fields = BASE_FIELDS.copy()

    # 2. Scope 3 fields (universal)
    final_fields.update(SCOPE3_FIELDS)

    # 3. Classify industry
    industry_category = classify_industry(company_industry)

    # 4. Add industry-specific fields
    if industry_category == "金融":
        final_fields.update(FINANCE_FIELDS)
        print(f"偵測到金融產業：{company_industry}，載入金融業專屬欄位（欄位57-60）。")

    elif industry_category in ["水泥", "玻璃", "石油化學", "鋼鐵", "紡織",
                                "造紙", "半導體", "平面顯示器", "電腦設備"]:
        # Add common manufacturing fields
        final_fields.update(MANUFACTURING_COMMON_FIELDS)

        # Add specific industry fields
        industry_info = INDUSTRY_CLASSIFICATIONS[industry_category]
        field_module_name = f"{industry_info['field_module']}_FIELDS"
        field_module = globals()[field_module_name]
        final_fields.update(field_module)

        print(f"偵測到{industry_category}產業：{company_industry}")
        print(f"載入製造業共通欄位（欄位61-70）+ {industry_category}專屬欄位（欄位{industry_info['field_range'][0]}-{industry_info['field_range'][1]}）")
        print(f"參考：永續經濟活動認定參考指引 {industry_info['附表編號']}")

    else:
        # General manufacturing - only common fields
        final_fields.update(MANUFACTURING_COMMON_FIELDS)
        print(f"偵測到一般製造產業：{company_industry}，載入製造業共通欄位（欄位61-70）。")

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



