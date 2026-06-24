#!/usr/bin/env python3
"""
CRO Expert — HTML & Copy Analyzer
Analyzes a page's HTML structure for CRO signals.
Usage: python html_analyzer.py <url> [page_type]
       page_type: home | plp | pdp | cart | checkout
"""

import sys
import json
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse


class CROHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.ctas = []
        self.forms = []
        self.images = []
        self.prices = []
        self.trust_signals = []
        self.social_proof = []
        self.urgency_signals = []
        self.nav_items = []
        self._in_title = False
        self._in_h1 = False
        self._in_h2 = False
        self._in_h3 = False
        self._current_tag = ""
        self._current_attrs = {}
        self._current_form = {}
        self._in_form = False
        self._form_fields = 0
        self.all_text = []
        self._breadcrumbs = False
        # WhatsApp / chat widgets
        self.whatsapp_signals = []   # list of dicts with detection details
        self._in_script = False
        self._script_buffer = []

    # ── WhatsApp detection helpers ────────────────────────────────────────
    _WA_HREF_PATTERNS = ["wa.me/", "api.whatsapp.com/send", "whatsapp://send", "web.whatsapp.com"]
    _WA_CLASS_KEYWORDS = ["whatsapp", "wapp", "wa-btn", "wa-float", "wa-chat", "wts-chat",
                          "wpp-button", "socialwidget", "wati-widget", "wp-whatsapp"]
    _WA_ID_KEYWORDS   = ["whatsapp", "wa-btn", "wa-chat", "wati", "wpp"]
    # Third-party scripts known to inject floating WA buttons
    _WA_SCRIPT_DOMAINS = ["wati.io", "elfsight.com", "getbutton.io", "socialintents.com",
                          "wappex.com", "joinchat.net", "callbell.eu", "tidio.co",
                          "mylivechat.com", "wa-link.io", "zopim.com"]
    # Inline CSS signals: position:fixed + bottom/right suggests floating widget
    _WA_STYLE_SIGNALS  = ["position:fixed", "position: fixed"]

    # SVG structural tags — never a button on their own
    _SVG_TAGS = {"symbol", "path", "defs", "svg", "g", "use", "circle", "rect",
                 "polygon", "polyline", "line", "ellipse", "clippath", "mask",
                 "linearGradient", "radialGradient", "stop", "filter", "feBlend"}

    def _check_whatsapp(self, tag, attrs_dict):
        """Returns a detection dict if this element looks like a WA floating button, else None."""
        # SVG definition tags are icon assets, not interactive elements
        if tag.lower() in self._SVG_TAGS:
            return None

        href     = attrs_dict.get("href", "").lower()
        classes  = attrs_dict.get("class", "").lower()
        elem_id  = attrs_dict.get("id", "").lower()
        style    = attrs_dict.get("style", "").lower().replace(" ", "")
        data_str = " ".join(str(v) for k, v in attrs_dict.items() if k.startswith("data-")).lower()
        src      = attrs_dict.get("src", "").lower()

        reasons = []

        # Href pointing directly to WhatsApp — strongest signal
        if any(p in href for p in self._WA_HREF_PATTERNS):
            reasons.append(f"href={href[:60]}")

        # Class/id signals only matter on interactive or positioned elements
        interactive = tag in {"a", "button", "div", "span", "section", "aside", "li", "img"}
        if interactive:
            if any(k in classes for k in self._WA_CLASS_KEYWORDS):
                reasons.append("class contains WA keyword")
            if any(k in elem_id for k in self._WA_ID_KEYWORDS):
                reasons.append(f"id={elem_id[:40]}")

        if "whatsapp" in data_str or "wa.me" in data_str:
            reasons.append("data-* attribute references WhatsApp")

        if "position:fixed" in style and ("bottom" in style or "right" in style):
            if "whatsapp" in (classes + elem_id + href + data_str):
                reasons.append("position:fixed + WA reference → floating widget")

        if any(k in src for k in ["whatsapp", "wa-logo", "wapp"]) and tag == "img":
            reasons.append(f"img src={src[:50]}")

        if not reasons:
            return None

        is_floating = (
            "position:fixed" in style
            or any(k in classes for k in ["float", "fixed", "sticky", "fab", "widget"])
        )
        return {"tag": tag, "reasons": reasons, "is_floating": is_floating}

    # ── End WhatsApp helpers ───────────────────────────────────────────────

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._current_tag = tag
        self._current_attrs = attrs_dict

        # Script buffering — needed to scan inline JS for WA widget init code
        if tag == "script":
            self._in_script = True
            self._script_buffer = []
            src = attrs_dict.get("src", "").lower()
            if any(domain in src for domain in self._WA_SCRIPT_DOMAINS):
                self.whatsapp_signals.append({
                    "tag": "script[src]",
                    "reasons": [f"known WA-widget provider in src: {src[:80]}"],
                    "is_floating": True,
                })
            return

        # WhatsApp element detection (any tag can host the button)
        wa = self._check_whatsapp(tag, attrs_dict)
        if wa:
            self.whatsapp_signals.append(wa)

        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "h2":
            self._in_h2 = True
        elif tag == "h3":
            self._in_h3 = True
        elif tag == "meta":
            if attrs_dict.get("name", "").lower() == "description":
                self.meta_description = attrs_dict.get("content", "")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            text_hint = attrs_dict.get("aria-label", "") or attrs_dict.get("title", "")
            role = attrs_dict.get("role", "")
            classes = attrs_dict.get("class", "").lower()
            # Detect CTA-like links
            if any(k in classes for k in ["btn", "button", "cta", "add-to-cart", "atc", "buy", "checkout", "comprar", "añadir"]):
                self.ctas.append({"tag": "a", "href": href, "class": classes, "hint": text_hint})
        elif tag == "button":
            classes = attrs_dict.get("class", "").lower()
            btn_type = attrs_dict.get("type", "")
            name = attrs_dict.get("name", "").lower()
            aria = attrs_dict.get("aria-label", "").lower()
            self.ctas.append({"tag": "button", "class": classes, "type": btn_type, "aria": aria})
        elif tag == "form":
            self._in_form = True
            self._form_fields = 0
            self._current_form = {
                "action": attrs_dict.get("action", ""),
                "method": attrs_dict.get("method", "get"),
                "id": attrs_dict.get("id", ""),
                "class": attrs_dict.get("class", ""),
            }
        elif tag in ["input", "select", "textarea"] and self._in_form:
            input_type = attrs_dict.get("type", "text").lower()
            if input_type not in ["hidden", "submit", "button", "checkbox", "radio"]:
                self._form_fields += 1
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            width = attrs_dict.get("width", "")
            height = attrs_dict.get("height", "")
            classes = attrs_dict.get("class", "").lower()
            self.images.append({
                "src": src[:80] if src else "",
                "alt": alt[:60] if alt else "",
                "has_alt": bool(alt),
                "is_likely_product": any(k in (src + classes).lower() for k in ["product", "item", "prod", "featured"]),
                "width": width,
                "height": height,
            })
        # Trust signal detection
        img_src = attrs_dict.get("src", "").lower()
        img_alt = attrs_dict.get("alt", "").lower()
        if any(t in img_src + img_alt for t in ["ssl", "secure", "visa", "mastercard", "paypal",
                                                    "trustpilot", "verified", "norton", "mcafee",
                                                    "bbva", "santander", "pago seguro"]):
            self.trust_signals.append(img_alt or img_src[:40])

        # Breadcrumb detection
        aria_label = attrs_dict.get("aria-label", "").lower()
        classes = attrs_dict.get("class", "").lower()
        if "breadcrumb" in classes or "breadcrumb" in aria_label or "miga" in classes:
            self._breadcrumbs = True

    def handle_endtag(self, tag):
        if tag == "script" and self._in_script:
            self._in_script = False
            script_text = " ".join(self._script_buffer).lower()
            # Scan inline JS for WhatsApp widget initialization patterns
            wa_js_patterns = [
                # Direct WA URLs
                "wa.me/", "api.whatsapp.com", "whatsapp://send",
                # Third-party widget providers
                "wati", "getbutton", "elfsight", "joinchat", "callbell",
                "socialintents", "wappex", "wa-link",
                # Common JS config keys
                "whatsappbuttoncolor", "whatsappphonenumber",
                "wafloating", "wppconnect",
                "whatsapp_phone", "phone_whatsapp",
                # Tienda Nube native WhatsApp button
                # TN injects a fixed bottom button and references it in scripts like:
                #   "// Whatsapp button position"  +  "js-btn-fixed-bottom"
                "whatsapp button position",
                "js-btn-fixed-bottom",
                # Shopify / WooCommerce common app patterns
                "whatsapp-chat-widget", "wp-whatsapp",
            ]
            matched = [p for p in wa_js_patterns if p in script_text]
            if matched:
                # Tienda Nube's native button requires both signals together
                is_tn_native = (
                    "whatsapp button position" in script_text
                    and "js-btn-fixed-bottom" in script_text
                )
                self.whatsapp_signals.append({
                    "tag": "script[inline]",
                    "reasons": [
                        f"inline JS contains: {', '.join(matched[:3])}"
                        + (" [Tienda Nube native WA button]" if is_tn_native else "")
                    ],
                    "is_floating": True,
                })
            self._script_buffer = []
            return

        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "h2":
            self._in_h2 = False
        elif tag == "h3":
            self._in_h3 = False
        elif tag == "form" and self._in_form:
            self._current_form["field_count"] = self._form_fields
            self.forms.append(self._current_form)
            self._in_form = False
            self._form_fields = 0

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return

        if self._in_script:
            self._script_buffer.append(data)
            return

        if self._in_title:
            self.title += data
        elif self._in_h1:
            self.h1.append(data)
        elif self._in_h2:
            self.h2.append(data)
        elif self._in_h3:
            self.h3.append(data)

        # Price detection (€, $, £, R$, S/.)
        price_pattern = r'[\$€£][\s]?\d+[,.]?\d*|R\$[\s]?\d+|\d+[,.]?\d*[\s]?[\$€£]|S\/\.[\s]?\d+'
        if re.search(price_pattern, data):
            self.prices.append(data.strip())

        # Social proof signals in text
        sp_patterns = [
            r'\d+[\s,.]?\d*\s*(reviews?|reseñas?|valoraciones?|avis|bewertungen?)',
            r'\d+[\s,.]?\d*\s*(customers?|clientes?|compradores?)',
            r'(best.?seller|más vendido|top.?seller|trending)',
            r'\d+\s*(personas?|people|persones?)\s*(han comprado|bought|viewed)',
        ]
        for pattern in sp_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                self.social_proof.append(data.strip()[:80])

        # Urgency signals in text
        urgency_patterns = [
            r'(only|solo|sólo|apenas|queda[n]?|left|reste)\s+\d+',
            r'(limited|limitado|agotándose|last\s+chance)',
            r'\d+:\d+:\d+',  # countdown timer
            r'(offer ends|oferta termina|termine le)',
            r'(\d+\s+(hours?|horas?|heures?)\s+(left|remaining|restantes?))',
        ]
        for pattern in urgency_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                self.urgency_signals.append(data.strip()[:80])

        # Accumulate all text for copy analysis
        if len(data) > 10:
            self.all_text.append(data)


