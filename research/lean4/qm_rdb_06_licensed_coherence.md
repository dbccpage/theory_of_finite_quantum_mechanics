/-!
RDB-06: licensed coherence.

L1 residual weights canonically give a diagonal density diagnostic. Off-diagonal
coherence is an additional lift and must carry an explicit license. This file
records the finite checklist firewall: a phase/coherence declaration alone does
not construct licensed coherence.
-/

namespace QM

namespace RDB06

/-- Minimal finite checklist for an off-diagonal/coherence lift. -/
structure CoherenceLicense where
  sectorIdentityPreserved : Bool
  phaseRelationDeclared : Bool
  psdConditionSatisfied : Bool
  observerBasisDeclared : Bool
  authorityCeilingUnchanged : Bool
deriving DecidableEq

def LicensedCoherence (L : CoherenceLicense) : Prop :=
  L.sectorIdentityPreserved = true ∧
    L.phaseRelationDeclared = true ∧
    L.psdConditionSatisfied = true ∧
    L.observerBasisDeclared = true ∧
    L.authorityCeilingUnchanged = true

theorem licensedCoherence_iff_all_fields_true (L : CoherenceLicense) :
    LicensedCoherence L ↔
      L.sectorIdentityPreserved = true ∧
        L.phaseRelationDeclared = true ∧
        L.psdConditionSatisfied = true ∧
        L.observerBasisDeclared = true ∧
        L.authorityCeilingUnchanged = true := by
  rfl

theorem licensedCoherence_requires_phase_relation
    (L : CoherenceLicense) :
    LicensedCoherence L -> L.phaseRelationDeclared = true := by
  intro h
  exact h.2.1

theorem licensedCoherence_requires_authority_ceiling
    (L : CoherenceLicense) :
    LicensedCoherence L -> L.authorityCeilingUnchanged = true := by
  intro h
  exact h.2.2.2.2

theorem missing_psd_blocks_licensedCoherence
    (L : CoherenceLicense) (hPSD : L.psdConditionSatisfied = false) :
    ¬ LicensedCoherence L := by
  intro h
  unfold LicensedCoherence at h
  rw [hPSD] at h
  cases h.2.2.1

theorem missing_observer_basis_blocks_licensedCoherence
    (L : CoherenceLicense) (hBasis : L.observerBasisDeclared = false) :
    ¬ LicensedCoherence L := by
  intro h
  unfold LicensedCoherence at h
  rw [hBasis] at h
  cases h.2.2.2.1

theorem missing_authority_ceiling_blocks_licensedCoherence
    (L : CoherenceLicense) (hAuthority : L.authorityCeilingUnchanged = false) :
    ¬ LicensedCoherence L := by
  intro h
  unfold LicensedCoherence at h
  rw [hAuthority] at h
  cases h.2.2.2.2

/-- A declared phase relation alone is not a coherence license. -/
theorem phaseRelation_not_licensedCoherence :
    ∃ L : CoherenceLicense,
      L.phaseRelationDeclared = true ∧ ¬ LicensedCoherence L := by
  refine ⟨⟨true, true, false, true, true⟩, rfl, ?_⟩
  exact missing_psd_blocks_licensedCoherence _ rfl

theorem not_phaseRelation_implies_licensedCoherence :
    ¬ (∀ L : CoherenceLicense,
      L.phaseRelationDeclared = true -> LicensedCoherence L) := by
  intro h
  rcases phaseRelation_not_licensedCoherence with ⟨L, hPhase, hNot⟩
  exact hNot (h L hPhase)

end RDB06

end QM

#print axioms QM.RDB06.licensedCoherence_iff_all_fields_true
#print axioms QM.RDB06.not_phaseRelation_implies_licensedCoherence
