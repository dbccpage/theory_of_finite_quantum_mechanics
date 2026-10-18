import MubBalancedCoefficients

/-!
# Complete numbered coefficient system and actual quartet existence

AuthorityEffect: None.
The theorem concerns the defined coefficient lists, not external file bytes.
-/

noncomputable section
namespace MUB.BalancedCodedSystem
open BalancedQuadraticLift BalancedQuadraticPolynomials BalancedIndices BalancedCoefficients
open QuadraticLiftPolynomials (Equation)
open QuadraticLiftIndices (equations equations_complete)
open BoundedTermCollection (CodedPoly listPolynomial)
open MvPolynomial

def pull (x : Fin 320 → ℝ) : Coord → ℝ := fun c => x (variableFin c)
def push (x : Coord → ℝ) : Fin 320 → ℝ := fun i => x (variableEquiv.symm i)
def extend (x : Fin 320 → ℝ) (n : Nat) : ℝ := if h : n < 320 then x ⟨n, h⟩ else 0
def codedRealEval (x : Fin 320 → ℝ) : CodedPoly →+* ℝ := eval₂Hom (algebraMap Rat ℝ) (extend x)

theorem pull_push (x : Coord → ℝ) : pull (push x) = x := by
  funext c
  change x (variableEquiv.symm (variableEquiv c)) = x c
  rw [Equiv.symm_apply_apply]

theorem rename_eval (x : Fin 320 → ℝ) (p : Poly) :
    codedRealEval x (rename variableCode p) = realEval (pull x) p := by
  rw [codedRealEval, coded_eval]
  have h : (fun v => extend x (variableCode v)) = pull x := by
    funext v
    simp [extend, variableCode_lt, pull, variableFin]
  rw [h]

theorem equation_eval (x : Fin 320 → ℝ) (e : Equation) :
    codedRealEval x (listPolynomial (equationCoefficients e)) =
      realEval (pull x) (equationPolynomial e) := by
  rw [equation_coefficients_polynomial, rename_eval]

def CodedSolution (x : Fin 320 → ℝ) : Prop :=
  ∀ e ∈ equations, codedRealEval x (listPolynomial (equationCoefficients e)) = 0

def CodedBox (x : Fin 320 → ℝ) : Prop :=
  ∀ i, -(codeRadius i.val : ℝ) ≤ x i ∧ x i ≤ (codeRadius i.val : ℝ)

theorem codedSolution_iff (x : Fin 320 → ℝ) : CodedSolution x ↔ Solution (pull x) := by
  simp only [CodedSolution, Solution, equation_eval]
  constructor
  · intro h
    exact fun e => h e (equations_complete e)
  · intro h
    exact fun e _ => h e

theorem codedBox_iff (x : Fin 320 → ℝ) : CodedBox x ↔ InBox (pull x) := by
  constructor
  · intro h c
    simpa only [pull, variableFin, radius_code] using h (variableFin c)
  · intro h i
    obtain ⟨c, hc⟩ := variableFin_bijective.2 i
    rw [← hc]
    simpa only [InBox, pull, variableFin, radius_code] using h c

theorem exists_quartet_iff_coded :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ x, CodedSolution x ∧ CodedBox x := by
  rw [exists_quartet_iff_balanced_polynomials]
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
#print axioms codedSolution_iff
#print axioms codedBox_iff
#print axioms exists_quartet_iff_coded
end MUB.BalancedCodedSystem
