# [TFQ-0581] wdp-affine-thickening-conjecture

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `02bef1b7-f6cf-5b09-87d8-63d1ae392322`  
> **Parent Derivation**: [TFQ-0580](tfq_0580_wdp_exact_scalar_hadamard_obstruction.md)

---

## 1. Abstract & Formal Statement

Construct a finite observation and recovery cost reduction for rational affine supports thickened by bounded independent measurement error epsilon > 0, replacing Appendix Y's discrete finite-fiber counting argument.

### Governing Obligation
Derive a dyadic cell partition or covering-number witness algorithm with sound abstention tokens that bounds worst-case recovery cost under bounded noise epsilon > 0.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0573](tfq_0573_wdp_out_3_realizable_future_observation.md) wdp-out-3-realizable-future-observation

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open conjecture in affine_thickening_conjecture.md; Appendix Y's exact finite-fiber theorem applies only at zero thickening (epsilon = 0).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: finite reduction for epsilon-thickened affine supports is open`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust solver for epsilon-thickened affine supports yet`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py::ExactField`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0582](tfq_0582_wdp_meron_m1_correlation_estimates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md:15-18`
