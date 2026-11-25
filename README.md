# oxidepm.com

The public website of [OxidePM](https://github.com/oxidekit/oxidepm), published with GitHub Pages at oxidepm.com.

It is plain static HTML, one stylesheet and a little vanilla JavaScript. There are no trackers, no cookies, no analytics and no third-party requests: the fonts are self-hosted.

## Layout

The generated site is committed at the repository root, so Pages can serve the root of the `main` branch as it is.

| Path | What |
|---|---|
| `index.html`, `adapters/`, `docs/`, `security/`, `404.html` | The pages (generated) |
| `assets/` | `site.css`, `site.js` (generated) and `fonts/` with their licences |
| `install.sh` | The installer served at `/install.sh` |
| `CNAME`, `.nojekyll`, `favicon.svg`, `og-image.png` | Pages files and the social preview image |
| `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt` | Crawler and AI-reader files (generated) |
| `docs/**/<page>.md` | The Markdown of each docs page, next to its HTML (generated) |
| `src/` | Sources: page templates, docs in Markdown (with a title and a description for search in `src/docs/nav.json`), styles, script, adapter list, captured terminal output, `og-image.html` |
| `scripts/build.py` | The generator (Python 3, standard library only) |

## Build and preview

```sh
python3 scripts/build.py          # writes the site into the repository root
python3 -m http.server 8000       # then open http://127.0.0.1:8000/
```

Edit files in `src/`, run the build, and commit the sources together with the generated output. `src/captures/` holds sample terminal output that was recorded from a real build of OxidePM; the pages include it by name.

## Search, sharing and AI readers

`build.py` writes, from the same sources as the pages:

- the title, description, canonical URL, Open Graph and Twitter tags of every page, JSON-LD (SoftwareApplication and WebSite on the home page, BreadcrumbList on the others, TechArticle on docs pages), and `sitemap.xml` with `lastmod` taken from the last git commit of the page's source (today for a source with uncommitted changes);
- `robots.txt`, which allows every crawler, the AI crawlers by name too, and lists the sitemap;
- `llms.txt` (a summary and links to the docs) and `llms-full.txt` (every docs page in Markdown), and one `.md` file next to each docs page, so they cannot drift from the pages.

A new docs page needs a `seo_title` (up to about 60 characters) and a `description` (up to 160) in `src/docs/nav.json`. The build warns about longer ones and stops when they are missing.

`og-image.png` (1200 by 630) is rendered from `src/og-image.html` and committed. After changing that file, render it again:

```sh
chromium --headless --no-sandbox --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=5000 \
  --screenshot=og-image.png file://$PWD/src/og-image.html
```

## Release updates

Set `RELEASE_VERSION` in `scripts/build.py` when the site moves to a new release. The build uses it on the home page, in the install and upgrade docs, in structured data and in the plain-text exports. Check the release archives and the adapter installation instructions before rebuilding.

`src/` and `scripts/` are in the served root because Pages serves the repository root. They contain nothing that is not already public in the repository.

## Publish

In the repository settings choose Pages, source "Deploy from a branch", branch `main`, folder `/ (root)`, and set the custom domain to `oxidepm.com`.

## Fonts

Barlow, Barlow Condensed and JetBrains Mono, Latin subsets as woff2 files from the Fontsource packages, under the SIL Open Font License 1.1. The licence texts are in `assets/fonts/`.
