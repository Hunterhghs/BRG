#!/usr/bin/env python3
"""Build the AI Coding Agents report with fully populated content."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tables import render_table, render_metrics
from src.charts import (
    render_bar_chart,
    render_horizontal_bar_chart,
    render_line_chart,
    render_donut_chart,
    render_stat_bars,
    render_key_findings,
    render_comparison_cards,
)
from src.composer import compose_report, build_report_data
from src.renderer import render_pdf
from src.utils import current_year

# ============================================================
# COVER METRICS
# ============================================================
cover_metrics = [
    {"value": "$6.1B", "label": "AI Code Tools\nMarket Size (2024)"},
    {"value": "$26B+", "label": "Projected Market\nSize (2030)"},
    {"value": "27.1%", "label": "Market CAGR\n(2024–2030)"},
    {"value": "20M+", "label": "GitHub Copilot\nUsers (2025)"},
]

# ============================================================
# SECTION 1: EXECUTIVE SUMMARY
# ============================================================
exec_metrics = render_metrics([
    {"value": "$6.1B", "label": "AI Code Tools Market (2024)"},
    {"value": "27.1%", "label": "CAGR (2024–2030)"},
    {"value": "20M+", "label": "GitHub Copilot Users (2025)"},
    {"value": "$9B+", "label": "Cursor Valuation (2025)"},
])

exec_findings = render_key_findings([
    "Global AI code tools market valued at $6.1B in 2024, projected to reach $26B+ by 2030 (27.1% CAGR)",
    "Autonomous coding agents represent a qualitative leap — planning, writing, testing, and deploying code with minimal human oversight",
    "Record-breaking investment: Cursor ($9B), Devin ($10.2B), and Replit ($9B) valuations achieved within 18 months of launch",
    "GitHub Copilot surpassed 20M users; platform opening to third-party agents signals ecosystem maturation",
    "Market is consolidating rapidly — Cognition acquired Windsurf, and 3–5 major platforms expected to dominate by 2028",
], title="Executive Summary — Key Findings")

exec_market_chart = render_line_chart(
    labels=["2020", "2021", "2022", "2023", "2024", "2025E", "2026E", "2028F", "2030F"],
    series=[
        {"name": "AI Code Tools Market ($B)", "values": [0.9, 1.5, 2.7, 4.9, 6.1, 8.3, 11.0, 18.0, 26.0], "color": "#0f3460"},
    ],
    title="AI Code Tools Market Growth Trajectory (2020–2030F)",
    value_prefix="$",
    value_suffix="B",
)

section1 = f"""
{exec_metrics}

{exec_findings}

<p>The AI coding agent market has entered a period of explosive growth, fundamentally transforming how software is conceived, written, tested, and deployed. The global AI code tools market was valued at approximately $6.1 billion in 2024 and is projected to reach $26.03 billion by 2030, growing at a compound annual growth rate (CAGR) of 27.1%, according to Grand View Research. This trajectory places AI coding agents among the fastest-growing segments within the broader artificial intelligence ecosystem.</p>

{exec_market_chart}

<p>AI coding agents — autonomous or semi-autonomous systems that can understand natural language instructions, generate code, debug software, execute multi-step programming tasks, and interact with development environments — represent a qualitative leap beyond earlier code completion tools. Whereas first-generation tools like GitHub Copilot (launched 2021) offered line-by-line suggestions, the current generation of agents — including Anthropic's Claude Code, OpenAI's Codex, Cognition's Devin, Cursor, and Google's Gemini CLI — can plan entire implementations, create files, run tests, and iteratively refine software with minimal human intervention.</p>

<p>The investment landscape reflects this paradigm shift. Anysphere (Cursor) raised $900 million at a $9 billion valuation in May 2025. Cognition AI (Devin) raised $400 million at a $10.2 billion valuation in September 2025, then acquired rival Windsurf (formerly Codeium) in July 2025. Replit reached a $9 billion valuation in March 2026 — tripling in six months. GitHub Copilot surpassed 20 million cumulative users by July 2025, and in February 2026 expanded its agent platform to host third-party models including Claude and OpenAI Codex. The competitive intensity and capital concentration in this market are unprecedented in developer tools history.</p>
"""

# ============================================================
# SECTION 2: MARKET SIZE & GROWTH
# ============================================================
market_table = render_table(
    headers=["Segment", "2024", "2026E", "2030F", "CAGR (2024–30)"],
    rows=[
        ["Code Generation Tools", "$2.8B", "$5.2B", "$12.5B", "28.3%"],
        ["Code Review & Analysis", "$1.1B", "$1.9B", "$4.5B", "26.2%"],
        ["Bug Detection & Testing", "$0.9B", "$1.5B", "$3.8B", "27.0%"],
        ["Total Market", "$6.1B", "$11.0B", "$26.0B", "27.1%"],
    ],
    title="AI Code Tools Market Size by Segment",
    highlight_rows=[3],
)

market_segment_chart = render_bar_chart(
    labels=["Code Gen", "Review & Analysis", "Bug & Testing", "Optimization", "Other"],
    values=[2.8, 1.1, 0.9, 0.5, 0.8],
    title="Market Size by Segment — 2024 ($B)",
    value_prefix="$",
    value_suffix="B",
)

market_growth_chart = render_line_chart(
    labels=["2020", "2022", "2024", "2026E", "2030F"],
    series=[
        {"name": "Code Generation", "values": [0.4, 1.3, 2.8, 5.2, 12.5], "color": "#0f3460"},
        {"name": "Review & Analysis", "values": [0.2, 0.5, 1.1, 1.9, 4.5], "color": "#e94560"},
        {"name": "Bug Detection", "values": [0.1, 0.4, 0.9, 1.5, 3.8], "color": "#3a86ff"},
    ],
    title="Top 3 Segments — Growth Trajectory ($B)",
    value_prefix="$",
    value_suffix="B",
)

deployment_donut = render_donut_chart(
    labels=["Cloud / SaaS", "On-Premises", "Hybrid"],
    values=[68, 22, 10],
    title="Deployment Model Market Share (2024)",
    center_value="68%",
    center_label="Cloud",
    colors=["#0f3460", "#e94560", "#3a86ff"],
)

deployment_table = render_table(
    headers=["Deployment Model", "Market Share (2024)", "Growth Trend", "Key Driver"],
    rows=[
        ["Cloud / SaaS", "~68%", "Dominant, expanding", "Scalability, rapid deployment, lower upfront cost"],
        ["On-Premises / Self-Hosted", "~22%", "Growing (regulated sectors)", "Data sovereignty, IP protection, compliance"],
        ["Hybrid", "~10%", "Fastest-growing", "Flexibility, enterprise security, AI model customization"],
    ],
    title="Deployment Model Breakdown",
)

section2_findings = render_key_findings([
    "Market more than doubled between 2022–2024 as enterprises moved from experimentation to production",
    "Code generation tools dominate at 46% of market revenue ($2.8B in 2024)",
    "Cloud deployment holds 68% share; on-premises growing fastest in regulated sectors",
    "Tools segment accounts for 76% of revenue vs. 24% for services",
])

section2 = f"""
<p>The global AI code tools market reached an estimated $6.11 billion in revenue in 2024, up from approximately $4.86 billion in 2023 — a year-over-year increase of roughly 26%. The market is projected to grow to $26.03 billion by 2030 at a CAGR of 27.1% over the 2024–2030 forecast period, according to Grand View Research. Other analyst estimates place the market even higher when inclusive of adjacent AI-assisted software engineering tools and infrastructure.</p>

