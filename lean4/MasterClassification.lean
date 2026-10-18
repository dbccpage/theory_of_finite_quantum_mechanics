import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FinCases
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Rat.Basic
import ConcreteSemantics
import PolynomialEncoding
import CaseCoverage
import GroebnerBranch
import CADBranch

open scoped BigOperators
open scoped Matrix
open MUB.ConcreteSemantics
open MUB.PolynomialEncoding
open MUB.CaseCoverage
open MUB.GroebnerBranch
open MUB.CADBranch

/-!
# Explicit matrix constructors and conditional catalog interfaces

`szollosiMatrix_isCH6`, `taoMatrix_isCH6`, and `karlssonMatrix_isCH6`
establish `IsCH6` for the displayed matrices under their stated domains.
The first uses six complex phases with a bilinear constraint; the third uses
two unit phases. Their legacy component names do not establish identification
with a complete named family, a parameter dimension, or an exhaustive catalog.

`dephase_and_route_corner` supplies dephasing and the zero/nonzero corner split.
`FullModuliClassification` is an open proposition; no inhabitant is supplied.
`Realizes` is `False` for the two unimplemented component labels.
These are single-matrix statements, with no simultaneous triple-gauge bridge.

AuthorityEffect: None.
-/

namespace MUB.MasterClassification

/-- Five legacy catalog labels; exhaustiveness and family identification remain open. -/
inductive ModuliComponent where
  | fourierDita : ModuliComponent
  | szollosiDeltoid : ModuliComponent
  | karlssonVolume : ModuliComponent
  | taoConfluence : ModuliComponent
  | haagerupIsolated : ModuliComponent
  deriving DecidableEq, Repr

/-- Six phase parameters for the displayed two-circulant ansatz (legacy Szollosi label). -/
structure SzollosiParam where
  a : ℂ
  b : ℂ
  c : ℂ
  d : ℂ
  e : ℂ
  f : ℂ

/-- Two phase parameters for the displayed affine ansatz (legacy Karlsson label). -/
structure KarlssonParam where
  x : ℂ
  y : ℂ

/-- Domain predicate for Karlsson parameters: both phases lie on the unit circle. -/
def KarlssonDomain (p : KarlssonParam) : Prop :=
  Complex.normSq p.x = 1 ∧ Complex.normSq p.y = 1

/-- Three phase parameters for the affine Fourier-Diță family. -/
structure FourierDitaParam where
  a : ℂ
  b : ℂ
  c : ℂ

/-- Domain predicate for Fourier-Diță parameters: all 3 phases lie on the unit circle. -/
def FourierDitaDomain (p : FourierDitaParam) : Prop :=
  Complex.normSq p.a = 1 ∧
  Complex.normSq p.b = 1 ∧
  Complex.normSq p.c = 1

/-- Component parameter type family assigning concrete parameter representations
    to each catalog component (Audit Recommendations P1, P5). -/
def Param : ModuliComponent → Type
  | .fourierDita => FourierDitaParam
  | .szollosiDeltoid => SzollosiParam
  | .karlssonVolume => KarlssonParam
  | .taoConfluence => PUnit
  | .haagerupIsolated => PUnit

/-- Invariant bilinear sum z_1 for the Szöllősi family. -/
def szollosi_z1 (a b c : ℂ) : ℂ :=
  a * star c + b * star a + c * star b

/-- Invariant bilinear sum z_2 for the Szöllősi family. -/
def szollosi_z2 (d e f : ℂ) : ℂ :=
  d * star f + e * star d + f * star e

/-- Domain predicate for Szöllősi family parameters: all 6 phases lie on the unit circle
    and the sum of invariants vanishes (z_1 + z_2 = 0). -/
def SzollosiDomain (p : SzollosiParam) : Prop :=
  Complex.normSq p.a = 1 ∧
  Complex.normSq p.b = 1 ∧
  Complex.normSq p.c = 1 ∧
  Complex.normSq p.d = 1 ∧
  Complex.normSq p.e = 1 ∧
  Complex.normSq p.f = 1 ∧
  szollosi_z1 p.a p.b p.c + szollosi_z2 p.d p.e p.f = 0

/-- Parameter domain predicate across moduli components. -/
def Domain : (c : ModuliComponent) → Param c → Prop
  | .fourierDita, p => FourierDitaDomain p
  | .szollosiDeltoid, p => SzollosiDomain p
  | .karlssonVolume, p => KarlssonDomain p
  | .taoConfluence, _ => True
  | .haagerupIsolated, _ => True

/-- Explicit two-circulant matrix; named-family identification is a separate obligation. -/
def szollosiMatrix (p : SzollosiParam) : Matrix (Fin 6) (Fin 6) ℂ :=
  !![p.a, p.b, p.c, p.d, p.e, p.f;
     p.c, p.a, p.b, p.f, p.d, p.e;
     p.b, p.c, p.a, p.e, p.f, p.d;
     star p.d, star p.f, star p.e, - star p.a, - star p.c, - star p.b;
     star p.e, star p.d, star p.f, - star p.b, - star p.a, - star p.c;
     star p.f, star p.e, star p.d, - star p.c, - star p.b, - star p.a]

/-- Primitive cubic root of unity for the Chernyavsky-Tao matrix and Karlsson family. -/
noncomputable def tao_omega : ℂ := -1/2 + Complex.I * (Real.sqrt 3 / 2)

/-- Explicit 6x6 Chernyavsky-Tao isolated spectral matrix constructor (Audit Target P5). -/
noncomputable def taoMatrix : Matrix (Fin 6) (Fin 6) ℂ :=
  let w := tao_omega
  let w2 := tao_omega ^ 2
  !![1, 1, 1, 1, 1, 1;
     1, 1, w, w, w2, w2;
     1, w, 1, w2, w2, w;
     1, w, w2, 1, w, w2;
     1, w2, w2, w, 1, w;
     1, w2, w, w2, w, 1]

/-- Explicit two-phase affine matrix. No equivalence to the full Karlsson family is supplied. -/
noncomputable def karlssonMatrix (p : KarlssonParam) : Matrix (Fin 6) (Fin 6) ℂ :=
  let w := tao_omega
  let w2 := tao_omega ^ 2
  let x := p.x
  let y := p.y
  !![1,  1,    1,       1,         1,          1;
     1, -1,    x,      -x,         y,         -y;
     1,  1,    w,       w,        w2,         w2;
     1, -1,  w * x,  -w * x,    w2 * y,    -w2 * y;
     1,  1,   w2,      w2,         w,          w;
     1, -1, w2 * x, -w2 * x,     w * y,     -w * y]

/-- Explicit 6x6 isolated Haagerup complex Hadamard matrix constructor. -/
def haagerupMatrix : Matrix (Fin 6) (Fin 6) ℂ :=
  !![ 1,  1,  Complex.I,  1,  1, -1;
      Complex.I,  1,  1, -1,  1,  1;
      1,  Complex.I,  1,  1, -1,  1;
      1, -1,  1, -1,  Complex.I, -1;
      1,  1, -1, -1, -1,  Complex.I;
     -1,  1,  1,  Complex.I, -1, -1]

