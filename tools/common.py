"""Helpers shared by build_site.py and build_legal.py. Nothing here talks to the network."""

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # the repository root = the site root
SITE_URL = "https://rustcraftmc.github.io"
ORG_URL = "https://github.com/RustCraftMC"
REPO_URL = "https://github.com/RustCraftMC/cairn-launcher"
RELEASES_URL = REPO_URL + "/releases"
BENCH_URL = REPO_URL + "/blob/main/docs/BENCHMARK.md"
RUSTCRAFT_URL = "https://rustcraftmc.github.io/rustycraft/"
LASTMOD = "2026-11-06"

DISCLAIMER_EN = "NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT."
DISCLAIMER_ZH = "非 Minecraft 官方产品，未获 Mojang 或 Microsoft 批准，也与其无关联。"


def esc(text):
    return html.escape(text, quote=True)


def href(from_dir, to):
    """Relative link from a page that lives in `from_dir` to the site path `to`.

    Both are site-relative with forward slashes; '' is the site root. A target that ends in '/' (or is '')
    is a directory and keeps a trailing slash, so it resolves to its index.html.
    """
    a = [p for p in from_dir.split("/") if p]
    b = [p for p in to.split("/") if p]
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    rel = "/".join([".."] * (len(a) - i) + b[i:]) or "."
    if to == "" or to.endswith("/"):
        return "./" if rel == "." else rel + "/"
    return rel


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", path.relative_to(ROOT).as_posix())


def head(lang, title, desc, canonical, alternates, icons, og_image, og_size, css, from_dir):
    """The <head> of a page. `canonical` is a site path ('' or 'cairnlauncher/'), `alternates` a list of
    (hreflang, site path), `icons` a dict with svg/png/touch site paths (any may be missing), `css` a list
    of site paths. Paths in the output are relative to the page, except the absolute URLs that crawlers need."""
    h = lambda p: href(from_dir, p)
    locale, other = ("zh_CN", "en_US") if lang == "zh" else ("en_US", "zh_CN")
    out = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        '<meta name="color-scheme" content="dark">',
        '<meta name="theme-color" content="#080a0f">',
        f'<link rel="canonical" href="{SITE_URL}/{canonical}">',
    ]
    for hreflang, path in alternates:
        out.append(f'<link rel="alternate" hreflang="{hreflang}" href="{SITE_URL}/{path}">')
    if icons.get("svg"):
        out.append(f'<link rel="icon" type="image/svg+xml" href="{h(icons["svg"])}">')
    if icons.get("png"):
        out.append(f'<link rel="icon" type="image/png" href="{h(icons["png"])}">')
    if icons.get("touch"):
        out.append(f'<link rel="apple-touch-icon" href="{h(icons["touch"])}">')
    image = f"{SITE_URL}/{og_image}"
    out += [
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{SITE_URL}/{canonical}">',
        f'<meta property="og:locale" content="{locale}">',
        f'<meta property="og:locale:alternate" content="{other}">',
        f'<meta property="og:image" content="{image}">',
        f'<meta property="og:image:width" content="{og_size[0]}">',
        f'<meta property="og:image:height" content="{og_size[1]}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{image}">',
    ]
    out += [f'<link rel="stylesheet" href="{h(p)}">' for p in css]
    # Content is hidden for the scroll reveal only while this class is set. If the script never runs it is removed.
    out.append(
        "<script>document.documentElement.classList.add('js');"
        "setTimeout(function(){window.__ok||document.documentElement.classList.remove('js')},4500)</script>"
    )
    return "\n".join(out)


FOOT = {
    "zh": {
        "nav": "页脚",
        "home": "官网首页",
        "terms": "用户协议",
        "privacy": "隐私政策",
        "repo": "GitHub 仓库",
        "releases": "下载",
        "org": "RustCraftMC Team",
        "disc_local": DISCLAIMER_ZH,
        "trademark": "Minecraft 是 Mojang Studios 和 Microsoft 的商标。Cairn Launcher 是第三方的非官方启动器。",
        "thanks": (
            '特别感谢 <a href="https://github.com/Hex-Dragon/PCL2" rel="noopener">Plain Craft Launcher 2</a> 与 '
            '<a href="https://github.com/HMCL-dev/HMCL" rel="noopener">Hello Minecraft! Launcher</a>。'
        ),
    },
    "en": {
        "nav": "Footer",
        "home": "Home",
        "terms": "Terms of Service",
        "privacy": "Privacy Policy",
        "repo": "GitHub repository",
        "releases": "Download",
        "org": "RustCraftMC Team",
        "disc_local": DISCLAIMER_ZH,
        "trademark": "Minecraft is a trademark of Mojang Studios and Microsoft. Cairn Launcher is an unofficial launcher.",
        "thanks": (
            'Special thanks to <a href="https://github.com/Hex-Dragon/PCL2" rel="noopener">Plain Craft Launcher 2</a> and '
            '<a href="https://github.com/HMCL-dev/HMCL" rel="noopener">Hello Minecraft! Launcher</a>.'
        ),
    },
}


def cairn_paths(lang):
    """Site paths of the Cairn Launcher pages in one language."""
    base = "cairnlauncher/" if lang == "zh" else "cairnlauncher/en/"
    return {"home": base, "terms": base + "terms/", "privacy": base + "privacy/"}


def cairn_footer(lang, from_dir):
    f = FOOT[lang]
    p = cairn_paths(lang)
    h = lambda path: href(from_dir, path)
    return f"""<footer class="foot">
<div class="wrap">
<div class="foot__mark" aria-hidden="true">Cairn</div>
<div class="foot__grid">
<nav class="foot__links" aria-label="{f['nav']}">
<a href="{h(p['home'])}">{f['home']}</a>
<a href="{h(p['terms'])}">{f['terms']}</a>
<a href="{h(p['privacy'])}">{f['privacy']}</a>
<a href="{REPO_URL}" rel="noopener">{f['repo']}</a>
<a href="{RELEASES_URL}" rel="noopener">{f['releases']}</a>
<a href="{h('' if lang == 'zh' else 'en/')}">{f['org']}</a>
</nav>
<div class="foot__legal">
<p class="foot__disc">{DISCLAIMER_EN}</p>
<p>{f['disc_local']}</p>
<p>{f['trademark']}</p>
<p>{f['thanks']}</p>
</div>
</div>
</div>
</footer>"""
