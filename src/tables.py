"""
BRG — Business Report Generator
Table formatting and calculation utilities.
"""

from typing import Optional
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def render_table(
    headers: list[str],
    rows: list[list[str]],
    title: Optional[str] = None,
    numeric_columns: bool = True,
    policy_table: bool = False,
    highlight_rows: Optional[list[int]] = None,
) -> str:
    """Render a data table as HTML using the table template.

    Args:
        headers: Column header strings.
        rows: List of rows, each row is a list of cell strings.
        title: Optional table title displayed above the table.
        numeric_columns: If True, right-align columns after the first.
        policy_table: If True, use wider first column styling.
        highlight_rows: Optional list of 0-based row indices to highlight.

    Returns:
        HTML string for the rendered table.
    """
    highlight_rows = highlight_rows or []

    row_data = []
    for i, row in enumerate(rows):
        row_data.append({
            "cells": row,
            "highlight": i in highlight_rows,
        })

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("table.html")
    return template.render(
        headers=headers,
        rows=row_data,
        table_title=title,
        numeric_columns=numeric_columns,
        policy_table=policy_table,
    )


def render_metrics(metrics: list[dict]) -> str:
    """Render a row of metric callout boxes.

    Args:
        metrics: List of dicts with 'value' and 'label' keys.

    Returns:
        HTML string for the metrics callout row.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("metrics_callout.html")
    return template.render(metrics=metrics)


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """Calculate Compound Annual Growth Rate."""
    if start_value <= 0 or years <= 0:
        return 0.0
    return ((end_value / start_value) ** (1 / years) - 1) * 100
