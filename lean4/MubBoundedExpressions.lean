import MubBoundedPolynomials
import Mathlib.Algebra.MvPolynomial.Degrees

/-!
# Executable expressions for the bounded quartet polynomials

AuthorityEffect: None.

The arithmetic expressions retain the full rational polynomial specification.
Their interpretation is checked before any numerical or coefficient export.
-/

namespace MUB.BoundedExpressions
open BoundedCoordinates BoundedPolynomials BoundedBlockChart
open scoped BigOperators

inductive Expr where
  | constant : Rat → Expr
  | input : Coord → Expr
  | add : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  | neg : Expr → Expr
  deriving Inhabited

instance : Add Expr := ⟨Expr.add⟩
instance : Mul Expr := ⟨Expr.mul⟩
instance : Neg Expr := ⟨Expr.neg⟩
instance : Sub Expr := ⟨fun p q => p + -q⟩
instance (n : Nat) : OfNat Expr n := ⟨Expr.constant n⟩

noncomputable def Expr.polynomial : Expr → Poly
  | .constant q => MvPolynomial.C q
  | .input v => MvPolynomial.X v
  | .add p q => p.polynomial + q.polynomial
  | .mul p q => p.polynomial * q.polynomial
  | .neg p => -p.polynomial

@[simp] theorem polynomial_add (p q : Expr) : (p + q).polynomial = p.polynomial + q.polynomial := rfl
@[simp] theorem polynomial_mul (p q : Expr) : (p * q).polynomial = p.polynomial * q.polynomial := rfl
@[simp] theorem polynomial_neg (p : Expr) : (-p).polynomial = -p.polynomial := rfl
@[simp] theorem polynomial_sub (p q : Expr) : (p - q).polynomial = p.polynomial - q.polynomial := by
  exact (sub_eq_add_neg _ _).symm
@[simp] theorem polynomial_nat (n : Nat) : (ofNat(n) : Expr).polynomial = (n : Poly) := by
  change MvPolynomial.C (n : Rat) = (n : Poly)
  simp

structure CExpr where
  re : Expr
  im : Expr
  deriving Inhabited

instance : Zero CExpr := ⟨⟨0, 0⟩⟩
instance : One CExpr := ⟨⟨1, 0⟩⟩
instance : Add CExpr := ⟨fun p q => ⟨p.re + q.re, p.im + q.im⟩⟩
instance : Neg CExpr := ⟨fun p => ⟨-p.re, -p.im⟩⟩
instance : Sub CExpr := ⟨fun p q => ⟨p.re - q.re, p.im - q.im⟩⟩
instance : Mul CExpr := ⟨fun p q => ⟨p.re * q.re - p.im * q.im, p.re * q.im + p.im * q.re⟩⟩
instance : Star CExpr := ⟨fun p => ⟨p.re, -p.im⟩⟩

noncomputable def translate (p : CExpr) : CPoly := ⟨p.re.polynomial, p.im.polynomial⟩
@[simp] theorem translate_zero : translate 0 = 0 := by
  change (⟨MvPolynomial.C (0 : ℚ), MvPolynomial.C (0 : ℚ)⟩ : CPoly) = 0
  simp only [map_zero]
  rfl
@[simp] theorem translate_one : translate 1 = 1 := by
  change (⟨MvPolynomial.C (1 : ℚ), MvPolynomial.C (0 : ℚ)⟩ : CPoly) = 1
  simp only [map_one, map_zero]
  rfl
@[simp] theorem translate_add (p q : CExpr) : translate (p + q) = translate p + translate q := rfl
@[simp] theorem translate_neg (p : CExpr) : translate (-p) = -translate p := rfl
@[simp] theorem translate_sub (p q : CExpr) : translate (p - q) = translate p - translate q := by
  apply QuadraticAlgebra.ext <;> exact polynomial_sub _ _
@[simp] theorem translate_mul (p q : CExpr) : translate (p * q) = translate p * translate q := by
  apply QuadraticAlgebra.ext
  · change (p.re * q.re - p.im * q.im).polynomial = (translate p * translate q).re
    simp [translate, sub_eq_add_neg]
  · change (p.re * q.im + p.im * q.re).polynomial = (translate p * translate q).im
    simp [translate]
