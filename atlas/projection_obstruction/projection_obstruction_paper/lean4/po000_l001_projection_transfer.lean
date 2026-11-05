/-
  Projection-transfer lemma (Paper 001, §5.4, support-ledger item "S4") in Lean 4 + Mathlib.

  Paper: research/published/001_..._States.../001_Projection_Obstruction_v5_4.md (v5.5).

  THREE layered results, from most general to most specific:

  PART 1 — `transfer` (FULLY PROVED).
    The abstract reverse-triangle transfer bound over an arbitrary `SeminormedAddCommGroup`,
    for an ARBITRARY map `P : E → E` (no linearity, continuity, or idempotence). This is the
    entire logical content of S4; only the triangle inequality is used.

  PART 1' — `transfer_of_lipschitz` (FULLY PROVED).
    If `P` is `L`-Lipschitz on the segment, the defect transfers with the FINITE constant
    `1 + L`. Theorem 5.1 is proved directly via double commutators on the raw defect without
    requiring Lieb–Robinson error bounds. No trace-norm / tensor facts are required at all for this.

  PART 2 — `tensor_subadd` + `transfer_product_KPi_three` (REDUCTION PROVED; analytic facts as
    explicit, correctly-typed hypotheses). The product-of-marginals retraction
    `P x = tens (mA x) (mB x)` with marginals typed in their OWN spaces `EA`, `EB` (not the
    joint space `E`). Tensor sub-additivity is DERIVED from norm-multiplicativity + bilinearity
    + the UNIT-TRACE normalizations `‖mB ρ‖ = 1`, `‖mA σ‖ = 1` — so the normalization that an
    unqualified sub-additivity assumption would hide is made visible. Partial-trace
    contractivity (the true, easy direction) stays as a hypothesis. Conclusion: `K_Π = 1+2 = 3`.

    The remaining inputs (contractivity; norm-multiplicativity of the tensor) are NOT in core
    Mathlib — they live only in downstream quantum libraries (PhysLean / LeanQuantumInfo /
    LeanQuantum). They are therefore hypotheses, exactly as the paper *assumes* the analytic
    ingredients of S4. K_Π = 3 is cosmetic for 001 (see Part 1'); it is proved here for the
    standalone strength of the S4 claim.
-/
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace ProjectionTransfer

/-! ## Part 1 — abstract transfer over a single seminormed group -/

section Abstract

variable {E : Type*} [SeminormedAddCommGroup E]

/-- Projection defect `C_P(x) = ‖x − P x‖` for a retraction-like map `P` (written `Π` in the
paper; `Π` is reserved in Lean 4 as Pi-type notation, hence `P`). -/
def C (P : E → E) (x : E) : ℝ := ‖x - P x‖

/--
**Part 1 — abstract transfer lemma (the logical core of S4).**

For any map `P : E → E` and elements `ρ σ : E`, if `‖ρ − σ‖ ≤ ε` and `P` moves the pair by at
most `L · ε` (`‖P ρ − P σ‖ ≤ L · ε`), then the projection defects satisfy
`C P ρ ≥ C P σ − (1 + L) · ε`.

Only the triangle inequality is used; `P` need not be linear, continuous, or idempotent.
-/
theorem transfer (P : E → E) {ρ σ : E} {ε L : ℝ}
    (h1 : ‖ρ - σ‖ ≤ ε) (h2 : ‖P ρ - P σ‖ ≤ L * ε) :
    C P ρ ≥ C P σ - (1 + L) * ε := by
  -- Telescope: σ − P σ = (ρ − P ρ) + (−(ρ − σ) + (P ρ − P σ)).
  have hsplit : σ - P σ = (ρ - P ρ) + (-(ρ - σ) + (P ρ - P σ)) := by abel
  have hstep : ‖σ - P σ‖ ≤ ‖ρ - P ρ‖ + (‖ρ - σ‖ + ‖P ρ - P σ‖) := by
    calc ‖σ - P σ‖
        = ‖(ρ - P ρ) + (-(ρ - σ) + (P ρ - P σ))‖ := by rw [hsplit]
      _ ≤ ‖ρ - P ρ‖ + ‖-(ρ - σ) + (P ρ - P σ)‖ := norm_add_le _ _
      _ ≤ ‖ρ - P ρ‖ + (‖-(ρ - σ)‖ + ‖P ρ - P σ‖) := by
        exact add_le_add_right (norm_add_le (-(ρ - σ)) (P ρ - P σ)) _
      _ = ‖ρ - P ρ‖ + (‖ρ - σ‖ + ‖P ρ - P σ‖) := by rw [norm_neg]
  have hexp : (1 + L) * ε = ε + L * ε := by ring
  simp only [C, ge_iff_le]
  linarith [hstep, h1, h2, hexp]

/--
**Part 1' — finiteness form (what Theorem 5.1 actually consumes).**

If `P` is `L`-Lipschitz on the segment `ρ–σ` (`‖P ρ − P σ‖ ≤ L · ‖ρ − σ‖`, `0 ≤ L`), the defect
transfers with the FINITE constant `1 + L`. Theorem 5.1 only needs *some* finite transfer
constant, so it never needs the value of `L` — only that `P` is Lipschitz with finite `L`.
No trace-norm or tensor facts are required.
-/
theorem transfer_of_lipschitz (P : E → E) {ρ σ : E} {ε L : ℝ}
    (h1 : ‖ρ - σ‖ ≤ ε) (hL : ‖P ρ - P σ‖ ≤ L * ‖ρ - σ‖) (hLnn : 0 ≤ L) :
    C P ρ ≥ C P σ - (1 + L) * ε := by
  refine transfer P h1 ?_
  calc ‖P ρ - P σ‖ ≤ L * ‖ρ - σ‖ := hL
    _ ≤ L * ε := mul_le_mul_of_nonneg_left h1 hLnn

end Abstract

/-! ## Part 2 — the product-of-marginals retraction, cross-space typed, `K_Π = 3` -/

section Product

variable {E EA EB : Type*}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup EA] [SeminormedAddCommGroup EB]

