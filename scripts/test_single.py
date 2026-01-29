#!/usr/bin/env python3
"""
Test script for single company analysis.

Usage:
    python scripts/test_single.py --company 2330
    python scripts/test_single.py --pdf /path/to/report.pdf
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import validate_config, print_config
from src.utils import setup_logging, get_logger
from src.pdf_processor import CacheManager
from src.analyzer import FieldCollectionAnalyzer


def test_local_pdf(pdf_path: str):
    """Test analysis with a local PDF file."""
    logger = get_logger()

    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return

    print(f"\n📄 Testing with local PDF: {pdf_path}")

    cache_manager = CacheManager()
    analyzer = FieldCollectionAnalyzer(cache_manager)

    # Extract company info from filename if possible
    results = analyzer.analyze_company_report(pdf_path)

    if results:
        print(f"\n✅ Successfully extracted {len(results)} fields")
        print("\nSample results (first 5 fields):")
        for result in results[:5]:
            print(f"  Field {result['欄位編號']}: {result['欄位名稱']}")
            print(f"    Value: {result['欄位數值'][:50]}..." if len(result['欄位數值']) > 50 else f"    Value: {result['欄位數值']}")
            print(f"    Page: {result['參考頁數']}")
            print()
    else:
        print("\n❌ Analysis failed")

    print(analyzer.get_session_summary())


def main():
    parser = argparse.ArgumentParser(
        description="Test single company or PDF analysis"
    )
    parser.add_argument(
        "--pdf", "-p",
        type=str,
        help="Path to local PDF file to analyze"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        help="Company code to test (requires Google Sheets setup)"
    )

    args = parser.parse_args()

    # Setup
    setup_logging(session_name="test")
    logger = get_logger()

    if not validate_config():
        logger.error("Configuration validation failed")
        sys.exit(1)

    print_config()

    if args.pdf:
        test_local_pdf(args.pdf)
    elif args.company:
        print(f"Testing company {args.company} - requires Google Sheets integration")
        print("Use run_analysis.py --company {args.company} instead")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
