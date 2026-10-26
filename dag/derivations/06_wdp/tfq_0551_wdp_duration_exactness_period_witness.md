# [TFQ-0551] wdp-duration-exactness-period-witness

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `15dfcca5-03d7-5e92-8e37-3d03d8729d14`  
> **Parent Derivation**: [TFQ-0550](tfq_0550_wdp_succession_strict_order.md)

---

## 1. Abstract & Formal Statement

WDP-CH07-D01: a finite duration gauge is a path system with an additive edge valuation λ: E → M into a commutative monoid, D_λ(p) = Σ_j λ(e_j); positivity, Archimedean structure, units and real values are extra hypotheses, and WDP-CH07-P01 gives D_λ(pq) = D_λ(p) + D_λ(q) whenever pq is defined. Section 7.2 keeps four statuses apart: exact (a displayed t with d₀t = λ), closed nonexact (d₁λ = 0 for a declared d₁ while a period or dual certificate shows λ ∉ im d₀), active closure failure (d₁λ ≠ 0 on an exhibited 2-cell) and exactness undetermined. WDP-CH07-P02: if λ = d₀t, every directed path from a to b has duration t(b) − t(a). The converse needs more than weak connectedness: a base vertex reaching every vertex with path-independent sums, or vanishing periods under signed walks; the difference of two path sums with common endpoints is a period witness, and a nonzero period refutes exactness.

### Governing Obligation
Sum durations exactly along declared paths, report one of the four exactness statuses, construct t from a rooted path family only under the stated hypotheses, and return a period witness when two paths with common endpoints disagree.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Commutative additive monoid of durations, and an abelian group where exactness is asked (assumption)`

### Further Prerequisites
- [TFQ-0004](tfq_0004_witnessed_difference_degree_1_window.md) Witnessed-difference degree-1 window

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Duration is a declared magnitude, not physical or continuum time; the four-status classification carries no ledger row, Lean mechanizes P01 and P02 (duration_append, exact_duration_path_independent), and Python duration_sum fixes M = ℚ with strict positivity, narrower than D01.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean::duration_append`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean::exact_duration_path_independent`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Succession.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no omega_wdp Rust binding of the duration gauge or the four exactness statuses`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py::solve_potential`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/duration.py::classify_duration`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/duration.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:2961-2990`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:3025-3045`
  - `omega_engine_education/documentation/006_oewdp/levels/level_06_finite_event_valuations.md:117-140`
