# CRO Expert — Claude Code Skill

**Full-funnel e-commerce conversion audit powered by real data.**  
Built by [Lucio Monopoli](mailto:inima.lucio@gmail.com) · [INIMA Interactive](https://inimainteractive.com)

---

## What it does

Run `/cro-expert https://your-store.com` in Claude Code and get a **professional 10-page HTML/PDF audit report** covering:

- Visual screenshots (desktop + mobile) with **numbered callout markers overlaid** on each page
- 4Ps · AIDA · Cialdini · Nielsen framework analysis
- Real GA4 funnel data — auto-discovered by domain via `analytics-mcp`, no property ID needed
- Google Ads via `google-ads-mcp` — GAQL queries for ROAS, CPA, CVR by device, landing page quality score per keyword
- Meta Ads via Master Metrics — ROAS, CPA, paid funnel by campaign and platform (Facebook vs. Instagram)
- TiendaNube data via `tiendanube-mcp` — real orders, abandoned carts, UTM attribution, top products
- **Multi-source triangulation** — cross-references all 4 sources to detect double attribution, real vs. claimed ROAS, and mobile CVR gaps
- Priority matrix with Impact × Effort recommendations
- A/B test plan with sample size calculations
- Plugin recommendations ranked by CVR impact
- Client-ready conclusions + 30-day action checklist

The report is a **self-contained HTML file** (inline screenshots with visual annotations, SVG charts, no external dependencies). Works offline, converts to PDF.

**Works for any e-commerce platform** — Shopify, WooCommerce, VTEX, Tiendanube, Magento, custom. Each data source degrades gracefully if unavailable — the report always generates.

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

This skill uses **4 independent MCPs**. Each adds a richer data layer. You don't need all four — the report always generates with whatever is available.

---

### MCP 1 — `analytics-mcp` (Google Analytics 4)

**What it unlocks:** Full GA4 funnel (session → view_item → add_to_cart → checkout → purchase), CVR by device, drop-off by page, custom dimensions, conversion events. Auto-discovered by domain — no property ID needed.

Add to `~/.claude/settings.json`:

```json
"analytics-mcp": {
  "type": "stdio",
  "command": "pipx",
  "args": ["run", "analytics-mcp"],
  "env": {}
}
```

**Authenticate:**
```bash
gcloud auth application-default login \
  --client-id-file=/path/to/client_secret.json \
  --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform
```
Then in Claude Code: `/mcp` → Reconnect `analytics-mcp`.

**Verify:** Ask `List all my GA4 properties` — you should see your accounts.  
**Fallback:** If unavailable, skill uses Master Metrics `source: "google_analytics"`.

---

### MCP 2 — `google-ads-mcp` (Google Ads API via GAQL)

**What it unlocks:** Direct GAQL queries — campaign ROAS/CPA/CVR, performance by device, landing page quality score per keyword, accessible customer list.

**Prerequisites:**
1. A Google Ads Developer Token (from [Google Ads API Center](https://ads.google.com/aw/apiaccess))
2. Your Google Cloud project ID
3. Manager account ID (if using MCC)

Add to `~/.claude/settings.json`:

```json
"google-ads-mcp": {
  "type": "stdio",
  "command": "pipx",
  "args": [
    "run",
    "--spec",
    "git+https://github.com/googleads/google-ads-mcp.git",
    "google-ads-mcp"
  ],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "/Users/<you>/.config/gcloud/application_default_credentials.json",
    "GOOGLE_PROJECT_ID": "your-gcp-project-id",
    "GOOGLE_ADS_DEVELOPER_TOKEN": "your-22-char-developer-token",
    "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "1234567890"
  }
}
```

**Verify:** Ask `List my Google Ads accounts` — you should see customer IDs.  
**Fallback:** If unavailable, skill uses Master Metrics `source: "google"`.

---

### MCP 3 — `tiendanube-mcp` (TiendaNube API — only for TN stores)

**What it unlocks:** Real order data (revenue, ticket promedio, UTM attribution per order), abandoned carts, top products, customer new/returning split. Direct from TiendaNube API — not aggregated.

**Prerequisites:**
1. A TiendaNube app with API access (create one at [partners.tiendanube.com](https://partners.tiendanube.com))
2. Your store's `access_token` and `store_id` (obtained via OAuth flow or Partner Portal)
3. Docker installed locally

**Setup:**
```bash
git clone https://github.com/AlexandreProenca/nuvemshop-mcp-server.git ~/tiendanube-mcp
cd ~/tiendanube-mcp

# Create .env file
echo "TIENDANUBE_ACCESS_TOKEN=your_token_here" > .env
echo "TIENDANUBE_STORE_ID=your_store_id" >> .env
echo "MCP_TRANSPORT=sse" >> .env
echo "MCP_HOST=0.0.0.0" >> .env
echo "MCP_PORT=8080" >> .env

docker-compose up -d
```

Add to `~/.claude/settings.json`:

```json
"tiendanube-mcp": {
  "type": "sse",
  "url": "http://localhost:8080/sse"
}
```

**Verify:** Ask `Get my TiendaNube store info` — you should see store name and details.  
**Fallback:** If unavailable, skill uses Master Metrics `source: "tiendanube"`.  
**Note:** If your store is not on TiendaNube, skip this MCP — GA4 Enhanced E-commerce covers sales data.

---

### MCP 4 — `Master Metrics` (hub — fallback + Meta Ads)

**What it unlocks:** Meta Ads (Facebook + Instagram) as primary source. Also serves as fallback for GA4, Google Ads, and TiendaNube when their dedicated MCPs are unavailable.

**Type:** Claude.ai native integration — configured at account level, not locally.

1. Go to [claude.ai](https://claude.ai) → Settings → Integrations → **Master Metrics** → Connect
2. Follow the OAuth flow to link Google Ads, Meta Ads, and/or TiendaNube
3. Verify in Claude Code: `What data sources do I have in Master Metrics?`

---

### What each MCP unlocks

| Report section | Primary source | Fallback | Without any |
|---|---|---|---|
| GA4 funnel + CVR by device | `analytics-mcp` | Master Metrics `google_analytics` | No funnel data |
| Google Ads ROAS/CPA/quality | `google-ads-mcp` (GAQL) | Master Metrics `google` | Google Ads skipped |
| Meta Ads ROAS/CPA/paid funnel | Master Metrics `meta` | — | Meta Ads skipped |
| TiendaNube orders + abandonment | `tiendanube-mcp` | Master Metrics `tiendanube` | GA4 e-commerce used |
| Multi-source triangulation | All 4 sources combined | Partial (with what's available) | Skipped |
| Pinterest / YouTube Ads | Master Metrics | — | Not shown |

**The report always generates** — each missing source is documented in the report.

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
