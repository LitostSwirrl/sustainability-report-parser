"""
Utility functions for Sustainability Report Parser.
Includes logging setup, retry decorators, and helper functions.
"""

import logging
import time
import random
import functools
from datetime import datetime
from pathlib import Path
from typing import Callable, TypeVar, ParamSpec

from .config import LOG_DIR, LOG_LEVEL, MAX_RETRIES, BASE_RETRY_DELAY

P = ParamSpec('P')
T = TypeVar('T')

# Global logger instance
logger: logging.Logger = None  # type: ignore


def setup_logging(session_name: str = None) -> logging.Logger:
    """
    Setup logging configuration with file and console handlers.

    Args:
        session_name: Optional session name for the log file

    Returns:
        Configured logger instance
    """
    global logger

    # Create log directory if not exists
    Path(LOG_DIR).mkdir(exist_ok=True)

    # Generate timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_suffix = f"_{session_name}" if session_name else ""
    log_filename = f"run_{timestamp}{session_suffix}.log"
    log_path = Path(LOG_DIR) / log_filename

    # Configure root logger
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Create handlers
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    console_handler.setFormatter(logging.Formatter(log_format))

    # Setup logger
    logger = logging.getLogger("sustainability_parser")
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized. Log file: {log_path}")

    return logger


def get_logger() -> logging.Logger:
    """Get the global logger instance, initializing if needed."""
    global logger
    if logger is None:
        logger = setup_logging()
    return logger


def retry_with_backoff(
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_RETRY_DELAY,
    exceptions: tuple = (Exception,),
    retry_on_quota: bool = True
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds before first retry
        exceptions: Tuple of exceptions to catch and retry
        retry_on_quota: Whether to specifically handle quota/rate limit errors

    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            log = get_logger()

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    error_str = str(e)

                    # Check for quota/rate limit errors
                    is_quota_error = (
                        "429" in error_str or
                        "Resource has been exhausted" in error_str or
                        "quota" in error_str.lower()
                    )

                    if retry_on_quota and is_quota_error and attempt < max_retries:
                        # Exponential backoff with jitter
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 10)
                        log.warning(
                            f"API quota limit hit, attempt {attempt + 1}/{max_retries}. "
                            f"Waiting {delay:.1f}s before retry..."
                        )
                        time.sleep(delay)
                        continue
                    elif attempt < max_retries:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 5)
                        log.warning(
                            f"Error in {func.__name__}: {e}. "
                            f"Attempt {attempt + 1}/{max_retries}. Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        continue
                    else:
                        log.error(f"Failed after {max_retries} retries: {e}")
                        raise

            return func(*args, **kwargs)  # This line shouldn't be reached

        return wrapper
    return decorator


def log_timing(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to log function execution time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        log = get_logger()
        start_time = time.time()
        log.info(f"Starting {func.__name__}...")

        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            log.info(f"Completed {func.__name__} in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            log.error(f"Failed {func.__name__} after {elapsed:.2f}s: {e}")
            raise

    return wrapper


class SessionSummary:
    """Track and summarize processing session statistics."""

    def __init__(self):
        self.start_time = datetime.now()
        self.companies_processed = 0
        self.companies_failed = 0
        self.fields_extracted = 0
        self.api_calls = 0
        self.errors: list[str] = []

    def record_success(self, company_code: str, fields_count: int) -> None:
        """Record successful company processing."""
        self.companies_processed += 1
        self.fields_extracted += fields_count

    def record_failure(self, company_code: str, error: str) -> None:
        """Record failed company processing."""
        self.companies_failed += 1
        self.errors.append(f"{company_code}: {error}")

    def record_api_call(self) -> None:
        """Record an API call."""
        self.api_calls += 1

    def get_summary(self) -> str:
        """Generate session summary string."""
        elapsed = datetime.now() - self.start_time
        total = self.companies_processed + self.companies_failed

        summary = f"""
========================================
SESSION SUMMARY
========================================
Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {elapsed}
Total Companies: {total}
  - Successful: {self.companies_processed}
  - Failed: {self.companies_failed}
Fields Extracted: {self.fields_extracted}
API Calls: {self.api_calls}
"""

        if self.errors:
            summary += f"\nErrors ({len(self.errors)}):\n"
            for error in self.errors[:10]:  # Show first 10 errors
                summary += f"  - {error}\n"
            if len(self.errors) > 10:
                summary += f"  ... and {len(self.errors) - 10} more errors\n"

        summary += "========================================"
        return summary

    def log_summary(self) -> None:
        """Log the session summary."""
        log = get_logger()
        log.info(self.get_summary())
