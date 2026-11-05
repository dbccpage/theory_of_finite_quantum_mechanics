import WitnessedDifference.EmpiricalModel
import WitnessedDifference.Measurement

/-!
# Measurement packets into empirical models

This module instantiates the adapter of `EmpiricalModel` with the measurement
packets of Chapter 13 (`WDP-CH13-D01`) and states which observer and evaluator
fields survive the map (`WDP-CH19-O01`).

A packet profile declares the measurand that each measurement reads, and a
partition of calibrated results into outcomes (the value and partition
structure of CH13-D01). A packet may fill slot `x` of a run only when its
measurand is the one declared for `x`. It reports the bin of its calibrated
value.

This file imports both Mathlib and the package's core declarations. Their
notations for the rationals and the empty set collide, so it writes `Rat` and
uses neither.
-/

namespace WitnessedDifference.PacketAdapter

open WitnessedDifference.Empirical

/-- A declared packet profile: the measurand read by each measurement, and the
outcome bin of each calibrated result. -/
structure PacketProfile (X Measurand Result O : Type*) where
  measurandOf : X → Measurand
  bin : X → Result → O

section Profile

variable {World Report Trace Measurand Indication Result Unit Reference
    Procedure : Type*} {X O : Type*}
  (prof : PacketProfile X Measurand Result O)

/-- Slot `x` accepts a packet whose measurand is the one declared for `x`. -/
def admissible (x : X)
    (M : MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure) : Prop :=
  M.measurand = prof.measurandOf x

/-- The outcome a packet reports for measurement `x`: the bin of its
calibrated value. -/
def readout (x : X)
    (M : MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure) : O :=
  prof.bin x (M.calibratedValue (M.indication M.acceptedObservation.receipt.report))

/-- The evidence a packet carries for outcome `o` of measurement `x`: the
declared measurand, an accepted evaluator status, a report retrievable from
the observer's memory, a replayable provenance record, and the outcome
itself. -/
def Backs
    (M : MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure) (x : X) (o : O) : Prop :=
  M.measurand = prof.measurandOf x ∧
    M.acceptedObservation.receipt.status = EvaluationStatus.accept ∧
    M.acceptedObservation.receipt.observer.memory.retrieve
        M.acceptedObservation.receipt.trace =
      some M.acceptedObservation.receipt.report ∧
    M.provenance M.acceptedObservation.receipt.trace =
      some (M.indication M.acceptedObservation.receipt.report,
        M.calibratedValue (M.indication M.acceptedObservation.receipt.report)) ∧
    readout prof x M = o

theorem backs_iff
    (M : MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure) (x : X) (o : O) :
    Backs prof M x o ↔ admissible prof x M ∧ readout prof x M = o := by
  constructor
  · rintro ⟨hm, -, -, -, ho⟩
    exact ⟨hm, ho⟩
  · rintro ⟨hm, ho⟩
    exact ⟨hm, M.acceptedObservation.accepted,
      (MeasurementPacket.report_and_result_reaccessible M).1,
      (MeasurementPacket.report_and_result_reaccessible M).2, ho⟩

variable [DecidableEq X] [_root_.Fintype O] [DecidableEq O] {ι : Type*}
  (ctx : ι → Finset X)

/-- The typed map on packet tables: it returns `m` exactly when no context is
empty and `m` is the table of frequencies, and it returns a model exactly when,
in addition, the frequencies agree on every overlap. -/
theorem measurement_packet_adapter
    (T : ∀ i, List (Run (MeasurementPacket World Report Trace Measurand
      Indication Result Unit Reference Procedure) (admissible prof) (ctx i))) :
    (∀ m, adapt (readout prof) ctx T = .inr m ↔
        (∀ i, T i ≠ []) ∧ m.weight = freqs (readout prof) ctx T) ∧
      ((∃ m, adapt (readout prof) ctx T = .inr m) ↔
        (∀ i, T i ≠ []) ∧ Compatible ctx (freqs (readout prof) ctx T)) :=
  ⟨adapt_eq_inr_iff (readout prof) ctx T, adapt_succeeds_iff (readout prof) ctx T⟩

