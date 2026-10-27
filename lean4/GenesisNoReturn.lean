import Mathlib.Tactic.SplitIfs
import Derivation.Erasure
import SecondRun.Run

namespace GenesisNoReturn

/-- The array model represents each source collection coordinate explicitly. -/
structure ArrayRegime where
  data : Nat
  forms : Array Nat
  insts : Array Derivation.Inst
  rules : Array Nat
  reqs : Array (Nat × Nat)
deriving Repr, DecidableEq

def decode (r : ArrayRegime) : Derivation.Regime :=
  ⟨r.data, r.forms.toList, r.insts.toList, r.rules.toList, r.reqs.toList⟩

def encode (r : Derivation.Regime) : ArrayRegime :=
  ⟨r.data, r.forms.toArray, r.insts.toArray, r.rules.toArray, r.reqs.toArray⟩

@[simp] theorem decode_encode (r : Derivation.Regime) : decode (encode r) = r := by
  cases r; simp [decode, encode]

@[simp] theorem encode_decode (r : ArrayRegime) : encode (decode r) = r := by
  cases r; simp [decode, encode]

theorem decode_injective : Function.Injective decode :=
  Function.LeftInverse.injective encode_decode

def arrayInsert {α : Type} [DecidableEq α] (xs : Array α) (x : α) : Array α :=
  if x ∈ xs then xs else xs.push x

theorem arrayInsert_toList {α : Type} [DecidableEq α] (xs : Array α) (x : α) :
    (arrayInsert xs x).toList = Derivation.insertNew xs.toList x := by
  unfold arrayInsert Derivation.insertNew
  split_ifs <;> simp_all

