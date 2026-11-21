# Mobile Ergonomics & Viewport Rules

Mobile devices represent the majority of user touchpoints. Interfaces must be engineered thumb-first.

## 1. The Thumb Zone & Tap Ergonomics
- **Interactive Target Size:** Interactive controls must be $\ge$ 44×44px in physical footprint (using padding or pseudo-elements if visual icon is smaller).
- **Sticky Actions (Bottom CTA):**
  - Place primary flow actions (checkout, confirm, submit, filter) in a sticky bottom container anchored to the bottom thumb zone:
    `fixed bottom-0 left-0 right-0 p-4 border-t pb-[calc(1rem+env(safe-area-inset-bottom,0px))]`
- **Separation:** Maintain at least 8px spacing between adjacent touch targets to avoid accidental taps.

## 2. Viewport & Scrolling Dynamics
- **Dynamic Viewports (`dvh`):** Never use `100vh` on mobile layouts because browser URL address bars cause layout jumps when scrolling. Use:
  `min-h-[100dvh]` or `h-[100dvh]`
- **Safe Area Insets:** Account for hardware notches and gesture home indicators:
  `pb-[env(safe-area-inset-bottom)]` and `pt-[env(safe-area-inset-top)]`
- **Horizontal Overflow Isolation:** Apply `overflow-x-clip` or `overflow-x-hidden` on application wrappers to stop horizontal page wobbling during vertical swipes.

## 3. Responsive Overlays
- **Desktop:** Centered modal dialog (`max-w-md mx-auto`).
- **Mobile ($\le$ 640px):** Slide-up bottom sheet drawer with swipe gesture dismissibility.