/--
**Trace-norm tensor sub-additivity — DERIVED, not assumed.**

From bilinearity of the tensor map `tens` (the two subtraction-distribution facts `hbilL`,
`hbilR`), norm-multiplicativity `‖tens a b‖ = ‖a‖·‖b‖` (`hmul`), and the **unit-trace
normalizations** `‖ρB‖ = 1`, `‖σA‖ = 1`, the cross term `tens σA ρB` telescopes to give
`‖tens ρA ρB − tens σA σB‖ ≤ ‖ρA − σA‖ + ‖ρB − σB‖`.

The two `= 1` hypotheses are exactly the normalization an unqualified sub-additivity assumption
would silently absorb (Schatten-1 multiplicativity gives `‖X‖₁·‖ρB‖₁`; you may drop the second
factor *only because* the marginals are normalized states).
-/
theorem tensor_subadd
    (tens : EA → EB → E)
    (hbilL : ∀ (a₁ a₂ : EA) (b : EB), tens (a₁ - a₂) b = tens a₁ b - tens a₂ b)
    (hbilR : ∀ (a : EA) (b₁ b₂ : EB), tens a (b₁ - b₂) = tens a b₁ - tens a b₂)
    (hmul : ∀ (a : EA) (b : EB), ‖tens a b‖ = ‖a‖ * ‖b‖)
    {ρA σA : EA} {ρB σB : EB} (hρB : ‖ρB‖ = 1) (hσA : ‖σA‖ = 1) :
    ‖tens ρA ρB - tens σA σB‖ ≤ ‖ρA - σA‖ + ‖ρB - σB‖ := by
  have hsplit : tens ρA ρB - tens σA σB
      = tens (ρA - σA) ρB + tens σA (ρB - σB) := by
    rw [hbilL, hbilR]; abel
  calc ‖tens ρA ρB - tens σA σB‖
      = ‖tens (ρA - σA) ρB + tens σA (ρB - σB)‖ := by rw [hsplit]
    _ ≤ ‖tens (ρA - σA) ρB‖ + ‖tens σA (ρB - σB)‖ := norm_add_le _ _
    _ = ‖ρA - σA‖ * ‖ρB‖ + ‖σA‖ * ‖ρB - σB‖ := by rw [hmul, hmul]
    _ = ‖ρA - σA‖ + ‖ρB - σB‖ := by rw [hρB, hσA]; ring

