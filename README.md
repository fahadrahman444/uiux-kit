# SlopGuard (Gemini UI/UX Kit)

[![CI](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml)
[![Deploy Studio](https://github.com/fahadrahman444/uiux-kit/actions/workflows/pages.yml/badge.svg)](https://github.com/fahadrahman444/uiux-kit/actions/workflows/pages.yml)
[![Version](https://img.shields.io/badge/version-v1.6.1-blue.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Audit Score: 100/100](https://img.shields.io/badge/audit%20score-100%2F100-success.svg)](AUDIT_REPORT.md)

**Live Studio Workbench:** **https://fahadrahman444.github.io/uiux-kit/**

An enterprise-grade, design-system-first UI/UX engineering kit, accessible React/TypeScript pattern library, static AST auditor, and zero-backend **Client Discovery & Multi-Page Blueprint Studio**.

The kit enforces **WCAG 2.2 AA accessibility**, **mobile ergonomics (`>= 44px` touch targets & `320px` reflow)**, **compositor-safe motion & View Transitions**, **semantic design tokens**, and **anti-slop quality gates**.

---

## Core Playbooks & Documentation

* **[docs/README.md](docs/README.md):** Guide for the zero-backend Static Discovery Studio (GitHub Pages deployment, offline `file://` usage, 5-step dual-layer intake, View Transitions, and `.json` session format).
* **[WORKFLOW.md](WORKFLOW.md):** Hardened operational UI/UX engineering workflow (`v1.6.1`), 3-tier token architecture, single-source-of-truth rules, and waiver governance.
* **[AUDIT_REPORT.md](AUDIT_REPORT.md):** Latest verified audit metrics across all **7 verification suites** (`100/100` static AST audit across 30 files, `100.0/100` dataset audit, `100.00/100` golden-set eval, and Playwright + Axe checks).
* **[TEST_CASES.md](TEST_CASES.md):** Functional, accessibility (`WCAG 2.2 AA`), mobile reflow, View Transitions, and static studio test matrix.
* **[databases/README.md](databases/README.md):** Standalone reusable reference design databases including [polygon-uiux-db](databases/polygon-uiux-db/README.md) (`Dark Kinetic Emerald` SQLite DB, ANSI SQL, design tokens, CSS primitives, button catalog, motion choreography, and 14 page templates with zero company data).
* **[MULTIPAGE_IMPLEMENTATION_PLAN.md](MULTIPAGE_IMPLEMENTATION_PLAN.md):** Completed multi-page intelligence catalog (`13` native page routes, `43` sections, `188` archetypes, normalized foreign keys, enterprise components).
* **[CHANGELOG.md](CHANGELOG.md):** Detailed release and unreleased development history.

---

## Key Capabilities

### 1. Zero-Backend Client Discovery & Multi-Page Studio (`docs/`)
Runs cleanly in any browser via GitHub Pages or directly over local `file://` with zero server runtime:
* **5-Step Progressive Dual-Layer Discovery:** Walks through **Business & Buyers**, **Brand & A11y**, **Content & Proof**, **Sitemap & Flows**, and **Tech & Launch** using plain-language client prompts plus an optional **Layer 2 Studio Overrides** drawer.
* **Warm Drafting Paper & Graphite Dark Palette:** Intentional editorial surfaces with single Cobalt ink accents, instant theme switching, and strict `<meta>` CSP (`style-src 'self'`).
* **Sticky Live Specification Inspector:** Updates derived WCAG AA/AAA color spectrum, font pairings, contrast pass ratios, active sitemap counts, and open research gaps in real time while interviewing a client.
* **Multi-Page Sitemap Compiler:** Select one page (`pricing`, `about`, `careers`, etc.) or an entire multi-page website project (`Home + About + Services + Pricing + Case Studies`) and compile **Section Blueprints**, a consolidated **Client & UX Strategy Brief**, **Design System & Reasoning**, **Stack Guidelines**, a full **Markdown Master Brief**, and **JSON / CLI equivalents**.
* **Progressive View Transitions API:** Smooth `forward`/`backward` directional slides on step transitions (`#wizard-stage`), subtle output panel fades (`#output-panels`), and full `@media (prefers-reduced-motion: reduce)` fallbacks.
* **Portable Drafts:** Auto-saves progress to `localStorage` and supports **Save `.json` / Load `.json`** session portability.

### 2. Design Intelligence Engine (`skills/ui-ux-pro-max/` & `databases/`)
* **13 Page Templates:** `home`, `pricing`, `about`, `services`, `case_studies`, `contact`, `blog`, `careers`, `legal`, `product_showcase`, `product_detail`, `service_detail`, `case_study_detail`.
* **43 Sections & 188 Reachable Archetypes** (`100%` reachability verified via `system_audit.py`).
* **98 WCAG AA/AAA Palettes (588 Hex Tokens)** with zero deprecated `Neumorphism` recommendations (`98` normalized products, `102` reasoning rules, `106` UX guidelines).
* **58 Typography Pairings** and **11 Framework Stack Guides** (`nextjs`, `react`, `shadcn`, `html-tailwind`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`).
* **Standalone Kinetic Emerald Database (`databases/polygon-uiux-db/`):** Relational SQLite (`polygon_uiux.db`), SQL dump, tokens/CSS primitives, `6` button patterns, `21` GSAP/ScrollTrigger motion specs, `14` page templates, and `8` accessibility/performance remediations.

### 3. Production Component Library & Static AST Auditor (`components/` & `scripts/`)
* **23 Accessible React/TypeScript Components:** Includes `PatternSplitHero`, `PatternBentoGrid`, `PatternComparison`, `PatternSpecAccordion`, `PatternStepper`, `PatternSocialProof`, `PatternTieredPricing`, `PatternCtaBand`, `PatternDataTable`, `PatternFormEngine`, `PatternAppShell`, `PatternChartRow`, overlays, navigation, and feedback primitives wired to [styles/tokens.css](styles/tokens.css).
* **TypeScript AST + Multi-File CSS Auditor:** [scripts/audit_engine.py](scripts/audit_engine.py) and [scripts/ast_analyzer.mjs](scripts/ast_analyzer.mjs) enforce 19 static and heuristic rules across `.tsx`, `.css`, and static HTML sites.

---

## Architecture

```text
gemini-uiux-kit/
├── .github/workflows/
│   ├── ci.yml                     # CI matrix (ShellCheck, TS typecheck, AST audit, Python unit, Playwright/Axe)
│   └── pages.yml                  # Auto-builds studio data bundle and deploys docs/ to GitHub Pages
├── apps/demo/                     # Runnable Vite + React + Tailwind host app verified by Playwright E2E
├── bin/
│   ├── slopguard                  # Primary CLI binary (init, audit, doctor, component, upgrade, version)
│   └── gemini-uiux                # Backward-compatible CLI alias
├── components/                    # 23 accessible React components (patterns/, feedback/, navigation/, overlays/)
├── databases/                     # Standalone reference UI/UX databases (zero company data)
│   └── polygon-uiux-db/           # Dark Kinetic Emerald SQLite DB, SQL dump, tokens, buttons, motion & 14 templates
├── docs/                          # Zero-backend Static Discovery Studio deployed to GitHub Pages
│   ├── README.md                  # Studio documentation
│   ├── index.html                 # 5-step discovery workbench + sticky live inspector + 6-tab output
│   ├── tokens.css                 # Warm Drafting Paper Light & Graphite Dark design tokens
│   ├── styles.css                 # Layout, accessible focus/target states, and View Transitions
│   ├── app.js                     # Client-side BM25 engine, multi-page compiler, View Transitions, JSON I/O
│   └── data/                      # kit-bundle.json (HTTP fetch) & kit-bundle.js (file:// offline fallback)
├── rules/                         # 7 immutable rule sets (visuals, philosophies, UX laws, enterprise, a11y, mobile, motion)
├── scripts/
│   ├── audit_engine.py            # 19-rule TypeScript AST + multi-file CSS static auditor
│   ├── ast_analyzer.mjs           # Node TypeScript compiler AST wrapper & prop analyzer
│   ├── build_studio_bundle.py     # Builds docs/data/kit-bundle.{json,js} from canonical CSV/JSON datasets
│   ├── audit-ui.sh & doctor.sh    # Shell diagnostics and targeted scans
├── skills/                        # 14 autonomous design/engineering skills & UI/UX Pro Max datasets (+ scripts/migrations/)
├── styles/tokens.css              # Kit-wide Tier 2 semantic design tokens
├── templates/                     # DESIGN_SYSTEM.md & UI_AUDIT.md starter templates
└── tests/
    ├── test_kit.py                # Python adversarial AST, waiver, and page generator tests
    ├── e2e.spec.mjs               # Playwright + Axe Light/Dark E2E checks on apps/demo
    └── studio.spec.mjs            # Playwright + Axe HTTP, file://, View Transitions, and 320px checks on docs/
```

---

## Quick Start

### Use the Static Discovery Studio (Zero Install)
* **Online:** Open **https://fahadrahman444.github.io/uiux-kit/**
* **Offline:** Clone the repo and open [docs/index.html](docs/index.html) directly in any Chromium, Firefox, or Safari browser (loaded via `docs/data/kit-bundle.js` over `file://`).

### Local Verification & Development
```bash
# Install Node dependencies (Playwright, Axe-Core, TypeScript, Vite)
npm ci

# Rebuild static studio bundle after editing CSV/JSON data
python scripts/build_studio_bundle.py

# Run complete 7-suite verification (Typecheck, System Audit, AST Static Audit, Golden Eval, Unit, E2E, Studio)
npm test
```

### Kit CLI Installation
```bash
git clone https://github.com/fahadrahman444/uiux-kit.git ~/.gemini/uiux-kit
bash ~/.gemini/uiux-kit/install.sh

slopguard init
slopguard audit . --ci
slopguard doctor
slopguard component list
slopguard version
```

---

## Core Engineering Principles

1. **Dual-Layer Discovery First:** Gather real buyer friction, research confidence, and verified evidence before selecting layout archetypes or KPI claims (`SLOP-003`).
2. **Drafting-Desk Restraint:** Grounded neutral surfaces, subtle hairlines, single purposeful accent color, sentence case, and zero rainbow gradients (`SLOP-001`, `SLOP-004`, `SLOP-006`).
3. **WCAG 2.2 AA Native:** Verified contrast ratios (`>= 4.5:1` text / `>= 3:1` UI), keyboard navigation, Windows Forced Colors fallback outlines, `24x24px+` / `44x44px` targets, and `320px` reflow (`A11Y-001..008`).
4. **Compositor-Safe Motion & View Transitions:** Directional View Transitions (`forward`/`backward`/`panel`) guarded by `prefers-reduced-motion: reduce` and synchronous fallback focus routing.

---

## License

Distributed under the MIT License ([LICENSE](LICENSE)). Text methodologies carry attribution to original authors under CC BY 4.0 (see [NOTICE](NOTICE)).
