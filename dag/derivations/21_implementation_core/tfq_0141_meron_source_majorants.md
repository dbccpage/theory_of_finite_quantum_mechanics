# [TFQ-0141] Meron source majorants

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a6a6f844-6e93-5e65-b89f-3f1dcf463099`  
> **Parent Derivation**: [TFQ-0140](tfq_0140_product_formulas_and_locality_cones.md)

---

## 1. Abstract & Formal Statement

Covers meron_source_field.rs, meron_spatial_source.rs, meron_time_refinement.rs, and adaptive_integrator.rs. meron_source_field.rs takes a supplied source target and an exact rational error majorant, leaving infinite-volume arguments aside. The spatial and time files bound a written Gaussian source and rational Euler slices without inferring a thermodynamic limit. adaptive_integrator.rs updates an open two-local qubit chain from full cluster factors in order A then B. A Python replay and a Lean 4 declaration would still have to match the rational majorant and the refused limits.

### Governing Obligation
Match the exact rational source majorant and the refusal to infer an infinite-volume or thermodynamic limit.

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
- [`absent: no local rust twin located for external:sha256:1d63cec400ac8406dc4fa31d974130853f1938647193bdbbf607c6c6b1358c69`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:d943330648b462e0b19d85cfad3d1d3ef74f74acaa7ea14bf9504e6851feffd5`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:4ea200be723ed74e2090d95d338a5b72e24849f9688ef439873f27949d22a0e0`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:b43e218a4285c2cb65d9817f4078f5042b8adead83afd55766232a3322ade97a`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for meron_source_field.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
