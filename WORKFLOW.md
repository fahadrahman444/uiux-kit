# SlopGuard UI/UX Kit: Hardened Production Engineering Workflow & Operating Model

> **Specification Version:** `v1.6.1`  
> **Tooling Compatibility:** CLI `slopguard@^1.6.1` (legacy alias: `gemini-uiux`, deprecated) | Token Schema `tokens@1` | Rules Schema `rules@1`  
> **Package License:** `MIT` (Core software & CLI) | Creative methodology text assets under `CC-BY-4.0` (See `NOTICE` file)  
> **Operational Posture:** Automated static and runtime-playwright verification coupled with mandatory human and assistive technology (AT) evaluation. Replaces subjective assertions with mathematically scored rubrics, single-source-of-truth rule IDs, CI exit codes, and an audited waiver governance process.

---

## 1. Architectural Foundation & Governance Model

The framework operates on a **three-tier token architecture** and a **phased verification pipeline**, preventing "vibe-coded" drift and ensuring enterprise-grade accessibility, performance, and brand distinction.

### 1.1 Three-Tier Token Architecture

```
[ Tier 1: Primitive Tokens ]
  (Raw values: palette hexes, raw spacing numbers, bezier curves)
  e.g., --color-blue-600: #0047FF; --space-4: 16px;
                 ↓
[ Tier 2: Semantic System Tokens ]
  (Purpose, context, and theme mappings across light/dark/forced-colors)
  e.g., --color-action-primary, --color-focus-ring, --border-subtle, --surface-raised
                 ↓
[ Tier 3: Component Scoped Tokens ]
  (Tied directly to component implementation contracts)
  e.g., --btn-primary-bg: var(--color-action-primary); --card-border: var(--border-subtle);
```

### 1.2 System Governance & Waiver Lifecycle
No rule is absolute without an escape valve for valid domain exceptions (e.g., identical cards are legitimate in financial comparison matrices).

* **Review Board:** Design System Lead (Aesthetic & Tokens) + Staff Accessibility Engineer (WCAG Compliance).
* **Waiver Lifecycle:**
  1. **Application:** Developer/Designer creates or updates `.design/audit-baseline.json` with rule ID, file location, visual evidence (screenshot/DOM path), and business justification.
  2. **Severity Classification:** 
     * `blocker` (Requires VP/Principal sign-off)
     * `major` (Requires System Lead sign-off)
     * `minor` (Requires Peer Reviewer sign-off)
  3. **Time-Boxing:** Waivers expire after **90 days** and must be re-evaluated or permanently resolved.

### 1.3 Rule Lifecycle Policy
Rules progress through **five** standardized stages:
1. `proposed` — RFC under review by Design System Board.
2. `experimental` — Emits non-blocking CI warnings (`Exit 1`).
3. `stable` — Enforced as blocking criteria (`Exit 2`).
4. `deprecated` — Scheduled for retirement (minimum 180-day grace window; aliased in `rule-aliases.json`).
5. `retired` — Removed from active audit runs.

### 1.4 What Changed in v1.6.1 (Changelog Summary)
* **Rebrand & Trademark De-risking:** Standardized CLI binary name on `slopguard` (npm package: `@slopguard/uiux`). `gemini-uiux` maintained only as a legacy shell alias until v2.0.0.
* **Encoding Normalization:** Normalized entire specification to strict UTF-8 with zero mojibake corruption.
* **Severity Override Guard:** Corrected mathematical formula to prevent accidental downgrades of `blocker` rules via local config.
* **Catalog Traceability:** Aligned rule axes, merged `SLOP-007` to canonical `PERF-001`, and reclassified `A11Y-007` and `SLOP-004` detection mechanisms.
* **CLI Command Restoration:** Restored `slopguard version` to command surface.

---

## 2. Complete Inventories & System Catalogs

### 2.1 The 7 Immutable Law Sets
Located in `rules/`:

