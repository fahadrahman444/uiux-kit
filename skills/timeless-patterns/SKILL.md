---
name: timeless-patterns
description: Playbook for selecting, blending, and executing the 12 timeless UI design approaches (Swiss, Minimalist, Editorial, Neo-Brutalist, Neo-Swiss, Luxury, etc.) to produce lasting, premium interfaces.
---

# Timeless UI Patterns & Design Approaches

Use this skill when defining the visual direction of an application, redesigning an interface, or selecting which timeless design philosophy best fits a product's domain.

---

## 1. The 12 Foundational Design Philosophies

Refer to [`rules/design-philosophies.md`](../../rules/design-philosophies.md) for full historical context and taxonomy. When selecting an approach:

| Domain / Product Type | Recommended Primary Approach | Supporting Secondary Approach |
|---|---|---|
| **AI & Developer Tools** | Neo-Swiss / Contemporary Swiss | Minimalist |
| **High-End SaaS / Fintech** | Swiss / International | Luxury / High-End |
| **Publishing / Media / Portfolios** | Editorial / Magazine | Minimalist |
| **Creative Agencies / Web3** | Neo-Brutalism or Experimental | Swiss Grids |
| **Enterprise / Dashboards** | Material Design / Flat 2.0 | Minimalist |
| **Spatial / Ambient Interfaces** | Glassmorphism (Restrained) | Minimalist |

---

## 2. The Golden 4-Pillar Hybrid Playbook

For flagship agency and enterprise products that must feel **timeless, authoritative, and exceptionally premium**, execute the **Swiss + Minimalist + Editorial + Luxury** hybrid.

### Pillar 1: Swiss Grids for Architectural Structure
- Use strict CSS Grid / Flexbox scales (`grid-cols-12` with uniform `gap-4 sm:gap-6 lg:gap-8`).
- Align all text, badges, borders, and CTA actions along deliberate vertical baseline tracks.
- Enforce visible or implied hairline boundaries (`border border-slate-200 dark:border-slate-800`).

### Pillar 2: Minimalist Discipline for Calm Surfaces
- Use solid grounded surfaces (`surface-canvas`, `surface-card`, `surface-elevated`) instead of stacked translucent blurs.
- Maintain wide vertical section spacing (`py-20` to `py-28`).
- Restrict palettes to neutral ramps (Zinc/Slate) + 1 semantic accent color. 90% of surfaces should be calm and monochromatic.

### Pillar 3: Editorial Typography for Personality
- Pair an expressive display typeface (e.g., Swiss Geometric Sans or high-contrast Serif/Sans) with a clean, high-legibility body font (Inter, Geist, SF Pro).
- Apply `text-wrap: balance` on H1/H2 titles to eliminate orphan words.
- Use tight letter tracking (`tracking-tight` / `tracking-[-0.03em]`) on display headlines and loose tracking (`tracking-wider`) on uppercase eyebrows.

### Pillar 4: Luxury Art Direction for High-Value Moments
- Limit high-chroma visual complexity to **1 or 2 focal moments per page** (e.g. an interactive live proof card, an engineered hardware render, or a dynamic ROI calculator).
- Treat product previews like physical objects with light, shadow, and depth.
- Never use generic neon blobs or random gradient stock vectors.

---

## 3. Anti-Patterns: What to Avoid

1. **Pure Glassmorphism without Grounding:** Unbounded blurred cards turn interfaces into low-contrast mush and degrade mobile scroll performance.
2. **Neumorphism for Functional Forms:** Fails WCAG 2.1 AA contrast requirements because soft shadows cannot clearly define form boundaries.
3. **Trend-Chasing Hybrid Clashes:** Do not mix Neo-Brutalism (thick 3px black borders, harsh offset shadows) with delicate Luxury/Glassmorphism in the same viewport.
