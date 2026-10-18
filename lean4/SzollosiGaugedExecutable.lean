import SzollosiGaugeBalance
import SzollosiTermExpansion

/-!
# Executable quartet system with derived gauge and balance equations

AuthorityEffect: None.

All 618 original expressions are retained, followed by 24 column-gauge equations
and 24 derived transition row/column balance equations. Every constructed-family
quartet has a solution of this 666-equation, 440-coordinate system, also at each
fixed admissible parameter. Every solution gives a quartet. No full cell/cusp
cover, root existence or variety emptiness is asserted.
-/

namespace MUB.SzollosiGaugedExecutable
open SzollosiGaugeBalance SzollosiColumnGauge SzollosiExecutableSystem
open SzollosiQuadraticSystem SzollosiTwoCirculant SzollosiQuartetSystem
open SzollosiTermExpansion ConcreteMubPolynomialSystem
open scoped BigOperators

def eGauge (s : GaugeIndex) : Expr :=
  .input (.inr (.inl (candidateIndex s.1,0,s.2.1,s.2.2))) -
    .constant (if s.2.2 then 0 else 1)

def eBalance (s : BalanceIndex) : Expr :=
  eComponent (sumExpr fun j : Fin 6 =>
    if s.1 then eProduct 2 j s.2.1 else eProduct 2 s.2.1 j) s.2.2 -
    .constant (if s.2.2 then 0 else 6)

theorem eGauge_polynomial (s : GaugeIndex) : (eGauge s).polynomial = gaugePolynomial s := by
  simp [eGauge,gaugePolynomial,Expr.polynomial]

theorem eBalance_polynomial (s : BalanceIndex) : (eBalance s).polynomial = balancePolynomial s := by
  rcases s with ⟨t,i,b⟩
  rw [eBalance,polynomial_sub,translate_component,translate_sum]
  cases t <;> cases b <;>
    simp [balancePolynomial,component,SzollosiExecutableSystem.translate,Expr.polynomial,eProduct,productPolynomial,Fin.sum_univ_succ]

def gaugeIndices : List GaugeIndex := (List.finRange 2).flatMap fun a =>
  (List.finRange 6).flatMap fun j => bools.map fun b => (a,j,b)
def balanceIndices : List BalanceIndex := bools.flatMap fun t =>
  (List.finRange 6).flatMap fun i => bools.map fun b => (t,i,b)

theorem gauge_indices_complete (s : GaugeIndex) : s ∈ gaugeIndices := by
  rcases s with ⟨a,j,b⟩
  cases b <;> simp [gaugeIndices,bools]

theorem balance_indices_complete (s : BalanceIndex) : s ∈ balanceIndices := by
  rcases s with ⟨t,i,b⟩
  cases t <;> cases b <;> simp [balanceIndices,bools]

def extraExpressions : List Expr := gaugeIndices.map eGauge ++ balanceIndices.map eBalance
def augmentedExpressions : List Expr := equations.map eEquation ++ extraExpressions

set_option maxRecDepth 30000 in
theorem augmented_length : augmentedExpressions.length = 666 := by rfl

def AllExpressionsZero (r : Variable → ℝ) : Prop :=
  ∀ e ∈ augmentedExpressions, e.evalReal r = 0

theorem augmented_zeros_iff (r : Variable → ℝ) :
    AllExpressionsZero r ↔ (∀ e, realEval r (equationPolynomial e) = 0) ∧ FirstRowGauge r := by
  constructor
  · intro h
    have hz : ∀ e, realEval r (equationPolynomial e) = 0 := by
      intro e
      have he := h (eEquation e) (List.mem_append_left _
        (List.mem_map.mpr ⟨e,equations_complete e,rfl⟩))
      simpa only [evalReal_polynomial,expression_polynomial] using he
    refine ⟨hz,(gauge_equations_iff r).mp ?_⟩
    intro s
    have he := h (eGauge s) (List.mem_append_right _
      (List.mem_append_left _ (List.mem_map.mpr ⟨s,gauge_indices_complete s,rfl⟩)))
    simpa only [evalReal_polynomial,eGauge_polynomial] using he
  · rintro ⟨hz,hg⟩ e he
    rcases List.mem_append.mp he with he | he
    · rcases List.mem_map.mp he with ⟨d,_,rfl⟩
      simpa only [evalReal_polynomial,expression_polynomial] using hz d
    · rcases List.mem_append.mp he with he | he
      · rcases List.mem_map.mp he with ⟨s,_,rfl⟩
        simpa only [evalReal_polynomial,eGauge_polynomial] using (gauge_equations_iff r).mpr hg s
      · rcases List.mem_map.mp he with ⟨s,_,rfl⟩
        simpa only [evalReal_polynomial,eBalance_polynomial] using solution_balance_equations r hz hg s