def _summarize_whatsapp(signals):
    """Collapse raw WA signals into a clean summary dict."""
    if not signals:
        return {"detected": False, "floating": False, "signals": []}

    # Deduplicate by reason text
    seen = set()
    unique = []
    for s in signals:
        key = s["tag"] + "|" + "|".join(s["reasons"])
        if key not in seen:
            seen.add(key)
            unique.append(s)

    floating = any(s["is_floating"] for s in unique)
    return {
        "detected": True,
        "floating": floating,
        "signal_count": len(unique),
        "signals": [{"tag": s["tag"], "reason": s["reasons"][0]} for s in unique[:5]],
        "note": (
            "Floating WhatsApp button detected — positive for mobile conversion (direct channel)"
            if floating else
            "WhatsApp link detected (not clearly floating/fixed position)"
        ),
    }


def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"⚠️  Could not fetch {url}: {e}")
        return None


def analyze_page(url, page_type="unknown"):
    """Run full CRO HTML analysis on a page."""

    html = fetch_html(url)
    if not html:
        return {"error": f"Could not fetch {url}"}

    parser = CROHTMLParser()
    parser.feed(html)

    # Post-processing
    title = parser.title.strip()
    h1 = [h.strip() for h in parser.h1 if h.strip()]
    h2 = [h.strip() for h in parser.h2 if h.strip()]

    # Deduplicate
    prices = list(set(parser.prices))[:10]
    social_proof = list(set(parser.social_proof))[:5]
    urgency_signals = list(set(parser.urgency_signals))[:5]

    # CTA analysis
    cta_count = len(parser.ctas)
    cta_texts = [c.get("aria", "") or c.get("hint", "") or c.get("class", "")[:30] for c in parser.ctas][:8]

    # Form analysis
    checkout_forms = [f for f in parser.forms if any(
        k in (f.get("action", "") + f.get("id", "") + f.get("class", "")).lower()
        for k in ["checkout", "pago", "payment", "billing", "shipping", "address"]
    )]

    # Image analysis
    product_images = [i for i in parser.images if i["is_likely_product"]]
    images_without_alt = [i for i in parser.images if not i["has_alt"]]

    # Build findings
    findings = {
        "url": url,
        "page_type": page_type,
        "meta": {
            "title": title,
            "title_length": len(title),
            "title_ok": 30 <= len(title) <= 65,
            "meta_description": parser.meta_description[:160],
            "meta_desc_length": len(parser.meta_description),
            "meta_desc_ok": 120 <= len(parser.meta_description) <= 160,
        },
        "structure": {
            "h1_count": len(h1),
            "h1_texts": h1[:3],
            "h1_ok": len(h1) == 1,
            "h2_count": len(h2),
            "h2_sample": h2[:5],
            "has_breadcrumbs": parser._breadcrumbs,
        },
        "ctas": {
            "total_count": cta_count,
            "sample_texts": cta_texts,
            "cta_density": "high" if cta_count > 5 else "medium" if cta_count > 2 else "low",
        },
        "pricing": {
            "prices_found": prices,
            "price_count": len(prices),
            "has_discount_signals": len(prices) > 1,  # original + sale price
        },
        "social_proof": {
            "signals_found": social_proof,
            "has_reviews": bool(social_proof),
            "urgency_signals": urgency_signals,
        },
        "trust": {
            "trust_signals": list(set(parser.trust_signals))[:5],
            "trust_count": len(set(parser.trust_signals)),
        },
        "forms": {
            "form_count": len(parser.forms),
            "checkout_forms": len(checkout_forms),
            "avg_field_count": sum(f.get("field_count", 0) for f in parser.forms) / max(len(parser.forms), 1),
            "high_friction": any(f.get("field_count", 0) > 5 for f in checkout_forms),
        },
        "images": {
            "total": len(parser.images),
            "product_images": len(product_images),
            "missing_alt": len(images_without_alt),
            "alt_coverage": f"{(1 - len(images_without_alt)/max(len(parser.images),1))*100:.0f}%",
        },
        "whatsapp": _summarize_whatsapp(parser.whatsapp_signals),
        "issues": [],
        "strengths": [],
    }

    # Auto-detect issues
    if not h1:
        findings["issues"].append("🔴 No H1 tag found — critical for SEO and content hierarchy")
    elif len(h1) > 1:
        findings["issues"].append(f"🟡 Multiple H1 tags ({len(h1)}) — use only one")

    if len(title) < 30:
        findings["issues"].append("🟡 Title too short — add value proposition or keywords")
    elif len(title) > 65:
        findings["issues"].append("🟡 Title too long — truncated in search results")

    if not parser.meta_description:
        findings["issues"].append("🟡 Missing meta description")
    elif len(parser.meta_description) < 120:
        findings["issues"].append("🟡 Meta description too short — add benefits/CTA")

    if cta_count == 0:
        findings["issues"].append("🔴 No CTAs detected — critical conversion element missing")
    elif cta_count > 8 and page_type in ["pdp", "home"]:
        findings["issues"].append("🟡 Too many CTAs — creates decision paralysis")

    if not parser._breadcrumbs and page_type in ["pdp", "plp"]:
        findings["issues"].append("🟡 No breadcrumbs detected — hurts navigation and SEO")

    if findings["forms"]["high_friction"]:
        findings["issues"].append("🔴 Checkout form has >5 fields — high abandonment risk")

    if not social_proof:
        findings["issues"].append("🟡 No social proof signals detected")

    if len(product_images) == 0 and page_type == "pdp":
        findings["issues"].append("🔴 No product images detected")

    if not urgency_signals and page_type in ["pdp", "cart"]:
        findings["issues"].append("🟢 No urgency signals — consider adding stock/time triggers")

    wa = findings["whatsapp"]
    if wa["detected"] and wa["floating"]:
        pass  # handled in strengths below
    elif wa["detected"] and not wa["floating"]:
        findings["issues"].append("🟡 WhatsApp link detected but not as a floating button — a fixed-position widget converts better on mobile")
    else:
        # Only flag missing WA on home/pdp/cart — checkout noise is irrelevant
        if page_type in ["home", "pdp", "cart"]:
            findings["issues"].append("🟡 No WhatsApp button detected — floating WA chat increases mobile conversions 8–15% for LATAM stores")

    # Strengths
    if h1 and len(h1) == 1:
        findings["strengths"].append("✅ Single clear H1 tag")
    if social_proof:
        findings["strengths"].append("✅ Social proof signals present")
    if urgency_signals:
        findings["strengths"].append("✅ Urgency signals active")
    if parser.trust_signals:
        findings["strengths"].append(f"✅ Trust signals found ({len(set(parser.trust_signals))})")
    if parser._breadcrumbs:
        findings["strengths"].append("✅ Breadcrumb navigation present")
    if wa["detected"] and wa["floating"]:
        findings["strengths"].append("✅ Floating WhatsApp button detected — direct conversion channel active")

    return findings


