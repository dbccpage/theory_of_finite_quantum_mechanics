


import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H006PermutationUnitary

namespace FableHilbertWalk20260819.H006Envelope

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (Reversible toggle toggleRev)
open FableHilbertWalk20260819.H004 (Vec delta)
open FableHilbertWalk20260819.H006

def idRev : Reversible (fun q : Bool => q) where
  inv := fun q => q
  left := fun _ => rfl
  right := fun _ => rfl

theorem bool_reversible_id_or_toggle {τ : Bool → Bool}
    (R : Reversible τ) :
    (∀ q, τ q = q) ∨ (∀ q, τ q = toggle q) := by
  cases h0 : τ false <;> cases h1 : τ true
  · have hr := R.right true
    have hτ : τ (R.inv true) = false := by
      cases hinv : R.inv true
      · rw [h0]
      · rw [h1]
    rw [hr] at hτ
    cases hτ
  · refine Or.inl fun q => ?_
    cases q <;> assumption
  · refine Or.inr fun q => ?_
    cases q <;> assumption
  · have hr := R.right false
    have hτ : τ (R.inv false) = true := by
      cases hinv : R.inv false
      · rw [h0]
      · rw [h1]
    rw [hr] at hτ
    cases hτ

#print axioms bool_reversible_id_or_toggle

theorem permU_id (v : Vec GaussInt Bool) (q : Bool) :
    permU gaussPack idRev v q = v q :=
  rfl

#print axioms permU_id

theorem permU_toggle (v : Vec GaussInt Bool) (q : Bool) :
    permU gaussPack toggleRev v q = v (toggle q) :=
  rfl

#print axioms permU_toggle

theorem toggle_toggle (q : Bool) : toggle (toggle q) = q := by
  cases q <;> rfl

#print axioms toggle_toggle

theorem permutation_lift_id_or_swap
    {τ : Bool → Bool} (R : Reversible τ) :
    (∀ v q, permU gaussPack R v q = v q) ∨
      (∀ v q, permU gaussPack R v q = v (toggle q)) := by
  rcases bool_reversible_id_or_toggle R with hid | hto
  · refine Or.inl fun v q => ?_
    have hinv : R.inv q = q := (hid (R.inv q)).symm.trans (R.right q)
    unfold permU
    exact congrArg v hinv
  · refine Or.inr fun v q => ?_
    have hinv : R.inv q = toggle q := by
      have hleft := R.left (toggle q)
      have hτ : τ (toggle q) = q := by
        rw [hto (toggle q)]
        exact toggle_toggle q
      rw [hτ] at hleft
      exact hleft
    unfold permU
    exact congrArg v hinv

#print axioms permutation_lift_id_or_swap

theorem id_and_toggle_lifts_unequal :
    permU gaussPack idRev ≠ permU gaussPack toggleRev := by
  intro h
  have hx := congrFun (congrFun h (delta gaussPack false)) false
  rw [permU_id, permU_toggle] at hx
  unfold delta toggle at hx
  exact absurd hx (by decide)

#print axioms id_and_toggle_lifts_unequal

theorem two_permutation_lifts_envelope_strict :
    (permU gaussPack idRev ≠ permU gaussPack toggleRev) ∧
      ((∀ v q, permU gaussPack idRev v q = v q) ∧
        (∀ v q, permU gaussPack toggleRev v q = v (toggle q))) ∧
      (∀ {τ : Bool → Bool} (R : Reversible τ),
        (∀ v q, permU gaussPack R v q = v q) ∨
          (∀ v q, permU gaussPack R v q = v (toggle q))) ∧
      ¬ ∃ (τ : Bool → Bool) (R : Reversible τ),
        ∀ v, swapI v = permU gaussPack R v :=
  ⟨id_and_toggle_lifts_unequal, ⟨permU_id, permU_toggle⟩,
    permutation_lift_id_or_swap, swapI_not_permutation⟩

#print axioms two_permutation_lifts_envelope_strict

end FableHilbertWalk20260819.H006Envelope

private def l5aProvenance : String :=
  "Origin: lean4/H006Envelope.lean Claim: bool_reversible_id_or_toggle AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