/-- What survives: a section has positive weight in the image exactly when a
recorded run backs it with accepted, re-accessible packets that carry the
declared measurands. -/
theorem support_is_backed_by_accepted_packets
    (T : ∀ i, List (Run (MeasurementPacket World Report Trace Measurand
      Indication Result Unit Reference Procedure) (admissible prof) (ctx i)))
    {m : EmpiricalModel ctx O} (hm : adapt (readout prof) ctx T = .inr m)
    (i : ι) (s : ctx i → O) :
    0 < m.weight i s ↔ ∃ r ∈ T i, ∀ x : ctx i, Backs prof (r.packet x) x.1 (s x) := by
  rw [adapt_support (readout prof) ctx T hm i s]
  constructor
  · rintro ⟨r, hr, rfl⟩
    exact ⟨r, hr, fun x => (backs_iff prof _ _ _).2 ⟨r.admissible_packet x, rfl⟩⟩
  · rintro ⟨r, hr, hb⟩
    exact ⟨r, hr, funext fun x => ((backs_iff prof _ _ _).1 (hb x)).2⟩

/-- Replace the calibration chain of a packet. -/
def recalibrate (c : CalibrationChain Reference Procedure)
    (M : MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure) :
    MeasurementPacket World Report Trace Measurand Indication Result Unit
      Reference Procedure :=
  { M with calibrationChain := c }

