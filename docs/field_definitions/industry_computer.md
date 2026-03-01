# 電腦及週邊設備產業欄位 (Computer Equipment Industry) — 欄位 286-295

> Source: `src/field_definitions.py` → `COMPUTER_EQUIPMENT_FIELDS`
> Applicable to: Computer and peripheral equipment companies (電腦及週邊設備業), including desktop/laptop/server/display/printer manufacturers. Appended after base fields and manufacturing common fields. Reference standard: 附表12 — 永續經濟活動認定參考指引. The screening standard for this industry is certification-based rather than emissions-intensity based: holding any one qualifying product certification is sufficient to meet the technical screening threshold (欄位 295).

---

### 欄位 286: 主要產品類型

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品資訊 |

**Description:** 列舉主要生產的電腦及週邊設備（如：桌上型電腦、筆記型電腦、伺服器、顯示器、印表機等）。

---

### 欄位 287: EPEAT標章取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得EPEAT（電子產品環境評估工具）標章及等級（金牌/銀牌/銅牌）。

---

### 欄位 288: Energy Star或節能標章取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得Energy Star或台灣節能標章認證。

---

### 欄位 289: ISO 14024第一類環保標章取得情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得經ISO 14024認定的第一類環保標章。

---

### 欄位 290: ISO 14021第二類環境宣告情形

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 是否依ISO 14021規範自行宣告環境訴求，並經第三方查驗證。

---

### 欄位 291: 產品能源效率等級

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 能源效率 |

**Description:** 產品能源效率分級或耗電量資訊。

---

### 欄位 292: 產品碳足跡標籤取得情形

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 產品認證 |

**Description:** 產品是否取得碳足跡標籤或產品碳足跡認證。

---

### 欄位 293: 產品可回收設計或循環經濟措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 循環經濟 |

**Description:** 產品設計是否考慮易拆解、模組化、使用再生材料等循環經濟原則。

---

### 欄位 294: 產品維修服務或延長保固措施

| Property | Value |
|----------|-------|
| Data Format | string |
| Unit | NA |
| Precision | NA |
| Category | 產品責任 |

**Description:** 是否提供延長保固、維修服務或升級方案以延長產品生命週期。

---

### 欄位 295: 是否符合永續經濟活動技術篩選標準

| Property | Value |
|----------|-------|
| Data Format | boolean |
| Unit | NA |
| Precision | NA |
| Category | 永續經濟活動 |

**Description:** 根據附表12判斷：產品是否取得以下任一項認證即視為符合標準——

**技術篩選標準 (附表12) — 符合任一即可:**
1. EPEAT（電子產品環境評估工具）標章
2. ISO 14024 第一類環保標章
3. Energy Star 或台灣節能標章
4. ISO 14021 第三方查驗證的第二類環境宣告