| Law Set File | Domain | Core Mandate & Technical Enforcement |
|---|---|---|
| `visual-identity.md` | Surface & Color Hierarchy | Eliminates AI slop (glowing purple blobs, ungrounded surfaces). Enforces semantic token mapping and quiet chrome. |
| `design-philosophies.md` | Architectural Styles | Categorizes the 12 timeless aesthetic approaches; guides style selection based on product domain. |
| `cognitive-ux-laws.md` | Behavioral Psychology | Enforces Hick’s Law (decision latency), Fitts’s Law (hit areas), Miller’s Law (chunking), and cognitive load reduction. |
| `enterprise-design-systems.md` | Scalable Architecture | Bridges patterns from GOV.UK, IBM Carbon, GitHub Primer, Material 3, and Fluent 2 for enterprise resilience. |
| `accessibility-wcag.md` | Inclusive Engineering | Enforces WCAG 2.2 AA (and targeted AAA) compliance, dual-ring focus, screen reader trees, and reflow. |
| `mobile-ergonomics.md` | Touch & Viewport | Dictates 44×44px preferred tap footprints (never < 24px), 100dvh dynamics, and thumb zones. |
| `motion-physics.md` | Compositor Performance | Mandates 60fps animations restricted to `transform` and `opacity`; enforces `prefers-reduced-motion`. |

---

### 2.2 The 14 Autonomous Skills Inventory
Located in `skills/`:

| # | Skill Directory | Core Purpose & Technical Assets | Author & License |
|---|---|---|---|
| **1** | `a11y-auditing/` | Automated AST parsing and runtime accessibility verification | SlopGuard Core / `MIT` |
| **2** | `anti-slop-design/` | 7-axis quality gating system curing AI frontend templates | @wwewtech / `MIT` |
| **3** | `anti-ui-slop/` | UIZZE design system extension; enforces state coverage | SlopGuard Core / `MIT` |
| **4** | `design-tokens/` | Token compilation (Style Dictionary) to CSS/Tailwind | SlopGuard Core / `MIT` |
| **5** | `micro-interactions/` | Physics-based interactions, mutation locks, spotlight cards | SlopGuard Core / `MIT` |
| **6** | `responsive-layouts/` | Mobile drawers, bottom-sheet patterns, safe-area math | SlopGuard Core / `MIT` |
| **7** | `text-density-reduction/`| Converts narrative prose into structured visual primitives | SlopGuard Core / `MIT` |
| **8** | `timeless-patterns/` | Playbook for selecting and executing the 12 design approaches | SlopGuard Core / `MIT` |
| **9** | `ui-ux-pro-max/` | Intelligence database (50+ styles, 96 palettes, 57 font pairs) | SlopGuard Core / `MIT` |
| **10** | `unslop/` | 9-pass redline refactoring methodology & prompt text | Damir Sokolovsky / `CC-BY-4.0` (Text) & `MIT` (Scripts) |
| **11** | `unslop-commit/` | Conventional commit guidelines stripping AI hype (Prompt rules)| Damir Sokolovsky / `CC-BY-4.0` |
| **12** | `unslop-engine/` | Quick diagnostic guidelines and redline checklists | Damir Sokolovsky / `CC-BY-4.0` |
| **13** | `unslop-review/` | Code review prompt instructions without AI marketing fluff | Damir Sokolovsky / `CC-BY-4.0` |
| **14** | `ux-patterns-guide/` | Developer UX patterns: command palettes, tables, forms | SlopGuard Core / `MIT` |

---

### 2.3 The 12 Timeless Design Approaches Catalog

