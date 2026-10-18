
import PrimitiveDifference




namespace OmegaCore.EventEffects

def replay {Event State : Type}
    (step : Event → State → State) : List Event → State → State
  | [], state => state
  | event :: rest, state => replay step rest (step event state)

def EventEquivalent {Event State : Type}
    (step : Event → State → State) (left right : Event) : Prop :=
  ∀ state, step left state = step right state

def TraceEquivalent {Event State : Type}
    (step : Event → State → State) (left right : List Event) : Prop :=
  ∀ state, replay step left state = replay step right state

def Commute {Event State : Type}
    (step : Event → State → State) (left right : Event) : Prop :=
  ∀ state, step right (step left state) = step left (step right state)

def Absorbing {Event State : Type}
    (step : Event → State → State) (terminal : State) : Prop :=
  ∀ event, step event terminal = terminal

theorem eventEquivalent_refl {Event State : Type}
    (step : Event → State → State) (event : Event) :
    EventEquivalent step event event := by
  intro state
  rfl

theorem eventEquivalent_symm {Event State : Type}
    (step : Event → State → State) (left right : Event)
    (equivalent : EventEquivalent step left right) :
    EventEquivalent step right left := by
  intro state
  exact (equivalent state).symm

theorem eventEquivalent_trans {Event State : Type}
    (step : Event → State → State) (first second third : Event)
    (firstSecond : EventEquivalent step first second)
    (secondThird : EventEquivalent step second third) :
    EventEquivalent step first third := by
  intro state
  exact (firstSecond state).trans (secondThird state)

theorem replay_append {Event State : Type}
    (step : Event → State → State)
    (left right : List Event) (state : State) :
    replay step (left ++ right) state =
      replay step right (replay step left state) := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest induction =>
      simp only [List.cons_append, replay]
      exact induction (step event state)

theorem eventEquivalent_replay_congruence {Event State : Type}
    (step : Event → State → State)
    (left right : Event)
    (equivalent : EventEquivalent step left right)
    (pre post : List Event) :
    TraceEquivalent step
      (pre ++ left :: post)
      (pre ++ right :: post) := by
  intro state
  rw [replay_append, replay_append]
  simp only [replay]
  rw [equivalent]

theorem commute_allows_adjacent_swap {Event State : Type}
    (step : Event → State → State)
    (left right : Event)
    (commute : Commute step left right)
    (pre post : List Event) :
    TraceEquivalent step
      (pre ++ left :: right :: post)
      (pre ++ right :: left :: post) := by
  intro state
  rw [replay_append, replay_append]
  simp only [replay]
  rw [commute]

theorem replay_absorbing {Event State : Type}
    (step : Event → State → State)
    (terminal : State)
    (absorbing : Absorbing step terminal) :
    ∀ trace, replay step trace terminal = terminal := by
  intro trace
  induction trace with
  | nil => rfl
  | cons event rest induction =>
      simp only [replay]
      rw [absorbing event]
      exact induction

theorem traceEquivalent_refl {Event State : Type}
    (step : Event → State → State) (trace : List Event) :
    TraceEquivalent step trace trace := by
  intro state
  rfl

theorem traceEquivalent_trans {Event State : Type}
    (step : Event → State → State) (first second third : List Event)
    (firstSecond : TraceEquivalent step first second)
    (secondThird : TraceEquivalent step second third) :
    TraceEquivalent step first third := by
  intro state
  exact (firstSecond state).trans (secondThird state)

#print axioms eventEquivalent_refl
#print axioms eventEquivalent_symm
#print axioms eventEquivalent_trans
#print axioms replay_append
#print axioms eventEquivalent_replay_congruence
#print axioms commute_allows_adjacent_swap
#print axioms replay_absorbing
#print axioms traceEquivalent_refl
#print axioms traceEquivalent_trans

end OmegaCore.EventEffects

private def l5aProvenance : String :=
  "Origin: lean4/EventEffects.lean Claim: eventEquivalent_refl AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
