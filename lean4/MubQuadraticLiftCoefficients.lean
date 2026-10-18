import MubQuadraticLiftIndices
import MubBoundedTermCollection

/-!
# Collected coefficients for the full quadratic lift

AuthorityEffect: None. Defined finite rational lists are linked to the actual
polynomials. No serialized bytes or infeasibility are assumed.
-/
namespace MUB.QuadraticLiftCoefficients
open QuadraticLift QuadraticLiftPolynomials QuadraticLiftIndices BoundedBlockChart
open BoundedCoordinates (fillE fillB fillC fillBasis)
open BoundedTermCollection (Term CodedPoly listPolynomial
  termsMul termNeg list_append list_mul list_neg termPolynomial
  keyLE removeZeros removeZeros_polynomial collect collect_polynomial)
open scoped BigOperators

abbrev CodedComplex := QuadraticAlgebra CodedPoly (-1) 0

noncomputable def renameComplex : CPoly →+* CodedComplex where
  toFun p := ⟨MvPolynomial.rename variableCode p.re, MvPolynomial.rename variableCode p.im⟩
  map_zero' := by apply QuadraticAlgebra.ext <;> simp
  map_one' := by apply QuadraticAlgebra.ext <;> simp [QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  map_add' p q := by apply QuadraticAlgebra.ext <;> simp
  map_mul' p q := by
    apply QuadraticAlgebra.ext <;> simp [QuadraticAlgebra.re_mul, QuadraticAlgebra.im_mul]

@[simp] theorem renameComplex_star (p : CPoly) : renameComplex (star p) = star (renameComplex p) := by
  apply QuadraticAlgebra.ext <;> simp [renameComplex]
@[simp] theorem renameMatrix_star (A : PMat6) :
    renameComplex.mapMatrix A.conjTranspose = (renameComplex.mapMatrix A).conjTranspose := by
  funext i j
  exact renameComplex_star _
@[simp] theorem renameMatrix_smul (p : CPoly) (A : PMat6) :
    renameComplex.mapMatrix (p • A) = renameComplex p • renameComplex.mapMatrix A := by
  funext i j
  exact map_mul renameComplex _ _

def sortFactors (t : Term) : Term := (t.1,t.2.insertionSort (· ≤ ·))

theorem sortFactors_polynomial (t : Term) : termPolynomial (sortFactors t) = termPolynomial t := by
  have h := ((List.perm_insertionSort (· ≤ ·) t.2).map (MvPolynomial.X : Nat → CodedPoly)).prod_eq
  exact congrArg (MvPolynomial.C t.1 * ·) h

theorem sortFactors_list (ts : List Term) :
    listPolynomial (ts.map sortFactors) = listPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    simpa [listPolynomial, sortFactors_polynomial] using congrArg (termPolynomial t + ·) ih

def normalize (ts : List Term) : List Term :=
  removeZeros (collect (((removeZeros ts).map sortFactors).insertionSort
    (fun t u => keyLE t.2 u.2 = true)))

theorem normalize_polynomial (ts : List Term) : listPolynomial (normalize ts) = listPolynomial ts := by
  rw [normalize, removeZeros_polynomial, collect_polynomial]
  have h := ((List.perm_insertionSort (fun t u : Term => keyLE t.2 u.2 = true)
    ((removeZeros ts).map sortFactors)).map termPolynomial).sum_eq
  rw [show listPolynomial (((removeZeros ts).map sortFactors).insertionSort
    (fun t u => keyLE t.2 u.2 = true)) = listPolynomial ((removeZeros ts).map sortFactors) from h]
  rw [sortFactors_list, removeZeros_polynomial]

def constant (q : Rat) : List Term := normalize [(q,[])]
def add (p q : List Term) : List Term := normalize (p ++ q)
def neg (p : List Term) : List Term := p.map termNeg
def sub (p q : List Term) : List Term := add p (neg q)
def mul (p q : List Term) : List Term := normalize (termsMul p q)

@[simp] theorem constant_poly (q : Rat) : listPolynomial (constant q) = MvPolynomial.C q := by
  rw [constant, normalize_polynomial]
  simp [listPolynomial, termPolynomial]
@[simp] theorem add_poly (p q : List Term) : listPolynomial (add p q) = listPolynomial p + listPolynomial q := by
  rw [add, normalize_polynomial, list_append]