| # | Philosophy | Core Principles | Best Used For | High-Risk Misapplications |
|---|---|---|---|---|
| **1** | **Swiss / International** | Mathematical grids, asymmetrical balance, objective sans-serif | DevTools, API platforms, B2B SaaS | Creative lifestyle, emotive brands |
| **2** | **Minimalist** | Extreme color discipline, content-first, razor-thin borders | Luxury goods, minimalist productivity | Dense data analytics, complex forms |
| **3** | **Editorial / Magazine** | High-contrast serifs, pull quotes, narrative multi-column | Digital publications, media brands, case studies | Dashboard utilities, transactional flows |
| **4** | **Neo-Brutalism** | 2–3px black borders, hard-drop shadows (`4px 4px 0px #000`) | Indie tools, Gen-Z creator apps, Figma/Gumroad | Enterprise healthcare, banking |
| **5** | **Material Design (M3)** | Purposeful surface elevation, tonal containers, round pills | Multi-platform enterprise suites, Android | Ultra-luxury, bespoke fashion |
| **6** | **Skeuomorphic** | Real-world tactile textures, brushed metal, physical lighting | Audio plugins (synths, mixers), simulation | Fast-paced SaaS, mobile checkouts |
| **7** | **Flat Design 2.0** | Geometric planes, low-elevation contact shadows, accessible tint | Business utilities, cloud portals (Stripe, Slack)| Luxury editorial storytelling |
| **8** | **Glassmorphism** | Frosted glass (`backdrop-filter`), multi-depth translucent planes| Spatial computing (visionOS), media players | High-data dashboards (compositor tax) |
| **9** | **Neo-Swiss** | Swiss grids + monospace technical specs, dark/light contrast | AI tools, developer infra (Linear, Vercel) | Mass-market consumer e-commerce |
| **10** | **Luxury / High-End** | Cinematic aspect ratios, black/off-white, generous tracking | High fashion, private banking, luxury real estate| Fast utility tools, high-density forms |
| **11** | **Neumorphism** *(Deprecated)* | Soft paired light/dark drop shadows extruded from background | **Conditional Waiver Only** (Inherently fails WCAG)| **Prohibited on web / general software** |
| **12** | **Motion-Driven** | Scroll-driven kinetic type, WebGL 3D canvases, fluid shaders | Awwwards portfolios, cinematic unveils | Mobile-first utility, low-bandwidth users |

---

### 2.4 Production Component Blueprints & API Contracts

```typescript
// Component Blueprint Contract: PatternSplitHero.tsx
export interface PatternSplitHeroProps {
  eyebrow?: string;
  title: string;
  description: string;
  primaryCta: {
    label: string;
    href: string;
    onClick?: () => Promise<void> | void;
  };
  secondaryCta?: {
    label: string;
    href: string;
  };
  metrics: Array<{
    value: string;
    label: string;
    delta?: string;
    sentiment?: 'positive' | 'neutral' | 'negative';
  }>;
  proofLogos?: Array<{
    src: string;
    alt: string;
    width: number;
    height: number;
  }>;
  mediaSlot: React.ReactNode;
}
```

#### Mandatory 14-State Component Quality Matrix
Every interactive component must implement and visually verify 14 discrete states:
1. `default` — Base resting state.
2. `hover` — Cursor hover with hardware-accelerated transition.
3. `focus-visible` — Dual-ring keyboard indicator.
4. `active / pressed` — Scale/depth feedback (`transform: scale(0.98)`).
5. `loading / mutating` — Debounced spinner/shimmer with pointer-events locked.
6. `disabled` — Semantic `aria-disabled="true"`, readable contrast (3:1 minimum).
7. `read-only` — Presentational without active form inputs.
8. `empty` — Helpful empty state with clear recovery action.
9. `error` — High-contrast alert state with inline error suggestion.
10. `success` — Confirmation state with clear status communication.
11. `partial-loading` — Skeleton placeholders preserving layout dimensions.
12. `permission-denied` — Explanatory state with upgrade/authorization prompt.
13. `long-content / overflow` — Truncation with tooltip or wrapping without container clipping.
14. `RTL (Right-to-Left)` — Directional mirroring using CSS Logical Properties (`margin-inline`, `padding-inline`, `inset-inline-start`).

---

## 3. Scored Anti-Slop Rubric & Verification Protocol

The 7 core axes of anti-slop design map in canonical sequence to testable rules:
**1. Surfaces → 2. Palette → 3. Typography → 4. Spatial Rhythm → 5. Iconography → 6. Integrity → 7. Motion.**

### 3.1 Mathematical Scoring Formula
```
score = max(0, 100 - (blockers * 100) - (majors * 5) - (minors * 1))
```
* **Gate Pass Condition:** `blockers === 0 && score >= 85`. Any single blocker results in an immediate score of `0` and build failure (`Exit 2`).

### 3.2 Anti-Slop Rules Aligned by Axis Order

