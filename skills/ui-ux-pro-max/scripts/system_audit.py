#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full System & Architectural Audit for UI/UX Pro Max Dataset & SlopGuard Kit.
Covers: schema integrity, WCAG contrast (text + CTA), page templates,
FK relations, BM25 engine health, component files, rules docs, and prompt generator.
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCRIPTS_DIR = Path(__file__).resolve().parent
KIT_ROOT = SCRIPTS_DIR.parent.parent.parent
COMPONENTS_DIR = KIT_ROOT / "components"
RULES_DIR = KIT_ROOT / "rules"

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

issues_critical = []
issues_warning = []
passes = []


def p(msg):
    print(msg, flush=True)


def relative_luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

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
        passes.append(f"colors.csv: all {len(rows)} rows x 6 hex tokens validated ({len(rows) * 6} tokens OK)")
        p(f"  PASS: {len(rows) * 6} hex tokens validated")
    else:
        p(f"  FAIL: {fails} invalid hex tokens")


# =========================================================
# AUDIT 2 — WCAG CONTRAST RATIOS (TEXT + CTA)
# =========================================================

def audit_wcag_contrast():
    p("\n[AUDIT 2] WCAG 2.2 AA Contrast Ratios (Text & CTA)")
    rows = read_csv(DATA_DIR / "colors.csv")
    aaa, aa, fail = 0, 0, 0
    cta_fail = 0
    failures = []
    for i, row in enumerate(rows, 2):
        bg = row.get("Background (Hex)", "").strip()
        text = row.get("Text (Hex)", "").strip()
        cta = row.get("CTA (Hex)", "").strip()
        if HEX_RE.match(bg) and HEX_RE.match(text):
            cr = contrast_ratio(bg, text)
            if cr >= 7.0:
                aaa += 1
            elif cr >= 4.5:
                aa += 1
            else:
                fail += 1
                failures.append(f"  FAIL row {i} [{row.get('Product Type', '?')}]: text/bg ratio {cr:.2f}:1 (< 4.5:1)")
        if HEX_RE.match(bg) and HEX_RE.match(cta):
            cr_cta_bg = contrast_ratio(cta, bg)
            cr_cta_fg = max(contrast_ratio(cta, "#FFFFFF"), contrast_ratio(cta, "#020617"))
            if cr_cta_bg < 3.0 or cr_cta_fg < 4.5:
                cta_fail += 1
                failures.append(
                    f"  FAIL row {i} [{row.get('Product Type', '?')}]: CTA {cta} contrast "
                    f"(vsBg={cr_cta_bg:.2f}:1, maxFg={cr_cta_fg:.2f}:1)"
                )

    total = aaa + aa + fail
    p(f"  Text/Bg — AAA (>=7:1): {aaa}/{total} | AA (>=4.5:1): {aa}/{total} | FAIL: {fail}/{total}")
    p(f"  CTA Contrast Failures: {cta_fail}/{total}")
    if fail == 0 and cta_fail == 0:
        passes.append(f"colors.csv WCAG 2.2 AA contrast: {aaa} AAA + {aa} AA text pairs and {total}/{total} CTA pairs OK")
    else:
        for f2 in failures[:10]:
            issues_critical.append(f2)


# =========================================================
# AUDIT 3 — SECTION ARCHETYPES JSON/CSV INTEGRITY
# =========================================================

def audit_section_archetypes():
    p("\n[AUDIT 3] Section Archetypes JSON & CSV Integrity")
    with open(DATA_DIR / "section-archetypes.json", encoding="utf-8") as f:
        data = json.load(f)
    csv_rows = read_csv(DATA_DIR / "section-archetypes.csv")

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
                issues_critical.append(f"section missing field {field}: {sec.get('section_id', '?')}")
                schema_fails += 1
        sid = sec.get("section_id")
        if sid in section_ids:
            issues_critical.append(f"DUPLICATE section_id: {sid}")
            schema_fails += 1
        section_ids.append(sid)
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

    csv_arch_ids = [r.get("Archetype ID", "") for r in csv_rows]
    if arch_ids != csv_arch_ids:
        issues_critical.append(
            f"JSON/CSV mismatch: JSON has {len(arch_ids)} archetypes, CSV has {len(csv_arch_ids)}"
        )
        schema_fails += 1

    p(f"  Sections: {len(data)} | Archetypes: {total_archs} | CSV Rows: {len(csv_rows)} | Failures: {schema_fails}")
    if schema_fails == 0:
        passes.append(
            f"section-archetypes.json & .csv: {len(data)} sections, {total_archs} archetypes synced with zero duplicates"
        )


