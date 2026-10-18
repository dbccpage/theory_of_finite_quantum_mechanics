import «l011_04_epk_path»
import «admission_firewall_q_admission_firewall»

/-!
QM-facing Paper 011 operator-trace bridge.

A QM residual-density proposal step may carry an operator label and density-like
source/target payloads, but acceptance is still the Paper 011 guarded evaluator
predicate on the before/after obstruction tuple and the `R_cl` gate. Changing
proposal metadata cannot change acceptance when the evaluator trace is fixed.

This is an interface theorem only. It does not derive quantum mechanics, select
the Born rule, certify dynamics, license a continuum lift, or mint authority.
-/

namespace QM

namespace PaperAF000OperatorTraceBridge

universe u v w z

/-- QM-facing proposal step: operator metadata plus density-like source and
target payloads, evaluated only through the Paper 011 tuple and gate. -/
structure DensityProposalStep (Operator : Type u) (DensityState : Type v) where
  operator : Operator
  sourceDensity : DensityState
  targetDensity : DensityState
  before : PaperAF000.EvalTuple
  after : PaperAF000.EvalTuple
  rclOk : Bool

/-- Forget the QM-facing names and view the proposal as a Paper 011 EPK step. -/
def toEpkStep {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState) :
    PaperAF000.EpkStep Operator DensityState where
  operator := step.operator
  source := step.sourceDensity
  target := step.targetDensity
  before := step.before
  after := step.after
  rclOk := step.rclOk

/-- Acceptance of a QM density proposal is Paper 011 step acceptance. -/
def DensityStepAccepted {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState) : Prop :=
  PaperAF000.StepAccepted (toEpkStep step)

/-- The evaluator trace seen by Paper 011 after forgetting proposal metadata. -/
def densityTraceOfStep {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState) : PaperAF000.StepTrace :=
  PaperAF000.traceOfStep (toEpkStep step)

/-- Replace all proposal metadata while preserving the evaluator trace. -/
def replaceDensityProposalMetadata
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (step : DensityProposalStep Operator₁ DensityState₁) :
    DensityProposalStep Operator₂ DensityState₂ where
  operator := replacement
  sourceDensity := sourceDensity
  targetDensity := targetDensity
  before := step.before
  after := step.after
  rclOk := step.rclOk

/-- QM density proposal acceptance factors through the Paper 011 evaluator trace. -/
theorem density_step_acceptance_iff_trace_accepted
    {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState) :
    DensityStepAccepted step ↔
      PaperAF000.TraceAccepted (densityTraceOfStep step) :=
  Iff.rfl

/-- Operator labels and density source/target payloads are proposal metadata:
replacing them cannot change acceptance when the evaluator trace is fixed. -/
theorem density_step_acceptance_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (step : DensityProposalStep Operator₁ DensityState₁) :
    DensityStepAccepted
        (replaceDensityProposalMetadata
          replacement sourceDensity targetDensity step) ↔
      DensityStepAccepted step :=
  Iff.rfl

/-- Finite paths of QM density proposal steps. -/
def DensityPathAccepted {Operator : Type u} {DensityState : Type v} :
    List (DensityProposalStep Operator DensityState) → Prop
  | [] => True
  | step :: rest => DensityStepAccepted step ∧ DensityPathAccepted rest

/-- Replace all proposal metadata in a finite QM density proposal path. -/
def replaceDensityPathMetadata
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (steps : List (DensityProposalStep Operator₁ DensityState₁)) :
    List (DensityProposalStep Operator₂ DensityState₂) :=
  steps.map (replaceDensityProposalMetadata replacement sourceDensity targetDensity)

/-- Extract only the evaluator traces from a finite QM density proposal path. -/
def densityTracePath {Operator : Type u} {DensityState : Type v}
    (steps : List (DensityProposalStep Operator DensityState)) :
    List PaperAF000.StepTrace :=
  steps.map densityTraceOfStep

/-- QM density proposal path acceptance factors through evaluator traces. -/
theorem density_path_acceptance_iff_trace_path_acceptance
    {Operator : Type u} {DensityState : Type v}
    (steps : List (DensityProposalStep Operator DensityState)) :
    DensityPathAccepted steps ↔
      PaperAF000.TracePathAccepted (densityTracePath steps) := by
  induction steps with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        (DensityStepAccepted step ∧ DensityPathAccepted rest) ↔
          (PaperAF000.TraceAccepted (densityTraceOfStep step) ∧
            PaperAF000.TracePathAccepted (densityTracePath rest))
      constructor
      · intro h
        exact ⟨(density_step_acceptance_iff_trace_accepted step).mp h.1, ih.mp h.2⟩
      · intro h
        exact ⟨(density_step_acceptance_iff_trace_accepted step).mpr h.1, ih.mpr h.2⟩

