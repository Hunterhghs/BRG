"""
BRG — Business Report Generator
Chart generation utilities — produces inline SVG charts for PDF rendering.
All charts are pure SVG, compatible with WeasyPrint (no JavaScript).
"""

from typing import Optional
import html as _html

# Default color palette matching the report theme
PALETTE = [
    "#0f3460",  # deep blue
    "#e94560",  # accent red
    "#16213e",  # dark navy
    "#3a86ff",  # bright blue
    "#8338ec",  # purple
    "#06d6a0",  # teal
    "#ff6b35",  # orange
    "#1b9aaa",  # sea blue
    "#f77f00",  # amber
    "#7209b7",  # violet
]


def _esc(text: str) -> str:
    """Escape text for safe SVG embedding."""
    return _html.escape(str(text))


def render_bar_chart(
    labels: list[str],
    values: list[float],
    title: Optional[str] = None,
    value_prefix: str = "",
    value_suffix: str = "",
    colors: Optional[list[str]] = None,
    height: int = 260,
    width: int = 560,
) -> str:
    """Render a vertical bar chart as inline SVG.

    Args:
        labels: Category labels for each bar.
        values: Numeric values for each bar.
        title: Optional chart title.
        value_prefix: Prefix for value labels (e.g. "$").
        value_suffix: Suffix for value labels (e.g. "B").
        colors: Optional list of bar colors; cycles PALETTE if omitted.
        height: SVG height in px.
        width: SVG width in px.
    """
    colors = colors or PALETTE
    n = len(values)
    if n == 0:
        return ""

    padding_top = 40 if title else 20
    padding_bottom = 50
    padding_left = 50
    padding_right = 20
    chart_w = width - padding_left - padding_right
    chart_h = height - padding_top - padding_bottom

    max_val = max(values) if max(values) > 0 else 1
    bar_width = min(chart_w / n * 0.6, 60)
    gap = chart_w / n

    lines = [f'<div class="chart-wrapper">']
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                 f'viewBox="0 0 {width} {height}" style="font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">')

    # Title
    if title:
        lines.append(f'<text x="{width / 2}" y="18" text-anchor="middle" '
                      f'font-size="11" font-weight="700" fill="#1a1a2e">{_esc(title)}</text>')

    # Y-axis gridlines
    num_gridlines = 5
    for i in range(num_gridlines + 1):
        y = padding_top + chart_h - (i / num_gridlines) * chart_h
        val = max_val * i / num_gridlines
        label = f"{value_prefix}{val:,.0f}{value_suffix}"
        lines.append(f'<line x1="{padding_left}" y1="{y:.1f}" x2="{width - padding_right}" y2="{y:.1f}" '
                      f'stroke="#e8e8e8" stroke-width="0.5"/>')
        lines.append(f'<text x="{padding_left - 6}" y="{y + 3:.1f}" text-anchor="end" '
                      f'font-size="7.5" fill="#888">{_esc(label)}</text>')

    # Baseline
    baseline_y = padding_top + chart_h
    lines.append(f'<line x1="{padding_left}" y1="{baseline_y}" x2="{width - padding_right}" y2="{baseline_y}" '
                  f'stroke="#1a1a2e" stroke-width="1"/>')

    # Bars
    for i, (label, val) in enumerate(zip(labels, values)):
        bar_h = (val / max_val) * chart_h
        x = padding_left + i * gap + (gap - bar_width) / 2
        y = padding_top + chart_h - bar_h
        color = colors[i % len(colors)]

        lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_h:.1f}" '
                      f'fill="{color}" rx="2"/>')

        # Value label above bar
        val_label = f"{value_prefix}{val:,.1f}{value_suffix}" if val != int(val) else f"{value_prefix}{val:,.0f}{value_suffix}"
        lines.append(f'<text x="{x + bar_width / 2:.1f}" y="{y - 5:.1f}" text-anchor="middle" '
                      f'font-size="8" font-weight="700" fill="{color}">{_esc(val_label)}</text>')

        # X-axis label
        lines.append(f'<text x="{x + bar_width / 2:.1f}" y="{baseline_y + 14:.1f}" text-anchor="middle" '
                      f'font-size="8" fill="#444">{_esc(label)}</text>')

    lines.append('</svg>')
    lines.append('</div>')
    return "\n".join(lines)


