import RectangularQuadraticExclusion
import SzollosiNativeReflection

/-!
# Rectangular exclusion bridge for all quartet equations

AuthorityEffect: None.

The full 618-by-440 system is retained. Coefficient shape and polynomial
semantics are derived from the checked native table. A successful rectangular
image separation excludes actual quartet solutions in the containing box.
No successful full-box check, cell/cusp computation, completeness of a new cover,
root existence or curvature certificate is supplied by this module.
-/

namespace MUB.SzollosiRectangularExclusion
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open SzollosiExecutableSystem SzollosiQuadraticSystem SzollosiNativeReflection
open SzollosiTwoCirculant SzollosiQuartetSystem

/-- Ordered actual native coefficient rows, with an empty out-of-range default. -/
def rows (e : Nat) : List CodedTerm := (nativeTerms[e]?).getD []

theorem normalized_shape (e : Equation) (he : e∈equations) :
    ∀ t∈normalizedEquation e, t.2.length≤2 ∧ ∀ k∈t.2, k<440 := by
  have hall := coefficient_shape_checked
  unfold coefficientShapeCheck at hall
  have hrow := List.all_eq_true.mp hall e he
  intro t ht
  have h := List.all_eq_true.mp hrow t ht
  simp only [Bool.and_eq_true,decide_eq_true_eq,List.all_eq_true] at h
  exact ⟨h.1.2,h.2⟩

theorem rows_shape (e : Nat) :
    ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k<440 := by
  cases hg : equations[e]? with
  | none => simp [rows,native_terms_match,List.getElem?_map,hg]
  | some d =>
    have hd := normalized_shape d (List.mem_of_getElem? hg)
    simpa only [rows,native_terms_match,List.getElem?_map,hg,Option.map_some,Option.getD_some] using hd

theorem rows_zero_of_solution (r : Variable → ℝ)
    (hz : ∀ e, realEval r (equationPolynomial e)=0) (n : Nat) :
    listValue (codedPoint r) (rows n)=0 := by
  unfold rows
  rw [native_terms_match,List.getElem?_map]
  cases hg : equations[n]? with
  | none => simp [listValue]
  | some e =>
    simp only [Option.map_some,Option.getD_some]
    rw [← coded_list_eval,normalized_equation_polynomial,coded_eval_rename,hz e]

/-- The bound encloses the formal derivative of the actual quartet polynomial. -/
theorem derivative_enclosed (r : Variable → ℝ)
    (hr : ∀ v, (fullBox v).Contains (r v)) (e : Equation) (k : Nat) :
    (RectangularQuadraticExclusion.listGradient codedFullBox (nativeCoefficients e) k).Contains
      (codedEval (codedPoint r)
        (MvPolynomial.pderiv k (MvPolynomial.rename variableCode (equationPolynomial e)))) := by
  rw [← native_coefficients_polynomial e,
    RectangularQuadraticExclusion.list_derivative_polynomial (codedPoint r) k (nativeCoefficients e)
      (fun t ht => (rows_shape (equationCode e) t ht).1)]
  exact RectangularQuadraticExclusion.list_derivative_enclosed codedFullBox (codedPoint r)
    (coded_point_in_box r hr) (nativeCoefficients e) k

/-- Each computed leaf check applies directly to actual polynomial solutions. -/
theorem no_solution_in_box_of_check (box : Nat → Bounds) (c : Nat → Rat)
    (C : Nat → Nat → Rat) (hc : ∀ k, (box k).Contains (c k:ℝ))
    (hcheck : RectangularQuadraticExclusion.exclusionCheck 440 618 rows box c C=true) :
    ¬ ∃ r : Variable → ℝ, (∀ k, (box k).Contains (codedPoint r k)) ∧
      ∀ e, realEval r (equationPolynomial e)=0 := by
  rintro ⟨r,hbox,hz⟩
  exact RectangularQuadraticExclusion.exclusion_sound 440 618 rows box c C hc
    (fun e _ => rows_shape e) hcheck ⟨codedPoint r,hbox,fun n _ => rows_zero_of_solution r hz n⟩

def check (c : Nat → Rat) (C : Nat → Nat → Rat) : Bool :=
  RectangularQuadraticExclusion.exclusionCheck 440 618 rows codedFullBox c C

/-- The remaining premise is an actual successful rational exclusion computation. -/
theorem no_quartet_of_check (c : Nat → Rat) (C : Nat → Nat → Rat)
    (hc : ∀ k, (codedFullBox k).Contains (c k:ℝ)) (hcheck : check c C=true) :
    ¬ ∃ p : ParameterCoord → ℝ, (∀ e, MvPolynomial.eval p (parameterPolynomial e)=0) ∧
      ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_solution_iff_quartet]
  rintro ⟨r,hr⟩
  exact RectangularQuadraticExclusion.exclusion_sound 440 618 rows codedFullBox c C hc
    (fun e _ => rows_shape e) hcheck
    ⟨codedPoint r,coded_point_in_box r (solution_in_fullBox r hr),fun n _ => rows_zero_of_solution r hr n⟩

#print axioms no_solution_in_box_of_check
#print axioms rows_shape
#print axioms rows_zero_of_solution
#print axioms derivative_enclosed
#print axioms no_quartet_of_check
end MUB.SzollosiRectangularExclusion
