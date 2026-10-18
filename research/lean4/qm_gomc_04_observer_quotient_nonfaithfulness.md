/-!
GOMC-04: observer-quotient nonfaithfulness.

This is the generic LGGR shape behind residual density, coarse-graining, and
orientation-blind diagnostics. If a local observer map identifies two states
while a hidden/global coordinate separates them, the joint readout cannot factor
through the local observer.
-/

namespace QM

namespace GOMC04

def FactorsThrough {α β γ : Type}
    (observer : α -> β) (readout : α -> γ) : Prop :=
  ∀ ⦃x y : α⦄, observer x = observer y -> readout x = readout y

theorem observer_factors_through_itself
    {α β : Type} (observer : α -> β) :
    FactorsThrough observer observer := by
  intro x y h
  exact h

theorem joint_not_factor_of_hidden_separation
    {α β γ : Type}
    (observer : α -> β) (hidden : α -> γ)
    (x y : α)
    (hLocal : observer x = observer y)
    (hHidden : hidden x ≠ hidden y) :
    ¬ FactorsThrough observer (fun z => (observer z, hidden z)) := by
  intro h
  have hJoint := h hLocal
  exact hHidden (congrArg Prod.snd hJoint)

inductive TwoState where
  | left
  | right
deriving DecidableEq, Repr

def localGreen (_ : TwoState) : Bool := true

def hiddenRed : TwoState -> Bool
  | TwoState.left => false
  | TwoState.right => true

theorem localGreen_not_injective :
    ¬ Function.Injective localGreen := by
  intro h
  have hState : TwoState.left = TwoState.right := h rfl
  cases hState

theorem localGreen_factors :
    FactorsThrough localGreen localGreen := by
  exact observer_factors_through_itself localGreen

theorem localGreen_jointRed_not_factors :
    ¬ FactorsThrough localGreen
      (fun z => (localGreen z, hiddenRed z)) := by
  exact joint_not_factor_of_hidden_separation
    localGreen hiddenRed TwoState.left TwoState.right rfl (by decide)

theorem observerQuotient_nonfaithful_witness :
    (¬ Function.Injective localGreen) ∧
      FactorsThrough localGreen localGreen ∧
      ¬ FactorsThrough localGreen
        (fun z => (localGreen z, hiddenRed z)) := by
  exact ⟨localGreen_not_injective, localGreen_factors,
    localGreen_jointRed_not_factors⟩

end GOMC04

end QM

#print axioms QM.GOMC04.observer_factors_through_itself
#print axioms QM.GOMC04.joint_not_factor_of_hidden_separation
#print axioms QM.GOMC04.observerQuotient_nonfaithful_witness
