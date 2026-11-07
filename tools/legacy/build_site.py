"""Build the entire RustCraftMC Team organization site and the Cairn Launcher site.

Usage:
    python tools/build_site.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Import common definitions and site content
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    DISCLAIMER_EN,
    DISCLAIMER_ZH,
    LASTMOD,
    ORG_URL,
    RELEASES_URL,
    REPO_URL,
    ROOT,
    RUSTCRAFT_URL,
    SITE_URL,
    cairn_footer,
    cairn_paths,
    esc,
    head,
    href,
    write,
)
from content import CAIRN, ORG  # noqa: E402

SRC = ROOT / "tools" / "src"

SVG_ARROW = (
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<line x1="4" y1="10" x2="16" y2="10"></line><polyline points="10 4 16 10 10 16"></polyline></svg>'
)
SVG_EXTERNAL = (
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<line x1="5" y1="15" x2="15" y2="5"></line><polyline points="7 5 15 5 15 13"></polyline></svg>'
)
SVG_COPY = (
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="7" y="7" width="10" height="10" rx="2"></rect>'
    '<path d="M4 13V5a2 2 0 0 1 2-2h8"></path></svg>'
)


def sync_assets():
    """Distribute source styles and scripts to public asset directories."""
    org_assets = ROOT / "assets"
    cairn_assets = ROOT / "cairnlauncher" / "assets"
    org_assets.mkdir(parents=True, exist_ok=True)
    cairn_assets.mkdir(parents=True, exist_ok=True)

    # Base assets shared by both
    for fn in ("base.css", "base.js"):
        shutil.copy2(SRC / fn, org_assets / fn)
        shutil.copy2(SRC / fn, cairn_assets / fn)

    # Org-specific assets
    shutil.copy2(SRC / "org.css", org_assets / "org.css")

    # Cairn-specific assets
    for fn in ("cairn.css", "cairn.js"):
        shutil.copy2(SRC / fn, cairn_assets / fn)

    print("synced css/js assets to public folders")


# ---------------------------------------------------------------- Cairn Launcher page


def render_cairn(lang):
    c = CAIRN[lang]
    from_dir = "cairnlauncher" if lang == "zh" else "cairnlauncher/en"
    other_lang = "en" if lang == "zh" else "zh"
    h = lambda p: href(from_dir, p)

    alternates = [
        ("zh-CN", "cairnlauncher/"),
        ("en", "cairnlauncher/en/"),
        ("x-default", "cairnlauncher/"),
    ]
    heads = head(
        lang,
        c["title"],
        c["desc"],
        f"{from_dir}/",
        alternates,
        {
            "svg": "cairnlauncher/assets/brand/logo.svg",
            "png": "cairnlauncher/assets/brand/logo.png",
            "touch": "cairnlauncher/assets/apple-touch-icon.png",
        },
        f"cairnlauncher/assets/og-{lang}.png",
        (1200, 630),
        ["cairnlauncher/assets/base.css", "cairnlauncher/assets/cairn.css"],
        from_dir,
    )

    # Stones stack on the left (the cairn)
    stone_specs = [
        (42, 13, 6),
        (38, 12, 6),
        (34, 11, 5),
        (28, 10, 5),
        (23, 9, 4),
        (18, 8, 4),
    ]
    stone_targets = ["hero", "native", "tour", "measured", "privacy", "download"]
    stones_html = []
    for (w, h_dim, br), target, label in zip(stone_specs, stone_targets, c["stones"]):
        stones_html.append(
            f'<li style="--w:{w}px;--h:{h_dim}px;--br:{br}px;">'
            f'<a href="#{target}"><span class="lbl">{esc(label)}</span></a></li>'
        )

    # Not-list lines
    nots_html = "".join(
        f'<span class="not" data-reveal style="--i:{i}">{a}<span class="strike">{b}</span>{d}</span>'
        for i, (a, b, d) in enumerate(c["nots"])
    )

    # Native facts
    facts_html = []
    for i, (title, body, is_key) in enumerate(c["facts"]):
        cls = ' class="is-key"' if is_key else ""
        facts_html.append(
            f"<li{cls} data-reveal style=\"--i:{i}\">"
            f"<strong>{esc(title)}</strong>"
            f"<p>{body}</p></li>"
        )

    # Technology stack
    stack_html = []
    for i, (name, role, width_pct) in enumerate(c["stack"]):
        br = 10 + i * 2
        stack_html.append(
            f'<li data-reveal style="--w:{width_pct}%;--br:{br}px;--i:{i}">'
            f"<code>{esc(name)}</code><span>{esc(role)}</span></li>"
        )

    # Tour steps
    steps_html = []
    shots_base = h("cairnlauncher/assets/shots/")
    for i, (shot_id, step_title, step_desc) in enumerate(c["steps"]):
        img_src = f"{shots_base}{shot_id}-{lang}-dark.webp"
        img_srcset = f"{shots_base}{shot_id}-{lang}-dark-840.webp 840w, {img_src} 1680w"
        steps_html.append(
            f'<div class="tour__step" data-shot="{shot_id}" data-alt="{esc(step_title)}" data-reveal style="--i:{i}">'
            f"<h3>{esc(step_title)}</h3>"
            f"<p>{esc(step_desc)}</p>"
            f'<div class="tour__fig frame">'
            f'<img src="{img_src}" srcset="{img_srcset}" sizes="(max-width: 979px) 100vw, 840px" '
            f'alt="{esc(step_title)}" loading="lazy" width="840" height="525" data-shot="{shot_id}">'
            f"</div>"
            f"</div>"
        )

    # Measured benchmarks
    bench_html = []
    for i, (num, unit, what, more) in enumerate(c["bench"]):
        bench_html.append(
            f'<li class="bench__row" data-reveal style="--i:{i}">'
            f'<p class="num"><span>{esc(num)}<small>{esc(unit)}</small></span></p>'
            f'<div class="bench__meta">'
            f'<p class="bench__what">{esc(what)}</p>'
            f'<p class="bench__more">{more}</p>'
            f"</div></li>"
        )

    # Privacy items
    priv_html = "".join(
        f'<li data-reveal style="--i:{i}">'
        f"<strong>{esc(title)}</strong>"
        f"<p>{body}</p></li>"
        for i, (title, body) in enumerate(c["priv"])
    )

    # Download facts
    dl_facts_html = "".join(f"<li>{item}</li>" for item in c["get_facts"])

    # Code build snippet
    code_lines = "\n".join(f"{cmd:<42} # {comment}" for cmd, comment in c["code"])

    # Nav links
    nav_links_html = "".join(
        f'<a href="#{slug}">{esc(label)}</a>' for slug, label in c["nav"]
    )

    other_path = cairn_paths(other_lang)["home"]

    hero_img = f"{shots_base}home-{lang}-dark.webp"
    hero_img_small = f"{shots_base}home-{lang}-dark-840.webp"

    return f"""<!doctype html>
