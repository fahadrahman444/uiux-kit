#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 5 Golden-Set Evaluation Harness
Scores 30 diverse reference client briefs (10 Enterprise B2B, 10 Creative Agencies,
10 Consumer & Growth SaaS across all 9 page types) on a 5-axis 100-point rubric:
  1. Section Relevance & Flow   (25 pts)
  2. Token Integrity            (20 pts)
  3. WCAG 2.2 Compliance        (25 pts)
  4. Anti-Slop Compliance       (20 pts)
  5. Engineering Readiness      (10 pts)
"""

import json
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPTS_DIR.parent / "data"
sys.path.insert(0, str(SCRIPTS_DIR))

import generate_section_prompt as g  # noqa: E402

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

GOLDEN_BRIEFS = [
    # 10 B2B Enterprise & Infrastructure
    {"group": "Enterprise", "page_id": "home", "project_name": "CloudCore Telemetry", "style": "Industrial Minimalist", "industry": "b2b", "enterprise": True, "has_proof_stats": True},
    {"group": "Enterprise", "page_id": "pricing", "project_name": "VaultSec Enterprise", "style": "Swiss Modern", "industry": "fintech", "enterprise": True, "has_matrix": True, "has_sla": True, "has_billing_toggle": True},
    {"group": "Enterprise", "page_id": "services", "project_name": "GridMesh Infrastructure", "style": "Neo-Swiss", "industry": "cloud", "enterprise": True, "arch_layered": True, "workflow_phases": True},
    {"group": "Enterprise", "page_id": "about", "project_name": "LedgerTrust Systems", "style": "Corporate Minimal", "industry": "banking", "enterprise": True, "has_investors": True},
    {"group": "Enterprise", "page_id": "case_studies", "project_name": "DataForge Analytics", "style": "Technical Clean", "industry": "analytics", "enterprise": True, "data_dense": True, "has_vip_quote": True},
    {"group": "Enterprise", "page_id": "contact", "project_name": "Aegis Compliance", "style": "Trustworthy Corporate", "industry": "security", "enterprise": True, "multi_step": True, "has_support_route": True},
    {"group": "Enterprise", "page_id": "legal", "project_name": "Kinetix FinOps", "style": "Minimal Clean", "industry": "finance", "enterprise": True, "has_toc": True, "has_version_selector": True},
    {"group": "Enterprise", "page_id": "careers", "project_name": "ObservaStack", "style": "Technical Swiss", "industry": "devtools", "enterprise": True, "salary_transparent": True, "interview_pipeline": True},
    {"group": "Enterprise", "page_id": "blog", "project_name": "KernelScale Docs", "style": "Editorial Technical", "industry": "software", "enterprise": True, "feed_archive": True, "split_digest": True},
    {"group": "Enterprise", "page_id": "home", "project_name": "FreightPulse Global", "style": "Trustworthy Industrial", "industry": "logistics", "enterprise": True, "lead_header": True},
    # 10 Creative Studios & Agencies
    {"group": "Agency", "page_id": "home", "project_name": "Monolith Studio", "style": "Editorial Minimalist", "industry": "agency", "founder_led": True, "has_proof_stats": True},
    {"group": "Agency", "page_id": "about", "project_name": "Atelier Nord", "style": "Editorial Luxury", "industry": "design", "has_manifesto": True, "has_office_photos": True},
    {"group": "Agency", "page_id": "services", "project_name": "Signal & Craft", "style": "Editorial Modern", "industry": "marketing", "multi_persona": True, "interactive_scope": True},
    {"group": "Agency", "page_id": "case_studies", "project_name": "Vesper Interactive", "style": "Premium Editorial", "industry": "creative", "has_vip_quote": True},
    {"group": "Agency", "page_id": "pricing", "project_name": "SprintDesign Co", "style": "Clean Editorial", "industry": "consulting", "is_productized": True, "has_guarantee": True},
    {"group": "Agency", "page_id": "contact", "project_name": "Foundry Partners", "style": "Boutique Minimal", "industry": "agency", "direct_calendar": True, "map_view": True},
    {"group": "Agency", "page_id": "blog", "project_name": "Type & Grid Journal", "style": "Editorial Magazine", "industry": "media", "has_trending": True, "feed_horizontal": True},
    {"group": "Agency", "page_id": "careers", "project_name": "Formwork Collective", "style": "Editorial Clean", "industry": "design", "remote_stipend": True, "accordion_jobs": True},
    {"group": "Agency", "page_id": "home", "project_name": "Koma Architecture", "style": "Swiss Minimal", "industry": "architecture", "bento_hero": True},
    {"group": "Agency", "page_id": "legal", "project_name": "Meridian Advisory", "style": "Editorial Minimal", "industry": "legal", "multi_policy": True},
    # 10 Consumer & Growth SaaS
    {"group": "GrowthSaaS", "page_id": "home", "project_name": "FlowNote AI", "style": "Modern Clean", "industry": "productivity", "has_app_mockups": True, "cro_split": True},
    {"group": "GrowthSaaS", "page_id": "pricing", "project_name": "PulseCRM", "style": "Friendly Modern", "industry": "saas", "usage_based": True, "has_roi": True, "mobile_drawer": True},
    {"group": "GrowthSaaS", "page_id": "about", "project_name": "CalmClinic Health", "style": "Accessible Clean", "industry": "healthcare", "distributed_team": True, "culture_focus": True},
    {"group": "GrowthSaaS", "page_id": "services", "project_name": "SyncHub Automation", "style": "Fresh Modern", "industry": "saas", "searchable_integrations": True, "has_partners": True},
    {"group": "GrowthSaaS", "page_id": "case_studies", "project_name": "CartLift Commerce", "style": "Impressive Modern", "industry": "ecommerce", "has_proof_stats": True},
    {"group": "GrowthSaaS", "page_id": "contact", "project_name": "PayStream Go", "style": "Simple Clean", "industry": "fintech", "direct_calendar": True},
    {"group": "GrowthSaaS", "page_id": "blog", "project_name": "GrowthLoop Weekly", "style": "Fresh Minimal", "industry": "saas", "split_digest": True},
    {"group": "GrowthSaaS", "page_id": "careers", "project_name": "BrightPath EdTech", "style": "Friendly Clean", "industry": "education", "parental_wellness": True},
    {"group": "GrowthSaaS", "page_id": "home", "project_name": "ClipCraft Studio", "style": "Exciting Bold", "industry": "video", "has_video": True, "has_audio": True},
    {"group": "GrowthSaaS", "page_id": "legal", "project_name": "SafeNest Privacy", "style": "Trustworthy Clean", "industry": "consumer", "has_toc": True},
]


def score_brief(brief: dict, page_flows: dict[str, list[str]]) -> dict:
    prompt = g.generate_master_prompt(brief)
    page_id = brief["page_id"]
    expected_sections = page_flows.get(page_id, [])

    # 1. Section Relevance & Flow (25 pts)
    section_headers = re.findall(r"^### \d+\.\s+(.+)$", prompt, re.M)
    has_dupes = len(section_headers) != len(set(section_headers))
    has_warnings = bool(g.fallback_warnings) or "[WARN]" in prompt or "[ERROR]" in prompt
    flow_ok = len(section_headers) == len(expected_sections) and len(section_headers) > 0
    s1 = 25 if (flow_ok and not has_dupes and not has_warnings) else (15 if flow_ok else 0)

    # 2. Token Integrity (20 pts)
    m_bg = re.search(r"Surface Background:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
    m_card = re.search(r"Card Surface / Raised:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
    m_cta = re.search(r"Primary Action:\*\* `(#[0-9A-Fa-f]{6})` \(text `(#[0-9A-Fa-f]{6})`", prompt)
    m_t1 = re.search(r"Text Primary:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
    m_t2 = re.search(r"Text Secondary:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
    has_motion = "cubic-bezier" in prompt and "transform" in prompt
    has_fonts = "**Heading Font:**" in prompt and "**Body Font:**" in prompt
    tokens_valid = all(
        m and HEX_RE.match(m.group(1)) for m in (m_bg, m_card, m_t1, m_t2)
    ) and bool(m_cta and HEX_RE.match(m_cta.group(1)) and HEX_RE.match(m_cta.group(2)))
    s2 = 20 if (tokens_valid and has_motion and has_fonts) else 10

    # 3. WCAG 2.2 Compliance (25 pts)
    wcag_ok = False
    if tokens_valid:
        bg, card, t1, t2 = m_bg.group(1), m_card.group(1), m_t1.group(1), m_t2.group(1)
        cta_bg, cta_fg = m_cta.group(1), m_cta.group(2)
        ratios = [
            g._contrast_ratio(t1, bg),
            g._contrast_ratio(t1, card),
            g._contrast_ratio(t2, bg),
            g._contrast_ratio(t2, card),
            g._contrast_ratio(cta_fg, cta_bg),
        ]
        wcag_ok = all(r >= 4.5 for r in ratios) and ("A11Y-001" in prompt or "24x24px" in prompt)
    s3 = 25 if wcag_ok else 5

    # 4. Anti-Slop Compliance (20 pts)
    anti_slop_ok = (
        "Zero gradient blobs" in prompt
        and "Zero emoji icons" in prompt
        and "Neumorphism" not in prompt
        and "PERF-001" in prompt
        and "SLOP-003" in prompt
    )
    s4 = 20 if anti_slop_ok else 10

    # 5. Engineering Readiness (10 pts)
    eng_ok = (
        "Universal Interactive State Matrix" in prompt
        and "Production Engineering & Audit Guardrails" in prompt
        and "TOKEN-001" in prompt
        and "focus-visible" in prompt
    )
    s5 = 10 if eng_ok else 4

    total = s1 + s2 + s3 + s4 + s5
    return {
        "project": brief["project_name"],
        "group": brief["group"],
        "page": page_id,
        "total": total,
        "breakdown": {"flow": s1, "tokens": s2, "wcag": s3, "anti_slop": s4, "engineering": s5},
    }


def run_evaluation() -> tuple[float, list[dict]]:
    with open(DATA_DIR / "page-templates.json", "r", encoding="utf-8") as f:
        tpl = json.load(f)
    page_flows = {p["page_id"]: p["default_section_flow"] for p in tpl["pages"]}

    results = [score_brief(b, page_flows) for b in GOLDEN_BRIEFS]
    avg = sum(r["total"] for r in results) / len(results)
    return avg, results


def main():
    avg, results = run_evaluation()
    print("UI/UX Pro Max — Phase 5 Golden-Set Prompt Evaluation (30 Briefs)")
    print("=" * 72)
    for grp in ("Enterprise", "Agency", "GrowthSaaS"):
        grp_rows = [r for r in results if r["group"] == grp]
        grp_avg = sum(r["total"] for r in grp_rows) / len(grp_rows)
        print(f"  {grp:<12}: {len(grp_rows)} briefs | Avg Score = {grp_avg:.1f}/100")
    print("-" * 72)
    low = [r for r in results if r["total"] < 95]
    if low:
        print("Briefs below 95:")
        for r in low:
            print(f"  - {r['project']} ({r['page']}): {r['total']} {r['breakdown']}")
    else:
        print("All 30/30 briefs scored >= 95/100.")
    print(f"Overall Golden-Set Average: {avg:.2f}/100 (Target >= 95.00)")
    sys.exit(0 if avg >= 95.0 else 1)


if __name__ == "__main__":
    main()
