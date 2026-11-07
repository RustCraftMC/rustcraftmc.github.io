"""Build the web version of the Terms of Service and the Privacy Policy.

Usage:
    python tools/build_legal.py [path-to-CairnLauncher-repository]

Reads TERMS.md, TERMS.en.md, PRIVACY.md and PRIVACY.en.md from the launcher repository (default: the folder
named CairnLauncher next to this repository) and writes four static pages:
    cairnlauncher/terms/index.html        cairnlauncher/privacy/index.html
    cairnlauncher/en/terms/index.html     cairnlauncher/en/privacy/index.html
The text is converted word for word. Only the targets of the links between the four files change, so that they
point at these pages. The script re-reads its own output and stops if any visible text of a source file is
missing or altered. Commit the generated pages; run the script again whenever the documents change.
"""

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import REPO_URL, ROOT, cairn_footer, cairn_paths, esc, head, href, write  # noqa: E402

DOCS = [
    # language, kind, source file, site directory of the generated page
    ("zh", "terms", "TERMS.md", "cairnlauncher/terms"),
    ("zh", "privacy", "PRIVACY.md", "cairnlauncher/privacy"),
    ("en", "terms", "TERMS.en.md", "cairnlauncher/en/terms"),
    ("en", "privacy", "PRIVACY.en.md", "cairnlauncher/en/privacy"),
]
LINKMAP = {  # links between the documents, as written in the Markdown, and the pages they become
    "TERMS.md": "cairnlauncher/terms/",
    "TERMS.en.md": "cairnlauncher/en/terms/",
    "PRIVACY.md": "cairnlauncher/privacy/",
    "PRIVACY.en.md": "cairnlauncher/en/privacy/",
}
SPECIAL_IDS = {"重要提示": "important", "要点": "key-points", "Important notice": "important", "Key points": "key-points"}

UI = {
    "zh": dict(lang_attr="zh-CN", skip="跳到正文", toc="目录", home="官网首页", terms="用户协议", privacy="隐私政策",
               switch="English", switch_attr="en", nav="主导航", toc_nav="本文目录", progress="阅读进度"),
    "en": dict(lang_attr="en", skip="Skip to content", toc="Contents", home="Home", terms="Terms", privacy="Privacy",
               switch="中文", switch_attr="zh-CN", nav="Main", toc_nav="Table of contents", progress="Reading progress"),
}


# ---------------------------------------------------------------- Markdown subset -> HTML

def fmt(text, from_dir):
    s = esc(text)

    def link(m):
        label, url = m.group(1), html.unescape(m.group(2))
        if url in LINKMAP:
            return f'<a href="{href(from_dir, LINKMAP[url])}">{label}</a>'
        if url.startswith("https://"):
            return f'<a href="{esc(url)}" rel="noopener noreferrer" target="_blank">{label}</a>'
        raise SystemExit(f"unexpected link target: {url}")

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def inline(text, from_dir):
    out = []
    for part in re.split(r"(`[^`]+`)", text):
        if len(part) > 2 and part.startswith("`") and part.endswith("`"):
            out.append("<code>" + esc(part[1:-1]) + "</code>")
        else:
            out.append(fmt(part, from_dir))
    return "".join(out)


def table(rows, from_dir):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head_row, sep, *body = cells
    assert all(set(c) <= set("-: ") for c in sep), f"bad table separator: {sep}"
    width = len(head_row)
    for r in body:
        assert len(r) == width, f"table row has {len(r)} cells, expected {width}: {r[:2]}"
    th = "".join(f"<th>{inline(c, from_dir)}</th>" for c in head_row)
    tr = "".join("<tr>" + "".join(f"<td>{inline(c, from_dir)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def heading_id(text, n):
    if text in SPECIAL_IDS:
        return SPECIAL_IDS[text]
    m = re.match(r"^(\d+)\.(\d+)\s", text)
    if m:
        return f"s{m.group(1)}-{m.group(2)}"
    m = re.match(r"^(\d+)\.\s", text)
    if m:
        return f"s{m.group(1)}"
    return f"sec-{n}"


def convert(md, from_dir):
    """Returns (title, toc, html). toc is a list of (id, text) for the level-2 headings."""
    lines = md.replace("\r\n", "\n").split("\n")
    out, toc, para = [], [], []
    title, n, i = None, 0, 0

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para), from_dir) + "</p>")
            para = []

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush()
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*\S)\s*$", line)
        if m:
            flush()
            level, text = len(m.group(1)), m.group(2)
            if level == 1:
                title = text
                out.append(f"<h1>{inline(text, from_dir)}</h1>")
            else:
                n += 1
                hid = heading_id(text, n)
                if level == 2:
                    toc.append((hid, text))
                out.append(f'<h{level} id="{hid}"><a href="#{hid}">{inline(text, from_dir)}</a></h{level}>')
            i += 1
            continue
        if line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows, from_dir))
            continue
        ul, ol = re.match(r"^[-*]\s+(.*)$", line), re.match(r"^\d+\.\s+(.*)$", line)
        if ul or ol:
            flush()
            tag, pattern = ("ul", r"^[-*]\s+(.*)$") if ul else ("ol", r"^\d+\.\s+(.*)$")
            items = []
            while i < len(lines) and re.match(pattern, lines[i]):
                items.append(re.match(pattern, lines[i]).group(1))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t, from_dir)}</li>" for t in items) + f"</{tag}>")
            continue
        if line.startswith(">"):
            flush()
            paras, cur = [], []
            while i < len(lines) and lines[i].startswith(">"):
                text = lines[i][1:].strip()
                if text:
                    cur.append(text)
                elif cur:
                    paras.append(" ".join(cur))
                    cur = []
                i += 1
            if cur:
                paras.append(" ".join(cur))
            out.append("<blockquote>" + "".join(f"<p>{inline(t, from_dir)}</p>" for t in paras) + "</blockquote>")
            continue
        para.append(line.strip())
        i += 1
    flush()
    return title, toc, "\n".join(out)


