# SlopGuard UI/UX Kit: Production Test Suite & Verification Matrix

> **Document Version:** `v1.6.1`  
> **Target Framework:** `WORKFLOW.md` v1.6.1  
> **Execution Engine:** Playwright + Axe-Core + SlopGuard Static Linter + Manual AT Protocol  
> **Pass Standard:** 100% of P0 Blockers = PASS; Overall Anti-Slop Score ≥ 85/100; 10/10 Definition of Done Gates Satisfied.

---

## Test Suite Architecture & Traceability

```
[ Suite 1: Token & Anti-Slop Static Gates ] ──► Rules: SLOP-001..006, TOKEN-001..002, PERF-001
[ Suite 2: WCAG 2.2 Standards-Precise A11y ] ──► Rules: A11Y-001..008, 1.4.3, 1.4.10, 2.4.11, 2.5.8
[ Suite 3: 14-State Component Quality ]      ──► Mandatory 14-State Interactive Matrix
[ Suite 4: Mobile Ergonomics & Touch ]       ──► Thumb Zones, 100dvh, Safe-Area, Keyboard Resizing
[ Suite 5: Route Performance & CWV SLAs ]   ──► LCP, INP, CLS, Byte Weight, Font Fallbacks
[ Suite 6: Form Security, CSP & Privacy ]    ──► Triple Spam Defense, Strict CSP, Zero-PII Telemetry
```

---

## Suite 1: Design Tokens & Anti-Slop Gating

### TC-SLOP-001: Verification of AI Dark-Mode Blobs
* **Rule ID:** `SLOP-001` | **Severity:** `Blocker` | **Detection:** `static`
* **Objective:** Ensure no blurred radial gradients from saturated indigo/purple exist on dark surfaces.
* **Test Steps:**
  1. Parse all CSS, SCSS, and inline Tailwind classes across `src/` and `components/`.
  2. Search for AST matches on `radial-gradient` where colors fall into saturated purple/indigo spectrum (`#6366f1`, `#8b5cf6`, `hsl(260..)`) with `filter: blur()`.
* **Expected Result:** Zero matches. All dark surfaces resolve to solid token surfaces (`--surface-base: #09090b` or `#0C0D0E`).
* **Pass / Fail:** FAIL if any match found (Trips Blocker → Score = 0).

### TC-SLOP-002: Verification of Raw Emojis as UI Icons
* **Rule ID:** `SLOP-002` | **Severity:** `Blocker` | **Detection:** `static`
* **Objective:** Ensure emojis are not used as primary visual indicators or interactive button icons.
* **Test Steps:**
  1. Run regex pattern `[\u{1F300}-\u{1F9FF}]` against all `button`, `a`, and `.card-header` elements.
  2. Verify all UI icons are instances of SVG components (Lucide / Phosphor).
* **Expected Result:** Zero un-escaped emoji icons inside interactive primitives.
* **Pass / Fail:** FAIL if raw emoji icon detected.

### TC-SLOP-003: Audited Telemetry for Marketing Metrics
* **Rule ID:** `SLOP-003` | **Severity:** `Major` | **Detection:** `heuristic`
* **Objective:** Ensure all quantitative stat cards (`+99.9%`, `10x`) reference verified case study data or audited sources.
* **Test Steps:**
  1. Inspect metric components (`PatternSplitHero`, `PatternSocialProof`).
  2. Check for existence of supporting citation link, methodology footnote, or verified customer source.
* **Expected Result:** Every stat card features an audit citation or data popover.
* **Pass / Fail:** Deduct 5 points per unsubstantiated stat card.

### TC-TOKEN-001: Strict Design Token Conformance
* **Rule ID:** `TOKEN-001` | **Severity:** `Major` | **Detection:** `static`
* **Objective:** Verify that zero hardcoded hex/RGB color literals bypass the Tier 2/3 token system.
* **Test Steps:**
  1. AST scanner analyzes all `.tsx`, `.jsx`, and `.css` files for color declarations matching `#[0-9a-fA-F]{3,8}` or `rgba?\(.*\)`.
  2. Allow exceptions only inside `tokens.css` or `tokens.ts`.
* **Expected Result:** 100% of color rules utilize `var(--color-*)` or mapped Tailwind theme utility classes.
* **Pass / Fail:** FAIL if un-waived raw hex is detected.

### TC-TOKEN-002: Layout Grid Spacing Conformance
* **Rule ID:** `TOKEN-002` | **Severity:** `Minor` | **Detection:** `static`
* **Objective:** Ensure all margin, padding, and gap declarations adhere to the 4px/8px scale.
* **Test Steps:**
  1. Scan for one-off pixel values (e.g. `mt-[13px]`, `padding: 17px`).
