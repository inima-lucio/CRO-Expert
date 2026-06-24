# CRO Expert — Claude Code Skill

**Full-funnel e-commerce conversion audit powered by real data.**  
Built by [Lucio Monopoli](mailto:inima.lucio@gmail.com) · [INIMA Interactive](https://inimainteractive.com)

---

## What it does

Run `/cro-expert https://your-store.com` in Claude Code and get a **professional 9-page HTML/PDF audit report** covering:

- Visual screenshots (desktop + mobile) with **numbered callout markers overlaid** on each page
- 4Ps · AIDA · Cialdini · Nielsen framework analysis
- Real GA4 funnel data — auto-discovered by domain, no property ID needed
- Google Ads performance via Master Metrics — ROAS, CPA, CVR, landing page quality
- Meta Ads performance via Master Metrics — ROAS, CPA, paid funnel by campaign
- E-commerce platform data (Tiendanube if connected, GA4 enhanced e-commerce otherwise)
- Priority matrix with Impact × Effort recommendations
- A/B test plan with sample size calculations
- Plugin recommendations ranked by CVR impact
- Client-ready conclusions + 30-day action checklist

The report is a **self-contained HTML file** (inline screenshots with visual annotations, SVG charts, no external dependencies). Works offline, converts to PDF.

**Works for any e-commerce platform** — Shopify, WooCommerce, VTEX, Tiendanube, Magento, custom. The only Tiendanube-specific section is optional and only appears if your Master Metrics account has a Tiendanube store connected.

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

```
/cro-expert https://my-store.com
/cro-expert https://my-store.com --pdf
```

---

## MCP Configuration

This skill uses **2 MCPs**. You don't need both — each one you connect adds a richer data section to the report.

---

### MCP 1 — `analytics-mcp` (Google Analytics 4)

**What it unlocks:** Full GA4 funnel report (session → view_item → add_to_cart → checkout → purchase), CVR by device, bounce rate by page, drop-off analysis, custom dimensions, conversion events.

**Type:** Claude Code MCP — configured locally in `~/.claude/settings.json`

**Step 1 — Add to settings**

Open `~/.claude/settings.json` and add under `mcpServers`:

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

**Step 2 — Authenticate**

On first use, Claude will open a Google OAuth window. Sign in with the Google account that has access to your GA4 properties.

**Step 3 — Verify**

In Claude Code, ask: `List all my GA4 properties`  
You should see your accounts. If you get an `invalid_grant` error, your token expired — reconnect by running the OAuth flow again (restart Claude Code and trigger any analytics-mcp call).

**Fallback:** If analytics-mcp is unavailable, the skill automatically falls back to GA4 basic data via **Master Metrics** `source: "google_analytics"`.

---

### MCP 2 — `Master Metrics` (multi-source data hub)

**What it unlocks:** Google Ads, Meta Ads, GA4 basic, Pinterest Ads, YouTube Ads, and (optionally) Tiendanube store data — all from a single MCP.

**Type:** Claude.ai native integration — configured at account level, not locally

**Step 1 — Enable in claude.ai**

1. Go to [claude.ai](https://claude.ai) → Settings → Integrations
2. Find **Master Metrics** and click **Connect**
3. Follow the OAuth flow to link your advertising accounts (Google Ads, Meta Ads, etc.)

**Step 2 — Verify**

In Claude Code:
```
What data sources do I have in Master Metrics?
```
You should see a list like: `google, google_analytics, meta, tiendanube, pinterest, youtube`

Only sources you see here will appear in the report.

**Step 3 — Tiendanube (optional)**

If you use Tiendanube and want platform-level sales data (orders, abandoned carts, UTM attribution by actual order):
1. In Master Metrics, connect your Tiendanube store
2. The skill will auto-detect the matching store by domain

If you're not on Tiendanube, this step is irrelevant — the skill uses GA4 Enhanced E-commerce data for sales metrics.

---

### What each MCP unlocks in the report

| Section | Requires | Without it |
|---|---|---|
| GA4 funnel + CVR by device | `analytics-mcp` OR Master Metrics `google_analytics` | Placeholder — no funnel data |
| Google Ads ROAS/CPA/quality score | Master Metrics (`google` source) | Google Ads section skipped |
| Meta Ads ROAS/CPA/paid funnel | Master Metrics (`meta` source) | Meta Ads section skipped |
| Ad vs. landing page diagnosis | Either Google or Meta in Master Metrics | Skipped |
| Tiendanube orders + abandonment | Master Metrics (`tiendanube` source) | Skipped — GA4 e-commerce used instead |
| Pinterest / YouTube Ads | Master Metrics (`pinterest`/`youtube` source) | Not shown |

**The report always generates** — with or without MCPs. More MCPs = richer data sections.

---

## Report pages

| # | Page | Content |
|---|---|---|
| Cover | Portada | CRO score gauge (traffic light) + 4 KPI chips |
| 1 | Executive Summary | Score per page + critical issues + 30/60/90 day roadmap |
| 2 | Page Analysis | Screenshots **with numbered visual markers** + fold indicator + AIDA chart |
| 3 | Framework Audit | Cialdini 7 principles + Nielsen 10 heuristics |
| 4 | Data Dashboard | GA4 funnel + platform e-commerce data (if available) |
| 5 | Paid Media | Google Ads + Meta Ads + ad vs. landing diagnosis |
| 6 | Recommendations | Impact × Effort matrix + recommendation cards |
| 7 | A/B Test Plan | Summary table + full test specs |
| 8 | Plugins | Tools ranked by CVR impact |
| 9 | Action Plan | Conclusions + 30-day checklist + KPIs to track |

---

## Skill structure

```
cro-expert/
├── SKILL.md                    ← Agent instructions (phases + A/B plan + plugins)
├── scripts/
│   ├── crawler.py              ← Auto-discovers site pages
│   ├── html_analyzer.py        ← HTML & copy CRO analysis
│   ├── report_generator.py     ← Premium HTML report with annotated screenshots
│   └── pdf_generator.py        ← PDF export via Playwright
├── references/
│   ├── frameworks.md           ← 4Ps, AIDA, Cialdini, Nielsen criteria
│   ├── scoring.md              ← Scoring rubrics
│   └── benchmarks.md           ← CVR benchmarks by e-commerce category
└── assets/
    └── report_template.md      ← Report structure reference
```

---

## Requirements

- [Claude Code](https://claude.ai/code) with an active subscription
- Python 3.10+
- `pip install playwright requests beautifulsoup4 && playwright install chromium`

---

## FAQ

**Q: Does this work for Shopify / WooCommerce / VTEX?**  
A: Yes. GA4 provides full e-commerce funnel data for any platform. The paid media sections work for any advertiser. Only the Tiendanube-specific section requires a connected TN store.

**Q: Do I need both MCPs?**  
A: No. analytics-mcp alone gives you the full GA4 analysis. Master Metrics alone gives you paid media + (optionally) Tiendanube. Neither gives you the other's data, so both is ideal.

**Q: My analytics-mcp shows `invalid_grant`. What do I do?**  
A: Your Google OAuth token expired. Restart Claude Code and run any analytics-mcp command — it will trigger re-authentication. Or check `~/.claude/settings.json` and ensure the MCP is still configured correctly.

**Q: I don't see Master Metrics in claude.ai Integrations.**  
A: Contact [INIMA Interactive](mailto:inima.lucio@gmail.com) to request access.

**Q: Screenshots have no markers. Why?**  
A: Markers appear when Claude generates `callout_markers` with x/y coordinates during Phase 1. Make sure the analysis JSONs include this field (documented in SKILL.md data contract section).

---

## License

MIT — free to use, modify, and distribute. Attribution appreciated.

---

*Made with ❤️ by [INIMA Interactive](https://inimainteractive.com) · Buenos Aires, Argentina*
