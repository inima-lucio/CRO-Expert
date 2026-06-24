# CRO Expert — Claude Code Skill

**Full-funnel e-commerce conversion audit powered by real data.**  
Built by [Lucio Monopoli](mailto:inima.lucio@gmail.com) · [INIMA Interactive](https://inimainteractive.com)

---

## What it does

Run `/cro-expert https://your-store.com` in Claude Code and get a **professional 8-page HTML/PDF audit report** covering:

- Visual screenshots (desktop + mobile) of every key page
- 4Ps · AIDA · Cialdini · Nielsen framework analysis
- Real GA4 funnel data (auto-discovered, no property ID needed)
- Tiendanube sales data — orders, abandoned carts, UTM attribution
- Meta Ads & Google Ads performance — ROAS, CPA, ad vs. landing page diagnosis
- Priority matrix with numbered Impact × Effort recommendations
- A/B test plan with sample size calculations and test duration
- Plugin recommendations ranked by CVR impact

The report is a **self-contained HTML file** (base64 screenshots, inline SVG charts, no external dependencies). Works offline and converts to print-quality PDF.

---

## Installation

```bash
# 1. Clone into your Claude Code skills folder
git clone https://github.com/inima-lucio/CRO-Expert.git ~/.claude/skills/cro-expert

# 2. Install Python dependencies
pip3 install playwright requests beautifulsoup4
python3 -m playwright install chromium
```

---

## Usage

Open Claude Code and type:

```
/cro-expert https://my-store.com
```

With PDF export:

```
/cro-expert https://my-store.com --pdf
```

---

## Report pages

| # | Page | Content |
|---|---|---|
| 1 | Cover | CRO score gauge with traffic light (red/amber/green) + 4 KPI chips |
| 2 | Executive Summary | Score per page + critical issues + 30/60/90 day roadmap |
| 3 | Page Analysis | Real screenshots + AIDA chart + issues + strengths (Home → PLP → PDP → Cart → Checkout) |
| 4 | Framework Audit | Cialdini 7 principles bar chart + Nielsen 10 heuristics table |
| 5 | Data Dashboard | GA4 funnel + Tiendanube sales KPIs + abandoned cart revenue lost |
| 6 | Paid Media | Meta Ads + Google Ads ROAS/CPA + ad vs. landing page diagnosis table |
| 7 | Recommendations | Impact × Effort matrix (numbered dots + legend) + recommendation cards |
| 8 | A/B Test Plan | Summary table + full test spec per test (hypothesis, sample size, duration, tool) |
| 9 | Plugins | 10 tools ranked by CVR impact with price, setup hours, and install guide |

---

## Data integrations

| Source | MCP | What it pulls |
|---|---|---|
| Google Analytics 4 | `analytics-mcp` | Sessions, funnel, bounce rate, CVR by device — auto-discovered by domain |
| Tiendanube | `Master Metrics MCP` | Orders, abandoned checkouts, UTM attribution, top products, new vs returning |
| Meta Ads | `Master Metrics MCP` | ROAS, CPA, CVR, ATC→Checkout funnel by campaign |
| Google Ads | `Master Metrics MCP` | ROAS, CPA, conversion rate, landing page quality score |

**GA4 is auto-discovered** — just pass the URL, no property ID needed.  
**Tiendanube, Meta & Google** require Master Metrics MCP connected to your accounts.

---

## Skill structure

```
cro-expert/
├── SKILL.md                    ← Agent instructions (7 phases + A/B plan + plugins)
├── scripts/
│   ├── crawler.py              ← Auto-discovers site pages
│   ├── html_analyzer.py        ← HTML & copy CRO analysis
│   ├── report_generator.py     ← Builds the premium HTML report
│   └── pdf_generator.py        ← PDF export via Playwright
├── references/
│   ├── frameworks.md           ← 4Ps, AIDA, Cialdini, Nielsen criteria
│   ├── scoring.md              ← Scoring rubrics
│   └── benchmarks.md           ← E-commerce CVR benchmarks by category
└── assets/
    └── report_template.md      ← Report structure reference
```

---

## Requirements

- [Claude Code](https://claude.ai/code) with an active subscription
- Python 3.10+
- `playwright`, `requests`, `beautifulsoup4`
- (Optional) `analytics-mcp` for GA4 data
- (Optional) Master Metrics MCP for Tiendanube / Meta / Google data

---

## License

MIT — free to use, modify, and distribute. Attribution appreciated.

---

*Made with ❤️ by [INIMA Interactive](https://inimainteractive.com) · Buenos Aires, Argentina*
