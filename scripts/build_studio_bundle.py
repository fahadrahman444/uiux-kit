#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compile UI/UX Pro Max CSV and JSON datasets into a compact static client-side
bundle for the zero-backend GitHub Pages vanilla web studio (docs/data/).
"""

import csv
import json
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = KIT_ROOT / "skills" / "ui-ux-pro-max" / "data"
OUT_DIR = KIT_ROOT / "docs" / "data"


def read_csv_rows(path: Path, keep_cols: set[str] | None = None) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not keep_cols:
        return rows
    return [{k: v for k, v in r.items() if k in keep_cols} for r in rows]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_DIR / "section-archetypes.json", "r", encoding="utf-8") as f:
        section_archetypes = json.load(f)
    with open(DATA_DIR / "page-templates.json", "r", encoding="utf-8") as f:
        page_templates = json.load(f)
    with open(DATA_DIR / "product-type-mapping.json", "r", encoding="utf-8") as f:
        product_mapping = json.load(f)

    guideline_cols = {"Category", "Issue", "Keywords", "Description", "Do", "Don't", "Severity"}
    stack_cols = {"Category", "Guideline", "Description", "Do", "Don't", "Severity"}

    stacks = {}
    for stack_csv in sorted((DATA_DIR / "stacks").glob("*.csv")):
        stacks[stack_csv.stem] = read_csv_rows(stack_csv, stack_cols)

    bundle = {
        "version": (KIT_ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "pageTemplates": page_templates,
        "sectionArchetypes": section_archetypes,
        "productMapping": product_mapping,
        "domains": {
            "style": read_csv_rows(DATA_DIR / "styles.csv", {"Style Category", "Type", "Keywords", "Effects & Animation", "Best For", "Performance", "Accessibility"}),
            "prompt": read_csv_rows(DATA_DIR / "prompts.csv", {"Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords"}),
            "color": read_csv_rows(DATA_DIR / "colors.csv"),
            "chart": read_csv_rows(DATA_DIR / "charts.csv", {"Data Type", "Keywords", "Best Chart Type", "Accessibility Notes", "Library Recommendation"}),
            "landing": read_csv_rows(DATA_DIR / "landing.csv", {"Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Conversion Optimization"}),
            "product": read_csv_rows(DATA_DIR / "products.csv", {"product_slug", "Product Type", "Keywords", "style_id", "Primary Style Recommendation", "landing_id", "Landing Page Pattern", "Key Considerations"}),
            "ux": read_csv_rows(DATA_DIR / "ux-guidelines.csv", guideline_cols),
            "typography": read_csv_rows(DATA_DIR / "typography.csv", {"Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "Tailwind Config"}),
            "icons": read_csv_rows(DATA_DIR / "icons.csv", {"Category", "Icon Name", "Keywords", "Library", "Usage", "Best For"}),
            "react": read_csv_rows(DATA_DIR / "react-performance.csv", guideline_cols),
            "web": read_csv_rows(DATA_DIR / "web-interface.csv", guideline_cols),
        },
        "stacks": stacks,
        "reasoning": read_csv_rows(DATA_DIR / "ui-reasoning.csv"),
    }

    json_text = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    json_path = OUT_DIR / "kit-bundle.json"
    js_path = OUT_DIR / "kit-bundle.js"

    json_path.write_text(json_text, encoding="utf-8")
    js_path.write_text(f"window.__SLOPGUARD_KIT_BUNDLE__ = {json_text};\n", encoding="utf-8")

    print(f"[OK] Wrote {json_path} ({len(json_text):,} bytes) and {js_path}")


if __name__ == "__main__":
    main()
