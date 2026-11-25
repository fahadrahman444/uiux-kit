#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Pricing Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 5 dedicated sections:
1. pricing_hero (3 archetypes)
2. pricing_comparison_matrix (3 archetypes)
3. pricing_addons (2 archetypes)
4. pricing_enterprise_sla (2 archetypes)
5. pricing_guarantee_bar (2 archetypes)
Total: 12 new archetypes.
Combined dataset will have: 20 sections, 118 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

PRICING_SECTIONS = [
    {
        "section_id": "pricing_hero",
        "section_name": "Pricing Hero & Frequency Switch",
        "archetypes": [
            {
                "archetype_id": "phero-01",
                "name": "Centered Toggle Hero with Trial Chip",
                "keywords": "pricing-hero, billing-switch, annual-discount, trial-chip, centered",
                "best_for": "SaaS products offering self-serve monthly and annual plans with a discount incentive.",
                "selection_triggers": {"has_billing_toggle": True, "self_serve": True},
                "layout_structure": "Centered max-w-4xl mx-auto py-20 text-center flex flex-col items-center. Category eyebrow chip, punchy H1, subtitle, followed by an accessible segmented control pill toggle (Monthly / Annual [Save 20%]).",
                "typography_specs": "H1: text-5xl sm:text-6xl font-extrabold tracking-tight. Pill text: text-sm font-semibold. Discount badge: text-xs font-mono font-bold text-emerald-600 bg-emerald-500/10 px-2 py-0.5 rounded-full.",
                "key_components": "Category chip, massive H1, subhead, segmented pill button toggle with active sliding indicator, 14-day trial badge.",
                "responsive_behavior": "Stays centered; pill toggle remains full-width or auto-centered with 44px min tap target.",
                "accessibility": "Segmented switch uses role='radiogroup' or aria-pressed='true' on the selected billing interval.",
                "anti_slop_rules": "No shouting fake urgency timers ('Offer ends in 3 mins!'); keep discount pill tasteful and quiet."
            },
            {
                "archetype_id": "phero-02",
                "name": "Split Value-Proof Hero with ROI Calculator Trigger",
                "keywords": "split-hero, roi-anchor, value-proposition, calculator, b2b",
                "best_for": "B2B and enterprise solutions where price requires immediate ROI justification and payback-period evidence.",
                "selection_triggers": {"tier": "b2b", "has_roi": True},
                "layout_structure": "2-column split (grid-cols-1 lg:grid-cols-12 gap-12 items-center py-20). Left (7 cols): High-impact value proposition, guaranteed ROI statement. Right (5 cols): Compact interactive payback estimator widget.",
                "typography_specs": "H1: text-4xl sm:text-5xl font-bold tracking-tight. Metric callouts: text-3xl font-mono font-extrabold text-[var(--primary)].",
                "key_components": "Value headline, 3-bullet ROI guarantee list, interactive slider widget estimating monthly hours/dollars saved.",
                "responsive_behavior": "Stacks vertically on mobile with headline on top and calculator card below.",
                "accessibility": "Slider input has aria-label='Team size slider' with aria-valuemin, aria-valuemax, aria-valuenow.",
                "anti_slop_rules": "ROI estimates must state standard methodology assumptions; no arbitrary 10,000% claims."
            },
            {
                "archetype_id": "phero-03",
                "name": "Usage-Based Seat Estimator Hero",
                "keywords": "usage-based, seat-calculator, consumption, developer-tool, slider",
                "best_for": "Developer infrastructure, API platforms, and usage-based products where pricing scales with volume or seats.",
                "selection_triggers": {"pricing_model": "usage_based"},
                "layout_structure": "Single column max-w-3xl mx-auto text-center py-16. Interactive logarithmic scale slider directly under the headline dynamically updating tier recommendation in real time.",
                "typography_specs": "Slider readout: text-4xl font-mono font-bold text-[var(--text-primary)]. Sub-label: text-xs uppercase tracking-wider text-[var(--text-muted)].",
                "key_components": "Logarithmic range input, current value badge, recommended tier indicator, dynamic price preview.",
                "responsive_behavior": "Full width slider track with oversized 28px draggable thumb for touch friendliness.",
                "accessibility": "Keyboard arrow keys increment/decrement slider; aria-valuetext announces estimated tier.",
                "anti_slop_rules": "No jumping layout heights during value scrub; fixed dimension value container."
            }
        ]
    },
    {
        "section_id": "pricing_comparison_matrix",
        "section_name": "Granular Feature Comparison Matrix",
        "archetypes": [
            {
                "archetype_id": "pmat-01",
                "name": "Sticky Header Grouped Category Matrix",
                "keywords": "comparison-matrix, sticky-header, enterprise-features, grouped-table, feature-breakdown",
                "best_for": "Products with 20+ features categorized across Core, Security, Integrations, and Support tiers.",
                "selection_triggers": {"feature_count": "20+", "has_matrix": True, "style": "enterprise"},
                "layout_structure": "Full-width table with sticky top row containing plan names and mini-CTAs on window scroll. Rows grouped by category headers (collapsible). Cells display checkmarks, dashes, or specific numeric limits.",
                "typography_specs": "Category headers: text-xs font-mono uppercase tracking-wider text-[var(--text-muted)]. Feature names: text-sm font-medium text-[var(--text-primary)]. Tier headers: text-base font-bold.",
                "key_components": "Sticky thead, info tooltip triggers on technical terms, category accordion headers, SVG check / minus icons, plan CTA buttons.",
                "responsive_behavior": "Horizontal swipe container on mobile with sticky first column (feature name) and scroll indicators.",
                "accessibility": "th scope='col' on plan names, th scope='row' on feature names, tooltips accessible via keyboard focus and Esc to close.",
                "anti_slop_rules": "Do not use low-contrast grey checks against light backgrounds; use high-contrast primary or emerald checkmarks."
            },
            {
                "archetype_id": "pmat-02",
                "name": "Tabbed Category Feature Matrix",
                "keywords": "tabbed-matrix, category-tabs, modular-table, clean-comparison",
                "best_for": "SaaS platforms wanting to prevent 100-row endless scroll fatigue by partitioning features into switchable tabs.",
                "selection_triggers": {"feature_count": "30+", "prefer_tabs": True},
                "layout_structure": "Centered max-w-6xl mx-auto py-16. Top tab bar ('Platform Core', 'Security & Compliance', 'Analytics', 'APIs & Developer'). Selecting a tab swaps the active 8-12 row comparison table with zero page jump.",
                "typography_specs": "Tab labels: text-sm font-semibold. Table headers: text-base font-bold. Row cells: text-sm.",
                "key_components": "Segmented tab control, animated tab indicator, clean 4-column matrix, feature description tooltips.",
                "responsive_behavior": "Tabs convert to horizontal scroll list on mobile with snap-x scrolling.",
                "accessibility": "role='tablist' with role='tab' and aria-selected state; keyboard ArrowLeft / ArrowRight navigation.",
                "anti_slop_rules": "Tab transitions must use opacity only (duration-150); never use bouncy layout-shifting animations."
            },
            {
                "archetype_id": "pmat-03",
                "name": "Differentiator-Only Delta Table",
                "keywords": "delta-table, differences-only, minimalist, quick-decision, concise",
                "best_for": "High-velocity sales where prospects just want to know 'what do I get if I pay for Pro instead of Starter?'",
                "selection_triggers": {"matrix_style": "minimal_diff"},
                "layout_structure": "Compact table showing only the 8-10 features that differ between tiers, with a toggle button: 'Show all 45 features'.",
                "typography_specs": "Header: text-lg font-bold. Delta rows: text-sm font-medium. Toggle button: text-xs font-mono underline.",
                "key_components": "'Show differences only' switch, clean delta rows, expandable drawer for complete baseline specs.",
                "responsive_behavior": "Clean 3-column card comparison on mobile without horizontal scrolling.",
                "accessibility": "Expand button has aria-expanded='false' and aria-controls='full-feature-table'.",
                "anti_slop_rules": "Clearly state that baseline features are included in higher tiers so users are not confused."
            }
        ]
    },
    {
        "section_id": "pricing_addons",
        "section_name": "Modular Add-ons & Expansion",
        "archetypes": [
            {
                "archetype_id": "padd-01",
                "name": "2-Column Selectable Add-on Card Grid",
                "keywords": "addons, modular-pricing, optional-features, expansion, extras",
                "best_for": "Products with specialized upgrades (Dedicated IP, Custom Onboarding, SOC2 Report, Extra Storage).",
                "selection_triggers": {"has_addons": True, "addon_count": "3-6"},
                "layout_structure": "2-column grid (grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto py-12). Each card features checkbox/switch, addon title, description, and '+ $X/mo' badge.",
                "typography_specs": "Addon title: text-base font-semibold. Price tag: text-sm font-mono font-bold text-[var(--primary)]. Description: text-xs text-[var(--text-secondary)].",
                "key_components": "Custom accessible checkbox, price badge, title, 2-line explanation, optional tooltip.",
                "responsive_behavior": "Single column stack on mobile with full-width tap target cards.",
                "accessibility": "role='checkbox' with aria-checked, keyboard Space to toggle, card click delegates to input.",
                "anti_slop_rules": "No pre-checking optional add-ons as sneaky dark patterns; all add-ons default to unchecked."
            },
            {
                "archetype_id": "padd-02",
                "name": "Horizontal Add-on Strip with Live Cart Subtotal",
                "keywords": "horizontal-addons, inline-addons, subtotal-preview, cart-integration",
                "best_for": "E-commerce or developer API tools with quick one-click provision extras.",
                "selection_triggers": {"has_addons": True, "style": "compact"},
                "layout_structure": "Stacked horizontal strip rows separated by 1px borders. Left: Icon + title. Center: pricing metric. Right: '+ Add' button that changes to checked state.",
                "typography_specs": "Title: text-sm font-medium. Price: text-sm font-mono. Button: text-xs font-semibold px-3 py-1.5.",
                "key_components": "Icon, descriptor, unit price, actionable stateful toggle button, bottom sticky subtotal readout.",
                "responsive_behavior": "Wraps price and button cleanly on mobile without line truncation.",
                "accessibility": "Buttons have clear aria-label='Add Dedicated Support to subscription for $150 per month'.",
                "anti_slop_rules": "Explicit price per billing cycle; never hide whether addon is monthly or annual."
            }
        ]
    },
    {
        "section_id": "pricing_enterprise_sla",
        "section_name": "Enterprise SLA & Procurement Hub",
        "archetypes": [
            {
                "archetype_id": "psla-01",
                "name": "Full-Width High-Trust Procurement Card",
                "keywords": "enterprise-procurement, sla, security-badges, custom-contract, talk-to-sales",
                "best_for": "Enterprise procurement teams requiring SOC2, HIPAA, custom MSAs, 99.99% uptime, and vendor diligence.",
                "selection_triggers": {"has_enterprise": True, "compliance": True},
                "layout_structure": "Full-width elevated card (max-w-6xl mx-auto py-12 px-8 sm:px-12 rounded-3xl bg-[var(--surface-raised)] border border-[var(--border-subtle)]). Left 2/3: Enterprise capability matrix (SAML SSO, SCIM, Dedicated CSM, Custom Legal MSA). Right 1/3: 'Contact Enterprise Sales' primary action card with guaranteed response time.",
                "typography_specs": "Eyebrow: text-xs font-mono uppercase tracking-widest text-[var(--primary)]. Title: text-2xl sm:text-3xl font-bold. Checklist: text-sm font-medium.",
                "key_components": "Security certification badges (SOC2, HIPAA, ISO27001, GDPR), 4-item compliance checklist, 'Talk to Enterprise Sales' CTA button, response time guarantee chip ('< 2 hr response').",
                "responsive_behavior": "Stacks into single column on mobile with CTA pinned below the checklist.",
                "accessibility": "Semantic list <ul> with SVG checkmarks having aria-hidden='true', CTA button has descriptive focus ring.",
                "anti_slop_rules": "No generic 'Enterprise-grade' marketing buzzwords without citing actual verified protocols (e.g. specify SAML 2.0 / Okta / Azure AD)."
            },
            {
                "archetype_id": "psla-02",
                "name": "Split RFQ Direct Procurement Form",
                "keywords": "rfq, enterprise-quote, custom-pricing, inquiry-form, b2b-sales",
                "best_for": "Companies with high contract values ($20k+/yr) where instant quoting is replaced with custom scoping.",
                "selection_triggers": {"has_enterprise": True, "direct_form": True},
                "layout_structure": "2-column container. Left: Executive trust bullets and customer logos. Right: 4-field enterprise qualification form (Work email, Company size, Deployment timeline, Primary requirement).",
                "typography_specs": "Form labels: text-xs font-medium text-[var(--text-secondary)]. Form inputs: text-sm py-2.5 px-3.5.",
                "key_components": "Work email validator, company size dropdown, timeline selector, single submit button with loading state.",
                "responsive_behavior": "Full width form fields on mobile; labels remain top-aligned.",
                "accessibility": "Inputs paired with explicit <label for='...'> tags, aria-required='true', aria-invalid error state messaging.",
                "anti_slop_rules": "Never ask for phone numbers on step 1 unless strictly necessary; keep form friction low (max 4 fields)."
            }
        ]
    },
    {
        "section_id": "pricing_guarantee_bar",
        "section_name": "Trust, Security & Risk Reversal Banner",
        "archetypes": [
            {
                "archetype_id": "pbar-01",
                "name": "3-Badge Security & Money-Back Strip",
                "keywords": "money-back-guarantee, risk-reversal, secure-checkout, pci-dss, trust-badges",
                "best_for": "Overcoming final purchase anxiety before checkout across both consumer and B2B SaaS.",
                "selection_triggers": {"has_guarantee": True},
                "layout_structure": "Full-width subtle container py-8 border-y border-[var(--border-subtle)] bg-[var(--surface-subtle)]. 3-column layout (grid-cols-1 md:grid-cols-3 gap-6 text-center).",
                "typography_specs": "Badge title: text-sm font-bold text-[var(--text-primary)]. Sub-text: text-xs text-[var(--text-secondary)].",
                "key_components": "Shield SVG icon (30-day money-back guarantee), Lock SVG icon (256-bit SSL encrypted checkout), Refresh SVG icon (Cancel or downgrade anytime with 1 click).",
                "responsive_behavior": "Stacks into 3 centered items on mobile with 16px vertical gap.",
                "accessibility": "Semantic section with aria-label='Security and Guarantee Commitments'.",
                "anti_slop_rules": "No fake green padlock clipart or unverified security badges; clean monochromatic outline SVG icons only."
            },
            {
                "archetype_id": "pbar-02",
                "name": "Floating Sticky Mobile Checkout Drawer",
                "keywords": "mobile-cart, sticky-checkout, selected-plan, mobile-sticky, drawer",
                "best_for": "Mobile optimization for complex pricing pages where user scrolls far past the pricing cards.",
                "selection_triggers": {"mobile_optimized": True},
                "layout_structure": "Fixed bottom bar on mobile (sm:hidden) z-40 bg-[var(--surface)]/95 backdrop-blur-lg border-t border-[var(--border-subtle)] px-4 py-3 flex items-center justify-between shadow-2xl.",
                "typography_specs": "Selected plan: text-xs font-semibold. Price: text-base font-bold text-[var(--text-primary)]. Button: text-sm font-semibold.",
                "key_components": "Plan name summary, price/billing interval text, compact 'Choose Plan' CTA button.",
                "responsive_behavior": "Hidden on desktop (sm:hidden), visible and fixed to viewport bottom on mobile.",
                "accessibility": "Doesn't block content navigation; dismissible or scrolls quietly into view after passing tier section.",
                "anti_slop_rules": "Do not cover more than 68px of screen height; respect bottom safe-area-inset."
            }
        ]
    }
]