<html lang="{c['lang_attr']}">
<head>
{heads}
</head>
<body>
<a class="skip" href="#hero">{c['skip']}</a>

<aside class="cairn" aria-label="{c['cairn_label']}">
<ol>
{''.join(reversed(stones_html))}
</ol>
</aside>

<header class="nav">
<div class="nav__in">
<a class="brand" href="{h(cairn_paths(lang)['home'])}" aria-label="Cairn Launcher">
<img src="{h('cairnlauncher/assets/brand/logo.svg')}" width="28" height="28" alt="">
<span>Cairn</span>
</a>
<nav class="nav__links" aria-label="{c['nav_label']}">
{nav_links_html}
<a href="{REPO_URL}" rel="noopener">GitHub</a>
</nav>
<div class="nav__end">
<a class="btn btn--sm btn--gold" href="{RELEASES_URL}" rel="noopener">{c['dl_short']}</a>
<a class="lang" href="{h(other_path)}" hreflang="{c['switch_attr']}" lang="{c['switch_attr']}">{c['switch']}</a>
</div>
</div>
</header>

<main>
<!-- ------------------------------------------------------------- HERO (Side-by-side with half off-screen image) -->
<section id="hero" class="hero" data-chapter="hero">
<div class="wrap hero__grid">
<div class="hero__content">
<h1 class="hero__title">
<span>{c['h1a']}</span>
<span>{c['h1b']}</span>
</h1>
<p class="hero__lede">{c['lede']}</p>
<div class="hero__cta">
<a class="btn btn--gold" href="{RELEASES_URL}" rel="noopener">{c['cta_dl']} {SVG_ARROW}</a>
<a class="btn btn--ghost" href="{REPO_URL}" rel="noopener">{c['cta_src']}</a>
</div>
<p class="hero__note">{c['hero_note']}</p>
</div>
<div class="hero__stage">
<div class="hero__frame frame px" data-parallax="0.04">
<img src="{hero_img}" srcset="{hero_img_small} 840w, {hero_img} 1680w"
     sizes="(max-width: 980px) 100vw, 980px" width="1680" height="1050"
     alt="{esc(c['hero_alt'])}" fetchpriority="high">