def render_horizontal_bar_chart(
    labels: list[str],
    values: list[float],
    title: Optional[str] = None,
    value_suffix: str = "%",
    colors: Optional[list[str]] = None,
    height: Optional[int] = None,
    width: int = 560,
    bar_height: int = 22,
) -> str:
    """Render a horizontal bar chart as inline SVG.

    Args:
        labels: Category labels.
        values: Numeric values.
        title: Optional chart title.
        value_suffix: Suffix for value labels.
        colors: Optional bar colors.
        height: Auto-calculated if None.
        width: SVG width.
        bar_height: Height of each bar.
    """
    colors = colors or PALETTE
    n = len(values)
    if n == 0:
        return ""

    padding_top = 35 if title else 15
    row_height = bar_height + 18
    padding_bottom = 10
    label_width = 130
    padding_right = 55
    calc_height = height or (padding_top + n * row_height + padding_bottom)
    bar_area_w = width - label_width - padding_right

    max_val = max(values) if max(values) > 0 else 1

    lines = ['<div class="chart-wrapper">']
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{calc_height}" '
                 f'viewBox="0 0 {width} {calc_height}" style="font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">')

    if title:
        lines.append(f'<text x="{width / 2}" y="18" text-anchor="middle" '
                      f'font-size="11" font-weight="700" fill="#1a1a2e">{_esc(title)}</text>')

    for i, (label, val) in enumerate(zip(labels, values)):
        y = padding_top + i * row_height
        bar_w = (val / max_val) * bar_area_w
        color = colors[i % len(colors)]

        # Label
        lines.append(f'<text x="{label_width - 8}" y="{y + bar_height / 2 + 3:.1f}" text-anchor="end" '
                      f'font-size="8.5" fill="#2c2c2c">{_esc(label)}</text>')

        # Background bar
        lines.append(f'<rect x="{label_width}" y="{y:.1f}" width="{bar_area_w}" height="{bar_height}" '
                      f'fill="#f0f0f0" rx="3"/>')

        # Value bar
        lines.append(f'<rect x="{label_width}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_height}" '
                      f'fill="{color}" rx="3"/>')

        # Value text
        val_text = f"{val:,.1f}{value_suffix}" if val != int(val) else f"{val:,.0f}{value_suffix}"
        lines.append(f'<text x="{label_width + bar_w + 6:.1f}" y="{y + bar_height / 2 + 3:.1f}" '
                      f'text-anchor="start" font-size="8.5" font-weight="700" fill="{color}">{_esc(val_text)}</text>')

    lines.append('</svg>')
    lines.append('</div>')
    return "\n".join(lines)


