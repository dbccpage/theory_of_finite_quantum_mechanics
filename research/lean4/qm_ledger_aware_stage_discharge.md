import «fin_qm_shadow_complete»
import «qm_import_independence»

/-!
# QMLedgerAwareStageDischarge — W7.1 T3-ledger successor

This module adds the frozen ledger-aware successor to the legacy recovery-stage
evaluator.  The legacy #1755 counterexample remains imported and is restated as
a regression fence: package pathway flags alone still ignore a dropped import.

The W6.19 dual below is explicitly provisional and registry-relative to the
current eight-slot basis.  Ledger-aware pathway discharge is still a Boolean
checklist theorem, not sealed finite matrix recovery.

AuthorityEffect: None.  No recovery seal or Wave-7 exit is changed.
-/

namespace QM
namespace FiniteMatrixRecovery

/-! ## Frozen ledger-aware evaluator (D1–D4) -/

/-- Boolean membership in the declared recovery-import ledger. -/
def ledgerHas (ledger : List RecoveryImportSlot) (slot : RecoveryImportSlot) : Bool :=
  decide (slot ∈ ledger)

/--
A stage is ledger-aware discharged exactly when its legacy component pathway is
discharged and every slot named by the frozen stage-to-import map is present.
-/
def stagePathwayDischargedLedger
    (pkg : RecoveryPackage)
    (ledger : List RecoveryImportSlot)
    (s : RecoveryStage) : Bool :=
  stagePathwayDischarged pkg s &&
    (stageImportSlots s).all (fun slot => ledgerHas ledger slot)

/-- The frozen conjunction of all five ledger-aware recovery stages. -/
def allFiveStagesDischargedLedger
    (pkg : RecoveryPackage) (ledger : List RecoveryImportSlot) : Prop :=
  stagePathwayDischargedLedger pkg ledger .ClassicalShadow = true ∧
  stagePathwayDischargedLedger pkg ledger .Surplus = true ∧
  stagePathwayDischargedLedger pkg ledger .LiftHost = true ∧
  stagePathwayDischargedLedger pkg ledger .SpectralBornCompose = true ∧
  stagePathwayDischargedLedger pkg ledger .Ops = true

/-! ## T3L-0 — immutable legacy #1755 regression fence -/

/--
Dropping any slot still leaves the legacy, ledger-blind evaluator all-five true.
This is a direct restatement of the imported #1755 counterexample.
-/
theorem legacy_drop_one_still_all_five_stages (slot : RecoveryImportSlot) :
    (provisionalRecoveryLedger.erase slot).length = 7 ∧
    FinQMShadowComplete.allFiveStagesDischarged partialPackage := by
  simpa [FinQMShadowComplete.dropFullOpsImport, FinQMShadowComplete.fullOpsV0] using
    FinQMShadowComplete.t3_open_counterexample_drop_each_import_still_all_five slot

/-! ## T3L-1 — full B8 discharges the ledger-aware stage conjunction -/

theorem full_ops_ledger_aware_all_five :
    allFiveStagesDischargedLedger partialPackage provisionalRecoveryLedger := by
  unfold allFiveStagesDischargedLedger
  decide

/-! ## T3L-2 — drop-one necessity relative to the frozen stage map -/

theorem drop_import_breaks_some_ledger_aware_stage (slot : RecoveryImportSlot) :
    ∃ s : RecoveryStage,
      slot ∈ stageImportSlots s ∧
      stagePathwayDischargedLedger partialPackage
        (provisionalRecoveryLedger.erase slot) s = false := by
  cases slot with
  | NONCOMM => exact ⟨.LiftHost, by decide, by decide⟩
  | UNITARY => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | CLONE => exact ⟨.Ops, by decide, by decide⟩
  | CONT_TIME => exact ⟨.Ops, by decide, by decide⟩
  | HERM => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | L2_READOUT => exact ⟨.Surplus, by decide, by decide⟩
  | BORN => exact ⟨.SpectralBornCompose, by decide, by decide⟩
  | BUNDLE_U1_LT => exact ⟨.SpectralBornCompose, by decide, by decide⟩

/-! ## T3L-3 — provisional W6.19 registry-relative dual -/

/-- Explicit conversion from the W6.19 provisional B8 registry to this module's B8. -/
def recoverySlotOfIndependenceSlot :
    ImportIndependence.ImportSlot → RecoveryImportSlot
  | .OB_NONCOMM => .NONCOMM
  | .OB_UNITARY => .UNITARY
  | .OB_CLONE => .CLONE
  | .CONT_TIME => .CONT_TIME
  | .OB_HERM => .HERM
  | .OB_L2_READOUT => .L2_READOUT
  | .OB_BORN => .BORN
  | .BUNDLE_U1_LT => .BUNDLE_U1_LT

