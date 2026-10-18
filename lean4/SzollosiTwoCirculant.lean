import Mathlib.LinearAlgebra.Matrix.Circulant
import Mathlib.Data.Matrix.Block
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import ConcreteMubPolynomials

/-!
# The continuous two-circulant phase family

AuthorityEffect: None.

The six-phase block construction has Gram matrix six times the identity under
unit-modulus and one complex compatibility equation. Normalization constructs
an actual complex unitary matrix with entry modulus squared one sixth.
The four-phase form uses rows (1,x,xy) and (1,u,uv), with phase sum
x + y + star (x*y). Its domain is exactly six scalar real polynomial equations
in eight real coordinates. Every solution lies in the rational unit box, and
every point of the intersection of the two phase-sum images has such coordinates.
No distinct-root choice is required; the cubic identities hold at repeated roots.

Source: Szöllősi, arXiv:0811.3930v2, equations (1), (5), (8)-(14):
https://arxiv.org/pdf/0811.3930v2

These are actual matrix and parameter identities. No classification of arbitrary
Hadamard matrices, equivalence transport to a selected dephased representative,
cover subdivision, contractor exclusion, or curvature certificate is supplied.
-/

namespace MUB.SzollosiTwoCirculant
open Matrix

abbrev PhaseTriple := Fin 3 → ℂ
abbrev BlockIndex := Fin 3 ⊕ Fin 3

noncomputable def rowCirculant (a : PhaseTriple) : Matrix (Fin 3) (Fin 3) ℂ :=
  Matrix.circulant (fun i => a (-i))

