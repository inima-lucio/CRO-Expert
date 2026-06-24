#!/usr/bin/env python3
"""
CRO Expert — Site Crawler
Discovers key pages on an e-commerce site for CRO analysis.
Usage: python crawler.py <url>
"""

import sys
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import re


class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self.tech_signals = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href and not href.startswith("#") and not href.startswith("mailto:") and not href.startswith("tel:"):
                full_url = urllib.parse.urljoin(self.base_url, href)
                if urllib.parse.urlparse(full_url).netloc == urllib.parse.urlparse(self.base_url).netloc:
                    self.links.append(full_url)
        # Detect tech signals
        if tag == "script" and "src" in attrs_dict:
            src = attrs_dict["src"] or ""
            if "shopify" in src: self.tech_signals.append("Shopify")
            if "woocommerce" in src or "woo" in src: self.tech_signals.append("WooCommerce")
            if "vtex" in src: self.tech_signals.append("VTEX")
            if "magento" in src: self.tech_signals.append("Magento")
            if "prestashop" in src: self.tech_signals.append("PrestaShop")


def classify_url(url, base_domain):
    """Classify a URL by page type based on path patterns."""
    path = urllib.parse.urlparse(url).path.lower()

    # Checkout patterns
    if any(p in path for p in ["/checkout", "/cart", "/carrito", "/cesta", "/panier", "/kasse", "/order"]):
        if any(p in path for p in ["/cart", "/carrito", "/cesta", "/panier"]):
            return "cart"
        return "checkout"

    # Product page patterns
    if any(p in path for p in ["/product/", "/products/", "/producto/", "/p/", "/item/", "/dp/", "-p-", "/detail"]):
        return "pdp"

    # Category/listing patterns
    if any(p in path for p in ["/category/", "/categories/", "/collection/", "/collections/", "/catalog/",
                                  "/categoria/", "/categorie/", "/shop/", "/tienda/", "/boutique/", "/c/"]):
        return "plp"

    # Search results
    if any(p in path for p in ["/search", "/buscar", "/busqueda", "/recherche", "?q=", "?s="]):
        return "search"

    # Home
    if path in ["/", ""]:
        return "home"

    return "other"


