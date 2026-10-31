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
| `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `favicon.svg` | Pages and crawler files |
| `src/` | Sources: page templates, docs in Markdown, styles, script, adapter list, captured terminal output |
| `scripts/build.py` | The generator (Python 3, standard library only) |

## Build and preview

```sh
python3 scripts/build.py          # writes the site into the repository root
python3 -m http.server 8000       # then open http://127.0.0.1:8000/
```

Edit files in `src/`, run the build, and commit the sources together with the generated output. `src/captures/` holds sample terminal output that was recorded from a real build of OxidePM; the pages include it by name.

## Publish

In the repository settings choose Pages, source "Deploy from a branch", branch `main`, folder `/ (root)`, and set the custom domain to `oxidepm.com`.

## Fonts

Barlow, Barlow Condensed and JetBrains Mono, Latin subsets as woff2 files from the Fontsource packages, under the SIL Open Font License 1.1. The licence texts are in `assets/fonts/`.
