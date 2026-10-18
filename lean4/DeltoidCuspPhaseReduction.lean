import DeltoidCuspInputAudit

/-!
# Generic phase and normalization reductions for literal overlap equations

These lemmas preserve the displayed row-amplitude equations under a common
unit phase and convert coordinate norm squares `1/6` to `1`. They do not
identify a cusp matrix or establish Hadamardness of any supplied matrix.

AuthorityEffect: None.
-/

namespace MUB.DeltoidCuspPhaseReduction

open scoped BigOperators
noncomputable section

def rowAmplitude (H : Matrix (Fin 6) (Fin 6) ℂ) (z : Fin 6 → ℂ)
    (i : Fin 6) : ℂ :=
  ∑ k : Fin 6, star (H i k) * z k

theorem rowAmplitude_scale (H : Matrix (Fin 6) (Fin 6) ℂ)
    (z : Fin 6 → ℂ) (c : ℂ) (i : Fin 6) :
    rowAmplitude H (fun k => c * z k) i = c * rowAmplitude H z i := by
  unfold rowAmplitude
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  ring

def dephase (z : Fin 6 → ℂ) : Fin 6 → ℂ :=
  fun k => star (z 0) * z k

theorem dephase_zero (z : Fin 6 → ℂ) (hzero : Complex.normSq (z 0) = 1) :
    dephase z 0 = 1 := by
  simp only [dephase, Complex.star_def]
  rw [mul_comm, Complex.mul_conj, hzero]
  rfl

theorem dephase_normSq (z : Fin 6 → ℂ) (hzero : Complex.normSq (z 0) = 1)
    (k : Fin 6) : Complex.normSq (dephase z k) = Complex.normSq (z k) := by
  simp only [dephase, Complex.normSq_mul, Complex.star_def, Complex.normSq_conj,
    hzero, one_mul]

theorem dephase_unit (z : Fin 6 → ℂ) (hunit : ∀ k, Complex.normSq (z k) = 1) :
    ∀ k, Complex.normSq (dephase z k) = 1 := by
  intro k
  rw [dephase_normSq z (hunit 0) k, hunit k]

theorem dephase_rowAmplitude_normSq (H : Matrix (Fin 6) (Fin 6) ℂ)
    (z : Fin 6 → ℂ) (hzero : Complex.normSq (z 0) = 1) (i : Fin 6) :
    Complex.normSq (rowAmplitude H (dephase z) i) =
      Complex.normSq (rowAmplitude H z i) := by
  unfold dephase
  rw [rowAmplitude_scale, Complex.normSq_mul]
  simp only [Complex.star_def, Complex.normSq_conj, hzero, one_mul]

def scaleBySqrtSix (u : Fin 6 → ℂ) : Fin 6 → ℂ :=
  fun k => (Real.sqrt 6 : ℂ) * u k

theorem sqrtSix_normSq : Complex.normSq (Real.sqrt 6 : ℂ) = 6 := by
  rw [Complex.normSq_ofReal]
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 6 by norm_num)]

theorem scaleBySqrtSix_unit (u : Fin 6 → ℂ)
    (hunit : ∀ k, Complex.normSq (u k) = 1 / 6) :
    ∀ k, Complex.normSq (scaleBySqrtSix u k) = 1 := by
  intro k
  rw [scaleBySqrtSix, Complex.normSq_mul, sqrtSix_normSq, hunit k]
  norm_num

theorem scaleBySqrtSix_rowAmplitude_normSq (H : Matrix (Fin 6) (Fin 6) ℂ)
    (u : Fin 6 → ℂ) (i : Fin 6) :
    Complex.normSq (rowAmplitude H (scaleBySqrtSix u) i) =
      6 * Complex.normSq (rowAmplitude H u i) := by
  unfold scaleBySqrtSix
  rw [rowAmplitude_scale, Complex.normSq_mul, sqrtSix_normSq]

theorem scaleBySqrtSix_overlaps (H : Matrix (Fin 6) (Fin 6) ℂ)
    (u : Fin 6 → ℂ) (hoverlaps : ∀ i, Complex.normSq (rowAmplitude H u i) = 1) :
    ∀ i, Complex.normSq (rowAmplitude H (scaleBySqrtSix u) i) = 6 := by
  intro i
  rw [scaleBySqrtSix_rowAmplitude_normSq, hoverlaps i]
  norm_num

#print axioms rowAmplitude_scale
#print axioms dephase_zero
#print axioms dephase_normSq
#print axioms dephase_unit
#print axioms dephase_rowAmplitude_normSq
#print axioms sqrtSix_normSq
#print axioms scaleBySqrtSix_unit
#print axioms scaleBySqrtSix_rowAmplitude_normSq
#print axioms scaleBySqrtSix_overlaps

end
end MUB.DeltoidCuspPhaseReduction