/-- Appending the derived equations preserves quartet existence. -/
theorem augmented_exists_iff_quartet :
    (∃ r : Variable → ℝ, AllExpressionsZero r) ↔
      ∃ p : ParameterCoord → ℝ, (∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) ∧
        ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_solution_iff_quartet]
  constructor
  · rintro ⟨r,hr⟩
    exact ⟨r,((augmented_zeros_iff r).mp hr).1⟩
  · rintro ⟨r,hr⟩
    exact ⟨gaugeSolution r,(augmented_zeros_iff _).mpr
      ⟨gaugeSolution_equations r hr,gaugeSolution_firstRow r hr⟩⟩

theorem augmented_exists_with_parameters_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ AllExpressionsZero r) ↔
      ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_gauged_solution_with_parameters_iff p hp]
  constructor
  · rintro ⟨r,hp,hr⟩
    exact ⟨r,hp,(augmented_zeros_iff r).mp hr⟩
  · rintro ⟨r,hp,hr,hg⟩
    exact ⟨r,hp,(augmented_zeros_iff r).mpr ⟨hr,hg⟩⟩

theorem augmented_solution_six_charts (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∃ j, 1 ≤ (product r 2 0 j).re :=
  solution_six_charts r ((augmented_zeros_iff r).mp h).1 ((augmented_zeros_iff r).mp h).2

def normalizedExpr (e : Expr) : List CodedTerm :=
  normalizeTerms ((expand e).map encodeTerm)

theorem normalized_expr_polynomial (e : Expr) :
    codedListPolynomial (normalizedExpr e) = MvPolynomial.rename variableCode e.polynomial := by
  rw [normalizedExpr,normalize_polynomial,encode_list,expansion_polynomial]

def coefficientShapeCheck : Bool := augmentedExpressions.all fun e =>
  (normalizedExpr e).all fun t => decide (t.1≠0) && decide (t.2.length≤2) &&
    t.2.all (fun n => decide (n<440))

set_option maxRecDepth 30000 in
set_option maxHeartbeats 4000000 in
theorem coefficient_shape_checked : coefficientShapeCheck = true := by decide +kernel

def exportJson : Lean.Json := Lean.Json.mkObj [
  ("schema",.str "omega.mub6.szollosi-gauged-expressions.v1"),
  ("variable_count",natJson 440),("equation_count",natJson 666),
  ("box",.arr ((allVariables.map fun v => Lean.Json.mkObj [
    ("index",natJson (variableCode v)),("lo",.str (rationalText (-eRadius v))),
    ("hi",.str (rationalText (eRadius v)))]).toArray)),
  ("equations",.arr ((augmentedExpressions.zipIdx.map fun (e,n) => Lean.Json.mkObj [
    ("index",natJson n),("expression",e.json)]).toArray)),
  ("probes",.arr (([0,1,2].map fun n => Lean.Json.mkObj [
    ("point",.arr ((allVariables.map fun v => .str (rationalText (probePoint n v))).toArray)),
    ("expected",.arr ((augmentedExpressions.map fun e => .str (rationalText (e.eval (probePoint n)))).toArray))]).toArray))]

def coefficientExport : Lean.Json := Lean.toJson (augmentedExpressions.zipIdx.map fun (e,n) =>
  Lean.Json.mkObj [("index",Lean.toJson n),("terms",Lean.toJson ((normalizedExpr e).map codedTermJson))])

#print axioms eGauge_polynomial
#print axioms eBalance_polynomial
#print axioms augmented_zeros_iff
#print axioms augmented_exists_iff_quartet
#print axioms augmented_exists_with_parameters_iff
#print axioms augmented_solution_six_charts
#print axioms normalized_expr_polynomial
#print axioms coefficient_shape_checked
end MUB.SzollosiGaugedExecutable
