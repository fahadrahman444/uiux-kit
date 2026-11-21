---
name: design-tokens
description: Architecture, naming conventions, and Tailwind/CSS variable definitions for scalable design tokens across color, typography, spacing, radius, and elevation.
---

# Design Tokens Architecture

Use this skill when configuring theme tokens, CSS variables, and Tailwind theme extensions.

## 1. Token Taxonomy
Design tokens follow a 3-tier taxonomy:
1. **Primitive Tokens (Raw values):**
   - `--blue-500: #3b82f6`
   - `--slate-900: #0f172a`
2. **Semantic Tokens (Meaning/Role):**
   - `--bg-surface-elevated: var(--slate-900)`
   - `--text-primary: var(--slate-50)`
   - `--text-secondary: var(--slate-400)`
   - `--action-primary: var(--blue-500)`
3. **Component Tokens (Specific UI element):**
   - `--btn-primary-bg: var(--action-primary)`

## 2. Standard CSS Variables Setup (Tailwind V3 / V4)
```css
:root {
  --bg-app: #ffffff;
  --bg-surface: #f8fafc;
  --bg-surface-hover: #f1f5f9;
  --border-subtle: #e2e8f0;
  --text-primary: #0f172a;
  --text-muted: #64748b;
  --accent: #2563eb;
  --accent-foreground: #ffffff;
}

.dark {
  --bg-app: #090d16;
  --bg-surface: #111827;
  --bg-surface-hover: #1f2937;
  --border-subtle: #1f2937;
  --text-primary: #f9fafb;
  --text-muted: #9ca3af;
  --accent: #3b82f6;
  --accent-foreground: #ffffff;
}
```

## 3. Spacing and Radius Tokens
- Control Radius: `rounded-lg` (8px) for buttons, inputs, pills.
- Container Radius: `rounded-xl` (12px) or `rounded-2xl` (16px) for cards, sheets, panels.
- Spacing Scale: Base 4px system (`p-1`=4px, `p-2`=8px, `p-3`=12px, `p-4`=16px, `p-6`=24px).
