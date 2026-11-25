# SlopGuard (Gemini UI/UX Kit) 🎨

[![CI](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-v1.6.1-blue.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Audit Score: 100/100](https://img.shields.io/badge/audit%20score-100%2F100-success.svg)](AUDIT_REPORT.md)

An enterprise-grade, design-system-first UI/UX engineering toolkit for AI agents and modern web developers.

The kit enforces **mobile ergonomics**, **WCAG 2.2 AA accessibility**, **physics-grounded micro-interactions**, **anti-slop visual rehabilitation**, **text density reduction**, and **compositor performance standards** across React, Next.js, and Tailwind CSS.

---

## 📚 Core Playbooks & Production Specifications

* **[WORKFLOW.md](WORKFLOW.md):** The hardened 7-phase operational engineering workflow & operating model (v1.6.1). Includes the 12 timeless design approaches, three-tier token architecture, single-source-of-truth rule catalog, and waiver governance.
* **[TEST_CASES.md](TEST_CASES.md):** Production test suite & verification matrix (6 functional suites, 14-state interactive matrix, and manual Screen Reader smoke test scripts).
* **[AUDIT_REPORT.md](AUDIT_REPORT.md):** Automated static component audit (`100/100`, `Exit 0`) and UI/UX Pro Max dataset/prompt audit (`93.3/100`, `0` critical errors).

---

## 🏗️ Architecture

```text
gemini-uiux-kit/
├── bin/
│   ├── slopguard                 # Primary CLI binary (init, audit, doctor, component, upgrade, version)
│   └── gemini-uiux               # Backward-compatible CLI alias
├── rules/
│   ├── visual-identity.md        # Anti-slop aesthetics, clean surfaces, color hierarchy
│   ├── design-philosophies.md    # The 12 Timeless UI Design Approaches & Golden Hybrid
│   ├── cognitive-ux-laws.md      # Gestalt, Hick's, Fitts's, Miller's & Cognitive Load Theory
│   ├── enterprise-design-systems.md # GOV.UK, IBM Carbon, GitHub Primer, M3 & Fluent
│   ├── accessibility-wcag.md     # 4.5:1 contrast, keyboard focus traps, explicit ARIA
│   ├── mobile-ergonomics.md      # 44px+ tap targets, dynamic dvh, thumb zone CTAs
│   └── motion-physics.md         # 60fps compositor rules, pipeline costs & Bézier curves
├── skills/
│   ├── ux-patterns-guide/        # Developer-focused UX patterns (forms, tables, command palette)
│   ├── timeless-patterns/        # Selection & execution playbook for the 12 design approaches
│   ├── anti-slop-design/         # 7-axis quality gating system & token archetypes by wwewtech
│   ├── anti-ui-slop/             # UIZZE design system extension and state coverage
│   ├── ui-ux-pro-max/            # Design intelligence database (50+ styles, 96 palettes, 57 font pairings)
│   ├── unslop/                   # Full anti-slop system (9 passes, signs, tokens, visuals, effects)
│   │   ├── SKILL.md              # 9-pass redline workflow by Damir Sokolovsky
│   │   ├── references/           # signs.md, tokens.md, visuals.md, effects.md, rtl.md
│   │   └── scripts/              # snapshot.mjs, story.mjs, story-path.mjs
│   ├── unslop-engine/            # Executive summary & quick rehabilitation playbook
│   ├── unslop-commit/            # Strips AI marketing tropes from Conventional Commits
│   ├── unslop-review/            # Direct human code review feedback without fluff
│   ├── text-density-reduction/   # Prose-to-UI conversions, copy budgets & scannability
│   ├── design-tokens/            # Semantic CSS variables & Tailwind scales
│   ├── responsive-layouts/       # Bottom sheet drawers vs. desktop dialogs
│   ├── micro-interactions/       # Button tap physics, mutation locks, hardware spotlights
│   └── a11y-auditing/            # Systematic accessibility validation
├── components/                   # Production-grade accessible UI patterns
│   ├── patterns/                 # The 8 Global Layout Primitives
│   │   ├── PatternSplitHero.tsx  # Hero + interactive proof card + trust stats
│   │   ├── PatternBentoGrid.tsx  # Asymmetric bento grid feature showcases
│   │   ├── PatternComparison.tsx # Before vs. After / Old Way vs. New Way matrix
│   │   ├── PatternSpecAccordion.tsx # Progressive disclosure deep technical specs
│   │   ├── PatternStepper.tsx    # Step-by-step roadmap / delivery pipeline
│   │   ├── PatternSocialProof.tsx # Metrics, badges & client logo cloud
│   │   ├── PatternTieredPricing.tsx # Tiered pricing comparison with CTAs
│   │   ├── PatternCtaBand.tsx    # High-impact bottom conversion band
│   │   └── types.ts & index.ts
│   ├── feedback/                 # ActionButton, SkeletonLoader, SpotlightCard
│   ├── navigation/               # ResponsiveHeader, BottomTabBar
│   └── overlays/                 # BottomSheet drawer, ModalDialog
├── scripts/
│   ├── audit-ui.sh               # Scans for sub-44px targets, blur lag, arbitrary hexes
│   └── doctor.sh                 # Diagnostics for UI tooling & environment
└── templates/
    ├── DESIGN_SYSTEM.md          # Design token specification template
    └── UI_AUDIT.md               # Audit report template
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/fahadrahman444/uiux-kit.git ~/.gemini/uiux-kit
bash ~/.gemini/uiux-kit/install.sh
```

### 2. CLI Commands
```bash
# Initialize design system & rules in your project
slopguard init

# Run deterministic accessibility, token, and performance audit
slopguard audit . --ci

# Check frontend environment health
slopguard doctor

# List available component blueprints
slopguard component list

# Inject an accessible component blueprint into your project
slopguard component add PatternBentoGrid
slopguard component add SpotlightCard

# Print version information
slopguard version
```
*(Legacy alias `gemini-uiux` is fully supported)*.

---

## 🎯 Core Principles

1. **Anti-Slop Design:** Replaces generic purple gradients and heavy frosted glass with grounded surfaces, crisp borders, and purposeful accent palettes.
2. **Text Density Reduction:** Replaces dense paragraphs with scannable UI primitives (chips, stat blocks, bento cards, steppers, and spec accordions).
3. **Hardware-Accelerated Interactions:** Uses CSS custom properties for cursor spotlight effects to avoid re-rendering React trees on mouse movements.
4. **Thumb-First Ergonomics:** 44×44px minimum touch footprints, sticky bottom CTAs on mobile, and dynamic viewports (`100dvh`).
5. **WCAG 2.2 AA Accessibility:** Focus rings with Windows Forced Colors fallbacks, required `aria-label`s on icon-only buttons, and minimum 4.5:1 contrast ratios.
6. **State Safety:** Interactive mutation buttons feature built-in loading locks to eliminate double-click race conditions.

---

## 📄 License
Distributed under the MIT License. Text methodologies carry attribution to original authors under CC BY 4.0 (see `NOTICE`).
