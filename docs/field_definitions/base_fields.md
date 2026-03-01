# 基礎欄位 (Base Fields) — 欄位 1-72

> Source: `src/field_definitions.py` → `BASE_FIELDS_V2`
> Applicable to: All companies (universal)

These fields apply to every company regardless of industry. They are organized into 13 category sections as defined in the source code.

---

## Table of Contents

- [氣候承諾 (Fields 1–8)](#氣候承諾-fields-18)
- [碳排放 (Fields 9–30)](#碳排放-fields-930)
- [資料透明度 (Fields 31–33)](#資料透明度-fields-3133)
- [能源 (Fields 34–38)](#能源-fields-3438)
- [燃煤 (Fields 39–41)](#燃煤-fields-3941)
- [用電 (Fields 42–43)](#用電-fields-4243)
- [再生能源 (Fields 44–47)](#再生能源-fields-4447)
- [氣候行動 (Fields 48–55)](#氣候行動-fields-4855)
- [資料透明度-低碳產品 (Fields 56–57)](#資料透明度-低碳產品-fields-5657)
- [勞動 (Fields 58–62)](#勞動-fields-5862)
- [治理 (Field 63)](#治理-field-63)
- [勞動延伸 (Fields 64–65)](#勞動延伸-fields-6465)
- [水資源 (Fields 66–72)](#水資源-fields-6672)

---

## 氣候承諾 (Fields 1–8)

### 欄位 1: 是否承諾淨零排放／碳中和

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 若有淨零/碳中和承諾，請節錄關鍵句（50字以內），包含目標年份。若無明確承諾，填「無承諾」。

---

### 欄位 2: 預計達成淨零排放／碳中和年份

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 請只填入西元年份，若沒有明確承諾，請留空。若原始資料為民國年份，請協助轉換。

---

### 欄位 3: 是否設定中期溫室氣體絕對減量目標

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 企業是否設定了在達到淨零前的中期減量檢核點？

---

### 欄位 4: 中期減量目標年設定

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 請只填入年份，若沒有明確設定，請留空。若有多個目標年，填最近的目標年，並在補充說明中敘明所有目標年。

---

### 欄位 5: 中期溫室氣體絕對減量目標值（百分比）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 氣候承諾 |

**Description:** 若僅有「單位產品碳排放係數降低」或「特定廠減排目標」，請留空。以小數表示（如30%填0.3）。

---

### 欄位 6: 中期減量基準年設定

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 中期目標對應的基準年西元年份。若未提供明確基準年，則留空。

---

### 欄位 7: 中期減量基準年排放量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 氣候承諾 |

**Description:** 中期目標的基準年碳排放量。若未提供明確基準年數據，則留空。

---

### 欄位 8: 中期目標是否取得SBT認證

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候承諾 |

**Description:** 中期減量目標是否取得科學基礎減量目標認證（SBT/SBTi）。

---

## 碳排放 (Fields 9–30)

### 欄位 9: 範疇一/類別一（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** 溫室氣體排放量中，範疇一（直接排放）的值。若公司有加總值，請填寫總額，不含海外廠。若沒有2024年資料，請於補充說明註記。

---

### 欄位 10: 範疇二/類別二（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** 溫室氣體排放量中，範疇二（間接排放/外購電力）的值。若公司有加總值，請填寫總額，不含海外廠。

---

### 欄位 11: 範疇三（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** 溫室氣體排放量中，範疇三（其他間接排放）的總值。若公司給的是類別三到六或類別三到十五，請協助加總。

---

### 欄位 12: 類別三（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** ISO/CNS 14064-1類別三（運輸的間接溫室氣體排放）的值。

---

### 欄位 13: 類別四（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** ISO/CNS 14064-1類別四（組織使用的產品所產生的間接溫室氣體排放）的值。

---

### 欄位 14: 類別五（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** ISO/CNS 14064-1類別五（與組織產品使用相關聯的間接溫室氣體排放）的值。

---

### 欄位 15: 類別六（值）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** ISO/CNS 14064-1類別六（由其他來源產生的間接溫室氣體排放）的值。

---

### 欄位 16: Scope 3 類別 1 (購買商品或服務)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別1。

---

### 欄位 17: Scope 3 類別 2 (資本商品)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別2。

---

### 欄位 18: Scope 3 類別 3 (燃料與能源相關活動)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別3（非範疇一二之排放）。

---

### 欄位 19: Scope 3 類別 4 (上游運輸和配送)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別4。

---

### 欄位 20: Scope 3 類別 5 (營運廢棄物)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別5。

---

### 欄位 21: Scope 3 類別 6 (商務旅行)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別6。

---

### 欄位 22: Scope 3 類別 7 (員工通勤)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別7。

---

### 欄位 23: Scope 3 類別 8 (上游租賃資產)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別8。

---

### 欄位 24: Scope 3 類別 9 (下游運輸和配送)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別9。

---

### 欄位 25: Scope 3 類別 10 (銷售產品的加工)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別10。

---

### 欄位 26: Scope 3 類別 11 (使用銷售產品)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別11。

---

### 欄位 27: Scope 3 類別 12 (銷售產品廢棄處理)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別12。

---

### 欄位 28: Scope 3 類別 13 (下游租賃資產)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別13。

---

### 欄位 29: Scope 3 類別 14 (特許經營)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別14。

---

### 欄位 30: Scope 3 類別 15 (投資)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 公噸CO2e |
| Precision | 0.0001 |
| Category | 碳排放 |

**Description:** GHG Protocol 範疇三類別15。金融業請特別注意，通常為投融資組合排放。

---

## 資料透明度 (Fields 31–33)

### 欄位 31: 是否揭露近三年溫室氣體排放資料

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 資料透明度 |

**Description:** 企業是否有逐年揭露溫室氣體排放狀況（2022-2024年）。通常可於最後附錄查詢。

---

### 欄位 32: 是否設定範疇三減量目標

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 資料透明度 |

**Description:** 判斷公司是否針對範疇三（Scope 3）設定減量目標或規劃。

---

### 欄位 33: 範疇三減量目標實際作為

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 資料透明度 |

**Description:** 範疇三的具體減碳作為（限3項）。格式：「作為1、作為2、作為3」。若無具體作為或僅有宣示性文字，留空。

---

## 能源 (Fields 34–38)

### 欄位 34: 2024年度總能源使用量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | MJ |
| Precision | 0.0001 |
| Category | 能源 |

**Description:** 通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。

---

### 欄位 35: 2023年度總能源使用量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | MJ |
| Precision | 0.0001 |
| Category | 能源 |

**Description:** 通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。

---

### 欄位 36: 2022年度總能源使用量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | MJ |
| Precision | 0.0001 |
| Category | 能源 |

**Description:** 通常以熱量（GJ或MJ）為單位，計算時不需排除電力使用。通常可於最後面的附錄查詢得到。

---

### 欄位 37: 是否揭露各項能源使用細項

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 能源 |

**Description:** 是否揭露2024年使用的各種能源細項。

---

### 欄位 38: 2024年度使用的各種能源項目

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 依報告書原始格式 |
| Precision | NA |
| Category | 能源 |

**Description:** 列出各能源使用量。格式：「能源: 數值 單位; 」。排序：電力>天然氣>柴油>汽油>其他。

---

## 燃煤 (Fields 39–41)

### 欄位 39: 燃煤使用量

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | 依報告書原始格式 |
| Precision | NA |
| Category | 燃煤 |

**Description:** 報告年度的燃煤使用量。燃煤包含煙煤、無煙煤、褐煤等。若公司不使用燃煤請填「0」或「不適用」。

---

### 欄位 40: 燃煤淘汰計劃

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 燃煤 |

**Description:** 公司是否有燃煤淘汰或減量計劃？若有，請說明目標年份與減量目標。若不使用燃煤請填「不適用」。

---

### 欄位 41: 化石燃料轉型計劃

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 燃煤 |

**Description:** 公司是否有化石燃料整體轉型計劃？請說明轉型目標與時程。化石燃料包含煤炭、天然氣、石油。若無相關計劃請填「無」。

---

## 用電 (Fields 42–43)

### 欄位 42: 當年度總用電量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 度（KWh） |
| Precision | 0.0001 |
| Category | 能源 |

**Description:** 只看該公司使用電力或外購電力的數值，自行使用再生能源發電不計入。以報告書原記錄單位為主。

---

### 欄位 43: 再生能源使用佔總發電量（百分比）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 能源 |

**Description:** 透過利用再生能源所產生之發電量，佔總發電量的比例。以小數表示。

---

## 再生能源 (Fields 44–47)

### 欄位 44: 再生能源裝置容量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 瓩（KW） |
| Precision | 0.001 |
| Category | 再生能源 |

**Description:** 僅收公司自行建置的再生能源（太陽光電、風電、地熱等）。只收確定建置完成的容量，不收規劃數值。

---

### 欄位 45: 再生能源使用來源（自發自用、購電協議、再生能源憑證）

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 再生能源 |

**Description:** 公司使用的再生能源來源是什麼？

---

### 欄位 46: 是否達成政府用電大戶再生能源建置義務

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 再生能源 |

**Description:** 如果有達到，通常會寫「已達到/遠高於政府用電大戶條款所規定的10%」。

---

### 欄位 47: 是否取得RE100認證

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 再生能源 |

**Description:** 請判斷企業之再生能源目標，是否取得RE100目標認證。

---

## 氣候行動 (Fields 48–55)

### 欄位 48: 是否設定再生能源使用目標

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 是否設定要於何時達到再生能源使用率幾%。

---

### 欄位 49: 再生能源目標年設定

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 請只填入目標年份（西元年）。若未提及或目標年為2050，請留空。

---

### 欄位 50: 再生能源目標值（百分比）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 氣候行動 |

**Description:** 請填入目標值的數字，可包含小數點。以小數表示。

---

### 欄位 51: 是否設定節能目標

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 節能、節電等皆可算入。僅處理明確寫出節能目標設定的內容。

---

### 欄位 52: 節能目標年設定

| Property | Value |
|----------|-------|
| Data Format | integer |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 請只填入年份，若沒有明確承諾，請留空。

---

### 欄位 53: 節能目標值（百分比）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 氣候行動 |

**Description:** 請填入目標值的數字，可包含小數點。如30%則填0.3。

---

### 欄位 54: 節電目標值設定（百分比）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 氣候行動 |

**Description:** 請填入公司設定的節電目標值（以小數表示，例如2%請填0.02）。

---

### 欄位 55: 是否說明關鍵減量策略

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 氣候行動 |

**Description:** 列舉公司主要減碳策略（限5項）。格式：「策略1、策略2、策略3」。每項4-8字名詞短語。

---

## 資料透明度-低碳產品 (Fields 56–57)

### 欄位 56: 是否生產支持轉型至低碳經濟之產品/服務

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 資料透明度 |

**Description:** 公司是否說明有生產或進行低碳經濟相關的產品或服務內容。

---

### 欄位 57: 支持轉型至低碳經濟之產品/服務產生的營收或營收占比

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 元 |
| Precision | 0.0001 |
| Category | 資料透明度 |

**Description:** 揭露公司2024年低碳產品/服務之收入佔總營收之比例。公司須說明該低碳產品與服務之定義。

---

## 勞動 (Fields 58–62)

### 欄位 58: 失能傷害頻率(LTIFR)

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | NA |
| Precision | 0.0001 |
| Category | 職災 |

**Description:** 報告年度的失能傷害頻率(Lost Time Injury Frequency Rate)。請提供整體數值。

---

### 欄位 59: 職業傷害件數

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職災 |

**Description:** 報告年度發生的職業傷害總件數。格式：死亡X件、永久失能X件、暫時失能X件。

---

### 欄位 60: 損失工作日數

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職災 |

**Description:** 報告年度因職業傷害造成的損失工作日數(Lost Days)。此數值通常出現在職業安全統計表格中。

---

### 欄位 61: 重大職業安全意外事件

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 工安 |

**Description:** 報告年度是否有發生重大職業安全意外事件？重大事件包含：造成死亡、永久失能、多人受傷之事故，以及火災、爆炸等工安事故。若有發生，請填入傷亡人數與說明文字（如：死亡1人，因鍋爐爆炸事故）；若無請填「無」。

---

### 欄位 62: 勞動法規違規與裁罰

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 勞動裁罰 |

**Description:** 報告年度是否有違反勞動法規？若有請列出違規內容與裁罰金額。若無請填「無」。

---

## 治理 (Field 63)

### 欄位 63: 政府補貼或獎勵

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 補貼 |

**Description:** 報告年度是否接受政府補貼或獎勵計劃？若有請說明計劃名稱與金額。若無請填「無」或「未揭露」。

---

## 勞動延伸 (Fields 64–65)

### 欄位 64: 受傷、死亡比率

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職災 |

**Description:** 報告年度的職業傷害率(IR)與死亡率(FR)。傷害率計算公式：(傷害件數 × 200,000) / 總工時。死亡率計算公式：(死亡人數 × 200,000) / 總工時。格式範例：傷害率0.5、死亡率0。若報告書未揭露請留空。

---

### 欄位 65: 職業病

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 職災 |

**Description:** 該公司當年度是否發生職業病？若有，請填入人數與說明文字（如：3人，塵肺症）。職業病包含：職業性癌症、呼吸系統疾病、皮膚病、聽力損失、肌肉骨骼疾病等經認定之職業病。若無請填「無」。

---

## 水資源 (Fields 66–72)

### 欄位 66: 取水量-自來水

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司用水量中，取自自來水廠的水（如自來水、水庫水等）。若公司僅寫總用水量，請留空。

---

### 欄位 67: 取水量-地表水

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司用水量中，取自自然河川的水（如溪流、攔河堰等）。若公司僅寫總用水量，請留空。

---

### 欄位 68: 取水量-地下水

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司用水量中，取自地下水的水。若公司僅寫總用水量，請留空。

---

### 欄位 69: 取水量-其他來源（海水、冷凝水、雨水、再生水）

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司用水量中，取自其他來源的水（如海水淡化、雨水等）。若公司僅寫總用水量，請留空。

---

### 欄位 70: 回收水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司在生產過程中回收的水資源。通常回收水量會比取水量高，因為一滴水會被重複利用。

---

### 欄位 71: 排放水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 公司在生產過程最後排放掉的廢污水（廢水、排放水、放流水同概念）。

---

### 欄位 72: 耗用水量

| Property | Value |
|----------|-------|
| Data Format | decimal |
| Unit | 噸 |
| Precision | 0.0001 |
| Category | 水資源 |

**Description:** 生產過程中消耗掉，沒有回到自然界的水。若報告書有明確揭露耗用水量請填入，若無明確資料請留空，無須協助公司計算。
