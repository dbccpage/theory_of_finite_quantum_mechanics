import Mathlib.Data.Complex.BigOperators
import Mathlib.Analysis.Real.Sqrt
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import ConcreteSemantics

/-!
# Exact audit of the literal matrix in the deltoid-cusp mission input

The `D6` below is the full exponent table supplied by the mission prompt. This
module checks that particular input; it does not identify a deltoid boundary
matrix or classify MUB triples. Its first two rows have inner product `2`, and
the normalized `F6` and `D6` share their first column. Consequently this `D6`
does not satisfy the repository's `ConcreteSemantics.IsCH6` predicate.

All constants and algebraic identities are exact. `omega` is represented by
its exact real and imaginary parts, using the positive square root of `3`.

AuthorityEffect: None.
-/

namespace MUB.DeltoidCuspInputAudit

open scoped BigOperators
noncomputable section

/-- Exact sixth root with real part `1/2` and imaginary part `sqrt(3)/2`. -/
def omega : ℂ := ⟨1 / 2, Real.sqrt 3 / 2⟩

/-- The complete exponent table, in zero-based row and column indexing. -/
def suppliedExponents : Matrix (Fin 6) (Fin 6) ℕ :=
  !![0, 0, 0, 0, 0, 0;
     0, 0, 2, 4, 5, 1;
     0, 2, 0, 5, 1, 4;
     0, 4, 5, 0, 2, 1;
     0, 5, 1, 2, 0, 4;
     0, 1, 4, 1, 4, 0]

/-- The literal matrix displayed in the mission prompt. -/
def D6 : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => omega ^ suppliedExponents i j

/-- The Fourier exponent convention used in the mission prompt. -/
def F6 : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => omega ^ (i.val * j.val)

theorem omega_sq : omega ^ 2 = omega - 1 := by
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  apply Complex.ext
  · simp only [pow_two, omega, Complex.mul_re, Complex.sub_re,
      Complex.one_re]
    nlinarith
  · simp only [pow_two, omega, Complex.mul_im, Complex.sub_im,
      Complex.one_im]
    ring

theorem omega_cube : omega ^ 3 = -1 := by
  calc
    omega ^ 3 = omega * omega ^ 2 := by ring
    _ = omega * (omega - 1) := by rw [omega_sq]
    _ = omega ^ 2 - omega := by ring
    _ = -1 := by rw [omega_sq]; ring

theorem omega_four : omega ^ 4 = -omega := by
  calc
    omega ^ 4 = omega ^ 3 * omega := by ring
    _ = -omega := by rw [omega_cube]; ring

theorem omega_five : omega ^ 5 = 1 - omega := by
  calc
    omega ^ 5 = omega ^ 3 * omega ^ 2 := by ring
    _ = 1 - omega := by rw [omega_cube, omega_sq]; ring

theorem omega_six : omega ^ 6 = 1 := by
  calc
    omega ^ 6 = (omega ^ 3) ^ 2 := by ring
    _ = 1 := by rw [omega_cube]; ring

@[simp] theorem D6_first_row (j : Fin 6) : D6 0 j = 1 := by
  fin_cases j <;> norm_num [D6, suppliedExponents]

@[simp] theorem D6_first_column (i : Fin 6) : D6 i 0 = 1 := by
  fin_cases i <;> norm_num [D6, suppliedExponents]

@[simp] theorem F6_first_row (j : Fin 6) : F6 0 j = 1 := by
  simp [F6]

@[simp] theorem F6_first_column (i : Fin 6) : F6 i 0 = 1 := by
  simp [F6]

theorem D6_first_two_row_inner_product :
    (∑ j : Fin 6, D6 0 j * star (D6 1 j)) = 2 := by
  have hs : (∑ j : Fin 6, D6 1 j) = 2 := by
    simp [D6, suppliedExponents, Fin.sum_univ_succ,
      omega_sq, omega_four, omega_five]
    ring
  simpa only [map_sum, map_ofNat, D6_first_row, one_mul, starRingEnd_apply] using
    congrArg (starRingEnd ℂ) hs

