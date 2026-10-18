# [TFQ-0133] Observables and local star algebras

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b0b42608-dfe8-5e77-94d0-5605adab58dd`  
> **Parent Derivation**: [TFQ-0131](TFQ-0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers observable.rs, hermitian_spectral.rs, commutator.rs, commuting_observables.rs, local_operator_algebra.rs, superselection_sector.rs, and algebraic_qft.rs. observable.rs takes an observable to be an exact Hermitian over Q(i), with rational expectation and a checked Robertson-Schrodinger comparison. The other files isolate bounded-dimension eigenvalues, record the Weyl commutator, finite star-subalgebras, superselection, and local nets that do not establish continuum Haag duality. A Python replay and a Lean 4 declaration would still have to match the exact expectation and that net boundary.

### Governing Obligation
Match exact rational expectations of Hermitian observables and the statement that finite local nets do not establish continuum Haag duality.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/algebraic_qft.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/commutator.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/commuting_observables.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hermitian_spectral.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/local_operator_algebra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/observable.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/superselection_sector.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for observable.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0134](TFQ-0134_pauli_group_and_exchange_characters.md)
- [TFQ-0137](TFQ-0137_unitary_steps_and_hamiltonians.md)
- [TFQ-0144](TFQ-0144_projective_measurement_and_instruments.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
