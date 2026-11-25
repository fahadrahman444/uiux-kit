#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SlopGuard Static Audit Engine (v1.6.1)
Deterministic AST + multi-file CSS/token static scanner for React/TSX/JSX/CSS/HTML enforcing:
- Full 19-rule catalog (A11Y-001..008, TOKEN-001..002, PERF-001..003, SLOP-001..006)
- TypeScript compiler AST analysis (via scripts/ast_analyzer.mjs when Node + TS are available)
  with cross-file wrapper component resolution + Python fallback
- Multi-file CSS variable & class resolution across styles/tokens.css and project stylesheets
- .designrc.json severity overrides with Blocker protection
- .design/audit-baseline.json time-boxed (90-day) waiver evaluation
- Weighted scoring: max(0, 100 - blockers*100 - majors*5 - minors*1)
- CI JSON output (audit-v1 schema) and Exit 0 / 1 / 2 precedence
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.6.1"
SCHEMA_URL = "https://schema.slopguard.dev/schemas/audit-v1.json"
KIT_ROOT = Path(__file__).resolve().parent.parent
AST_SCRIPT = Path(__file__).resolve().parent / "ast_analyzer.mjs"

RULE_ALIASES = {
    "SLOP-007": "PERF-001",
}

RULES = {
    "A11Y-001": {
        "severity": "blocker",
        "detection": "static",
        "title": "Target size strictly < 24x24px (WCAG 2.5.8).",
        "remediation": "Use min-h-[44px] min-w-[44px] (minimum >= 24x24px).",
    },
    "A11Y-002": {
        "severity": "blocker",
        "detection": "static",
        "title": "Missing accessible name / aria-label on interactive element or wrapper.",
        "remediation": "Add aria-label='...' or <span className='sr-only'>...</span>.",
    },
    "A11Y-003": {
        "severity": "blocker",
        "detection": "static",
        "title": "Insufficient text contrast ratio against resolved background/surface token (< 4.5:1).",
        "remediation": "Use high-contrast semantic tokens (e.g. text-[var(--text-primary)] / text-slate-600+ on light surfaces).",
    },
    "A11Y-004": {
        "severity": "major",
        "detection": "static",
        "title": "Missing prefers-reduced-motion / motion-reduce safeguard.",
        "remediation": "Add motion-reduce:animate-none, @media (prefers-reduced-motion), or useReducedMotion().",
    },
    "A11Y-005": {
        "severity": "blocker",
        "detection": "static",
        "title": "Sticky/fixed bar without scroll-margin-top or anchor clearance (WCAG 2.4.11).",
        "remediation": "Add scroll-mt-20 (scroll-margin-top) to anchored sections and bottom clearance above fixed bars.",
    },
    "A11Y-006": {
        "severity": "major",
        "detection": "static",
        "title": "outline-none without genuine focus-visible outline / forced-colors fallback.",
        "remediation": "Add focus-visible:outline-2 focus-visible:outline-offset-2 forced-colors:focus-visible:outline-[Highlight].",
    },
    "A11Y-007": {
        "severity": "major",
        "detection": "static",
        "title": "Inconsistent help/support link ordering across routes (WCAG 3.2.6).",
        "remediation": "Keep help links (Contact, FAQ, Support, Help) in identical relative order across pages.",
    },
    "A11Y-008": {
        "severity": "major",
        "detection": "static",
        "title": "Multi-step form missing autocomplete / pre-fill persistence (WCAG 3.3.7).",
        "remediation": "Add autoComplete attributes or shared pre-fill defaults on multi-step form controls.",
    },
    "TOKEN-001": {
        "severity": "major",
        "detection": "static",
        "title": "Hardcoded hex/rgb color bypassing design tokens.",
        "remediation": "Replace raw hex with semantic token var(--...) or Tailwind theme variable.",
    },
    "TOKEN-002": {
        "severity": "minor",
        "detection": "static",
        "title": "Non-standard spacing value outside 4px/8px scale or rigid 100vh.",
        "remediation": "Use 4px/8px scale multiples or dynamic viewport units (100dvh).",
    },
    "PERF-001": {
        "severity": "blocker",
        "detection": "static",
        "title": "Uncontained backdrop-filter / animated opacity on backdrop-blur or mousemove state thrash.",
        "remediation": "Separate static backdrop-blur from animated opacity and keep cursor coords in CSS vars.",
    },
    "PERF-002": {
        "severity": "major",
        "detection": "static",
        "title": "Raw third-party iframe embed without click-to-load facade or lazy loading.",
        "remediation": "Wrap iframe in a click-to-load facade or add loading='lazy'.",
    },
    "PERF-003": {
        "severity": "major",
        "detection": "static",
        "title": "Image missing explicit width/height/aspect-ratio reservation.",
        "remediation": "Provide explicit width & height attributes or an aspect-* container.",
    },
    "SLOP-001": {
        "severity": "blocker",
        "detection": "static",
        "title": "Banned AI radial gradient / purple glow blob background detected.",
        "remediation": "Replace glowing blur blobs with solid surface tokens and hairline borders.",
    },
    "SLOP-002": {
        "severity": "blocker",
        "detection": "static",
        "title": "Emoji character used inside interactive UI primitive.",
        "remediation": "Replace emoji character with a crisp SVG vector icon (aria-hidden='true').",
    },
    "SLOP-003": {
        "severity": "major",
        "detection": "heuristic",
        "title": "Hardcoded vanity metric without audited telemetry / source citation.",
        "remediation": "Attach a verified footnote, sourceNote, dateRange, or citation element.",
    },
    "SLOP-004": {
        "severity": "minor",
        "detection": "static",
        "title": "More than 1 screaming uppercase eyebrow label per view/component.",
        "remediation": "Limit uppercase eyebrows to at most 1 per screen and prefer sentence-case chips.",
    },
    "SLOP-005": {
        "severity": "major",
        "detection": "heuristic",
        "title": "Unjustified identical 3-card grid without tier parity or bento asymmetry.",
        "remediation": "Use asymmetric colSpan bento items or reserve equal 3-column parity for pricing tiers.",
    },
    "SLOP-006": {
        "severity": "minor",
        "detection": "heuristic",
        "title": "Single-word italic/gradient headline accent.",
        "remediation": "Apply uniform typographic weight and solid high-contrast text color.",
    },
}

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", ".design", "__pycache__", ".venv", "venv"}
IGNORE_FILES = {"kit-bundle.js"}
SCAN_EXTS = {".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".html", ".astro", ".vue", ".svelte"}
JS_AST_EXTS = {".tsx", ".jsx", ".ts", ".js"}
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

# Common Tailwind palette hex values for static A11Y-003 contrast checking
TW_PALETTE = {
    "white": "#FFFFFF",
    "black": "#000000",
    "slate-50": "#F8FAFC",
    "slate-100": "#F1F5F9",
    "slate-200": "#E2E8F0",
    "slate-300": "#CBD5E1",
    "slate-400": "#94A3B8",
    "slate-500": "#64748B",
    "slate-600": "#475569",
    "slate-700": "#334155",
    "slate-800": "#1E293B",
    "slate-900": "#0F172A",
    "slate-950": "#020617",
    "gray-300": "#D1D5DB",
    "gray-400": "#9CA3AF",
    "gray-500": "#6B7280",
    "gray-600": "#4B5563",
    "gray-700": "#374151",
    "gray-900": "#111827",
    "zinc-400": "#A1A1AA",
    "zinc-500": "#71717A",
    "zinc-700": "#3F3F46",
    "zinc-900": "#18181B",
    "blue-400": "#60A5FA",
    "blue-500": "#3B82F6",
    "blue-600": "#2563EB",
    "blue-700": "#1D4ED8",
    "emerald-400": "#34D399",
    "emerald-600": "#059669",
    "emerald-700": "#047857",
    "rose-400": "#FB7185",
    "rose-600": "#E11D48",
    "rose-700": "#BE123C",
}


def _relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = _relative_luminance(c1), _relative_luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_nl = text.rfind("\n", 0, offset)
    col = offset - last_nl if last_nl != -1 else offset + 1
    return line, col


def load_json_safe(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def resolve_rule_severities(config: dict) -> tuple[dict, list]:
    effective = {rid: meta["severity"] for rid, meta in RULES.items()}
    overrides_log = []
    raw_rules = config.get("rules", {}) if isinstance(config, dict) else {}

    for raw_id, req in raw_rules.items():
        canonical = RULE_ALIASES.get(raw_id, raw_id)
        if canonical not in RULES:
            continue
        default_sev = RULES[canonical]["severity"]
        req_norm = str(req).lower().strip()
        if default_sev == "blocker":
            if req_norm in ("warn", "off", "minor", "major", "ignore"):
                overrides_log.append({
                    "ruleId": canonical,
                    "requested": req_norm,
                    "effective": "blocker",
                    "rejected": True,
                    "reason": "Rule is a Blocker; cannot be downgraded in .designrc.json. Requires .design/audit-baseline.json.",
                })
            else:
                overrides_log.append({
                    "ruleId": canonical,
                    "requested": req_norm,
                    "effective": "blocker",
                    "rejected": False,
                })
        else:
            if req_norm == "off":
                effective[canonical] = "off"
            elif req_norm == "warn":
                effective[canonical] = "minor"
            elif req_norm == "error":
                effective[canonical] = default_sev if default_sev == "major" else "major"
            elif req_norm in ("major", "minor", "blocker"):
                effective[canonical] = req_norm
            overrides_log.append({
                "ruleId": canonical,
                "requested": req_norm,
                "effective": effective[canonical],
                "rejected": False,
            })
    return effective, overrides_log


def load_active_waivers(baseline: dict) -> set[tuple[str, str]]:
    active = set()
    now = datetime.now(timezone.utc)
    for w in baseline.get("waivers", []) if isinstance(baseline, dict) else []:
        rid = RULE_ALIASES.get(w.get("ruleId", ""), w.get("ruleId", ""))
        rel_file = str(w.get("file", "")).replace("\\", "/").lstrip("./")
        expires_raw = w.get("expiresAt", "")
        if not rid or not rel_file:
            continue
        if expires_raw:
            try:
                exp = datetime.fromisoformat(expires_raw.replace("Z", "+00:00"))
                if exp < now:
                    continue
            except ValueError:
                continue
        active.add((rid, rel_file))
    return active


def iter_source_files(target_paths: list[Path]):
    seen = set()
    for root in target_paths:
        if root.is_file():
            rp = root.resolve()
            if rp not in seen and root.suffix.lower() in SCAN_EXTS:
                seen.add(rp)
                yield root
            continue
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            if p.name in IGNORE_FILES:
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            rp = p.resolve()
            if rp not in seen and p.suffix.lower() in SCAN_EXTS:
                seen.add(rp)
                yield p


def strip_js_comments(text: str) -> str:
    def repl(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", repl, text)


def _css_len_to_px(raw_val: str) -> float | None:
    m = re.match(r"^(\d+(?:\.\d+)?)(px|rem)$", raw_val.strip(), re.I)
    if not m:
        return None
    num = float(m.group(1))
    return num if m.group(2).lower() == "px" else num * 16.0


def _is_interactive_css_selector(selector_group: str) -> bool:
    interactive_re = re.compile(
        r"(?:^|[\s>+~])(?:a|button|\.[a-z0-9_-]*(?:link|btn|button|tab|slot|trigger|close|toggle)[a-z0-9_-]*)(?::[a-z-]+(?:\([^)]*\))?)*\s*$",
        re.I,
    )
    pseudo_or_child_re = re.compile(r"::(?:before|after|backdrop)|\b(?:svg|path|icon)\b", re.I)
    for sel in selector_group.split(","):
        s = sel.strip()
        if not s or pseudo_or_child_re.search(s):
            continue
        if interactive_re.search(s):
            return True
    return False


def _resolve_color_value(raw_val: str, css_vars: dict[str, str]) -> str | None:
    val = raw_val.strip()
    if HEX_RE.match(val):
        return val.upper()
    m_var = re.match(r"var\(\s*(--[a-zA-Z0-9_-]+)\s*(?:,\s*([^)]+))?\)", val)
    if m_var:
        var_name = m_var.group(1)
        if var_name in css_vars:
            return css_vars[var_name]
        if m_var.group(2):
            return _resolve_color_value(m_var.group(2), css_vars)
    return None


def build_style_context(files: list[Path], base_root: Path) -> dict:
    """Pre-index CSS variables and CSS class rules across all stylesheets (multi-file styles)."""
    css_vars: dict[str, str] = {}
    class_rules: dict[str, dict] = {}

    candidate_css = [p for p in files if p.suffix.lower() in {".css", ".scss"}]
    kit_tokens = KIT_ROOT / "styles" / "tokens.css"
    if kit_tokens.exists() and kit_tokens.resolve() not in {p.resolve() for p in candidate_css}:
        candidate_css.insert(0, kit_tokens)

    for css_path in candidate_css:
        raw = css_path.read_text(encoding="utf-8", errors="replace")
        text = strip_js_comments(raw)
        # Collect :root (light baseline) variables first
        for m in re.finditer(r":root\s*\{([^}]*)\}", text, re.S):
            for vm in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);", m.group(1)):
                val = vm.group(2).strip()
                if HEX_RE.match(val):
                    css_vars[vm.group(1)] = val.upper()
        # Any additional custom props not yet indexed
        for vm in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*(#[0-9A-Fa-f]{6})\b", text):
            css_vars.setdefault(vm.group(1), vm.group(2).upper())

        # Index class rules across stylesheets
        try:
            rel_css = str(css_path.resolve().relative_to(base_root.resolve())).replace("\\", "/")
        except ValueError:
            rel_css = css_path.name

        for bm in re.finditer(r"([^{}@;]+)\{([^{}]+)\}", text):
            sel_group, body = bm.group(1).strip(), bm.group(2)
            decls = {}
            for dm in re.finditer(r"([a-zA-Z-]+)\s*:\s*([^;]+)", body):
                decls[dm.group(1).strip().lower()] = dm.group(2).strip()
            if not decls:
                continue
            for sel in sel_group.split(","):
                s = sel.strip()
                cm = re.match(r"^\.([a-zA-Z0-9_-]+)$", s)
                if cm:
                    cname = cm.group(1)
                    entry = class_rules.setdefault(cname, {"file": rel_css, "decls": {}})
                    entry["decls"].update(decls)

    return {"css_vars": css_vars, "class_rules": class_rules}


def run_ast_analyzer(files: list[Path], base_root: Path) -> dict | None:
    """Run TypeScript compiler AST analyzer when Node and typescript are installed."""
    node_bin = shutil.which("node")
    if not node_bin or not AST_SCRIPT.exists():
        return None
    js_files = []
    for f in files:
        if f.suffix.lower() in JS_AST_EXTS:
            try:
                rel = str(f.resolve().relative_to(base_root.resolve())).replace("\\", "/")
            except ValueError:
                rel = f.name
            js_files.append({"absPath": str(f.resolve()), "relPath": rel})
    if not js_files:
        return {"wrappers": {}, "files": {}}

    try:
        proc = subprocess.run(
            [node_bin, str(AST_SCRIPT)],
            input=json.dumps({"files": js_files}),
            text=True,
            encoding="utf-8",
            capture_output=True,
            cwd=str(KIT_ROOT),
            timeout=30,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return json.loads(proc.stdout)
    except Exception:
        return None
    return None


def _check_tailwind_contrast(class_str: str) -> tuple[str, str, float] | None:
    """Check explicit static bg-<token> + text-<token> contrast pairs within same element."""
    if "dark:" in class_str:
        # Strip dark: tokens when checking light-mode default pairing
        light_tokens = [t for t in class_str.split() if not t.startswith("dark:") and not t.startswith("hover:")]
    else:
        light_tokens = [t for t in class_str.split() if not t.startswith("hover:")]
    bg_hex = None
    fg_hex = None
    bg_tok = ""
    fg_tok = ""
    for tok in light_tokens:
        if tok.startswith("bg-") and tok[3:] in TW_PALETTE:
            bg_hex = TW_PALETTE[tok[3:]]
            bg_tok = tok
        elif tok.startswith("text-") and tok[5:] in TW_PALETTE:
            fg_hex = TW_PALETTE[tok[5:]]
            fg_tok = tok
    if bg_hex and fg_hex:
        cr = contrast_ratio(fg_hex, bg_hex)
        if cr < 4.5:
            return bg_tok, fg_tok, cr
    return None


def scan_file(
    filepath: Path,
    rel_path: str,
    severities: dict,
    waivers: set,
    style_ctx: dict,
    ast_file: dict | None,
    ast_wrappers: dict,
) -> list[dict]:
    raw = filepath.read_text(encoding="utf-8", errors="replace")
    ext = filepath.suffix.lower()
    is_token_file = any(k in filepath.name.lower() for k in ("tokens.", "tailwind.config"))
    is_ui_markup = ext in {".tsx", ".jsx", ".html", ".astro", ".vue", ".svelte"}
    text = strip_js_comments(raw) if ext in {".tsx", ".jsx", ".ts", ".js", ".css", ".scss"} else raw
    css_vars = style_ctx["css_vars"]
    class_rules = style_ctx["class_rules"]
    findings = []

    def add(rule_id: str, offset: int | None, msg: str, line_col_override: tuple[int, int] | None = None):
        sev = severities.get(rule_id, "off")
        if sev == "off":
            return
        if (rule_id, rel_path) in waivers:
            return
        if line_col_override:
            line, col = line_col_override
        else:
            line, col = line_col(raw, offset or 0)
        findings.append({
            "ruleId": rule_id,
            "severity": sev,
            "detection": RULES[rule_id]["detection"],
            "file": rel_path,
            "line": line,
            "column": col,
            "message": msg,
            "remediation": RULES[rule_id]["remediation"],
        })

    # 1. SLOP-001: AI dark-mode purple/indigo radial blur blobs
    for m in re.finditer(r"radial-gradient\([^)]*(?:#6366f1|#8b5cf6|indigo|purple|violet|hsl\(2[5-8]\d)", text, re.I):
        window = text[max(0, m.start() - 120):min(len(text), m.end() + 120)]
        if "blur" in window.lower():
            add("SLOP-001", m.start(), "Blurred purple/indigo radial-gradient blob detected.")
    for m in re.finditer(r"class(?:Name)?\s*=\s*[\"'`{][^\"'`}]*\b(?:bg-(?:purple|indigo|violet)-[4-9]00|from-(?:purple|indigo)-[4-9]00)[^\"'`}]*\bblur-(?:xl|2xl|3xl|\[)", text):
        add("SLOP-001", m.start(), "Blurred purple/indigo glow blob utility detected.")

    # 2. SLOP-002: Raw emojis inside interactive UI primitives (AST-preferred)
    if ast_file is not None:
        for el in ast_file["jsxElements"]:
            if el["isInteractive"] and el["children"].get("hasEmojiInChildren"):
                em = el["children"]["hasEmojiInChildren"]
                add("SLOP-002", None, f"Raw emoji {em!r} used inside <{el['tag']}>.", (el["line"], el["column"]))
    elif is_ui_markup:
        for tag_m in re.finditer(r"<(button|a)\b[^>]*>([\s\S]*?)</\1>", text, re.I):
            em = EMOJI_RE.search(tag_m.group(0))
            if em:
                add("SLOP-002", tag_m.start() + em.start(), f"Raw emoji {em.group(0)!r} used inside <{tag_m.group(1)}>.")

    # 3. SLOP-003: Unverified vanity metrics without footnote / telemetry source
    if ast_file is not None and not ast_file.get("hasVerificationCitation"):
        if ast_file.get("metricTokens"):
            first_m = ast_file["metricTokens"][0]
            add(
                "SLOP-003",
                None,
                f"Metric {first_m['value']!r} displayed without audited source/footnote/dateRange citation.",
                (first_m["line"], first_m["column"]),
            )
    elif is_ui_markup and not re.search(r"\b(footnote|sourceNote|source|verified|citation|audit|dateRange|cite|figcaption)\b", text, re.I):
        vm = re.search(r">\s*(\+?\d+(?:\.\d+)?%|\d+x)\s*<", text)
        if vm:
            add("SLOP-003", vm.start(), f"Metric {vm.group(1)!r} displayed without audited source or footnote citation.")

    # 4. SLOP-004: >1 screaming uppercase eyebrow per view/component
    if ast_file is not None:
        up_els = [el for el in ast_file["jsxElements"] if re.search(r"\buppercase\b", el.get("className", ""))]
        if len(up_els) > 1:
            add(
                "SLOP-004",
                None,
                f"Found {len(up_els)} uppercase labels in component (max 1 per view).",
                (up_els[1]["line"], up_els[1]["column"]),
            )
    elif is_ui_markup:
        up_matches = list(re.finditer(r"class(?:Name)?\s*=\s*[\"'`{][^\"'`}]*\buppercase\b", text))
        if len(up_matches) > 1:
            add("SLOP-004", up_matches[1].start(), f"Found {len(up_matches)} uppercase labels in component (max 1 per view).")

    # 5. SLOP-005: Unjustified identical 3-column symmetric card grid
    if ast_file is not None and not ast_file.get("hasPricingContext"):
        for el in ast_file["jsxElements"]:
            cn = el.get("className", "")
            if re.search(r"\b(?:lg:)?grid-cols-3\b", cn) and "colSpan" not in raw:
                add(
                    "SLOP-005",
                    None,
                    "Identical 3-column symmetric grid without pricing tier parity or bento colSpan asymmetry.",
                    (el["line"], el["column"]),
                )
    elif is_ui_markup and not re.search(r"\b(pricing|tier|plan|popular|billing|colSpan|bento|chart)\b", text, re.I):
        gm = re.search(r"class(?:Name)?\s*=\s*[\"'`{][^\"'`}]*\b(?:lg:)?grid-cols-3\b", text)
        if gm:
            add("SLOP-005", gm.start(), "Identical 3-column symmetric grid without pricing tier parity or bento colSpan asymmetry.")

    # 6. SLOP-006: Single-word gradient/italic headline accent
    if is_ui_markup:
        for m in re.finditer(r"<h[1-3]\b[^>]*>[\s\S]*?(?:bg-clip-text\s+text-transparent|<(?:em|i)\b[^>]*>\s*[A-Za-z]+\s*</(?:em|i)>)", text):
            add("SLOP-006", m.start(), "Single-word italic or gradient text accent detected in headline.")

    # 7. TOKEN-001: Arbitrary hex utilities or raw hex outside token files
    if not is_token_file:
        for m in re.finditer(r"(?:bg|text|border|ring|outline|fill|stroke)-\[#[0-9a-fA-F]{3,8}\]", text):
            add("TOKEN-001", m.start(), f"Arbitrary hex utility '{m.group(0)}' bypasses semantic tokens.")
        if ext in {".css", ".scss"}:
            for m in re.finditer(r"([a-zA-Z_-][a-zA-Z0-9_-]*)\s*:\s*([^;{}]*#[0-9a-fA-F]{3,8}\b[^;{}]*)", text):
                prop, val = m.group(1), m.group(2)
                if prop.startswith("--") or "var(--" in val:
                    continue
                add("TOKEN-001", m.start(), f"Hardcoded CSS hex color '{prop}: {val.strip()}' bypasses tokens.")
        if is_ui_markup:
            for m in re.finditer(r"<(?:svg|path|circle|rect|line|polygon|polyline|ellipse)\b[^>]*\b(?:fill|stroke)=[\"'](#[0-9a-fA-F]{3,8})[\"']", text, re.I):
                add("TOKEN-001", m.start(), f"Hardcoded inline SVG hex '{m.group(1)}' bypasses semantic tokens (use currentColor or var(--...)).")
            for m in re.finditer(r"style=\{\{[^}]*?(?:color|backgroundColor|borderColor)\s*:\s*[\"'](#[0-9a-fA-F]{3,8})[\"']", text):
                add("TOKEN-001", m.start(), f"Hardcoded inline style hex '{m.group(1)}' bypasses semantic tokens.")

    # 8. TOKEN-002: Off-grid arbitrary px spacing & rigid 100vh
    for m in re.finditer(r"\b(?:m|mr|ml|mt|mb|mx|my|p|pt|pr|pb|pl|px|py|gap)-\[(\d+)px\]", text):
        px = int(m.group(1))
        if px > 2 and px % 4 != 0:
            add("TOKEN-002", m.start(), f"Off-grid spacing '{m.group(0)}' ({px}px is not a multiple of 4px).")
    for m in re.finditer(r"\b(h-screen|min-h-screen|h-\[100vh\])\b", text):
        if "dvh" not in text[max(0, m.start() - 20):min(len(text), m.end() + 30)]:
            add("TOKEN-002", m.start(), f"Rigid '{m.group(1)}' viewport class may jump with mobile URL bar; prefer 100dvh.")

    # 9. PERF-001: backdrop-blur + animated opacity / CSS ::backdrop blur / mousemove React state thrash
    for m in re.finditer(r"<(?:motion\.\w+|\w+)[^>]*backdrop-blur[^>]*>", text, re.S):
        tag_str = m.group(0)
        if re.search(r"\b(animate-fade|animate-pulse|opacity:\s*0|initial=\{\{[^}]*opacity|animate=\{\{[^}]*opacity)\b", tag_str):
            add("PERF-001", m.start(), "Animating opacity on a backdrop-blur element causes severe compositor/FPS lag.")
    if ext in {".css", ".scss"}:
        for m in re.finditer(r"([^{};]+)::backdrop\s*\{([^}]*)\}", text):
            sel_base = m.group(1).strip().split(",")[-1].strip()
            body = m.group(2)
            blur_m = re.search(r"(?:-webkit-)?backdrop-filter\s*:\s*[^;]*blur\(", body, re.I)
            if blur_m and sel_base:
                anim_pat = rf"(?:^|[}}\s;]){re.escape(sel_base)}(?:\[open\])?\s*\{{[^}}]*\b(?:transition|animation)\b[^;}}]*\bopacity\b"
                if re.search(anim_pat, text, re.S):
                    add("PERF-001", m.start(2) + blur_m.start(), f"'{sel_base}::backdrop' applies backdrop-filter blur while '{sel_base}' animates opacity.")
    if ast_file is not None:
        for mm in ast_file["mouseMoveStateUpdates"]:
            add("PERF-001", None, "React state update inside onMouseMove; offload coordinates to CSS custom properties.", (mm["line"], mm["column"]))
    else:
        for m in re.finditer(r"onMouseMove=\{[^}]*\bset[A-Z]\w*\(", text):
            add("PERF-001", m.start(), "React state update inside onMouseMove; offload coordinates to CSS custom properties.")

    # 10. PERF-002 & PERF-003: iframe and img checks (AST-backed when available)
    if ast_file is not None:
        for el in ast_file["jsxElements"]:
            if el["tag"] == "iframe":
                attrs = el["attrs"]
                if "loading" not in attrs and "facade" not in el.get("className", "").lower():
                    add("PERF-002", None, "Third-party <iframe> missing click-to-load facade or loading='lazy'.", (el["line"], el["column"]))
            elif el["tag"] == "img":
                attrs = el["attrs"]
                has_dims = ("width" in attrs and "height" in attrs) or ("aspect-" in el.get("className", "")) or ("fill" in attrs)
                if not has_dims:
                    add("PERF-003", None, "<img> missing explicit width/height or aspect-* layout reservation.", (el["line"], el["column"]))
    elif is_ui_markup:
        for m in re.finditer(r"<iframe\b([^>]*)>", text, re.S | re.I):
            attrs = m.group(1)
            if "loading=" not in attrs and "facade" not in attrs.lower():
                add("PERF-002", m.start(), "Third-party <iframe> missing click-to-load facade or loading='lazy'.")
        for m in re.finditer(r"<img\b([^>]*)>", text, re.S | re.I):
            attrs = m.group(1)
            has_dims = ("width" in attrs and "height" in attrs) or "aspect-" in attrs or "fill" in attrs
            if not has_dims:
                add("PERF-003", m.start(), "<img> missing explicit width/height or aspect-* layout reservation.")

    # 11. A11Y-001: Sub-24px interactive targets (AST + wrapper + multi-file CSS classes)
    if ast_file is not None:
        for el in ast_file["jsxElements"]:
            if not el["isInteractive"]:
                continue
            cn = el.get("className", "")
            has_min = bool(re.search(r"min-[hw]-\[(?:2[4-9]|[3-9]\d|\d{3,})px\]", cn))
            if not has_min:
                tiny = re.search(r"\b(?:h-[1-5]|w-[1-5]|size-[1-5]|h-\[(?:[1-9]|1\d|2[0-3])px\]|w-\[(?:[1-9]|1\d|2[0-3])px\])\b", cn)
                if tiny:
                    add("A11Y-001", None, f"Interactive <{el['tag']}> has sub-24px dimension '{tiny.group(0)}'.", (el["line"], el["column"]))
                    continue
            # Check multi-file CSS class definitions referenced on this interactive element
            for tok in cn.split():
                if tok in class_rules:
                    decls = class_rules[tok]["decls"]
                    has_css_min = any(
                        p.startswith("min-") and (_css_len_to_px(decls[p]) or 0) >= 24.0
                        for p in decls
                    )
                    if not has_css_min:
                        for prop in ("height", "block-size", "width", "inline-size", "min-height", "min-width"):
                            if prop in decls:
                                px_v = _css_len_to_px(decls[prop])
                                if px_v is not None and 0 < px_v < 24.0:
                                    add(
                                        "A11Y-001",
                                        None,
                                        f"Interactive <{el['tag']}> uses CSS class '.{tok}' ({class_rules[tok]['file']}) with {prop}: {decls[prop]} (< 24px).",
                                        (el["line"], el["column"]),
                                    )
                                    break
    elif is_ui_markup:
        for m in re.finditer(r"<(button|a)\b([^>]*)>", text, re.S):
            attrs = m.group(2)
            has_min = bool(re.search(r"min-[hw]-\[(?:2[4-9]|[3-9]\d|\d{3,})px\]", attrs))
            if not has_min:
                tiny = re.search(r"\b(?:h-[1-5]|w-[1-5]|size-[1-5]|h-\[(?:[1-9]|1\d|2[0-3])px\]|w-\[(?:[1-9]|1\d|2[0-3])px\])\b", attrs)
                if tiny:
                    add("A11Y-001", m.start(), f"Interactive <{m.group(1)}> has sub-24px dimension '{tiny.group(0)}'.")
    elif ext in {".css", ".scss"}:
        for m in re.finditer(r"([^{}@;]+)\{([^{}]+)\}", text):
            sel, body = m.group(1).strip(), m.group(2)
            if not _is_interactive_css_selector(sel):
                continue
            decls = re.findall(r"\b(min-block-size|min-height|block-size|height|min-inline-size|min-width|inline-size|width)\s*:\s*([^;]+)", body, re.I)
            if not decls:
                continue
            has_min_ok = any(
                prop.lower().startswith("min-") and (_css_len_to_px(val) or 0) >= 24.0
                for prop, val in decls
            )
            if has_min_ok:
                continue
            for prop, val in decls:
                px_val = _css_len_to_px(val)
                if px_val is not None and 0 < px_val < 24.0:
                    add("A11Y-001", m.start(), f"Interactive CSS rule '{sel}' sets '{prop}: {val.strip()}' (< 24px WCAG 2.5.8 minimum).")
                    break

    # 12. A11Y-002: Missing accessible name on icon-only native buttons OR custom button wrappers
    if ast_file is not None:
        for el in ast_file["jsxElements"]:
            tag = el["tag"]
            attrs = el["attrs"]
            children = el["children"]
            if tag == "button":
                has_label = (
                    any(k in attrs for k in ("aria-label", "aria-labelledby", "title"))
                    or children.get("hasSrOnly")
                    or el["hasSpread"]
                )
                txt = children.get("text", "")
                is_icon_only = children.get("hasSvg") and not txt and not children.get("hasDynamicChild") and not children.get("hasNonSvgChildElement")
                is_glyph_only = txt in {"✕", "×", "▼", "▲", "→", "←", "+", "-", "..."}
                if (is_icon_only or is_glyph_only) and not has_label:
                    add("A11Y-002", None, "Icon-only <button> lacks aria-label, aria-labelledby, or .sr-only label.", (el["line"], el["column"]))
            elif el["isWrapper"] and (el["wrapperMeta"] or {}).get("kind") == "button":
                meta = el["wrapperMeta"]
                if meta.get("hasFixedLabel"):
                    continue
                has_label = (
                    any(k in attrs for k in ("aria-label", "aria-labelledby", "title", "label", "cta"))
                    or children.get("hasSrOnly")
                    or bool(children.get("text"))
                    or children.get("hasDynamicChild")
                    or children.get("hasNonSvgChildElement")
                )
                if not has_label:
                    add("A11Y-002", None, f"Interactive wrapper <{tag}> renders <button> without accessible label or text children.", (el["line"], el["column"]))
    elif is_ui_markup:
        for m in re.finditer(r"<([A-Za-z]*[Bb]utton)\b([^>]*)>([\s\S]*?)</\1>", text):
            tag_name, attrs, body = m.group(1), m.group(2), m.group(3)
            if tag_name.lower() != "button":
                continue
            has_label = bool(re.search(r"\b(aria-label|aria-labelledby|title)\s*=", attrs)) or "sr-only" in body
            stripped_body = re.sub(r"<svg\b[\s\S]*?</svg>", "", body, flags=re.I)
            stripped_body = re.sub(r"<[^>]+>", "", stripped_body)
            stripped_body = re.sub(r"\{[^}]+\}", "text", stripped_body).strip()
            is_icon_only = bool(re.search(r"<svg\b", body, re.I)) and not stripped_body
            is_glyph_only = stripped_body in {"✕", "×", "▼", "▲", "→", "←", "+", "-", "..."}
            if (is_icon_only or is_glyph_only) and not has_label:
                add("A11Y-002", m.start(), "Icon-only <button> lacks aria-label, aria-labelledby, or .sr-only label.")

    # 13. A11Y-003: Static contrast check across Tailwind pairs & resolved multi-file CSS rules
    if ast_file is not None:
        for el in ast_file["jsxElements"]:
            cn = el.get("className", "")
            tw_fail = _check_tailwind_contrast(cn)
            if tw_fail:
                bg_tok, fg_tok, cr = tw_fail
                add(
                    "A11Y-003",
                    None,
                    f"Low contrast utility pair '{fg_tok}' on '{bg_tok}' ({cr:.2f}:1 < 4.5:1).",
                    (el["line"], el["column"]),
                )
            for tok in cn.split():
                if tok in class_rules:
                    decls = class_rules[tok]["decls"]
                    fg = _resolve_color_value(decls.get("color", ""), css_vars)
                    bg = _resolve_color_value(decls.get("background-color", decls.get("background", "")), css_vars)
                    if fg and bg:
                        cr = contrast_ratio(fg, bg)
                        if cr < 4.5:
                            add(
                                "A11Y-003",
                                None,
                                f"CSS class '.{tok}' resolves to low contrast {fg} on {bg} ({cr:.2f}:1 < 4.5:1).",
                                (el["line"], el["column"]),
                            )
    if ext in {".css", ".scss"}:
        for bm in re.finditer(r"([^{}@;]+)\{([^{}]+)\}", text):
            sel, body = bm.group(1).strip(), bm.group(2)
            decls = {dm.group(1).strip().lower(): dm.group(2).strip() for dm in re.finditer(r"([a-zA-Z-]+)\s*:\s*([^;]+)", body)}
            fg = _resolve_color_value(decls.get("color", ""), css_vars)
            bg = _resolve_color_value(decls.get("background-color", decls.get("background", "")), css_vars)
            if fg and bg:
                cr = contrast_ratio(fg, bg)
                if cr < 4.5:
                    add("A11Y-003", bm.start(), f"CSS rule '{sel}' has contrast {cr:.2f}:1 ({fg} on {bg} < 4.5:1).")

    # 14. A11Y-004: Motion without prefers-reduced-motion / useReducedMotion / motion-reduce
    if is_ui_markup:
        for m in re.finditer(r"\b(animate-pulse|animate-ping|animate-bounce)\b", text):
            window = text[max(0, m.start() - 80):min(len(text), m.end() + 80)]
            if "motion-reduce:" not in window:
                add("A11Y-004", m.start(), f"'{m.group(1)}' used without motion-reduce: safeguard.")
        has_motion = (
            any(el["tag"].startswith("motion.") for el in ast_file["jsxElements"])
            if ast_file is not None
            else "<motion." in text
        )
        has_rm = ast_file["usesReducedMotionHook"] if ast_file is not None else "useReducedMotion" in text
        if has_motion and not has_rm:
            m = re.search(r"<motion\.", text)
            add("A11Y-004", m.start() if m else 0, "Framer Motion <motion.*> component does not check useReducedMotion().")
    elif ext in {".css", ".scss"} and "@keyframes" in text and "prefers-reduced-motion" not in text:
        m = re.search(r"@keyframes\b", text)
        add("A11Y-004", m.start(), "CSS @keyframes defined without @media (prefers-reduced-motion) override.")

    # 15. A11Y-005: Sticky/fixed headers paired with unpadded anchored sections
    if ast_file is not None:
        if ast_file.get("hasStickyBar") and ast_file.get("hasAnchorSection") and not ast_file.get("hasScrollMarginClass"):
            add("A11Y-005", 0, "Sticky/fixed header paired with anchored section missing scroll-mt-* (WCAG 2.4.11).")

    # 16. A11Y-006: outline-none without forced-colors outline fallback
    for m in re.finditer(r"\b(?:focus-visible:|focus:)?outline-none\b", text):
        window = text[max(0, m.start() - 40):min(len(text), m.end() + 220)]
        if "forced-colors:" not in window:
            line_slice = text[max(0, m.start() - 80):m.end() + 40]
            if "<main" in line_slice and "tabIndex={-1}" in line_slice:
                continue
            add("A11Y-006", m.start(), f"'{m.group(0)}' strips focus outline without a forced-colors fallback.")

    # 17. A11Y-008: Multi-step form missing autocomplete / pre-fill
    if ast_file is not None:
        if ast_file.get("hasMultiStepHint") and ast_file.get("hasFormElement") and not ast_file.get("hasAutocompleteInput"):
            add("A11Y-008", 0, "Multi-step form lacks autoComplete attributes for redundant-entry prevention (WCAG 3.3.7).")

    return findings


def run_cross_file_checks(ast_data: dict | None, severities: dict, waivers: set) -> list[dict]:
    """Run A11Y-007 consistent help mechanism order check across multi-page files."""
    if not ast_data:
        return []
    findings = []
    help_sequences: list[tuple[str, list[str]]] = []
    for rel_path, fdata in sorted(ast_data.get("files", {}).items()):
        seq = fdata.get("helpLinks", [])
        if len(seq) >= 2:
            help_sequences.append((rel_path, seq))

    if len(help_sequences) >= 2 and severities.get("A11Y-007", "off") != "off":
        baseline_file, baseline_seq = help_sequences[0]
        for rel_path, seq in help_sequences[1:]:
            if seq != baseline_seq and ("A11Y-007", rel_path) not in waivers:
                findings.append({
                    "ruleId": "A11Y-007",
                    "severity": severities["A11Y-007"],
                    "detection": RULES["A11Y-007"]["detection"],
                    "file": rel_path,
                    "line": 1,
                    "column": 1,
                    "message": f"Help link order {seq} diverges from {baseline_file} {baseline_seq} (WCAG 3.2.6).",
                    "remediation": RULES["A11Y-007"]["remediation"],
                })
    return findings


def run_audit(targets: list[Path], strict: bool = False) -> tuple[dict, int]:
    primary_root = targets[0] if targets else Path(".")
    config_root = primary_root if primary_root.is_dir() else primary_root.parent
    config = load_json_safe(config_root / ".designrc.json")
    if not config and Path.cwd() != config_root:
        config = load_json_safe(Path.cwd() / ".designrc.json")
    baseline = load_json_safe(config_root / ".design" / "audit-baseline.json")
    if not baseline and Path.cwd() != config_root:
        baseline = load_json_safe(Path.cwd() / ".design" / "audit-baseline.json")

    severities, overrides_log = resolve_rule_severities(config)
    waivers = load_active_waivers(baseline)

    all_files = list(iter_source_files(targets))
    if len(targets) == 1:
        common_root = config_root
    else:
        try:
            common_root = Path(os.path.commonpath([str((t if t.is_dir() else t.parent).resolve()) for t in targets]))
        except ValueError:
            common_root = Path.cwd()
    style_ctx = build_style_context(all_files, common_root)
    ast_data = run_ast_analyzer(all_files, common_root)
    ast_files = ast_data.get("files", {}) if ast_data else {}
    ast_wrappers = ast_data.get("wrappers", {}) if ast_data else {}

    results = []
    for fpath in all_files:
        if len(targets) == 1 and targets[0].is_file():
            rel = fpath.name
        else:
            try:
                rel = str(fpath.resolve().relative_to(common_root.resolve())).replace("\\", "/")
            except ValueError:
                rel = fpath.name
        results.extend(
            scan_file(
                fpath,
                rel,
                severities,
                waivers,
                style_ctx,
                ast_files.get(rel),
                ast_wrappers,
            )
        )

    results.extend(run_cross_file_checks(ast_data, severities, waivers))

    blockers = sum(1 for r in results if r["severity"] == "blocker")
    majors = sum(1 for r in results if r["severity"] == "major")
    minors = sum(1 for r in results if r["severity"] == "minor")
    score = max(0, 100 - (blockers * 100) - (majors * 5) - (minors * 1))

    if blockers > 0 or score < 85:
        exit_code = 2
    elif majors > 0:
        exit_code = 2 if strict else 1
    else:
        exit_code = 0

    payload = {
        "$schema": SCHEMA_URL,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target": ", ".join(str(t.resolve()) for t in targets),
        "analyzerMode": "typescript-ast+multifile-css" if ast_data is not None else "regex-fallback+multifile-css",
        "rulesEnabled": len(RULES),
        "filesScanned": len(all_files),
        "summary": {
            "blockers": blockers,
            "majors": majors,
            "minors": minors,
            "score": score,
            "exitCode": exit_code,
        },
        "configOverrides": overrides_log,
        "results": results,
    }
    return payload, exit_code


def format_human(payload: dict, use_color: bool = True) -> str:
    c_cyan = "\033[0;36m" if use_color else ""
    c_green = "\033[0;32m" if use_color else ""
    c_red = "\033[0;31m" if use_color else ""
    c_yellow = "\033[0;33m" if use_color else ""
    c_bold = "\033[1m" if use_color else ""
    c_reset = "\033[0m" if use_color else ""

    s = payload["summary"]
    lines = [
        f"{c_bold}{c_cyan}SlopGuard Static Audit Engine (v{VERSION} | {payload['analyzerMode']}){c_reset}",
        f"Target: {payload['target']} ({payload['filesScanned']} files scanned | {payload['rulesEnabled']} rules)",
        "-" * 60,
    ]
    if not payload["results"]:
        lines.append(f"{c_green}PASS: 0 violations found.{c_reset}")
    else:
        for r in payload["results"]:
            sev = r["severity"].upper()
            col = c_red if sev == "BLOCKER" else c_yellow
            lines.append(f"{col}[{sev}] {r['ruleId']}{c_reset} {r['file']}:{r['line']}:{r['column']} — {r['message']}")
    lines.append("-" * 60)
    verdict_col = c_green if s["exitCode"] == 0 else (c_yellow if s["exitCode"] == 1 else c_red)
    lines.append(
        f"Score: {verdict_col}{s['score']}/100{c_reset} | "
        f"Blockers: {s['blockers']} | Majors: {s['majors']} | Minors: {s['minors']} | "
        f"Exit: {s['exitCode']}"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SlopGuard Static Audit Engine")
    parser.add_argument("targets", nargs="*", default=["."], help="Paths to audit")
    parser.add_argument("--ci", action="store_true", help="CI mode (--format=json --no-color)")
    parser.add_argument("--strict", action="store_true", help="Promote Exit 1 warnings to Exit 2")
    parser.add_argument("--format", choices=["human", "json"], default="human", help="Output format")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--out", default=None, help="Write report output to file")
    args = parser.parse_args()

    fmt = "json" if args.ci else args.format
    use_color = False if (args.ci or args.no_color or not sys.stdout.isatty()) else True
    target_paths = [Path(t) for t in (args.targets or ["."])]

    payload, exit_code = run_audit(target_paths, strict=args.strict)
    output_text = json.dumps(payload, indent=2) if fmt == "json" else format_human(payload, use_color=use_color)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output_text + "\n", encoding="utf-8")

    print(output_text)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