/-- Independent array operations; this is not defined by wrapping source stepE. -/
def arrayStep (r : ArrayRegime) : Derivation.Event → Option ArrayRegime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms.push a } else none
  | .admitInst f xs =>
      if f < r.forms.size ∧ xs.length = r.forms.toList.getD f 0 ∧
          (∀ x ∈ xs, x < r.data) then
        some { r with insts := arrayInsert r.insts (f, xs) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.size then some { r with rules := arrayInsert r.rules f } else none
  | .impose i j =>
      if i < j ∧ j < r.data then some { r with reqs := arrayInsert r.reqs (i, j) } else none

theorem array_step_commutes (r : ArrayRegime) (e : Derivation.Event) :
    (arrayStep r e).map decode = Derivation.stepE (decode r) e := by
  cases e with
  | supply t => rfl
  | admitDatum => rfl
  | admitForm a =>
      by_cases h : 1 ≤ a
      all_goals simp [arrayStep, Derivation.stepE, decode, arrayInsert_toList, h]
  | admitInst f xs =>
      by_cases h : f < r.forms.size ∧ xs.length = r.forms.toList.getD f 0 ∧ (∀ x ∈ xs, x < r.data)
      all_goals simp [arrayStep, Derivation.stepE, decode, arrayInsert_toList, h]
  | admitRuleAll f =>
      by_cases h : f < r.forms.size
      all_goals simp [arrayStep, Derivation.stepE, decode, arrayInsert_toList, h]
  | impose i j =>
      by_cases h : i < j ∧ j < r.data
      all_goals simp [arrayStep, Derivation.stepE, decode, arrayInsert_toList, h]

def arrayReplay : List Derivation.Event → ArrayRegime → Option ArrayRegime
  | [], r => some r
  | e :: h, r => (arrayStep r e).bind (arrayReplay h)

theorem array_replay_commutes (h : List Derivation.Event) (r : ArrayRegime) :
    (arrayReplay h r).map decode = Derivation.replayE h (decode r) := by
  induction h generalizing r with
  | nil => rfl
  | cons e h ih =>
      rw [arrayReplay, Derivation.replayE_cons]
      have hs := array_step_commutes r e
      cases hx : arrayStep r e with
      | none => simp [hx] at hs; simp [hx, ← hs]
      | some t => simp [hx] at hs; simpa [← hs] using ih t

/-- Success, every output coordinate, and failure are reflected as well as preserved. -/
theorem array_replay_exact (h : List Derivation.Event) (r : ArrayRegime) (s : Derivation.Regime) :
    arrayReplay h r = some (encode s) ↔ Derivation.replayE h (decode r) = some s := by
  have hc := array_replay_commutes h r
  constructor
  · intro hs; simpa [hs] using hc.symm
  · intro hs
    cases ha : arrayReplay h r with
    | none => simp [ha, hs] at hc
    | some a =>
        have he : decode a = s := by simpa [ha, hs] using hc
        have : a = encode s := by rw [← he, encode_decode]
        simp [this]

theorem array_failure_exact (h : List Derivation.Event) (r : ArrayRegime) :
    arrayReplay h r = none ↔ Derivation.replayE h (decode r) = none := by
  have hc := array_replay_commutes h r
  rw [← hc]
  simp


def secondRegime (r : Derivation.Regime) : SecondRun.Sealed.Regime :=
  ⟨r.data, r.forms, r.insts, r.rules, r.reqs⟩

def secondEvent : Derivation.Event → SecondRun.Sealed.Event
  | .supply t => .supply t
  | .admitDatum => .admitDatum
  | .admitForm a => .admitForm a
  | .admitInst f xs => .admitInst f xs
  | .admitRuleAll f => .admitRuleAll f
  | .impose i j => .impose i j

theorem secondRegime_injective : Function.Injective secondRegime := by
  intro r s h
  cases r; cases s
  simpa [secondRegime, SecondRun.Sealed.Regime.mk.injEq] using h

theorem second_step_commutes (r : Derivation.Regime) (e : Derivation.Event) :
    (Derivation.stepE r e).map secondRegime = SecondRun.Sealed.stepE (secondRegime r) (secondEvent e) := by
  cases e with
  | supply t => rfl
  | admitDatum => rfl
  | admitForm a =>
      by_cases h : 1 ≤ a
      all_goals simp [Derivation.stepE, SecondRun.Sealed.stepE, secondRegime, secondEvent, Derivation.insertNew, SecondRun.Sealed.insertNew, h] <;> split_ifs <;> simp_all
  | admitInst f xs =>
      by_cases h : f < r.forms.length ∧ xs.length = r.forms.getD f 0 ∧ (∀ x ∈ xs, x < r.data)
      all_goals simp [Derivation.stepE, SecondRun.Sealed.stepE, secondRegime, secondEvent, Derivation.insertNew, SecondRun.Sealed.insertNew, h] <;> split_ifs <;> simp_all
  | admitRuleAll f =>
      by_cases h : f < r.forms.length
      all_goals simp [Derivation.stepE, SecondRun.Sealed.stepE, secondRegime, secondEvent, Derivation.insertNew, SecondRun.Sealed.insertNew, h] <;> split_ifs <;> simp_all
  | impose i j =>
      by_cases h : i < j ∧ j < r.data
      all_goals simp [Derivation.stepE, SecondRun.Sealed.stepE, secondRegime, secondEvent, Derivation.insertNew, SecondRun.Sealed.insertNew, h] <;> split_ifs <;> simp_all

def potential (r : Derivation.Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length


structure EngineState where
  regime : ArrayRegime
  flipped : Bool
deriving DecidableEq

inductive EngineEvent where
  | sealed (event : Derivation.Event)
  | switch
deriving DecidableEq

def sourceState (s : EngineState) : SecondRun.Run.EState :=
  ⟨secondRegime (decode s.regime),s.flipped⟩

def sourceEvent : EngineEvent → SecondRun.Run.EEvent
  | .sealed e => .sealed (secondEvent e)
  | .switch => .switch

def arrayEvent : SecondRun.Run.EEvent → EngineEvent
  | .switch => .switch
  | .sealed e => .sealed (match e with
      | .supply t => .supply t
      | .admitDatum => .admitDatum
      | .admitForm a => .admitForm a
      | .admitInst f xs => .admitInst f xs
      | .admitRuleAll f => .admitRuleAll f
      | .impose i j => .impose i j)

theorem sourceEvent_arrayEvent (e : SecondRun.Run.EEvent) : sourceEvent (arrayEvent e) = e := by
  cases e with
  | switch => rfl
  | sealed e => cases e <;> rfl

theorem arrayEvent_sourceEvent (e : EngineEvent) : arrayEvent (sourceEvent e) = e := by
  cases e with
  | switch => rfl
  | sealed e => cases e <;> rfl

def arrayOfSource (s : SecondRun.Run.EState) : EngineState :=
  ⟨encode ⟨s.regime.data,s.regime.forms,s.regime.insts,s.regime.rules,s.regime.reqs⟩,s.flipped⟩

@[simp] theorem source_array (s : SecondRun.Run.EState) : sourceState (arrayOfSource s) = s := by
  cases s with
  | mk r m => cases r; simp [sourceState,arrayOfSource,encode,decode,secondRegime]

@[simp] theorem array_source (s : EngineState) : arrayOfSource (sourceState s) = s := by
  cases s with
  | mk r m => cases r; simp [sourceState,arrayOfSource,encode,decode,secondRegime]

theorem sourceState_injective : Function.Injective sourceState :=
  Function.LeftInverse.injective array_source

def engineStep (s : EngineState) : EngineEvent → Option EngineState
  | .sealed e => (arrayStep s.regime e).map (fun r => {s with regime := r})
  | .switch => some {s with flipped := !s.flipped}

theorem engine_step_commutes (s : EngineState) (e : EngineEvent) :
    (engineStep s e).map sourceState = SecondRun.Run.estep (sourceState s) (sourceEvent e) := by
  cases e with
  | switch => rfl
  | sealed e =>
    simp only [engineStep,SecondRun.Run.estep,sourceEvent,sourceState]
    rw [← second_step_commutes, ← array_step_commutes]
    cases arrayStep s.regime e <;> rfl

def engineReplay : List EngineEvent → EngineState → Option EngineState
  | [], s => some s
  | e::h, s => (engineStep s e).bind (engineReplay h)

theorem engine_replay_commutes (h : List EngineEvent) (s : EngineState) :
    (engineReplay h s).map sourceState =
      SecondRun.Run.ereplay (h.map sourceEvent) (sourceState s) := by
  induction h generalizing s with
  | nil => rfl
  | cons e h ih =>
    have hs := engine_step_commutes s e
    have hr : SecondRun.Run.ereplay ((e::h).map sourceEvent) (sourceState s) =
        (SecondRun.Run.estep (sourceState s) (sourceEvent e)).bind
          (SecondRun.Run.ereplay (h.map sourceEvent)) := by
      rfl
    rw [hr,engineReplay]
    cases he : engineStep s e with
    | none => simp [he] at hs; simp [he, ← hs]
    | some t => simp [he] at hs; simpa [← hs] using ih t

theorem engine_replay_exact (h : List EngineEvent) (s : EngineState) (t : SecondRun.Run.EState) :
    engineReplay h s = some (arrayOfSource t) ↔
      SecondRun.Run.ereplay (h.map sourceEvent) (sourceState s) = some t := by
  rw [← engine_replay_commutes]
  constructor
  · intro hr; simp [hr]
  · intro hr
    apply Option.map_injective sourceState_injective
    simpa using hr

theorem source_regime_injective {s t : EngineState}
    (h : (sourceState s).regime = (sourceState t).regime) : s.regime = t.regime :=
  decode_injective (secondRegime_injective h)

theorem engine_replay_failure_exact (h : List EngineEvent) (s : EngineState) :
    engineReplay h s = none ↔ SecondRun.Run.ereplay (h.map sourceEvent) (sourceState s) = none := by
  rw [← engine_replay_commutes]; simp

theorem engine_replay_source {h : List EngineEvent} {s t : EngineState}
    (hr : engineReplay h s = some t) :
    SecondRun.Run.ereplay (h.map sourceEvent) (sourceState s) = some (sourceState t) := by
  rw [← engine_replay_commutes,hr]; rfl

theorem no_return (h k : List EngineEvent) {s t u : EngineState}
    (h1 : engineReplay h s = some t) (hne : t.regime ≠ s.regime)
    (h2 : engineReplay k t = some u) : u.regime ≠ s.regime := by
  have hs := SecondRun.Run.no_return (h.map sourceEvent) (k.map sourceEvent)
    (engine_replay_source h1) (fun he => hne (source_regime_injective he)) (engine_replay_source h2)
  exact fun he => hs (congrArg (fun r => secondRegime (decode r)) he)

theorem cycle_regime_const (h k : List EngineEvent) {s t : EngineState}
    (h1 : engineReplay h s = some t) (h2 : engineReplay k t = some s) : t.regime = s.regime :=
  source_regime_injective (SecondRun.Run.cycle_regime_const (h.map sourceEvent) (k.map sourceEvent)
    (engine_replay_source h1) (engine_replay_source h2))

theorem cumulative_potential (h : List EngineEvent) {s t : EngineState}
    (hr : engineReplay h s = some t) :
    SecondRun.Run.elems (sourceState s).regime ≤ SecondRun.Run.elems (sourceState t).regime :=
  SecondRun.Run.ereplay_elems_le (h.map sourceEvent) (engine_replay_source hr)

theorem strict_potential (h : List EngineEvent) {s t : EngineState}
    (hr : engineReplay h s = some t) (hne : t.regime ≠ s.regime) :
    SecondRun.Run.elems (sourceState s).regime < SecondRun.Run.elems (sourceState t).regime :=
  SecondRun.Run.ereplay_elems_lt_of_ne (h.map sourceEvent) (engine_replay_source hr)
    (fun he => hne (source_regime_injective he))

theorem two_switches_return (s : EngineState) : engineReplay [.switch,.switch] s = some s := by
  cases s; simp [engineReplay,engineStep]

end GenesisNoReturn

#print axioms GenesisNoReturn.decode_encode
#print axioms GenesisNoReturn.encode_decode
#print axioms GenesisNoReturn.array_step_commutes
#print axioms GenesisNoReturn.array_replay_exact
#print axioms GenesisNoReturn.array_failure_exact
#print axioms GenesisNoReturn.second_step_commutes
#print axioms GenesisNoReturn.engine_step_commutes
#print axioms GenesisNoReturn.engine_replay_commutes
#print axioms GenesisNoReturn.engine_replay_failure_exact
#print axioms GenesisNoReturn.engine_replay_source
#print axioms GenesisNoReturn.no_return
#print axioms GenesisNoReturn.cycle_regime_const
#print axioms GenesisNoReturn.strict_potential
#print axioms GenesisNoReturn.two_switches_return

#print axioms GenesisNoReturn.source_array
#print axioms GenesisNoReturn.array_source
#print axioms GenesisNoReturn.sourceState_injective
#print axioms GenesisNoReturn.engine_replay_exact

#print axioms GenesisNoReturn.sourceEvent_arrayEvent
#print axioms GenesisNoReturn.arrayEvent_sourceEvent

#print axioms GenesisNoReturn.cumulative_potential
