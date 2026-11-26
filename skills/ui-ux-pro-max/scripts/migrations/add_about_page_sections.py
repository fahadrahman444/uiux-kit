#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated About Us Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 4 dedicated sections:
1. about_timeline (3 archetypes)
2. about_values (3 archetypes)
3. about_culture_gallery (3 archetypes)
4. about_leadership_board (2 archetypes)
Total: 11 new archetypes.
Combined dataset will have: 24 sections, 129 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

ABOUT_SECTIONS = [
    {
        "section_id": "about_timeline",
        "section_name": "Company Origin & Milestones",
        "archetypes": [
            {
                "archetype_id": "time-01",
                "name": "Vertical Alternating Milestone Spine",
                "keywords": "timeline, milestones, company-history, journey, origin-story, vertical-timeline",
                "best_for": "Established companies or agencies with 4-8 chronological milestones (Founding, Seed, Series A, Global Expansion).",
                "selection_triggers": {"has_milestones": True, "years_operating": "3+", "style": "editorial"},
                "layout_structure": "Central vertical spine (1px subtle border) with alternating cards on left and right (desktop). Each node features a glowing year pill, milestone headline, 2-line description, and metric badge.",
                "typography_specs": "Year badge: text-xs font-mono font-bold tracking-wider text-[var(--primary)] bg-primary/10 px-2.5 py-1 rounded-full. Milestone title: text-lg font-bold. Body: text-sm text-[var(--text-secondary)].",
                "key_components": "Vertical SVG connecting line, milestone node dots, year badge, event title, optional press/metric tag.",
                "responsive_behavior": "Collapses to single-sided timeline on mobile: vertical line aligns to left margin (pl-8), all cards align right.",
                "accessibility": "Semantic ordered list <ol>, each milestone is an <li> with an aria-label indicating date and milestone.",
                "anti_slop_rules": "No pulsating cartoon dots; use subtle border highlights and clean monospaced year typography."
            },
            {
                "archetype_id": "time-02",
                "name": "Horizontal Snapping Milestone Carousel",
                "keywords": "horizontal-timeline, stepper, carousel, interactive-milestones",
                "best_for": "Fast-moving tech startups wanting a punchy, interactive chronology without vertical page bloat.",
                "selection_triggers": {"has_milestones": True, "timeline_style": "horizontal"},
                "layout_structure": "Horizontal scroll container with snap-x alignment. Progress line connecting chronological nodes horizontally. Navigation arrow triggers with progress bar indicator.",
                "typography_specs": "Year: text-2xl font-mono font-extrabold text-[var(--primary)]. Headline: text-base font-semibold. Body: text-sm leading-relaxed.",
                "key_components": "Horizontal track, active stage indicator, prev/next buttons, stage cards with consistent 320px width.",
                "responsive_behavior": "Smooth touch-swipe horizontal scroll on mobile with pagination dots.",
                "accessibility": "Scrollable region marked with role='region' and aria-label='Company Timeline Carousel'; keyboard arrows navigate items.",
                "anti_slop_rules": "Ensure cards do not truncate text on small screens; enforce minimum readable height."
            },
            {
                "archetype_id": "time-03",
                "name": "Minimalist Year-by-Year Editorial Ledger",
                "keywords": "ledger, minimalist-timeline, typography-first, high-density",
                "best_for": "Design studios, venture studios, and architecture firms wanting clean, sophisticated typography without graphics.",
                "selection_triggers": {"has_milestones": True, "style": "minimalist"},
                "layout_structure": "Clean stacked list with 1px top/bottom border dividers. Left col: Year (text-mono). Center col: Milestone headline and narrative. Right col: Key stat or partner logo.",
                "typography_specs": "Year: text-sm font-mono text-[var(--text-muted)]. Headline: text-xl font-medium text-[var(--text-primary)]. Summary: text-sm text-[var(--text-secondary)].",
                "key_components": "3-column grid row, hover highlight, subtle border separators, monospaced timestamp.",
                "responsive_behavior": "Stacks to 2-column or single column on mobile with year above headline.",
                "accessibility": "Uses <dl>, <dt> (Year), and <dd> (Description) for accessible definition list semantics.",
                "anti_slop_rules": "Zero floating badges or emoji decorations; pure typographic craft and strict alignment."
            }
        ]
    },
    {
        "section_id": "about_values",
        "section_name": "Core Beliefs & Operating Principles",
        "archetypes": [
            {
                "archetype_id": "val-01",
                "name": "6-Card Numbered Principle Grid",
                "keywords": "values, beliefs, principles, numbered-cards, culture",
                "best_for": "Agencies and tech companies with 4 to 6 clear internal philosophies guiding their work.",
                "selection_triggers": {"value_count": "4-6", "style": "clean"},
                "layout_structure": "3x2 grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8). Each card: oversized monospaced number (01, 02, ...), bold belief title, 3-sentence operational explanation.",
                "typography_specs": "Number: text-3xl font-mono font-bold text-[var(--text-muted)]. Title: text-xl font-bold text-[var(--text-primary)]. Body: text-sm leading-relaxed text-[var(--text-secondary)].",
                "key_components": "Card surface, monospaced index, title, operational rationale, subtle bottom accent line on hover.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 3 columns desktop with stretch alignment.",
                "accessibility": "Semantic <section> with <h3> for each principle title; contrast ratio exceeds 7:1.",
                "anti_slop_rules": "No cliché stock buzzwords ('We innovate with synergy'); principles must describe actual trade-offs and behaviors."
            },
            {
                "archetype_id": "val-02",
                "name": "Split Manifesto & Belief Accordion",
                "keywords": "manifesto, philosophy-accordion, thesis, founder-beliefs",
                "best_for": "Mission-driven companies where the founders' point of view is the primary differentiator.",
                "selection_triggers": {"founder_led": True, "has_manifesto": True},
                "layout_structure": "2-column container. Left (5 cols): Sticky founder manifesto statement in large editorial serif font. Right (7 cols): Expandable accordion detailing how each belief is executed.",
                "typography_specs": "Manifesto: text-2xl sm:text-3xl font-serif font-medium leading-relaxed. Accordion title: text-lg font-semibold. Body: text-sm leading-relaxed.",
                "key_components": "Sticky manifesto column, accessible accordion rows, plus/minus indicator, quote attribution.",
                "responsive_behavior": "Stacks vertically on mobile with manifesto statement on top.",
                "accessibility": "<button aria-expanded='false'> on accordion headers with keyboard navigation support.",
                "anti_slop_rules": "No glowing purple gradient text in the manifesto; maintain clean dark-mode or high-contrast editorial look."
            },
            {
                "archetype_id": "val-03",
                "name": "Asymmetric Bento Grid of Cultural Pillars",
                "keywords": "bento-values, cultural-pillars, asymmetric-grid, modern-culture",
                "best_for": "Modern tech brands, creative agencies, and AI companies seeking a visually striking, non-traditional layout.",
                "selection_triggers": {"style": "contemporary/bento"},
                "layout_structure": "4-card bento grid (2 large span-2 cards + 2 compact cards). Cards mix typography, code/terminal snippets, and concrete behavioral rules.",
                "typography_specs": "Pillar title: text-xl sm:text-2xl font-bold. Code snippet: text-xs font-mono text-emerald-400 bg-slate-900 p-4 rounded-xl.",
                "key_components": "Asymmetric grid cells, ambient card borders, code snippet element, metric anchor badge.",
                "responsive_behavior": "Converts to single-column stacked cards on mobile with consistent 16px gap.",
                "accessibility": "Cards have role='region' or <article> with clear heading hierarchy.",
                "anti_slop_rules": "Bento cards must contain actual substance, not empty decorative gradient filler."
            }
        ]
    },
    {
        "section_id": "about_culture_gallery",
        "section_name": "Life, Workspaces & Remote Team",
        "archetypes": [
            {
                "archetype_id": "cult-01",
                "name": "Curated Multi-Aspect Studio Collage",
                "keywords": "photo-collage, team-life, office-gallery, studio-photos, authentic-workplace",
                "best_for": "Companies with high-quality authentic workplace, studio, or offsite photography.",
                "selection_triggers": {"has_office_photos": True, "gallery_type": "collage"},
                "layout_structure": "Asymmetric 5-image collage grid (grid-cols-12 gap-6). Mix of aspect-video hero photo (span-7), vertical portrait (span-5), and bottom panoramic strip.",
                "typography_specs": "Photo caption: text-xs font-mono text-[var(--text-muted)]. Location badge: text-xs font-semibold px-2 py-1 bg-black/60 backdrop-blur rounded.",
                "key_components": "Aspect-ratio locked image containers, subtle hover zoom (scale-102 duration-300), location tags, caption overlays.",
                "responsive_behavior": "Converts to 2-column or swipeable photo strip on mobile.",
                "accessibility": "Every <img> has descriptive alt text describing the team context and physical environment.",
                "anti_slop_rules": "STRICT: Zero generic stock photography (e.g. models in suits high-fiving in glass meeting rooms). Real workplace only."
            },
            {
                "archetype_id": "cult-02",
                "name": "Global Hubs & Distributed Footprint Map",
                "keywords": "global-map, distributed-team, remote-culture, office-locations",
                "best_for": "Distributed or multi-city agencies and tech platforms with offices in New York, London, Tokyo, etc.",
                "selection_triggers": {"distributed_team": True},
                "layout_structure": "Full-width dark container with stylized SVG world map graphic. Interactive or pinned hub markers (San Francisco, London, Singapore) displaying local team headcount and local time.",
                "typography_specs": "City name: text-base font-bold. Local time & headcount: text-xs font-mono text-[var(--text-secondary)].",
                "key_components": "SVG vector map, pulsing location pins, city card popovers, remote-first manifesto pill.",
                "responsive_behavior": "Map scrolls horizontally or simplifies into a 3-column city card grid on mobile viewports.",
                "accessibility": "City list also provided in an accessible semantic <ul> hidden visually or beneath the map for screen readers.",
                "anti_slop_rules": "Map pins must be accurate and vector-clean; no pixelated map textures."
            },
            {
                "archetype_id": "cult-03",
                "name": "Employee Voice & Working Norms Strip",
                "keywords": "employee-quotes, day-in-the-life, working-norms, team-perspectives",
                "best_for": "Culture-first companies wanting to highlight how team members actually work and collaborate.",
                "selection_triggers": {"culture_focus": True},
                "layout_structure": "3-column card grid. Each card combines a natural photo of a team member in their setup, a direct quote about working norms, and their role.",
                "typography_specs": "Quote: text-base italic leading-relaxed text-[var(--text-primary)]. Role: text-xs font-mono uppercase text-[var(--primary)].",
                "key_components": "Authentic portrait, quote text, role label, working style badge (e.g., 'Async / Deep Work Focus').",
                "responsive_behavior": "1 column on mobile, 3 columns desktop with stretch card heights.",
                "accessibility": "Quotes wrapped in <figure> and <blockquote> with <figcaption> for attribution.",
                "anti_slop_rules": "No manufactured corporate praise; focus on practical working realities."
            }
        ]
    },
    {
        "section_id": "about_leadership_board",
        "section_name": "Executive Board, Advisors & Investors",
        "archetypes": [
            {
                "archetype_id": "lead-01",
                "name": "C-Suite Grid with Alumni Credibility Badges",
                "keywords": "leadership, executive-team, c-suite, founders, pedigree, alumni-badges",
                "best_for": "High-growth tech startups and top-tier consultancies where leadership background drives enterprise trust.",
                "selection_triggers": {"team_tier": "executive", "has_alumni_proof": True},
                "layout_structure": "4-column grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8). Each profile: crisp headshot, executive name, title, and mini previous experience pill strip ('Ex-Stripe', 'Ex-Google', 'MIT').",
                "typography_specs": "Name: text-lg font-bold. Title: text-sm font-medium text-[var(--primary)]. Alumni pill: text-xs font-mono text-[var(--text-muted)].",
                "key_components": "Headshot (aspect-[4/5] rounded-2xl), name, title, previous company logos/chips, LinkedIn SVG link.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 4 columns desktop.",
                "accessibility": "Headshot alt text includes full name and title; LinkedIn link has accessible aria-label.",
                "anti_slop_rules": "Consistent portrait lighting and aspect ratios across all photos; no mismatched crops."
            },
            {
                "archetype_id": "lead-02",
                "name": "Backed-By Venture Capital & Advisory Board Strip",
                "keywords": "investors, backed-by, advisory-board, venture-capital, angel-investors",
                "best_for": "Venture-backed companies where investor tier-1 brand backing establishes institutional stability.",
                "selection_triggers": {"has_investors": True},
                "layout_structure": "Full-width section with 2-tier layout: Top tier displays Tier-1 VC investor logos (e.g. Sequoia, Accel, YC); Bottom tier displays 4 advisory board quotes.",
                "typography_specs": "Section eyebrow: text-xs font-mono uppercase tracking-widest text-[var(--text-muted)]. Quote: text-sm font-medium.",
                "key_components": "Monochrome investor logo row, advisor headshots, quote bubbles, partner credentials.",
                "responsive_behavior": "Logos wrap into 2-3 columns on mobile; advisor quotes stack cleanly.",
                "accessibility": "Logo SVGs have title attributes; advisor cards use semantic figure/blockquote.",
                "anti_slop_rules": "All logos normalized to uniform greyscale height; no full-color competing sponsor banners."
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
    for new_sec in ABOUT_SECTIONS:
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