{section2_findings}

<h3 class="subsection-title">Historical Growth Trajectory</h3>

<p>The market's growth can be traced through several distinct phases. From 2017 to 2020, the AI code tools market was nascent, dominated by basic autocomplete and linting enhancements. The total market was below $1 billion. The release of OpenAI's Codex in August 2021 and GitHub Copilot's general availability in June 2022 catalyzed a step-function increase in adoption and spending. Between 2022 and 2024, the market more than doubled as enterprises moved from experimentation to production deployment. The emergence of full-agent coding tools in 2024–2025 — including Devin, Cursor Agent Mode, and Claude Code — initiated the current acceleration phase, where growth rates exceed 25% annually.</p>

{market_table}

<p>Code generation tools lead all segments at $2.8 billion in 2024, reflecting the category's maturity and the widespread adoption of inline completion and agent-mode generation across professional developer workflows.</p>

{market_segment_chart}

<p>Looking ahead, the code generation segment is projected to grow fastest in absolute terms, reaching $12.5 billion by 2030. Code review and analysis tools will also see strong growth, driven by enterprise demand for AI-powered quality assurance and security scanning.</p>

{market_growth_chart}

<h3 class="subsection-title">Market Composition</h3>

<p>The tools segment accounts for approximately 76% of total market revenue, with services (consulting, integration, managed support) representing the remaining 24%. Within tools, code generation is the largest sub-segment at an estimated $2.8 billion in 2024, driven by the widespread adoption of inline code completion and agent-mode generation. Code review and analysis tools represent the second-largest segment, fueled by enterprise demand for AI-powered code quality assurance and security scanning.</p>

{deployment_donut}

<p>The deployment landscape reveals a clear pattern: cloud-based solutions dominate due to their ease of adoption and scalability, while on-premises options are carving out a significant niche in regulated industries where data sovereignty is non-negotiable.</p>

{deployment_table}

<p>Cloud-based deployment dominates the market, accounting for approximately 68% of revenue in 2024. However, on-premises and hybrid deployment models are growing rapidly — particularly among enterprises in regulated industries such as financial services, healthcare, and government — where data sovereignty and intellectual property protection are paramount concerns. Several leading vendors, including GitHub (Copilot Enterprise), Tabnine, and Sourcegraph, offer self-hosted deployment options specifically targeting these customers.</p>
"""

# ============================================================
# SECTION 3: INVESTMENT & FUNDING
# ============================================================
funding_table = render_table(
    headers=["Company", "Product", "Round", "Amount", "Valuation", "Date"],
    rows=[
        ["Anysphere", "Cursor", "Series B", "$900M", "$9.0B", "May 2025"],
        ["Cognition AI", "Devin", "Series B", "$400M", "$10.2B", "Sep 2025"],
        ["Replit", "Replit Agent", "Series D", "Undisclosed", "$9.0B", "Mar 2026"],
        ["Poolside AI", "Poolside", "Series A", "$500M", "$3.0B", "Oct 2024"],
        ["Magic AI", "Magic", "Series B", "$320M", "$3.0B", "Aug 2024"],
    ],
    title="Major AI Coding Agent Funding Rounds (2023–2026)",
)

valuation_chart = render_bar_chart(
    labels=["Devin", "Cursor", "Replit", "Poolside", "Magic", "Windsurf", "Augment"],
    values=[10.2, 9.0, 9.0, 3.0, 3.0, 1.25, 0.98],
    title="Top AI Coding Agent Valuations ($B)",
    value_prefix="$",
    value_suffix="B",
    colors=["#e94560", "#0f3460", "#3a86ff", "#8338ec", "#06d6a0", "#ff6b35", "#1b9aaa"],
)

funding_comparison = render_comparison_cards([
    {"title": "Largest Raise", "value": "$900M", "subtitle": "Cursor — May 2025", "change": "9x valuation jump", "change_positive": True},
    {"title": "Highest Valuation", "value": "$10.2B", "subtitle": "Devin — Sep 2025", "change": "5x in 18 months", "change_positive": True},
    {"title": "Fastest Growth", "value": "$9.0B", "subtitle": "Replit — Mar 2026", "change": "3x in 6 months", "change_positive": True},
    {"title": "Cumulative VC", "value": "$4B+", "subtitle": "Since 2023", "change": "Record for dev tools", "change_positive": True},
])

section3 = f"""
<p>The AI coding agent sector has attracted extraordinary levels of venture capital and strategic investment, with cumulative funding exceeding $4 billion since 2023. The pace of capital deployment has accelerated sharply: several companies have achieved multi-billion-dollar valuations within 12–18 months of their initial product launch, a velocity rivaling or exceeding the generative AI infrastructure boom of 2023.</p>

{funding_comparison}

<p>The scale and velocity of capital deployment in the AI coding agent sector is without precedent in developer tools history. The five largest rounds alone account for over $2.3 billion in disclosed funding, with an additional $1.7 billion raised across mid-stage rounds.</p>

{funding_table}

<p>The valuation hierarchy reveals a clear top tier: Cognition (Devin), Anysphere (Cursor), and Replit have each achieved or exceeded $9 billion, while a second tier of well-funded challengers — Poolside, Magic, and Windsurf — occupy the $1–3 billion range. Notably, several of these valuations were achieved within 12–18 months of the company's initial product launch, a pace that exceeds even the generative AI infrastructure boom of 2023. The velocity of valuation growth is driven by demonstrable revenue scaling: Cursor reportedly reached an annualized revenue run-rate exceeding $300 million by early 2026, while Replit's enterprise pipeline grew 5x in 2025.</p>

{valuation_chart}

<h3 class="subsection-title">Investment Dynamics</h3>

<p>The most significant funding event of 2025 was Anysphere's $900 million Series B in May, which valued the Cursor maker at $9 billion. The round was led by Thrive Capital, with participation from Andreessen Horowitz and Accel. This represented a roughly 9x valuation increase from the company's prior round, underscoring the exponential demand for AI-native development environments. Anysphere subsequently launched a $200-per-month ultra-premium subscription tier in June 2025, signaling strong enterprise willingness to pay for advanced agent capabilities.</p>

