#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Idempotently add kinetic dark agency archetypes to existing sections and insert
3 reusable product/case-study dossier sections into section-archetypes.json
and rebuild section-archetypes.csv.
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dataset_utils import DATA_DIR, write_sections_dataset

ARCHETYPE_EXTENSIONS = {
    "navbar": [
        {
            "archetype_id": "nav-07",
            "name": "Dark Overlay Header with Char-Wave Dropdowns & Accent-Outlined Pill CTA",
            "keywords": "dark-header, menu-wave, text-shadow, sticky-header, pill-cta, kinetic-agency",
            "best_for": "Dark-mode software agencies, enterprise engineering partners, and multi-product consultancies with 5-6 top-level categories.",
            "selection_triggers": {"kinetic_dark": True, "link_count": "5-6", "has_dropdowns": True},
            "layout_structure": "Full-width 90px dark/transparent overlay header (sticky toggle past 20px scroll). Left vector brand logo; center 5-6 inline links (.menu-anim char-split with 16px vertical text-shadow duplicate shifting over 0.4s ease in +0.05s per-character stagger) + dropdowns descending to top:75px; right accent-outlined pill CTA (~182x50px, rounded-[46px], 1px border #61CE70).",
            "typography_specs": "Top links: 18px line-height 16px text-[#FFFFFF]; Dropdown panel: #FFFFFF bg with #121212 links shifting letter-spacing: 1px on hover; Pill CTA: text-base font-medium uppercase tracking-wide.",
            "key_components": "Vector SVG brand mark, accessible dropdown disclosures (<button aria-expanded>), char-wave hover spans (disabled under reduced-motion), accent-outlined pill CTA button, mobile drawer trigger (< 1200px).",
            "responsive_behavior": "Desktop shows inline char-wave dropdown nav + right pill CTA; collapses below 1200px to logo + >=44px hamburger trigger opening a full-height accessible slide-over menu.",
            "accessibility": "Dropdown toggles support Escape key and arrow navigation; skip link precedes header; interactive targets >= 44x44px; scroll-margin-top set on anchored sections.",
            "anti_slop_rules": "Never use raw hover-only dropdowns inaccessible to keyboard users; keep >= 4.5:1 contrast on dark nav items and pill CTA borders; pause char-wave stagger when prefers-reduced-motion: reduce."
        }
    ],
    "hero": [
        {
            "archetype_id": "hero-11",
            "name": "Kinetic Dark Display Hero with Radial/Magnetic 170px CTA & 250px Video Trigger",
            "keywords": "kinetic-dark, display-hero, circular-cta, radial-fill, magnetic-button, scroll-smoother, parallax",
            "best_for": "Dark kinetic tech agencies, AI/software studios, and creative engineering consultancies seeking high-impact typographic presence and continuous smoothed scroll flow.",
            "selection_triggers": {"kinetic_dark": True, "circular_cta": True},
            "layout_structure": "Full-bleed dark canvas (min-h-[700px] bg-[var(--surface-base)] relative px-6 lg:px-12) inside ScrollSmoother (1.35 smooth, data-speed 0.3-0.9 imagery/shape layers). Oversized asymmetrical SplitText H1 (rotationX -80deg 1s reveal, .animation__char_come x:70 stagger 0.05s) paired with split subhead and 250px .btn_wrapper containing 170x170px circular CTA (.wc-btn-primary.btn-hover: 20->350px cursor-origin emerald span fill in 0.7s + 80px magnetic parallax over 0.5s power2.out) plus 250px video trigger.",
            "typography_specs": "H1: clamp(2.25rem, 1.4rem + 4.2vw, 6.125rem) font-medium leading-[1.15] text-[var(--text-primary)]. Subhead: text-base leading-relaxed text-[var(--text-secondary)] max-w-xl.",
            "key_components": "Kinetic SplitText display H1, 170x170px circular radial-fill magnetic CTA (transition: all 0.7s inner fill + 0.3s outer border), 250px video modal trigger, optional mix-blend-mode cursor ring (40px/8px desktop only).",
            "responsive_behavior": "Display H1 scales smoothly down to 28-48px on 375px viewports with 0px horizontal overflow; .btn_wrapper shrinks 250px -> 175px mobile with ScrollSmoother effects disabled below 1025px and cursors hidden <= 1200px.",
            "accessibility": "Circular icon-only play buttons carry explicit aria-label='Play overview video'; kinetic SplitText, magnetic cursor offset, and ScrollSmoother disable under prefers-reduced-motion: reduce.",
            "anti_slop_rules": "Zero glowing purple mesh blobs; contrast on backdrop banner scrim must keep white H1 >= 7:1 and radial emerald fill ink #020617 >= 7:1; never trap pointer focus on magnetic cursor wrappers."
        }
    ],
    "trusted_by": [
        {
            "archetype_id": "tb-07",
            "name": "Dark 24-Logo Monochrome Wall + Swiper Emerald Marquee Strip",
            "keywords": "logo-wall, dark-marquee, emerald-ticker, swiper-freemode, monochrome-grid, client-proof",
            "best_for": "Enterprise software agencies and solution providers showcasing 12-24+ client logos alongside a continuous capability ticker.",
            "selection_triggers": {"kinetic_dark": True, "logo_count": "12+"},
            "layout_structure": "Dual-layer proof band: Upper 108px full-bleed accent marquee band (bg-[var(--color-action-primary)] text-[#020617], Swiper freemode loop with speed:2000 / 10000ms autoplay delay:1), plus dark client logo grid (.fade_bottom y:30->0 stagger 0.2s entry, grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-px bg-[var(--border-subtle)]).",
            "typography_specs": "Ticker items: 21px font-bold capitalize text-[#020617]. Section heading: clamp(2rem, 1.4rem + 2.5vw, 3.75rem) font-medium text-[var(--text-primary)].",
            "key_components": "Swiper continuous freemode ticker with pause toggle, monochrome normalized client SVG/PNG tiles in uniform aspect boxes.",
            "responsive_behavior": "Swiper slidesPerView shifts cleanly (1 -> 3 at 640px -> 4 at 1024px -> 5 at 1300px -> 8 at 1900px); logo grid shifts from 6 columns desktop to 3 tablet and 2 mobile.",
            "accessibility": "Marquee pauses on hover/focus and stops automatically when prefers-reduced-motion: reduce is active; dark #020617 ink on #3BC77B exceeds 9:1 contrast.",
            "anti_slop_rules": "Normalize all client logos to consistent monochrome treatment and uniform height; never leave raw unstyled white JPEG boxes on dark #000000 surfaces."
        }
    ],
    "services": [
        {
            "archetype_id": "srv-09",
            "name": "Dark Sticky-Preview 15deg Service Hover List with Diagonal Ribbon Wipe",
            "keywords": "hover-service-list, sticky-preview, numbered-rows, diagonal-wipe, dark-agency, split-reveal",
            "best_for": "Agencies and consultancies presenting 4-6 core service pillars with rich visual previews without cluttering the initial scan.",
            "selection_triggers": {"kinetic_dark": True, "hover_service_list": True},
            "layout_structure": "2-column dark split (border-t border-[var(--border-subtle)]). Left (4 cols): sticky .service__img pane transitioning opacity 0->1 and transform rotate(0deg) translateX(-100px) -> rotate(15deg) translateX(60px) translateY(30px) over 0.5s, paired with a 175x70px accent span sweeping -26deg over 0.3s (delay 0.2s). Right (8 cols): numbered rows (.animation_home1_service x:-50->0 staggered timeline on scroll) separated by 1px borders.",
            "typography_specs": "Index numeral: text-sm font-mono text-[var(--text-secondary)]. Service title: 36px font-medium text-[var(--text-primary)]. Summary: text-base text-[var(--text-secondary)].",
            "key_components": "Sticky 15deg rotating preview image container + -26deg accent shape wipe, 01-05 numbered service rows, 170px circular CTA 'View All' trigger, >=44px row links.",
            "responsive_behavior": "Below 1024px hides fixed hover panel (prevents broken touch preview) and renders inline rows cleanly with ScrollTrigger x:-30->0 staggered entries.",
            "accessibility": "Keyboard focus (:focus-visible) triggers the exact same preview swap as pointer hover; full row exposes high-contrast emerald focus ring.",
            "anti_slop_rules": "Never use un-cleared setInterval inside mousemove handlers (use pure CSS/GPU compositor state classes); fix dark #212529 inherited copy contrast on dark #000000."
        }
    ],
    "results_metrics": [
        {
            "archetype_id": "res-07",
            "name": "Oversized 100px Light-Weight Bounce-Entry Count-Up Metric Strip",
            "keywords": "oversized-counters, count-up, bounce-entrance, dark-metrics, tabular-nums, agency-stats",
            "best_for": "Software agencies and product studios highlighting 3-4 flagship scale indicators with impactful vertical scroll drop choreography.",
            "selection_triggers": {"kinetic_dark": True, "oversized_counters": True},
            "layout_structure": "4-column dark full-width metric strip (grid-cols-2 lg:grid-cols-4 gap-8 py-16 border-y border-[var(--border-subtle)]). Cells drop in from y:-100 opacity:0 via GSAP ScrollTrigger (ease: 'bounce', duration: 1.5s, stagger: 0.3s at top center+=300).",
            "typography_specs": "Counter numeral: clamp(3rem, 1.8rem + 4.2vw, 6.25rem) font-normal leading-[1.1] tabular-nums text-[var(--text-primary)]. Descriptor: text-base font-normal text-[var(--text-secondary)].",
            "key_components": "ScrollTrigger bounce entrance + counter count-up digits, suffix span (M+, +), optional verified scope/date footnote below grid.",
            "responsive_behavior": "2x2 grid on 320-767px mobile viewports switching to per-item triggers (< 1023px); 4-column horizontal strip on desktop.",
            "accessibility": "Each stat container carries an aria-label with the final static value; bounce & count-up animations skip immediately under prefers-reduced-motion: reduce.",
            "anti_slop_rules": "Verify all numbers against a single source of truth so footer stats never contradict hero or about-page counters (SLOP-003)."
        }
    ],
    "portfolio": [
        {
            "archetype_id": "port-09",
            "name": "MixItUp Filterable Dark Case Study Grid with Velocity SkewY & Slide Overlay",
            "keywords": "mixitup-filter, velocity-skew, case-study-grid, dark-portfolio, vertical-filter-pills, pinned-header",
            "best_for": "Multi-industry software agencies showcasing 10-30+ client engagements filtered by vertical with scroll-velocity image motion.",
            "selection_triggers": {"kinetic_dark": True, "mixitup_filter": True},
            "layout_structure": "Filter bar of 44px-tall rounded-[5px] MixItUp pills (active bg #65BC7B with high-contrast #020617 ink) above 3-col cards (29% desktop / 48.5% tablet / 100% mobile) with horizontal divider lines (#items__border) and optional ScrollTrigger pinned title (.portfolio__title-wrap-6). Scrolling skews .portfolio__item-5 thumbnails along Y (velocity/-80 clamped -15..15deg); card hover slides .portfolio__content-5 badge from right:-70px opacity:0 to right:-50px opacity:1 over 0.5s.",
            "typography_specs": "Filter pill: text-sm font-medium. Category eyebrow: text-sm font-normal text-[var(--text-secondary)]. Project title: 24px font-medium text-[var(--text-primary)].",
            "key_components": "MixItUp filter buttons (aria-pressed), aspect-locked WebP cards, scroll-velocity skewY thumbnail, sliding hover/focus badge overlay.",
            "responsive_behavior": "1 column mobile (100%, metadata badge pinned visible at right:0 opacity:1), 2 columns tablet (48.5%), 3 columns desktop (29%); filter bar wraps cleanly.",
            "accessibility": "Expose aria-pressed on filter buttons + aria-live='polite' count; pair #65BC7B active pills with dark #020617 text (avoid white-on-#65BC7B low contrast) and mirror :hover content reveal on :focus-within.",
            "anti_slop_rules": "Disable velocity skewY and scale-2.5 scrub under prefers-reduced-motion; maintain consistent aspect ratios with zero uncropped raw PNG bloat."
        }
    ],
    "testimonials": [
        {
            "archetype_id": "tst-09",
            "name": "Video-Modal Testimonial Carousel with Cursor-Follower & Zoom Reveal",
            "keywords": "video-testimonial, modal-carousel, cursor-follower, circular-play, dark-reviews, executive-endorsement",
            "best_for": "B2B engineering agencies featuring recorded executive client interviews alongside written quotes, pointer-tracking media parallax, and video lightbox modals.",
            "selection_triggers": {"kinetic_dark": True, "has_video_reviews": True},
            "layout_structure": "Full-width dark carousel stage pairing a 16:9 / 4:3 executive video thumbnail (.animation_image_zoom scale 0.5->1 over 2.5s + +/-15px mouse-move parallax) and 250px play trigger / 80->100px .cursor-testi 'Play' follower beside quote headline, client name, and role subtitle.",
            "typography_specs": "Section title: clamp(2rem, 1.4rem + 2.5vw, 3.75rem) font-medium. Client name: text-lg font-medium text-[var(--text-primary)]. Client role: 14px font-normal text-[var(--text-secondary)].",
            "key_components": "Accessible video poster card, circular play trigger button, native <dialog> lightbox video player, contextual cursor follower (desktop >=1200px only), Swiper prev-next controls (>= 44x44px).",
            "responsive_behavior": "Video poster stacks above quote attribution on mobile; custom cursor hides <= 1200px while preserving explicit 44px+ play button trigger.",
            "accessibility": "Video modal traps focus, closes on Escape, restores focus to the trigger, and includes transcript/captions; custom cursor never replaces focusable button controls.",
            "anti_slop_rules": "Do not auto-play unmuted video; provide a real transcript or summary alongside video interviews so screen-reader users are never blocked."
        }
    ],
    "contact_location_map": [
        {
            "archetype_id": "cmap-03",
            "name": "Interactive Geo Coverage Map with Region Marquee Strip",
            "keywords": "geo-map, world-coverage, country-marquee, interactive-svg-map, global-delivery",
            "best_for": "Offshore/global software consultancies and staff augmentation partners illustrating international client delivery regions.",
            "selection_triggers": {"kinetic_dark": True, "geo_map": True},
            "layout_structure": "Full-width dark showcase pairing an interactive SVG choropleth/pin world map (with hover tooltips highlighting active delivery markets) and a continuous accent/neutral horizontal marquee listing covered countries.",
            "typography_specs": "Section heading: text-4xl sm:text-6xl font-medium text-[var(--text-primary)]. Country marquee items: text-lg font-medium tracking-wide.",
            "key_components": "Vector SVG world map with highlighted market fills (#3BC77B on #1E1E1E), accessible region list fallback, continuous marquee strip with pause button.",
            "responsive_behavior": "SVG map scales proportionally inside an aspect-[2/1] container on mobile; marquee remains single-row with reduced-motion pause.",
            "accessibility": "Provide an explicit accessible <ul> or <dl> regional summary alongside the SVG map (role='img') so keyboard and screen-reader users can inspect every covered country.",
            "anti_slop_rules": "Never use heavy unoptimized raster world maps or non-semantic click-only SVG paths without text equivalents."
        }
    ],
    "footer": [
        {
            "archetype_id": "ftr-07",
            "name": "Pre-Footer Consultation Banner + Dark 4-Column Sitemap Footer",
            "keywords": "pre-footer-cta, dark-footer, consultation-band, 4-column-sitemap, agency-footer",
            "best_for": "Dark kinetic agencies combining a high-impact consultation CTA + 3 proof stats right above a structured 4-column dark corporate footer.",
            "selection_triggers": {"kinetic_dark": True, "consultation_prefooter": True},
            "layout_structure": "Upper pre-footer band (py-20 bg-[var(--surface-raised)] border-t border-[var(--border-subtle)]): eyebrow, display quote headline, 3 inline KPI metrics, and circular CTA / consultation form. Lower footer (bg-[#000000] py-16): 4 columns (Brand summary + social icons, Navigation links, Contact address/phone/email, Legal & action buttons) + bottom copyright bar.",
            "typography_specs": "Pre-footer quote: text-3xl sm:text-5xl font-medium leading-tight. Column headings: text-xl font-semibold text-[var(--text-primary)]. Links/body: text-base text-[var(--text-secondary)] hover:text-[var(--color-action-primary)].",
            "key_components": "Pre-footer quote & KPI strip, 4-column semantic link/address footer, >= 44x44px social icon buttons, copyright bar.",
            "responsive_behavior": "Pre-footer stacks vertically on mobile; footer collapses from 4 columns desktop to 2 columns tablet and 1 column mobile.",
            "accessibility": "Semantic <footer> role='contentinfo'; single clear link list hierarchy; all footer/social links >= 24x24px (>= 44x44px touch); high contrast >= 4.5:1 on all muted copy.",
            "anti_slop_rules": "Avoid duplicating footer markup across hidden mobile/desktop DOM trees; maintain consistent single copyright year and verified metrics."
        }
    ],
}

