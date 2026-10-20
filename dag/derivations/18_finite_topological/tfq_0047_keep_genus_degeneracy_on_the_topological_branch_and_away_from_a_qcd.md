# [TFQ-0047] Keep genus degeneracy on the topological branch and away from a QCD

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `10cfb5c3-155c-5efd-8629-e8899b380689`  
> **Parent Derivation**: [TFQ-0046](tfq_0046_cite_a_zero_residual_only_for_the_supplied_exact_matrix.md)

---

## 1. Abstract & Formal Statement

modular_tensor_category.rs builds ModularData::verified from an AnyonModel and exposes ground_state_degeneracy at a declared genus. The modular arithmetic lives in omega_fusion_categories::modular, which states that the familiar normalized relation (ST)^3 = S^2 needs a root that need not lie in the coefficient field. The in-field statements are the ones actually checked. A genus degeneracy computed from S and T data is a topological count. It is not a QCD vacuum degeneracy, and the module does not claim a mass gap. Toric or Ising modular data must stay on this side branch.

### Governing Obligation
Keep genus degeneracy on the topological branch and away from a QCD vacuum claim.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: ModularData is not a FiniteQM theorem`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/modular_tensor_category.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/modular.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: modular genus count has no QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