/--
**Part 2 — product-retraction transfer with `K_Π = 3` (cross-space typed, normalization explicit).**

The retraction is `P x = tens (mA x) (mB x)` (product of marginals `mA : E → EA`, `mB : E → EB`),
with the marginal defects typed in their OWN spaces `EA`, `EB`. From:
* partial-trace contractivity `hcA : ‖mA ρ − mA σ‖ ≤ ‖ρ − σ‖`, `hcB` (the true, easy direction),
* the DERIVED tensor sub-additivity (`tensor_subadd`), whose unit-trace inputs `hρB`, `hσA` are
  surfaced here as hypotheses,

`P` is 2-Lipschitz on the segment, and Part 1 gives `C P ρ ≥ C P σ − 3·ε` (`K_Π = 1 + 2 = 3`).
-/
theorem transfer_product_KPi_three
    (tens : EA → EB → E) (mA : E → EA) (mB : E → EB) (P : E → E)
    (hP : ∀ x, P x = tens (mA x) (mB x))
    (hbilL : ∀ (a₁ a₂ : EA) (b : EB), tens (a₁ - a₂) b = tens a₁ b - tens a₂ b)
    (hbilR : ∀ (a : EA) (b₁ b₂ : EB), tens a (b₁ - b₂) = tens a b₁ - tens a b₂)
    (hmul : ∀ (a : EA) (b : EB), ‖tens a b‖ = ‖a‖ * ‖b‖)
    {ρ σ : E} {ε : ℝ}
    (h1 : ‖ρ - σ‖ ≤ ε)
    (hcA : ‖mA ρ - mA σ‖ ≤ ‖ρ - σ‖)        -- partial-trace contractivity, marginal A
    (hcB : ‖mB ρ - mB σ‖ ≤ ‖ρ - σ‖)        -- partial-trace contractivity, marginal B
    (hρB : ‖mB ρ‖ = 1) (hσA : ‖mA σ‖ = 1) : -- unit traces (normalization, made explicit)
    C P ρ ≥ C P σ - 3 * ε := by
  have hsub : ‖tens (mA ρ) (mB ρ) - tens (mA σ) (mB σ)‖
      ≤ ‖mA ρ - mA σ‖ + ‖mB ρ - mB σ‖ :=
    tensor_subadd tens hbilL hbilR hmul hρB hσA
  have hLip : ‖P ρ - P σ‖ ≤ 2 * ε := by
    rw [hP ρ, hP σ]
    linarith [hsub, hcA, hcB, h1]
  have h := transfer P h1 hLip
  have h3 : (1 + 2 : ℝ) * ε = 3 * ε := by ring
  linarith [h, h3]

end Product

end ProjectionTransfer

-- Axiom audit (added v6.3 Zenodo-preparation pass, 2026-08-31): this file now
-- carries its own trailing report, because the aggregator po000_axiom_audit.lean
-- imports sibling modules by name and therefore has no standalone green build.
#print axioms ProjectionTransfer.transfer
#print axioms ProjectionTransfer.transfer_of_lipschitz
#print axioms ProjectionTransfer.tensor_subadd
#print axioms ProjectionTransfer.transfer_product_KPi_three
