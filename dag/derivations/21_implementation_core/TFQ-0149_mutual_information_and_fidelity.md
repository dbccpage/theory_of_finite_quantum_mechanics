# [TFQ-0149] Mutual information and fidelity

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1d85d481-14db-585d-b9f9-5e3f166e7bd6`  
> **Parent Derivation**: [TFQ-0148](TFQ-0148_population_and_spectral_entropy.md)

---

## 1. Abstract & Formal Statement

Covers quantum_mutual_information.rs, quantum_entropy_cone.rs, fidelity.rs, simplicial_entropy_schedule.rs, and ancilla_capacity.rs. quantum_mutual_information.rs evaluates mutual information, conditional entropy, and coherent information from the entropy face. quantum_entropy_cone.rs treats monogamy as an optional constraint, not a law of every entropy vector. The other files are Uhlmann-Jozsa fidelity, a declared Page schedule, and ancilla extension-purity bounds. A Python replay and a Lean 4 declaration would still have to match those inequalities and the optional monogamy flag.

### Governing Obligation
Match mutual information from the entropy face and the optional status of monogamy on entropy vectors.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/ancilla_capacity.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/fidelity.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_entropy_cone.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_mutual_information.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/simplicial_entropy_schedule.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/simplicial_complex_qm.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0150](TFQ-0150_discrete_phase_estimation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