@[simp] theorem translate_star (p : CExpr) : translate (star p) = star (translate p) := by
  apply QuadraticAlgebra.ext
  · change p.re.polynomial = _
    simp [translate]
  · rfl

def eNorm (p : CExpr) : Expr := p.re * p.re + p.im * p.im
def eReal (p : Expr) : CExpr := ⟨p, 0⟩
def eComponent (p : CExpr) (b : Bool) : Expr := if b then p.im else p.re

@[simp] theorem translate_norm (p : CExpr) : (eNorm p).polynomial = normPoly (translate p) := by
  simp [eNorm, normPoly, translate, pow_two]
@[simp] theorem translate_real (p : Expr) : translate (eReal p) = liftReal p.polynomial := by
  apply QuadraticAlgebra.ext <;> simp [eReal, translate, liftReal]
@[simp] theorem translate_component (p : CExpr) (b : Bool) :
    (eComponent p b).polynomial = component (translate p) b := by cases b <;> rfl

def eVariable (s : Slot) : CExpr := ⟨.input (s, false), .input (s, true)⟩
@[simp] theorem translate_variable (s : Slot) : translate (eVariable s) = coordinatePoly s := rfl

abbrev EMat3 := Matrix I3 I3 CExpr
abbrev EMat6 := Matrix I6 I6 CExpr
noncomputable def matrixTranslate {ι κ : Type*} (A : Matrix ι κ CExpr) : Matrix ι κ CPoly :=
  fun i j => translate (A i j)

def eE : EMat3 := fillE (fun s => eVariable (.inl s))
def eB : EMat3 := fillB (fun s => eVariable (.inr (.inl s)))
def eC : EMat3 := fillC (fun s => eVariable (.inr (.inr (.inl s))))
def eU : EMat6 := fillBasis (fun s => eVariable (.inr (.inr (.inr (.inl s)))))
def eV : EMat6 := fillBasis (fun s => eVariable (.inr (.inr (.inr (.inr s)))))

@[simp] theorem translate_E : matrixTranslate eE = pE := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · exact congrArg (fun z : CPoly => z) translate_one
  · refine Fin.cases ?_ (fun l => ?_) j
    · exact translate_one
    · rfl
@[simp] theorem translate_B : matrixTranslate eB = pB := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · exact translate_one
  · rfl
@[simp] theorem translate_C : matrixTranslate eC = pC := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) j
  · exact translate_one
  · rfl
@[simp] theorem translate_U : matrixTranslate eU = pU := by
  funext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · exact translate_one
  · simp [matrixTranslate, eU, pU, fillBasis]
@[simp] theorem translate_V : matrixTranslate eV = pV := by
  funext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · exact translate_one
  · simp [matrixTranslate, eV, pV, fillBasis]

def sumExpr : {n : Nat} → (Fin n → CExpr) → CExpr
  | 0, _ => 0
  | n+1, f => sumExpr (fun i : Fin n => f i.castSucc) + f (Fin.last n)

theorem translate_sum {n : Nat} (f : Fin n → CExpr) :
    translate (sumExpr f) = ∑ i, translate (f i) := by
  induction n with
  | zero => simp [sumExpr]
  | succ n ih => rw [sumExpr, translate_add, ih, Fin.sum_univ_castSucc]

def eAdjoint {ι κ : Type*} (A : Matrix ι κ CExpr) : Matrix κ ι CExpr := fun i j => star (A j i)
def eScale {ι κ : Type*} (p : CExpr) (A : Matrix ι κ CExpr) : Matrix ι κ CExpr := fun i j => p * A i j
def eMul3 (A B : EMat3) : EMat3 := fun i j => sumExpr (fun k => A i k * B k j)
def eMul6 (A B : EMat6) : EMat6 :=
  fun i j => sumExpr (fun k : Fin 6 => A i (blockIndex.symm k) * B (blockIndex.symm k) j)