/--
Ledger induced by a W6.19 independence model: retain exactly the admitted
columns and convert their slot labels into the recovery-stage registry.
-/
def recoveryLedgerOfIndependenceModel
    (model : ImportIndependence.IndependenceModel) : List RecoveryImportSlot :=
  ImportIndependence.workingBasisB8.filterMap (fun slot =>
    if ImportIndependence.admits model slot then
      some (recoverySlotOfIndependenceSlot slot)
    else
      none)

/-- Each W6.19 drop row induces exactly the corresponding seven-slot ledger. -/
theorem drop_model_induces_drop_one_recovery_ledger
    (slot : ImportIndependence.ImportSlot) :
    recoveryLedgerOfIndependenceModel (ImportIndependence.modelRow slot) =
      provisionalRecoveryLedger.erase (recoverySlotOfIndependenceSlot slot) := by
  cases slot <;> decide

/--
T3L-3 (provisional / registry-relative): every W6.19 drop-model row induces a
ledger that fails a recovery stage requiring the dropped column.  This does
not adjudicate the provisional B8 registry as the final import basis.
-/
theorem independence_drop_model_breaks_some_ledger_aware_stage_provisional
    (slot : ImportIndependence.ImportSlot) :
    ∃ s : RecoveryStage,
      recoverySlotOfIndependenceSlot slot ∈ stageImportSlots s ∧
      stagePathwayDischargedLedger partialPackage
        (recoveryLedgerOfIndependenceModel (ImportIndependence.modelRow slot)) s = false := by
  rw [drop_model_induces_drop_one_recovery_ledger]
  exact drop_import_breaks_some_ledger_aware_stage
    (recoverySlotOfIndependenceSlot slot)

/-! ## T3L-4 — pure FinL1 remains classical-only -/

theorem pure_finl1_ledger_aware_refuses_nonclassical :
    stagePathwayDischargedLedger pureFinL1Package [] .ClassicalShadow = true ∧
    stagePathwayDischargedLedger pureFinL1Package [] .Surplus = false ∧
    stagePathwayDischargedLedger pureFinL1Package [] .LiftHost = false ∧
    stagePathwayDischargedLedger pureFinL1Package [] .SpectralBornCompose = false ∧
    stagePathwayDischargedLedger pureFinL1Package [] .Ops = false := by
  decide

/-! ## T3L-5 — exact admission remains distinct from stage discharge -/

theorem drop_import_refuses_full_ops_v0_admission (slot : RecoveryImportSlot) :
    ¬ FinQMShadowComplete.FullOpsV0Admitted
      (FinQMShadowComplete.dropFullOpsImport slot) :=
  FinQMShadowComplete.drop_import_refuses_full_ops_v0_admission slot

/-- Clearly labeled T3L-5 alias preserving the admission-versus-stage split. -/
theorem t3l5_drop_import_refuses_full_ops_v0_admission
    (slot : RecoveryImportSlot) :
    ¬ FinQMShadowComplete.FullOpsV0Admitted
      (FinQMShadowComplete.dropFullOpsImport slot) :=
  drop_import_refuses_full_ops_v0_admission slot

/-! ## Seal and authority firewalls -/

/-- Ledger-aware T3 closes no recovery seal and claims no Wave-7 exit. -/
theorem ledger_aware_stage_discharge_seal_firewall :
    sealedRecoveryClosed = false ∧
    sealedFullMatrixRecovery = false ∧
    fullMatrixRecovery_closed = false ∧
    wave7Exit_claimed = false ∧
    sealMayAutoFlipFromPackage = false := by
  decide

/-- This scoped ledger theorem has no authorization effect. -/
theorem ledger_aware_stage_discharge_authority_effect_none (C : Type) :
    ¬ IsAuth C :=
  structure_not_auth C

end FiniteMatrixRecovery
end QM

#print axioms QM.FiniteMatrixRecovery.legacy_drop_one_still_all_five_stages
#print axioms QM.FiniteMatrixRecovery.full_ops_ledger_aware_all_five
#print axioms QM.FiniteMatrixRecovery.drop_import_breaks_some_ledger_aware_stage
#print axioms QM.FiniteMatrixRecovery.drop_model_induces_drop_one_recovery_ledger
#print axioms QM.FiniteMatrixRecovery.independence_drop_model_breaks_some_ledger_aware_stage_provisional
#print axioms QM.FiniteMatrixRecovery.pure_finl1_ledger_aware_refuses_nonclassical
#print axioms QM.FiniteMatrixRecovery.drop_import_refuses_full_ops_v0_admission
#print axioms QM.FiniteMatrixRecovery.t3l5_drop_import_refuses_full_ops_v0_admission
#print axioms QM.FiniteMatrixRecovery.ledger_aware_stage_discharge_seal_firewall
#print axioms QM.FiniteMatrixRecovery.ledger_aware_stage_discharge_authority_effect_none
