
namespace FableHilbertWalk20260819.H077

inductive FQMC1Clause where
  | C01_FiniteCarrierScalarDomain
  | C02_NormalizedStatesEffectsPairing
  | C03_TransformationsInstruments
  | C04_CompositionSubsystemInterface
  | C05_ReversibleIrreversibleTimeSemantics
  | C06_ContextualMultipartiteCorrelations
  | C07_TerminatingComputationalClaims
  | C08_TypedStructuralClaims
  | C09_MetricAndErrorForComparisons
  | C10_ImportedStructurePriceRefusalLedger
  deriving DecidableEq, Repr

def allClauses : List FQMC1Clause := [
  .C01_FiniteCarrierScalarDomain, .C02_NormalizedStatesEffectsPairing,
  .C03_TransformationsInstruments, .C04_CompositionSubsystemInterface,
  .C05_ReversibleIrreversibleTimeSemantics, .C06_ContextualMultipartiteCorrelations,
  .C07_TerminatingComputationalClaims, .C08_TypedStructuralClaims,
  .C09_MetricAndErrorForComparisons, .C10_ImportedStructurePriceRefusalLedger]

theorem fqmc1_has_ten_clause_labels : allClauses.length = 10 := by decide

theorem every_clause_label_listed (clause : FQMC1Clause) : allClauses.contains clause = true := by
  cases clause <;> decide

inductive CampaignTerminal where
  | FQMC1_CLOSED_AT_DECLARED_CLASS
  | FQMC1_OPEN_INTERNAL_GAPS
  | FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT
  deriving DecidableEq, Repr

def decide_terminal (untyped_count open_count : Nat) (global_refusal : Bool) : CampaignTerminal :=
  if global_refusal then .FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT
  else if untyped_count > 0 ∨ open_count > 0 then .FQMC1_OPEN_INTERNAL_GAPS
  else .FQMC1_CLOSED_AT_DECLARED_CLASS

theorem unresolved_counts_yield_open (untyped_count open_count : Nat)
    (h : untyped_count > 0 ∨ open_count > 0) :
    decide_terminal untyped_count open_count false = .FQMC1_OPEN_INTERNAL_GAPS := by
  simp [decide_terminal, h]

theorem zero_counts_yield_conditional_closed :
    decide_terminal 0 0 false = .FQMC1_CLOSED_AT_DECLARED_CLASS := rfl

theorem explicit_global_refusal (untyped_count open_count : Nat) :
    decide_terminal untyped_count open_count true = .FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT := rfl

inductive RefusalId where
  | DirectNonZeroCcrFiniteDim | TopologyFreeContinuumLimit
  | UnrestrictedCorrelationAlgorithm | UnpricedContinuumFieldLimits
  deriving DecidableEq, Repr

def refusalLabels : List RefusalId := [.DirectNonZeroCcrFiniteDim, .TopologyFreeContinuumLimit,
  .UnrestrictedCorrelationAlgorithm, .UnpricedContinuumFieldLimits]

theorem has_four_refusal_labels : refusalLabels.length = 4 := by decide

#print axioms fqmc1_has_ten_clause_labels
#print axioms every_clause_label_listed
#print axioms unresolved_counts_yield_open
#print axioms zero_counts_yield_conditional_closed
#print axioms explicit_global_refusal
#print axioms has_four_refusal_labels
end FableHilbertWalk20260819.H077

private def l5aProvenance : String :=
  "Origin: lean4/H077FiniteOperationalClosureContract.lean Claim: fqmc1_has_ten_clause_labels AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