/-- The failed Gram-matrix entry connects the computation to full matrices. -/
theorem D6_gram_zero_one :
    (D6 * Matrix.conjTranspose D6) 0 1 = 2 := by
  simpa [Matrix.mul_apply, Matrix.conjTranspose_apply] using
    D6_first_two_row_inner_product

/-- The displayed matrix fails the repository's concrete Hadamard definition. -/
theorem supplied_D6_not_IsCH6 : ¬ ConcreteSemantics.IsCH6 D6 := by
  intro h
  have h01 := congrArg (fun H : Matrix (Fin 6) (Fin 6) ℂ => H 0 1) h.2
  rw [D6_gram_zero_one] at h01
  norm_num [Matrix.smul_apply, Matrix.one_apply] at h01

/-- Exact normalization by `sqrt(6)`, applied entrywise. -/
def normalize (H : Matrix (Fin 6) (Fin 6) ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => ((Real.sqrt 6)⁻¹ : ℝ) * H i j

/-- Column overlap of two matrices, with the first argument conjugated. -/
def columnOverlap (H K : Matrix (Fin 6) (Fin 6) ℂ) (i j : Fin 6) : ℂ :=
  ∑ k : Fin 6, star (H k i) * K k j

/-- Row overlap of two matrices, with the first argument conjugated. -/
def rowOverlap (H K : Matrix (Fin 6) (Fin 6) ℂ) (i j : Fin 6) : ℂ :=
  ∑ k : Fin 6, star (H i k) * K j k

private theorem sqrt_six_inverse_identity :
    6 * ((Real.sqrt 6)⁻¹ * (Real.sqrt 6)⁻¹) = 1 := by
  have hs : Real.sqrt 6 ≠ 0 := by positivity
  have hs2 : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  field_simp
  nlinarith

theorem normalized_first_column_overlap :
    columnOverlap (normalize F6) (normalize D6) 0 0 = 1 := by
  simp only [columnOverlap, normalize, F6_first_column, D6_first_column,
    mul_one, Complex.star_def, Complex.conj_ofReal]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  exact_mod_cast sqrt_six_inverse_identity

theorem normalized_first_row_overlap :
    rowOverlap (normalize F6) (normalize D6) 0 0 = 1 := by
  simp only [rowOverlap, normalize, F6_first_row, D6_first_row,
    mul_one, Complex.star_def, Complex.conj_ofReal]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  exact_mod_cast sqrt_six_inverse_identity

theorem normalized_first_column_overlap_squared :
    Complex.normSq (columnOverlap (normalize F6) (normalize D6) 0 0) = 1 := by
  rw [normalized_first_column_overlap]
  norm_num

theorem normalized_first_row_overlap_squared :
    Complex.normSq (rowOverlap (normalize F6) (normalize D6) 0 0) = 1 := by
  rw [normalized_first_row_overlap]
  norm_num

/-- This particular normalized pair fails the column mutual-unbiasedness equations. -/
theorem normalized_pair_not_column_unbiased :
    ¬ (∀ i j : Fin 6,
      Complex.normSq (columnOverlap (normalize F6) (normalize D6) i j) = 1 / 6) := by
  intro h
  have h00 := h 0 0
  rw [normalized_first_column_overlap_squared] at h00
  norm_num at h00

/-- The same failure holds under the row convention in the mission equations. -/
theorem normalized_pair_not_row_unbiased :
    ¬ (∀ i j : Fin 6,
      Complex.normSq (rowOverlap (normalize F6) (normalize D6) i j) = 1 / 6) := by
  intro h
  have h00 := h 0 0
  rw [normalized_first_row_overlap_squared] at h00
  norm_num at h00

#print axioms omega_sq
#print axioms omega_cube
#print axioms omega_four
#print axioms omega_five
#print axioms omega_six
#print axioms D6_first_two_row_inner_product
#print axioms D6_gram_zero_one
#print axioms supplied_D6_not_IsCH6
#print axioms normalized_first_column_overlap
#print axioms normalized_first_row_overlap
#print axioms normalized_first_column_overlap_squared
#print axioms normalized_first_row_overlap_squared
#print axioms normalized_pair_not_column_unbiased
#print axioms normalized_pair_not_row_unbiased

end
end MUB.DeltoidCuspInputAudit
