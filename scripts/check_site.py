#!/usr/bin/env python3
"""Static quality checks for the standalone PlayVerse public website."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
ICON = ROOT / "assets" / "playverse-icon.svg"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.fragments = []
        self.errors = []
        self.viewport = False
        self.title = False
        self.nav = False
        self.menu_button = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        value = attrs.get("id")
        if value:
            self.ids.append(value)
        href = attrs.get("href", "")
        if href.startswith("#") and len(href) > 1:
            self.fragments.append(href[1:])
        if tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "title":
            self.title = True
        if tag == "nav" and attrs.get("id") == "mainNav":
            self.nav = True
        if tag == "button" and attrs.get("id") == "menuBtn":
            self.menu_button = True

def fail(message):
    print(f"FAIL: {message}")
    return False

def main():
    if not PAGE.is_file():
        return 1 if fail("index.html is missing") else 0
    if not ICON.is_file():
        return 1 if fail("assets/playverse-icon.svg is missing") else 0

    html = PAGE.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)
    ok = True

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        ok = fail("duplicate HTML id(s): " + ", ".join(duplicates)) and ok

    missing = sorted(set(parser.fragments) - set(parser.ids))
    if missing:
        ok = fail("broken internal anchor(s): " + ", ".join(missing)) and ok

    if not parser.viewport:
        ok = fail("responsive viewport meta tag is missing") and ok
    if "<title>" not in html.lower():
        ok = fail("document title is missing") and ok
    if not parser.nav or not parser.menu_button:
        ok = fail("responsive navigation or mobile menu control is missing") and ok

    css = re.search(r"<style[^>]*>(.*?)</style>", html, re.I | re.S)
    css_text = css.group(1) if css else ""
    for breakpoint in ("max-width:980px", "max-width:760px", "max-width:520px"):
        if breakpoint not in re.sub(r"\s+", "", css_text):
            ok = fail(f"responsive CSS breakpoint {breakpoint} is missing") and ok

    for required_section in ("inicio", "experiencia", "explorar", "en-vivo", "comunidad",
                             "perfiles", "conexiones", "plataformas", "descargas",
                             "instalacion", "ayuda"):
        if f'id="{required_section}"' not in html:
            ok = fail(f"required public section #{required_section} is missing") and ok

    if ok:
        print("PASS: standalone site structure, internal navigation, mobile menu, responsive breakpoints and brand asset are present.")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
