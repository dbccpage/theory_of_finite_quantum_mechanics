import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# A quantitative invertible minor for a three-row frame

AuthorityEffect: None.

The finite Cauchy--Binet identity is checked as a polynomial identity. For
three rows with Gram matrix 6I, it gives an actual minor with squared
determinant at least 54/5. This is not a finite-fibre or nonextension result.
-/

namespace MUB.MinorChart
open scoped BigOperators Matrix

def columns : Fin 20 → Fin 3 → Fin 6 := ![
  ![0,1,2], ![0,1,3], ![0,1,4], ![0,1,5],
  ![0,2,3], ![0,2,4], ![0,2,5], ![0,3,4], ![0,3,5], ![0,4,5],
  ![1,2,3], ![1,2,4], ![1,2,5], ![1,3,4], ![1,3,5], ![1,4,5],
  ![2,3,4], ![2,3,5], ![2,4,5], ![3,4,5]]

def minor (A : Matrix (Fin 3) (Fin 6) ℂ) (s : Fin 20) :
    Matrix (Fin 3) (Fin 3) ℂ := A.submatrix id (columns s)

theorem columns_injective (s : Fin 20) : Function.Injective (columns s) := by
  revert s
  decide

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
theorem cauchy_binet_3_6 (A : Matrix (Fin 3) (Fin 6) ℂ) :
    ((∑ s : Fin 20, Complex.normSq (minor A s).det) : ℂ) =
      (A * A.conjTranspose).det := by
  simp only [Complex.normSq_eq_conj_mul_self]
  norm_num [minor, columns, Matrix.det_fin_three, Matrix.submatrix_apply,
    Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ,
    Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons]
  ring

theorem minor_norm_sum (A : Matrix (Fin 3) (Fin 6) ℂ)
    (hA : A * A.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ)) :
    (∑ s : Fin 20, Complex.normSq (minor A s).det) = 216 := by
  have h := cauchy_binet_3_6 A
  rw [hA] at h
  norm_num [Matrix.det_smul] at h
  have hr := congrArg Complex.re h
  simpa [Fin.sum_univ_succ] using hr

theorem exists_minor_norm_ge (A : Matrix (Fin 3) (Fin 6) ℂ)
    (hA : A * A.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ)) :
    ∃ s : Fin 20, (54 / 5 : ℝ) ≤ Complex.normSq (minor A s).det := by
  by_contra! h
  have hsum : (∑ s : Fin 20, Complex.normSq (minor A s).det) <
      ∑ _s : Fin 20, (54 / 5 : ℝ) :=
    Finset.sum_lt_sum (fun s _ => (h s).le) ⟨0, Finset.mem_univ _, h 0⟩
  rw [minor_norm_sum A hA] at hsum
  norm_num at hsum

def firstRows (H : Matrix (Fin 6) (Fin 6) ℂ) : Matrix (Fin 3) (Fin 6) ℂ :=
  H.submatrix (Fin.castAdd 3) id

theorem firstRows_gram (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : H * H.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 6) (Fin 6) ℂ)) :
    firstRows H * (firstRows H).conjTranspose =
      (6 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
  simp only [firstRows, Matrix.conjTranspose_submatrix]
  change H.submatrix (Fin.castAdd 3) (Equiv.refl (Fin 6)) *
    H.conjTranspose.submatrix (Equiv.refl (Fin 6)) (Fin.castAdd 3) = _
  rw [Matrix.submatrix_mul_equiv H H.conjTranspose (Fin.castAdd 3)
    (Equiv.refl (Fin 6)) (Fin.castAdd 3), hH]
  ext i j
  simp [Matrix.submatrix_apply, Matrix.smul_apply, Matrix.one_apply, Fin.ext_iff]

theorem exists_invertible_minor (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : H * H.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 6) (Fin 6) ℂ)) :
    ∃ s : Fin 20, (54 / 5 : ℝ) ≤ Complex.normSq (minor (firstRows H) s).det ∧
      IsUnit (minor (firstRows H) s).det := by
  obtain ⟨s, hs⟩ := exists_minor_norm_ge (firstRows H) (firstRows_gram H hH)
  refine ⟨s, hs, isUnit_iff_ne_zero.mpr ?_⟩
  intro hz
  norm_num [hz] at hs

theorem unit_difference_normSq_le (z w : ℂ)
    (hz : Complex.normSq z = 1) (hw : Complex.normSq w = 1) :
    Complex.normSq (z - w) ≤ 4 := by
  have h := Complex.normSq_nonneg (z + w)
  rw [Complex.normSq_add, hz, hw] at h
  rw [Complex.normSq_sub, hz, hw]
  linarith

theorem adjugate_entry_normSq_le (B : Matrix (Fin 3) (Fin 3) ℂ)
    (hB : ∀ i j, Complex.normSq (B i j) = 1) (i j : Fin 3) :
    Complex.normSq (B.adjugate i j) ≤ 4 := by
  fin_cases i <;> fin_cases j <;>
    simp only [Matrix.adjugate_fin_three, Matrix.of_apply, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons,
      neg_add_eq_sub]
  all_goals apply unit_difference_normSq_le <;> simp [Complex.normSq_mul, hB]

theorem inverse_entry_normSq_le (B : Matrix (Fin 3) (Fin 3) ℂ)
    (hB : ∀ i j, Complex.normSq (B i j) = 1)
    (hdet : (54 / 5 : ℝ) ≤ Complex.normSq B.det) (i j : Fin 3) :
    Complex.normSq (B⁻¹ i j) ≤ 10 / 27 := by
  have hd : 0 < Complex.normSq B.det := lt_of_lt_of_le (by norm_num) hdet
  have ha := adjugate_entry_normSq_le B hB i j
  rw [Matrix.inv_def, Ring.inverse_eq_inv, Matrix.smul_apply, smul_eq_mul,
    Complex.normSq_mul, Complex.normSq_inv, mul_comm, ← div_eq_mul_inv]
  apply (div_le_iff₀ hd).mpr
  nlinarith

theorem exists_bounded_inverse_minor (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hunit : ∀ i j, Complex.normSq (H i j) = 1)
    (hH : H * H.conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 6) (Fin 6) ℂ)) :
    ∃ s : Fin 20, (54 / 5 : ℝ) ≤ Complex.normSq (minor (firstRows H) s).det ∧
      IsUnit (minor (firstRows H) s).det ∧
      ∀ i j, Complex.normSq ((minor (firstRows H) s)⁻¹ i j) ≤ 10 / 27 := by
  obtain ⟨s, hs, hdet⟩ := exists_invertible_minor H hH
  refine ⟨s, hs, hdet, inverse_entry_normSq_le _ ?_ hs⟩
  intro i j
  exact hunit _ _

#print axioms columns_injective
#print axioms cauchy_binet_3_6
#print axioms minor_norm_sum
#print axioms exists_minor_norm_ge
#print axioms firstRows_gram
#print axioms exists_invertible_minor
#print axioms unit_difference_normSq_le
#print axioms adjugate_entry_normSq_le
#print axioms inverse_entry_normSq_le
#print axioms exists_bounded_inverse_minor
end MUB.MinorChart
