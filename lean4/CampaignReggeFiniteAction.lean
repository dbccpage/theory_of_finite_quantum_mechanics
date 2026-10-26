import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring

/- Finite algebraic Regge sums with a symbolic full turn and declared areas/angles.
No geometric realizability or continuum-convergence theorem is supplied. -/
namespace CampaignReggeFiniteAction
open scoped BigOperators

variable {R ι κ : Type*} [CommRing R]

def action (hinges : Finset ι) (area deficit : ι → R) : R :=
  ∑ h ∈ hinges, area h * deficit h

theorem deficit_expansion (hinges : Finset ι) (around : ι → Finset κ)
    (area : ι → R) (angle : ι → κ → R) (fullTurn : R) :
    action hinges area (fun h => fullTurn - ∑ j ∈ around h, angle h j) =
      fullTurn * (∑ h ∈ hinges, area h) -
        ∑ h ∈ hinges, area h * (∑ j ∈ around h, angle h j) := by
  simp only [action, mul_sub, Finset.sum_sub_distrib, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro h _
  ring

theorem area_linearity (hinges : Finset ι) (area other deficit : ι → R) (a b : R) :
    action hinges (fun h => a * area h + b * other h) deficit =
      a * action hinges area deficit + b * action hinges other deficit := by
  simp only [action, add_mul, mul_assoc, Finset.sum_add_distrib, Finset.mul_sum]

theorem flat_deficits_give_zero (hinges : Finset ι) (area deficit : ι → R)
    (flat : ∀ h ∈ hinges, deficit h = 0) : action hinges area deficit = 0 := by
  apply Finset.sum_eq_zero
  intro h hh
  rw [flat h hh, mul_zero]

theorem same_deficit_area_split (area₁ area₂ deficit : R) :
    area₁ * deficit + area₂ * deficit = (area₁ + area₂) * deficit := by ring

theorem zero_action_does_not_imply_flat :
    action ({0, 1} : Finset Nat) (fun _ => (1 : Int))
      (fun h => if h = 0 then 1 else -1) = 0 ∧ (1 : Int) ≠ 0 := by
  decide

theorem declared_areas_change_action :
    action ({0} : Finset Nat) (fun _ => (1 : Int)) (fun _ => 1) = 1 ∧
    action ({0} : Finset Nat) (fun _ => (2 : Int)) (fun _ => 1) = 2 ∧
    (1 : Int) ≠ 2 := by decide

#print axioms deficit_expansion
#print axioms area_linearity
#print axioms flat_deficits_give_zero
#print axioms same_deficit_area_split
#print axioms zero_action_does_not_imply_flat
#print axioms declared_areas_change_action
end CampaignReggeFiniteAction
