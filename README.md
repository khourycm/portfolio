# khourycm.github.io/portfolio

Personal site for Christopher Khoury — strategy, healthcare AI, and innovation.

Live: https://khourycm.github.io/portfolio/

## What's here

    index.html                          the entire site: markup, CSS, and JS in one file
    static/images/headshot.jpg          portrait (800x800)
    static/images/hero-background.webp  hero backdrop (50 KB WebP)
    static/images/og-card.jpg           1200x630 social preview card
    static/images/video-ai4.webp        thumbnail still for the Ai4 2020 talk
    static/favicon.svg, favicon-32.png  monogram favicon
    static/apple-touch-icon.png         iOS home-screen icon
    tools/build_assets.py               regenerates the OG card and favicons
    .github/workflows/                  deploys the repo root to GitHub Pages on push

No build step. `index.html` is served as-is; the Pages workflow uploads the
repo root (`actions/upload-pages-artifact`, `path: '.'`), so anything committed
here is public. Do not commit drafts or working notes.

## Editing

All content — hero, experience, expertise, publications, videos, education,
contact — lives in `index.html` as plain HTML. Find the section by its
`<section id="...">` anchor, edit the text, commit, push. The deploy takes
about a minute.

Section backgrounds are pinned by id (`#experience, #publications, #education`
get `--surface`; `#expertise, #videos, #contact` get `--white`). Keep it that
way rather than using `nth-child` parity — parity re-tints the whole page
whenever a section is added, hidden, or commented out.

The hero stat band ($400M / 20+ / 2 / $57M) is currently commented out. Delete
the wrapping comment markers to restore it; the `.stat-row` CSS is still there.

## Rebuilding the social card and favicons

    python3 tools/build_assets.py

Fetches the four OFL fonts from the Google Fonts repo into `tools/fonts/`
(gitignored) and rewrites the OG card, favicon, and touch icon in place.
Edit the constants at the top of the script for palette or copy changes.

## When the site moves to a custom domain

These absolute URLs are hard-coded to the github.io origin. Update every one:

  - `<link rel="canonical">`
  - `og:url`
  - `og:image` and `twitter:image`
  - the `url` and `image` fields in the JSON-LD Person block

Then point the domain's DNS at GitHub Pages (CNAME file at the repo root) and
re-scrape with LinkedIn Post Inspector so the cached preview card is replaced.
