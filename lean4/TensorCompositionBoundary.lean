







import HWKernel

namespace HilbertWalk.TensorCompositionBoundary

open HilbertWalk.HWKernel

def tensor (u v : Bool → Int) : Bool × Bool → Int :=
  fun p => u p.1 * v p.2

def bell : Bool × Bool → Int :=
  fun p => if p.1 == p.2 then 1 else 0

theorem bell_not_product :
    ¬ ∃ u v : Bool → Int, ∀ p : Bool × Bool, bell p = tensor u v p := by
  intro h
  rcases h with ⟨u, v, huv⟩
  have hff : u false * v false = 1 := (huv (false, false)).symm
  have htt : u true * v true = 1 := (huv (true, true)).symm
  have hft : u false * v true = 0 := (huv (false, true)).symm
  rcases Int.mul_eq_zero.mp hft with hu | hv
  · rw [hu, Int.zero_mul] at hff
    cases hff
  · rw [hv, Int.mul_zero] at htt
    cases htt

#print axioms bell_not_product


def sumSplit (w : Sum Bool Bool → Int) : (Bool → Int) × (Bool → Int) :=
  ⟨fun a => w (Sum.inl a), fun b => w (Sum.inr b)⟩

def sumJoin (p : (Bool → Int) × (Bool → Int)) : Sum Bool Bool → Int :=
  fun x => Sum.casesOn x p.1 p.2

theorem sum_component_embedding_surjective (w : Sum Bool Bool → Int) :
    sumJoin (sumSplit w) = w := by
  funext x
  rcases x with a | b <;> rfl

#print axioms sum_component_embedding_surjective


structure NonForcingPack where
  rival_embeds_components : Bool
  rival_meets_same_interface : Bool

def tensorNonForcing : NonForcingPack where
  rival_embeds_components := true
  rival_meets_same_interface := false

def NonForcingDischarged (P : NonForcingPack) : Bool :=
  P.rival_embeds_components && P.rival_meets_same_interface

theorem tensor_not_forced_open :
    NonForcingDischarged tensorNonForcing = false :=
  rfl

#print axioms tensor_not_forced_open

theorem tensor_composition_boundary :
    (¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool, bell p = tensor u v p) ∧
      (∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w) ∧
      NonForcingDischarged tensorNonForcing = false :=
  ⟨bell_not_product, sum_component_embedding_surjective,
    tensor_not_forced_open⟩

#print axioms tensor_composition_boundary

end HilbertWalk.TensorCompositionBoundary

private def l5aProvenance : String :=
  "Origin: lean4/TensorCompositionBoundary.lean Claim: bell_not_product AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
