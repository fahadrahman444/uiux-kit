#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SlopGuard Static Audit Engine (v1.6.1)
Deterministic multi-line static scanner for React/TSX/JSX/CSS/HTML enforcing:
- Rule catalog (SLOP-*, TOKEN-*, PERF-*, A11Y-*)
- .designrc.json severity overrides with Blocker protection
- .design/audit-baseline.json time-boxed (90-day) waiver evaluation
- Weighted scoring: max(0, 100 - blockers*100 - majors*5 - minors*1)
- CI JSON output (audit-v1 schema) and Exit 0 / 1 / 2 precedence
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.6.1"
SCHEMA_URL = "https://schema.slopguard.dev/schemas/audit-v1.json"

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
        "title": "Missing accessible name / aria-label on interactive icon button.",
        "remediation": "Add aria-label='...' or <span className='sr-only'>...</span>.",
    },
    "A11Y-004": {
        "severity": "major",
        "detection": "static",
        "title": "Missing prefers-reduced-motion / motion-reduce safeguard.",
        "remediation": "Add motion-reduce:animate-none, @media (prefers-reduced-motion), or useReducedMotion().",
    },
    "A11Y-006": {
        "severity": "major",
        "detection": "static",
        "title": "outline-none without genuine focus-visible outline / forced-colors fallback.",
        "remediation": "Add focus-visible:outline-2 focus-visible:outline-offset-2 forced-colors:focus-visible:outline-[Highlight].",
    },
    "TOKEN-001": {
        "severity": "major",
        "detection": "static",
        "title": "Hardcoded hex/rgb color bypassing design tokens.",
        "remediation": "Replace raw hex with semantic token or Tailwind theme variable.",
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
    "SLOP-004": {
        "severity": "minor",
        "detection": "static",
        "title": "More than 1 screaming uppercase eyebrow label per view/component.",
        "remediation": "Limit uppercase eyebrows to at most 1 per screen and prefer sentence-case chips.",
    },
    "SLOP-006": {
        "severity": "minor",
        "detection": "static",
        "title": "Single-word italic/gradient headline accent.",
        "remediation": "Apply uniform typographic weight and solid high-contrast text color.",
    },
}

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", ".design", "__pycache__", ".venv", "venv"}
SCAN_EXTS = {".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".html", ".astro", ".vue", ".svelte"}
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")


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


def iter_source_files(root: Path):
    if root.is_file():
        if root.suffix.lower() in SCAN_EXTS:
            yield root
        return
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SCAN_EXTS:
            yield p


def strip_js_comments(text: str) -> str:
    # Replace line/block comments with spaces preserving line/column offsets
    def repl(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", repl, text)


def scan_file(filepath: Path, rel_path: str, severities: dict, waivers: set) -> list[dict]:
    raw = filepath.read_text(encoding="utf-8", errors="replace")
    ext = filepath.suffix.lower()
    is_token_file = any(k in filepath.name.lower() for k in ("tokens.", "tailwind.config"))
    is_ui_markup = ext in {".tsx", ".jsx", ".html", ".astro", ".vue", ".svelte"}
    text = strip_js_comments(raw) if ext in {".tsx", ".jsx", ".ts", ".js", ".css", ".scss"} else raw
    findings = []

    def add(rule_id: str, offset: int, msg: str):
        sev = severities.get(rule_id, "off")
        if sev == "off":
            return
        if (rule_id, rel_path) in waivers:
            return
        line, col = line_col(raw, offset)
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

    # 2. SLOP-002: Raw emojis inside interactive elements or JSX/HTML
    if is_ui_markup:
        for tag_m in re.finditer(r"<(button|a)\b[^>]*>([\s\S]*?)</\1>", text, re.I):
            em = EMOJI_RE.search(tag_m.group(0))
            if em:
                add("SLOP-002", tag_m.start() + em.start(), f"Raw emoji {em.group(0)!r} used inside <{tag_m.group(1)}>.")

    # 3. SLOP-004: >1 screaming uppercase eyebrow per view/component
    if is_ui_markup:
        up_matches = list(re.finditer(r"class(?:Name)?\s*=\s*[\"'`{][^\"'`}]*\buppercase\b", text))
        if len(up_matches) > 1:
            add("SLOP-004", up_matches[1].start(), f"Found {len(up_matches)} uppercase labels in component (max 1 per view).")

    # 4. SLOP-006: Single-word gradient/italic headline accent
    if is_ui_markup:
        for m in re.finditer(r"<h[1-3]\b[^>]*>[\s\S]*?(?:bg-clip-text\s+text-transparent|<(?:em|i)\b[^>]*>\s*[A-Za-z]+\s*</(?:em|i)>)", text):
            add("SLOP-006", m.start(), "Single-word italic or gradient text accent detected in headline.")

    # 5. TOKEN-001: Arbitrary hex utilities or raw hex outside token files
    if not is_token_file:
        for m in re.finditer(r"(?:bg|text|border|ring|outline|fill|stroke)-\[#[0-9a-fA-F]{3,8}\]", text):
            add("TOKEN-001", m.start(), f"Arbitrary hex utility '{m.group(0)}' bypasses semantic tokens.")
        if ext in {".css", ".scss"}:
            for m in re.finditer(r":[^;{}]*#[0-9a-fA-F]{3,8}\b", text):
                if "var(--" not in m.group(0):
                    add("TOKEN-001", m.start(), f"Hardcoded CSS hex color '{m.group(0).strip()}' bypasses tokens.")

    # 6. TOKEN-002: Off-grid arbitrary px spacing & rigid 100vh
    for m in re.finditer(r"\b(?:m|mt|mr|mb|ml|mx|my|p|pt|pr|pb|pl|px|py|gap)-\[(\d+)px\]", text):
        px = int(m.group(1))
        if px > 2 and px % 4 != 0:
            add("TOKEN-002", m.start(), f"Off-grid spacing '{m.group(0)}' ({px}px is not a multiple of 4px).")
    for m in re.finditer(r"\b(h-screen|min-h-screen|h-\[100vh\])\b", text):
        if "dvh" not in text[max(0, m.start() - 20):min(len(text), m.end() + 30)]:
            add("TOKEN-002", m.start(), f"Rigid '{m.group(1)}' viewport class may jump with mobile URL bar; prefer 100dvh.")

    # 7. PERF-001: Multi-line backdrop-blur + animated opacity / mousemove React state thrash
    for m in re.finditer(r"<(?:motion\.\w+|\w+)[^>]*backdrop-blur[^>]*>", text, re.S):
        tag_str = m.group(0)
        if re.search(r"\b(animate-fade|animate-pulse|opacity:\s*0|initial=\{\{[^}]*opacity|animate=\{\{[^}]*opacity)\b", tag_str):
            add("PERF-001", m.start(), "Animating opacity on a backdrop-blur element causes severe compositor/FPS lag.")
    for m in re.finditer(r"onMouseMove=\{[^}]*\bset[A-Z]\w*\(", text):
        add("PERF-001", m.start(), "React state update inside onMouseMove; offload coordinates to CSS custom properties.")

    # 8. PERF-002: Raw iframe without lazy/facade
    if is_ui_markup:
        for m in re.finditer(r"<iframe\b([^>]*)>", text, re.S | re.I):
            attrs = m.group(1)
            if "loading=" not in attrs and "facade" not in attrs.lower():
                add("PERF-002", m.start(), "Third-party <iframe> missing click-to-load facade or loading='lazy'.")

    # 9. PERF-003: <img> without dimensions / aspect reservation
    if is_ui_markup:
        for m in re.finditer(r"<img\b([^>]*)>", text, re.S | re.I):
            attrs = m.group(1)
            has_dims = ("width" in attrs and "height" in attrs) or "aspect-" in attrs or "fill" in attrs
            if not has_dims:
                add("PERF-003", m.start(), "<img> missing explicit width/height or aspect-* layout reservation.")

    # 10. A11Y-001: Sub-24px interactive targets
    if is_ui_markup:
        for m in re.finditer(r"<(button|a)\b([^>]*)>", text, re.S):
            attrs = m.group(2)
            has_min = bool(re.search(r"min-[hw]-\[(?:2[4-9]|[3-9]\d|\d{3,})px\]", attrs))
            if not has_min:
                tiny = re.search(r"\b(?:h-[1-5]|w-[1-5]|size-[1-5]|h-\[(?:[1-9]|1\d|2[0-3])px\]|w-\[(?:[1-9]|1\d|2[0-3])px\])\b", attrs)
                if tiny:
                    add("A11Y-001", m.start(), f"Interactive <{m.group(1)}> has sub-24px dimension '{tiny.group(0)}'.")

    # 11. A11Y-002: Multi-line icon-only buttons missing accessible name
    if is_ui_markup:
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

    # 12. A11Y-004: Motion without prefers-reduced-motion / useReducedMotion / motion-reduce
    if is_ui_markup:
        for m in re.finditer(r"\b(animate-pulse|animate-ping|animate-bounce)\b", text):
            window = text[max(0, m.start() - 80):min(len(text), m.end() + 80)]
            if "motion-reduce:" not in window:
                add("A11Y-004", m.start(), f"'{m.group(1)}' used without motion-reduce: safeguard.")
        if "<motion." in text and "useReducedMotion" not in text:
            m = re.search(r"<motion\.", text)
            add("A11Y-004", m.start(), "Framer Motion <motion.*> component does not check useReducedMotion().")
    elif ext in {".css", ".scss"} and "@keyframes" in text and "prefers-reduced-motion" not in text:
        m = re.search(r"@keyframes\b", text)
        add("A11Y-004", m.start(), "CSS @keyframes defined without @media (prefers-reduced-motion) override.")

    # 13. A11Y-006: outline-none without forced-colors outline fallback
    for m in re.finditer(r"\b(?:focus-visible:|focus:)?outline-none\b", text):
        window = text[max(0, m.start() - 40):min(len(text), m.end() + 220)]
        if "forced-colors:" not in window:
            add("A11Y-006", m.start(), f"'{m.group(0)}' strips focus outline without a forced-colors fallback.")

    return findings


def run_audit(target_path: Path, strict: bool = False) -> tuple[dict, int]:
    config_root = target_path if target_path.is_dir() else target_path.parent
    config = load_json_safe(config_root / ".designrc.json")
    if not config and Path.cwd() != config_root:
        config = load_json_safe(Path.cwd() / ".designrc.json")
    baseline = load_json_safe(config_root / ".design" / "audit-baseline.json")
    if not baseline and Path.cwd() != config_root:
        baseline = load_json_safe(Path.cwd() / ".design" / "audit-baseline.json")

    severities, overrides_log = resolve_rule_severities(config)
    waivers = load_active_waivers(baseline)

    results = []
    files_scanned = 0
    for fpath in iter_source_files(target_path):
        files_scanned += 1
        if target_path.is_file():
            rel = fpath.name
        else:
            try:
                rel = str(fpath.resolve().relative_to(target_path.resolve())).replace("\\", "/")
            except ValueError:
                rel = fpath.name
        results.extend(scan_file(fpath, rel, severities, waivers))

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
        "target": str(target_path.resolve()),
        "filesScanned": files_scanned,
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
        f"{c_bold}{c_cyan}SlopGuard Static Audit Engine (v{VERSION}){c_reset}",
        f"Target: {payload['target']} ({payload['filesScanned']} files scanned)",
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
    parser.add_argument("target", nargs="?", default=".", help="Path to audit")
    parser.add_argument("legacy_out", nargs="?", default=None, help="Optional legacy positional output path")
    parser.add_argument("--ci", action="store_true", help="CI mode (--format=json --no-color)")
    parser.add_argument("--strict", action="store_true", help="Promote Exit 1 warnings to Exit 2")
    parser.add_argument("--format", choices=["human", "json"], default="human", help="Output format")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--out", default=None, help="Write report output to file")
    args = parser.parse_args()

    fmt = "json" if args.ci else args.format
    use_color = False if (args.ci or args.no_color or not sys.stdout.isatty()) else True
    out_file = args.out or args.legacy_out

    payload, exit_code = run_audit(Path(args.target), strict=args.strict)
    output_text = json.dumps(payload, indent=2) if fmt == "json" else format_human(payload, use_color=use_color)

    if out_file:
        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        Path(out_file).write_text(output_text + "\n", encoding="utf-8")

    print(output_text)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
