---
name: micro-interactions
description: Physics-grounded micro-interactions, tap/hover states, mutation locks, and tactile UI feedback using Framer Motion and modern CSS.
---

# Micro-Interactions & Tactile Feedback

Use this skill when building buttons, toggles, list items, cards, and state transitions.

## 1. Tactile Button Interaction
Every interactive button should communicate physical presence:
- **Tap Scale:** Shrink slightly on press (`whileTap={{ scale: 0.97 }}`).
- **Spring Response:** Quick recovery bounce (`transition={{ type: "spring", stiffness: 400, damping: 25 }}`).
- **Active State:** Clear brightness change on `:hover` and `:active`.

## 2. Mutation Lock & Progress Feedback
Double-clicking a payment or submit button can trigger duplicate transactions.
- Always provide an internal `loading` lock.
- Disable pointer events and show an animated spinner or pulse indicator while the async task runs.

```tsx
<motion.button
  whileTap={!loading ? { scale: 0.98 } : undefined}
  disabled={loading}
  className="relative inline-flex items-center justify-center min-h-[44px] min-w-[44px] px-4 py-2 font-medium rounded-lg bg-blue-600 text-white disabled:opacity-60 disabled:cursor-not-allowed"
>
  {loading ? <Spinner className="w-5 h-5 animate-spin" /> : children}
</motion.button>
```

## 3. Shimmer Skeleton Loading
Mirror the exact geometry of expected content with animated subtle background pulses instead of generic circle spinners for full pages.
