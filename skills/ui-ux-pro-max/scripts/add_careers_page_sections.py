#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dedicated Careers & Talent Acquisition Page sections and archetypes to
section-archetypes.json and rebuild section-archetypes.csv.
"""

from dataset_utils import upsert_sections

CAREERS_SECTIONS = [
    {
        "section_id": "careers_perks",
        "section_name": "Compensation Philosophy & Benefits",
        "archetypes": [
            {
                "archetype_id": "perk-01",
                "name": "4-Column High-Trust Benefits Grid",
                "keywords": "benefits, perks, compensation, equity, healthcare, time-off, careers",
                "best_for": "Companies presenting structured benefits across compensation, health, workspace, and time off.",
                "selection_triggers": {"has_perks": True, "style": "clean"},
                "layout_structure": "4-column grid (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto py-14). Categorized cards: Compensation & Equity, Health & Family, Workspace Stipends, Time Off & Sabbaticals.",
                "typography_specs": "Category header: text-xs font-mono uppercase tracking-wider text-[var(--primary)]. Benefit title: text-base font-bold. Detail: text-sm text-[var(--text-secondary)].",
                "key_components": "24x24 precision SVG icon, categorized benefit heading, concrete numeric policy items, transparent footnote.",
                "responsive_behavior": "1 column mobile, 2 columns tablet, 4 columns desktop.",
                "accessibility": "Each benefit card uses <article> with <h3> headings and explicit list markup <ul>.",
                "anti_slop_rules": "Zero generic 'ping-pong and free snacks' clichés; publish actual numeric benefits and eligibility dates."
            },
            {
                "archetype_id": "perk-02",
                "name": "Compensation Philosophy Manifesto",
                "keywords": "salary-transparency, compensation-bands, equity-formula, pay-equity",
                "best_for": "Organizations differentiating on transparent salary formulas, geographic tiers, and annual equity refreshers.",
                "selection_triggers": {"salary_transparent": True},
                "layout_structure": "2-column split (grid-cols-1 lg:grid-cols-12 gap-10 max-w-6xl mx-auto py-14). Left (5 cols): Compensation philosophy statement and pay equity pledge. Right (7 cols): Band formula breakdown table and level progression.",
                "typography_specs": "Formula readout: text-lg font-mono font-semibold text-[var(--text-primary)]. Band row: text-sm tabular-nums.",
                "key_components": "Salary formula equation block, level progression table, equity refresher schedule badge.",
                "responsive_behavior": "Stacks vertically on mobile; table scrolls horizontally with sticky role column.",
                "accessibility": "Semantic <table> with <th scope='col'> and <th scope='row'>; high-contrast tabular numerals.",
                "anti_slop_rules": "Never say 'competitive salary' without posting band ranges and leveling methodology."
            },
            {
                "archetype_id": "perk-03",
                "name": "Remote-First Stipend Matrix",
                "keywords": "remote-stipend, home-office, learning-budget, coworking, distributed",
                "best_for": "Remote-first companies detailing home office setup budgets, learning stipends, and coworking allowances.",
                "selection_triggers": {"remote_stipend": True},
                "layout_structure": "3-column card grid with bold annual stipend totals anchored at top of each card ($2,000 Home Office, $1,500 Learning, $350/mo Coworking).",
                "typography_specs": "Stipend figure: text-3xl font-mono font-extrabold text-[var(--primary)] tabular-nums. Title: text-lg font-bold.",
                "key_components": "Monospaced dollar figure, reimbursement rule chip, eligible expenses list.",
                "responsive_behavior": "1 column mobile, 3 columns desktop with equal card height.",
                "accessibility": "Figures paired with descriptive text labels; contrast >= 4.5:1 across light and dark modes.",
                "anti_slop_rules": "State exact annual vs. one-time cadence and approval constraints transparently."
            },
            {
                "archetype_id": "perk-04",
                "name": "Parental & Wellness Commitment Banner",
                "keywords": "parental-leave, wellness, mental-health, recharge, sabbatical",
                "best_for": "People-first companies highlighting paid parental leave, mental health stipends, and company-wide recharge weeks.",
                "selection_triggers": {"parental_wellness": True},
                "layout_structure": "Full-width elevated card (max-w-5xl mx-auto rounded-2xl border border-[var(--border-subtle)] p-8 sm:p-10) split into 3 horizontal pillars with subtle vertical dividers.",
                "typography_specs": "Metric anchor: text-2xl sm:text-3xl font-bold font-mono. Policy summary: text-sm text-[var(--text-secondary)].",
                "key_components": "16-week paid leave block, mental health coverage badge, annual company recharge calendar.",
                "responsive_behavior": "Dividers switch from vertical to horizontal on mobile stack.",
                "accessibility": "Semantic <section> with aria-label='Parental Leave and Wellness Commitments'.",
                "anti_slop_rules": "Avoid vague 'unlimited PTO' claims without stating minimum encouraged days off."
            }
        ]
    },
    {
        "section_id": "careers_jobs",
        "section_name": "Open Requisitions & Hiring Pipeline",
        "archetypes": [
            {
                "archetype_id": "jobs-01",
                "name": "Department Filterable Requisition Board",
                "keywords": "job-board, open-roles, department-filter, hiring, requisitions",
                "best_for": "Growing teams with 5+ open roles across Engineering, Product, Design, and Go-To-Market.",
                "selection_triggers": {"has_open_roles": True, "style": "filterable"},
                "layout_structure": "Sticky department tab bar (All, Engineering, Product, Design, Go-To-Market) above stacked full-width job rows showing role title, location/remote tag, salary range, and 'Apply ->' button.",
                "typography_specs": "Role title: text-lg font-semibold. Metadata (Location, Salary Range): text-xs font-mono text-[var(--text-secondary)].",
                "key_components": "Accessible tab filter, live role counter, salary band badge, 44px Apply button, zero-roles fallback alert.",
                "responsive_behavior": "Filter pills scroll horizontally on mobile; job rows stack metadata cleanly under role title.",
                "accessibility": "role='tablist' filter bar, aria-live='polite' result count, descriptive link labels ('Apply for Senior Frontend Engineer').",
                "anti_slop_rules": "Display location eligibility and salary band on every role row; zero 'rockstar/ninja' titles."
            },
            {
                "archetype_id": "jobs-02",
                "name": "Single Requisition Expandable Accordion",
                "keywords": "job-accordion, role-details, inline-apply, expandable-jobs",
                "best_for": "Lean teams wanting candidates to inspect role mission, responsibilities, and apply inline without page hops.",
                "selection_triggers": {"accordion_jobs": True},
                "layout_structure": "Centered max-w-4xl mx-auto py-12 space-y-3. Each accordion header shows title, team, and location; expanding reveals role mission, 3 core responsibilities, qualifications, and inline application form.",
                "typography_specs": "Role trigger: text-lg font-semibold. Section label: text-xs font-mono uppercase.",
                "key_components": "Accordion trigger with aria-expanded and aria-controls, structured bullet lists, inline CV/link upload form.",
                "responsive_behavior": "Full width on mobile with >= 44px touch targets and generous field spacing.",
                "accessibility": "Keyboard Enter/Space toggle, explicit <label> on inline application fields, focus-visible dual ring.",
                "anti_slop_rules": "Keep qualification bullets realistic (3-5 essentials); no 20-requirement wishlists."
            },
            {
                "archetype_id": "jobs-03",
                "name": "Interview Pipeline & Transparent Process Stepper",
                "keywords": "interview-process, hiring-pipeline, timeline, candidate-experience",
                "best_for": "Teams reducing candidate anxiety by documenting exact interview stages, durations, and decision timelines.",
                "selection_triggers": {"interview_pipeline": True},
                "layout_structure": "4-step horizontal stepper on desktop (grid-cols-4 gap-6) covering Recruiter Sync (30m), Technical Deep Dive (60m), Paid Work Sample or Pairing (2h), and Final Offer.",
                "typography_specs": "Step badge: text-xs font-mono font-bold text-[var(--primary)]. Duration chip: text-xs font-mono. Stage title: text-base font-bold.",
                "key_components": "Sequential stage cards, time commitment badges, preparation guide note, candidate SLA ('Decision within 48h').",
                "responsive_behavior": "Collapses to numbered vertical timeline on mobile.",
                "accessibility": "Ordered list <ol> preserving chronological step sequence.",
                "anti_slop_rules": "Never omit expected turnaround times or ask for unpaid multi-day take-home projects."
            }
        ]
    }
]


if __name__ == "__main__":
    upsert_sections(CAREERS_SECTIONS)
