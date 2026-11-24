#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Complete Production-Grade UI/UX Prompts.
Now includes:
- Full selection rules for all 15 sections
- Intent normalization layer for vague inputs
- Per-section fallback archetypes (never silently skips)
- Fallback warning log when triggered
"""

import json
import argparse
import sys
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import search

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# =====================================================
# INTENT NORMALIZATION (vague → domain vocabulary)
# =====================================================
INTENT_VOCABULARY = {
    "fresh": ["minimal", "clean", "modern"],
    "trustworthy": ["enterprise", "b2b", "corporate", "professional"],
    "exciting": ["bold", "creative", "dynamic", "editorial"],
    "premium": ["luxury", "editorial", "high-end", "boutique"],
    "simple": ["minimal", "single-column", "clean"],
    "technical": ["developer", "engineering", "terminal", "api"],
    "friendly": ["modern", "saas", "approachable"],
    "impressive": ["immersive", "interactive", "editorial", "bento"],
    "innovative": ["tech", "ai", "modern", "cutting-edge"],
}


def normalize_intent(raw_style: str) -> str:
    """Map vague adjectives to domain-searchable vocabulary."""
    lowered = raw_style.lower()
    tokens = []
    for vague, synonyms in INTENT_VOCABULARY.items():
        if vague in lowered:
            tokens.extend(synonyms)
    return " ".join(tokens) if tokens else raw_style


# =====================================================
# PER-SECTION SAFE FALLBACK ARCHETYPES
# =====================================================
SECTION_FALLBACKS = {
    # Homepage Core
    "navbar":                    "nav-02",   # Full-Width Enterprise Edge-to-Edge
    "hero":                      "hero-01",  # Split-Screen
    "trusted_by":                "tb-01",    # Infinite Greyscale Marquee
    "about":                     "abt-02",   # Split Mission & Metric Cards
    "services":                  "srv-01",   # 3-Column Feature Cards
    "why_choose_us":             "wcu-01",   # 4-Column Icon Feature Grid
    "how_we_work":               "hww-04",   # Big Number Typography
    "portfolio":                 "port-01",  # Masonry Visual Grid
    "testimonials":              "tst-01",   # Masonry Wall of Love
    "results_metrics":           "res-01",   # 4-Column Animated Counter Strip
    "pricing":                   "prc-01",   # 3-Tier Standard Cards
    "team":                      "team-01",  # Card Grid
    "faq":                       "faq-01",   # Single-Column Centered Accordion
    "final_cta":                 "cta-01",   # High-Impact Contrast Card Band
    "footer":                    "ftr-01",   # Multi-Column Sitemap Hub
    # Dedicated Pricing Page
    "pricing_hero":              "phero-01", # Centered Toggle Hero with Trial Chip
    "pricing_comparison_matrix": "pmat-01",  # Sticky Header Grouped Category Matrix
    "pricing_addons":            "padd-01",  # 2-Column Selectable Add-on Card Grid
    "pricing_enterprise_sla":    "psla-01",  # Full-Width High-Trust Procurement Card
    "pricing_guarantee_bar":     "pbar-01",  # 3-Badge Security & Money-Back Strip
    # Dedicated About Page
    "about_timeline":            "time-01",  # Vertical Alternating Milestone Spine
    "about_values":              "val-01",   # 6-Card Numbered Principle Grid
    "about_culture_gallery":     "cult-01",  # Curated Multi-Aspect Studio Collage
    "about_leadership_board":    "lead-01",  # C-Suite Grid with Alumni Credibility Badges
    # Dedicated Services Page
    "service_architecture":      "arch-01",  # Node-Based Data Pipeline Diagram
    "service_deliverables_matrix": "deliv-01",# Categorized Scope & Artifact Accordion
    "service_tech_stack":        "stack-01", # Categorized Monochromatic Tech Stack Grid
    "service_use_cases":         "use-01",   # Industry Tabbed Solution Switcher
}

fallback_warnings = []


def load_json_dataset():
    json_path = DATA_DIR / "section-archetypes.json"
    if not json_path.exists():
        raise FileNotFoundError(f"Dataset missing: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_page_templates():
    tpl_path = DATA_DIR / "page-templates.json"
    if not tpl_path.exists():
        return None
    with open(tpl_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_archetype(archetypes, archetype_id, section_id, reason="fallback"):
    """Find archetype by ID with fallback warning."""
    match = next((a for a in archetypes if a["archetype_id"] == archetype_id), None)
    if match:
        return match
    # Hard fallback: return first available
    fallback_warnings.append(
        f"[FALLBACK] section={section_id}: archetype {archetype_id!r} not found "
        f"(reason: {reason}). Using first available: {archetypes[0]['archetype_id']!r}"
    )
    return archetypes[0]


def select_archetype(section_data: dict, project_info: dict) -> dict:
    """
    Full selection matrix for all 15 sections.
    Every branch ends in an explicit archetype_id or falls back safely.
    Never returns None.
    """
    archetypes = section_data.get("archetypes", [])
    sec_id = section_data.get("section_id", "")

    if not archetypes:
        fallback_warnings.append(f"[ERROR] section={sec_id} has 0 archetypes — dataset issue")
        return {"archetype_id": "MISSING", "name": "MISSING", "best_for": "", "layout_structure": "",
                "typography_specs": "", "key_components": "", "responsive_behavior": "",
                "accessibility": "", "anti_slop_rules": ""}

    def pick(aid):
        return get_archetype(archetypes, aid, sec_id)

    # ── NAVBAR ────────────────────────────────────────────
    if sec_id == "navbar":
        link_count = project_info.get("link_count", 5)
        if project_info.get("mega_menu"):            return pick("nav-03")
        if project_info.get("style") == "editorial": return pick("nav-05")
        if project_info.get("has_portal"):           return pick("nav-06")
        if link_count <= 5:                          return pick("nav-01")
        return pick("nav-02")

    # ── HERO ─────────────────────────────────────────────
    elif sec_id == "hero":
        if project_info.get("has_video"):            return pick("hero-03")
        if project_info.get("lead_magnet"):          return pick("hero-04")
        if project_info.get("has_3d"):               return pick("hero-09")
        s = project_info.get("style", "").lower()
        if "minimalist" in s or "editorial" in s:    return pick("hero-02")
        if project_info.get("has_mockup", True):     return pick("hero-01")
        return pick("hero-07")

    # ── TRUSTED BY ───────────────────────────────────────
    elif sec_id == "trusted_by":
        logo_count = project_info.get("logo_count", 8)
        if project_info.get("compliance_required"):  return pick("tb-06")
        if project_info.get("has_press"):            return pick("tb-04")
        if project_info.get("has_case_studies"):     return pick("tb-05")
        if logo_count >= 8:                          return pick("tb-01")
        return pick("tb-02")

    # ── ABOUT ────────────────────────────────────────────
    elif sec_id == "about":
        if project_info.get("has_video"):            return pick("abt-06")
        if project_info.get("founder_led"):          return pick("abt-01")
        years = project_info.get("years_operating", 0)
        if years >= 5:                               return pick("abt-03")
        if project_info.get("has_office_photos"):    return pick("abt-04")
        s = project_info.get("style", "").lower()
        if "editorial" in s or "minimalist" in s:    return pick("abt-05")
        return pick("abt-02")

    # ── SERVICES ─────────────────────────────────────────
    elif sec_id == "services":
        count = project_info.get("service_count", 3)
        if project_info.get("target_audience") == "developers/ctos":  return pick("srv-08")
        if project_info.get("enterprise"):           return pick("srv-07")
        if project_info.get("is_productized"):       return pick("srv-06")
        if project_info.get("mobile_heavy"):         return pick("srv-05")
        if project_info.get("wants_tabs"):           return pick("srv-04")
        s = project_info.get("style", "").lower()
        if "creative" in s or "editorial" in s:      return pick("srv-02")
        if project_info.get("has_flagship_service"): return pick("srv-03")
        return pick("srv-01")

    # ── WHY CHOOSE US ────────────────────────────────────
    elif sec_id == "why_choose_us":
        if project_info.get("has_founder_video"):    return pick("wcu-05")
        if project_info.get("has_certifications"):   return pick("wcu-06")
        if project_info.get("enterprise"):           return pick("wcu-04")
        if project_info.get("high_competition"):     return pick("wcu-02")
        if project_info.get("has_proof_stats"):      return pick("wcu-03")
        return pick("wcu-01")

    # ── HOW WE WORK ──────────────────────────────────────
    elif sec_id == "how_we_work":
        step_count = project_info.get("step_count", 4)
        if project_info.get("is_cyclical"):          return pick("hww-09")
        if project_info.get("has_rich_media"):       return pick("hww-10")
        s = project_info.get("style", "").lower()
        if "creative" in s and project_info.get("immersive"): return pick("hww-07")
        if project_info.get("is_non_linear"):        return pick("hww-05")
        if project_info.get("has_step_images"):      return pick("hww-06")
        if step_count > 6:                           return pick("hww-08")
        if step_count >= 5:                          return pick("hww-02")
        if "bento" in s or "contemporary" in s:      return pick("hww-12")
        return pick("hww-04")

    # ── PORTFOLIO ────────────────────────────────────────
    elif sec_id == "portfolio":
        case_count = project_info.get("case_count", 6)
        s = project_info.get("style", "").lower()
        if "avant-garde" in s or "editorial" in s:  return pick("port-08")
        if case_count >= 10:                         return pick("port-04")
        if project_info.get("has_metrics"):          return pick("port-02")
        if project_info.get("enterprise"):           return pick("port-03")
        if project_info.get("focus") == "responsive_web": return pick("port-06")
        if project_info.get("analytical"):           return pick("port-07")
        if case_count <= 5:                          return pick("port-05")
        return pick("port-01")

    # ── TESTIMONIALS ─────────────────────────────────────
    elif sec_id == "testimonials":
        reviews = project_info.get("review_count", 5)
        if project_info.get("has_video_reviews"):   return pick("tst-03")
        if reviews > 20:                            return pick("tst-07")
        if reviews > 10:                            return pick("tst-01")
        if project_info.get("has_analytics_data"):  return pick("tst-05")
        if project_info.get("social_proof_type") == "social_posts": return pick("tst-04")
        if project_info.get("has_vip_quote"):       return pick("tst-02")
        if project_info.get("wants_compact"):       return pick("tst-08")
        return pick("tst-01")

    # ── RESULTS / METRICS ────────────────────────────────
    elif sec_id == "results_metrics":
        if project_info.get("has_live_data"):        return pick("res-05")
        if project_info.get("has_before_after"):     return pick("res-02")
        if project_info.get("has_analytics_data"):   return pick("res-03")
        years = project_info.get("years_operating", 0)
        if years >= 5:                               return pick("res-04")
        if project_info.get("enterprise") and project_info.get("has_named_quotes"):
            return pick("res-06")
        return pick("res-01")

    # ── PRICING ──────────────────────────────────────────
    elif sec_id == "pricing":
        if project_info.get("is_productized"):       return pick("prc-04")
        if project_info.get("custom_quotes"):        return pick("prc-06")
        if project_info.get("has_annual_discount"):  return pick("prc-02")
        if project_info.get("pricing_model") == "usage/scope_based": return pick("prc-03")
        if project_info.get("enterprise") and project_info.get("feature_density") == "high":
            return pick("prc-05")
        return pick("prc-01")

    # ── TEAM ─────────────────────────────────────────────
    elif sec_id == "team":
        team_size = project_info.get("team_size", 6)
        if team_size >= 30:                          return pick("team-06")
        if team_size >= 15 and project_info.get("has_departments"): return pick("team-04")
        if project_info.get("has_editorial_photos"): return pick("team-05")
        if project_info.get("culture_focus"):        return pick("team-03")
        if project_info.get("founder_led"):          return pick("team-02")
        return pick("team-01")

    # ── FAQ ──────────────────────────────────────────────
    elif sec_id == "faq":
        faq_count = project_info.get("faq_count", 6)
        if faq_count >= 15:                          return pick("faq-04")
        if faq_count >= 10 and project_info.get("has_categories"): return pick("faq-02")
        if project_info.get("goal") == "consultation": return pick("faq-05")
        if project_info.get("wants_compact"):        return pick("faq-06")
        if faq_count <= 6 and project_info.get("answers_short"): return pick("faq-03")
        return pick("faq-01")

    # ── FINAL CTA ────────────────────────────────────────
    elif sec_id == "final_cta":
        if project_info.get("direct_calendar"):      return pick("cta-02")
        if project_info.get("lead_magnet"):          return pick("cta-03")
        if project_info.get("needs_qualification"):  return pick("cta-04")
        if project_info.get("founder_led") and project_info.get("brand_tier") == "boutique":
            return pick("cta-05")
        if project_info.get("has_enterprise_tier"):  return pick("cta-06")
        return pick("cta-01")

    # ── FOOTER ───────────────────────────────────────────
    elif sec_id == "footer":
        if project_info.get("has_mobile_app"):       return pick("ftr-06")
        if project_info.get("has_multiple_offices"): return pick("ftr-05")
        if project_info.get("has_newsletter"):       return pick("ftr-03")
        s = project_info.get("style", "").lower()
        if "editorial" in s or "luxury" in s:        return pick("ftr-02")
        if project_info.get("single_page"):          return pick("ftr-04")
        return pick("ftr-01")

    # ── PRICING HERO ─────────────────────────────────────
    elif sec_id == "pricing_hero":
        if project_info.get("pricing_model") == "usage_based": return pick("phero-03")
        if project_info.get("has_roi") or project_info.get("enterprise"): return pick("phero-02")
        return pick("phero-01")

    # ── PRICING COMPARISON MATRIX ────────────────────────
    elif sec_id == "pricing_comparison_matrix":
        if project_info.get("matrix_tabs"):          return pick("pmat-02")
        if project_info.get("minimal_diff"):         return pick("pmat-03")
        return pick("pmat-01")

    # ── PRICING ADDONS ───────────────────────────────────
    elif sec_id == "pricing_addons":
        if project_info.get("addon_compact"):        return pick("padd-02")
        return pick("padd-01")

    # ── PRICING ENTERPRISE SLA ───────────────────────────
    elif sec_id == "pricing_enterprise_sla":
        if project_info.get("direct_rfq_form"):      return pick("psla-02")
        return pick("psla-01")

    # ── PRICING GUARANTEE BAR ────────────────────────────
    elif sec_id == "pricing_guarantee_bar":
        if project_info.get("mobile_drawer"):        return pick("pbar-02")
        return pick("pbar-01")

    # ── ABOUT TIMELINE ───────────────────────────────────
    elif sec_id == "about_timeline":
        if project_info.get("timeline_horizontal"):  return pick("time-02")
        s = project_info.get("style", "").lower()
        if "minimalist" in s or "editorial" in s:   return pick("time-03")
        return pick("time-01")

    # ── ABOUT VALUES ─────────────────────────────────────
    elif sec_id == "about_values":
        if project_info.get("has_manifesto") or project_info.get("founder_led"): return pick("val-02")
        s = project_info.get("style", "").lower()
        if "bento" in s or "contemporary" in s:      return pick("val-03")
        return pick("val-01")

    # ── ABOUT CULTURE GALLERY ────────────────────────────
    elif sec_id == "about_culture_gallery":
        if project_info.get("distributed_team"):     return pick("cult-02")
        if project_info.get("culture_focus"):        return pick("cult-03")
        return pick("cult-01")

    # ── ABOUT LEADERSHIP BOARD ───────────────────────────
    elif sec_id == "about_leadership_board":
        if project_info.get("has_investors"):        return pick("lead-02")
        return pick("lead-01")

    # ── SERVICE ARCHITECTURE ─────────────────────────────
    elif sec_id == "service_architecture":
        if project_info.get("arch_layered"):         return pick("arch-02")
        if project_info.get("workflow_phases") or project_info.get("service_model") == "consulting":
            return pick("arch-03")
        return pick("arch-01")

    # ── SERVICE DELIVERABLES MATRIX ──────────────────────
    elif sec_id == "service_deliverables_matrix":
        if project_info.get("has_sla"):              return pick("deliv-02")
        if project_info.get("interactive_scope"):    return pick("deliv-03")
        return pick("deliv-01")

    # ── SERVICE TECH STACK ───────────────────────────────
    elif sec_id == "service_tech_stack":
        if project_info.get("has_partners"):         return pick("stack-02")
        if project_info.get("searchable_integrations"): return pick("stack-03")
        return pick("stack-01")

    # ── SERVICE USE CASES ────────────────────────────────
    elif sec_id == "service_use_cases":
        if project_info.get("multi_persona"):        return pick("use-02")
        return pick("use-01")

    # ── GLOBAL FALLBACK (unknown section) ────────────────
    else:
        fallback_id = SECTION_FALLBACKS.get(sec_id, archetypes[0]["archetype_id"])
        fallback_warnings.append(
            f"[FALLBACK] Unknown section_id={sec_id!r}; using default {fallback_id!r}"
        )
        return pick(fallback_id)


# =====================================================
# PROMPT GENERATOR
# =====================================================

def generate_master_prompt(project_info: dict) -> str:
    all_sections = load_json_dataset()
    section_map = {s["section_id"]: s for s in all_sections}

    page_id = project_info.get("page_id", "home")
    templates = load_page_templates()
    page_meta = None
    if templates and "pages" in templates:
        page_meta = next((p for p in templates["pages"] if p["page_id"] == page_id), None)

    if page_meta and "default_section_flow" in page_meta:
        sections = []
        for sid in page_meta["default_section_flow"]:
            if sid in section_map:
                sections.append(section_map[sid])
            else:
                fallback_warnings.append(f"[WARN] Page '{page_id}' requested section '{sid}' which is not in dataset yet")
        page_display_name = page_meta.get("name", page_id.title())
    else:
        sections = all_sections
        page_display_name = "Full System (15 Sections)"

    proj_name = project_info.get("project_name", "Modern Web Platform")
    raw_style = project_info.get("style", "Industrial Precision / Minimalist")
    target = project_info.get("target_audience", "B2B Decision Makers")

    # Normalize intent for color/typography lookups
    normalized = normalize_intent(raw_style)
    color_query = project_info.get("industry", "b2b") + " " + normalized
    typo_query = normalized + " tech"

    color_res = search(color_query, "color", 1)
    color_row = color_res.get("results", [{}])[0] if color_res.get("results") else {}

    typo_res = search(typo_query, "typography", 1)
    typo_row = typo_res.get("results", [{}])[0] if typo_res.get("results") else {}

    p = []
    p.append(f"# Master Production-Grade UI/UX Blueprint")
    p.append(f"**Project:** {proj_name}")
    p.append(f"**Page:** {page_display_name} (`{page_id}`)")
    p.append(f"**Style Archetype:** {raw_style}")
    p.append(f"**Target Audience:** {target}")
    p.append(f"**Sections covered:** {len(sections)} sections")
    p.append(f"**Compliance:** WCAG 2.2 AA | Anti-Slop Gates Enabled\n")

    p.append("---")
    p.append("## 1. Global Design Token Foundation")
    p.append(f"- **Surface Background:** `{color_row.get('Background (Hex)', '#0B0F17')}`")
    p.append(f"- **Card Surface / Raised:** `#151C28`")
    p.append(f"- **Primary Action:** `{color_row.get('CTA (Hex)', '#2563EB')}` — dual-ring focus")
    p.append(f"- **Text Primary:** `{color_row.get('Text (Hex)', '#F8FAFC')}`")
    p.append(f"- **Text Secondary:** `#94A3B8`")
    p.append(f"- **Border Subtle:** `{color_row.get('Border (Hex)', '#1E293B')}` (1px solid)")
    p.append(f"- **Heading Font:** `{typo_row.get('Heading Font', 'Space Grotesk')}` — Bold, tracking-tight")
    p.append(f"- **Body Font:** `{typo_row.get('Body Font', 'Inter')}` — 400/500, leading-relaxed")
    p.append(f"- **Mono / Chips:** `JetBrains Mono` or `ui-monospace`")
    p.append(f"- **Motion:** 150–200ms `cubic-bezier(0.16,1,0.3,1)`, compositor-only (`transform`, `opacity`)")
    p.append(f"- **Anti-Slop:** Zero gradient blobs · Zero emoji icons · Zero rainbow borders\n")

    p.append("---")
    p.append("## 2. Section-by-Section Blueprint\n")

    for i, sec in enumerate(sections, 1):
        chosen = select_archetype(sec, project_info)
        sec_name = sec.get("section_name", sec.get("section_id"))
        p.append(f"### {i:02d}. {sec_name}")
        p.append(f"**Pattern:** {chosen['name']} (`{chosen['archetype_id']}`)")
        p.append(f"**Rationale:** {chosen['best_for']}")
        p.append(f"**Layout:** {chosen['layout_structure']}")
        p.append(f"**Typography:** {chosen['typography_specs']}")
        p.append(f"**Components:** {chosen['key_components']}")
        p.append(f"**Responsive:** {chosen['responsive_behavior']}")
        p.append(f"**A11y:** {chosen['accessibility']}")
        p.append(f"**Anti-Slop:** {chosen['anti_slop_rules']}\n")

    p.append("---")
    p.append("## 3. Universal Interactive State Matrix")
    p.append("All buttons, inputs, cards, accordions MUST implement:")
    p.append("1. `default` — Resting semantic token colors")
    p.append("2. `hover` — Subtle transform/brightness shift (duration-150)")
    p.append("3. `focus-visible` — `outline-2 outline-offset-2 outline-blue-600 forced-colors:outline-[Highlight]`")
    p.append("4. `active` — Tactical downscale `scale-[0.98]`")
    p.append("5. `disabled` — `opacity-50 cursor-not-allowed pointer-events-none`")
    p.append("6. `loading` — Animated SVG spinner + `aria-busy='true'` + label preserved")
    p.append("7. `error` — `aria-invalid='true'` + `aria-describedby` pointing to inline error\n")

    if fallback_warnings:
        p.append("---")
        p.append("## 4. Generator Warnings")
        for w in fallback_warnings:
            p.append(f"- {w}")

    return "\n".join(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Production UI/UX Master Prompt")
    parser.add_argument("--page", default="home", choices=["home", "pricing", "about", "services", "case_studies", "contact", "blog", "careers", "legal"], help="Page type")
    parser.add_argument("--name", default="Apex Growth Agency", help="Project name")
    parser.add_argument("--style", default="Industrial Minimalist", help="Style archetype")
    parser.add_argument("--industry", default="b2b", help="Industry for color lookup")
    parser.add_argument("--steps", type=int, default=4, help="Process step count")
    parser.add_argument("--reviews", type=int, default=12, help="Review count")
    parser.add_argument("--team-size", type=int, default=6, help="Team size")
    parser.add_argument("--faq-count", type=int, default=6, help="FAQ count")
    parser.add_argument("--calendar", action="store_true", help="Use calendar booking CTA")
    parser.add_argument("--productized", action="store_true", help="Flat-rate productized pricing")
    parser.add_argument("--founder-led", action="store_true", help="Founder-led agency")
    parser.add_argument("--has-stats", action="store_true", help="Agency has proof stats")
    parser.add_argument("--enterprise", action="store_true", help="Enterprise tier targeting")
    # Pricing Page flags
    parser.add_argument("--billing-toggle", action="store_true", help="Include billing cycle toggle")
    parser.add_argument("--has-matrix", action="store_true", help="Include deep feature comparison matrix")
    parser.add_argument("--matrix-tabs", action="store_true", help="Use tabbed feature matrix")
    parser.add_argument("--minimal-diff", action="store_true", help="Use delta/diff-only matrix")
    parser.add_argument("--has-addons", action="store_true", help="Include modular add-on upgrades")
    parser.add_argument("--addon-compact", action="store_true", help="Compact horizontal addon strip")
    parser.add_argument("--has-sla", action="store_true", help="Include enterprise procurement / SLA card")
    parser.add_argument("--direct-rfq", action="store_true", help="Direct RFQ inquiry form")
    parser.add_argument("--has-guarantee", action="store_true", help="Include risk reversal guarantee banner")
    parser.add_argument("--mobile-drawer", action="store_true", help="Sticky bottom mobile checkout drawer")
    parser.add_argument("--roi-calc", action="store_true", help="Interactive ROI payback estimator")
    parser.add_argument("--usage-based", action="store_true", help="Usage-based consumption pricing")
    # About Page flags
    parser.add_argument("--timeline-horizontal", action="store_true", help="Horizontal timeline carousel")
    parser.add_argument("--has-manifesto", action="store_true", help="Founder core thesis manifesto")
    parser.add_argument("--distributed-team", action="store_true", help="Global distributed hubs and remote map")
    parser.add_argument("--culture-focus", action="store_true", help="Focus on team working norms and culture quotes")
    parser.add_argument("--has-investors", action="store_true", help="Tier-1 VC backers and advisory board")
    parser.add_argument("--has-office-photos", action="store_true", help="Studio and authentic office photo collage")
    # Services Page flags
    parser.add_argument("--arch-layered", action="store_true", help="Layered enterprise stack architecture diagram")
    parser.add_argument("--workflow-phases", action="store_true", help="4-phase delivery workflow and milestone outputs")
    parser.add_argument("--interactive-scope", action="store_true", help="Interactive module scope configurator")
    parser.add_argument("--has-partners", action="store_true", help="Official certified cloud partner badges")
    parser.add_argument("--searchable-integrations", action="store_true", help="Searchable integration ecosystem playground")
    parser.add_argument("--multi-persona", action="store_true", help="Role-based persona solution cards (CTO/CMO/CFO)")
    parser.add_argument("--out", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    project = {
        "page_id": args.page,
        "project_name": args.name,
        "style": args.style,
        "industry": args.industry,
        "step_count": args.steps,
        "review_count": args.reviews,
        "team_size": args.team_size,
        "faq_count": args.faq_count,
        "direct_calendar": args.calendar,
        "is_productized": args.productized,
        "founder_led": args.founder_led,
        "has_proof_stats": args.has_stats,
        "enterprise": args.enterprise,
        "target_audience": "Enterprise & Growth Leaders" if args.enterprise else "B2B Marketing and Sales Leaders",
        "has_mockup": True,
        "logo_count": 10,
        # Pricing Page variables
        "has_billing_toggle": args.billing_toggle,
        "has_matrix": args.has_matrix,
        "matrix_tabs": args.matrix_tabs,
        "minimal_diff": args.minimal_diff,
        "has_addons": args.has_addons,
        "addon_compact": args.addon_compact,
        "compliance": args.has_sla,
        "direct_rfq_form": args.direct_rfq,
        "has_guarantee": args.has_guarantee,
        "mobile_drawer": args.mobile_drawer,
        "has_roi": args.roi_calc,
        "pricing_model": "usage_based" if args.usage_based else "subscription",
        # About Page variables
        "timeline_horizontal": args.timeline_horizontal,
        "has_manifesto": args.has_manifesto,
        "distributed_team": args.distributed_team,
        "culture_focus": args.culture_focus,
        "has_investors": args.has_investors,
        "has_office_photos": args.has_office_photos,
        # Services Page variables
        "arch_layered": args.arch_layered,
        "workflow_phases": args.workflow_phases,
        "interactive_scope": args.interactive_scope,
        "has_partners": args.has_partners,
        "searchable_integrations": args.searchable_integrations,
        "multi_persona": args.multi_persona,
    }

    prompt = generate_master_prompt(project)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"[OK] Prompt written: {args.out}")
        if fallback_warnings:
            print(f"[WARN] {len(fallback_warnings)} fallback(s) triggered:")
            for w in fallback_warnings:
                print(f"  {w}")
    else:
        print(prompt[:2000])
        print(f"\n... [preview truncated] | Full: use --out flag")
        if fallback_warnings:
            for w in fallback_warnings:
                print(f"  {w}")