* **Expected Result:** All spacing values are exact multiples of 4px (`4, 8, 12, 16, 24, 32, 48, 64px`).
* **Pass / Fail:** Deduct 1 point per non-standard spacing value unless explicitly waived.

---

## Suite 2: Standards-Precise Accessibility (WCAG 2.2 AA / AAA)

### TC-A11Y-001: Target Size Compliance (WCAG 2.5.8 vs Mobile Baseline)
* **Rule ID:** `A11Y-001` | **Severity:** `Blocker` | **Detection:** `static` + `runtime-playwright`
* **Objective:** Guarantee all clickable elements meet legal WCAG 2.2 AA minimum (24×24px) and primary touch actions meet 44×44px.
* **Test Steps:**
  1. Launch Playwright at mobile viewport (390×844px).
  2. Query bounding client rect for all `button`, `a`, `input`, `select`, and `role="button"` elements.
  3. Validate width and height:
     * Hard Blocker: Any target < 24×24px without 24px circular exclusion clearance.
     * Advisory Warning: Primary action button < 44×44px.
* **Expected Result:** Zero targets under 24px; all primary mobile CTAs satisfy ≥ 44×44px.
* **Pass / Fail:** FAIL if any target < 24×24px.

### TC-A11Y-002: Accessible Name Computation
* **Rule ID:** `A11Y-002` | **Severity:** `Blocker` | **Detection:** `static`
* **Objective:** Ensure all interactive elements expose an accessible name to the accessibility tree.
* **Test Steps:**
  1. Run Axe-Core check `button-name`, `link-name`, `aria-label`.
  2. Verify icon-only buttons include `.sr-only` text or valid `aria-label`.
* **Expected Result:** Axe-Core returns 0 violations for accessible names.
* **Pass / Fail:** FAIL if any icon button lacks an accessible name.

### TC-A11Y-003: Text & UI Element Contrast (WCAG 1.4.3 / 1.4.11)
* **Rule ID:** `A11Y-003` | **Severity:** `Blocker` | **Detection:** `static` + `runtime-playwright`
* **Objective:** Verify contrast ratios under light, dark, and disabled states.
* **Test Steps:**
  1. Compute color contrast against resolved background for all text nodes:
     * Body text (< 18.5px bold or < 24px regular): Must be ≥ 4.5:1.
     * Large text / Headers: Must be ≥ 3:1.
     * Interactive borders and focus rings: Must be ≥ 3:1.
* **Expected Result:** 100% of text and meaningful UI boundaries meet required ratios.
* **Pass / Fail:** FAIL if any text contrast ratio is below threshold.

### TC-A11Y-005: Focus Not Obscured (WCAG 2.4.11)
* **Rule ID:** `A11Y-005` | **Severity:** `Blocker` | **Detection:** `runtime-playwright`
* **Objective:** Ensure sticky headers and bottom mobile bars never obscure keyboard-focused elements.
* **Test Steps:**
  1. Focus through every form input and button on mobile viewport.
  2. Execute `document.elementFromPoint(box.x, box.y)` at the center of the focused element.
* **Expected Result:** The focused element itself (or its child) is returned, proving it is not hidden under sticky headers or action bars.
* **Pass / Fail:** FAIL if sticky bar overlays the active focus indicator.

### TC-A11Y-006: Windows Forced Colors / High Contrast Outline Fallback
* **Rule ID:** `A11Y-006` | **Severity:** `Major` | **Detection:** `static`
* **Objective:** Ensure focus indicators remain clearly visible in Windows High Contrast Mode.
* **Test Steps:**
  1. Scan CSS for `@media (forced-colors: active)`.
  2. Verify `:focus-visible` defines an `outline: 2px solid Highlight` or equivalent system color.
* **Expected Result:** Real CSS `outline` is declared; does not rely solely on `box-shadow`.
* **Pass / Fail:** FAIL if focus ring is solely implemented via `box-shadow`.

### TC-A11Y-007: Consistent Help Mechanism (WCAG 3.2.6)
* **Rule ID:** `A11Y-007` | **Severity:** `Major` | **Detection:** `manual-review`
* **Objective:** Verify help triggers (Contact, FAQ, Live Chat) appear in the identical relative order across all pages.
* **Test Steps:**
  1. Compare DOM position of help triggers across `/`, `/work`, `/services`, and `/contact`.
* **Expected Result:** Support mechanisms maintain consistent relative placement in header and footer.
* **Pass / Fail:** Deduct 5 points if help mechanisms shift relative order between views.