</div>
</div>
</div>
</section>

<!-- ------------------------------------------------------------- NATIVE -->
<section id="native" class="chapter chapter--native" data-chapter="native">
<div class="wrap">
<div class="not-list" aria-label="{c['nots'][0][1]}? {c['nots'][1][1]}? {c['nots'][2][1]}?">
{nots_html}
</div>
<p class="lede" data-reveal>{c['native_lede']}</p>
<div class="native__cols">
<ul class="facts">
{''.join(facts_html)}
</ul>
<div class="stack-wrap">
<ul class="stack">
{''.join(stack_html)}
</ul>
<p class="stack-cap">{c['stack_cap']}</p>
</div>
</div>
</div>
</section>

<!-- ------------------------------------------------------------- TOUR -->
<section id="tour" class="chapter chapter--tour" data-chapter="tour">
<div class="wrap">
<div class="tour__head">
<div class="chapter__head" style="margin-bottom:0;">
<h2>{c['tour_h']}</h2>
<p class="sub">{c['tour_sub']}</p>
</div>
<div class="tour__ctl">
<div class="seg" role="group" aria-label="{c['seg_theme']}">
<button type="button" data-set="theme:dark" aria-pressed="true">{c['dark']}</button>
<button type="button" data-set="theme:light" aria-pressed="false">{c['light']}</button>
</div>
<div class="seg" role="group" aria-label="{c['seg_lang']}">
<button type="button" data-set="lang:zh" aria-pressed="{'true' if lang == 'zh' else 'false'}">中文</button>
<button type="button" data-set="lang:en" aria-pressed="{'true' if lang == 'en' else 'false'}">English</button>
</div>
</div>
</div>

<div class="tour" data-shots="{shots_base}">
<div class="tour__grid">
<div class="tour__steps">
{''.join(steps_html)}
</div>
<div class="tour__stage frame px" data-parallax="0.03">
<img src="{hero_img}" srcset="{hero_img_small} 840w, {hero_img} 1680w"
     sizes="(max-width: 1440px) 50vw, 840px" width="840" height="525"
     alt="{esc(c['steps'][0][1])}">
</div>
</div>
</div>
</div>
</section>

<!-- ------------------------------------------------------------- MEASURED -->
<section id="measured" class="chapter chapter--bench" data-chapter="measured">
<div class="wrap">
<div class="chapter__head">
<h2>{c['bench_h']}</h2>
</div>
<ul class="bench__rows">
{''.join(bench_html)}
</ul>
<div class="bench__cond">
<p><strong>{c['bench_how_h']}：</strong>{c['bench_how']}</p>
</div>
</div>
</section>

<!-- ------------------------------------------------------------- PRIVACY -->
<section id="privacy" class="chapter chapter--priv" data-chapter="privacy">
<div class="wrap">
<div class="priv__grid">
<div class="priv__head">
<h2>{c['priv_h']}</h2>
<p class="sub">{c['priv_sub']}</p>
<div class="callout glass">
<h3>{c['callout_h']}</h3>
<p>{c['callout']}</p>
</div>
<div class="priv__links">
<a class="btn btn--ghost" href="{h(cairn_paths(lang)['privacy'])}">{c['read_privacy']}</a>
<a class="btn btn--ghost" href="{h(cairn_paths(lang)['terms'])}">{c['read_terms']}</a>
</div>
</div>
<ul class="priv__rows">
{priv_html}
</ul>
</div>
</div>
</section>

<!-- ------------------------------------------------------------- DOWNLOAD -->
<section id="download" class="chapter chapter--get" data-chapter="download">
<div class="wrap">
<div class="get__grid">
<div class="get__info">
<h2>{c['get_h']}</h2>
<p class="lede">{c['get_lede']}</p>
<div class="get__cta">
<a class="btn btn--gold" href="{RELEASES_URL}" rel="noopener">{c['get_dl']} {SVG_ARROW}</a>
<a class="btn btn--ghost" href="{REPO_URL}" rel="noopener">{c['get_repo']}</a>
</div>
<ul class="get__facts">
{dl_facts_html}
</ul>
</div>
<div class="code glass frame">
<div class="code__top">
<span>{c['code_title']}</span>
<button type="button" class="copy" data-copy="#code-build" data-done="{c['copied']}">
{SVG_COPY}<span>{c['copy']}</span>
</button>
</div>
<pre id="code-build"><code>{esc(code_lines)}</code></pre>
</div>
</div>
</div>
</section>
</main>