/-- Replacing all operator/density proposal metadata in a finite path preserves
acceptance when the evaluator traces are unchanged. -/
theorem density_path_acceptance_ignores_metadata_replacement
    {Operator₁ : Type u} {DensityState₁ : Type v}
    {Operator₂ : Type w} {DensityState₂ : Type z}
    (replacement : Operator₂) (sourceDensity targetDensity : DensityState₂)
    (steps : List (DensityProposalStep Operator₁ DensityState₁)) :
    DensityPathAccepted
        (replaceDensityPathMetadata
          replacement sourceDensity targetDensity steps) ↔
      DensityPathAccepted steps := by
  induction steps with
  | nil =>
      rfl
  | cons step rest ih =>
      change
        (DensityStepAccepted
            (replaceDensityProposalMetadata replacement sourceDensity targetDensity step) ∧
          DensityPathAccepted
            (replaceDensityPathMetadata replacement sourceDensity targetDensity rest)) ↔
        (DensityStepAccepted step ∧ DensityPathAccepted rest)
      constructor
      · intro h
        exact
          ⟨(density_step_acceptance_ignores_metadata_replacement
              replacement sourceDensity targetDensity step).mp h.1,
            ih.mp h.2⟩
      · intro h
        exact
          ⟨(density_step_acceptance_ignores_metadata_replacement
              replacement sourceDensity targetDensity step).mpr h.1,
            ih.mpr h.2⟩
/-- QM density proposal path acceptance is exactly componentwise under path
concatenation. Concatenation adds no proposal-side authority beyond the accepted
left and right segments. -/
theorem density_path_acceptance_append_iff
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    DensityPathAccepted (left ++ right) ↔
      DensityPathAccepted left ∧ DensityPathAccepted right := by
  induction left with
  | nil =>
      constructor
      · intro h
        exact ⟨trivial, h⟩
      · intro h
        exact h.2
  | cons step rest ih =>
      change
        (DensityStepAccepted step ∧ DensityPathAccepted (rest ++ right)) ↔
          (DensityStepAccepted step ∧ DensityPathAccepted rest) ∧
            DensityPathAccepted right
      constructor
      · intro h
        exact ⟨⟨h.1, (ih.mp h.2).1⟩, (ih.mp h.2).2⟩
      · intro h
        exact ⟨h.1.1, ih.mpr ⟨h.1.2, h.2⟩⟩

/-- The evaluator-trace form of density path append acceptance is also
componentwise. -/
theorem density_trace_path_acceptance_append_iff
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    PaperAF000.TracePathAccepted (densityTracePath (left ++ right)) ↔
      PaperAF000.TracePathAccepted (densityTracePath left) ∧
        PaperAF000.TracePathAccepted (densityTracePath right) := by
  induction left with
  | nil =>
      constructor
      · intro h
        exact ⟨trivial, h⟩
      · intro h
        exact h.2
  | cons step rest ih =>
      change
        (PaperAF000.TraceAccepted (densityTraceOfStep step) ∧
            PaperAF000.TracePathAccepted (densityTracePath (rest ++ right))) ↔
          (PaperAF000.TraceAccepted (densityTraceOfStep step) ∧
              PaperAF000.TracePathAccepted (densityTracePath rest)) ∧
            PaperAF000.TracePathAccepted (densityTracePath right)
      constructor
      · intro h
        exact ⟨⟨h.1, (ih.mp h.2).1⟩, (ih.mp h.2).2⟩
      · intro h
        exact ⟨h.1.1, ih.mpr ⟨h.1.2, h.2⟩⟩
/-- Accepted concatenated density paths project to accepted left segments. -/
theorem density_path_acceptance_of_append_left
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    DensityPathAccepted (left ++ right) → DensityPathAccepted left := by
  intro h
  exact ((density_path_acceptance_append_iff left right).mp h).1

/-- Accepted concatenated density paths project to accepted right segments. -/
theorem density_path_acceptance_of_append_right
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    DensityPathAccepted (left ++ right) → DensityPathAccepted right := by
  intro h
  exact ((density_path_acceptance_append_iff left right).mp h).2

/-- A rejected left density segment rejects the concatenated density path. -/
theorem density_path_append_rejects_of_left_rejects
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState))
    (hReject : ¬ DensityPathAccepted left) :
    ¬ DensityPathAccepted (left ++ right) := by
  intro h
  exact hReject (density_path_acceptance_of_append_left left right h)

