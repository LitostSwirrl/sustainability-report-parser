#!/usr/bin/env python3
"""
Compare extraction results across multiple runs.

Loads validation results and calculates consistency metrics for each field.
Generates a comparison report for filling 檢查欄 (columns K:O).

Usage:
    python scripts/compare_results.py
    python scripts/compare_results.py --company 1216
"""

import sys
import json
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.utils import setup_logging, get_logger

# Validation target companies
VALIDATION_COMPANIES = [
    "1216", "1409", "1444", "1451", "1563",
    "2023", "2101", "2313", "5425", "6443"
]


def normalize_value(value: str) -> str:
    """
    Normalize a value for comparison.

    - Strip whitespace
    - Normalize empty values
    - Normalize booleans
    - Normalize numbers (remove trailing zeros)
    """
    if value is None:
        return ""

    value = str(value).strip()

    # Normalize empty values
    if value.lower() in ['', '無', '無資料', '無法填答', 'na', 'n/a', 'none', '-']:
        return ""

    # Normalize booleans
    if value.lower() in ['true', 'yes', '是']:
        return "True"
    if value.lower() in ['false', 'no', '否']:
        return "False"

    # Normalize numeric strings (remove trailing zeros for decimals)
    try:
        num = float(value)
        if num == int(num):
            return str(int(num))
        # Remove trailing zeros but keep reasonable precision
        return f"{num:.10f}".rstrip('0').rstrip('.')
    except ValueError:
        pass

    return value


def calculate_consistency(values: List[str]) -> Tuple[float, List[str], str]:
    """
    Calculate consistency metrics for a list of values.

    Args:
        values: List of extracted values (normalized)

    Returns:
        Tuple of (consistency_pct, unique_values, confidence_level)
    """
    if not values:
        return 0.0, [], "低"

    # Count occurrences
    counter = Counter(values)
    most_common_count = counter.most_common(1)[0][1]

    # Consistency percentage
    consistency_pct = (most_common_count / len(values)) * 100

    # Unique values (sorted by frequency)
    unique_values = [v for v, _ in counter.most_common()]

    # Confidence level
    if consistency_pct == 100:
        confidence = "高"
    elif consistency_pct >= 67:
        confidence = "中"
    else:
        confidence = "低"

    return consistency_pct, unique_values, confidence


def check_page_ref_consistency(page_refs: List[str]) -> Tuple[bool, str]:
    """
    Check if page references are consistent across runs.

    Returns:
        Tuple of (is_consistent, summary)
    """
    # Normalize page refs (strip, lowercase)
    normalized = [p.strip().lower() for p in page_refs if p.strip()]

    if not normalized:
        return True, "無頁碼"

    unique = set(normalized)

    if len(unique) == 1:
        return True, "✓"
    else:
        return False, "✗"


def values_are_equivalent(val1: str, val2: str) -> bool:
    """
    Check if two values are semantically equivalent.

    Handles:
    - Numeric values with different formats (1000 vs 1,000)
    - Boolean values (True vs true vs 是)
    - Empty values
    - Slight text variations
    """
    # Both empty
    if not val1 and not val2:
        return True

    # One empty, one not
    if not val1 or not val2:
        return False

    # Already equal
    if val1 == val2:
        return True

    # Try numeric comparison
    try:
        num1 = float(val1.replace(",", ""))
        num2 = float(val2.replace(",", ""))
        # Allow small tolerance for floating point
        if abs(num1 - num2) < 0.0001 or (num1 != 0 and abs(num1 - num2) / abs(num1) < 0.001):
            return True
    except (ValueError, ZeroDivisionError):
        pass

    # Check if one contains the other (for text summaries)
    if len(val1) > 20 and len(val2) > 20:
        # For long text, check significant overlap
        if val1 in val2 or val2 in val1:
            return True

    return False


