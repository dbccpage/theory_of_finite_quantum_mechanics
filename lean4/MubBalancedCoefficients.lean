import MubBalancedIndices

/-!
# Exact coefficient substitution for the balanced quadratic model

AuthorityEffect: None. The coefficient lists implement the proved affine
replacement; serialized bytes and infeasibility are separate obligations.
-/
namespace MUB.BalancedCoefficients
open BalancedQuadraticLift BalancedQuadraticPolynomials BalancedIndices BoundedBlockChart
open QuadraticLiftCoefficients (CExpr CodedComplex translate constant add mul sumExpr
  normalize normalize_polynomial constant_poly add_poly mul_poly translate_sum
  translate_sub eConst eComponent)
open BoundedTermCollection (Term CodedPoly listPolynomial termPolynomial)
open scoped BigOperators

noncomputable def renameComplex : CPoly →+* CodedComplex where
  toFun p := ⟨MvPolynomial.rename variableCode p.re, MvPolynomial.rename variableCode p.im⟩
  map_zero' := by apply QuadraticAlgebra.ext <;> simp
  map_one' := by apply QuadraticAlgebra.ext <;> simp [QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  map_add' p q := by apply QuadraticAlgebra.ext <;> simp
  map_mul' p q := by
    apply QuadraticAlgebra.ext <;> simp [QuadraticAlgebra.re_mul, QuadraticAlgebra.im_mul]

def varTerms (c : Coord) : List Term := [(1,[variableCode c])]

@[simp] theorem variable_poly (c : Coord) :
    listPolynomial (varTerms c) = MvPolynomial.X (variableCode c) := by
  simp [varTerms, listPolynomial, termPolynomial]

def eCore (a : Fin 3) (i j : Fin 5) : CExpr :=
  ⟨varTerms (.inr (.inr (a,i,j)),false),varTerms (.inr (.inr (a,i,j)),true)⟩

theorem translate_core (a : Fin 3) (i j : Fin 5) :
    translate (eCore a i j) = renameComplex (pCore a i j) := by
  apply QuadraticAlgebra.ext <;> simp [translate,eCore,renameComplex,pCore]

def eComplete (A : Matrix (Fin 5) (Fin 5) CExpr) : Matrix (Fin 6) (Fin 6) CExpr :=
  fun i j => if hi : i.val < 5 then
    if hj : j.val < 5 then A ⟨i.val,hi⟩ ⟨j.val,hj⟩
    else eConst 6 - sumExpr (A ⟨i.val,hi⟩)
  else if hj : j.val < 5 then eConst 6 - sumExpr (fun k => A k ⟨j.val,hj⟩)
  else sumExpr (fun k => sumExpr (A k)) - eConst 24

theorem translate_const (n : Nat) : translate (eConst n) = (n : CodedComplex) := by
  apply QuadraticAlgebra.ext <;> simp [translate,eConst,QuadraticAlgebra.re_natCast,QuadraticAlgebra.im_natCast]

theorem translate_const_24 : translate (eConst 24) = 24 := translate_const 24

theorem translate_complete (a : Fin 3) (i j : Fin 6) :
    translate (eComplete (eCore a) i j) =
      renameComplex (BalancedCompletion.complete (pCore a) i j) := by
  refine Fin.lastCases ?_ (fun k => ?_) i
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [BalancedCompletion.complete_corner]
      simp [eComplete,translate_sub,translate_sum,translate_core,translate_const_24,map_ofNat]
    · rw [BalancedCompletion.complete_last_row]
      simp [eComplete,l.isLt,translate_sub,translate_sum,translate_core,map_ofNat]
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [BalancedCompletion.complete_last_column]
      simp [eComplete,k.isLt,translate_sub,translate_sum,translate_core,map_ofNat]
    · rw [BalancedCompletion.complete_core]
      simp [eComplete,k.isLt,l.isLt,translate_core]

def typedReplacement : QuadraticLift.Coord → List Term
  | (.inl s,b) => varTerms (.inl s,b)
  | (.inr (.inl (i,j)),b) => varTerms (.inr (.inl (i,j)),b)
  | (.inr (.inr (a,i,j)),b) => eComponent (eComplete (eCore a) (blockIndex i) (blockIndex j)) b

