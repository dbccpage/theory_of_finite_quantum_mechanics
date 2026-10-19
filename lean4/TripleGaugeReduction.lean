import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.ContinuousMap.Basic
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Order.MonotoneContinuity
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FinCases
import BasisExtensionObstruction
import ExtensionCurvatureObstruction
import TripleExtensionAssembly
/-!
# D1: the U(d) gauge action on MU triples and the normalization reduction

This is the first symmetry-reduction step (D1) of the MUB(d) ≤ 3 attack, built on the
ASSEMBLY reduction (`MUB.TripleExtensionAssembly`). It mechanizes:

* `gaugeSmul V T` — the action of `U(d)` on an MU triple by left-multiplying every
  basis by a fixed unitary `V` (well-defined: pairwise unbiasedness is preserved).
* `psiVal_gaugeSmul` — **the basis-level obstruction `psiVal` is gauge-invariant**:
  `psiVal (gaugeSmul V T) = psiVal T`. (This discharges the gauge-invariance claim the
  ASSEMBLY only asserted.)
* `no_four_mub_of_psiVal_pos_normalized` — **the normalization reduction**: every MU
  triple is gauge-equivalent (via `V = star T₀`) to one whose first basis is the
  identity, so it suffices to verify `psiVal > 0` on the *normalized slice* (first
  basis standard). This formally reduces the cover obligation from all of `𝒯` to the
  Hadamard slice (the domain of D2), removing the 30-real-dimensional `U(d)` gauge.

All declarations are axiom-clean (`[propext, Classical.choice, Quot.sound]`, no `sorry`).

## Firewall (honest scope)

This is a *symmetry reduction*, not a solution of MUB(6) ≤ 3. It shrinks the open core
(the positivity hypothesis of the ASSEMBLY) to a transversal; it does not produce a
cover. The *discrete* Weyl–Heisenberg/Clifford reduction (a further fundamental-domain
quotient) and the transversal construction remain follow-up work. `psiVal` is a
diagnostic; it mints no authority.
-/

open Matrix Metric
open MUB.BasisExtensionObstruction
open MUB.ExtensionCurvatureObstruction
open MUB.TripleExtensionAssembly

namespace MUB.TripleGaugeReduction

variable {d : ℕ}

/-- The gram entry `∑ₖ conj(Aₖᵢ)·Bₖⱼ` as a matrix product entry `(Aᴴ·B)ᵢⱼ`. -/
theorem gram_as_mul (A B : Matrix (Fin d) (Fin d) ℂ) (i j : Fin d) :
    (∑ k, (starRingEnd ℂ) (A k i) * B k j) = (Aᴴ * B) i j := by
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, starRingEnd_apply]

/-- `Vᴴ V = 1` cancels a common left factor in a gram product. -/
theorem conjT_mul_left_cancel (Vm Am Bm : Matrix (Fin d) (Fin d) ℂ) (h : Vmᴴ * Vm = 1) :
    (Vm * Am)ᴴ * (Vm * Bm) = Amᴴ * Bm := by
  rw [Matrix.conjTranspose_mul, mul_assoc, ← mul_assoc Vmᴴ Vm Bm, h, one_mul]

/-- Left-multiplying every basis by a fixed unitary `V` preserves pairwise-MU. -/
theorem pairwiseMU_gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) {T} (hT : pairwiseMU T) :
    pairwiseMU (fun a => V * T a) := by
  intro a b hab i j
  have hVV : (V : Matrix (Fin d) (Fin d) ℂ)ᴴ * (V : Matrix (Fin d) (Fin d) ℂ) = 1 := by
    rw [← Matrix.star_eq_conjTranspose]; exact Unitary.coe_star_mul_self V
  have hmat : ((V * T a : Matrix (Fin d) (Fin d) ℂ)ᴴ * (V * T b : Matrix (Fin d) (Fin d) ℂ))
            = ((T a : Matrix (Fin d) (Fin d) ℂ)ᴴ * (T b : Matrix (Fin d) (Fin d) ℂ)) :=
    conjT_mul_left_cancel (V : Matrix (Fin d) (Fin d) ℂ) (T a : Matrix (Fin d) (Fin d) ℂ)
      (T b : Matrix (Fin d) (Fin d) ℂ) hVV
  show ‖∑ k, (starRingEnd ℂ) ((V * T a : Matrix (Fin d) (Fin d) ℂ) k i)
          * (V * T b : Matrix (Fin d) (Fin d) ℂ) k j‖ ^ 2 = 1 / (d : ℝ)
  rw [gram_as_mul, hmat,
    ← gram_as_mul (T a : Matrix (Fin d) (Fin d) ℂ) (T b : Matrix (Fin d) (Fin d) ℂ) i j]
  exact hT a b hab i j

/-- The gauge action of `U(d)` on MU triples: left-multiply each basis by `V`. -/
def gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d) : MUTriple d :=
  ⟨fun a => V * T.val a, pairwiseMU_gaugeSmul V T.2⟩

theorem toFlat_gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d) (i k) :
    (gaugeSmul V T).toFlat i k
      = ∑ m, (V : Matrix (Fin d) (Fin d) ℂ) k m * T.toFlat i m := by
  simp only [MUTriple.toFlat, gaugeSmul, Matrix.UnitaryGroup.mul_val, Matrix.mul_apply]

