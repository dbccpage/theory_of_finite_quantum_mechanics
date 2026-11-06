# [TFQ-0586] wdp-meron-m5-toric-noise-repair

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `59002dd1-015b-55cd-8136-71c40fc55992`  
> **Parent Derivation**: [TFQ-0585](tfq_0585_wdp_meron_m4_native_adapters.md)

---

## 1. Abstract & Formal Statement

Meron Field-Limit Target M5: repair Chapter 23 toric-code kernel, restricted-error rank, and adaptivity claims under explicit finite detector and noise-support hypotheses.

### Governing Obligation
Formalize the corrected finite toric-code syndrome kernel and restricted-error rank bounds in Lean 4 and Python under explicit noise-model assumptions.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open finite-lattice target in meron_field_limit_derivations/README.md; unrestricted toric-code adaptivity claims are fenced in Chapter 23.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: Lean 4 formalization of Chapter 23 restricted-error toric-code rank bound is open`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked by Python toric boundary witness`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py::toric_boundary_witness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0587](tfq_0587_wdp_meron_spacetime_limit.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md:34-35`
