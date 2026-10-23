/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/LpWeakDuality.lean
   Original sha256: 9833a16848d053ad81129b65634afeb566ff0f48f766de532dacfd770d5b4c9c (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.LpWeakDuality
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Does not elaborate on the v4.34.0 package: that package does not depend on
Mathlib. The pinned Mathlib rev is `0df444a360eaa60ab8c11dca51a86af692955474`
on v4.33.1 (`research_programs/mub6`). This file was not typechecked
against that build. Declarations below were not typechecked.
-/
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Data.Matrix.Mul

/-!
# Paper 043, T7: ordered-field LP weak duality

This module discharges PL-043-1 for the maximum-form matrix convention recorded
in the Paper 043 ledger:

* primal feasibility: A *ᵥ x ≤ b and 0 ≤ x;
* dual feasibility: c ≤ A.transpose *ᵥ y and 0 ≤ y;
* conclusion: c ⬝ᵥ x ≤ b ⬝ᵥ y.

The proof is a finite rearrangement of sums and ordered-field inequalities. It
uses no completeness, topology, limits, strong duality, or optimizer existence.

Scope fence: this theorem does not by itself prove the distinct minimum/equality
convention A z = b, A.transpose *ᵥ y ≤ c, nor is a conversion between the two
conventions supplied here. It also does not prove the separate norm/dual-norm
weak-duality statement used for the Phi_1 bound.
-/

namespace PaperER007

open Matrix

/--
Weak duality for the Paper 043 maximum-form LP over an arbitrary
linearly ordered field. Current Mathlib expresses this unbundled as `Field`,
`LinearOrder`, and `IsStrictOrderedRing`.
-/
theorem lp_max_form_weak_duality
    {M N K : Type*}
    [Fintype M] [Fintype N]
    [Field K] [LinearOrder K] [IsStrictOrderedRing K]
    (A : Matrix M N K)
    (b : M → K) (c : N → K)
    (x : N → K) (y : M → K)
    (hAx_le_b : ∀ i : M, (A *ᵥ x) i ≤ b i)
    (hx_nonnegative : ∀ j : N, 0 ≤ x j)
    (hc_le_transpose_y : ∀ j : N, c j ≤ (A.transpose *ᵥ y) j)
    (hy_nonnegative : ∀ i : M, 0 ≤ y i) :
    c ⬝ᵥ x ≤ b ⬝ᵥ y := by
  have hDualBound : c ⬝ᵥ x ≤ (A.transpose *ᵥ y) ⬝ᵥ x := by
    simp only [dotProduct]
    exact Finset.sum_le_sum fun j _ =>
      mul_le_mul_of_nonneg_right (hc_le_transpose_y j) (hx_nonnegative j)
  have hPrimalBound : (A *ᵥ x) ⬝ᵥ y ≤ b ⬝ᵥ y := by
    simp only [dotProduct]
    exact Finset.sum_le_sum fun i _ =>
      mul_le_mul_of_nonneg_right (hAx_le_b i) (hy_nonnegative i)
  calc
    c ⬝ᵥ x ≤ (A.transpose *ᵥ y) ⬝ᵥ x := hDualBound
    _ = x ⬝ᵥ (A.transpose *ᵥ y) := dotProduct_comm _ _
    _ = (x ᵥ* A.transpose) ⬝ᵥ y := Matrix.dotProduct_mulVec x A.transpose y
    _ = (A *ᵥ x) ⬝ᵥ y := by rw [Matrix.vecMul_transpose]
    _ ≤ b ⬝ᵥ y := hPrimalBound

#print axioms PaperER007.lp_max_form_weak_duality

end PaperER007
