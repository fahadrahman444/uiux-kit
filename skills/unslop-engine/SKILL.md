---
name: unslop-engine
description: Systematic process to diagnose, deconstruct, and redesign generic AI-generated interfaces into character-rich, accessible, and polished user experiences.
---

# Unslop Engine: AI Interface Rehabilitation

Use this skill when auditing or revising interfaces that look "AI generated", generic, or bloated.

> **Full Anti-Slop Reference Suite:** For the complete 9-pass methodology, exact token ramps, visual benchmarks, and sign checklists, refer to the integrated [`unslop` skill](../unslop/SKILL.md) and its references:
> - [`signs.md`](../unslop/references/signs.md) — The comprehensive audit checklist of AI slop signs.
> - [`tokens.md`](../unslop/references/tokens.md) — Tinted neutral ramps (Graphite, Warm, Ink) & exact type/spacing scales.
> - [`visuals.md`](../unslop/references/visuals.md) — Working visual styles, lighting, shadows, and hero scenes.
> - [`effects.md`](../unslop/references/effects.md) — Glyph rendering, canvas effects, and code treatments.
> - [`rtl.md`](../unslop/references/rtl.md) — Bi-directional & RTL layout rules.

---

## Diagnostic Checklist: The Hallmarks of AI Slop
1. **Purple/Pink/Cyan Gradient Overkill:** Defaulting to neon cyberpunk or generic SaaS purple gradients.
2. **Excessive Glassmorphism:** Layering `backdrop-blur-md` on cards with faint 1px white borders that look washed out.
3. **Floating Glowing Blobs:** Uncontrolled radial gradients in the background that add noise without visual meaning.
4. **Emoji-as-Icons:** Relying on emojis for navigation instead of crisp SVG icons (Lucide, Heroicons).
5. **No Visual Hierarchy:** Everything is a card with the same border, same shadow, and same font weight.

## Transformation Playbook

### Step 1: Establish Grounded Surfaces
- Replace translucent floating blur cards with solid background layers:
  - Dark: `#0F172A` (Slate 900) base with `#1E293B` (Slate 800) cards and `border-slate-700/50`.
  - Light: `#F8FAFC` (Slate 50) base with `#FFFFFF` cards and `border-slate-200`.

### Step 2: Intentional Color Restraint
- Pick **one** signature accent color that fits the domain (e.g. Amber/Orange for developer tools, Emerald for finance, Cobalt for enterprise SaaS).
- Use neutral grays for 90% of the UI; reserve the accent strictly for primary CTAs and active states.

### Step 3: Typography Tightening
- Increase body text legibility (14–16px, `leading-relaxed`, slate-600/slate-300).
- Use `text-balance` on headings to prevent single hanging words.
- Give headings strong semantic weights (`font-semibold` or `font-bold`) and clear scale increments.

### Step 4: Ergonomics & Polish
- Ensure every touch target is at least 44×44px.
- Replace generic spinners with skeleton shimmer loaders that mirror actual content shapes.
