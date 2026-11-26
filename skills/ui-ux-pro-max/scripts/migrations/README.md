# Dataset Migration & Seed Scripts

Historical one-off Python seed scripts used to expand and normalize `skills/ui-ux-pro-max/data/section-archetypes.{json,csv}`.

- Active runtime/audit tools remain in [`../`](../): `core.py`, `search.py`, `design_system.py`, `generate_section_prompt.py`, `system_audit.py`, `eval_golden_set.py`, `normalize_products_dataset.py`, and `dataset_utils.py`.
- Migration scripts (`add_*.py`) remain runnable idempotently from the repo root:

```bash
python skills/ui-ux-pro-max/scripts/migrations/add_kinetic_agency_sections.py
```