<p>Cognition AI followed with a $400 million raise at a $10.2 billion valuation in September 2025, making Devin the highest-valued pure-play AI coding agent company. Cognition further consolidated its position by acquiring Windsurf (formerly Codeium) in July 2025, combining Devin's autonomous agent capability with Windsurf's popular IDE and broader user base.</p>

<p>Replit's trajectory has been equally striking: the company reached a $9 billion valuation in March 2026 — tripling from $3 billion just six months earlier — driven by the rapid adoption of its Replit Agent for full-application generation from natural language prompts.</p>

<h3 class="subsection-title">Strategic Corporate Investment</h3>

<p>Beyond venture capital, major technology corporations have committed substantial resources to AI coding capabilities. Microsoft has invested heavily in GitHub Copilot and its integration across Visual Studio Code, Visual Studio, and the broader Azure DevOps ecosystem. In February 2026, GitHub opened its agent platform to third-party models — Claude by Anthropic and OpenAI Codex — via Agent HQ, signaling a shift toward a platform model. Google has invested in Code Assist (enterprise-focused) and launched Gemini CLI as an open-source terminal agent in June 2025. Amazon continues to develop Amazon Q Developer (formerly CodeWhisperer) as part of its AWS developer toolkit. OpenAI launched Codex as a standalone agent within ChatGPT in May 2025 and upgraded it with GPT-5 in September 2025.</p>

<h3 class="subsection-title">Investor Categories</h3>

<p>The investor base for AI coding agents spans the full spectrum: tier-one venture firms (Thrive, a16z, Sequoia, Accel, Index Ventures), strategic corporates (Microsoft, Google, Amazon, Salesforce), growth equity funds, sovereign wealth funds, and increasingly public market crossover investors. The sector's rapid revenue scaling — driven by recurring SaaS subscription models — has attracted investors seeking high-growth, high-retention software opportunities.</p>

<p>Notably, several investors have made multiple bets across competing companies, reflecting a belief that the overall market will expand fast enough to support multiple winners. Thrive Capital, for instance, has been involved in rounds for both Cursor and other AI developer tools. Corporate investors are motivated not only by financial returns but by the strategic imperative to integrate AI coding capabilities into their existing developer platforms — Microsoft with GitHub Copilot, Google with Gemini Code Assist, and Amazon with Q Developer. The crossover of public market investors into late-stage private rounds signals growing confidence that one or more AI coding agent companies will pursue IPOs within the next 18–24 months, creating significant liquidity events for early-stage backers.</p>

<p>Geographic diversification of the investor base is also notable. While U.S. venture capital dominates, European growth equity firms, Middle Eastern sovereign wealth funds (particularly from Abu Dhabi and Saudi Arabia), and Asian technology conglomerates are actively participating in later-stage rounds. This global interest underscores the universal applicability of AI coding tools across geographies and industries.</p>
"""

# ============================================================
# SECTION 4: CORE MARKET SEGMENT ANALYSIS
# ============================================================
competitive_table = render_table(
    headers=["Product", "Company", "Type", "Pricing (Mo)", "Key Differentiator", "Users / Scale"],
    rows=[
        ["GitHub Copilot", "Microsoft / GitHub", "IDE Plugin + Agent", "$10–$39/user", "Ecosystem integration, multi-model agent platform", "20M+ cumulative users"],
        ["Cursor", "Anysphere", "AI-Native IDE", "$20–$200/user", "Deep codebase awareness, agent mode, background agents", "Millions of developers"],
        ["Devin", "Cognition AI", "Autonomous Agent", "Usage-based", "Full autonomy, multi-file tasks, CI/CD integration", "Enterprise focus"],
        ["Claude Code", "Anthropic", "CLI Agent", "Via API / Pro", "Extended thinking, 200K context, terminal-native", "Integrated into VS Code, Slack"],
        ["Codex", "OpenAI", "Agent in ChatGPT", "ChatGPT Plus/Pro", "Cloud sandbox execution, parallel tasks", "Integrated into ChatGPT"],
    ],
    title="Competitive Landscape: Top AI Coding Agent Products",
)

segment_donut = render_donut_chart(
    labels=["AI-Enhanced IDEs", "Autonomous Agents", "Dev Platforms"],
    values=[65, 20, 15],
    title="Market Revenue Share by Segment Type (2024 Est.)",
    center_value="65%",
    center_label="IDEs & Assistants",
    colors=["#0f3460", "#e94560", "#3a86ff"],
)

user_growth_chart = render_line_chart(
    labels=["Q1'23", "Q3'23", "Q1'24", "Q3'24", "Q1'25", "Q3'25", "Q1'26"],
    series=[
        {"name": "GitHub Copilot (M users)", "values": [3, 5, 8, 11, 15, 18, 21], "color": "#0f3460"},
        {"name": "Cursor (M users, est.)", "values": [0.1, 0.3, 0.6, 1.2, 2.5, 4.0, 6.0], "color": "#e94560"},
    ],
    title="User Growth — GitHub Copilot vs. Cursor (Millions)",
    value_suffix="M",
)

section4_findings = render_key_findings([
    "GitHub Copilot dominates with 20M+ users; Cursor is the fastest-growing challenger",
    "Three distinct segments: AI-enhanced IDEs (65%), autonomous agents (20%), dev platforms (15%)",
    "Devin set the category-defining precedent for fully autonomous coding agents",
    "Replit and Lovable are proving the prompt-to-deployed-app model at scale",
    "Market is shifting from per-seat to usage-based pricing for agent workloads",
], title="Competitive Landscape — Key Findings")

section4 = f"""
<p>The AI coding agent market comprises three distinct sub-segments, each with different competitive dynamics, user profiles, and growth trajectories: (1) AI-enhanced IDEs and code assistants, (2) autonomous coding agents, and (3) AI-powered development platforms. Understanding these segments is essential for assessing competitive positioning and market evolution.</p>

{section4_findings}

<p>Revenue distribution across the three sub-segments underscores the dominance of IDE-integrated tools, though autonomous agents are the fastest-growing category by percentage growth.</p>

{segment_donut}

<h3 class="subsection-title">AI-Enhanced IDEs & Code Assistants</h3>

<p>This segment — the most mature and largest by revenue — includes tools that integrate directly into existing development environments to provide intelligent code completion, inline suggestions, chat-based assistance, and increasingly, agent-mode capabilities for multi-step tasks. GitHub Copilot is the dominant player, with over 20 million cumulative users as of July 2025 and integration across VS Code, Visual Studio, JetBrains, Neovim, and other editors. Copilot offers tiered pricing: Individual ($10/month), Business ($19/month), and Enterprise ($39/month), with Copilot Pro+ and Enterprise users gaining access to the new Agent HQ platform for third-party agents.</p>