# =========================================================
# AUDIT 4 — PAGE TEMPLATES REGISTRY INTEGRITY
# =========================================================

def audit_page_templates():
    p("\n[AUDIT 4] Page Templates Registry Integrity")
    with open(DATA_DIR / "section-archetypes.json", encoding="utf-8") as f:
        sec_ids = {s["section_id"] for s in json.load(f)}
    with open(DATA_DIR / "page-templates.json", encoding="utf-8") as f:
        tpls = json.load(f)

    pages = tpls.get("pages", [])
    declared = tpls.get("total_pages")
    errs = 0
    if declared != len(pages):
        issues_critical.append(f"page-templates.json: total_pages={declared} does not match len(pages)={len(pages)}")
        errs += 1
    for pg in pages:
        missing = [sid for sid in pg.get("default_section_flow", []) if sid not in sec_ids]
        if missing:
            issues_critical.append(f"page-templates.json [{pg.get('page_id')}]: missing sections {missing}")
            errs += 1
    p(f"  Pages: {len(pages)} (declared {declared}) | Missing section refs: {errs}")
    if errs == 0:
        passes.append(f"page-templates.json: all {len(pages)} pages and section flows resolve cleanly")


# =========================================================
# AUDIT 5 — CROSS-DATASET FOREIGN KEY INTEGRITY
# =========================================================

def audit_foreign_keys():
    p("\n[AUDIT 5] Cross-Dataset Foreign Key Integrity")

    styles = {row.get("Style Category", "").strip().lower() for row in read_csv(DATA_DIR / "styles.csv")}
    landing_patterns = {row.get("Pattern Name", "").strip().lower() for row in read_csv(DATA_DIR / "landing.csv")}
    products = read_csv(DATA_DIR / "products.csv")

    style_unresolved = []
    landing_compound = 0
    for i, row in enumerate(products, 2):
        ps = row.get("Primary Style Recommendation", "").strip().lower()
        if ps:
            parts = [part.strip() for part in ps.split("+")]
            if not any(any(part in s or s in part for s in styles) for part in parts):
                style_unresolved.append(f"row {i}: {ps}")
        lp = row.get("Landing Page Pattern", "").strip().lower()
        if lp and lp not in landing_patterns:
            landing_compound += 1

    p(f"  Unresolved style FKs: {len(style_unresolved)} | Non-exact compound landing labels: {landing_compound}/{len(products)}")
    if style_unresolved:
        issues_warning.append(f"products.csv style FKs unresolved ({len(style_unresolved)}): {style_unresolved[:3]}")
    else:
        passes.append(f"products.csv style FKs: all {len(products)} product rows resolve to styles.csv")

    if landing_compound > 0:
        issues_warning.append(
            f"products.csv landing labels: {landing_compound}/{len(products)} use descriptive compound labels outside landing.csv"
        )
    else:
        passes.append("products.csv landing FKs: all references resolve strictly to landing.csv")


# =========================================================
# AUDIT 6 — BM25 SEARCH ENGINE HEALTH
# =========================================================

def audit_search_engine():
    p("\n[AUDIT 6] BM25 Search Engine Functional Tests")
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from core import search, detect_domain, CSV_CONFIG
        domain_queries = {
            "style": "minimalism clean",
            "prompt": "minimalism tailwind",
            "color": "b2b service",
            "chart": "bar trend",
            "landing": "hero cta",
            "product": "saas dashboard",
            "ux": "accessibility contrast",
            "typography": "modern sans",
            "icons": "arrow navigation",
            "react": "memo rerender",
            "web": "aria focus",
            "section": "hero split",
        }
        engine_pass = 0
        engine_fail = 0
        for domain in CSV_CONFIG:
            q = domain_queries.get(domain, "modern design")
            try:
                start = time.perf_counter()
                result = search(q, domain, 1)
                elapsed = (time.perf_counter() - start) * 1000
                if result.get("results"):
                    engine_pass += 1
                    p(f"  PASS [{domain}] ({q!r}): {len(result['results'])} result(s) in {elapsed:.1f}ms")
                else:
                    engine_fail += 1
                    issues_warning.append(f"BM25 domain [{domain}]: zero results for {q!r}")
                    p(f"  WARN [{domain}]: zero results")
            except Exception as e:
                engine_fail += 1
                issues_critical.append(f"BM25 domain [{domain}]: exception {e}")
                p(f"  FAIL [{domain}]: {e}")

        # Verify detect_domain avoids substring false positives
        fp_checks = {
            "sidebar toolbar": "ux",
            "c# desktop app": "style",
            "build a quick guide": "style",
            "section hero": "section",
        }
        fp_fails = []
        for q, expected in fp_checks.items():
            got = detect_domain(q)
            if got != expected:
                fp_fails.append(f"{q!r}->{got!r} (expected {expected!r})")
        if fp_fails:
            issues_warning.append(f"detect_domain false routing: {fp_fails}")
        else:
            passes.append("detect_domain(): word-boundary routing checks passed")

        if engine_fail == 0:
            passes.append(f"BM25 search engine: all {engine_pass}/{len(CSV_CONFIG)} domains respond correctly")
    except ImportError as e:
        issues_critical.append(f"BM25 core.py import failed: {e}")
        p(f"  CRITICAL: Cannot import core.py: {e}")


