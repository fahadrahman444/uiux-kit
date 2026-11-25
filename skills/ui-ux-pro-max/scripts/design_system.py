#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Design System Generator - Aggregates search results and applies reasoning
to generate comprehensive design system recommendations.

Usage:
    from design_system import generate_design_system
    result = generate_design_system("SaaS dashboard", "My Project")
"""

import csv
import json
import re
import html
from pathlib import Path
from core import search, DATA_DIR, _load_csv


# ============ CONFIGURATION ============
REASONING_FILE = "ui-reasoning.csv"

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "landing": {"max_results": 2},
    "typography": {"max_results": 2}
}


# ============ DESIGN SYSTEM GENERATOR ============
class DesignSystemGenerator:
    """Generates design system recommendations from aggregated searches."""

    def __init__(self):
        self.reasoning_data = self._load_reasoning()

    def _load_reasoning(self) -> list:
        """Load reasoning rules from CSV."""
        filepath = DATA_DIR / REASONING_FILE
        if not filepath.exists():
            return []
        return _load_csv(filepath)

    def _multi_domain_search(self, query: str, style_priority: list = None) -> dict:
        """Execute searches across multiple domains."""
        results = {}
        for domain, config in SEARCH_CONFIG.items():
            if domain == "product":
                continue
            if domain == "style" and style_priority:
                # For style, also search with priority keywords
                priority_query = " ".join(style_priority[:2]) if style_priority else query
                combined_query = f"{query} {priority_query}"
                results[domain] = search(combined_query, domain, config["max_results"])
            else:
                results[domain] = search(query, domain, config["max_results"])
        return results

    def _find_reasoning_rule(self, category: str) -> dict:
        """Find matching reasoning rule for a category using word boundaries."""
        category_lower = category.lower().strip()
        if not category_lower or category_lower == "general":
            return {}

        # Try exact match first
        for rule in self.reasoning_data:
            if rule.get("UI_Category", "").lower().strip() == category_lower:
                return rule

        # Try phrase match on word boundaries
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower().strip()
            if ui_cat and re.search(rf"(?<![a-z0-9]){re.escape(ui_cat)}(?![a-z0-9])", category_lower):
                return rule

        # Try meaningful token overlap (avoid generic words and short fragments like 'e' or 'app')
        generic = {"app", "tool", "platform", "service", "services", "system", "hub", "portal", "web", "page", "store", "shop", "client"}
        cat_tokens = set(re.findall(r"[a-z0-9]{3,}", category_lower)) - generic
        best_rule = {}
        best_hits = 0
        for rule in self.reasoning_data:
            ui_cat = rule.get("UI_Category", "").lower()
            rule_tokens = set(re.findall(r"[a-z0-9]{3,}", ui_cat)) - generic
            hits = len(cat_tokens & rule_tokens)
            if hits > best_hits:
                best_hits = hits
                best_rule = rule

        return best_rule

    def _apply_reasoning(self, category: str, search_results: dict) -> dict:
        """Apply reasoning rules to search results."""
        rule = self._find_reasoning_rule(category)

        if not rule:
            return {
                "pattern": "Hero + Features + CTA",
                "style_priority": ["Minimalism", "Flat Design"],
                "color_mood": "Professional",
                "typography_mood": "Clean",
                "key_effects": "Subtle hover transitions",
                "anti_patterns": "",
                "decision_rules": {},
                "severity": "MEDIUM"
            }

        # Parse decision rules JSON
        decision_rules = {}
        try:
            decision_rules = json.loads(rule.get("Decision_Rules", "{}"))
        except json.JSONDecodeError:
            pass

        return {
            "pattern": rule.get("Recommended_Pattern", ""),
            "style_priority": [s.strip() for s in rule.get("Style_Priority", "").split("+")],
            "color_mood": rule.get("Color_Mood", ""),
            "typography_mood": rule.get("Typography_Mood", ""),
            "key_effects": rule.get("Key_Effects", ""),
            "anti_patterns": rule.get("Anti_Patterns", ""),
            "decision_rules": decision_rules,
            "severity": rule.get("Severity", "MEDIUM")
        }

    def _select_best_match(self, results: list, priority_keywords: list) -> dict:
        """Select best matching result based on priority keywords."""
        if not results:
            return {}

        if not priority_keywords:
            return results[0]

        # First: try exact style name match, then substring match
        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower().strip()
                if priority_lower and style_name == priority_lower:
                    return result

        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower().strip()
                if priority_lower and style_name and (priority_lower in style_name or style_name in priority_lower):
                    return result

        # Second: score by keyword match in all fields
        scored = []
        for result in results:
            result_str = str(result).lower()
            score = 0
            for kw in priority_keywords:
                kw_lower = kw.lower().strip()
                # Higher score for style name match
                if kw_lower in result.get("Style Category", "").lower():
                    score += 10
                # Lower score for keyword field match
                elif kw_lower in result.get("Keywords", "").lower():
                    score += 3
                # Even lower for other field matches
                elif kw_lower in result_str:
                    score += 1
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else results[0]

    def _extract_results(self, search_result: dict) -> list:
        """Extract results list from search result dict."""
        return search_result.get("results", [])

    def generate(self, query: str, project_name: str = None) -> dict:
        """Generate complete design system recommendation."""
        # Step 1: First search product to get category
        product_result = search(query, "product", 1)
        product_results = product_result.get("results", [])
        category = "General"
        if product_results:
            category = product_results[0].get("Product Type", "General")

        # Step 2: Get reasoning rules for this category
        reasoning = self._apply_reasoning(category, {})
        style_priority = reasoning.get("style_priority", [])

        # Step 3: Multi-domain search with style priority hints
        search_results = self._multi_domain_search(query, style_priority)
        search_results["product"] = product_result  # Reuse product search

        # Step 4: Select best matches from each domain using priority
        style_results = self._extract_results(search_results.get("style", {}))
        color_results = self._extract_results(search_results.get("color", {}))
        typography_results = self._extract_results(search_results.get("typography", {}))
        landing_results = self._extract_results(search_results.get("landing", {}))

        best_style = self._select_best_match(style_results, reasoning.get("style_priority", []))
        best_color = color_results[0] if color_results else {}
        best_typography = typography_results[0] if typography_results else {}
        best_landing = landing_results[0] if landing_results else {}

        # Step 5: Build final recommendation
        # Combine effects from both reasoning and style search
        style_effects = best_style.get("Effects & Animation", "")
        reasoning_effects = reasoning.get("key_effects", "")
        combined_effects = style_effects if style_effects else reasoning_effects

        return {
            "project_name": re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", project_name or query.upper())[:200],
            "category": category,
            "pattern": {
                "name": best_landing.get("Pattern Name", reasoning.get("pattern", "Hero + Features + CTA")),
                "sections": best_landing.get("Section Order", "Hero > Features > CTA"),
                "cta_placement": best_landing.get("Primary CTA Placement", "Above fold"),
                "color_strategy": best_landing.get("Color Strategy", ""),
                "conversion": best_landing.get("Conversion Optimization", "")
            },
            "style": {
                "name": best_style.get("Style Category", "Minimalism"),
                "type": best_style.get("Type", "General"),
                "effects": style_effects,
                "keywords": best_style.get("Keywords", ""),
                "best_for": best_style.get("Best For", ""),
                "performance": best_style.get("Performance", ""),
                "accessibility": best_style.get("Accessibility", "")
            },
            "colors": {
                "primary": best_color.get("Primary (Hex)", "#2563EB"),
                "secondary": best_color.get("Secondary (Hex)", "#3B82F6"),
                "cta": best_color.get("CTA (Hex)", "#F97316"),
                "background": best_color.get("Background (Hex)", "#F8FAFC"),
                "text": best_color.get("Text (Hex)", "#1E293B"),
                "notes": best_color.get("Notes", "")
            },
            "typography": {
                "heading": best_typography.get("Heading Font", "Inter"),
                "body": best_typography.get("Body Font", "Inter"),
                "mood": best_typography.get("Mood/Style Keywords", reasoning.get("typography_mood", "")),
                "best_for": best_typography.get("Best For", ""),
                "google_fonts_url": best_typography.get("Google Fonts URL", ""),
                "css_import": best_typography.get("CSS Import", "")
            },
            "key_effects": combined_effects,
            "anti_patterns": reasoning.get("anti_patterns", ""),
            "decision_rules": reasoning.get("decision_rules", {}),
            "severity": reasoning.get("severity", "MEDIUM")
        }


# ============ OUTPUT FORMATTERS ============
BOX_WIDTH = 90  # Total line width including leading and trailing '|'

def format_ascii_box(design_system: dict) -> str:
    """Format design system as a fixed-width ASCII box."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    inner_w = BOX_WIDTH - 2
    border = "+" + "-" * inner_w + "+"
    blank = "|" + " " * inner_w + "|"

    def emit_wrapped(lines: list, text: str, prefix: str = "|  "):
        """Wrap text cleanly so every line fits exact BOX_WIDTH."""
        if not text:
            return
        max_body = inner_w - (len(prefix) - 1) - 1
        words = str(text).split()
        if not words:
            return
        cur = ""
        for word in words:
            while len(word) > max_body:
                if cur:
                    lines.append((prefix + cur).ljust(BOX_WIDTH - 1) + "|")
                    cur = ""
                chunk, word = word[:max_body], word[max_body:]
                lines.append((prefix + chunk).ljust(BOX_WIDTH - 1) + "|")
            if not cur:
                cur = word
            elif len(cur) + 1 + len(word) <= max_body:
                cur += " " + word
            else:
                lines.append((prefix + cur).ljust(BOX_WIDTH - 1) + "|")
                cur = word
        if cur:
            lines.append((prefix + cur).ljust(BOX_WIDTH - 1) + "|")

    sections = [s.strip() for s in pattern.get("sections", "").split(">") if s.strip()]

    lines = []
    lines.append("Advisory keyword matches; missing domains use defaults. Implementation remains unverified.")
    lines.append(border)
    emit_wrapped(lines, f"TARGET: {project} - RECOMMENDED DESIGN SYSTEM", "|  ")
    lines.append(border)
    lines.append(blank)

    # Pattern section
    emit_wrapped(lines, f"PATTERN: {pattern.get('name', '')}", "|  ")
    if pattern.get('conversion'):
        emit_wrapped(lines, f"Conversion: {pattern.get('conversion', '')}", "|     ")
    if pattern.get('cta_placement'):
        emit_wrapped(lines, f"CTA: {pattern.get('cta_placement', '')}", "|     ")
    emit_wrapped(lines, "Sections:", "|     ")
    for i, section in enumerate(sections, 1):
        emit_wrapped(lines, f"{i}. {section}", "|       ")
    lines.append(blank)

    # Style section
    emit_wrapped(lines, f"STYLE: {style.get('name', '')}", "|  ")
    if style.get("keywords"):
        emit_wrapped(lines, f"Keywords: {style.get('keywords', '')}", "|     ")
    if style.get("best_for"):
        emit_wrapped(lines, f"Best For: {style.get('best_for', '')}", "|     ")
    if style.get("performance") or style.get("accessibility"):
        perf_a11y = f"Performance: {style.get('performance', '')} | Accessibility: {style.get('accessibility', '')}"
        emit_wrapped(lines, perf_a11y, "|     ")
    lines.append(blank)

    # Colors section
    emit_wrapped(lines, "COLORS:", "|  ")
    emit_wrapped(lines, f"Primary:    {colors.get('primary', '')}", "|     ")
    emit_wrapped(lines, f"Secondary:  {colors.get('secondary', '')}", "|     ")
    emit_wrapped(lines, f"CTA:        {colors.get('cta', '')}", "|     ")
    emit_wrapped(lines, f"Background: {colors.get('background', '')}", "|     ")
    emit_wrapped(lines, f"Text:       {colors.get('text', '')}", "|     ")
    if colors.get("notes"):
        emit_wrapped(lines, f"Notes: {colors.get('notes', '')}", "|     ")
    lines.append(blank)

    # Typography section
    emit_wrapped(lines, f"TYPOGRAPHY: {typography.get('heading', '')} / {typography.get('body', '')}", "|  ")
    if typography.get("mood"):
        emit_wrapped(lines, f"Mood: {typography.get('mood', '')}", "|     ")
    if typography.get("best_for"):
        emit_wrapped(lines, f"Best For: {typography.get('best_for', '')}", "|     ")
    if typography.get("google_fonts_url"):
        emit_wrapped(lines, f"Google Fonts: {typography.get('google_fonts_url', '')}", "|     ")
    if typography.get("css_import"):
        emit_wrapped(lines, f"CSS Import: {typography.get('css_import', '')}", "|     ")
    lines.append(blank)

    # Key Effects section
    if effects:
        emit_wrapped(lines, "KEY EFFECTS:", "|  ")
        emit_wrapped(lines, effects, "|     ")
        lines.append(blank)

    # Anti-patterns section
    if anti_patterns:
        emit_wrapped(lines, "AVOID (Anti-patterns):", "|  ")
        emit_wrapped(lines, anti_patterns, "|     ")
        lines.append(blank)

    # Pre-Delivery Checklist section
    emit_wrapped(lines, "PRE-DELIVERY CHECKLIST:", "|  ")
    checklist_items = [
        "[ ] No emojis as icons (use SVG: Heroicons/Lucide)",
        "[ ] cursor-pointer on all clickable elements",
        "[ ] Hover states with smooth transitions (150-300ms)",
        "[ ] Light mode: text contrast 4.5:1 minimum",
        "[ ] Focus states visible for keyboard nav",
        "[ ] prefers-reduced-motion respected",
        "[ ] Responsive: 375px, 768px, 1024px, 1440px"
    ]
    for item in checklist_items:
        emit_wrapped(lines, item, "|     ")
    lines.append(blank)

    lines.append(border)

    return "\n".join(lines)


