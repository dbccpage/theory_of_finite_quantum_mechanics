# [TFQ-0045] Admit an exchange only after the exact inverse check, and do not

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `2d93fb5a-3283-5b87-a784-6c9e62bb33de`  
> **Parent Derivation**: [TFQ-0044](tfq_0044_do_not_treat_su_2_k_as_a_color_fusion_category_su3_level_rs_is_absent.md)

---

## 1. Abstract & Formal Statement

r_matrix.rs stores an exact exchange on a tensor product or on a fusion space whose dimension need not be a square. try_new refuses a non-square or empty matrix and asks elimination::inverse_with_limits to succeed under DEFAULT_BRAID_LIMITS before the matrix is kept. The residual Yang-Baxter test lives in the next module; this file only admits the operator. AuthorityEffect is None. An invertible exchange on a fusion space is a topological control. It does not act on the weighted Gell-Mann generators, and it does not produce a plaquette holonomy for the 3 by 3 QCD graph.

### Governing Obligation
Admit an exchange only after the exact inverse check, and do not attach it to color generators.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: braid-limited inversion is not a FiniteQM theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/r_matrix.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: RMatrix has no finite_qm use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0046](tfq_0046_cite_a_zero_residual_only_for_the_supplied_exact_matrix.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
