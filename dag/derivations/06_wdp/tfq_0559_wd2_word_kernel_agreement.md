# [TFQ-0559] wd2-word-kernel-agreement

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `71269c13-f84f-5416-8a3f-eef3e7258788`  
> **Parent Derivation**: [TFQ-0558](tfq_0558_wdp_handoff_to_l1.md)

---

## 1. Abstract & Formal Statement

At finite horizon n, the recursive indistinguishability relation R_n of a finite deterministic Moore machine coincides with the intersection of kernels of the observation map composed with update words of length at most n (WD2-L1).

### Governing Obligation
Provide a general inductive proof in Lean 4 on word length connecting the recursive definition R_{n+1} to word-kernel agreement over arbitrary finite alphabets and state types.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0536](tfq_0536_wdp_failed_sameness.md) wdp-failed-sameness

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Establishes word-kernel agreement R_n = intersect_{|w|<=n} ker(p o u_w) in Lean 4 for both concrete Nat machines and polymorphic state and alphabet types; does not bound stabilization horizon N (tracked in TFQ-0561).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.poly_word_kernel_agreement`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.word_kernel_agreement`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified directly in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py::word_kernel_agrees`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0560](tfq_0560_wd2_refinement_stabilization.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md:5`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/wd2_open_targets.md:19-23`