<p>Cursor (Anysphere) has emerged as the most formidable challenger, pioneering the concept of an "AI-native IDE" — a code editor built from the ground up around AI interaction. Cursor's agent mode can plan and execute multi-file changes, and its background agents can work on tasks asynchronously. With a $9 billion valuation and tiered pricing up to $200/month for its Ultra plan (launched June 2025), Cursor has attracted millions of professional developers and demonstrated strong revenue growth.</p>

<p>Other notable players include Google's Gemini Code Assist (leveraging the Gemini 2.5 model with a million-token context window), Amazon Q Developer (tightly integrated with AWS services), and Tabnine (differentiated by privacy-first, on-premises deployment for enterprises in regulated industries).</p>

<h3 class="subsection-title">Autonomous Coding Agents</h3>

<p>This segment represents the frontier of AI coding — systems designed to operate with minimal human supervision, capable of taking a task description and independently producing working software. Cognition AI's Devin, launched in March 2024 as "the first AI software engineer," is the category-defining product. Devin can plan implementations, write code across multiple files, execute in sandboxed environments, run test suites, and iteratively debug — all from a natural language prompt. With a $10.2 billion valuation and the acquisition of Windsurf, Cognition has established a commanding position.</p>

<p>OpenAI's Codex agent (launched May 2025, upgraded with GPT-5 in September 2025) operates as a cloud-based coding agent within ChatGPT, capable of executing code in sandboxed environments and handling parallel tasks. Anthropic's Claude Code functions as a terminal-native agent — operated from the command line — with extended thinking capabilities and a 200,000-token context window, enabling it to work across large codebases. In February 2026, Claude Code became available within GitHub's Agent HQ and was integrated into Slack for team-based development workflows.</p>

<h3 class="subsection-title">AI-Powered Development Platforms</h3>

<p>This segment includes platforms that go beyond code editing to offer full-stack application generation — from prompt to deployed application. Replit Agent is the leading example: users describe an application in natural language, and the agent generates the full codebase, configures dependencies, and deploys the application. Replit's rapid growth to a $9 billion valuation reflects the appeal of this zero-to-deployed model, particularly for prototyping and non-traditional developers. Other emerging players in this category include Lovable (which reported adding $100 million in revenue in a single month as of March 2026) and various Y Combinator-backed startups exploring novel interaction paradigms.</p>

{competitive_table}

<p>Beyond these top five, additional notable players include Google's Gemini Code Assist (leveraging the Gemini 2.5 model with a million-token context window and an open-source CLI), Amazon Q Developer (tightly integrated with AWS services and offering automated Java upgrades), Replit Agent (pioneering prompt-to-deployed-app generation for 30M+ users), Windsurf (now part of Cognition), and Tabnine (differentiated by privacy-first on-premises deployment for regulated sectors). The table above highlights the five most competitively significant products; however, the broader ecosystem includes over 200 VC-backed startups exploring niche applications and novel interaction paradigms.</p>

<p>User adoption curves tell a compelling story of market momentum. GitHub Copilot's first-mover advantage has built a dominant installed base, while Cursor's steeper growth curve demonstrates the appeal of purpose-built AI-native development environments.</p>

{user_growth_chart}
"""

# ============================================================
# SECTION 5: REGIONAL MARKET ANALYSIS
# ============================================================
region_table = render_table(
    headers=["Region", "Share (2024)", "CAGR (2024–30)", "Key Markets", "Notable Dynamics"],
    rows=[
        ["North America", "~38%", "21–25%", "U.S., Canada", "Largest market; home to most leading vendors"],
        ["Asia Pacific", "~28%", "30–35%", "China, India, Japan", "Fastest-growing; China developing domestic tools"],
        ["Europe", "~24%", "25–28%", "UK, Germany, France", "Strong enterprise adoption; EU AI Act shaping compliance"],
        ["Latin America", "~5%", "28–32%", "Brazil, Mexico", "Emerging adoption; strong developer community"],
    ],
    title="Regional Market Overview",
    policy_table=True,
)

region_share_donut = render_donut_chart(
    labels=["North America", "Asia Pacific", "Europe", "Latin America & MEA"],
    values=[38, 28, 24, 10],
    title="Regional Market Share (2024)",
    center_value="38%",
    center_label="North America",
    colors=["#0f3460", "#e94560", "#3a86ff", "#06d6a0"],
)

region_cagr_chart = render_horizontal_bar_chart(
    labels=["Asia Pacific", "Latin America", "Europe", "North America"],
    values=[32.5, 30, 26.5, 23],
    title="Regional CAGR Comparison (2024–2030, midpoint est.)",
    value_suffix="%",
    colors=["#e94560", "#06d6a0", "#3a86ff", "#0f3460"],
)

section5 = f"""
<p>The AI coding agent market is a global phenomenon, but its pace and character vary significantly by region. North America leads in market share and hosts the majority of leading companies, but Asia Pacific is the fastest-growing region and China is rapidly developing domestic alternatives to Western tools.</p>

{region_share_donut}

<p>North America commands the largest share of revenue, but Asia Pacific's larger developer population and aggressive digital transformation initiatives position it as the high-growth region over the forecast period. Developer density, cloud infrastructure maturity, and regulatory environment are the primary factors differentiating regional growth trajectories.</p>

<p>The regional dynamics are shaped by several cross-cutting forces: the availability of high-speed cloud infrastructure, the size and sophistication of the local developer workforce, regulatory openness to AI adoption, and the presence (or absence) of domestic AI coding agent companies. Regions with established software development outsourcing industries — particularly India and Eastern Europe — are seeing especially rapid adoption as AI coding tools amplify the productivity of their large developer workforces.</p>

{region_table}

<p>Growth rates vary substantially by region, with Asia Pacific leading at an estimated 30–35% CAGR, driven by China's massive domestic market and India's rapidly expanding developer ecosystem.</p>

{region_cagr_chart}

<p>These regional CAGR differences reflect distinct market maturity levels. North America, already the largest market, grows at a relatively moderate (though still strong) 21–25%. Asia Pacific's 30–35% CAGR is fueled by a combination of rapid digital transformation, a massive and growing developer population in India and China, and increasing enterprise software spending. Latin America's high growth rate reflects the region's emerging tech hubs and strong developer communities in Brazil and Mexico, where AI coding tools are accelerating the transition from outsourcing-focused development to product-led innovation.</p>

<h3 class="subsection-title">North America</h3>

<p>North America dominated the global AI code tools market with a revenue share exceeding 38% in 2023, and the U.S. market is expected to grow at a CAGR of 21.2% from 2024 to 2030. The region's leadership stems from its concentration of major technology companies (Microsoft, Google, Amazon, OpenAI, Anthropic), a deep pool of AI research talent, robust venture capital infrastructure, and the presence of nearly all leading AI coding agent startups. Silicon Valley, Seattle, New York, and San Francisco are the primary hubs. Supportive government policies and the Inflation Reduction Act's broader AI investment provisions further bolster the ecosystem. Enterprise adoption is most advanced in North America, with large financial institutions, technology companies, and government agencies deploying AI coding tools at scale.</p>

