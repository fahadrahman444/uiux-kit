# Visual Identity & Anti-Slop Interface Rules

## 1. Defining "Slop" vs. Distinctive Design
AI-generated interfaces often look interchangeable: purple linear gradients, excessive backdrop blurs, floating glow orbs, identical rounded cards, and unreadable low-contrast text.

To build distinctive, high-end interfaces:
- **Prioritize Solid Surfaces:** Rely on crisp borders (`border border-slate-200 dark:border-slate-800`), clean background elevations, and subtle drop shadows rather than heavy translucent blurs.
- **Controlled Accents:** Choose a clear monochromatic or neutral foundation (Zinc, Slate, Neutral) with one intentional primary accent color (e.g., deep sapphire, electric blue, or terracotta).
- **Surface Elevation over Pure White/Black:** Use layered shades to create depth instead of extreme contrast or floating blur halos.

## 2. Typography & Hierarchy
- **Contrast & Legibility:** Maintain a minimum 4.5:1 contrast ratio for body text against backgrounds, and 3:1 for large display text.
- **Leading & Balance:**
  - Headings that wrap on mobile must have adequate line-height (`leading-[1.15]` or `leading-[1.2]`).
  - Use `text-wrap: balance` on section titles to avoid single trailing words ("orphans").
- **Font Pairing Restraint:** Stick to maximum 2 font families (one expressive display/serif or geometric sans for headlines, one high-legibility sans for body).

## 3. Form & Control Discipline
- Avoid borderless floating inputs. Provide clear input bounding boxes with visible default borders.
- State feedback: Always define distinct `:hover`, `:focus-visible`, `:active`, and `:disabled` states.
