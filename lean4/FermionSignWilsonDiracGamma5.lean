import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Polynomial.Div
import Mathlib.Basic.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormDet

/-!
# FSP-WILSON-DIRAC-GAMMA5

AuthorityEffect: None.
Origin: lean4/FermionSignWilsonDiracGamma5.lean
Claim: Euclidean Clifford data for dimensions 2 and 4; equal algebraic
root multiplicities for a polynomial whose coefficients are fixed by
conjugation; the determinant of two repeated diagonal blocks is a square;
the square of a real complex number has imaginary part 0 and real part >= 0.
This module does not state gamma5 D gamma5 = D adjoint.
-/

open scoped BigOperators Kronecker
open Matrix Complex Polynomial

namespace FermionSignWilsonDiracGamma5

noncomputable section

/-! ## Clifford data -/

structure EuclideanClifford (d : ℕ) (Spin : Type*) [Fintype Spin] [DecidableEq Spin] where
  gamma : Fin d → Matrix Spin Spin ℂ
  gamma5 : Matrix Spin Spin ℂ
  gamma_herm : ∀ μ, (gamma μ)ᴴ = gamma μ
  gamma_anticomm :
    ∀ μ ν, gamma μ * gamma ν + gamma ν * gamma μ = if μ = ν then (2 : Matrix Spin Spin ℂ) else 0
  gamma5_herm : gamma5ᴴ = gamma5
  gamma5_sq : gamma5 * gamma5 = 1
  gamma5_anti : ∀ μ, gamma5 * gamma μ * gamma5 = -gamma μ

lemma half_selfAdjoint : star (1 / 2 : ℂ) = (1 / 2 : ℂ) := by simp

lemma neg_half_selfAdjoint : star (-(1 / 2 : ℂ)) = -(1 / 2 : ℂ) := by simp

def forwardSpin {Spin : Type*} [Fintype Spin] [DecidableEq Spin]
    (γ : Matrix Spin Spin ℂ) : Matrix Spin Spin ℂ :=
  (1 / 2 : ℂ) • (γ - 1)

def backwardSpin {Spin : Type*} [Fintype Spin] [DecidableEq Spin]
    (γ : Matrix Spin Spin ℂ) : Matrix Spin Spin ℂ :=
  (-(1 / 2 : ℂ)) • (γ + 1)

lemma forwardSpin_herm {Spin : Type*} [Fintype Spin] [DecidableEq Spin]
    {γ : Matrix Spin Spin ℂ} (hγ : γᴴ = γ) : (forwardSpin γ)ᴴ = forwardSpin γ := by
  unfold forwardSpin
  rw [conjTranspose_smul, half_selfAdjoint, conjTranspose_sub, hγ, conjTranspose_one]

lemma backwardSpin_herm {Spin : Type*} [Fintype Spin] [DecidableEq Spin]
    {γ : Matrix Spin Spin ℂ} (hγ : γᴴ = γ) : (backwardSpin γ)ᴴ = backwardSpin γ := by
  unfold backwardSpin
  rw [conjTranspose_smul, neg_half_selfAdjoint, conjTranspose_add, hγ, conjTranspose_one]

lemma gamma5_conj_forwardSpin {Spin : Type*} [Fintype Spin] [DecidableEq Spin]
    (γ5 γ : Matrix Spin Spin ℂ) (hanti : γ5 * γ * γ5 = -γ) (hsq : γ5 * γ5 = 1) :
    γ5 * forwardSpin γ * γ5 = backwardSpin γ := by
  unfold forwardSpin backwardSpin
  rw [Matrix.mul_smul, smul_mul]
  have hsub : γ5 * (γ - 1) * γ5 = -(γ + 1) := by
    calc
      γ5 * (γ - 1) * γ5 = (γ5 * γ - γ5 * 1) * γ5 := by rw [mul_sub]
      _ = γ5 * γ * γ5 - γ5 * 1 * γ5 := by rw [sub_mul]
      _ = γ5 * γ * γ5 - γ5 * γ5 := by simp [mul_one]
      _ = -γ - 1 := by rw [hanti, hsq]
      _ = -(γ + 1) := by simp [sub_eq_add_neg, neg_add, add_comm]
  rw [hsub, smul_neg, ← neg_smul]

