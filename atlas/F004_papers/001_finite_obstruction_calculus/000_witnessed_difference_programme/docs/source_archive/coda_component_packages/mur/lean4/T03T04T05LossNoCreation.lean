import D01D02D03Records

/-!
Lean 4 proof kernels for GTMUR-T03, GTMUR-T04, and GTMUR-T05.

AuthorityEffect: None.

T03 and T05 are encoded as conditional authority-transport rules:
lossy transport requires a ledger, and lossy transport cannot be the sole
source of target authority under the stated no-third-source hypothesis.

T04 is represented by a finite Boolean loss ledger. This captures the
structural accumulation law and its unit/associativity properties. Richer
paper-level components such as equivalence closure and approximation
composition remain semantic refinements of this kernel.
-/

namespace CODA_MUR

/-- Minimal transport evidence relevant to loss-ledger necessity. -/
structure TransportEvidence where
  kind : MorphismKind
  lossDefined : Prop
  chiExists : Prop

/-- Loss accounting admissibility requires every lossy move to define a loss ledger. -/
def LossAccountingAdmissible (F : TransportEvidence) : Prop :=
  LossRequired F.kind -> F.lossDefined

/-- Backward-compatible alias for policy predicate. -/
def AuthorityPreserving := LossAccountingAdmissible

/-- MUR-T7: if loss is required but missing, the move is not loss-accounting admissible. -/
theorem loss_accounting_admissible_necessity
    (F : TransportEvidence)
    (hLossy : LossRequired F.kind)
    (hMissing : ¬ F.lossDefined) :
    ¬ LossAccountingAdmissible F := by
  intro hAdmiss
  exact hMissing (hAdmiss hLossy)

/-- Backward-compatible alias for MUR-T7. -/
abbrev loss_ledger_necessity := loss_accounting_admissible_necessity

/-- Concrete quotient case of MUR-T7. -/
theorem quotient_without_ledger_not_loss_accounting_admissible
    (chi : Prop) :
    ¬ LossAccountingAdmissible
      { kind := MorphismKind.quotient, lossDefined := False, chiExists := chi } := by
  exact loss_accounting_admissible_necessity _ quotient_loss_required (by intro h; exact h)

/-- Backward-compatible alias for quotient case. -/
abbrev quotient_without_ledger_not_authority_preserving := quotient_without_ledger_not_loss_accounting_admissible

theorem bool_or_assoc (a b c : Bool) : (a || b) || c = a || (b || c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem bool_false_or (a : Bool) : false || a = a := by
  cases a <;> rfl

theorem bool_or_false (a : Bool) : a || false = a := by
  cases a <;> rfl

/-- T04 finite-ledger associativity. -/
theorem loss_sum_assoc (L M N : LossLedger) :
    (L.sum M).sum N = L.sum (M.sum N) := by
  cases L with
  | mk Le Li La Lu =>
    cases M with
    | mk Me Mi Ma Mu =>
      cases N with
      | mk Ne Ni Na Nu =>
        cases Le <;> cases Li <;> cases La <;> cases Lu <;>
        cases Me <;> cases Mi <;> cases Ma <;> cases Mu <;>
        cases Ne <;> cases Ni <;> cases Na <;> cases Nu <;> rfl

/-- T04 empty ledger is a left unit. -/
theorem loss_sum_left_unit (L : LossLedger) :
    LossLedger.empty.sum L = L := by
  cases L with
  | mk e i a u =>
    cases e <;> cases i <;> cases a <;> cases u <;> rfl

/-- T04 empty ledger is a right unit. -/
theorem loss_sum_right_unit (L : LossLedger) :
    L.sum LossLedger.empty = L := by
  cases L with
  | mk e i a u =>
    cases e <;> cases i <;> cases a <;> cases u <;> rfl

/-- Composite loss ledger: push forward earlier loss, then accumulate later loss. -/
def composeLoss (push : LossLedger -> LossLedger)
    (lossF lossG : LossLedger) : LossLedger :=
  (push lossF).sum lossG

/-- GTMUR-T04 formula in the finite Boolean ledger kernel. -/
theorem loss_composition_formula
    (push : LossLedger -> LossLedger)
    (lossF lossG : LossLedger) :
    composeLoss push lossF lossG = (push lossF).sum lossG :=
  rfl

/-- Pushforward distributes over finite-ledger sum when declared so. -/
def PushDistributes (push : LossLedger -> LossLedger) : Prop :=
  ∀ L M, push (L.sum M) = (push L).sum (push M)

/-- Pushforward preserves empty ledger when declared so. -/
def PushPreservesEmpty (push : LossLedger -> LossLedger) : Prop :=
  push LossLedger.empty = LossLedger.empty

/-- Identity composition law for ledger transport. -/
theorem loss_identity_left
    (push : LossLedger -> LossLedger)
    (hEmpty : PushPreservesEmpty push)
    (lossF : LossLedger) :
    composeLoss push LossLedger.empty lossF = lossF := by
  unfold composeLoss
  rw [hEmpty]
  exact loss_sum_left_unit lossF

/-- Associativity of three-step Boolean loss accumulation under declared push laws. -/
theorem loss_chain_assoc
    (pushH pushG pushHG : LossLedger -> LossLedger)
    (hComp : ∀ L, pushH (pushG L) = pushHG L)
    (hDistrib : PushDistributes pushH)
    (lossF lossG lossH : LossLedger) :
    composeLoss pushH (composeLoss pushG lossF lossG) lossH =
      (pushHG lossF).sum ((pushH lossG).sum lossH) := by
  unfold composeLoss
  rw [hDistrib]
  rw [hComp]
  exact loss_sum_assoc (pushHG lossF) (pushH lossG) lossH

/-- Minimal no-creation context for lossy morphisms. -/
structure NoCreationContext where
  targetAuthority : Prop
  freshDescent : Prop
  certifiedPreimage : Prop
  noThirdAuthoritySource :
    targetAuthority -> freshDescent ∨ certifiedPreimage

/-- GTMUR-T05: under the exhaustiveness hypothesis, lossy transport cannot be the sole source. -/
theorem lossy_no_creation
    (C : NoCreationContext)
    (hAuthority : C.targetAuthority) :
    C.freshDescent ∨ C.certifiedPreimage :=
  C.noThirdAuthoritySource hAuthority

/-- Authority-by-collapse is refused when neither permitted source is present. -/
theorem authority_by_collapse_refused
    (C : NoCreationContext)
    (hAuthority : C.targetAuthority)
    (hNoFresh : ¬ C.freshDescent)
    (hNoPreimage : ¬ C.certifiedPreimage) :
    False := by
  cases C.noThirdAuthoritySource hAuthority with
  | inl hFresh => exact hNoFresh hFresh
  | inr hPreimage => exact hNoPreimage hPreimage

end CODA_MUR

#print axioms CODA_MUR.loss_ledger_necessity
#print axioms CODA_MUR.quotient_without_ledger_not_authority_preserving
#print axioms CODA_MUR.loss_sum_assoc
#print axioms CODA_MUR.loss_sum_left_unit
#print axioms CODA_MUR.loss_sum_right_unit
#print axioms CODA_MUR.loss_composition_formula
#print axioms CODA_MUR.loss_identity_left
#print axioms CODA_MUR.loss_chain_assoc
#print axioms CODA_MUR.lossy_no_creation
#print axioms CODA_MUR.authority_by_collapse_refused