def format_markdown(design_system: dict) -> str:
    """Format design system as markdown."""
    project = re.sub(r"([\\`*_{}\[\]()#+.!|>-])", r"\\\1", html.escape(design_system.get("project_name", "PROJECT")))
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")

    lines = []
    lines.append(f"## Design System: {project}")
    lines.append("Advisory keyword matches; missing domains use defaults. Accessibility, security, conversion and performance remain unverified.")
    lines.append("")

    # Pattern section
    lines.append("### Pattern")
    lines.append(f"- **Name:** {pattern.get('name', '')}")
    if pattern.get('conversion'):
        lines.append(f"- **Conversion Focus:** {pattern.get('conversion', '')}")
    if pattern.get('cta_placement'):
        lines.append(f"- **CTA Placement:** {pattern.get('cta_placement', '')}")
    if pattern.get('color_strategy'):
        lines.append(f"- **Color Strategy:** {pattern.get('color_strategy', '')}")
    lines.append(f"- **Sections:** {pattern.get('sections', '')}")
    lines.append("")

    # Style section
    lines.append("### Style")
    lines.append(f"- **Name:** {style.get('name', '')}")
    if style.get('keywords'):
        lines.append(f"- **Keywords:** {style.get('keywords', '')}")
    if style.get('best_for'):
        lines.append(f"- **Best For:** {style.get('best_for', '')}")
    if style.get('performance') or style.get('accessibility'):
        lines.append(f"- **Performance:** {style.get('performance', '')} | **Accessibility:** {style.get('accessibility', '')}")
    lines.append("")

    # Colors section
    lines.append("### Colors")
    lines.append(f"| Role | Hex |")
    lines.append(f"|------|-----|")
    lines.append(f"| Primary | {colors.get('primary', '')} |")
    lines.append(f"| Secondary | {colors.get('secondary', '')} |")
    lines.append(f"| CTA | {colors.get('cta', '')} |")
    lines.append(f"| Background | {colors.get('background', '')} |")
    lines.append(f"| Text | {colors.get('text', '')} |")
    if colors.get("notes"):
        lines.append(f"\n*Notes: {colors.get('notes', '')}*")
    lines.append("")

    # Typography section
    lines.append("### Typography")
    lines.append(f"- **Heading:** {typography.get('heading', '')}")
    lines.append(f"- **Body:** {typography.get('body', '')}")
    if typography.get("mood"):
        lines.append(f"- **Mood:** {typography.get('mood', '')}")
    if typography.get("best_for"):
        lines.append(f"- **Best For:** {typography.get('best_for', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** {typography.get('google_fonts_url', '')}")
    if typography.get("css_import"):
        lines.append(f"- **CSS Import:**")
        lines.append(f"```css")
        lines.append(f"{typography.get('css_import', '')}")
        lines.append(f"```")
    lines.append("")

    # Key Effects section
    if effects:
        lines.append("### Key Effects")
        lines.append(f"{effects}")
        lines.append("")

    # Anti-patterns section
    if anti_patterns:
        lines.append("### Avoid (Anti-patterns)")
        anti_bullets = "- " + anti_patterns.replace(' + ', '\n- ')
        lines.append(anti_bullets)
        lines.append("")

    # Pre-Delivery Checklist section
    lines.append("### Pre-Delivery Checklist")
    lines.append("- [ ] No emojis as icons (use SVG: Heroicons/Lucide)")
    lines.append("- [ ] cursor-pointer on all clickable elements")
    lines.append("- [ ] Hover states with smooth transitions (150-300ms)")
    lines.append("- [ ] Light mode: text contrast 4.5:1 minimum")
    lines.append("- [ ] Focus states visible for keyboard nav")
    lines.append("- [ ] prefers-reduced-motion respected")
    lines.append("- [ ] Responsive: 375px, 768px, 1024px, 1440px")
    lines.append("")

    return "\n".join(lines)


# ============ MAIN ENTRY POINT ============
def generate_design_system(query: str, project_name: str = None, output_format: str = "ascii") -> str:
    """
    Main entry point for design system generation.

    Args:
        query: Search query (e.g., "SaaS dashboard", "e-commerce luxury")
        project_name: Optional project name for output header
        output_format: "ascii" (default) or "markdown"

    Returns:
        Formatted design system string
    """
    generator = DesignSystemGenerator()
    design_system = generator.generate(query, project_name)

    if output_format == "markdown":
        return format_markdown(design_system)
    return format_ascii_box(design_system)


# ============ CLI SUPPORT ============
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Design System")
    parser.add_argument("query", help="Search query (e.g., 'SaaS dashboard')")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format")

    args = parser.parse_args()

    result = generate_design_system(args.query, args.project_name, args.format)
    print(result)
