import DeltoidCuspInputAudit
import LiteralCuspCertificate

/-!
# Semantic bridge for the literal input certificate

These theorems concern the displayed matrix `DeltoidCuspInputAudit.D6`.
That matrix fails the Hadamard condition. No cusp-family identification follows.

AuthorityEffect: None.
-/

namespace MUB.DeltoidCuspLiteralSemantics

open DeltoidCuspInputAudit
open MUB6.LiteralCuspCertificate
open scoped BigOperators
noncomputable section
set_option linter.unusedSimpArgs false
set_option maxRecDepth 100000
set_option maxHeartbeats 1000000

def phaseVector (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) : Fin 6 → ℂ :=
  ![1, ⟨x2, Real.sqrt 3 * t2⟩, ⟨x3, Real.sqrt 3 * t3⟩,
    ⟨x4, Real.sqrt 3 * t4⟩, ⟨x5, Real.sqrt 3 * t5⟩, ⟨x6, Real.sqrt 3 * t6⟩]

def rowAmplitude (H : Matrix (Fin 6) (Fin 6) ℂ) (z : Fin 6 → ℂ) (i : Fin 6) : ℂ :=
  ∑ k : Fin 6, star (H i k) * z k

private theorem F6_mod (i j : Fin 6) :
    F6 i j = omega ^ ((i.val * j.val) % 6) :=
  pow_eq_pow_mod _ omega_six

private theorem sqrt_three_squared : Real.sqrt 3 ^ 2 = 3 :=
  Real.sq_sqrt (by norm_num)

private theorem sqrt_three_fourth : Real.sqrt 3 ^ 4 = 9 := by
  rw [show Real.sqrt 3 ^ 4 = (Real.sqrt 3 ^ 2) ^ 2 by ring,
    sqrt_three_squared]
  norm_num

private theorem sqrt_three_6 : Real.sqrt 3 ^ 6 = 3 ^ 3 := by
  rw [show Real.sqrt 3 ^ 6 = (Real.sqrt 3 ^ 2) ^ 3 by ring, sqrt_three_squared]

private theorem sqrt_three_8 : Real.sqrt 3 ^ 8 = 3 ^ 4 := by
  rw [show Real.sqrt 3 ^ 8 = (Real.sqrt 3 ^ 2) ^ 4 by ring, sqrt_three_squared]

private theorem sqrt_three_10 : Real.sqrt 3 ^ 10 = 3 ^ 5 := by
  rw [show Real.sqrt 3 ^ 10 = (Real.sqrt 3 ^ 2) ^ 5 by ring, sqrt_three_squared]

private theorem sqrt_three_12 : Real.sqrt 3 ^ 12 = 3 ^ 6 := by
  rw [show Real.sqrt 3 ^ 12 = (Real.sqrt 3 ^ 2) ^ 6 by ring, sqrt_three_squared]

theorem source0_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source0 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 1) - 1 := by
  change source0 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 =
    Complex.normSq (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) - 1
  norm_num [source0, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source1_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source1 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 2) - 1 := by
  change source1 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 =
    Complex.normSq (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) - 1
  norm_num [source1, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source2_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source2 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 3) - 1 := by
  change source2 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 =
    Complex.normSq (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) - 1
  norm_num [source2, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source3_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source3 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 4) - 1 := by
  change source3 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 =
    Complex.normSq (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) - 1
  norm_num [source3, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source4_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source4 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 5) - 1 := by
  change source4 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 =
    Complex.normSq (⟨x6, Real.sqrt 3 * t6⟩ : ℂ) - 1
  norm_num [source4, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source5_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source5 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 0) - 6 := by
  norm_num [source5, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source6_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source6 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 1) - 6 := by
  norm_num [source6, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source7_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source7 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 2) - 6 := by
  norm_num [source7, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source8_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source8 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 3) - 6 := by
  norm_num [source8, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source9_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source9 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 4) - 6 := by
  norm_num [source9, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source10_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source10 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 5) - 6 := by
  norm_num [source10, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source11_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source11 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 0) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source11 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 0) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 0) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 0) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 0) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 0) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source11, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source12_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source12 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 1) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source12 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 0) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 2) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 4) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 5) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 1) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source12, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source13_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source13 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 2) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source13 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 2) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 0) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 5) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 1) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 4) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source13, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source14_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source14 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 3) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source14 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 4) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 5) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 0) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 2) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 1) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source14, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source15_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source15 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 4) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source15 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 5) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 1) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 2) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 0) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 4) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source15, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