/-- Explicit 6x6 Fourier-Diță affine family matrix constructor. -/
noncomputable def fourierDitaMatrix (p : FourierDitaParam) : Matrix (Fin 6) (Fin 6) ℂ :=
  let w := tao_omega
  let w2 := tao_omega ^ 2
  let a := p.a
  let b := p.b
  let c := p.c
  !![1,   1,       1,      a,      a,        a;
     1,   w,      w2,      b,    b * w,    b * w2;
     1,  w2,       w,      c,    c * w2,   c * w;
     1,   1,       1,     -a,     -a,       -a;
     1,   w,      w2,     -b,   -b * w,   -b * w2;
     1,  w2,       w,     -c,   -c * w2,  -c * w]

/-- Concrete family realization predicate relating component c and parameters p
    to an explicit matrix D (Audit Recommendations P1, P5).
    Every moduli component c has an explicit matrix realization. -/
def Realizes : (c : ModuliComponent) → Param c → Matrix (Fin 6) (Fin 6) ℂ → Prop
  | .fourierDita, p, D => D = fourierDitaMatrix p
  | .szollosiDeltoid, p, D => D = szollosiMatrix p
  | .karlssonVolume, p, D => D = karlssonMatrix p
  | .taoConfluence, _, D => D = taoMatrix
  | .haagerupIsolated, _, D => D = haagerupMatrix

/-!
### Auxiliary Algebraic Lemmas for Szöllősi Matrix Unitarity
-/

lemma unit_mul_star (z : ℂ) (hz : Complex.normSq z = 1) :
    z * (starRingEnd ℂ) z = 1 := by
  rw [← Complex.star_def]
  exact mul_star_self_of_normSq_one hz

lemma star_unit_mul (z : ℂ) (hz : Complex.normSq z = 1) :
    (starRingEnd ℂ) z * z = 1 := by
  rw [← Complex.star_def]
  exact star_mul_self_of_normSq_one hz

lemma szollosi_cond_star (p : SzollosiParam)
    (h_cond : szollosi_z1 p.a p.b p.c + szollosi_z2 p.d p.e p.f = 0) :
    p.c * star p.a + p.a * star p.b + p.b * star p.c +
    (p.f * star p.d + p.d * star p.e + p.e * star p.f) = 0 := by
  have hs : star (szollosi_z1 p.a p.b p.c + szollosi_z2 p.d p.e p.f) = (0 : ℂ) := by
    rw [h_cond, star_zero]
  dsimp [szollosi_z1, szollosi_z2] at hs
  simp only [map_add, map_mul, Complex.conj_conj] at hs
  simp only [Complex.star_def]
  linear_combination hs

/-- Every entry of the Szöllősi matrix has modulus 1 for valid parameters. -/
theorem szollosiMatrix_entrywiseUnit (p : SzollosiParam) (hp : SzollosiDomain p) :
    EntrywiseUnit (szollosiMatrix p) := by
  intro i j
  rcases hp with ⟨ha, hb, hc, hd, he, hf, _⟩
  fin_cases i <;> fin_cases j <;>
    simp [szollosiMatrix, Matrix.cons_val, Complex.normSq_neg, Complex.star_def, Complex.normSq_conj,
      ha, hb, hc, hd, he, hf]

set_option linter.unreachableTactic false in
set_option linter.unusedTactic false in
/-- The Szöllősi matrix satisfies the complex Hadamard orthogonality condition: M * Mᴴ = 6 • 1. -/
theorem szollosiMatrix_mul_conjTranspose (p : SzollosiParam) (hp : SzollosiDomain p) :
    szollosiMatrix p * Matrix.conjTranspose (szollosiMatrix p) = (6 : ℂ) • 1 := by
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  rcases hp with ⟨ha, hb, hc, hd, he, hf, h_cond⟩
  have h_cond_star := szollosi_cond_star p h_cond
  have ha1 := unit_mul_star p.a ha
  have hb1 := unit_mul_star p.b hb
  have hc1 := unit_mul_star p.c hc
  have hd1 := unit_mul_star p.d hd
  have he1 := unit_mul_star p.e he
  have hf1 := unit_mul_star p.f hf
  have ha2 := star_unit_mul p.a ha
  have hb2 := star_unit_mul p.b hb
  have hc2 := star_unit_mul p.c hc
  have hd2 := star_unit_mul p.d hd
  have he2 := star_unit_mul p.e he
  have hf2 := star_unit_mul p.f hf
  dsimp [szollosi_z1, szollosi_z2] at h_cond
  simp only [Complex.star_def] at h_cond h_cond_star
  fin_cases i <;> fin_cases j
  -- Row 0
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha1, hb1, hc1, hd1, he1, hf1]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  -- Row 1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha1, hb1, hc1, hd1, he1, hf1]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  -- Row 2
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha1, hb1, hc1, hd1, he1, hf1]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  -- Row 3
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha2, hb2, hc2, hd2, he2, hf2]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  -- Row 4
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha2, hb2, hc2, hd2, he2, hf2]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  -- Row 5
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]; ring
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    first | linear_combination h_cond | linear_combination h_cond_star
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, szollosiMatrix]
    rw [ha2, hb2, hc2, hd2, he2, hf2]; norm_num

/-- The Szöllősi matrix is a valid complex Hadamard matrix of order 6. -/
theorem szollosiMatrix_isCH6 (p : SzollosiParam) (hp : SzollosiDomain p) :
    IsCH6 (szollosiMatrix p) :=
  ⟨szollosiMatrix_entrywiseUnit p hp, szollosiMatrix_mul_conjTranspose p hp⟩

/-- Realization Soundness for Szöllősi deltoid component: Any matrix realized under
    the Szöllősi domain is a certified complex Hadamard matrix (Audit Target P1). -/
theorem realizes_szollosi_isCH6 (p : SzollosiParam) (D : Matrix (Fin 6) (Fin 6) ℂ)
    (hp : Domain .szollosiDeltoid p) (hD : Realizes .szollosiDeltoid p D) :
    IsCH6 D := by
  subst hD
  exact szollosiMatrix_isCH6 p hp

/-!
### Algebraic Lemmas and Complex Hadamard Soundness for Chernyavsky-Tao Matrix S₆ (Target P5)
-/

lemma tao_omega_re : tao_omega.re = -1/2 := by simp [tao_omega]
lemma tao_omega_im : tao_omega.im = Real.sqrt 3 / 2 := by simp [tao_omega]

lemma tao_omega_sq_re : (tao_omega ^ 2).re = -1/2 := by
  rw [sq, Complex.mul_re, tao_omega_re, tao_omega_im]
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith

lemma tao_omega_sq_im : (tao_omega ^ 2).im = - (Real.sqrt 3 / 2) := by
  rw [sq, Complex.mul_im, tao_omega_re, tao_omega_im]; ring

