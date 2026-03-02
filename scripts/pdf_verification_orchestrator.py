#!/usr/bin/env python3
"""
PDF Verification Orchestrator — Batch Generator

Reads discrepancies from Phase 1 comparison, groups by company,
and generates per-company verification batch JSONs for PDF agents.

Usage:
    python scripts/pdf_verification_orchestrator.py
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import PROJECT_ROOT, OUTPUT_DIR
from src.utils import setup_logging, get_logger

DISCREPANCIES_CSV = OUTPUT_DIR / "comparison" / "discrepancies_only.csv"
VERIFICATION_DIR = OUTPUT_DIR / "verification"
BATCHES_DIR = VERIFICATION_DIR / "batches"
RESULTS_DIR = VERIFICATION_DIR / "results"
PDF_DIR = PROJECT_ROOT / "analysis" / "pdfs"


def load_discrepancies(csv_path: Path) -> list[dict]:
    """Load discrepancies CSV."""
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def find_pdf(company_code: str, company_name: str) -> Path | None:
    """Find the PDF file for a company."""
    # Try exact match first
    for pattern in [
        f"{company_code}_{company_name}_2024.pdf",
        f"{company_code}_*_2024.pdf",
    ]:
        matches = list(PDF_DIR.glob(pattern))
        if matches:
            return matches[0]

    # Broader search
    for f in PDF_DIR.glob("*.pdf"):
        if company_code in f.name:
            return f

    return None


def extract_page_numbers(page_refs: str) -> list[int]:
    """Extract page numbers from a page reference string like 'p.10, p.12'."""
    if not page_refs or page_refs.strip().upper() == "NA":
        return []
    return sorted(set(int(p) for p in re.findall(r"p\.(\d+)", page_refs, re.IGNORECASE)))


def generate_batch(
    company_code: str,
    company_name: str,
    discrepancies: list[dict],
    pdf_path: Path,
) -> dict:
    """Generate a verification batch JSON for one company."""
    # Collect all referenced pages
    all_pages: set[int] = set()
    fields = []

    for row in discrepancies:
        g_pages = extract_page_numbers(row.get("google_page_refs", ""))
        a_pages = extract_page_numbers(row.get("agentic_page_refs", ""))
        combined_pages = sorted(set(g_pages + a_pages))
        all_pages.update(combined_pages)

        fields.append({
            "field_id": row["欄位編號"],
            "field_name": row["欄位名稱"],
            "discrepancy_type": row["discrepancy_type"],
            "severity": row["severity"],
            "google_value": row["google_value"],
            "agentic_value": row["agentic_value"],
            "google_notes": row.get("google_notes", ""),
            "agentic_notes": row.get("agentic_notes", ""),
            "google_page_refs": row.get("google_page_refs", ""),
            "agentic_page_refs": row.get("agentic_page_refs", ""),
            "referenced_pages": combined_pages,
        })

    # Build page reading plan: cluster into 20-page chunks
    sorted_pages = sorted(all_pages)
    page_chunks: list[tuple[int, int]] = []
    if sorted_pages:
        chunk_start = sorted_pages[0]
        chunk_end = min(chunk_start + 19, sorted_pages[-1])
        for page in sorted_pages:
            if page > chunk_end:
                page_chunks.append((chunk_start, chunk_end))
                chunk_start = page
                chunk_end = min(page + 19, sorted_pages[-1])
            else:
                chunk_end = max(chunk_end, page)
        page_chunks.append((chunk_start, chunk_end))

    return {
        "company_code": company_code,
        "company_name": company_name,
        "pdf_path": str(pdf_path),
        "total_discrepancies": len(fields),
        "page_reading_plan": [
            {"start": s, "end": e} for s, e in page_chunks
        ],
        "all_referenced_pages": sorted_pages,
        "fields": fields,
        "generated_at": datetime.now().isoformat(),
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate per-company PDF verification batches from discrepancies"
    )
    parser.add_argument(
        "--comparison-dir",
        type=Path,
        default=OUTPUT_DIR / "comparison",
        help="Directory containing discrepancies_only.csv (default: output/comparison)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=VERIFICATION_DIR,
        help="Base output directory for batches/ and results/ (default: output/verification)",
    )
    args = parser.parse_args()

    setup_logging(session_name="pdf_verification_orchestrator")
    logger = get_logger()

    discrepancies_csv = args.comparison_dir / "discrepancies_only.csv"
    batches_dir = args.output_dir / "batches"
    results_dir = args.output_dir / "results"

    # Ensure directories exist
    batches_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # Load discrepancies
    if not discrepancies_csv.exists():
        logger.error(f"Discrepancies CSV not found: {discrepancies_csv}")
        logger.error("Run 'python scripts/orchestrate_comparison.py' first.")
        sys.exit(1)

    rows = load_discrepancies(discrepancies_csv)
    logger.info(f"Loaded {len(rows)} discrepancies")

    # Group by company
    by_company: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_company[row["公司代碼"]].append(row)

    # Generate batches
    for company_code, disc_rows in sorted(by_company.items()):
        company_name = disc_rows[0]["公司簡稱"]
        pdf_path = find_pdf(company_code, company_name)

        if not pdf_path:
            logger.warning(f"No PDF found for {company_code} {company_name}, skipping")
            continue

        batch = generate_batch(company_code, company_name, disc_rows, pdf_path)
        batch_path = batches_dir / f"{company_code}_{company_name}_batch.json"

        with open(batch_path, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)

        logger.info(
            f"Generated batch: {batch_path.name} — "
            f"{batch['total_discrepancies']} fields, "
            f"{len(batch['all_referenced_pages'])} pages to read"
        )

    print(f"\nBatches written to: {batches_dir}/")
    for f in sorted(batches_dir.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(f"  {f.name}: {data['total_discrepancies']} fields, pages {data['all_referenced_pages']}")


if __name__ == "__main__":
    main()