theorem source16_semantics (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ) :
    source16 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) 5) - 6 := by
  simp only [rowAmplitude, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero]
  change source16 x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 = Complex.normSq
    (star (omega ^ 0) * 1 + (star (omega ^ 1) * (⟨x2, Real.sqrt 3 * t2⟩ : ℂ) + (star (omega ^ 4) * (⟨x3, Real.sqrt 3 * t3⟩ : ℂ) + (star (omega ^ 1) * (⟨x4, Real.sqrt 3 * t4⟩ : ℂ) + (star (omega ^ 4) * (⟨x5, Real.sqrt 3 * t5⟩ : ℂ) + (star (omega ^ 0) * (⟨x6, Real.sqrt 3 * t6⟩ : ℂ))))))) - 6
  simp only [omega_sq, omega_cube, omega_four, omega_five, pow_zero, pow_one]
  norm_num [source16, rowAmplitude, phaseVector, F6_mod, D6, suppliedExponents,
    Fin.sum_univ_succ, Matrix.cons_val, omega, Complex.normSq_apply, Complex.star_def, pow_succ] <;>
    (try ring_nf) <;>
    norm_num [sqrt_three_squared, sqrt_three_fourth, sqrt_three_6, sqrt_three_8, sqrt_three_10, sqrt_three_12] <;>
    ring

/-- The exact certificate applies to the concrete dephased phase vector. -/
theorem no_phaseVector (x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 : ℝ)
    (hunit : ∀ k, Complex.normSq (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6 k) = 1)
    (hfourier : ∀ i, Complex.normSq
      (rowAmplitude F6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) i) = 6)
    (hliteral : ∀ i, Complex.normSq
      (rowAmplitude D6 (phaseVector x2 t2 x3 t3 x4 t4 x5 t5 x6 t6) i) = 6) : False := by
  apply no_common_zero x2 t2 x3 t3 x4 t4 x5 t5 x6 t6
  · rw [source0_semantics, hunit]
    ring
  · rw [source1_semantics, hunit]
    ring
  · rw [source2_semantics, hunit]
    ring
  · rw [source3_semantics, hunit]
    ring
  · rw [source4_semantics, hunit]
    ring
  · rw [source5_semantics, hfourier]
    ring
  · rw [source6_semantics, hfourier]
    ring
  · rw [source7_semantics, hfourier]
    ring
  · rw [source8_semantics, hfourier]
    ring
  · rw [source9_semantics, hfourier]
    ring
  · rw [source10_semantics, hfourier]
    ring
  · rw [source11_semantics, hliteral]
    ring
  · rw [source12_semantics, hliteral]
    ring
  · rw [source13_semantics, hliteral]
    ring
  · rw [source14_semantics, hliteral]
    ring
  · rw [source15_semantics, hliteral]
    ring
  · rw [source16_semantics, hliteral]
    ring

private theorem reconstruct_coordinate (z : ℂ) :
    (⟨z.re, Real.sqrt 3 * (z.im / Real.sqrt 3)⟩ : ℂ) = z := by
  have hs : Real.sqrt 3 ≠ 0 := by positivity
  apply Complex.ext
  · rfl
  · change Real.sqrt 3 * (z.im / Real.sqrt 3) = z.im
    field_simp

theorem reconstruct_dephased_vector (z : Fin 6 → ℂ) (hzero : z 0 = 1) :
    phaseVector
      (z 1).re ((z 1).im / Real.sqrt 3)
      (z 2).re ((z 2).im / Real.sqrt 3)
      (z 3).re ((z 3).im / Real.sqrt 3)
      (z 4).re ((z 4).im / Real.sqrt 3)
      (z 5).re ((z 5).im / Real.sqrt 3) = z := by
  funext k
  fin_cases k <;> simp [phaseVector, reconstruct_coordinate, hzero]

/-- Empty literal overlap system with the global phase fixed to make entry zero one. -/
theorem no_dephased_literal_vector (z : Fin 6 → ℂ) (hzero : z 0 = 1)
    (hunit : ∀ k, Complex.normSq (z k) = 1)
    (hfourier : ∀ i, Complex.normSq (rowAmplitude F6 z i) = 6)
    (hliteral : ∀ i, Complex.normSq (rowAmplitude D6 z i) = 6) : False := by
  have hrebuild := reconstruct_dephased_vector z hzero
  apply no_phaseVector
    (z 1).re ((z 1).im / Real.sqrt 3)
    (z 2).re ((z 2).im / Real.sqrt 3)
    (z 3).re ((z 3).im / Real.sqrt 3)
    (z 4).re ((z 4).im / Real.sqrt 3)
    (z 5).re ((z 5).im / Real.sqrt 3)
  · simpa only [hrebuild] using hunit
  · simpa only [hrebuild] using hfourier
  · simpa only [hrebuild] using hliteral

#print axioms no_phaseVector
#print axioms reconstruct_dephased_vector
#print axioms no_dephased_literal_vector

end
end MUB.DeltoidCuspLiteralSemantics
