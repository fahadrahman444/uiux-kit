# Enterprise Design System Standards: The Industry Benchmarks

A unified engineering synthesis of the world's most rigorously tested, accessible, and scalable enterprise design systems: **GOV.UK**, **IBM Carbon**, **GitHub Primer**, and **Material Design 3 / Microsoft Fluent UI**.

---

## 1. GOV.UK Design System: The Form & Accessibility Gold Standard

The UK Government Digital Service (GDS) is universally recognized as the gold standard for accessible forms, cognitive simplicity, and transaction flows.

### 1.1 "One Thing Per Page" Philosophy
* When users face complex multi-step processes (tax filing, registration, checkout), break the journey into discrete steps where each page addresses **one clear question or intent**.
* Prevents cognitive overload, reduces form validation bounce rates, and makes navigation backward and forward deterministic.

### 1.2 Error Summary Pattern (Mandatory for Forms)
* When a form submission fails validation:
  1. Set keyboard focus immediately to an **Error Summary Box** at the very top of the page.
  2. Include an `<h2 className="text-rose-600 font-bold">There is a problem</h2>`.
  3. List every invalid field as a clickable link pointing directly to the corresponding input (`<a href="#email">Enter an email address in the correct format</a>`).
  4. Display inline red error text directly between the label and the input.

### 1.3 Error Message Writing Formula
Never use developer jargon or accusatory language. Follow the strict formula:
$$\text{[State what went wrong]} + \text{[State how to fix it]}$$
* ❌ *"Invalid input in field."*
* ❌ *"Email is required."*
* ✅ *"Enter your email address in the format name@example.com"*
* ✅ *"Your password must be at least 8 characters and include at least one number"*

### 1.4 Grouping with `<fieldset>` and `<legend>`
* Every group of related radios or checkboxes must be wrapped in a `<fieldset>` with an explicit `<legend>`. This ensures screen readers announce the category question when focusing each individual option.

### 1.5 "Check Your Answers" Pattern
* Always provide a summary table showing all entered data with "Change" links before final submission.

---

## 2. IBM Carbon Design System: The Data & Enterprise Standard

IBM Carbon is built for complex, mission-critical, data-dense enterprise applications (cloud consoles, cybersecurity, analytics).

### 2.1 Complex Data Table Architecture
Enterprise tables must support high-volume data manipulation without page reloads:
* **Batch Action Toolbar:** When 1 or more rows are checked, the header transforms into a batch action bar (e.g. *3 items selected: [Delete] [Export] [Reassign]*).
* **Multi-Column Sorting:** Clear visual sort arrows (neutral when unsorted, active when sorted, indicating ASC/DESC order).
* **Row Expansion:** Nested details (logs, sub-tasks) expand smoothly within the row rather than forcing modal popups.
* **Sticky Column / Header Pinning:** Keep column headers and primary identifiers (e.g. name or ID) visible during horizontal and vertical scrolling.

### 2.2 Table Row Density Scale
Provide user-toggleable density modes:
* **Compact (32px height):** For data analysts and operators scanning 50+ rows simultaneously.
* **Default (48px height):** Standard balance of legibility and information density.
* **Tall (64px height):** For rows containing multi-line text, avatar groups, or complex badge arrays.

### 2.3 The 4-Tier Notification Hierarchy
Never use toasts for everything. Respect the notification matrix:
1. **Toast (Ephemeral / Low Urgency):** Auto-dismisses in 4–6s. Used only for background confirmations (*"Export generated successfully"*). Never put critical errors in toasts.
2. **Inline Notification (Field/Section Level):** Positioned directly alongside relevant controls. Persistent until resolved.
3. **Banner / Global Callout (System Level):** Positioned at top of viewport for system outages, subscription expirations, or maintenance warnings.
4. **Modal Dialog (Disruptive / Blocking):** Requires explicit user confirmation for irreversible destructive actions.

---

## 3. GitHub Primer: Information Density & Developer Ergonomics

GitHub Primer specializes in high-density, low-friction interfaces for engineers and technical users.

### 3.1 Developer Metadata & Monospace Discipline
* Use monospaced font tokens (`font-mono text-xs`) for machine-generated data: Git commit SHAs, file paths, branch names, IP addresses, and HTTP status codes.
* Pair monospaced data with single-click copy affordances and tactile feedback tooltips (*"Copied!"*).

### 3.2 Visual Breadcrumb & Repository Hierarchy
* Deep technical hierarchies must use structured breadcrumbs with distinct separators (`/` or `›`) and truncated parent directories (`... / repo / src / index.ts`).

### 3.3 Split vs. Unified Diff Ergonomics
* Provide split (side-by-side) and unified diff views with synchronized line numbering.
* Add line-level expansion markers (`@@ -42,7 +42,9 @@`) to load context without page jumps.

---

## 4. Material Design 3 & Microsoft Fluent UI: Elevation & Light Physics

### 4.1 The 8pt / 4pt Spatial Grid
* Layout dimensions, component heights, and padding must be multiples of **8px** (`8, 16, 24, 32, 48, 64px`).
* Micro-spacing (inner button padding, icon-to-label gaps) uses the **4px** half-grid.

### 4.2 Tonal Surface Elevation vs. Heavy Drop Shadows
* **Material Design 3 (Tonal Elevation):** Instead of black drop shadows, higher elevation surfaces receive a subtle semi-transparent primary color tint layer (e.g. Surface Container Low $\rightarrow$ Surface Container $\rightarrow$ Surface Container High).
* **Microsoft Fluent UI (Mica & Acrylic Materials):** Translucent depth effects that tint based on desktop theme wallpaper while maintaining crisp 1px borders for structural delineation.

### 4.3 Adaptive Responsive Breakpoint Taxonomy
| Breakpoint | Window Width | Layout Anatomy | Primary Navigation |
|---|---|---|---|
| **Compact** | `< 600px` | 4-column grid, 16px margin | Bottom Tab Bar or Drawer |
| **Medium** | `600px – 840px` | 8-column grid, 24px margin | Navigation Rail (icons only) |
| **Expanded** | `> 840px` | 12-column grid, 32px margin | Permanent Left Sidebar |

### 4.4 Complete 6-State Interactive Coverage
Every interactive component must define explicit visual styles for:
1. **Rest (Default)**
2. **Hover (Cursor proximity)**
3. **Focus-Visible (Keyboard navigation focus ring)**
4. **Active / Pressed (Tactile pushdown)**
5. **Dragged (Elevation rise & cursor grab)**
6. **Disabled (50% opacity, pointer-events none)**
