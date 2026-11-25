#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compile UI/UX Pro Max CSV and JSON datasets into a static client-side bundle
for the zero-backend GitHub Pages vanilla web studio (docs/data/).
"""

import csv
import json
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = KIT_ROOT / "skills" / "ui-ux-pro-max" / "data"
OUT_DIR = KIT_ROOT / "docs" / "data"


def read_csv_rows(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_DIR / "section-archetypes.json", "r", encoding="utf-8") as f:
        section_archetypes = json.load(f)
    with open(DATA_DIR / "page-templates.json", "r", encoding="utf-8") as f:
        page_templates = json.load(f)
    with open(DATA_DIR / "product-type-mapping.json", "r", encoding="utf-8") as f:
        product_mapping = json.load(f)

    stacks = {}
    for stack_csv in sorted((DATA_DIR / "stacks").glob("*.csv")):
        stacks[stack_csv.stem] = read_csv_rows(stack_csv)

    bundle = {
        "version": (KIT_ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "pageTemplates": page_templates,
        "sectionArchetypes": section_archetypes,
        "productMapping": product_mapping,
        "domains": {
            "style": read_csv_rows(DATA_DIR / "styles.csv"),
            "prompt": read_csv_rows(DATA_DIR / "prompts.csv"),
            "color": read_csv_rows(DATA_DIR / "colors.csv"),
            "chart": read_csv_rows(DATA_DIR / "charts.csv"),
            "landing": read_csv_rows(DATA_DIR / "landing.csv"),
            "product": read_csv_rows(DATA_DIR / "products.csv"),
            "ux": read_csv_rows(DATA_DIR / "ux-guidelines.csv"),
            "typography": read_csv_rows(DATA_DIR / "typography.csv"),
            "icons": read_csv_rows(DATA_DIR / "icons.csv"),
            "react": read_csv_rows(DATA_DIR / "react-performance.csv"),
            "web": read_csv_rows(DATA_DIR / "web-interface.csv"),
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
