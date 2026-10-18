import MubBoundedExportIndices
import Mathlib.Data.List.Sort

/-!
# Collected rational coefficient lists for the bounded quartet system

AuthorityEffect: None.

Sorting, adjacent collection and exact-zero deletion preserve the polynomial.
Collection is performed at each expression node, avoiding the complete raw
distributive expansion. No native file or infeasibility is assumed here.
-/

namespace MUB.BoundedTermCollection
open BoundedCoordinates BoundedPolynomials BoundedExpressions BoundedExportIndices MvPolynomial

abbrev Term := Rat × List Nat
abbrev CodedPoly := MvPolynomial Nat Rat
noncomputable def termPolynomial (t : Term) : CodedPoly := C t.1 * (t.2.map X).prod
noncomputable def listPolynomial (ts : List Term) : CodedPoly := (ts.map termPolynomial).sum

def termMul (t u : Term) : Term := (t.1 * u.1, t.2 ++ u.2)
def termNeg (t : Term) : Term := (-t.1, t.2)
def termsMul (ts us : List Term) : List Term := ts.flatMap fun t => us.map (termMul t)

theorem term_mul (t u : Term) : termPolynomial (termMul t u) = termPolynomial t * termPolynomial u := by
  simp only [termPolynomial, termMul, List.map_append, List.prod_append, map_mul]
  ring
theorem term_neg (t : Term) : termPolynomial (termNeg t) = -termPolynomial t := by
  simp [termPolynomial, termNeg]
theorem list_append (ts us : List Term) : listPolynomial (ts ++ us) = listPolynomial ts + listPolynomial us := by
  simp [listPolynomial]
theorem list_map_mul (t : Term) (us : List Term) :
    listPolynomial (us.map (termMul t)) = termPolynomial t * listPolynomial us := by
  induction us with
  | nil => simp [listPolynomial]
  | cons u us ih => simpa [listPolynomial, term_mul, mul_add] using congrArg (termPolynomial (termMul t u) + ·) ih
theorem list_mul (ts us : List Term) : listPolynomial (termsMul ts us) = listPolynomial ts * listPolynomial us := by
  induction ts with
  | nil => simp [termsMul, listPolynomial]
  | cons t ts ih =>
    change listPolynomial (us.map (termMul t) ++ termsMul ts us) = _
    rw [list_append, list_map_mul, ih]
    simp [listPolynomial, add_mul]
theorem list_neg (ts : List Term) : listPolynomial (ts.map termNeg) = -listPolynomial ts := by
  induction ts with
  | nil => simp [listPolynomial]
  | cons t ts ih =>
    change termPolynomial (termNeg t) + listPolynomial (ts.map termNeg) = -(termPolynomial t + listPolynomial ts)
    rw [term_neg, ih]
    ring

def sortFactors (t : Term) : Term := (t.1, t.2.mergeSort (fun i j => decide (i ≤ j)))
def keyLE : List Nat → List Nat → Bool
  | [], _ => true
  | _ :: _, [] => false
  | i :: is, j :: js => if i < j then true else if i = j then keyLE is js else false

theorem sortFactors_polynomial (t : Term) : termPolynomial (sortFactors t) = termPolynomial t := by
  have h := ((List.mergeSort_perm t.2 (fun i j => decide (i ≤ j))).map (X : Nat → CodedPoly)).prod_eq
  exact congrArg (C t.1 * ·) h

theorem sortFactors_list (ts : List Term) :
    listPolynomial (ts.map sortFactors) = listPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih => simpa [listPolynomial, sortFactors_polynomial] using congrArg (termPolynomial t + ·) ih

theorem sortTerms_polynomial (ts : List Term) :
    listPolynomial (ts.mergeSort (fun t u => keyLE t.2 u.2)) = listPolynomial ts :=
  ((List.mergeSort_perm ts (fun t u => keyLE t.2 u.2)).map termPolynomial).sum_eq

def insertHead (t : Term) : List Term → List Term
  | [] => [t]
  | u :: us => if t.2 = u.2 then (t.1 + u.1, u.2) :: us else t :: u :: us

theorem insertHead_polynomial (t : Term) (us : List Term) :
    listPolynomial (insertHead t us) = termPolynomial t + listPolynomial us := by
  cases us with
  | nil => simp [insertHead, listPolynomial]
  | cons u us =>
    by_cases h : t.2 = u.2
    · simp only [insertHead, h, if_true, listPolynomial, List.map_cons, List.sum_cons,
        termPolynomial, map_add]
      ring
    · simp [insertHead, h, listPolynomial]

