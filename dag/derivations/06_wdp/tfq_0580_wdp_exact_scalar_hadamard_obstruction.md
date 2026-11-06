# [TFQ-0580] wdp-exact-scalar-hadamard-obstruction

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `3379e576-3ef6-5ee0-b0ad-029e97a12855`  
> **Parent Derivation**: [TFQ-0579](tfq_0579_wdp_born_rule_nonselection.md)

---

## 1. Abstract & Formal Statement

No rational scalar squares to 1/2, so normalized Hadamard and T gates cannot be represented inside the exact Gaussian-rational matrix algebra without quadratic irrational extension or scaled-unitary tracking (GEN-WDP-68).

### Governing Obligation
Keep the 2-adic parity descent proof that 2*a^2 != b^2 for b != 0 scoped to exact rational and Gaussian-rational matrix entries without quadratic extension.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> FiniteProcessComposition.lean and WdpBatch4.lean formalize 2-adic parity descent (nat_two_mul_sq_ne_sq, int_two_mul_sq_ne_sq, exact_scalar_hadamard_and_t_obstruction) alongside unitary_mass_preserving.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WDP.FiniteProcessComposition.postFactor_compose`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WDP.FiniteProcessComposition.unitary_mass_preserving`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WitnessedDifference.FiniteProcessComposition.int_two_mul_sq_ne_sq`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WitnessedDifference.FiniteProcessComposition.nat_two_mul_sq_ne_sq`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean::WitnessedDifference.WdpBatch4.exact_scalar_hadamard_and_t_obstruction`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked in Lean 4 and Python process composition modules`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py::to_gaussian_rational`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0581](tfq_0581_wdp_affine_thickening_conjecture.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:79`
