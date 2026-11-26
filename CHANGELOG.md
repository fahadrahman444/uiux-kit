# Changelog

All notable changes to the Gemini UI/UX Kit (SlopGuard) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Dark Kinetic Emerald System & Central Prompt Enrichment (`skills/ui-ux-pro-max/`, `docs/`):**
  - Added reusable `Dark Kinetic Emerald` aesthetic (`styles.csv #59`, `prompts.csv #24`), WCAG AAA palettes (`colors.csv #97–98`), `Kinetic Agency Sans` (`typography.csv #58`, `Poppins` + `Kanit`), `Dark Kinetic Agency Showcase` (`landing.csv #31`), normalized product categories (`products.csv #97–98`), reasoning rules (`ui-reasoning.csv #101–102`), and kinetic scroll/hover/button/cursor UX guardrails (`ux-guidelines.csv #100–106`).
  - Expanded section dataset to **43 sections / 188 archetypes** (`nav-07`, `hero-11`, `tb-07`, `srv-09`, `res-07`, `port-09`, `tst-09`, `cmap-03`, `ftr-07`, plus `product_catalog_grid` `pcg-01..02`, `product_feature_matrix` `pfm-01..02`, and `case_study_dossier` `csd-01..02`) and extended `page-templates.json` to **13 page templates** (`product_showcase`, `product_detail`, `service_detail`, `case_study_detail`).
  - Synced `generate_section_prompt.py` (`--kinetic-dark` & selector branches + kinetic scroll/button choreography output), `docs/app.js`, `docs/index.html`, and rebuilt `docs/data/kit-bundle.{json,js}`.
- **Standalone Reference Database (`databases/polygon-uiux-db/`):**
  - Added normalized, zero-company-data SQLite database (`polygon_uiux.db`), ANSI SQL dump (`polygon_uiux.sql`), deterministic builder (`build_db.py`), W3C-style tokens (`tokens/design-tokens.json`), CSS primitives (`tokens/polygon-theme.tokens.css`), and 11 CSV/JSON exports covering `6` button patterns, `21` GSAP/ScrollTrigger/ScrollSmoother motion rules, `14` components, `14` page templates, and `8` contrast/performance/a11y remediations.
- **Repository Reorganization:**
  - Consolidated `polygon-uiux-db` under `databases/polygon-uiux-db/` and grouped historical one-off seed scripts (`add_*.py` & deprecated `build_section_dataset.py`) under `skills/ui-ux-pro-max/scripts/migrations/`.
- **Zero-Backend Static Discovery Studio (`docs/` & `docs/README.md`):**
  - Standalone HTML/CSS/JS workbench deployed automatically to GitHub Pages (`https://fahadrahman444.github.io/uiux-kit/`) via `.github/workflows/pages.yml` and playable offline over `file://` via `docs/data/kit-bundle.js`.
  - **5-Step Dual-Layer Client Discovery Wizard:** Covers Business & Buyers, Brand Assets & A11y, Content Ownership & `SLOP-003` Proof, Multi-Page Sitemap & Commercial Flows, and Stack/P0-P2 Launch Reality with collapsible Layer 2 Studio Overrides.
  - **Warm Drafting Paper & Graphite Dark Design (`docs/tokens.css` & `docs/styles.css`):** Unslopped studio chrome with compact top bar, single-row mobile stepper, sticky Live Specification Inspector, scannable 2-column section spec grids, and strict `<meta>` CSP (`style-src 'self'`).
  - **Multi-Page Sitemap Compiler & 6 Output Tabs (`docs/app.js`):** Compiles single pages or multi-page website sitemaps across all 9 native routes plus custom scope pages, flags open research gaps, auto-saves drafts to `localStorage`, and supports portable `.json` session export/import + full `.md` export.
  - **Progressive View Transitions API (`runViewTransition`):** Directional `forward`/`backward` transitions for wizard steps, fade-rise transitions for output panels, theme crossfades, and `@media (prefers-reduced-motion: reduce)` guards.
