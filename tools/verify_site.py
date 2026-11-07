"""Verify all links, assets, and structural integrity across the entire static site."""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTML_FILES = list(ROOT.glob("**/*.html"))
print(f"Checking {len(HTML_FILES)} HTML files...")

errors = []
external_assets = []
checked_links = 0


def check_html_file(file_path: Path):
    global checked_links
    rel_path = file_path.relative_to(ROOT).as_posix()
    content = file_path.read_text(encoding="utf-8")
    page_dir = file_path.parent

    # 1. Check for external scripts, external stylesheets, external fonts
    for tag in re.findall(r"<(?:script|link|img)[^>]+>", content, re.IGNORECASE):
        # Allow rel="canonical", rel="alternate", property="og:image" to have full URLs
        if 'rel="canonical"' in tag or 'rel="alternate"' in tag or 'property="og:' in tag or 'name="twitter:' in tag:
            continue
        src_m = re.search(r'(?:src|href)=["\']([^"\']+)["\']', tag)
        if src_m:
            target = src_m.group(1)
            if target.startswith("http://") or target.startswith("https://"):
                external_assets.append(f"{rel_path}: External asset found: {tag}")

    # 2. Check all local href and src references
    refs = re.findall(r'(?:href|src)=["\']([^"\'#][^"\']*)["\']', content)
    for ref in refs:
        if ref.startswith("http://") or ref.startswith("https://") or ref.startswith("mailto:"):
            continue
        checked_links += 1

        clean_ref = ref.split("?")[0].split("#")[0]
        if not clean_ref:
            continue

        if clean_ref.startswith("/"):
            target = ROOT / clean_ref.lstrip("/")
        else:
            target = (page_dir / clean_ref).resolve()

        if target.is_dir() or clean_ref.endswith("/"):
            target_file = target / "index.html"
        else:
            target_file = target

        if not target_file.exists():
            errors.append(f"{rel_path}: Broken reference '{ref}' -> file not found: {target_file}")

    # 3. Check srcset references
    srcsets = re.findall(r'srcset=["\']([^"\']+)["\']', content)
    for srcset in srcsets:
        parts = [p.strip().split(" ")[0] for p in srcset.split(",")]
        for p in parts:
            if not p:
                continue
            checked_links += 1
            if p.startswith("/"):
                target = ROOT / p.lstrip("/")
            else:
                target = (page_dir / p).resolve()
            if not target.exists():
                errors.append(f"{rel_path}: Broken srcset reference '{p}' -> file not found: {target}")


for hf in HTML_FILES:
    check_html_file(hf)

print(f"Verified {checked_links} local links and asset paths.")

if external_assets:
    print("\n[!] Disallowed external assets detected:")
    for ea in external_assets:
        print("  ", ea)
    sys.exit(1)
else:
    print("[OK] Zero external scripts, fonts, or assets (strictly adheres to privacy policy).")

if errors:
    print("\n[!] Errors found:")
    for err in errors:
        print("  ", err)
    sys.exit(1)
else:
    print("[OK] All internal links and references resolved successfully.")
