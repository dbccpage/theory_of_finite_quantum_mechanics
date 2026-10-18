import MubBoundedExportIndices

/-!
# Cancellation of the positive determinant factor in 36 MU equations

AuthorityEffect: None.
The determinant lower bound is retained throughout the solution equivalence.
-/

namespace MUB.BoundedMUFactor
open BoundedCoordinates BoundedBlockChart BoundedPolynomials BoundedExpressions
open scoped BigOperators

noncomputable def pLeft : PMat6 := Matrix.fromBlocks pE 0 pC 0
def eLeft : EMat6 := Matrix.fromBlocks eE 0 eC 0

theorem translate_left : matrixTranslate eLeft = pLeft := by
  have h : matrixTranslate eLeft =
      Matrix.fromBlocks (matrixTranslate eE) 0 (matrixTranslate eC) 0 := by
    funext i j
    cases i with
    | inl i => cases j with
      | inl j => rfl
      | inr j => exact translate_zero
    | inr i => cases j with
      | inl j => rfl
      | inr j => exact translate_zero
  simpa only [translate_E, translate_C, pLeft] using h

theorem normPoly_mul (z w : CPoly) : normPoly (z * w) = normPoly z * normPoly w := by
  simp [normPoly, QuadraticAlgebra.re_mul, QuadraticAlgebra.im_mul]
  ring

theorem normPoly_star (z : CPoly) : normPoly (star z) = normPoly z := by
  simp [normPoly]

theorem scaled_left_transition (A : PMat6) (i : I3) (j : I6) :
    (pS.conjTranspose * A) (.inl i) j =
      star pD * ((pLeft.conjTranspose * A) (.inl i) j) := by
  have h (k : I6) : pS k (.inl i) = pD * pLeft k (.inl i) := by
    cases k <;> rfl
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply]
  calc
    (∑ k, star (pS k (.inl i)) * A k j) =
        ∑ k, star pD * (star (pLeft k (.inl i)) * A k j) := by
      apply Finset.sum_congr rfl
      intro k _
      rw [h, star_mul]
      ring
    _ = _ := (Finset.mul_sum _ _ _).symm

theorem left_factor (A : PMat6) (i : I3) (j : I6) :
    normPoly ((pS.conjTranspose * A) (.inl i) j) - 6 * pQ =
      pQ * (normPoly ((pLeft.conjTranspose * A) (.inl i) j) - 6) := by
  rw [scaled_left_transition, normPoly_mul, normPoly_star]
  have h : normPoly pD = pQ := by rw [pD, normPoly_star]; rfl
  rw [h]
  ring

def eReduced (a : Fin 2) (i : I3) (j : I6) : Expr :=
  eNorm (eMul6 (eAdjoint eLeft) (![eU, eV] a) (.inl i) j) - 6

noncomputable def pReduced (a : Fin 2) (i : I3) (j : I6) : Poly :=
  normPoly ((pLeft.conjTranspose * (![pU, pV] a)) (.inl i) j) - 6

theorem reduced_polynomial (a : Fin 2) (i : I3) (j : I6) :
    (eReduced a i j).polynomial = pReduced a i j := by
  have h (a : Fin 2) : matrixTranslate (![eU, eV] a) = ![pU, pV] a := by
    fin_cases a
    · exact translate_U
    · exact translate_V
  rw [eReduced, polynomial_sub, norm_entry, translate_mul6, translate_adjoint,
    translate_left, h, polynomial_nat]
  rfl

def leftEquation (a : Fin 2) (i : I3) (j : I6) : Equation :=
  .inr (.inr (.inr (.inl (a.castLE (by decide), .inl i, j))))

theorem equation_factor (a : Fin 2) (i : I3) (j : I6) :
    equationPolynomial (leftEquation a i j) = pQ * (eReduced a i j).polynomial := by
  rw [reduced_polynomial]
  fin_cases a
  · exact left_factor pU i j
  · exact left_factor pV i j

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem reduced_expression_degree : ∀ a i j, (eReduced a i j).degree ≤ 4 := by decide

theorem reduced_polynomial_degree (a : Fin 2) (i : I3) (j : I6) :
    (pReduced a i j).totalDegree ≤ 4 := by
  rw [← reduced_polynomial]
  exact (polynomial_degree _).trans (reduced_expression_degree a i j)

def replacement : Equation → Option (Fin 2 × I3 × I6)
  | .inr (.inr (.inr (.inl (a, .inl i, j)))) => ![some (0, i, j), some (1, i, j), none] a
  | _ => none

def eEquationReduced (e : Equation) : Expr :=
  match replacement e with
  | some (a, i, j) => eReduced a i j
  | none => eEquation e

