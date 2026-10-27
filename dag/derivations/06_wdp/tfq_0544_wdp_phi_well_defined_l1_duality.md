# [TFQ-0544] wdp-phi-well-defined-l1-duality

> **Stage**: `WDP` | **Status**: `CONDITIONAL`  
> **UUID**: `e9c07c57-ad2e-591b-9c5f-34c327144059`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P01: Φ_J([δ]) = inf_f J(δ − d₀f) is independent of the representative, because δ' = δ + d₀g turns the infimum into one over h = f − g, a bijection of C⁰. WDP-CH04-P02 (conditional): when the repair space is finite-dimensional over ℝ or ℂ and J is a norm, the infimum is attained after quotienting ker d₀; the hypotheses cannot be dropped silently for seminorms or infinite carriers. WDP-CH04-C01 (conditional): with positive weights w, Φ_{1,w}([δ]) = max{⟨y, δ⟩ : d₀*y = 0, |y_e| ≤ w_e}, an imported finite-dimensional convex-duality result (REF-MATH-005, Rockafellar, Convex Analysis) specialized to the declared weighted graph complex. In code, finite_quotient_l1 minimizes over an explicit candidate list, and exact_quotient_l1 solves the weighted ℓ¹ programme over Fraction and reports a value only after an independent certificate check.

### Governing Obligation
Return the same Φ_J for every representative of a class, report attainment only under the finite-dimensional norm hypothesis, and treat weighted-ℓ¹ strong duality as imported, accepting an instance only with a matching repair and bounded circulation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)`
- **Admitted**: `Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)`

### Further Prerequisites
- [TFQ-0538](tfq_0538_wdp_quotient_defect_root_p.md) wdp-quotient-defect-root-p
- [TFQ-0522](../05_mssn_sn/tfq_0522_sn_e08_weighted_l1_duality.md) sn-e08-weighted-l1-duality

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The checked slice is the integer triangle coboundary: linearity, residual identity under a vertex shift, and minimum absolute residual sum 2 for delta = (1, 1, 0) and for each integer coboundary shift of that one triple. Representative independence for a general cost, attainment on a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, and a general coefficient field stay open. The weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::dual_certificate_lower_bound`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::absSum_attained`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::absSum_ge_two`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::absSum_shift`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::d0_linear`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::residual_shift`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::shifted_attained`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)
- [`lean4/PregenesisWdpPhiWellDefinedL1Duality.lean::shifted_ge`](../../../lean4/PregenesisWdpPhiWellDefinedL1Duality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs::FenchelDualityReceipt` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py::finite_quotient_l1`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/cochains.py)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::exact_quotient_l1`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:921-940`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:942-944`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1342-1359`
