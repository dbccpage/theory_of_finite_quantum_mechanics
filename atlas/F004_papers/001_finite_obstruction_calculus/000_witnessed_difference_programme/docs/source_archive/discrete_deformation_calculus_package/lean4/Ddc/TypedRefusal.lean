/-
Letter M: typed refusal. AuthorityEffect: None.
-/
import Ddc.Law

namespace Ddc

/-- DDC-M-01: a refusal leaves the state unchanged and names a reason. -/
theorem M_preserves_state (b a : State) (w : Witness) (h : stepLaw .M b a w = true) :
    a = b ∧ w.reason.isSome = true := law_M.1 h

/-- A refusal moves the tape into the refused control state. -/
theorem M_refuses (c : Control) : nextCtrl c .M = .refused := by
  cases c <;> rfl

end Ddc
