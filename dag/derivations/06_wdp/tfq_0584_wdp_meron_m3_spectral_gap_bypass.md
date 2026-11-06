# [TFQ-0584] wdp-meron-m3-spectral-gap-bypass

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `5698fe5b-1e61-5c55-a694-cfd1ec5e7193`  
> **Parent Derivation**: [TFQ-0583](tfq_0583_wdp_meron_m2_cumulant_bounds.md)

---

## 1. Abstract & Formal Statement

Meron Field-Limit Target M3: establish the all-M transfer-matrix spectral gap statement or prove that the fixed-carrier response theorem bypasses all-M spectral separation.

### Governing Obligation
Prove or refute uniform spectral separation across checkerboard Trotter steps M, respecting the Gate E finite-M counterexample.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open target; Gate E refutes naive finite-M positivity at a specific parameter point, so any spectral or bypass argument must respect that obstruction.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean::WitnessedDifference.WdpBatch13.m3_margin_positivity_bypass`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean::WitnessedDifference.WdpBatch13.wdp_meron_m3_gate_e_obstruction_and_margin_bypass`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean::WitnessedDifference.WdpBatch13Rep.wdp_meron_m3_gate_e_obstruction_and_margin_bypass`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch13Rep.lean)
- `missing obligation: all-M spectral gap or bypass theorem is open`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust certifier for all-M transfer spectrum yet`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/code/gate_e_exact_counterexample.py::main`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/code/gate_e_exact_counterexample.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0585](tfq_0585_wdp_meron_m4_native_adapters.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md:30-31`
