/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\global_computability_lift_models.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.GlobalLift
-/
/-!
# Class-relative undecidability transport for authorization

Paper key: `authorization_an_incompleteness_theory`

This file is not Rice's theorem. It formalizes the smaller transport
shape needed before a Rice-style lift can be claimed: if a source problem
reduces to proposal validity, and every allowed proposal authorizer
precomposes to an allowed source decider, then source undecidability
blocks a total allowed authorizer.

The `allowedHard` and `allowedProposal` predicates are deliberately
explicit. Calling every `X -> Bool` function "computable" would erase the
computability representation that the later Rice proof must supply.
The next lift must instantiate them with a real code language, total
evaluator, and closure proof.

This file proves neither the source undecidability premise nor a Rice
reduction, and it says nothing about P versus NP.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.GlobalComputabilityLift

/-- A Boolean procedure decides a predicate exactly when it is sound and
    complete for that predicate on every input in the stated carrier. -/
def Decides {Input : Type} (predicate : Input -> Prop)
    (decider : Input -> Bool) : Prop :=
  ∀ input, decider input = true ↔ predicate input

/-- No procedure in the declared decision class is a total decider for the
    predicate. This is class-relative, not a bare set-theoretic claim. -/
def NoTotalDecider {Input : Type} (allowed : (Input -> Bool) -> Prop)
    (predicate : Input -> Prop) : Prop :=
  ¬ ∃ decider, allowed decider ∧ Decides predicate decider

/-- A reduction maps source instances to proposal instances while preserving
    the source predicate exactly. -/
structure ValidityReduction {HardInput Proposal : Type}
    (hard : HardInput -> Prop) (valid : Proposal -> Prop) where
  map : HardInput -> Proposal
  preserves : ∀ input, valid (map input) ↔ hard input

/-- The proposal decision class may be transported back through the declared
    reduction. A Rice lift must prove this for its actual program encoding. -/
def ClosedUnderReduction {HardInput Proposal : Type}
    (allowedHard : (HardInput -> Bool) -> Prop)
    (allowedProposal : (Proposal -> Bool) -> Prop)
    {hard : HardInput -> Prop} {valid : Proposal -> Prop}
    (reduction : ValidityReduction hard valid) : Prop :=
  ∀ authorize, allowedProposal authorize ->
    allowedHard (fun input => authorize (reduction.map input))

/-- A total allowed authorizer for reduced proposal validity yields a total
    allowed decider for the source problem. -/
theorem total_authorizer_yields_source_decider
    {HardInput Proposal : Type}
    {hard : HardInput -> Prop} {valid : Proposal -> Prop}
    {allowedHard : (HardInput -> Bool) -> Prop}
    {allowedProposal : (Proposal -> Bool) -> Prop}
    (reduction : ValidityReduction hard valid)
    (closure : ClosedUnderReduction allowedHard allowedProposal reduction)
    (hasAuthorizer : ∃ authorize,
      allowedProposal authorize ∧ Decides valid authorize) :
    ∃ decide, allowedHard decide ∧ Decides hard decide := by
  rcases hasAuthorizer with ⟨authorize, allowed, decides⟩
  refine ⟨fun input => authorize (reduction.map input), closure authorize allowed, ?_⟩
  intro input
  constructor
  · intro decision
    exact (reduction.preserves input).mp ((decides (reduction.map input)).mp decision)
  · intro verdict
    exact (decides (reduction.map input)).mpr ((reduction.preserves input).mpr verdict)

/-- The contrapositive transport used by the global authorization program.
    It becomes a Rice-style result only after a real source no-decider,
    program reduction, and decision-class closure are supplied. -/
theorem no_source_decider_blocks_total_authorizer
    {HardInput Proposal : Type}
    {hard : HardInput -> Prop} {valid : Proposal -> Prop}
    {allowedHard : (HardInput -> Bool) -> Prop}
    {allowedProposal : (Proposal -> Bool) -> Prop}
    (reduction : ValidityReduction hard valid)
    (closure : ClosedUnderReduction allowedHard allowedProposal reduction)
    (noSourceDecider : NoTotalDecider allowedHard hard) :
    NoTotalDecider allowedProposal valid := by
  intro hasAuthorizer
  exact noSourceDecider
    (total_authorizer_yields_source_decider reduction closure hasAuthorizer)

end AuthorizationIncompleteness.GlobalComputabilityLift

#print axioms
  AuthorizationIncompleteness.GlobalComputabilityLift.total_authorizer_yields_source_decider
#print axioms
  AuthorizationIncompleteness.GlobalComputabilityLift.no_source_decider_blocks_total_authorizer
