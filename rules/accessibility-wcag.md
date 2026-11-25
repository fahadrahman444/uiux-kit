# Accessibility (WCAG 2.1 AA) Rules

All components and generated interfaces must satisfy Web Content Accessibility Guidelines (WCAG) 2.1 Level AA.

## 1. Keyboard Navigability & Focus Management
- **Focus Rings:** Never strip default focus styles without replacing them. Use genuine CSS `outline` with a Windows Forced Colors Mode fallback:
  `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]`
- **Tab Sequence:** Natural, logical tab order following visual hierarchy.
- **Modal Dialog Focus Traps:**
  - When a dialog or sheet opens, trap focus within the overlay.
  - Pressing `Escape` must close the overlay and return focus to the trigger element.

## 2. Screen Reader Semantics & ARIA
- **Icon-Only Buttons:** Every button that renders only an icon (e.g., close icon `X`, search icon, hamburger menu) MUST have an explicit `aria-label`:
  `<button aria-label="Close navigation menu">...</button>`
- **Live Regions:** Asynchronous notifications and form alert banners must declare `aria-live="polite"` or `role="alert"`.
- **Semantic HTML First:** Use native `<button>`, `<nav>`, `<main>`, `<dialog>`, and `<header>` tags rather than `<div>` with click listeners.

## 3. Visual & Perceptual Accessibility
- **Color Independence:** Do not rely solely on color to convey state. Pair color changes with icons, text labels, or distinct shapes.
- **Minimum Contrast:** Text must exceed 4.5:1 against its background.
- **Target Sizes:** Touch/click targets must be at least 44px by 44px on interactive controls.