| Rule ID | Canonical Axis | Defect Description | Severity | Detection | Allowed Exceptions & Remediation |
|---|---|---|---|---|---|
| **SLOP-001** | 1. Surfaces | AI Dark-Mode Blob (Blurred radial gradients in dark UI) | Blocker | `static` | None. Replace with solid token surfaces (`--surface-base`). |
| **SLOP-006** | 2. Palette | Single-Word Italic/Color Text Highlight in Headlines | Minor | `heuristic` | Brand names. Otherwise apply uniform typographic weight. |
| **SLOP-004** | 3. Typography | Screaming Uppercase Eyebrows (>1 tracked all-caps per viewport)| Minor | `runtime-playwright` | Max 1 per screen. Use sentence-case metadata chips. |
| **SLOP-005** | 4. Spatial Rhythm| Cookie-Cutter Identical Grids (3 glowing identical cards) | Major | `heuristic` | True parity matrices (e.g. pricing tiers). Otherwise use bento. |
| **SLOP-002** | 5. Iconography | Raw Emojis as UI Icons (🚀, 🔥, 💡 in buttons/cards) | Blocker | `static` | None. Replace with single-stroke SVG vector icons. |
| **SLOP-003** | 6. Integrity | Vanity Fabricated Stats ("+99.9% Faster" with no telemetry) | Major | `heuristic` | Verified third-party audits or remove the card entirely. |
| **PERF-001** | 7. Motion | Unbounded Compositor Tax (`backdrop-filter` on scrolling tree)| Blocker | `static` | Static overlays only. *(SLOP-007 is a deprecated alias)*. |

---

## 4. Standards-Precise Accessibility Specification (WCAG 2.2 AA / Targeted AAA)

> [!NOTE]
> **Statutory Harmonization Note:** WCAG 2.2 AA is a technical standard that informs statutory compliance under the **US Americans with Disabilities Act (ADA Titles II/III)**, **Section 508**, the **European Accessibility Act (EN 301 549)**, and **Canada's ACA/AODA**.

### 4.1 Target Size: WCAG Standard vs. Mobile Platform Convention
* **WCAG 2.2 AA Minimum (SC 2.5.8 - Target Size Minimum):** Interactive targets must be at least **24×24 CSS px**, or provide sufficient adjacent spacing so a 24px diameter circle centered on the target does not intersect another target.
* **Mobile Platform Convention (Platform/AAA Standard):** Primary mobile actions target **44×44px** to fit the human thumb pad.
* *Enforcement:* Sub-24px = CI **Blocker** (`A11Y-001`); 24–43px = **Warning**; ≥ 44px = **Pass**.

### 4.2 Contrast Ratios (WCAG 1.4.3 / 1.4.11)
* **Normal Body Text:** Minimum **4.5:1** against adjacent background.
* **Large Text (≥ 24px or ≥ 18.5px bold):** Minimum **3:1**.
* **UI Controls & Meaningful Borders:** Minimum **3:1**.
* *Note on ≥ 14:1:* High contrast ratios are brand design decisions, **not** accessibility criteria. Muted text must still meet 4.5:1 (e.g., `#525866` on `#FAF9F6` = 5.6:1).

### 4.3 High Contrast & Windows Forced Colors Mode
`box-shadow` is completely discarded in Windows Forced Colors Mode. Focus systems must use genuine CSS `outline` with explicit forced-colors fallbacks:

```css
:focus-visible {
  outline: 2px solid var(--color-focus, #0047FF);
  outline-offset: 3px;
  box-shadow: 0 0 0 5px var(--surface-base, #FFFFFF);
}

@media (forced-colors: active) {
  :focus-visible {
    outline: 3px solid Highlight;
    outline-offset: 3px;
    box-shadow: none;
  }
}

@media (prefers-contrast: more) {
  :focus-visible {
    outline-width: 3px;
    outline-offset: 4px;
  }
}
```

### 4.4 WCAG 2.2 AA Comprehensive Criterion Coverage Matrix

