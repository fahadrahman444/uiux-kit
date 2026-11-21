---
name: text-density-reduction
description: The information scannability playbook for converting prose-heavy, text-bloated landing pages and service pages into crisp, visual, high-conversion UI layouts.
---

# Text Density Reduction: The Scannability Playbook

Use this skill when auditing or revising interfaces that feel text-heavy, academic, or structured like a documentation page rather than an engaging product or agency surface.

---

## 1. Core Principle: Scannable Units vs. Prose Documents

Interfaces fail when they are **written like a document** (multi-sentence paragraphs, essay-style explanations) but **displayed like a product interface** (cards, grids, vertical sections).

> **The Golden Rule:** Cut the main scroll word count by 40–50%. Never delete technical depth—push it behind **progressive disclosure** (accordions, tabs, interactive calculators) so that the primary scan is confident, fast, and visual.

---

## 2. Hard Copy Budgets per Element

Enforce strict word caps across all template elements:

| Element | Max Word Budget | Purpose & Format Rule |
|---|---|---|
| **H1 Hero Headline** | 6–8 words | Outcome and proposition, not descriptive explanation. |
| **Hero Subhead** | 15–20 words | One sentence (maximum two). Zero fluff. |
| **Section Eyebrow** | 1–3 words | All-caps tracking token (e.g. `ARCHITECTURE`, `ROI METRICS`). |
| **Section H2** | 5–8 words | Punchy outcome statement. No run-on sentences. |
| **Section Subcopy** | 15–25 words | One line max. If it repeats the H2, delete it. |
| **Card Headline** | 4–7 words | Noun phrase, never a full sentence. |
| **Card Body** | 8–12 words | Single idea. Maximum 2–3 visual lines. |
| **Feature Bullet** | 4–8 words | Action or outcome phrase. No full stops. |
| **Button / CTA Label** | 2–4 words | Direct verb + object (e.g., "Deploy Project", "Calculate ROI"). |
| **Accordion / FAQ Answer** | 40–60 words | Progressive disclosure: this is where depth lives. |

*If any content block exceeds its word budget, it **must** be converted into an accordion, comparison table, or data grid.*

---

## 3. The 6 Prose-to-UI Conversions

Never remove copy without replacing it with an equivalent, high-velocity visual primitive:

### A. Prose → Chip / Pill Cloud
* ❌ *"Our stack includes Next.js 15, TypeScript, Tailwind CSS, and edge caching deployed on global CDN infrastructure."*
* ✅ `Next.js 15` · `TypeScript` · `Tailwind CSS` · `Edge CDN` (as an interactive badge array).

### B. Prose → Stat Block
* ❌ *"Our engineering practices guarantee near-instant page load times and perfect accessibility compliance across devices."*
* ✅ **100** Lighthouse · **0.8s** LCP · **AA** WCAG (three high-contrast numbers paired with micro-labels).

### C. Prose → Comparison Table (The "Old Way vs. New Way")
* ❌ Two 80-word paragraphs describing how standard agencies build websites versus our modern methodology.
* ✅ A 2-column, 4-row matrix (`Typical Build` vs `Modern Architecture`) comparing Speed, Ownership, Accessibility, and Guarantees with 2–4 word values.

### D. Prose → Icon + Monospace Spec Grid
* ❌ *"We support automated CI/CD deployment pipelines, automated end-to-end regression testing, and zero-downtime rollbacks."*
* ✅ 3-column micro-card grid with Lucide icons, bold headlines, and single-sentence descriptions.

### E. Prose → Visual Stepper / Delivery Roadmap
* ❌ *"In the first week we do discovery, in the second week we design, and by the third week we deploy."*
* ✅ Linear horizontal or vertical timeline stepper (`01 Discovery` → `02 Architecture` → `03 Ship`) with milestone tags.

### F. Prose → Interactive Playmaker / Calculator
* ❌ Lengthy explanations of how much revenue or time a client saves with optimized leads.
* ✅ Interactive ROI Slider / Lead Value Calculator that updates projected numbers in real-time.

---

## 4. The 3-Line Card Rule

Every card across feature grids and bentos must obey:
1. **Line 1:** Category tag or Lucide icon + concise noun title.
2. **Line 2–3:** Single-sentence value proposition (maximum 12 words).
3. **Bottom Line:** Metric badge or monospace specification (`Sub-second TTFB`, `TypeScript 5.0`).

---

## 5. Structural Anti-Density Heuristics

1. **Section Splitting:** Split 8–10 item bullet lists into two balanced 4–5 item columns or cards.
2. **Generous Vertical Breathing:** Maintain `py-20` to `py-28` (80–112px) padding between sections to avoid claustrophobic page feel.
3. **Alternating Surface Contrast:** Alternate section backgrounds (`surface-canvas` vs `surface-card`) to break up the endless-scroll sensation.
4. **Sticky Mini-CTA:** Place an accessible sticky CTA on mobile so visitors can convert without having to read through 1,500 words of copy.

---

## 6. The Visual "Blur Test"

> **Deterministic Test:** Zoom out or blur the webpage screenshot. If the layout blends into a uniform gray wall of text, the page fails the scannability audit. The page must resolve into distinct silhouettes: headline + stat blocks + grid cards + high-contrast CTA anchors.
