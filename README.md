# Gemini UI/UX Kit 🎨

An enterprise-grade, design-system-first UI/UX engineering toolkit for AI agents and modern web developers.

The kit enforces **mobile ergonomics**, **WCAG 2.1 AA accessibility**, **physics-grounded micro-interactions**, **anti-slop visual rehabilitation**, and **compositor performance standards** across React, Next.js, and Tailwind CSS.

---

## 🏗️ Architecture

```text
gemini-uiux-kit/
├── bin/
│   └── gemini-uiux               # CLI tool (init, audit, doctor, component)
├── rules/
│   ├── visual-identity.md        # Anti-slop aesthetics, clean surfaces, color hierarchy
│   ├── accessibility-wcag.md     # 4.5:1 contrast, keyboard focus traps, explicit ARIA
│   ├── mobile-ergonomics.md      # 44px+ tap targets, dynamic dvh, thumb zone CTAs
│   └── motion-physics.md         # 60fps compositor rules, Framer Motion springs
├── skills/
│   ├── unslop-engine/            # Transforming generic AI interfaces into distinct UI
│   ├── design-tokens/            # Semantic CSS variables & Tailwind scales
│   ├── responsive-layouts/       # Bottom sheet drawers vs. desktop dialogs
│   ├── micro-interactions/       # Button tap physics, mutation locks, skeletons
│   └── a11y-auditing/            # Systematic accessibility validation
├── components/                   # Production-grade accessible UI patterns
│   ├── navigation/               # ResponsiveHeader, BottomTabBar
│   ├── overlays/                 # BottomSheet drawer, ModalDialog
│   └── feedback/                 # ActionButton (mutation-locked), SkeletonLoader
├── scripts/
│   ├── audit-ui.sh               # Scans for sub-44px targets, blur lag, missing aria
│   └── doctor.sh                 # Diagnostics for UI tooling & environment
└── templates/
    ├── DESIGN_SYSTEM.md          # Design token specification template
    └── UI_AUDIT.md               # Audit report template
```

---

## 🚀 Quick Start

### 1. Installation
```bash
bash install.sh
```

### 2. CLI Commands
```bash
# Initialize design system & rules in your project
gemini-uiux init

# Run deterministic accessibility and performance audit
gemini-uiux audit

# Check frontend environment health
gemini-uiux doctor

# List available component blueprints
gemini-uiux component list

# Inject an accessible component blueprint into your project
gemini-uiux component add BottomSheet
```

---

## 🎯 Core Principles

1. **Anti-Slop Design:** Replaces generic purple gradients and heavy frosted glass with grounded surfaces, crisp borders, and purposeful accent palettes.
2. **Thumb-First Ergonomics:** 44×44px minimum touch footprints, sticky bottom CTAs on mobile, and dynamic viewports (`100dvh`).
3. **WCAG 2.1 AA Accessibility:** Focus rings on all keyboard inputs, required `aria-label`s on icon-only buttons, and minimum 4.5:1 contrast ratios.
4. **Compositor Performance:** Banned opacity animations on `backdrop-filter: blur` to protect 60fps mobile scroll performance.
5. **State Safety:** Interactive mutation buttons feature built-in loading locks to eliminate double-click race conditions.

---

## 📄 License
Distributed under the MIT License.
