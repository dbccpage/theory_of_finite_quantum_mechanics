# [TFQ-0290] Direct normalization of sector weights

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ab14bb13-d9d3-522a-929d-a2f72554c475`  
> **Parent Derivation**: [TFQ-0289](../09_finite_hilbert/TFQ-0289_diagonal_density_with_coherences_unfixed.md)

---

## 1. Abstract & Formal Statement

In qm_020_born_normalization_and_conditional_hilbert_lift.md the section labeled Theorem 1 defines the unit-sum profile of a finite nonnegative weight vector with positive total by dividing by that total. The finite obligation is that profile: nonnegative coordinates summing to one, with a later probability reading treated as a separate adapter the paper says it does not supply. The claim ledger types this row as algebra that needs no Hilbert space. derivation_dag.json records the ids L1-QM020-THM1-DIRECT-NORMALIZATION and FQ-BORN-NORMALIZATION-REDUNDANCY beside it.

### Governing Obligation
Compute the unit-sum weight profile on a positive total without a Hilbert carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Born/quadratic readout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none for the finite rational statement. Ledger-cited names PaperQF002 / L010_01_BornRedundancy were not found as modules; BornRedundancy.lean (axioms include Classical.choice per its header) is the located home.

> [!WARNING]
> The cited declarations live in lean4/original_lean_20260809/qm_l010_01_born_redundancy.lean (2,215 lines, Mathlib.Tactic import); repo-level lean4/quantum_mechanics copy is Mathlib-free but this extraction did not run a build. Zenodo 20683775 needs the narrowing erratum.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::listSum_normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize_idempotent`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::ray_quotient_classification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/simplex.rs::try_from_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0291](TFQ-0291_disjoint_aggregation_and_the_real_p_1_import.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/ch02_conditional_hilbert_lift_and_born_normalization.md`