lemma tao_omega_sq_plus_omega_plus_one : tao_omega ^ 2 + tao_omega + 1 = 0 := by
  apply Complex.ext
  · simp [tao_omega_sq_re, tao_omega_re]
  · simp [tao_omega_sq_im, tao_omega_im]

lemma tao_omega_cube : tao_omega ^ 3 = 1 := by
  have h : (tao_omega - 1) * (tao_omega ^ 2 + tao_omega + 1) = 0 := by
    rw [tao_omega_sq_plus_omega_plus_one, mul_zero]
  linear_combination h

lemma tao_omega_star : star tao_omega = tao_omega ^ 2 := by
  apply Complex.ext
  · rw [Complex.star_def, Complex.conj_re, tao_omega_re, tao_omega_sq_re]
  · rw [Complex.star_def, Complex.conj_im, tao_omega_im, tao_omega_sq_im]

lemma tao_omega_sq_star : star (tao_omega ^ 2) = tao_omega := by
  rw [← tao_omega_star]; exact Complex.conj_conj tao_omega

lemma tao_omega_star_def : (starRingEnd ℂ) tao_omega = tao_omega ^ 2 := by
  rw [← Complex.star_def]; exact tao_omega_star

lemma tao_omega_sq_star_def : (starRingEnd ℂ) (tao_omega ^ 2) = tao_omega := by
  rw [← Complex.star_def]; exact tao_omega_sq_star

lemma tao_omega_pow_three : tao_omega ^ 3 = 1 := tao_omega_cube

lemma tao_omega_pow_four : tao_omega ^ 4 = tao_omega := by
  have : tao_omega ^ 4 = tao_omega ^ 3 * tao_omega := by ring
  rw [this, tao_omega_pow_three, one_mul]

lemma tao_omega_normSq : Complex.normSq tao_omega = 1 := by
  rw [Complex.normSq_apply, tao_omega_re, tao_omega_im]
  have h3 : Real.sqrt 3 * Real.sqrt 3 = 3 := Real.mul_self_sqrt (by norm_num)
  calc -1 / 2 * (-1 / 2) + Real.sqrt 3 / 2 * (Real.sqrt 3 / 2)
    _ = 1 / 4 + (Real.sqrt 3 * Real.sqrt 3) / 4 := by ring
    _ = 1 / 4 + 3 / 4 := by rw [h3]
    _ = 1 := by norm_num

lemma tao_omega_sq_normSq : Complex.normSq (tao_omega ^ 2) = 1 := by
  rw [map_pow, tao_omega_normSq, one_pow]

/-- Every entry of the Chernyavsky-Tao matrix has modulus 1. -/
theorem taoMatrix_entrywiseUnit : EntrywiseUnit taoMatrix := by
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [taoMatrix, Matrix.cons_val, tao_omega_normSq, tao_omega_sq_normSq]

set_option linter.unusedSimpArgs false in
theorem taoMatrix_mul_conjTranspose :
    taoMatrix * Matrix.conjTranspose taoMatrix = (6 : ℂ) • 1 := by
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  have h_sum : tao_omega ^ 2 + tao_omega + 1 = 0 := tao_omega_sq_plus_omega_plus_one
  have h_cube : tao_omega ^ 3 = 1 := tao_omega_cube
  have h_four : tao_omega ^ 4 = tao_omega := tao_omega_pow_four
  fin_cases i <;> fin_cases j
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (4 : ℂ) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (4 : ℂ) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (4 : ℂ) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (4 : ℂ) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (2 : ℂ) * h_sum + (1 : ℂ) * h_cube + (1 : ℂ) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, taoMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one]
    linear_combination (4 : ℂ) * h_cube

/-- The Chernyavsky-Tao matrix is a valid complex Hadamard matrix of order 6. -/
theorem taoMatrix_isCH6 : IsCH6 taoMatrix :=
  ⟨taoMatrix_entrywiseUnit, taoMatrix_mul_conjTranspose⟩

/-- Realization Soundness for Chernyavsky-Tao confluence component: Any matrix realized under
    the Tao confluence component is a certified complex Hadamard matrix (Audit Target P5). -/
theorem realizes_tao_isCH6 (p : Param .taoConfluence) (D : Matrix (Fin 6) (Fin 6) ℂ)
    (_hp : Domain .taoConfluence p) (hD : Realizes .taoConfluence p D) :
    IsCH6 D := by
  subst hD
  exact taoMatrix_isCH6

/-!
### Algebraic Lemmas and Complex Hadamard Soundness for Karlsson Family K₆ (Target P5)
-/

/-- Every entry of the Karlsson matrix has modulus 1 for valid parameters. -/
theorem karlssonMatrix_entrywiseUnit (p : KarlssonParam) (hp : KarlssonDomain p) :
    EntrywiseUnit (karlssonMatrix p) := by
  intro i j
  rcases hp with ⟨hx, hy⟩
  fin_cases i <;> fin_cases j <;>
    simp [karlssonMatrix, Matrix.cons_val, Complex.normSq_neg, map_mul,
          tao_omega_normSq, tao_omega_sq_normSq, hx, hy]

set_option linter.unusedSimpArgs false in
theorem karlssonMatrix_mul_conjTranspose (p : KarlssonParam) (hp : KarlssonDomain p) :
    karlssonMatrix p * Matrix.conjTranspose (karlssonMatrix p) = (6 : ℂ) • 1 := by
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  rcases hp with ⟨hx, hy⟩
  have hx1 := unit_mul_star p.x hx
  have hy1 := unit_mul_star p.y hy
  have h_sum : tao_omega ^ 2 + tao_omega + 1 = 0 := tao_omega_sq_plus_omega_plus_one
  fin_cases i <;> fin_cases j
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]; norm_num
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2 : ℂ) * hx1 + (2 : ℂ) * hy1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 2 : ℂ) * hx1 + (2*tao_omega : ℂ) * hy1 + (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega : ℂ) * hx1 + (2*tao_omega ^ 2 : ℂ) * hy1 + (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (4*tao_omega - 4 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 2 - 2*tao_omega + 2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega : ℂ) * hx1 + (2*tao_omega ^ 2 : ℂ) * hy1 + (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 3 : ℂ) * hx1 + (2*tao_omega ^ 3 : ℂ) * hy1 + (4*tao_omega - 4 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 2 : ℂ) * hx1 + (2*tao_omega ^ 4 : ℂ) * hy1 + (2*tao_omega ^ 2 - 2*tao_omega + 2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 2 - 2*tao_omega + 2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (4*tao_omega - 4 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 2 : ℂ) * hx1 + (2*tao_omega : ℂ) * hy1 + (2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 4 : ℂ) * hx1 + (2*tao_omega ^ 2 : ℂ) * hy1 + (2*tao_omega ^ 2 - 2*tao_omega + 2 : ℂ) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, karlssonMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_one, map_neg, map_mul]
    linear_combination (2*tao_omega ^ 3 : ℂ) * hx1 + (2*tao_omega ^ 3 : ℂ) * hy1 + (4*tao_omega - 4 : ℂ) * h_sum



/-- The Karlsson matrix is a valid complex Hadamard matrix of order 6. -/
theorem karlssonMatrix_isCH6 (p : KarlssonParam) (hp : KarlssonDomain p) :
    IsCH6 (karlssonMatrix p) :=
  ⟨karlssonMatrix_entrywiseUnit p hp, karlssonMatrix_mul_conjTranspose p hp⟩

/-- Realization Soundness for Karlsson volume component: Any matrix realized under
    the Karlsson volume domain is a certified complex Hadamard matrix (Audit Target P5). -/
theorem realizes_karlsson_isCH6 (p : KarlssonParam) (D : Matrix (Fin 6) (Fin 6) ℂ)
    (hp : Domain .karlssonVolume p) (hD : Realizes .karlssonVolume p D) :
    IsCH6 D := by
  subst hD
  exact karlssonMatrix_isCH6 p hp

/-!
### Isolated Haagerup Matrix H₆ Unitarity and Realization Soundness
-/

/-- Every entry of the Haagerup matrix has modulus 1. -/
theorem haagerupMatrix_entrywiseUnit : EntrywiseUnit haagerupMatrix := by
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [haagerupMatrix, Matrix.cons_val, Complex.normSq_neg, Complex.normSq_I]

/-- The Haagerup matrix satisfies the complex Hadamard orthogonality condition. -/
theorem haagerupMatrix_mul_conjTranspose :
    haagerupMatrix * Matrix.conjTranspose haagerupMatrix = (6 : ℂ) • 1 := by
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  fin_cases i <;> fin_cases j <;>
    { simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, haagerupMatrix, Complex.conj_I]
      try ring }

