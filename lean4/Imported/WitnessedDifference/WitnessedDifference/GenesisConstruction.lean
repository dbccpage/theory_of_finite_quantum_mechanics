/- Imported so that this repository carries its own Lean evidence.
   Original sha256: f1d9c3859de7ed4109600bb93ee59fa9cd3e1d1f2d9585183f8b4afa781a2904 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.GenesisConstruction
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WitnessedDifference.WitnessedDifference.GenerativeHistoryCompression

/-!
# Literal-root construction and replay correspondence

This file reuses WDP's partial replay and typed transition histories. A recorded
history beginning with `supply "<>"` retains that exact event, even when supply
does not change the admitted state. Accepted replay constructs a typed history;
an event-by-event interpretation transports both success and refusal through
the complete history.

The step-commutation and supply-inertness hypotheses are explicit interfaces.
They are not a formal verification of either Rust implementation. In particular,
this file does not substitute a total no-op-on-error model for the Rust partial
admission rules, or derive mathematical incidence from the spelling of `<>`.
The executable source/target correspondence and incidence construction are
separate obligations. No new Genesis state or admission model is defined here.
-/

namespace WitnessedDifference.GenesisConstruction

open GenerativeHistoryCompression

universe u v w z

/-- The recorded presentation, without an internal parse into two marks. -/
def literalRoot : String := "<>"

/-- An accepted event list determines a typed history with exactly those events.
Together with `replay_transitionEvents`, this gives both directions of the
correspondence between successful partial replay and typed histories. -/
theorem accepted_replay_has_typed_history
    {State : Type u} {Event : Type v}
    (step : State → Event → Option State) (events : List Event)
    {initial final : State} (accepted : replay step events initial = some final) :
    ∃ path : Path (transitionSignature step) initial final,
      transitionEvents path = events := by
  induction events generalizing initial with
  | nil =>
      have h : initial = final := Option.some.inj accepted
      subst final
      exact ⟨.nil initial, rfl⟩
  | cons event events ih =>
      cases hstep : step initial event with
      | none => simp [replay, hstep] at accepted
      | some next =>
          have htail : replay step events next = some final := by
            simpa only [replay, hstep] using accepted
          obtain ⟨tail, hevents⟩ := ih htail
          exact ⟨.cons ⟨event, hstep⟩ tail, by
            simp only [transitionEvents, hevents]⟩

/-- One checked commuting equation per event suffices for every finite history.
The equation includes rejection: `none` cannot become an accepted transition. -/
theorem replay_commutes
    {Source : Type u} {Target : Type v}
    {SourceEvent : Type w} {TargetEvent : Type z}
    (sourceStep : Source → SourceEvent → Option Source)
    (targetStep : Target → TargetEvent → Option Target)
    (stateMap : Source → Target) (eventMap : SourceEvent → TargetEvent)
    (commutes : ∀ state event,
      targetStep (stateMap state) (eventMap event) =
        (sourceStep state event).map stateMap)
    (events : List SourceEvent) (initial : Source) :
    replay targetStep (events.map eventMap) (stateMap initial) =
      (replay sourceStep events initial).map stateMap := by
  induction events generalizing initial with
  | nil => rfl
  | cons event events ih =>
      simp only [List.map_cons, replay, commutes]
      cases hstep : sourceStep initial event with
      | none => rfl
      | some next => exact ih next

/-- Refusal is preserved and reflected without assuming that the state map is
injective. This concerns the mapped source history and mapped initial state. -/
theorem replay_refusal_iff
    {Source : Type u} {Target : Type v}
    {SourceEvent : Type w} {TargetEvent : Type z}
    (sourceStep : Source → SourceEvent → Option Source)
    (targetStep : Target → TargetEvent → Option Target)
    (stateMap : Source → Target) (eventMap : SourceEvent → TargetEvent)
    (commutes : ∀ state event,
      targetStep (stateMap state) (eventMap event) =
        (sourceStep state event).map stateMap)
    (events : List SourceEvent) (initial : Source) :
    replay targetStep (events.map eventMap) (stateMap initial) = none ↔
      replay sourceStep events initial = none := by
  rw [replay_commutes sourceStep targetStep stateMap eventMap commutes]
  cases replay sourceStep events initial <;> simp

