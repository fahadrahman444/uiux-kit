#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚠️  DEPRECATED — DO NOT RUN THIS SCRIPT DIRECTLY  ⚠️

This file only contains 12 of the 15 canonical sections.
Running it will OVERWRITE section-archetypes.json and section-archetypes.csv,
silently DESTROYING the 3 additional sections (why_choose_us, results_metrics, team)
and reverting the dataset from 106 to 72 archetypes.

Canonical rebuild tool (all 15 sections, 106 archetypes):
  python add_missing_sections.py

If you need to add new sections or archetypes, edit add_missing_sections.py instead.
"""
import sys
raise SystemExit(
    "\n[BLOCKED] build_section_dataset.py is OUTDATED (12 sections only).\n"
    "Use add_missing_sections.py to rebuild the full 15-section, 106-archetype dataset.\n"
)

# ---- ARCHIVED CODE BELOW — DO NOT USE ----
# Original script preserved for reference only.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Master Section Archetypes Dataset for UI/UX Pro Max.
Generates both:
- data/section-archetypes.json (rich structured metadata for prompt generator)
- data/section-archetypes.csv  (tabular format for BM25 search engine)
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SECTIONS_DATA = [
    # 01. Navbar / Header
    {
        "section_id": "navbar",
        "section_name": "Navbar / Header",
        "archetypes": [
            {
                "archetype_id": "nav-01",
                "name": "Minimal Floating Pill",
                "keywords": "floating, pill, minimal, rounded, compact, sticky, glassmorphism",
                "best_for": "Modern SaaS, design studios, portfolios, sites with < 5 navigation links.",
                "selection_triggers": {"link_count": "3-5", "brand_tier": "modern/creative", "cta_style": "compact"},
                "layout_structure": "Fixed/sticky floating container centered horizontally with max-w-4xl, rounded-full, px-6 py-2.5, backdrop-blur-md.",
                "typography_specs": "Links: text-sm font-medium tracking-normal. Brand: text-sm font-semibold or monospaced icon.",
                "key_components": "Logo, 3-5 links, compact pill primary CTA button.",
                "responsive_behavior": "Collapses to pill with logo + compact hamburger trigger; drawer expands downwards as floating card.",
                "accessibility": "role='navigation', aria-label='Primary Navigation', 2px focus ring with 2px offset.",
                "anti_slop_rules": "No screaming gradient borders, no 50px excessive blurs that lag scroll performance."
            },
            {
                "archetype_id": "nav-02",
                "name": "Full-Width Enterprise Edge-to-Edge",
                "keywords": "full-width, enterprise, clean, border-bottom, traditional, corporate",
                "best_for": "B2B SaaS, enterprise platforms, professional agencies with 5-8 primary links.",
                "selection_triggers": {"link_count": "5-8", "brand_tier": "enterprise/b2b", "cta_style": "dual"},
                "layout_structure": "Full-width w-full h-16 sm:h-20 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]/90 backdrop-blur-sm px-6 lg:px-12 flex items-center justify-between.",
                "typography_specs": "Links: text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)].",
                "key_components": "Brand logo, center navigation links with subtle underline indicator on active, right button group (Login + Primary CTA).",
                "responsive_behavior": "Desktop flex row; mobile displays right-side slide-over sheet (BottomSheet / Drawer).",
                "accessibility": "Skip-to-content link preceding header; keyboard tab sequence preserved.",
                "anti_slop_rules": "No raw emoji navigation items, no animated gradient text."
            },
            {
                "archetype_id": "nav-03",
                "name": "Mega-Menu Gateway",
                "keywords": "mega-menu, multi-column, categories, rich-dropdown, services-catalog",
                "best_for": "Agencies with deep services (SEO, PPC, Web Dev, Branding) and rich content resources.",
                "selection_triggers": {"link_count": "8+", "service_depth": "deep", "has_subcategories": True},
                "layout_structure": "Full-width header with relative dropdown triggers opening 2-column or 3-column structured flyout cards with feature highlights.",
                "typography_specs": "Category headers: text-xs font-mono uppercase text-[var(--text-muted)]. Item titles: text-sm font-semibold.",
                "key_components": "Category icons (20x20 SVG), descriptive micro-copy per link, featured case study badge in right column.",
                "responsive_behavior": "Mobile transforms to nested collapsible accordion list with chevron indicators.",
                "accessibility": "aria-expanded, aria-haspopup='true', Escape key closes active dropdown, arrow keys navigate items.",
                "anti_slop_rules": "No multi-level cascading 3-tier sub-dropdowns that fail hover intent."
            },
            {
                "archetype_id": "nav-04",
                "name": "Action-Split Lead Header",
                "keywords": "lead-gen, emergency, phone, direct-action, high-converting, local-b2b",
                "best_for": "Lead generation agencies, local B2B, performance marketing where direct phone/call action is priority #1.",
                "selection_triggers": {"primary_goal": "phone/lead", "conversion_focus": "ultra-high"},
                "layout_structure": "Left logo, middle confidence badge ('Avg Response: 15 mins' with green pulse dot), right click-to-call + booking CTA.",
                "typography_specs": "Phone: text-sm font-mono font-semibold. CTA: text-sm font-bold.",
                "key_components": "Status indicator dot, phone icon + number link, high-contrast consultation CTA.",
                "responsive_behavior": "Sticky bottom bar appears on mobile with click-to-call and quick inquiry button.",
                "accessibility": "tel: schema formatted correctly, phone target min 44x44px touch target.",
                "anti_slop_rules": "No obnoxious blinking animations; use subtle CSS opacity transition."
            },
            {
                "archetype_id": "nav-05",
                "name": "Drawer / Off-Canvas Editorial Overlay",
                "keywords": "editorial, minimal, hamburger, luxury, fashion, fullscreen-overlay",
                "best_for": "Awwwards-style creative studios, luxury brands, editorial agencies prioritizing visual canvas.",
                "selection_triggers": {"brand_tier": "luxury/editorial", "style": "minimalist"},
                "layout_structure": "Top corner logo and top corner minimal menu trigger ('MENU' / 2-line icon); opens full-viewport modal overlay.",
                "typography_specs": "Overlay links: text-4xl sm:text-6xl font-light tracking-tight hover:italic transition-all.",
                "key_components": "Minimal trigger, full-page overlay with social links and office locations in bottom grid.",
                "responsive_behavior": "Unified interaction across desktop and mobile.",
                "accessibility": "Focus trapped inside modal when open, body scroll locked, aria-modal='true'.",
                "anti_slop_rules": "Maintain quick dismiss button; never hide close button off-screen."
            },
            {
                "archetype_id": "nav-06",
                "name": "Double-Decker Utility Header",
                "keywords": "utility-bar, double-decker, multi-tenant, enterprise, phone-bar",
                "best_for": "Large agencies, international businesses with language switchers, client portals, and secondary links.",
                "selection_triggers": {"has_portal": True, "multi_language": True, "enterprise": True},
                "layout_structure": "Top tier (h-9, subtle bg, text-xs links, client portal login, language switch) + Main tier (h-16, logo, main links, primary CTA).",
                "typography_specs": "Top tier: text-xs text-[var(--text-muted)]. Main tier: text-sm font-medium.",
                "key_components": "Language selector, portal login link, phone number, main nav links, primary CTA.",
                "responsive_behavior": "Top tier hidden on mobile; essential actions consolidated into mobile menu drawer.",
                "accessibility": "Two separate <nav> regions with distinct aria-labels ('Utility Navigation' and 'Primary Navigation').",
                "anti_slop_rules": "Keep top tier strictly secondary; do not crowd with duplicate CTA buttons."
            }
        ]
    },

    # 02. Hero Section
    {
        "section_id": "hero",
        "section_name": "Hero Section",
        "archetypes": [
            {
                "archetype_id": "hero-01",
                "name": "Split-Screen (Text Left / Mockup Right)",
                "keywords": "split-screen, classic-saas, mockup, dashboard-preview, high-converting",
                "best_for": "B2B SaaS, digital agencies with concrete deliverables or dashboard software.",
                "selection_triggers": {"has_mockup": True, "goal": "leads/demo", "layout": "balanced"},
                "layout_structure": "2-column asymmetric grid (lg:grid-cols-12 gap-8 lg:gap-12); Left col (7 cols) text & CTAs; Right col (5 cols) interactive or framed mockup.",
                "typography_specs": "H1: text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight. Subhead: text-lg sm:text-xl text-[var(--text-secondary)].",
                "key_components": "Metadata chip badge, primary CTA + secondary ghost button, avatar trust strip, aspect-ratio reserved mockup container.",
                "responsive_behavior": "Stacks vertically on mobile with text top, mockup below. Container reserves min-height to prevent CLS.",
                "accessibility": "Semantic H1, descriptive alt on mockup or aria-hidden='true' if decorative.",
                "anti_slop_rules": "No purple gradient blobs behind mockup; use grounded border and subtle dark surface."
            },
            {
                "archetype_id": "hero-02",
                "name": "Centered Minimalist Power-Typography",
                "keywords": "centered, big-type, minimalist, copy-first, bold, high-impact",
                "best_for": "Consultancies, design studios, strategic marketing firms with strong punchy messaging.",
                "selection_triggers": {"media_available": "none", "style": "minimalist", "brand_tier": "premium"},
                "layout_structure": "Centered single column max-w-4xl mx-auto py-24 sm:py-32 text-center flex flex-col items-center.",
                "typography_specs": "H1: text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.08]. Subhead: text-lg sm:text-xl max-w-2xl mt-6.",
                "key_components": "Category eyebrow tag, massive H1, centered dual CTA buttons, client logo strip below.",
                "responsive_behavior": "Dynamic fluid typography using clamp() or responsive Tailwind steps (`text-4xl sm:text-6xl lg:text-7xl`).",
                "accessibility": "High contrast ratio (min 7:1 for hero typography on dark or light background).",
                "anti_slop_rules": "No rainbow gradient text fill; use solid white or high-contrast slate."
            },
            {
                "archetype_id": "hero-03",
                "name": "Video / Ambient Canvas Background",
                "keywords": "video-background, ambient, cinema, visual-brand, reel",
                "best_for": "Video agencies, 3D studios, creative event productions, luxury lifestyle brands.",
                "selection_triggers": {"has_video": True, "brand_tier": "luxury/creative"},
                "layout_structure": "Full-height min-h-[85vh] relative flex items-center justify-center overflow-hidden; background video with 50-70% dark scrim.",
                "typography_specs": "H1: text-4xl sm:text-6xl font-semibold tracking-tight text-white. Subhead: text-lg text-slate-200.",
                "key_components": "Compressed webm/mp4 video loop, mute/pause accessibility toggle button in bottom corner, high-contrast white CTA.",
                "responsive_behavior": "Fallback high-res static poster image on mobile or low-power mode.",
                "accessibility": "Mute by default, prefers-reduced-motion pause, accessible play/pause control.",
                "anti_slop_rules": "Never autoplay sound; video must be under 3MB compressed."
            },
            {
                "archetype_id": "hero-04",
                "name": "Interactive Lead Magnet / Input Field",
                "keywords": "input-field, instant-audit, calculator-hero, lead-capture, high-intent",
                "best_for": "SEO agencies (Website URL Audit), PPC agencies (Ad Spend Calculator), high-velocity lead gen.",
                "selection_triggers": {"primary_goal": "direct-lead", "conversion_focus": "instant-action"},
                "layout_structure": "Centered or split layout with an oversized single-field input group embedded directly under the subhead.",
                "typography_specs": "H1: text-4xl sm:text-5xl font-bold. Input placeholder: text-base text-[var(--text-muted)].",
                "key_components": "URL / Email input field with embedded submit button ('Run Free Audit $\\to$'), trust bullet points below input.",
                "responsive_behavior": "Desktop inline horizontal input + button; mobile stacks input and full-width button.",
                "accessibility": "Explicit <label> (visually hidden if needed with sr-only), aria-describedby for error state.",
                "anti_slop_rules": "Do not request 8 form fields in hero; strict 1-field rule."
            },
            {
                "archetype_id": "hero-05",
                "name": "Bento Hero Showcase",
                "keywords": "bento-hero, modular, multi-widget, tech, interactive-cards",
                "best_for": "AI agencies, multi-faceted growth platforms, tech-forward product agencies.",
                "selection_triggers": {"style": "tech/modern", "has_multiple_features": True},
                "layout_structure": "Top headline row + asymmetric 4-tile bento grid directly below (1 large interactive card, 2 metric cards, 1 review card).",
                "typography_specs": "Tile headers: text-base font-semibold. Metric numbers: text-3xl font-mono font-bold.",
                "key_components": "Mini chart widget, testimonial snippet tile, interactive toggle card, live status badge.",
                "responsive_behavior": "Grid shifts from 3 columns desktop to 2 columns tablet to single vertical column mobile.",
                "accessibility": "Each bento tile is an independent article/section with appropriate heading levels.",
                "anti_slop_rules": "No fake glowing purple outlines; use solid 1px border with surface hover lift."
            },
            {
                "archetype_id": "hero-06",
                "name": "Device Frame Carousel / Slider",
                "keywords": "device-mockups, multi-screen, mobile-app, responsive-preview",
                "best_for": "Mobile app developers, cross-platform agencies showcasing UI across phone, tablet, and desktop.",
                "selection_triggers": {"has_app_mockups": True, "target": "cross-platform"},
                "layout_structure": "Centered text on top, floating overlapping device frames (iPhone + iPad + Mac) resting on horizontal shelf below.",
                "typography_specs": "H1: text-4xl sm:text-5xl font-bold text-center.",
                "key_components": "SVG device bezels, screenshots with realistic shadows, subtle hover tilt.",
                "responsive_behavior": "On small screens, secondary devices fade away leaving only the primary mobile phone frame.",
                "accessibility": "Alt text describing what is shown on screen; interactive slider buttons keyboard accessible.",
                "anti_slop_rules": "Ensure realistic bezel dimensions, no skewed funhouse 3D distortion."
            },
            {
                "archetype_id": "hero-07",
                "name": "Social Proof-First Hero",
                "keywords": "trust-first, rating-strip, avatar-stack, high-credibility, verified",
                "best_for": "Competitive markets, B2B agencies where trust is the #1 friction point for buyers.",
                "selection_triggers": {"social_proof_priority": "extreme", "has_reviews": True},
                "layout_structure": "Avatar stack + 5-star rating widget positioned *above* the main headline; H1 centered below, followed by video quote preview.",
                "typography_specs": "Proof banner: text-xs font-semibold. H1: text-4xl sm:text-6xl font-bold.",
                "key_components": "Avatar overlap row (4 real photos), star rating SVG cluster, verified review count text, dual CTA.",
                "responsive_behavior": "Avatars scale down gracefully, headline wraps without orphans.",
                "accessibility": "aria-label='Rated 4.9 out of 5 stars by over 300 verified clients'.",
                "anti_slop_rules": "Real human headshots only; no generic AI-generated stock avatars."
            },
            {
                "archetype_id": "hero-08",
                "name": "Editorial Two-Tone Column",
                "keywords": "editorial, swiss, asymmetrical, serif, high-fashion, architectural",
                "best_for": "Architecture firms, luxury branding studios, editorial magazines, high-end strategy firms.",
                "selection_triggers": {"style": "editorial/swiss", "brand_tier": "luxury"},
                "layout_structure": "Left narrow rail (3 cols) containing project metadata, date, index, and location; Right wide rail (9 cols) with giant typography and single large photograph.",
                "typography_specs": "Left rail: text-xs font-mono uppercase tracking-widest. Main title: text-5xl sm:text-7xl font-serif italic/regular mix.",
                "key_components": "Monospaced index indicators, thin 1px dividing rules, high-contrast monochrome palette.",
                "responsive_behavior": "Left rail stacks on top as an eyebrow badge bar on mobile.",
                "accessibility": "Strict semantic heading levels; high contrast ratio exceeding 7:1.",
                "anti_slop_rules": "No rounded button bubbles; sharp 0px or 2px radius strictly enforced."
            },
            {
                "archetype_id": "hero-09",
                "name": "Interactive 3D / WebGL Canvas Hero",
                "keywords": "3d, webgl, spline, threejs, interactive, cutting-edge",
                "best_for": "Next-gen tech startups, WebGL creative agencies, hardware/AI ventures.",
                "selection_triggers": {"has_3d_asset": True, "style": "cutting-edge"},
                "layout_structure": "Left floating content card; right full-bleed interactive 3D model reacting to pointer move.",
                "typography_specs": "H1: text-4xl sm:text-5xl font-mono or modern geometric sans.",
                "key_components": "Canvas container with loading fallback, interactive 3D object, pointer inertia listener.",
                "responsive_behavior": "3D canvas disabled or replaced with static SVG/WebP preview on low-power/mobile devices.",
                "accessibility": "Skip button for keyboard users; canvas marked aria-hidden='true' with text equivalent.",
                "anti_slop_rules": "Must maintain 60 FPS; fall back to WebP on mobile to prevent phone overheating."
            },
            {
                "archetype_id": "hero-10",
                "name": "Problem vs Solution Split Hero",
                "keywords": "before-after, problem-solution, comparison, conversion, cro",
                "best_for": "Performance agencies, conversion rate optimizers, turnaround consultancies.",
                "selection_triggers": {"goal": "contrast/cro", "focus": "transformation"},
                "layout_structure": "Centered value proposition with dual split cards directly below: Left card 'The Old Way' (muted/grey), Right card 'The Agency Way' (vibrant/highlighted).",
                "typography_specs": "Card headers: text-sm font-mono uppercase. Bullets: text-sm font-medium.",
                "key_components": "Red cross icons vs green checkmark icons, contrast metrics, direct booking CTA.",
                "responsive_behavior": "Side-by-side on desktop, stacks with 'The Old Way' first, 'The Agency Way' second on mobile.",
                "accessibility": "Screen reader text distinguishes problem list from solution list clearly.",
                "anti_slop_rules": "Keep comparison factual and quantitative; avoid dramatic hyperbole."
            }
        ]
    },

    # 03. Trusted By / Client Logos
    {
        "section_id": "trusted_by",
        "section_name": "Trusted By / Social Proof Logos",
        "archetypes": [
            {
                "archetype_id": "tb-01",
                "name": "Infinite Greyscale Marquee",
                "keywords": "marquee, continuous-scroll, ticker, logo-train, modern",
                "best_for": "Agencies with 8 to 20+ recognizable client logos.",
                "selection_triggers": {"logo_count": "8+", "style": "modern/tech"},
                "layout_structure": "Full-width overflow-hidden relative py-8 border-y border-[var(--border-subtle)]; CSS translateX animation running continuously.",
                "typography_specs": "Section title: text-xs font-mono uppercase tracking-widest text-center mb-6 text-[var(--text-muted)].",
                "key_components": "CSS keyframe continuous marquee, left and right linear gradient fade masks (mask-image).",
                "responsive_behavior": "Same layout on mobile; speed adjusted slightly for small viewport width.",
                "accessibility": "Pause on hover and pause when prefers-reduced-motion is active.",
                "anti_slop_rules": "All logos normalized to single monochrome color (slate-400/500) and equal visual height (24-32px)."
            },
            {
                "archetype_id": "tb-02",
                "name": "Static Balanced Grid (High-Trust)",
                "keywords": "static-grid, prestigious, fortune500, clean, enterprise",
                "best_for": "High-end agencies with 4 to 8 prestigious blue-chip client logos.",
                "selection_triggers": {"logo_count": "4-8", "brand_tier": "enterprise"},
                "layout_structure": "max-w-6xl mx-auto grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-8 items-center justify-items-center py-12.",
                "typography_specs": "Title: text-xs font-mono uppercase tracking-wider text-[var(--text-muted)].",
                "key_components": "Static SVG logos with 50% opacity, transitioning to 100% on individual logo hover.",
                "responsive_behavior": "Neat 2-column or 3-column grid on mobile; zero overflow.",
                "accessibility": "Each logo has descriptive alt text (e.g., 'Stripe logo').",
                "anti_slop_rules": "Never use rainbow colored logos; strict single-tint saturation."
            },
            {
                "archetype_id": "tb-03",
                "name": "Logo + Key Outcome Pill",
                "keywords": "logo-outcome, proof-metrics, verified-results, high-intent",
                "best_for": "B2B performance agencies where client logos need immediate proof backing.",
                "selection_triggers": {"has_metrics": True, "goal": "conversion"},
                "layout_structure": "Grid of 3 or 4 cards; each card contains the client logo at top and a bold result stat below (e.g., '+180% Inbound SQLs').",
                "typography_specs": "Stat: text-xl font-bold text-[var(--text-primary)]. Description: text-xs text-[var(--text-muted)].",
                "key_components": "Client SVG logo, metric badge, 1-line case study link.",
                "responsive_behavior": "Horizontal carousel or 1-column stack on mobile.",
                "accessibility": "Screen reader announces: 'Client Stripe achieved 180% inbound growth'.",
                "anti_slop_rules": "All stats must be verifiable, no fabricated round numbers."
            },
            {
                "archetype_id": "tb-04",
                "name": "Press & Media Mentions with Pull Quotes",
                "keywords": "press, media, forbes, techcrunch, quotes, authority",
                "best_for": "Startups and agencies featured in major publications.",
                "selection_triggers": {"has_press": True, "type": "authority"},
                "layout_structure": "Row of 3 publication logos (TechCrunch, Forbes, Bloomberg); clicking or viewing shows the exact pull quote beneath.",
                "typography_specs": "Quote: text-sm sm:text-base font-serif italic text-[var(--text-secondary)].",
                "key_components": "Publication logo, italic quote snippet, external verification link.",
                "responsive_behavior": "Stacked vertically on mobile with divider lines.",
                "accessibility": "External links have aria-label and rel='noopener noreferrer'.",
                "anti_slop_rules": "No fake press badges without real article citations."
            },
            {
                "archetype_id": "tb-05",
                "name": "Interactive Client Work Hover Reveal",
                "keywords": "interactive-logos, hover-reveal, work-snippet, portfolio-teaser",
                "best_for": "Design agencies where each client logo links directly to their case study.",
                "selection_triggers": {"has_case_studies": True, "style": "interactive"},
                "layout_structure": "Row of client logos; hovering a logo displays a dynamic floating preview card of the website built for them.",
                "typography_specs": "Hover card title: text-sm font-semibold. Category: text-xs font-mono.",
                "key_components": "SVG logo button, floating tooltip/popover preview card with project thumbnail.",
                "responsive_behavior": "On touch devices, tap opens the case study directly without hover state.",
                "accessibility": "Full keyboard focus reveals preview card, Esc closes.",
                "anti_slop_rules": "Keep preview card render lightweight; preload images."
            },
            {
                "archetype_id": "tb-06",
                "name": "Security, Compliance & ISO Badges",
                "keywords": "security, compliance, soc2, iso, gdpr, hipaa, trust",
                "best_for": "Fintech, healthtech, and enterprise software agencies requiring formal security validation.",
                "selection_triggers": {"compliance_required": True, "enterprise": True},
                "layout_structure": "Side-by-side dual strip: Left client brand logos; Right formal compliance seals (SOC2 Type II, ISO 27001, GDPR).",
                "typography_specs": "Badges label: text-xs font-mono font-semibold text-emerald-600 dark:text-emerald-400.",
                "key_components": "Security shield icons, verification date badge, audit report link.",
                "responsive_behavior": "Stacks into two distinct sub-sections on mobile.",
                "accessibility": "Compliance status explicitly declared in aria-description.",
                "anti_slop_rules": "Do not mix playful emojis with formal compliance seals."
            }
        ]
    },

    # 04. About / Who We Are
    {
        "section_id": "about",
        "section_name": "About / Who We Are",
        "archetypes": [
            {
                "archetype_id": "abt-01",
                "name": "Editorial Founder Story & Signature",
                "keywords": "founder-story, letter, signature, boutique, authentic, mission",
                "best_for": "Boutique agencies, founder-led studios, high-trust consulting practices.",
                "selection_triggers": {"founder_led": True, "brand_tier": "boutique"},
                "layout_structure": "2-column layout: Left column candid high-res founder portrait with location/bio pill; Right column personal manifesto letter with SVG signature.",
                "typography_specs": "Manifesto headline: text-3xl font-serif font-normal. Body: text-base leading-relaxed. Signature: SVG vector.",
                "key_components": "Founder portrait, pull-quote block, handwritten SVG signature, credentials badges.",
                "responsive_behavior": "Portrait stacks above letter on mobile with consistent 24px spacing.",
                "accessibility": "Portrait has descriptive alt text; signature has aria-label='Founder signature'.",
                "anti_slop_rules": "No fake AI-generated corporate headshots; real candid photo only."
            },
            {
                "archetype_id": "abt-02",
                "name": "Split Mission & Asymmetric Metric Cards",
                "keywords": "split-mission, company-stats, asymmetric, enterprise-about",
                "best_for": "Growing agencies (15-50 people) with tangible milestone numbers.",
                "selection_triggers": {"has_milestones": True, "company_size": "medium"},
                "layout_structure": "Left column bold mission statement + core values accordion; Right column 2x2 asymmetric stat card cluster.",
                "typography_specs": "Mission H2: text-3xl sm:text-4xl font-bold tracking-tight. Stat numbers: text-4xl font-extrabold.",
                "key_components": "Value bullets with stroke checkmarks, raised surface stat cards with subtle borders.",
                "responsive_behavior": "Grid collapses to single column on mobile.",
                "accessibility": "Headings follow strict H2 -> H3 nesting.",
                "anti_slop_rules": "No hollow corporate buzzwords ('synergistic paradigm shifts')."
            },
            {
                "archetype_id": "abt-03",
                "name": "Interactive Timeline / Evolution Story",
                "keywords": "timeline, company-history, evolution, milestones, years",
                "best_for": "Established agencies celebrating 5 to 15+ years of industry leadership.",
                "selection_triggers": {"years_operating": "5+", "story_focus": "history"},
                "layout_structure": "Vertical central spine with alternating year cards (2018 -> 2021 -> 2024 -> Today) showing pivotal pivots.",
                "typography_specs": "Year: text-2xl font-mono font-bold text-[var(--color-primary)]. Event title: text-lg font-semibold.",
                "key_components": "Connecting line with node dots, milestone cards, historical photography thumbnails.",
                "responsive_behavior": "Shifts to single left-aligned vertical line on mobile with cards on right.",
                "accessibility": "Timeline ordered sequentially in DOM (<ol> and <li>).",
                "anti_slop_rules": "Keep entries strictly limited to 4-5 major milestones; do not document every minor date."
            },
            {
                "archetype_id": "abt-04",
                "name": "Culture & Office Atmosphere Bento Grid",
                "keywords": "culture, office-photos, team-bento, behind-the-scenes",
                "best_for": "Agencies hiring top talent and pitching clients who value strong team culture.",
                "selection_triggers": {"has_office_photos": True, "goal": "culture/hiring"},
                "layout_structure": "Asymmetric bento grid of 5 cards: 3 candid office/workshop photos, 1 core philosophy quote card, 1 team stat card.",
                "typography_specs": "Philosophy text: text-xl font-medium tracking-tight.",
                "key_components": "Rounded image frames (rounded-2xl), subtle inner shadow, location tag badge ('San Francisco & London').",
                "responsive_behavior": "Bento reflows smoothly to 2 columns on tablet, single column on phone.",
                "accessibility": "All images have complete contextual alt tags.",
                "anti_slop_rules": "Zero generic handshake stock photos."
            },
            {
                "archetype_id": "abt-05",
                "name": "Philosophy Manifesto (Typography-First)",
                "keywords": "manifesto, big-text, swiss, philosophy, no-images",
                "best_for": "Intellectual, high-craft design and development agencies with no photo assets.",
                "selection_triggers": {"media_available": "none", "style": "editorial"},
                "layout_structure": "Oversized paragraph text with highlighted keywords, structured into 3 core beliefs (01 / 02 / 03).",
                "typography_specs": "Belief statement: text-2xl sm:text-3xl font-medium leading-relaxed. Eyebrow: text-xs font-mono uppercase.",
                "key_components": "Numbered anchors (`01`, `02`, `03`), subtle horizontal rules dividing beliefs.",
                "responsive_behavior": "Fluid responsive font sizing preserving line-length between 45-75 characters.",
                "accessibility": "Meets WCAG 2.2 AA text contrast (min 4.5:1, target 7:1).",
                "anti_slop_rules": "No purple glowing text highlights; use high-contrast foreground color changes."
            },
            {
                "archetype_id": "abt-06",
                "name": "Video Manifesto / Mini-Documentary",
                "keywords": "video-manifesto, documentary, agency-film, leadership",
                "best_for": "High-end agencies with a produced 60-90 second brand film.",
                "selection_triggers": {"has_video": True, "brand_tier": "flagship"},
                "layout_structure": "Left column brief text summary and CTA; Right column 16:9 custom video player with play trigger and runtime badge ('1:20 min').",
                "typography_specs": "H2: text-3xl font-bold. Runtime badge: text-xs font-mono.",
                "key_components": "Custom video thumbnail with play button overlay, modal video lightbox trigger.",
                "responsive_behavior": "Video player fills full width on mobile.",
                "accessibility": "Closed captions (VTT) provided, accessible video player controls.",
                "anti_slop_rules": "No autoplaying video with sound; user-initiated only."
            }
        ]
    },

    # 05. Services Section
    {
        "section_id": "services",
        "section_name": "Services Section",
        "archetypes": [
            {
                "archetype_id": "srv-01",
                "name": "3-Column Feature Cards",
                "keywords": "3-column, cards, classic, scannable, icons, deliverables",
                "best_for": "Standard agencies offering 3, 6, or 9 structured services.",
                "selection_triggers": {"service_count": "3-6", "style": "clean"},
                "layout_structure": "Standard 3-column grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8`).",
                "typography_specs": "Service title: text-xl font-semibold. Body: text-sm leading-relaxed text-[var(--text-secondary)].",
                "key_components": "SVG icon container (p-3 rounded-xl bg-primary/10), title, 3-bullet deliverables list, 'Learn more $\\to$' link.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 3 columns desktop.",
                "accessibility": "Cards use semantic <article>, links have descriptive aria-labels.",
                "anti_slop_rules": "No cartoonish 3D emoji icons; use precision 1.5px stroke SVG icons."
            },
            {
                "archetype_id": "srv-02",
                "name": "Interactive Hover List with Floating Image Reveal",
                "keywords": "hover-reveal, floating-image, modern-agency, sleek, editorial",
                "best_for": "Creative studios, Awwwards-style agencies offering 4 to 8 high-craft services.",
                "selection_triggers": {"style": "creative/editorial", "service_count": "4-8"},
                "layout_structure": "Vertical list of services separated by 1px borders; hovering any item causes a smooth floating preview thumbnail to follow the cursor.",
                "typography_specs": "Service title: text-3xl sm:text-5xl font-light hover:translate-x-3 transition-transform.",
                "key_components": "Cursor-tracking floating image container (fixed pointer-events-none), service number index, category tag.",
                "responsive_behavior": "Floating hover image disabled on touch screens; thumbnail appears statically beneath item title.",
                "accessibility": "Full keyboard focus highlights row and displays thumbnail natively.",
                "anti_slop_rules": "Ensure pointer-events-none on floating image so it never blocks click events."
            },
            {
                "archetype_id": "srv-03",
                "name": "Bento Grid Hierarchy (Flagship + Satellites)",
                "keywords": "bento-services, flagship, hero-tile, modular",
                "best_for": "Agencies with 1 primary flagship service (e.g., SEO/Growth) and 3-4 supporting services.",
                "selection_triggers": {"has_flagship_service": True, "style": "modern"},
                "layout_structure": "Asymmetric 12-column grid: 1 large 7-column card showcasing core service with live diagram, paired with two 5-column satellite cards.",
                "typography_specs": "Flagship title: text-2xl font-bold. Satellite title: text-lg font-semibold.",
                "key_components": "Embedded mini-interactive widget in flagship card, deliverable pills, micro-CTA.",
                "responsive_behavior": "Reflows to single column stack on mobile.",
                "accessibility": "Each bento cell has unique H3 landmark.",
                "anti_slop_rules": "No shiny purple borders or rainbow gradients on cards."
            },
            {
                "archetype_id": "srv-04",
                "name": "Tabbed Interactive Switcher",
                "keywords": "tabs, interactive-switcher, deep-dive, compact, no-scroll",
                "best_for": "Agencies with deep, technical services requiring detailed explanations without making the page too long.",
                "selection_triggers": {"service_depth": "deep", "wants_compact": True},
                "layout_structure": "Top horizontal tab buttons (or left vertical rail); clicking a tab updates the active right panel with deliverables, tech stack, and case study snippet.",
                "typography_specs": "Tab label: text-sm font-semibold. Panel title: text-2xl font-bold.",
                "key_components": "Accessible tab list (`role='tablist'`), active pill indicator with CSS layout transition, deliverables checklist.",
                "responsive_behavior": "Transforms into a vertical accordion on mobile screens for easy thumb tapping.",
                "accessibility": "role='tablist', role='tab', aria-selected='true', left/right arrow key navigation.",
                "anti_slop_rules": "Ensure instant state changes (<50ms) without jarring layout shifts."
            },
            {
                "archetype_id": "srv-05",
                "name": "Horizontal Scrolling Card Shelf",
                "keywords": "horizontal-scroll, carousel, card-shelf, touch-friendly",
                "best_for": "Agencies targeting mobile-heavy audiences or showcasing 6+ service packages.",
                "selection_triggers": {"service_count": "6+", "mobile_heavy": True},
                "layout_structure": "Full-bleed horizontal scrolling track with snap-mandatory scrolling; navigation arrows on top right.",
                "typography_specs": "Card title: text-xl font-bold. Price tag: text-sm font-mono.",
                "key_components": "Snap-start card containers, left/right arrow buttons, scroll progress indicator bar.",
                "responsive_behavior": "Native touch scroll on mobile with CSS scroll-snap-type: x mandatory.",
                "accessibility": "Keyboard accessible previous/next buttons, aria-roledescription='carousel'.",
                "anti_slop_rules": "Never hijack vertical mousewheel scrolling unless explicitly opted-in."
            },
            {
                "archetype_id": "srv-06",
                "name": "Productized Service Scope Drawer",
                "keywords": "productized, scope, fixed-price, drawer, transparent",
                "best_for": "Designjoy-style productized agencies with fixed scopes and rapid turnarounds.",
                "selection_triggers": {"is_productized": True, "transparent_scope": True},
                "layout_structure": "Grid of structured service boxes with 'What's Included' checklist and 'View Full Scope' trigger that opens a Slide-Over Sheet.",
                "typography_specs": "Turnaround badge: text-xs font-mono font-bold text-emerald-500. Title: text-xl font-bold.",
                "key_components": "Turnaround time pill ('48h turnaround'), checkmark scope list, sheet drawer trigger.",
                "responsive_behavior": "Sheet opens full width on mobile.",
                "accessibility": "Focus management inside drawer; Escape key dismisses.",
                "anti_slop_rules": "Clearly delineate what is NOT included to prevent client scope creep."
            },
            {
                "archetype_id": "srv-07",
                "name": "Service Capability Matrix Table",
                "keywords": "table, matrix, comparison, detailed-deliverables",
                "best_for": "Enterprise IT, technical SEO, and cyber security agencies with exhaustive deliverable matrices.",
                "selection_triggers": {"enterprise": True, "deliverable_density": "high"},
                "layout_structure": "Structured data table with sticky header row; service categories on left, deliverable checkmarks and SLAs across columns.",
                "typography_specs": "Headers: text-xs font-mono uppercase text-[var(--text-muted)]. Cells: text-sm.",
                "key_components": "Checkmarks, SLA tags ('Same-day', 'Weekly'), downloadable PDF scope button.",
                "responsive_behavior": "Horizontal overflow scroll container with subtle shadow indicators on table edges.",
                "accessibility": "Strict table markup (<thead>, <tbody>, <th scope='col'>, <th scope='row'>).",
                "anti_slop_rules": "Ensure high-contrast borders; no low-contrast faint grey lines."
            },
            {
                "archetype_id": "srv-08",
                "name": "Terminal / Code-Style Deliverables Block",
                "keywords": "terminal, developer, engineering, devops, technical",
                "best_for": "Web3, DevOps, engineering, and API development agencies targeting CTOs.",
                "selection_triggers": {"target_audience": "developers/ctos", "style": "technical"},
                "layout_structure": "Dark simulated terminal window with traffic light buttons (red, yellow, green) and monospaced command outputs detailing agency stack.",
                "typography_specs": "Font: JetBrains Mono or Fira Code, text-sm leading-relaxed.",
                "key_components": "Simulated bash prompt (`$ agency deploy --stack full`), syntax-highlighted service JSON output.",
                "responsive_behavior": "Wraps cleanly with overflow-x-auto on small screens.",
                "accessibility": "role='region', aria-label='Interactive Technical Deliverables Terminal'.",
                "anti_slop_rules": "No fake typing animations that take 10 seconds to read; render immediately."
            }
        ]
    },

    # 07. How We Work / Process (12 Archetypes from post.txt)
    {
        "section_id": "how_we_work",
        "section_name": "How We Work / Our Process",
        "archetypes": [
            {
                "archetype_id": "hww-01",
                "name": "Horizontal Timeline",
                "keywords": "horizontal-timeline, linear, simple, connecting-lines, numbers",
                "best_for": "Simple 3-4 step linear processes with concise explanations.",
                "selection_triggers": {"step_count": "3-4", "media_available": "none", "complexity": "low"},
                "layout_structure": "Horizontal 4-column row linked by connecting line with step nodes and directional arrows.",
                "typography_specs": "Step number: text-sm font-mono font-bold text-primary. Title: text-lg font-semibold.",
                "key_components": "Connecting horizontal line, circular step node icons, title, 2-line description.",
                "responsive_behavior": "Converts cleanly to vertical stepper on mobile (`PatternStepper.tsx`).",
                "accessibility": "Wrapped in <ol> and <li> list with aria-label='Process steps'.",
                "anti_slop_rules": "No neon glowing connector lines; use clean 1px border with primary accent dot."
            },
            {
                "archetype_id": "hww-02",
                "name": "Vertical Timeline",
                "keywords": "vertical-timeline, storytelling, alternating, detailed-steps",
                "best_for": "5-6 steps where each stage has deeper storytelling and requires breathing room.",
                "selection_triggers": {"step_count": "5-6", "has_descriptions": True},
                "layout_structure": "Central vertical spine line with alternating step cards on left and right.",
                "typography_specs": "Timeline node: text-sm font-mono. Step title: text-xl font-bold.",
                "key_components": "Vertical dashed/solid spine, node badges, alternating content cards.",
                "responsive_behavior": "Spine shifts to left edge on mobile with all content cards aligned right.",
                "accessibility": "DOM order is sequential regardless of left/right visual alternation.",
                "anti_slop_rules": "Avoid large empty whitespace gaps between alternating cards."
            },
            {
                "archetype_id": "hww-03",
                "name": "Card Grid Layout",
                "keywords": "card-grid, professional, icons, structured, uniform",
                "best_for": "Clean, corporate, professional agencies wanting uniform balanced layout.",
                "selection_triggers": {"step_count": "4", "style": "corporate/clean"},
                "layout_structure": "2x2 or 4x1 grid of identical structured cards with step pill, icon, title, description.",
                "typography_specs": "Step pill: text-xs font-mono font-semibold. Title: text-lg font-bold.",
                "key_components": "Raised surface cards, 1px subtle borders, icon container, step number badge.",
                "responsive_behavior": "Single column mobile, 2 columns tablet, 4 columns desktop.",
                "accessibility": "Standard grid semantics with semantic heading levels.",
                "anti_slop_rules": "No mismatched card heights; use CSS flex-1 or grid stretch."
            },
            {
                "archetype_id": "hww-04",
                "name": "Big Number Typography",
                "keywords": "big-numbers, oversized-type, 01-02-03, premium, modern",
                "best_for": "Modern, premium agencies with short, confident copy and high visual impact.",
                "selection_triggers": {"step_count": "3-4", "style": "modern/premium", "copy_length": "short"},
                "layout_structure": "4-column grid dominated by giant oversized `01`, `02`, `03`, `04` numerals anchored above minimal titles.",
                "typography_specs": "Numeral: text-6xl sm:text-7xl font-extrabold text-[var(--border-subtle)] hover:text-primary transition-colors.",
                "key_components": "Oversized typography numerals, micro-tag pill, bold title, concise summary.",
                "responsive_behavior": "Numerals scale down gracefully using responsive font sizing.",
                "accessibility": "Numerals marked aria-hidden='true' if redundant to semantic list index.",
                "anti_slop_rules": "Keep numerals legible; do not use unreadable decorative scripts."
            },
            {
                "archetype_id": "hww-05",
                "name": "Workflow Diagram / Node Graph",
                "keywords": "workflow-diagram, nodes, arrows, complex-process, engineering",
                "best_for": "Complex technical processes involving feedback loops, branching, or multiple stakeholders.",
                "selection_triggers": {"is_non_linear": True, "technical": True},
                "layout_structure": "Interactive SVG flowchart showing nodes (Client Input -> AI Analysis -> Human Craft -> QA Audit) with active signal pulses.",
                "typography_specs": "Node labels: text-xs font-mono font-bold. Tooltips: text-xs.",
                "key_components": "SVG bezier connection paths, interactive node pills, status indicator badges.",
                "responsive_behavior": "Horizontal panning viewport or simplified linear node list on mobile.",
                "accessibility": "Provides accessible text table alternative for screen readers (`sr-only`).",
                "anti_slop_rules": "No chaotic spaghetti line connections; strictly orthogonal or smooth beziers."
            },
            {
                "archetype_id": "hww-06",
                "name": "Alternating Image & Text Rows",
                "keywords": "alternating, visual, screenshot-steps, deep-dive",
                "best_for": "Agencies that have real deliverables/screenshots to show for each step.",
                "selection_triggers": {"has_step_images": True, "step_count": "3-5"},
                "layout_structure": "Full-width alternating 2-column rows (Row 1: Image Left / Text Right; Row 2: Text Left / Image Right).",
                "typography_specs": "Step H3: text-2xl font-bold. Step tag: text-xs font-mono text-primary.",
                "key_components": "Step screenshot/illustration frame, deliverables pill cluster, step description.",
                "responsive_behavior": "Always renders image first or text first consistently on mobile.",
                "accessibility": "Images have contextual alt text explaining what deliverable is shown.",
                "anti_slop_rules": "Do not use generic conceptual stock 3D graphics (e.g. floating puzzle pieces)."
            },
            {
                "archetype_id": "hww-07",
                "name": "Horizontal Scroll Runway",
                "keywords": "horizontal-scroll, runway, interactive, awwwards, creative-portfolio",
                "best_for": "Creative studios, Awwwards-style agencies wanting immersive horizontal track exploration.",
                "selection_triggers": {"style": "creative", "immersive": True},
                "layout_structure": "Pinned container with CSS horizontal transform tracking scroll position; large step panels slide into view.",
                "typography_specs": "Step titles: text-4xl sm:text-5xl font-bold.",
                "key_components": "Horizontal scroll track, progress bar indicator, step milestone panels.",
                "responsive_behavior": "Reverts to standard vertical scroll on mobile to avoid scroll-trapping.",
                "accessibility": "Respects prefers-reduced-motion; provides keyboard left/right arrow navigation.",
                "anti_slop_rules": "Never lock user page scroll permanently; provide quick bypass button."
            },
            {
                "archetype_id": "hww-08",
                "name": "Accordion Layout (Progressive Disclosure)",
                "keywords": "accordion, expandable, long-descriptions, dense-steps",
                "best_for": "Processes with 6-8 steps where clients need to read thorough methodology paragraphs.",
                "selection_triggers": {"step_count": "6-8", "text_density": "high"},
                "layout_structure": "Left sticky title and overview; Right stacked accordion rows that expand one at a time.",
                "typography_specs": "Accordion trigger: text-lg font-semibold. Body: text-sm leading-relaxed.",
                "key_components": "Plus/minus or chevron icon with 180deg rotation, expanded content panel with deliverable tags.",
                "responsive_behavior": "Left title stacks above accordion rows on mobile.",
                "accessibility": "aria-expanded, aria-controls, keyboard Enter/Space expansion.",
                "anti_slop_rules": "Ensure smooth CSS height transition without content pop-in."
            },
            {
                "archetype_id": "hww-09",
                "name": "Circular / Loop Process",
                "keywords": "circular, continuous-loop, sprint, agile, recurring",
                "best_for": "Ongoing retainer services (Audit -> Strategy -> Execute -> Analyze -> Repeat).",
                "selection_triggers": {"is_cyclical": True, "retainer_model": True},
                "layout_structure": "Circular diagram with central core hub ('Continuous Growth') and 4-5 orbiting stage nodes with directional arrows.",
                "typography_specs": "Hub text: text-sm font-bold font-mono. Orbiting node: text-sm font-semibold.",
                "key_components": "Central anchor circle, radial dashed connector ring, step badges.",
                "responsive_behavior": "Reorganizes into linear closed loop list with 'Repeat Cycle' banner on mobile.",
                "accessibility": "Accessible linear fallback list declared in HTML.",
                "anti_slop_rules": "Keep SVG math responsive; no clipped text nodes on small viewports."
            },
            {
                "archetype_id": "hww-10",
                "name": "Sticky Scroll Storytelling",
                "keywords": "sticky-scroll, scrollama, fixed-canvas, dynamic-visuals",
                "best_for": "Flagship marketing sites with custom UI previews or interactive graphics for each phase.",
                "selection_triggers": {"has_rich_media": True, "style": "immersive"},
                "layout_structure": "2-column container: Left column scrolls through text steps; Right column stays sticky (`sticky top-24`) and cross-fades matching graphic.",
                "typography_specs": "Step title: text-3xl font-bold. Active indicator: text-xs font-mono font-bold text-primary.",
                "key_components": "Sticky canvas container, intersection observer step triggers, cross-fading graphic layers.",
                "responsive_behavior": "Stacks into standard alternating cards on mobile viewports.",
                "accessibility": "Screen reader reads uninterrupted sequential text without sticky distraction.",
                "anti_slop_rules": "No GPU-choking WebGL shaders; use lightweight CSS opacity transitions."
            },
            {
                "archetype_id": "hww-11",
                "name": "Full-Width Visual Steps",
                "keywords": "full-width, high-visual, atmospheric, background-photos",
                "best_for": "Agencies with high-production video or photo assets of their real team at work.",
                "selection_triggers": {"has_cinematic_photos": True, "visual_brand": True},
                "layout_structure": "Stacked full-width sections; each step has a dark atmospheric background photo with card overlay.",
                "typography_specs": "Step numeral: text-5xl font-mono text-white/40. Headline: text-3xl font-bold text-white.",
                "key_components": "High-res compressed background photos, dark gradient scrim, glassmorphic content card.",
                "responsive_behavior": "Background photos set to object-cover with centered focal points.",
                "accessibility": "High-contrast text overlay ensuring min 7:1 ratio over photo scrim.",
                "anti_slop_rules": "Ensure photos are heavily compressed (WebP/AVIF under 150kB)."
            },
            {
                "archetype_id": "hww-12",
                "name": "Bento Grid Process",
                "keywords": "bento-process, modular, mixed-media, contemporary, apple-style",
                "best_for": "Modern tech agencies mixing deliverables, tools, timeframes, and descriptions.",
                "selection_triggers": {"style": "contemporary/bento", "has_varied_metadata": True},
                "layout_structure": "4-card or 5-card bento collage: Step 1 is wide hero block; Step 2-4 are compact modular blocks with tool icons.",
                "typography_specs": "Card title: text-xl font-bold. Metadata tag: text-xs font-mono.",
                "key_components": "Tool stack icons (Figma, Next.js), timeframe badge ('Days 1-3'), checklist items.",
                "responsive_behavior": "Reflows into a single column on mobile.",
                "accessibility": "Numbered step progression clearly indicated in heading text.",
                "anti_slop_rules": "No noisy gradient borders; clean dark slate surface with 1px border."
            }
        ]
    },

    # 08. Portfolio / Case Studies
    {
        "section_id": "portfolio",
        "section_name": "Portfolio / Case Studies",
        "archetypes": [
            {
                "archetype_id": "port-01",
                "name": "Masonry Visual Grid",
                "keywords": "masonry, visual, agency-work, varied-heights, creative",
                "best_for": "Design agencies with stunning, varied visual assets across web, mobile, and branding.",
                "selection_triggers": {"visual_quality": "high", "has_varied_dimensions": True},
                "layout_structure": "2 or 3-column masonry grid with staggered card heights and smooth hover zoom.",
                "typography_specs": "Project title: text-xl font-bold. Category tag: text-xs font-mono uppercase.",
                "key_components": "Rounded image frame, category badge, subtle hover scale (`scale-[1.02]`), case study link.",
                "responsive_behavior": "Collapses to single column on mobile.",
                "accessibility": "Descriptive alt text for all portfolio imagery; keyboard focus ring on card.",
                "anti_slop_rules": "No blurry thumbnail images; use crisp WebP assets."
            },
            {
                "archetype_id": "port-02",
                "name": "Metric-First Case Study Cards",
                "keywords": "metric-first, roi-cards, performance, stats, b2b-results",
                "best_for": "Performance marketing, SEO, and CRO agencies where business outcomes matter most.",
                "selection_triggers": {"goal": "roi/performance", "has_metrics": True},
                "layout_structure": "Grid of 3 cards; the primary visual focal point of each card is a giant stat (e.g. '+340% MRR') placed above a clean UI preview.",
                "typography_specs": "Stat: text-4xl sm:text-5xl font-extrabold text-emerald-500. Title: text-lg font-bold.",
                "key_components": "Giant metric badge, client logo, 3-sentence outcome summary, 'Read Case Study $\\to$'.",
                "responsive_behavior": "1 column mobile, 3 columns desktop.",
                "accessibility": "Stats read cleanly by screen readers: 'Result: 340% increase in monthly recurring revenue'.",
                "anti_slop_rules": "All metrics must have context (e.g., 'Over 6 months'); avoid raw context-free numbers."
            },
            {
                "archetype_id": "port-03",
                "name": "Full-Bleed Alternating Deep Dives",
                "keywords": "full-bleed, alternating, deep-dive, enterprise-cases, longform",
                "best_for": "Agencies with 3 to 4 flagship enterprise transformation case studies.",
                "selection_triggers": {"case_count": "3-4", "enterprise": True},
                "layout_structure": "Stacked full-width rows alternating media left/text right, then media right/text left, with deliverable lists.",
                "typography_specs": "Client H3: text-3xl font-bold. Deliverable pills: text-xs font-mono.",
                "key_components": "Deliverable tags, client quote pull, challenge/solution bullets, full case study button.",
                "responsive_behavior": "Always renders image first or text first consistently on mobile.",
                "accessibility": "Strict semantic heading hierarchy; full keyboard focusable CTA.",
                "anti_slop_rules": "No stock mockups with generic lorem ipsum placeholders."
            },
            {
                "archetype_id": "port-04",
                "name": "Interactive Category Filter Tabs",
                "keywords": "filter-tabs, categories, multi-disciplinary, instant-filter",
                "best_for": "Full-service agencies with 12+ case studies across multiple disciplines (SEO, Branding, Dev).",
                "selection_triggers": {"case_count": "10+", "multi_disciplinary": True},
                "layout_structure": "Top pill filter bar (All, E-Commerce, SaaS, B2B); clicking filters portfolio grid with smooth transition.",
                "typography_specs": "Filter button: text-sm font-semibold. Project title: text-lg font-semibold.",
                "key_components": "Active filter pill, animated grid reflow, count indicators per category ('SaaS (8)').",
                "responsive_behavior": "Horizontal scrolling filter pill bar on mobile.",
                "accessibility": "aria-pressed on active filter button, live region announces number of filtered results.",
                "anti_slop_rules": "Filter animations must run in under 200ms; avoid slow layout repaints."
            },
            {
                "archetype_id": "port-05",
                "name": "Sticky Card Stack (Scroll-Over)",
                "keywords": "sticky-stack, card-stack, modern, interactive-scroll",
                "best_for": "High-end studios showcasing 3 to 5 premier projects with tactile scroll feel.",
                "selection_triggers": {"case_count": "3-5", "style": "modern/tactile"},
                "layout_structure": "Vertical stack where each project card sticks to viewport top (`sticky top-20`) as the next card slides up and covers it.",
                "typography_specs": "Title: text-3xl sm:text-4xl font-bold text-white.",
                "key_components": "Stacked cards with increasing z-index and subtle top shadow, project metadata strip.",
                "responsive_behavior": "Disables sticky overlay on mobile to maintain smooth scrolling.",
                "accessibility": "Keyboard navigation moves cleanly through all cards in sequence.",
                "anti_slop_rules": "Ensure proper top offset (`top-20`, `top-24`) so cards don't overlap awkwardly."
            },
            {
                "archetype_id": "port-06",
                "name": "Dual-Device Responsive Mockup Slider",
                "keywords": "responsive-slider, mobile-desktop, device-showcase",
                "best_for": "Web design and development agencies emphasizing mobile-responsive excellence.",
                "selection_triggers": {"focus": "responsive_web", "has_mobile_shots": True},
                "layout_structure": "Each project card features an overlapping desktop monitor + iPhone frame showing synchronized UI.",
                "typography_specs": "Title: text-xl font-bold. Tags: text-xs font-mono.",
                "key_components": "Monitor bezel + mobile bezel SVG frames, live website preview link, tech stack badges.",
                "responsive_behavior": "Desktop monitor scales down; mobile frame stays sharp.",
                "accessibility": "Alt text describes both desktop and mobile viewports.",
                "anti_slop_rules": "Device frames must be geometrically precise; no cheap skewed borders."
            },
            {
                "archetype_id": "port-07",
                "name": "Challenge $\\to$ Strategy $\\to$ Result Triplets",
                "keywords": "triplets, challenge-strategy-result, problem-solving, analytical",
                "best_for": "Consulting agencies and UX research studios that want to showcase analytical rigor.",
                "selection_triggers": {"focus": "ux_research/strategy", "analytical": True},
                "layout_structure": "Project card divided into 3 equal horizontal segments: 1. The Challenge (Red tint), 2. The Strategy (Blue tint), 3. The Result (Green tint).",
                "typography_specs": "Segment label: text-xs font-mono uppercase font-bold. Text: text-sm.",
                "key_components": "3-column segment card, verified client badge, outcome metric.",
                "responsive_behavior": "Stacks into 3 vertical micro-blocks on mobile.",
                "accessibility": "Clear screen reader landmarking for each of the 3 stages.",
                "anti_slop_rules": "Keep text concise (max 2 sentences per segment)."
            },
            {
                "archetype_id": "port-08",
                "name": "Minimalist Text List with Image Hover",
                "keywords": "minimalist-list, awwwards-style, typography-list, image-follow",
                "best_for": "Avant-garde design studios, editorial practices with prestigious client names.",
                "selection_triggers": {"style": "avant-garde/editorial", "brand_tier": "luxury"},
                "layout_structure": "Clean horizontal typography rows (Year, Client Name, Service, Award Badge); hovering row shows floating project thumbnail.",
                "typography_specs": "Client Name: text-2xl sm:text-4xl font-light hover:italic transition-all.",
                "key_components": "Floating pointer-following image preview, award badge (`Site of the Day`), arrow icon.",
                "responsive_behavior": "Thumbnail renders inline beneath text on mobile viewports.",
                "accessibility": "Standard HTML table or list markup with full keyboard accessibility.",
                "anti_slop_rules": "Image hover must follow cursor smoothly without jitter."
            }
        ]
    },

    # 10. Testimonials / Reviews
    {
        "section_id": "testimonials",
        "section_name": "Testimonials / Client Reviews",
        "archetypes": [
            {
                "archetype_id": "tst-01",
                "name": "Masonry Wall of Love",
                "keywords": "wall-of-love, masonry, high-volume, social-proof, avatars",
                "best_for": "Agencies with 10+ glowing client reviews of varied lengths.",
                "selection_triggers": {"review_count": "10+", "has_avatars": True},
                "layout_structure": "3-column masonry card grid (`columns-1 md:columns-2 lg:columns-3 gap-6`).",
                "typography_specs": "Quote: text-sm leading-relaxed. Client Name: text-sm font-semibold. Title: text-xs text-[var(--text-muted)].",
                "key_components": "Avatar image (40x40 rounded-full), 5-star SVG cluster, client role & company logo, verified review badge.",
                "responsive_behavior": "Single column on mobile, 2 columns on tablet, 3 columns on desktop.",
                "accessibility": "Each review wrapped in <blockquote> and <figure> with <figcaption>.",
                "anti_slop_rules": "All reviewer photos must be real clients with verifiable LinkedIn/Twitter links."
            },
            {
                "archetype_id": "tst-02",
                "name": "Single Large Featured Editorial Quote",
                "keywords": "featured-quote, editorial, enterprise-testimonial, high-prestige",
                "best_for": "Agencies with 1 or 2 mega-prestige enterprise quotes (e.g., from a VP at a Fortune 500).",
                "selection_triggers": {"has_vip_quote": True, "brand_tier": "enterprise"},
                "layout_structure": "Centered or split layout with an oversized 32px serif quotation mark, giant 28px quote text, client headshot and company logo.",
                "typography_specs": "Quote: text-2xl sm:text-3xl font-medium tracking-tight text-[var(--text-primary)].",
                "key_components": "Oversized decorative quote mark, client company SVG logo, high-res executive headshot.",
                "responsive_behavior": "Scales font down gracefully on mobile screens.",
                "accessibility": "Semantic blockquote with cite attribute.",
                "anti_slop_rules": "No fake generic praise ('They did great work!'); must cite specific business impact."
            },
            {
                "archetype_id": "tst-03",
                "name": "Playable Video Testimonial Grid",
                "keywords": "video-testimonials, founder-interviews, watch-proof, high-ticket",
                "best_for": "High-ticket agencies ($10k-$100k+) where video interviews convert skeptics.",
                "selection_triggers": {"has_video_reviews": True, "deal_size": "high"},
                "layout_structure": "Grid of 2 or 3 video cards with play button overlay, video runtime badge ('1:45 min'), and summary bullet beneath.",
                "typography_specs": "Headline quote: text-base font-semibold. Runtime badge: text-xs font-mono.",
                "key_components": "Video thumbnail with play icon, modal video player, client credentials badge.",
                "responsive_behavior": "Cards stack into single column on mobile.",
                "accessibility": "Play button has aria-label='Watch video review from [Name]'; captions provided.",
                "anti_slop_rules": "Do not autoplay all videos; user must explicitly click to play."
            },
            {
                "archetype_id": "tst-04",
                "name": "Verifiable Twitter / LinkedIn Social Embed Cards",
                "keywords": "social-embeds, twitter-cards, linkedin-proof, organic, unedited",
                "best_for": "Tech agencies, developer tools, and modern growth agencies whose clients tweet praise organically.",
                "selection_triggers": {"social_proof_type": "social_posts", "style": "tech"},
                "layout_structure": "Grid of cards styled exactly like native Twitter/LinkedIn posts with verification checks and timestamps.",
                "typography_specs": "Body: text-sm. Handle: text-xs text-[var(--text-muted)].",
                "key_components": "Social platform icon (X or LinkedIn), verified checkmark icon, clickable link to original post.",
                "responsive_behavior": "1 column mobile, 2-3 columns desktop.",
                "accessibility": "Card contains link to external post with aria-label='View original post on Twitter'.",
                "anti_slop_rules": "Do not fabricate fake social posts; links must point to live public tweets."
            },
            {
                "archetype_id": "tst-05",
                "name": "Split Testimonial with Verified Revenue Graph",
                "keywords": "split-proof, graph-testimonial, data-backed, cro-agency",
                "best_for": "B2B performance agencies backing client quotes with empirical revenue analytics.",
                "selection_triggers": {"has_analytics_data": True, "goal": "conversion"},
                "layout_structure": "2-column card: Left column client quote & credentials; Right column verified revenue chart from Stripe/Google Analytics.",
                "typography_specs": "Metric callout: text-3xl font-extrabold text-emerald-500. Quote: text-base font-medium.",
                "key_components": "Verified data tag ('Stripe Verified Revenue'), SVG area graph, client quote.",
                "responsive_behavior": "Quote on top, chart below on mobile.",
                "accessibility": "Chart data summarized in accessible text description for screen readers.",
                "anti_slop_rules": "Graph axes must be clearly labeled; no meaningless upward squiggles."
            },
            {
                "archetype_id": "tst-06",
                "name": "Audio Voice Note Player Cards",
                "keywords": "audio-testimonials, voice-notes, human-connection, authentic",
                "best_for": "Boutique agencies and consultants where hearing real client enthusiasm builds massive rapport.",
                "selection_triggers": {"has_audio": True, "brand_tier": "boutique"},
                "layout_structure": "Card featuring client avatar, quote snippet, and an interactive audio waveform player with play/pause and progress bar.",
                "typography_specs": "Client Name: text-sm font-semibold. Duration: text-xs font-mono.",
                "key_components": "SVG audio waveform bars, play/pause toggle button, scrubber timeline.",
                "responsive_behavior": "Full width card on mobile.",
                "accessibility": "Full written text transcript provided right beneath the audio player.",
                "anti_slop_rules": "Audio must be user-triggered; never autoplay."
            },
            {
                "archetype_id": "tst-07",
                "name": "Dual Infinite Marquee (Opposing Directions)",
                "keywords": "dual-marquee, fast-ticker, momentum, volume-proof",
                "best_for": "Consumer tech, high-volume B2B with 20+ short one-line reviews.",
                "selection_triggers": {"review_count": "20+", "short_quotes": True},
                "layout_structure": "Two horizontal rows of testimonial cards: Row 1 scrolls smoothly left-to-right; Row 2 scrolls right-to-left.",
                "typography_specs": "Card quote: text-xs sm:text-sm font-medium.",
                "key_components": "Compact review cards, subtle border, star rating, CSS marquee track with pause-on-hover.",
                "responsive_behavior": "Maintains continuous marquee on mobile with touch drag support.",
                "accessibility": "Pause button provided, respects prefers-reduced-motion.",
                "anti_slop_rules": "Speed must be comfortable to read (35-45s per cycle); not hyper-fast."
            },
            {
                "archetype_id": "tst-08",
                "name": "Compact Star Rating Strip with Featured Avatar Stack",
                "keywords": "compact-strip, minimalist-proof, single-line, lightweight",
                "best_for": "Single-page landing pages, minimal sites that don't want a heavy review section.",
                "selection_triggers": {"wants_compact": True, "style": "minimalist"},
                "layout_structure": "A single compact horizontal banner: Overlapping avatar cluster left + 'Rated 4.9/5 by 340+ clients' center + Trustpilot/Google badge right.",
                "typography_specs": "Rating text: text-sm font-semibold text-[var(--text-primary)].",
                "key_components": "Avatar stack, 5 gold star icons, external review platform badge (Clutch/Google).",
                "responsive_behavior": "Flex items wrap gracefully on small screens.",
                "accessibility": "Accessible rating description: 'Average rating 4.9 out of 5 based on 340 reviews'.",
                "anti_slop_rules": "No fake star ratings without platform link."
            }
        ]
    },

    # 12. Pricing / Packages
    {
        "section_id": "pricing",
        "section_name": "Pricing / Packages",
        "archetypes": [
            {
                "archetype_id": "prc-01",
                "name": "3-Tier Standard Cards (Starter / Growth / Scale)",
                "keywords": "3-tier, standard, highlighted-card, popular-badge, transparent",
                "best_for": "Agencies with standardized service tiers or retainer packages.",
                "selection_triggers": {"tier_count": "3", "style": "standard"},
                "layout_structure": "3-column grid (`grid-cols-1 lg:grid-cols-3 gap-8`); center card elevated with primary border, 'Most Popular' chip, and prominent CTA.",
                "typography_specs": "Price: text-4xl sm:text-5xl font-extrabold. Tier name: text-lg font-bold. Period: text-sm text-[var(--text-muted)].",
                "key_components": "Pill badge ('Most Popular'), price numeral, feature checkmark list, primary/secondary CTA button.",
                "responsive_behavior": "Stacks into 3 cards on mobile with the highlighted tier shown first or labeled clearly.",
                "accessibility": "Clear H3 per tier, feature lists use <ul> and accessible icons.",
                "anti_slop_rules": "No hidden fee disclaimers in 8px unreadable micro-text."
            },
            {
                "archetype_id": "prc-02",
                "name": "Monthly vs Annual Billing Switcher",
                "keywords": "toggle, monthly-annual, discount-badge, recurring-saas",
                "best_for": "Recurring retainers, software subscriptions, productized agencies with discount incentives.",
                "selection_triggers": {"has_annual_discount": True, "subscription": True},
                "layout_structure": "Centered toggle pill button ('Monthly' / 'Annual — Save 20%') above 3 pricing cards; prices smoothly update via state.",
                "typography_specs": "Toggle: text-sm font-semibold. Discount badge: text-xs font-mono font-bold text-emerald-500.",
                "key_components": "Accessible switch toggle, discount pill badge, animated price transition.",
                "responsive_behavior": "Cards stack vertically on mobile; toggle stays sticky or centered.",
                "accessibility": "role='switch', aria-checked, keyboard spacebar triggers toggle.",
                "anti_slop_rules": "Show exact dollar savings, not misleading percentage math."
            },
            {
                "archetype_id": "prc-03",
                "name": "Interactive Scope / Price Calculator Slider",
                "keywords": "calculator, sliders, dynamic-pricing, custom-scope",
                "best_for": "Custom agencies where pricing scales with pages, ad spend, or team seats.",
                "selection_triggers": {"pricing_model": "usage/scope_based", "custom_quotes": True},
                "layout_structure": "Interactive slider panel on left (e.g., 'Estimated Monthly Ad Spend: $10,000'); Right card calculates recommended retainer and deliverables in real time.",
                "typography_specs": "Calculated total: text-4xl font-extrabold text-primary. Slider label: text-sm font-semibold.",
                "key_components": "Accessible range input sliders, dynamic price ticker, instant 'Book Scope Call' CTA.",
                "responsive_behavior": "1 column vertical stack on mobile.",
                "accessibility": "input type='range' with aria-valuemin, aria-valuemax, aria-valuenow.",
                "anti_slop_rules": "Always include a baseline floor price to avoid unrealistic low estimates."
            },
            {
                "archetype_id": "prc-04",
                "name": "Single Transparent Flat-Rate Box",
                "keywords": "flat-rate, single-price, designjoy-style, transparent, pause-anytime",
                "best_for": "Productized subscription agencies offering one all-inclusive flagship tier.",
                "selection_triggers": {"pricing_model": "flat_rate", "is_productized": True},
                "layout_structure": "Single large prominent card (max-w-2xl mx-auto) with bold flat monthly fee, 'Pause or cancel anytime' guarantee, and 2-column checklist of all inclusions.",
                "typography_specs": "Price: text-5xl sm:text-6xl font-black. Inclusions: text-sm font-medium.",
                "key_components": "'Pause or cancel anytime' tag, lightning turnaround guarantee, comprehensive deliverable list.",
                "responsive_behavior": "Inclusions list collapses to single column on mobile.",
                "accessibility": "Clear single tab stop for CTA button, fully semantic list.",
                "anti_slop_rules": "No asterisks or fine print hiding cancellation lock-ins."
            },
            {
                "archetype_id": "prc-05",
                "name": "Feature Matrix Comparison Grid",
                "keywords": "feature-matrix, comparison-table, enterprise-pricing, checkboxes",
                "best_for": "Enterprise tools and large agencies with 20+ granular feature distinctions between tiers.",
                "selection_triggers": {"feature_density": "high", "enterprise": True},
                "layout_structure": "Top tier summary cards + comprehensive comparison table below with sticky table header on scroll.",
                "typography_specs": "Feature name: text-sm. Category header: text-xs font-mono uppercase font-bold.",
                "key_components": "Green checkmark icons, grey minus icons, tooltip definitions for complex features.",
                "responsive_behavior": "Horizontal overflow scroll container on mobile with sticky left feature column.",
                "accessibility": "Table has proper scope attributes (<th scope='col'> and <th scope='row'>).",
                "anti_slop_rules": "Keep checkmark colors accessible; do not use faint unreadable greens."
            },
            {
                "archetype_id": "prc-06",
                "name": "Custom Quote Gate / Request Consultation",
                "keywords": "custom-quote, enterprise-gate, contact-sales, bespoke",
                "best_for": "High-end bespoke agencies and enterprise consultants who do not publish fixed rates.",
                "selection_triggers": {"pricing_model": "bespoke", "enterprise": True},
                "layout_structure": "3 value bracket cards ('Bespoke Sprint', 'Dedicated Pod', 'Enterprise Retainer') with starting budgets (e.g. 'From $25k') and 'Request Custom Proposal' CTA.",
                "typography_specs": "Bracket title: text-xl font-bold. Starting at text: text-sm font-mono text-[var(--text-muted)].",
                "key_components": "Scope description, typical duration pill ('8-12 weeks'), proposal booking button.",
                "responsive_behavior": "Cards stack into 3 neat rows on mobile.",
                "accessibility": "Distinct button labels specifying which bracket proposal is being requested.",
                "anti_slop_rules": "Always state a realistic baseline ('Projects typically start at $20k') to filter unqualified leads."
            }
        ]
    },

    # 13. FAQ Section
    {
        "section_id": "faq",
        "section_name": "FAQ Section",
        "archetypes": [
            {
                "archetype_id": "faq-01",
                "name": "Single-Column Centered Accordion",
                "keywords": "single-column, accordion, classic, clean, standard",
                "best_for": "Standard agencies with 5 to 8 common client questions.",
                "selection_triggers": {"faq_count": "5-8", "style": "clean"},
                "layout_structure": "Centered container (max-w-3xl mx-auto) with stacked accordion rows separated by subtle 1px borders.",
                "typography_specs": "Question trigger: text-base sm:text-lg font-semibold text-[var(--text-primary)]. Answer: text-sm sm:text-base leading-relaxed text-[var(--text-secondary)].",
                "key_components": "Expanding container, plus/minus or rotating chevron icon, smooth height transition.",
                "responsive_behavior": "Full width with 16px horizontal screen padding on mobile.",
                "accessibility": "<button aria-expanded='false' aria-controls='faq-answer-1'>, keyboard Enter/Space toggles.",
                "anti_slop_rules": "No sudden jarring height jumps; use CSS grid 0fr -> 1fr transition."
            },
            {
                "archetype_id": "faq-02",
                "name": "Two-Column Category Split (Filterable)",
                "keywords": "two-column, categories, tabs, filterable-faq, comprehensive",
                "best_for": "Agencies with 12+ questions across multiple categories (General, Pricing, Process, Technical).",
                "selection_triggers": {"faq_count": "10+", "has_categories": True},
                "layout_structure": "Left sticky column with category navigation pills; Right column displays matching accordion questions.",
                "typography_specs": "Category tab: text-sm font-semibold. Question: text-base font-semibold.",
                "key_components": "Sticky category sidebar, active category indicator pill, accordion list.",
                "responsive_behavior": "Category tabs convert to horizontal scrollable strip on mobile.",
                "accessibility": "role='tablist' for categories; aria-selected states managed properly.",
                "anti_slop_rules": "Do not duplicate identical questions across multiple categories."
            },
            {
                "archetype_id": "faq-03",
                "name": "Open 2-Column Card Grid (No Clicks)",
                "keywords": "open-grid, cards, no-clicks, scannable, punchy",
                "best_for": "Agencies with 4 to 6 short, punchy questions where answers are immediately visible without clicking.",
                "selection_triggers": {"faq_count": "4-6", "answers_short": True, "no_accordion": True},
                "layout_structure": "2-column grid (`grid-cols-1 md:grid-cols-2 gap-6`); each card contains the question as an H3 and the answer directly below.",
                "typography_specs": "Question: text-base font-bold text-[var(--text-primary)]. Answer: text-sm text-[var(--text-secondary)].",
                "key_components": "Bordered surface cards, subtle icon accent, zero hidden text.",
                "responsive_behavior": "Single column vertical stack on mobile.",
                "accessibility": "Direct text in DOM, zero aria-expanded state overhead.",
                "anti_slop_rules": "Answers must be under 3 sentences; long essays belong in an accordion."
            },
            {
                "archetype_id": "faq-04",
                "name": "Searchable FAQ with Live Instant Filter",
                "keywords": "searchable-faq, instant-filter, knowledge-base, support",
                "best_for": "Technical agencies, platforms, and products with 15+ detailed questions.",
                "selection_triggers": {"faq_count": "15+", "searchable": True},
                "layout_structure": "Prominent search input bar on top with search icon and clear button; questions filter in real time as user types.",
                "typography_specs": "Search placeholder: text-base. Match count: text-xs font-mono text-[var(--text-muted)].",
                "key_components": "Search input, real-time regex/BM25 filter, 'No matching questions found' fallback state with contact button.",
                "responsive_behavior": "Input fills 100% width on mobile.",
                "accessibility": "aria-live='polite' announces number of matching questions.",
                "anti_slop_rules": "Filter response must be instantaneous (<16ms, zero debounce lag)."
            },
            {
                "archetype_id": "faq-05",
                "name": "Split Layout (Contact Card Left / FAQ Right)",
                "keywords": "split-faq, contact-card, talk-to-us, conversion-faq",
                "best_for": "Agencies focused on lead generation where the FAQ directly funnels into a consultation.",
                "selection_triggers": {"goal": "consultation", "has_contact_prompt": True},
                "layout_structure": "Left column has H2, intro copy, and a sticky 'Still have questions? Chat with our team' card; Right column has accordion questions.",
                "typography_specs": "Left title: text-3xl font-bold. Chat card: text-sm font-medium.",
                "key_components": "Support team avatar stack, live response time badge, direct WhatsApp / Calendar button.",
                "responsive_behavior": "Left contact prompt stacks beneath the accordion on mobile.",
                "accessibility": "Clear focus sequence from questions to the contact card.",
                "anti_slop_rules": "Do not hide the contact button behind an accordion."
            },
            {
                "archetype_id": "faq-06",
                "name": "Slide-Over Drawer / Modal FAQ",
                "keywords": "slide-over, drawer-faq, clean-landing, zero-clutter",
                "best_for": "Ultra-minimalist landing pages that want to keep page length short.",
                "selection_triggers": {"style": "ultra-minimalist", "wants_compact": True},
                "layout_structure": "A single compact section row: 'Have questions before getting started? [Open FAQ $\\to$]'; clicking slides open a right-side drawer containing the full FAQ.",
                "typography_specs": "Prompt text: text-lg font-semibold. Drawer title: text-2xl font-bold.",
                "key_components": "Drawer trigger button, accessible slide-over sheet component (`BottomSheet` / `ModalDialog`).",
                "responsive_behavior": "Drawer opens fullscreen on mobile devices.",
                "accessibility": "Focus trapped inside sheet, Escape key dismisses, aria-modal='true'.",
                "anti_slop_rules": "Ensure drawer backdrop is dark enough (50% scrim) to maintain text focus."
            }
        ]
    },

    # 14. Final CTA Band
    {
        "section_id": "final_cta",
        "section_name": "Final CTA / Let's Talk",
        "archetypes": [
            {
                "archetype_id": "cta-01",
                "name": "High-Impact Contrast Card Band",
                "keywords": "contrast-card, bold-cta, full-width-card, primary-button, high-converting",
                "best_for": "General agencies and SaaS landing pages with a clear primary conversion goal.",
                "selection_triggers": {"goal": "consultation/trial", "style": "standard"},
                "layout_structure": "Centered rounded card (`rounded-3xl p-12 sm:p-16`) with high-contrast background (dark on light site, or primary gradient on dark site), bold H2, subtitle, and dual CTA buttons.",
                "typography_specs": "H2: text-3xl sm:text-4xl lg:text-5xl font-bold text-white tracking-tight. Subhead: text-lg text-slate-300.",
                "key_components": "High-contrast container, primary action button, secondary ghost button, confidence guarantee tag ('No credit card required').",
                "responsive_behavior": "Paddings reduce to p-8 on mobile; buttons stack full width.",
                "accessibility": "Ensures min 7:1 contrast ratio between text and card background.",
                "anti_slop_rules": "No purple radioactive gradient glows; use deep grounded slate or accessible navy."
            },
            {
                "archetype_id": "cta-02",
                "name": "Embedded Interactive Calendar Scheduler",
                "keywords": "calendar-embed, calendly, cal-com, direct-booking, friction-free",
                "best_for": "Agencies where booking a 30-minute discovery call is the sole metric of success.",
                "selection_triggers": {"primary_goal": "calendar_booking", "friction_reduction": True},
                "layout_structure": "Left column explains what happens on the call (Agenda, Who you will meet, Deliverables); Right column embeds an inline Cal.com / Calendly booking widget.",
                "typography_specs": "Agenda items: text-sm font-semibold. Call duration badge: text-xs font-mono.",
                "key_components": "Agenda bullet list, host avatar & bio, responsive iframe/widget container with loading state.",
                "responsive_behavior": "Stacks vertically on mobile with booking widget on bottom.",
                "accessibility": "Iframe has descriptive title='Book a discovery call on Cal.com'.",
                "anti_slop_rules": "Do not embed broken widgets without a direct link fallback."
            },
            {
                "archetype_id": "cta-03",
                "name": "Inline Instant Lead Capture Form",
                "keywords": "instant-lead, single-field, url-audit, free-quote, high-velocity",
                "best_for": "SEO, PPC, and CRO agencies offering a free automated audit or quote.",
                "selection_triggers": {"lead_magnet": "free_audit", "conversion_speed": "instant"},
                "layout_structure": "Centered banner with bold headline ('Get your free 14-point audit in 24 hours') + clean 2-field form (Website URL + Email) with submit CTA.",
                "typography_specs": "Input text: text-base. Button text: text-base font-bold.",
                "key_components": "Form fields with floating labels, honeypot spam protection, submission status spinner.",
                "responsive_behavior": "Inline desktop layout; stacked inputs and button on mobile.",
                "accessibility": "Visible labels, aria-live status announcement on submit.",
                "anti_slop_rules": "Never ask for phone numbers or company size in a final instant capture form."
            },
            {
                "archetype_id": "cta-04",
                "name": "Interactive Contact Form with Budget Pills",
                "keywords": "budget-pills, multi-choice, qualification, qualified-leads",
                "best_for": "High-ticket agencies that need to qualify client budgets before accepting calls.",
                "selection_triggers": {"needs_qualification": True, "high_ticket": True},
                "layout_structure": "Clean card with multi-choice budget pills ('$5k-$10k', '$10k-$25k', '$25k+') + service checkboxes + message field.",
                "typography_specs": "Pill text: text-xs font-mono font-semibold. Section labels: text-sm font-bold.",
                "key_components": "Custom toggle pills (`role='radio'`), accessible text inputs, privacy reassurance tag.",
                "responsive_behavior": "Budget pills wrap neatly in 2 columns on mobile.",
                "accessibility": "role='radiogroup' for budget selection; keyboard arrow navigation.",
                "anti_slop_rules": "Keep form steps under 4 questions to prevent abandonment."
            },
            {
                "archetype_id": "cta-05",
                "name": "Founder Personal Letter & Direct Phone/Email",
                "keywords": "founder-letter, personal-invitation, direct-email, boutique-consulting",
                "best_for": "Elite boutique studios and high-trust consultants pitching senior executives.",
                "selection_triggers": {"brand_tier": "boutique/exclusive", "founder_led": True},
                "layout_structure": "Personal invitation card: Founder headshot, direct phone number, personal direct email, and promise: 'I reply to every email personally within 4 hours'.",
                "typography_specs": "Letter text: text-lg font-serif leading-relaxed. Founder name: text-base font-bold.",
                "key_components": "Authentic candid portrait, direct mailto/tel links, copyable email button.",
                "responsive_behavior": "Centered stack on mobile viewports.",
                "accessibility": "Clear tel and mailto links with aria-labels.",
                "anti_slop_rules": "No generic contact@ or info@ addresses; use real person's email."
            },
            {
                "archetype_id": "cta-06",
                "name": "Dual-Path Split CTA (Startups vs Enterprise)",
                "keywords": "dual-path, audience-split, self-serve-vs-sales, targeted",
                "best_for": "Agencies or SaaS catering to two completely different customer tiers.",
                "selection_triggers": {"target_audience": "dual_market", "has_enterprise_tier": True},
                "layout_structure": "Side-by-side 2-column card: Left side 'For Early-Stage Startups' (Self-serve / Fast kickoff); Right side 'For Enterprise Teams' (Custom security / Talk to VP).",
                "typography_specs": "Path title: text-2xl font-bold. Description: text-sm.",
                "key_components": "Two distinct CTA buttons with specific routing, separate feature bullet points.",
                "responsive_behavior": "Stacks into two distinct sequential cards on mobile.",
                "accessibility": "Distinct heading levels (H3) and clear button labels for each path.",
                "anti_slop_rules": "Make visual weight equal or intentionally elevate the higher-value path."
            }
        ]
    },

    # 15. Footer
    {
        "section_id": "footer",
        "section_name": "Footer",
        "archetypes": [
            {
                "archetype_id": "ftr-01",
                "name": "Multi-Column Sitemap Hub (Standard Corporate)",
                "keywords": "multi-column, sitemap, 4-column, links, copyright, legal",
                "best_for": "Standard agencies with rich sitemaps, services, resources, and legal pages.",
                "selection_triggers": {"link_count": "15+", "style": "standard"},
                "layout_structure": "4 or 5-column grid: Column 1 brand logo & mission summary; Columns 2-4 category link columns; Column 5 newsletter / social links.",
                "typography_specs": "Column headers: text-xs font-mono uppercase tracking-wider text-[var(--text-muted)]. Links: text-sm text-[var(--text-secondary)] hover:text-white.",
                "key_components": "Brand logo, social icon strip (SVG), category columns, bottom copyright and legal bar (Privacy, Terms, Cookies).",
                "responsive_behavior": "Collapses to 2-column on tablet, single accordion or stacked list on mobile.",
                "accessibility": "role='contentinfo', link lists wrapped in <ul>, valid focus states.",
                "anti_slop_rules": "No broken placeholder links; all links must resolve."
            },
            {
                "archetype_id": "ftr-02",
                "name": "Editorial Giant Typography Footer",
                "keywords": "giant-typography, editorial, awwwards, brand-statement, massive-logo",
                "best_for": "Awwwards-style creative design studios and luxury brands.",
                "selection_triggers": {"style": "editorial/luxury", "brand_statement": True},
                "layout_structure": "Top tier simple link row; Bottom tier dominated by a massive full-width agency name in 12vw typography stretching across the viewport.",
                "typography_specs": "Giant wordmark: text-[12vw] font-black uppercase tracking-tighter leading-none text-[var(--border-subtle)].",
                "key_components": "Massive SVG or font wordmark, time zone clocks ('London 14:32 • New York 09:32'), minimal legal row.",
                "responsive_behavior": "Viewport-width typography (`12vw`) scales smoothly without horizontal overflow.",
                "accessibility": "Giant wordmark marked aria-hidden='true' if redundant to brand text.",
                "anti_slop_rules": "Ensure overflow-hidden on container to prevent horizontal scrollbar bugs."
            },
            {
                "archetype_id": "ftr-03",
                "name": "Newsletter-First Content Hub",
                "keywords": "newsletter-footer, subscribe, content-first, blog, resources",
                "best_for": "Agencies with active thought leadership, research reports, or newsletters.",
                "selection_triggers": {"has_newsletter": True, "content_focus": True},
                "layout_structure": "Top prominent newsletter card ('Join 15,000 marketing leaders receiving our weekly teardown') with inline email form + standard link grid below.",
                "typography_specs": "Newsletter title: text-xl font-bold. Form button: text-sm font-semibold.",
                "key_components": "Email input field, subscribe button, anti-spam reassurance, subscriber count badge.",
                "responsive_behavior": "Newsletter input stacks above button on mobile.",
                "accessibility": "Explicit label for email input, aria-live error/success message.",
                "anti_slop_rules": "No annoying pop-ups; keep the newsletter anchored gracefully in the footer."
            },
            {
                "archetype_id": "ftr-04",
                "name": "Minimalist Single-Line Strip",
                "keywords": "minimal-footer, single-line, portfolio, clean, lightweight",
                "best_for": "Single-page landing pages, personal portfolios, minimal micro-sites.",
                "selection_triggers": {"style": "minimalist", "single_page": True},
                "layout_structure": "A single clean horizontal row (`h-16 border-t border-[var(--border-subtle)] px-6 flex items-center justify-between`): Logo left, Copyright center, Social links right.",
                "typography_specs": "Text: text-xs text-[var(--text-muted)]. Social icons: 18x18 SVG.",
                "key_components": "Logo mark, copyright text, minimal social icon links.",
                "responsive_behavior": "Stacks into centered vertical column on mobile with 8px spacing.",
                "accessibility": "Full keyboard accessibility on all social icon links with aria-labels.",
                "anti_slop_rules": "Do not omit mandatory legal links (Privacy Policy) if collecting data."
            },
            {
                "archetype_id": "ftr-05",
                "name": "Multi-Office Global Footprint",
                "keywords": "global-offices, timezones, physical-locations, international",
                "best_for": "International agencies with offices across multiple cities (e.g. New York, London, Tokyo).",
                "selection_triggers": {"has_multiple_offices": True, "international": True},
                "layout_structure": "Grid of office location cards; each card features city name, local live time clock, physical address, and local phone number.",
                "typography_specs": "City name: text-lg font-bold. Time clock: text-xs font-mono text-emerald-500.",
                "key_components": "Live JavaScript time clock per city, Google Maps link, local phone number.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 4 columns desktop.",
                "accessibility": "Live clocks update without triggering disruptive screen reader announcements.",
                "anti_slop_rules": "Ensure phone numbers use international dial codes (+1, +44)."
            },
            {
                "archetype_id": "ftr-06",
                "name": "App Download & Ecosystem Matrix",
                "keywords": "app-store-badges, mobile-app, qr-code, ecosystem, platforms",
                "best_for": "Agencies with proprietary software, mobile apps, or extensive partner integrations.",
                "selection_triggers": {"has_mobile_app": True, "ecosystem": True},
                "layout_structure": "Top tier App Store & Google Play badge buttons + QR code for instant phone scan; Bottom tier standard legal and platform status link.",
                "typography_specs": "Badge subtext: text-[10px]. Badge title: text-xs font-bold.",
                "key_components": "App Store SVG badge, Google Play SVG badge, QR code frame with scan tooltip, system status badge ('All systems normal').",
                "responsive_behavior": "QR code hides on mobile viewports; direct app store buttons take full width.",
                "accessibility": "Badges have descriptive aria-labels ('Download on Apple App Store').",
                "anti_slop_rules": "Use official brand SVG assets for store badges; no distorted PNGs."
            }
        ]
    }
]


def build_json(output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(SECTIONS_DATA, f, indent=2, ensure_ascii=False)
    print(f"[OK] Wrote JSON dataset to: {output_path}")


def build_csv(output_path: Path):
    fieldnames = [
        "Section ID",
        "Section Name",
        "Archetype ID",
        "Archetype Name",
        "Keywords",
        "Best For",
        "Selection Triggers",
        "Layout Structure",
        "Typography Specs",
        "Key Components",
        "Responsive Behavior",
        "Accessibility",
        "Anti-Slop Rules"
    ]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        for sec in SECTIONS_DATA:
            sec_id = sec["section_id"]
            sec_name = sec["section_name"]
            for arch in sec["archetypes"]:
                writer.writerow({
                    "Section ID": sec_id,
                    "Section Name": sec_name,
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
                    "Anti-Slop Rules": arch["anti_slop_rules"]
                })
                count += 1
    print(f"[OK] Wrote CSV dataset ({count} archetypes) to: {output_path}")


if __name__ == "__main__":
    json_path = DATA_DIR / "section-archetypes.json"
    csv_path = DATA_DIR / "section-archetypes.csv"
    build_json(json_path)
    build_csv(csv_path)
