#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Legal, Privacy & Compliance Hub Page sections and archetypes to
section-archetypes.json and rebuild section-archetypes.csv.
"""

from dataset_utils import upsert_sections

LEGAL_SECTIONS = [
    {
        "section_id": "legal_doc",
        "section_name": "Structured Legal & Compliance Documentation",
        "archetypes": [
            {
                "archetype_id": "leg-01",
                "name": "Sticky Table of Contents & Prose Split",
                "keywords": "legal, privacy-policy, terms-of-service, toc, gdpr, compliance",
                "best_for": "Audit-grade Privacy Policies, Terms of Service, and Security Docs requiring scannable long-form legibility.",
                "selection_triggers": {"has_toc": True, "style": "editorial/legal"},
                "layout_structure": "2-column container (grid-cols-1 lg:grid-cols-12 gap-10 max-w-6xl mx-auto py-16). Left (3 cols): Sticky scroll-spy Table of Contents tracking active anchor sections. Right (9 cols): Prose container constrained to max-w-prose (65ch) with generous vertical spacing.",
                "typography_specs": "H1: text-3xl sm:text-4xl font-bold tracking-tight. Section H2: text-xl font-semibold mt-10 mb-3. Body: text-base leading-relaxed (1.65) text-[var(--text-secondary)].",
                "key_components": "Sticky TOC nav with active anchor highlight, effective date stamp, plain-English callout boxes, anchored section headings.",
                "responsive_behavior": "Sticky sidebar collapses into a collapsible 'Jump to section' select/accordion above content on mobile.",
                "accessibility": "Landmark <nav aria-label='Table of contents'> with aria-current='location' on active section and scroll-margin-top for sticky headers.",
                "anti_slop_rules": "Never render unstyled 10,000-word walls of tiny gray text; enforce >= 4.5:1 contrast and 65ch max measure."
            },
            {
                "archetype_id": "leg-02",
                "name": "Tabbed Policy Multi-Doc Hub",
                "keywords": "policy-hub, terms, privacy, dpa, subprocessors, acceptable-use",
                "best_for": "SaaS and enterprise platforms hosting Terms, Privacy Policy, Sub-processors List, AUP, and DPA in one hub.",
                "selection_triggers": {"multi_policy": True},
                "layout_structure": "Top segmented tab navigation switching cleanly across Terms of Service, Privacy Policy, Sub-processors, Acceptable Use, and DPA, paired with structured tables for sub-processors and retention schedules.",
                "typography_specs": "Tab button: text-sm font-semibold min-h-[44px]. Table metadata: text-xs font-mono.",
                "key_components": "Accessible policy tabs, sub-processor table (Vendor, Purpose, Region), contact DPO card.",
                "responsive_behavior": "Horizontal snap-scroll tab bar on mobile; sub-processor table wraps in horizontal scroll region.",
                "accessibility": "role='tablist', role='tab', aria-selected, keyboard ArrowLeft/ArrowRight navigation, proper <table> headers.",
                "anti_slop_rules": "Keep every policy URL deep-linkable via hash or query param so procurement teams can bookmark specific agreements."
            },
            {
                "archetype_id": "leg-03",
                "name": "Versioned Compliance Header with PDF Download",
                "keywords": "versioned-legal, pdf-download, changelog, plain-english-summary",
                "best_for": "Regulated enterprise vendors maintaining version history, diff summaries, and downloadable signed PDFs.",
                "selection_triggers": {"has_version_selector": True},
                "layout_structure": "Top compliance utility bar (max-w-5xl mx-auto py-8 border-b border-[var(--border-subtle)]) with Last Updated timestamp, version selector dropdown (v2.4 Active / v2.3 Archived), Plain-English Summary toggle, and PDF download action.",
                "typography_specs": "Version badge: text-xs font-mono font-semibold. Summary text: text-sm leading-relaxed.",
                "key_components": "Version selector <select> with explicit <label>, plain-English summary panel, accessible PDF download link with file size.",
                "responsive_behavior": "Utility controls wrap cleanly into a 2-row stack on mobile with >= 44px tap heights.",
                "accessibility": "Download link announces file format and size; summary toggle uses aria-expanded and aria-controls.",
                "anti_slop_rules": "Clearly distinguish archived versions with a high-contrast banner so users do not mistake superseded terms for current terms."
            }
        ]
    }
]


if __name__ == "__main__":
    upsert_sections(LEGAL_SECTIONS)
