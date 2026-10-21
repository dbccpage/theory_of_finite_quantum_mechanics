/-!
# Authorization Incompleteness: finite information core

Paper key: `authorization_an_incompleteness_theory`

This file proves a necessary condition for total report-only
authorization. If a validity predicate has two different values on one
report fiber, then no decision function receiving only that report can
be correct on every proposal.

It does not mention LLMs, arbitrary programs, Rice's theorem, Goedel's
theorem, physical independence, or final authority. Those are later
proof goals with their own carriers and hypotheses.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness

/-- A report-only authorizer decides validity exactly when validity
    factors through the report. -/
def FactorsThrough {Proposal Report : Type} (report : Proposal -> Report)
    (valid : Proposal -> Bool) (authorize : Report -> Bool) : Prop :=
  ∀ proposal, authorize (report proposal) = valid proposal

/-- A report is adequate for a validity predicate exactly when the
    predicate is constant on every report fiber. -/
def Adequate {Proposal Report : Type} (report : Proposal -> Report)
    (valid : Proposal -> Bool) : Prop :=
  ∀ left right, report left = report right -> valid left = valid right

/-- Any totally correct report-only authorizer requires report adequacy. -/
theorem total_authorization_requires_adequacy {Proposal Report : Type}
    (report : Proposal -> Report) (valid : Proposal -> Bool)
    (authorize : Report -> Bool)
    (h : FactorsThrough report valid authorize) :
    Adequate report valid := by
  intro left right sameReport
  calc
    valid left = authorize (report left) := (h left).symm
    _ = authorize (report right) := congrArg authorize sameReport
    _ = valid right := h right

/-- A single validity-splitting report fiber blocks every report-only
    total authorizer. -/
theorem split_fiber_blocks_total_authorization {Proposal Report : Type}
    (report : Proposal -> Report) (valid : Proposal -> Bool)
    (split : ∃ left right,
      report left = report right ∧ valid left ≠ valid right) :
    ¬ (∃ authorize : Report -> Bool,
      FactorsThrough report valid authorize) := by
  rintro ⟨authorize, hAuthorizes⟩
  rcases split with ⟨left, right, sameReport, differentValidity⟩
  exact differentValidity
    (total_authorization_requires_adequacy report valid authorize
      hAuthorizes left right sameReport)

/-- A tiny submitted packet. `semanticBit` stands for a fact that the
    contract cares about; it is not an LLM model. -/
structure Packet where
  semanticBit : Bool

/-- A source can emit a receipt that carries no information about the
    contract-relevant bit. -/
def selfReceipt (_packet : Packet) : Unit := ()

/-- The declared validity predicate for the toy contract. -/
def toyValid (packet : Packet) : Bool := packet.semanticBit

/-- The constant receipt identifies a valid and an invalid packet. -/
theorem self_receipt_splits_validity :
    ∃ left right : Packet,
      selfReceipt left = selfReceipt right ∧ toyValid left ≠ toyValid right := by
  refine ⟨{ semanticBit := false }, { semanticBit := true }, rfl, ?_⟩
  decide

/-- Hence no function of this self-receipt supplies total authorization
    for the toy contract. -/
theorem self_receipt_blocks_authorization :
    ¬ (∃ authorize : Unit -> Bool,
      FactorsThrough selfReceipt toyValid authorize) :=
  split_fiber_blocks_total_authorization selfReceipt toyValid
    self_receipt_splits_validity

/-- A complete report can decide the deliberately small contract. This
    positive witness prevents the theorem from being read as a ban on
    all local authorization. -/
def completeReceipt (packet : Packet) : Bool := toyValid packet

theorem complete_receipt_decides_toy_contract :
    FactorsThrough completeReceipt toyValid id := by
  intro packet
  rfl

end AuthorizationIncompleteness

#print axioms AuthorizationIncompleteness.total_authorization_requires_adequacy
#print axioms AuthorizationIncompleteness.split_fiber_blocks_total_authorization
#print axioms AuthorizationIncompleteness.self_receipt_blocks_authorization
#print axioms AuthorizationIncompleteness.complete_receipt_decides_toy_contract