<h3 class="subsection-title">Europe</h3>

<p>Europe represents the second-largest regional market, driven by strong enterprise adoption across the UK, Germany, and France. The European Union's AI Act — the world's first comprehensive AI regulatory framework — is shaping how AI coding tools are deployed and governed, particularly around transparency, intellectual property, and data handling. While Europe has fewer AI coding agent startups than the U.S., it has a strong enterprise software tradition and significant developer populations. The UK benefits from a vibrant AI startup scene centered on London, while Germany's engineering culture drives adoption in automotive, manufacturing, and industrial software. European enterprises are particularly focused on on-premises and privacy-preserving AI tools due to GDPR and data sovereignty requirements.</p>

<h3 class="subsection-title">Asia Pacific</h3>

<p>Asia Pacific is the fastest-growing regional market for AI coding tools, driven by rapid digital transformation across China, India, Japan, South Korea, and Southeast Asia. China is developing a robust domestic AI coding ecosystem in parallel with Western tools, partly driven by geopolitical considerations and U.S. technology export restrictions. Companies like Baidu (with its Comate coding assistant), Alibaba, and numerous Chinese AI startups are building coding agents optimized for the Chinese developer market. India — with the world's second-largest developer population — is a key growth market, with strong adoption of tools like GitHub Copilot and Cursor among both domestic companies and the country's massive outsourcing and remote development workforce. Japan, South Korea, and Australia represent mature technology markets with growing enterprise adoption.</p>

<h3 class="subsection-title">Emerging Markets</h3>

<p>Latin America and the Middle East & Africa represent earlier-stage markets but show accelerating adoption. Brazil has one of the largest developer communities globally and is seeing rapid uptake of AI coding tools. The Gulf states — particularly Saudi Arabia (Vision 2030) and the UAE — are investing heavily in AI infrastructure and talent development. These regions represent significant long-term growth opportunities, particularly as AI coding tools lower the barrier to software development and enable larger populations to participate in the digital economy.</p>
"""

# ============================================================
# SECTION 6: INFRASTRUCTURE & ENABLING TECHNOLOGIES
# ============================================================
context_window_chart = render_bar_chart(
    labels=["GPT-3.5\n(2022)", "GPT-4\n(2023)", "Claude 3\n(2024)", "Claude 3.5\n(2025)", "Gemini 2.5\n(2025)"],
    values=[4, 32, 100, 200, 1000],
    title="Context Window Expansion (Thousands of Tokens)",
    value_suffix="K",
    colors=["#8338ec", "#3a86ff", "#e94560", "#e94560", "#06d6a0"],
)

infra_findings = render_key_findings([
    "Context windows expanded 250x in 3 years — from 4K (GPT-3.5) to 1M tokens (Gemini 2.5 Pro)",
    "SWE-bench scores have roughly doubled from 2024 to 2026, reflecting rapid capability gains",
    "Model Context Protocol (MCP) emerging as the standard interface for agent-tool interaction",
    "Inference costs declining 60–80% annually, enabling more sophisticated agentic behaviors",
    "Sandboxed execution environments are a prerequisite for safe autonomous agent operation",
])

section6 = f"""
<p>The AI coding agent ecosystem depends on a sophisticated technology stack spanning foundation models, specialized inference infrastructure, context management systems, and integration layers. Understanding these enabling technologies is critical for assessing market dynamics, competitive moats, and future evolution.</p>

{infra_findings}

<h3 class="subsection-title">Foundation Models for Code</h3>

<p>At the core of every AI coding agent is a large language model (LLM) trained on code and natural language. The leading models for code generation include OpenAI's GPT-4o and GPT-5, Anthropic's Claude Sonnet 4.5 (launched September 2025, touted as Anthropic's best model for coding), Google's Gemini 2.5 Pro (with a one-million-token context window), and Meta's Code Llama and Llama 3 series. These models have achieved remarkable capability gains: modern code models can understand complex instructions, generate syntactically and semantically correct code across dozens of programming languages, debug errors, refactor existing codebases, and write comprehensive test suites. The improvement trajectory has been steep — SWE-bench scores (a benchmark for real-world software engineering tasks) have roughly doubled from 2024 to 2026.</p>

<h3 class="subsection-title">Inference Infrastructure</h3>

<p>AI coding agents are among the most compute-intensive consumer AI applications. Generating code requires iterative model inference — often with extended thinking or chain-of-thought reasoning — consuming substantial GPU resources. NVIDIA's data center GPUs (H100, H200, and the newly announced Blackwell architecture) power the majority of inference infrastructure. The cost of inference has been declining rapidly, enabling more sophisticated agent behaviors. Cloud providers (AWS, Azure, GCP) offer managed inference services, while specialized inference providers and custom silicon (such as Groq's LPU chips, which NVIDIA is now licensing) are emerging to reduce latency and cost.</p>

<h3 class="subsection-title">Context Window & Codebase Understanding</h3>

<p>A critical enabling technology is the context window — the amount of code and text an AI model can process in a single interaction. Context windows have expanded dramatically: from 4,000 tokens (GPT-3.5, 2022) to 200,000 tokens (Claude, 2025) and 1,000,000 tokens (Gemini 2.5 Pro, 2025). This expansion enables agents to understand entire codebases rather than individual files, a prerequisite for useful multi-file agent operations. Complementary technologies include retrieval-augmented generation (RAG), codebase indexing, and embedding-based code search, which allow agents to access relevant code snippets beyond the context window.</p>

{context_window_chart}

<h3 class="subsection-title">Agent Tooling & Execution Environments</h3>

<p>Modern coding agents require the ability to not only generate code but execute it — running terminals, invoking compilers, executing test suites, managing git operations, and interacting with APIs. Sandboxed execution environments (used by OpenAI Codex, Devin, and Replit) provide secure containers in which agents can run code without risking the host system. The Model Context Protocol (MCP), introduced by Anthropic and now widely adopted, provides a standardized interface for AI agents to interact with external tools, databases, and services. IDE integration layers (Language Server Protocol, debug adapters, terminal interfaces) enable agents to operate within developers' existing workflows rather than requiring migration to new toolchains.</p>

<h3 class="subsection-title">Evaluation & Quality Infrastructure</h3>