/-- A rejected right density segment rejects the concatenated density path. -/
theorem density_path_append_rejects_of_right_rejects
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState))
    (hReject : ¬ DensityPathAccepted right) :
    ¬ DensityPathAccepted (left ++ right) := by
  intro h
  exact hReject (density_path_acceptance_of_append_right left right h)

/-- Accepted concatenated density trace paths project to accepted left trace segments. -/
theorem density_trace_path_acceptance_of_append_left
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    PaperAF000.TracePathAccepted (densityTracePath (left ++ right)) →
      PaperAF000.TracePathAccepted (densityTracePath left) := by
  intro h
  exact ((density_trace_path_acceptance_append_iff left right).mp h).1

/-- Accepted concatenated density trace paths project to accepted right trace segments. -/
theorem density_trace_path_acceptance_of_append_right
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState)) :
    PaperAF000.TracePathAccepted (densityTracePath (left ++ right)) →
      PaperAF000.TracePathAccepted (densityTracePath right) := by
  intro h
  exact ((density_trace_path_acceptance_append_iff left right).mp h).2

/-- A rejected left density trace segment rejects the concatenated trace path. -/
theorem density_trace_path_append_rejects_of_left_rejects
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState))
    (hReject : ¬ PaperAF000.TracePathAccepted (densityTracePath left)) :
    ¬ PaperAF000.TracePathAccepted (densityTracePath (left ++ right)) := by
  intro h
  exact hReject (density_trace_path_acceptance_of_append_left left right h)

/-- A rejected right density trace segment rejects the concatenated trace path. -/
theorem density_trace_path_append_rejects_of_right_rejects
    {Operator : Type u} {DensityState : Type v}
    (left right : List (DensityProposalStep Operator DensityState))
    (hReject : ¬ PaperAF000.TracePathAccepted (densityTracePath right)) :
    ¬ PaperAF000.TracePathAccepted (densityTracePath (left ++ right)) := by
  intro h
  exact hReject (density_trace_path_acceptance_of_append_right left right h)

/-- Accepted QM density paths require every member step's `R_cl` gate. -/
theorem density_path_acceptance_requires_step_gate
    {Operator : Type u} {DensityState : Type v}
    {steps : List (DensityProposalStep Operator DensityState)}
    (hPath : DensityPathAccepted steps)
    {step : DensityProposalStep Operator DensityState}
    (hMem : step ∈ steps) :
    step.rclOk = true := by
  induction steps with
  | nil =>
      cases hMem
  | cons head tail ih =>
      change DensityStepAccepted head ∧ DensityPathAccepted tail at hPath
      have hMemCases : step = head ∨ step ∈ tail :=
        List.mem_cons.mp hMem
      cases hMemCases with
      | inl hEq =>
          subst hEq
          exact PaperAF000.accept_requires_rcl_gate hPath.1
      | inr hTail =>
          exact ih hPath.2 hTail

/-- Accepted QM density paths require every member step's strict evaluator descent. -/
theorem density_path_acceptance_requires_step_descent
    {Operator : Type u} {DensityState : Type v}
    {steps : List (DensityProposalStep Operator DensityState)}
    (hPath : DensityPathAccepted steps)
    {step : DensityProposalStep Operator DensityState}
    (hMem : step ∈ steps) :
    PaperAF000.StrictLexDescends step.before step.after := by
  induction steps with
  | nil =>
      cases hMem
  | cons head tail ih =>
      change DensityStepAccepted head ∧ DensityPathAccepted tail at hPath
      have hMemCases : step = head ∨ step ∈ tail :=
        List.mem_cons.mp hMem
      cases hMemCases with
      | inl hEq =>
          subst hEq
          exact PaperAF000.accept_requires_strict_lex_descent hPath.1
      | inr hTail =>
          exact ih hPath.2 hTail

/-- A rejected member density proposal step rejects the whole density path. -/
theorem density_path_rejects_if_member_rejects
    {Operator : Type u} {DensityState : Type v}
    {steps : List (DensityProposalStep Operator DensityState)}
    {step : DensityProposalStep Operator DensityState}
    (hMem : step ∈ steps)
    (hReject : ¬ DensityStepAccepted step) :
    ¬ DensityPathAccepted steps := by
  intro hPath
  have hGate : step.rclOk = true :=
    density_path_acceptance_requires_step_gate hPath hMem
  have hDescent : PaperAF000.StrictLexDescends step.before step.after :=
    density_path_acceptance_requires_step_descent hPath hMem
  exact hReject ⟨hGate, hDescent⟩

