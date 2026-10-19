# [TFQ-0135] Parity contextuality and frame functions

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1bc63a61-f018-5166-9b22-15d57ac377c5`  
> **Parent Derivation**: [TFQ-0134](tfq_0134_pauli_group_and_exchange_characters.md)

---

## 1. Abstract & Formal Statement

Covers contextuality_obstruction.rs, kochen_specker.rs, separating_predictions.rs, frame_function_polytope.rs, and gauge_cochain_complex.rs. contextuality_obstruction.rs computes finite parity contextuality as a Z2 cochain class, with a Cabello 18-ray witness and a product scenario whose class vanishes. The other files decide Kochen-Specker hypergraphs, replay Mermin-Peres assignments over F2, tie frame functions to symmetric matrices, and classify packets on M_2(Q(i)). A Python replay and a Lean 4 declaration would still have to match that Z2 class and the vanishing control.

### Governing Obligation
Match the Z2 cochain obstruction, the Cabello witness, and the product scenario whose class vanishes.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/separating_predictions.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/contextuality_f2.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/mermin_peres.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
