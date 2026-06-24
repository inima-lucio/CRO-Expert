# CRO Expert — Claude Code Skill

**Full-funnel e-commerce conversion audit powered by real data.**  
Built by [Lucio Monopoli](mailto:inima.lucio@gmail.com) · [INIMA Interactive](https://inimainteractive.com)

---

## What it does

Run `/cro-expert https://your-store.com` in Claude Code and get a **professional 9-page HTML/PDF audit report** covering:

- Visual screenshots (desktop + mobile) with **numbered callout markers overlaid** on each page
- 4Ps · AIDA · Cialdini · Nielsen framework analysis
- Real GA4 funnel data (auto-discovered by domain, no property ID needed)
- Tiendanube sales data — orders, abandoned carts, UTM attribution, top products
- Meta Ads & Google Ads performance — ROAS, CPA, ad vs. landing page diagnosis
- Priority matrix with Impact × Effort recommendations
- A/B test plan with sample size calculations and test duration
- Plugin recommendations ranked by CVR impact
- Client-ready conclusions + 30-day action checklist

The report is a **self-contained HTML file** (base64 screenshots with visual annotations, inline SVG charts, no external dependencies). Works offline and converts to print-quality PDF.

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
| Cover | Portada | CRO score gauge (traffic light) + 4 KPI chips |
| 1 | Executive Summary | Score per page + critical issues list + 30/60/90 day roadmap |
| 2 | Page Analysis | Screenshots **with numbered markers** + AIDA chart + fold line indicator |
| 3 | Framework Audit | Cialdini 7 principles bar chart + Nielsen 10 heuristics table |
| 4 | Data Dashboard | GA4 funnel + Tiendanube KPIs + abandoned cart revenue lost |
| 5 | Paid Media | Meta Ads + Google Ads ROAS/CPA + ad vs. landing page diagnosis |
| 6 | Recommendations | Impact × Effort matrix + recommendation cards |
| 7 | A/B Test Plan | Summary table + full test spec per test |
| 8 | Plugins | Tools ranked by CVR impact |
| 9 | Action Plan | Conclusions + 30-day checklist + KPIs to track (client-ready) |

---

## Data integrations

| Source | MCP | What it pulls |
|---|---|---|
| Google Analytics 4 | `analytics-mcp` | Sessions, funnel, bounce rate, CVR by device — auto-discovered by domain |
| Tiendanube | `Master Metrics` | Orders, abandoned checkouts, UTM attribution, top products, new vs returning |
| Meta Ads | `Master Metrics` | ROAS, CPA, CVR post-click, ATC→Checkout funnel by campaign |
| Google Ads | `Master Metrics` | ROAS, CPA, conversion rate, landing page quality score by campaign |

The skill runs without any MCP — it falls back to visual + heuristic analysis only. Each MCP you connect unlocks a richer data section.

---

## MCP Configuration — Step by Step

There are **two types** of MCP integrations used by this skill:

| Type | MCPs | How to configure |
|---|---|---|
| **Claude Code MCP** (local, in your machine) | `analytics-mcp` | Add to `~/.claude/settings.json` → `mcpServers` |
| **Claude.ai native integration** | `Master Metrics`, `META Ads` | Enable in claude.ai → Settings → Integrations |

---

### 1. Google Analytics 4 — `analytics-mcp`

**What you get:** Sessions, funnel (session → view_item → ATC → checkout → purchase), CVR by device, bounce rate, top channels, drop-off by page.

**Step 1 — Install the MCP**

Add this block to `~/.claude/settings.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "analytics-mcp": {
      "command": "npx",
      "args": ["-y", "@anthropic-samples/analytics-mcp"],
      "env": {}
    }
  }
}
```

Restart Claude Code after saving.

**Step 2 — Authenticate with Google**

On first use, Claude will open a browser window for Google OAuth. Sign in with the account that has access to your GA4 properties.

**Step 3 — Verify**

In Claude Code, type:  
```
List all my GA4 properties
```
You should see your accounts. If you do, GA4 data will appear automatically in the report.

**Step 4 — No property ID needed**

The skill auto-discovers the GA4 property that matches the audited domain. If there's more than one match, Claude will ask which one to use.

---

### 2. Tiendanube + Meta Ads + Google Ads — `Master Metrics`

**What you get:**
- **Tiendanube:** Orders, revenue, abandoned checkouts, ticket promedio, UTM attribution, top products, new vs. returning customers
- **Meta Ads:** ROAS, CPA, CVR, ATC→Checkout funnel by campaign and platform
- **Google Ads:** ROAS, CPA, conversion rate, landing page quality score by campaign

**These 3 sources use the same MCP: `Master Metrics`.** It's a claude.ai native integration — no local installation needed.

**Step 1 — Enable in claude.ai**

1. Go to [claude.ai](https://claude.ai) → Settings → Integrations
2. Find **Master Metrics** and click **Connect**
3. Follow the OAuth flow to connect your accounts (Tiendanube, Google Ads, Meta Ads)

If Master Metrics is not visible in the integrations list, contact [INIMA Interactive](mailto:inima.lucio@gmail.com) to request access.

**Step 2 — Verify in Claude Code**

In Claude Code, type:
```
List my Tiendanube stores via Master Metrics
```
You should see your connected stores. Then:
```
List my Meta Ads accounts via Master Metrics
```
And:
```
List my Google Ads accounts via Master Metrics
```

**Step 3 — Auto-discovery in the report**

The skill auto-matches the audited domain against your connected accounts. No account IDs needed.

---

### 3. Meta Ads (native auth — optional)

If your Meta Ads account requires separate authentication beyond Master Metrics:

1. Go to claude.ai → Settings → Integrations
2. Find **META Ads** and click **Connect**
3. Complete the Facebook/Meta OAuth flow

This adds a direct Meta Ads connection alongside the Master Metrics aggregated data.

---

### Connection status check

Before running an audit, verify all connections with:

```
/cro-expert --check-connections
```

Or manually in Claude Code:

```
Check my analytics-mcp connection and list GA4 properties
Check my Master Metrics connection and list Tiendanube stores
```

---

### What happens without each MCP

| Without | Report section | Fallback |
|---|---|---|
| `analytics-mcp` | Data Dashboard → GA4 section | "GA4 not connected" placeholder |
| `Master Metrics` | Data Dashboard → TN + Paid Media | Visual/heuristic analysis only |
| Both | Full report still generated | 100% heuristic, no data charts |

---

## Skill structure

```
cro-expert/
├── SKILL.md                    ← Agent instructions (7 phases + A/B plan + plugins)
├── scripts/
│   ├── crawler.py              ← Auto-discovers site pages
│   ├── html_analyzer.py        ← HTML & copy CRO analysis
│   ├── report_generator.py     ← Builds premium HTML report with annotated screenshots
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
- `pip install playwright requests beautifulsoup4`
- `playwright install chromium`

MCPs are optional but strongly recommended for premium reports.

---

## Frequently Asked Questions

**Q: Do I need all MCPs for the skill to work?**  
A: No. The skill runs without any MCP and produces a full heuristic report. Each MCP adds a data layer.

**Q: Can I use this for platforms other than Tiendanube?**  
A: Yes. GA4 and paid media sections work for any e-commerce. Tiendanube-specific data only appears if you have Master Metrics connected to a Tiendanube store.

**Q: How does the GA4 auto-discovery work?**  
A: The skill calls `get_account_summaries` via analytics-mcp, then filters properties by domain name match. If multiple properties match, Claude asks which one to use.

**Q: My screenshots don't show markers. Why?**  
A: Markers appear when `callout_markers` data is present in the page analysis JSON. Make sure Claude generates this field during Phase 1. The field format is documented in the data contract section of SKILL.md.

**Q: Can I run this in Spanish?**  
A: Yes. The report language follows the audited site's language. Use `--lang es` to force Spanish output.

---

## License

MIT — free to use, modify, and distribute. Attribution appreciated.

---

*Made with ❤️ by [INIMA Interactive](https://inimainteractive.com) · Buenos Aires, Argentina*
