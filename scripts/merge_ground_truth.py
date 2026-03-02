#!/usr/bin/env python3
"""
Merge Ground Truth — Combine existing ground truth with new verification results.

Merges by (company_code, field_id) key. Newer results override older ones.

Usage:
    python scripts/merge_ground_truth.py \
        --existing output/verification/ground_truth.json \
        --new-results output/verification/results/v2/ \
        --output output/verification/ground_truth_v2.json
"""

import json
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import OUTPUT_DIR

DEFAULT_GT_PATH = OUTPUT_DIR / "verification" / "ground_truth.json"


def load_ground_truth(path: Path) -> dict:
    """Load existing ground truth JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_verification_results(results_dir: Path) -> list[dict]:
    """Load all verification result JSONs from a directory."""
    all_fields: list[dict] = []
    for json_path in sorted(results_dir.glob("*.json")):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        fields = data.get("fields", data.get("verified_fields", []))
        all_fields.extend(fields)
    return all_fields


def merge(existing: dict, new_fields: list[dict]) -> dict:
    """Merge new verification fields into existing ground truth."""
    # Index existing fields by (company_code, field_id)
    index: dict[tuple[str, str], dict] = {}
    for field in existing.get("fields", []):
        key = (str(field["company_code"]), str(field["field_id"]))
        index[key] = field

    # Override or add new fields
    added = 0
    updated = 0
    for field in new_fields:
        key = (str(field["company_code"]), str(field["field_id"]))
        if key in index:
            index[key] = field
            updated += 1
        else:
            index[key] = field
            added += 1

    # Rebuild fields list sorted by (company_code, field_id as int)
    merged_fields = sorted(
        index.values(),
        key=lambda f: (f["company_code"], int(f["field_id"])),
    )

    # Collect all company codes
    companies = sorted(set(f["company_code"] for f in merged_fields))

    result = {
        "description": existing.get("description", "Merged ground truth"),
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "page_number_standard": "printed_footer_v2",
        "companies": companies,
        "total_fields": len(merged_fields),
        "merge_stats": {
            "previous_total": len(existing.get("fields", [])),
            "new_fields_added": added,
            "fields_updated": updated,
            "final_total": len(merged_fields),
        },
        "fields": merged_fields,
    }

    return result


def main():
    parser = ArgumentParser(description="Merge ground truth with new verification results")
    parser.add_argument(
        "--existing",
        type=Path,
        default=DEFAULT_GT_PATH,
        help=f"Path to existing ground truth JSON (default: {DEFAULT_GT_PATH})",
    )
    parser.add_argument(
        "--new-results",
        type=Path,
        required=True,
        help="Directory containing new verification result JSONs",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for merged ground truth (default: overwrite existing)",
    )
    args = parser.parse_args()

    if not args.existing.exists():
        print(f"Existing ground truth not found: {args.existing}", file=sys.stderr)
        sys.exit(1)

    if not args.new_results.exists():
        print(f"New results directory not found: {args.new_results}", file=sys.stderr)
        sys.exit(1)

    existing = load_ground_truth(args.existing)
    new_fields = load_verification_results(args.new_results)

    if not new_fields:
        print("No new verification fields found.", file=sys.stderr)
        sys.exit(0)

    merged = merge(existing, new_fields)
    output_path = args.output or args.existing

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    stats = merged["merge_stats"]
    print(
        f"Merged ground truth: {stats['previous_total']} existing "
        f"+ {stats['new_fields_added']} added, {stats['fields_updated']} updated "
        f"→ {stats['final_total']} total"
    )
    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