theorem rowCirculant_explicit (a : PhaseTriple) :
    rowCirculant a = !![a 0, a 1, a 2; a 2, a 0, a 1; a 1, a 2, a 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

noncomputable def compatibility (a b : PhaseTriple) : ℂ :=
  a 0 * star (a 2) + a 1 * star (a 0) + a 2 * star (a 1) +
  (b 0 * star (b 2) + b 1 * star (b 0) + b 2 * star (b 1))

def UnitPhases (a : PhaseTriple) : Prop := ∀ i, a i * star (a i) = 1

noncomputable def rawBlock (a b : PhaseTriple) : Matrix BlockIndex BlockIndex ℂ :=
  Matrix.fromBlocks (rowCirculant a) (rowCirculant b)
    (rowCirculant b).conjTranspose (-(rowCirculant a).conjTranspose)

theorem rowCirculant_commute (a b : PhaseTriple) :
    rowCirculant a * rowCirculant b = rowCirculant b * rowCirculant a :=
  Matrix.circulant_mul_comm _ _

theorem rowCirculant_normal (a : PhaseTriple) :
    rowCirculant a * (rowCirculant a).conjTranspose =
      (rowCirculant a).conjTranspose * rowCirculant a := by
  unfold rowCirculant
  rw [Matrix.conjTranspose_circulant]
  exact Matrix.circulant_mul_comm _ _

set_option maxRecDepth 2048 in
theorem circulant_gram_sum (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (hc : compatibility a b = 0) :
    rowCirculant a * (rowCirculant a).conjTranspose +
      rowCirculant b * (rowCirculant b).conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
  have ha0 := ha 0
  have ha1 := ha 1
  have ha2 := ha 2
  have hb0 := hb 0
  have hb1 := hb 1
  have hb2 := hb 2
  have hcc := congrArg star hc
  simp only [compatibility, star_add, star_mul, star_star, star_zero] at hc hcc
  simp only [Complex.star_def] at ha0 ha1 ha2 hb0 hb1 hb2 hc hcc
  rw [rowCirculant_explicit, rowCirculant_explicit]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_succ,
      Matrix.conjTranspose_apply, Matrix.one_apply, Complex.star_def] <;>
    first | linear_combination ha0 + ha1 + ha2 + hb0 + hb1 + hb2
          | linear_combination hc
          | linear_combination hcc

theorem rawBlock_gram (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (hc : compatibility a b = 0) :
    rawBlock a b * (rawBlock a b).conjTranspose = (6 : ℂ) • (1 : Matrix BlockIndex BlockIndex ℂ) := by
  have hsum := circulant_gram_sum a b ha hb hc
  have hab := rowCirculant_commute a b
  have hstar := congrArg Matrix.conjTranspose hab
  simp only [Matrix.conjTranspose_mul] at hstar
  unfold rawBlock
  rw [Matrix.fromBlocks_conjTranspose, Matrix.conjTranspose_neg,
    Matrix.conjTranspose_conjTranspose, Matrix.fromBlocks_multiply]
  simp only [Matrix.conjTranspose_conjTranspose]
  rw [← Matrix.fromBlocks_one, Matrix.fromBlocks_smul]
  apply Matrix.fromBlocks_inj.mpr
  refine ⟨hsum, ?_, ?_, ?_⟩
  · simp only [Matrix.mul_neg, hab, add_neg_cancel, smul_zero]
  · simp only [Matrix.neg_mul, hstar, add_neg_cancel, smul_zero]
  · simpa only [neg_mul_neg, ← rowCirculant_normal,
      add_comm] using hsum


theorem rawBlock_entry_unit (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (i j : BlockIndex) : rawBlock a b i j * star (rawBlock a b i j) = 1 := by
  cases i with
  | inl i =>
    cases j with
    | inl j => exact ha (-(i-j))
    | inr j => exact hb (-(i-j))
  | inr i =>
    cases j with
    | inl j =>
      simpa [rawBlock, rowCirculant, Matrix.circulant, Matrix.conjTranspose_apply, mul_comm] using hb (-(j-i))
    | inr j =>
      simpa [rawBlock, rowCirculant, Matrix.circulant, Matrix.conjTranspose_apply, mul_comm] using ha (-(j-i))

def blockEquiv : BlockIndex ≃ Fin 6 := finSumFinEquiv

noncomputable def rawSix (a b : PhaseTriple) : Matrix (Fin 6) (Fin 6) ℂ :=
  (rawBlock a b).submatrix (blockEquiv.symm) (blockEquiv.symm)

theorem rawSix_gram (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (hc : compatibility a b = 0) :
    rawSix a b * (rawSix a b).conjTranspose = (6 : ℂ) • (1 : Matrix (Fin 6) (Fin 6) ℂ) := by
  unfold rawSix
  rw [Matrix.conjTranspose_submatrix, Matrix.submatrix_mul_equiv, rawBlock_gram a b ha hb hc]
  change (6 : ℂ) • ((1 : Matrix BlockIndex BlockIndex ℂ).submatrix blockEquiv.symm blockEquiv.symm) = _
  rw [Matrix.submatrix_one_equiv]

noncomputable def normalizer : ℂ := ((Real.sqrt 6 : ℝ) : ℂ)⁻¹

theorem normalizer_square : normalizer * star normalizer = (6 : ℂ)⁻¹ := by
  have hs : ((Real.sqrt 6 : ℝ) : ℂ) * ((Real.sqrt 6 : ℝ) : ℂ) = 6 := by
    exact_mod_cast Real.mul_self_sqrt (show (0 : ℝ) ≤ 6 by norm_num)
  have hstar : star normalizer = normalizer := by simp [normalizer]
  rw [hstar]
  change ((Real.sqrt 6 : ℝ) : ℂ)⁻¹ * ((Real.sqrt 6 : ℝ) : ℂ)⁻¹ = _
  rw [← mul_inv, hs]

noncomputable def normalized (a b : PhaseTriple) : Matrix (Fin 6) (Fin 6) ℂ :=
  normalizer • rawSix a b

theorem normalized_mul_adjoint (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (hc : compatibility a b = 0) : normalized a b * (normalized a b).conjTranspose = 1 := by
  unfold normalized
  rw [Matrix.conjTranspose_smul, Matrix.smul_mul, Matrix.mul_smul, smul_smul,
    normalizer_square, rawSix_gram a b ha hb hc, smul_smul]
  norm_num

theorem normalized_unitary (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (hc : compatibility a b = 0) : (normalized a b).conjTranspose * normalized a b = 1 :=
  mul_eq_one_comm.mp (normalized_mul_adjoint a b ha hb hc)

theorem normalized_entry_modulus (a b : PhaseTriple) (ha : UnitPhases a) (hb : UnitPhases b)
    (i j : Fin 6) : normalized a b i j * star (normalized a b i j) = (1/6 : ℂ) := by
  have hr := rawBlock_entry_unit a b ha hb (blockEquiv.symm i) (blockEquiv.symm j)
  change (normalizer * rawBlock a b _ _) * star (normalizer * rawBlock a b _ _) = _
  rw [star_mul]
  calc
    _ = (normalizer * star normalizer) * (rawBlock a b _ _ * star (rawBlock a b _ _)) := by ring
    _ = (1/6 : ℂ) := by rw [normalizer_square, hr]; norm_num


noncomputable def phaseSum (x y : ℂ) : ℂ := x + y + star (x*y)
noncomputable def phaseRow (x y : ℂ) : PhaseTriple := ![1,x,x*y]

theorem phaseRow_unit (x y : ℂ) (hx : x * star x = 1) (hy : y * star y = 1) :
    UnitPhases (phaseRow x y) := by
  intro i
  fin_cases i
  · simp [phaseRow]
  · change x * star x = 1
    exact hx
  · change (x*y) * star (x*y) = 1
    rw [star_mul]
    calc
      _ = (x*star x) * (y*star y) := by ring
      _ = 1 := by rw [hx,hy]; norm_num

theorem phaseRow_compatibility (x y u v : ℂ)
    (hx : x * star x = 1) (hu : u * star u = 1) :
    compatibility (phaseRow x y) (phaseRow u v) = phaseSum x y + phaseSum u v := by
  change 1 * star (x*y) + x * star (1 : ℂ) + (x*y) * star x +
    (1 * star (u*v) + u * star (1 : ℂ) + (u*v) * star u) =
      (x+y+star (x*y)) + (u+v+star (u*v))
  simp only [star_one, mul_one, one_mul]
  linear_combination y * hx + v * hu

def ParameterDomain (x y u v : ℂ) : Prop :=
  x * star x = 1 ∧ y * star y = 1 ∧ u * star u = 1 ∧ v * star v = 1 ∧
    phaseSum x y + phaseSum u v = 0

noncomputable def familyMatrix (x y u v : ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  normalized (phaseRow x y) (phaseRow u v)

theorem familyMatrix_unitary (x y u v : ℂ) (h : ParameterDomain x y u v) :
    (familyMatrix x y u v).conjTranspose * familyMatrix x y u v = 1 := by
  rcases h with ⟨hx,hy,hu,hv,hc⟩
  exact normalized_unitary _ _ (phaseRow_unit x y hx hy) (phaseRow_unit u v hu hv)
    ((phaseRow_compatibility x y u v hx hu).trans hc)

theorem familyMatrix_entry_modulus (x y u v : ℂ) (h : ParameterDomain x y u v) (i j : Fin 6) :
    familyMatrix x y u v i j * star (familyMatrix x y u v i j) = (1/6 : ℂ) :=
  normalized_entry_modulus _ _ (phaseRow_unit x y h.1 h.2.1)
    (phaseRow_unit u v h.2.2.1 h.2.2.2.1) i j

theorem unit_phase_coordinates_bounded (z : ℂ) (hz : z * star z = 1) :
    -1 ≤ z.re ∧ z.re ≤ 1 ∧ -1 ≤ z.im ∧ z.im ≤ 1 := by
  have h := congrArg Complex.re hz
  simp only [Complex.mul_re, Complex.star_def, Complex.conj_re, Complex.conj_im,
    Complex.one_re] at h
  have hre := sq_nonneg z.re
  have him := sq_nonneg z.im
  constructor
  · nlinarith
  constructor
  · nlinarith
  constructor <;> nlinarith


abbrev ParameterCoord := Fin 4 × Bool
abbrev ParameterPoly := MvPolynomial ParameterCoord ℝ
abbrev ParameterEquation := Fin 4 ⊕ Bool

def decodeParameters (r : ParameterCoord → ℝ) (i : Fin 4) : ℂ := ⟨r (i,false),r (i,true)⟩
def encodeParameters (z : Fin 4 → ℂ) : ParameterCoord → ℝ :=
  fun i => if i.2 then (z i.1).im else (z i.1).re

theorem decode_encode (z : Fin 4 → ℂ) : decodeParameters (encodeParameters z) = z := by
  funext i
  rfl

theorem encode_decode (r : ParameterCoord → ℝ) : encodeParameters (decodeParameters r) = r := by
  funext i
  rcases i with ⟨i,b⟩
  cases b <;> rfl

open MvPolynomial
noncomputable def circlePolynomial (i : Fin 4) : ParameterPoly :=
  X (i,false)^2 + X (i,true)^2 - 1
noncomputable def phaseSumRePolynomial : ParameterPoly :=
  (X (0,false)+X (1,false)+X (0,false)*X (1,false)-X (0,true)*X (1,true)) +
  (X (2,false)+X (3,false)+X (2,false)*X (3,false)-X (2,true)*X (3,true))
noncomputable def phaseSumImPolynomial : ParameterPoly :=
  (X (0,true)+X (1,true)-(X (0,false)*X (1,true)+X (0,true)*X (1,false))) +
  (X (2,true)+X (3,true)-(X (2,false)*X (3,true)+X (2,true)*X (3,false)))
noncomputable def parameterPolynomial : ParameterEquation → ParameterPoly
  | .inl i => circlePolynomial i
  | .inr false => phaseSumRePolynomial
  | .inr true => phaseSumImPolynomial

theorem circlePolynomial_eval (r : ParameterCoord → ℝ) (i : Fin 4) :
    eval r (circlePolynomial i) = Complex.normSq (decodeParameters r i) - 1 := by
  simp [circlePolynomial, decodeParameters, Complex.normSq_apply, pow_two]

theorem circlePolynomial_zero_iff (r : ParameterCoord → ℝ) (i : Fin 4) :
    eval r (circlePolynomial i) = 0 ↔
      decodeParameters r i * star (decodeParameters r i) = 1 := by
  rw [circlePolynomial_eval, sub_eq_zero]
  simp [Complex.mul_conj]

theorem phaseSumRePolynomial_eval (r : ParameterCoord → ℝ) :
    eval r phaseSumRePolynomial =
      (phaseSum (decodeParameters r 0) (decodeParameters r 1) +
        phaseSum (decodeParameters r 2) (decodeParameters r 3)).re := by
  simp [phaseSumRePolynomial, phaseSum, decodeParameters, Complex.mul_re]
  ring

theorem phaseSumImPolynomial_eval (r : ParameterCoord → ℝ) :
    eval r phaseSumImPolynomial =
      (phaseSum (decodeParameters r 0) (decodeParameters r 1) +
        phaseSum (decodeParameters r 2) (decodeParameters r 3)).im := by
  simp [phaseSumImPolynomial, phaseSum, decodeParameters, Complex.mul_im]
  ring

theorem parameter_equations_iff (r : ParameterCoord → ℝ) :
    (∀ e, eval r (parameterPolynomial e) = 0) ↔
      ParameterDomain (decodeParameters r 0) (decodeParameters r 1)
        (decodeParameters r 2) (decodeParameters r 3) := by
  constructor
  · intro h
    refine ⟨(circlePolynomial_zero_iff r 0).mp (h (.inl 0)),
      (circlePolynomial_zero_iff r 1).mp (h (.inl 1)),
      (circlePolynomial_zero_iff r 2).mp (h (.inl 2)),
      (circlePolynomial_zero_iff r 3).mp (h (.inl 3)), ?_⟩
    apply Complex.ext
    · exact (phaseSumRePolynomial_eval r).symm.trans (h (.inr false))
    · exact (phaseSumImPolynomial_eval r).symm.trans (h (.inr true))
  · rintro ⟨hx,hy,hu,hv,hc⟩ e
    cases e with
    | inl i =>
      fin_cases i
      · exact (circlePolynomial_zero_iff r 0).mpr hx
      · exact (circlePolynomial_zero_iff r 1).mpr hy
      · exact (circlePolynomial_zero_iff r 2).mpr hu
      · exact (circlePolynomial_zero_iff r 3).mpr hv
    | inr b =>
      cases b
      · change eval r phaseSumRePolynomial = 0
        rw [phaseSumRePolynomial_eval, hc, Complex.zero_re]
      · change eval r phaseSumImPolynomial = 0
        rw [phaseSumImPolynomial_eval, hc, Complex.zero_im]

theorem parameter_solutions_in_unit_box (r : ParameterCoord → ℝ)
    (h : ∀ e, eval r (parameterPolynomial e) = 0) : ∀ i, -1 ≤ r i ∧ r i ≤ 1 := by
  rintro ⟨i,b⟩
  have hz := (circlePolynomial_zero_iff r i).mp (h (.inl i))
  have hb := unit_phase_coordinates_bounded (decodeParameters r i) hz
  cases b
  · exact ⟨hb.1,hb.2.1⟩
  · exact ⟨hb.2.2.1,hb.2.2.2⟩

theorem parameter_equation_count : Fintype.card ParameterEquation = 6 := by decide
theorem parameter_coordinate_count : Fintype.card ParameterCoord = 8 := by decide


theorem phaseSum_cubic_root (x y : ℂ) (hx : x * star x = 1) :
    x^3 - phaseSum x y * x^2 + star (phaseSum x y) * x - 1 = 0 := by
  simp only [phaseSum, star_add, star_mul, star_star]
  linear_combination (1-x*star y) * hx

theorem phaseSum_swap (x y : ℂ) : phaseSum x y = phaseSum y x := by
  simp only [phaseSum, mul_comm, add_comm]

theorem parameter_cubic_roots (x y u v : ℂ) (h : ParameterDomain x y u v) :
    let α := phaseSum x y
    (x^3 - α*x^2 + star α*x - 1 = 0) ∧ (y^3 - α*y^2 + star α*y - 1 = 0) ∧
    (u^3 - (-α)*u^2 + star (-α)*u - 1 = 0) ∧ (v^3 - (-α)*v^2 + star (-α)*v - 1 = 0) := by
  dsimp
  have hneg : -phaseSum x y = phaseSum u v := (eq_neg_of_add_eq_zero_right h.2.2.2.2).symm
  refine ⟨phaseSum_cubic_root x y h.1, ?_, ?_, ?_⟩
  · rw [phaseSum_swap x y]
    exact phaseSum_cubic_root y x h.2.1
  · rw [hneg]
    exact phaseSum_cubic_root u v h.2.2.1
  · rw [hneg, phaseSum_swap u v]
    exact phaseSum_cubic_root v u h.2.2.2.1

theorem boundary_parameter_point : ParameterDomain 1 (-1) 1 Complex.I := by
  norm_num [ParameterDomain, phaseSum, Complex.star_def]

#print axioms parameter_cubic_roots
#print axioms boundary_parameter_point
#print axioms parameter_equations_iff
#print axioms parameter_solutions_in_unit_box
#print axioms familyMatrix_unitary
#print axioms familyMatrix_entry_modulus
#print axioms unit_phase_coordinates_bounded
#print axioms normalized_unitary
#print axioms normalized_entry_modulus
#print axioms rawBlock_gram

/-- Every row with leading phase one is represented without a root choice. -/
theorem phaseRow_surjective (b c : ℂ) (hb : b * star b = 1) (hc : c * star c = 1) :
    ∃ x y, x * star x = 1 ∧ y * star y = 1 ∧ phaseRow x y = ![1,b,c] := by
  refine ⟨b, star b * c, hb, ?_, ?_⟩
  · rw [star_mul, star_star]
    calc
      _ = (b * star b) * (c * star c) := by ring
      _ = 1 := by rw [hb,hc]; norm_num
  · funext i
    fin_cases i
    · rfl
    · rfl
    · change b * (star b * c) = c
      rw [← mul_assoc, hb, one_mul]

/-- The source domain is the intersection of the two phase-sum images. -/
def DeltoidIntersection (α : ℂ) : Prop :=
  (∃ x y, x * star x = 1 ∧ y * star y = 1 ∧ phaseSum x y = α) ∧
  (∃ u v, u * star u = 1 ∧ v * star v = 1 ∧ phaseSum u v = -α)

theorem parameter_covers_intersection (α : ℂ) : DeltoidIntersection α ↔
    ∃ r : ParameterCoord → ℝ, (∀ e, eval r (parameterPolynomial e) = 0) ∧
      phaseSum (decodeParameters r 0) (decodeParameters r 1) = α := by
  constructor
  · rintro ⟨⟨x,y,hx,hy,hα⟩,⟨u,v,hu,hv,hneg⟩⟩
    refine ⟨encodeParameters ![x,y,u,v], (parameter_equations_iff _).mpr ?_, ?_⟩
    · change ParameterDomain x y u v
      refine ⟨hx,hy,hu,hv,?_⟩
      rw [hα,hneg]
      exact add_neg_cancel α
    · change phaseSum x y = α
      exact hα
  · rintro ⟨r,hr,hα⟩
    have h := (parameter_equations_iff r).mp hr
    refine ⟨⟨_,_,h.1,h.2.1,hα⟩,⟨_,_,h.2.2.1,h.2.2.2.1,?_⟩⟩
    rw [← hα]
    exact eq_neg_of_add_eq_zero_right h.2.2.2.2

theorem parameter_solution_matrix (r : ParameterCoord → ℝ)
    (hr : ∀ e, eval r (parameterPolynomial e) = 0) :
    let H := familyMatrix (decodeParameters r 0) (decodeParameters r 1)
      (decodeParameters r 2) (decodeParameters r 3)
    H.conjTranspose * H = 1 ∧ ∀ i j, H i j * star (H i j) = (1/6 : ℂ) := by
  have h := (parameter_equations_iff r).mp hr
  exact ⟨familyMatrix_unitary _ _ _ _ h, familyMatrix_entry_modulus _ _ _ _ h⟩

#print axioms phaseRow_surjective
#print axioms parameter_covers_intersection
#print axioms parameter_solution_matrix

end MUB.SzollosiTwoCirculant