# =========================================================
# AUDIT 7 — COMPONENT LIBRARY COVERAGE
# =========================================================

def audit_components():
    p("\n[AUDIT 7] React Component Library Coverage")
    expected = [
        "feedback/ActionButton.tsx",
        "feedback/SkeletonLoader.tsx",
        "feedback/SpotlightCard.tsx",
        "navigation/BottomTabBar.tsx",
        "navigation/ResponsiveHeader.tsx",
        "overlays/BottomSheet.tsx",
        "overlays/ModalDialog.tsx",
        "patterns/index.ts",
        "patterns/types.ts",
        "patterns/PatternBentoGrid.tsx",
        "patterns/PatternComparison.tsx",
        "patterns/PatternCtaBand.tsx",
        "patterns/PatternSocialProof.tsx",
        "patterns/PatternSpecAccordion.tsx",
        "patterns/PatternSplitHero.tsx",
        "patterns/PatternStepper.tsx",
        "patterns/PatternTieredPricing.tsx",
    ]
    missing = [rel for rel in expected if not (COMPONENTS_DIR / rel).exists()]
    for m in missing:
        issues_critical.append(f"Component missing: {m}")
    p(f"  Present: {len(expected) - len(missing)}/{len(expected)}")
    if not missing:
        passes.append(f"Component library: all {len(expected)} files present")


# =========================================================
# AUDIT 8 — ANTI-SLOP RULE COVERAGE & DEPRECATED STYLES
# =========================================================

def audit_anti_slop():
    p("\n[AUDIT 8] Anti-Slop Rule Coverage & Deprecated Style Check")
    with open(DATA_DIR / "section-archetypes.json", encoding="utf-8") as f:
        data = json.load(f)

    weak_rules = []
    total = 0
    for sec in data:
        for arch in sec.get("archetypes", []):
            total += 1
            if len(arch.get("anti_slop_rules", "")) < 30:
                weak_rules.append(arch.get("archetype_id", "?"))

    reasoning = read_csv(DATA_DIR / "ui-reasoning.csv")
    banned_rec = [
        r.get("UI_Category", "?")
        for r in reasoning
        if "neumorphism" in r.get("Style_Priority", "").lower()
    ]

    p(f"  Total archetypes: {total} | Weak anti-slop rules: {len(weak_rules)} | Banned Neumorphism recs: {len(banned_rec)}")
    if not weak_rules:
        passes.append(f"Anti-slop: all {total} archetypes have substantive anti_slop_rules")
    else:
        issues_warning.append(f"Anti-slop weak coverage in {len(weak_rules)} archetypes: {weak_rules[:5]}")
    if banned_rec:
        issues_critical.append(f"ui-reasoning.csv recommends prohibited Neumorphism in: {banned_rec}")
    else:
        passes.append("ui-reasoning.csv: zero prohibited Neumorphism recommendations")


# =========================================================
# AUDIT 9 — TYPOGRAPHY CSV COMPLETENESS
# =========================================================

def audit_typography():
    p("\n[AUDIT 9] Typography Dataset Completeness")
    rows = read_csv(DATA_DIR / "typography.csv")
    required = ["Font Pairing Name", "Heading Font", "Body Font", "Google Fonts URL", "Tailwind Config"]
    empty_fields = 0
    for i, row in enumerate(rows, 2):
        for col in required:
            if not row.get(col, "").strip():
                empty_fields += 1
                issues_warning.append(f"typography.csv row {i}: empty required field [{col}]")
    p(f"  Rows: {len(rows)} | Empty required fields: {empty_fields}")
    if empty_fields == 0:
        passes.append(f"typography.csv: all {len(rows)} pairings have complete required fields")


