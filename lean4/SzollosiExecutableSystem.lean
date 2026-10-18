import SzollosiQuadraticSystem
import Lean.Data.Json.Basic

/-!
# Executable expression export for all quartet equations

AuthorityEffect: None.

Every executable expression translates to its checked rational polynomial.
Real evaluation agrees for every coordinate assignment; rational evaluation
commutes with the real embedding. Coordinate/equation IDs cover exactly 0..439
and 0..617 with no duplicates. The exported rational box is the checked full
containing box. Three rational probes support cross-language replay.

JSON serialization and native evaluation are not themselves kernel-reflected
interval exclusion. No real solution set is established empty, no system/gauge
reduction or complete 56-cell/three-cusp calculation is supplied here.
-/

namespace MUB.SzollosiExecutableSystem
open SzollosiQuadraticSystem SzollosiTwoCirculant ConcreteMubPolynomialSystem
open Matrix MvPolynomial
open scoped BigOperators

inductive Expr where
  | constant : Rat → Expr
  | input : Variable → Expr
  | add : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  | neg : Expr → Expr
  deriving Inhabited

instance : Add Expr := ⟨Expr.add⟩
instance : Mul Expr := ⟨Expr.mul⟩
instance : Neg Expr := ⟨Expr.neg⟩
instance : Sub Expr := ⟨fun p q => p + (-q)⟩
instance (n : Nat) : OfNat Expr n := ⟨Expr.constant n⟩

noncomputable def Expr.polynomial : Expr → QPoly
  | .constant q => C q
  | .input v => X v
  | .add p q => p.polynomial + q.polynomial
  | .mul p q => p.polynomial * q.polynomial
  | .neg p => -p.polynomial

@[simp] theorem polynomial_add (p q : Expr) : (p+q).polynomial = p.polynomial+q.polynomial := rfl
@[simp] theorem polynomial_mul (p q : Expr) : (p*q).polynomial = p.polynomial*q.polynomial := rfl
@[simp] theorem polynomial_neg (p : Expr) : (-p).polynomial = -p.polynomial := rfl
@[simp] theorem polynomial_sub (p q : Expr) : (p-q).polynomial = p.polynomial-q.polynomial := by
  change p.polynomial + -q.polynomial = p.polynomial-q.polynomial
  exact (sub_eq_add_neg _ _).symm
@[simp] theorem polynomial_nat (n : Nat) : (ofNat(n) : Expr).polynomial = (n : QPoly) := by
  change C (n : Rat) = (n : QPoly)
  simp

abbrev CExpr := Expr × Expr
abbrev EMatrix := Matrix (Fin 6) (Fin 6) CExpr
noncomputable def translate (p : CExpr) : CPoly := (p.1.polynomial,p.2.polynomial)

@[simp] theorem translate_add (p q : CExpr) : translate (p+q) = translate p + translate q := rfl
@[simp] theorem translate_sub (p q : CExpr) : translate (p-q) = translate p - translate q := by
  apply Prod.ext <;> simp [translate]

def eStar (p : CExpr) : CExpr := (p.1,-p.2)
def eNeg (p : CExpr) : CExpr := (-p.1,-p.2)
def eMul (p q : CExpr) : CExpr := (p.1*q.1-p.2*q.2,p.1*q.2+p.2*q.1)
def eNorm (p : CExpr) : Expr := p.1*p.1+p.2*p.2
def eOne : CExpr := (1,0)

@[simp] theorem translate_star (p : CExpr) : translate (eStar p) = cStar (translate p) := rfl
@[simp] theorem translate_neg (p : CExpr) : translate (eNeg p) = cNeg (translate p) := rfl
@[simp] theorem translate_mul (p q : CExpr) : translate (eMul p q) = cMul (translate p) (translate q) := by
  apply Prod.ext <;> simp [translate,eMul,cMul]
@[simp] theorem translate_norm (p : CExpr) : (eNorm p).polynomial = normPolynomial (translate p) := by
  simp [eNorm,Expr.polynomial,normPolynomial,translate,pow_two]
@[simp] theorem translate_one : translate eOne = cOne := by simp [translate,eOne,cOne]

def ePhase (i : Fin 4) : CExpr := (.input (.inl (i,false)),.input (.inl (i,true)))
def eBasis (a : Fin 3) (i j : Fin 6) : CExpr :=
  (.input (.inr (.inl (a,i,j,false))),.input (.inr (.inl (a,i,j,true))))