@[simp] theorem neg_poly (p : List Term) : listPolynomial (neg p) = -listPolynomial p := list_neg p
@[simp] theorem sub_poly (p q : List Term) : listPolynomial (sub p q) = listPolynomial p - listPolynomial q := by
  simp [sub, sub_eq_add_neg]
@[simp] theorem mul_poly (p q : List Term) : listPolynomial (mul p q) = listPolynomial p * listPolynomial q := by
  rw [mul, normalize_polynomial, list_mul]

structure CExpr where
  re : List Term
  im : List Term
  deriving Inhabited
instance : Zero CExpr := ⟨⟨constant 0,constant 0⟩⟩
instance : One CExpr := ⟨⟨constant 1,constant 0⟩⟩
instance : Add CExpr := ⟨fun p q => ⟨add p.re q.re,add p.im q.im⟩⟩
instance : Neg CExpr := ⟨fun p => ⟨neg p.re,neg p.im⟩⟩
instance : Sub CExpr := ⟨fun p q => ⟨sub p.re q.re,sub p.im q.im⟩⟩
instance : Mul CExpr := ⟨fun p q => ⟨sub (mul p.re q.re) (mul p.im q.im),add (mul p.re q.im) (mul p.im q.re)⟩⟩
instance : Star CExpr := ⟨fun p => ⟨p.re,neg p.im⟩⟩

noncomputable def translate (p : CExpr) : CodedComplex := ⟨listPolynomial p.re,listPolynomial p.im⟩
@[simp] theorem translate_zero : translate 0 = 0 := by
  apply QuadraticAlgebra.ext <;> simp [translate, show (0 : CExpr).re = constant 0 from rfl,
    show (0 : CExpr).im = constant 0 from rfl]