| WCAG SC | Criterion Name | Level | Test Method | Failure Remediation & Verification Rules |
|---|---|---|---|---|
| **1.4.3** | Contrast (Minimum) | AA | Automated (Axe) + Manual Spot-check | Adjust text or surface token to achieve ≥ 4.5:1. Inspect gradients & hover states manually. |
| **1.4.10**| Reflow (400% Zoom) | AA | Playwright (320px) | Flex-wrap layout; zero horizontal scroll at 320px width. |
| **1.4.12**| Text Spacing | AA | Stylus / Bookmarklet Test | Line-height ≥ 1.5×, spacing below ≥ 2×, letter-spacing ≥ 0.12×, word-spacing ≥ 0.16×. Zero text clipping. |
| **1.4.13**| Content on Hover/Focus | AA | Playwright Interaction | Tooltips/popovers must be dismissible without moving pointer, hoverable, and persistent. |
| **2.4.11**| Focus Not Obscured | AA | Playwright (`elementFromPoint`) | Sticky bottom bars must never cover the actively focused control (`scroll-margin` required). |
| **2.5.7** | Dragging Movements | AA | Manual Walkthrough | Provide single-pointer tap controls alongside drag gestures. |
| **2.5.8** | Target Size (Minimum) | AA | Automated (`A11Y-001`)| Ensure hit area bounding box ≥ 24×24px. |
| **3.2.6** | Consistent Help | AA | Manual Site Audit | Help/support links and chat triggers appear in identical relative order across pages. |
| **3.3.4** | Error Prevention (Legal/Data)| AA | Manual Checkout Audit | Confirmation screen with editable review before irreversible submission. |
| **3.3.7** | Redundant Entry | AA | Manual Form Audit | Multi-step forms must auto-populate previously entered addresses or provide 1-click select. |
| **3.3.8** | Accessible Authentication | AA | Manual Auth Audit | Support 1-click password managers, passkeys, or magic links. Zero transcription puzzles. |
| *Note* | *4.1.1 Parsing* | — | *Deprecated in 2.2* | HTML validity still enforced via linters for general cleanliness. |

### 4.5 Manual Assistive Technology (AT) Smoke Test Script
Before signing off on Gate 5, the reviewer executes this standardized script:
1. **Screen Reader Environment:** 
   * **Windows Targets:** NVDA + Firefox.
   * **macOS / iOS Targets:** VoiceOver + Safari.
   * **Cross-Platform Targets:** Both required per project `browserslist`.
2. **Execution Steps:**
   * Navigate entirely via `Tab`, `Shift+Tab`, and arrow keys with screen curtain active (or monitor turned off / speech-viewer active).
   * Verify all icon buttons announce purpose (e.g., *"Toggle navigation menu, button, collapsed"*).
   * Submit an empty form: Verify focus programmatically jumps to the error summary (`role="alert"`), and each field error is spoken aloud.
   * Open modal/drawer: Verify focus is trapped within container and restored to the trigger button upon `Escape`.

---

## 5. Single-Source-of-Truth Rule Catalog & CLI Operational Contract

### 5.1 Single-Source-of-Truth Rule Catalog with Detection Method

| Rule ID | Severity | Detection | Rule Title & Mandate |
|---|---|---|---|
| **A11Y-001** | Blocker | `static` | Target size strictly < 24×24px (WCAG 2.5.8). |
| **A11Y-002** | Blocker | `static` | Missing accessible name / `aria-label` on interactive element. |
| **A11Y-003** | Blocker | `static` | Insufficient text contrast ratio against computed surface token. |
| **A11Y-004** | Major | `static` | Missing `@media (prefers-reduced-motion)` overrides. |
| **A11Y-005** | Blocker | `runtime-playwright`| Sticky container obscuring focused element (WCAG 2.4.11). |
| **A11Y-006** | Major | `static` | Missing high-contrast outline fallback for forced-colors. |
| **A11Y-007** | Major | `manual-review` | Inconsistent help link positioning across routes (WCAG 3.2.6). |
| **A11Y-008** | Major | `manual-review` | Redundant data entry without pre-fill in multi-step form (WCAG 3.3.7). |
| **TOKEN-001** | Major | `static` | Hardcoded hex/rgb color bypassing design tokens. |
| **TOKEN-002** | Minor | `static` | Non-standard spacing value outside 4px/8px scale. |
| **PERF-001** | Blocker | `static` | Uncontained `backdrop-filter` causing layout thrash *(canonical ID for SLOP-007)*. |
| **PERF-002** | Major | `static` | Raw third-party iframe embed without click-to-load facade. |
| **PERF-003** | Major | `static` | Image missing explicit width/height/aspect-ratio reservation. |
| **SLOP-001** | Blocker | `static` | Banned AI radial gradient background detected. |
| **SLOP-002** | Blocker | `static` | Emoji character used as sole interactive icon. |
| **SLOP-003** | Major | `heuristic` | Fabricated vanity metrics without audited telemetry. |
| **SLOP-004** | Minor | `runtime-playwright`| More than 1 screaming uppercase eyebrow label per viewport (390/768/1440px). |
| **SLOP-005** | Major | `heuristic` | Unjustified identical 3-card grid without tier comparison context. |
| **SLOP-006** | Minor | `heuristic` | Arbitrary single-word italic/color headline accent. |

