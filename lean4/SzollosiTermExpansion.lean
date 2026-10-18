import SzollosiExecutableSystem

/-!
# Complete rational coefficient expansion of the quartet equations

AuthorityEffect: None.

Expansion, variable coding, factor sorting, coefficient collection and removal
of zero terms preserve the checked polynomial for every expression. For every
quartet equation, the resulting finite table is its polynomial with the
injective coordinate codes as variables. This is a coefficient identity,
without variety emptiness, a complete cover or contractor soundness.
-/

namespace MUB.SzollosiTermExpansion
open SzollosiExecutableSystem SzollosiQuadraticSystem MvPolynomial
abbrev Term := Rat × List Variable
noncomputable def termPolynomial (t : Term) : QPoly := C t.1 * (t.2.map X).prod
noncomputable def listPolynomial (ts : List Term) : QPoly := (ts.map termPolynomial).sum

def termMul (t u : Term) : Term := (t.1*u.1,t.2++u.2)
def termNeg (t : Term) : Term := (-t.1,t.2)
def termsMul (ts us : List Term) : List Term := ts.flatMap fun t => us.map (termMul t)

def expand : Expr → List Term
  | .constant q => [(q,[])]
  | .input v => [(1,[v])]
  | .add p q => expand p ++ expand q
  | .mul p q => termsMul (expand p) (expand q)
  | .neg p => (expand p).map termNeg

theorem term_mul (t u : Term) : termPolynomial (termMul t u) = termPolynomial t * termPolynomial u := by
  simp only [termPolynomial,termMul,List.map_append,List.prod_append,map_mul]
  ring

theorem term_neg (t : Term) : termPolynomial (termNeg t) = -termPolynomial t := by
  simp [termPolynomial,termNeg]

theorem list_append (ts us : List Term) : listPolynomial (ts++us) = listPolynomial ts+listPolynomial us := by
  simp [listPolynomial]

theorem list_map_mul (t : Term) (us : List Term) :
    listPolynomial (us.map (termMul t)) = termPolynomial t * listPolynomial us := by
  induction us with
  | nil => simp [listPolynomial]
  | cons u us ih => simpa [listPolynomial,term_mul,mul_add] using congrArg (termPolynomial (termMul t u)+·) ih

theorem list_mul (ts us : List Term) : listPolynomial (termsMul ts us) = listPolynomial ts * listPolynomial us := by
  induction ts with
  | nil => simp [termsMul,listPolynomial]
  | cons t ts ih =>
    change listPolynomial (us.map (termMul t) ++ termsMul ts us) = _
    rw [list_append,list_map_mul,ih]
    simp [listPolynomial,add_mul]

theorem list_neg (ts : List Term) : listPolynomial (ts.map termNeg) = -listPolynomial ts := by
  induction ts with
  | nil => simp [listPolynomial]
  | cons t ts ih =>
    change termPolynomial (termNeg t) + listPolynomial (ts.map termNeg) = -(termPolynomial t + listPolynomial ts)
    rw [term_neg,ih]
    ring

theorem expansion_polynomial (e : Expr) : listPolynomial (expand e) = e.polynomial := by
  induction e with
  | constant q => simp [expand,listPolynomial,termPolynomial,Expr.polynomial]
  | input v => simp [expand,listPolynomial,termPolynomial,Expr.polynomial]
  | add p q hp hq => simpa [expand,Expr.polynomial,list_append] using congrArg₂ (·+·) hp hq
  | mul p q hp hq => simpa [expand,Expr.polynomial,list_mul] using congrArg₂ (·*·) hp hq
  | neg p hp => simpa [expand,Expr.polynomial,list_neg] using congrArg Neg.neg hp

theorem equation_expansion (e : Equation) :
    listPolynomial (expand (eEquation e)) = equationPolynomial e := by
  rw [expansion_polynomial,expression_polynomial]


abbrev CodedTerm := Rat × List Nat
abbrev CodedPoly := MvPolynomial Nat Rat
noncomputable def codedTermPolynomial (t : CodedTerm) : CodedPoly := C t.1 * (t.2.map X).prod
noncomputable def codedListPolynomial (ts : List CodedTerm) : CodedPoly := (ts.map codedTermPolynomial).sum

def encodeTerm (t : Term) : CodedTerm := (t.1,t.2.map variableCode)
def sortTerm (t : CodedTerm) : CodedTerm :=
  match t.2 with
  | [i,j] => if i≤j then t else (t.1,[j,i])
  | _ => t

def keyLess : List Nat → List Nat → Bool
  | [], [] => false
  | [], _::_ => true
  | _::_, [] => false
  | a::as, b::bs => if a<b then true else if a=b then keyLess as bs else false

theorem encode_polynomial (t : Term) :
    codedTermPolynomial (encodeTerm t) = rename variableCode (termPolynomial t) := by
  have hp : (t.2.map (X ∘ variableCode : Variable → CodedPoly)).prod =
      rename variableCode (t.2.map (X : Variable → QPoly)).prod := by
    induction t.2 with
    | nil => simp
    | cons v vs ih => simpa only [List.map_cons,List.prod_cons,map_mul,rename_X,Function.comp_apply] using congrArg (X (variableCode v)*·) ih
  simpa only [codedTermPolynomial,encodeTerm,termPolynomial,List.map_map,map_mul,rename_C] using congrArg (C t.1*·) hp

