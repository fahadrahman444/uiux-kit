---
name: micro-interactions
description: Physics-grounded micro-interactions, tap/hover states, mutation locks, and tactile UI feedback using Framer Motion and modern CSS.
---

# Micro-Interactions & Tactile Feedback

Use this skill when building buttons, toggles, list items, cards, and state transitions.

## 1. Tactile Button Interaction
Every interactive button should communicate physical presence:
- **Tap Scale:** Shrink slightly on press (`whileTap={{ scale: 0.98 }}` or `active:scale-[0.98]`).
- **Spring Response:** Quick recovery bounce (`transition={{ type: "spring", stiffness: 400, damping: 25 }}`).
- **Tactile Reset:** If translated on hover (`hover:-translate-y-0.5`), always reset on press (`active:translate-y-0`) to emulate tactile click feedback.
- **Explicit Pointer Affordance:** Every clickable surface must explicitly declare `cursor-pointer`.

## 2. Hardware-Accelerated Spotlight Effects (CSS Custom Properties)
Never bind `onMouseMove` coordinates to React component state (`setState({ x, y })`). Doing so triggers 60–120 full React virtual DOM re-renders per second, causing frame drops on scroll and typing.

### Correct Pattern:
Update CSS custom properties directly on the element DOM style:
```tsx
const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
  if (!divRef.current) return;
  const rect = divRef.current.getBoundingClientRect();
  divRef.current.style.setProperty("--spotlight-x", `${e.clientX - rect.left}px`);
  divRef.current.style.setProperty("--spotlight-y", `${e.clientY - rect.top}px`);
};
```
And reference in CSS:
```css
background: radial-gradient(350px circle at var(--spotlight-x, -999px) var(--spotlight-y, -999px), rgba(59, 130, 246, 0.15), transparent 70%);
```

## 3. Mutation Lock & Progress Feedback
Double-clicking a payment or submit button can trigger duplicate transactions or race conditions.
- Always provide an internal `loading` lock.
- Disable pointer events and show an animated spinner or pulse indicator while the async task runs.

```tsx
<motion.button
  whileTap={!loading ? { scale: 0.98 } : undefined}
  disabled={loading}
  className="relative inline-flex items-center justify-center min-h-[44px] min-w-[44px] px-4 py-2 font-medium rounded-lg bg-blue-600 text-white disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
>
  {loading ? <Spinner className="w-5 h-5 animate-spin" /> : children}
</motion.button>
```

## 4. Shimmer Skeleton Loading
Mirror the exact geometry of expected content with animated subtle background pulses instead of generic circle spinners for full pages.

## 5. Reduced-Motion Safeguard
Always respect user accessibility preferences:
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
