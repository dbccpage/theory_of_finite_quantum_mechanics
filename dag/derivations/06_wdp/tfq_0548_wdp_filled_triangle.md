# [TFQ-0548] wdp-filled-triangle

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `38fc9b45-ab2a-5ad0-a960-041d06596531`  
> **Parent Derivation**: [TFQ-0348](tfq_0348_certify_a_rational_phi1_value_by_a_bounded_circulation_that_meets_a.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P08: on vertices {0, 1, 2}, edges (01, 12, 02) and one 2-simplex, with d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂, the field δ = (1, 1, 0) over ℚ with unit weights has d₁d₀ = 0, Φ₁ = 2 attained at f = (0, 1, 0) (residual (0, 2, 0)) and certified by the circulation y = (1, 1, −1), Γ₂ = |1 + 1 − 0| = 2, ‖d₁‖_{1→1} = 1 and R_cl = 1, which saturates the closure-ratio bound; the class is ActiveClosureFailure. Without the 2-simplex, C² = 0 and the cyclic field (1, 1, 1) has Φ₁ = 3 (certificate y = (1, 1, 1)) and Γ₂ = 0, a ClosedResidual; filling the triangle converts that closed residual into closure charge without changing Φ₁. Orthogonal projection of δ onto ker d₁ subtracts (2/3, 2/3, −2/3) ∈ im d₁*, which meets im d₀ only in 0, so it is not a repair and Φ₁ of the original class stays 2.

### Governing Obligation
Reproduce the filled-triangle signature exactly over ℚ (d₁d₀ = 0; Φ₁ = 2 with its repair and circulation; Γ₂ = 2; ‖d₁‖_{1→1} = 1; R_cl = 1), the hollow comparison Φ₁ = 3, Γ₂ = 0, and refuse an orthogonal projection onto ker d₁ as a repair.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Unit weights on the declared filled triangle over Q (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean filled_triangle_signature covers the filled-triangle numbers over ℚ, including that 1 is the least operator constant; the hollow comparison and the projection remark are prose with Python checks, and the certificate fixes the value Φ₁ = 2, not one repair.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::filled_triangle_signature`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine/crates_rs/omega_wdp/src/obstruction.rs::DualWitnessCertificate` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_worked_filled_triangle_signature_and_certificate`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean:416-423`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1756-1782`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1848-1853`
