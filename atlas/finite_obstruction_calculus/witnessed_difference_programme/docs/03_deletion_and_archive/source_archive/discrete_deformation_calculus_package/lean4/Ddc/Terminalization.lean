/-
Letter T: terminalization under the nine CanContinue conjuncts. AuthorityEffect: None.
-/
import Ddc.Theorems

namespace Ddc

/-- The nine conjuncts named by `oeprmalg2::CONTINUATION_CONJUNCTS`. -/
structure ContinuationFacts where
  outstandingObligation : Bool
  higherObligationWitness : Bool
  nextCarrierDeclared : Bool
  adapterSound : Bool
  detectorAdequate : Bool
  minimalLicensedLift : Bool
  skeletonPreserved : Bool
  budgetAvailable : Bool
  noGtlaRefusal : Bool
  deriving DecidableEq, Repr

def canContinue (f : ContinuationFacts) : Bool :=
  f.outstandingObligation && f.higherObligationWitness && f.nextCarrierDeclared &&
    f.adapterSound && f.detectorAdequate && f.minimalLicensedLift && f.skeletonPreserved &&
    f.budgetAvailable && f.noGtlaRefusal

/-- CanContinue_n holds exactly when all nine conjuncts hold. -/
theorem canContinue_iff (f : ContinuationFacts) :
    canContinue f = true ↔
      f.outstandingObligation = true ∧ f.higherObligationWitness = true ∧
      f.nextCarrierDeclared = true ∧ f.adapterSound = true ∧ f.detectorAdequate = true ∧
      f.minimalLicensedLift = true ∧ f.skeletonPreserved = true ∧ f.budgetAvailable = true ∧
      f.noGtlaRefusal = true := by
  simp [canContinue, and_assoc]

/-- DDC-T: T never seals an open obstruction and never seals on a blind detector. -/
theorem T_never_seals_open (b a : State) (w : Witness) (h : stepLaw .T b a w = true) :
    a.gamma = 0 ∧ b.adequate = true ∧ a = b := by
  obtain ⟨hab, hg, ha⟩ := law_T.1 h
  exact ⟨hg, ha, hab⟩

/-- A lawful T lands on the CheckPassed route (exact) or the residual route (closed). -/
theorem T_routing (b a : State) (w : Witness) (h : stepLaw .T b a w = true) :
    a.cls = .exact ∨ a.cls = .closed := by
  obtain ⟨-, hg, -⟩ := law_T.1 h
  by_cases hp : a.phi = 0
  · exact Or.inl ((cls_exact_iff a).2 ⟨hg, hp⟩)
  · exact Or.inr ((cls_closed_iff a).2 ⟨hg, hp⟩)

/-- DDC-T-04: after T nothing more is admitted. -/
theorem T_seals (c : Control) : nextCtrl c .T = .terminalized := by
  cases c <;> rfl

end Ddc
