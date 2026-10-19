# [TFQ-0146] Kraus channels and completely positive maps

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `9e7e608d-6b41-53c3-ad74-587933e8ae7a`  
> **Parent Derivation**: [TFQ-0144](tfq_0144_projective_measurement_and_instruments.md)

---

## 1. Abstract & Formal Statement

Covers quantum_channel.rs, kraus_operators.rs, completely_positive_map.rs, and exact_channel.rs. quantum_channel.rs is the finite Kraus and CPTP face; floating-point parameters do not admit a channel, and exact admission is ExactKrausChannel. The other files are the Kraus-set face, the Choi isomorphism, and one declared Q(i) channel in weighted Kraus, Choi, and Stinespring forms. A Python replay and a Lean 4 declaration would still have to match that split between the diagnostic face and exact admission.

### Governing Obligation
Match the split between the diagnostic f64 channel face and exact Q(i) admission of one weighted Kraus channel.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/completely_positive_map.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/kraus_operators.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/cptp_channel.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0147](tfq_0147_weighted_stinespring_realizations.md)
- [TFQ-0153](tfq_0153_no_signalling_and_classical_storage.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