def assess_correctness(
    original_value: str,
    most_common_value: str,
    all_values: List[str],
    unique_values: List[str],
    consistency_pct: float,
    field_name: str
) -> Tuple[str, str]:
    """
    Intelligently assess correctness based on comparison with original.

    Returns:
        Tuple of (correctness_percentage, assessment_explanation)
    """
    counter = Counter(all_values)
    total_runs = len(all_values)
    matching_original = sum(1 for v in all_values if values_are_equivalent(v, original_value))

    # Helper to truncate long values for display
    def truncate(val: str, max_len: int = 30) -> str:
        if not val:
            return "(空)"
        if len(val) > max_len:
            return val[:max_len] + "..."
        return val

    orig_display = truncate(original_value)
    common_display = truncate(most_common_value)

    # Case 1: All values match original
    if matching_original == total_runs:
        return "100%", f"6次提取結果完全一致：「{orig_display}」"

    # Case 2: Most common matches original
    if values_are_equivalent(original_value, most_common_value):
        match_count = counter.get(most_common_value, 0)
        non_match = [v for v in all_values if not values_are_equivalent(v, original_value)]
        non_match_display = truncate(non_match[0] if non_match else "", 20)

        if match_count >= 5:
            return "100%", f"{match_count}/6次與原始值「{orig_display}」一致，僅1次異常「{non_match_display}」"
        elif match_count >= 4:
            return "75%", f"{match_count}/6次與原始值一致。變異值：「{non_match_display}」。原始值可能正確"
        elif match_count >= 3:
            return "50%", f"{match_count}/6次一致但有{len(unique_values)}種不同值，需人工確認哪個正確"
        else:
            return "25%", f"僅{match_count}/6次與原始值一致，提取結果分歧大，正確性存疑"

    # Case 3: Original value is empty but runs found data
    if not original_value and most_common_value:
        most_common_count = counter.get(most_common_value, 0)
        if most_common_count >= 5:
            return "75%", f"原始未填值，但{most_common_count}/6次提取到「{common_display}」，可能是原始遺漏"
        elif most_common_count >= 3:
            return "50%", f"原始未填值，{most_common_count}/6次提取到值「{common_display}」，需確認報告書是否有此資料"
        else:
            return "25%", f"原始未填值，提取結果分散（{len(unique_values)}種不同值），無法判斷正確答案"

    # Case 4: Original has value but runs mostly empty
    if original_value and not most_common_value:
        empty_count = sum(1 for v in all_values if not v)
        non_empty = [v for v in all_values if v]
        if empty_count >= 4:
            if non_empty:
                return "25%", f"原始值「{orig_display}」，但{empty_count}/6次提取為空，可能報告書中難以定位此資料"
            else:
                return "25%", f"原始值「{orig_display}」，但6次重新提取皆為空，需檢查原始值來源"
        else:
            return "50%", f"原始值「{orig_display}」與多數提取結果不同，需人工核對報告書"

    # Case 5: Most common differs from original
    if most_common_value and original_value:
        most_common_count = counter.get(most_common_value, 0)
        if most_common_count >= 5:
            # Runs consistently disagree with original - runs might be more accurate
            return "50%", f"原始值「{orig_display}」與{most_common_count}/6次提取值「{common_display}」不同，多數結果可能更正確"
        elif most_common_count >= 3:
            return "25%", f"原始值「{orig_display}」與多數提取「{common_display}」不符，需核對報告書原文"
        else:
            return "0%", f"6次提取有{len(unique_values)}種不同結果，無法判斷「{orig_display}」或其他值哪個正確"

    # Default case
    if consistency_pct >= 80:
        return "75%", f"提取一致性高({consistency_pct:.0f}%)，值為「{common_display}」，但與原始值「{orig_display}」不同"
    elif consistency_pct >= 50:
        return "50%", f"提取一致性中等({consistency_pct:.0f}%)，有{len(unique_values)}種不同結果，需人工判斷"
    else:
        return "0%", f"提取結果分散（一致性{consistency_pct:.0f}%，{len(unique_values)}種值），無法可靠評估正確性"


