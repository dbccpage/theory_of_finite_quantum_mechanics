module

public import Mathlib.LinearAlgebra.Matrix.Block
public import Mathlib.LinearAlgebra.Matrix.ConjTranspose
public import Mathlib.LinearAlgebra.Matrix.SchurComplement
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.Analysis.Complex.Order
public import Mathlib.Tactic

/-!
# Finite imaginary-fugacity determinant certificates

AuthorityEffect: None.
Claim: finite bipartite staggered matrices at unit fugacity have the
stated adjoint symmetry; positive real mass gives positive determinant.
Gamma Hermiticity alone gives reality and two-flavor nonnegativity.
A finite center-orbit sum has algebraic center periodicity. No continuum
limit, QCD measure, phase transition, or analytic continuation is certified.
-/

@[expose] public section

open Matrix Complex
open scoped ComplexOrder

namespace CampaignFspImaginaryMuRealDet
noncomputable section
variable {P N : Type*} [Fintype P] [Fintype N] [DecidableEq P] [DecidableEq N]

/-- The staggered site-parity involution on a declared bipartition. -/
def parity : Matrix (P ⊕ N) (P ⊕ N) ℂ := fromBlocks 1 0 0 (-1)

/-- Forward transport blocks are A and B; the reverse links use adjoints.
The nonzero fugacity is the algebraic substitute for exp(a mu). -/
def staggered (m : ℝ) (z : ℂ) (A : Matrix P N ℂ) (B : Matrix N P ℂ) :
    Matrix (P ⊕ N) (P ⊕ N) ℂ :=
  fromBlocks ((m : ℂ) • 1) (z • A - z⁻¹ • Bᴴ)
    (z • B - z⁻¹ • Aᴴ) ((m : ℂ) • 1)

/-- All anti-Hermitian off-diagonal hopping blocks, including zero mass. -/
def bipartite (m : ℝ) (X : Matrix P N ℂ) : Matrix (P ⊕ N) (P ⊕ N) ℂ :=
  fromBlocks ((m : ℂ) • 1) X (-Xᴴ) ((m : ℂ) • 1)

theorem parity_sq : (parity (P := P) (N := N)) * parity = 1 := by
  simp [parity, fromBlocks_multiply, fromBlocks_one]

omit [Fintype P] [Fintype N] in
theorem parity_hermitian : (parity (P := P) (N := N))ᴴ = parity := by
  simp [parity, fromBlocks_conjTranspose]

omit [Fintype P] [Fintype N] in
theorem inverse_eq_star (z : ℂ) (hz : star z * z = 1) : z⁻¹ = star z := by
  have hz0 : z ≠ 0 := by intro h; simp [h] at hz
  apply mul_right_cancel₀ hz0
  rw [inv_mul_cancel₀ hz0]
  exact hz.symm

omit [Fintype P] [Fintype N] in
theorem staggered_unit (m : ℝ) (z : ℂ) (hz : star z * z = 1)
    (A : Matrix P N ℂ) (B : Matrix N P ℂ) :
    staggered m z A B = bipartite m (z • A - star z • Bᴴ) := by
  simp [staggered, bipartite, inverse_eq_star z hz, conjTranspose_smul,
    sub_eq_add_neg, add_comm]

theorem bipartite_adjoint (m : ℝ) (X : Matrix P N ℂ) :
    parity * bipartite m X * parity = (bipartite m X)ᴴ := by
  simp [parity, bipartite, fromBlocks_multiply, fromBlocks_conjTranspose]

theorem staggered_adjoint (m : ℝ) (z : ℂ) (hz : star z * z = 1)
    (A : Matrix P N ℂ) (B : Matrix N P ℂ) :
    parity * staggered m z A B * parity = (staggered m z A B)ᴴ := by
  rw [staggered_unit m z hz A B]
  exact bipartite_adjoint _ _

/-- The determinant implication uses an involution, not an assumed sign. -/
theorem det_real_of_involution {S : Type*} [Fintype S] [DecidableEq S]
    (G D : Matrix S S ℂ) (hG : G * G = 1) (hD : G * D * G = Dᴴ) :
    star D.det = D.det := by
  have hsq : G.det * G.det = 1 := by rw [← det_mul, hG, det_one]
  rw [← det_conjTranspose, ← hD, det_mul, det_mul]
  calc
    G.det * D.det * G.det = (G.det * G.det) * D.det := by ring
    _ = D.det := by rw [hsq, one_mul]

theorem staggered_det_real (m : ℝ) (z : ℂ) (hz : star z * z = 1)
    (A : Matrix P N ℂ) (B : Matrix N P ℂ) :
    star (staggered m z A B).det = (staggered m z A B).det :=
  det_real_of_involution _ _ parity_sq (staggered_adjoint m z hz A B)

