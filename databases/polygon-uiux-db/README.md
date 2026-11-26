# Standalone Dark Kinetic Emerald UI/UX Reference Database

Normalized, reusable UI/UX design system extracted from dark-mode kinetic agency layout, motion, hover, button, and scroll choreography patterns. Contains **zero company data** (no brand names, addresses, phones, emails, team bios, client logos, or business copy)—only design tokens, button specs, scroll/motion rules, component specs, section templates, audit remediations, and 14 structural page templates with `{{slot}}` placeholders.

## Directory Structure

- `polygon_uiux.db` — Relational SQLite 3 database with foreign-key constraints and `v_page_blueprints` view
- `polygon_uiux.sql` — Full portable SQL schema + seed dump (SQLite / ANSI-compatible)
- `build_db.py` — Deterministic builder & zero-company-data validator
- `tokens/design-tokens.json` — Structured design tokens, buttons, ScrollSmoother/parallax layers, ScrollTrigger entrances, custom cursors, menu waves, and carousel configs
- `tokens/polygon-theme.tokens.css` — Drop-in CSS custom properties, utility primitives, forced-colors focus, and `prefers-reduced-motion` safety
- `data/*.json` & `data/*.csv` — Per-table exports (11 normalized tables):
  - `design_themes` (1 theme)
  - `color_tokens` (14 WCAG-verified palette tokens)
  - `typography_tokens` (13 display/body roles using `Poppins` + `Kanit`)
  - `breakpoints` (7 responsive breakpoints)
  - `button_catalog` (6 button patterns including 170px radial/magnetic CTAs, 46px header pill, 33px dark pill, 44px MixItUp filter pills, and 250px video lightbox trigger)
  - `motion_specs` (21 GSAP ScrollSmoother, `data-speed`, velocity `skewY`, SplitText, bounce drops, char-wave nav, 15deg service swap + ribbon wipe, custom cursors, pins, and Swiper specs)
  - `component_patterns` (14 signature UI & interaction primitives)
  - `section_templates` (12 reusable page building blocks mapped to `gemini-uiux-kit`)
  - `page_templates` (14 full page blueprints)
  - `page_section_slots` (54 ordered route-to-section slot definitions)
  - `audit_remediations` (8 contrast, keyboard focus, JS `mousemove` leak, fluid scale, reduced-motion, and anti-slop fixes)

## Rebuild & Query

```bash
python build_db.py
```