---

### 5.2 JSON Output Schema & Exit Code Precedence
* **Exit 0**: Clean pass (0 blockers, 0 majors, minors allowed).
* **Exit 1**: Quality Warnings present (`score >= 85`, advisory).
* **Exit 2**: Quality Blockers present (`blockers > 0 || score < 85`, terminates CI check). If `--strict` is passed, Exit 1 is promoted to Exit 2.

```json
{
  "$schema": "https://schema.slopguard.dev/schemas/audit-v1.json",
  "version": "1.6.1",
  "timestamp": "2026-11-22T02:45:00Z",
  "summary": { "blockers": 0, "majors": 1, "minors": 2, "score": 93 },
  "configOverrides": [
    {
      "ruleId": "TOKEN-002",
      "requested": "warn",
      "effective": "warn",
      "rejected": false
    },
    {
      "ruleId": "SLOP-001",
      "requested": "off",
      "effective": "blocker",
      "rejected": true,
      "reason": "Rule is a Blocker; cannot be downgraded in .designrc.json. Requires .design/audit-baseline.json."
    }
  ],
  "results": [
    {
      "ruleId": "TOKEN-001",
      "severity": "major",
      "detection": "static",
      "file": "src/components/HeaderNav.tsx",
      "line": 42,
      "column": 18,
      "message": "Hardcoded hex color '#6366F1' detected. Use semantic token.",
      "remediation": "Replace with: text-[var(--color-brand)]"
    }
  ]
}
```

---

### 5.3 Baseline Waiver Schema (`.design/audit-baseline.json`)
```json
{
  "$schema": "https://schema.slopguard.dev/schemas/baseline-v1.json",
  "waivers": [
    {
      "ruleId": "SLOP-005",
      "file": "src/components/PricingMatrix.tsx",
      "severity": "major",
      "justification": "Pricing tier comparison requires identical visual weights for true tier parity.",
      "approvedBy": "design-system-lead@yourorg.com",
      "approvedAt": "2026-11-22T02:30:00Z",
      "approvalTicket": "https://yourorg.atlassian.net/browse/A11Y-142",
      "expiresAt": "2027-02-20T00:00:00Z"
    }
  ]
}
```

---

### 5.4 Machine-Readable Rule Aliases (`rule-aliases.json`)
```json
{
  "$schema": "https://schema.slopguard.dev/schemas/rule-aliases-v1.json",
  "aliases": [
    {
      "deprecated": "SLOP-007",
      "canonical": "PERF-001",
      "since": "1.6.0",
      "removalPlanned": "2.0.0"
    }
  ]
}
```

---

### 5.5 CLI Operational Contract (`slopguard` / legacy alias: `gemini-uiux`)
* **Package Scope:** `@slopguard/uiux` on npm. Local binary: `slopguard` (legacy alias `gemini-uiux` supported with deprecation notice until v2.0.0).
* **Command Surface:**
  * `slopguard init`: Bootstraps `.design/tokens`, `.design/rules/`, and `.designrc.json`.
  * `slopguard audit [path]`: Executes static & runtime audit. Default: human output. Use `--ci` for JSON + exit codes.
  * `slopguard component list`: Lists production-grade component blueprints.
  * `slopguard component add <Name>`: Injects component into `./src/components/ui/` or `./components/ui/`.
  * `slopguard upgrade`: Migrates `.designrc.json` and tokens to latest schemas with interactive diff.
  * `slopguard version` (`-v`, `--version`): Outputs installed CLI, token, and rules versions (`slopguard@1.6.1 | tokens@1 | rules@1`).
  * `slopguard doctor`: Verifies dependencies, Tailwind configuration, and environment.
* **Flags:**
  * `--dry-run`: Simulates file creation/injection without writing to disk.
  * `--diff`: Displays git-style unified diff before writing component files.
  * `--strict`: Promotes Exit 1 (warnings) to Exit 2 (build failure).
  * `--ci`: Shorthand for `--format=json --exit-code-style=ci --no-color`.
