






import HWKernel
import InterferenceNonDescent

namespace HilbertWalk.U1SelectorBoundary

open HilbertWalk.HWKernel
open HilbertWalk.InterferenceNonDescent

structure SelectorPack where
  phase_composition_law : Bool
  transport_functoriality : Bool
  carrier_connectedness : Bool
  rival_excluded : Bool

def SelectorDischarged (S : SelectorPack) : Bool :=
  S.phase_composition_law && S.transport_functoriality &&
    S.carrier_connectedness && S.rival_excluded

def qm062Route : SelectorPack where
  phase_composition_law := true
  transport_functoriality := true
  carrier_connectedness := true
  rival_excluded := false

theorem selector_not_free : SelectorDischarged qm062Route = false :=
  rfl

#print axioms selector_not_free

theorem sign_carrier_suffices :
    (∀ q : Bool, iWeights iPsi1 q = iWeights iPsi2 q) ∧
      ¬(∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : HilbertWalk.FreeLinearization.Vec Int Bool,
          iReadout v = f (iWeights v) :=
  ⟨int_realization.1, int_realization.2, int_no_descent⟩

#print axioms sign_carrier_suffices

theorem u1_selector_boundary :
    SelectorDischarged qm062Route = false ∧
      ¬(∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) :=
  ⟨selector_not_free, int_realization.2⟩

#print axioms u1_selector_boundary

theorem selector_requires_rival_exclusion (S : SelectorPack)
    (hφ : S.phase_composition_law = true)
    (hτ : S.transport_functoriality = true)
    (hκ : S.carrier_connectedness = true)
    (hρ : S.rival_excluded = false) :
    SelectorDischarged S = false := by
  simp [SelectorDischarged, hφ, hτ, hκ, hρ]

theorem sign_units_closed (a b : Int) (ha : a = 1 ∨ a = -1) (hb : b = 1 ∨ b = -1) :
    a * b = 1 ∨ a * b = -1 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> decide

theorem quarter_turn_outside_sign_subgroup :
    let one : Fin 4 := 0
    let quarter : Fin 4 := 1
    let half : Fin 4 := 2
    (one + one = one) ∧ (one + half = half) ∧ (half + half = one) ∧
      (quarter + quarter = half) ∧ quarter ≠ one ∧ quarter ≠ half := by
  decide

end HilbertWalk.U1SelectorBoundary

private def l5aProvenance : String :=
  "Origin: lean4/U1SelectorBoundary.lean Claim: selector_not_free AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
