#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Contact & Sales Intake Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 3 dedicated sections:
1. contact_intake_form (3 archetypes)
2. contact_location_map (2 archetypes)
3. contact_sla_banner (2 archetypes)
Total: 7 new archetypes.
Combined dataset will have: 31 sections, 147 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CONTACT_SECTIONS = [
    {
        "section_id": "contact_intake_form",
        "section_name": "Lead Qualification & Intake Form",
        "archetypes": [
            {
                "archetype_id": "cform-01",
                "name": "Split 2-Column High-Trust Intake",
                "keywords": "contact-form, sales-inquiry, lead-qualification, split-contact, talk-to-sales",
                "best_for": "B2B SaaS, enterprise consulting, and agencies seeking high conversion with minimal form friction.",
                "selection_triggers": {"form_style": "split_trust", "tier": "b2b"},
                "layout_structure": "2-column container (grid-cols-1 lg:grid-cols-12 gap-12 max-w-6xl mx-auto py-16 items-start). Left (5 cols): Trust column ('What happens when you reach out', response time badge, enterprise client logo strip, VIP customer testimonial quote). Right (7 cols): Clean 5-field card form (Work Email, Full Name, Company Size dropdown, Project Scope, Submit button with micro-guarantee).",
                "typography_specs": "Eyebrow: text-xs font-mono uppercase tracking-widest text-[var(--primary)]. H1: text-3xl sm:text-4xl font-extrabold text-[var(--text-primary)]. Form labels: text-xs font-semibold text-[var(--text-secondary)]. Inputs: text-sm py-2.5 px-3.5.",
                "key_components": "Structured form card, work email domain validator, company size selector, trust bullets, response SLA badge ('We reply in < 2 hours'), submit button with loading spinner.",
                "responsive_behavior": "Stacks vertically on mobile with headline and trust metrics above form card.",
                "accessibility": "Inputs use explicit <label for='...'> tags, aria-required='true', aria-describedby for errors, focus-visible outline with 2px offset.",
                "anti_slop_rules": "STRICT: Maximum 5 fields; never ask for phone numbers on step 1 unless strictly requested. Zero generic captcha walls."
            },
            {
                "archetype_id": "cform-02",
                "name": "Multi-Step Progressive Disclosure Wizard",
                "keywords": "multi-step-form, progressive-disclosure, wizard, scope-selector, interactive-intake",
                "best_for": "High-ticket services ($15k+) where qualified scoping is required before an executive consultation.",
                "selection_triggers": {"multi_step": True, "high_ticket": True},
                "layout_structure": "Centered max-w-2xl mx-auto py-16. Top progress bar (Step 1: Your Goals -> Step 2: Timeline & Budget -> Step 3: Contact Details). Each step reveals 3-4 interactive pill buttons rather than text inputs.",
                "typography_specs": "Step indicator: text-xs font-mono uppercase tracking-wider text-[var(--text-muted)]. Step question: text-2xl font-bold text-[var(--text-primary)]. Option pill: text-sm font-medium.",
                "key_components": "Progress step bar, selectable option pills with check indicators, animated slide/fade step transition (opacity duration-150), Back and Next buttons.",
                "responsive_behavior": "Full width pills on mobile with 48px tap targets.",
                "accessibility": "role='form' with aria-live='polite' step announcements for screen readers; keyboard Arrow key navigation between options.",
                "anti_slop_rules": "Never animate with jarring layout height jumps; step transitions use opacity only with fixed min-height container."
            },
            {
                "archetype_id": "cform-03",
                "name": "Direct Embedded Meeting Scheduler",
                "keywords": "calendar-scheduler, cal-com, calendly-embed, direct-booking, instant-meeting",
                "best_for": "Founder-led agencies and agile teams where booking a direct 30-min discovery call is the fastest path to closing.",
                "selection_triggers": {"direct_calendar": True},
                "layout_structure": "2-column split. Left: Host profile (portrait photo, executive bio, meeting agenda, 'What to prepare'). Right: Embedded Cal.com / Calendly calendar widget with time zone detection and available slot picker.",
                "typography_specs": "Host name: text-lg font-bold. Meeting title: text-xl font-bold. Agenda items: text-sm leading-relaxed.",
                "key_components": "Host avatar (aspect-square rounded-2xl), agenda bullet list, responsive iframe container, direct calendar link fallback button.",
                "responsive_behavior": "Stacks on mobile with host details above the calendar embed.",
                "accessibility": "Iframe has descriptive title='Select a date and time for a 30-minute discovery consultation'; full keyboard trap avoidance.",
                "anti_slop_rules": "Must include a direct external booking link below the embed in case user ad-blockers block third-party iframes."
            }
        ]
    },
    {
        "section_id": "contact_location_map",
        "section_name": "Global Office Hubs & Regional Routing",
        "archetypes": [
            {
                "archetype_id": "cmap-01",
                "name": "Multi-City Interactive Location Cards",
                "keywords": "office-locations, global-hubs, multi-city, regional-offices, headquarters",
                "best_for": "Companies with physical offices in multiple major metropolitan markets (e.g. SF, NYC, London, Tokyo).",
                "selection_triggers": {"has_multiple_offices": True, "style": "clean"},
                "layout_structure": "3 or 4-column card grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 max-w-6xl mx-auto py-12). Each card features city photography thumbnail, local address, local time clock, and Google Maps directions link.",
                "typography_specs": "City name: text-lg font-bold text-[var(--text-primary)]. Local time: text-xs font-mono text-[var(--primary)]. Address: text-xs leading-relaxed text-[var(--text-secondary)].",
                "key_components": "City photo (rounded-xl object-cover), local time indicator, physical address, direct email link, external map pin icon.",
                "responsive_behavior": "1 column on mobile, 2 columns on tablet, 3-4 columns desktop.",
                "accessibility": "Cards use semantic <article> with clear H3 city names; external map links include aria-label.",
                "anti_slop_rules": "Use authentic city studio photos or clean architectural crops; no generic flag emojis."
            },
            {
                "archetype_id": "cmap-02",
                "name": "Global Stylized Vector Map with Office Pins",
                "keywords": "vector-world-map, global-presence, regional-routing, map-pins",
                "best_for": "Global enterprise platforms and multinational consultancies highlighting international coverage.",
                "selection_triggers": {"has_multiple_offices": True, "map_view": True},
                "layout_structure": "Full-width dark container featuring high-contrast monochrome SVG world map. Interactive glowing pins over active regions. Clicking a pin reveals office contact details.",
                "typography_specs": "Region title: text-sm font-bold. Pin popover text: text-xs font-mono.",
                "key_components": "Monochrome SVG world map, pulse SVG pin markers, interactive popover cards, fallback accessible text list.",
                "responsive_behavior": "Map scrolls horizontally on mobile or displays a stacked city directory list underneath.",
                "accessibility": "Visual map paired with accessible HTML directory list for screen readers.",
                "anti_slop_rules": "Crisp vector SVG map with zero blurry raster image backgrounds."
            }
        ]
    },
    {
        "section_id": "contact_sla_banner",
        "section_name": "Guaranteed Response Time & Direct Channels",
        "archetypes": [
            {
                "archetype_id": "csla-01",
                "name": "3-Pillar Response & Support Commitment Strip",
                "keywords": "response-sla, support-guarantee, direct-channels, response-time, trust-strip",
                "best_for": "Setting clear communication expectations and eliminating the fear that inquiries go into an unanswered black hole.",
                "selection_triggers": {"has_sla": True},
                "layout_structure": "Full-width subtle strip py-8 border-y border-[var(--border-subtle)] bg-[var(--surface-subtle)]. 3-column layout (grid-cols-1 md:grid-cols-3 gap-6 text-center).",
                "typography_specs": "Commitment title: text-sm font-bold text-[var(--text-primary)]. Description: text-xs text-[var(--text-secondary)].",
                "key_components": "Clock SVG icon ('< 2-Hour Response Time'), Shield SVG icon ('Strict NDA & Security Privacy'), Chat SVG icon ('Direct Slack Channel for Enterprise').",
                "responsive_behavior": "Stacks vertically on mobile with 16px gap.",
                "accessibility": "Semantic <section> with aria-label='Our Communication Commitments'.",
                "anti_slop_rules": "Keep commitments realistic; specify business hours if 24/7 coverage is not actually supported."
            },
            {
                "archetype_id": "csla-02",
                "name": "Dual-Track Sales vs Support Routing Banner",
                "keywords": "sales-vs-support, routing-banner, customer-portal, help-center-redirect",
                "best_for": "Preventing customer support tickets from cluttering the sales inquiry pipeline.",
                "selection_triggers": {"has_support_route": True},
                "layout_structure": "Split card container. Left half: 'Looking to hire us or buy? Stay on this page.' Right half: 'Already a customer? Visit our 24/7 Help Center or Submit a Ticket' with quick links.",
                "typography_specs": "Headline: text-base font-semibold. Link: text-sm font-medium text-[var(--primary)] underline.",
                "key_components": "Split container, support portal button, status page indicator ('All Systems Operational').",
                "responsive_behavior": "Stacks into 2 separate cards on mobile.",
                "accessibility": "Both links have descriptive text avoiding generic 'Click here'.",
                "anti_slop_rules": "Clean subtle borders; no screaming alert banners or bright yellow caution colors."
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
    for new_sec in CONTACT_SECTIONS:
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