@[simp] theorem translate_adjoint {ι κ : Type*} (A : Matrix ι κ CExpr) :
    matrixTranslate (eAdjoint A) = (matrixTranslate A).conjTranspose := by
  funext i j
  exact translate_star _
@[simp] theorem translate_scale {ι κ : Type*} (p : CExpr) (A : Matrix ι κ CExpr) :
    matrixTranslate (eScale p A) = translate p • matrixTranslate A := by
  funext i j
  exact translate_mul _ _
@[simp] theorem translate_mul3 (A B : EMat3) :
    matrixTranslate (eMul3 A B) = matrixTranslate A * matrixTranslate B := by
  funext i j
  simp only [matrixTranslate, eMul3, translate_sum, translate_mul, Matrix.mul_apply]
@[simp] theorem translate_mul6 (A B : EMat6) :
    matrixTranslate (eMul6 A B) = matrixTranslate A * matrixTranslate B := by
  funext i j
  simp only [matrixTranslate, eMul6, translate_sum, translate_mul, Matrix.mul_apply]
  exact Equiv.sum_comp blockIndex.symm (fun k => translate (A i k) * translate (B k j))

@[simp] theorem translate_matrix_add {ι κ : Type*} (A B : Matrix ι κ CExpr) :
    matrixTranslate (A + B) = matrixTranslate A + matrixTranslate B := by
  funext i j
  exact translate_add _ _
@[simp] theorem translate_matrix_sub {ι κ : Type*} (A B : Matrix ι κ CExpr) :
    matrixTranslate (A - B) = matrixTranslate A - matrixTranslate B := by
  funext i j
  exact translate_sub _ _
@[simp] theorem translate_matrix_neg {ι κ : Type*} (A : Matrix ι κ CExpr) :
    matrixTranslate (-A) = -matrixTranslate A := by
  funext i j
  exact translate_neg _

def eDet (A : EMat3) : CExpr :=
  A 0 0 * A 1 1 * A 2 2 - A 0 0 * A 1 2 * A 2 1 - A 0 1 * A 1 0 * A 2 2 +
    A 0 1 * A 1 2 * A 2 0 + A 0 2 * A 1 0 * A 2 1 - A 0 2 * A 1 1 * A 2 0

def eAdjugate (A : EMat3) : EMat3 :=
  !![A 1 1 * A 2 2 - A 1 2 * A 2 1, -(A 0 1 * A 2 2) + A 0 2 * A 2 1, A 0 1 * A 1 2 - A 0 2 * A 1 1;
     -(A 1 0 * A 2 2) + A 1 2 * A 2 0, A 0 0 * A 2 2 - A 0 2 * A 2 0, -(A 0 0 * A 1 2) + A 0 2 * A 1 0;
     A 1 0 * A 2 1 - A 1 1 * A 2 0, -(A 0 0 * A 2 1) + A 0 1 * A 2 0, A 0 0 * A 1 1 - A 0 1 * A 1 0]

@[simp] theorem translate_det (A : EMat3) : translate (eDet A) = (matrixTranslate A).det := by
  simp only [eDet, translate_sub, translate_add, translate_mul, Matrix.det_fin_three, matrixTranslate]
@[simp] theorem translate_adjugate (A : EMat3) :
    matrixTranslate (eAdjugate A) = (matrixTranslate A).adjugate := by
  rw [Matrix.adjugate_fin_three]
  funext i j
  fin_cases i <;> fin_cases j <;>
    simp [matrixTranslate, eAdjugate]

def eQ : Expr := eNorm (eDet eB)
def eD : CExpr := star (eDet eB)
def eN : EMat3 := -(eMul3 (eMul3 eC (eAdjoint eE)) (eAdjoint (eAdjugate eB)))
def eS : EMat6 := Matrix.fromBlocks (eScale eD eE) (eScale eD eB) (eScale eD eC) eN