theorem encode_list (ts : List Term) :
    codedListPolynomial (ts.map encodeTerm) = rename variableCode (listPolynomial ts) := by
  induction ts with
  | nil => simp [codedListPolynomial,listPolynomial]
  | cons t ts ih => simpa [codedListPolynomial,listPolynomial,encode_polynomial] using congrArg (codedTermPolynomial (encodeTerm t)+·) ih

theorem sort_polynomial (t : CodedTerm) : codedTermPolynomial (sortTerm t) = codedTermPolynomial t := by
  rcases t with ⟨c,vs⟩
  rcases vs with _ | ⟨i,is⟩
  · rfl
  rcases is with _ | ⟨j,js⟩
  · rfl
  rcases js with _ | ⟨k,ks⟩
  · by_cases h : i≤j
    · simp [sortTerm,h]
    · simp only [sortTerm,h,if_false,codedTermPolynomial,List.map_cons,List.map_nil,List.prod_cons,List.prod_nil]
      ring
  · rfl

def insertTerm (t : CodedTerm) : List CodedTerm → List CodedTerm
  | [] => [t]
  | u::us => if t.2=u.2 then (t.1+u.1,u.2)::us
    else if keyLess t.2 u.2 then t::u::us else u::insertTerm t us

theorem insert_polynomial (t : CodedTerm) (us : List CodedTerm) :
    codedListPolynomial (insertTerm t us) = codedTermPolynomial t + codedListPolynomial us := by
  induction us with
  | nil => simp [insertTerm,codedListPolynomial]
  | cons u us ih =>
    simp only [insertTerm]
    split
    next h =>
      simp only [codedListPolynomial,List.map_cons,List.sum_cons,codedTermPolynomial]
      simp only [h,map_add]
      ring
    next h =>
      split
      next h' => simp [codedListPolynomial]
      next h' =>
        change codedTermPolynomial u + codedListPolynomial (insertTerm t us) =
          codedTermPolynomial t + (codedTermPolynomial u + codedListPolynomial us)
        rw [ih]
        ring

def collect : List CodedTerm → List CodedTerm
  | [] => []
  | t::ts => insertTerm t (collect ts)

theorem collect_polynomial (ts : List CodedTerm) : codedListPolynomial (collect ts) = codedListPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    rw [collect,insert_polynomial,ih]
    rfl

def removeZeros (ts : List CodedTerm) : List CodedTerm := ts.filter (fun t => decide (t.1≠0))

theorem remove_zeros_polynomial (ts : List CodedTerm) :
    codedListPolynomial (removeZeros ts) = codedListPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    by_cases hc : t.1=0
    · simpa [removeZeros,hc,codedListPolynomial,codedTermPolynomial] using ih
    · simpa [removeZeros,hc,codedListPolynomial] using congrArg (codedTermPolynomial t+·) ih

theorem sort_list_polynomial (ts : List CodedTerm) :
    codedListPolynomial (ts.map sortTerm) = codedListPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih => simpa [codedListPolynomial,sort_polynomial] using congrArg (codedTermPolynomial t+·) ih

def normalizeTerms (ts : List CodedTerm) : List CodedTerm := removeZeros (collect (ts.map sortTerm))

theorem normalize_polynomial (ts : List CodedTerm) :
    codedListPolynomial (normalizeTerms ts) = codedListPolynomial ts := by
  rw [normalizeTerms,remove_zeros_polynomial,collect_polynomial,sort_list_polynomial]

def normalizedEquation (e : Equation) : List CodedTerm := normalizeTerms ((expand (eEquation e)).map encodeTerm)

theorem normalized_equation_polynomial (e : Equation) :
    codedListPolynomial (normalizedEquation e) = rename variableCode (equationPolynomial e) := by
  rw [normalizedEquation,normalize_polynomial,encode_list,equation_expansion]

def codedTermJson (t : CodedTerm) : Lean.Json := Lean.Json.mkObj
  [("coefficient",Lean.toJson (rationalText t.1)),("factors",Lean.toJson t.2)]

def coefficientExport : Lean.Json := Lean.toJson (equations.map fun e => Lean.Json.mkObj
  [("index",Lean.toJson (equationCode e)),("terms",Lean.toJson ((normalizedEquation e).map codedTermJson))])

def coefficientShapeCheck : Bool := equations.all fun e => (normalizedEquation e).all fun t =>
  decide (t.1≠0) && decide (t.2.length≤2) && t.2.all (fun n => decide (n<440))

set_option maxRecDepth 30000 in
set_option maxHeartbeats 4000000 in
theorem coefficient_shape_checked : coefficientShapeCheck = true := by decide +kernel

#print axioms coefficient_shape_checked
#print axioms normalized_equation_polynomial
end MUB.SzollosiTermExpansion
