# Quadrant 3: Obsolete Artifacts, Quarantined Swarms & Historical Archive

**Dimension 3 (Can Be Deleted / Quarantined)**: This directory isolates obsolete, superseded, or historical records that are retained solely for audit provenance or historical traceability, preventing search pollution in the active development workspace.

## Epistemic Posture
Nothing in this quadrant is active theory or production code. Automated search tools, code indexers, and LLMs SHOULD ignore this directory during standard retrieval and verification.

---

## Directory Inventory

### 1. Superseded Swarm Transcripts (`superseded_swarms/`)
Contains 14 historical multi-agent swarm transcripts from earlier development phases. As declared in `README.md`: *"The withdrawn generated swarm receipt is retained only in the source archive."*
- `swarm_empirical_repair.md`
- `swarm_functional_classification.md`
- `swarm_higher_category.md`
- `swarm_legacy_observers.md`
- `swarm_observer_adapter_completeness.md`
- `swarm_observer_descent.md`
- `swarm_original_genesis_observer.md`, `swarm_original_genesis_observer_formal.md`
- `swarm_policy_observer_adapter.md`
- `swarm_qm_reconstruction.md`
- `swarm_quantum_measurement.md`
- `swarm_relational_retention.md`
- `swarm_retention_choices.md`
- `swarm_self_reference_bridges.md`

### 2. Informal Essays (`informal_essays/`)
- `what_the_hell_is_authority_v002.md`: Conceptual essay on the epistemics of authority and mathematical verification.

### 3. Historical Source Archives (`source_archive/`)
Contains 529 absorbed source blobs and raw prompt histories referenced in `source_provenance.json`:
- `coda_component_packages/`: Historical snapshot of 113 `.lean` and 214 `.py` files from earlier monorepo modules.
- `meron_model_generation_history/`: Raw LLM prompts and exploratory runners.
- `toric_code_chapter_23_import.md`: Working draft absorbed into Chapter 23 of the master monograph.

### 4. Historical Errata & Audits
- `source_errata_20261008.md`: Errata log documenting earlier typographical and claim corrections.
- `terminology_audit_20261006.md`: Historical terminology alignment review.

---

## Deletion Log (Files Removed from Root)
During the restructuring of 2026-11-06, the following transient build artifacts were permanently purged from the programme root:
- `witnessed_difference_programme.aux` (122 KB)
- `witnessed_difference_programme.log` (101 KB)
- `witnessed_difference_programme.toc` (41 KB)
- Satellite release ZIP archive (`032_...zip`, 118 KB) and duplicate standalone configs (`pyproject.toml`, standalone licenses) were omitted during composition.