def render_line_chart(
    labels: list[str],
    series: list[dict],
    title: Optional[str] = None,
    value_prefix: str = "",
    value_suffix: str = "",
    height: int = 260,
    width: int = 560,
    show_area: bool = True,
) -> str:
    """Render a line chart (with optional area fill) as inline SVG.

    Args:
        labels: X-axis labels.
        series: List of dicts with 'name', 'values', and optional 'color'.
            Example: [{"name": "Revenue", "values": [1, 2, 3], "color": "#e94560"}]
        title: Optional chart title.
        value_prefix: Prefix for tooltip values.
        value_suffix: Suffix for tooltip values.
        height: SVG height.
        width: SVG width.
        show_area: If True, fill area under lines.
    """
    if not series or not labels:
        return ""

    padding_top = 40 if title else 20
    padding_bottom = 50
    padding_left = 55
    padding_right = 20
    legend_height = 25
    chart_h = height - padding_top - padding_bottom - legend_height
    chart_w = width - padding_left - padding_right

    all_vals = [v for s in series for v in s["values"]]
    max_val = max(all_vals) if all_vals and max(all_vals) > 0 else 1
    min_val = 0

    n_points = len(labels)
    x_step = chart_w / max(n_points - 1, 1)

    lines = ['<div class="chart-wrapper">']
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                 f'viewBox="0 0 {width} {height}" style="font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">')

    if title:
        lines.append(f'<text x="{width / 2}" y="18" text-anchor="middle" '
                      f'font-size="11" font-weight="700" fill="#1a1a2e">{_esc(title)}</text>')

    # Gridlines
    num_gridlines = 5
    for i in range(num_gridlines + 1):
        y = padding_top + chart_h - (i / num_gridlines) * chart_h
        val = min_val + (max_val - min_val) * i / num_gridlines
        label = f"{value_prefix}{val:,.0f}{value_suffix}"
        lines.append(f'<line x1="{padding_left}" y1="{y:.1f}" x2="{width - padding_right}" y2="{y:.1f}" '
                      f'stroke="#e8e8e8" stroke-width="0.5"/>')
        lines.append(f'<text x="{padding_left - 6}" y="{y + 3:.1f}" text-anchor="end" '
                      f'font-size="7.5" fill="#888">{_esc(label)}</text>')

    # Baseline
    baseline_y = padding_top + chart_h
    lines.append(f'<line x1="{padding_left}" y1="{baseline_y}" x2="{width - padding_right}" y2="{baseline_y}" '
                  f'stroke="#1a1a2e" stroke-width="1"/>')

    # X-axis labels
    for i, label in enumerate(labels):
        x = padding_left + i * x_step
        lines.append(f'<text x="{x:.1f}" y="{baseline_y + 14:.1f}" text-anchor="middle" '
                      f'font-size="8" fill="#444">{_esc(label)}</text>')

    # Plot series
    for si, s in enumerate(series):
        color = s.get("color", PALETTE[si % len(PALETTE)])
        vals = s["values"]
        points = []
        for i, v in enumerate(vals):
            x = padding_left + i * x_step
            y = padding_top + chart_h - ((v - min_val) / (max_val - min_val)) * chart_h
            points.append((x, y))

        # Area fill
        if show_area:
            area_points = [f"{x:.1f},{y:.1f}" for x, y in points]
            area_points.append(f"{points[-1][0]:.1f},{baseline_y:.1f}")
            area_points.append(f"{points[0][0]:.1f},{baseline_y:.1f}")
            lines.append(f'<polygon points="{" ".join(area_points)}" fill="{color}" opacity="0.08"/>')

        # Line
        line_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        lines.append(f'<polyline points="{line_points}" fill="none" stroke="{color}" stroke-width="2.5" '
                      f'stroke-linejoin="round" stroke-linecap="round"/>')

        # Data points
        for i, (x, y) in enumerate(points):
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="white" stroke="{color}" stroke-width="2"/>')

        # Value labels at first and last point
        for idx in [0, len(points) - 1]:
            x, y = points[idx]
            v = vals[idx]
            v_label = f"{value_prefix}{v:,.1f}{value_suffix}" if v != int(v) else f"{value_prefix}{v:,.0f}{value_suffix}"
            lines.append(f'<text x="{x:.1f}" y="{y - 8:.1f}" text-anchor="middle" '
                          f'font-size="7.5" font-weight="700" fill="{color}">{_esc(v_label)}</text>')

    # Legend
    legend_y = height - 12
    total_legend_w = sum(len(s["name"]) * 6 + 30 for s in series)
    legend_x = (width - total_legend_w) / 2
    for si, s in enumerate(series):
        color = s.get("color", PALETTE[si % len(PALETTE)])
        lines.append(f'<rect x="{legend_x:.1f}" y="{legend_y - 6}" width="12" height="8" '
                      f'fill="{color}" rx="1.5"/>')
        lines.append(f'<text x="{legend_x + 16:.1f}" y="{legend_y:.1f}" '
                      f'font-size="8" fill="#444">{_esc(s["name"])}</text>')
        legend_x += len(s["name"]) * 6 + 30

    lines.append('</svg>')
    lines.append('</div>')
    return "\n".join(lines)


