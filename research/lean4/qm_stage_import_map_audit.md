import «qm_ledger_aware_stage_discharge»

/-!
# QMStageImportMapAudit — Holy Land Phase 2 map audit

This module audits the frozen stage-to-import map used by the ledger-aware T3
successor. It proves that every slot in the provisional recovery ledger has a
named witness stage, records an exhaustive eight-row witness list, and preserves
the T3L-2 erase-one failure theorem on the audited map.

The audit is relative to the provisional B8 registry and frozen
`stageImportSlots` definition. It does not prove a final import basis,
import sufficiency, sealed finite matrix recovery, or an authority effect.

AuthorityEffect: None.
-/

namespace QM
namespace FiniteMatrixRecovery

/-! ## Explicit B8 stage witnesses -/

/--
One frozen witness stage for each provisional B8 recovery-import slot, in the
same order as `provisionalRecoveryLedger`.
-/
def provisionalRecoveryLedgerStageWitnesses :
    List (RecoveryImportSlot × RecoveryStage) :=
  [ (.NONCOMM, .LiftHost)
  , (.UNITARY, .SpectralBornCompose)
  , (.CLONE, .Ops)
  , (.CONT_TIME, .Ops)
  , (.HERM, .SpectralBornCompose)
  , (.L2_READOUT, .Surplus)
  , (.BORN, .SpectralBornCompose)
  , (.BUNDLE_U1_LT, .SpectralBornCompose) ]

/--
The eight-row witness list is exhaustive for the provisional ledger, and every
listed row names a stage whose frozen import list contains that slot.
-/
theorem provisional_recovery_ledger_stage_witnesses_exhaustive :
    provisionalRecoveryLedgerStageWitnesses.length = 8 ∧
    provisionalRecoveryLedgerStageWitnesses.map Prod.fst =
      provisionalRecoveryLedger ∧
    ∀ slot ∈ provisionalRecoveryLedger,
      ∃ s : RecoveryStage,
        (slot, s) ∈ provisionalRecoveryLedgerStageWitnesses ∧
        slot ∈ stageImportSlots s := by
  refine ⟨by decide, rfl, ?_⟩
  intro slot _
  cases slot with
  | NONCOMM => exact ⟨.LiftHost, by decide, by decide⟩
  | UNITARY => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | CLONE => exact ⟨.Ops, by decide, by decide⟩
  | CONT_TIME => exact ⟨.Ops, by decide, by decide⟩
  | HERM => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | L2_READOUT => exact ⟨.Surplus, by decide, by decide⟩
  | BORN => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | BUNDLE_U1_LT => exact ⟨.SpectralBornCompose, by decide, by decide⟩

/-! ## Coverage and ledger-aware erase stability -/

/-- Every provisional recovery-ledger slot occurs in at least one stage import list. -/
theorem provisional_recovery_ledger_stage_import_coverage :
    ∀ slot ∈ provisionalRecoveryLedger,
      ∃ s : RecoveryStage, slot ∈ stageImportSlots s := by
  intro slot hslot
  obtain ⟨s, _, hs⟩ :=
    provisional_recovery_ledger_stage_witnesses_exhaustive.2.2 slot hslot
  exact ⟨s, hs⟩

/--
T3L-2 restated on the audited map: erasing any provisional B8 slot leaves a
witness stage that both cites the slot and fails ledger-aware discharge.
-/
theorem stage_import_map_stable_under_ledger_aware_erase
    (slot : RecoveryImportSlot) :
    ∃ s : RecoveryStage,
      slot ∈ stageImportSlots s ∧
      stagePathwayDischargedLedger partialPackage
        (provisionalRecoveryLedger.erase slot) s = false :=
  drop_import_breaks_some_ledger_aware_stage slot

end FiniteMatrixRecovery
end QM

#print axioms QM.FiniteMatrixRecovery.provisional_recovery_ledger_stage_witnesses_exhaustive
#print axioms QM.FiniteMatrixRecovery.provisional_recovery_ledger_stage_import_coverage
#print axioms QM.FiniteMatrixRecovery.stage_import_map_stable_under_ledger_aware_erase
