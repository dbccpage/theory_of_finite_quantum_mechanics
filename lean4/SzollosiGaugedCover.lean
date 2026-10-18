import SzollosiGaugedExecutable

/-!
# Six candidate charts and a balance-separated box

AuthorityEffect: None.

The charts overlap and cover solutions, with no additional hypothesis on the
family parameters. The separated box restricts six candidate coordinates; it
is not a family-parameter exclusion or a complete cell/cusp calculation.
-/
noncomputable section
namespace MUB.SzollosiGaugedCover
open SzollosiGaugedExecutable SzollosiGaugeBalance SzollosiColumnGauge
open SzollosiQuadraticSystem SzollosiTwoCirculant ConcreteMubPolynomialSystem
open SzollosiExecutableSystem
open scoped BigOperators

def rowVariable (j : Fin 6) : Variable := .inr (.inr (2,0,j,false))

theorem row_coordinate (r : Variable → ℝ) (j : Fin 6) :
    (product r 2 0 j).re = r (rowVariable j) := by
  simp [product,productPolynomial,complexEval,realEval,rowVariable]

def chartLower (j : Fin 6) (v : Variable) : ℚ :=
  if v = rowVariable j then 1 else gaugeLower v

def InChart (r : Variable → ℝ) (j : Fin 6) : Prop :=
  ∀ v, (chartLower j v : ℝ) ≤ r v ∧ r v ≤ (gaugeUpper v : ℝ)

theorem augmented_solution_chart_cover (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∃ j, InChart r j := by
  have hs := (augmented_zeros_iff r).mp h
  have hb := gauged_solution_in_box r hs.1 hs.2
  obtain ⟨j,hj⟩ := augmented_solution_six_charts r h
  rw [row_coordinate] at hj
  refine ⟨j,fun v => ⟨?_,(hb v).2⟩⟩
  by_cases hv : v = rowVariable j
  · simpa [chartLower,hv] using hj
  · simpa [chartLower,hv] using (hb v).1

def lowRowLower : Variable → ℚ
  | .inr (.inr (a,i,j,b)) => if a = 2 ∧ i = 0 ∧ b = false then -1/2 else gaugeLower (.inr (.inr (a,i,j,b)))
  | v => gaugeLower v

def lowRowUpper : Variable → ℚ
  | .inr (.inr (a,i,j,b)) => if a = 2 ∧ i = 0 ∧ b = false then 1/2 else gaugeUpper (.inr (.inr (a,i,j,b)))
  | v => gaugeUpper v

def InLowRowBox (r : Variable → ℝ) : Prop :=
  ∀ v, (lowRowLower v : ℝ) ≤ r v ∧ r v ≤ (lowRowUpper v : ℝ)

theorem low_row_coordinate (r : Variable → ℝ) (hb : InLowRowBox r) (j : Fin 6) :
    -(1/2 : ℝ) ≤ r (rowVariable j) ∧ r (rowVariable j) ≤ 1/2 := by
  have hj := hb (rowVariable j)
  norm_num [lowRowLower,lowRowUpper,rowVariable] at hj ⊢
  exact hj

theorem balanced_row_image (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InLowRowBox r) :
    (7/2 : ℝ) ≤ r (rowVariable 0) ∧ r (rowVariable 0) ≤ 17/2 := by
  have hs := (augmented_zeros_iff r).mp h
  have he := congrArg Complex.re ((solution_product_balanced r hs.1 hs.2).1 0)
  simp [Fin.sum_univ_succ,row_coordinate] at he
  have h1 := low_row_coordinate r hb 1
  have h2 := low_row_coordinate r hb 2
  have h3 := low_row_coordinate r hb 3
  have h4 := low_row_coordinate r hb 4
  have h5 := low_row_coordinate r hb 5
  change r (rowVariable 0) + (r (rowVariable 1) + (r (rowVariable 2) +
    (r (rowVariable 3) + (r (rowVariable 4) + r (rowVariable 5))))) = 6 at he
  constructor <;> linarith

theorem low_row_box_empty (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InLowRowBox r) : False := by
  have hi := balanced_row_image r h hb
  have h0 := low_row_coordinate r hb 0
  linarith

def chartCodes : List Nat := (List.finRange 6).map (fun j => variableCode (rowVariable j))
set_option maxRecDepth 10000 in
theorem chart_codes_checked : chartCodes = [368,370,372,374,376,378] := by rfl

#print axioms augmented_solution_chart_cover
#print axioms balanced_row_image
#print axioms low_row_box_empty
end MUB.SzollosiGaugedCover