def render_donut_chart(
    labels: list[str],
    values: list[float],
    title: Optional[str] = None,
    colors: Optional[list[str]] = None,
    height: int = 240,
    width: int = 560,
    center_label: Optional[str] = None,
    center_value: Optional[str] = None,
) -> str:
    """Render a donut chart as inline SVG.

    Args:
        labels: Segment labels.
        values: Segment values (will be normalized to percentages).
        title: Optional chart title.
        colors: Optional segment colors.
        height: SVG height.
        width: SVG width.
        center_label: Optional text in the donut center (smaller).
        center_value: Optional large value in the donut center.
    """
    import math

    colors = colors or PALETTE
    n = len(values)
    if n == 0:
        return ""

    total = sum(values)
    if total == 0:
        return ""

    padding_top = 30 if title else 10
    cx = width * 0.35
    cy = padding_top + (height - padding_top) / 2
    outer_r = min((height - padding_top - 20) / 2, 90)
    inner_r = outer_r * 0.55

    lines = ['<div class="chart-wrapper">']
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                 f'viewBox="0 0 {width} {height}" style="font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">')

    if title:
        lines.append(f'<text x="{width / 2}" y="18" text-anchor="middle" '
                      f'font-size="11" font-weight="700" fill="#1a1a2e">{_esc(title)}</text>')

    # Draw arcs
    start_angle = -90  # start from top
    for i, (label, val) in enumerate(zip(labels, values)):
        pct = val / total
        angle = pct * 360
        end_angle = start_angle + angle
        color = colors[i % len(colors)]

        # Convert to radians
        sa = math.radians(start_angle)
        ea = math.radians(end_angle)

        # Outer arc points
        ox1 = cx + outer_r * math.cos(sa)
        oy1 = cy + outer_r * math.sin(sa)
        ox2 = cx + outer_r * math.cos(ea)
        oy2 = cy + outer_r * math.sin(ea)

        # Inner arc points
        ix1 = cx + inner_r * math.cos(ea)
        iy1 = cy + inner_r * math.sin(ea)
        ix2 = cx + inner_r * math.cos(sa)
        iy2 = cy + inner_r * math.sin(sa)

        large_arc = 1 if angle > 180 else 0

        path = (f'M {ox1:.1f},{oy1:.1f} '
                f'A {outer_r},{outer_r} 0 {large_arc},1 {ox2:.1f},{oy2:.1f} '
                f'L {ix1:.1f},{iy1:.1f} '
                f'A {inner_r},{inner_r} 0 {large_arc},0 {ix2:.1f},{iy2:.1f} Z')

        lines.append(f'<path d="{path}" fill="{color}"/>')
        start_angle = end_angle

    # Center text
    if center_value:
        lines.append(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" '
                      f'font-size="20" font-weight="700" fill="#1a1a2e">{_esc(center_value)}</text>')
    if center_label:
        lines.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" '
                      f'font-size="8" fill="#666">{_esc(center_label)}</text>')

    # Legend (right side)
    legend_x = width * 0.62
    legend_y_start = padding_top + 30
    row_h = 22

    for i, (label, val) in enumerate(zip(labels, values)):
        pct = val / total * 100
        color = colors[i % len(colors)]
        y = legend_y_start + i * row_h

        lines.append(f'<rect x="{legend_x}" y="{y - 6}" width="10" height="10" fill="{color}" rx="2"/>')
        lines.append(f'<text x="{legend_x + 16}" y="{y + 3}" font-size="8.5" fill="#2c2c2c">'
                      f'{_esc(label)}</text>')
        lines.append(f'<text x="{width - 25}" y="{y + 3}" text-anchor="end" '
                      f'font-size="8.5" font-weight="700" fill="{color}">{pct:.1f}%</text>')

    lines.append('</svg>')
    lines.append('</div>')
    return "\n".join(lines)