# =========================================================
# AUDIT 10 — RULES DOCUMENTATION COVERAGE
# =========================================================

def audit_rules_docs():
    p("\n[AUDIT 10] Rules Documentation Coverage")
    expected_rules = [
        "visual-identity.md",
        "design-philosophies.md",
        "cognitive-ux-laws.md",
        "enterprise-design-systems.md",
        "accessibility-wcag.md",
        "mobile-ergonomics.md",
        "motion-physics.md",
    ]
    missing = 0
    for rule_file in expected_rules:
        path = RULES_DIR / rule_file
        if path.exists():
            p(f"  PASS: {rule_file} ({path.stat().st_size}B)")
        else:
            missing += 1
            issues_critical.append(f"Rule doc missing: {rule_file}")
            p(f"  MISSING: {rule_file}")
    if missing == 0:
        passes.append(f"Rules documentation: all {len(expected_rules)} canonical rule sets present")


# =========================================================
# AUDIT 11 — PROMPT GENERATOR & REACHABILITY END-TO-END
# =========================================================

def audit_prompt_generator():
    p("\n[AUDIT 11] Prompt Generator & Archetype Reachability")
    gen_script = SCRIPTS_DIR / "generate_section_prompt.py"
    if not gen_script.exists():
        issues_critical.append("generate_section_prompt.py not found")
        return

    sys.path.insert(0, str(SCRIPTS_DIR))
    import generate_section_prompt as g

    # 1. Reachability check across all dataset archetypes
    secs = g.load_json_dataset()
    all_ids = {a["archetype_id"] for s in secs for a in s["archetypes"]}
    src = gen_script.read_text(encoding="utf-8")
    picked = set(re.findall(r'pick\("([a-z0-9-]+)"\)', src))
    unreachable = sorted(all_ids - picked)
    if unreachable:
        issues_warning.append(f"generate_section_prompt.py unreachable archetypes ({len(unreachable)}): {unreachable}")
    else:
        passes.append(f"select_archetype(): 100% ({len(all_ids)}/{len(all_ids)}) archetypes reachable")

    # 2. Generate every page in page-templates.json and check warnings & contrast
    with open(DATA_DIR / "page-templates.json", encoding="utf-8") as f:
        pages = [pg["page_id"] for pg in json.load(f)["pages"]]

    gen_failures = []
    for pg in pages:
        prompt = g.generate_master_prompt({"page_id": pg, "project_name": f"Audit {pg}", "style": "Industrial Minimalist"})
        if g.fallback_warnings or "[WARN]" in prompt or "[ERROR]" in prompt:
            gen_failures.append(f"{pg}: {g.fallback_warnings}")
        # Verify derived token contrast in generated prompt
        m_bg = re.search(r"Surface Background:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
        m_card = re.search(r"Card Surface / Raised:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
        m_t1 = re.search(r"Text Primary:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
        m_t2 = re.search(r"Text Secondary:\*\* `(#[0-9A-Fa-f]{6})`", prompt)
        if not (m_bg and m_card and m_t1 and m_t2):
            gen_failures.append(f"{pg}: missing token line in output")
        else:
            bg, card, t1, t2 = m_bg.group(1), m_card.group(1), m_t1.group(1), m_t2.group(1)
            for label, fg, surf in [("t1/bg", t1, bg), ("t1/card", t1, card), ("t2/bg", t2, bg), ("t2/card", t2, card)]:
                cr = contrast_ratio(fg, surf)
                if cr < 4.5:
                    gen_failures.append(f"{pg}: {label} contrast {cr:.2f}:1 (< 4.5:1)")

    if gen_failures:
        for gf in gen_failures:
            issues_critical.append(f"Prompt generator failure: {gf}")
    else:
        passes.append(f"generate_section_prompt.py: all {len(pages)} pages generate with 0 warnings and WCAG AA tokens")
    p(f"  Pages tested: {len(pages)} | Unreachable archetypes: {len(unreachable)} | Failures: {len(gen_failures)}")


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
    audit_page_templates()
    audit_foreign_keys()
    audit_search_engine()
    audit_components()
    audit_anti_slop()
    audit_typography()
    audit_rules_docs()
    audit_prompt_generator()
    print_report()
    sys.exit(1 if issues_critical else 0)
