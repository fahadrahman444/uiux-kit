# SlopGuard Studio — Zero-Backend Client Discovery & Multi-Page Compiler

This directory hosts the standalone, browser-only **Client UI/UX Discovery & Blueprint Studio** published via GitHub Pages at **https://fahadrahman444.github.io/uiux-kit/**.

It mirrors 100% of the Python `ui-ux-pro-max` BM25 search engine, WCAG 2.2 AA luminance contrast solver, UI reasoning lookups, and 173 section archetype selectors in pure vanilla HTML, CSS, and JavaScript — with **zero backend server**.

---

## Architecture & Files

| File | Purpose |
| :--- | :--- |
| [index.html](index.html) | Compact utility top bar, Starter Templates bar, 5-step dual-layer discovery wizard, sticky Live Specification Inspector, and 6-tab bottom compiled output |
| [tokens.css](tokens.css) | **Warm Drafting Paper** Light tokens (`#F7F6F3` paper, `#FFFFFF` cards, `#1E40AF` cobalt ink) and **Graphite Pro** Dark tokens (`#141415`, `#19191B`, `#EDEDED` primary actions) |
| [styles.css](styles.css) | Token-bound layout, `:has(input:checked)` active cards, `44px+` touch targets, responsive `320px+` grid, scannable 2-col blueprint specs, and **View Transitions API** animations |
| [app.js](app.js) | Client-side BM25 search, single/multi-page sitemap compiler, `hero_direction` bidirectional sync, View Transitions helper (`runViewTransition`), `localStorage` autosave, and `.json` session import/export |
| [data/kit-bundle.json](data/kit-bundle.json) | Precompiled dataset (`40` sections, `173` archetypes, `9` page templates, `96` color palettes, `57` fonts, `96` products, `100` UI reasoning rules, `11` stack CSVs) loaded via `fetch()` over HTTP |
| [data/kit-bundle.js](data/kit-bundle.js) | `window.__SLOPGUARD_KIT_BUNDLE__` wrapper dynamically loaded over direct `file://` URLs where browsers block local `fetch()` |

---

## Features & Workflow

### 1. Dual-Layer Discovery (5 Progressive Steps)
1. **Step 01 — Business & Buyers:** Brand vs Legal entity, tagline, URL, niche, business model, market tier, buyer pain points, competitor benchmarks, confidence status (`Partial`, `Verified Research`, `Assumptions Only`).
2. **Step 02 — Brand, Visuals & A11y:** Existing vector SVG logo, brand guidelines, photography/video/audio readiness, aesthetic keywords (`--style`), plain-English first-screen visual approach, dark/light modes, WCAG AA/AAA target, and reduced-motion preference.
3. **Step 03 — Content & Proof:** Copywriting ownership, core USP, clichés to avoid, and `SLOP-003` verified evidence source/date range paired with concrete trust toggles.
4. **Step 04 — Sitemap & Flows:**
   * Multi-page **Project Sitemap** selection supporting single-route focusing or compiling up to all **9 Native Blueprint Pages** (`home`, `about`, `services`, `pricing`, `case_studies`, `contact`, `blog`, `careers`, `legal`) plus custom scope-only pages.
   * Quantitative scale thresholds (`link_count`, `logo_count`, `step_count`, `case_count`, `review_count`, `team_size`, `faq_count`) and localization toggles (`multilingual_support`, `rtl_required`).
   * Commercial flows (`pricing_model`, calendar booking, RFQ, matrix, SLA, ROI) plus contextual **Page-Specific UX accordions** that auto-expand and highlight active routes checked in your sitemap.
5. **Step 05 — Tech, Scope & Launch:** Website type, frontend stack (`11` choices), CMS preference, hosting/DNS state, launch window, budget tier, final approver, P0/P2 scope notes, and **Layer 2: Studio Advanced Archetype Overrides** (auto-synced cleanly with Step 2).

### 2. Progressive View Transitions (`runViewTransition`)
* Directional horizontal slides (`forward` / `backward`) inside `#wizard-stage` (`view-transition-name: wizard-stage`) while holding the header, step bar, and live inspector steady.
* Subtle vertical crossfades inside `#output-panels` when switching tabs, plus theme crossfade on Light/Dark toggle.
* Automatically skips animation or disables spatial movement when `@media (prefers-reduced-motion: reduce)` is enabled or in browsers without `document.startViewTransition`, while routing focus safely after DOM updates.

### 3. Security, Privacy & Offline Portability
* **Strict CSP (`index.html` `<meta>`):** `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none';` — zero external CDNs, zero inline styles, zero third-party network tracking.
* **Session Persistence:** Auto-saves form state to browser `localStorage` (`slopguard_studio_draft_v2`) and supports **Save `.json` / Load `.json`** files for sharing discovery briefs asynchronously without a database.

---

## Rebuilding Data & Deploying to GitHub Pages

Whenever CSV or JSON files in `skills/ui-ux-pro-max/data/` change, regenerate the static bundles from the repository root:

```bash
python scripts/build_studio_bundle.py
```

Pushing changes in `docs/`, `skills/ui-ux-pro-max/data/`, or `scripts/build_studio_bundle.py` to `main` automatically runs [`.github/workflows/pages.yml`](../.github/workflows/pages.yml), rebuilds the bundle cleanly, and publishes `docs/` to GitHub Pages.

To test the studio locally (HTTP server mode, `file://` direct open mode, Axe WCAG 2.2 AA Light/Dark scans, View Transitions, multi-page compilation, and `320px` reflow):

```bash
npm run test:studio
```
