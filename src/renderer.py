"""
BRG — Business Report Generator
Renderer — converts assembled HTML to PDF using WeasyPrint.
"""

import os
from weasyprint import HTML


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def render_pdf(html_content: str, output_filename: str) -> str:
    """Render an HTML string to a PDF file.

    Args:
        html_content: Complete HTML report string.
        output_filename: Filename for the output PDF (e.g. "Report_2026.pdf").

    Returns:
        Absolute path to the generated PDF file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Use the templates directory as base_url so CSS and images resolve correctly
    html = HTML(string=html_content, base_url=TEMPLATE_DIR)
    html.write_pdf(output_path)

    return os.path.abspath(output_path)
