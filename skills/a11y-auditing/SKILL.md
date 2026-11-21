---
name: a11y-auditing
description: Comprehensive accessibility auditing playbook covering WCAG 2.1 AA validation, keyboard navigation, color contrast, focus rings, and ARIA tree compliance.
---

# Accessibility (A11y) Auditing Playbook

Use this skill to audit, diagnose, and fix accessibility compliance across web interfaces.

## 1. Key Automated Audit Points

### A. Touch Target Verification
- Find all `<button>`, `<a>`, and interactive elements.
- Verify that computed dimensions are at least `44px x 44px`.
- Common fix: add `min-h-[44px] min-w-[44px] flex items-center justify-center` or tap padding.

### B. Icon-Only Buttons
- Grep for `<button>` elements containing only an `<svg>` or `<i>` without text children.
- Fix: Add `aria-label="Descriptive action"` or `<span className="sr-only">Descriptive action</span>`.

### C. Color Contrast Math
- Body text (< 18pt or < 14pt bold): Minimum **4.5:1** contrast ratio.
- Large text ($\ge$ 18pt or $\ge$ 14pt bold): Minimum **3:1** contrast ratio.
- Form borders and active icons: Minimum **3:1** contrast ratio against background.

### D. Focus Indicators
- Audit all focusable inputs and buttons.
- Forbid `outline-none` unless accompanied by `focus-visible:ring-2 focus-visible:ring-offset-2`.

## 2. Manual Keyboard Navigation Test
1. Press `Tab` through the page: Is every interactive control reachable?
2. Open a modal: Does focus move inside the modal? Does pressing `Escape` dismiss it?
3. Tab order: Does it move predictably from top-to-bottom, left-to-right?