omit [DecidableEq X] [_root_.Fintype O] in
/-- Replacing the calibration chain of every packet changes the documented
traceability but not the image. -/
theorem recalibration_is_invisible {C : Finset X}
    (c : CalibrationChain Reference Procedure)
    (T : List (Run (MeasurementPacket World Report Trace Measurand Indication
      Result Unit Reference Procedure) (admissible prof) C)) :
    freq (readout prof)
        (T.map (Run.mapPacket (admissible := admissible prof)
          (admissible' := admissible prof) (recalibrate c) fun _ _ h => h)) =
      freq (readout prof) T :=
  freq_mapPacket (admissible := admissible prof) (admissible' := admissible prof)
    (readout prof) (readout prof) (recalibrate c) (fun _ _ h => h)
    (fun _ _ _ => rfl) T

/-- What is lost: the image depends only on the list of reported outcomes, so
every packet field that does not reach the readout is forgotten, whatever the
packet types; and two nonempty tables have the same image in a context
exactly when their outcome counts there are proportional. -/
theorem what_survives_the_adapter
    (T : ∀ i, List (Run (MeasurementPacket World Report Trace Measurand
      Indication Result Unit Reference Procedure) (admissible prof) (ctx i))) :
    (∀ (m : EmpiricalModel ctx O), adapt (readout prof) ctx T = .inr m →
        ∀ i s, 0 < m.weight i s ↔
          ∃ r ∈ T i, ∀ x : ctx i, Backs prof (r.packet x) x.1 (s x)) ∧
      (∀ {World' Report' Trace' Measurand' Indication' Result' Unit'
          Reference' Procedure' : Type*}
          (prof' : PacketProfile X Measurand' Result' O)
          (T' : ∀ i, List (Run (MeasurementPacket World' Report' Trace'
            Measurand' Indication' Result' Unit' Reference' Procedure')
            (admissible prof') (ctx i))),
          (∀ i, (T i).map (Run.outcome (readout prof)) =
            (T' i).map (Run.outcome (readout prof'))) →
          freqs (readout prof) ctx T = freqs (readout prof') ctx T') ∧
      (∀ i, T i ≠ [] → ∀ T'' : List (Run (MeasurementPacket World Report
          Trace Measurand Indication Result Unit Reference Procedure)
          (admissible prof) (ctx i)), T'' ≠ [] →
        (freq (readout prof) (T i) = freq (readout prof) T'' ↔
          ∀ s, count (readout prof) (T i) s * T''.length =
            count (readout prof) T'' s * (T i).length)) := by
  refine ⟨fun m hm i s => support_is_backed_by_accepted_packets prof ctx T hm i s,
    fun prof' T' h => funext fun i => freq_eq_of_outcomes _ _ (h i),
    fun i hT T'' hT'' => freq_eq_freq_iff _ _ hT hT''⟩

/-- If the profile can report every outcome of every measurement, every
empirical model on the cover is the image of some table of accepted
measurement packets. -/
theorem every_model_is_a_packet_image
    (realize : ∀ x o, ∃ M : MeasurementPacket World Report Trace Measurand
      Indication Result Unit Reference Procedure,
        admissible prof x M ∧ readout prof x M = o)
    (m : EmpiricalModel ctx O) :
    ∃ T : ∀ i, List (Run (MeasurementPacket World Report Trace Measurand
        Indication Result Unit Reference Procedure) (admissible prof) (ctx i)),
      adapt (readout prof) ctx T = .inr m :=
  exists_table (readout prof) ctx realize m

end Profile

/-! ## A concrete profile

One observer presents the world as its report, stores the report as its own
trace, and accepts every report. Each packet carries a one-step calibration
chain. Every outcome of every CHSH measurement is reported by some such packet,
so the results above are not vacuous for measurement packets.
-/

section Toy

/-- An observer that presents the world as its report, stores the report as
its trace, and accepts every report. -/
def toyObserver : ObserverPacket Bool Bool Bool EvaluationStatus where
  presentation := { present := id }
  memory := { store := id, retrieve := some, retrieve_store := fun _ => rfl }
  evaluator := { evaluate := fun _ => .accept, accepts := fun _ => true }

/-- The same observer with an evaluator that refuses the report `false`. -/
def pickyObserver : ObserverPacket Bool Bool Bool EvaluationStatus :=
  { toyObserver with
    evaluator :=
      { evaluate := fun r => if r then .accept else .refuse
        accepts := fun v => v == .accept } }

/-- The accepted observation of world `o` by an observer that presents the
world and stores the report. -/
def toyObservation (obs : ObserverPacket Bool Bool Bool EvaluationStatus)
    (hpresent : ∀ o, obs.presentation.present o = o)
    (hstore : ∀ o, obs.memory.store o = o) (o : Bool)
    (haccept : obs.evaluator.evaluate o = .accept) :
    AcceptedObservation Bool Bool Bool :=
  ⟨{ observer := obs, world := o, report := o, trace := o, status := .accept,
     report_eq := (hpresent o).symm, trace_eq := (hstore o).symm,
     status_eq := haccept.symm }, rfl⟩

/-- A one-step calibration chain with zero uncertainty. -/
def toyChain : CalibrationChain Unit Unit where
  length := 1
  nonempty := Nat.one_pos
  reference := fun _ => ()
  procedure := fun _ => ()
  calibrates := fun _ _ _ => True
  step_valid := fun _ => trivial
  uncertaintyContribution := fun _ => 0
  uncertainty_nonnegative := fun _ => le_refl _

/-- A packet reading measurement `x` from an accepted observation whose trace
is its report. -/
def toyPacket (x : ChshMeasurement) (obs : AcceptedObservation Bool Bool Bool)
    (htrace : obs.receipt.trace = obs.receipt.report) :
    MeasurementPacket Bool Bool Bool ChshMeasurement Bool Bool Unit Unit
      Unit where
  acceptedObservation := obs
  measurand := x
  indication := id
  calibratedValue := id
  scale := fun b => if b then 1 else 0
  unit := ()
  calibrationChain := toyChain
  resultUncertainty := fun _ => 0
  resultUncertainty_nonnegative := fun _ => le_refl _
  provenance := fun t => some (t, t)
  provenance_replay := by
    rw [htrace]
    rfl

/-- The CHSH profile: measurement `x` reads measurand `x`, and a calibrated
result is its own outcome. -/
def toyProfile : PacketProfile ChshMeasurement ChshMeasurement Bool Bool :=
  ⟨id, fun _ r => r⟩

theorem toy_realizes (x : ChshMeasurement) (o : Bool) :
    ∃ M : MeasurementPacket Bool Bool Bool ChshMeasurement Bool Bool Unit Unit
        Unit,
      admissible toyProfile x M ∧ readout toyProfile x M = o :=
  ⟨toyPacket x (toyObservation toyObserver (fun _ => rfl) (fun _ => rfl) o rfl)
    rfl, rfl, rfl⟩

/-- The evaluator is lost apart from its verdict on the recorded report: two
packets whose evaluators disagree on the report `false` have the same measurand
and the same readout, so any two tables built from them in the same pattern
have the same image. -/
theorem evaluator_is_lost :
    ∃ M M' : MeasurementPacket Bool Bool Bool ChshMeasurement Bool Bool Unit
        Unit Unit,
      M.acceptedObservation.receipt.observer.evaluator.evaluate false ≠
        M'.acceptedObservation.receipt.observer.evaluator.evaluate false ∧
      M.measurand = M'.measurand ∧
      ∀ x, readout toyProfile x M = readout toyProfile x M' := by
  refine ⟨toyPacket (false, false)
      (toyObservation toyObserver (fun _ => rfl) (fun _ => rfl) true rfl) rfl,
    toyPacket (false, false)
      (toyObservation pickyObserver (fun _ => rfl) (fun _ => rfl) true rfl) rfl,
    ?_, rfl, fun _ => rfl⟩
  decide

/-- Contextuality is the absence of a global table. For any cover and any
profile whose packets can report every outcome, a model with rational weights
is noncontextual exactly when some table of global packet runs has it as its
image. On the CHSH cover every global table obeys `CHSH ≤ 2`, whatever the
profile. The PR box has a signed global section with a negative weight and no
nonnegative one, and for the concrete profile above a finite table of accepted
measurement packets has it as its image, with CHSH value four, strong
contextuality, and no global table with the same image. -/
theorem contextuality_is_a_missing_global_table :
    (∀ {World Report Trace Measurand Indication Result Unit Reference
        Procedure X O ι : Type*} [DecidableEq X] [_root_.Fintype X]
        [_root_.Fintype O] [DecidableEq O]
        (prof : PacketProfile X Measurand Result O) (ctx : ι → Finset X),
        (∀ x o, ∃ M : MeasurementPacket World Report Trace Measurand
            Indication Result Unit Reference Procedure,
          admissible prof x M ∧ readout prof x M = o) →
        ∀ m : EmpiricalModel ctx O, IsNoncontextual ctx m.weight ↔
          ∃ G : List (GlobalRun (MeasurementPacket World Report Trace
              Measurand Indication Result Unit Reference Procedure)
              (admissible prof)),
            G ≠ [] ∧ adapt (readout prof) ctx (restrictTable ctx G) = .inr m) ∧
      (∀ {World Report Trace Measurand Indication Result Unit Reference
          Procedure : Type*} (prof : PacketProfile ChshMeasurement Measurand
            Result Bool)
          (G : List (GlobalRun (MeasurementPacket World Report Trace Measurand
            Indication Result Unit Reference Procedure) (admissible prof))),
          G ≠ [] →
          chsh (freqs (readout prof) chshContext
            (restrictTable chshContext G)) ≤ 2) ∧
      (IsGlobalSection chshContext prWeight prSigned ∧
        prSigned (globalEquiv.symm (false, false, true, false)) < 0 ∧
        ¬ IsNoncontextual chshContext prWeight) ∧
      ∃ T : ∀ xy, List (Run (MeasurementPacket Bool Bool Bool ChshMeasurement
          Bool Bool Unit Unit Unit) (admissible toyProfile) (chshContext xy)),
        adapt (readout toyProfile) chshContext T = .inr prBox ∧
        chsh (freqs (readout toyProfile) chshContext T) = 4 ∧
        IsStronglyContextual chshContext
          (freqs (readout toyProfile) chshContext T) ∧
        ¬ ∃ G : List (GlobalRun (MeasurementPacket Bool Bool Bool ChshMeasurement
            Bool Bool Unit Unit Unit) (admissible toyProfile)),
          G ≠ [] ∧ adapt (readout toyProfile) chshContext
            (restrictTable chshContext G) = .inr prBox :=
  ⟨fun prof ctx realize m =>
      noncontextual_iff_global_table (readout prof) ctx realize m,
    fun prof G hG => chsh_le_two_of_global_table (readout prof) G hG,
    prBox_signed_not_nonneg,
    pr_box_packet_table (readout toyProfile) toy_realizes⟩

end Toy

end WitnessedDifference.PacketAdapter
