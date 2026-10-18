






import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H015

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (Reversible collapse collapse_not_reversible)
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq)

theorem collapse_no_isometry :
    ¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack enumBool (U u) (U v) = sesq intPack enumBool u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false := by
  intro h
  rcases h with ⟨U, hiso, hf, ht⟩
  have h1 := hiso (delta intPack false) (delta intPack true)
  rw [hf, ht] at h1
  have h2 : sesq intPack enumBool (delta intPack false)
      (delta intPack false) = 1 := by decide
  have h3 : sesq intPack enumBool (delta intPack false)
      (delta intPack true) = 0 := by decide
  rw [h2, h3] at h1
  cases h1

#print axioms collapse_no_isometry


def dil1 (x : Bool × Bool) : Bool × Bool := x

def dil2 (x : Bool × Bool) : Bool × Bool := (x.1, !x.2)

theorem dil1_reversible : ∀ x, dil1 (dil1 x) = x := fun _ => rfl

theorem dil2_reversible : ∀ a b : Bool, dil2 (dil2 (a, b)) = (a, b) := by
  decide

theorem same_reduction :
    ∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1 := by
  decide

#print axioms same_reduction

theorem dilations_distinct : ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b)) := by
  decide

#print axioms dilations_distinct

theorem irreversible_fork :
    ¬ Nonempty (Reversible collapse) ∧
      (¬ ∃ U : Vec Int Bool → Vec Int Bool,
        (∀ u v : Vec Int Bool,
          sesq intPack enumBool (U u) (U v) =
            sesq intPack enumBool u v) ∧
        U (delta intPack false) = delta intPack false ∧
        U (delta intPack true) = delta intPack false) ∧
      (∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1) ∧
      ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b)) :=
  ⟨collapse_not_reversible, collapse_no_isometry,
    same_reduction, dilations_distinct⟩

#print axioms irreversible_fork

end FableHilbertWalk20260819.H015

private def l5aProvenance : String :=
  "Origin: lean4/H015IrreversibleFork.lean Claim: collapse_no_isometry AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
