/-!
RDB-11: branch ranking is not branch acceptance.

The runtime branch-search slice may rank candidate lifts by normalized proposal
mass. This file records the governance boundary: a ranking diagnostic can exist
without accepting any branch, so ranking is not a descent gate and not authority.
-/

namespace QM

namespace RDB11

structure BranchRankingRuntime where
  proposalWeightsNormalize : Bool
  rankingComputed : Bool
  authorityEffectNone : Bool
  descentAccepted : Bool
deriving DecidableEq, Repr

def BranchRankingDiagnostic (r : BranchRankingRuntime) : Prop :=
  r.proposalWeightsNormalize = true ∧
    r.rankingComputed = true ∧
    r.authorityEffectNone = true

def BranchAccepted (r : BranchRankingRuntime) : Prop :=
  r.descentAccepted = true

def AuthorityPromoted (r : BranchRankingRuntime) : Prop :=
  r.authorityEffectNone = false

theorem branchRankingDiagnostic_iff_fields (r : BranchRankingRuntime) :
    BranchRankingDiagnostic r ↔
      r.proposalWeightsNormalize = true ∧
        r.rankingComputed = true ∧
        r.authorityEffectNone = true := by
  rfl

theorem branchRankingDiagnostic_no_authority_promotion
    {r : BranchRankingRuntime} (h : BranchRankingDiagnostic r) :
    ¬ AuthorityPromoted r := by
  intro hp
  exact Bool.noConfusion (h.2.2.symm.trans hp)

theorem branchRankingDiagnostic_without_acceptance_witness :
    ∃ r : BranchRankingRuntime,
      BranchRankingDiagnostic r ∧ ¬ BranchAccepted r := by
  refine ⟨
    { proposalWeightsNormalize := true,
      rankingComputed := true,
      authorityEffectNone := true,
      descentAccepted := false }, ?_⟩
  constructor
  · exact ⟨rfl, rfl, rfl⟩
  · intro h
    exact Bool.noConfusion h

theorem not_branchRankingDiagnostic_implies_acceptance :
    ¬ (∀ r : BranchRankingRuntime,
      BranchRankingDiagnostic r -> BranchAccepted r) := by
  intro h
  obtain ⟨r, hr, hnot⟩ := branchRankingDiagnostic_without_acceptance_witness
  exact hnot (h r hr)

end RDB11

end QM

#print axioms QM.RDB11.branchRankingDiagnostic_no_authority_promotion
#print axioms QM.RDB11.not_branchRankingDiagnostic_implies_acceptance
