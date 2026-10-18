# [TFQ-0300] Descent-compatible maps stay row-sparse

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6a413e5b-3d74-5ab7-adc0-1ace6aca539b`  
> **Parent Derivation**: [TFQ-0299](TFQ-0299_orthogonal_additivity_is_an_extra_frame_law.md)

---

## 1. Abstract & Formal Statement

qm_020_born_normalization_and_conditional_hilbert_lift.md, in the section labeled Theorem 3, states that a linear map compatible with phase-blind descent on a chosen sector basis is strictly row-sparse, and that this is conditional on that basis plus an imported linear representation. The finite obligation is the row-sparsity test on the declared basis. A unitary that is also descent-compatible is then a monomial unitary: a permutation of sectors times phases. Generic unitaries need not commute with the phase-blind quotient.

### Governing Obligation
Test descent through the phase-blind quotient only for row-sparse maps on the declared basis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `linear representation of sectors: assumption`
- **Admitted**: `sector basis and quadratic readout (assumption)`
- **Admitted**: `unit phase rotations: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> General-n 2-sparse probe separation and 1-sparse invariance mechanized in DerivationDagQMClosure.lean.

> [!WARNING]
> General-n 2-sparse probe separation ((a+b)^2 - (a-b)^2 = 4ab != 0), 1-sparse phase-blind invariance, and projective-zero counterexample mechanized in DerivationDagQMClosure.lean.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::descent_compatible_iff_row_sparse`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::ray_quotient_classification`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::row_sparse_implies_descent_compatible`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::classify_descent`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::phase_equivalent`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0301](TFQ-0301_haar-independent_phases_are_not_the_finite_average.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
