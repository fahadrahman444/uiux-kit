---
name: responsive-layouts
description: Patterns for mobile-first responsive grids, fluid typography, dynamic viewports, and adaptive overlay transformations (dialogs vs bottom drawers).
---

# Responsive Layouts & Adaptive Overlays

Use this skill when scaffolding application layouts, grids, navigation, and modals.

## 1. Dynamic Overlays: Modal vs. Bottom Drawer
Never render a rigid desktop dialog modal on mobile screens. It forces awkward pinch-zooming and misaligned close buttons.

### Pattern:
- **Mobile (< 640px):** Slide-up Bottom Sheet Drawer anchored to the bottom with gesture drag-to-dismiss.
- **Desktop (>= 640px):** Centered Dialog Box (`max-w-md mx-auto`) with subtle backdrop fade.

## 2. Adaptive Navigation Bars
- **Desktop:** Horizontal top bar with logo, navigation links, search, and profile actions.
- **Mobile:**
  - Compact header (logo + action icons).
  - Bottom tab navigation bar with 4–5 core navigation destinations inside thumb reach.
  - Safe-area bottom padding (`pb-[env(safe-area-inset-bottom)]`).

## 3. Fluid Responsive Grids
```tsx
// Example responsive container pattern:
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```
