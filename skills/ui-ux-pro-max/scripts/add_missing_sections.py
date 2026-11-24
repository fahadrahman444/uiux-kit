#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insert 3 missing sections (why_choose_us, results_metrics, team)
into section-archetypes.json and rebuild the CSV.
Run from any directory.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path("D:/gemini/gemini-uiux-kit/skills/ui-ux-pro-max/data")

NEW_SECTIONS = [
    {
        "section_id": "why_choose_us",
        "section_name": "Why Choose Us",
        "archetypes": [
            {
                "archetype_id": "wcu-01",
                "name": "4-Column Icon Feature Grid",
                "keywords": "icon-grid, feature-cards, four-column, competitive, advantages, benefits",
                "best_for": "Agencies with 4-8 distinct competitive advantages expressible with an icon, title, and 2-line description.",
                "selection_triggers": {"advantage_count": "4-8", "style": "clean/corporate"},
                "layout_structure": "4-column icon grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8). Each cell: SVG icon in p-3 rounded-xl bg-primary/10 container, bold title, 2-line descriptor.",
                "typography_specs": "Title: text-lg font-semibold. Body: text-sm leading-relaxed text-[var(--text-secondary)].",
                "key_components": "24x24 precision SVG icon, titled advantage, short descriptor, optional stat badge.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 4 columns desktop. Consistent card heights via CSS grid stretch.",
                "accessibility": "Each feature block is an article with semantic H3 heading.",
                "anti_slop_rules": "No emoji icons, no purple gradient icon containers; use clean primary-tinted rounded backgrounds."
            },
            {
                "archetype_id": "wcu-02",
                "name": "Split Differentiator vs Competitor Table",
                "keywords": "comparison-table, us-vs-them, competitor, checklist, proof",
                "best_for": "Agencies in competitive markets where clients are explicitly comparing multiple vendors.",
                "selection_triggers": {"high_competition": True, "goal": "conversion"},
                "layout_structure": "2-column table: left column others do (grey X icons), right column we do (green check icons) with highlighted right column.",
                "typography_specs": "Column header: text-sm font-mono font-bold uppercase. Row text: text-sm font-medium.",
                "key_components": "Red-tinted competitor column vs vibrant primary-tinted us column, row-by-row contrast, bottom CTA.",
                "responsive_behavior": "On mobile, shows stacked card pair: The Old Way above, Our Way below.",
                "accessibility": "Proper table markup with th scope=col; screen reader announces column headers per row.",
                "anti_slop_rules": "Keep comparisons factual and verifiable; no vague claims without evidence."
            },
            {
                "archetype_id": "wcu-03",
                "name": "Big Statistic Anchors with Proof Copy",
                "keywords": "stats, big-numbers, proof, metrics, achievements, credibility",
                "best_for": "Agencies with compelling quantitative credibility: years in business, clients served, revenue generated.",
                "selection_triggers": {"has_proof_stats": True, "style": "bold"},
                "layout_structure": "Row of 3-4 oversized stat anchors (text-5xl font-black) with descriptor beneath, divider lines between, full-width centered container.",
                "typography_specs": "Stat numeral: text-5xl sm:text-6xl font-extrabold text-[var(--color-primary)]. Label: text-sm font-mono uppercase tracking-wider.",
                "key_components": "Animated count-up on scroll-enter, verified data footnote, bottom differentiator sentence.",
                "responsive_behavior": "2x2 grid on mobile, horizontal row on desktop.",
                "accessibility": "aria-label on each stat container reading the full statement.",
                "anti_slop_rules": "All numbers must be specific and verifiable; no round unqualified numbers."
            },
            {
                "archetype_id": "wcu-04",
                "name": "Accordion with Proof-Backed Benefit Deep-Dives",
                "keywords": "accordion, deep-dive, proof-backed, enterprise, detail",
                "best_for": "High-ticket enterprises where each differentiator requires evidence paragraphs to convert a skeptical buyer.",
                "selection_triggers": {"deal_size": "high", "enterprise": True},
                "layout_structure": "Left sticky H2 intro para; Right 5-7 accordion rows each expanding to reveal evidence paragraph, case study snippet, and stat badge.",
                "typography_specs": "Accordion trigger: text-lg font-semibold. Expanded body: text-sm leading-relaxed. Stat badge: text-xs font-mono font-bold.",
                "key_components": "Accordion triggers, smooth height transitions, inline mini-stat badge, evidence paragraph with client attribution.",
                "responsive_behavior": "Left column stacks above accordion on mobile; accordion full-width.",
                "accessibility": "aria-expanded, aria-controls, keyboard Enter/Space toggles.",
                "anti_slop_rules": "No generic passion copy; every claim must cite a specific metric or named client."
            },
            {
                "archetype_id": "wcu-05",
                "name": "Video Evidence Wall",
                "keywords": "video, evidence, founder-explains, trust, authentic",
                "best_for": "Agencies where founder or team video builds significantly more trust than text-based claims.",
                "selection_triggers": {"has_founder_video": True, "brand_tier": "boutique/premium"},
                "layout_structure": "Left: 1 large founder video card (16:9) with play button. Right: 3 stacked micro-evidence cards each with 1 bold stat plus 1 sentence proof.",
                "typography_specs": "Stat: text-3xl font-extrabold text-[var(--color-primary)]. Evidence: text-sm font-medium.",
                "key_components": "Video player card, 3 evidence micro-cards, bottom full story CTA.",
                "responsive_behavior": "Video fills full width on mobile, evidence cards stack below.",
                "accessibility": "Video player has caption (VTT), accessible play/pause control, written transcript link.",
                "anti_slop_rules": "Video must be real founder or team footage; no stock business meeting clips."
            },
            {
                "archetype_id": "wcu-06",
                "name": "Award, Certification and Trust Badge Cluster",
                "keywords": "awards, certifications, trust-badges, clutch, google-partner, iso",
                "best_for": "Agencies with industry certifications (Google Partner, Meta Partner, Clutch Top 100) that visually validate authority.",
                "selection_triggers": {"has_certifications": True, "goal": "trust/authority"},
                "layout_structure": "Centered cluster of 3-5 official certification badge cards in a row, each with the official badge SVG, certification name, year awarded, and issuer.",
                "typography_specs": "Badge name: text-sm font-semibold. Issuer: text-xs font-mono. Year: text-xs font-mono.",
                "key_components": "Official certification SVG badges, award year chips, issuer label, verification link.",
                "responsive_behavior": "Wraps into 2 rows on mobile with consistent card sizes.",
                "accessibility": "Each badge has aria-label describing the certification and year awarded.",
                "anti_slop_rules": "Only display certifications you actively hold; no expired or unobtained badges."
            }
        ]
    },
    {
        "section_id": "results_metrics",
        "section_name": "Results / Achievements",
        "archetypes": [
            {
                "archetype_id": "res-01",
                "name": "4-Column Animated Counter Strip",
                "keywords": "counter, animated-numbers, count-up, achievements, stats-row",
                "best_for": "Standard agencies wanting clean high-impact numerical proof: clients served, revenue generated, years active, success rate.",
                "selection_triggers": {"stat_count": "3-4", "style": "clean"},
                "layout_structure": "Full-width centered row of 3-4 stat blocks separated by subtle vertical dividers; each: giant counter numeral plus suffix plus descriptor label.",
                "typography_specs": "Counter: text-5xl sm:text-6xl font-extrabold text-[var(--color-primary)]. Label: text-sm font-mono uppercase tracking-widest.",
                "key_components": "Intersection Observer scroll-trigger, count-up animation via requestAnimationFrame, verified data footnote.",
                "responsive_behavior": "2x2 grid on mobile, horizontal row on desktop with consistent spacing.",
                "accessibility": "aria-label on each stat cell stating the full fact. Animation pauses if prefers-reduced-motion.",
                "anti_slop_rules": "Every stat must be specific and defensible; no unqualified round numbers. Add month/year qualifier."
            },
            {
                "archetype_id": "res-02",
                "name": "Before / After Transformation Slider",
                "keywords": "before-after, slider, transformation, cro, visual-proof",
                "best_for": "CRO, redesign, and performance agencies with dramatic before/after visual or metric proof.",
                "selection_triggers": {"has_before_after": True, "goal": "cro/redesign"},
                "layout_structure": "2-panel draggable comparison slider: left panel (muted grey tinted, Before badge), right panel (vibrant primary tinted, After badge) with draggable center divider.",
                "typography_specs": "Panel badge: text-xs font-mono font-bold uppercase. Metric callout: text-3xl font-extrabold text-emerald-500.",
                "key_components": "Draggable divider handle, metric overlay badges per panel, context caption beneath.",
                "responsive_behavior": "Touch-draggable on mobile with snap zones at 20%, 50%, 80%.",
                "accessibility": "input type=range controlling panel split position; keyboard left/right arrows adjust; aria-valuetext announces split percentage.",
                "anti_slop_rules": "Before state must be visually distinct; do not exaggerate cosmetic differences."
            },
            {
                "archetype_id": "res-03",
                "name": "Verified Analytics Chart Cards",
                "keywords": "analytics-chart, revenue-graph, verified, stripe, google-analytics",
                "best_for": "Performance and growth agencies with real analytics screenshots and verifiable growth trajectories.",
                "selection_triggers": {"has_analytics_data": True, "goal": "performance-proof"},
                "layout_structure": "3-column card grid; each card: client name and metric label at top, inline SVG area chart in middle, verified source badge and outcome stat at bottom.",
                "typography_specs": "Metric: text-4xl font-extrabold text-emerald-500. Source badge: text-xs font-mono font-bold.",
                "key_components": "Inline SVG area charts, Stripe Verified or GA4 Verified badges, client attribution.",
                "responsive_behavior": "Cards stack into single column on mobile. Charts remain readable at reduced width.",
                "accessibility": "Each chart has accessible text summary. Chart SVG marked aria-hidden with text alternative.",
                "anti_slop_rules": "Charts must have labeled axes and date ranges; no unlabeled upward squiggles."
            },
            {
                "archetype_id": "res-04",
                "name": "Agency Milestone Timeline",
                "keywords": "milestone-timeline, history, journey, years, growth-story",
                "best_for": "Established agencies (5+ years) celebrating key inflection points in their growth journey.",
                "selection_triggers": {"years_operating": "5+", "focus": "history/credibility"},
                "layout_structure": "Horizontal scrolling timeline (desktop) with year nodes and milestone cards; vertical left-spine timeline on mobile.",
                "typography_specs": "Year: text-2xl font-mono font-bold. Milestone title: text-base font-semibold. Detail: text-sm.",
                "key_components": "Year nodes with connecting spine, milestone cards for founding and expansion and awards, photo thumbnails.",
                "responsive_behavior": "Horizontal scroll with snap-mandatory on desktop; vertical spine on mobile.",
                "accessibility": "Wrapped in ordered list preserving chronological DOM sequence.",
                "anti_slop_rules": "Limit to 5-7 genuinely significant milestones; do not list every minor blog post."
            },
            {
                "archetype_id": "res-05",
                "name": "Live Performance Ticker",
                "keywords": "live-ticker, real-time, revenue-counter, momentum, urgency",
                "best_for": "High-volume growth agencies or e-commerce specialists wanting to demonstrate live scale.",
                "selection_triggers": {"has_live_data": True, "style": "dynamic"},
                "layout_structure": "Full-width dark banner with animated rolling counter showing live revenue metric, green pulse dot, and live timestamp.",
                "typography_specs": "Counter: text-3xl sm:text-4xl font-mono font-extrabold text-emerald-400. Label: text-xs font-mono uppercase.",
                "key_components": "Rolling number counter, green status pulse dot, live-updated timestamp, Last updated label.",
                "responsive_behavior": "Scales font down on mobile; counter remains readable.",
                "accessibility": "aria-live=off on counter to prevent screen reader announcing every digit change; summary read on page load.",
                "anti_slop_rules": "Only use live ticker if you can feed it real data; a static fake counter destroys trust when scrutinized."
            },
            {
                "archetype_id": "res-06",
                "name": "Stat Plus Signed Quote Proof Cards",
                "keywords": "stat-quote, signed-proof, executive-quote, enterprise-results",
                "best_for": "Enterprise agencies where each result needs direct attribution to a named executive for maximum credibility.",
                "selection_triggers": {"enterprise": True, "has_named_quotes": True},
                "layout_structure": "3-column grid of cards; each: giant metric plus signed client quote beneath with executive name, title, company logo.",
                "typography_specs": "Metric: text-4xl font-extrabold. Quote: text-sm font-medium italic. Attribution: text-xs font-semibold.",
                "key_components": "Bold metric badge, italic quote blockquote, executive avatar 40px plus name plus title plus company SVG logo.",
                "responsive_behavior": "Cards stack into single column on mobile with consistent padding.",
                "accessibility": "Quote wrapped in semantic blockquote with cite element.",
                "anti_slop_rules": "Quotes must be real attributed statements; no anonymous satisfied client attribution."
            }
        ]
    },
    {
        "section_id": "team",
        "section_name": "Our Team",
        "archetypes": [
            {
                "archetype_id": "team-01",
                "name": "Card Grid (Headshot + Bio + Role)",
                "keywords": "team-grid, cards, headshots, bio, role, standard",
                "best_for": "Agencies with 3-12 team members wanting a clean, professional team introduction.",
                "selection_triggers": {"team_size": "3-12", "style": "corporate/clean"},
                "layout_structure": "Responsive card grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8). Each card: portrait photo (aspect-square rounded-2xl object-cover), name, role badge, 2-line bio, LinkedIn icon link.",
                "typography_specs": "Name: text-lg font-semibold. Role: text-xs font-mono uppercase tracking-wider. Bio: text-sm.",
                "key_components": "Portrait photo (high-res, consistent aspect-square crop), role chip, 2-line bio, LinkedIn icon link.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 3-4 columns desktop.",
                "accessibility": "Portrait alt text includes Name, Role and Agency name. LinkedIn link has aria-label.",
                "anti_slop_rules": "No mismatched aspect ratios across team photos; enforce consistent cropping. No AI-generated headshots."
            },
            {
                "archetype_id": "team-02",
                "name": "Founder-Focus Split with Supporting Grid",
                "keywords": "founder-focus, leadership, two-tier, founding-team",
                "best_for": "Boutique agencies where the 1-2 founders are the primary trust signal and supporting staff are secondary.",
                "selection_triggers": {"founder_led": True, "team_size": "3-10"},
                "layout_structure": "Top tier: 1 or 2 large founder cards (wider aspect ratio, expanded bio paragraph, awards listed). Bottom tier: compact grid of 4-6 supporting team member cards.",
                "typography_specs": "Founder name: text-2xl font-bold. Founder bio: text-base. Supporting name: text-base font-semibold.",
                "key_components": "Large founder portrait (aspect-video or 3:4), credentials pill strip, expanded bio paragraph, compact team grid below.",
                "responsive_behavior": "Founder cards stack above supporting team grid on mobile.",
                "accessibility": "Clear H2 for Leadership section and H3 for Team subsection.",
                "anti_slop_rules": "Founder bio must be specific with years experience, past companies, notable wins; no generic visionary leader copy."
            },
            {
                "archetype_id": "team-03",
                "name": "Hover Reveal Interactive Profiles",
                "keywords": "hover-reveal, interactive, fun-facts, personality, creative",
                "best_for": "Creative agencies wanting to show team personality and culture, not just corporate credentials.",
                "selection_triggers": {"culture_focus": True, "style": "creative"},
                "layout_structure": "Grid of team cards; default: professional portrait plus name plus role. Hover: card flips or slides to reveal fun fact, favorite tool, and social links.",
                "typography_specs": "Role: text-xs font-mono. Fun fact: text-sm italic font-medium. Tool badge: text-xs font-mono.",
                "key_components": "Card flip animation via CSS transform rotateY or slide-reveal, fun fact, tool icon badge, social media links.",
                "responsive_behavior": "On touch devices, tap toggles card state. Touch-active state indicated by bottom indicator dot.",
                "accessibility": "Flip accessible via keyboard focus (Enter toggles). Both front and back content readable by screen reader with aria-hidden on inactive face.",
                "anti_slop_rules": "Fun facts must be genuine and unique per person; no generic loves coffee and coding placeholder copy."
            },
            {
                "archetype_id": "team-04",
                "name": "Departmental Tab Switcher",
                "keywords": "departments, tabs, large-team, organized, categorized",
                "best_for": "Larger agencies (15-50 people) with distinct departments: Strategy, Creative, Engineering, Client Success.",
                "selection_triggers": {"team_size": "15+", "has_departments": True},
                "layout_structure": "Top horizontal department tab bar; clicking a tab filters the team grid to show only that department with animated transition.",
                "typography_specs": "Department tab: text-sm font-semibold. Member count badge: text-xs font-mono.",
                "key_components": "Tab pill navigation with member count badges, animated grid reflow, All default tab.",
                "responsive_behavior": "Horizontal scrolling tab strip on mobile.",
                "accessibility": "role=tablist, role=tab, aria-selected, keyboard left/right navigation.",
                "anti_slop_rules": "Do not create a miscellaneous or other department tab; every person belongs to a named team."
            },
            {
                "archetype_id": "team-05",
                "name": "Editorial Masonry Portrait Gallery",
                "keywords": "editorial, masonry, portrait, luxury, artistic, photography-first",
                "best_for": "High-end creative studios and luxury brands with editorial-quality professional photography.",
                "selection_triggers": {"has_editorial_photos": True, "brand_tier": "luxury/editorial"},
                "layout_structure": "Asymmetric masonry layout with varied portrait card heights and minimal overlaid text; hovering reveals name and role in a bottom gradient scrim.",
                "typography_specs": "Overlay name: text-xl font-semibold text-white. Overlay role: text-xs font-mono text-white/70.",
                "key_components": "High-res editorial portraits, bottom gradient scrim overlay, hover reveal name/role, subtle image scale on hover.",
                "responsive_behavior": "Single column of portraits on mobile with static name/role visible beneath each.",
                "accessibility": "Portrait alt text includes name and role. Hover-revealed text also present in DOM (visually hidden on non-hover).",
                "anti_slop_rules": "Zero stock photography; all photos must be real team members shot with editorial lighting."
            },
            {
                "archetype_id": "team-06",
                "name": "Compact Name and Role List (Remote Distributed)",
                "keywords": "compact-list, remote-team, distributed, text-list, global",
                "best_for": "Fully remote or large distributed teams where showing 30+ faces is impractical but acknowledging scale matters.",
                "selection_triggers": {"team_size": "30+", "is_remote": True},
                "layout_structure": "2-column text list; each entry: name (font-semibold), role (font-mono text-muted), timezone/location tag. Header stats: total team size, countries represented.",
                "typography_specs": "Name: text-sm font-semibold. Role: text-xs font-mono. Location tag: text-xs.",
                "key_components": "Team size stat badge at section top, compact name/role rows, timezone flag as location indicator.",
                "responsive_behavior": "Single column list on mobile.",
                "accessibility": "List uses semantic ul and li. Location flags have aria-label with country name.",
                "anti_slop_rules": "Do not use country flag emojis as the primary location indicator; also include the country name in text."
            }
        ]
    }
]


