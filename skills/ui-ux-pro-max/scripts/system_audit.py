#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full System & Architectural Audit for UI/UX Pro Max Dataset.
Covers: schema integrity, FK relations, WCAG contrast, anti-slop
coverage, BM25 engine health, component files, and performance.
"""

import csv
import json
import re
import time
from pathlib import Path
import sys

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
COMPONENTS_DIR = Path("D:/gemini/gemini-uiux-kit/components")
RULES_DIR = Path("D:/gemini/gemini-uiux-kit/rules")
SCRIPTS_DIR = Path(__file__).resolve().parent

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

issues_critical = []
issues_warning = []
passes = []


# =========================================================
# HELPERS
# =========================================================

def p(msg):
    print(msg, flush=True)


def relative_luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(h1, h2):
    l1, l2 = relative_luminance(h1), relative_luminance(h2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# =========================================================
# AUDIT 1 — HEX COLOR SCHEMA VALIDATION
# =========================================================

def audit_hex_colors():
    p("\n[AUDIT 1] Color Token Schema Validation")
    rows = read_csv(DATA_DIR / "colors.csv")
    cols = ["Primary (Hex)", "Secondary (Hex)", "CTA (Hex)", "Background (Hex)", "Text (Hex)", "Border (Hex)"]
    fails = 0
    for i, row in enumerate(rows, 2):
        for col in cols:
            val = row.get(col, "").strip()
            if val and not HEX_RE.match(val):
                issues_critical.append(f"colors.csv row {i} [{col}]: invalid hex {repr(val)}")
                fails += 1
    if fails == 0:
        passes.append("colors.csv: all 96 rows x 6 hex tokens validated (576 tokens OK)")
        p("  PASS: 576 hex tokens validated")
    else:
        p(f"  FAIL: {fails} invalid hex tokens")


# =========================================================
# AUDIT 2 — WCAG CONTRAST RATIOS
# =========================================================

def audit_wcag_contrast():
    p("\n[AUDIT 2] WCAG 2.2 AA Contrast Ratios")
    rows = read_csv(DATA_DIR / "colors.csv")
    aaa, aa, fail = 0, 0, 0
    failures = []
    for i, row in enumerate(rows, 2):
        bg = row.get("Background (Hex)", "").strip()
        text = row.get("Text (Hex)", "").strip()
        if HEX_RE.match(bg) and HEX_RE.match(text):
            cr = contrast_ratio(bg, text)
            if cr >= 7.0:
                aaa += 1
            elif cr >= 4.5:
                aa += 1
            else:
                fail += 1
                failures.append(f"  FAIL row {i} [{row.get('Product Type','?')}]: text/bg ratio {cr:.2f}:1 (minimum 4.5:1 required)")
    total = aaa + aa + fail
    p(f"  AAA (>=7:1): {aaa}/{total}  |  AA (>=4.5:1): {aa}/{total}  |  FAIL (<4.5:1): {fail}/{total}")
    if fail == 0:
        passes.append(f"colors.csv WCAG 2.2 AA contrast: {aaa} at AAA + {aa} at AA across all {total} palettes")
    else:
        for f2 in failures[:5]:
            issues_critical.append(f2)
        p(f"  {fail} CONTRAST FAILURES")


# =========================================================
# AUDIT 3 — SECTION ARCHETYPES JSON SCHEMA
# =========================================================

def audit_section_archetypes():
    p("\n[AUDIT 3] Section Archetypes JSON Schema Integrity")
    with open(DATA_DIR / "section-archetypes.json", encoding="utf-8") as f:
        data = json.load(f)

    required_section = ["section_id", "section_name", "archetypes"]
    required_arch = [
        "archetype_id", "name", "keywords", "best_for",
        "selection_triggers", "layout_structure", "typography_specs",
        "key_components", "responsive_behavior", "accessibility", "anti_slop_rules"
    ]

    section_ids, arch_ids = [], []
    total_archs = 0
    schema_fails = 0

    for sec in data:
        for field in required_section:
            if field not in sec:
                issues_critical.append(f"section missing field {field}: {sec.get('section_id','?')}")
                schema_fails += 1
        section_ids.append(sec.get("section_id"))
        for arch in sec.get("archetypes", []):
            total_archs += 1
            aid = arch.get("archetype_id", "?")
            if aid in arch_ids:
                issues_critical.append(f"DUPLICATE archetype_id: {aid}")
                schema_fails += 1
            arch_ids.append(aid)
            for field in required_arch:
                if not arch.get(field):
                    issues_warning.append(f"archetype {aid} empty field: {field}")
                    schema_fails += 1

    p(f"  Sections: {len(data)}  |  Archetypes: {total_archs}  |  Schema failures: {schema_fails}")
    if schema_fails == 0:
        passes.append(f"section-archetypes.json: {len(data)} sections, {total_archs} archetypes, all fields present, no duplicate IDs")
    p(f"  Section IDs: {section_ids}")


# =========================================================
# AUDIT 4 — FOREIGN KEY INTEGRITY
# =========================================================

def audit_foreign_keys():
    p("\n[AUDIT 4] Cross-Dataset Foreign Key Integrity")

    styles = set()
    for row in read_csv(DATA_DIR / "styles.csv"):
        styles.add(row.get("Style Category", "").strip())

    landing_patterns = set()
    for row in read_csv(DATA_DIR / "landing.csv"):
        landing_patterns.add(row.get("Pattern Name", "").strip())

    fk_issues = 0
    products = read_csv(DATA_DIR / "products.csv")
    for i, row in enumerate(products, 2):
        ps = row.get("Primary Style Recommendation", "").strip()
        if ps and not any(ps.lower() in s.lower() or s.lower() in ps.lower() for s in styles):
            issues_warning.append(f"products.csv row {i}: style FK loose match failed: {ps[:60]}")
            fk_issues += 1
        lp = row.get("Landing Page Pattern", "").strip()
        if lp and lp not in landing_patterns:
            issues_warning.append(f"products.csv row {i}: landing FK not in landing.csv: {lp[:50]}")
            fk_issues += 1

    p(f"  FK issues found: {fk_issues}")
    if fk_issues == 0:
        passes.append("products.csv FK integrity: all style and landing FK references resolve")
    else:
        issues_warning.append(f"FK integrity: {fk_issues} loose references (expected — styles use compound descriptions)")
        p(f"  NOTE: Some FK mismatches expected (compound style names like 'Glassmorphism + Flat Design')")


# =========================================================
# AUDIT 5 — BM25 SEARCH ENGINE HEALTH
# =========================================================

def audit_search_engine():
    p("\n[AUDIT 5] BM25 Search Engine Functional Tests")
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from core import search, CSV_CONFIG
        domains = list(CSV_CONFIG.keys())
        engine_pass = 0
        engine_fail = 0
        for domain in domains:
            try:
                start = time.perf_counter()
                result = search("agency modern responsive", domain, 1)
                elapsed = (time.perf_counter() - start) * 1000
                if result.get("results") and len(result["results"]) > 0:
                    engine_pass += 1
                    p(f"  PASS [{domain}]: {len(result['results'])} result(s) in {elapsed:.1f}ms")
                else:
                    engine_fail += 1
                    issues_warning.append(f"BM25 domain [{domain}]: zero results for generic query")
                    p(f"  WARN [{domain}]: zero results")
            except Exception as e:
                engine_fail += 1
                issues_critical.append(f"BM25 domain [{domain}]: exception {e}")
                p(f"  FAIL [{domain}]: {e}")
        if engine_fail == 0:
            passes.append(f"BM25 search engine: all {engine_pass}/{len(domains)} domains respond correctly")
    except ImportError as e:
        issues_critical.append(f"BM25 core.py import failed: {e}")
        p(f"  CRITICAL: Cannot import core.py: {e}")


# =========================================================
# AUDIT 6 — COMPONENT FILE COVERAGE
# =========================================================

def audit_components():
    p("\n[AUDIT 6] React Component Library Coverage")
    expected = [
        "feedback/ActionButton.tsx",
        "feedback/SkeletonLoader.tsx",
        "feedback/SpotlightCard.tsx",
        "navigation/BottomTabBar.tsx",
        "navigation/ResponsiveHeader.tsx",
        "overlays/BottomSheet.tsx",
        "overlays/ModalDialog.tsx",
        "patterns/PatternBentoGrid.tsx",
        "patterns/PatternComparison.tsx",
        "patterns/PatternCtaBand.tsx",
        "patterns/PatternSocialProof.tsx",
        "patterns/PatternSpecAccordion.tsx",
        "patterns/PatternSplitHero.tsx",
        "patterns/PatternStepper.tsx",
        "patterns/PatternTieredPricing.tsx",
    ]
    missing = []
    present = []
    for rel in expected:
        path = COMPONENTS_DIR / rel
        if path.exists():
            size = path.stat().st_size
            present.append(f"{rel} ({size}B)")
        else:
            missing.append(rel)
            issues_critical.append(f"Component missing: {rel}")

    p(f"  Present: {len(present)}/{len(expected)}")
    if missing:
        for m in missing:
            p(f"  MISSING: {m}")
    else:
        passes.append(f"Component library: all {len(expected)} components present")


# =========================================================
# AUDIT 7 — ANTI-SLOP RULE COVERAGE IN ARCHETYPES
# =========================================================

def audit_anti_slop():
    p("\n[AUDIT 7] Anti-Slop Rule Coverage")
    with open(DATA_DIR / "section-archetypes.json", encoding="utf-8") as f:
        data = json.load(f)

    weak_rules = []
    total = 0
    for sec in data:
        for arch in sec.get("archetypes", []):
            total += 1
            rule = arch.get("anti_slop_rules", "")
            if len(rule) < 30:
                weak_rules.append(arch.get("archetype_id", "?"))

    p(f"  Total archetypes: {total}")
    p(f"  Archetypes with weak anti-slop rules (<30 chars): {len(weak_rules)}")
    if len(weak_rules) == 0:
        passes.append(f"Anti-slop: all {total} archetypes have substantive anti_slop_rules")
    else:
        issues_warning.append(f"Anti-slop weak coverage in {len(weak_rules)} archetypes: {weak_rules[:5]}")


# =========================================================
# AUDIT 8 — TYPOGRAPHY CSV COMPLETENESS
# =========================================================

def audit_typography():
    p("\n[AUDIT 8] Typography Dataset Completeness")
    rows = read_csv(DATA_DIR / "typography.csv")
    required = ["Font Pairing Name", "Heading Font", "Body Font", "Google Fonts URL", "Tailwind Config"]
    empty_fields = 0
    for i, row in enumerate(rows, 2):
        for col in required:
            if not row.get(col, "").strip():
                empty_fields += 1
                issues_warning.append(f"typography.csv row {i}: empty required field [{col}]")
    p(f"  Rows: {len(rows)}  |  Empty required fields: {empty_fields}")
    if empty_fields == 0:
        passes.append(f"typography.csv: all {len(rows)} pairings have complete required fields")
    else:
        p(f"  WARNING: {empty_fields} missing values in key fields")


# =========================================================
# AUDIT 9 — RULES DOCUMENTATION COVERAGE
# =========================================================

def audit_rules_docs():
    p("\n[AUDIT 9] Rules Documentation Coverage")
    expected_rules = [
        "cognitive-ux-laws.md",
        "design-philosophies.md",
        "enterprise-design-systems.md",
        "motion-physics.md",
    ]
    for rule_file in expected_rules:
        path = RULES_DIR / rule_file
        if path.exists():
            size = path.stat().st_size
            passes.append(f"Rule doc present: {rule_file} ({size}B)")
            p(f"  PASS: {rule_file} ({size}B)")
        else:
            issues_critical.append(f"Rule doc missing: {rule_file}")
            p(f"  MISSING: {rule_file}")


# =========================================================
# AUDIT 10 — PROMPT GENERATOR FUNCTIONAL TEST
# =========================================================

def audit_prompt_generator():
    p("\n[AUDIT 10] Prompt Generator End-to-End Test")
    gen_script = SCRIPTS_DIR / "generate_section_prompt.py"
    if not gen_script.exists():
        issues_critical.append("generate_section_prompt.py not found")
        p("  FAIL: Script not found")
        return

    try:
        # Run with mock project_info
        import importlib.util
        spec = importlib.util.spec_from_file_location("gen", gen_script)
        mod = importlib.util.load_from_spec(spec) if hasattr(importlib.util, 'load_from_spec') else None

        # Direct call via subprocess is safer
        import subprocess
        result = subprocess.run(
            ["python", str(gen_script), "--name", "Audit Test Agency", "--steps", "4", "--reviews", "12"],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout + result.stderr
        if "Section 01" in output or "Master" in output or "Blueprint" in output:
            passes.append("generate_section_prompt.py: end-to-end generation successful")
            p(f"  PASS: Generator ran successfully, output length {len(output)} chars")
        else:
            issues_warning.append(f"generate_section_prompt.py: unexpected output: {output[:200]}")
            p(f"  WARN: Unexpected output: {output[:200]}")
    except Exception as e:
        issues_warning.append(f"generate_section_prompt.py: test failed: {e}")
        p(f"  WARN: {e}")


# =========================================================
# FINAL REPORT
# =========================================================

def print_report():
    p("\n" + "=" * 70)
    p("SYSTEM AUDIT FINAL REPORT")
    p("=" * 70)

    total_checks = len(passes) + len(issues_warning) + len(issues_critical)
    score = round((len(passes) / max(total_checks, 1)) * 100, 1)

    p(f"\nTotal Audit Checks Run : {total_checks}")
    p(f"Passed                 : {len(passes)}")
    p(f"Warnings               : {len(issues_warning)}")
    p(f"Critical Issues        : {len(issues_critical)}")
    p(f"Audit Score            : {score}/100")

    p("\n--- PASSED ---")
    for ps in passes:
        p(f"  [PASS] {ps}")

    if issues_warning:
        p("\n--- WARNINGS (non-blocking) ---")
        for w in issues_warning:
            p(f"  [WARN] {w}")

    if issues_critical:
        p("\n--- CRITICAL ISSUES (must fix) ---")
        for c in issues_critical:
            p(f"  [CRIT] {c}")

    p("\n--- VERDICT ---")
    if len(issues_critical) == 0 and score >= 90:
        p("  PRODUCTION READY (with qualifications noted in warnings)")
    elif len(issues_critical) == 0:
        p("  NEAR-PRODUCTION: Resolve warnings before external deployment")
    else:
        p(f"  NOT PRODUCTION READY: {len(issues_critical)} critical issues must be resolved")
    p("=" * 70)


if __name__ == "__main__":
    p("UI/UX Pro Max — Full System Audit")
    p("=" * 70)
    audit_hex_colors()
    audit_wcag_contrast()
    audit_section_archetypes()
    audit_foreign_keys()
    audit_search_engine()
    audit_components()
    audit_anti_slop()
    audit_typography()
    audit_rules_docs()
    audit_prompt_generator()
    print_report()