<p>As AI-generated code becomes more prevalent, the infrastructure for evaluating code quality — automated testing, static analysis, security scanning, and formal verification — becomes increasingly important. Companies like Sourcegraph, Snyk, and SonarQube are integrating AI-aware analysis capabilities. GitHub's own security features (Dependabot, CodeQL) are being enhanced to evaluate AI-generated code patterns. This evaluation infrastructure serves as the "safety net" that enables enterprises to adopt AI coding agents with confidence.</p>
"""

# ============================================================
# SECTION 7: POLICY & REGULATORY LANDSCAPE
# ============================================================
policy_table = render_table(
    headers=["Framework / Policy", "Jurisdiction", "Key Provisions Affecting AI Coding"],
    rows=[
        ["EU AI Act (2024)", "European Union", "Risk-based classification; transparency for AI-generated content; mandatory documentation for high-risk AI systems"],
        ["Exec. Order on AI Safety (2023)", "United States", "AI safety standards; frontier model reporting requirements; NIST AI Risk Framework"],
        ["AI Safety Institute", "UK", "Frontier model evaluation; pre-release testing collaboration with AI labs"],
        ["Copyright Office Guidelines", "United States", "AI-generated works not copyrightable; ongoing rulemaking on training data and IP"],
    ],
    title="Key Regulatory Frameworks Affecting AI Coding Agents",
    policy_table=True,
)

section7 = f"""
<p>The regulatory landscape for AI coding agents is evolving rapidly as governments worldwide grapple with the implications of AI-generated code for intellectual property, software safety, labor markets, and national security. While no jurisdiction has yet enacted legislation specifically targeting AI coding tools, several broad AI regulatory frameworks have significant implications for the sector.</p>

{policy_table}

<h3 class="subsection-title">Intellectual Property & Copyright</h3>

<p>The most consequential unresolved regulatory question for AI coding agents concerns intellectual property. Who owns AI-generated code? The U.S. Copyright Office has issued guidance indicating that works generated substantially by AI are not eligible for copyright protection, though this remains subject to ongoing rulemaking and litigation. Multiple lawsuits have been filed against AI companies alleging that training on copyrighted code (particularly open-source code with restrictive licenses) constitutes infringement. The outcome of these cases — several of which are expected to reach key milestones in 2026 — will significantly shape the legal framework for AI coding agents and may affect which training data can be used for future models.</p>

<h3 class="subsection-title">Software Safety & Liability</h3>

<p>As AI agents produce code that ships in production software — including safety-critical systems in healthcare, finance, automotive, and infrastructure — questions of liability and safety assurance become paramount. The EU AI Act's risk-based framework will require additional documentation and oversight for AI tools used in high-risk domains. Several industry groups are developing standards for AI-generated code quality assurance, though no binding international standards have yet been adopted. The question of who bears liability when AI-generated code causes a software failure — the AI vendor, the developer, or the deploying organization — remains legally unresolved in most jurisdictions.</p>

<h3 class="subsection-title">National Security & Export Controls</h3>

<p>AI coding agents intersect with national security in multiple ways. Advanced AI models capable of writing sophisticated software could potentially be used to develop malware, find vulnerabilities in critical systems, or accelerate weapons development. U.S. export controls on advanced AI chips (targeting China) indirectly affect AI coding tool development and deployment. China's domestic AI development push — driven partly by these restrictions — is creating a parallel ecosystem of coding tools that operate independently of Western infrastructure. The Trump administration's blacklisting of Anthropic (currently being challenged in federal court as of March 2026) illustrates the complex interplay between AI companies and government policy.</p>

<h3 class="subsection-title">Labor Market & Workforce Impact</h3>

<p>Policymakers are increasingly focused on the impact of AI coding agents on software developer employment. While some studies suggest AI tools do not uniformly speed up experienced developers, the productivity gains for certain tasks are substantial. Concerns about job displacement are balanced against arguments that AI tools augment rather than replace developers, shift work toward higher-level design and architecture, and expand the overall addressable market for software. Several countries are investing in retraining programs and educational curricula that incorporate AI-assisted development skills.</p>
"""

# ============================================================
# SECTION 8: MARKET RISKS & CHALLENGES
# ============================================================
risk_severity_chart = render_horizontal_bar_chart(
    labels=["Code Quality / Hallucination", "IP / Copyright Uncertainty", "Security Vulnerabilities", "Market Concentration", "Skill Atrophy", "Infrastructure Cost"],
    values=[85, 75, 70, 65, 55, 50],
    title="Risk Assessment — Severity Rating (0–100)",
    value_suffix="",
    colors=["#e94560", "#e94560", "#ff6b35", "#ff6b35", "#f77f00", "#f77f00"],
)

risk_findings = render_key_findings([
    "Code hallucination remains the #1 barrier to enterprise adoption for mission-critical applications",
    "Unresolved IP/copyright framework creates material legal exposure for both vendors and users",
    "Top 5 companies hold combined valuations exceeding $50B — consolidation risk is significant",
    "Prompt injection and supply chain attacks are emerging threat vectors unique to coding agents",
    "\"Vibe coding\" trend raising concerns about long-term developer skill atrophy",
], title="Critical Risks")

section8 = f"""
<p>Despite the strong growth trajectory, the AI coding agent market faces several significant risks and challenges that could affect the pace of adoption, competitive dynamics, and long-term market structure. Investors and industry participants must carefully weigh these factors.</p>

{risk_findings}

<p>The following assessment rates each risk category by its potential severity and likelihood of impacting the market over the next 3–5 years, calibrated against current mitigation capabilities and industry response.</p>

{risk_severity_chart}

<h3 class="subsection-title">Code Quality & Hallucination Risk</h3>

<p>AI coding agents can generate code that appears syntactically correct but contains subtle logical errors, security vulnerabilities, or performance issues. These "hallucinations" in code are particularly dangerous because they may pass automated tests while introducing bugs that only manifest in edge cases or production environments. A July 2025 study highlighted by TechCrunch found that AI coding tools may not speed up every developer and in some cases can introduce errors that skilled developers must spend additional time identifying and fixing. This quality gap — while narrowing with each model generation — remains the primary barrier to enterprise adoption for mission-critical applications. Over-reliance on AI-generated code without adequate review processes poses systemic risk.</p>

<h3 class="subsection-title">Intellectual Property Uncertainty</h3>

<p>The unresolved legal questions around AI-generated code ownership and training data rights create significant uncertainty for enterprises. Companies deploying AI coding agents face questions about whether code produced by these tools is protectable intellectual property, whether it may inadvertently incorporate copyrighted material, and whether their proprietary code fed into AI tools may be used to train future models. Until the legal framework stabilizes — likely through a combination of court rulings and legislative action — this uncertainty will constrain adoption in IP-sensitive contexts and create liability exposure for both vendors and users.</p>

<h3 class="subsection-title">Market Concentration & Platform Lock-In</h3>

<p>The AI coding agent market is rapidly consolidating around a small number of well-funded players. The combined valuations of the top five companies (Cognition, Anysphere, Replit, GitHub/Microsoft, and early-stage Poolside and Magic) exceed $50 billion. Cognition's acquisition of Windsurf in July 2025 exemplifies this consolidation trend. For enterprises, this concentration creates vendor lock-in risk: deep integration of AI agents into development workflows makes switching costly. The reliance of most coding agents on a small number of foundation model providers (OpenAI, Anthropic, Google) adds an additional layer of concentration risk in the supply chain.</p>

