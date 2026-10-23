/-
Discrete Deformation Calculus — basic objects.

A state is modelled by a carrier identifier, a residual cochain and two
diagnostics. The laws use only equality, order and zero tests on Φ₁ and Γ₂,
so natural numbers stand in for the non-negative rationals of the Python
reference (`code/ddc/automaton.py`). AuthorityEffect: None.
-/

namespace Ddc

/-- The eight letters. `L` is Λ (structural lift). -/
inductive Letter where
  | E | R | C | I | L | D | M | T
  deriving DecidableEq, Repr

/-- FOC classes of a measured state. -/
inductive Cls where
  | exact | closed | active
  deriving DecidableEq, Repr

structure State where
  carrier  : Nat
  residual : List Int
  phi      : Nat
  gamma    : Nat
  adequate : Bool
  deriving DecidableEq, Repr

/-- Γ₂ > 0 dominates; otherwise Φ₁ = 0 is exact and Φ₁ > 0 is a closed residual. -/
def State.cls (s : State) : Cls :=
  if s.gamma = 0 then (if s.phi = 0 then .exact else .closed) else .active

/-- In-trace refusal reasons carried by `M` (the closed vocabulary). -/
inductive Reason where
  | invalidWitness | budgetExhausted | nonZeroCurl | unlicensedLift | liftTrigger
  | missingLossLedger | missingReceipt | requiresLift | detectorInadequate | openObstruction
  deriving DecidableEq, Repr

/-- Intake refusals: recorded before admission, never on the tape. -/
inductive IntakeReason where
  | untyped | ungroundedLocus | adapterInadequate
  deriving DecidableEq, Repr

structure Witness where
  receipt : Bool
  ledger  : Bool
  licence : Bool
  reason  : Option Reason
  deriving DecidableEq, Repr

/-- Control state of a tape. `ongoing` is the Python `Open`. -/
inductive Control where
  | ongoing | refused | terminalized
  deriving DecidableEq, Repr

structure Step where
  letter  : Letter
  after   : State
  witness : Witness
  deriving DecidableEq, Repr

/-- Two values so that `authority_effect_none` is not vacuous. -/
inductive AuthorityEffect where
  | none | granted
  deriving DecidableEq, Repr

structure StepReceipt where
  index     : Nat
  letter    : Letter
  before    : State
  after     : State
  authority : AuthorityEffect
  deriving DecidableEq, Repr

theorem cls_exact_iff (s : State) : s.cls = .exact ↔ s.gamma = 0 ∧ s.phi = 0 := by
  unfold State.cls
  by_cases hg : s.gamma = 0 <;> by_cases hp : s.phi = 0 <;> simp [hg, hp]

theorem cls_closed_iff (s : State) : s.cls = .closed ↔ s.gamma = 0 ∧ s.phi ≠ 0 := by
  unfold State.cls
  by_cases hg : s.gamma = 0 <;> by_cases hp : s.phi = 0 <;> simp [hg, hp]

theorem cls_active_iff (s : State) : s.cls = .active ↔ s.gamma ≠ 0 := by
  unfold State.cls
  by_cases hg : s.gamma = 0 <;> by_cases hp : s.phi = 0 <;> simp [hg, hp]

end Ddc
