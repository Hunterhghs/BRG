# Business Report Generator (BRG)

## Project Overview

BRG is a prompt-to-report system that generates professional-grade market research reports (20–30 pages) from a single input — a report title or topic. The tool is designed to be operated by AI coding agents (e.g., GitHub Copilot, Cursor, Windsurf) that have live internet access, enabling real-time data retrieval, source verification, and report assembly without human intervention beyond the initial prompt.

---

## Problem Statement

Producing a comprehensive market research report typically requires a team of analysts spending days or weeks gathering data, synthesizing findings, structuring narratives, and formatting deliverables. BRG collapses this workflow into a single automated pipeline: the user provides a title, and the system produces a publication-ready PDF report backed by current, verifiable data.

---

## How It Works

### Input
A report title or topic string. Examples:
- *"Clean Energy Transition"*
- *"AI Chip Market Landscape"*
- *"Global EV Battery Supply Chain"*
- *"Commercial Real Estate Outlook 2026"*

### Output
A professionally formatted PDF report containing:
- **Cover page** with title, subtitle, edition date, and 4 key headline metrics
- **Table of Contents**
- **Executive Summary** with key statistics callouts
- **8–12 analytical sections** with narrative prose, data tables, and statistics
- **Strategic Outlook & Forecasts** with projection tables
- **Conclusion & Recommendations** segmented by audience (investors, policymakers, industry)
- **Consistent header/footer** with report title, edition label, page numbers, and confidentiality notice

### Process (Agent-Driven)
1. **Topic Decomposition** — The agent parses the title and generates a report outline (section titles, key questions to answer, data points to find).
2. **Research & Data Collection** — The agent uses web search, API calls, and public data sources to gather current statistics, market figures, policy details, and competitive landscape information.
3. **Content Generation** — Section-by-section prose is written, grounded in the collected data. Every claim is backed by a sourced figure or verifiable fact.
4. **Table & Metrics Assembly** — Structured data (growth rates, market sizes, capacity figures, forecasts) is organized into formatted tables and highlighted metric callouts.
5. **Report Compilation** — All sections are assembled into a unified document with consistent styling, headers, footers, and page flow.
6. **PDF Rendering** — The final document is rendered to PDF with professional typography and layout.

---

## Report Structure (Reference Template)

Based on the sample report (*Clean Energy Transition Report.pdf*), the standard report follows this structure:

| #  | Section | Description | Approx. Pages |
|----|---------|-------------|---------------|
| —  | Cover Page | Title, subtitle, 4 headline KPIs, date, confidentiality | 1 |
| —  | Table of Contents | Numbered section listing | 1 |
| 1  | Executive Summary | High-level synthesis, 4 key stat callouts, investment thesis | 1 |
| 2  | Market Size & Capacity | Historical growth, capacity by segment, CAGR table | 1–2 |
| 3  | Investment Trends | Capital flows by sector, key investors, financing mechanisms | 1–2 |
| 4  | Core Market Segments (1–3 sections) | Deep dives on primary sub-sectors (tech, dynamics, pricing, competition) | 3–6 |
| 5  | Regional Market Analysis | 4–6 region profiles (leaders, policies, outlook) | 2–3 |
| 6  | Infrastructure & Enablers | Supporting systems, bottlenecks, modernization trends | 1–2 |
| 7  | Policy & Regulatory Landscape | Key legislation, carbon pricing, incentive programs, comparison table | 1–2 |
| 8  | Market Risks & Challenges | 4–6 named risk categories with analysis | 1–2 |
| 9  | Strategic Outlook & Forecasts | 5–10 year projection table, strategic investment themes | 1–2 |
| 10 | Conclusion & Recommendations | Summary, audience-specific recommendations | 1–2 |

**Target length: 20–30 pages.** Section count and depth scale with topic complexity.

---

## Data & Quality Standards

