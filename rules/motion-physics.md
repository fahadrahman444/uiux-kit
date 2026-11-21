# Motion Physics & Animation Rules

Animation in modern UI should be purposeful, responsive, and physically grounded.

## 1. Physics-Based Springs & Curves
- Prefer spring physics or standard cubic-bezier curves over linear or generic ease:
  - Quick UI feedback (buttons, toggles): `transition={{ duration: 0.15, ease: "easeOut" }}`
  - Sheet/Modal entrances: `transition={{ type: "spring", stiffness: 350, damping: 30 }}`
- Duration budget:
  - Micro-interactions (hover, click): 100ms – 150ms
  - Navigation transitions: 200ms – 300ms
  - Avoid animations exceeding 400ms for everyday UI controls.

## 2. Browser Compositor Performance (60fps Rule)
- **Animate only Composited Properties:** Animate `transform` (scale, x, y) and `opacity`. Never animate `width`, `height`, `top`, `margin`, or `padding` directly.
- **The Backdrop-Blur Lag Rule:**
  - NEVER animate the `opacity` of an element that has `backdrop-filter: blur(...)`.
  - Browsers recalculate full-surface GPU rasterizations on every frame when opacity changes on blur filters.
  - Solution: Keep the blur layer static, and animate a solid translucent overlay inside it or avoid blurs during rapid transitions.

## 3. Respect User Motion Preferences
- Always respect `prefers-reduced-motion`:
  In Tailwind: `motion-safe:animate-...` or disable Framer Motion animations when `useReducedMotion()` is active.
