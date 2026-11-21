# Changelog

All notable changes to the Gemini UI/UX Kit (SlopGuard) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