- **Real data only.** Every statistic, market figure, and projection must come from a verifiable source (public reports, government data, industry associations, credible news). No fabricated numbers.
- **Current data.** Figures should reflect the most recent available data at the time of generation. Historical data should span at least 5–10 years for trend analysis.
- **Source-quality hierarchy:** Government/intergovernmental agencies (IEA, World Bank, BLS, etc.) > industry associations & research firms (BloombergNEF, IRENA, Gartner, etc.) > reputable financial/business press > company filings and press releases.
- **Professional tone.** Formal, analytical, third-person. No hedging language or filler. Dense with facts and analysis.
- **Internally consistent.** Figures cited in the executive summary must match those in detailed sections. Totals must add up.

---

## Technical Architecture

### Core Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | Python | Main pipeline: outline generation, research dispatch, content assembly |
| Report Template | Jinja2 + HTML/CSS | Section templates, cover page, headers/footers, table styles |
| PDF Rendering | WeasyPrint or ReportLab | HTML-to-PDF conversion with professional typography |
| Data Formatting | Python (tabulate / pandas) | Table generation, number formatting, CAGR calculations |
| Configuration | YAML | Report style config, section templates, prompt templates |

### Agent Integration Layer
The system is designed to be driven by AI coding agents. The agent:
- Runs the Python pipeline
- Performs web research to populate data (via search tools, web fetch, APIs)
- Fills in section content with sourced data
- Executes the PDF rendering step

**No API keys or paid services required for the core pipeline.** The agent's built-in internet access and reasoning capabilities handle research and writing.

### Project Structure
```
BRG/
├── PROJECT_OVERVIEW.md            # This document
├── Clean Energy Transition Report.pdf  # Sample reference report
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
├── output/                        # Generated reports land here
├── requirements.txt               # Python dependencies
└── README.md                      # Usage instructions
```

---

## Usage

```bash
# Generate a report
python src/generator.py "AI Chip Market Landscape"

# Output
# → output/AI_Chip_Market_Landscape_2026.pdf
```

When run by an AI coding agent, the workflow is:
1. User provides a title/topic
2. Agent runs the generator, which produces an outline
3. Agent researches each section (web search, data retrieval)
4. Agent populates section content with real data and analysis
5. Agent renders the final PDF

---

## Design Principles

1. **Data-first.** The report's value comes from accurate, current data — not generic prose. Every section must contain concrete figures.
2. **Template-driven.** Consistent formatting across all reports via HTML/CSS templates. Style changes are config-level, not code-level.
3. **Agent-native.** The pipeline assumes an AI agent is the operator. The system provides structure and rendering; the agent provides research and writing.
4. **Minimal dependencies.** Pure Python with lightweight libraries. No databases, no SaaS APIs, no complex infrastructure.
5. **Reproducible.** Given the same title and data, the system produces the same report. Sections are modular and independently testable.

---

## Report Types (Initial Scope)

The system is optimized for **market research reports**, including:

| Report Type | Example Title | Key Sections |
|-------------|--------------|--------------|
| Market Analysis & Outlook | "Global Cloud Infrastructure Market" | Market size, segmentation, competitive landscape, forecasts |
| Industry Deep Dive | "Semiconductor Foundry Industry" | Supply chain, technology roadmap, capacity analysis, regional dynamics |
| Sector Investment Report | "Healthcare AI Investment Landscape" | Funding trends, deal flow, key players, valuation analysis, exit outlook |
| Technology Assessment | "Quantum Computing Commercial Readiness" | Technology maturity, use cases, competitive benchmarking, adoption timeline |
| Regional Market Report | "Southeast Asia Fintech Market" | Country profiles, regulatory comparison, growth drivers, market sizing |

The template system is flexible enough to accommodate other structured research formats with minimal modification.

---

## Success Criteria

A generated report is considered successful when it:

- [ ] Is 20–30 pages in length
- [ ] Contains a professional cover page with 4 headline metrics
- [ ] Includes a table of contents matching actual sections
- [ ] Has an executive summary with key statistics
- [ ] Contains at least 3 data tables with real, sourced figures
- [ ] Covers regional/geographic analysis where relevant
- [ ] Includes a policy/regulatory section where relevant
- [ ] Presents a forward-looking forecast with projection table
- [ ] Ends with actionable recommendations by audience segment
- [ ] Uses consistent formatting (headers, footers, page numbers, fonts)
- [ ] Contains no fabricated data — all figures are verifiable
- [ ] Reads as a professional analyst report suitable for executive distribution
