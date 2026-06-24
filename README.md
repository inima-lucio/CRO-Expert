# CRO Expert — Claude Code Skill

**Full-funnel conversion audit powered by real data.**  
Built by [Lucio Monopoli](mailto:inima.lucio@gmail.com) · [INIMA Interactive](https://inimainteractive.com)

---

## What it does

Run `/cro-expert https://your-store.com` in Claude Code and get a **professional HTML/PDF audit report** covering:

- Viewport screenshots (desktop + mobile) with **numbered callout markers** overlaid above the fold
- 4Ps · AIDA · Cialdini · Nielsen framework analysis
- Real GA4 funnel data — auto-discovered by domain, no property ID needed
- Google Ads — ROAS, CPA, CVR by device, landing page quality score per keyword
- Meta Ads (Facebook + Instagram) — ROAS, CPA, paid funnel by campaign and platform
- TiendaNube — real orders, abandoned carts, UTM attribution per order, top products
- **Section 5B — Multi-source triangulation** — cross-references all sources to detect double attribution, real vs. claimed ROAS, and mobile CVR gaps
- Priority matrix with Impact × Effort recommendations
- A/B test plan with sample size calculations
- Client-ready conclusions + 30-day action checklist

The report is a **self-contained HTML file** — inline screenshots, SVG charts, no external dependencies. Works offline and converts to PDF.

**Works for any site type** — e-commerce (Shopify, WooCommerce, VTEX, Tiendanube, Magento, custom) and lead generation (agencies, SaaS, professional services). Each data source degrades gracefully — the report always generates.

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

## MCP Connections

The skill uses **5 independent MCPs** as data sources. You don't need all of them — the report always generates with whatever is available. Each missing source is documented in the report with a note explaining what data was skipped.

**Priority rule:** dedicated MCP → Master Metrics fallback → heuristic analysis only.

---

### ✅ MCP 1 — `analytics-mcp` (Google Analytics 4)

**Status: Supported — connect to activate**

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
**Fallback if unavailable:** Master Metrics `source: "google_analytics"`.

---

### ✅ MCP 2 — `google-ads-mcp` (Google Ads API via GAQL)

**Status: Supported — connect to activate**

**What it unlocks:** Direct GAQL queries — campaign ROAS/CPA/CVR, performance by device, landing page quality score per keyword, accessible customer list. Supports MCC (manager accounts) for agencies.

**Prerequisites:**
1. A Google Ads Developer Token ([Google Ads API Center](https://ads.google.com/aw/apiaccess))
2. Your Google Cloud project ID
3. Manager account ID if using MCC

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
**Fallback if unavailable:** Master Metrics `source: "google"`.

---

### ⚠️ MCP 3 — `meta-ads-mcp` (Meta Ads — Facebook + Instagram)

**Status: Not connected yet — setup pending**

**What it unlocks:** Meta Marketing API direct — campaigns, ad sets, creatives, pixel events (purchase, add_to_cart, initiate_checkout, view_content), ROAS and CPA by campaign, device breakdown (mobile vs. desktop), Facebook vs. Instagram split.

**Prerequisites:**
1. A Meta App in [developers.facebook.com](https://developers.facebook.com) with permissions: `ads_read`, `ads_management`, `business_management`
2. A long-lived access token (valid 60 days) or a System User with a permanent token
3. Your Business ID from [business.facebook.com](https://business.facebook.com)

**Setup:**
```bash
npm install -g meta-ads-mcp
# or use npx (no install needed)
```

Add to `~/.claude/settings.json`:

```json
"meta-ads-mcp": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "meta-ads-mcp"],
  "env": {
    "META_ACCESS_TOKEN": "your-long-lived-access-token",
    "META_BUSINESS_ID": "your-business-id"
  }
}
```

Then in Claude Code: `/mcp` → Reconnect.

**Verify:** Ask `List my Meta Ads accounts` — you should see your ad account IDs.  
**Fallback while not connected:** Master Metrics `source: "meta"` provides aggregated Meta Ads data automatically.

> **Note for token renewal:** Meta long-lived tokens expire after 60 days. Renew via:  
> `https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN`

---

### ✅ MCP 4 — `tiendanube-mcp` (TiendaNube / Nuvemshop)

**Status: Supported — only needed for TiendaNube stores**

**What it unlocks:** Real order data (revenue, AOV, UTM attribution per order), abandoned carts with recovery value, top products, new vs. returning customer split. Direct from TiendaNube API — not aggregated.

**Prerequisites:**
1. A TiendaNube app with API access ([partners.tiendanube.com](https://partners.tiendanube.com))
2. Your store's `access_token` and `store_id`
3. Docker installed locally

**Setup:**
```bash
git clone https://github.com/AlexandreProenca/nuvemshop-mcp-server.git ~/tiendanube-mcp
cd ~/tiendanube-mcp

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
**Fallback if unavailable:** Master Metrics `source: "tiendanube"`.  
**If not TiendaNube:** Skip this MCP — GA4 Enhanced E-commerce covers sales data for other platforms.

---

### ✅ MCP 5 — `Master Metrics` (universal fallback hub)

**Status: Active — configured at account level**

**What it unlocks:** Aggregated data from Google Analytics, Google Ads, Meta Ads, TiendaNube, Pinterest, and YouTube through a single integration. Acts as the fallback for every dedicated MCP above, and as the primary source for platforms without a dedicated MCP (Pinterest, YouTube).

This is a **Claude.ai native integration** — not configured in `settings.json`.

1. Go to [claude.ai](https://claude.ai) → Settings → Integrations → **Master Metrics** → Connect
2. Follow the OAuth flow to link Google Ads, Meta Ads, TiendaNube, and/or Pinterest
3. Verify in Claude Code: `What data sources do I have in Master Metrics?`

**Sources available:**

| source | Data | Role in this skill |
|---|---|---|
| `google_analytics` | GA4 sessions, bounce, CVR | Fallback if `analytics-mcp` is unavailable |
| `google` | Google Ads ROAS, CPA, spend | Fallback if `google-ads-mcp` is unavailable |
| `meta` | Meta Ads ROAS, CPA, funnel | **Primary** while `meta-ads-mcp` is not connected |
| `tiendanube` | TN orders, revenue, abandonment | Fallback if `tiendanube-mcp` is unavailable |
| `pinterest` | Pinterest Ads spend, clicks, ROAS | Primary source (no dedicated MCP yet) |
| `youtube` | YouTube Ads performance | Primary source (no dedicated MCP yet) |

---

### Data availability summary

| Data | Dedicated MCP | Fallback | Without either |
|---|---|---|---|
| Google Analytics 4 | `analytics-mcp` ✅ | Master Metrics `google_analytics` | Heuristic only |
| Google Ads | `google-ads-mcp` ✅ | Master Metrics `google` | Section skipped |
| Meta Ads | `meta-ads-mcp` ⚠️ pending | Master Metrics `meta` ✅ | Section skipped |
| TiendaNube | `tiendanube-mcp` ✅ | Master Metrics `tiendanube` | GA4 e-commerce used |
| Pinterest Ads | *(see planned connections)* | Master Metrics `pinterest` ✅ | Not shown |
| YouTube Ads | *(see planned connections)* | Master Metrics `youtube` ✅ | Not shown |
| TikTok Ads | *(see planned connections)* | — | Not shown |
| LinkedIn Ads | *(see planned connections)* | — | Not shown |

**The report always generates.** Unavailable sources are documented inline.

---

## Planned connections

The skill is designed to add new data sources without changing the core audit logic. Adding a new MCP requires: (1) entry in `settings.json`, (2) a new section in `SKILL.md`, (3) a new audit phase.

| Platform | MCP | Status | What it would unlock |
|---|---|---|---|
| **TikTok Ads** | `tiktok-ads-mcp` | Available on npm — integration pending | TikTok campaign ROAS, CPA, video funnel, demographics |
| **Pinterest Ads** | `pinterest-ads-mcp` | In development — Master Metrics covers basics | Pin performance, shopping campaigns, audience insights |
| **LinkedIn Ads** | `linkedin-ads-mcp` | Community MCP in development | B2B funnel, lead gen forms, company targeting data |
| **Shopify** | Official Shopify MCP | Available — integration pending | Direct orders, abandoned checkouts, product analytics (replaces tiendanube-mcp for Shopify stores) |
| **Klaviyo** | `klaviyo-mcp` | Available — integration pending | Email + SMS revenue attribution, flow performance, list health |
| **Hotjar / Clarity** | REST API via WebFetch | No official MCP yet | Heatmaps, session recordings, rage clicks, scroll maps |

> Want to contribute a new MCP integration? See `SKILL.md` → "MCPs opcionales — Extensibilidad" for the 5-step guide.

---

## Report pages

| # | Page | Content |
|---|---|---|
| Cover | Portada | CRO score gauge (traffic light) + 4 KPI chips |
| 1 | Executive Summary | Score per page + critical issues list + 30/60/90 day roadmap |
| 2 | Page Analysis | Viewport screenshots with numbered visual markers + fold line + AIDA chart |
| 3 | Framework Audit | Cialdini 7 principles + Nielsen 10 heuristics |
| 4 | Data Dashboard | GA4 funnel + platform e-commerce data |
| 5 | Paid Media | Google Ads + Meta Ads + ad vs. landing diagnosis |
| 5B | Multi-source triangulation | Sessions by channel · Engagement by channel · CVR device gap · Organic vs. paid comparison |
| 6 | Recommendations | Impact × Effort matrix + recommendation cards |
| 7 | A/B Test Plan | Summary table + full test specs with sample size calculations |
| 8 | Plugins | CRO tools ranked by conversion impact |
| 9 | Action Plan | Conclusions + 30-day checklist + KPIs to track |

---

## Platform detection

The crawler automatically identifies the site's technology stack before auditing. Supported platforms:

| Platform | Detection method |
|---|---|
| Shopify | `cdn.shopify.com`, `Shopify.theme`, `myshopify.com` |
| WooCommerce | `wp-content/plugins/woocommerce` |
| WordPress | `wp-content/`, `wp-includes/`, meta generator tag |
| Magento | `Mage.Cookies`, `MAGE_CACHE_STORAGE`, `mage-init` |
| Tiendanube | `tiendanube.com`, `nuvemshop.com.br`, `nube-sdk` |
| VTEX | `vtex.com`, `vtexcommerce` |
| Wix | `wixstatic.com`, `parastorage.com` |
| Squarespace | `squarespace.com`, `sqsp.net`, meta generator |
| Webflow | `data-wf-page`, `uploads-ssl.webflow.com` |
| Next.js | `__NEXT_DATA__`, `_next/static` |
| Nuxt.js | `__NUXT_DATA__`, `/_nuxt/` |
| PrestaShop | `prestashop`, meta generator |
| BigCommerce | `bigcommerce.com`, `bc-sf-filter` |
| Jumpseller | `jumpseller.com` |
| Custom / Ad-hoc | Multi-signal scoring — if no platform matches, reports `Custom HTML / Ad-hoc` |

Detection uses **multi-signal confidence scoring** (each platform requires score ≥ 10 from weighted signals) to avoid false positives.

---

## Skill structure

```
cro-expert/
├── SKILL.md                    ← Agent instructions (all phases + data contracts)
├── scripts/
│   ├── crawler.py              ← Auto-discovers pages + platform detection
│   ├── html_analyzer.py        ← HTML & copy CRO analysis
│   ├── report_generator.py     ← Self-contained HTML report with annotated screenshots
│   └── pdf_generator.py        ← PDF export via Playwright
├── references/
│   ├── frameworks.md           ← 4Ps, AIDA, Cialdini, Nielsen criteria
│   ├── scoring.md              ← Scoring rubrics per framework
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

**Q: Do I need all 5 MCPs?**  
A: No. `analytics-mcp` alone gives you the full GA4 analysis. Master Metrics alone covers Meta Ads, Google Ads basics, and TiendaNube. The more MCPs you connect, the richer the multi-source triangulation in Section 5B.

**Q: Does this work for non-e-commerce sites (agencies, SaaS, lead gen)?**  
A: Yes. The framework adapts — the conversion event becomes form submission or WhatsApp contact instead of purchase. GA4 funnel and paid media sections work for any site type.

**Q: Does this work for Shopify / WooCommerce / VTEX?**  
A: Yes. GA4 provides full e-commerce funnel data for any platform. Skip `tiendanube-mcp` and connect the Shopify MCP (planned) for direct order data instead.

**Q: My analytics-mcp shows `invalid_grant`. What do I do?**  
A: Your Google OAuth token expired. Run `gcloud auth application-default login` again with the same scopes, then `/mcp` → Reconnect in Claude Code.

**Q: My meta-ads-mcp token expired. What do I do?**  
A: Meta long-lived tokens expire every 60 days. Exchange your token via the Graph API endpoint (see setup instructions above). Consider creating a System User in Business Manager for a non-expiring token.

**Q: I don't see Master Metrics in claude.ai Integrations.**  
A: Contact [INIMA Interactive](mailto:inima.lucio@gmail.com) to request access.

**Q: Screenshots show no callout markers. Why?**  
A: Markers appear when Claude generates `callout_markers` with x/y coordinates during Phase 1. Verify the analysis JSONs include this field — see the data contract in SKILL.md.

**Q: The platform was detected incorrectly. What do I do?**  
A: The crawler uses multi-signal scoring to avoid false positives. If detection is wrong, it means the site has unusual signals. You can manually specify the platform in the first prompt: `/cro-expert https://site.com --platform shopify`.

---

## License

MIT — free to use, modify, and distribute. Attribution appreciated.

---

*Made with ❤️ by [INIMA Interactive](https://inimainteractive.com) · Buenos Aires, Argentina*
