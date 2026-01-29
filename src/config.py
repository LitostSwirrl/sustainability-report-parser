"""
Configuration module for Sustainability Report Parser.
Centralizes all configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================================
# API Configuration
# ===========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ===========================================
# Google Sheets Configuration
# ===========================================
COMPANY_LIST_SHEET_ID = os.getenv(
    "COMPANY_LIST_SHEET_ID",
    "1PC5V7dMaX8fh336i2H-KEP56c2rpQZb0UjArBRurnCU"
)
OUTPUT_SHEET_ID = os.getenv(
    "OUTPUT_SHEET_ID",
    "1PC5V7dMaX8fh336i2H-KEP56c2rpQZb0UjArBRurnCU"
)
COMPANY_LIST_SHEET_NAME = os.getenv("COMPANY_LIST_SHEET_NAME", "raw_報告書清單")
OUTPUT_SHEET_NAME = os.getenv("OUTPUT_SHEET_NAME", "欄位蒐集結果")

# ===========================================
# Model Configuration
# ===========================================
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.0-pro")

# ===========================================
# Directory Configuration
# ===========================================
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
LOG_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create directories if they don't exist
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ===========================================
# Logging Configuration
# ===========================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ===========================================
# Processing Configuration
# ===========================================
MAX_RETRIES = 3
BASE_RETRY_DELAY = 30  # seconds
REQUEST_TIMEOUT = 300  # seconds


def validate_config() -> bool:
    """Validate required configuration is present."""
    errors = []

    if not GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is not set")

    if errors:
        for error in errors:
            print(f"Configuration Error: {error}")
        return False

    return True


def print_config() -> None:
    """Print current configuration (masking sensitive values)."""
    print("=== Configuration ===")
    print(f"MODEL_NAME: {MODEL_NAME}")
    print(f"COMPANY_LIST_SHEET_ID: {COMPANY_LIST_SHEET_ID}")
    print(f"OUTPUT_SHEET_ID: {OUTPUT_SHEET_ID}")
    print(f"CACHE_DIR: {CACHE_DIR}")
    print(f"LOG_DIR: {LOG_DIR}")
    print(f"GEMINI_API_KEY: {'***' + GEMINI_API_KEY[-4:] if GEMINI_API_KEY else 'NOT SET'}")
    print("=====================")
