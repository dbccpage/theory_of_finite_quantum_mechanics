# [TFQ-0140] Product formulas and locality cones

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b979ce59-3d45-5eea-bff5-9ef13b4e6f4d`  
> **Parent Derivation**: [TFQ-0137](tfq_0137_unitary_steps_and_hamiltonians.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:ce1c94d0ab84256d9dfd38a365daf2c8b0451d2628be4dce26e70c9493dc7d4e`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:dfb5bb461f97bf8df5e6f2a89f446ad4e057ea3c840bac23c7c726d32459ea56`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:aaf25aa062ea0b5b2c12ef380659735be18e44837a39eebb6c904013236f3807`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/growth_refinement.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:7fa6cf79f7aa766503b4ccac8815d017703c1d7086e7cc8572bfb24fecf21aaa`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:137371a7ef39fe21af104b863ad39cb8d7476c8c4fe6f0f0fa98e158e83f5e4d`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/continuous_time_locality_limit.py`](../../code/python/)
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/norm_approximation_frontier.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0141](tfq_0141_meron_source_majorants.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
