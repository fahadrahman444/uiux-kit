---
name: ux-patterns-guide
description: Developer-focused UX pattern blueprints covering accessible form validation, high-density data tables, modal vs drawer dialogs, command palettes, multi-step wizards, and empty states.
---

# Developer-Focused UX Patterns & Implementation Blueprints

Use this skill when implementing core interactive workflows, data displays, navigation components, and state management in web applications.

---

## 1. Accessible Form Validation Pattern (GOV.UK & W3C Standard)

Never validate forms only on blur or only on submit without accessible error communication.

### Implementation Blueprint:
1. **Live vs. Submit Validation:**
   - Validate format and completeness upon initial `onSubmit`.
   - Once a field has failed, switch that specific field to `onChange` validation so the user sees immediate feedback when they correct the error.
2. **Error Summary Banner:**
   - Display a high-contrast red error summary block at the top of the form containing anchor links to invalid fields.
   - Set `tabIndex={-1}` and call `.focus()` on the summary banner on submit failure.
3. **ARIA Association:**
   - Link error messages to input fields with `aria-describedby="email-error"`.
   - Set `aria-invalid="true"` on invalid inputs.

```tsx
<div className="space-y-1.5">
  <label htmlFor="email" className="block text-sm font-semibold text-slate-900 dark:text-slate-100">
    Email address
  </label>
  {error && (
    <p id="email-error" className="text-xs font-medium text-rose-600 dark:text-rose-400">
      Enter an email address in the format name@domain.com
    </p>
  )}
  <input
    id="email"
    type="email"
    aria-invalid={!!error}
    aria-describedby={error ? "email-error" : undefined}
    className="w-full min-h-[44px] px-3.5 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 aria-invalid:border-rose-500 aria-invalid:ring-rose-500/20"
  />
</div>
```

---

## 2. Enterprise Data Table Pattern (IBM Carbon Standard)

For data-dense operational tables:
- **Sticky Header & Fixed Column:** Pin `thead` with `sticky top-0 z-10 bg-slate-100 dark:bg-slate-800`.
- **Keyboard Navigation:** Support Arrow keys navigation between cells with `role="grid"`.
- **Row Density Toggle:** Allow user switching between Compact (`h-8`), Default (`h-12`), and Relaxed (`h-16`).
- **Batch Actions:** When rows are selected, convert the table header into a batch action toolbar (`Delete Selected`, `Export`, `Tag`).

---

## 3. Command Palette (`Cmd+K` / `Ctrl+K`) Pattern

- **Keyboard Trap:** Trap focus inside the search input upon opening (`Esc` closes and restores focus to previous element).
- **Fuzzy Search:** Filter commands in real time with grouped categories (Navigation, Actions, Settings).
- **A11y Announcement:** Use `role="combobox"` with `aria-expanded="true"` and `aria-activedescendant` pointing to the highlighted option.

---

## 4. Multi-Step Wizard Pattern

- **Step Tracker:** Show clear step indicators (`Step 2 of 4: Organization Details`) with completed, current, and upcoming states.
- **State Persistence:** Cache progress in `sessionStorage` or URL query params so accidental reloads do not wipe user input.
- **Save & Exit:** Always provide a "Save and finish later" option on forms requiring $>3$ minutes.

---

## 5. Meaningful Empty States

Never display a completely blank white box or raw empty array.
- **Icon / Visual Silhouette:** Monochromatic or subtle tinted illustration matching the missing entity.
- **Clear Heading:** State what is missing (e.g. *"No API keys generated yet"*).
- **Explanatory Subcopy:** 1 sentence explaining the benefit of creating one.
- **Primary Action Button:** Single prominent CTA (`Create Your First Key`).
