# Design System Specification

## 1. Palette & Surface Hierarchy
- **Base Neutral:** Slate / Zinc / Neutral
- **Background Primary:** `#0B0F17` (Dark) / `#FFFFFF` (Light)
- **Surface Elevation 1:** `#131926` (Dark) / `#F8FAFC` (Light)
- **Surface Elevation 2:** `#1E293B` (Dark) / `#F1F5F9` (Light)
- **Primary Brand Accent:** `#3B82F6` (Electric Indigo / Sapphire)
- **Semantic Accents:**
  - Success: `#10B981` (Emerald)
  - Warning: `#F59E0B` (Amber)
  - Critical: `#EF4444` (Rose)

## 2. Typography Scale
- **Display / Hero:** `clamp(2.25rem, 5vw, 4.5rem)` (leading-tight)
- **H1:** `clamp(1.75rem, 3.5vw, 2.75rem)` (leading-tight, text-balance)
- **H2:** `clamp(1.35rem, 2.5vw, 2rem)` (leading-snug)
- **H3:** `1.25rem` (leading-snug)
- **Body Large:** `1.125rem` (leading-relaxed)
- **Body Base:** `1rem` (leading-normal)
- **Small / Metadata:** `0.875rem` (leading-normal)

## 3. Touch & Spacing Metrics
- Minimum Interactive Tap Area: `44px x 44px`
- Base Spacing Grid: 4px increments (`4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`, `64px`)
- Radius Tokens:
  - Small elements (Badges, tags): `rounded-md` (6px)
  - Controls (Inputs, buttons): `rounded-lg` (8px)
  - Cards & Drawers: `rounded-2xl` (16px)
