#!/usr/bin/env python3
"""Download all verification PDFs from Google Drive to local folder."""

import json
import os
import re
import requests
from pathlib import Path

CACHE_DIR = Path("/Users/jinsoon/Desktop/sustainability-report-parser/cache")
OUTPUT_DIR = Path("/Users/jinsoon/Desktop/sustainability-report-parser/verification_pdfs")

def extract_file_id(drive_url: str) -> str:
    """Extract Google Drive file ID from URL."""
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)',
        r'/d/([a-zA-Z0-9_-]+)/'
    ]
    for pattern in patterns:
        match = re.search(pattern, drive_url)
        if match:
            return match.group(1)
    return None

def download_from_drive(file_id: str, output_path: Path) -> bool:
    """Download file from Google Drive using direct download URL."""
    # Direct download URL for large files
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"

    try:
        print(f"  Downloading from {file_id}...")
        response = requests.get(download_url, stream=True, timeout=120)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"  ✓ Saved to {output_path.name} ({output_path.stat().st_size:,} bytes)")
            return True
        else:
            print(f"  ✗ Failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get all cache files
    cache_files = sorted(CACHE_DIR.glob("*_2024_analysis.json"))

    print(f"Found {len(cache_files)} companies to download\n")

    downloaded = []
    failed = []

    for cache_file in cache_files:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        company_info = data['company_info']
        code = company_info['company_code']
        name = company_info['company_name']
        file_link = company_info['file_link']

        print(f"[{code}] {name}")

        file_id = extract_file_id(file_link)
        if not file_id:
            print(f"  ✗ Could not extract file ID from: {file_link}")
            failed.append(code)
            continue

        output_path = OUTPUT_DIR / f"{code}_{name}_2024_永續報告書.pdf"

        if output_path.exists():
            print(f"  ⏭ Already exists: {output_path.name}")
            downloaded.append(code)
            continue

        if download_from_drive(file_id, output_path):
            downloaded.append(code)
        else:
            failed.append(code)

        print()

    print("=" * 50)
    print(f"Downloaded: {len(downloaded)} files")
    print(f"Failed: {len(failed)} files")
    if failed:
        print(f"Failed companies: {', '.join(failed)}")

if __name__ == "__main__":
    main()
