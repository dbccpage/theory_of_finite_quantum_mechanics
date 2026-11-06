# [TFQ-0582] wdp-meron-m1-correlation-estimates

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `424ae1ad-c670-5e7d-985a-4b97be2af0a2`  
> **Parent Derivation**: [TFQ-0581](tfq_0581_wdp_affine_thickening_conjecture.md)

---

## 1. Abstract & Formal Statement

Meron Field-Limit Target M1: establish or refute uniform spatial and time-dependent correlation estimates required for a joint (L, M) thermodynamic and Trotter continuum limit.

### Governing Obligation
Derive uniform in-(L, M) spatial and temporal two-point correlation bounds or exhibit a finite-scaling counterexample.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0569](tfq_0569_wdp_bridge_o04_tensor_reconstruction.md) wdp-bridge-o04-tensor-reconstruction

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open continuum-limit target; fixed four-site Trotter bounds (GEN-WDP-57) do not establish uniform joint (L, M) convergence.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean::paired_bound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/TrotterObservableFiltering.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean::WitnessedDifference.WdpBatch13.m1_int_paired_bound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean::WitnessedDifference.WdpBatch13.wdp_meron_m1_scoped_finite_correlation_and_scaling_obstruction`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean::WitnessedDifference.WdpBatch13Rep.wdp_meron_m1_scoped_finite_correlation_and_scaling_obstruction`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: joint (L, M) thermodynamic correlation bound is an open analytic target`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py::layer_transfer`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/open_derivations/meron_spacetime_limit/meron_spacetime_finite_checks.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0583](tfq_0583_wdp_meron_m2_cumulant_bounds.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md:26-27`