# ---------------------------------------------------------------- word-for-word check

def squash(text):
    return re.sub(r"\s+", " ", text).strip()


def visible_text(fragment):
    text = re.sub(r"</(p|li|h[1-6]|td|th|tr|blockquote|table|ul|ol|div)>", "\n", fragment)
    return squash(html.unescape(re.sub(r"<[^>]+>", "", text)))


def source_pieces(md):
    """The visible text of every Markdown line: what a reader of the rendered page must find."""
    pieces = []
    for line in md.replace("\r\n", "\n").split("\n"):
        if not line.strip():
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            cells = [re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", c).replace("**", "").replace("`", "") for c in cells]
            pieces += cells
            continue
        t = re.sub(r"^#{1,6}\s+", "", line)
        t = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", t)
        t = re.sub(r"^>\s?", "", t)
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
        pieces.append(t.replace("**", "").replace("`", ""))
    return [squash(p) for p in pieces if squash(p)]


def verify(md, body_html, name):
    text = visible_text(body_html)
    missing = [p for p in source_pieces(md) if p not in text]
    if missing:
        raise SystemExit(f"{name}: text changed or missing, first {min(3, len(missing))}: {missing[:3]}")
    if "**" in text or "`" in text:
        raise SystemExit(f"{name}: unconverted Markdown left in the output")
    return len(source_pieces(md))


# ---------------------------------------------------------------- page

def render_page(lang, kind, title, toc, body, from_dir, meta):
    ui = UI[lang]
    other = "en" if lang == "zh" else "zh"
    mine, theirs = cairn_paths(lang), cairn_paths(other)
    h = lambda p: href(from_dir, p)
    page_path = mine[kind]
    desc = (f"{title}。文档版本 {meta['version']}，{meta['date']} 生效。" if lang == "zh"
            else f"{title}. Document version {meta['version']}, effective {meta['date']}.")
    alternates = [("zh-CN", cairn_paths("zh")[kind]), ("en", cairn_paths("en")[kind]), ("x-default", cairn_paths("zh")[kind])]
    heads = head(
        lang, f"{title} · Cairn Launcher", desc, page_path, alternates,
        {"svg": "cairnlauncher/assets/brand/logo.svg", "touch": "cairnlauncher/assets/apple-touch-icon.png"},
        f"cairnlauncher/assets/og-{lang}.png", (1200, 630),
        ["cairnlauncher/assets/base.css", "cairnlauncher/assets/cairn.css"], from_dir,
    )
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    return f"""<!doctype html>
<html lang="{ui['lang_attr']}">
<head>
{heads}
</head>
<body class="doc-page">
<a class="skip" href="#main">{ui['skip']}</a>
<div class="progress" role="progressbar" aria-label="{ui['progress']}"><i></i></div>
<header class="nav is-stuck">
<div class="nav__in">
<a class="brand" href="{h(mine['home'])}" aria-label="Cairn Launcher"><img src="{h('cairnlauncher/assets/brand/logo.svg')}" width="28" height="28" alt=""><span>Cairn</span></a>
<nav class="nav__links" aria-label="{ui['nav']}">
<a href="{h(mine['home'])}">{ui['home']}</a>
<a href="{h(mine['terms'])}"{' aria-current="page"' if kind == 'terms' else ''}>{ui['terms']}</a>
<a href="{h(mine['privacy'])}"{' aria-current="page"' if kind == 'privacy' else ''}>{ui['privacy']}</a>
<a href="{REPO_URL}" rel="noopener">GitHub</a>
</nav>
<div class="nav__end"><a class="lang" href="{h(theirs[kind])}" hreflang="{ui['switch_attr']}" lang="{ui['switch_attr']}">{ui['switch']}</a></div>
</div>
</header>
<main id="main" class="doc">
<div class="wrap doc__grid">
<aside class="doc__toc"><nav aria-label="{ui['toc_nav']}"><p>{ui['toc']}</p><ol>{toc_html}</ol></nav></aside>
<article class="doc__body">
{body}
</article>
</div>
</main>
{cairn_footer(lang, from_dir)}
<script src="{h('cairnlauncher/assets/base.js')}" defer></script>
</body>
</html>
"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "CairnLauncher"
    for lang, kind, name, directory in DOCS:
        path = src / name
        if not path.exists():
            raise SystemExit(f"not found: {path}")
        md = path.read_text(encoding="utf-8")
        title, toc, body = convert(md, directory)
        pieces = verify(md, body, name)
        version = re.search(r"^(?:文档版本：|Document version: )(.+)$", md, re.M)
        date = re.search(r"^(?:生效日期：|Effective date: )(.+)$", md, re.M)
        meta = {"version": version.group(1).strip(), "date": date.group(1).strip()}
        write(ROOT / directory / "index.html", render_page(lang, kind, title, toc, body, directory, meta))
        print(f"  {name}: {pieces} text pieces verified, version {meta['version']}, effective {meta['date']}")


if __name__ == "__main__":
    main()
