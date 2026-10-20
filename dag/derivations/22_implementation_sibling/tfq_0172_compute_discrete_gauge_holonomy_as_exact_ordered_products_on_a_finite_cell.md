# [TFQ-0172] Compute discrete gauge holonomy as exact ordered products on a finite cell

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `c6ef0795-5b8d-551b-b16b-221ca37806fb`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

Discrete gauge holonomy is the omega_holonomy crate, under a stated zero-float law and AuthorityEffect None. src/lib.rs exports path and loop products, Wilson traces, and cycle pairings; src/holonomy.rs builds a HolonomyLoop only when the vertex list closes, rejecting a short path and an open loop. Transport data are ExactMatrix values, not display floats. The obligation is to evaluate ordered products on a finite cell complex without promoting the result to a continuum connection or to a U(1) Hilbert phase. This crate is not the scaffold type in omega_general_relativity/src/holonomy.rs.

### Governing Obligation
Compute discrete gauge holonomy as exact ordered products on a finite cell complex.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CoboundaryHolonomy.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/majorana/holonomy.rs`](../../code/rust/src/)
- [`code/rust/src/general_relativity/exact_regge/connection.rs`](../../code/rust/src/)
- [`code/rust/src/holonomy/graph.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0173](tfq_0173_keep_discrete_curvature_as_an_exact_plaquette_defect_and_matrix_commutator_without.md)
- [TFQ-0174](tfq_0174_keep_the_discrete_connection_laplacian_and_gauge_quotient_on_exact_matrix_data.md)
- [TFQ-0175](tfq_0175_keep_integer_coboundary_holonomy_distinct_from_exact_matrix_gauge_holonomy.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
