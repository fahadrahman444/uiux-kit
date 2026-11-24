#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Case Studies & Portfolio Hub Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 3 dedicated sections:
1. case_study_hero_highlight (3 archetypes)
2. case_study_filter_hub (3 archetypes)
3. case_study_client_quote_strip (2 archetypes)
Total: 8 new archetypes.
Combined dataset will have: 34 sections, 155 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path("D:/gemini/gemini-uiux-kit/skills/ui-ux-pro-max/data")

CASE_STUDIES_SECTIONS = [
    {
        "section_id": "case_study_hero_highlight",
        "section_name": "Flagship Impact Case Study Hero",
        "archetypes": [
            {
                "archetype_id": "csh-01",
                "name": "Split Hero Transformation Spotlight",
                "keywords": "case-study-hero, spotlight, transformation, metrics-strip, flagship-project",
                "best_for": "Highlighting a major flagship client success story with undeniable ROI and visual polish.",
                "selection_triggers": {"has_flagship": True, "style": "split_impact"},
                "layout_structure": "2-column split (grid-cols-1 lg:grid-cols-12 gap-12 max-w-6xl mx-auto py-20 items-center). Left (6 cols): Client logo, category eyebrow chip, punchy outcome headline, 3-metric ROI badge strip (+340% Pipeline, 45ms P99 Latency, 6-Week Delivery), 'Read Full Story ->' primary CTA. Right (6 cols): High-res responsive device mockup frame (MacBook + iPhone) with subtle ambient glow.",
                "typography_specs": "Eyebrow: text-xs font-mono uppercase tracking-widest text-[var(--primary)]. Headline: text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-[var(--text-primary)]. Stat numerals: text-2xl font-mono font-bold text-emerald-400.",
                "key_components": "Client vector logo, metric pill badges, primary case study CTA button, multi-device mockup container with 1px border.",
                "responsive_behavior": "Stacks vertically on mobile with headline and metrics above mockup.",
                "accessibility": "Device mockup image has descriptive alt text describing the client application UI; CTA has clear destination aria-label.",
                "anti_slop_rules": "Metrics must be qualified and defensible; zero generic round stats like '100% better'."
            },
            {
                "archetype_id": "csh-02",
                "name": "Full-Bleed Cinematic Visual Hero",
                "keywords": "cinematic-hero, full-bleed, video-reel, immersive-case-study, visual-craft",
                "best_for": "High-craft digital product studios, branding agencies, and 3D visual production houses.",
                "selection_triggers": {"has_video": True, "immersive": True},
                "layout_structure": "Full-width container (aspect-[21/9] or min-h-[520px] rounded-3xl overflow-hidden relative mx-auto max-w-7xl my-8). Background: looping muted MP4 video reel or high-res photography. Foreground card (bottom-left): Client name, project scope, key quote, and 'Explore Project' button.",
                "typography_specs": "Overlay title: text-2xl sm:text-3xl font-bold text-white. Scope chips: text-xs font-mono text-slate-300 bg-black/50 px-2 py-0.5 rounded.",
                "key_components": "HTML5 video element with playsinline and autoplay, gradient scrim mask, floating glassmorphism metadata card, play/pause toggle.",
                "responsive_behavior": "Video aspect ratio adjusts to aspect-video on mobile; card sits cleanly below or inside.",
                "accessibility": "Includes visible play/pause button for WCAG 2.2 Pause/Stop/Hide rule; video is muted by default.",
                "anti_slop_rules": "Must provide a fallback poster image for slow connections; video must be compressed under 4MB."
            },
            {
                "archetype_id": "csh-03",
                "name": "Minimalist Power-Metric Header",
                "keywords": "power-metric, cumulative-results, editorial-portfolio-hero, typographic-hero",
                "best_for": "Enterprise engineering consultancies where cumulative track record outweighs single visual projects.",
                "selection_triggers": {"style": "minimalist/editorial"},
                "layout_structure": "Single column max-w-4xl mx-auto py-24 text-center. Giant editorial headline announcing cumulative scale (e.g. '$4.2B in client value shipped across 85+ production deployments'), followed by a 3-badge proof strip.",
                "typography_specs": "Eyebrow: text-xs font-mono uppercase tracking-widest text-[var(--text-muted)]. H1: text-4xl sm:text-6xl font-serif font-bold text-[var(--text-primary)] leading-[1.12].",
                "key_components": "Oversized typography headline, client logo row, category quick-jump anchors.",
                "responsive_behavior": "Fluid typography clamping preserving line breaks on mobile.",
                "accessibility": "Headings follow strict hierarchy H1 -> H2; text contrast exceeds 7:1.",
                "anti_slop_rules": "Zero cartoon emojis or floating sparkles; pure typographic authority."
            }
        ]
    },
    {
        "section_id": "case_study_filter_hub",
        "section_name": "Filterable Multi-Axis Portfolio Grid",
        "archetypes": [
            {
                "archetype_id": "csf-01",
                "name": "Multi-Pill Filterable Grid with Impact Badges",
                "keywords": "filterable-grid, portfolio-filters, sector-pills, outcome-badges, interactive-portfolio",
                "best_for": "Agencies and dev shops with 12 to 30+ varied case studies spanning multiple industries and tech stacks.",
                "selection_triggers": {"case_count": "10+", "has_filters": True},
                "layout_structure": "Sticky filter pill header (All, Fintech, Healthtech, AI & Data, B2B SaaS). Below: 2 or 3-column responsive card grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8). Each card: high-res project image (aspect-[16/10]), client logo, deliverables tag, bold impact metric badge (e.g. '+240% ARR'), and case title.",
                "typography_specs": "Filter pill: text-xs font-semibold px-3.5 py-1.5. Card title: text-xl font-bold text-[var(--text-primary)]. Metric tag: text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full.",
                "key_components": "Filter pill bar with active indicator, image card with hover zoom (scale-102 duration-200), client logo chip, impact metric pill, tag list.",
                "responsive_behavior": "Filter pills scroll horizontally with snap-x on mobile; grid collapses to single column.",
                "accessibility": "Filter bar uses role='tablist' with aria-selected states; filter updates announce item count via aria-live='polite'.",
                "anti_slop_rules": "Zero slow animated reflows; filter uses fast CSS opacity/visibility transitions with zero layout shifts."
            },
            {
                "archetype_id": "csf-02",
                "name": "Asymmetric Editorial Masonry with Embedded Quotes",
                "keywords": "editorial-masonry, staggered-grid, embedded-quotes, design-studio",
                "best_for": "Award-winning creative design studios showcasing varied aspect ratios and typography.",
                "selection_triggers": {"style": "editorial/creative"},
                "layout_structure": "Asymmetric 2-column masonry grid. Standard project cards alternate with full-quote cards (large quote from client CEO) and video preview cards.",
                "typography_specs": "Title: text-2xl font-bold font-serif. Tag: text-xs font-mono uppercase text-[var(--text-muted)]. Quote: text-lg italic.",
                "key_components": "Asymmetric card heights, embedded client testimonial cards, hover video loops, clean link arrows.",
                "responsive_behavior": "Collapses to single column on mobile while maintaining quote cards between projects.",
                "accessibility": "Quote cards use semantic <figure> and <blockquote>; images have rich descriptive alt text.",
                "anti_slop_rules": "Ensure image cards maintain consistent contrast and alignment; avoid unreadable text over photos."
            },
            {
                "archetype_id": "csf-03",
                "name": "High-Density Data-Dense Ledger",
                "keywords": "data-dense, project-ledger, table-portfolio, enterprise-index",
                "best_for": "Enterprise systems consultancies, cybersecurity firms, and technical architecture teams.",
                "selection_triggers": {"style": "data_dense/ledger"},
                "layout_structure": "Full-width searchable table with live search input. Columns: Client & Sector, Scope of Work, Primary Deliverable, Verified Impact Metric, Link / Case Study.",
                "typography_specs": "Search input: text-sm font-medium. Table headers: text-xs font-mono uppercase text-[var(--text-muted)]. Rows: text-sm font-medium.",
                "key_components": "Live search filter, column sorting triggers, verified metric pills, PDF download / case link buttons.",
                "responsive_behavior": "Horizontal scroll container on mobile with sticky client column.",
                "accessibility": "Semantic <table> with th scope='col', sortable buttons announce direction via aria-sort.",
                "anti_slop_rules": "Crisp 1px borders; zero bloated decorative empty space."
            }
        ]
    },
    {
        "section_id": "case_study_client_quote_strip",
        "section_name": "Executive Client Impact Quotes",
        "archetypes": [
            {
                "archetype_id": "csq-01",
                "name": "3-Column Pull Quote Grid with Enterprise Headshots",
                "keywords": "client-quotes, pull-quotes, executive-testimonials, case-study-proof",
                "best_for": "Reinforcing project outcomes with direct quotes from verified C-suite stakeholders.",
                "selection_triggers": {"has_quotes": True},
                "layout_structure": "3-column card grid (grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto py-16). Each card: verified client avatar, executive name and title, company logo chip, 3-sentence quote on tangible project impact.",
                "typography_specs": "Quote text: text-base leading-relaxed text-[var(--text-primary)]. Executive name: text-sm font-semibold. Title: text-xs text-[var(--text-muted)].",
                "key_components": "Avatar photo (rounded-full 44x44), company logo SVG, quote block, LinkedIn profile link icon.",
                "responsive_behavior": "1 column on mobile, 3 columns desktop.",
                "accessibility": "Semantic <figure> and <blockquote>; avatar has alt text.",
                "anti_slop_rules": "Quotes must reference specific project results; no generic 'They were great to work with'."
            },
            {
                "archetype_id": "csq-02",
                "name": "Full-Width Single Endorsement Banner",
                "keywords": "single-endorsement, marquee-quote, vip-quote, spotlight-quote",
                "best_for": "Highlighting an exceptional marquee quote from a globally recognized Fortune 500 partner.",
                "selection_triggers": {"has_vip_quote": True},
                "layout_structure": "Full-width elevated card (py-16 px-8 sm:px-16 rounded-3xl bg-[var(--surface-raised)] border border-[var(--border-subtle)] text-center max-w-5xl mx-auto my-12).",
                "typography_specs": "Quote: text-2xl sm:text-3xl font-serif font-medium leading-relaxed text-[var(--text-primary)]. Attribution: text-sm font-mono uppercase tracking-wider text-[var(--primary)].",
                "key_components": "Marquee client logo, oversized quotation mark, executive signature or headshot, video interview trigger button.",
                "responsive_behavior": "Typography scales smoothly via fluid clamp; quote wraps cleanly.",
                "accessibility": "Quote wrapped in semantic blockquote with cite attribute.",
                "anti_slop_rules": "Clean monochromatic logo; no bright clashing client brand colors."
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
    for new_sec in CASE_STUDIES_SECTIONS:
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
