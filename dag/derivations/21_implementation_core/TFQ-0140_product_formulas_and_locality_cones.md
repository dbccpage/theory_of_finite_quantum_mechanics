# [TFQ-0140] Product formulas and locality cones

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b979ce59-3d45-5eea-bff5-9ef13b4e6f4d`  
> **Parent Derivation**: [TFQ-0137](TFQ-0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers continuous_time_locality_limit.rs, product_defect_bound.rs, norm_approximation_frontier.rs, growth_refinement.rs, refinement_subsystem_tower.rs, and richardson.rs. continuous_time_locality_limit.rs evaluates exact product-formula commutator bounds and says a declared-velocity graph cone is not a Lieb-Robinson estimate. The other files check a short-time product-defect premise, CCR trace defects, conductor growth, unital star embeddings, and rational zero-noise extrapolation. A Python replay and a Lean 4 declaration would still have to match those explicit norm hypotheses.

### Governing Obligation
Match explicit product-formula commutator bounds and the statement that a declared-velocity graph cone is not a Lieb-Robinson estimate.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/continuous_time_locality_limit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/growth_refinement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/norm_approximation_frontier.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/product_defect_bound.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/refinement_subsystem_tower.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/richardson.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/continuous_time_locality_limit.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/norm_approximation_frontier.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0141](TFQ-0141_meron_source_majorants.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