@[simp] theorem translate_Q : eQ.polynomial = pQ := by simp [eQ, pQ]
@[simp] theorem translate_D : translate eD = pD := by simp [eD, pD]
@[simp] theorem translate_N : matrixTranslate eN = pN := by simp [eN, pN]
@[simp] theorem translate_S : matrixTranslate eS = pS := by
  have hb : matrixTranslate eS = Matrix.fromBlocks
      (matrixTranslate (eScale eD eE)) (matrixTranslate (eScale eD eB))
      (matrixTranslate (eScale eD eC)) (matrixTranslate eN) := by
    funext i j
    cases i <;> cases j <;> rfl
  simpa [pS] using hb

def eIdentity {ι : Type*} [DecidableEq ι] (p : Expr) : Matrix ι ι CExpr :=
  fun i j => if i = j then eReal p else 0

@[simp] theorem translate_identity {ι : Type*} [DecidableEq ι] (p : Expr) :
    matrixTranslate (eIdentity p : Matrix ι ι CExpr) = liftReal p.polynomial • 1 := by
  funext i j
  by_cases h : i = j <;> simp [matrixTranslate, eIdentity, h]

def eTop : EMat3 := eMul3 eE (eAdjoint eE) + eMul3 eB (eAdjoint eB) - eIdentity 6
def eBottom : EMat3 := eScale (eReal eQ) (eMul3 eC (eAdjoint eC)) +
  eMul3 eN (eAdjoint eN) - eIdentity (6 * eQ)
def eGram (A : EMat6) : EMat6 := eMul6 (eAdjoint A) A - eIdentity 6

@[simp] theorem liftReal_nat (n : Nat) : liftReal (n : Poly) = (n : CPoly) :=
  map_natCast (algebraMap Poly CPoly) n

@[simp] theorem liftReal_six : liftReal (6 : Poly) = (6 : CPoly) := by
  simpa only [Nat.cast_ofNat] using liftReal_nat 6

@[simp] theorem liftReal_mul (p q : Poly) : liftReal (p * q) = liftReal p * liftReal q :=
  map_mul (algebraMap Poly CPoly) p q

@[simp] theorem translate_top : matrixTranslate eTop = pTop := by
  simp only [eTop, translate_matrix_sub, translate_matrix_add, translate_mul3,
    translate_adjoint, translate_E, translate_B, translate_identity, polynomial_nat,
    liftReal_six, Nat.cast_ofNat, pTop]
@[simp] theorem translate_bottom : matrixTranslate eBottom = pBottom := by
  simp only [eBottom, translate_matrix_sub, translate_matrix_add, translate_scale,
    translate_real, translate_mul3, translate_adjoint, translate_C, translate_N,
    translate_identity, polynomial_mul, polynomial_nat, translate_Q,
    liftReal_mul, liftReal_six, Nat.cast_ofNat, pBottom]
@[simp] theorem translate_gram (A : EMat6) : matrixTranslate (eGram A) = pGram (matrixTranslate A) := by
  simp only [eGram, translate_matrix_sub, translate_mul6, translate_adjoint,
    translate_identity, polynomial_nat, liftReal_six, Nat.cast_ofNat, pGram]

def eEquation : Equation → Expr
  | .inl (a, i, j) => eNorm (![eE, eB, eC] a i j) - 1
  | .inr (.inl (i, j)) => eNorm (eN i j) - eQ
  | .inr (.inr (.inl (a, i, j))) => eNorm (![eU, eV] a i j) - 1
  | .inr (.inr (.inr (.inl (a, i, j)))) =>
      ![eNorm (eMul6 (eAdjoint eS) eU i j) - 6 * eQ,
        eNorm (eMul6 (eAdjoint eS) eV i j) - 6 * eQ,
        eNorm (eMul6 (eAdjoint eU) eV i j) - 6] a
  | .inr (.inr (.inr (.inr (.inl (a, i, j, b))))) => eComponent (![eTop, eBottom] a i j) b
  | .inr (.inr (.inr (.inr (.inr (a, i, j, b))))) => eComponent (eGram (![eU, eV] a) i j) b

theorem norm_entry {ι κ : Type*} (A : Matrix ι κ CExpr) (i : ι) (j : κ) :
    (eNorm (A i j)).polynomial = normPoly (matrixTranslate A i j) := translate_norm _
