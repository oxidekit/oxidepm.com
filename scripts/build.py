#!/usr/bin/env python3
"""Build the OxidePM site into the repository root.

Standard library only. Run from anywhere:

    python3 scripts/build.py

Sources live in src/. The output (index.html, adapters/, docs/, security/, 404.html,
assets/site.css, assets/site.js, sitemap.xml, robots.txt) is committed, so GitHub Pages can
serve the repository root as it is.
"""

import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = "https://oxidepm.com"
GENERATED_DIRS = ["docs", "adapters", "security"]

NAV_LINKS = [("docs", "Docs", "/docs/"), ("adapters", "Adapters", "/adapters/"), ("security", "Security", "/security/")]


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(rel, text):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def esc(s):
    return html.escape(s, quote=True)


def fill(template, values):
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{[a-z_]+\}\}", out)
    if left:
        raise SystemExit("unfilled placeholders: %s" % ", ".join(sorted(set(left))))
    return out


def split_front(text):
    """Front matter (key: value lines) up to a line of three dashes, then the body."""
    head, sep, body = text.partition("\n---\n")
    if not sep:
        raise SystemExit("page has no front matter")
    meta = {}
    for line in head.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


# ---------------------------------------------------------------- inline and block markup

def inline(text):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if len(part) > 1 and part.startswith("`") and part.endswith("`"):
            out.append("<code>%s</code>" % esc(part[1:-1]))
            continue
        part = esc(part)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', part)
        out.append(part)
    return "".join(out)


def term_markup(text):
    """Escape terminal text and turn {hi:..} {ox:..} {dim:..} {b:..} into spans."""
    text = esc(text).replace("\u2139", "\u2139\ufe0e")
    return re.sub(r"\{(hi|ox|dim|b):(.*?)\}", lambda m: '<span class="t-%s">%s</span>' % (m.group(1), m.group(2)), text)


STATUS_WORDS = "online|errored|stopped|starting|waiting|backoff|unhealthy|stopping|building"


def colorize(line):
    """Escape one line of captured terminal output and colour its prompt, marks and statuses."""
    t = esc(line).replace("\u2139", "\u2139\ufe0e")
    t = re.sub(r"^\$ ", '<span class="t-hi">$</span> ', t)
    t = re.sub(r"^agent\$ ", '<span class="t-ox">agent$</span> ', t)
    t = re.sub(r"^(\u2713)", r'<span class="t-hi">\1</span>', t)
    t = re.sub(r"^(\u2717)", r'<span class="t-ox">\1</span>', t)
    t = re.sub(r"^(\u2139)", r'<span class="t-dim">\1</span>', t)
    t = re.sub(r"^(Error:)", r'<span class="t-ox">\1</span>', t)
    t = t.replace("[BROAD]", '<span class="t-ox">[BROAD]</span>')
    t = t.replace(" DENIED ", ' <span class="t-ox">DENIED</span> ')
    if "\u2502" in t:
        t = re.sub(r"(?<= )(online)(?= )", r'<span class="t-hi">\1</span>', t)
        t = re.sub(r"(?<= )(errored|unhealthy)(?= )", r'<span class="t-ox">\1</span>', t)
        t = re.sub(r"(?<= )(stopped|starting|waiting|backoff|stopping|building)(?= )", r'<span class="t-dim">\1</span>', t)
    return t


def capture(name):
    path = SRC / "captures" / (name + ".txt")
    if not path.exists():
        raise SystemExit("missing capture: %s" % name)
    return "\n".join(colorize(l) for l in read(path).rstrip("\n").split("\n"))


def resolve_captures(text):
    return re.sub(r"\{\{cap:([a-z0-9-]+)\}\}", lambda m: capture(m.group(1)), text)


def corners():
    return '<i class="corner tl"></i><i class="corner tr"></i><i class="corner bl"></i><i class="corner br"></i>'


def term_figure(lines, bar=None, label=None, wrap=False, extra="", rendered=None):
    body = rendered if rendered is not None else "\n".join(term_markup(l) for l in lines)
    classes = ["term-body"]
    if wrap:
        classes.append("wrap")
    if any(ch in body for ch in "│╭╰├"):
        classes.append("tight")
    bar_html = ""
    if bar:
        left, _, right = bar.partition("|")
        bar_html = '<div class="term-bar"><span>%s</span><span>%s</span></div>' % (esc(left.strip()), esc(right.strip()))
    aria = ' role="img" aria-label="%s"' % esc(label) if label else ""
    return '<figure class="blueprint term"%s>%s%s<pre class="%s"%s>%s</pre></figure>' % (
        aria, corners(), bar_html, " ".join(classes), extra, body)


_fig_counter = [0]