* **Idempotency & Safety:** Injections never overwrite existing components without `--force`.
* **Offline-First Guarantee:** **100% Offline-First.** Zero outbound telemetry calls. No remote phone-home.
* **Severity-Override Logic in `.designrc.json`:**
  ```text
  effectiveSeverity =
    if ruleDefault is "blocker":
      "blocker" (downgrade attempts logged as rejected; requires .design/audit-baseline.json)
    else if configOverride is defined:
      configOverride (valid: "error", "warn", "off")
    else:
      ruleDefault
  ```
* **Configuration Schema (`.designrc.json`):**
  ```json
  {
    "aesthetic": "swiss-modern",
    "tokenOutputs": [
      { "format": "css/variables", "path": "./src/styles/tokens.css" },
      { "format": "tailwind/theme", "path": "./src/styles/tailwind.tokens.ts" },
      { "format": "typescript", "path": "./src/types/tokens.d.ts", "shape": "union" }
    ],
    "componentsDir": "./src/components/ui",
    "rules": {
      "TOKEN-002": "warn",
      "SLOP-004": "warn"
    }
  }
  ```
* **Aesthetic Presets Enum:** `swiss-modern` | `minimalist-dark` | `neo-brutalist` | `editorial-magazine` | `contemporary-neo-swiss` *(Curated starter subset mapping directly to Tier 2 semantic token defaults)*.

---

## 6. Route-Level Performance Budgets, CSP & Security

Performance targets are separated into **Production SLAs (Hard Commitments)** and **Internal Stretch Goals (Optimizations)**.

### 6.1 Route-Specific Performance Budgets

| Route Type | Initial JS Transfer (gzip) | Total Weight at LCP | LCP: SLA / Stretch | INP: SLA / Stretch | CLS: SLA / Stretch |
|---|---|---|---|---|---|
| **Marketing / Landing** | ≤ 25kB | ≤ 450kB | ≤ 2.2s / 1.6s | ≤ 150ms / 80ms | ≤ 0.05 / 0.01 |
| **Case Study / Editorial** | ≤ 20kB | ≤ 650kB | ≤ 2.0s / 1.5s | ≤ 100ms / 50ms | ≤ 0.03 / 0.00 |
| **Product Detail / PDP** | ≤ 50kB | ≤ 850kB | ≤ 2.5s / 1.8s | ≤ 180ms / 100ms| ≤ 0.05 / 0.02 |
| **Checkout / Lead Form** | ≤ 35kB | ≤ 350kB | ≤ 1.8s / 1.2s | ≤ 120ms / 70ms | ≤ 0.02 / 0.00 |

* **Asset Budget Footnote:** Weight is measured as compressed network transfer size at initial `load`, including critical responsive images (`.avif`/WebP) and self-hosted fonts.
* **CLS ≤ 0.00 Font Strategy:** To achieve CLS ≤ 0.00 without layout shift, projects must either:
  1. Use `font-display: optional` (zero layout shift; browser uses cached font or falls back cleanly), **or**
  2. Implement size-adjusted fallback metrics in `@font-face` (`size-adjust`, `ascent-override`, `descent-override`).
* **Lab CWV Proxy for New Routes (< 28 days without CrUX data):** New routes must achieve Lighthouse Mobile CI composite score ≥ 90 on a simulated 4G profile before production release.

---

### 6.2 Hardened Content Security Policy (CSP) Templates

#### Strict Template (Production Recommended)
```http
Reporting-Endpoints: csp-endpoint="/api/csp-report"
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-{RANDOM}';
  style-src 'self' 'nonce-{RANDOM}';
  img-src 'self' data: https:;
  font-src 'self';
  frame-src 'self' https://cal.com https://www.youtube-nocookie.com;
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';
  form-action 'self' https://your-form-endpoint.example;
  upgrade-insecure-requests;
  report-to csp-endpoint;
  report-uri /api/csp-report;
```

#### Compat Template (For Legacy Build Toolchains & Static Hosts)
```http
/* WAIVER REQUIRED: Use only when static host does not support per-request nonces */
Reporting-Endpoints: csp-endpoint="/api/csp-report"
Content-Security-Policy: 
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  frame-src 'self' https://cal.com https://www.youtube-nocookie.com;
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';
  form-action 'self' https://your-form-endpoint.example;
  upgrade-insecure-requests;
  report-to csp-endpoint;
  report-uri /api/csp-report;
```

---

