# [TFQ-0301] Haar-independent phases are not the finite average

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `713e8a02-91bd-5e62-9978-eaaa9e5d39cd`  
> **Parent Derivation**: [TFQ-0300](TFQ-0300_descent-compatible_maps_stay_row-sparse.md)

---

## 1. Abstract & Formal Statement

Independent Haar phases are an import. The section labeled Theorem 5 in qm_020_born_normalization_and_conditional_hilbert_lift.md conditions the phase-averaged shadow on a chosen Hilbert lift, a Haar phase measure, and an independence adapter. The finite obligation is narrower. phase_averaged_shadow.rs averages over a declared finite unit group by enumeration, says a nontrivial finite group is only a stand-in that dephases, and states that the continuous Haar average is not computed. The trivial group averages nothing. Budgets refuse enumerations that are too large.

### Governing Obligation
Import Haar independence, or label the finite phase-group average as a stand-in.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Haar probability measure on U(1)^n: assumption`
- **Admitted**: `independence of phases: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No measure-theoretic discharge; finite group stand-in only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs::phase_group_average`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0302](TFQ-0302_phase-averaged_shadow_under_declared_phases.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
