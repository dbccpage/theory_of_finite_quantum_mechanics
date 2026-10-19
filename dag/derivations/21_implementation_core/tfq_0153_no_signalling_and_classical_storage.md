# [TFQ-0153] No-signalling and classical storage

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `91a1b910-e879-5085-8a39-26431d7870b3`  
> **Parent Derivation**: [TFQ-0146](tfq_0146_kraus_channels_and_completely_positive_maps.md)

---

## 1. Abstract & Formal Statement

Covers no_signalling.rs, classical_storage.rs, process_matrix.rs, classical_structure.rs, and frobenius_algebra.rs. no_signalling.rs checks that a local Kraus channel on Alice leaves Bob partial trace invariant, while a conditional branch needs an outcome message. The other files store a quantum-classical-quantum path over Q(i), carry process matrices and the quantum switch, and replay dagger-Frobenius pointer algebras. A Python replay and a Lean 4 declaration would still have to match the partial-trace invariance and the message proviso.

### Governing Obligation
Match invariance of Bob partial trace under a local Alice channel, and the outcome-message proviso for conditional branches.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/classical_storage.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/classical_structure.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/frobenius_algebra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/no_signalling.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/process_matrix.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for no_signalling.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
