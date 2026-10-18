import «gomc_04_observer_quotient_nonfaithfulness»

/-!
GOMC-07: LGGR composition theorem.

Two observer fragments can each be locally green, and their visible pair can
also be locally green, while a hidden/global glue coordinate still separates
the underlying states. Composition of local diagnostics therefore does not
remove the global-red obstruction.
-/

namespace QM

namespace GOMC07

def PairObserver {α β γ : Type}
    (left : α -> β) (right : α -> γ) : α -> β × γ :=
  fun x => (left x, right x)

def AugmentedJoint {α β γ δ : Type}
    (left : α -> β) (right : α -> γ) (hidden : α -> δ) :
    α -> (β × γ) × δ :=
  fun x => (PairObserver left right x, hidden x)

theorem pairObserver_eq_of_local_eq
    {α β γ : Type}
    (left : α -> β) (right : α -> γ)
    {x y : α}
    (hLeft : left x = left y)
    (hRight : right x = right y) :
    PairObserver left right x = PairObserver left right y := by
  exact Prod.ext hLeft hRight

theorem composedLocalGreen_globalRed
    {α β γ δ : Type}
    (left : α -> β) (right : α -> γ) (hidden : α -> δ)
    (x y : α)
    (hLeft : left x = left y)
    (hRight : right x = right y)
    (hHidden : hidden x ≠ hidden y) :
    PairObserver left right x = PairObserver left right y ∧
      ¬ GOMC04.FactorsThrough (PairObserver left right)
        (AugmentedJoint left right hidden) := by
  have hPair : PairObserver left right x = PairObserver left right y :=
    pairObserver_eq_of_local_eq left right hLeft hRight
  exact ⟨hPair,
    GOMC04.joint_not_factor_of_hidden_separation
      (PairObserver left right) hidden x y hPair hHidden⟩

inductive FragmentState where
  | leftState
  | rightState
deriving DecidableEq, Repr

def localFragmentA (_ : FragmentState) : Bool := true

def localFragmentB (_ : FragmentState) : Bool := true

def hiddenGlue : FragmentState -> Bool
  | FragmentState.leftState => false
  | FragmentState.rightState => true

theorem localFragments_compose_green :
    PairObserver localFragmentA localFragmentB FragmentState.leftState =
      PairObserver localFragmentA localFragmentB FragmentState.rightState := by
  rfl

theorem hiddenGlue_global_red :
    hiddenGlue FragmentState.leftState ≠ hiddenGlue FragmentState.rightState := by
  decide

theorem locallyGreenFragments_globallyRed_witness :
    PairObserver localFragmentA localFragmentB FragmentState.leftState =
        PairObserver localFragmentA localFragmentB FragmentState.rightState ∧
      ¬ GOMC04.FactorsThrough (PairObserver localFragmentA localFragmentB)
        (AugmentedJoint localFragmentA localFragmentB hiddenGlue) := by
  exact composedLocalGreen_globalRed
    localFragmentA localFragmentB hiddenGlue
    FragmentState.leftState FragmentState.rightState rfl rfl hiddenGlue_global_red

end GOMC07

end QM

#print axioms QM.GOMC07.pairObserver_eq_of_local_eq
#print axioms QM.GOMC07.composedLocalGreen_globalRed
#print axioms QM.GOMC07.locallyGreenFragments_globallyRed_witness