noncomputable def factor (e : Equation) : Poly := if (replacement e).isSome then pQ else 1

theorem factorization (e : Equation) :
    equationPolynomial e = factor e * (eEquationReduced e).polynomial := by
  rcases e with ⟨a,i,j⟩ | ⟨i,j⟩ | ⟨a,i,j⟩ | ⟨a,i,j⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩
  all_goals try simp [factor, replacement, eEquationReduced, expression_polynomial]
  cases i with
  | inl i =>
    fin_cases a
    · exact equation_factor 0 i j
    · exact equation_factor 1 i j
    · simp [expression_polynomial]
  | inr i => simp [expression_polynomial]

theorem zero_iff (r : Coord → ℝ) (e : Equation) (hb : (54 / 5 : ℝ) ≤ realEval r pQ) :
    realEval r (equationPolynomial e) = 0 ↔ realEval r (eEquationReduced e).polynomial = 0 := by
  have hq : realEval r pQ ≠ 0 := by linarith
  have hf : realEval r (factor e) ≠ 0 := by
    cases h : replacement e with
    | none => rw [factor, h]; simp
    | some v => rw [factor, h]; exact hq
  rw [factorization, map_mul, mul_eq_zero, or_iff_right hf]

noncomputable def ReducedSolution (r : Coord → ℝ) : Prop :=
  (∀ e, realEval r (eEquationReduced e).polynomial = 0) ∧ (54 / 5 : ℝ) ≤ realEval r pQ

theorem solution_iff_reduced (r : Coord → ℝ) : Solution r ↔ ReducedSolution r := by
  constructor
  · intro h
    exact ⟨fun e => (zero_iff r e h.2).mp (h.1 e), h.2⟩
  · intro h
    exact ⟨fun e => (zero_iff r e h.2).mpr (h.1 e), h.2⟩

theorem exists_quartet_iff_reduced :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ r, ReducedSolution r ∧ InBox r := by
  rw [exists_quartet_iff_polynomials]
  simp only [solution_iff_reduced]

set_option maxRecDepth 10000 in
theorem replacement_count :
    (BoundedExportIndices.equations.filter (fun e => (replacement e).isSome)).length = 36 := by decide

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem singular_rational_probe :
    eQ.eval (fun _ => 0) = 0 ∧
    (eEquation (leftEquation 0 0 (.inl 0))).eval (fun _ => 0) = 0 ∧
    (eReduced 0 0 (.inl 0)).eval (fun _ => 0) = -5 := by decide +kernel

theorem singular_real_probe :
    realEval (fun _ => 0) (equationPolynomial (leftEquation 0 0 (.inl 0))) = 0 ∧
    realEval (fun _ => 0) (eReduced 0 0 (.inl 0)).polynomial = -5 := by
  have he (e : Expr) : realEval (fun _ => 0) e.polynomial = (e.eval (fun _ => 0) : ℝ) := by
    rw [← evalReal_polynomial]
    simpa using (eval_rational (fun _ => 0) e).symm
  constructor
  · rw [← expression_polynomial, he, singular_rational_probe.2.1]
    norm_num
  · rw [he, singular_rational_probe.2.2]
    norm_num

theorem unconditional_cancellation_false :
    ¬ (∀ r : Coord → ℝ,
      realEval r (equationPolynomial (leftEquation 0 0 (.inl 0))) = 0 ↔
      realEval r (eReduced 0 0 (.inl 0)).polynomial = 0) := by
  intro h
  have hf := (h (fun _ => 0)).mp singular_real_probe.1
  rw [singular_real_probe.2] at hf
  norm_num at hf

theorem reduced_system_degree (e : Equation) : (eEquationReduced e).polynomial.totalDegree ≤ 8 := by
  apply (polynomial_degree _).trans
  cases h : replacement e with
  | none => simpa only [eEquationReduced, h] using expression_degree e
  | some p =>
    rcases p with ⟨a, i, j⟩
    simpa only [eEquationReduced, h] using (reduced_expression_degree a i j).trans (by decide : 4 ≤ 8)

#print axioms translate_left
#print axioms normPoly_mul
#print axioms normPoly_star
#print axioms scaled_left_transition
#print axioms left_factor
#print axioms reduced_polynomial
#print axioms equation_factor
#print axioms reduced_expression_degree
#print axioms reduced_polynomial_degree
#print axioms factorization
#print axioms zero_iff
#print axioms solution_iff_reduced
#print axioms exists_quartet_iff_reduced
#print axioms replacement_count
#print axioms singular_rational_probe
#print axioms singular_real_probe
#print axioms unconditional_cancellation_false
#print axioms reduced_system_degree
end MUB.BoundedMUFactor