def eProduct (a : Fin 3) (i j : Fin 6) : CExpr :=
  (.input (.inr (.inr (a,i,j,false))),.input (.inr (.inr (a,i,j,true))))
@[simp] theorem translate_phase (i : Fin 4) : translate (ePhase i) = phasePolynomial i := rfl
@[simp] theorem translate_basis (a : Fin 3) (i j : Fin 6) : translate (eBasis a i j) = basisPolynomial a i j := rfl
@[simp] theorem translate_product (a : Fin 3) (i j : Fin 6) : translate (eProduct a i j) = productPolynomial a i j := rfl

def eCirculant (a : Fin 3 → CExpr) : Matrix (Fin 3) (Fin 3) CExpr :=
  Matrix.circulant (fun i => a (-i))
def eAdjoint {ι κ : Type*} (A : Matrix ι κ CExpr) : Matrix κ ι CExpr := fun i j => eStar (A j i)
def eRaw (a b : Fin 3 → CExpr) : EMatrix :=
  (Matrix.fromBlocks (eCirculant a) (eCirculant b)
    (eAdjoint (eCirculant b)) (fun i j => eNeg (eAdjoint (eCirculant a) i j))).submatrix
      blockEquiv.symm blockEquiv.symm

theorem translate_raw (a b : Fin 3 → CExpr) :
    (fun i j => translate (eRaw a b i j)) = pRaw (fun i => translate (a i)) (fun i => translate (b i)) := by
  funext i j
  unfold eRaw pRaw
  simp only [Matrix.submatrix_apply]
  cases hi : blockEquiv.symm i with
  | inl k =>
    cases hj : blockEquiv.symm j with
    | inl l => rfl
    | inr l => rfl
  | inr k =>
    cases hj : blockEquiv.symm j with
    | inl l => exact translate_star _
    | inr l => exact (translate_neg _).trans (congrArg cNeg (translate_star _))

def eRow (x y : CExpr) : Fin 3 → CExpr := ![eOne,x,eMul x y]
theorem translate_row (x y : CExpr) :
    (fun i => translate (eRow x y i)) = phaseRowPolynomial (translate x) (translate y) := by
  funext i
  fin_cases i
  · exact translate_one
  · rfl
  · exact translate_mul x y

def eFamily : EMatrix := eRaw (eRow (ePhase 0) (ePhase 1)) (eRow (ePhase 2) (ePhase 3))
theorem translate_family : (fun i j => translate (eFamily i j)) = rawFamilyPolynomial := by
  rw [eFamily,translate_raw,translate_row,translate_row]
  rfl

def sumExpr : {n : Nat} → (Fin n → CExpr) → CExpr
  | 0, _ => (0,0)
  | n+1, f => sumExpr (fun i : Fin n => f i.castSucc) + f (Fin.last n)

theorem translate_sum {n : Nat} (f : Fin n → CExpr) :
    translate (sumExpr f) = ∑ i, translate (f i) := by
  induction n with
  | zero => simp [sumExpr,translate]
  | succ n ih => rw [sumExpr,translate_add,ih,Fin.sum_univ_castSucc]

def eGram (A B : EMatrix) (i j : Fin 6) : CExpr := sumExpr (fun k => eMul (eStar (A k i)) (B k j))
theorem translate_gram (A B : EMatrix) (i j : Fin 6) :
    translate (eGram A B i j) = gramPolynomial (fun k l => translate (A k l)) (fun k l => translate (B k l)) i j := by
  simp only [eGram,translate_sum,translate_mul,translate_star,gramPolynomial]

def ePhaseSum (x y : CExpr) : CExpr := x+y+eStar (eMul x y)
def eCompatibility : CExpr := ePhaseSum (ePhase 0) (ePhase 1) + ePhaseSum (ePhase 2) (ePhase 3)
theorem translate_compatibility : translate eCompatibility = compatibilityPolynomial := by
  simp only [eCompatibility,ePhaseSum,translate_add,translate_star,translate_mul,translate_phase,
    compatibilityPolynomial,phaseSumPolynomial]

def eComponent (p : CExpr) (b : Bool) : Expr := if b then p.2 else p.1
theorem translate_component (p : CExpr) (b : Bool) :
    (eComponent p b).polynomial = component (translate p) b := by cases b <;> rfl

