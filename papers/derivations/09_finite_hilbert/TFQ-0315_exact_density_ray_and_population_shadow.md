# [TFQ-0315] Exact density, ray, and population shadow

> **Stage**: `FINITE_HILBERT` | **Status**: `SOURCE_RECORD`  
> **UUID**: `8d7a2934-8da6-5f6c-928a-c9d458c40a40`  
> **Parent Derivation**: [TFQ-0314](TFQ-0314_cochain_lift_still_prices_the_born_law_as_an_import.md)

---

## 1. Abstract & Formal Statement

density_matrix.rs accepts an exact density over Gaussian rationals only when it is Hermitian, positive semidefinite by an exact test, and of trace one, and it separates that operator from the population shadow of its diagonal. The finite obligation is that split. The shadow of a pure projector and the shadow of a classical mixture can agree while the coherences differ, and the module says those coherences are reported rather than dropped. quantum_state.rs keeps unnormalized rays and applies a declared squared-modulus rule for computational-basis weights.

### Governing Obligation
Validate exact finite densities separately from their classical population shadows.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/lean4/FromPrimitiveDifferenceToQuantumMechanics/FiniteDensity.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/density_matrix.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/python/src/finite_quantum/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0316](TFQ-0316_package_chapter_states_a_conditional_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F003`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/floor.yaml`
