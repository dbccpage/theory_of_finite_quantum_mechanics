# [TFQ-0547] wdp-trichotomy-bounds

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `45decd49-4235-54ad-ad92-42e148b8f311`  
> **Parent Derivation**: [TFQ-0546](tfq_0546_wdp_exact_sequence_h1_q1.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P04: in a window with d₁d₀ = 0 and a norm J meeting the norm hypothesis, every class [h] ∈ Q¹ has exactly one of ExactClass ([h] = 0), ClosedResidual ([h] ≠ 0 and Γ₂ = 0) or ActiveClosureFailure (Γ₂ > 0); Φ₁ = 0 exactly on ExactClass, and every active class has Φ₁ > 0. WDP-CH04-P05: Φ₁, Γ₂ ≥ 0, Γ₂ = 0 iff [h] ∈ H¹, Γ₂ ≤ ‖d₁‖_{J→1}Φ₁ (repair invariance of d₁h, then the infimum), no constant c > 0 gives Γ₂ ≥ cΦ₁ when H¹ ≠ 0, and Γ₂ is a norm on Q¹/H¹. WDP-CH04-P06: if Φ₁ > 0 then 0 ≤ R_cl ≤ ‖d₁‖_{J→1}, and the normalized ratio is undefined (0/0) when d₁ = 0. The norm hypothesis (ℝ, ℂ, or ℚ with J restricted from a norm on the real extension) is needed: J(x) = |x₀₁ + √2 x₁₂ + √3 x₀₂| is a norm on ℚ³, yet on the filled triangle with δ = (1, 1, 0) its repair values accumulate at 0, so Φ₁ = 0 while Γ₂ = 2.

### Governing Obligation
Assign every class exactly one diagnostic class, check Γ₂ ≤ ‖d₁‖_{J→1}Φ₁ and 0 ≤ R_cl ≤ ‖d₁‖_{J→1} in exact arithmetic, refuse with NoRule a window missing its carrier, norm, closure data or d₁d₀ = 0 certificate, and apply none of this to a norm outside the norm hypothesis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Norm hypothesis: F = R or C, or F = Q with J the restriction of a norm on the real extension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized in Lean 4 (closure_charge_le_opnorm_mul_phi in Obstruction.lean plus diagnostic_trichotomy_exclusive_exhaustive, no_reverse_bound_when_h1_nontrivial, gamma2_quotient_norm_laws, and irrational_weight_accumulation_violates_trichotomy in WdpBatch2.lean) and checked in Python core.py.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::WitnessedDifference.closure_charge_le_opnorm_mul_phi`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean::WitnessedDifference.WdpBatch2.diagnostic_trichotomy_exclusive_exhaustive`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean::WitnessedDifference.WdpBatch2.gamma2_quotient_norm_laws`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean::WitnessedDifference.WdpBatch2.irrational_weight_accumulation_violates_trichotomy`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean::WitnessedDifference.WdpBatch2.no_reverse_bound_when_h1_nontrivial`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::TriadSignature` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::classify_signature`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1543-1593`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1505-1516`
  - `external:sha256:f444bcaa3ae162d185a3a8a21cf0b59606958107ac5510e84015090750d5c3cc:309-312`
