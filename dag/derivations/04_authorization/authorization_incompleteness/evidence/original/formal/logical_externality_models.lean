import authorization_incompleteness_core

/-!
# Logical versus physical externality: finite authorization models

Paper key: `authorization_an_incompleteness_theory`

This file separates two claims that must not be conflated.

1. A physically co-located proposal source and evaluator can authorize a
   bounded contract when the report retains every contract-relevant bit.
2. Physically distinct source and evaluator sites cannot authorize a
   contract from an inadequate report.

Thus the finite information theorem requires report adequacy, not a
different computer, company, or human. `Site` is only a finite label in
this model. It does not formalize causal custody, adversarial process
isolation, cryptographic binding, or semantic truth beyond `valid`.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.LogicalExternalityModels

/-- A proposal/report interface with labels for the proposal and
    evaluator execution sites. The labels alone carry no trust claim. -/
structure Presentation (Proposal Report Site : Type) where
  sourceSite : Site
  evaluatorSite : Site
  report : Proposal -> Report
  valid : Proposal -> Bool

/-- A presentation admits total report-only authorization exactly when
    some decision factors the supplied validity predicate through report. -/
def CanAuthorize {Proposal Report Site : Type}
    (presentation : Presentation Proposal Report Site) : Prop :=
  ∃ decide : Report -> Bool,
    FactorsThrough presentation.report presentation.valid decide

theorem can_authorize_requires_adequacy {Proposal Report Site : Type}
    (presentation : Presentation Proposal Report Site)
    (h : CanAuthorize presentation) :
    Adequate presentation.report presentation.valid := by
  rcases h with ⟨decide, hdecide⟩
  exact total_authorization_requires_adequacy presentation.report
    presentation.valid decide hdecide

/-- A complete Boolean report and its checker run on the same declared
    site. This is a local bounded contract, not a security architecture. -/
def coLocatedComplete : Presentation Bool Bool Unit where
  sourceSite := ()
  evaluatorSite := ()
  report := id
  valid := id

theorem coLocatedComplete_same_site :
    coLocatedComplete.sourceSite = coLocatedComplete.evaluatorSite := by
  rfl

theorem coLocatedComplete_can_authorize :
    CanAuthorize coLocatedComplete := by
  refine ⟨id, ?_⟩
  intro proposal
  rfl

/-- A report that erases its Boolean proposal bit while the declared
    evaluator site is different from the source site. -/
def separatedCollapsed : Presentation Bool Unit Bool where
  sourceSite := false
  evaluatorSite := true
  report := fun _ => ()
  valid := id

theorem separatedCollapsed_distinct_sites :
    separatedCollapsed.sourceSite ≠ separatedCollapsed.evaluatorSite := by
  decide

theorem separatedCollapsed_split_fiber :
    ∃ left right : Bool,
      separatedCollapsed.report left = separatedCollapsed.report right ∧
        separatedCollapsed.valid left ≠ separatedCollapsed.valid right := by
  refine ⟨false, true, rfl, ?_⟩
  decide

theorem separatedCollapsed_cannot_authorize :
    ¬ CanAuthorize separatedCollapsed := by
  exact split_fiber_blocks_total_authorization separatedCollapsed.report
    separatedCollapsed.valid separatedCollapsed_split_fiber

/-- The finite conclusion about physical placement. This does not say
    that co-location is secure, nor that site labels capture independence. -/
theorem physical_separation_neither_needed_nor_sufficient_for_toy_authorization :
    (coLocatedComplete.sourceSite = coLocatedComplete.evaluatorSite ∧
      CanAuthorize coLocatedComplete) ∧
    (separatedCollapsed.sourceSite ≠ separatedCollapsed.evaluatorSite ∧
      ¬ CanAuthorize separatedCollapsed) := by
  exact ⟨⟨coLocatedComplete_same_site, coLocatedComplete_can_authorize⟩,
    ⟨separatedCollapsed_distinct_sites, separatedCollapsed_cannot_authorize⟩⟩

end AuthorizationIncompleteness.LogicalExternalityModels

#print axioms AuthorizationIncompleteness.LogicalExternalityModels.can_authorize_requires_adequacy
#print axioms AuthorizationIncompleteness.LogicalExternalityModels.coLocatedComplete_can_authorize
#print axioms AuthorizationIncompleteness.LogicalExternalityModels.separatedCollapsed_cannot_authorize
#print axioms AuthorizationIncompleteness.LogicalExternalityModels.physical_separation_neither_needed_nor_sufficient_for_toy_authorization
