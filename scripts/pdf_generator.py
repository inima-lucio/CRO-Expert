#!/usr/bin/env python3
"""
CRO Expert — PDF Generator
Converts the HTML report to a high-quality PDF using Playwright.
Usage: python pdf_generator.py <report.html> [--output report.pdf]
"""

import sys
from pathlib import Path


def html_to_pdf(html_path, pdf_path=None):
    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"❌ File not found: {html_path}")
        sys.exit(1)

    if pdf_path is None:
        pdf_path = html_path.with_suffix(".pdf")
    pdf_path = Path(pdf_path)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright not installed.")
        print("   Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    print(f"▶ Generating PDF from {html_path.name}...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(f"file://{html_path}", wait_until="networkidle")
        page.wait_for_timeout(2000)  # let SVG/fonts render

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
            prefer_css_page_size=False,
        )
        browser.close()

    size_kb = round(pdf_path.stat().st_size / 1024)
    print(f"✅ PDF saved: {pdf_path} ({size_kb} KB)")
    return str(pdf_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_generator.py <report.html> [--output report.pdf]")
        sys.exit(1)

    html_file = sys.argv[1]
    pdf_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            pdf_file = sys.argv[i + 1]

    html_to_pdf(html_file, pdf_file)


if __name__ == "__main__":
    main()
