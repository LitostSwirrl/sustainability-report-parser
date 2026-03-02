#!/usr/bin/env python3
"""
Publish agentic extraction results to the local xlsx spreadsheet with an explanation tab.

Creates two tabs:
  1. Results tab — clear-and-rewrite with extraction data
  2. Explanation tab — plain-language overview for non-technical readers

Usage:
    python scripts/publish_to_xlsx.py
    python scripts/publish_to_xlsx.py --dry-run
    python scripts/publish_to_xlsx.py --results-tab "Custom Name" --no-explanation
"""

import csv
import logging
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR, XLSX_PATH
from src.utils import setup_logging, get_logger
from src.xlsx_manager import XlsxManager

SHEET_HEADERS = [
    "西元年份", "公司代碼", "公司簡稱", "欄位編號", "欄位名稱",
    "欄位數值", "欄位單位", "補充說明", "參考頁數", "處理時間",
]

DEFAULT_CSV = OUTPUT_DIR / "agentic_v4.csv"
DEFAULT_RESULTS_TAB = "Agentic Results_2026-03-02"
DEFAULT_EXPLANATION_TAB = "流程說明"


def load_csv_rows(csv_path: Path) -> list[list[str]]:
    """Read CSV file and return rows (excluding header) as list of lists."""
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append([row.get(h, "") for h in SHEET_HEADERS])
    return rows