- **Enterprise Patterns, Runner & Evaluators:**
  - Added `PatternDataTable.tsx`, `PatternFormEngine.tsx`, `PatternAppShell.tsx`, `PatternChartRow.tsx` and runnable host showcase in `apps/demo/`.
  - Upgraded `scripts/audit_engine.py` + `scripts/ast_analyzer.mjs` to 19 rules with TypeScript AST + multi-file CSS resolution across `components/`, `apps/demo/src/`, and `docs/`.
  - Added `skills/ui-ux-pro-max/scripts/eval_golden_set.py` (30 briefs, `100.00/100`), `tests/test_kit.py`, `tests/e2e.spec.mjs`, `tests/studio.spec.mjs`, and `scripts/build_studio_bundle.py`.

### Fixed & Remediated
- **Dataset Normalization & Anti-Slop Debt:** Normalized all `98` `products.csv` rows via `product-type-mapping.json` (`0` FK warnings) and eliminated all prohibited `Neumorphism` recommendations (`0` in `ui-reasoning.csv` and `products.csv`).
- **Accessibility & Static Checks:** Fixed `PatternSpecAccordion.tsx` collapsed focusability (`inert`, `aria-hidden`, `visible`/`invisible`), fixed `ActionButton.tsx` `HTMLMotionProps` typing, resolved CI `shellcheck` warnings (`SC2013`/`SC2034`), renamed `.sr-only` to `.studio-vh` inside `docs/`, and fixed `aria-label` on live spectrum bar (`role="img"` + `aria-hidden` stops).

---

## [1.6.1] - 2026-11-22

### Fixed & Remediated
- **Component Accessibility & Tokens:**
  - `ResponsiveHeader.tsx`: Replaced raw border references and added dual-ring focus: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 forced-colors:focus-visible:outline-[Highlight]`.
  - `ActionButton.tsx`: Removed `focus-visible:outline-none`. Added genuine dual-ring CSS `outline` with Windows Forced Colors Mode fallback: `forced-colors:focus-visible:outline-[Highlight]`.
  - `PatternSplitHero.tsx`: Added explicit aspect ratio container reservation (`min-h-[360px] aspect-video sm:aspect-auto`) eliminating CLS during async media hydration; normalized spacing tokens to canonical 4px/8px steps (`gap-3 pt-2`).
  - `PatternBentoGrid.tsx`: Converted default screaming uppercase badge (`CAPABILITIES`) to sentence-case metadata chip: `badge = "Capabilities"`.
- **System Hardening:**
  - Normalized all documentation and test matrices to clean UTF-8.
  - Implemented mathematical precedence guard for `.designrc.json` severity overrides preventing accidental blocker downgrades.
  - Restored `slopguard version` CLI command.
  - Achieved **100/100 Anti-Slop Score**, **0 Blockers**, and **10/10 Definition of Done Gates Passed** (`Exit 0`, Production Ready).

---

## [1.6.0] - 2026-11-22

### Added
- **SlopGuard Engineering Workflow (`WORKFLOW.md`):** Complete 7-stage operational design system engineering playbook.
- **Mathematical Anti-Slop Scoring:** `score = max(0, 100 - (blockers * 100) - (majors * 5) - (minors * 1))`.
- **Standards-Precise Accessibility:** Comprehensive WCAG 2.2 AA coverage matrix (3.2.6 Consistent Help, 1.4.12 Text Spacing, 1.4.13 Hover/Focus, 2.4.11 Focus Not Obscured, 3.3.7 Redundant Entry, 3.3.8 Auth).
- **Single-Source-of-Truth Rule Catalog:** With explicit `Detection` method classification (`static`, `runtime-playwright`, `heuristic`, `manual-review`).
- **Route-Level Performance Budgets:** Delineated Production SLAs vs. Internal Stretch Goals for LCP, INP, CLS, and page weight.
- **Form Security & Privacy:** Triple spam defense (Honeypot + Time-Trap + Edge rate limiting), No-JS semantic fallback, Strict/Compat CSP templates, and Zero-PII telemetry policy.
- **Comprehensive Test Suite (`TEST_CASES.md`):** 6 functional suites, 14-state interactive component matrix, and standardized manual Screen Reader audio smoke test script.
- **Automated Audit Report (`AUDIT_REPORT.md`):** Structured audit report conforming to JSON schema `$schema: https://schema.slopguard.dev/schemas/audit-v1.json`.