def load_validation_results(validation_dir: Path, company_code: str) -> Dict:
    """
    Load all validation results for a company.

    Returns:
        Dict with structure:
        {
            'original': {...},
            'run_1': {...},
            'run_2': {...},
            ...
        }
    """
    logger = get_logger()
    results = {}

    # Load original (cache format uses 'analysis_results')
    original_dir = validation_dir / "original"
    for f in original_dir.glob(f"{company_code}_*.json"):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Normalize key: cache uses 'analysis_results', validation uses 'results'
            if 'analysis_results' in data:
                data['results'] = data.pop('analysis_results')
            results['original'] = data
        break

    # Load each run
    for run_num in range(1, 6):
        run_dir = validation_dir / f"run_{run_num}"
        for f in run_dir.glob(f"{company_code}_*.json"):
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Normalize key
                if 'analysis_results' in data:
                    data['results'] = data.pop('analysis_results')
                results[f'run_{run_num}'] = data
            break

    logger.info(f"Loaded {len(results)} result sets for {company_code}")
    return results


def compare_company_results(company_code: str, all_results: Dict) -> List[Dict]:
    """
    Compare results for a single company across all runs.

    Args:
        company_code: Company stock code
        all_results: Dict with original + run results

    Returns:
        List of comparison records (one per field)
    """
    logger = get_logger()
    comparisons = []

    # Get field list from original
    if 'original' not in all_results or not all_results['original'].get('results'):
        logger.warning(f"No original results for {company_code}")
        return comparisons

    # Build field map for each source
    sources = ['original', 'run_1', 'run_2', 'run_3', 'run_4', 'run_5']
    field_maps = {}

    for source in sources:
        if source not in all_results:
            continue
        source_results = all_results[source].get('results', [])
        field_maps[source] = {
            str(r.get('欄位編號', r.get('field_id', ''))): r
            for r in source_results
        }

    # Get all field IDs from original
    field_ids = list(field_maps.get('original', {}).keys())

    for field_id in sorted(field_ids, key=lambda x: int(x) if x.isdigit() else 0):
        # Collect values from all sources
        values = []
        page_refs = []
        raw_values = {}

        for source in sources:
            if source in field_maps and field_id in field_maps[source]:
                field_data = field_maps[source][field_id]
                value = field_data.get('欄位數值', '')
                values.append(normalize_value(value))
                page_refs.append(field_data.get('參考頁數', ''))
                raw_values[source] = value

        # Calculate metrics
        consistency_pct, unique_values, confidence = calculate_consistency(values)
        page_consistent, page_summary = check_page_ref_consistency(page_refs)

        # Get field metadata from original
        original_field = field_maps.get('original', {}).get(field_id, {})
        field_name = original_field.get('欄位名稱', f'欄位{field_id}')

        # Build variation string and get most common value
        counter = Counter(values)
        if len(unique_values) <= 1:
            variations = unique_values[0] if unique_values else ""
            most_common_value = unique_values[0] if unique_values else ""
        else:
            top_3 = counter.most_common(3)
            variations = " | ".join([f"{v}" for v, c in top_3])
            most_common_value = top_3[0][0] if top_3 else ""

        # Get most common page reference
        page_counter = Counter([p for p in page_refs if p.strip()])
        most_common_page = page_counter.most_common(1)[0][0] if page_counter else ""

        # Get original value (normalized)
        original_value = normalize_value(raw_values.get('original', ''))
        original_page = page_refs[0] if page_refs else ""

        # Intelligent correctness assessment
        correctness, assessment = assess_correctness(
            original_value=original_value,
            most_common_value=most_common_value,
            all_values=values,
            unique_values=unique_values,
            consistency_pct=consistency_pct,
            field_name=field_name
        )

        # Check page reference correctness
        page_correct = ""
        if original_page and most_common_page:
            # Normalize page refs for comparison
            orig_pages = set(original_page.replace(" ", "").lower().split(","))
            common_pages = set(most_common_page.replace(" ", "").lower().split(","))
            if orig_pages == common_pages or orig_pages.issubset(common_pages) or common_pages.issubset(orig_pages):
                page_correct = "TRUE"

        # Generate notes
        notes = ""
        if len(unique_values) > 2:
            notes = f"{len(unique_values)}種不同值"
        elif consistency_pct < 50:
            notes = "高變異"

        comparisons.append({
            '公司代碼': company_code,
            '欄位編號': field_id,
            '欄位名稱': field_name,
            '一致性%': round(consistency_pct, 1),
            '變異值': variations,
            '信心度': confidence,
            '頁碼一致': page_summary,
            '備註': notes,
            '答案正確性': correctness,
            '正確數值': most_common_value,
            '判斷說明': assessment,
            '實際參考頁數': most_common_page,
            '參考頁數正確': page_correct,
            '原始值': raw_values.get('original', ''),
            'run_1': raw_values.get('run_1', ''),
            'run_2': raw_values.get('run_2', ''),
            'run_3': raw_values.get('run_3', ''),
            'run_4': raw_values.get('run_4', ''),
            'run_5': raw_values.get('run_5', ''),
        })

    return comparisons


