/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 6c20ad0f18828ce44925bc2a672f1bab7bdc432e98cfee511fb9b0d43fc4a9c8 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.ProposalAdmissionBridge
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Std

/-!
Abstract semantic roles, not physical agents. Factorization is on the actual
report image: no extension to unused reports or surjectivity assumption.
Replay soundness is relative to the declared deterministic transition; no
physical truth, provenance authenticity, or authority follows from this model.
-/
namespace WitnessedDifference.ProposalAdmissionBridge

universe u v w z

def ReportImage {X : Type u} {R : Type v} (report : X → R) :=
  {r : R // ∃ x, report x = r}

def imageReport {X : Type u} {R : Type v} (report : X → R) (x : X) :
    ReportImage report := ⟨report x, ⟨x, rfl⟩⟩

def FiberConstant {X : Type u} {R : Type v} {D : Type w}
    (report : X → R) (decision : X → D) : Prop :=
  ∀ x y, report x = report y → decision x = decision y

def FactorsOnImage {X : Type u} {R : Type v} {D : Type w}
    (report : X → R) (decision : X → D) : Prop :=
  ∃ decoder : ReportImage report → D, ∀ x, decoder (imageReport report x) = decision x

theorem factorization_iff_fiber_constancy {X : Type u} {R : Type v} {D : Type w}
    (report : X → R) (decision : X → D) :
    FactorsOnImage report decision ↔ FiberConstant report decision := by
  constructor
  · rintro ⟨decoder, h⟩ x y eq
    have images : imageReport report x = imageReport report y := Subtype.ext eq
    calc
      decision x = decoder (imageReport report x) := (h x).symm
      _ = decoder (imageReport report y) := congrArg decoder images
      _ = decision y := h y
  · intro h
    classical
    let representative : ReportImage report → X := fun r => Classical.choose r.property
    have chosen : ∀ r, report (representative r) = r.val :=
      fun r => Classical.choose_spec r.property
    refine ⟨fun r => decision (representative r), ?_⟩
    intro x
    exact h _ x (chosen (imageReport report x))

theorem equal_report_opposite_decision_no_decoder
    {X : Type u} {R : Type v} {D : Type w}
    (report : X → R) (decision : X → D) (x y : X)
    (same : report x = report y) (opposite : decision x ≠ decision y) :
    ¬ FactorsOnImage report decision := by
  intro decoder
  exact opposite ((factorization_iff_fiber_constancy report decision).mp decoder x y same)

theorem postprocessing_cannot_restore_decision
    {X : Type u} {R : Type v} {S : Type z} {D : Type w}
    (report : X → R) (post : R → S) (decision : X → D)
    (x y : X) (same : report x = report y) (opposite : decision x ≠ decision y) :
    ¬ FactorsOnImage (post ∘ report) decision := by
  exact equal_report_opposite_decision_no_decoder _ _ x y (congrArg post same) opposite

/-- Faithful for these two declared roles only; not necessarily injective on X. -/
theorem joint_report_preserves_permission
    {X : Type u} {E : Type v} {P : Type w}
    (evaluation : X → E) (permission : X → P) :
    FactorsOnImage (fun x => (evaluation x, permission x)) permission := by
  refine ⟨fun r => r.val.2, ?_⟩
  intro x
  rfl

theorem joint_report_preserves_evaluation
    {X : Type u} {E : Type v} {P : Type w}
    (evaluation : X → E) (permission : X → P) :
    FactorsOnImage (fun x => (evaluation x, permission x)) evaluation := by
  refine ⟨fun r => r.val.1, ?_⟩
  intro x
  rfl

/-- Joint equality identifies exactly agreement of the two semantic roles. -/
theorem joint_report_equality_iff
    {X : Type u} {E : Type v} {P : Type w}
    (evaluation : X → E) (permission : X → P) (x y : X) :
    (evaluation x, permission x) = (evaluation y, permission y) ↔
    evaluation x = evaluation y ∧ permission x = permission y := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨he, hp⟩
    rw [he, hp]

/-- Two finite states can have identical successful evaluation and opposite permission. -/
theorem evaluation_does_not_determine_authorization :
    ¬ FactorsOnImage (fun _ : Bool => true) (fun b : Bool => b) := by
  exact equal_report_opposite_decision_no_decoder _ _ false true rfl (by decide)

section Replay
variable {State : Type u} {Proposal : Type v}

def admittedStep (transition : State → Proposal → State)
    (valid permitted : State → Proposal → Bool) (state : State) (proposal : Proposal) : State :=
  if valid state proposal && permitted state proposal then transition state proposal else state

def replay (step : State → Proposal → State) (state : State) (log : List Proposal) : State :=
  log.foldl step state

theorem replay_nil (step : State → Proposal → State) (state : State) :
    replay step state [] = state := rfl

theorem replay_cons (step : State → Proposal → State) (state : State)
    (proposal : Proposal) (log : List Proposal) :
    replay step state (proposal :: log) = replay step (step state proposal) log := rfl

theorem replay_append (step : State → Proposal → State) (state : State)
    (first second : List Proposal) :
    replay step state (first ++ second) = replay step (replay step state first) second := by
  induction first generalizing state with
  | nil => rfl
  | cons proposal rest ih => exact ih (step state proposal)

/-- An independently supplied state trace must obey the declared step at every entry. -/
inductive DeclaredRun (step : State → Proposal → State) : State → List Proposal → State → Prop
  | nil (state) : DeclaredRun step state [] state
  | cons {state final proposal rest} : DeclaredRun step (step state proposal) rest final →
      DeclaredRun step state (proposal :: rest) final

theorem declared_run_replay_sound (step : State → Proposal → State)
    {initial final : State} {log : List Proposal}
    (run : DeclaredRun step initial log final) : replay step initial log = final := by
  induction run with
  | nil => rfl
  | cons _ ih => exact ih

theorem replay_has_declared_run (step : State → Proposal → State)
    (initial : State) (log : List Proposal) :
    DeclaredRun step initial log (replay step initial log) := by
  induction log generalizing initial with
  | nil => exact DeclaredRun.nil initial
  | cons proposal rest ih => exact DeclaredRun.cons (ih (step initial proposal))

theorem declared_run_iff_replay (step : State → Proposal → State)
    (initial final : State) (log : List Proposal) :
    DeclaredRun step initial log final ↔ replay step initial log = final := by
  constructor
  · exact declared_run_replay_sound step
  · intro eq
    rw [← eq]
    exact replay_has_declared_run step initial log

theorem invalid_proposal_noop (transition : State → Proposal → State)
    (valid permitted : State → Proposal → Bool) (state : State) (proposal : Proposal)
    (invalid : valid state proposal = false) :
    admittedStep transition valid permitted state proposal = state := by
  simp [admittedStep, invalid]

theorem unpermitted_proposal_noop (transition : State → Proposal → State)
    (valid permitted : State → Proposal → Bool) (state : State) (proposal : Proposal)
    (denied : permitted state proposal = false) :
    admittedStep transition valid permitted state proposal = state := by
  simp [admittedStep, denied]

theorem admitted_proposal_transition (transition : State → Proposal → State)
    (valid permitted : State → Proposal → Bool) (state : State) (proposal : Proposal)
    (accepted : valid state proposal = true) (authorized : permitted state proposal = true) :
    admittedStep transition valid permitted state proposal = transition state proposal := by
  simp [admittedStep, accepted, authorized]

end Replay
end WitnessedDifference.ProposalAdmissionBridge

#print axioms WitnessedDifference.ProposalAdmissionBridge.factorization_iff_fiber_constancy
#print axioms WitnessedDifference.ProposalAdmissionBridge.equal_report_opposite_decision_no_decoder
#print axioms WitnessedDifference.ProposalAdmissionBridge.postprocessing_cannot_restore_decision
#print axioms WitnessedDifference.ProposalAdmissionBridge.joint_report_preserves_permission
#print axioms WitnessedDifference.ProposalAdmissionBridge.joint_report_preserves_evaluation
#print axioms WitnessedDifference.ProposalAdmissionBridge.evaluation_does_not_determine_authorization
#print axioms WitnessedDifference.ProposalAdmissionBridge.replay_append
#print axioms WitnessedDifference.ProposalAdmissionBridge.declared_run_replay_sound
#print axioms WitnessedDifference.ProposalAdmissionBridge.replay_has_declared_run
#print axioms WitnessedDifference.ProposalAdmissionBridge.declared_run_iff_replay
#print axioms WitnessedDifference.ProposalAdmissionBridge.invalid_proposal_noop
#print axioms WitnessedDifference.ProposalAdmissionBridge.unpermitted_proposal_noop
#print axioms WitnessedDifference.ProposalAdmissionBridge.admitted_proposal_transition

#print axioms WitnessedDifference.ProposalAdmissionBridge.joint_report_equality_iff
#print axioms WitnessedDifference.ProposalAdmissionBridge.replay_nil
#print axioms WitnessedDifference.ProposalAdmissionBridge.replay_cons
