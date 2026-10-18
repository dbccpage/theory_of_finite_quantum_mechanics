


import HWKernel
import H008PhaseBlindPresentation
import H013BornPairingBoundary

namespace FableHilbertWalk20260819.H013Contract

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H008 (phaseBlind totalWeight weight_nonneg)
open FableHilbertWalk20260819.H013 (pair indicator psi21)

def unitEffect : Bool → Int :=
  fun _ => 1

def bornRule (v : Vec GaussInt Bool) (e : Bool → Int) : Int :=
  pair enumBool (phaseBlind v) e

def swapEffect (e : Bool → Int) : Bool → Int :=
  fun q => e (!q)

def swappedRule (v : Vec GaussInt Bool) (e : Bool → Int) : Int :=
  pair enumBool (phaseBlind v) (swapEffect e)

theorem rsum_nonneg {X : Type} (f : X → Int) :
    ∀ l : List X, (∀ x ∈ l, 0 ≤ f x) → 0 ≤ rsum intPack (l.map f) := by
  intro l h
  induction l with
  | nil =>
      simp only [List.map_nil, rsum, intPack]
      exact Int.le_refl 0
  | cons a t ih =>
      simp only [List.map_cons, rsum, intPack]
      exact Int.add_nonneg (h a List.mem_cons_self)
        (ih (fun x hx => h x (List.mem_cons_of_mem a hx)))

#print axioms rsum_nonneg

theorem born_unit_is_total (v : Vec GaussInt Bool) :
    bornRule v unitEffect = totalWeight enumBool v := by
  unfold bornRule pair totalWeight unitEffect
  apply congrArg
  apply map_congr_mem
  intro q _
  exact Int.mul_one (phaseBlind v q)

#print axioms born_unit_is_total

theorem swapped_unit_is_total (v : Vec GaussInt Bool) :
    swappedRule v unitEffect = totalWeight enumBool v := by
  unfold swappedRule pair totalWeight unitEffect swapEffect
  apply congrArg
  apply map_congr_mem
  intro q _
  exact Int.mul_one (phaseBlind v q)

#print axioms swapped_unit_is_total

theorem born_positive (v : Vec GaussInt Bool) (e : Bool → Int)
    (he : ∀ q, 0 ≤ e q) : 0 ≤ bornRule v e := by
  unfold bornRule pair
  apply rsum_nonneg
  intro q _
  exact Int.mul_nonneg (weight_nonneg v q) (he q)

#print axioms born_positive

theorem swapped_positive (v : Vec GaussInt Bool) (e : Bool → Int)
    (he : ∀ q, 0 ≤ e q) : 0 ≤ swappedRule v e := by
  unfold swappedRule pair swapEffect
  apply rsum_nonneg
  intro q _
  exact Int.mul_nonneg (weight_nonneg v q) (he (!q))

#print axioms swapped_positive

theorem disagree_on_false_indicator :
    bornRule psi21 (indicator false) = 4 ∧
      swappedRule psi21 (indicator false) = 1 := by
  decide

#print axioms disagree_on_false_indicator

theorem two_effect_rules_share_unit_total_and_disagree :
    (∀ v, bornRule v unitEffect = totalWeight enumBool v) ∧
      (∀ v, swappedRule v unitEffect = totalWeight enumBool v) ∧
      (∀ v e, (∀ q, 0 ≤ e q) → 0 ≤ bornRule v e) ∧
      (∀ v e, (∀ q, 0 ≤ e q) → 0 ≤ swappedRule v e) ∧
      bornRule psi21 (indicator false) ≠
        swappedRule psi21 (indicator false) :=
  ⟨born_unit_is_total, swapped_unit_is_total,
    born_positive, swapped_positive, by
      have h := disagree_on_false_indicator
      omega⟩

#print axioms two_effect_rules_share_unit_total_and_disagree

end FableHilbertWalk20260819.H013Contract

private def l5aProvenance : String :=
  "Origin: lean4/H013SameContract.lean Claim: rsum_nonneg AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