{cairn_footer(lang, from_dir)}
<script src="{h('cairnlauncher/assets/base.js')}" defer></script>
<script src="{h('cairnlauncher/assets/cairn.js')}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- Organization page


def org_footer(lang, from_dir):
    o = ORG[lang]
    h = lambda p: href(from_dir, p)
    links_html = "".join(f'<a href="{h(path)}">{esc(label)}</a>' for label, path in o["foot_links"])
    return f"""<footer class="org-foot">
<div class="wrap org-foot__in">
<nav class="org-foot__nav" aria-label="Footer links">
<a href="{h('' if lang == 'zh' else 'en/')}">RustCraftMC</a>
{links_html}
<a href="{ORG_URL}" rel="noopener">{o['foot_gh']}</a>
</nav>
<div class="org-foot__meta">
<p>{DISCLAIMER_EN}</p>
<p>{DISCLAIMER_ZH if lang == 'zh' else DISCLAIMER_EN}</p>
<p>{o['trademark']}</p>
</div>
</div>
</footer>"""


def render_org(lang):
    o = ORG[lang]
    from_dir = "" if lang == "zh" else "en"
    other_lang = "en" if lang == "zh" else "zh"
    other_path = "en/" if lang == "zh" else ""
    h = lambda p: href(from_dir, p)

    alternates = [
        ("zh-CN", ""),
        ("en", "en/"),
        ("x-default", ""),
    ]
    heads = head(
        lang,
        o["title"],
        o["desc"],
        f"{from_dir}/" if from_dir else "",
        alternates,
        {
            "png": "assets/favicon.png",
            "touch": "assets/apple-touch-icon.png",
        },
        "assets/og.png",
        (1200, 630),
        ["assets/base.css", "assets/org.css"],
        from_dir,
    )

    cairn_home = cairn_paths(lang)["home"]
    cairn_hero_shot = h(f"cairnlauncher/assets/shots/home-{lang}-dark-840.webp")

    return f"""<!doctype html>
<html lang="{o['lang_attr']}">
<head>
{heads}
</head>
<body class="org-body">
<a class="skip" href="#main">{o['skip']}</a>

<header class="org-nav">
<div class="nav__in">
<a class="brand" href="{h('')}" aria-label="RustCraftMC Team">
<img src="{h('assets/favicon.png')}" width="24" height="24" alt="">
<span>RustCraftMC // Team</span>
</a>
<nav class="nav__links" aria-label="{o['nav_label']}">
<a href="#projects">{o['nav'][0][1]}</a>
<a href="#github">{o['nav'][1][1]}</a>
<a href="{h(cairn_home)}">Cairn Launcher</a>
</nav>
<div class="nav__end">
<a class="lang" href="{h(other_path)}" hreflang="{o['switch_attr']}" lang="{o['switch_attr']}">{o['switch']}</a>
</div>
</div>
</header>

<main id="main" class="org-main">
<!-- ------------------------------------------------------------- HERO -->
<section class="org-hero">
<div class="wrap org-hero__grid">
<div class="org-hero__content">
<div class="org-meta">
<span class="org-badge">Active Systems Lab</span>
<span>// RUST 2024</span>
</div>
<h1 class="org-title">{o['h1']}</h1>
<p class="org-lede">{o['lede']}</p>
</div>
<div class="org-logo-card">
<img class="org-logo" src="{h('assets/brand/rustcraftmc.png')}" width="160" height="160" alt="RustCraftMC Team Logo">
</div>
</div>
</section>

<!-- ------------------------------------------------------------- PROJECTS (Bento Style) -->
<section id="projects" class="org-section">
<div class="wrap">
<div class="org-section__head">
<h2>{o['projects_h']}</h2>
<span class="org-section__meta">02 Featured</span>
</div>

<!-- Cairn Launcher Bento Card -->
<div class="org-bento">
<div class="org-card org-card--hero">
<div>
<span class="org-card__tag">Native Launcher // Desktop</span>
<h3>Cairn Launcher</h3>
<p>{o['cairn_body']}</p>
<div class="org-chips">
<span class="org-chip">Rust Native</span>
<span class="org-chip">cairn-ui</span>
<span class="org-chip">GPU Glass</span>
<span class="org-chip">Zero JVM Shell</span>
<span class="org-chip">QuickJS Sandbox</span>
</div>
</div>
<div class="org-card__actions">
<a class="btn btn--org" href="{h(cairn_home)}">{o['cairn_site']} {SVG_ARROW}</a>
<a class="btn btn--org-ghost" href="{REPO_URL}" rel="noopener">{o['cairn_repo']}</a>
</div>
</div>
<div class="org-card org-preview-card">
<a href="{h(cairn_home)}" tabindex="-1" aria-hidden="true" style="display:block;width:100%;height:100%;">
<img src="{cairn_hero_shot}" width="840" height="525" alt="{esc(o['cairn_alt'])}" loading="lazy">
</a>
</div>
</div>

<!-- Grid: RustCraft Project & GitHub -->
<div class="org-grid-2">
<a class="org-link-card" href="{RUSTCRAFT_URL}" rel="noopener">
<div class="org-link-card__top">
<span class="org-card__tag">Core Engine Exploration</span>
<span class="org-link-card__arrow">{SVG_EXTERNAL}</span>
</div>
<h3 class="org-link-card__name">RustCraft</h3>
<p>{o['rustcraft_body']}</p>
</a>

<a class="org-link-card" href="{ORG_URL}" rel="noopener">
<div class="org-link-card__top">
<span class="org-card__tag">GitHub Organization</span>
<span class="org-link-card__arrow">{SVG_EXTERNAL}</span>
</div>
<h3 class="org-link-card__name">{o['github_hint']}</h3>
<p>{o['github_sub']}</p>
</a>
</div>
</div>
</section>
</main>

{org_footer(lang, from_dir)}
<script src="{h('assets/base.js')}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- 404 page


def render_404():
    o = ORG["zh"]
    heads = head(
        "zh",
        f"404 · {o['nf_subtitle']} — RustCraftMC Team",
        o["nf_text"],
        "404.html",
        [],
        {"png": "assets/favicon.png", "touch": "assets/apple-touch-icon.png"},
        "assets/og.png",
        (1200, 630),
        ["assets/base.css", "assets/org.css"],
        "",
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{heads}
</head>
<body>
<header class="nav is-always is-stuck">
<div class="nav__in">
<a class="brand" href="./" aria-label="RustCraftMC Team">
<img src="assets/favicon.png" width="28" height="28" alt="">
<span>RustCraftMC</span>
</a>
<div class="nav__end">
<a class="btn btn--sm btn--ghost" href="./">{o['nf_home']}</a>
</div>
</div>
</header>

<main class="nf">
<div class="wrap">
<h1>404</h1>
<h2>{o['nf_subtitle']}</h2>
<p>{o['nf_text']}</p>
<div style="display:flex; gap:12px; margin-top:20px;">
<a class="btn btn--gold" href="./">{o['nf_home']} {SVG_ARROW}</a>
<a class="btn btn--ghost" href="cairnlauncher/">{o['nf_cairn']}</a>
</div>
</div>
</main>

{org_footer('zh', '')}
<script src="assets/base.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- Metadata


def emit_sitemap():
    urls = [
        ("", "1.0"),
        ("en/", "0.9"),
        ("cairnlauncher/", "1.0"),
        ("cairnlauncher/en/", "0.9"),
        ("cairnlauncher/terms/", "0.6"),
        ("cairnlauncher/privacy/", "0.6"),
        ("cairnlauncher/en/terms/", "0.6"),
        ("cairnlauncher/en/privacy/", "0.6"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio in urls:
        lines += [
            "  <url>",
            f"    <loc>{SITE_URL}/{path}</loc>",
            f"    <lastmod>{LASTMOD}</lastmod>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")


def emit_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    write(ROOT / "robots.txt", content)


def emit_nojekyll():
    p = ROOT / ".nojekyll"
    if not p.exists():
        p.write_bytes(b"")
        print("wrote .nojekyll")


# ---------------------------------------------------------------- Main


def main():
    print("Building site...")
    sync_assets()

    # 1. Cairn Launcher pages
    write(ROOT / "cairnlauncher" / "index.html", render_cairn("zh"))
    write(ROOT / "cairnlauncher" / "en" / "index.html", render_cairn("en"))

    # 2. Org pages
    write(ROOT / "index.html", render_org("zh"))
    write(ROOT / "en" / "index.html", render_org("en"))
    write(ROOT / "404.html", render_404())

    # 3. Search and GitHub Pages configs
    emit_sitemap()
    emit_robots()
    emit_nojekyll()

    # 4. Legal documents
    print("Building legal documents...")
    res = subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "build_legal.py")], check=True)
    if res.returncode != 0:
        sys.exit(res.returncode)

    print("Site build complete.")


if __name__ == "__main__":
    main()
