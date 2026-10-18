# [TFQ-0157] Characteristic-two projector MUBs

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54c0bb1d-7c42-521b-9dc4-1dc07ae3b2e4`  
> **Parent Derivation**: [TFQ-0154](TFQ-0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers mub/char_two.rs, mub/char_two_weyl_board.rs, mub/finite_projector_control.rs, mub/projector_algebra.rs, mub/spectral_lift.rs, mub/hilbert_transport.rs, and mub/gtmur_projector_ledger.rs. char_two.rs builds characteristic-two complete MUBs on exact projector matrices from independent binary generators. The other files avoid division by two, separate incidence from the operator lift, transport Pauli projectors, and audit representation changes. A Python replay and a Lean 4 declaration would still have to match the generator-dimension check and that incidence split.

### Governing Obligation
Match characteristic-two complete MUBs from independent binary generators whose count fits the Hilbert dimension.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/char_two.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/char_two_weyl_board.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/finite_projector_control.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/gtmur_projector_ledger.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/hilbert_transport.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/projector_algebra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/spectral_lift.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for characteristic-two MUB projectors under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