### 6.3 Layered Bot & Spam Defense + No-JS Fallback
1. **Hidden Honeypot Field:** Off-screen input (`tabindex="-1"`) that bots fill automatically.
2. **Cryptographic Time-Trap:** Submissions occurring < 2.5 seconds from initial HTML render are rejected.
3. **Behavioral Sliding Token:** Cloudflare Turnstile invoked conditionally only when the risk score exceeds threshold. Governed under separate third-party DPA.
4. **Edge Rate Limiting:** Sliding window tied to `IP + User-Agent Fingerprint` (maximum 10 requests per 10 minutes).
5. **No-JS Semantic Fallback:** Standard `<form action="https://your-form-endpoint.example" method="POST">` with standard HTTP 303 redirects ensures 100% submission reliability without client scripts.

---

## 7. Operational Standards & Browser Support

### 7.1 Browser Support Matrix
All components and tokens are continuously targeted and validated against:
* **Desktop:** Chrome (last 2 versions), Edge (last 2 versions), Firefox (last 2 versions), Safari (last 2 versions).
* **Mobile:** iOS Safari (iOS 16+), Android Chrome (last 2 versions).
* **Accessibility Engines:** 
  * Windows Forced Colors Mode: Chromium (Edge/Chrome) **and** Firefox (v89+).
  * macOS & iOS: Increase Contrast, Smart Invert, and `prefers-contrast: more`.

### 7.2 Telemetry Privacy Policy
First-party analytics telemetry (Gate 10) operates strictly under these privacy constraints:
* **Zero PII Storage:** Names, emails, phone numbers, and full IP addresses are permanently stripped before dispatch.
* **Allowed Parameters:** `cta_name`, `source_section`, `scroll_depth_tier`, `duration_ms`, `error_type`.
* **Consent Gating:** Telemetry dispatches only after consent is granted via the cookie consent layer.
* *Sub-processor note:* Conditional CAPTCHA verification (Turnstile) is strictly segregated from analytics telemetry and governed under separate data processing agreements.

---

## 8. The 10-Gate Definition of Done (Production Release Criteria)

Every feature branch or component release must satisfy all 10 gates prior to production deployment:

1. [ ] **Token Compliance:** 100% of colors, spacing, borders, and typography mapped to Tier 2/3 tokens. Zero raw hex codes (`TOKEN-001`).
2. [ ] **Scored Slop Scorecard:** 0 Blockers; Weighted Anti-Slop Score ≥ 85/100.
3. [ ] **Target Size Verification:** 100% of targets ≥ 24px (WCAG AA); mobile primary actions ≥ 44px.
4. [ ] **Complete 14-State Matrix:** Component verified across all 14 discrete states (including focus, error, loading, RTL).
5. [ ] **Assistive Technology Walkthrough:** Audio smoke test passed using NVDA and/or VoiceOver following Section 4.5 script.
6. [ ] **High Contrast / Forced Colors:** Dual-ring focus verified with Windows Forced Colors Mode active in Edge and Firefox.
7. [ ] **Performance SLA Sign-Off:** Route bundle size within allocated limits; Core Web Vitals satisfy Section 6.1 SLAs (or Lighthouse ≥ 90 lab proxy for new routes).
8. [ ] **Layered Bot & CSP Defense:** Honeypot + time-trap + edge defense active; CSP headers validated; No-JS fallback verified.
9. [ ] **Reflow & Motion Isolation:** Layout verified at 400% zoom (320px viewport); zero motion when `prefers-reduced-motion` is active.
10. [ ] **Telemetry & Privacy Verification:** Events fire with sanitized zero-PII payloads and adhere to user consent state.

---

## 9. Pilot Instrumentation & Metric Tracking

During pilot deployment, track velocity and quality against these 5 benchmark metrics:

| Metric Indicator | Pre-Adoption Baseline | Post-Adoption Pilot Target | Expected Impact Delta |
|---|---|---|---|
| **Design-Review Cycle Time** | 4.2 days | ≤ 1.5 days | −64% latency |
| **Post-Release A11y Defects** | 14 defects / sprint | ≤ 1 defect / sprint | −92% defect rate |
| **CWV Mobile SLA Pass Rate** | 68% passing routes | ≥ 98% passing routes | +30% field compliance |
| **Token Adherence Ratio** | 71% token mapping | ≥ 99% token mapping | +28% visual consistency |
| **Rework Rate Post-Redline** | 28% rejected PRs | ≤ 5% rejected PRs | −82% wasted rework |