NEW_SECTIONS = [
    {
        "section_id": "product_catalog_grid",
        "section_name": "Software Products & Solutions Catalog Grid",
        "archetypes": [
            {
                "archetype_id": "pcg-01",
                "name": "Asymmetric Staggered Product Showcase Cards",
                "keywords": "product-catalog, staggered-grid, software-products, dark-cards, portfolio-cards",
                "best_for": "Multi-product technology companies presenting 6-12 flagship software platforms (e.g. eKYC, LMS, Gateway, Security) on a single scannable index.",
                "selection_triggers": {"is_product_catalog": True, "kinetic_dark": True},
                "layout_structure": "Hero intro with staggered showcase strip followed by a 2- or 3-column dark card grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8). Each card features a 16:10 dark UI preview frame, product title (text-2xl font-medium), concise category tag, and detail link.",
                "typography_specs": "Page H1: clamp(2.75rem, 1.6rem + 4vw, 5.75rem) font-semibold leading-[1.06]. Card title: text-2xl font-medium text-[var(--text-primary)].",
                "key_components": "Product preview card, category badge, subtle hover image scale (1.03), circular arrow detail link, bottom demo CTA.",
                "responsive_behavior": "3 columns desktop, 2 columns tablet, 1 column mobile with full-width cards.",
                "accessibility": "Each product card uses <article> with a single descriptive primary link to avoid duplicate tab stops.",
                "anti_slop_rules": "No glowing neon borders or placeholder blurred mockups; use clean 1px #2C2C2C borders and real UI screen previews."
            },
            {
                "archetype_id": "pcg-02",
                "name": "Filterable Multi-Vertical Solution Grid",
                "keywords": "filterable-products, category-pills, enterprise-solutions, solution-directory",
                "best_for": "Enterprise solution providers categorizing SaaS/FinTech/Security tools by industry vertical or deployment model.",
                "selection_triggers": {"is_product_catalog": True, "has_categories": True},
                "layout_structure": "Top filter pill strip (All, FinTech, Identity, EdTech, Security, Operations) with rounded-[5px] min-h-[44px] triggers above a uniform 3-column solution card grid with capability bullets.",
                "typography_specs": "Filter pill: text-sm font-medium. Card title: text-xl font-semibold. Bullet text: text-sm text-[var(--text-secondary)].",
                "key_components": "Filter pill bar with aria-pressed state, solution cards with 3 capability highlights and 'Explore Solution' link.",
                "responsive_behavior": "Filter pills wrap cleanly on mobile with 8px gaps; grid collapses to 1 column.",
                "accessibility": "Filter changes announce visible count in an aria-live='polite' status region.",
                "anti_slop_rules": "Keep capability bullets concrete and technical; avoid generic marketing filler across every card."
            }
        ]
    },
    {
        "section_id": "product_feature_matrix",
        "section_name": "Product Capabilities & Multi-Portal Feature Matrix",
        "archetypes": [
            {
                "archetype_id": "pfm-01",
                "name": "8-Card Core Capability Grid + Additional Feature Chips",
                "keywords": "feature-grid, 8-card-matrix, capability-cards, product-detail, feature-chips",
                "best_for": "Detailed SaaS/enterprise product landing pages breaking down 6-8 core capabilities plus secondary compliance/integration chips.",
                "selection_triggers": {"is_product_detail": True},
                "layout_structure": "Structured dark capability grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6) with bordered feature tiles (#121212 bg, 1px solid #2C2C2C), followed by a compact 6-chip 'Additional Capabilities' row and 3-column KPI differentiator strip.",
                "typography_specs": "Feature title: text-[22px] font-normal leading-snug text-[var(--text-primary)]. Description: text-sm leading-relaxed text-[var(--text-secondary)]. Chip: text-xs font-mono.",
                "key_components": "Icon + title + short paragraph feature cards, secondary capability chips, 3-metric differentiator callouts.",
                "responsive_behavior": "4 columns desktop, 2 columns tablet, 1 column mobile with uniform vertical rhythm.",
                "accessibility": "Each capability card uses semantic heading hierarchy (H3 inside H2 section) and readable >= 4.5:1 body contrast.",
                "anti_slop_rules": "Never duplicate identical feature cards across hidden responsive DOM blocks; render one clean responsive CSS grid."
            },
            {
                "archetype_id": "pfm-02",
                "name": "Multi-Portal Role-Tabbed Feature Matrix",
                "keywords": "portal-tabs, role-features, admin-portal, user-portal, enterprise-modules",
                "best_for": "Multi-stakeholder enterprise systems (e.g. Visitor Management, LMS, Payment Gateways) with distinct End-User, Branch, and Admin portals.",
                "selection_triggers": {"is_product_detail": True, "has_portal": True},
                "layout_structure": "Segmented portal switcher (User Portal, Operations/Branch Portal, Company Admin Portal) revealing a 4-column role-specific feature grid with workflow diagram preview.",
                "typography_specs": "Tab button: text-sm font-semibold. Module title: text-lg font-medium. Body: text-sm text-[var(--text-secondary)].",
                "key_components": "Accessible tablist switching role-specific 4-card feature sets, paired UI screenshot frame, integration badges.",
                "responsive_behavior": "Tabs convert to scrollable segmented pills or stacked accordion panels on < 640px screens.",
                "accessibility": "Implements full WAI-ARIA Tabs pattern (role='tablist', role='tab', aria-selected, aria-controls, arrow-key navigation).",
                "anti_slop_rules": "Keep tab labels concise so controls never wrap awkwardly or clip on 320px viewports."
            }
        ]
    },
    {
        "section_id": "case_study_dossier",
        "section_name": "Case Study Metadata, Challenge/Solution & Gallery",
        "archetypes": [
            {
                "archetype_id": "csd-01",
                "name": "Metadata Summary Grid + Challenge/Solution Split & Visual Showcase",
                "keywords": "case-study-dossier, problem-solution, metadata-strip, ui-gallery, project-detail",
                "best_for": "Individual portfolio and engineering case study detail pages explaining client context, architectural challenge, and delivered UI.",
                "selection_triggers": {"is_case_study_detail": True},
                "layout_structure": "3-tier vertical flow: (1) 4-column project metadata bar (Industry, Services, Tech Stack, Timeline); (2) Full-width 16:9 UI showcase banner; (3) 2-column Challenge vs Solution split followed by feature breakdown cards and screen carousel.",
                "typography_specs": "Metadata label: text-xs font-mono uppercase tracking-wider text-[var(--text-secondary)]. Section H2: text-4xl sm:text-5xl font-medium. Body: text-base leading-relaxed.",
                "key_components": "Metadata definition list (<dl>), hero UI mockup image, Problem/Solution 2-column narrative, feature gallery carousel.",
                "responsive_behavior": "Metadata bar collapses from 4 columns to 2x2 on mobile; Challenge/Solution split stacks vertically.",
                "accessibility": "Carousel includes accessible prev/next controls and pause button; all UI showcase screenshots include descriptive alt text.",
                "anti_slop_rules": "Document concrete engineering decisions and delivered modules rather than generic praise or fabricated uplift percentages."
            },
            {
                "archetype_id": "csd-02",
                "name": "Impact Telemetry Banner + Next/Prev Dossier Navigation",
                "keywords": "case-study-navigation, next-prev-project, outcome-summary, dossier-footer",
                "best_for": "Bottom narrative closure on individual project/case study pages guiding evaluators seamlessly to related work or consultation.",
                "selection_triggers": {"is_case_study_detail": True, "has_proof_stats": True},
                "layout_structure": "Full-width dark outcome summary strip (3 audited deliverable/scale metrics) above a 2-column Next/Previous Case Study navigation card bar with hover arrow shift.",
                "typography_specs": "Metric value: text-4xl font-medium tabular-nums. Nav label: text-xs font-mono uppercase text-[var(--text-secondary)]. Project title: text-2xl font-medium.",
                "key_components": "Audited outcome stat cards, Next/Previous project link cards (>= 44px height) with directional SVG arrows.",
                "responsive_behavior": "Next/Prev cards stack vertically on mobile with clear directional labels.",
                "accessibility": "Navigation wrapped in <nav aria-label='Case study pagination'> with descriptive link text.",
                "anti_slop_rules": "Attach clear project scope context to any displayed scale numbers; avoid placeholder lorem text or dead links."
            }
        ]
    }
]