---

## [1.3.0] - 2026-11-22

### Added
- **Cognitive UX & Behavioral Laws (`rules/cognitive-ux-laws.md`):** Comprehensive foundation covering Gestalt Principles, Hick-Hyman Law, Fitts's Law, Miller's Law, Jakob's Law, Cognitive Load Theory, Dual-Process Theory, and the Doherty Threshold.
- **Enterprise Design System Standards (`rules/enterprise-design-systems.md`):** Synthesized benchmarks from GOV.UK (accessible forms, "One thing per page", error summaries), IBM Carbon (data tables, density modes, notification hierarchy), GitHub Primer (information density, monospaced metadata), and Material Design 3 / Microsoft Fluent (elevation, acrylic/mica, spatial grid).
- **Motion Pipeline & Physics (`rules/motion-physics.md`):** Added 3-tier browser rendering cost breakdown (Compositor GPU vs. Paint vs. Reflow), calibrated Bézier timing curves, and strict duration perception budgets.
- **Developer UX Pattern Blueprints (`skills/ux-patterns-guide/`):** Implementation playbooks for accessible forms, data tables, command palettes (`Cmd+K`), multi-step wizards, and empty states.

---

## [1.2.0] - 2026-11-22

### Added
- **Curated Design Intelligence & Anti-Slop Skills:**
  - `anti-slop-design`: 7-axis quality gating system and curated token archetypes by wwewtech.
  - `anti-ui-slop`: UIZZE design system extension and complete state coverage.
  - `ui-ux-pro-max`: Multi-stack design intelligence dataset (50+ visual styles, 96 palettes, 57 font pairings, 99 UX rules).
  - `unslop-commit` & `unslop-review`: Strips AI marketing tropes and corporate filler from commits and code reviews.
- **The 12 Timeless UI Design Approaches (`rules/design-philosophies.md` & `skills/timeless-patterns/`):** Full breakdown of Swiss, Minimalist, Editorial, Neo-Brutalist, Neo-Swiss, Luxury, and the Golden 4-Pillar Hybrid.

---

## [1.1.0] - 2026-11-22

### Added
- **The 8 Global Layout Pattern Primitives (`components/patterns/`):** Production-ready, accessible blueprints for `PatternSplitHero`, `PatternBentoGrid`, `PatternComparison`, `PatternSpecAccordion`, `PatternStepper`, `PatternSocialProof`, `PatternTieredPricing`, and `PatternCtaBand`.
- **Text Density Reduction Skill (`skills/text-density-reduction/`):** Copy budgets, scannable units, the 6 prose-to-UI conversions, and the visual blur test.
- **Hardware-Accelerated Micro-Interactions (`components/feedback/SpotlightCard.tsx`):** CSS custom property driven spotlight card eliminating React re-renders on cursor movement.
- **Full Unslop Suite (`skills/unslop/`):** Complete 9-pass design overhaul system by Damir Sokolovsky with all reference documents (`signs.md`, `tokens.md`, `visuals.md`, `effects.md`, `rtl.md`).
- **Enhanced Deterministic Audit Engine (`scripts/audit-ui.sh`):** Added scans for arbitrary hex utilities (`bg-[#...]`), sub-44px buttons, backdrop-blur animation lag, and unaccelerated `onMouseMove` state updates.

---

## [1.0.0] - 2026-11-22

### Added
- Initial release of Gemini UI/UX Kit.
- Deterministic CLI (`bin/gemini-uiux`) with `init`, `audit`, `doctor`, and `component` subcommands.
- Core rules: `visual-identity.md`, `accessibility-wcag.md`, `mobile-ergonomics.md`, `motion-physics.md`.
- Foundational components: `ActionButton`, `SkeletonLoader`, `BottomTabBar`, `ResponsiveHeader`, `BottomSheet`, `ModalDialog`.
