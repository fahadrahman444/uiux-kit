#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Complete Production-Grade UI/UX Prompts.
Includes:
- Full selection rules covering 100% of archetypes across all 43 sections / 13 pages
- Non-destructive intent normalization layer for vague inputs
- Dynamic luminance-aware surface/text token derivation (WCAG 2.2 AA safe)
- Isolated per-call warning collection and safe fallbacks
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import search

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# =====================================================
# INTENT NORMALIZATION (vague -> domain vocabulary)
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
    "kinetic": ["dark", "emerald", "agency", "motion"],
}


def normalize_intent(raw_style: str) -> str:
    """Expand vague adjectives while preserving explicit style tokens."""
    lowered = raw_style.lower()
    tokens = re.findall(r"[a-z0-9-]+", lowered)
    expanded = []
    for vague, synonyms in INTENT_VOCABULARY.items():
        if re.search(rf"\b{re.escape(vague)}\b", lowered):
            for syn in synonyms:
                if syn not in tokens and syn not in expanded:
                    expanded.append(syn)
    return " ".join(tokens + expanded) if expanded else raw_style


# =====================================================
# CONTRAST & SURFACE TOKEN DERIVATION
# =====================================================
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def _relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def linearize(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = _relative_luminance(c1), _relative_luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def derive_surface_tokens(color_row: dict) -> dict:
    """Derive WCAG-compliant raised surface, secondary text, and CTA text tokens."""
    bg_hex = color_row.get("Background (Hex)", "#0B0F17").strip()
    cta_hex = color_row.get("CTA (Hex)", "#2563EB").strip()
    text_hex = color_row.get("Text (Hex)", "#F8FAFC").strip()
    border_hex = color_row.get("Border (Hex)", "#1E293B").strip()

    if not HEX_RE.match(bg_hex):
        bg_hex = "#0B0F17"
    if not HEX_RE.match(text_hex):
        text_hex = "#F8FAFC"
    if not HEX_RE.match(cta_hex):
        cta_hex = "#2563EB"
    if not HEX_RE.match(border_hex):
        border_hex = "#1E293B"

    is_light = _relative_luminance(bg_hex) > 0.5
    if is_light:
        card_surface = "#FFFFFF" if bg_hex.upper() != "#FFFFFF" else "#F8FAFC"
        text_secondary = "#475569"
        if _contrast_ratio(text_secondary, bg_hex) < 4.5 or _contrast_ratio(text_secondary, card_surface) < 4.5:
            text_secondary = "#334155"
        if _contrast_ratio(text_secondary, bg_hex) < 4.5 or _contrast_ratio(text_secondary, card_surface) < 4.5:
            text_secondary = text_hex
    else:
        card_surface = "#151C28" if bg_hex.upper() != "#151C28" else "#1E293B"
        text_secondary = "#94A3B8"
        if _contrast_ratio(text_secondary, bg_hex) < 4.5 or _contrast_ratio(text_secondary, card_surface) < 4.5:
            text_secondary = "#CBD5E1"
        if _contrast_ratio(text_secondary, bg_hex) < 4.5 or _contrast_ratio(text_secondary, card_surface) < 4.5:
            text_secondary = text_hex

    cta_text = "#FFFFFF" if _contrast_ratio("#FFFFFF", cta_hex) >= _contrast_ratio("#020617", cta_hex) else "#020617"

    return {
        "background": bg_hex,
        "card_surface": card_surface,
        "cta": cta_hex,
        "cta_text": cta_text,
        "text_primary": text_hex,
        "text_secondary": text_secondary,
        "border_subtle": border_hex,
    }


# =====================================================
# PER-SECTION SAFE FALLBACK ARCHETYPES
# =====================================================
SECTION_FALLBACKS = {
    # Homepage Core
    "navbar": "nav-02",
    "hero": "hero-01",
    "trusted_by": "tb-01",
    "about": "abt-02",
    "services": "srv-01",
    "why_choose_us": "wcu-01",
    "how_we_work": "hww-04",
    "portfolio": "port-01",
    "testimonials": "tst-01",
    "results_metrics": "res-01",
    "pricing": "prc-01",
    "team": "team-01",
    "faq": "faq-01",
    "final_cta": "cta-01",
    "footer": "ftr-01",
    # Dedicated Pricing Page
    "pricing_hero": "phero-01",
    "pricing_comparison_matrix": "pmat-01",
    "pricing_addons": "padd-01",
    "pricing_enterprise_sla": "psla-01",
    "pricing_guarantee_bar": "pbar-01",
    # Dedicated About Page
    "about_timeline": "time-01",
    "about_values": "val-01",
    "about_culture_gallery": "cult-01",
    "about_leadership_board": "lead-01",
    # Dedicated Services Page
    "service_architecture": "arch-01",
    "service_deliverables_matrix": "deliv-01",
    "service_tech_stack": "stack-01",
    "service_use_cases": "use-01",
    # Dedicated Contact Page
    "contact_intake_form": "cform-01",
    "contact_location_map": "cmap-01",
    "contact_sla_banner": "csla-01",
    # Dedicated Case Studies Page
    "case_study_hero_highlight": "csh-01",
    "case_study_filter_hub": "csf-01",
    "case_study_client_quote_strip": "csq-01",
    # Dedicated Blog Page
    "blog_featured_editorial": "bfeat-01",
    "blog_topic_filter_feed": "bfeed-01",
    "blog_newsletter_capture": "bnews-01",
    # Dedicated Careers Page
    "careers_perks": "perk-01",
    "careers_jobs": "jobs-01",
    # Dedicated Legal Page
    "legal_doc": "leg-01",
    # Product Showcase, Product/Service Detail & Case Study Dossier Pages
    "product_catalog_grid": "pcg-01",
    "product_feature_matrix": "pfm-01",
    "case_study_dossier": "csd-01",
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


def get_archetype(archetypes, archetype_id, section_id, reason="fallback", warnings=None):
    """Find archetype by ID with fallback warning."""
    match = next((a for a in archetypes if a["archetype_id"] == archetype_id), None)
    if match:
        return match
    target_log = warnings if warnings is not None else fallback_warnings
    target_log.append(
        f"[FALLBACK] section={section_id}: archetype {archetype_id!r} not found "
        f"(reason: {reason}). Using first available: {archetypes[0]['archetype_id']!r}"
    )
    return archetypes[0]


def select_archetype(section_data: dict, project_info: dict, warnings: list = None) -> dict:
    """
    Full selection matrix covering all sections and archetypes.
    Every branch ends in an explicit archetype_id or falls back safely.
    Never returns None.
    """
    target_log = warnings if warnings is not None else fallback_warnings
    archetypes = section_data.get("archetypes", [])
    sec_id = section_data.get("section_id", "")

    if not archetypes:
        target_log.append(f"[ERROR] section={sec_id} has 0 archetypes — dataset issue")
        return {
            "archetype_id": "MISSING", "name": "MISSING", "best_for": "",
            "layout_structure": "", "typography_specs": "", "key_components": "",
            "responsive_behavior": "", "accessibility": "", "anti_slop_rules": ""
        }

    def pick(aid):
        return get_archetype(archetypes, aid, sec_id, warnings=target_log)

    s = project_info.get("style", "").lower()

    # ── NAVBAR ────────────────────────────────────────────
    if sec_id == "navbar":
        link_count = project_info.get("link_count", 5)
        if project_info.get("mega_menu"):
            return pick("nav-03")
        if (project_info.get("lead_header")
                or project_info.get("primary_goal") == "phone/lead"
                or project_info.get("conversion_focus") == "ultra-high"):
            return pick("nav-04")
        if project_info.get("kinetic_dark") or project_info.get("has_dropdowns") or "kinetic" in s:
            return pick("nav-07")
        if "editorial" in s:
            return pick("nav-05")
        if project_info.get("has_portal"):
            return pick("nav-06")
        if link_count <= 5:
            return pick("nav-01")
        return pick("nav-02")

    # ── HERO ─────────────────────────────────────────────
    elif sec_id == "hero":
        if project_info.get("kinetic_dark") or project_info.get("circular_cta") or "kinetic" in s:
            return pick("hero-11")
        if project_info.get("has_video"):
            return pick("hero-03")
        if project_info.get("lead_magnet"):
            return pick("hero-04")
        if project_info.get("has_3d"):
            return pick("hero-09")
        if project_info.get("bento_hero") or "bento" in s or project_info.get("has_multiple_features"):
            return pick("hero-05")
        if project_info.get("has_app_mockups"):
            return pick("hero-06")
        if project_info.get("cro_split") or project_info.get("focus") == "transformation":
            return pick("hero-10")
        if ("editorial" in s or "swiss" in s) and project_info.get("brand_tier") == "luxury":
            return pick("hero-08")
        if "minimalist" in s or "editorial" in s:
            return pick("hero-02")
        if project_info.get("has_mockup", True):
            return pick("hero-01")
        return pick("hero-07")

    # ── TRUSTED BY ───────────────────────────────────────
    elif sec_id == "trusted_by":
        logo_count = project_info.get("logo_count", 8)
        if project_info.get("kinetic_dark") or "kinetic" in s:
            return pick("tb-07")
        if project_info.get("compliance_required"):
            return pick("tb-06")
        if project_info.get("has_press"):
            return pick("tb-04")
        if project_info.get("has_case_studies"):
            return pick("tb-05")
        if (project_info.get("has_metrics") or project_info.get("has_proof_stats")) and logo_count < 8:
            return pick("tb-03")
        if logo_count >= 8:
            return pick("tb-01")
        return pick("tb-02")

    # ── ABOUT ────────────────────────────────────────────
    elif sec_id == "about":
        if project_info.get("has_video"):
            return pick("abt-06")
        if project_info.get("founder_led"):
            return pick("abt-01")
        years = project_info.get("years_operating", 0)
        if years >= 5:
            return pick("abt-03")
        if project_info.get("has_office_photos"):
            return pick("abt-04")
        if "editorial" in s or "minimalist" in s:
            return pick("abt-05")
        return pick("abt-02")

    # ── SERVICES ─────────────────────────────────────────
    elif sec_id == "services":
        if project_info.get("kinetic_dark") or project_info.get("hover_service_list") or "kinetic" in s:
            return pick("srv-09")
        if project_info.get("target_audience") == "developers/ctos":
            return pick("srv-08")
        if project_info.get("enterprise"):
            return pick("srv-07")
        if project_info.get("is_productized"):
            return pick("srv-06")
        if project_info.get("mobile_heavy"):
            return pick("srv-05")
        if project_info.get("wants_tabs"):
            return pick("srv-04")
        if "creative" in s or "editorial" in s:
            return pick("srv-02")
        if project_info.get("has_flagship_service"):
            return pick("srv-03")
        return pick("srv-01")

    # ── WHY CHOOSE US ────────────────────────────────────
    elif sec_id == "why_choose_us":
        if project_info.get("has_founder_video"):
            return pick("wcu-05")
        if project_info.get("has_certifications"):
            return pick("wcu-06")
        if project_info.get("enterprise"):
            return pick("wcu-04")
        if project_info.get("high_competition"):
            return pick("wcu-02")
        if project_info.get("has_proof_stats"):
            return pick("wcu-03")
        return pick("wcu-01")

    # ── HOW WE WORK ──────────────────────────────────────
    elif sec_id == "how_we_work":
        step_count = project_info.get("step_count", 4)
        if project_info.get("is_cyclical"):
            return pick("hww-09")
        if project_info.get("has_rich_media"):
            return pick("hww-10")
        if project_info.get("has_cinematic_photos"):
            return pick("hww-11")
        if "creative" in s and project_info.get("immersive"):
            return pick("hww-07")
        if project_info.get("is_non_linear"):
            return pick("hww-05")
        if project_info.get("has_step_images"):
            return pick("hww-06")
        if step_count > 6:
            return pick("hww-08")
        if step_count >= 5:
            return pick("hww-02")
        if "bento" in s or "contemporary" in s:
            return pick("hww-12")
        if step_count <= 4 and project_info.get("complexity") == "low":
            return pick("hww-01")
        if step_count == 4 and ("corporate" in s or "clean" in s):
            return pick("hww-03")
        return pick("hww-04")

    # ── PORTFOLIO ────────────────────────────────────────
    elif sec_id == "portfolio":
        case_count = project_info.get("case_count", 6)
        if project_info.get("kinetic_dark") or project_info.get("mixitup_filter") or "kinetic" in s:
            return pick("port-09")
        if "avant-garde" in s or "editorial" in s:
            return pick("port-08")
        if case_count >= 10:
            return pick("port-04")
        if project_info.get("has_metrics"):
            return pick("port-02")
        if project_info.get("enterprise"):
            return pick("port-03")
        if project_info.get("focus") == "responsive_web":
            return pick("port-06")
        if project_info.get("analytical"):
            return pick("port-07")
        if case_count <= 5:
            return pick("port-05")
        return pick("port-01")

    # ── TESTIMONIALS ─────────────────────────────────────
    elif sec_id == "testimonials":
        reviews = project_info.get("review_count", 5)
        if project_info.get("kinetic_dark") or "kinetic" in s:
            return pick("tst-09")
        if project_info.get("has_video_reviews"):
            return pick("tst-03")
        if project_info.get("has_audio"):
            return pick("tst-06")
        if project_info.get("has_analytics_data"):
            return pick("tst-05")
        if project_info.get("social_proof_type") == "social_posts":
            return pick("tst-04")
        if project_info.get("has_vip_quote"):
            return pick("tst-02")
        if project_info.get("wants_compact"):
            return pick("tst-08")
        if reviews > 20:
            return pick("tst-07")
        if reviews > 10:
            return pick("tst-01")
        return pick("tst-01")

    # ── RESULTS / METRICS ────────────────────────────────
    elif sec_id == "results_metrics":
        if project_info.get("kinetic_dark") or project_info.get("oversized_counters") or "kinetic" in s:
            return pick("res-07")
        if project_info.get("has_live_data"):
            return pick("res-05")
        if project_info.get("has_before_after"):
            return pick("res-02")
        if project_info.get("has_analytics_data"):
            return pick("res-03")
        years = project_info.get("years_operating", 0)
        if years >= 5:
            return pick("res-04")
        if project_info.get("enterprise") and project_info.get("has_named_quotes"):
            return pick("res-06")
        return pick("res-01")

    # ── PRICING ──────────────────────────────────────────
    elif sec_id == "pricing":
        if project_info.get("is_productized"):
            return pick("prc-04")
        if project_info.get("custom_quotes"):
            return pick("prc-06")
        if project_info.get("has_annual_discount") or project_info.get("has_billing_toggle"):
            return pick("prc-02")
        if project_info.get("pricing_model") in ("usage_based", "usage/scope_based"):
            return pick("prc-03")
        if project_info.get("enterprise") and project_info.get("feature_density") == "high":
            return pick("prc-05")
        return pick("prc-01")

    # ── TEAM ─────────────────────────────────────────────
    elif sec_id == "team":
        team_size = project_info.get("team_size", 6)
        if team_size >= 30:
            return pick("team-06")
        if team_size >= 15 and project_info.get("has_departments"):
            return pick("team-04")
        if project_info.get("has_editorial_photos"):
            return pick("team-05")
        if project_info.get("culture_focus"):
            return pick("team-03")
        if project_info.get("founder_led"):
            return pick("team-02")
        return pick("team-01")

    # ── FAQ ──────────────────────────────────────────────
    elif sec_id == "faq":
        faq_count = project_info.get("faq_count", 6)
        if faq_count >= 15:
            return pick("faq-04")
        if faq_count >= 10 and project_info.get("has_categories"):
            return pick("faq-02")
        if project_info.get("goal") == "consultation":
            return pick("faq-05")
        if project_info.get("wants_compact"):
            return pick("faq-06")
        if faq_count <= 6 and project_info.get("answers_short"):
            return pick("faq-03")
        return pick("faq-01")

    # ── FINAL CTA ────────────────────────────────────────
    elif sec_id == "final_cta":
        if project_info.get("direct_calendar"):
            return pick("cta-02")
        if project_info.get("lead_magnet"):
            return pick("cta-03")
        if project_info.get("needs_qualification"):
            return pick("cta-04")
        if project_info.get("founder_led") and project_info.get("brand_tier") == "boutique":
            return pick("cta-05")
        if project_info.get("has_enterprise_tier"):
            return pick("cta-06")
        return pick("cta-01")

    # ── FOOTER ───────────────────────────────────────────
    elif sec_id == "footer":
        if project_info.get("kinetic_dark") or project_info.get("consultation_prefooter") or "kinetic" in s:
            return pick("ftr-07")
        if project_info.get("has_mobile_app"):
            return pick("ftr-06")
        if project_info.get("has_multiple_offices"):
            return pick("ftr-05")
        if project_info.get("has_newsletter"):
            return pick("ftr-03")
        if "editorial" in s or "luxury" in s:
            return pick("ftr-02")
        if project_info.get("single_page"):
            return pick("ftr-04")
        return pick("ftr-01")

    # ── PRICING HERO ─────────────────────────────────────
    elif sec_id == "pricing_hero":
        if project_info.get("pricing_model") in ("usage_based", "usage/scope_based"):
            return pick("phero-03")
        if project_info.get("has_roi") or project_info.get("enterprise"):
            return pick("phero-02")
        if project_info.get("has_billing_toggle"):
            return pick("phero-01")
        return pick("phero-01")

    # ── PRICING COMPARISON MATRIX ────────────────────────
    elif sec_id == "pricing_comparison_matrix":
        if project_info.get("matrix_tabs"):
            return pick("pmat-02")
        if project_info.get("minimal_diff"):
            return pick("pmat-03")
        if project_info.get("has_matrix"):
            return pick("pmat-01")
        return pick("pmat-01")

    # ── PRICING ADDONS ───────────────────────────────────
    elif sec_id == "pricing_addons":
        if project_info.get("addon_compact"):
            return pick("padd-02")
        if project_info.get("has_addons"):
            return pick("padd-01")
        return pick("padd-01")

    # ── PRICING ENTERPRISE SLA ───────────────────────────
    elif sec_id == "pricing_enterprise_sla":
        if project_info.get("direct_rfq_form"):
            return pick("psla-02")
        return pick("psla-01")

    # ── PRICING GUARANTEE BAR ────────────────────────────
    elif sec_id == "pricing_guarantee_bar":
        if project_info.get("mobile_drawer"):
            return pick("pbar-02")
        if project_info.get("has_guarantee"):
            return pick("pbar-01")
        return pick("pbar-01")

    # ── ABOUT TIMELINE ───────────────────────────────────
    elif sec_id == "about_timeline":
        if project_info.get("timeline_horizontal"):
            return pick("time-02")
        if "minimalist" in s or "editorial" in s:
            return pick("time-03")
        return pick("time-01")

    # ── ABOUT VALUES ─────────────────────────────────────
    elif sec_id == "about_values":
        if project_info.get("has_manifesto") or project_info.get("founder_led"):
            return pick("val-02")
        if "bento" in s or "contemporary" in s:
            return pick("val-03")
        return pick("val-01")

    # ── ABOUT CULTURE GALLERY ────────────────────────────
    elif sec_id == "about_culture_gallery":
        if project_info.get("distributed_team"):
            return pick("cult-02")
        if project_info.get("culture_focus"):
            return pick("cult-03")
        return pick("cult-01")

    # ── ABOUT LEADERSHIP BOARD ───────────────────────────
    elif sec_id == "about_leadership_board":
        if project_info.get("has_investors"):
            return pick("lead-02")
        return pick("lead-01")

    # ── SERVICE ARCHITECTURE ─────────────────────────────
    elif sec_id == "service_architecture":
        if project_info.get("arch_layered"):
            return pick("arch-02")
        if project_info.get("workflow_phases") or project_info.get("service_model") == "consulting":
            return pick("arch-03")
        return pick("arch-01")

    # ── SERVICE DELIVERABLES MATRIX ──────────────────────
    elif sec_id == "service_deliverables_matrix":
        if project_info.get("has_sla"):
            return pick("deliv-02")
        if project_info.get("interactive_scope"):
            return pick("deliv-03")
        return pick("deliv-01")

    # ── SERVICE TECH STACK ───────────────────────────────
    elif sec_id == "service_tech_stack":
        if project_info.get("has_partners"):
            return pick("stack-02")
        if project_info.get("searchable_integrations"):
            return pick("stack-03")
        return pick("stack-01")

    # ── SERVICE USE CASES ────────────────────────────────
    elif sec_id == "service_use_cases":
        if project_info.get("multi_persona"):
            return pick("use-02")
        return pick("use-01")

    # ── CONTACT INTAKE FORM ──────────────────────────────
    elif sec_id == "contact_intake_form":
        if project_info.get("direct_calendar"):
            return pick("cform-03")
        if project_info.get("multi_step"):
            return pick("cform-02")
        return pick("cform-01")

    # ── CONTACT LOCATION MAP ─────────────────────────────
    elif sec_id == "contact_location_map":
        if project_info.get("geo_map") or project_info.get("kinetic_dark") or "kinetic" in s:
            return pick("cmap-03")
        if project_info.get("map_view"):
            return pick("cmap-02")
        return pick("cmap-01")

    # ── CONTACT SLA BANNER ───────────────────────────────
    elif sec_id == "contact_sla_banner":
        if project_info.get("has_support_route"):
            return pick("csla-02")
        return pick("csla-01")

    # ── CASE STUDY HERO HIGHLIGHT ────────────────────────
    elif sec_id == "case_study_hero_highlight":
        if project_info.get("has_video") or project_info.get("immersive"):
            return pick("csh-02")
        if "minimalist" in s or "editorial" in s:
            return pick("csh-03")
        return pick("csh-01")

    # ── CASE STUDY FILTER HUB ────────────────────────────
    elif sec_id == "case_study_filter_hub":
        if project_info.get("data_dense") or project_info.get("ledger_view"):
            return pick("csf-03")
        if "creative" in s or "editorial" in s:
            return pick("csf-02")
        return pick("csf-01")

    # ── CASE STUDY CLIENT QUOTE STRIP ────────────────────
    elif sec_id == "case_study_client_quote_strip":
        if project_info.get("has_vip_quote"):
            return pick("csq-02")
        return pick("csq-01")

    # ── BLOG FEATURED EDITORIAL ──────────────────────────
    elif sec_id == "blog_featured_editorial":
        if project_info.get("has_trending") or project_info.get("post_density") == "high":
            return pick("bfeat-02")
        if "minimalist" in s or "longform" in s:
            return pick("bfeat-03")
        return pick("bfeat-01")

    # ── BLOG TOPIC FILTER FEED ───────────────────────────
    elif sec_id == "blog_topic_filter_feed":
        if project_info.get("feed_horizontal"):
            return pick("bfeed-02")
        if project_info.get("feed_archive"):
            return pick("bfeed-03")
        return pick("bfeed-01")

    # ── BLOG NEWSLETTER CAPTURE ──────────────────────────
    elif sec_id == "blog_newsletter_capture":
        if project_info.get("split_digest"):
            return pick("bnews-02")
        return pick("bnews-01")

    # ── CAREERS PERKS ────────────────────────────────────
    elif sec_id == "careers_perks":
        if project_info.get("remote_stipend"):
            return pick("perk-03")
        if project_info.get("salary_transparent"):
            return pick("perk-02")
        if project_info.get("parental_wellness"):
            return pick("perk-04")
        return pick("perk-01")

    # ── CAREERS JOBS ─────────────────────────────────────
    elif sec_id == "careers_jobs":
        if project_info.get("accordion_jobs"):
            return pick("jobs-02")
        if project_info.get("interview_pipeline"):
            return pick("jobs-03")
        return pick("jobs-01")

    # ── LEGAL DOC ────────────────────────────────────────
    elif sec_id == "legal_doc":
        if project_info.get("multi_policy"):
            return pick("leg-02")
        if project_info.get("has_version_selector"):
            return pick("leg-03")
        if project_info.get("has_toc"):
            return pick("leg-01")
        return pick("leg-01")

    # ── PRODUCT CATALOG GRID ─────────────────────────────
    elif sec_id == "product_catalog_grid":
        if project_info.get("has_categories") or project_info.get("filterable_products"):
            return pick("pcg-02")
        return pick("pcg-01")

    # ── PRODUCT FEATURE MATRIX ───────────────────────────
    elif sec_id == "product_feature_matrix":
        if project_info.get("has_portal"):
            return pick("pfm-02")
        return pick("pfm-01")

    # ── CASE STUDY DOSSIER ───────────────────────────────
    elif sec_id == "case_study_dossier":
        if project_info.get("has_proof_stats"):
            return pick("csd-02")
        return pick("csd-01")

    # ── GLOBAL FALLBACK (unknown section) ────────────────
    else:
        fallback_id = SECTION_FALLBACKS.get(sec_id, archetypes[0]["archetype_id"])
        target_log.append(
            f"[FALLBACK] Unknown section_id={sec_id!r}; using default {fallback_id!r}"
        )
        return pick(fallback_id)


# =====================================================
# PROMPT GENERATOR
# =====================================================

def generate_master_prompt(project_info: dict) -> str:
    local_warnings = []
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
                local_warnings.append(f"[WARN] Page '{page_id}' requested section '{sid}' which is not in dataset yet")
        page_display_name = page_meta.get("name", page_id.title())
    else:
        sections = all_sections
        page_display_name = f"Full System ({len(sections)} Sections)"

    proj_name = project_info.get("project_name", "Modern Web Platform")
    raw_style = project_info.get("style", "Industrial Minimalist")
    target = project_info.get("target_audience", "B2B Decision Makers")

    # Normalize intent for color/typography lookups
    normalized = normalize_intent(raw_style)
    color_query = project_info.get("industry", "b2b") + " " + normalized
    typo_query = normalized + " tech"

    color_res = search(color_query, "color", 1)
    color_row = color_res.get("results", [{}])[0] if color_res.get("results") else {}
    tokens = derive_surface_tokens(color_row)

    typo_res = search(typo_query, "typography", 1)
    typo_row = typo_res.get("results", [{}])[0] if typo_res.get("results") else {}
    heading_font = typo_row.get("Heading Font", "Space Grotesk")
    body_font = typo_row.get("Body Font", "Inter")

    style_res = search(normalized, "style", 1)
    style_row = style_res.get("results", [{}])[0] if style_res.get("results") else {}
    prompt_res = search(style_row.get("Style Category", normalized), "prompt", 1)
    prompt_row = prompt_res.get("results", [{}])[0] if prompt_res.get("results") else {}
    high_contrast_serifs = {
        "bodoni moda", "libre bodoni", "playfair display", "cormorant garamond", "instrument serif"
    }
    if heading_font.lower() in high_contrast_serifs:
        heading_spec = (
            f"`{heading_font}` — 600–700 weight max, tracking >= -0.015em "
            "(avoid 800/900 or 300 hairlines so hyphens, '+' signs, and serifs stay crisp; "
            "use body/mono `tabular-nums` for compact KPI numerals)"
        )
    else:
        heading_spec = f"`{heading_font}` — Bold (600–700), tracking-tight"

    p = []
    p.append("# Master Production-Grade UI/UX Blueprint")
    p.append(f"**Project:** {proj_name}")
    p.append(f"**Page:** {page_display_name} (`{page_id}`)")
    p.append(f"**Style Archetype:** {raw_style}")
    p.append(f"**Target Audience:** {target}")
    p.append(f"**Sections covered:** {len(sections)} sections")
    p.append("**Compliance:** WCAG 2.2 AA | Anti-Slop Gates Enabled\n")

    p.append("---")
    p.append("## 1. Global Design Token Foundation")
    p.append(f"- **Surface Background:** `{tokens['background']}`")
    p.append(f"- **Card Surface / Raised:** `{tokens['card_surface']}`")
    p.append(f"- **Primary Action:** `{tokens['cta']}` (text `{tokens['cta_text']}`) — dual-ring focus")
    p.append(f"- **Text Primary:** `{tokens['text_primary']}`")
    p.append(f"- **Text Secondary:** `{tokens['text_secondary']}`")
    p.append(f"- **Border Subtle:** `{tokens['border_subtle']}` (1px solid — borders/dividers only, never body/numeral text)")
    p.append(f"- **Heading Font:** {heading_spec}")
    p.append(f"- **Body Font:** `{body_font}` — 400/500, leading-relaxed")
    p.append("- **Mono / Chips:** `JetBrains Mono` or `ui-monospace`")
    p.append("- **Motion:** 150–200ms `cubic-bezier(0.16,1,0.3,1)`, compositor-only (`transform`, `opacity`)")
    if style_row.get("Effects & Animation"):
        p.append(f"- **Style Effects & Choreography:** {style_row['Effects & Animation']}")
    if prompt_row.get("CSS/Technical Keywords"):
        p.append(f"- **CSS/Motion Primitives:** `{prompt_row['CSS/Technical Keywords']}`")
    if project_info.get("kinetic_dark") or "kinetic" in raw_style.lower():
        p.append("- **Kinetic Scroll & Transition Spec:** Continuous smooth scroll (`ScrollSmoother` `1.35`, no section snap), differential `data-speed` layers (`0.2`, `0.3`, `0.5`, `0.9` with `will-change: transform` on `>=1025px`), velocity `skewY` (`-15..15deg`), scrub zooms (`1->1.15`, `2.5->1`), `ScrollTrigger` entrances (`.title-anim`/`.text-anim p` `rotationX: -80deg` at `top 90%`, `.fade_bottom` `y:30->0` stagger `0.2s`, `.animation_home1_service` `x:-50->0`, `.bounce` counters `y:-100` & CTAs `y:-70`, `.blog__item` `x:50->0`), pinned columns (`.portfolio__title-wrap-6`, `.job__detail-sidebar`), sticky header past `20px`, `170px` CTA (`0.7s` radial fill + `0.5s` `80px` magnetic pull), `.menu-text` char wave (`0.05s/char` `16px` `text-shadow`), `15deg` diagonal `.service__img` swap + `-26deg` ribbon wipe (`0.3s`), desktop (`>1200px`) `.cursor1`/`.cursor2` (`mix-blend-mode: difference`), and `prefers-reduced-motion` + `:focus-visible` parity.")
    p.append("- **Anti-Slop:** Zero gradient blobs · Zero emoji icons · Zero rainbow borders\n")

    p.append("---")
    p.append("## 2. Section-by-Section Blueprint\n")

    for i, sec in enumerate(sections, 1):
        chosen = select_archetype(sec, project_info, warnings=local_warnings)
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
    p.append("5. `disabled` — `aria-disabled='true' opacity-50 cursor-not-allowed`")
    p.append("6. `loading` — Animated SVG spinner + `aria-busy='true'` + label preserved")
    p.append("7. `error` — `aria-invalid='true'` + `aria-describedby` pointing to inline error\n")

    p.append("---")
    p.append("## 4. Production Engineering & Audit Guardrails")
    p.append("1. **CSS Tokens & SVGs (`TOKEN-001`):** Define `:root` custom properties in `tokens.css` (or `:root` block only) and reference `var(--...)` / `currentColor` everywhere else—never hardcode raw hexes in hover rules, modal themes, or inline SVG `stroke`/`fill` attributes.")
    p.append("2. **Target Size & Sticky-Header Focus (`A11Y-001`, `2.4.11`):** Every interactive link/button (including footer, social, and inline links) MUST maintain `>= 24x24px` hit box (`>= 44x44px` on touch). Add `scroll-margin-top` to anchored sections and transfer focus to the destination section/heading after closing modal/drawer navigation.")
    p.append("3. **Accordion & Backdrop Discipline (`PERF-001`):** Collapsed `0fr` accordion panels must set `inert` or `visibility: hidden` alongside `aria-hidden='true'`. Never apply `backdrop-filter: blur(...)` to an animated `opacity` `<dialog>::backdrop`.")
    p.append("4. **Embedded Widgets & Real Data (`SLOP-003`):** Never freeze `<iframe>` scheduler heights on mobile (auto-resize height or render inline) and never simulate fake `'Confirmation sent'` emails or hardcoded `.ics` timestamps. Keep displayed numbers mathematically consistent, replace generic placeholder social URLs, and reserve `fetchpriority='high'` strictly for above-the-fold LCP media.\n")

    # Sync module-level list for backwards compatibility without leaking across calls
    fallback_warnings.clear()
    fallback_warnings.extend(local_warnings)

    if local_warnings:
        p.append("---")
        p.append("## 5. Generator Warnings")
        for w in local_warnings:
            p.append(f"- {w}")

    return "\n".join(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Production UI/UX Master Prompt")
    parser.add_argument(
        "--page",
        default="home",
        choices=[
            "home", "pricing", "about", "services", "case_studies", "contact",
            "blog", "careers", "legal",
            "product_showcase", "product_detail", "service_detail", "case_study_detail",
        ],
        help="Page type",
    )
    parser.add_argument("--name", default="Apex Growth Agency", help="Project name")
    parser.add_argument("--style", default="Industrial Minimalist", help="Style archetype")
    parser.add_argument("--industry", default="b2b", help="Industry for color lookup")
    parser.add_argument("--kinetic-dark", action="store_true", help="Enable Dark Kinetic Emerald agency archetypes")
    parser.add_argument("--steps", type=int, default=4, help="Process step count")
    parser.add_argument("--reviews", type=int, default=12, help="Review count")
    parser.add_argument("--team-size", type=int, default=6, help="Team size")
    parser.add_argument("--faq-count", type=int, default=6, help="FAQ count")
    parser.add_argument("--calendar", action="store_true", help="Use calendar booking CTA")
    parser.add_argument("--productized", action="store_true", help="Flat-rate productized pricing")
    parser.add_argument("--founder-led", action="store_true", help="Founder-led agency")
    parser.add_argument("--has-stats", action="store_true", help="Agency has proof stats")
    parser.add_argument("--enterprise", action="store_true", help="Enterprise tier targeting")
    parser.add_argument("--lead-header", action="store_true", help="Use action-split lead header")
    parser.add_argument("--bento-hero", action="store_true", help="Use Bento hero showcase")
    parser.add_argument("--app-mockups", action="store_true", help="Use multi-device mockup hero")
    parser.add_argument("--cro-split", action="store_true", help="Use problem-vs-solution CRO hero")
    parser.add_argument("--has-video", action="store_true", help="Enable video showcase hero/about")
    parser.add_argument("--has-audio", action="store_true", help="Enable audio voice-note testimonials")
    # Pricing Page flags
    parser.add_argument("--billing-toggle", action="store_true", help="Include billing cycle toggle")
    parser.add_argument("--has-matrix", action="store_true", help="Include deep feature comparison matrix")
    parser.add_argument("--matrix-tabs", action="store_true", help="Use tabbed feature matrix")
    parser.add_argument("--minimal-diff", action="store_true", help="Use delta/diff-only matrix")
    parser.add_argument("--has-addons", action="store_true", help="Include modular add-on upgrades")
    parser.add_argument("--addon-compact", action="store_true", help="Compact horizontal addon strip")
    parser.add_argument("--has-sla", action="store_true", help="Include enterprise procurement / SLA card and compliance badges")
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
    # Contact Page flags
    parser.add_argument("--multi-step", action="store_true", help="Multi-step progressive disclosure wizard")
    parser.add_argument("--map-view", action="store_true", help="Stylized vector map view")
    parser.add_argument("--has-support-route", action="store_true", help="Dual-track sales vs support routing banner")
    # Case Studies Page flags
    parser.add_argument("--data-dense", action="store_true", help="Data-dense ledger portfolio view")
    parser.add_argument("--has-vip-quote", action="store_true", help="Marquee Fortune 500 client quote banner")
    # Blog Page flags
    parser.add_argument("--has-trending", action="store_true", help="Asymmetric 1+2 trending stories hero")
    parser.add_argument("--feed-horizontal", action="store_true", help="Magazine-style horizontal article rows")
    parser.add_argument("--feed-archive", action="store_true", help="High-density date ledger archive")
    parser.add_argument("--split-digest", action="store_true", help="Split curated newsletter box with RSS link")
    # Careers Page flags
    parser.add_argument("--remote-stipend", action="store_true", help="Remote-first stipend matrix")
    parser.add_argument("--salary-transparent", action="store_true", help="Compensation philosophy manifesto")
    parser.add_argument("--parental-wellness", action="store_true", help="Parental and wellness commitment banner")
    parser.add_argument("--accordion-jobs", action="store_true", help="Single requisition expandable accordion")
    parser.add_argument("--interview-pipeline", action="store_true", help="Interview pipeline stepper")
    # Legal Page flags
    parser.add_argument("--has-toc", action="store_true", help="Sticky table of contents and prose split")
    parser.add_argument("--has-version-selector", action="store_true", help="Versioned compliance header with PDF download")
    parser.add_argument("--multi-policy", action="store_true", help="Tabbed multi-policy legal hub")
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
        "lead_header": args.lead_header,
        "bento_hero": args.bento_hero,
        "has_app_mockups": args.app_mockups,
        "cro_split": args.cro_split,
        "has_video": args.has_video,
        "has_audio": args.has_audio,
        # Pricing Page variables
        "has_billing_toggle": args.billing_toggle,
        "has_matrix": args.has_matrix,
        "matrix_tabs": args.matrix_tabs,
        "minimal_diff": args.minimal_diff,
        "has_addons": args.has_addons,
        "addon_compact": args.addon_compact,
        "has_sla": args.has_sla,
        "compliance_required": args.has_sla,
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
        # Contact Page variables
        "multi_step": args.multi_step,
        "map_view": args.map_view,
        "has_support_route": args.has_support_route,
        # Case Studies Page variables
        "data_dense": args.data_dense,
        "has_vip_quote": args.has_vip_quote,
        # Blog Page variables
        "has_trending": args.has_trending,
        "feed_horizontal": args.feed_horizontal,
        "feed_archive": args.feed_archive,
        "split_digest": args.split_digest,
        # Careers Page variables
        "remote_stipend": args.remote_stipend,
        "salary_transparent": args.salary_transparent,
        "parental_wellness": args.parental_wellness,
        "accordion_jobs": args.accordion_jobs,
        "interview_pipeline": args.interview_pipeline,
        # Legal Page variables
        "has_toc": args.has_toc,
        "has_version_selector": args.has_version_selector,
        "multi_policy": args.multi_policy,
        "kinetic_dark": args.kinetic_dark,
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
        print("\n... [preview truncated] | Full: use --out flag")
        if fallback_warnings:
            for w in fallback_warnings:
                print(f"  {w}")