### TC-A11Y-009: Screen Reader Audio Smoke Test Protocol
* **Rule ID:** `A11Y-MANUAL` | **Severity:** `Blocker` | **Detection:** `manual-review`
* **Objective:** Ensure end-to-end task completion with monitor off using NVDA (Windows) or VoiceOver (macOS/iOS).
* **Test Steps:**
  1. Activate screen curtain / speech viewer with display off.
  2. Navigate from Header to Hero, trigger "Book Strategy Call", submit empty form, and verify error alert announcement (`role="alert"`).
  3. Close modal via `Escape` key and verify focus returns to initiating trigger button.
* **Expected Result:** Clear, non-repetitive audio announcements; zero keyboard focus traps.
* **Pass / Fail:** Sign-off requires signed QA tester record.

---

## Suite 3: 14-State Component Quality

### TC-COMP-001: 14-State Interactive Component Matrix
* **Target Components:** `ActionButton.tsx`, `PatternSplitHero.tsx`, `BottomSheet.tsx`, `lead-form`.
* **Verification Matrix:**

| # | State | Test Action & Trigger | Expected DOM / Visual Behavior | Pass/Fail |
|---|---|---|---|:---:|
| 1 | `default` | Initial render | Standard surface token, crisp 1px hairline border. | [x] |
| 2 | `hover` | Pointer enters element | Smooth transition (< 220ms), subtle elevation or surface shift. | [x] |
| 3 | `focus-visible` | `Tab` into control | Dual-ring focus outline (2px brand + 3px offset). | [x] |
| 4 | `active / pressed` | Mouse down / touch start | Hardware scale transform (`scale(0.98)`). | [x] |
| 5 | `loading / mutating` | Trigger async submission | Button text displays spinner; `pointer-events: none` mutation lock. | [x] |
| 6 | `disabled` | Set `disabled={true}` | `aria-disabled="true"`, cursor `not-allowed`, contrast ≥ 3:1. | [x] |
| 7 | `read-only` | Set `readOnly={true}` | Content selectable but non-editable; distinct visual presentation. | [x] |
| 8 | `empty` | Zero items in dataset | Clean icon, helpful copy, direct call-to-action button. | [x] |
| 9 | `error` | Validation failure | High-contrast outline, `aria-invalid="true"`, linked error message. | [x] |
| 10 | `success` | Action completed | Visual confirmation icon, `role="status"` live announcement. | [x] |
| 11 | `partial-loading` | Data fetching | Shimmer skeleton cards matching exact dimensions to avoid CLS. | [x] |
| 12 | `permission-denied`| User unauthorized | Clear explanation with single upgrade / login action button. | [x] |
| 13 | `overflow` | 300-character string | Text wraps cleanly or truncates with accessible tooltip. | [x] |
| 14 | `RTL` | Set `dir="rtl"` | Margins, paddings, and directional icons mirror automatically. | [x] |

---

## Suite 4: Mobile Ergonomics & Viewport Dynamics

### TC-MOB-001: Thumb Zone Natural Reach
* **Objective:** Ensure 100% of high-frequency interactive actions sit in the lower 45% mobile screen area.
* **Test Steps:**
  1. Emulate iPhone 15 (393×852px) and Pixel 8 (412×915px).
  2. Measure distance of Primary CTA (Add to Bag / Book Call) from viewport bottom.
* **Expected Result:** Primary CTA is anchored within bottom sticky action bar with safe-area padding.
* **Pass / Fail:** FAIL if primary CTA requires reach to top 30% of screen on mobile.

### TC-MOB-002: Dynamic Viewport & Keyboard Resizing
* **Objective:** Prevent virtual keyboard from crushing or overlapping form inputs and sticky action footers.
* **Test Steps:**
  1. Set viewport to `interactive-widget=resizes-content`.
  2. Focus input inside form on mobile simulator.
* **Expected Result:** Sticky bottom action bar automatically hides (`display: none`) while virtual keyboard is open. Input remains in clear vertical view.
* **Pass / Fail:** FAIL if virtual keyboard overlaps focused input or crushes bottom bar into content.

---

## Suite 5: Route Performance & Core Web Vitals SLAs

### TC-PERF-001: LCP, INP, and CLS Benchmark Execution
* **Tooling:** Lighthouse CI + Web-Vitals Chrome Extension / Headless Chromium.
* **Thresholds (SLA vs Stretch):**

