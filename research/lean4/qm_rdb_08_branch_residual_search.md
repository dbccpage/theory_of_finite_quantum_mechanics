import «rdb_01_normalized_residual_weights»
import «possibility_boundaries»

/-!
RDB-08: branch-residual search.

Branches are candidate residual repairs/lifts with proposal mass. Their weights
can be normalized exactly like residual-sector weights, but branch
representation does not construct an ontology terminal.
-/

open scoped BigOperators

namespace QM

namespace RDB08

noncomputable section

variable {Branch : Type*} [Fintype Branch]

abbrev branchTotalMass (mass : Branch -> ℚ) : ℚ :=
  RDB01.residualTotalMass mass

abbrev branchProposalWeight (mass : Branch -> ℚ) (b : Branch) : ℚ :=
  RDB01.residualWeight mass b

theorem branchProposalWeights_probability
    (mass : Branch -> ℚ)
    (hmass : ∀ b, 0 ≤ mass b) (hTotal : 0 < branchTotalMass mass) :
    (∀ b, 0 ≤ branchProposalWeight mass b ∧
      branchProposalWeight mass b ≤ 1) ∧
      ∑ b, branchProposalWeight mass b = 1 := by
  simpa [branchProposalWeight, branchTotalMass] using
    RDB01.normalizedResidualWeights_probability mass hmass hTotal

theorem branchRepresentation_not_ontology :
    ∃ s : EverettSituation,
      BranchRepresentation s ∧ ¬ OntologyTerminal s := by
  exact branch_not_ontology

theorem not_branchRepresentation_implies_ontology :
    ¬ (∀ s : EverettSituation,
      BranchRepresentation s -> OntologyTerminal s) := by
  exact not_branch_implies_ontology

/-- Branch proposal weights are diagnostics for search; they do not turn branch
representation into ontology. -/
theorem branchSearch_probability_and_no_ontology_promotion
    (mass : Branch -> ℚ)
    (hmass : ∀ b, 0 ≤ mass b) (hTotal : 0 < branchTotalMass mass) :
    ((∀ b, 0 ≤ branchProposalWeight mass b ∧
      branchProposalWeight mass b ≤ 1) ∧
      ∑ b, branchProposalWeight mass b = 1) ∧
      ¬ (∀ s : EverettSituation,
        BranchRepresentation s -> OntologyTerminal s) := by
  exact
    ⟨branchProposalWeights_probability mass hmass hTotal,
      not_branchRepresentation_implies_ontology⟩

end

end RDB08

end QM

#print axioms QM.RDB08.branchProposalWeights_probability
#print axioms QM.RDB08.branchSearch_probability_and_no_ontology_promotion
