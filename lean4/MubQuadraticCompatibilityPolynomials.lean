import MubQuadraticLiftCompatibility
import MubQuadraticLiftNarrowBox

/-!
# Polynomial consequences coupling the quadratic transition variables

AuthorityEffect: None. All 504 added equations follow from the original
648-equation system. They do not replace it or assert independence.
-/

noncomputable section
namespace MUB.QuadraticCompatibilityPolynomials
open QuadraticLift QuadraticLiftCompatibility QuadraticLiftPolynomials
open QuadraticLiftNarrowBox QuadraticLiftCodedSystem BoundedBlockChart
open scoped BigOperators

abbrev CompatibilityEquation :=
  (Fin 3 × I6 × I6 × Bool) ⊕ (Fin 3 × I6 × I6 × Bool) ⊕ (Fin 3 × Bool × I6 × Bool)

theorem compatibility_equation_count : Fintype.card CompatibilityEquation = 504 := by
  norm_num [CompatibilityEquation, I6, Fintype.card_sum, Fintype.card_prod]

def pTransitionGram (a : Fin 3) : PMat6 :=
  (pW a).conjTranspose * pW a - (36 : CPoly) • 1

def pCycles : Fin 3 → PMat6 :=
  ![pW 0 * pW 2 - (6 : CPoly) • pW 1,
    (pW 0).conjTranspose * pW 1 - (6 : CPoly) • pW 2,
    pW 1 * (pW 2).conjTranspose - (6 : CPoly) • pW 0]

def pBalance (a : Fin 3) (column : Bool) (i : I6) : CPoly :=
  (if column then ∑ j, pW a j i else ∑ j, pW a i j) - 6

def compatibilityPolynomial : CompatibilityEquation → Poly
  | .inl (a,i,j,b) => component (pTransitionGram a i j) b
  | .inr (.inl (a,i,j,b)) => component (pCycles a i j) b
  | .inr (.inr (a,column,i,b)) => component (pBalance a column i) b

def CompatibilitySolution (r : Coord → ℝ) : Prop :=
  ∀ e, realEval r (compatibilityPolynomial e) = 0

theorem transitionGram_zero {r : Coord → ℝ} (h : System r) (a : Fin 3) :
    ZeroMatrix r (pTransitionGram a) := by
  rw [zeroMatrix_iff]
  simp only [pTransitionGram, map_sub, map_mul, matrixEval_star, pW_eval,
    matrixEval_smul, map_ofNat, map_one, transition_column_gram h, sub_self]

theorem cycles_zero {r : Coord → ℝ} (h : System r) (a : Fin 3) :
    ZeroMatrix r (pCycles a) := by
  rw [zeroMatrix_iff]
  fin_cases a
  · change (complexEval r).mapMatrix (pW 0 * pW 2 - (6 : CPoly) • pW 1) = 0
    simp only [map_sub, map_mul, matrixEval_smul, map_ofNat, pW_eval, cycle_02 h, sub_self]
  · change (complexEval r).mapMatrix ((pW 0).conjTranspose * pW 1 - (6 : CPoly) • pW 2) = 0
    simp only [map_sub, map_mul, matrixEval_smul, map_ofNat, matrixEval_star, pW_eval,
      cycle_01 h, sub_self]
  · change (complexEval r).mapMatrix (pW 1 * (pW 2).conjTranspose - (6 : CPoly) • pW 0) = 0
    simp only [map_sub, map_mul, matrixEval_smul, map_ofNat, matrixEval_star, pW_eval,
      cycle_12 h, sub_self]

theorem balance_zero {r : Coord → ℝ} (h : System r) (a : Fin 3) (column : Bool) (i : I6) :
    complexEval r (pBalance a column i) = 0 := by
  have hw (j k : I6) : complexEval r (pW a j k) = W r a j k := by
    exact congrFun (congrFun (pW_eval r a) j) k
  cases column
  · simp only [pBalance, Bool.false_eq_true, ↓reduceIte, map_sub, map_sum, map_ofNat, hw,
      transition_row_sum h, sub_self]
  · simp only [pBalance, ↓reduceIte, map_sub, map_sum, map_ofNat, hw,
      transition_column_sum h, sub_self]

theorem system_compatibility {r : Coord → ℝ} (h : System r) : CompatibilitySolution r := by
  rintro (⟨a,i,j,b⟩ | ⟨a,i,j,b⟩ | ⟨a,column,i,b⟩)
  · exact transitionGram_zero h a i j b
  · exact cycles_zero h a i j b
  · exact (component_zero_iff r (pBalance a column i)).mpr (balance_zero h a column i) b

