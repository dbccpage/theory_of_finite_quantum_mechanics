# [TFQ-0174] Keep the discrete connection Laplacian and gauge quotient on exact matrix data

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `423c11d5-d4f9-5c8e-9c86-0d15881f30c0`  
> **Parent Derivation**: [TFQ-0172](tfq_0172_compute_discrete_gauge_holonomy_as_exact_ordered_products_on_a_finite_cell.md)

---

## 1. Abstract & Formal Statement

The connection Laplacian and the gauge-quotient modules extend the same discrete holonomy control. src/laplacian.rs defines Delta_U as D minus A_U and states a zero-float law, with GaussianRational and BigRational among its imports. src/lib.rs also declares gauge_fixing.rs, gauge_quotient.rs, signed_transport.rs, and functional_graph.rs. The obligation is to treat the Laplacian spectrum and any gauge fixing as exact linear algebra on the finite complex. A perturbation certificate in that file is not a licence to replace the exact matrix by a float diagonal.

### Governing Obligation
Keep the discrete connection Laplacian and gauge quotient on exact matrix data.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/holonomy/laplacian.rs`](../../code/rust/src/)
- [`code/rust/src/holonomy/gauge_fixing.rs`](../../code/rust/src/)
- [`code/rust/src/holonomy/gauge_quotient.rs`](../../code/rust/src/)
- [`code/rust/src/holonomy/signed_transport.rs`](../../code/rust/src/)
- [`code/rust/src/holonomy/functional_graph.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