| Route | Metric | Production SLA (Commitment) | Internal Stretch Goal |
|---|---|---|---|
| **Marketing (`/`)** | **LCP** | ≤ 2.2s | ≤ 1.6s |
| | **INP** | ≤ 150ms | ≤ 80ms |
| | **CLS** | ≤ 0.05 | ≤ 0.01 |
| **Case Study (`/work/*`)** | **LCP** | ≤ 2.0s | ≤ 1.5s |
| | **INP** | ≤ 100ms | ≤ 50ms |
| | **CLS** | ≤ 0.03 | ≤ 0.00 |
| **Lead / Checkout Form** | **LCP** | ≤ 1.8s | ≤ 1.2s |
| | **INP** | ≤ 120ms | ≤ 70ms |
| | **CLS** | ≤ 0.02 | 0.00 |

* **Asset Weight Check:** Initial un-cached network transfer at LCP must be ≤ 450kB (gzip).

---

## Suite 6: Form Security, Bot Defense & Telemetry Privacy

### TC-SEC-001: Triple Bot Defense & Time-Trap Verification
* **Test Steps:**
  1. **Honeypot Test:** Programmatically populate hidden field `company_fax_field` and submit.
     * Expected: HTTP 200 returned, but payload safely discarded; no CRM sync.
  2. **Time-Trap Test:** Submit valid form payload in < 2.5 seconds from render.
     * Expected: Request rejected as automated script submission.
  3. **No-JS Fallback Test:** Disable JavaScript in browser and submit native `<form>`.
     * Expected: Clean standard POST submission succeeds via HTTP 303 redirect.

### TC-SEC-002: Strict Content Security Policy (CSP) Header Check
* **Test Steps:**
  1. Inspect HTTP response headers on production preview.
* **Expected Result:**
  * `object-src 'none'`
  * `base-uri 'self'`
  * `frame-ancestors 'none'`
  * `Reporting-Endpoints: csp-endpoint="/api/csp-report"`
* **Pass / Fail:** FAIL if any critical CSP directive is missing.

### TC-SEC-003: Zero-PII Telemetry Sanitization
* **Test Steps:**
  1. Intercept analytics payload on form submission.
  2. Inspect payload fields for PII (names, email strings, IP addresses).
* **Expected Result:** Payload contains only sanitized behavioral data (`cta_name`, `source_section`, `duration_ms`).
* **Pass / Fail:** FAIL if raw email or user identity is detected in analytics payload.

---

## Suite 7: Zero-Backend Static Discovery Studio & View Transitions (`tests/studio.spec.mjs`)

### TC-STUDIO-001: GitHub Pages HTTP Mode, WCAG 2.2 AA & View Transitions Wizard
* **Target:** [docs/index.html](docs/index.html) served over local HTTP (`tests/studio.spec.mjs`).
* **Test Steps:**
  1. Load `docs/` over HTTP, wait for initial `#panel-sections .blueprint-card` render, verify 0 runtime page errors.
  2. Run `AxeBuilder` (`wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa`) in **Light Mode**.
  3. Select `[data-preset="pricing"]`, fill `#project_name`, click `#compile-btn`, and verify `10` section cards plus all 6 output tabs (`#tab-sections`, `#tab-strategy`, `#tab-intel`, `#tab-stack`, `#tab-markdown`, `#tab-cli`).
  4. Select `[data-preset="multisite"]` and assert 5 `.page-group-header` route blueprints render cleanly.
  5. Navigate wizard Step 1 → Step 2 (`#wizard-next-btn`) → Step 1 (`#wizard-prev-btn`) → Step 4 (`.step-pill`), confirming View Transition frame settlement (`waitFor`) and contextual `[data-route-group]` accordion opening (`about` open, `careers` closed).
  6. Test validation step auto-return: clear required `#project_name` on Step 1, navigate to Step 5, click `#compile-btn`, and verify wizard switches back to Step 1 and focuses `#project_name`.
  7. Toggle Dark Mode (`#theme-toggle`) and run `AxeBuilder` (`0` violations).
* **Pass / Fail:** PASS when all checks pass with `0` runtime errors and `0` Axe violations in Light and Dark themes.

### TC-STUDIO-002: Direct `file://` Execution & 320px Mobile Reflow
* **Target:** Direct file URL (`file://.../docs/index.html`) at `320×740px` mobile viewport.
* **Test Steps:**
  1. Open `docs/index.html` directly via `file://` (`docs/data/kit-bundle.js` offline loader).
  2. Verify sections compile with `0` console/page errors and `document.documentElement.scrollWidth <= window.innerWidth`.
* **Pass / Fail:** PASS with zero errors and `0px` horizontal overflow.
