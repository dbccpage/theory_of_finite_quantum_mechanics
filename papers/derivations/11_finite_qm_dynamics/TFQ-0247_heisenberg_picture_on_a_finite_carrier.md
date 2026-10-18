# [TFQ-0247] Heisenberg picture on a finite carrier

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `00357ae4-5bdf-571d-b2c6-bc6dcdb14c37`  
> **Parent Derivation**: [TFQ-0245](TFQ-0245_unitary_finite-shadow_slot_still_reserved.md)

---

## 1. Abstract & Formal Statement

QM_041 is a redirect. The opened pages keep a finite-dimensional Heisenberg evolution: for a fixed Hermitian operator and a unitary built as an exponential of that operator, the evolved observable is the conjugate action, and its derivative is the commutator with the generator. The sign depends on the exponential convention, which the paper records rather than hiding. The same redirect sends the history-sum rules to QM_043 and names heisenberg_picture.rs as the implementation home. DS-QM041-HEISENBERG-PICTURE-FINITE is the derivation-graph id.

### Governing Obligation
Conjugate a supplied observable by a supplied finite unitary, and keep the generator and the sign convention as declared data.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex matrices (assumption)`
- **Admitted**: `unitary family U(t) and generator H (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> U(t) and H not produced by anything upstream.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/heisenberg_picture.rs::heisenberg_observable`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0248](TFQ-0248_finite_history_decoherence_matrix.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
