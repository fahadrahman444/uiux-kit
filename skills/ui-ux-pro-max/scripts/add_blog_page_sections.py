#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Blog & Editorial Hub Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 3 dedicated sections:
1. blog_featured_editorial (3 archetypes)
2. blog_topic_filter_feed (3 archetypes)
3. blog_newsletter_capture (2 archetypes)
Total: 8 new archetypes.
Combined dataset will have: 37 sections, 163 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path("D:/gemini/gemini-uiux-kit/skills/ui-ux-pro-max/data")

BLOG_SECTIONS = [
    {
        "section_id": "blog_featured_editorial",
        "section_name": "Lead Story & Editorial Spotlight",
        "archetypes": [
            {
                "archetype_id": "bfeat-01",
                "name": "Split Hero Lead Story",
                "keywords": "featured-article, lead-story, marquee-blog, editorial-spotlight, hero-post",
                "best_for": "Highlighting a major flagship thought-leadership essay, product announcement, or quarterly report.",
                "selection_triggers": {"has_featured": True, "style": "split"},
                "layout_structure": "2-column container (grid-cols-1 lg:grid-cols-12 gap-12 max-w-6xl mx-auto py-16 items-center). Left (6 cols): Category chip, publish date, oversized editorial H1, 3-line excerpt, author metadata row (36x36 avatar, author name, estimated read time pill e.g. '8 min read'), 'Read Article ->' link button. Right (6 cols): Aspect-[16/10] editorial cover image with subtle 1px border and hover zoom.",
                "typography_specs": "Category: text-xs font-mono uppercase tracking-widest text-[var(--primary)]. Title: text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-[var(--text-primary)]. Excerpt: text-base leading-relaxed text-[var(--text-secondary)]. Author: text-sm font-semibold.",
                "key_components": "Category pill, editorial H1, excerpt, author avatar, reading time badge, high-res cover image.",
                "responsive_behavior": "Stacks vertically on mobile with image above or below the headline.",
                "accessibility": "Cover image has descriptive alt text summarizing visual; article link has explicit aria-label with full title.",
                "anti_slop_rules": "No clickbait emoji titles or radioactive gradient badges; clean, authoritative editorial styling."
            },
            {
                "archetype_id": "bfeat-02",
                "name": "Asymmetric 1+2 Editorial Trio",
                "keywords": "asymmetric-editorial, trio-blog, trending-posts, hero-plus-list",
                "best_for": "Active publications and company blogs publishing 2-5 articles per week.",
                "selection_triggers": {"post_density": "high", "has_trending": True},
                "layout_structure": "Asymmetric 12-column grid. Left (7 cols): Large hero card with full cover image, category badge, and bold title. Right (5 cols): 2 stacked secondary trending cards with smaller horizontal thumbnails, titles, and read times.",
                "typography_specs": "Hero title: text-2xl sm:text-3xl font-bold. Secondary title: text-lg font-semibold text-[var(--text-primary)]. Date: text-xs font-mono text-[var(--text-muted)].",
                "key_components": "Primary lead card, 2 secondary stacked cards, 'Trending Stories' header, category tags.",
                "responsive_behavior": "Stacks into 3 sequential cards on mobile viewports.",
                "accessibility": "Articles wrapped in semantic <article> tags with independent headings.",
                "anti_slop_rules": "Ensure thumbnail crops maintain consistent aspect ratios; no distorted imagery."
            },
            {
                "archetype_id": "bfeat-03",
                "name": "Minimalist Editorial Cover",
                "keywords": "minimalist-blog, typography-first, longform-essay, substack-style",
                "best_for": "Deep research institutions, engineering engineering-heavy blogs, and intellectual essays without photographic assets.",
                "selection_triggers": {"style": "minimalist/longform"},
                "layout_structure": "Single column max-w-3xl mx-auto py-24 text-center. Category eyebrow in monospace, giant serif title, 2-line thesis excerpt, followed by author bio pill and publication timestamp.",
                "typography_specs": "Title: text-4xl sm:text-5xl font-serif font-bold text-[var(--text-primary)] leading-[1.15]. Excerpt: text-lg text-[var(--text-secondary)]. Metadata: text-xs font-mono text-[var(--text-muted)].",
                "key_components": "Oversized serif typography, thesis callout, author signature, reading time estimate.",
                "responsive_behavior": "Fluid typography scaling for mobile screens maintaining comfortable line length (55-75 chars).",
                "accessibility": "Meets WCAG 2.2 AA text contrast (min 7:1 for editorial typography).",
                "anti_slop_rules": "Zero floating badges or emoji decorations; pure typographic authority."
            }
        ]
    },
    {
        "section_id": "blog_topic_filter_feed",
        "section_name": "Faceted Topic Navigation & Article Feed",
        "archetypes": [
            {
                "archetype_id": "bfeed-01",
                "name": "3-Column Responsive Article Card Grid",
                "keywords": "article-grid, topic-filters, blog-feed, card-grid, pagination",
                "best_for": "Standard company blogs and knowledge bases with 15+ published articles across 4-6 topics.",
                "selection_triggers": {"has_topics": True, "feed_style": "grid"},
                "layout_structure": "Sticky topic filter pill bar (All, Engineering, Product, Culture, Case Studies). Below: 3-column card grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto py-12). Each card: aspect-[16/10] cover, topic badge, publication date, H3 title, 2-line summary, and read-time pill.",
                "typography_specs": "Filter pill: text-xs font-semibold px-3 py-1.5. Card title: text-lg font-bold text-[var(--text-primary)]. Summary: text-sm text-[var(--text-secondary)].",
                "key_components": "Topic filter pills with active state, article card with hover elevation, bookmark/save SVG button, pagination controls.",
                "responsive_behavior": "Filter pills scroll horizontally with snap-x on mobile; grid collapses to single column.",
                "accessibility": "role='tablist' on topic filters; each article card is an <article> with semantic H3.",
                "anti_slop_rules": "Fast client-side filtering with zero layout jump; no infinite scroll without footer access."
            },
            {
                "archetype_id": "bfeed-02",
                "name": "Magazine Horizontal Article Strip List",
                "keywords": "horizontal-cards, magazine-feed, medium-style, clean-reading",
                "best_for": "Publications focused on reading comfort and high-density browsing (similar to Medium or Substack).",
                "selection_triggers": {"feed_style": "horizontal_list"},
                "layout_structure": "Stacked horizontal article rows (max-w-4xl mx-auto divide-y divide-[var(--border-subtle)] py-8). Each row: Left col: Author chip, publish date, bold title, excerpt, tags. Right col: Compact aspect-square thumbnail (96x96 or 120x120).",
                "typography_specs": "Title: text-xl font-bold text-[var(--text-primary)]. Excerpt: text-sm text-[var(--text-secondary)] line-clamp-2. Meta: text-xs font-mono.",
                "key_components": "Horizontal card flex container, compact thumbnail, reading time pill, bookmark trigger.",
                "responsive_behavior": "Thumbnail moves to top or maintains compact 80x80 size on mobile.",
                "accessibility": "Links contain descriptive title text; bookmark button has accessible aria-label.",
                "anti_slop_rules": "No animated text truncation glitches; use clean CSS line-clamp-2."
            },
            {
                "archetype_id": "bfeed-03",
                "name": "High-Density Chronological Index",
                "keywords": "chronological-index, archive, date-ledger, minimalist-feed",
                "best_for": "Developer documentation blogs, security changelogs, and research archives.",
                "selection_triggers": {"feed_style": "archive/changelog"},
                "layout_structure": "Clean table or stacked list grouped by Year (e.g. '2026', '2025'). Each entry: Date in monospace on left, article title in center with hover underline, topic tag and read time on right.",
                "typography_specs": "Year header: text-sm font-mono font-bold text-[var(--primary)]. Date: text-xs font-mono text-[var(--text-muted)]. Title: text-base font-medium.",
                "key_components": "Year anchors, 3-column row, hover background tint, topic tag chips.",
                "responsive_behavior": "Stacks date above title on mobile screens.",
                "accessibility": "Semantic <ol> or <dl> with clear date-title association.",
                "anti_slop_rules": "Zero unnecessary decorative graphics; maximum reading efficiency."
            }
        ]
    },
    {
        "section_id": "blog_newsletter_capture",
        "section_name": "In-Feed Newsletter & Knowledge Capture",
        "archetypes": [
            {
                "archetype_id": "bnews-01",
                "name": "Full-Width High-Contrast Knowledge Card",
                "keywords": "newsletter-signup, email-capture, lead-magnet, subscriber-card",
                "best_for": "Growing an organic email subscriber base of industry practitioners and executives.",
                "selection_triggers": {"has_newsletter": True},
                "layout_structure": "Elevated centered card (max-w-4xl mx-auto py-12 px-8 sm:px-12 rounded-3xl bg-[var(--surface-raised)] border border-[var(--border-subtle)] my-16 text-center). Headline, subscriber count proof ('Join 35,000+ engineers'), single-field email input with embedded submit button, zero-spam micro-guarantee.",
                "typography_specs": "Title: text-2xl sm:text-3xl font-bold text-[var(--text-primary)]. Subtitle: text-sm text-[var(--text-secondary)]. Input: text-sm py-2.5 px-4.",
                "key_components": "Email input, submit action button with loading state, subscriber count chip, privacy guarantee text ('No spam. Unsubscribe anytime with 1 click').",
                "responsive_behavior": "Input and button stack vertically on mobile with full width.",
                "accessibility": "Explicit <label for='newsletter-email'> (can be visually hidden), aria-required='true', aria-invalid error state messaging.",
                "anti_slop_rules": "No deceptive dark patterns ('No, I hate learning' cancel buttons); clean, dignified opt-in."
            },
            {
                "archetype_id": "bnews-02",
                "name": "Split Curated Digest Box with RSS Fallback",
                "keywords": "split-newsletter, weekly-digest, rss-feed, curated-dispatch",
                "best_for": "Technical blogs catering to senior engineers and developers who value RSS and curated digests.",
                "selection_triggers": {"has_newsletter": True, "target": "developers"},
                "layout_structure": "2-column split card. Left: 'The Weekly Dispatch' + bullet list of 3 recent exclusive deep dives sent to subscribers. Right: Email subscription form + direct RSS feed link button.",
                "typography_specs": "Title: text-xl font-bold. Bullet items: text-xs font-medium text-[var(--text-secondary)]. RSS link: text-xs font-mono text-[var(--primary)].",
                "key_components": "Curated issue preview list, email form, RSS XML feed icon link, frequency note ('Every Tuesday at 9am EST').",
                "responsive_behavior": "Stacks vertically on mobile with preview list above form.",
                "accessibility": "RSS link has aria-label='Subscribe via RSS XML feed (opens in reader)'.",
                "anti_slop_rules": "Specify exact sending frequency and topic scope so users know what they are subscribing to."
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
    for new_sec in BLOG_SECTIONS:
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