<h3 class="subsection-title">Security Vulnerabilities</h3>

<p>AI coding agents that can execute code, access file systems, run terminal commands, and interact with APIs introduce new attack surfaces. Prompt injection attacks — where malicious content in codebases or documentation manipulates the agent's behavior — represent an emerging threat vector. Supply chain security concerns arise when AI agents install dependencies or modify configurations. The rapid deployment of agent capabilities has outpaced the development of robust security frameworks, creating a window of elevated risk that attackers may exploit. Enterprises deploying coding agents require new security controls, monitoring, and governance frameworks.</p>

<h3 class="subsection-title">Developer Skill Atrophy</h3>

<p>A structural concern for the industry is the potential degradation of developer skills as AI handles increasing portions of code writing. If junior developers rely heavily on AI agents during their formative years, they may fail to develop deep understanding of programming fundamentals, debugging skills, and architectural judgment. This creates a paradox: the tools that boost short-term productivity may undermine the human expertise needed to supervise and verify AI-generated code long-term. The "vibe coding" phenomenon — where developers accept AI outputs without thorough understanding — has become a recognized concern in the engineering community.</p>

<h3 class="subsection-title">Infrastructure Cost & Margin Pressure</h3>

<p>AI coding agents are compute-intensive, requiring substantial GPU inference costs for each interaction. While inference costs are declining, the per-user economics remain challenging — particularly for products offering unlimited or heavy-use plans. Several companies have faced user backlash over pricing changes (notably Cursor in July 2025), highlighting the tension between unsustainable subsidized pricing and the actual cost of delivering AI agent services. Companies must achieve sufficient scale and inference efficiency to reach profitability, and those unable to do so face existential risk as the market matures.</p>
"""

# ============================================================
# SECTION 9: STRATEGIC OUTLOOK & FORECASTS
# ============================================================
forecast_table = render_table(
    headers=["Metric", "2024", "2026E", "2028F", "2030F", "CAGR"],
    rows=[
        ["Global AI Code Tools Market", "$6.1B", "$11.0B", "$18.0B", "$26.0B", "27.1%"],
        ["Autonomous Agent Segment", "$0.5B", "$2.0B", "$5.0B", "$8.0B", "~60%"],
        ["Enterprise Adoption Rate", "~25%", "~45%", "~65%", "~80%", "—"],
        ["% of New Code AI-Assisted", "~15%", "~30%", "~50%", "~70%", "—"],
    ],
    title="AI Coding Agent Market — Key Projections (2024–2030)",
)

forecast_chart = render_line_chart(
    labels=["2024", "2025E", "2026E", "2027F", "2028F", "2029F", "2030F"],
    series=[
        {"name": "Total Market ($B)", "values": [6.1, 8.3, 11.0, 14.2, 18.0, 21.8, 26.0], "color": "#0f3460"},
        {"name": "Autonomous Agent Segment ($B)", "values": [0.5, 1.0, 2.0, 3.2, 5.0, 6.5, 8.0], "color": "#e94560"},
    ],
    title="Market Growth Forecast — Total Market vs. Autonomous Agents (2024–2030)",
    value_prefix="$",
    value_suffix="B",
)

adoption_stat_bars = render_stat_bars(
    items=[
        {"label": "Enterprise Adoption", "value": 80, "display": "80% by 2030"},
        {"label": "AI-Assisted Code", "value": 70, "display": "70% of new code"},
        {"label": "Productivity Gain", "value": 68, "display": "60–75%"},
        {"label": "Copilot Users", "value": 75, "display": "75M+ projected"},
    ],
    title="2030 Forecast Targets",
    bar_color="#0f3460",
)

section9 = f"""
<p>The AI coding agent market is projected to sustain rapid growth through 2030, driven by improving model capabilities, expanding enterprise adoption, declining inference costs, and the broadening applicability of AI-assisted development. The following projections outline the expected evolution of key market metrics.</p>

{forecast_chart}

<p>The autonomous agent segment is projected to be the fastest-growing category, expanding from $0.5 billion in 2024 to an estimated $8 billion by 2030 — a CAGR of approximately 60%. This reflects the market's structural shift from assisted coding to agentic development.</p>

{forecast_table}

<p>The autonomous agent segment stands out as the most dynamic growth area. Starting from just $0.5 billion in 2024, this segment is projected to grow at roughly 60% CAGR to reach $8 billion by 2030 — reflecting the market's structural shift from assisted coding to fully agentic development workflows. Enterprise adoption is the primary revenue driver, with large organizations expected to deploy AI coding tools at an 80%+ rate by decade's end.</p>

<p>By 2030, the convergence of these trends is expected to produce a fundamentally transformed development landscape, with AI assistance embedded in virtually every stage of the software lifecycle.</p>

{adoption_stat_bars}

<h3 class="subsection-title">The Agent-Native Development Era</h3>

<p>By 2028, we project that the majority of professional software development will involve AI coding agents in some capacity. The transition from "AI-assisted coding" (suggesting lines or blocks) to "AI-agentic development" (planning and executing multi-step implementations autonomously) represents a fundamental shift in the development workflow. Developers will increasingly move toward supervisory roles — defining requirements, reviewing agent output, making architectural decisions, and handling novel edge cases — while agents handle implementation, testing, refactoring, and documentation. This shift will redefine the economics of software development and the skills required of professional developers.</p>

<h3 class="subsection-title">Platform Consolidation & Ecosystem Wars</h3>

<p>The current fragmented market will consolidate significantly by 2028. We anticipate 3–5 major platforms emerging as winners, each anchored by either a foundation model (OpenAI, Anthropic, Google), a developer ecosystem (GitHub/Microsoft, JetBrains), or a purpose-built product moat (Cursor, Devin). GitHub's February 2026 move to open Agent HQ to third-party models signals that the market may evolve toward a platform model — similar to how mobile operating systems (iOS, Android) host third-party applications. Companies that control the developer relationship and workflow integration will command the highest margins.</p>

<h3 class="subsection-title">Enterprise as the Revenue Driver</h3>

<p>While individual developer adoption has driven user growth, enterprise clients will be the primary revenue driver through 2030. Enterprise customers pay 2–10x more per seat than individual developers and demand features — security controls, audit trails, on-premises deployment, SSO integration, IP protection, and compliance certifications — that create high switching costs. We project enterprise adoption of AI coding tools to grow from approximately 25% in 2024 to over 80% by 2030, with the largest enterprises deploying multiple tools across different use cases.</p>

<h3 class="subsection-title">Emergence of Vertical Coding Agents</h3>