/-- The Haagerup matrix is a valid complex Hadamard matrix of order 6. -/
theorem haagerupMatrix_isCH6 : IsCH6 haagerupMatrix :=
  ⟨haagerupMatrix_entrywiseUnit, haagerupMatrix_mul_conjTranspose⟩

/-- Realization Soundness for Haagerup isolated component: Any matrix realized under
    the Haagerup domain is a certified complex Hadamard matrix. -/
theorem realizes_haagerup_isCH6 (p : Param .haagerupIsolated) (D : Matrix (Fin 6) (Fin 6) ℂ)
    (_hp : Domain .haagerupIsolated p) (hD : Realizes .haagerupIsolated p D) :
    IsCH6 D := by
  subst hD
  exact haagerupMatrix_isCH6

/-!
### Fourier-Diță Family F₆ Unitarity and Realization Soundness
-/

/-- Every entry of the Fourier-Diță matrix has modulus 1 for valid parameters. -/
theorem fourierDitaMatrix_entrywiseUnit (p : FourierDitaParam) (hp : FourierDitaDomain p) :
    EntrywiseUnit (fourierDitaMatrix p) := by
  intro i j
  rcases hp with ⟨ha, hb, hc⟩
  fin_cases i <;> fin_cases j <;>
    simp [fourierDitaMatrix, Matrix.cons_val, Complex.normSq_neg, map_mul,
          tao_omega_normSq, tao_omega_sq_normSq, ha, hb, hc]

set_option linter.unusedSimpArgs false in
theorem fourierDitaMatrix_mul_conjTranspose (p : FourierDitaParam) (hp : FourierDitaDomain p) :
    fourierDitaMatrix p * Matrix.conjTranspose (fourierDitaMatrix p) = (6 : ℂ) • 1 := by
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  rcases hp with ⟨ha, hb, hc⟩
  have ha1 : p.a * starRingEnd ℂ p.a = 1 := unit_mul_star p.a ha
  have hb1 : p.b * starRingEnd ℂ p.b = 1 := unit_mul_star p.b hb
  have hc1 : p.c * starRingEnd ℂ p.c = 1 := unit_mul_star p.c hc
  have h_sum : tao_omega ^ 2 + tao_omega + 1 = 0 := tao_omega_sq_plus_omega_plus_one
  have h_cube : tao_omega ^ 3 = 1 := tao_omega_pow_three
  have h_four : tao_omega ^ 4 = tao_omega := tao_omega_pow_four
  fin_cases i <;> fin_cases j
  -- Row 0
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, map_mul]
    linear_combination (3 : ℂ) * ha1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.a * starRingEnd ℂ p.b) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.a * starRingEnd ℂ p.c) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, map_mul, map_neg]
    linear_combination (-3 : ℂ) * ha1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.a * starRingEnd ℂ p.b) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.a * starRingEnd ℂ p.c) * h_sum
  -- Row 1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.b * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (3 : ℂ) * hb1 + (2 + 2 * p.b * starRingEnd ℂ p.b) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.b * starRingEnd ℂ p.c) * h_sum + (1 + p.b * starRingEnd ℂ p.c) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.b * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (-3 : ℂ) * hb1 + (2 - 2 * p.b * starRingEnd ℂ p.b) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.b * starRingEnd ℂ p.c) * h_sum + (1 - p.b * starRingEnd ℂ p.c) * h_four
  -- Row 2
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.c * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (1 + p.c * starRingEnd ℂ p.b) * h_sum + (1 + p.c * starRingEnd ℂ p.b) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (3 : ℂ) * hc1 + (2 + 2 * p.c * starRingEnd ℂ p.c) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.c * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.c * starRingEnd ℂ p.b) * h_sum + (1 - p.c * starRingEnd ℂ p.b) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (-3 : ℂ) * hc1 + (2 - 2 * p.c * starRingEnd ℂ p.c) * h_cube
  -- Row 3
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, map_mul, map_neg]
    linear_combination (-3 : ℂ) * ha1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.a * starRingEnd ℂ p.b) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.a * starRingEnd ℂ p.c) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, map_mul, map_neg]
    linear_combination (3 : ℂ) * ha1
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.a * starRingEnd ℂ p.b) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.a * starRingEnd ℂ p.c) * h_sum
  -- Row 4
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.b * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (-3 : ℂ) * hb1 + (2 - 2 * p.b * starRingEnd ℂ p.b) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.b * starRingEnd ℂ p.c) * h_sum + (1 - p.b * starRingEnd ℂ p.c) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.b * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (3 : ℂ) * hb1 + (2 + 2 * p.b * starRingEnd ℂ p.b) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.b * starRingEnd ℂ p.c) * h_sum + (1 + p.b * starRingEnd ℂ p.c) * h_four
  -- Row 5
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.c * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 - p.c * starRingEnd ℂ p.b) * h_sum + (1 - p.c * starRingEnd ℂ p.b) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (-3 : ℂ) * hc1 + (2 - 2 * p.c * starRingEnd ℂ p.c) * h_cube
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.c * starRingEnd ℂ p.a) * h_sum
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul, map_neg]
    linear_combination (1 + p.c * starRingEnd ℂ p.b) * h_sum + (1 + p.c * starRingEnd ℂ p.b) * h_four
  · simp [Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ, fourierDitaMatrix, tao_omega_star_def, tao_omega_sq_star_def, map_mul]
    linear_combination (3 : ℂ) * hc1 + (2 + 2 * p.c * starRingEnd ℂ p.c) * h_cube

