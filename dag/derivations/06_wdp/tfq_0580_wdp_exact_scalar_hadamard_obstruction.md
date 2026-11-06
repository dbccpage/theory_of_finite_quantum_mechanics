# [TFQ-0580] wdp-exact-scalar-hadamard-obstruction

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3379e576-3ef6-5ee0-b0ad-029e97a12855`  
> **Parent Derivation**: [TFQ-0579](tfq_0579_wdp_born_rule_nonselection.md)

---

## 1. Abstract & Formal Statement

No rational scalar squares to 1/2, so normalized Hadamard and T gates cannot be represented inside the exact Gaussian-rational matrix algebra without quadratic irrational extension or scaled-unitary tracking (GEN-WDP-68).

### Governing Obligation
Mechanize the exact rational non-square obstruction q^2 != 1/2 directly inside FiniteProcessComposition.lean alongside unitary_mass_preserving.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> FiniteProcessComposition.lean formalizes exact Gaussian-rational Kraus and Pauli-X unitary transport; the 2-adic valuation proof that no rational squares to 1/2 is written in prose and checked in Python.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WDP.FiniteProcessComposition.postFactor_compose`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean::WDP.FiniteProcessComposition.unitary_mass_preserving`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)

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
