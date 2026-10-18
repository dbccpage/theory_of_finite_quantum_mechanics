# [TFQ-0303] Linear isometric dynamics are an import

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `f8fa4c78-b475-538f-a132-74bad24cfc9b`  
> **Parent Derivation**: [TFQ-0302](TFQ-0302_phase-averaged_shadow_under_declared_phases.md)

---

## 1. Abstract & Formal Statement

Reversible linear isometric dynamics on the lift are an import. qm_020_born_normalization_and_conditional_hilbert_lift.md lists them as assumption five in the section labeled Theorem 6. qm_122_finite_hilbert_boundary_from_primitive_difference.md records a different finite object: a reversible report update extends to a linear map preserving an admitted form, and that map is an isometric automorphism of a ring with conjugation, not a Hilbert-space unitary, because there is no completeness and the coefficients need not be a field. A deterministic report update need not be reversible.

### Governing Obligation
Import linear isometric Hilbert dynamics, and do not equate them with report-level isometries.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `isometry / unitarity: assumption`
- **Admitted**: `linear structure on dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean module symbols not grepped; file existence only checked via listing in prior survey.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H003ReversibilityGate.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H006PermutationUnitary.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0304](TFQ-0304_lift_capacity_is_not_a_dynamics_derivation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