theorem component_entry {ι κ : Type*} (A : Matrix ι κ CExpr) (i : ι) (j : κ) (b : Bool) :
    (eComponent (A i j) b).polynomial = component (matrixTranslate A i j) b := translate_component _ _

theorem expression_polynomial (e : Equation) : (eEquation e).polynomial = equationPolynomial e := by
  have hs (a : Fin 3) : matrixTranslate (![eE, eB, eC] a) = ![pE, pB, pC] a := by
    fin_cases a
    · exact translate_E
    · exact translate_B
    · exact translate_C
  have hl (a : Fin 2) : matrixTranslate (![eU, eV] a) = ![pU, pV] a := by
    fin_cases a
    · exact translate_U
    · exact translate_V
  have hb (a : Fin 2) : matrixTranslate (![eTop, eBottom] a) = ![pTop, pBottom] a := by
    fin_cases a
    · exact translate_top
    · exact translate_bottom
  have hmu (A B : EMat6) (q : Expr) (i j : I6) :
      (eNorm (eMul6 (eAdjoint A) B i j) - q).polynomial =
        normPoly (((matrixTranslate A).conjTranspose * matrixTranslate B) i j) - q.polynomial := by
    rw [polynomial_sub, norm_entry, translate_mul6, translate_adjoint]
  rcases e with ⟨a, i, j⟩ | ⟨i, j⟩ | ⟨a, i, j⟩ | ⟨a, i, j⟩ | ⟨a, i, j, b⟩ | ⟨a, i, j, b⟩
  · change (eNorm (![eE, eB, eC] a i j) - 1).polynomial = _
    rw [polynomial_sub, norm_entry, hs, polynomial_nat]
    simp only [Nat.cast_one, equationPolynomial]
  · change (eNorm (eN i j) - eQ).polynomial = _
    rw [polynomial_sub, norm_entry, translate_N, translate_Q]
    rfl
  · change (eNorm (![eU, eV] a i j) - 1).polynomial = _
    rw [polynomial_sub, norm_entry, hl, polynomial_nat]
    simp only [Nat.cast_one, equationPolynomial]
  · fin_cases a
    · change (eNorm (eMul6 (eAdjoint eS) eU i j) - 6 * eQ).polynomial = _
      rw [hmu, translate_S, translate_U, polynomial_mul, polynomial_nat, translate_Q]
      rfl
    · change (eNorm (eMul6 (eAdjoint eS) eV i j) - 6 * eQ).polynomial = _
      rw [hmu, translate_S, translate_V, polynomial_mul, polynomial_nat, translate_Q]
      rfl
    · change (eNorm (eMul6 (eAdjoint eU) eV i j) - 6).polynomial = _
      rw [hmu, translate_U, translate_V, polynomial_nat]
      rfl
  · change (eComponent (![eTop, eBottom] a i j) b).polynomial = _
    rw [component_entry, hb]
    rfl
  · change (eComponent (eGram (![eU, eV] a) i j) b).polynomial = _
    rw [component_entry, translate_gram, hl]
    rfl

def Expr.eval (r : Coord → Rat) : Expr → Rat
  | .constant q => q
  | .input v => r v
  | .add p q => p.eval r + q.eval r
  | .mul p q => p.eval r * q.eval r
  | .neg p => -p.eval r

noncomputable def Expr.evalReal (r : Coord → ℝ) : Expr → ℝ
  | .constant q => q
  | .input v => r v
  | .add p q => p.evalReal r + q.evalReal r
  | .mul p q => p.evalReal r * q.evalReal r
  | .neg p => -p.evalReal r

theorem evalReal_polynomial (r : Coord → ℝ) (e : Expr) : e.evalReal r = realEval r e.polynomial := by
  induction e with
  | constant q => simp [Expr.evalReal, Expr.polynomial, realEval]
  | input v => simp [Expr.evalReal, Expr.polynomial, realEval]
  | add p q hp hq => simp [Expr.evalReal, Expr.polynomial, ← hp, ← hq]
  | mul p q hp hq => simp [Expr.evalReal, Expr.polynomial, ← hp, ← hq]
  | neg p hp => simp [Expr.evalReal, Expr.polynomial, ← hp]