/-- Repeated flavor blocks square the determinant, with no rooting. -/
theorem two_flavor_nonneg {S : Type*} [Fintype S] [DecidableEq S]
    (D : Matrix S S ℂ) (hD : star D.det = D.det) :
    0 ≤ (fromBlocks D 0 0 D).det.re := by
  have hre : (D.det.re : ℂ) = D.det :=
    (conj_eq_iff_re).1 (by simpa only [star_def] using hD)
  rw [det_fromBlocks_zero₂₁, ← hre]
  simpa only [mul_re, ofReal_re, ofReal_im, mul_zero, sub_zero, pow_two] using sq_nonneg D.det.re

/-- Normalized mass one gives a Gram-matrix Schur complement. -/
theorem bipartite_one_det (X : Matrix P N ℂ) :
    (bipartite 1 X).det = (1 + Xᴴ * X).det := by
  simpa only [bipartite, ofReal_one, one_smul, Matrix.neg_mul, sub_neg_eq_add]
    using det_fromBlocks_one₁₁ X (-Xᴴ) (1 : Matrix N N ℂ)

theorem bipartite_one_det_pos (X : Matrix P N ℂ) :
    0 < (bipartite 1 X).det := by
  rw [bipartite_one_det]
  exact (Matrix.PosDef.one.add_posSemidef
    (posSemidef_conjTranspose_mul_self X)).det_pos

omit [Fintype P] [Fintype N] in
theorem bipartite_scale (m : ℝ) (hm : m ≠ 0) (X : Matrix P N ℂ) :
    bipartite m X = (m : ℂ) • bipartite 1 ((m : ℂ)⁻¹ • X) := by
  have hc : (m : ℂ) ≠ 0 := by exact_mod_cast hm
  ext i j
  cases i <;> cases j <;>
    simp [bipartite, fromBlocks, hc, mul_comm, mul_left_comm]

theorem bipartite_det_pos (m : ℝ) (hm : 0 < m) (X : Matrix P N ℂ) :
    0 < (bipartite m X).det := by
  rw [bipartite_scale m (ne_of_gt hm), det_smul]
  exact mul_pos (pow_pos (by exact_mod_cast hm) _) (bipartite_one_det_pos _)

theorem staggered_det_pos (m : ℝ) (hm : 0 < m) (z : ℂ)
    (hz : star z * z = 1) (A : Matrix P N ℂ) (B : Matrix N P ℂ) :
    0 < (staggered m z A B).det := by
  rw [staggered_unit m z hz A B]
  exact bipartite_det_pos m hm _

/-- Gamma Hermiticity without the mass/hopping hypotheses need not give a sign. -/
def negativeExample : Matrix (Fin 2) (Fin 2) ℂ := !![-1, 0; 0, 1]

theorem gamma_hermitian_negative :
    (!![1, 0; 0, -1] : Matrix (Fin 2) (Fin 2) ℂ) * negativeExample *
      !![1, 0; 0, -1] = negativeExampleᴴ ∧
    negativeExample.det = -1 := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [negativeExample, Matrix.mul_apply, Fin.sum_univ_two, conjTranspose_apply]
  · norm_num [negativeExample, Matrix.det_fin_two]

/-- Declared finite center-orbit ensemble; no gauge integral is implicit. -/
def centerSum (f : ℂ → ℂ) (w z : ℂ) : ℂ := f z + f (w * z) + f (w ^ 2 * z)

theorem centerSum_periodic (f : ℂ → ℂ) (w z : ℂ) (hw : w ^ 3 = 1) :
    centerSum f w (w * z) = centerSum f w z := by
  have h1 : w * (w * z) = w ^ 2 * z := by ring
  have h2 : w ^ 2 * (w * z) = z := by rw [← mul_assoc, ← pow_succ, hw, one_mul]
  simp only [centerSum, h1, h2]
  ring

end
end CampaignFspImaginaryMuRealDet

#print axioms CampaignFspImaginaryMuRealDet.parity_sq
#print axioms CampaignFspImaginaryMuRealDet.parity_hermitian
#print axioms CampaignFspImaginaryMuRealDet.inverse_eq_star
#print axioms CampaignFspImaginaryMuRealDet.staggered_unit
#print axioms CampaignFspImaginaryMuRealDet.bipartite_adjoint
#print axioms CampaignFspImaginaryMuRealDet.staggered_adjoint
#print axioms CampaignFspImaginaryMuRealDet.det_real_of_involution
#print axioms CampaignFspImaginaryMuRealDet.staggered_det_real
#print axioms CampaignFspImaginaryMuRealDet.two_flavor_nonneg
#print axioms CampaignFspImaginaryMuRealDet.bipartite_one_det
#print axioms CampaignFspImaginaryMuRealDet.bipartite_one_det_pos
#print axioms CampaignFspImaginaryMuRealDet.bipartite_scale
#print axioms CampaignFspImaginaryMuRealDet.bipartite_det_pos
#print axioms CampaignFspImaginaryMuRealDet.staggered_det_pos
#print axioms CampaignFspImaginaryMuRealDet.gamma_hermitian_negative
#print axioms CampaignFspImaginaryMuRealDet.centerSum_periodic
