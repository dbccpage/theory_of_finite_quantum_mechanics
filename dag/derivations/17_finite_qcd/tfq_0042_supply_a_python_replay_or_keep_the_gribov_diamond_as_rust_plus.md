# [TFQ-0042] Supply a Python replay or keep the Gribov diamond as Rust plus

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `6181a140-4d12-5202-a730-119fbe654fd4`  
> **Parent Derivation**: [TFQ-0023](tfq_0023_keep_the_3_by_3_betti_count_separate_from_a_link_ensemble.md)

---

## 1. Abstract & Formal Statement

ravera_dfm_finite_to_continuum.rs evaluates evaluate_su3_spanning_tree_vs_landau_gribov_control on CarrierGraph::diamond with five explicit block links over Q(i), checks a non-abelian commutator, and dresses every spanning tree, and it counts diagonal Klein-four copies. Lean su3_diagonal_klein_four_landau_gribov_copies and spanning_tree_dfm_eliminates_gribov_copies treat the copy count 4^3=64 and a tree identity for rational, not matrix, link variables. No Python twin of this function was found under 006_finite_qm/python. The module title uses continuum language; that title is not a bridge theorem.

### Governing Obligation
Supply a Python replay or keep the Gribov diamond as Rust plus a Lean rational shadow.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/ravera_dfm_finite_to_continuum.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: evaluate_su3_spanning_tree_vs_landau_gribov_control has no Python twin under 006_finite_qm/python`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge/shelf.yaml`
