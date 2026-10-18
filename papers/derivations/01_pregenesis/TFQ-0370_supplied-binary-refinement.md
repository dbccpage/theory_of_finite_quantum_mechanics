# [TFQ-0370] supplied-binary-refinement

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c3d238af-7743-5a39-808f-065c7ebe6750`  
> **Parent Derivation**: [TFQ-0369](TFQ-0369_finite-demand-count.md)

---

## 1. Abstract & Formal Statement

PG-REFINE-SEPARATES and ledger row WDP-P001-004 say a supplied binary tag can separate one collapsed pair while the old report is retained. Opened Paper.lean declares refine_separates, and preservation.refine pairs reports with tags. The tag is an input. Pre-Genesis paper.md section 9 is the heading. The finite statement still required is that finding which tag to supply, and satisfying many conflicts at once, stay separate questions and are not discharged by one pair. Chapter 3 says a comparison regime is declared data, not something read off two marks.

### Governing Obligation
One supplied binary tag may separate one collapsed pair and retain the old report; tag search and many conflicts stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Supplied tag (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Tag supply is an input; no derivation of which tag to supply.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: refine_separates, one supplied tag, one collapsed pair`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::refine_separates`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::supplied_tag_separates`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a supplied-tag splitter in crate pre_mssn_preservation with the tag passed in, not chosen inside the function`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: preservation.refine must take the tag as an argument and must not search for a tag`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0371](TFQ-0371_old-image-injective-lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch03_marks_presentations_and_declared_comparisons.md`