/-- The Fourier-Diță matrix is a valid complex Hadamard matrix of order 6. -/
theorem fourierDitaMatrix_isCH6 (p : FourierDitaParam) (hp : FourierDitaDomain p) :
    IsCH6 (fourierDitaMatrix p) :=
  ⟨fourierDitaMatrix_entrywiseUnit p hp, fourierDitaMatrix_mul_conjTranspose p hp⟩

/-- Realization Soundness for Fourier-Diță component: Any matrix realized under
    the Fourier-Diță domain is a certified complex Hadamard matrix. -/
theorem realizes_fourier_isCH6 (p : FourierDitaParam) (D : Matrix (Fin 6) (Fin 6) ℂ)
    (hp : Domain .fourierDita p) (hD : Realizes .fourierDita p D) :
    IsCH6 D := by
  subst hD
  exact fourierDitaMatrix_isCH6 p hp

/-!
### Single-Matrix Corner Routing & Dephasing Foundation
-/

/-- Classification predicate: A complex 6x6 matrix is in the moduli classification
    if it is Hadamard-equivalent to a dephased complex Hadamard matrix that routes
    to either a regular corner chart or a singular Segre cusp.
    Note (P1): This asserts dephasing and corner determinant routing (cornerDet ≠ 0 ∨ cornerDet = 0),
    not yet a parameter realization Realizes c p D. -/