def eParameter : ParameterEquation → Expr
  | .inl i => eNorm (ePhase i)-1
  | .inr b => eComponent eCompatibility b

def eTarget (i j : Fin 6) : CExpr := (.constant (if i=j then 6 else 0),0)
theorem translate_target (i j : Fin 6) : translate (eTarget i j) = unitaryTarget i j := by
  simp [translate,eTarget,unitaryTarget,Expr.polynomial]

def eEquation : Equation → Expr
  | .inl e => eParameter e
  | .inr (.inl (i,j,b)) => eComponent (eBasis 0 i j - eFamily i j) b
  | .inr (.inr (.inl (a,i,j,b))) => eComponent
      (eGram (eBasis (candidateIndex a)) (eBasis (candidateIndex a)) i j - eTarget i j) b
  | .inr (.inr (.inr (.inl (a,i,j)))) => eNorm (eBasis (candidateIndex a) i j)-1
  | .inr (.inr (.inr (.inr (.inl (a,i,j,b))))) => eComponent
      (eProduct a i j-eGram (eBasis (pairLeft a)) (eBasis (pairRight a)) i j) b
  | .inr (.inr (.inr (.inr (.inr (a,i,j))))) => eNorm (eProduct a i j)-6

/-- Every executable expression is the checked rational polynomial. -/
theorem expression_polynomial (e : Equation) : (eEquation e).polynomial = equationPolynomial e := by
  rcases e with e | e
  · rcases e with i | b
    · simp only [eEquation,eParameter,polynomial_sub,polynomial_nat,translate_norm,translate_phase,SzollosiQuadraticSystem.equationPolynomial,parameterEquation,Nat.cast_one]
    · rw [eEquation,eParameter,translate_component,translate_compatibility]; rfl
  rcases e with e | e
  · rcases e with ⟨i,j,b⟩
    rw [eEquation,translate_component,translate_sub,translate_basis]
    have hf := congrArg (fun M : PMatrix => M i j) translate_family
    rw [hf]; rfl
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩
    rw [eEquation,translate_component,translate_sub,translate_gram (eBasis (candidateIndex a)) (eBasis (candidateIndex a)) i j,translate_target]
    simp only [translate_basis]
    rfl
  rcases e with e | e
  · rcases e with ⟨a,i,j⟩
    simp only [eEquation,polynomial_sub,polynomial_nat,translate_norm,translate_basis,SzollosiQuadraticSystem.equationPolynomial,entryEquation,Nat.cast_one]
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩
    rw [eEquation,translate_component,translate_sub,translate_product,translate_gram (eBasis (pairLeft a)) (eBasis (pairRight a)) i j]
    simp only [translate_basis]
    rfl
  · rcases e with ⟨a,i,j⟩
    simp only [eEquation,polynomial_sub,polynomial_nat,translate_norm,translate_product,SzollosiQuadraticSystem.equationPolynomial,overlapEquation]; norm_num
    exact (map_natCast (C : Rat →+* QPoly) 6).symm

def Expr.eval (r : Variable → Rat) : Expr → Rat
  | .constant q => q
  | .input v => r v
  | .add p q => p.eval r+q.eval r
  | .mul p q => p.eval r*q.eval r
  | .neg p => -p.eval r

noncomputable def Expr.evalReal (r : Variable → ℝ) : Expr → ℝ
  | .constant q => q
  | .input v => r v
  | .add p q => p.evalReal r+q.evalReal r
  | .mul p q => p.evalReal r*q.evalReal r
  | .neg p => -p.evalReal r

theorem evalReal_polynomial (r : Variable → ℝ) (e : Expr) : e.evalReal r = realEval r e.polynomial := by
  induction e with
  | constant q => simp [Expr.evalReal,Expr.polynomial,realEval]
  | input v => simp [Expr.evalReal,Expr.polynomial,realEval]
  | add p q hp hq => simp only [Expr.evalReal,Expr.polynomial,map_add,←hp,←hq]
  | mul p q hp hq => simp only [Expr.evalReal,Expr.polynomial,map_mul,←hp,←hq]
  | neg p hp => simp only [Expr.evalReal,Expr.polynomial,map_neg,←hp]

