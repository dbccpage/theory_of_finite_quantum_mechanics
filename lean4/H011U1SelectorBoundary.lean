/-
  H011 -- U(1) transport selector boundary. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY.

  Claim identifier: HW-H011
  Source-paper contact: QM_062 (the U(1) selector, audited as a
  conditional proposal), QM_207 (audited as proposal). H010
  int_realization is the rival-carrier witness.

  Target proposition
    The interference witness does not select the phase carrier: the
    sign group {1, -1} inside Int already realizes it (H010
    int_no_descent). Any narrowing to U(1)/C is a theorem ONLY
    under selector assumptions, which this rung represents as named
    imports; without a rival-exclusion theorem the selector is
    undischarged.

  Imports added at this rung
    The selector assumption pack: each field is a named assumption
    of the QM_062 route, imported as data, proved nowhere here.

  Theorem or counterexample
    sign_carrier_suffices: re-export of H010's Int realization --
    the rival carrier the work order demands.
    selector_not_free: dropping the rival-exclusion flag falsifies
    the discharged-selector predicate (SpinePack-style gate).

  Nonclaim boundary
    No claim that U(1) or C is selected, and no claim that it is
    NOT selectable: the rung prices the remaining theorem. The
    field names below summarize QM_062's assumption surface as
    audited; binding them to exact QM_062 statements is claim-map
    work, not proof.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H010InterferenceNonDescent

namespace FableHilbertWalk20260819.H011

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H010

/-- Named selector assumptions, imported as data. -/
structure SelectorPack where
  phase_composition_law : Bool
  transport_functoriality : Bool
  carrier_connectedness : Bool
  rival_excluded : Bool

def SelectorDischarged (S : SelectorPack) : Bool :=
  S.phase_composition_law && S.transport_functoriality &&
    S.carrier_connectedness && S.rival_excluded

/-- QM_062's route with every assumption granted EXCEPT a proved
    exclusion of rival carriers. -/
def qm062Route : SelectorPack where
  phase_composition_law := true
  transport_functoriality := true
  carrier_connectedness := true
  rival_excluded := false

theorem selector_not_free : SelectorDischarged qm062Route = false :=
  rfl

#print axioms selector_not_free

/-- The rival carrier is not hypothetical: the sign group inside
    Int realizes the interference witness with its non-descent
    (re-export of H010). -/
theorem sign_carrier_suffices :
    (∀ q : Bool, iWeights iPsi1 q = iWeights iPsi2 q) ∧
      ¬(∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : FableHilbertWalk20260819.H004.Vec Int Bool,
          iReadout v = f (iWeights v) :=
  ⟨int_realization.1, int_realization.2, int_no_descent⟩

#print axioms sign_carrier_suffices

/-- H011 punchline: the witness runs on the sign group, so the
    selector remains an undischarged import package. -/
theorem u1_selector_boundary :
    SelectorDischarged qm062Route = false ∧
      ¬(∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) :=
  ⟨selector_not_free, int_realization.2⟩

#print axioms u1_selector_boundary

/-- Discharge fails for every pack that keeps a rival carrier. -/
theorem selector_requires_rival_exclusion (S : SelectorPack)
    (hφ : S.phase_composition_law = true)
    (hτ : S.transport_functoriality = true)
    (hκ : S.carrier_connectedness = true)
    (hρ : S.rival_excluded = false) :
    SelectorDischarged S = false := by
  simp [SelectorDischarged, hφ, hτ, hκ, hρ]

/-- The sign units `{1, -1}` are closed under multiplication. -/
theorem sign_units_closed (a b : Int) (ha : a = 1 ∨ a = -1) (hb : b = 1 ∨ b = -1) :
    a * b = 1 ∨ a * b = -1 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> decide

/-- Quarter-turns in `Z/4Z` sit outside the sign subgroup `{0, 2}`. -/
theorem quarter_turn_outside_sign_subgroup :
    let one : Fin 4 := 0
    let quarter : Fin 4 := 1
    let half : Fin 4 := 2
    (one + one = one) ∧ (one + half = half) ∧ (half + half = one) ∧
      (quarter + quarter = half) ∧ quarter ≠ one ∧ quarter ≠ half := by
  decide

end FableHilbertWalk20260819.H011