def code_figure(lang, title, lines):
    _fig_counter[0] += 1
    text = "\n".join(lines)
    if title:
        fid = "code-%d" % _fig_counter[0]
        return (
            '<figure class="blueprint codefig">%s<div class="bar"><span>%s</span>'
            '<button type="button" class="btn btn-ghost" data-copy="%s" data-copy-message="Copied to clipboard">'
            '<span data-copy-label>Copy</span></button></div><pre><code id="%s">%s</code></pre></figure>'
            % (corners(), esc(title), fid, fid, esc(text))
        )
    return '<figure class="blueprint codefig">%s<pre><code>%s</code></pre></figure>' % (corners(), esc(text))


def slugify(text):
    s = re.sub(r"<[^>]+>", "", text)
    s = html.unescape(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def markdown(text, toc=None):
    """A small markdown subset: ## ### headings, paragraphs, lists, tables, fenced code, and the
    blocks ::: note and ::: fields."""
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    seen_ids = set()

    def uniq(slug):
        base, k = slug, 2
        while slug in seen_ids:
            slug = "%s-%d" % (base, k)
            k += 1
        seen_ids.add(slug)
        return slug

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        m = re.match(r"^```(\S*)\s*(.*)$", line)
        if m:
            lang, rest = m.group(1), m.group(2)
            body = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            opts = dict(re.findall(r'(\w+)="([^"]*)"', rest))
            if lang == "term":
                rendered = capture(opts["cap"]) if "cap" in opts else None
                out.append(term_figure(body, bar=opts.get("bar"), label=opts.get("label"), wrap=opts.get("wrap") == "yes", rendered=rendered))
            else:
                out.append(code_figure(lang, opts.get("title"), body))
            continue

        if line.startswith("::: "):
            kind = line[4:].strip()
            body = []
            i += 1
            while i < n and lines[i].strip() != ":::":
                body.append(lines[i])
                i += 1
            i += 1
            if kind.startswith("note"):
                label = kind[4:].strip() or "Note"
                out.append('<div class="blueprint note">%s<span class="lbl">%s</span>%s</div>' % (corners(), esc(label), markdown("\n".join(body))))
            elif kind == "fields":
                out.append(fields_block(body))
            else:
                raise SystemExit("unknown block ::: %s" % kind)
            continue

        m = re.match(r"^(##|###) (.+)$", line)
        if m:
            level = len(m.group(1))
            title = inline(m.group(2))
            hid = uniq(slugify(title))
            if level == 2 and toc is not None:
                toc.append((hid, re.sub(r"<[^>]+>", "", title)))
            out.append('<h%d id="%s">%s</h%d>' % (level, hid, title, level))
            i += 1
            continue

        if line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body_rows = rows[0], [r for r in rows[2:]]
            t = ['<div class="table-wrap"><table><thead><tr>']
            t += ["<th>%s</th>" % inline(c) for c in head]
            t.append("</tr></thead><tbody>")
            for r in body_rows:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        if re.match(r"^(- |\d+\. )", line):
            ordered = bool(re.match(r"^\d+\. ", line))
            items = []
            while i < n and re.match(r"^(- |\d+\. |  \S)", lines[i]):
                if re.match(r"^(- |\d+\. )", lines[i]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        if line.startswith("<"):
            block = []
            while i < n and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue

        para = []
        while i < n and lines[i].strip() and not re.match(r"^(##|###|```|::: |\||- |\d+\. |<)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    return "\n".join(out)


def fields_block(body):
    """name | type | default: x, then lines starting with ': ' for the description."""
    items = []
    for line in body:
        if not line.strip():
            continue
        if line.startswith(": "):
            items[-1]["desc"].append(line[2:])
        else:
            items.append({"head": [p.strip() for p in line.split(" | ")], "desc": []})
    out = ['<dl class="fields">']
    for it in items:
        name = it["head"][0]
        extras = it["head"][1:]
        dt = "<code>%s</code>" % esc(name)
        if extras:
            dt += ' <span class="tag tag-neutral">%s</span>' % inline(extras[0])
        if len(extras) > 1:
            dt += ' <span class="dflt">%s</span>' % inline(extras[1])
        paras = "".join("<p>%s</p>" % inline(d) for d in it["desc"])
        out.append("<div><dt>%s</dt><dd>%s</dd></div>" % (dt, paras))
    out.append("</dl>")
    return "".join(out)


# ---------------------------------------------------------------- shared parts

def nav_html(current, cls=""):
    items = []
    for key, label, href in NAV_LINKS:
        cur = ' aria-current="page"' if key == current else ""
        items.append('      <a href="%s"%s>%s</a>' % (href, cur, label))
    return "\n".join(items)


def menu_html(current):
    items = []
    for key, label, href in NAV_LINKS:
        cur = ' aria-current="page"' if key == current else ""
        items.append('    <a href="%s"%s>%s</a>' % (href, cur, label))
    return "\n".join(items)


class Site:
    def __init__(self):
        self.layout = read(SRC / "partials" / "layout.html")
        self.header = read(SRC / "partials" / "header.html")
        self.footer = read(SRC / "partials" / "footer.html")
        self.urls = []

    def page(self, path, title, description, body, nav="", noindex=False, out=None):
        header = fill(self.header, {"nav_links": nav_html(nav), "menu_links": menu_html(nav)})
        canonical = SITE + path
        robots = '<meta name="robots" content="noindex">\n' if noindex else ""
        text = fill(self.layout, {
            "title": esc(title),
            "description": esc(description),
            "canonical": canonical,
            "robots": robots,
            "header": header,
            "footer": self.footer,
            "body": body,
        })
        if out is None:
            out = (path.lstrip("/") + "index.html") if path.endswith("/") else path.lstrip("/")
        write(out, text)
        if not noindex:
            self.urls.append(canonical)


# ---------------------------------------------------------------- adapters data

def adapter_cards(adapters):
    items = []
    for a in adapters:
        later = a["status"] == "later"
        tag = '<span class="tag tag-outline">Coming later</span>' if later else ""
        perms = "".join("<li><span>%s</span></li>" % esc(p) for p in a["perms"])
        search = " ".join([a["name"], a["kind"], a["summary"]] + a["perms"]).lower()
        cmd = ""
        if not later:
            cmd = '<p class="acard-cmd">%s</p>' % esc(a["cmd"])
        items.append(
            '<li class="blueprint acard" data-card data-status="%s" data-text="%s">%s'
            '<div class="acard-top"><span class="acard-kind">%s</span>%s</div>'
            '<h2>%s</h2><p>%s</p>'
            '<div class="acard-perms"><h3>%s</h3><ul>%s</ul></div>%s</li>'
            % (a["status"], esc(search), corners(), esc(a["kind"]), tag, esc(a["name"]), esc(a["summary"]),
               esc(a["head"]), perms, cmd)
        )
    return "\n".join(items)


def chips(adapters, status):
    cls = "tag tag-neutral chip" if status == "available" else "tag tag-outline chip"
    return "\n".join('<li class="%s">%s</li>' % (cls, esc(a["name"])) for a in adapters if a["status"] == status)


# ---------------------------------------------------------------- docs

def load_docs():
    nav = json.loads(read(SRC / "docs" / "nav.json"))
    flat = []
    for g in nav:
        for p in g["pages"]:
            p["group"] = g
            p["path"] = "/docs/%s/%s/" % (g["slug"], p["slug"])
            flat.append(p)
    return nav, flat


def sidebar(nav, current_path, mobile=False):
    groups = []
    for g in nav:
        lis = []
        for p in g["pages"]:
            cur = ' aria-current="page"' if p["path"] == current_path else ""
            lis.append('<li><a href="%s"%s>%s</a></li>' % (p["path"], cur, esc(p["title"])))
        groups.append('<div class="docs-group" data-group="%s"><h2>%s</h2><ul>%s</ul></div>' % (esc(g["title"]), esc(g["title"]), "".join(lis)))
    none = '<p class="docs-empty" data-docs-none hidden>No page matches &ldquo;<span data-docs-query></span>&rdquo;.</p>'
    return "".join(groups) + none


def docs_shell(nav, current_path, label, inner, toc_html):
    side = (
        '<aside class="docs-side" aria-label="Documentation" data-docs-nav>'
        '<label class="sr-only" for="docs-filter">Filter the docs</label>'
        '<input id="docs-filter" class="input" type="search" placeholder="Filter pages" data-docs-filter>'
        + sidebar(nav, current_path) + "</aside>"
    )
    mobile = (
        '<div class="docs-mobile">'
        '<button type="button" class="btn btn-secondary" data-docs-toggle aria-expanded="false" aria-controls="docs-nav">'
        '<span>Docs: %s</span><span data-docs-toggle-label>Menu</span></button>'
        '<nav id="docs-nav" aria-label="Documentation" hidden data-docs-nav>'
        '<label class="sr-only" for="docs-filter-m">Filter the docs</label>'
        '<input id="docs-filter-m" class="input" type="search" placeholder="Filter pages" data-docs-filter>'
        % esc(label) + sidebar(nav, current_path) + "</nav></div>"
    )
    static_mobile = (
        '<noscript><nav class="docs-mobile-static" aria-label="Documentation">' + sidebar(nav, current_path) + "</nav></noscript>"
    )
    return (
        '<div class="docs">%s%s%s<main id="main" class="docs-main">%s</main>%s</div>'
        % (side, mobile, static_mobile, inner, toc_html)
    )


def build_docs(site):
    nav, flat = load_docs()
    for idx, p in enumerate(flat):
        g = p["group"]
        src = SRC / "docs" / g["slug"] / (p["slug"] + ".md")
        if not src.exists():
            raise SystemExit("missing docs source: %s" % src)
        toc = []
        body_html = markdown(read(src), toc)
        crumbs = (
            '<nav class="crumbs" aria-label="Breadcrumb"><ol>'
            '<li><a href="/docs/">Docs</a></li><li aria-hidden="true">/</li>'
            '<li><a href="%s">%s</a></li><li aria-hidden="true">/</li>'
            '<li aria-current="page">%s</li></ol></nav>' % (g["pages"][0]["path"], esc(g["title"]), esc(p["title"]))
        )
        prev_p = flat[idx - 1] if idx > 0 else None
        next_p = flat[idx + 1] if idx + 1 < len(flat) else None
        pager = '<div class="pager">'
        pager += ('<a href="%s" rel="prev"><small>Previous</small><span>%s</span></a>' % (prev_p["path"], esc(prev_p["title"]))) if prev_p else "<span></span>"
        pager += ('<a href="%s" rel="next"><small>Next</small><span>%s</span></a>' % (next_p["path"], esc(next_p["title"]))) if next_p else ""
        pager += "</div>"
        article = (
            '<article class="docs-article">%s<h1>%s</h1><p class="docs-lede">%s</p><div class="prose">%s</div>%s</article>'
            % (crumbs, esc(p["title"]), inline(p["summary"]), body_html, pager)
        )
        toc_html = ""
        if toc:
            toc_html = (
                '<nav class="docs-toc" aria-label="On this page"><h2>On this page</h2><ul>%s</ul></nav>'
                % "".join('<li><a href="#%s">%s</a></li>' % (hid, esc(t)) for hid, t in toc)
            )
        label = "%s / %s" % (g["title"], p["title"])
        body = docs_shell(nav, p["path"], label, article, toc_html)
        site.page(
            p["path"],
            "%s — OxidePM docs" % p["title"],
            re.sub(r"`", "", p["summary"]),
            body,
            nav="docs",
        )

    # the docs landing page
    cards = []
    for g in nav:
        lis = "".join('<li><a href="%s">%s</a></li>' % (p["path"], esc(p["title"])) for p in g["pages"])
        cards.append('<section class="blueprint">%s<h2>%s</h2><ul>%s</ul></section>' % (corners(), esc(g["title"]), lis))
    inner = (
        '<article class="docs-article wide"><h1>Documentation</h1>'
        '<p class="docs-lede">How to install OxidePM, configure apps, use the commands, add adapters and keep AI agents inside limits. '
        'These pages describe the code on the development branch, which is ahead of the latest published release (0.3.2), and say where something is not built yet.</p>'
        '<div class="docs-index">%s</div></article>' % "".join(cards)
    )
    body = docs_shell(nav, "", "Documentation", inner, "")
    site.page("/docs/", "Documentation — OxidePM",
              "Documentation for OxidePM: install, configuration, commands, adapters, AI safety and the adapter protocol.",
              body, nav="docs")


# ---------------------------------------------------------------- main

def main():
    for d in GENERATED_DIRS:
        shutil.rmtree(ROOT / d, ignore_errors=True)

    # styles: put the dark tokens in both places they are needed
    css = read(SRC / "site.css")
    dark = read(SRC / "dark-tokens.css").strip().splitlines()
    dark_block = "\n    ".join(dark)
    css = css.replace("/*DARK:tokens*/", dark_block, 1)
    css = css.replace("/*DARK:tokens*/", "\n  ".join(dark), 1)
    write("assets/site.css", css)
    write("assets/site.js", read(SRC / "site.js"))

    adapters = json.loads(read(SRC / "adapters.json"))
    counts = {
        "all": len(adapters),
        "available": sum(1 for a in adapters if a["status"] == "available"),
        "later": sum(1 for a in adapters if a["status"] == "later"),
    }
    values = {
        "adapter_cards": adapter_cards(adapters),
        "chips_available": chips(adapters, "available"),
        "chips_later": chips(adapters, "later"),
        "count_all": str(counts["all"]),
        "count_available": str(counts["available"]),
        "count_later": str(counts["later"]),
        "count_text": "%d adapters" % counts["all"],
    }

    site = Site()
    for page_file in sorted((SRC / "pages").glob("*.html")):
        meta, body = split_front(read(page_file))
        body = fill(resolve_captures(body), values) if "{{" in body else body
        site.page(
            meta["path"], meta["title"], meta["description"], body,
            nav=meta.get("nav", ""), noindex=meta.get("robots") == "noindex",
            out=meta.get("out"),
        )
    build_docs(site)

    urls = sorted(set(site.urls), key=lambda u: (u != SITE + "/", u))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += ["  <url><loc>%s</loc></url>" % u for u in urls]
    sitemap.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap) + "\n")
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    print("built %d pages" % len(urls))


if __name__ == "__main__":
    sys.exit(main())
