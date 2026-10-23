import WitnessedDifference.Difference

/-!
# Retention and observer layers

Presentation, memory, and evaluation are separate declared structures. An
evaluator verdict is not an authority grant.
-/

namespace WitnessedDifference

structure Retention (State Mark : Type _) where
  encode : State → Mark
  «recall» : Mark → State
  encode_recall : ∀ mark, encode («recall» mark) = mark

namespace Retention

def retain {State Mark : Type _} (R : Retention State Mark) : State → State :=
  fun state => R.recall (R.encode state)

@[simp] theorem encode_retain {State Mark : Type _}
    (R : Retention State Mark) (state : State) :
    R.encode (R.retain state) = R.encode state := by
  unfold retain
  rw [R.encode_recall]

@[simp] theorem retain_idempotent {State Mark : Type _}
    (R : Retention State Mark) (state : State) :
    R.retain (R.retain state) = R.retain state := by
  unfold retain
  rw [R.encode_recall]

end Retention

structure Presentation (World Report : Type _) where
  present : World → Report

structure Memory (Report Trace : Type _) where
  store : Report → Trace
  retrieve : Trace → Option Report
  retrieve_store : ∀ report, retrieve (store report) = some report

structure Evaluator (Report Verdict : Type _) where
  evaluate : Report → Verdict
  accepts : Verdict → Bool

structure ObserverPacket
    (World Report Trace Verdict : Type _) where
  presentation : Presentation World Report
  memory : Memory Report Trace
  evaluator : Evaluator Report Verdict

namespace ObserverPacket

def report {World Report Trace Verdict : Type _}
    (O : ObserverPacket World Report Trace Verdict) : World → Report :=
  O.presentation.present

@[simp] theorem report_reaccessible
    {World Report Trace Verdict : Type _}
    (O : ObserverPacket World Report Trace Verdict) (world : World) :
    O.memory.retrieve (O.memory.store (O.report world)) =
      some (O.report world) := by
  exact O.memory.retrieve_store (O.report world)

end ObserverPacket

inductive EvaluationStatus where
  | accept
  | refuse
  | reject
  deriving DecidableEq, Repr

/-!
`ObservationReceipt` records whatever status the evaluator returned. The type
does not silently turn refusal or rejection into acceptance.
-/
structure ObservationReceipt (World Report Trace : Type _) where
  observer : ObserverPacket World Report Trace EvaluationStatus
  world : World
  report : Report
  trace : Trace
  status : EvaluationStatus
  report_eq : report = observer.report world
  trace_eq : trace = observer.memory.store report
  status_eq : status = observer.evaluator.evaluate report

namespace ObservationReceipt

@[simp] theorem report_reaccessible
    {World Report Trace : Type _}
    (receipt : ObservationReceipt World Report Trace) :
    receipt.observer.memory.retrieve receipt.trace = some receipt.report := by
  rw [receipt.trace_eq]
  exact receipt.observer.memory.retrieve_store receipt.report

end ObservationReceipt

/-!
An accepted observation is a general receipt plus evidence that its actual
evaluator result is `accept`. This proof field prevents refusal and rejection
receipts from inhabiting the type.
-/
structure AcceptedObservation (World Report Trace : Type _) where
  receipt : ObservationReceipt World Report Trace
  accepted : receipt.status = .accept

namespace AcceptedObservation

theorem status_ne_refuse
    {World Report Trace : Type _}
    (observation : AcceptedObservation World Report Trace) :
    observation.receipt.status ≠ .refuse := by
  rw [observation.accepted]
  simp

theorem status_ne_reject
    {World Report Trace : Type _}
    (observation : AcceptedObservation World Report Trace) :
    observation.receipt.status ≠ .reject := by
  rw [observation.accepted]
  simp

end AcceptedObservation

structure AuthorityPolicy (Report : Type _) where
  authorized : Report → Prop

def AcceptedBy {Report Verdict : Type _}
    (E : Evaluator Report Verdict) (report : Report) : Prop :=
  E.accepts (E.evaluate report) = true

def acceptingUnitEvaluator : Evaluator Unit Bool where
  evaluate := fun _ => true
  accepts := fun verdict => verdict

def denyingUnitAuthority : AuthorityPolicy Unit where
  authorized := fun _ => False

theorem acceptance_does_not_entail_authority :
    ∃ (E : Evaluator Unit Bool) (A : AuthorityPolicy Unit) (report : Unit),
      AcceptedBy E report ∧ ¬ A.authorized report := by
  refine ⟨acceptingUnitEvaluator, denyingUnitAuthority, (), ?_, ?_⟩
  · rfl
  · simp [denyingUnitAuthority]

theorem presentation_blind_spot
    {State Report Output : Type _}
    (present : State → Report) {left right : State}
    (_hdistinct : left ≠ right)
    (hsame : present left = present right)
    (evaluate : Report → Output) :
    evaluate (present left) = evaluate (present right) := by
  exact congrArg evaluate hsame

end WitnessedDifference