theorem typedReplacement_poly (c : QuadraticLift.Coord) :
    listPolynomial (typedReplacement c) = MvPolynomial.rename variableCode (replacement c) := by
  rcases c with ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · simp [typedReplacement,replacement]
  · simp [typedReplacement,replacement]
  · have h := translate_complete a (blockIndex i) (blockIndex j)
    cases b
    · exact congrArg QuadraticAlgebra.re h
    · exact congrArg QuadraticAlgebra.im h

def oldCoordinate (n : Nat) : Option QuadraticLift.Coord :=
  QuadraticLiftIndices.allVariables.find? (fun c => QuadraticLiftIndices.variableCode c == n)

theorem oldCoordinate_code (c : QuadraticLift.Coord) :
    oldCoordinate (QuadraticLiftIndices.variableCode c) = some c := by
  have hn : oldCoordinate (QuadraticLiftIndices.variableCode c) ≠ none := by
    intro h
    have hh := List.find?_eq_none.mp h c (QuadraticLiftIndices.variables_complete c)
    simp at hh
  cases he : oldCoordinate (QuadraticLiftIndices.variableCode c) with
  | none => exact (hn he).elim
  | some d =>
    have hd := List.find?_some he
    have hc : d = c := QuadraticLiftIndices.variableCode_injective (by simpa using hd)
    simp [hc]

def codedReplacement (n : Nat) : List Term := ((oldCoordinate n).map typedReplacement).getD []

theorem codedReplacement_poly (c : QuadraticLift.Coord) :
    listPolynomial (codedReplacement (QuadraticLiftIndices.variableCode c)) =
      MvPolynomial.rename variableCode (replacement c) := by
  simp only [codedReplacement,oldCoordinate_code,Option.map_some,Option.getD_some]
  exact typedReplacement_poly c

def productReplacement (f : Nat → List Term) : List Nat → List Term
  | [] => constant 1
  | n :: ns => mul (f n) (productReplacement f ns)

theorem productReplacement_poly (f : Nat → List Term) (ns : List Nat) :
    listPolynomial (productReplacement f ns) = (ns.map (fun n => listPolynomial (f n))).prod := by
  induction ns with
  | nil => simp [productReplacement]
  | cons n ns ih => simp [productReplacement,ih]

def substituteTerms (f : Nat → List Term) : List Term → List Term
  | [] => []
  | t :: ts => add (mul (constant t.1) (productReplacement f t.2)) (substituteTerms f ts)

theorem substituteTerms_poly (f : Nat → List Term) (ts : List Term) :
    listPolynomial (substituteTerms f ts) = MvPolynomial.bind₁ (fun n => listPolynomial (f n)) (listPolynomial ts) := by
  induction ts with
  | nil => simp [substituteTerms,listPolynomial]
  | cons t ts ih =>
    rw [substituteTerms,add_poly,mul_poly,constant_poly,productReplacement_poly,ih]
    simp [listPolynomial,termPolynomial,map_list_prod,List.map_map,Function.comp_def,MvPolynomial.bind₁_X_right]

def equationCoefficients (e : QuadraticLiftPolynomials.Equation) : List Term :=
  substituteTerms codedReplacement (QuadraticLiftCoefficients.equationCoefficients e)

theorem equation_coefficients_polynomial (e : QuadraticLiftPolynomials.Equation) :
    listPolynomial (equationCoefficients e) = MvPolynomial.rename variableCode (equationPolynomial e) := by
  rw [equationCoefficients,substituteTerms_poly,QuadraticLiftCoefficients.equation_coefficients_polynomial,
    MvPolynomial.bind₁_rename]
  simp only [equationPolynomial,substitute,MvPolynomial.rename_bind₁]
  have h : ((fun n => listPolynomial (codedReplacement n)) ∘ QuadraticLiftIndices.variableCode) =
      (fun c => MvPolynomial.rename variableCode (replacement c)) := funext codedReplacement_poly
  rw [h]

theorem coded_eval (r : Nat → ℝ) (p : Poly) :
    MvPolynomial.eval₂Hom (algebraMap Rat ℝ) r (MvPolynomial.rename variableCode p) =
      realEval (fun v => r (variableCode v)) p := by
  simp [realEval,MvPolynomial.eval₂Hom,MvPolynomial.eval₂_rename,Function.comp_def]

#print axioms translate_complete
#print axioms typedReplacement_poly
#print axioms oldCoordinate_code
#print axioms codedReplacement_poly
#print axioms substituteTerms_poly
#print axioms equation_coefficients_polynomial
#print axioms coded_eval
end MUB.BalancedCoefficients
