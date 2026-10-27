# [TFQ-0100] GAP: Sigma A_h squared kappa_h is not the Einstein-Hilbert action and is

> **Stage**: `FINITE_QG` | **Status**: `EXACT_PROXY_NOT_EH`  
> **UUID**: `86de1a1b-2f67-5fe7-ba66-b6ffe6763e96`  
> **Parent Derivation**: [TFQ-0099](tfq_0099_gap_float_regge_deficit_is_not_smooth_manifold_curvature_and_is_not_the.md)

---

## 1. Abstract & Formal Statement

The exact rational proxy sits in exact_regge, not in the float script. It sums squared hinge area times kappa, where kappa is the squared Frobenius distance of a certified holonomy from the identity. Deficit angles are inverse cosines and are not rational, so the classical sum of area times deficit is not implemented. The proxy is not the Einstein-Hilbert action. Rational zero on a flat chart is not the round four-sphere action. What is finite is rational arithmetic on a declared chart. What is not discharged is smooth curvature; equating the proxy with a Riemann tensor stays GAP.

### Governing Obligation
GAP: Sigma A_h squared kappa_h is not the Einstein-Hilbert action and is not smooth curvature.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/category_theory/monoidal/mod.rs`](../../code/rust/src/)
- [`code/rust/src/general_relativity/exact_regge/action.rs`](../../code/rust/src/)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0101](tfq_0101_the_f64_face_does_not_discharge_the_einstein_hilbert_action_the_einstein_equation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `external:git-tree:6c3ddd228c139e91dd74dc2ea348d97cc54608a0`