def print_analysis(findings):
    """Print human-readable analysis."""
    if "error" in findings:
        print(f"❌ Error: {findings['error']}")
        return

    print(f"\n{'═' * 60}")
    print(f"📄 {findings['page_type'].upper()} — {findings['url'][:50]}")
    print(f"{'─' * 60}")

    print(f"\n📝 META")
    print(f"  Title ({findings['meta']['title_length']} chars): {findings['meta']['title'][:60]}")
    print(f"  Description ({findings['meta']['meta_desc_length']} chars): {findings['meta']['meta_description'][:80]}...")

    print(f"\n📐 STRUCTURE")
    print(f"  H1: {findings['structure']['h1_count']} found — {findings['structure']['h1_texts']}")
    print(f"  H2s: {findings['structure']['h2_count']} found")
    print(f"  Breadcrumbs: {'Yes' if findings['structure']['has_breadcrumbs'] else 'No'}")

    print(f"\n🖱️  CTAs: {findings['ctas']['total_count']} detected ({findings['ctas']['cta_density']} density)")

    if findings["pricing"]["prices_found"]:
        print(f"\n💰 PRICES: {findings['pricing']['prices_found'][:3]}")

    if findings["social_proof"]["signals_found"]:
        print(f"\n⭐ SOCIAL PROOF: {findings['social_proof']['signals_found'][:2]}")

    if findings["social_proof"]["urgency_signals"]:
        print(f"\n⏰ URGENCY: {findings['social_proof']['urgency_signals'][:2]}")

    if findings["trust"]["trust_signals"]:
        print(f"\n🔒 TRUST: {findings['trust']['trust_signals'][:3]}")

    wa = findings["whatsapp"]
    if wa["detected"]:
        icon = "✅" if wa["floating"] else "🟡"
        print(f"\n💬 WHATSAPP: {icon} {wa['note']}")
        for s in wa["signals"][:3]:
            print(f"   → [{s['tag']}] {s['reason']}")
    else:
        print(f"\n💬 WHATSAPP: ❌ No WhatsApp button detected")

    if findings["issues"]:
        print(f"\n❗ ISSUES FOUND:")
        for issue in findings["issues"]:
            print(f"  {issue}")

    if findings["strengths"]:
        print(f"\n✅ STRENGTHS:")
        for s in findings["strengths"]:
            print(f"  {s}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python html_analyzer.py <url> [page_type]")
        print("page_type: home | plp | pdp | cart | checkout")
        sys.exit(1)

    url = sys.argv[1]
    page_type = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    findings = analyze_page(url, page_type)
    print_analysis(findings)

    # Save JSON
    output_file = f"cro_analysis_{page_type}.json"
    with open(output_file, "w") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Analysis saved to {output_file}")


if __name__ == "__main__":
    main()