def fetch_page(url, timeout=10):
    """Fetch a page and return HTML content."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None


def detect_platform(html):
    """
    Detect web/e-commerce platform using multi-signal confidence scoring.
    Each signal has a weight; a platform needs score >= 10 to be reported.
    This avoids false positives from coincidental substring matches.
    """
    if not html:
        return ["Unknown"]

    h  = html           # original case (for case-sensitive signals)
    hl = html.lower()   # lowercase (for case-insensitive signals)

    # (pattern, weight, case_sensitive)
    # Score >= 10 → confirmed.  Single weak signals (weight < 10) are never enough alone.
    PLATFORMS = {
        "Shopify": [
            ("cdn.shopify.com",              15, False),
            ("shopify.com/s/files",          15, False),
            ("Shopify.theme",                10, True),
            ("shopify-buy",                  10, False),
            ("myshopify.com",                15, False),
            ("shopify-section",               5, False),
        ],
        "WooCommerce": [
            ("wp-content/plugins/woocommerce", 15, False),
            ("woocommerce",                  10, False),
            ("wp-content/",                   5, False),
            ("wp-includes/",                  5, False),
        ],
        "WordPress": [
            ("wp-content/",                   8, False),
            ("wp-includes/",                  8, False),
            ("/wp-json/",                      8, False),
            ("generator\" content=\"WordPress", 15, False),
            ("generator' content='WordPress",  15, False),
        ],
        "Magento": [
            ("Mage.Cookies",                 15, True),
            ("MAGE_CACHE_STORAGE",           15, True),
            ("mage/cookies",                 15, False),
            ("mage-init",                    12, True),
            ("/static/version",              10, False),
            ("requirejs/require.js",          5, False),
            ("magento",                       8, False),
        ],
        "Tiendanube": [
            ("tiendanube.com",               15, False),
            ("nuvemshop.com.br",             15, False),
            ("d26lpennugtm8s.cloudfront.net", 15, False),
            ("nube-sdk",                     15, False),
            ("tiendanube",                   10, False),
        ],
        "VTEX": [
            ("vtex.com",                     15, False),
            ("vtexcommerce",                 15, False),
            ("vteximg",                      15, False),
            ("io.vtex.com",                  15, False),
        ],
        "PrestaShop": [
            ("prestashop",                   12, False),
            ("generator\" content=\"PrestaShop", 15, False),
        ],
        "BigCommerce": [
            ("bigcommerce.com",              15, False),
            ("bc-sf-filter",                 10, False),
            ("bigcommerce",                  10, False),
        ],
        "Salesforce Commerce": [
            ("demandware.net",               15, False),
            ("salesforce.com/s/",            15, False),
            ("demandware.edgesuite",         15, False),
        ],
        "MercadoShops": [
            ("mercadoshops",                 15, False),
        ],
        "Wix": [
            ("wix.com/",                     15, False),
            ("wixstatic.com",                15, False),
            ("parastorage.com",              15, False),
            ("_wix_browser_id",              10, True),
        ],
        "Squarespace": [
            ("squarespace.com",              15, False),
            ("sqsp.net",                     15, False),
            ("generator\" content=\"Squarespace", 15, False),
        ],
        "Webflow": [
            ("webflow.com",                  15, False),
            ("uploads-ssl.webflow.com",      15, False),
            ("data-wf-page=",                15, False),
            ("data-wf-site=",                15, False),
        ],
        "Jumpseller": [
            ("jumpseller.com",               15, False),
            ("jumpseller",                   10, False),
        ],
        "Next.js": [
            ("__NEXT_DATA__",                15, True),
            ("_next/static",                 12, False),
        ],
        "Nuxt.js": [
            ("__NUXT_DATA__",                15, True),
            ("/_nuxt/",                      12, False),
            ("__nuxt",                        8, True),
        ],
    }

    scores = {}
    for platform, signals in PLATFORMS.items():
        score = 0
        for pattern, weight, case_sensitive in signals:
            haystack = h  if case_sensitive else hl
            needle   = pattern if case_sensitive else pattern.lower()
            if needle in haystack:
                score += weight
        if score >= 10:
            scores[platform] = score

    # WooCommerce implies WordPress — show the more specific one only
    if "WooCommerce" in scores:
        scores.pop("WordPress", None)

    if scores:
        return [p for p, _ in sorted(scores.items(), key=lambda x: -x[1])]

    # ── Fallback 1: meta generator tag ────────────────────────────────────────
    gen = re.search(
        r'<meta[^>]+name=["\']generator["\'][^>]+content=["\'](.*?)["\']'
        r'|<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']generator["\']',
        hl
    )
    if gen:
        name = (gen.group(1) or gen.group(2) or "").strip()
        if name:
            return [name.title()]

    # ── Fallback 2: JS framework fingerprinting ───────────────────────────────
    if '"react"' in hl or "react-dom" in hl or "react.production.min" in hl:
        return ["Custom (React)"]
    if "vue.js" in hl or "vue.min.js" in hl or "vue.runtime" in hl:
        return ["Custom (Vue.js)"]
    if "angular" in hl and "ng-app" in hl:
        return ["Custom (Angular)"]

    # ── Fallback 3: generic custom site ──────────────────────────────────────
    return ["Custom HTML / Ad-hoc"]


def detect_features(html):
    """Detect notable CRO features present on the page (static HTML only)."""
    if not html:
        return []

    features = []

    checks = {
        "Live chat (Cliengo)":    ["cliengo", "cliengo.com"],
        "Live chat (Intercom)":   ["intercom.io", "intercomcdn"],
        "Live chat (Zendesk)":    ["zendesk.com", "zdassets.com"],
        "Live chat (Tawk.to)":    ["tawk.to"],
        "Live chat (Crisp)":      ["crisp.chat"],
        "Live chat (Tidio)":      ["tidio"],
        "Live chat (HubSpot)":    ["hubspot"],
        "Live chat (Drift)":      ["drift.com"],
        "Google Tag Manager":     ["googletagmanager.com", "gtm.js"],
        "Google Analytics":       ["google-analytics.com", "gtag/js", "ga.js"],
        "Meta Pixel":             ["connect.facebook.net", "fbevents.js", "fbq("],
        "Google Ads (remarketing)": ["googleadservices.com", "googlesyndication", "adwords"],
        "Email popup / Klaviyo":  ["klaviyo"],
        "Email popup / Mailchimp":["mailchimp"],
        "Email popup / Omnisend": ["omnisend"],
        "Countdown timer":        ["countdown", "countdowntimer"],
        "Trust badges":           ["trustpilot", "mcafee", "norton", "sello-confianza"],
        "Reviews (Yotpo)":        ["yotpo"],
        "Reviews (Judge.me)":     ["judge.me"],
        "Reviews (Okendo)":       ["okendo"],
        "Wishlist":               ["wishlist", "lista-de-deseos", "favoritos"],
        "Express checkout (MercadoPago)": ["mercadopago", "sdk.mercadopago"],
        "Express checkout (PayPal)": ["paypal.com/sdk", "paypalobjects"],
        "Express checkout (Stripe)": ["stripe.com/v3", "stripe.js"],
        "Free shipping bar":      ["free-shipping", "envio-gratis", "envío gratis"],
        "Back in stock":          ["back-in-stock", "notify-me", "avisame"],
        "Recently viewed":        ["recently-viewed", "visto-recientemente"],
        "Hotjar / Heatmaps":      ["hotjar.com", "hj("],
        "Microsoft Clarity":      ["clarity.ms"],
        "Optimizely / A-B test":  ["optimizely", "abtasty", "vwo.com", "googleoptimize"],
    }

    html_lower = html.lower()
    for feature, patterns in checks.items():
        if any(p in html_lower for p in patterns):
            features.append(feature)

    return features


def detect_js_features(url, timeout=15):
    """
    Detect JS-rendered features using Playwright (floating buttons, chat widgets, etc.).
    Returns a dict with confirmed presence/absence of key CRO elements.
    Falls back gracefully if Playwright is not installed.
    """
    result = {
        "whatsapp_button": False,
        "whatsapp_url": None,
        "live_chat_widget": False,
        "sticky_header": False,
        "exit_intent_popup": False,
        "cookie_banner": False,
        "checked": False,
    }

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return result  # Playwright not installed — skip JS detection

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(
                viewport={"width": 1440, "height": 900},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            page.wait_for_timeout(2500)  # Let JS widgets initialize

            result["checked"] = True

            # ── WhatsApp button detection ──────────────────────────────────────
            wa_selectors = [
                "a[href*='wa.me']",
                "a[href*='whatsapp.com/send']",
                "a[href*='api.whatsapp.com']",
                "[class*='whatsapp']",
                "[id*='whatsapp']",
                "[class*='btn-whatsapp']",
                "[class*='whatsapp-btn']",
                "[class*='wp-widget-chat']",
            ]
            for sel in wa_selectors:
                els = page.query_selector_all(sel)
                for el in els:
                    try:
                        if el.is_visible():
                            result["whatsapp_button"] = True
                            href = el.get_attribute("href") or ""
                            if href:
                                result["whatsapp_url"] = href
                            break
                    except Exception:
                        pass
                if result["whatsapp_button"]:
                    break

            # ── Live chat widget ───────────────────────────────────────────────
            chat_selectors = [
                "#intercom-container", "#tidio-chat", ".tawk-min-container",
                "[data-testid='chat-widget']", "#hubspot-messages-iframe-container",
                ".drift-widget", "#crisp-chatbox",
            ]
            for sel in chat_selectors:
                el = page.query_selector(sel)
                if el:
                    try:
                        if el.is_visible():
                            result["live_chat_widget"] = True
                            break
                    except Exception:
                        pass

            # ── Cookie banner ──────────────────────────────────────────────────
            cookie_selectors = [
                "[class*='cookie']", "[id*='cookie']",
                "[class*='consent']", "[id*='consent']",
                "[class*='gdpr']",
            ]
            for sel in cookie_selectors:
                el = page.query_selector(sel)
                if el:
                    try:
                        if el.is_visible():
                            result["cookie_banner"] = True
                            break
                    except Exception:
                        pass

            ctx.close()
            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def crawl_site(base_url, max_pages=50):
    """Crawl a site and discover key pages."""

    # Normalize URL
    if not base_url.startswith("http"):
        base_url = "https://" + base_url

    base_domain = urllib.parse.urlparse(base_url).netloc

    print(f"\n🔍 Crawling: {base_url}", flush=True)
    print("─" * 50, flush=True)

    # Fetch homepage first
    home_html = fetch_page(base_url)

    results = {
        "base_url": base_url,
        "domain": base_domain,
        "platform": detect_platform(home_html) if home_html else [],
        "pages": {
            "home": [base_url],
            "plp": [],
            "pdp": [],
            "cart": [],
            "checkout": [],
            "search": [],
            "other": []
        },
        "features": detect_features(home_html) if home_html else [],
        "crawled_count": 0,
    }

    # Parse homepage links
    if home_html:
        parser = LinkParser(base_url)
        parser.feed(home_html)

        discovered_links = list(set(parser.links))
        results["crawled_count"] = len(discovered_links)

        # Classify links
        for link in discovered_links[:max_pages]:
            page_type = classify_url(link, base_domain)
            if page_type in results["pages"]:
                if link not in results["pages"][page_type]:
                    results["pages"][page_type].append(link)

    # Try common paths if not found
    common_paths = {
        "cart": ["/cart", "/carrito", "/cesta", "/panier", "/basket", "/shopping-cart"],
        "checkout": ["/checkout", "/pago", "/checkout/information"],
        "search": ["/search?q=", "/buscar?q="],
    }

    for page_type, paths in common_paths.items():
        if not results["pages"][page_type]:
            for path in paths:
                url = urllib.parse.urljoin(base_url, path)
                if fetch_page(url):
                    results["pages"][page_type].append(url)
                    break

    # Limit results to most relevant pages
    for page_type in results["pages"]:
        results["pages"][page_type] = results["pages"][page_type][:5]

    return results


def print_report(results):
    """Print a human-readable summary."""
    print(f"\n✅ Site Discovery Complete")
    print(f"{'─' * 50}")
    print(f"Domain: {results['domain']}")

    if results["platform"]:
        print(f"Platform: {', '.join(results['platform'])}")
    else:
        print("Platform: Unknown / Custom")

    if results["features"]:
        print(f"Features detected: {', '.join(results['features'])}")

    print(f"\n📄 Pages discovered:")
    for page_type, urls in results["pages"].items():
        if urls:
            print(f"\n  {page_type.upper()} ({len(urls)} page{'s' if len(urls) > 1 else ''}):")
            for url in urls[:3]:
                print(f"    - {url}")

    # Warnings
    missing = [p for p, urls in results["pages"].items()
               if not urls and p in ["home", "plp", "pdp", "cart", "checkout"]]
    if missing:
        print(f"\n⚠️  Could not auto-discover: {', '.join(missing)}")
        print("   Please provide these URLs manually for complete analysis.")

    print(f"\n{'─' * 50}")
    print("JSON output saved to: cro_discovery.json")


def main():
    if len(sys.argv) < 2:
        print("Usage: python crawler.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    results = crawl_site(url)

    # ── JS feature detection (Playwright) ─────────────────────────────────────
    print("\n🔎 Detecting JS-rendered features (WhatsApp, chat, popups)...", flush=True)
    js_features = detect_js_features(url)
    results["js_features"] = js_features

    # Merge confirmed JS features into the features list for visibility
    if js_features.get("checked"):
        if js_features.get("whatsapp_button"):
            wa_url = js_features.get("whatsapp_url", "")
            label = f"WhatsApp button (visible, flotante) — {wa_url}" if wa_url else "WhatsApp button (visible, flotante)"
            results["features"].append(label)
            print(f"   ✅ WhatsApp button VISIBLE — {wa_url or 'no URL captured'}", flush=True)
        else:
            results["features"].append("⚠️ Sin botón WhatsApp visible")
            print("   ⚠️  No WhatsApp button detected", flush=True)

        if js_features.get("live_chat_widget"):
            results["features"].append("Live chat widget (JS-rendered)")
            print("   ✅ Live chat widget detected", flush=True)

        if js_features.get("cookie_banner"):
            results["features"].append("Cookie banner (JS-rendered)")
    else:
        print("   ℹ️  Playwright not available — JS detection skipped", flush=True)

    # Print human-readable report
    print_report(results)

    # Save JSON for other scripts
    with open("cro_discovery.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    main()