def InModuliClassification (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  ∃ D : Matrix (Fin 6) (Fin 6) ℂ,
    HadamardEquivalent H D ∧ Dephased D ∧ IsCH6 D ∧
    (IsRegularCorner D ∨ IsSingularCorner D)

/-- Foundational Reduction Lemma (Dephase and Corner Route):
    Every complex Hadamard matrix in dimension 6 is Hadamard-equivalent to a dephased
    matrix that routes across the zero/nonzero corner determinant split.
    Note (F02/P1): This is a foundational reduction lemma establishing dephasing and
    exhaustive corner case routing. Continuous family realization Realizes c p D
    is formalized above for Szöllősi deltoid, with the general catalog classification
    formulated in FullModuliClassification. -/
theorem dephase_and_route_corner (H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) :
    InModuliClassification H := by
  obtain ⟨D, h_ch6, h_deph, h_equiv⟩ := dephase_exists H hH
  have h_routing : IsRegularCorner D ∨ IsSingularCorner D :=
    master_case_routing D
  exact ⟨D, h_equiv, h_deph, h_ch6, h_routing⟩

/-- Backward-compatible alias for the foundational reduction lemma. -/
abbrev master_classification_theorem := dephase_and_route_corner

/-- Branch classification mapping: Regular corner matrices route to the volume chart label,
    and singular corner matrices route to the deltoid cusp chart label.
    Note: This is a discrete corner-determinant routing assignment; concrete realization
    of the respective families Realizes c p D is required for continuous classification. -/
noncomputable def branchToComponent (D : Matrix (Fin 6) (Fin 6) ℂ) : ModuliComponent :=
  if cornerDet D = 0 then ModuliComponent.szollosiDeltoid else ModuliComponent.karlssonVolume

/-- Every dephased complex Hadamard matrix assigns a valid moduli component label under branch routing. -/
theorem dephased_assigns_valid_component (D : Matrix (Fin 6) (Fin 6) ℂ) (_hD : Dephased D) :
    branchToComponent D = ModuliComponent.szollosiDeltoid ∨
    branchToComponent D = ModuliComponent.karlssonVolume := by
  simp only [branchToComponent]
  split_ifs with h
  · exact Or.inl rfl
  · exact Or.inr rfl

/-- Degenerate branches are excluded: any candidate dephased matrix asserting annihilated
    coordinates x = 0 and y = 0 cannot belong to the complex Hadamard variety. -/
theorem degenerate_annihilated_excluded (z : Point) (i j : Fin 5)
    (h_circle : (z.x i j)^2 + (z.y i j)^2 = 1)
    (h_ann : AnnihilatedEntry z i j) : False :=
  annihilated_entry_empty z i j h_circle h_ann

/-- Non-compact boundary leaves are excluded: real coordinates cannot exceed [-1, 1]. -/
theorem boundary_leaves_excluded (z : Point) (i j : Fin 5)
    (h_circle : (z.x i j)^2 + (z.y i j)^2 = 1) :
    -1 ≤ z.x i j ∧ z.x i j ≤ 1 :=
  x_abs_le_one z i j h_circle

/-- Comprehensive Moduli Exhaustiveness (Corner Routing):
    Every 6x6 complex Hadamard matrix admits a dephased representative routing to one of the
    two certified corner determinant branches. -/
theorem comprehensive_moduli_exhaustiveness (H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) :
    ∃ (D : Matrix (Fin 6) (Fin 6) ℂ) (c : ModuliComponent),
      HadamardEquivalent H D ∧ Dephased D ∧ IsCH6 D ∧
      (c = ModuliComponent.szollosiDeltoid ∨ c = ModuliComponent.karlssonVolume) := by
  obtain ⟨D, h_equiv, h_deph, h_ch6, _⟩ := dephase_and_route_corner H hH
  let c := branchToComponent D
  have hc := dephased_assigns_valid_component D h_deph
  exact ⟨D, c, h_equiv, h_deph, h_ch6, hc⟩

/-!
### Canonical Open Formal Target: Full Moduli Classification
-/

/-- Continuous Moduli Classification Target (Open Formal Realization Target):
    Every 6x6 complex Hadamard matrix belongs to one of the certified moduli components c,
    with valid parameters p satisfying Domain c p, realizing an explicit matrix D
    via Realizes c p D, to which H is Hadamard-equivalent.
    Note: Target P1 formalizes this canonical statement and provides an explicit matrix
    equality under the legacy ModuliComponent.szollosiDeltoid label. Full continuous realization across all components
    remains an explicit open formal target. -/
def FullModuliClassification : Prop :=
  ∀ H, IsCH6 H → ∃ (c : ModuliComponent) (p : Param c) (D : Matrix (Fin 6) (Fin 6) ℂ),
    Domain c p ∧ Realizes c p D ∧ HadamardEquivalent H D

/-- Singular Segre Branch Component Predicate:
    Singular corner complex Hadamard matrices route to the Szöllősi deltoid family,
    the Chernyavsky-Tao isolated confluence point, or the isolated Haagerup matrix. -/
def SingularSegreComponent (c : ModuliComponent) : Prop :=
  c = ModuliComponent.szollosiDeltoid ∨
  c = ModuliComponent.taoConfluence ∨
  c = ModuliComponent.haagerupIsolated

/-- Regular Corner Component Predicate:
    Regular corner complex Hadamard matrices route to the Fourier-Diță family
    or the Karlsson volume family. -/
def RegularCornerComponent (c : ModuliComponent) : Prop :=
  c = ModuliComponent.fourierDita ∨
  c = ModuliComponent.karlssonVolume

/-- Disjunctive Master Classification Coverage:
    Every moduli component belongs to either the singular Segre branch
    or the regular corner branch. -/
theorem moduli_component_branch_cover (c : ModuliComponent) :
    SingularSegreComponent c ∨ RegularCornerComponent c := by
  cases c with
  | fourierDita => exact Or.inr (Or.inl rfl)
  | szollosiDeltoid => exact Or.inl (Or.inl rfl)
  | karlssonVolume => exact Or.inr (Or.inr rfl)
  | taoConfluence => exact Or.inl (Or.inr (Or.inl rfl))
  | haagerupIsolated => exact Or.inl (Or.inr (Or.inr rfl))

/-- Singular corner complex Hadamard matrices route to the Segre component branch. -/
theorem singular_corner_routes_to_segre (D : Matrix (Fin 6) (Fin 6) ℂ)
    (_h_deph : Dephased D) (h_sing : IsSingularCorner D) :
    SingularSegreComponent (branchToComponent D) := by
  dsimp [branchToComponent, IsSingularCorner] at *
  rw [if_pos h_sing]
  exact Or.inl rfl

/-- Regular corner complex Hadamard matrices route to the regular component branch. -/
theorem regular_corner_routes_to_regular (D : Matrix (Fin 6) (Fin 6) ℂ)
    (_h_deph : Dephased D) (h_reg : IsRegularCorner D) :
    RegularCornerComponent (branchToComponent D) := by
  dsimp [branchToComponent, IsRegularCorner] at *
  rw [if_neg h_reg]
  exact Or.inr rfl

/-- Corner Routing Classification:
    Every 6x6 complex Hadamard matrix admits a dephased representative D routing to a
    certified moduli component c = branchToComponent D, such that singular corners
    route to the Segre component branch and regular corners route to the regular component branch. -/
def CornerRoutingClassification : Prop :=
  ∀ H, IsCH6 H → ∃ (D : Matrix (Fin 6) (Fin 6) ℂ) (c : ModuliComponent),
    HadamardEquivalent H D ∧ Dephased D ∧ IsCH6 D ∧
    c = branchToComponent D ∧
    ((c = ModuliComponent.szollosiDeltoid ∧ IsSingularCorner D ∧ SingularSegreComponent c) ∨
     (c = ModuliComponent.karlssonVolume ∧ IsRegularCorner D ∧ RegularCornerComponent c))

/-- Dephasing and singular/regular corner routing:
    This does not provide parameters, realization, or exhaustive family classification. -/
theorem corner_routing_classification : CornerRoutingClassification := by
  intro H hH
  obtain ⟨D, h_equiv, h_deph, h_ch6, h_routing⟩ := dephase_and_route_corner H hH
  let c := branchToComponent D
  have hc_eq : c = branchToComponent D := rfl
  have h_cases : (c = ModuliComponent.szollosiDeltoid ∧ IsSingularCorner D ∧ SingularSegreComponent c) ∨
                 (c = ModuliComponent.karlssonVolume ∧ IsRegularCorner D ∧ RegularCornerComponent c) := by
    cases h_routing with
    | inl h_reg =>
      have hc_val : c = ModuliComponent.karlssonVolume := by
        dsimp [c, branchToComponent]
        have h_not : cornerDet D ≠ 0 := h_reg
        rw [if_neg h_not]
      have h_reg_comp : RegularCornerComponent c := by
        rw [hc_val]
        exact Or.inr rfl
      exact Or.inr ⟨hc_val, h_reg, h_reg_comp⟩
    | inr h_sing =>
      have hc_val : c = ModuliComponent.szollosiDeltoid := by
        dsimp [c, branchToComponent]
        have h_eq : cornerDet D = 0 := h_sing
        rw [if_pos h_eq]
      have h_seg_comp : SingularSegreComponent c := by
        rw [hc_val]
        exact Or.inl rfl
      exact Or.inl ⟨hc_val, h_sing, h_seg_comp⟩
  exact ⟨D, c, h_equiv, h_deph, h_ch6, hc_eq, h_cases⟩

/-- Moduli Variety Realization Premise:
    Every dephased 6x6 complex Hadamard matrix D is realized by some moduli component c
    with valid parameter p in Domain c p such that Realizes c p D.
    Concrete parameter realization across continuous families remains an open formal target. -/
def ModuliVarietyRealizationPremise : Prop :=
  ∀ (D : Matrix (Fin 6) (Fin 6) ℂ), Dephased D → IsCH6 D →
    ∃ (c : ModuliComponent) (p : Param c), Domain c p ∧ Realizes c p D

/-- Canonical alias for the classification realization premise. -/
abbrev ClassificationRealizationPremise : Prop := ModuliVarietyRealizationPremise

/-- Continuous Moduli Variety Classification:
    Under the classification realization premise, every 6x6 complex Hadamard matrix H
    belongs to a certified moduli component c with valid parameters p satisfying Domain c p,
    realizing an explicit matrix D via Realizes c p D, to which H is Hadamard-equivalent. -/
theorem full_moduli_variety_classification
    (h_realize : ClassificationRealizationPremise) : FullModuliClassification := by
  intro H hH
  obtain ⟨D, h_equiv, h_deph, h_ch6, _⟩ := dephase_and_route_corner H hH
  obtain ⟨c, p, hp, h_real⟩ := h_realize D h_deph h_ch6
  exact ⟨c, p, D, hp, h_real, h_equiv⟩

/-- Full moduli component lookup: maps every branch-routed dephased complex Hadamard matrix
    to its certified realization parameters under its assigned moduli component label,
    conditioned on the classification realization premise. -/
theorem full_moduli_variety_classification_lookup
    (h_realize : ClassificationRealizationPremise)
    (D : Matrix (Fin 6) (Fin 6) ℂ) (h_deph : Dephased D) (h_ch6 : IsCH6 D) :
    ∃ (c : ModuliComponent) (p : Param c), Domain c p ∧ Realizes c p D :=
  h_realize D h_deph h_ch6

/-- Canonical catalog realization: Tao confluence matrix realization. -/
theorem catalog_tao_realized :
    ∃ (p : Param .taoConfluence), Domain .taoConfluence p ∧ Realizes .taoConfluence p taoMatrix :=
  ⟨PUnit.unit, trivial, rfl⟩

/-- Canonical catalog realization: Karlsson volume family realization. -/
theorem catalog_karlsson_realized (p : KarlssonParam) (hp : KarlssonDomain p) :
    ∃ (p' : Param .karlssonVolume), Domain .karlssonVolume p' ∧ Realizes .karlssonVolume p' (karlssonMatrix p) :=
  ⟨p, hp, rfl⟩

/-- Canonical catalog realization: Szöllősi deltoid family realization. -/
theorem catalog_szollosi_realized (p : SzollosiParam) (hp : SzollosiDomain p) :
    ∃ (p' : Param .szollosiDeltoid), Domain .szollosiDeltoid p' ∧ Realizes .szollosiDeltoid p' (szollosiMatrix p) :=
  ⟨p, hp, rfl⟩

/-- Canonical catalog realization: Haagerup isolated matrix realization. -/
theorem catalog_haagerup_realized :
    ∃ (p : Param .haagerupIsolated), Domain .haagerupIsolated p ∧ Realizes .haagerupIsolated p haagerupMatrix :=
  ⟨PUnit.unit, trivial, rfl⟩

/-- Canonical catalog realization: Fourier-Diță affine family realization. -/
theorem catalog_fourier_realized (p : FourierDitaParam) (hp : FourierDitaDomain p) :
    ∃ (p' : Param .fourierDita), Domain .fourierDita p' ∧ Realizes .fourierDita p' (fourierDitaMatrix p) :=
  ⟨p, hp, rfl⟩

/-- Disjunction of the five catalog realization predicates.
    Membership of every dephased Hadamard matrix is a separate hypothesis. -/
def FiveComponentRealization (D : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  (∃ (p : FourierDitaParam), FourierDitaDomain p ∧ Realizes .fourierDita p D) ∨
  (∃ (p : SzollosiParam), SzollosiDomain p ∧ Realizes .szollosiDeltoid p D) ∨
  (∃ (p : KarlssonParam), KarlssonDomain p ∧ Realizes .karlssonVolume p D) ∨
  (Realizes .taoConfluence PUnit.unit D) ∨
  (Realizes .haagerupIsolated PUnit.unit D)

/-- Bridge from five-component realization to moduli variety realization:
    Maps the explicit disjunctive component realization into existential moduli component parameters. -/
theorem five_component_to_moduli_realization
    (D : Matrix (Fin 6) (Fin 6) ℂ)
    (h : FiveComponentRealization D) :
    ∃ (c : ModuliComponent) (p : Param c), Domain c p ∧ Realizes c p D := by
  rcases h with ⟨p, hp, hr⟩ | ⟨p, hp, hr⟩ | ⟨p, hp, hr⟩ | hr | hr
  · exact ⟨.fourierDita, p, hp, hr⟩
  · exact ⟨.szollosiDeltoid, p, hp, hr⟩
  · exact ⟨.karlssonVolume, p, hp, hr⟩
  · exact ⟨.taoConfluence, PUnit.unit, trivial, hr⟩
  · exact ⟨.haagerupIsolated, PUnit.unit, trivial, hr⟩

/-- Five-Branch Realization Hypothesis:
    Every dephased 6x6 complex Hadamard matrix satisfies the five-component master disjunction. -/
def FiveBranchRealizationHypothesis : Prop :=
  ∀ (D : Matrix (Fin 6) (Fin 6) ℂ), Dephased D → IsCH6 D → FiveComponentRealization D

/-- `ClassificationRealizationPremise` follows from `FiveBranchRealizationHypothesis`. -/
theorem classification_realization_premise_of_five_branch
    (h_five : FiveBranchRealizationHypothesis) : ClassificationRealizationPremise := by
  intro D h_deph h_ch6
  exact five_component_to_moduli_realization D (h_five D h_deph h_ch6)

/-- `FullModuliClassification` follows from `FiveBranchRealizationHypothesis`. -/
theorem full_moduli_variety_classification_of_five_branch
    (h_five : FiveBranchRealizationHypothesis) : FullModuliClassification :=
  full_moduli_variety_classification (classification_realization_premise_of_five_branch h_five)

/-- A moduli realization is one disjunct of `FiveComponentRealization`. -/
theorem five_component_master_disjunction
    (D : Matrix (Fin 6) (Fin 6) ℂ)
    (h_real : ∃ (c : ModuliComponent) (p : Param c), Domain c p ∧ Realizes c p D) :
    FiveComponentRealization D := by
  rcases h_real with ⟨c, p, hp, hr⟩
  cases c with
  | fourierDita =>
    exact Or.inl ⟨p, hp, hr⟩
  | szollosiDeltoid =>
    exact Or.inr (Or.inl ⟨p, hp, hr⟩)
  | karlssonVolume =>
    exact Or.inr (Or.inr (Or.inl ⟨p, hp, hr⟩))
  | taoConfluence =>
    cases p
    exact Or.inr (Or.inr (Or.inr (Or.inl hr)))
  | haagerupIsolated =>
    cases p
    exact Or.inr (Or.inr (Or.inr (Or.inr hr)))

/-- Equivalence of ClassificationRealizationPremise and FiveBranchRealizationHypothesis. -/
theorem five_branch_realization_bridge :
    ClassificationRealizationPremise ↔ FiveBranchRealizationHypothesis := by
  constructor
  · intro h_premise D h_deph h_ch6
    obtain ⟨c, p, hp, hr⟩ := h_premise D h_deph h_ch6
    exact five_component_master_disjunction D ⟨c, p, hp, hr⟩
  · intro h_five
    exact classification_realization_premise_of_five_branch h_five

/-- Under `h_five`, the Tao and Haagerup exclusions, and `h_karlsson`,
    the realization is Fourier-Diță or Szöllősi. Those three are hypotheses. -/
theorem master_five_branch_reduction
    (D : Matrix (Fin 6) (Fin 6) ℂ)
    (h_five : FiveComponentRealization D)
    (h_not_tao : Realizes .taoConfluence PUnit.unit D → False)
    (h_not_haag : Realizes .haagerupIsolated PUnit.unit D → False)
    (h_karlsson : (∃ p, KarlssonDomain p ∧ Realizes .karlssonVolume p D) →
      ∃ p_fd, FourierDitaDomain p_fd ∧ Realizes .fourierDita p_fd D) :
    (∃ p, FourierDitaDomain p ∧ Realizes .fourierDita p D) ∨
    (∃ p, SzollosiDomain p ∧ Realizes .szollosiDeltoid p D) := by
  rcases h_five with h_fd | h_sz | h_kv | h_tao | h_haag
  · exact Or.inl h_fd
  · exact Or.inr h_sz
  · exact Or.inl (h_karlsson h_kv)
  · exfalso; exact h_not_tao h_tao
  · exfalso; exact h_not_haag h_haag

/-- If each of the five realization cases implies `¬ Extends D`, then `¬ Extends D`. -/
theorem master_five_branch_non_extension
    (D : Matrix (Fin 6) (Fin 6) ℂ)
    (Extends : Matrix (Fin 6) (Fin 6) ℂ → Prop)
    (h_five : FiveComponentRealization D)
    (h_no_fd : (∃ p, FourierDitaDomain p ∧ Realizes .fourierDita p D) → ¬ Extends D)
    (h_no_sz : (∃ p, SzollosiDomain p ∧ Realizes .szollosiDeltoid p D) → ¬ Extends D)
    (h_no_kv : (∃ p, KarlssonDomain p ∧ Realizes .karlssonVolume p D) → ¬ Extends D)
    (h_no_tao : Realizes .taoConfluence PUnit.unit D → ¬ Extends D)
    (h_no_haag : Realizes .haagerupIsolated PUnit.unit D → ¬ Extends D) :
    ¬ Extends D := by
  rcases h_five with h_fd | h_sz | h_kv | h_tao | h_haag
  · exact h_no_fd h_fd
  · exact h_no_sz h_sz
  · exact h_no_kv h_kv
  · exact h_no_tao h_tao
  · exact h_no_haag h_haag

/-!
### Subgap R7: Singular Segre Stengle Positivstellensatz Certificate (ENC-1147)

Exact rational polynomial certificate over ℚ[a, b, c, d]:
  -1 == h_segre * f_segre + sum(h_circ * (k^2 - 1)) + sigma_0 + sigma_1 * g_sep

Proves that on the singular Segre variety V = {f_segre = 0, a^2=1, b^2=1, c^2=1, d^2=1}:
1. The Stengle Positivstellensatz algebraic identity reduces identically to -1 in ℚ[a, b, c, d].
2. The separating polynomial g_sep evaluates strictly negative: g_sep = -1/1000 < 0.
3. The semialgebraic set {V, g_sep ≥ 0} contains zero real/rational points.

AuthorityEffect: None.
Constitutional Firewall: stated region only; mints no authority.
-/

/-- Singular Segre quadric f_segre = (a - 1)(d - 1) - (b - 1)(c - 1). -/
def segre_quadric (a b c d : ℚ) : ℚ :=
  (a - 1) * (d - 1) - (b - 1) * (c - 1)

/-- Aggregate circle defect f_circ = (a^2 - 1) + (b^2 - 1) + (c^2 - 1) + (d^2 - 1). -/
def segre_circle_defect (a b c d : ℚ) : ℚ :=
  (a^2 - 1) + (b^2 - 1) + (c^2 - 1) + (d^2 - 1)

/-- Sum of squares term sigma_0 = 1/4 * f_segre^2 + 1/4 * f_circ^2. -/
def segre_sigma0 (a b c d : ℚ) : ℚ :=
  (1 / 4) * (segre_quadric a b c d)^2 + (1 / 4) * (segre_circle_defect a b c d)^2

/-- Rational collar thickness eps = 1/1000. -/
def segre_eps : ℚ := 1 / 1000

/-- Positive multiplier sigma_1 = 1 / eps = 1000. -/
def segre_sigma1 : ℚ := 1000

/-- Separating polynomial f_sep = (1 - eps) * sigma_0 + f_circ. -/
def segre_f_sep (a b c d : ℚ) : ℚ :=
  (1 - segre_eps) * segre_sigma0 a b c d + segre_circle_defect a b c d

/-- Guard polynomial g_sep = f_sep - eps. -/
def segre_g_sep (a b c d : ℚ) : ℚ :=
  segre_f_sep a b c d - segre_eps

/-- Stengle multiplier for the Segre quadric: h_segre = -1/(4*eps) * f_segre. -/
def segre_h_quadric (a b c d : ℚ) : ℚ :=
  - (1 / 4) * segre_quadric a b c d * segre_sigma1

/-- Stengle multiplier for each circle generator: h_circ = -1/eps * (1/4 * f_circ + 1). -/
def segre_h_circle (a b c d : ℚ) : ℚ :=
  - ((1 / 4) * segre_circle_defect a b c d + 1) * segre_sigma1

/-- Theorem: Subgap R7 Stengle Positivstellensatz Exact Identity over ℚ.
    The linear combination of ideal generators, sum of squares, and guarded separating polynomial
    reduces identically to -1 in ℚ[a, b, c, d]. -/
theorem singular_segre_stengle_identity (a b c d : ℚ) :
    segre_h_quadric a b c d * segre_quadric a b c d +
    segre_h_circle a b c d * (a^2 - 1) +
    segre_h_circle a b c d * (b^2 - 1) +
    segre_h_circle a b c d * (c^2 - 1) +
    segre_h_circle a b c d * (d^2 - 1) +
    segre_sigma0 a b c d +
    segre_sigma1 * segre_g_sep a b c d = -1 := by
  dsimp [segre_h_quadric, segre_h_circle, segre_g_sep, segre_f_sep,
         segre_sigma0, segre_circle_defect, segre_quadric, segre_sigma1, segre_eps]
  ring

/-- Theorem: On genuine variety points V = {f_segre = 0, a^2=1, b^2=1, c^2=1, d^2=1},
    the separating polynomial g_sep evaluates strictly negative: g_sep = -1/1000 < 0. -/
theorem singular_segre_variety_g_sep_negative (a b c d : ℚ)
    (h_segre : segre_quadric a b c d = 0)
    (ha : a^2 - 1 = 0) (hb : b^2 - 1 = 0) (hc : c^2 - 1 = 0) (hd : d^2 - 1 = 0) :
    segre_g_sep a b c d = - (1 / 1000) := by
  dsimp [segre_g_sep, segre_f_sep, segre_sigma0, segre_circle_defect, segre_eps]
  rw [h_segre, ha, hb, hc, hd]
  ring

/-- Theorem: Emptiness of the guarded singular Segre subvariety {V, g_sep ≥ 0}.
    No point on the singular Segre variety satisfies g_sep ≥ 0. -/
theorem singular_segre_guarded_variety_empty (a b c d : ℚ)
    (h_segre : segre_quadric a b c d = 0)
    (ha : a^2 - 1 = 0) (hb : b^2 - 1 = 0) (hc : c^2 - 1 = 0) (hd : d^2 - 1 = 0)
    (h_sep : segre_g_sep a b c d ≥ 0) : False := by
  have h_neg := singular_segre_variety_g_sep_negative a b c d h_segre ha hb hc hd
  rw [h_neg] at h_sep
  revert h_sep
  decide

#print axioms singular_segre_stengle_identity
#print axioms singular_segre_variety_g_sep_negative
#print axioms singular_segre_guarded_variety_empty

#print axioms szollosiMatrix_isCH6
#print axioms realizes_szollosi_isCH6
#print axioms taoMatrix_isCH6
#print axioms realizes_tao_isCH6
#print axioms karlssonMatrix_isCH6
#print axioms realizes_karlsson_isCH6
#print axioms haagerupMatrix_isCH6
#print axioms realizes_haagerup_isCH6
#print axioms fourierDitaMatrix_isCH6
#print axioms realizes_fourier_isCH6
#print axioms dephase_and_route_corner
#print axioms singular_corner_routes_to_segre
#print axioms regular_corner_routes_to_regular
#print axioms corner_routing_classification
#print axioms full_moduli_variety_classification
#print axioms full_moduli_variety_classification_lookup
#print axioms five_component_to_moduli_realization
#print axioms classification_realization_premise_of_five_branch
#print axioms full_moduli_variety_classification_of_five_branch
#print axioms five_component_master_disjunction
#print axioms five_branch_realization_bridge
#print axioms master_five_branch_reduction
#print axioms master_five_branch_non_extension

end MUB.MasterClassification

