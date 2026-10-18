/-!
LT-G — lift trigger ⊬ licensed lift.

Paper: `06_tower_walk_registry_relative_interface_lift.md` §2; `20_…` §1.1.

A lift situation carries representation `pressure` (the lift *trigger*) and,
separately, a `license` (a declared transport + minimality certificate). Pressure
flags that a lift is *required*, but the firewall is that a trigger does **not**
construct a *licensed* lift: pressure can hold while no license exists. No
authority; Mathlib-free.
-/

namespace QM

/-- A lift situation: representation pressure, and—separately—a license certificate. -/
structure LiftSituation where
  pressure : Bool
  license  : Bool
deriving DecidableEq

/-- The lift trigger: representation pressure is present. -/
def LiftTrigger (s : LiftSituation) : Prop := s.pressure = true

/-- A lift is flagged as required (here: by the same pressure). -/
def LiftRequired (s : LiftSituation) : Prop := s.pressure = true

/-- A licensed lift: a declared transport + minimality certificate is present. -/
def LicensedLift (s : LiftSituation) : Prop := s.license = true

/-- Representation pressure flags that a lift is required. -/
theorem trigger_implies_required (s : LiftSituation) : LiftTrigger s → LiftRequired s :=
  fun h => h

/-- **Firewall.** A lift trigger does not construct a licensed lift — pressure can
hold while no license exists. -/
theorem trigger_not_licensing : ∃ s, LiftTrigger s ∧ ¬ LicensedLift s := by
  refine ⟨{ pressure := true, license := false }, rfl, ?_⟩
  show ¬ (false = true)
  decide

/-- The general non-implication fails: `LiftTrigger → LicensedLift` does not hold
for all situations. -/
theorem not_trigger_implies_licensed :
    ¬ (∀ s, LiftTrigger s → LicensedLift s) := by
  intro h
  obtain ⟨s, htrig, hnot⟩ := trigger_not_licensing
  exact hnot (h s htrig)

end QM

#print axioms QM.trigger_implies_required
#print axioms QM.trigger_not_licensing
#print axioms QM.not_trigger_implies_licensed
