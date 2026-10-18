# [TFQ-0305] Sector weights do not force the quadratic form

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e1ac77e5-11d6-5ed6-b319-2e8024610db8`  
> **Parent Derivation**: [TFQ-0304](TFQ-0304_lift_capacity_is_not_a_dynamics_derivation.md)

---

## 1. Abstract & Formal Statement

The section labeled Theorem 6, part 1, in qm_020_born_normalization_and_conditional_hilbert_lift.md is a scope fence: additive sector weights already give a unit-sum profile and do not force a complex vector space, an inner product, phases, unitary dynamics, projectors, POVMs, interference, or a measurement lattice. The finite obligation is to keep those alternatives on the record. The same weights can be left as the classical profile, or encoded with real signed amplitudes, or given some other redundant encoding. The claim ledger types this part as a scope fence.

### Governing Obligation
State that l1 weights do not force the quadratic Born form, and stop at that fence.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean declaration originally cited was a True stub per the audit. H013BornPairingBoundary.lean is a candidate (header: Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY), not a mechanization of this Part 1.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm6_p1_scope_fence`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_nonuniqueness_open`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0306](TFQ-0306_born_uniqueness_stays_an_imported_boundary.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
