import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Algebra.Order.Star.Real
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import BellClassicalJointExtension

/- Admitted two-qubit tensor/Born construction, exact rational data.
   Origin: FQ-BELL-RATIONAL-VIOLATION-14-5. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptBellRational

abbrev M2 := Matrix (Fin 2) (Fin 2) Rat
abbrev M4 := Matrix (Fin 4) (Fin 4) Rat
def phi : Fin 4 → Rat := ![1, 0, 0, 1]
def rho : M4 := !![1/2, 0, 0, 1/2; 0, 0, 0, 0; 0, 0, 0, 0; 1/2, 0, 0, 1/2]
def z : M2 := !![1, 0; 0, -1]
def x : M2 := !![0, 1; 1, 0]
def b0 : M2 := !![3/5, 4/5; 4/5, -3/5]
def b1 : M2 := !![4/5, -3/5; -3/5, -4/5]

def tensor (a b : M2) : M4 := fun i j =>
  a ⟨i.val / 2, by omega⟩ ⟨j.val / 2, by omega⟩ *
  b ⟨i.val % 2, by omega⟩ ⟨j.val % 2, by omega⟩

def tr (a : M4) : Rat := ∑ i, a i i
def projector (a : M2) (positive : Bool) : M2 :=
  fun i j => ((if i = j then (1 : Rat) else 0) +
    (if positive then (1 : Rat) else -1) * a i j) / 2
def probability (a b : M2) (s t : Bool) : Rat :=
  tr (rho * tensor (projector a s) (projector b t))
def correlation (a b : M2) : Rat := tr (rho * tensor a b)
def chsh : Rat := correlation z b0 + correlation z b1 + correlation x b0 - correlation x b1

-- Positivity is stated on the real interpretation of the rational matrix.
-- No unsupported StarOrderedRing Rat instance is introduced.
theorem density_positive : (rho.map (fun q : Rat => (q : ℝ))).PosSemidef := by
  have h := Matrix.posSemidef_vecMulVec_self_star (fun i : Fin 4 => (phi i : ℝ))
  have hscale := h.smul (by norm_num : (0 : ℝ) ≤ 1/2)
  have heq : rho.map (fun q : Rat => (q : ℝ)) = (1/2 : ℝ) •
      Matrix.vecMulVec (fun i : Fin 4 => (phi i : ℝ))
        (star (fun i : Fin 4 => (phi i : ℝ))) := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [rho, phi, Matrix.vecMulVec]
  rw [heq]
  exact hscale

set_option maxHeartbeats 2000000 in
theorem rational_density_and_involutions :
    tr rho = 1 ∧ z * z = 1 ∧ x * x = 1 ∧ b0 * b0 = 1 ∧ b1 * b1 = 1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · norm_num [tr, rho, Fin.sum_univ_succ]
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [z, x, b0, b1, Matrix.mul_apply, Fin.sum_univ_succ]

set_option maxHeartbeats 2000000 in
theorem exact_born_correlations :
    correlation z b0 = 3/5 ∧ correlation z b1 = 4/5 ∧
    correlation x b0 = 4/5 ∧ correlation x b1 = -3/5 ∧ chsh = 14/5 ∧ 2 < chsh := by
  norm_num [correlation, chsh, tr, rho, tensor, z, x, b0, b1,
    Matrix.mul_apply, Fin.sum_univ_succ]

set_option maxHeartbeats 2000000 in
theorem all_born_cells_strictly_positive :
    ∀ a ∈ ([z, x] : List M2), ∀ b ∈ ([b0, b1] : List M2),
    ∀ s t : Bool, 0 < probability a b s t := by
  intro a ha b hb s t
  simp at ha hb
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> cases s <;> cases t <;>
    norm_num [probability, projector, tr, rho, tensor, z, x, b0, b1,
      Matrix.mul_apply, Fin.sum_univ_succ]

open BellClassicalJointExtension

theorem no_scaled_joint_law (law : List (Nat × Assignment))
    (positive_mass : 0 < mass law) :
    5 * correlationChsh law ≠ 14 * mass law := by
  have bounds := joint_scaled_bound law
  rw [numerator_eq_four_correlations] at bounds
  intro h
  omega

end QuantumMechanics.PromptBellRational

#print axioms QuantumMechanics.PromptBellRational.density_positive
#print axioms QuantumMechanics.PromptBellRational.rational_density_and_involutions
#print axioms QuantumMechanics.PromptBellRational.exact_born_correlations
#print axioms QuantumMechanics.PromptBellRational.all_born_cells_strictly_positive
#print axioms QuantumMechanics.PromptBellRational.no_scaled_joint_law