theorem eval_polynomial (r : Variable → Rat) (e : Expr) :
    (e.eval r : ℝ) = e.evalReal (fun v => (r v : ℝ)) := by
  induction e with
  | constant q => rfl
  | input v => rfl
  | add p q hp hq => simpa only [Expr.eval,Expr.evalReal,Rat.cast_add] using congrArg₂ (·+·) hp hq
  | mul p q hp hq => simpa only [Expr.eval,Expr.evalReal,Rat.cast_mul] using congrArg₂ (·*·) hp hq
  | neg p hp => simpa only [Expr.eval,Expr.evalReal,Rat.cast_neg] using congrArg Neg.neg hp

theorem equation_eval (r : Variable → Rat) (e : Equation) :
    ((eEquation e).eval r : ℝ) = realEval (fun v => (r v : ℝ)) (equationPolynomial e) := by
  rw [eval_polynomial,evalReal_polynomial,expression_polynomial]

#print axioms expression_polynomial
#print axioms equation_eval


def bit : Bool → Nat | false => 0 | true => 1

def slotCode {n : Nat} (p : Fin n × Fin 6 × Fin 6 × Bool) : Nat :=
  ((p.1.val*6+p.2.1.val)*6+p.2.2.1.val)*2+bit p.2.2.2

def entryCode {n : Nat} (p : Fin n × Fin 6 × Fin 6) : Nat :=
  (p.1.val*6+p.2.1.val)*6+p.2.2.val

def variableCode : Variable → Nat
  | .inl (i,b) => i.val*2+bit b
  | .inr (.inl p) => 8+slotCode p
  | .inr (.inr p) => 224+slotCode p

def equationCode : Equation → Nat
  | .inl (.inl i) => i.val
  | .inl (.inr b) => 4+bit b
  | .inr (.inl (i,j,b)) => 6+(i.val*6+j.val)*2+bit b
  | .inr (.inr (.inl p)) => 78+slotCode p
  | .inr (.inr (.inr (.inl p))) => 222+entryCode p
  | .inr (.inr (.inr (.inr (.inl p)))) => 294+slotCode p
  | .inr (.inr (.inr (.inr (.inr p)))) => 510+entryCode p

def bools : List Bool := [false,true]
def phaseCoords : List ParameterCoord := (List.finRange 4).flatMap fun i => bools.map fun b => (i,b)
def coords : List Coord := (List.finRange 6).flatMap fun i => (List.finRange 6).flatMap fun j => bools.map fun b => (i,j,b)
def slots (n : Nat) : List (Fin n × Fin 6 × Fin 6 × Bool) :=
  (List.finRange n).flatMap fun a => coords.map fun (i,j,b) => (a,i,j,b)
def entries (n : Nat) : List (Fin n × Fin 6 × Fin 6) :=
  (List.finRange n).flatMap fun a => (List.finRange 6).flatMap fun i =>
    (List.finRange 6).map fun j => (a,i,j)

def allVariables : List Variable := phaseCoords.map Sum.inl ++
  (slots 3).map (fun p => .inr (.inl p)) ++ (slots 3).map (fun p => .inr (.inr p))

def equations : List Equation :=
  (List.finRange 4).map (fun i => .inl (.inl i)) ++
  bools.map (fun b => .inl (.inr b)) ++
  coords.map (fun p => .inr (.inl p)) ++
  (slots 2).map (fun p => .inr (.inr (.inl p))) ++
  (entries 2).map (fun p => .inr (.inr (.inr (.inl p)))) ++
  (slots 3).map (fun p => .inr (.inr (.inr (.inr (.inl p))))) ++
  (entries 3).map (fun p => .inr (.inr (.inr (.inr (.inr p)))))

set_option maxRecDepth 10000 in
theorem variable_codes : allVariables.map variableCode = List.range 440 := by decide
set_option maxRecDepth 10000 in
theorem equation_codes : equations.map equationCode = List.range 618 := by decide

theorem variables_complete (v : Variable) : v ∈ allVariables := by
  rcases v with ⟨i,b⟩ | v
  · cases b <;> simp [allVariables,phaseCoords,bools]
  rcases v with ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩
  all_goals cases b <;> simp [allVariables,slots,coords,bools]

theorem equations_complete (e : Equation) : e ∈ equations := by
  rcases e with e | e
  · rcases e with i | b
    · simp [equations]
    · cases b <;> simp [equations,bools]
  rcases e with e | e
  · rcases e with ⟨i,j,b⟩; cases b <;> simp [equations,coords,bools]
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩; fin_cases a <;> cases b <;> simp [equations,slots,coords,bools]
  rcases e with e | e
  · rcases e with ⟨a,i,j⟩; simp [equations,entries]
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩; fin_cases a <;> cases b <;> simp [equations,slots,coords,bools]
  · rcases e with ⟨a,i,j⟩; simp [equations,entries]

