#!/usr/bin/env python3
"""
BRG — Business Report Generator
Main entry point — orchestrates the report generation pipeline.

Usage:
    python src/generator.py "Report Title"
    python src/generator.py "Report Title" --type market_analysis
    python src/generator.py "Report Title" --subtitle "Custom Subtitle"

This script is designed to be run by an AI coding agent. The pipeline:
1. Generates a report outline from the title
2. Prints the outline and section guidance for the agent to review
3. Creates a report data JSON file for the agent to populate with researched content
4. Once populated, compiles and renders the final PDF

The agent workflow:
    Step 1: Run generator.py to create the outline and data file
    Step 2: Research each section (using web search, APIs, etc.)
    Step 3: Populate the report data file with HTML content for each section
    Step 4: Run generator.py --render to compile the final PDF
"""

import argparse
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.outline import generate_outline, print_outline, outline_to_dict
from src.composer import compose_report, build_report_data
from src.renderer import render_pdf
from src.utils import sanitize_filename, current_year

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def step_outline(title: str, subtitle: str = "", report_type: str = "default",
                 description: str = "") -> dict:
    """Step 1: Generate and display the report outline.

    Returns the outline as a dict and saves it as a JSON data file
    that the agent will populate with content.
    """
    outline = generate_outline(
        title=title,
        subtitle=subtitle,
        report_type=report_type,
        description=description,
    )

    # Display the outline for the agent
    print("=" * 70)
    print("REPORT OUTLINE")
    print("=" * 70)
    print(print_outline(outline))

    # Convert to dict for data file
    data = outline_to_dict(outline)
    data["year"] = current_year()

    # Save the data file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    slug = sanitize_filename(title)
    data_path = os.path.join(OUTPUT_DIR, f"{slug}_data.json")
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nReport data file created: {data_path}")
    print(f"\nNext steps:")
    print(f"  1. Research each section using web search and data sources")
    print(f"  2. Populate the 'content' field of each section in the data file with HTML")
    print(f"  3. Add cover_metrics (list of {{value, label}} dicts)")
    print(f"  4. Run: python src/generator.py --render \"{data_path}\"")

    return data


def step_render(data_path: str) -> str:
    """Step 2: Render the populated data file to PDF.

    Args:
        data_path: Path to the populated JSON data file.

    Returns:
        Path to the generated PDF.
    """
    with open(data_path, "r") as f:
        data = json.load(f)

    # Build report data
    report_data = build_report_data(
        title=data["title"],
        subtitle=data["subtitle"],
        short_title=data["short_title"],
        sections=data["sections"],
        cover_metrics=data.get("cover_metrics", []),
        description=data.get("description", ""),
    )

    # Compose HTML
    html = compose_report(report_data)

    # Render PDF
    slug = sanitize_filename(data["title"])
    filename = f"{slug}_{data.get('year', current_year())}.pdf"
    pdf_path = render_pdf(html, filename)

    print(f"\nReport generated: {pdf_path}")
    return pdf_path


def quick_render(report_data: dict) -> str:
    """Render directly from a report_data dict (for programmatic use).

    Args:
        report_data: Complete report data dict with all sections populated.

    Returns:
        Path to the generated PDF.
    """
    html = compose_report(report_data)
    slug = sanitize_filename(report_data["title"])
    filename = f"{slug}_{report_data.get('year', current_year())}.pdf"
    return render_pdf(html, filename)


def main():
    parser = argparse.ArgumentParser(
        description="BRG — Business Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Step 1: Generate outline
  python src/generator.py "AI Chip Market Landscape"

  # Step 2: Render populated data file
  python src/generator.py --render output/AI_Chip_Market_Landscape_data.json

  # With options
  python src/generator.py "Clean Energy Transition" --type market_analysis \\
      --subtitle "Global Market Analysis & Investment Outlook"
        """,
    )

    parser.add_argument(
        "title",
        nargs="?",
        help="Report title (for outline generation)",
    )

    parser.add_argument(
        "--render",
        metavar="DATA_FILE",
        help="Path to populated JSON data file to render as PDF",
    )

    parser.add_argument(
        "--type",
        default="default",
        choices=["default", "market_analysis", "industry_deep_dive",
                 "sector_investment", "technology_assessment", "regional_market"],
        help="Report type template (default: default)",
    )

    parser.add_argument(
        "--subtitle",
        default="",
        help="Custom subtitle for cover page",
    )

    parser.add_argument(
        "--description",
        default="",
        help="Cover page description paragraph",
    )

    args = parser.parse_args()

    if args.render:
        step_render(args.render)
    elif args.title:
        step_outline(
            title=args.title,
            subtitle=args.subtitle,
            report_type=args.type,
            description=args.description,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
