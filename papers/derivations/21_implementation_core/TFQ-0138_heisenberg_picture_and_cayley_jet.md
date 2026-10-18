# [TFQ-0138] Heisenberg picture and Cayley jet

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `46d4a54c-9b7a-535a-bd3e-8f685e20e25a`  
> **Parent Derivation**: [TFQ-0137](TFQ-0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers heisenberg_picture.rs, heisenberg_representation_uniqueness.rs, dynamics_dichotomy.rs, stochastic_unitary_boundary.rs, and finite_report_dynamics.rs. heisenberg_picture.rs updates states and observables by declared unitary steps over Q(i) so the trace pairing agrees, plus the first-order Cayley jet. The representation file is a finite odd-prime certificate, not an infinite-dimensional uniqueness claim. The other files separate periodic sectors from stochastic steps and dilate report dynamics. A Python replay and a Lean 4 declaration would still have to match the trace pairing and the Cayley tangent.

### Governing Obligation
Match equality of the trace pairing under Schrodinger and Heisenberg updates and the first-order Cayley tangent.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/dynamics_dichotomy.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/heisenberg_picture.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/heisenberg_representation_uniqueness.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/stochastic_unitary_boundary.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dynamics_dichotomy.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/heisenberg_representation_uniqueness.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0139](TFQ-0139_page-wootters_clock_and_tsirelson.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
