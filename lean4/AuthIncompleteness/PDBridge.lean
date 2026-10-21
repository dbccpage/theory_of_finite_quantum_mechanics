/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\primitive_difference_p0_bridge.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.PDBridge
  NOT BUILT / NOT IN LAKEFILE ROOTS: imports J011's candidate
  `J011_minimal_publication` (namespace `GrokPdNight20260814`), whose source is
  not present in this repository or in the recovered folder. Statements are
  unchanged; the import is kept verbatim so the file elaborates unchanged once
  J011 is supplied.
-/
import J011_minimal_publication

/-!
# Primitive Difference quotient to the P0 authorization boundary

Paper key: `authorization_an_incompleteness_theory`

This bridge imports the candidate J011 Primitive Difference quotient
interface. For a supplied validity predicate on the original carrier, it
proves that a report-only decision on J011's canonical quotient cannot be
totally correct when validity splits a ZeroRel class.

The bridge is a statement-level specialization of PO-000's
`AuthorizationBoundary.no_report_decision`; PO-000 has no Lake module to
import here. The correspondence is explicit:

* PO-000 proposal carrier `X` is J011's `α`;
* PO-000 report `p` is J011's canonical `pdProj P`;
* PO-000 report fiber equality is J011's `ZeroRel P`, by
  `pdProj_eq_iff_zeroRel`;
* PO-000 `valid` remains supplied data, not Primitive Difference output.

It proves neither a global authorization theorem nor that Primitive
Difference produces validity, a Turing machine, an LLM, or a terminal
policy. The positive direction requires an explicit ZeroRel-constancy
hypothesis.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge

open GrokPdNight20260814.Core
open GrokPdNight20260814.J011

/-- A report-only decision is totally correct when validity factors
    through the declared report. -/
def FactorsThrough {Proposal Report : Type} (report : Proposal -> Report)
    (valid : Proposal -> Bool) (authorize : Report -> Bool) : Prop :=
  ∀ proposal, authorize (report proposal) = valid proposal

/-- If a decision factors through the J011 Primitive Difference quotient,
    supplied validity must be constant on its ZeroRel classes. -/
theorem pd_quotient_total_decision_requires_zeroRel_constancy
    {α β : Type} (P : PrimitiveDifference α β) (valid : α -> Bool)
    (authorize : ResidualQuotient (pdSetoid P) -> Bool)
    (hAuthorize : FactorsThrough (pdProj P) valid authorize) :
    ∀ left right : α, ZeroRel P left right -> valid left = valid right := by
  intro left right hzero
  have sameReport : pdProj P left = pdProj P right :=
    (pdProj_eq_iff_zeroRel P left right).mpr hzero
  calc
    valid left = authorize (pdProj P left) := (hAuthorize left).symm
    _ = authorize (pdProj P right) := congrArg authorize sameReport
    _ = valid right := hAuthorize right

/-- A validity-splitting ZeroRel class blocks every decision that reads
    only the canonical J011 quotient report. -/
theorem pd_quotient_split_blocks_report_only_authorization
    {α β : Type} (P : PrimitiveDifference α β) (valid : α -> Bool)
    (split : ∃ left right : α,
      ZeroRel P left right ∧ valid left ≠ valid right) :
    ¬ (∃ authorize : ResidualQuotient (pdSetoid P) -> Bool,
      FactorsThrough (pdProj P) valid authorize) := by
  rintro ⟨authorize, hAuthorize⟩
  rcases split with ⟨left, right, hzero, differentValidity⟩
  exact differentValidity
    (pd_quotient_total_decision_requires_zeroRel_constancy P valid authorize
      hAuthorize left right hzero)

/-- When supplied validity is constant on the ZeroRel classes, it has a
    well-defined quotient decision. The hypothesis is an added adequacy
    condition; it is not derived from Primitive Difference. -/
def pdQuotientDecision {α β : Type} (P : PrimitiveDifference α β)
    (valid : α -> Bool)
    (hconst : ∀ left right : α,
      ZeroRel P left right -> valid left = valid right) :
    ResidualQuotient (pdSetoid P) -> Bool :=
  Quotient.lift valid (by
    intro left right hzero
    exact hconst left right hzero)

theorem pd_quotient_decision_if_zeroRel_constant
    {α β : Type} (P : PrimitiveDifference α β) (valid : α -> Bool)
    (hconst : ∀ left right : α,
      ZeroRel P left right -> valid left = valid right) :
    FactorsThrough (pdProj P) valid (pdQuotientDecision P valid hconst) := by
  intro proposal
  rfl

/-- A J011 concrete negative model: the collapse Primitive Difference
    identifies `false` and `true`, while supplied validity keeps the bit. -/
def collapseValidity : Bool -> Bool := id

theorem collapse_pd_zeroRel_splits_validity :
    ∃ left right : Bool,
      ZeroRel collapsePD left right ∧
        collapseValidity left ≠ collapseValidity right := by
  refine ⟨false, true, True.intro, ?_⟩
  decide

theorem collapse_pd_blocks_report_only_authorization :
    ¬ (∃ authorize : ResidualQuotient (pdSetoid collapsePD) -> Bool,
      FactorsThrough (pdProj collapsePD) collapseValidity authorize) :=
  pd_quotient_split_blocks_report_only_authorization collapsePD
    collapseValidity collapse_pd_zeroRel_splits_validity

end AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge

#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_total_decision_requires_zeroRel_constancy
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_split_blocks_report_only_authorization
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_decision_if_zeroRel_constant
#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.collapse_pd_blocks_report_only_authorization