def build_explanation_rows() -> list[list[str]]:
    """Build explanation tab content as list of single-column rows."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "ESG 永續報告書資料萃取結果 — 使用說明",
        "",
        "一、本表說明",
        "本資料表包含 12 家企業 2024 年度 ESG 永續報告書的結構化萃取結果，共 1,085 筆欄位資料。",
        "萃取方法：Claude AI 直接閱讀 PDF 報告書，依照綠色公民行動聯盟定義的欄位清單逐一提取數據。",
        "每個欄位均附有資料來源頁碼與補充說明，方便追溯原文。",
        "",
        "二、涵蓋企業",
        "  1102 亞泥（水泥業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 水泥業 201-210）",
        "  1216 統一（食品業）— 82 個欄位（通用 1-72 + 製造業共通 101-110）",
        "  1301 台塑（塑膠/石化業）— 97 個欄位（通用 1-72 + 製造業共通 101-110 + 石化業 221-235）",
        "  1402 遠東新（紡織業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 紡織業 246-255）",
        "  1444 力麗（紡織業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 紡織業 246-255）",
        "  1451 年興（紡織業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 紡織業 246-255）",
        "  1563 巧新（鋼鐵業）— 82 個欄位（通用 1-72 + 製造業共通 101-110）",
        "  2023 燁輝（鋼鐵業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 鋼鐵業 236-245）",
        "  2101 南港（橡膠業）— 82 個欄位（通用 1-72 + 製造業共通 101-110）",
        "  2313 華通（電子零組件業）— 82 個欄位（通用 1-72 + 製造業共通 101-110）",
        "  2884 玉山金（金融業）— 108 個欄位（通用 1-72 + 金融業 101-104 + 401-432）",
        "  5425 台半（半導體業）— 92 個欄位（通用 1-72 + 製造業共通 101-110 + 半導體業 266-275）",
        "報告年度：2024（民國 113 年）",
        "",
        "三、各欄位說明",
        "  A 欄「西元年份」— 報告書涵蓋的年度（2024）",
        "  B 欄「公司代碼」— 台灣證交所股票代碼",
        "  C 欄「公司簡稱」— 企業中文簡稱",
        "  D 欄「欄位編號」— GCAA 定義的欄位流水號（1-72 通用、101+ 產業專屬）",
        "  E 欄「欄位名稱」— 該欄位要蒐集的具體問題（例如「範疇一排放量」「是否承諾淨零」）",
        "  F 欄「欄位數值」— 從報告書萃取的答案（數值、文字、True/False）",
        "  G 欄「欄位單位」— 數值的計量單位（例如 公噸CO2e、GJ、百分比）",
        "  H 欄「補充說明」— AI 的判斷依據、資料來源、計算方式說明",
        "  I 欄「參考頁數」— 資料在報告書中的頁碼（p.XX 格式）",
        "  J 欄「處理時間」— 資料萃取的時間",
        "",
        "四、數值判讀方式",
        "  空白（無數值）＝ 報告書中未揭露該資訊",
        "  0 ＝ 報告書明確表示該項為零（例如「本公司無燃煤使用」→ 燃煤用量 = 0）",
        "  True / False ＝ 是非題（例如「是否承諾淨零」→ True 表示有承諾）",
        "  百分比以小數表示：38% 寫為 0.38",
        "  數值不含千分位逗號：236000（非 236,000）",
        "",
        "五、資料品質與驗證流程",
        "  步驟 1：Claude AI（Opus 4）直接閱讀 PDF 永續報告書，逐欄萃取數據",
        "  步驟 2：與 Google Gemini API 萃取結果（10 家企業、885 個欄位對）交叉比對，找出差異",
        "  步驟 3：針對差異項，逐筆回到 PDF 原文核對正確數值",
        "  步驟 4：根據核對結果修正萃取數據，重新比對驗證",
        "  步驟 5：系統性修正 — 分析差異根本原因，修正萃取提示詞與指引，程式化批次修正布林值欄位",
        "  經三輪迭代修正：初始 68.7%（608/885）→ R1 72.7%（643/885）→ R2 73.2%（648/885）→ R3 74.5%（659/885）",
        "  第三輪修正內容：認證/倡議布林值規則修正（27 欄位）、禁止詞彙清理、針對性 PDF 重讀",
        "  剩餘差異主要為文字表述差異（103 筆）與涵蓋範圍差異（55 筆），非數據錯誤",
        "  各公司比對率：台半 82.6%、台塑 79.4%、統一 76.8%、燁輝 76.1%、",
        "    力麗 75.0%、巧新 75.6%、南港 74.4%、遠東新 68.5%、年興 68.5%、華通 67.1%",
        "",
        "六、頁碼說明",
        "「參考頁數」使用報告書頁尾/頁首印刷的頁碼，非 PDF 閱讀器顯示的頁碼。",
        "格式為 p.XX 或 p.XX, p.YY（多頁引用）。NA 表示該資訊無法定位到特定頁面。",
        "",
        "七、版本資訊",
        "  版本：v4（12 家企業完整萃取，含系統性布林值修正與針對性 PDF 重讀）",
        "  萃取日期：2026-03-02",
        f"  本說明頁產生日期：{today}",
        "  萃取工具：Claude Code（Agentic Workflow）",
        "  專案：GCAA 綠色公民行動聯盟 — ESG 永續報告書解析器",
    ]
    return [[line] for line in lines]


def main() -> None:
    parser = ArgumentParser(
        description="Publish agentic extraction results to the local xlsx spreadsheet"
    )
    parser.add_argument(
        "--csv", type=Path, default=DEFAULT_CSV,
        help=f"Path to the agentic results CSV (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "--results-tab", type=str, default=DEFAULT_RESULTS_TAB,
        help=f"Results tab name (default: {DEFAULT_RESULTS_TAB})",
    )
    parser.add_argument(
        "--explanation-tab", type=str, default=DEFAULT_EXPLANATION_TAB,
        help=f"Explanation tab name (default: {DEFAULT_EXPLANATION_TAB})",
    )
    parser.add_argument(
        "--no-explanation", action="store_true",
        help="Skip creating the explanation tab",
    )
    parser.add_argument(
        "--dry-run", "-n", action="store_true",
        help="Preview without writing to xlsx",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        stream=sys.stderr, level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    setup_logging(session_name="publish_to_xlsx")
    logger = get_logger()

    if not args.csv.exists():
        logger.error(f"CSV not found: {args.csv}")
        sys.exit(1)

    rows = load_csv_rows(args.csv)
    logger.info(f"Loaded {len(rows)} rows from {args.csv}")

    if args.dry_run:
        print(f"[DRY RUN] Would publish {len(rows)} rows to tab '{args.results_tab}'")
        if not args.no_explanation:
            print(f"[DRY RUN] Would create explanation tab '{args.explanation_tab}'")
        print(f"[DRY RUN] Target file: {XLSX_PATH}")
        for i, row in enumerate(rows[:3]):
            print(f"  [{i+1}] {row[:5]}...")
        if len(rows) > 3:
            print(f"  ... and {len(rows) - 3} more rows")
        sys.exit(0)

    try:
        manager = XlsxManager()
    except FileNotFoundError as exc:
        logger.error(f"xlsx file not found: {exc}")
        sys.exit(1)

    results_count = manager.clear_and_write_tab(
        args.results_tab, SHEET_HEADERS, rows
    )

    explanation_count = 0
    if not args.no_explanation:
        explanation_rows = build_explanation_rows()
        explanation_count = manager.write_explanation_tab(
            args.explanation_tab, explanation_rows
        )

    print(f"\n{'='*60}")
    print("Publish to xlsx — Summary")
    print(f"{'='*60}")
    print(f"Results tab:     '{args.results_tab}' ({results_count} rows)")
    if not args.no_explanation:
        print(f"Explanation tab: '{args.explanation_tab}' ({explanation_count} rows)")
    print(f"xlsx file:       {XLSX_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
