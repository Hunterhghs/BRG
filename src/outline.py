"""
BRG — Business Report Generator
Outline generation — builds a report structure from a title/topic.

The outline module produces the section structure that the agent will then
populate with researched content. It uses the section_templates.yaml config
as a starting framework and adapts it to the specific topic.
"""

import os
import yaml
from dataclasses import dataclass, field

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")


@dataclass
class SectionOutline:
    """A single section in the report outline."""
    number: int
    title: str
    key_elements: list[str] = field(default_factory=list)
    guidance: str = ""
    subsections: list[str] = field(default_factory=list)


@dataclass
class ReportOutline:
    """Complete report outline with metadata."""
    title: str
    subtitle: str
    short_title: str
    report_type: str
    sections: list[SectionOutline] = field(default_factory=list)
    cover_metrics: list[dict] = field(default_factory=list)
    description: str = ""


def load_section_templates() -> dict:
    """Load section templates from config."""
    config_path = os.path.join(CONFIG_DIR, "section_templates.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def generate_outline(
    title: str,
    subtitle: str = "",
    report_type: str = "default",
    description: str = "",
) -> ReportOutline:
    """Generate a report outline from a title and optional parameters.

    This creates the default section structure. The AI agent is expected to:
    1. Review the outline
    2. Adapt section titles to the specific topic
    3. Research and populate each section's content

    Args:
        title: Report title (e.g. "Clean Energy Transition")
        subtitle: Subtitle for the cover page
        report_type: Template type key from section_templates.yaml
        description: Cover page description paragraph

    Returns:
        ReportOutline with sections ready to be populated.
    """
    templates = load_section_templates()

    # Get the template for this report type
    template = templates.get(report_type, templates["default"])

    # If this type inherits from default, merge sections
    base_sections = templates["default"]["sections"]
    if "inherits" in template and template["inherits"] == "default":
        extra = template.get("additional_sections", [])
        # Insert additional sections before "Conclusion & Recommendations"
        all_sections = base_sections[:-1] + extra + [base_sections[-1]]
    else:
        all_sections = template.get("sections", base_sections)

    # Build short title (for headers/footers)
    short_title = title.split(":")[0].strip() if ":" in title else title

    # Build section outlines
    section_outlines = []
    for i, sec in enumerate(all_sections, start=1):
        section_outlines.append(SectionOutline(
            number=i,
            title=sec["title"],
            key_elements=sec.get("key_elements", []),
            guidance=sec.get("guidance", ""),
        ))

    # Auto-generate subtitle if not provided
    if not subtitle:
        subtitle = f"Global Market Analysis &\nInvestment Outlook"

    return ReportOutline(
        title=title,
        subtitle=subtitle,
        short_title=short_title,
        report_type=report_type,
        sections=section_outlines,
        description=description,
    )


def outline_to_dict(outline: ReportOutline) -> dict:
    """Convert a ReportOutline to a plain dict for template rendering."""
    return {
        "title": outline.title,
        "subtitle": outline.subtitle,
        "short_title": outline.short_title,
        "report_type": outline.report_type,
        "description": outline.description,
        "cover_metrics": outline.cover_metrics,
        "sections": [
            {
                "number": s.number,
                "title": s.title,
                "key_elements": s.key_elements,
                "guidance": s.guidance,
                "subsections": s.subsections,
                "content": "",  # To be populated by the agent
            }
            for s in outline.sections
        ],
    }


def print_outline(outline: ReportOutline) -> str:
    """Pretty-print the outline for agent review."""
    lines = [
        f"Report: {outline.title}",
        f"Subtitle: {outline.subtitle}",
        f"Type: {outline.report_type}",
        f"Sections ({len(outline.sections)}):",
        "",
    ]
    for s in outline.sections:
        lines.append(f"  {s.number}. {s.title}")
        if s.key_elements:
            for elem in s.key_elements:
                lines.append(f"     - {elem}")
        if s.guidance:
            lines.append(f"     [Guidance: {s.guidance}]")
        lines.append("")
    return "\n".join(lines)