/-! ## Checked representations: d = 2 and d = 4 -/

def gamma2d : Fin 2 → Matrix (Fin 2) (Fin 2) ℂ
  | 0 => !![0, 1; 1, 0]
  | 1 => !![1, 0; 0, -1]

def gamma5Two : Matrix (Fin 2) (Fin 2) ℂ := !![0, I; -I, 0]

lemma gamma2d_sq (μ : Fin 2) : gamma2d μ * gamma2d μ = 1 := by
  fin_cases μ <;>
    ext i j <;> fin_cases i <;> fin_cases j <;>
      simp [gamma2d, mul_apply, Fin.sum_univ_two, one_apply]

lemma gamma2d_herm (μ : Fin 2) : (gamma2d μ)ᴴ = gamma2d μ := by
  fin_cases μ <;>
    ext i j <;> fin_cases i <;> fin_cases j <;>
      simp [gamma2d, conjTranspose_apply]

lemma gamma2d_off : gamma2d 0 * gamma2d 1 + gamma2d 1 * gamma2d 0 = 0 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [gamma2d, mul_apply, Fin.sum_univ_two, Matrix.add_apply]

lemma gamma5Two_herm : gamma5Twoᴴ = gamma5Two := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [gamma5Two, conjTranspose_apply, star_def, conj_I, star_neg]

lemma gamma5Two_sq : gamma5Two * gamma5Two = 1 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [gamma5Two, mul_apply, Fin.sum_univ_two, one_apply, I_mul_I,
      ext_iff, mul_re, mul_im, I_re, I_im]

lemma gamma5Two_anti (μ : Fin 2) : gamma5Two * gamma2d μ * gamma5Two = -gamma2d μ := by
  fin_cases μ <;>
    ext i j <;> fin_cases i <;> fin_cases j <;>
      simp [gamma5Two, gamma2d, mul_apply, Fin.sum_univ_two, neg_apply, I_mul_I,
        ext_iff, mul_re, mul_im, I_re, I_im, add_assoc]

def euclideanClifford2 : EuclideanClifford 2 (Fin 2) where
  gamma := gamma2d
  gamma5 := gamma5Two
  gamma_herm := gamma2d_herm
  gamma_anticomm := by
    intro μ ν
    by_cases h : μ = ν
    · subst h
      simp [gamma2d_sq, two_smul, one_add_one_eq_two]
    · fin_cases μ <;> fin_cases ν <;> simp [h] at h ⊢ <;> simp [gamma2d_off, add_comm]
  gamma5_herm := gamma5Two_herm
  gamma5_sq := gamma5Two_sq
  gamma5_anti := gamma5Two_anti

def pauli1 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def pauli2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, -I; I, 0]
def pauli3 : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

lemma pauli1_sq : pauli1 * pauli1 = 1 := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [pauli1, mul_apply, Fin.sum_univ_two, one_apply]

lemma pauli3_sq : pauli3 * pauli3 = 1 := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [pauli3, mul_apply, Fin.sum_univ_two, one_apply]

lemma pauli2_sq : pauli2 * pauli2 = 1 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [pauli2, mul_apply, Fin.sum_univ_two, one_apply, I_mul_I, ext_iff,
      mul_re, mul_im, I_re, I_im]

lemma pauli1_herm : pauli1ᴴ = pauli1 := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [pauli1, conjTranspose_apply]

lemma pauli3_herm : pauli3ᴴ = pauli3 := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [pauli3, conjTranspose_apply, star_def, star_neg]

lemma pauli2_herm : pauli2ᴴ = pauli2 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [pauli2, conjTranspose_apply, star_def, conj_I, star_neg]

lemma pauli_anti_12 : pauli1 * pauli2 + pauli2 * pauli1 = 0 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [pauli1, pauli2, mul_apply, Fin.sum_univ_two, Matrix.add_apply, I_mul_I, ext_iff,
      mul_re, mul_im, I_re, I_im]

lemma pauli_anti_13 : pauli1 * pauli3 + pauli3 * pauli1 = 0 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [pauli1, pauli3, mul_apply, Fin.sum_univ_two, Matrix.add_apply]

lemma pauli_anti_23 : pauli2 * pauli3 + pauli3 * pauli2 = 0 := by
  ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [pauli2, pauli3, mul_apply, Fin.sum_univ_two, Matrix.add_apply, I_mul_I, ext_iff,
      mul_re, mul_im, I_re, I_im]

