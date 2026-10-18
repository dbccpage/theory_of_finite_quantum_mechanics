import MubBoundedTermCollection

/-!
# Complete numbered coefficient system and actual quartet existence

AuthorityEffect: None.
The theorem concerns the defined coefficient lists, not external file bytes.
-/

noncomputable section
namespace MUB.BoundedCodedSystem
open BoundedCoordinates BoundedPolynomials BoundedExpressions BoundedExportIndices
open BoundedTermCollection MvPolynomial

def pull (x : Fin 152 → ℝ) : Coord → ℝ := fun c => x (variableFin c)
def push (x : Coord → ℝ) : Fin 152 → ℝ := fun i => x (variableEquiv.symm i)
def extend (x : Fin 152 → ℝ) (n : Nat) : ℝ := if h : n < 152 then x ⟨n, h⟩ else 0
def codedRealEval (x : Fin 152 → ℝ) : CodedPoly →+* ℝ := eval₂Hom (algebraMap Rat ℝ) (extend x)

theorem pull_push (x : Coord → ℝ) : pull (push x) = x := by
  funext c
  change x (variableEquiv.symm (variableEquiv c)) = x c
  rw [Equiv.symm_apply_apply]

theorem rename_eval (x : Fin 152 → ℝ) (p : Poly) :
    codedRealEval x (rename variableCode p) = realEval (pull x) p := by
  rw [codedRealEval, coded_eval]
  have h : (fun v => extend x (variableCode v)) = pull x := by
    funext v
    simp [extend, variableCode_lt, pull, variableFin]
  rw [h]

theorem equation_eval (x : Fin 152 → ℝ) (e : Equation) :
    codedRealEval x (listPolynomial (equationCoefficients e)) =
      realEval (pull x) (equationPolynomial e) := by
  rw [equation_coefficients_polynomial, rename_eval]

theorem determinant_eval (x : Fin 152 → ℝ) :
    codedRealEval x (listPolynomial determinantCoefficients) = realEval (pull x) pQ := by
  rw [determinant_coefficients_polynomial, rename_eval]

def CodedSolution (x : Fin 152 → ℝ) : Prop :=
  (∀ e ∈ equations, codedRealEval x (listPolynomial (equationCoefficients e)) = 0) ∧
    (54 / 5 : ℝ) ≤ codedRealEval x (listPolynomial determinantCoefficients)

def CodedBox (x : Fin 152 → ℝ) : Prop := ∀ i, -1 ≤ x i ∧ x i ≤ 1

theorem codedSolution_iff (x : Fin 152 → ℝ) : CodedSolution x ↔ Solution (pull x) := by
  simp only [CodedSolution, Solution, equation_eval, determinant_eval]
  constructor
  · intro h
    exact ⟨fun e => h.1 e (equations_complete e), h.2⟩
  · intro h
    exact ⟨fun e _ => h.1 e, h.2⟩

theorem codedBox_iff (x : Fin 152 → ℝ) : CodedBox x ↔ InBox (pull x) := by
  constructor
  · intro h c
    exact h (variableFin c)
  · intro h i
    obtain ⟨c, hc⟩ := variableFin_bijective.2 i
    rw [← hc]
    exact h c

theorem exists_quartet_iff_coded :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ x, CodedSolution x ∧ CodedBox x := by
  rw [exists_quartet_iff_polynomials]
  constructor
  · rintro ⟨r, hr, hb⟩
    refine ⟨push r, (codedSolution_iff _).mpr ?_, (codedBox_iff _).mpr ?_⟩
    · simpa only [pull_push] using hr
    · simpa only [pull_push] using hb
  · rintro ⟨x, hx, hb⟩
    exact ⟨pull x, (codedSolution_iff _).mp hx, (codedBox_iff _).mp hb⟩

#print axioms pull_push
#print axioms rename_eval
#print axioms equation_eval
#print axioms determinant_eval
#print axioms codedSolution_iff
#print axioms codedBox_iff
#print axioms exists_quartet_iff_coded
end MUB.BoundedCodedSystem