theorem solution_compatibility {r : Coord → ℝ} (h : Solution r) : CompatibilitySolution r :=
  system_compatibility ((solution_iff_system r).mp h)

theorem solution_iff_strengthened (r : Coord → ℝ) :
    Solution r ↔ Solution r ∧ CompatibilitySolution r :=
  ⟨fun h => ⟨h,solution_compatibility h⟩, And.left⟩

theorem exists_quartet_iff_strengthened_table :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔
      ∃ x, QuadraticLiftTable.TableSolution x ∧ NarrowCodedBox x ∧ CompatibilitySolution (pull x) := by
  rw [exists_quartet_iff_narrow_table]
  constructor
  · rintro ⟨x,hx,hb⟩
    refine ⟨x,hx,hb,solution_compatibility ?_⟩
    exact (codedSolution_iff x).mp ((QuadraticLiftTable.tableSolution_iff x).mp hx)
  · rintro ⟨x,hx,hb,_⟩
    exact ⟨x,hx,hb⟩

theorem matrix_product_degree (A B : PMat6)
    (ha : ∀ i j, DegreeLE (A i j) 1) (hb : ∀ i j, DegreeLE (B i j) 1) (i j : I6) :
    DegreeLE ((A * B) i j) 2 := by
  apply degree_sum
  intro k _
  exact degree_mul (ha i k) (hb k j)

theorem scaled_transition_degree (a : Fin 3) (i j : I6) :
    DegreeLE (((6 : CPoly) • pW a) i j) 1 := by
  exact degree_mul six_degree (pW_degree a i j)

theorem transitionGram_degree (a : Fin 3) (i j : I6) :
    DegreeLE (pTransitionGram a i j) 2 := by
  apply degree_sub (transition_degree _ _ (pW_degree a) (pW_degree a) i j)
  change DegreeLE ((36 : CPoly) * (1 : PMat6) i j) 2
  have hc : DegreeLE (36 : CPoly) 0 := by
    change (MvPolynomial.C (36 : ℚ)).totalDegree ≤ 0 ∧ (0 : Poly).totalDegree ≤ 0
    simp
  have hi : DegreeLE ((1 : PMat6) i j) 0 := by
    classical
    by_cases h : i = j
    · simp only [Matrix.one_apply, if_pos h]
      exact degree_one 0
    · simp only [Matrix.one_apply, if_neg h]
      exact degree_zero 0
  exact degree_mono (degree_mul hc hi) (by omega)

theorem cycles_degree (a : Fin 3) (i j : I6) : DegreeLE (pCycles a i j) 2 := by
  have hs (k : Fin 3) := degree_mono (scaled_transition_degree k i j) (by omega : 1 ≤ 2)
  fin_cases a
  · exact degree_sub (matrix_product_degree _ _ (pW_degree 0) (pW_degree 2) i j) (hs 1)
  · exact degree_sub (transition_degree _ _ (pW_degree 0) (pW_degree 1) i j) (hs 2)
  · exact degree_sub (matrix_product_degree _ _ (pW_degree 1)
      (fun k l => degree_star (pW_degree 2 l k)) i j) (hs 0)

theorem balance_degree (a : Fin 3) (column : Bool) (i : I6) : DegreeLE (pBalance a column i) 1 := by
  apply degree_sub _ (degree_mono six_degree (by omega))
  cases column
  · change DegreeLE (∑ j, pW a i j) 1
    apply degree_sum
    intro j _
    exact pW_degree a _ _
  · change DegreeLE (∑ j, pW a j i) 1
    apply degree_sum
    intro j _
    exact pW_degree a _ _

theorem compatibility_degree (e : CompatibilityEquation) : (compatibilityPolynomial e).totalDegree ≤ 2 := by
  rcases e with ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩ | ⟨a,column,i,b⟩
  · exact component_degree (transitionGram_degree a i j) b
  · exact component_degree (cycles_degree a i j) b
  · exact (component_degree (balance_degree a column i) b).trans (by omega)

#print axioms compatibility_equation_count
#print axioms transitionGram_zero
#print axioms cycles_zero
#print axioms balance_zero
#print axioms system_compatibility
#print axioms solution_compatibility
#print axioms solution_iff_strengthened
#print axioms exists_quartet_iff_strengthened_table
#print axioms transitionGram_degree
#print axioms cycles_degree
#print axioms balance_degree
#print axioms compatibility_degree
end MUB.QuadraticCompatibilityPolynomials