def generate_comparison_report(
    validation_dir: Path,
    target_companies: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Generate comparison report for all companies.

    Args:
        validation_dir: Path to validation directory
        target_companies: Optional list of company codes

    Returns:
        DataFrame with comparison results
    """
    logger = get_logger()

    if not target_companies:
        target_companies = VALIDATION_COMPANIES

    all_comparisons = []

    for company_code in target_companies:
        logger.info(f"Processing {company_code}...")

        # Load results
        all_results = load_validation_results(validation_dir, company_code)

        if not all_results:
            logger.warning(f"No results found for {company_code}")
            continue

        # Compare
        comparisons = compare_company_results(company_code, all_results)
        all_comparisons.extend(comparisons)

        logger.info(f"Compared {len(comparisons)} fields for {company_code}")

    # Create DataFrame
    df = pd.DataFrame(all_comparisons)

    # Save to CSV
    report_path = validation_dir / "comparison_report.csv"
    df.to_csv(report_path, index=False, encoding='utf-8-sig')
    logger.info(f"Report saved to: {report_path}")

    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print summary statistics."""
    print(f"\n{'='*60}")
    print("Comparison Summary")
    print(f"{'='*60}")

    print(f"\nTotal fields analyzed: {len(df)}")
    print(f"Companies: {df['公司代碼'].nunique()}")

    # Consistency distribution
    print("\nConsistency Distribution:")
    high_consistency = len(df[df['一致性%'] == 100])
    medium_consistency = len(df[(df['一致性%'] >= 67) & (df['一致性%'] < 100)])
    low_consistency = len(df[df['一致性%'] < 67])

    print(f"  高 (100%): {high_consistency} ({high_consistency/len(df)*100:.1f}%)")
    print(f"  中 (67-99%): {medium_consistency} ({medium_consistency/len(df)*100:.1f}%)")
    print(f"  低 (<67%): {low_consistency} ({low_consistency/len(df)*100:.1f}%)")

    # Page reference consistency
    page_consistent = len(df[df['頁碼一致'] == '✓'])
    print(f"\nPage reference consistency: {page_consistent}/{len(df)} ({page_consistent/len(df)*100:.1f}%)")

    # Fields with highest variation
    print("\nFields with lowest consistency:")
    low_fields = df[df['一致性%'] < 67].sort_values('一致性%')
    for _, row in low_fields.head(10).iterrows():
        print(f"  {row['公司代碼']} - {row['欄位名稱']}: {row['一致性%']}%")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare validation results across runs"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Compare specific company only"
    )
    parser.add_argument(
        "--validation-dir",
        type=str,
        help="Path to validation directory"
    )

    args = parser.parse_args()

    setup_logging(session_name="comparison")
    logger = get_logger()

    validation_dir = Path(args.validation_dir) if args.validation_dir else \
        Path(__file__).parent.parent / "validation"

    if not validation_dir.exists():
        logger.error(f"Validation directory not found: {validation_dir}")
        print("\nPlease run validation first:")
        print("  python scripts/run_validation.py --runs 5")
        sys.exit(1)

    target_companies = [args.company] if args.company else None

    # Generate report
    df = generate_comparison_report(validation_dir, target_companies)

    # Print summary
    print_summary(df)

    print(f"\nFull report saved to: {validation_dir / 'comparison_report.csv'}")


if __name__ == "__main__":
    main()
