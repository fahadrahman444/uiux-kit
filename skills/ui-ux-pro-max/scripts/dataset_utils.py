#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared JSON + CSV synchronization helpers for section-archetypes datasets."""

import csv
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CSV_FIELDNAMES = [
    "Section ID", "Section Name", "Archetype ID", "Archetype Name",
    "Keywords", "Best For", "Selection Triggers", "Layout Structure",
    "Typography Specs", "Key Components", "Responsive Behavior",
    "Accessibility", "Anti-Slop Rules",
]


def upsert_sections(new_sections: list, data_dir: Path = DATA_DIR) -> tuple[int, int]:
    """Append missing sections to section-archetypes.json and rebuild section-archetypes.csv."""
    json_path = data_dir / "section-archetypes.json"
    csv_path = data_dir / "section-archetypes.csv"

    with open(json_path, "r", encoding="utf-8") as f:
        existing_sections = json.load(f)

    existing_ids = {s["section_id"] for s in existing_sections}
    for new_sec in new_sections:
        if new_sec["section_id"] not in existing_ids:
            existing_sections.append(new_sec)
            existing_ids.add(new_sec["section_id"])
            print(f"  + Added section: {new_sec['section_id']} ({len(new_sec['archetypes'])} archetypes)")
        else:
            print(f"  * Section {new_sec['section_id']} already exists, skipping duplicate")

    return write_sections_dataset(existing_sections, data_dir)


def write_sections_dataset(sections: list, data_dir: Path = DATA_DIR) -> tuple[int, int]:
    """Persist sections list to section-archetypes.json and section-archetypes.csv."""
    json_path = data_dir / "section-archetypes.json"
    csv_path = data_dir / "section-archetypes.csv"

    total_sections = len(sections)
    total_archetypes = sum(len(s["archetypes"]) for s in sections)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON updated: {total_sections} sections, {total_archetypes} archetypes")

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for sec in sections:
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
    return total_sections, total_archetypes