/-- A faithful state representation also reflects the exact successful result.
It is not enough for the target merely to report an arbitrary success label. -/
theorem replay_exact_result_iff
    {Source : Type u} {Target : Type v}
    {SourceEvent : Type w} {TargetEvent : Type z}
    (sourceStep : Source → SourceEvent → Option Source)
    (targetStep : Target → TargetEvent → Option Target)
    (stateMap : Source → Target) (eventMap : SourceEvent → TargetEvent)
    (faithful : ∀ {a b}, stateMap a = stateMap b → a = b)
    (commutes : ∀ state event,
      targetStep (stateMap state) (eventMap event) =
        (sourceStep state event).map stateMap)
    (events : List SourceEvent) (initial final : Source) :
    replay targetStep (events.map eventMap) (stateMap initial) =
        some (stateMap final) ↔
      replay sourceStep events initial = some final := by
  rw [replay_commutes sourceStep targetStep stateMap eventMap commutes]
  cases h : replay sourceStep events initial with
  | none => simp
  | some result =>
      simp only [Option.map_some, Option.some.injEq]
      exact ⟨faithful, congrArg stateMap⟩

/-- Supply may be state-inert while remaining an actual first event. The rule
for that event is a hypothesis, not an inference from its visible spelling. -/
def rootedHistory
    {State : Type u} {Event : Type v}
    {step : State → Event → Option State}
    (supply : String → Event) {initial final : State}
    (inert : step initial (supply literalRoot) = some initial)
    (path : Path (transitionSignature step) initial final) :
    Path (transitionSignature step) initial final :=
  .cons ⟨supply literalRoot, inert⟩ path

/-- The literal-root event is retained in the ordered history. -/
theorem rootedHistory_events
    {State : Type u} {Event : Type v}
    {step : State → Event → Option State}
    (supply : String → Event) {initial final : State}
    (inert : step initial (supply literalRoot) = some initial)
    (path : Path (transitionSignature step) initial final) :
    transitionEvents (rootedHistory supply inert path) =
      supply "<>" :: transitionEvents path := rfl

/-- Prepending the recorded literal supply preserves the replayed state. -/
theorem literal_supply_replay
    {State : Type u} {Event : Type v}
    (step : State → Event → Option State) (supply : String → Event)
    (initial : State)
    (inert : step initial (supply literalRoot) = some initial)
    (events : List Event) :
    replay step (supply "<>" :: events) initial = replay step events initial := by
  change (match step initial (supply literalRoot) with
    | none => none
    | some next => replay step events next) = _
  rw [inert]

/-- A literal-root history and its ordinary continuation reach the same target,
and the constructed typed history still contains the root event. -/
theorem literal_root_construction
    {State : Type u} {Event : Type v}
    (step : State → Event → Option State) (supply : String → Event)
    {initial final : State}
    (inert : step initial (supply literalRoot) = some initial)
    (events : List Event) (accepted : replay step events initial = some final) :
    ∃ path : Path (transitionSignature step) initial final,
      transitionEvents path = supply "<>" :: events ∧
      replay step (transitionEvents path) initial = some final := by
  obtain ⟨tail, hevents⟩ := accepted_replay_has_typed_history step events accepted
  refine ⟨rootedHistory supply inert tail, ?_, replay_transitionEvents _⟩
  simp only [rootedHistory_events, hevents]

end WitnessedDifference.GenesisConstruction

#print axioms WitnessedDifference.GenesisConstruction.accepted_replay_has_typed_history
#print axioms WitnessedDifference.GenesisConstruction.replay_commutes
#print axioms WitnessedDifference.GenesisConstruction.replay_refusal_iff
#print axioms WitnessedDifference.GenesisConstruction.replay_exact_result_iff
#print axioms WitnessedDifference.GenesisConstruction.rootedHistory_events
#print axioms WitnessedDifference.GenesisConstruction.literal_supply_replay
#print axioms WitnessedDifference.GenesisConstruction.literal_root_construction