def offDirac (B C : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℂ :=
  fromBlocks 0 B C 0

lemma scalar_shift (σ τ : Matrix (Fin 2) (Fin 2) ℂ) :
    ((-I) • σ) * (I • τ) = σ * τ := by
  rw [smul_mul, Matrix.mul_smul, smul_smul]
  have hI : (-I) * I = (1 : ℂ) := by simp [neg_mul, I_mul_I]
  rw [hI, one_smul]

lemma scalar_shift' (σ τ : Matrix (Fin 2) (Fin 2) ℂ) :
    (I • σ) * ((-I) • τ) = σ * τ := by
  rw [smul_mul, Matrix.mul_smul, smul_smul]
  have hI : I * (-I) = (1 : ℂ) := by simp [mul_neg, I_mul_I]
  rw [hI, one_smul]

lemma offDirac_mul (B C B' C' : Matrix (Fin 2) (Fin 2) ℂ) :
    offDirac B C * offDirac B' C' = fromBlocks (B * C') 0 0 (C * B') := by
  simp [offDirac, fromBlocks_multiply, mul_zero, zero_mul, add_zero, zero_add]

lemma offDirac_sq_of (σ : Matrix (Fin 2) (Fin 2) ℂ) (hs : σ * σ = 1) :
    offDirac ((-I) • σ) (I • σ) * offDirac ((-I) • σ) (I • σ) = 1 := by
  rw [offDirac_mul, scalar_shift, scalar_shift', hs, fromBlocks_one]

lemma offDirac_anti_of (σ τ : Matrix (Fin 2) (Fin 2) ℂ)
    (h : σ * τ + τ * σ = 0) :
    offDirac ((-I) • σ) (I • σ) * offDirac ((-I) • τ) (I • τ)
      + offDirac ((-I) • τ) (I • τ) * offDirac ((-I) • σ) (I • σ) = 0 := by
  rw [offDirac_mul, offDirac_mul, fromBlocks_add, scalar_shift, scalar_shift,
    scalar_shift', scalar_shift']
  have h' : τ * σ + σ * τ = 0 := by simpa [add_comm] using h
  simp [h, h', fromBlocks_zero]

lemma temporal_sq : offDirac (1 : Matrix (Fin 2) (Fin 2) ℂ) 1 * offDirac 1 1 = 1 := by
  rw [offDirac_mul, mul_one, fromBlocks_one]

lemma spatial_temporal_anti (σ : Matrix (Fin 2) (Fin 2) ℂ) :
    offDirac ((-I) • σ) (I • σ) * offDirac 1 1
      + offDirac 1 1 * offDirac ((-I) • σ) (I • σ) = 0 := by
  rw [offDirac_mul, offDirac_mul, fromBlocks_add]
  have hsum : ((-I) • σ) + (I • σ) = 0 := by
    rw [← add_smul]
    simp
  have hsum' : (I • σ) + ((-I) • σ) = 0 := by simpa [add_comm] using hsum
  simp [mul_one, one_mul, hsum, hsum', fromBlocks_zero]

lemma offDirac_herm (σ : Matrix (Fin 2) (Fin 2) ℂ) (hσ : σᴴ = σ) :
    (offDirac ((-I) • σ) (I • σ))ᴴ = offDirac ((-I) • σ) (I • σ) := by
  simp only [offDirac, fromBlocks_conjTranspose, conjTranspose_zero, conjTranspose_smul, hσ,
    star_def, conj_I, star_neg]
  have hB : star (-I) • σ = I • σ := by simp [star_def, star_neg, conj_I, neg_neg]
  have hC : star I • σ = (-I) • σ := by simp [star_def, conj_I]
  simp [hB, hC]

lemma temporal_herm : (offDirac (1 : Matrix (Fin 2) (Fin 2) ℂ) 1)ᴴ = offDirac 1 1 := by
  simp [offDirac, fromBlocks_conjTranspose, conjTranspose_zero, conjTranspose_one]

def gamma5Four : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℂ :=
  fromBlocks (1 : Matrix (Fin 2) (Fin 2) ℂ) 0 0 (-1)

lemma gamma5Four_sq : gamma5Four * gamma5Four = 1 := by
  simp [gamma5Four, fromBlocks_multiply, mul_zero, zero_mul, one_mul, mul_one, add_zero, zero_add,
    neg_mul, mul_neg, neg_neg, fromBlocks_one]

lemma gamma5Four_herm : gamma5Fourᴴ = gamma5Four := by
  simp [gamma5Four, fromBlocks_conjTranspose, conjTranspose_zero, conjTranspose_one, conjTranspose_neg]

lemma gamma5Four_conj_off (B C : Matrix (Fin 2) (Fin 2) ℂ) :
    gamma5Four * offDirac B C * gamma5Four = -offDirac B C := by
  simp only [gamma5Four, offDirac]
  rw [fromBlocks_multiply]
  simp only [mul_zero, zero_mul, one_mul, mul_one, add_zero, zero_add, mul_neg, neg_mul, neg_zero]
  rw [fromBlocks_multiply]
  simp only [mul_zero, zero_mul, one_mul, mul_one, add_zero, zero_add, mul_neg, neg_mul, neg_zero,
    neg_neg]
  simp [fromBlocks_neg, neg_zero]

def gamma4d : Fin 4 → Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℂ
  | 0 => offDirac ((-I) • pauli1) (I • pauli1)
  | 1 => offDirac ((-I) • pauli2) (I • pauli2)
  | 2 => offDirac ((-I) • pauli3) (I • pauli3)
  | 3 => offDirac 1 1

lemma gamma4d_sq (μ : Fin 4) : gamma4d μ * gamma4d μ = 1 := by
  fin_cases μ
  · exact offDirac_sq_of _ pauli1_sq
  · exact offDirac_sq_of _ pauli2_sq
  · exact offDirac_sq_of _ pauli3_sq
  · simpa [gamma4d] using temporal_sq

lemma gamma4d_herm (μ : Fin 4) : (gamma4d μ)ᴴ = gamma4d μ := by
  fin_cases μ
  · simpa [gamma4d] using offDirac_herm _ pauli1_herm
  · simpa [gamma4d] using offDirac_herm _ pauli2_herm
  · simpa [gamma4d] using offDirac_herm _ pauli3_herm
  · simpa [gamma4d] using temporal_herm

lemma gamma4d_anti_pair :
    gamma4d 0 * gamma4d 1 + gamma4d 1 * gamma4d 0 = 0 ∧
    gamma4d 0 * gamma4d 2 + gamma4d 2 * gamma4d 0 = 0 ∧
    gamma4d 1 * gamma4d 2 + gamma4d 2 * gamma4d 1 = 0 ∧
    gamma4d 0 * gamma4d 3 + gamma4d 3 * gamma4d 0 = 0 ∧
    gamma4d 1 * gamma4d 3 + gamma4d 3 * gamma4d 1 = 0 ∧
    gamma4d 2 * gamma4d 3 + gamma4d 3 * gamma4d 2 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals first
    | simpa [gamma4d] using offDirac_anti_of _ _ pauli_anti_12
    | simpa [gamma4d] using offDirac_anti_of _ _ pauli_anti_13
    | simpa [gamma4d] using offDirac_anti_of _ _ pauli_anti_23
    | simpa [gamma4d] using spatial_temporal_anti pauli1
    | simpa [gamma4d] using spatial_temporal_anti pauli2
    | simpa [gamma4d] using spatial_temporal_anti pauli3

lemma gamma5Four_anti (μ : Fin 4) : gamma5Four * gamma4d μ * gamma5Four = -gamma4d μ := by
  fin_cases μ <;> simp only [gamma4d] <;> exact gamma5Four_conj_off _ _

def euclideanClifford4 : EuclideanClifford 4 (Fin 2 ⊕ Fin 2) where
  gamma := gamma4d
  gamma5 := gamma5Four
  gamma_herm := gamma4d_herm
  gamma_anticomm := by
    intro μ ν
    fin_cases μ <;> fin_cases ν
    · simp [gamma4d_sq, two_smul, one_add_one_eq_two]
    · exact gamma4d_anti_pair.1
    · exact gamma4d_anti_pair.2.1
    · exact gamma4d_anti_pair.2.2.2.1
    · rw [add_comm]; exact gamma4d_anti_pair.1
    · simp [gamma4d_sq, two_smul, one_add_one_eq_two]
    · exact gamma4d_anti_pair.2.2.1
    · exact gamma4d_anti_pair.2.2.2.2.1
    · rw [add_comm]; exact gamma4d_anti_pair.2.1
    · rw [add_comm]; exact gamma4d_anti_pair.2.2.1
    · simp [gamma4d_sq, two_smul, one_add_one_eq_two]
    · exact gamma4d_anti_pair.2.2.2.2.2
    · rw [add_comm]; exact gamma4d_anti_pair.2.2.2.1
    · rw [add_comm]; exact gamma4d_anti_pair.2.2.2.2.1
    · rw [add_comm]; exact gamma4d_anti_pair.2.2.2.2.2
    · simp [gamma4d_sq, two_smul, one_add_one_eq_two]
  gamma5_herm := gamma5Four_herm
  gamma5_sq := gamma5Four_sq
  gamma5_anti := gamma5Four_anti


theorem charpoly_rootMultiplicity_conj (p : ℂ[X])
    (hp : ∀ n, star (p.coeff n) = p.coeff n) (z : ℂ) :
    p.rootMultiplicity (star z) = p.rootMultiplicity z := by
  by_cases hp0 : p = 0
  · simp [hp0]
  · have hmap : p.map (starRingEnd ℂ) = p := by
      ext n
      simp only [Polynomial.coeff_map, starRingEnd_apply]
      exact hp n
    have hlin (w : ℂ) : (X - C w).map (starRingEnd ℂ) = X - C (star w) := by
      rw [Polynomial.map_sub, Polynomial.map_X, Polynomial.map_C, starRingEnd_apply]
    have hpow (w : ℂ) (n : ℕ) :
        ((X - C w) ^ n).map (starRingEnd ℂ) = (X - C (star w)) ^ n := by
      rw [Polynomial.map_pow, hlin]
    have hdvd : ∀ n : ℕ, (X - C (star z)) ^ n ∣ p ↔ (X - C z) ^ n ∣ p := by
      intro n
      constructor
      · intro h
        have hm := map_dvd (starRingEnd ℂ) h
        rw [hpow, hmap, star_star] at hm
        exact hm
      · intro h
        have hm := map_dvd (starRingEnd ℂ) h
        rw [hpow, hmap] at hm
        exact hm
    apply le_antisymm
    · rw [le_rootMultiplicity_iff (p := p) hp0]
      exact (hdvd _).1 (pow_rootMultiplicity_dvd p (star z))
    · rw [le_rootMultiplicity_iff (p := p) hp0]
      exact (hdvd _).2 (pow_rootMultiplicity_dvd p z)

def twoFlavor {n : Type*} [Fintype n] [DecidableEq n] (D : Matrix n n ℂ) :
    Matrix (n ⊕ n) (n ⊕ n) ℂ :=
  fromBlocks D 0 0 D

theorem two_flavor_det_eq_sq {n : Type*} [Fintype n] [DecidableEq n]
    (D : Matrix n n ℂ) : (twoFlavor D).det = D.det ^ 2 := by
  simp [twoFlavor, det_fromBlocks_zero₂₁, pow_two]

theorem two_flavor_det_real_nonneg {z : ℂ} (hz : star z = z) :
    ((z ^ 2).im = 0) ∧ 0 ≤ (z ^ 2).re := by
  have hre : (z.re : ℂ) = z := (conj_eq_iff_re).1 (by simpa only [star_def] using hz)
  have hsq : z ^ 2 = (z.re ^ 2 : ℝ) := by
    rw [← hre]
    exact (ofReal_pow z.re 2).symm
  rw [hsq, ofReal_im, ofReal_re]
  exact ⟨rfl, sq_nonneg z.re⟩

end

end FermionSignWilsonDiracGamma5

#print axioms FermionSignWilsonDiracGamma5.euclideanClifford2
#print axioms FermionSignWilsonDiracGamma5.euclideanClifford4
#print axioms FermionSignWilsonDiracGamma5.charpoly_rootMultiplicity_conj
#print axioms FermionSignWilsonDiracGamma5.two_flavor_det_eq_sq
#print axioms FermionSignWilsonDiracGamma5.two_flavor_det_real_nonneg
