import D01D02Records

/-!
# CODA-A T01: The Anomalon Terminal & Residual Taxonomy (GTLA-01 / GTLA-02)

Formalizes:
1. GTLA-01: Anomalon is the `closedResidual` bin, not the whole taxonomy.
2. Negative distinctions: other residual outcomes are strictly not the Anomalon.
3. Toy discrete homomorphisms: Anomalon is not initial to open residuals in the toy.
4. Open status: initiality among residuals is not shown in CODA-A.

AuthorityEffect: None.
-/

namespace CodaA

open CodaA

set_option linter.unusedVariables false

theorem closedResidual_is_anomalon : IsAnomalon .closedResidual := trivial

theorem openResidual_is_not_anomalon : ¬ IsAnomalon .openResidual := by
  intro h
  contradiction

theorem closureAbsorbed_is_not_anomalon : ¬ IsAnomalon .closureAbsorbed := by
  intro h
  contradiction

theorem liftRequired_is_not_anomalon : ¬ IsAnomalon .liftRequired := by
  intro h
  contradiction

theorem refusedClosure_is_not_anomalon : ¬ IsAnomalon .refusedClosure := by
  intro h
  contradiction

/-- Toy identity-only homs. Not a declared category; serves to test initiality. -/
inductive ToyDiscreteHom : ResidualTerminal → ResidualTerminal → Prop where
  | id : (t : ResidualTerminal) → ToyDiscreteHom t t

theorem toy_discrete_hom_no_anomalon_to_open :
    ToyDiscreteHom .closedResidual .openResidual → False := by
  intro h
  cases h

theorem toy_discrete_hom_not_initial :
    ¬ (∀ t, ToyDiscreteHom .closedResidual t) := by
  intro h
  exact toy_discrete_hom_no_anomalon_to_open (h .openResidual)

/-- Initiality status for the living taxonomy: OPEN. -/
inductive InitialityStatus where
  | openStatus
  | shownInitial
  | shownNotInitial
  deriving Repr, DecidableEq

def anomalonInitiality : InitialityStatus := .openStatus

theorem anomalon_initiality_not_shown :
    anomalonInitiality ≠ InitialityStatus.shownInitial := by
  intro h
  cases h

theorem anomalon_initiality_not_shown_negative :
    anomalonInitiality ≠ InitialityStatus.shownNotInitial := by
  intro h
  cases h

end CodaA
