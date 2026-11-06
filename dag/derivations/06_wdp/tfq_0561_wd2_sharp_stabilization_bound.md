# [TFQ-0561] wd2-sharp-stabilization-bound

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `1c0505cc-4a50-5ac5-81d1-5b377f324e2d`  
> **Parent Derivation**: [TFQ-0560](tfq_0560_wd2_refinement_stabilization.md)

---

## 1. Abstract & Formal Statement

A finite deterministic Moore machine with state set S and b_0 initial observation classes stabilizes by horizon N <= |S| - b_0, and the five-state chain reaches the sharp bound N = 3 = 5 - 2 (WD2-T2).

### Governing Obligation
Formalize the general partition-cardinality pigeonhole bound N <= |S| - b_0 and the general m-state sharp chain witness in Lean 4 alongside Wd2.sharp_m5_bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Establishes the strict-refinement partition-cardinality bound N <= |S| - b_0 and the general m-state sharp chain separation witness at horizon m - 2 in Lean 4; applies to finite deterministic Moore machines.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.sharp_chain_general_witness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.sharp_m5_bound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.stabilization_horizon_le_card_sub_b0`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified directly in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py::sharp_profile`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0562](tfq_0562_wd2_no_escape_update_congruence.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md:7`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/wd2_open_targets.md:25-28`