def render_stat_bars(
    items: list[dict],
    title: Optional[str] = None,
    width: int = 560,
    bar_color: str = "#0f3460",
    bg_color: str = "#e8ecef",
) -> str:
    """Render a set of labeled progress/stat bars.

    Args:
        items: List of dicts with 'label', 'value' (numeric 0–100), 'display' (shown text).
            Example: [{"label": "North America", "value": 38, "display": "38%"}]
        title: Optional title above the bars.
        width: SVG width.
        bar_color: Fill color for the bars.
        bg_color: Background track color.
    """
    n = len(items)
    if n == 0:
        return ""

    padding_top = 30 if title else 10
    row_h = 36
    calc_height = padding_top + n * row_h + 10
    label_w = 130
    bar_start = label_w + 5
    bar_w = width - bar_start - 60
    bar_h = 14

    lines = ['<div class="chart-wrapper">']
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{calc_height}" '
                 f'viewBox="0 0 {width} {calc_height}" style="font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">')

    if title:
        lines.append(f'<text x="{width / 2}" y="18" text-anchor="middle" '
                      f'font-size="11" font-weight="700" fill="#1a1a2e">{_esc(title)}</text>')

    for i, item in enumerate(items):
        y = padding_top + i * row_h
        fill_w = (item["value"] / 100) * bar_w

        # Label
        lines.append(f'<text x="{label_w - 4}" y="{y + bar_h / 2 + 3:.1f}" text-anchor="end" '
                      f'font-size="8.5" fill="#2c2c2c">{_esc(item["label"])}</text>')

        # Background track
        lines.append(f'<rect x="{bar_start}" y="{y:.1f}" width="{bar_w}" height="{bar_h}" '
                      f'fill="{bg_color}" rx="3"/>')

        # Fill bar
        lines.append(f'<rect x="{bar_start}" y="{y:.1f}" width="{fill_w:.1f}" height="{bar_h}" '
                      f'fill="{bar_color}" rx="3"/>')

        # Display value
        lines.append(f'<text x="{bar_start + bar_w + 8:.1f}" y="{y + bar_h / 2 + 3:.1f}" '
                      f'text-anchor="start" font-size="9" font-weight="700" fill="{bar_color}">'
                      f'{_esc(item["display"])}</text>')

    lines.append('</svg>')
    lines.append('</div>')
    return "\n".join(lines)


def render_key_findings(
    findings: list[str],
    title: str = "Key Findings",
) -> str:
    """Render a visually distinct key findings callout box.

    Args:
        findings: List of finding strings.
        title: Box title.

    Returns:
        HTML string for the key findings box.
    """
    items_html = "\n".join(
        f'        <li><span class="finding-icon">&#9656;</span> {_esc(f)}</li>'
        for f in findings
    )
    return f"""<div class="key-findings">
    <div class="key-findings-header">
        <span class="key-findings-icon">&#9670;</span> {_esc(title)}
    </div>
    <ul class="key-findings-list">
{items_html}
    </ul>
</div>"""


def render_comparison_cards(
    cards: list[dict],
) -> str:
    """Render side-by-side comparison cards.

    Args:
        cards: List of dicts with 'title', 'value', 'subtitle', optional 'change' (e.g. "+25%"),
               optional 'change_positive' (bool).

    Returns:
        HTML string for the comparison card row.
    """
    card_items = []
    for c in cards:
        change_html = ""
        if c.get("change"):
            cls = "positive" if c.get("change_positive", True) else "negative"
            change_html = f'<div class="comparison-change {cls}">{_esc(c["change"])}</div>'

        card_items.append(f"""<div class="comparison-card">
    <div class="comparison-title">{_esc(c['title'])}</div>
    <div class="comparison-value">{_esc(c['value'])}</div>
    <div class="comparison-subtitle">{_esc(c.get('subtitle', ''))}</div>
    {change_html}
</div>""")

    return f'<div class="comparison-row">\n' + "\n".join(card_items) + '\n</div>'
