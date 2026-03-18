# BRG — Business Report Generator

A prompt-to-report system that generates professional-grade market research reports (20–30 pages) from a single input title. Designed to be operated by AI coding agents with internet access.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** WeasyPrint requires system libraries. On macOS: `brew install pango libffi`. On Ubuntu: `apt install libpango-1.0-0 libpangoft2-1.0-0`.

### 2. Generate a Report Outline

```bash
python src/generator.py "AI Chip Market Landscape"
```

This creates:
- A report outline printed to the console
- A JSON data file at `output/AI_Chip_Market_Landscape_data.json`

### 3. Populate the Report (Agent Step)

The AI agent:
1. Reviews the outline and section guidance
2. Researches each section using web search and data sources
3. Populates the `content` field of each section in the JSON data file with HTML
4. Adds `cover_metrics` (list of `{value, label}` dicts)

### 4. Render the PDF

```bash
python src/generator.py --render output/AI_Chip_Market_Landscape_data.json
```

Output: `output/AI_Chip_Market_Landscape_2026.pdf`

## Project Structure

```
BRG/
├── config/
│   ├── report_style.yaml          # Fonts, colors, margins, header/footer config
│   └── section_templates.yaml     # Default section outlines by report type
├── templates/
│   ├── report.html                # Master Jinja2 template
│   ├── cover.html                 # Cover page template
│   ├── toc.html                   # Table of contents template
│   ├── section.html               # Generic section template
│   ├── table.html                 # Data table partial
│   ├── metrics_callout.html       # KPI/stat callout partial
│   └── styles.css                 # Report stylesheet
├── src/
│   ├── generator.py               # Main entry point — orchestrates the pipeline
│   ├── outline.py                 # Generates report outline from title
│   ├── researcher.py              # Data collection and source management
│   ├── composer.py                # Assembles section content into template
│   ├── tables.py                  # Table formatting and calculation utilities
│   ├── renderer.py                # HTML → PDF rendering
│   └── utils.py                   # Date formatting, number formatting, helpers
├── output/                        # Generated reports
├── requirements.txt
└── README.md
```

## Report Types

| Type | Flag | Description |
|------|------|-------------|
| Default | `--type default` | General market research report |
| Market Analysis | `--type market_analysis` | Market sizing, segmentation, and investment outlook |
| Industry Deep Dive | `--type industry_deep_dive` | Supply chain, technology roadmap, capacity analysis |
| Sector Investment | `--type sector_investment` | Funding trends, deal flow, valuations, exit outlook |
| Technology Assessment | `--type technology_assessment` | Maturity assessment, benchmarking, adoption timeline |
| Regional Market | `--type regional_market` | Country profiles, regulatory comparison, regional dynamics |

## Agent Integration

BRG is designed for AI agents (Copilot, Cursor, Windsurf, etc.). The agent:

1. Runs `generator.py` with a title to scaffold the outline
2. Uses its internet-connected tools to research each section
3. Writes HTML content into the JSON data file using the table/metrics helpers in `src/tables.py`
4. Runs `generator.py --render` to produce the PDF

### Using Table Helpers

```python
from src.tables import render_table, render_metrics

# Data table
table_html = render_table(
    headers=["Technology", "2020 (GW)", "2025E (GW)", "CAGR"],
    rows=[
        ["Solar PV", "714", "1,950", "24.0%"],
        ["Wind", "743", "1,230", "11.0%"],
    ],
    title="Capacity Growth by Technology"
)

# Metric callout boxes
metrics_html = render_metrics([
    {"value": "$860B+", "label": "Clean Energy Investment (2025E)"},
    {"value": "4,765 GW", "label": "Global RE Capacity (2025E)"},
])
```

## Sample Report

See `Clean Energy Transition Report.pdf` for a reference example of the target output quality and structure.
