"""
BRG — Business Report Generator
Composer — assembles section content into the full report HTML.
"""

import os
from jinja2 import Environment, FileSystemLoader
from .utils import current_year, current_month_year

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def compose_report(report_data: dict) -> str:
    """Assemble a complete HTML report from structured report data.

    Args:
        report_data: Dict containing:
            - title: str
            - subtitle: str
            - short_title: str
            - description: str (optional)
            - year: int
            - prepared_date: str
            - metrics: list[dict] with 'value' and 'label'
            - sections: list[dict] with 'number', 'title', 'content' (HTML)
            - extra_css: str (optional)

    Returns:
        Complete HTML string ready for PDF rendering.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report.html")

    # Ensure required fields have defaults
    report_data.setdefault("year", current_year())
    report_data.setdefault("prepared_date", current_month_year())
    report_data.setdefault("metrics", [])
    report_data.setdefault("description", "")
    report_data.setdefault("extra_css", "")

    return template.render(**report_data)


def build_report_data(
    title: str,
    subtitle: str,
    short_title: str,
    sections: list[dict],
    cover_metrics: list[dict] = None,
    description: str = "",
    extra_css: str = "",
) -> dict:
    """Build the report_data dict expected by compose_report.

    Args:
        title: Full report title.
        subtitle: Cover page subtitle.
        short_title: Short title for headers/footers.
        sections: List of section dicts with 'number', 'title', 'content'.
        cover_metrics: List of cover KPI dicts with 'value' and 'label'.
        description: Cover page description paragraph.
        extra_css: Additional CSS to inject.

    Returns:
        report_data dict.
    """
    return {
        "title": title,
        "subtitle": subtitle,
        "short_title": short_title,
        "description": description,
        "year": current_year(),
        "prepared_date": current_month_year(),
        "metrics": cover_metrics or [],
        "sections": sections,
        "extra_css": extra_css,
    }
