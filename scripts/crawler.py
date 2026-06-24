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
    """Detect e-commerce platform from HTML."""
    signals = []
    if not html:
        return signals

    patterns = {
        "Shopify": ["shopify.com", "shopify-cdn", "Shopify.theme", "cdn.shopify"],
        "WooCommerce": ["woocommerce", "wp-content/plugins/woocommerce"],
        "VTEX": ["vtex.com", "vtexcommerce", "vteximg"],
        "Magento": ["mage/", "magento", "Mage.Cookies"],
        "PrestaShop": ["prestashop", "/modules/", "presta"],
        "BigCommerce": ["bigcommerce", "bc-sf-filter"],
        "Salesforce Commerce": ["demandware", "salesforce.com/s/"],
        "Tiendanube": ["tiendanube", "nube-sdk"],
        "MercadoShops": ["mercadoshops"],
    }

    for platform, patterns_list in patterns.items():
        if any(p in html for p in patterns_list):
            signals.append(platform)

    return list(set(signals))


def detect_features(html):
    """Detect notable CRO features present on the page."""
    if not html:
        return []

    features = []

    checks = {
        "Live chat": ["intercom", "zendesk", "tawk.to", "livechat", "drift.com", "crisp.chat", "tidio"],
        "Email popup": ["popup", "modal", "klaviyo", "mailchimp", "omnisend"],
        "Countdown timer": ["countdown", "timer", "account_down"],
        "Trust badges": ["trustpilot", "verified", "secure", "ssl", "mcafee", "norton"],
        "Reviews": ["reviews", "reseñas", "ratings", "yotpo", "stamped", "judge.me", "okendo"],
        "Wishlist": ["wishlist", "lista de deseos", "favoritos", "save for later"],
        "Express checkout": ["apple-pay", "google-pay", "paypal", "klarna", "afterpay", "express"],
        "Free shipping bar": ["free.shipping", "envio.gratis", "livraison.gratuite"],
        "Back in stock": ["back.in.stock", "notify.me", "avisa"],
        "Recently viewed": ["recently.viewed", "visto.recientemente"],
    }

    html_lower = html.lower()
    for feature, patterns in checks.items():
        if any(p in html_lower for p in patterns):
            features.append(feature)

    return features


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

    # Print human-readable report
    print_report(results)

    # Save JSON for other scripts
    with open("cro_discovery.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    main()
