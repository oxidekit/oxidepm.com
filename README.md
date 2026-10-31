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

## Before it goes live

The pages describe code that is newer than the latest published release (0.3.2), and the adapters are not published yet. Until a release contains them, the notice in `src/partials/release-note.html` (shown on the home, security and adapters pages), the "Release status" section of `src/docs/getting-started/install.md` and the sentence in the docs index (`scripts/build.py`) say so. Remove them when a release has the code, and link the adapters repository and archives when they exist.

The text was checked against a build of the unpublished core. Re-check the pages that mention the `web` command (docs: commands, adapters list, home page) after the web server moves out of the core.

`src/` and `scripts/` are in the served root because Pages serves the repository root. They contain nothing that is not already public in the repository.

## Publish

In the repository settings choose Pages, source "Deploy from a branch", branch `main`, folder `/ (root)`, and set the custom domain to `oxidepm.com`.

## Fonts

Barlow, Barlow Condensed and JetBrains Mono, Latin subsets as woff2 files from the Fontsource packages, under the SIL Open Font License 1.1. The licence texts are in `assets/fonts/`.
