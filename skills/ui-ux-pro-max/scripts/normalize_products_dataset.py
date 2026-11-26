#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalize products.csv foreign keys (style_id, landing_id, product_slug),
eliminate prohibited Neumorphism recommendations, map every Landing Page Pattern
to an exact canonical Pattern Name in landing.csv, and emit product-type-mapping.json.
"""

import csv
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s


def load_csv(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_style_lookup(styles_rows: list[dict]) -> dict[str, int]:
    lookup: dict[str, int] = {}
    for row in styles_rows:
        name = row["Style Category"].strip().lower()
        sid = int(row["STT"])
        if name not in lookup:
            lookup[name] = sid
    return lookup


def build_landing_lookup(landing_rows: list[dict]) -> tuple[dict[str, int], dict[int, str]]:
    by_name: dict[str, int] = {}
    by_id: dict[int, str] = {}
    for row in landing_rows:
        lid = int(row["No"])
        name = row["Pattern Name"].strip()
        by_name[name.lower()] = lid
        by_id[lid] = name
    return by_name, by_id


EXPLICIT_STYLE_ALIASES = {
    "minimal": "Minimalism & Swiss Style",
    "minimalism": "Minimalism & Swiss Style",
    "minimalism (frame)": "Minimalism & Swiss Style",
    "swiss modernism": "Swiss Modernism 2.0",
    "vibrant & block": "Vibrant & Block-based",
    "dark mode": "Dark Mode (OLED)",
    "holographic / hud": "HUD / Sci-Fi FUI",
    "storytelling-driven": "Storytelling-Driven",
    "gen z chaos": "Gen Z Chaos / Maximalism",
    "clean science": "Minimalism & Swiss Style",
    "spatial ui": "Spatial UI (VisionOS)",
    "real-time monitor": "Real-Time Monitoring",
    "heat map & heatmap": "Heat Map & Heatmap Style",
    "e-ink / paper": "E-Ink / Paper",
    "high imagery": "Exaggerated Minimalism",
    "parallax": "Parallax Storytelling",
    "masonry grid": "Bento Box Grid",
}


def resolve_style_id(raw_rec: str, style_lookup: dict[str, int]) -> tuple[int, str]:
    cleaned = re.sub(r"\bNeumorphism\b", "Accessible & Ethical", raw_rec, flags=re.I)
    parts = [p.strip() for p in cleaned.split("+") if p.strip()]
    # Deduplicate while preserving order
    deduped = []
    for part in parts:
        if part.lower() not in [d.lower() for d in deduped]:
            deduped.append(part)
    cleaned_str = " + ".join(deduped) if deduped else "Minimalism & Swiss Style"

    for candidate in deduped:
        cl = candidate.lower()
        if cl in style_lookup and style_lookup[cl] != 2:
            return style_lookup[cl], cleaned_str
        alias = EXPLICIT_STYLE_ALIASES.get(cl)
        if alias and alias.lower() in style_lookup:
            return style_lookup[alias.lower()], cleaned_str
        for known, sid in style_lookup.items():
            if sid == 2:
                continue
            if cl in known or known in cl:
                return sid, cleaned_str
    return 1, cleaned_str


def sanitize_secondary_styles(raw_sec: str) -> str:
    if not raw_sec:
        return ""
    parts = [p.strip() for p in raw_sec.split(",") if p.strip()]
    updated = []
    for p in parts:
        if "neumorphism" in p.lower():
            replacement = "Soft UI Evolution"
        else:
            replacement = p
        if replacement.lower() not in [u.lower() for u in updated]:
            updated.append(replacement)
    return ", ".join(updated)


def resolve_landing_pattern(product_type: str, raw_lp: str, landing_by_name: dict[str, int], landing_by_id: dict[int, str]) -> tuple[int, str]:
    pt = product_type.lower()
    lp = raw_lp.lower().strip()

    # Exact match already
    if lp in landing_by_name:
        lid = landing_by_name[lp]
        return lid, landing_by_id[lid]

    # Product-specific high-precision mappings
    if "podcast" in pt or "brewery" in pt or "museum" in pt or "non-profit" in pt or "education" in pt or "pet tech" in pt:
        return 10, landing_by_id[10]  # Scroll-Triggered Storytelling
    if "portfolio" in pt or "photography" in pt or "architecture" in pt:
        return 26, landing_by_id[26]  # Portfolio Grid
    if "generative art" in pt:
        return 28, landing_by_id[28]  # Bento Grid Showcase
    if "knowledge base" in pt or "documentation" in pt or "developer tool" in pt:
        return 16, landing_by_id[16]  # FAQ/Documentation Landing
    if "newsletter" in pt or "magazine" in pt or "blog" in pt:
        return 23, landing_by_id[23]  # Newsletter / Content First
    if "marketplace" in pt:
        return 22, landing_by_id[22]  # Marketplace / Directory
    if "event" in pt:
        return 18, landing_by_id[18]  # Event/Conference Landing
    if "conference" in pt or "webinar" in pt:
        return 24, landing_by_id[24]  # Webinar Registration
    if "ai/chatbot" in pt:
        return 30, landing_by_id[30]  # AI-Driven Dynamic Landing
    if "automotive" in pt:
        return 29, landing_by_id[29]  # Interactive 3D Configurator
    if "space tech" in pt or "quantum" in pt or "spatial computing" in pt or "gaming" in pt:
        return 17, landing_by_id[17]  # Immersive/Interactive Experience
    if "insurance" in pt or "fintech" in pt or "job board" in pt or "cleaning" in pt or "home services" in pt or "pharmacy" in pt or "hyperlocal" in pt:
        return 5, landing_by_id[5]  # Funnel (3-Step Conversion)
    if "banking" in pt or "legal" in pt or "consulting" in pt or "cybersecurity" in pt or "b2b" in pt or "sustainability" in pt or "micro-credentials" in pt or "senior care" in pt or "medical" in pt:
        return 25, landing_by_id[25]  # Enterprise Gateway
    if "healthcare" in pt or "mental health" in pt or "childcare" in pt or "dental" in pt or "veterinary" in pt or "membership" in pt or "dating" in pt or "creator economy" in pt or "service landing" in pt or "beauty" in pt or "hotel" in pt or "wedding" in pt or "church" in pt:
        return 2, landing_by_id[2]  # Hero + Testimonials + CTA
    if "productivity" in pt or "smart home" in pt or "sustainable energy" in pt or "financial dashboard" in pt or "analytics dashboard" in pt or "drone" in pt or "biohacking" in pt:
        return 3, landing_by_id[3]  # Product Demo + Features
    if "government" in pt:
        return 4, landing_by_id[4]  # Minimal Single Column
    if "micro saas" in pt:
        return 4, landing_by_id[4]  # Minimal Single Column

    # Pattern keyword fallbacks
    if "bento" in lp:
        return 28, landing_by_id[28]
    if "social proof" in lp:
        return 2, landing_by_id[2]
    if "storytelling" in lp:
        return 10, landing_by_id[10]
    if "interactive" in lp or "demo" in lp:
        return 3, landing_by_id[3]
    if "minimal" in lp:
        return 4, landing_by_id[4]
    if "comparison" in lp:
        return 6, landing_by_id[6]
    if "pricing" in lp:
        return 8, landing_by_id[8]
    if "trust" in lp:
        return 25, landing_by_id[25]
    if "conversion" in lp:
        return 5, landing_by_id[5]

    return 1, landing_by_id[1]  # Hero + Features + CTA


def choose_sections(product_type: str, landing_name: str) -> list[str]:
    pt = product_type.lower()
    base = ["navbar", "hero", "trusted_by"]
    if "pricing" in landing_name.lower() or "saas" in pt or "subscription" in pt:
        return base + ["services", "why_choose_us", "pricing", "pricing_comparison_matrix", "faq", "final_cta", "footer"]
    if "portfolio" in pt or "agency" in pt or "photography" in pt or "architecture" in pt:
        return base + ["about", "portfolio", "case_study_filter_hub", "testimonials", "final_cta", "footer"]
    if "documentation" in landing_name.lower() or "knowledge" in pt or "developer" in pt:
        return ["navbar", "hero", "service_architecture", "service_tech_stack", "faq", "final_cta", "footer"]
    if "newsletter" in landing_name.lower() or "blog" in pt or "magazine" in pt:
        return ["navbar", "blog_featured_editorial", "blog_topic_filter_feed", "blog_newsletter_capture", "footer"]
    if "software agency" in pt or "solutions hub" in pt or "dark kinetic" in landing_name.lower():
        return ["navbar", "hero", "trusted_by", "about", "services", "results_metrics", "portfolio", "testimonials", "final_cta", "footer"]
    return base + ["services", "how_we_work", "results_metrics", "testimonials", "faq", "final_cta", "footer"]


def main():
    styles_rows = load_csv(DATA_DIR / "styles.csv")
    landing_rows = load_csv(DATA_DIR / "landing.csv")
    products_rows = load_csv(DATA_DIR / "products.csv")

    with open(DATA_DIR / "section-archetypes.json", "r", encoding="utf-8") as f:
        valid_sections = {s["section_id"] for s in json.load(f)}

    style_lookup = build_style_lookup(styles_rows)
    landing_by_name, landing_by_id = build_landing_lookup(landing_rows)

    fieldnames = [
        "No",
        "product_slug",
        "Product Type",
        "Keywords",
        "style_id",
        "Primary Style Recommendation",
        "Secondary Styles",
        "landing_id",
        "Landing Page Pattern",
        "Dashboard Style (if applicable)",
        "Color Palette Focus",
        "Key Considerations",
    ]

    updated_rows = []
    mapping_json: dict[str, dict] = {}
    seen_slugs: set[str] = set()

    for row in products_rows:
        ptype = row["Product Type"].strip()
        slug = slugify(ptype)
        if slug in seen_slugs:
            slug = f"{slug}-{row['No'].strip()}"
        seen_slugs.add(slug)

        style_id, clean_primary = resolve_style_id(row.get("Primary Style Recommendation", ""), style_lookup)
        clean_secondary = sanitize_secondary_styles(row.get("Secondary Styles", ""))
        landing_id, canonical_lp = resolve_landing_pattern(
            ptype, row.get("Landing Page Pattern", ""), landing_by_name, landing_by_id
        )
        rec_sections = [s for s in choose_sections(ptype, canonical_lp) if s in valid_sections]

        updated = {
            "No": row["No"].strip(),
            "product_slug": slug,
            "Product Type": ptype,
            "Keywords": row.get("Keywords", "").strip(),
            "style_id": str(style_id),
            "Primary Style Recommendation": clean_primary,
            "Secondary Styles": clean_secondary,
            "landing_id": str(landing_id),
            "Landing Page Pattern": canonical_lp,
            "Dashboard Style (if applicable)": row.get("Dashboard Style (if applicable)", "").strip(),
            "Color Palette Focus": row.get("Color Palette Focus", "").strip(),
            "Key Considerations": row.get("Key Considerations", "").strip(),
        }
        updated_rows.append(updated)

        mapping_json[slug] = {
            "product_type": ptype,
            "style_ids": [style_id],
            "primary_style": clean_primary,
            "landing_pattern_id": landing_id,
            "landing_pattern": canonical_lp,
            "recommended_sections": rec_sections,
        }

    with open(DATA_DIR / "products.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    with open(DATA_DIR / "product-type-mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping_json, f, indent=2, ensure_ascii=False)

    print(f"[OK] Normalized {len(updated_rows)} rows in products.csv and wrote product-type-mapping.json")


if __name__ == "__main__":
    main()
