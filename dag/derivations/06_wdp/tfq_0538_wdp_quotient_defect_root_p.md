# [TFQ-0538] wdp-quotient-defect-root-p

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `880d7ad8-af13-55eb-b1d2-a2173f6b1a46`  
> **Parent Derivation**: [TFQ-0536](tfq_0536_wdp_failed_sameness.md)

---

## 1. Abstract & Formal Statement

Root P, the evaluation layer: with V a finite-dimensional real space of defects, A a finite-dimensional space of repairs, d: A → V a linear repair map, δ ∈ V an exhibited defect and J a declared seminorm or cost, the quotient defect is Φ_J([δ]) = inf_{α ∈ A} J(δ − dα), where [δ] is the coset of δ modulo im d. The expression is not primitive: it imports a linear carrier, a repair map and a cost, each declared rather than derived. Root P presupposes Root W, the admitted cut with its witnessed irreflexive relation, as carrier and never substitutes for it. This infimum over repairs is the quantity WDP later writes Φ₁.

### Governing Obligation
Compute Φ_J as the infimum of J(δ − dα) over the declared repair space, record V, A, d and J as inputs, and never evaluate J on a single representative in its place.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared defect space V, repair space A, linear repair map d and cost J (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A declared construction, not a theorem; it derives none of the carrier, repair map or cost from the admitted cut, and Φ_J([δ]) equals J(δ) or ‖d₀δ‖₁ only where that value is shown to be the infimum.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Q1`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Repair`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/obstruction.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::matrix_quotient_l1`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0539](tfq_0539_wdp_seven_witness_roles.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:543-557`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:559-564`
  - `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md:60-76`
