/-
Step laws, control laws and the tape runner. Mirrors `code/ddc/automaton.py`.
AuthorityEffect: None.
-/
import Ddc.Basic

namespace Ddc

/-- The paper's step law. -/
def stepLaw : Letter → State → State → Witness → Bool
  | .E, b, a, _ =>
      b.carrier == a.carrier && b.cls == .exact && a.phi == 0 && a.gamma == 0 &&
        a.residual.all (· == 0) && b.adequate
  | .R, b, a, _ => b.carrier == a.carrier && a.phi == b.phi && a.gamma == b.gamma && b.adequate
  | .C, b, a, _ => b.carrier != a.carrier && decide (b.phi ≤ a.phi) && decide (b.gamma ≤ a.gamma)
  | .I, b, a, w => a == b && w.receipt
  | .L, b, a, w => b.carrier != a.carrier && w.licence && (b.cls == .closed || !b.adequate)
  | .D, b, a, w => b.carrier != a.carrier && w.ledger
  | .M, b, a, w => a == b && w.reason.isSome
  | .T, b, a, _ => a == b && a.gamma == 0 && b.adequate

/-- The engine's `op_verification::verify_step`, on the same abstract state. -/
def engineLaw : Letter → State → State → Bool
  | .E, b, a => b.carrier == a.carrier && a.phi == 0 && a.gamma == 0
  | .R, b, a => b.carrier == a.carrier && a.phi == b.phi
  | .I, b, a => a == b
  | .M, b, a => a == b
  | .T, b, a => a == b && a.gamma == 0
  | .C, b, a => b.carrier != a.carrier
  | .D, b, a => b.carrier != a.carrier
  | .L, b, a => b.carrier != a.carrier

/-- Law 2 (T absorbs) and Law 3 (after M only C, Λ or T). -/
def ctrlOk : Control → Letter → Bool
  | .terminalized, _ => false
  | .refused, l => l == .C || l == .L || l == .T
  | .ongoing, _ => true

def nextCtrl : Control → Letter → Control
  | _, .T => .terminalized
  | _, .M => .refused
  | .refused, _ => .ongoing
  | c, _ => c

/-- Replay a tape; `none` at the first unlawful step. -/
def run : Control → State → List Step → Option (Control × State)
  | c, s, [] => some (c, s)
  | c, s, st :: rest =>
      if ctrlOk c st.letter && stepLaw st.letter s st.after st.witness then
        run (nextCtrl c st.letter) st.after rest
      else none

def Lawful (c : Control) (s : State) (t : List Step) : Prop := (run c s t).isSome = true

def mkReceipt (i : Nat) (b : State) (st : Step) : StepReceipt :=
  ⟨i, st.letter, b, st.after, .none⟩

/-- The receipts a replay emits, one per lawful step. -/
def receipts : Nat → Control → State → List Step → List StepReceipt
  | _, _, _, [] => []
  | i, c, s, st :: rest =>
      if ctrlOk c st.letter && stepLaw st.letter s st.after st.witness then
        mkReceipt i s st :: receipts (i + 1) (nextCtrl c st.letter) st.after rest
      else []

/-- The §23 driver: letters a state may propose. -/
def driverLetters (s : State) : List Letter :=
  if s.adequate then
    match s.cls with
    | .exact => [.E, .T, .I]
    | .closed => [.R, .L, .T, .I]
    | .active => [.R, .C, .D, .M, .I]
  else [.L, .M, .C, .I]

end Ddc

/-! ## Each step law as a plain conjunction -/

namespace Ddc

variable {b a : State} {w : Witness}

theorem law_E : stepLaw .E b a w = true ↔
    b.carrier = a.carrier ∧ b.cls = .exact ∧ a.phi = 0 ∧ a.gamma = 0 ∧
      (∀ x ∈ a.residual, x = 0) ∧ b.adequate = true := by
  simp [stepLaw, and_assoc]

theorem law_R : stepLaw .R b a w = true ↔
    b.carrier = a.carrier ∧ a.phi = b.phi ∧ a.gamma = b.gamma ∧ b.adequate = true := by
  simp [stepLaw, and_assoc]

theorem law_C : stepLaw .C b a w = true ↔ b.carrier ≠ a.carrier ∧ b.phi ≤ a.phi ∧ b.gamma ≤ a.gamma := by
  simp [stepLaw, and_assoc]

theorem law_I : stepLaw .I b a w = true ↔ a = b ∧ w.receipt = true := by
  simp [stepLaw]

theorem law_L : stepLaw .L b a w = true ↔
    b.carrier ≠ a.carrier ∧ w.licence = true ∧ (b.cls = .closed ∨ b.adequate = false) := by
  simp [stepLaw, and_assoc]

theorem law_D : stepLaw .D b a w = true ↔ b.carrier ≠ a.carrier ∧ w.ledger = true := by
  simp [stepLaw]

theorem law_M : stepLaw .M b a w = true ↔ a = b ∧ w.reason.isSome = true := by
  simp [stepLaw]

theorem law_T : stepLaw .T b a w = true ↔ a = b ∧ a.gamma = 0 ∧ b.adequate = true := by
  simp [stepLaw, and_assoc]

end Ddc