def main():
    with open(DATA_DIR / "section-archetypes.json", "r", encoding="utf-8") as f:
        sections = json.load(f)

    sec_map = {s["section_id"]: s for s in sections}

    for sid, new_archs in ARCHETYPE_EXTENSIONS.items():
        if sid not in sec_map:
            raise KeyError(f"Expected existing section_id {sid!r} not found")
        idx_map = {a["archetype_id"]: i for i, a in enumerate(sec_map[sid]["archetypes"])}
        for arch in new_archs:
            aid = arch["archetype_id"]
            if aid not in idx_map:
                sec_map[sid]["archetypes"].append(arch)
                idx_map[aid] = len(sec_map[sid]["archetypes"]) - 1
                print(f"  + Extended {sid} with {aid}")
            else:
                sec_map[sid]["archetypes"][idx_map[aid]] = arch
                print(f"  * Updated {sid}:{aid} in place")

    for new_sec in NEW_SECTIONS:
        sid = new_sec["section_id"]
        if sid not in sec_map:
            sections.append(new_sec)
            sec_map[sid] = new_sec
            print(f"  + Added section {sid} ({len(new_sec['archetypes'])} archetypes)")
        else:
            print(f"  * Section {sid} already present")

    write_sections_dataset(sections, DATA_DIR)


if __name__ == "__main__":
    main()