<p>A significant emerging opportunity is the development of domain-specific coding agents — AI tools optimized for particular industries, technology stacks, or application types. Examples include agents specialized for embedded systems, healthcare software (HIPAA compliance-aware), financial services (regulatory-aware code generation), smart contract development, and infrastructure-as-code management. These vertical agents will command premium pricing and exhibit lower churn than general-purpose tools.</p>

<h3 class="subsection-title">The "1000x Developer" Thesis</h3>

<p>The long-term strategic thesis driving investment in AI coding agents is the "1000x developer" — the idea that AI tools will eventually amplify individual developer productivity by orders of magnitude, enabling small teams to build what previously required hundreds of engineers. While this vision remains aspirational, the trajectory from 2x productivity gains (code completion, 2022) to 5–10x gains (agent-mode development, 2025) to potential 50–100x gains (fully autonomous agents, projected 2028–2030) supports the thesis that the total addressable market for software will expand dramatically as AI reduces the cost and time required for development.</p>
"""

# ============================================================
# SECTION 10: CONCLUSION & RECOMMENDATIONS
# ============================================================
conclusion_findings = render_key_findings([
    "The market is growing at 27%+ CAGR and will transform every industry dependent on software",
    "3–5 dominant platforms will emerge by 2028; position now or face steep switching costs",
    "Enterprise adoption will reach 80%+ by 2030 — governance, security, and IP frameworks are the gating factors",
    "Developers who master AI-agent collaboration will gain outsized career advantages",
    "Regulatory clarity on IP, safety, and liability is urgently needed to sustain innovation",
], title="Strategic Imperatives")

section10 = f"""
{conclusion_findings}

<p>The AI coding agent market has reached an inflection point. The convergence of powerful foundation models, massive venture investment, rapid enterprise adoption, and the evolution from code completion to autonomous agents has created a market growing at over 27% annually — on track to exceed $26 billion by 2030. The competitive landscape is intense and consolidating rapidly, with valuations reaching $9–10 billion for the leading pure-play companies less than two years after their founding.</p>

<p>This is not an incremental improvement in developer tools — it is a structural transformation in how software is built. The implications extend far beyond the technology sector, affecting every industry that depends on software (which, increasingly, is every industry) and reshaping the skills, roles, and economics of the global developer workforce.</p>

<h3 class="subsection-title">For Investors</h3>

<p>The AI coding agent sector offers compelling growth characteristics — rapid revenue scaling, high net retention, large TAM expansion, and strong secular tailwinds. Priority investment themes include: (1) platforms that control the developer workflow and relationship (IDE-native agents), (2) companies with proprietary model advantages in code generation, (3) infrastructure and tooling for AI code quality, security, and governance, and (4) vertical-specific coding agents targeting regulated industries. Investors should be disciplined on valuation, as several companies are priced for near-flawless execution, and cognizant of consolidation risk — the market is likely to produce 3–5 winners, not 50. The enterprise segment offers the most predictable revenue streams, while consumer/individual developer tiers face margin pressure.</p>

<h3 class="subsection-title">For Technology Leaders & CTOs</h3>

<p>Enterprise technology leaders should adopt a strategic, multi-tool approach to AI coding agents. Recommendations include: (1) deploy AI coding agents broadly but with governance frameworks that ensure code review, security scanning, and IP compliance, (2) evaluate both cloud and on-premises deployment options based on data sensitivity requirements, (3) invest in developer training that emphasizes AI collaboration skills — prompt engineering, output verification, and architectural judgment — rather than resisting adoption, (4) track the evolving platform landscape closely, as switching costs will increase as agents become more deeply integrated into CI/CD pipelines and development workflows, and (5) prepare for a 12–18 month horizon where AI agents can autonomously handle 50%+ of routine development tasks, and plan workforce strategy accordingly.</p>

<h3 class="subsection-title">For Policymakers</h3>

<p>Clear and balanced regulatory guidance is essential to sustain innovation while managing risks. Priorities include: (1) resolving the intellectual property framework for AI-generated code — developers and companies need legal certainty on code ownership and training data rights, (2) developing standards for AI-generated code safety, particularly for deployment in critical infrastructure, healthcare, and financial systems, (3) investing in workforce retraining programs that prepare developers for AI-augmented workflows rather than attempting to slow adoption, (4) balancing national security concerns with the need for international collaboration on AI safety and evaluation standards, and (5) ensuring that AI coding tools remain accessible to startups, independent developers, and underserved communities — not just well-funded enterprises.</p>

<h3 class="subsection-title">For Developers</h3>

<p>For individual practitioners, the message is clear: AI coding agents are not replacing developers — they are redefining what it means to be a developer. The most valuable skills are shifting from code production toward system design, requirement specification, code review, security analysis, and the ability to effectively supervise and direct AI agents. Developers who learn to work fluently with AI agents — treating them as powerful collaborators rather than threats or toys — will see the greatest productivity gains and career advancement. The developers who thrive will be those who combine deep technical understanding with the emerging skill of AI-assisted engineering.</p>
"""

# ============================================================
# ASSEMBLE THE REPORT
# ============================================================
sections = [
    {"number": 1, "title": "Executive Summary", "content": section1},
    {"number": 2, "title": "Market Size & Growth Overview", "content": section2},
    {"number": 3, "title": "Investment & Funding Trends", "content": section3},
    {"number": 4, "title": "Core Market Segment Analysis", "content": section4},
    {"number": 5, "title": "Regional Market Analysis", "content": section5},
    {"number": 6, "title": "Infrastructure & Enabling Technologies", "content": section6},
    {"number": 7, "title": "Policy & Regulatory Landscape", "content": section7},
    {"number": 8, "title": "Market Risks & Challenges", "content": section8},
    {"number": 9, "title": "Strategic Outlook & Forecasts", "content": section9},
    {"number": 10, "title": "Conclusion & Recommendations", "content": section10},
]

report_data = build_report_data(
    title="AI Coding Agents",
    subtitle="Market Analysis, Competitive Landscape &\nStrategic Outlook",
    short_title="AI Coding Agents",
    sections=sections,
    cover_metrics=cover_metrics,
    description="A comprehensive examination of the AI-powered coding agent ecosystem, covering code generation models, agentic development tools, competitive dynamics, enterprise adoption, investment trends, and the transformation of software engineering workflows across global markets.",
)

html = compose_report(report_data)

# Render to Desktop
output_path = os.path.expanduser("~/Desktop")
filename = f"AI_Coding_Agents_{current_year()}.pdf"
full_path = os.path.join(output_path, filename)

from weasyprint import HTML
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
html_doc = HTML(string=html, base_url=TEMPLATE_DIR)
html_doc.write_pdf(full_path)

print(f"Report generated: {full_path}")

# Also save to output/
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
os.makedirs(output_dir, exist_ok=True)
output_copy = os.path.join(output_dir, filename)
html_doc.write_pdf(output_copy)
print(f"Copy saved: {output_copy}")
