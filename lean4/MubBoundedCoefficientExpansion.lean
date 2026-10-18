import MubBoundedExpressions

/-!
# Finite rational coefficient representation of the bounded equations

AuthorityEffect: None.

Expansion gives a finite list of rational coefficients and coordinate factors.
The list may contain duplicates and zero terms. The theorem identifies its
polynomial exactly; it does not assert infeasibility or native byte parity.
-/

namespace MUB.BoundedCoefficientExpansion
open BoundedCoordinates BoundedPolynomials BoundedExpressions MvPolynomial

abbrev Term := Rat × List Coord
noncomputable def termPolynomial (t : Term) : Poly := C t.1 * (t.2.map X).prod
noncomputable def listPolynomial (ts : List Term) : Poly := (ts.map termPolynomial).sum

def termMul (t u : Term) : Term := (t.1 * u.1, t.2 ++ u.2)
def termNeg (t : Term) : Term := (-t.1, t.2)
def termsMul (ts us : List Term) : List Term := ts.flatMap fun t => us.map (termMul t)

def expand : Expr → List Term
  | .constant q => [(q, [])]
  | .input v => [(1, [v])]
  | .add p q => expand p ++ expand q
  | .mul p q => termsMul (expand p) (expand q)
  | .neg p => (expand p).map termNeg

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

theorem expansion_polynomial (e : Expr) : listPolynomial (expand e) = e.polynomial := by
  induction e with
  | constant q => simp [expand, listPolynomial, termPolynomial, Expr.polynomial]
  | input v => simp [expand, listPolynomial, termPolynomial, Expr.polynomial]
  | add p q hp hq => simpa [expand, Expr.polynomial, list_append] using congrArg₂ (·+·) hp hq
  | mul p q hp hq => simpa [expand, Expr.polynomial, list_mul] using congrArg₂ (·*·) hp hq
  | neg p hp => simpa [expand, Expr.polynomial, list_neg] using congrArg Neg.neg hp

theorem equation_expansion (e : Equation) :
    listPolynomial (expand (eEquation e)) = equationPolynomial e := by
  rw [expansion_polynomial, expression_polynomial]

theorem determinant_expansion : listPolynomial (expand eQ) = pQ := by
  rw [expansion_polynomial, translate_Q]

theorem expansion_factor_bound (e : Expr) : ∀ t ∈ expand e, t.2.length ≤ e.degree := by
  induction e with
  | constant q => simp [expand, Expr.degree]
  | input v => simp [expand, Expr.degree]
  | add p q hp hq =>
    intro t ht
    rcases List.mem_append.mp ht with ht | ht
    · exact (hp t ht).trans (Nat.le_max_left _ _)
    · exact (hq t ht).trans (Nat.le_max_right _ _)
  | mul p q hp hq =>
    intro t ht
    obtain ⟨u, hu, ht⟩ := List.mem_flatMap.mp ht
    obtain ⟨v, hv, rfl⟩ := List.mem_map.mp ht
    exact (List.length_append ..) ▸ (Nat.add_le_add (hp u hu) (hq v hv))
  | neg p hp =>
    intro t ht
    obtain ⟨u, hu, rfl⟩ := List.mem_map.mp ht
    exact hp u hu

theorem equation_factor_bound (e : Equation) (t : Term) (ht : t ∈ expand (eEquation e)) :
    t.2.length ≤ 8 := (expansion_factor_bound _ t ht).trans (expression_degree e)

theorem determinant_factor_bound (t : Term) (ht : t ∈ expand eQ) :
    t.2.length ≤ 4 := (expansion_factor_bound _ t ht).trans determinant_expression_degree

#print axioms expansion_polynomial
#print axioms equation_expansion
#print axioms determinant_expansion
#print axioms expansion_factor_bound
#print axioms equation_factor_bound
#print axioms determinant_factor_bound
end MUB.BoundedCoefficientExpansion