def rebuild():
    json_path = DATA_DIR / "section-archetypes.json"
    csv_path = DATA_DIR / "section-archetypes.csv"

    # Load current dataset
    with open(json_path, encoding="utf-8") as f:
        existing = json.load(f)

    # Inject new sections at correct positions:
    # why_choose_us after services (index 4), results_metrics after portfolio (now 8), team after testimonials (now 10)
    existing_ids = [s["section_id"] for s in existing]
    print(f"Current sections ({len(existing)}): {existing_ids}")

    # Build ordered final list
    final_order = [
        "navbar", "hero", "trusted_by", "about", "services",
        "why_choose_us",
        "how_we_work", "portfolio", "testimonials",
        "results_metrics",
        "pricing",
        "team",
        "faq", "final_cta", "footer"
    ]
    new_map = {s["section_id"]: s for s in NEW_SECTIONS}
    existing_map = {s["section_id"]: s for s in existing}

    ordered = []
    for sid in final_order:
        if sid in existing_map:
            ordered.append(existing_map[sid])
        elif sid in new_map:
            ordered.append(new_map[sid])
        else:
            print(f"  WARNING: section_id {sid!r} not found in either dataset")

    print(f"Final sections ({len(ordered)}): {[s['section_id'] for s in ordered]}")

    # Count archetypes
    total = sum(len(s["archetypes"]) for s in ordered)
    print(f"Total archetypes: {total}")

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON written: {json_path}")

    # Write CSV
    fieldnames = [
        "Section ID", "Section Name", "Archetype ID", "Archetype Name",
        "Keywords", "Best For", "Selection Triggers", "Layout Structure",
        "Typography Specs", "Key Components", "Responsive Behavior",
        "Accessibility", "Anti-Slop Rules"
    ]
    count = 0
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sec in ordered:
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
                count += 1
    print(f"[OK] CSV written: {count} archetypes -> {csv_path}")


if __name__ == "__main__":
    rebuild()
