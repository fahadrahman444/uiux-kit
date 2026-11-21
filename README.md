# Gemini UI/UX Kit 🎨

[![CI](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/fahadrahman444/uiux-kit/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-v1.3.0-blue.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, design-system-first UI/UX engineering toolkit for AI agents and modern web developers.

The kit enforces **mobile ergonomics**, **WCAG 2.1 AA accessibility**, **physics-grounded micro-interactions**, **anti-slop visual rehabilitation**, **text density reduction**, and **compositor performance standards** across React, Next.js, and Tailwind CSS.

---

## 🏗️ Architecture

```text
gemini-uiux-kit/
├── bin/
│   └── gemini-uiux               # CLI tool (init, audit, doctor, component)
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

### 1. One-Command Installation
```bash
git clone https://github.com/fahadrahman444/uiux-kit.git ~/.gemini/uiux-kit
bash ~/.gemini/uiux-kit/install.sh
```

### 2. Local Installation
```bash
bash install.sh
```

### 3. CLI Commands
```bash
# Initialize design system & rules in your project
gemini-uiux init

# Run deterministic accessibility, token, and performance audit
gemini-uiux audit

# Check frontend environment health
gemini-uiux doctor

# List available component blueprints
gemini-uiux component list

# Inject an accessible component blueprint into your project
gemini-uiux component add PatternBentoGrid
gemini-uiux component add SpotlightCard
```

---

## 🎯 Core Principles

1. **Anti-Slop Design:** Replaces generic purple gradients and heavy frosted glass with grounded surfaces, crisp borders, and purposeful accent palettes.
2. **Text Density Reduction:** Replaces dense paragraphs with scannable UI primitives (chips, stat blocks, bento cards, steppers, and spec accordions).
3. **Hardware-Accelerated Interactions:** Uses CSS custom properties for cursor spotlight effects to avoid re-rendering React trees on mouse movements.
4. **Thumb-First Ergonomics:** 44×44px minimum touch footprints, sticky bottom CTAs on mobile, and dynamic viewports (`100dvh`).
5. **WCAG 2.1 AA Accessibility:** Focus rings on all keyboard inputs, required `aria-label`s on icon-only buttons, and minimum 4.5:1 contrast ratios.
6. **State Safety:** Interactive mutation buttons feature built-in loading locks to eliminate double-click race conditions.

---

## 📄 License
Distributed under the MIT License.
