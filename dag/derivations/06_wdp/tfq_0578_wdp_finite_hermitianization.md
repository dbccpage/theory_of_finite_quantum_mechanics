# [TFQ-0578] wdp-finite-hermitianization

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `baa94bba-7189-5981-9a65-1923eadbbb13`  
> **Parent Derivation**: [TFQ-0577](tfq_0577_wdp_dagger_observer_gram_radical.md)

---

## 1. Abstract & Formal Statement

A supplied rational-linear operator J satisfying J^2 = -I compatible with a symmetric positive-semidefinite bilinear form constructs a Q(i)-Hermitian positive-semidefinite form with the same radical, while leaving the sign of J unselected (GEN-WDP-62, GEN-WDP-63).

### Governing Obligation
Maintain zero-axiom Lean 4 verification of Gaussian-rational Hermitianization and radical invariance in FiniteHermitianization.lean.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Requires a supplied compatible complex structure J; positive form alone does not select between J and -J.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean::WDP.FiniteHermitianization.hermitian_radical_iff_form_radical`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean::WDP.FiniteHermitianization.hermitian_self_nonnegative`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py::to_gaussian_rational`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0579](tfq_0579_wdp_born_rule_nonselection.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:73-74`
