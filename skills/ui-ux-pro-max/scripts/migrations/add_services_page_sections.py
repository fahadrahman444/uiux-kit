#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Services / Solutions Page sections and archetypes to section-archetypes.json
and rebuild section-archetypes.csv.

Adds 4 dedicated sections:
1. service_architecture (3 archetypes)
2. service_deliverables_matrix (3 archetypes)
3. service_tech_stack (3 archetypes)
4. service_use_cases (2 archetypes)
Total: 11 new archetypes.
Combined dataset will have: 28 sections, 140 archetypes.
"""

import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

SERVICES_SECTIONS = [
    {
        "section_id": "service_architecture",
        "section_name": "System Architecture & Technical Flow",
        "archetypes": [
            {
                "archetype_id": "arch-01",
                "name": "Node-Based Data Pipeline Diagram",
                "keywords": "architecture, data-pipeline, node-graph, technical-diagram, system-flow, engineering",
                "best_for": "Engineering consultancies, cloud infrastructure, AI/ML pipelines, and data platforms.",
                "selection_triggers": {"has_diagram": True, "tier": "technical/engineering"},
                "layout_structure": "Interactive SVG flowchart container (min-h-[400px] rounded-2xl bg-[var(--surface-raised)] border border-[var(--border-subtle)] p-8). 3-stage visual nodes (Ingestion -> Processing -> Output/APIs) connected by animated directional paths.",
                "typography_specs": "Node title: text-xs font-mono font-bold uppercase tracking-wider text-[var(--primary)]. Metric badge: text-xs font-mono text-emerald-400. Subtitle: text-xs text-[var(--text-secondary)].",
                "key_components": "SVG vector nodes, dashed bezier connecting lines, protocol labels (gRPC, Kafka, REST), inspect drawer on click.",
                "responsive_behavior": "Horizontal scroll with pan-zoom controls on tablet/mobile, or stacks into 3 linear stages.",
                "accessibility": "SVG has role='img' and aria-label; full text alternative provided in accessible <ul> for screen readers.",
                "anti_slop_rules": "No fake 3D isometric clipart; clean 2D engineering blueprint styling with crisp 1px borders."
            },
            {
                "archetype_id": "arch-02",
                "name": "Layered Modern Stack Diagram",
                "keywords": "layered-stack, architecture-layers, infrastructure, security-layer, platform-stack",
                "best_for": "Enterprise SaaS, cybersecurity, and full-stack software development services.",
                "selection_triggers": {"has_diagram": True, "architecture_style": "layered"},
                "layout_structure": "Vertical stack of 4 horizontal layers: Presentation Layer, Core Logic / API Layer, Data & Storage Layer, Security & Observability Layer. Each layer expands to reveal technical specifications.",
                "typography_specs": "Layer label: text-sm font-mono font-bold uppercase text-[var(--text-primary)]. Technology pills: text-xs font-mono bg-slate-800 text-slate-300 px-2 py-1 rounded.",
                "key_components": "Collapsible layer bands, security badge callouts, compliance seals, expandable spec panel.",
                "responsive_behavior": "Layers stack vertically on all devices with 100% width.",
                "accessibility": "Semantic <section> with <button aria-expanded> for layer details.",
                "anti_slop_rules": "No glowing purple gradient borders; maintain structured enterprise blueprint aesthetics."
            },
            {
                "archetype_id": "arch-03",
                "name": "Split Methodology & Deliverable Workflow",
                "keywords": "methodology, delivery-workflow, phase-outputs, discovery-to-launch",
                "best_for": "Agencies and consultancies that pride themselves on rigorous project governance and risk mitigation.",
                "selection_triggers": {"service_model": "consulting/turnkey"},
                "layout_structure": "2-column split (grid-cols-1 lg:grid-cols-12 gap-12 py-16). Left (5 cols): 4-phase sequential methodology (Discovery, Architecture, Sprint Build, QA & Handover). Right (7 cols): Dynamic card updating to show tangible deliverables per phase.",
                "typography_specs": "Phase number: text-xs font-mono font-bold text-[var(--primary)]. Title: text-xl font-bold. Deliverable item: text-sm font-medium.",
                "key_components": "Phase progress indicator, active phase tab, deliverable asset list, client involvement estimate badge.",
                "responsive_behavior": "Converts to 4 stacked accordion items on mobile.",
                "accessibility": "role='tablist' with role='tab' and aria-controls for the deliverable preview panel.",
                "anti_slop_rules": "Clearly state actual technical artifacts, not vague promises like 'synergistic transformation'."
            }
        ]
    },
    {
        "section_id": "service_deliverables_matrix",
        "section_name": "Scope Breakdown & Artifact Catalog",
        "archetypes": [
            {
                "archetype_id": "deliv-01",
                "name": "Categorized Scope & Artifact Accordion",
                "keywords": "scope-accordion, deliverables, artifacts, technical-specs, codebases",
                "best_for": "Product studios and software shops detailing exact handover artifacts (Design tokens, Figma system, Clean CI/CD, Documentation).",
                "selection_triggers": {"has_deliverables": True, "style": "clean"},
                "layout_structure": "Centered max-w-4xl mx-auto py-12 space-y-4. Stack of 4 broad categories (Design System, Backend Architecture, Quality Assurance, DevOps & Infrastructure), each opening to a checklist of exact deliverables.",
                "typography_specs": "Category title: text-lg font-semibold text-[var(--text-primary)]. Deliverable name: text-sm font-medium. Format pill: text-xs font-mono text-[var(--text-muted)].",
                "key_components": "Accordion trigger, artifact count chip ('8 artifacts'), checkmark list, export format tags (.tsx, .fig, .tf).",
                "responsive_behavior": "Full width on mobile with touch-friendly 48px trigger height.",
                "accessibility": "Standard accordion pattern with aria-expanded and keyboard Space/Enter toggle.",
                "anti_slop_rules": "Specify file formats and licensing; no vague lists of 'good designs'."
            },
            {
                "archetype_id": "deliv-02",
                "name": "High-Density SLA & Turnaround Table",
                "keywords": "sla-table, turnaround-time, velocity, engineering-hours, commitments",
                "best_for": "Managed service providers, retainer agencies, and dev shops with strict delivery commitments.",
                "selection_triggers": {"has_deliverables": True, "has_sla": True},
                "layout_structure": "Full-width table with 5 columns: Service Component, Typical Turnaround, Weekly Dev Allocation, Included Revisions, Testing Coverage Guarantee.",
                "typography_specs": "Table header: text-xs font-mono uppercase tracking-wider text-[var(--text-muted)]. Cell text: text-sm font-medium text-[var(--text-primary)].",
                "key_components": "Semantic <table>, SLA guarantee pill, revision policy badge, coverage badge (>90% unit test).",
                "responsive_behavior": "Horizontal swipe container on mobile with sticky first column.",
                "accessibility": "Proper th scope='col' and scope='row' markup; contrast ratio exceeds 4.5:1.",
                "anti_slop_rules": "SLA numbers must be defensible and clear; no ambiguous 'unlimited everything'."
            },
            {
                "archetype_id": "deliv-03",
                "name": "Interactive Scope Configurator",
                "keywords": "scope-configurator, custom-scope, calculator, module-picker",
                "best_for": "Modern agency websites allowing prospects to select their exact needs before requesting a proposal.",
                "selection_triggers": {"interactive_scope": True},
                "layout_structure": "Interactive 3-column selection matrix. Prospects toggle required modules (e.g., Auth & RBAC, Stripe Billing, Realtime WebSockets, Admin Dashboard) and view an estimated delivery timeline.",
                "typography_specs": "Module title: text-base font-semibold. Timeline readout: text-3xl font-mono font-bold text-[var(--primary)].",
                "key_components": "Selectable module cards with checkboxes, estimated timeline meter, 'Generate Scope Brief' CTA button.",
                "responsive_behavior": "1 column on mobile with sticky bottom timeline readout.",
                "accessibility": "role='checkbox' with aria-checked states; keyboard toggle.",
                "anti_slop_rules": "Estimates must state they are preliminary pending discovery; no misleading auto-commitments."
            }
        ]
    },
    {
        "section_id": "service_tech_stack",
        "section_name": "Supported Tech Stack, Frameworks & Integrations",
        "archetypes": [
            {
                "archetype_id": "stack-01",
                "name": "Categorized Monochromatic Tech Stack Grid",
                "keywords": "tech-stack, frameworks, tools, languages, cloud-providers, monochromatic-icons",
                "best_for": "Developer-focused dev shops and SaaS software agencies where technical stack choices dictate vendor suitability.",
                "selection_triggers": {"has_tech_stack": True, "style": "monochrome/clean"},
                "layout_structure": "4-column category grid: Frontend & Mobile (Next.js, React, React Native), Backend & APIs (Node, Go, Python, GraphQL), Databases & Caching (PostgreSQL, Redis, ClickHouse), Cloud & Infrastructure (AWS, Vercel, Docker, Kubernetes).",
                "typography_specs": "Category title: text-xs font-mono uppercase tracking-widest text-[var(--primary)]. Tech name: text-sm font-medium text-[var(--text-secondary)].",
                "key_components": "Subtle card containers, 24x24 SVG technology icons, version compatibility notes, category headers.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 4 columns desktop.",
                "accessibility": "Each tech item has descriptive text (never just an unlabelled icon).",
                "anti_slop_rules": "All technology logos must be normalized to clean monochromatic SVGs; no chaotic multi-color logo circus."
            },
            {
                "archetype_id": "stack-02",
                "name": "Certified Partner Ecosystem Strip",
                "keywords": "certified-partners, official-partners, aws-partner, vercel-expert, stripe-partner",
                "best_for": "Agencies holding official cloud and software partner credentials (AWS Advanced Partner, Vercel Partner, Stripe Expert).",
                "selection_triggers": {"has_partners": True},
                "layout_structure": "Centered horizontal card strip with 4 high-trust partner cards. Each card displays official partner badge, certified engineer headcount, and direct credential verification link.",
                "typography_specs": "Partner title: text-base font-bold. Certified count: text-xs font-mono text-emerald-400.",
                "key_components": "Official vector partner badge, certification badge, certified engineer count, external credential link.",
                "responsive_behavior": "2x2 grid on mobile, 4-column row on desktop.",
                "accessibility": "External links have aria-label='Verify AWS Partnership credential (opens in new tab)'.",
                "anti_slop_rules": "Only show legitimate, verifiable partner credentials; no self-made fake gold awards."
            },
            {
                "archetype_id": "stack-03",
                "name": "Searchable Filterable Integration Playground",
                "keywords": "integrations, searchable-stack, filter-pills, ecosystem",
                "best_for": "Enterprise integrations, iPaaS, and software platforms supporting 30+ integrations.",
                "selection_triggers": {"integration_count": "20+"},
                "layout_structure": "Filter pill bar (All, CRM, Payments, Data, Cloud) + live search input. Below: 6x4 compact icon grid updating instantly on filter/search without page reload.",
                "typography_specs": "Search input: text-sm font-medium. Pill text: text-xs font-semibold. Tech title: text-xs font-medium.",
                "key_components": "Search input, category pills, compact technology badge cards, zero-results fallback state.",
                "responsive_behavior": "Horizontal scroll for category pills on mobile; 3-column grid for tech cards.",
                "accessibility": "Search input has explicit aria-label='Filter supported integrations'; results announce count.",
                "anti_slop_rules": "Fast client-side filtering with zero layout jump; empty state has helpful contact CTA."
            }
        ]
    },
    {
        "section_id": "service_use_cases",
        "section_name": "Industry Solutions & Persona Fit",
        "archetypes": [
            {
                "archetype_id": "use-01",
                "name": "Industry Tabbed Solution Switcher",
                "keywords": "industry-solutions, fintech, healthtech, e-commerce, sector-solutions",
                "best_for": "Companies catering to multiple regulated industries with distinct compliance and functional needs.",
                "selection_triggers": {"multi_industry": True},
                "layout_structure": "Top tab bar (Fintech & Banking, Healthcare & HIPAA, Enterprise SaaS, AI & Data). Selecting a tab reveals an industry hero card with sector-specific architecture, compliance badges, and case study link.",
                "typography_specs": "Tab label: text-sm font-semibold. Sector title: text-2xl font-bold. Compliance pill: text-xs font-mono.",
                "key_components": "Segmented tab bar, industry solution card, compliance badge strip, featured client quote.",
                "responsive_behavior": "Tabs convert to horizontal swipe list on mobile with snap-x scrolling.",
                "accessibility": "role='tablist' with aria-selected states and arrow key navigation.",
                "anti_slop_rules": "Industry sections must address real regulatory requirements (e.g. HIPAA, PCI-DSS Level 1), not generic copy."
            },
            {
                "archetype_id": "use-02",
                "name": "Role / Persona Solution Cards",
                "keywords": "persona-solutions, cto-solutions, cmo-solutions, stakeholder-value",
                "best_for": "B2B enterprise platforms selling to multiple internal stakeholders with different purchasing criteria.",
                "selection_triggers": {"multi_persona": True},
                "layout_structure": "3-column card grid: 'For Technical Leaders (CTO/VP Eng)', 'For Product & Growth Leaders (CPO/VP Growth)', 'For Financial & Executive Leaders (CEO/CFO)'.",
                "typography_specs": "Persona title: text-xs font-mono uppercase tracking-wider text-[var(--primary)]. Headline: text-lg font-bold. Value bullet: text-sm.",
                "key_components": "Stakeholder icon, core outcome headline, 3 concrete value metrics (e.g. '50% less tech debt', '2x release velocity').",
                "responsive_behavior": "1 column mobile, 3 columns desktop.",
                "accessibility": "Semantic <article> per persona with clear H3 heading.",
                "anti_slop_rules": "Speak directly to each stakeholder's concrete metrics; avoid universal vague platitudes."
            }
        ]
    }
]


def rebuild():
    json_path = DATA_DIR / "section-archetypes.json"
    csv_path = DATA_DIR / "section-archetypes.csv"

    with open(json_path, "r", encoding="utf-8") as f:
        existing_sections = json.load(f)

    existing_ids = {s["section_id"] for s in existing_sections}
    
    # Append or update
    added_count = 0
    for new_sec in SERVICES_SECTIONS:
        if new_sec["section_id"] not in existing_ids:
            existing_sections.append(new_sec)
            added_count += len(new_sec["archetypes"])
            print(f"  + Added section: {new_sec['section_id']} ({len(new_sec['archetypes'])} archetypes)")
        else:
            print(f"  * Section {new_sec['section_id']} already exists, skipping duplicate")

    total_sections = len(existing_sections)
    total_archetypes = sum(len(s["archetypes"]) for s in existing_sections)

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing_sections, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON updated: {total_sections} sections, {total_archetypes} archetypes")

    # Rebuild CSV
    fieldnames = [
        "Section ID", "Section Name", "Archetype ID", "Archetype Name",
        "Keywords", "Best For", "Selection Triggers", "Layout Structure",
        "Typography Specs", "Key Components", "Responsive Behavior",
        "Accessibility", "Anti-Slop Rules"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sec in existing_sections:
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


if __name__ == "__main__":
    rebuild()
