"""
BRG — Business Report Generator
Utility functions: date formatting, number formatting, filename sanitization.
"""

import re
from datetime import datetime


def current_year() -> int:
    return datetime.now().year


def current_month_year() -> str:
    return datetime.now().strftime("%B %Y")


def prepared_date() -> str:
    return datetime.now().strftime("Prepared %B %Y")


def sanitize_filename(title: str) -> str:
    """Convert a report title to a safe filename slug."""
    clean = re.sub(r"[^\w\s-]", "", title)
    clean = re.sub(r"\s+", "_", clean.strip())
    return clean


def format_number(value, prefix="", suffix="", decimals=0) -> str:
    """Format a number with optional prefix/suffix.
    E.g. format_number(860, prefix="$", suffix="B") -> "$860B"
    """
    if isinstance(value, (int, float)):
        if decimals > 0:
            formatted = f"{value:,.{decimals}f}"
        else:
            formatted = f"{value:,.0f}"
    else:
        formatted = str(value)
    return f"{prefix}{formatted}{suffix}"


def format_cagr(rate: float) -> str:
    """Format a CAGR value as a percentage string."""
    return f"{rate:.1f}%"


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text
