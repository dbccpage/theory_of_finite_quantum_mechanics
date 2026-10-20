# [TFQ-0159] MUB tomography and composition

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1c031433-56d9-519d-b61a-236846977f04`  
> **Parent Derivation**: [TFQ-0154](tfq_0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers tomography.rs, composition_tensor_mub.rs, composition_tomography.rs, and four_wall_reconstruction.rs. tomography.rs reconstructs a qutrit by MUB linear inversion: Born weights are traces against projectors, and rho is their weighted sum minus the identity, with no floating-point gap. The other files check tensor composition of densities, a monoidal face with a real rebit countermodel, and four exact four-wall checks. A Python replay and a Lean 4 declaration would still have to match the d=3 inversion identity.

### Governing Obligation
Match qutrit MUB inversion rho = sum p Pi - I and the real rebit countermodel on monoidal composition.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/tomography.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/composition_tensor_mub.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/composition_tomography.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/four_wall_reconstruction.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/composition_tensor_mub.py`](../../code/python/)
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/four_wall_reconstruction_and_operad_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
