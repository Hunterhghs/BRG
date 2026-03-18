"""
BRG — Business Report Generator
Researcher module — data collection helpers and source management.

This module provides utilities that an AI agent uses during the research phase.
It does NOT perform web searches itself — the agent uses its own tools for that.
Instead, this module provides:
  - Source tracking and formatting
  - Data validation helpers
  - Research prompt generation for each section
"""

from dataclasses import dataclass, field


@dataclass
class Source:
    """A data source used in the report."""
    name: str
    url: str = ""
    date: str = ""
    category: str = ""  # e.g. "government", "industry", "press"


@dataclass
class DataPoint:
    """A verified data point with its source."""
    metric: str
    value: str
    year: str = ""
    source: str = ""


class ResearchBrief:
    """Collects research data for a single report section."""

    def __init__(self, section_title: str):
        self.section_title = section_title
        self.data_points: list[DataPoint] = []
        self.sources: list[Source] = []
        self.notes: list[str] = []
        self.content: str = ""

    def add_data_point(self, metric: str, value: str, year: str = "", source: str = ""):
        self.data_points.append(DataPoint(
            metric=metric, value=value, year=year, source=source
        ))

    def add_source(self, name: str, url: str = "", date: str = "", category: str = ""):
        self.sources.append(Source(
            name=name, url=url, date=date, category=category
        ))

    def add_note(self, note: str):
        self.notes.append(note)

    def set_content(self, html_content: str):
        """Set the final HTML content for this section."""
        self.content = html_content


class ResearchManager:
    """Manages research data across all report sections."""

    def __init__(self):
        self.briefs: dict[str, ResearchBrief] = {}
        self.global_sources: list[Source] = []

    def create_brief(self, section_title: str) -> ResearchBrief:
        brief = ResearchBrief(section_title)
        self.briefs[section_title] = brief
        return brief

    def get_brief(self, section_title: str) -> ResearchBrief:
        return self.briefs.get(section_title)

    def all_data_points(self) -> list[DataPoint]:
        """Return all data points across all sections."""
        points = []
        for brief in self.briefs.values():
            points.extend(brief.data_points)
        return points

    def all_sources(self) -> list[Source]:
        """Return all unique sources across all sections."""
        seen = set()
        sources = list(self.global_sources)
        for brief in self.briefs.values():
            for src in brief.sources:
                key = src.name + src.url
                if key not in seen:
                    seen.add(key)
                    sources.append(src)
        return sources


def generate_research_prompts(section_title: str, key_elements: list[str]) -> list[str]:
    """Generate research search prompts for a section.

    These are suggested search queries the agent can use to gather data.

    Args:
        section_title: The section's title.
        key_elements: List of key data elements needed.

    Returns:
        List of search query strings.
    """
    prompts = []
    for element in key_elements:
        prompts.append(f"{section_title}: {element} latest data statistics")
    return prompts