theorem eval_rational (r : Coord → Rat) (e : Expr) :
    (e.eval r : ℝ) = e.evalReal (fun v => (r v : ℝ)) := by
  induction e with
  | constant q => rfl
  | input v => rfl
  | add p q hp hq => simpa only [Expr.eval, Expr.evalReal, Rat.cast_add] using congrArg₂ (·+·) hp hq
  | mul p q hp hq => simpa only [Expr.eval, Expr.evalReal, Rat.cast_mul] using congrArg₂ (·*·) hp hq
  | neg p hp => simpa only [Expr.eval, Expr.evalReal, Rat.cast_neg] using congrArg Neg.neg hp

theorem equation_eval (r : Coord → ℝ) (e : Equation) :
    (eEquation e).evalReal r = realEval r (equationPolynomial e) := by
  rw [evalReal_polynomial, expression_polynomial]

def Expr.degree : Expr → Nat
  | .constant _ => 0
  | .input _ => 1
  | .add p q => max p.degree q.degree
  | .mul p q => p.degree + q.degree
  | .neg p => p.degree

theorem polynomial_degree (e : Expr) : e.polynomial.totalDegree ≤ e.degree := by
  induction e with
  | constant q => simp [Expr.polynomial, Expr.degree]
  | input v => simp [Expr.polynomial, Expr.degree]
  | add p q hp hq =>
    exact (MvPolynomial.totalDegree_add _ _).trans (max_le_max hp hq)
  | mul p q hp hq =>
    exact (MvPolynomial.totalDegree_mul _ _).trans (Nat.add_le_add hp hq)
  | neg p hp => simpa only [Expr.polynomial, Expr.degree, MvPolynomial.totalDegree_neg] using hp

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem expression_degree : ∀ e : Equation, (eEquation e).degree ≤ 8 := by decide

theorem equation_degree (e : Equation) : (equationPolynomial e).totalDegree ≤ 8 := by
  rw [← expression_polynomial]
  exact (polynomial_degree _).trans (expression_degree e)

set_option maxRecDepth 10000 in
theorem determinant_expression_degree : eQ.degree ≤ 4 := by decide

theorem determinant_degree : pQ.totalDegree ≤ 4 := by
  rw [← translate_Q]
  exact (polynomial_degree _).trans determinant_expression_degree

def ExpressionSolution (r : Coord → ℝ) : Prop :=
  (∀ e, (eEquation e).evalReal r = 0) ∧ (54 / 5 : ℝ) ≤ eQ.evalReal r

theorem expressionSolution_iff (r : Coord → ℝ) : ExpressionSolution r ↔ Solution r := by
  simp only [ExpressionSolution, Solution, evalReal_polynomial, expression_polynomial, translate_Q]

theorem exists_quartet_iff_expressions :
    (∃ Q : Fin 4 → MonomialTransport.Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ r : Coord → ℝ, ExpressionSolution r ∧ InBox r := by
  rw [exists_quartet_iff_polynomials]
  simp_rw [expressionSolution_iff]

theorem no_quartet_iff_no_expressions :
    (∀ Q : Fin 4 → MonomialTransport.Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ r : Coord → ℝ, InBox r → ¬ ExpressionSolution r := by
  rw [no_quartet_iff_no_polynomials]
  simp_rw [expressionSolution_iff]

#print axioms translate_det
#print axioms translate_adjugate
#print axioms expression_polynomial
#print axioms evalReal_polynomial
#print axioms eval_rational
#print axioms equation_eval
#print axioms polynomial_degree
#print axioms expression_degree
#print axioms equation_degree
#print axioms determinant_expression_degree
#print axioms determinant_degree
#print axioms expressionSolution_iff
#print axioms exists_quartet_iff_expressions
#print axioms no_quartet_iff_no_expressions
end MUB.BoundedExpressions