theorem collectFold_polynomial (ts acc : List Term) :
    listPolynomial (ts.foldl (fun us t => insertHead t us) acc) = listPolynomial ts + listPolynomial acc := by
  induction ts generalizing acc with
  | nil => simp [listPolynomial]
  | cons t ts ih =>
    rw [List.foldl_cons, ih, insertHead_polynomial]
    simp only [listPolynomial, List.map_cons, List.sum_cons]
    ring

def collect (ts : List Term) : List Term := (ts.foldl (fun us t => insertHead t us) []).reverse
theorem collect_polynomial (ts : List Term) : listPolynomial (collect ts) = listPolynomial ts := by
  have hr (us : List Term) : listPolynomial us.reverse = listPolynomial us := by simp [listPolynomial]
  rw [collect, hr, collectFold_polynomial]
  simp [listPolynomial]

def removeZeros (ts : List Term) : List Term := ts.filter (fun t => decide (t.1 ≠ 0))
theorem removeZeros_polynomial (ts : List Term) :
    listPolynomial (removeZeros ts) = listPolynomial ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    by_cases h : t.1 = 0
    · simpa [removeZeros, h, listPolynomial, termPolynomial] using ih
    · simpa [removeZeros, h, listPolynomial] using congrArg (termPolynomial t + ·) ih

def normalize (ts : List Term) : List Term :=
  removeZeros (collect (((removeZeros ts).map sortFactors).mergeSort (fun t u => keyLE t.2 u.2)))

theorem normalize_polynomial (ts : List Term) : listPolynomial (normalize ts) = listPolynomial ts := by
  rw [normalize, removeZeros_polynomial, collect_polynomial, sortTerms_polynomial,
    sortFactors_list, removeZeros_polynomial]

def coefficients : Expr → List Term
  | .constant q => normalize [(q, [])]
  | .input v => [(1, [variableCode v])]
  | .add p q => normalize (coefficients p ++ coefficients q)
  | .mul p q => normalize (termsMul (coefficients p) (coefficients q))
  | .neg p => (coefficients p).map termNeg

theorem coefficients_polynomial (e : Expr) :
    listPolynomial (coefficients e) = rename variableCode e.polynomial := by
  induction e with
  | constant q =>
    rw [coefficients, normalize_polynomial]
    simp [listPolynomial, termPolynomial, Expr.polynomial]
  | input v => simp [coefficients, listPolynomial, termPolynomial, Expr.polynomial]
  | add p q hp hq =>
    simp only [coefficients, normalize_polynomial, list_append, hp, hq, Expr.polynomial, map_add]
  | mul p q hp hq =>
    simp only [coefficients, normalize_polynomial, list_mul, hp, hq, Expr.polynomial, map_mul]
  | neg p hp =>
    simp only [coefficients, list_neg, hp, Expr.polynomial, map_neg]

def equationCoefficients (e : Equation) : List Term := coefficients (eEquation e)
def determinantCoefficients : List Term := coefficients eQ

theorem equation_coefficients_polynomial (e : Equation) :
    listPolynomial (equationCoefficients e) = rename variableCode (equationPolynomial e) := by
  rw [equationCoefficients, coefficients_polynomial, expression_polynomial]

theorem determinant_coefficients_polynomial :
    listPolynomial determinantCoefficients = rename variableCode pQ := by
  rw [determinantCoefficients, coefficients_polynomial, translate_Q]

theorem coded_eval (r : Nat → ℝ) (p : Poly) :
    eval₂Hom (algebraMap Rat ℝ) r (rename variableCode p) =
      realEval (fun v => r (variableCode v)) p := by
  simp [realEval, eval₂Hom, eval₂_rename, Function.comp_def]

theorem equation_coefficients_eval (r : Nat → ℝ) (e : Equation) :
    eval₂Hom (algebraMap Rat ℝ) r (listPolynomial (equationCoefficients e)) =
      realEval (fun v => r (variableCode v)) (equationPolynomial e) := by
  rw [equation_coefficients_polynomial, coded_eval]

#print axioms sortFactors_polynomial
#print axioms sortTerms_polynomial
#print axioms insertHead_polynomial
#print axioms collectFold_polynomial
#print axioms collect_polynomial
#print axioms removeZeros_polynomial
#print axioms normalize_polynomial
#print axioms coefficients_polynomial
#print axioms equation_coefficients_polynomial
#print axioms determinant_coefficients_polynomial
#print axioms coded_eval
#print axioms equation_coefficients_eval
end MUB.BoundedTermCollection