@[simp] theorem translate_one : translate 1 = 1 := by
  apply QuadraticAlgebra.ext <;> simp [translate, show (1 : CExpr).re = constant 1 from rfl,
    show (1 : CExpr).im = constant 0 from rfl, QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
@[simp] theorem translate_add (p q : CExpr) : translate (p + q) = translate p + translate q := by
  apply QuadraticAlgebra.ext <;> exact add_poly _ _
@[simp] theorem translate_sub (p q : CExpr) : translate (p - q) = translate p - translate q := by
  apply QuadraticAlgebra.ext <;> exact sub_poly _ _
@[simp] theorem translate_mul (p q : CExpr) : translate (p * q) = translate p * translate q := by
  apply QuadraticAlgebra.ext
  · change listPolynomial (sub (mul p.re q.re) (mul p.im q.im)) = _
    simp [translate, QuadraticAlgebra.re_mul, sub_eq_add_neg]
  · change listPolynomial (add (mul p.re q.im) (mul p.im q.re)) = _
    simp [translate, QuadraticAlgebra.im_mul]
@[simp] theorem translate_star (p : CExpr) : translate (star p) = star (translate p) := by
  apply QuadraticAlgebra.ext
  · simp [translate, show (star p).re = p.re from rfl]
  · exact neg_poly _

def eNorm (p : CExpr) : List Term := add (mul p.re p.re) (mul p.im p.im)
def eComponent (p : CExpr) (b : Bool) : List Term := if b then p.im else p.re
def eConst (q : Rat) : CExpr := ⟨constant q,constant 0⟩
@[simp] theorem translate_const_six : translate (eConst 6) = 6 := by
  apply QuadraticAlgebra.ext
  · change listPolynomial (constant 6) = (6 : CodedPoly)
    rw [constant_poly]
    exact map_ofNat MvPolynomial.C 6
  · change listPolynomial (constant 0) = 0
    simp
@[simp] theorem norm_poly (p : CExpr) :
    listPolynomial (eNorm p) = (translate p).re ^ 2 + (translate p).im ^ 2 := by
  simp [eNorm, translate, pow_two]

def eVariable (s : LiftSlot) : CExpr := ⟨[(1,[variableCode (s,false)])],[(1,[variableCode (s,true)])]⟩
@[simp] theorem translate_variable (s : LiftSlot) :
    translate (eVariable s) = renameComplex (coordinatePoly s) := by
  apply QuadraticAlgebra.ext <;> simp [translate, eVariable, renameComplex, coordinatePoly, listPolynomial, termPolynomial]
def eOldVariable (s : BoundedCoordinates.Slot) : CExpr := eVariable (.inl s)
@[simp] theorem translate_oldVariable (s : BoundedCoordinates.Slot) :
    translate (eOldVariable s) = renameComplex (oldVariable s) := translate_variable (.inl s)

abbrev EMat3 := Matrix I3 I3 CExpr
abbrev EMat6 := Matrix I6 I6 CExpr
noncomputable def matrixTranslate {ι κ : Type*} (A : Matrix ι κ CExpr) : Matrix ι κ CodedComplex :=
  fun i j => translate (A i j)

def eE : EMat3 := fillE (fun s => eOldVariable (.inl s))
def eB : EMat3 := fillB (fun s => eOldVariable (.inr (.inl s)))
def eC : EMat3 := fillC (fun s => eOldVariable (.inr (.inr (.inl s))))
def eU : EMat6 := fillBasis (fun s => eOldVariable (.inr (.inr (.inr (.inl s)))))
def eV : EMat6 := fillBasis (fun s => eOldVariable (.inr (.inr (.inr (.inr s)))))

@[simp] theorem translate_E : matrixTranslate eE = renameComplex.mapMatrix pE := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · change translate 1 = renameComplex 1
    rw [translate_one, map_one]
  · refine Fin.cases ?_ (fun l => ?_) j
    · change translate 1 = renameComplex 1
      rw [translate_one, map_one]
    · exact translate_oldVariable _
@[simp] theorem translate_B : matrixTranslate eB = renameComplex.mapMatrix pB := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · change translate 1 = renameComplex 1
    rw [translate_one, map_one]
  · exact translate_oldVariable _
@[simp] theorem translate_C : matrixTranslate eC = renameComplex.mapMatrix pC := by
  funext i j
  refine Fin.cases ?_ (fun k => ?_) j
  · change translate 1 = renameComplex 1
    rw [translate_one, map_one]
  · exact translate_oldVariable _
@[simp] theorem translate_U : matrixTranslate eU = renameComplex.mapMatrix pU := by
  funext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · change translate 1 = renameComplex 1
    rw [translate_one, map_one]
  · simp [matrixTranslate, eU, pU, fillBasis, oldVariable, eOldVariable, translate_variable]
@[simp] theorem translate_V : matrixTranslate eV = renameComplex.mapMatrix pV := by
  funext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k
  · change translate 1 = renameComplex 1
    rw [translate_one, map_one]
  · simp [matrixTranslate, eV, pV, fillBasis, oldVariable, eOldVariable, translate_variable]

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
def eD : EMat3 := fun i j => eVariable (.inr (.inl (i,j)))
def eW : Fin 3 → EMat6 := fun a i j => eVariable (.inr (.inr (a,i,j)))
def eH : EMat6 := Matrix.fromBlocks eE eB eC eD
@[simp] theorem translate_D : matrixTranslate eD = renameComplex.mapMatrix pD := by
  funext i j
  exact translate_variable _
@[simp] theorem translate_W (a : Fin 3) : matrixTranslate (eW a) = renameComplex.mapMatrix (pW a) := by
  funext i j
  exact translate_variable _
@[simp] theorem translate_H : matrixTranslate eH = renameComplex.mapMatrix pH := by
  funext i j
  cases i <;> cases j
  · exact congrFun (congrFun translate_E _) _
  · exact congrFun (congrFun translate_B _) _
  · exact congrFun (congrFun translate_C _) _
  · exact congrFun (congrFun translate_D _) _

def eBases : Fin 3 → EMat6 := ![eH,eU,eV]
def eTransitions : Fin 3 → EMat6 :=
  ![eMul6 (eAdjoint eH) eU,eMul6 (eAdjoint eH) eV,eMul6 (eAdjoint eU) eV]
def eGram (A : EMat6) : EMat6 := eMul6 (eAdjoint A) A - eScale (eConst 6) 1

@[simp] theorem translate_Bases (a : Fin 3) : matrixTranslate (eBases a) = renameComplex.mapMatrix (pBases a) := by
  fin_cases a
  · exact translate_H
  · exact translate_U
  · exact translate_V
@[simp] theorem translate_Transitions (a : Fin 3) : matrixTranslate (eTransitions a) = renameComplex.mapMatrix (pTransitions a) := by
  fin_cases a
  · change matrixTranslate (eMul6 (eAdjoint eH) eU) = renameComplex.mapMatrix (pH.conjTranspose * pU)
    rw [translate_mul6, translate_adjoint, translate_H, translate_U, map_mul, renameMatrix_star]
  · change matrixTranslate (eMul6 (eAdjoint eH) eV) = renameComplex.mapMatrix (pH.conjTranspose * pV)
    rw [translate_mul6, translate_adjoint, translate_H, translate_V, map_mul, renameMatrix_star]
  · change matrixTranslate (eMul6 (eAdjoint eU) eV) = renameComplex.mapMatrix (pU.conjTranspose * pV)
    rw [translate_mul6, translate_adjoint, translate_U, translate_V, map_mul, renameMatrix_star]
@[simp] theorem translate_matrix_one : matrixTranslate (1 : EMat6) = 1 := by
  funext i j
  classical
  by_cases h : i = j
  · simpa only [matrixTranslate, Matrix.one_apply, if_pos h] using translate_one
  · simpa only [matrixTranslate, Matrix.one_apply, if_neg h] using translate_zero
@[simp] theorem translate_Gram (a : Fin 3) :
    matrixTranslate (eGram (eBases a)) = renameComplex.mapMatrix (pGram (pBases a)) := by
  rw [eGram, translate_matrix_sub, translate_mul6, translate_adjoint, translate_Bases,
    translate_scale, translate_const_six, translate_matrix_one]
  simp only [pGram, map_sub, map_mul, renameMatrix_star, renameMatrix_smul, map_ofNat, map_one]
@[simp] theorem translate_Graph (a : Fin 3) :
    matrixTranslate (eW a - eTransitions a) = renameComplex.mapMatrix (pW a - pTransitions a) := by
  rw [translate_matrix_sub, translate_W, translate_Transitions, map_sub]

theorem norm_rename (p : CExpr) (q : CPoly) (h : translate p = renameComplex q) :
    listPolynomial (eNorm p) = MvPolynomial.rename variableCode (normPoly q) := by
  rw [norm_poly,h]
  simp [renameComplex, normPoly]
theorem component_rename (p : CExpr) (q : CPoly) (h : translate p = renameComplex q) (b : Bool) :
    listPolynomial (eComponent p b) = MvPolynomial.rename variableCode (component q b) := by
  cases b
  · exact congrArg QuadraticAlgebra.re h
  · exact congrArg QuadraticAlgebra.im h

def equationCoefficients : Equation → List Term
  | .inl (a,i,j) => sub (eNorm (eBases a i j)) (constant 1)
  | .inr (.inl (a,i,j,b)) => eComponent (eGram (eBases a) i j) b
  | .inr (.inr (.inl (a,i,j,b))) => eComponent ((eW a - eTransitions a) i j) b
  | .inr (.inr (.inr (a,i,j))) => sub (eNorm (eW a i j)) (constant 6)

theorem equation_coefficients_polynomial (e : Equation) :
    listPolynomial (equationCoefficients e) = MvPolynomial.rename variableCode (equationPolynomial e) := by
  rcases e with ⟨a,i,j⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j⟩
  · change listPolynomial (sub (eNorm _) (constant 1)) = _
    rw [sub_poly,constant_poly,norm_rename _ _ (congrFun (congrFun (translate_Bases a) i) j)]
    simp [equationPolynomial, map_ofNat]
  · exact component_rename _ _ (congrFun (congrFun (translate_Gram a) i) j) b
  · exact component_rename _ _ (congrFun (congrFun (translate_Graph a) i) j) b
  · change listPolynomial (sub (eNorm _) (constant 6)) = _
    rw [sub_poly,constant_poly,norm_rename _ _ (congrFun (congrFun (translate_W a) i) j)]
    simp [equationPolynomial, map_ofNat]

theorem coded_eval (r : Nat → ℝ) (p : Poly) :
    MvPolynomial.eval₂Hom (algebraMap Rat ℝ) r (MvPolynomial.rename variableCode p) =
      realEval (fun v => r (variableCode v)) p := by
  simp [realEval, MvPolynomial.eval₂Hom, MvPolynomial.eval₂_rename, Function.comp_def]

#print axioms renameComplex_star
#print axioms normalize_polynomial
#print axioms translate_mul
#print axioms translate_H
#print axioms translate_Bases
#print axioms translate_Transitions
#print axioms translate_Gram
#print axioms translate_Graph
#print axioms equation_coefficients_polynomial
#print axioms coded_eval
end MUB.QuadraticLiftCoefficients