/-- `overlap` as a matrix product: conjugate the fixed vectors, multiply by `U`. -/
theorem overlap_eq_mul (e : Fin (3 * d) → Fin d → ℂ) (U : Matrix.unitaryGroup (Fin d) ℂ)
    (i : Fin (3 * d)) (j : Fin d) :
    overlap e U i j
      = (Matrix.map (Matrix.of e) (starRingEnd ℂ) * (U : Matrix (Fin d) (Fin d) ℂ)) i j := by
  simp only [overlap, Matrix.mul_apply, Matrix.map_apply, Matrix.of_apply]

/-- The gauge action is right-multiplication of the (matrix of) fixed vectors by `Vᵀ`. -/
theorem toFlat_gaugeSmul_mat (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d) :
    Matrix.of ((gaugeSmul V T).toFlat)
      = Matrix.of (T.toFlat) * (V : Matrix (Fin d) (Fin d) ℂ)ᵀ := by
  ext i k
  rw [Matrix.of_apply, toFlat_gaugeSmul, Matrix.mul_apply]
  refine Finset.sum_congr rfl (fun m _ => ?_)
  rw [Matrix.of_apply, Matrix.transpose_apply]; ring

/-- Conjugate-transpose as the conjugate of the transpose. -/
theorem map_conj_transpose_eq (W : Matrix (Fin d) (Fin d) ℂ) :
    Matrix.map (Wᵀ) (starRingEnd ℂ) = Wᴴ := by
  ext a b
  simp only [Matrix.map_apply, Matrix.transpose_apply, Matrix.conjTranspose_apply, starRingEnd_apply]

/-- **Overlap invariance.** Left-multiplying the fixed vectors by `V` is absorbed by
moving `star V` onto the candidate basis. -/
theorem overlap_gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d)
    (U : Matrix.unitaryGroup (Fin d) ℂ) (i : Fin (3 * d)) (j : Fin d) :
    overlap ((gaugeSmul V T).toFlat) U i j = overlap T.toFlat (star V * U) i j := by
  have hM : Matrix.map (Matrix.of ((gaugeSmul V T).toFlat)) (starRingEnd ℂ)
              * (U : Matrix (Fin d) (Fin d) ℂ)
            = Matrix.map (Matrix.of (T.toFlat)) (starRingEnd ℂ)
              * ((star V * U : Matrix.unitaryGroup (Fin d) ℂ) : Matrix (Fin d) (Fin d) ℂ) := by
    rw [toFlat_gaugeSmul_mat, Matrix.map_mul, map_conj_transpose_eq, Matrix.mul_assoc]
    rfl
  rw [overlap_eq_mul, overlap_eq_mul, hM]

/-- The deviation mass transforms by the same `star V` shift. -/
theorem basisDeviation_gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d)
    (U : Matrix.unitaryGroup (Fin d) ℂ) :
    basisDeviation ((gaugeSmul V T).toFlat) U = basisDeviation T.toFlat (star V * U) := by
  simp only [basisDeviation, overlap_gaugeSmul]

/-- **D1 (gauge invariance).** `psiVal` is invariant under the `U(d)` gauge action.
This discharges the gauge-invariance claim used (asserted) by the ASSEMBLY. -/
theorem psiVal_gaugeSmul (V : Matrix.unitaryGroup (Fin d) ℂ) (T : MUTriple d) :
    psiVal (gaugeSmul V T) = psiVal T := by
  rw [psiVal, psiVal, phi_eq_sInf, phi_eq_sInf]
  congr 1
  ext r
  constructor
  · rintro ⟨U, -, rfl⟩
    exact ⟨star V * U, Set.mem_univ _, (basisDeviation_gaugeSmul V T U).symm⟩
  · rintro ⟨U, -, rfl⟩
    refine ⟨V * U, Set.mem_univ _, ?_⟩
    rw [show (Psi_basis (gaugeSmul V T).toFlat).mass = basisDeviation (gaugeSmul V T).toFlat from rfl,
      basisDeviation_gaugeSmul]
    congr 1
    rw [← mul_assoc, Unitary.star_mul_self, one_mul]

/-- **D1 (normalization reduction).** Every MU triple is gauge-equivalent to one whose
first basis is the identity (`V = star T₀`), so it suffices to verify positivity on the
normalized slice (first basis standard) — the Hadamard slice the cover lives on. This
removes the continuous `U(d)` gauge from the open core of the ASSEMBLY. -/
theorem no_four_mub_of_psiVal_pos_normalized
    (h : ∀ T : MUTriple d, T.val 0 = 1 → 0 < psiVal T) : ¬ FourMUB d := by
  apply no_four_mub_of_psiVal_pos
  intro T
  have hfst : (gaugeSmul (star (T.val 0)) T).val 0 = 1 := by
    show star (T.val 0) * T.val 0 = 1
    exact Unitary.star_mul_self (T.val 0)
  have hpos := h (gaugeSmul (star (T.val 0)) T) hfst
  rwa [psiVal_gaugeSmul] at hpos

/-! ### The d = 6 instance -/

/-- **The d = 6 normalization reduction.** It suffices to verify `psiVal > 0` on MU
triples of ℂ⁶ whose first basis is the standard basis. -/
theorem no_four_mub6_of_psiVal_pos_normalized
    (h : ∀ T : MUTriple6, T.val 0 = 1 → 0 < psiVal T) : ¬ FourMUB6 :=
  no_four_mub_of_psiVal_pos_normalized h

end MUB.TripleGaugeReduction

#print axioms MUB.TripleGaugeReduction.psiVal_gaugeSmul
#print axioms MUB.TripleGaugeReduction.no_four_mub_of_psiVal_pos_normalized
#print axioms MUB.TripleGaugeReduction.no_four_mub6_of_psiVal_pos_normalized