/-- A QM density proposal with unchanged evaluator tuple is rejected. -/
theorem density_unchanged_step_rejected
    {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState)
    (hTuple : step.before = step.after) :
    ¬ DensityStepAccepted step := by
  exact PaperAF000.unchanged_step_rejected (toEpkStep step) hTuple
/-- QHeld admission for a QM density proposal is exactly the shared Q admission
firewall predicate. Paper 011 trace acceptance does not inhabit this field. -/
def DensityProposalQHeldAdmissible
    (evidence : Paper_Q.QAdmissionEvidence) : Prop :=
  Paper_Q.QHeldAdmissible evidence

/-- Terminal-within-scope admission for a QM density proposal is exactly the
shared Q terminal firewall predicate. It requires witness support beyond trace
acceptance. -/
def DensityProposalTerminalWithinScopeAdmissible
    (evidence : Paper_Q.QAdmissionEvidence) : Prop :=
  Paper_Q.TerminalWithinScopeAdmissible evidence

/-- An accepted Paper 011 evaluator trace cannot bypass incomplete Q admission
debt for a QM density proposal. -/
theorem density_trace_acceptance_admission_gap_blocks_qheld
    {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState)
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hTrace : PaperAF000.TraceAccepted (densityTraceOfStep step))
    (hGap : Paper_Q.AdmissionDebtGap evidence) :
    ¬ DensityProposalQHeldAdmissible evidence := by
  exact Paper_Q.admission_debt_gap_blocks_qheld evidence hGap

/-- An accepted finite Paper 011 trace path cannot bypass incomplete Q admission
debt for a QM density proposal path. -/
theorem density_path_acceptance_admission_gap_blocks_qheld
    {Operator : Type u} {DensityState : Type v}
    (steps : List (DensityProposalStep Operator DensityState))
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hPath : PaperAF000.TracePathAccepted (densityTracePath steps))
    (hGap : Paper_Q.AdmissionDebtGap evidence) :
    ¬ DensityProposalQHeldAdmissible evidence := by
  exact Paper_Q.admission_debt_gap_blocks_qheld evidence hGap

/-- An accepted Paper 011 evaluator trace cannot turn a QM density proposal into
TerminalWithinScope without separate witness support. -/
theorem density_trace_acceptance_without_witness_blocks_terminal
    {Operator : Type u} {DensityState : Type v}
    (step : DensityProposalStep Operator DensityState)
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hTrace : PaperAF000.TraceAccepted (densityTraceOfStep step))
    (hMissingWitness : ¬ evidence.witness_support) :
    ¬ DensityProposalTerminalWithinScopeAdmissible evidence := by
  exact Paper_Q.terminal_within_scope_without_witness_blocked evidence hMissingWitness

/-- An accepted finite Paper 011 trace path cannot turn a QM density proposal
path into TerminalWithinScope without separate witness support. -/
theorem density_path_acceptance_without_witness_blocks_terminal
    {Operator : Type u} {DensityState : Type v}
    (steps : List (DensityProposalStep Operator DensityState))
    (evidence : Paper_Q.QAdmissionEvidence)
    (_hPath : PaperAF000.TracePathAccepted (densityTracePath steps))
    (hMissingWitness : ¬ evidence.witness_support) :
    ¬ DensityProposalTerminalWithinScopeAdmissible evidence := by
  exact Paper_Q.terminal_within_scope_without_witness_blocked evidence hMissingWitness

end PaperAF000OperatorTraceBridge

end QM

#print axioms QM.PaperAF000OperatorTraceBridge.density_step_acceptance_iff_trace_accepted
#print axioms QM.PaperAF000OperatorTraceBridge.density_step_acceptance_ignores_metadata_replacement
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_append_iff
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_path_acceptance_append_iff
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_of_append_left
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_of_append_right
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_append_rejects_of_left_rejects
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_append_rejects_of_right_rejects
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_path_acceptance_of_append_left
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_path_acceptance_of_append_right
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_path_append_rejects_of_left_rejects
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_path_append_rejects_of_right_rejects
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_requires_step_gate
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_requires_step_descent
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_rejects_if_member_rejects
#print axioms QM.PaperAF000OperatorTraceBridge.density_unchanged_step_rejected
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_iff_trace_path_acceptance
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_ignores_metadata_replacement
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_acceptance_admission_gap_blocks_qheld
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_admission_gap_blocks_qheld
#print axioms QM.PaperAF000OperatorTraceBridge.density_trace_acceptance_without_witness_blocks_terminal
#print axioms QM.PaperAF000OperatorTraceBridge.density_path_acceptance_without_witness_blocks_terminal