def rebuild():
    json_path = DATA_DIR / "section-archetypes.json"
    csv_path = DATA_DIR / "section-archetypes.csv"

    with open(json_path, "r", encoding="utf-8") as f:
        existing_sections = json.load(f)

    existing_ids = {s["section_id"] for s in existing_sections}
    
    # Append or update
    added_count = 0
    for new_sec in PRICING_SECTIONS:
        if new_sec["section_id"] not in existing_ids:
            existing_sections.append(new_sec)
            added_count += len(new_sec["archetypes"])
            print(f"  + Added section: {new_sec['section_id']} ({len(new_sec['archetypes'])} archetypes)")
        else:
            print(f"  * Section {new_sec['section_id']} already exists, skipping duplicate")

    total_sections = len(existing_sections)
    total_archetypes = sum(len(s["archetypes"]) for s in existing_sections)

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing_sections, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON updated: {total_sections} sections, {total_archetypes} archetypes")

    # Rebuild CSV
    fieldnames = [
        "Section ID", "Section Name", "Archetype ID", "Archetype Name",
        "Keywords", "Best For", "Selection Triggers", "Layout Structure",
        "Typography Specs", "Key Components", "Responsive Behavior",
        "Accessibility", "Anti-Slop Rules"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sec in existing_sections:
            for arch in sec["archetypes"]:
                writer.writerow({
                    "Section ID": sec["section_id"],
                    "Section Name": sec["section_name"],
                    "Archetype ID": arch["archetype_id"],
                    "Archetype Name": arch["name"],
                    "Keywords": arch["keywords"],
                    "Best For": arch["best_for"],
                    "Selection Triggers": json.dumps(arch["selection_triggers"]),
                    "Layout Structure": arch["layout_structure"],
                    "Typography Specs": arch["typography_specs"],
                    "Key Components": arch["key_components"],
                    "Responsive Behavior": arch["responsive_behavior"],
                    "Accessibility": arch["accessibility"],
                    "Anti-Slop Rules": arch["anti_slop_rules"],
                })

    print(f"[OK] CSV updated: {total_archetypes} rows written to {csv_path}")


if __name__ == "__main__":
    rebuild()