theorem variableCode_injective : Function.Injective variableCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [variable_codes]; exact List.nodup_range)
    (variables_complete u) (variables_complete v) h

theorem equationCode_injective : Function.Injective equationCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [equation_codes]; exact List.nodup_range)
    (equations_complete u) (equations_complete v) h

def eRadius : Variable → Rat
  | .inl _ => 1
  | .inr (.inl _) => 1
  | .inr (.inr _) => 3

theorem eRadius_eq (v : Variable) : eRadius v = radius v := by
  rcases v with p | (p | p) <;> rfl

def rationalText (q : Rat) : String :=
  if q.den == 1 then toString q.num else s!"{q.num}/{q.den}"

def natJson (n : Nat) : Lean.Json := Lean.Json.num n

def Expr.json : Expr → Lean.Json
  | .constant q => Lean.Json.mkObj [("op",.str "constant"),("value",.str (rationalText q))]
  | .input v => Lean.Json.mkObj [("op",.str "variable"),("index",natJson (variableCode v))]
  | .add p q => Lean.Json.mkObj [("op",.str "add"),("left",p.json),("right",q.json)]
  | .mul p q => Lean.Json.mkObj [("op",.str "mul"),("left",p.json),("right",q.json)]
  | .neg p => Lean.Json.mkObj [("op",.str "neg"),("argument",p.json)]

def probePoint (n : Nat) (v : Variable) : Rat :=
  match n with
  | 0 => 0
  | 1 => ((variableCode v % 11 : Nat) : Rat)/7-5/7
  | _ => if variableCode v % 2 == 0 then 1 else -1

def probeJson (n : Nat) : Lean.Json := Lean.Json.mkObj [
  ("point",.arr ((allVariables.map fun v => .str (rationalText (probePoint n v))).toArray)),
  ("expected",.arr ((equations.map fun e => .str (rationalText ((eEquation e).eval (probePoint n)))).toArray))]

def exportJson : Lean.Json := Lean.Json.mkObj [
  ("schema",.str "omega.mub6.szollosi-expressions.v1"),
  ("variable_count",natJson 440),("equation_count",natJson 618),
  ("box",.arr ((allVariables.map fun v => Lean.Json.mkObj [
    ("index",natJson (variableCode v)),("lo",.str (rationalText (-eRadius v))),
    ("hi",.str (rationalText (eRadius v)))]).toArray)),
  ("equations",.arr ((equations.map fun e => Lean.Json.mkObj [
    ("index",natJson (equationCode e)),("expression",(eEquation e).json)]).toArray)),
  ("probes",.arr (([0,1,2].map probeJson).toArray))]

#print axioms variable_codes
#print axioms equation_codes
#print axioms variableCode_injective
#print axioms equationCode_injective



theorem variableCode_lt (v : Variable) : variableCode v < 440 := by
  have h : variableCode v ∈ allVariables.map variableCode :=
    List.mem_map.mpr ⟨v,variables_complete v,rfl⟩
  rw [variable_codes] at h
  exact List.mem_range.mp h

theorem equationCode_lt (e : Equation) : equationCode e < 618 := by
  have h : equationCode e ∈ equations.map equationCode :=
    List.mem_map.mpr ⟨e,equations_complete e,rfl⟩
  rw [equation_codes] at h
  exact List.mem_range.mp h

theorem executable_zeros_iff (r : Variable → ℝ) :
    (∀ e, (eEquation e).evalReal r = 0) ↔
      ∀ e, realEval r (SzollosiQuadraticSystem.equationPolynomial e) = 0 := by
  simp only [evalReal_polynomial,expression_polynomial]

theorem quartet_of_executable_solution (r : Variable → ℝ)
    (h : ∀ e, (eEquation e).evalReal r = 0) :
    SzollosiQuartetSystem.Quartet (SzollosiQuartetSystem.bases
      (SzollosiQuartetSystem.parameterMatrix (parameters r)) (normalize (basis r 1)) (normalize (basis r 2))) :=
  quartet_of_solution r ((executable_zeros_iff r).mp h)

#print axioms executable_zeros_iff
#print axioms quartet_of_executable_solution

end MUB.SzollosiExecutableSystem
