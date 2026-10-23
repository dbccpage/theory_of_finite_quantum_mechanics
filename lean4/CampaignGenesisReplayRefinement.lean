import Mathlib.Tactic.SplitIfs
import GenesisComputation
import Derivation.Erasure
import Derivation.Inertia
import SecondRun.Run

/-!
AuthorityEffect: None. Exact representation of the five-field sealed regime,
its partial transition function and every finite history. The source Basic
module is the blob at sealed-derivation-v1, 3100c4e, compiled from the immutable
atlas archive. This is a mathematical representation theorem, not a theorem
about execution of the CPython or Rust runtimes.
-/

namespace CampaignGenesisReplayRefinement


def sourceRegime (r : GenesisComputation.GenesisCopy.Regime) : Derivation.Regime :=
  ⟨r.data, r.forms, r.insts, r.rules, r.reqs⟩

def copyRegime (r : Derivation.Regime) : GenesisComputation.GenesisCopy.Regime :=
  ⟨r.data, r.forms, r.insts, r.rules, r.reqs⟩

def sourceEvent : GenesisComputation.GenesisCopy.Event → Derivation.Event
  | .supply t => .supply t
  | .admitDatum => .admitDatum
  | .admitForm a => .admitForm a
  | .admitInst f xs => .admitInst f xs
  | .admitRuleAll f => .admitRuleAll f
  | .impose i j => .impose i j

def copyEvent : Derivation.Event → GenesisComputation.GenesisCopy.Event
  | .supply t => .supply t
  | .admitDatum => .admitDatum
  | .admitForm a => .admitForm a
  | .admitInst f xs => .admitInst f xs
  | .admitRuleAll f => .admitRuleAll f
  | .impose i j => .impose i j

@[simp] theorem source_copy (r : Derivation.Regime) : sourceRegime (copyRegime r) = r := by
  cases r; rfl

@[simp] theorem copy_source (r : GenesisComputation.GenesisCopy.Regime) : copyRegime (sourceRegime r) = r := by
  cases r; rfl

@[simp] theorem source_copy_event (e : Derivation.Event) : sourceEvent (copyEvent e) = e := by
  cases e <;> rfl

@[simp] theorem copy_source_event (e : GenesisComputation.GenesisCopy.Event) : copyEvent (sourceEvent e) = e := by
  cases e <;> rfl

theorem sourceRegime_injective : Function.Injective sourceRegime :=
  Function.LeftInverse.injective copy_source

/-- Includes the `none` branch of every guard; no success premise is needed. -/
theorem copy_step_commutes (r : GenesisComputation.GenesisCopy.Regime) (e : GenesisComputation.GenesisCopy.Event) :
    (GenesisComputation.GenesisCopy.stepE r e).map sourceRegime = Derivation.stepE (sourceRegime r) (sourceEvent e) := by
  cases e with
  | supply t => rfl
  | admitDatum => rfl
  | admitForm a =>
      by_cases h : 1 ≤ a
      all_goals simp [GenesisComputation.GenesisCopy.stepE, Derivation.stepE, sourceRegime, sourceEvent, GenesisComputation.GenesisCopy.insertNew, Derivation.insertNew, h] <;> split_ifs <;> simp_all
  | admitInst f xs =>
      by_cases h : f < r.forms.length ∧ xs.length = r.forms.getD f 0 ∧ (∀ x ∈ xs, x < r.data)
      all_goals simp [GenesisComputation.GenesisCopy.stepE, Derivation.stepE, sourceRegime, sourceEvent, GenesisComputation.GenesisCopy.insertNew, Derivation.insertNew, h] <;> split_ifs <;> simp_all
  | admitRuleAll f =>
      by_cases h : f < r.forms.length
      all_goals simp [GenesisComputation.GenesisCopy.stepE, Derivation.stepE, sourceRegime, sourceEvent, GenesisComputation.GenesisCopy.insertNew, Derivation.insertNew, h] <;> split_ifs <;> simp_all
  | impose i j =>
      by_cases h : i < j ∧ j < r.data
      all_goals simp [GenesisComputation.GenesisCopy.stepE, Derivation.stepE, sourceRegime, sourceEvent, GenesisComputation.GenesisCopy.insertNew, Derivation.insertNew, h] <;> split_ifs <;> simp_all

theorem copy_replay_commutes (h : List GenesisComputation.GenesisCopy.Event) (r : GenesisComputation.GenesisCopy.Regime) :
    (GenesisComputation.GenesisCopy.replayE h r).map sourceRegime = Derivation.replayE (h.map sourceEvent) (sourceRegime r) := by
  induction h generalizing r with
  | nil => rfl
  | cons e h ih =>
      have hs := copy_step_commutes r e
      simp only [List.map_cons, Derivation.replayE_cons]
      have hc : GenesisComputation.GenesisCopy.replayE (e :: h) r = (GenesisComputation.GenesisCopy.stepE r e).bind (GenesisComputation.GenesisCopy.replayE h) := by
        unfold GenesisComputation.GenesisCopy.replayE
        cases hx : GenesisComputation.GenesisCopy.stepE r e <;> simp [List.foldlM, hx]
      rw [hc]
      cases hx : GenesisComputation.GenesisCopy.stepE r e with
      | none => simp [hx] at hs; simp [hx, ← hs]
      | some t => simp [hx] at hs; simpa [← hs] using ih t

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

def isSupply : Derivation.Event → Bool
  | .supply _ => true
  | _ => false

theorem source_supply_no_op (r : Derivation.Regime) (t : Nat) :
    Derivation.stepE r (.supply t) = some r := rfl

theorem array_supply_no_op (r : ArrayRegime) (t : Nat) :
    arrayStep r (.supply t) = some r := rfl

/-- Erasing presentation events preserves failure, not only successful regimes. -/
theorem source_supply_erasure (h : List Derivation.Event) (r : Derivation.Regime) :
    Derivation.replayE (h.filter (fun e => !isSupply e)) r = Derivation.replayE h r := by
  induction h generalizing r with
  | nil => rfl
  | cons e h ih =>
      by_cases he : isSupply e = true
      · have hs : Derivation.stepE r e = some r := by
          cases e <;> simp_all [isSupply, Derivation.stepE]
        simp [List.filter, he, Derivation.replayE_cons, hs, ih]
      · have hf : isSupply e = false := Bool.eq_false_iff.mpr he
        simp only [List.filter, hf, Bool.not_false,
          Derivation.replayE_cons]
        cases hs : Derivation.stepE r e <;> simp [ih]

theorem array_supply_erasure (h : List Derivation.Event) (r : ArrayRegime) :
    arrayReplay (h.filter (fun e => !isSupply e)) r = arrayReplay h r := by
  apply Option.map_injective decode_injective
  rw [array_replay_commutes, array_replay_commutes, source_supply_erasure]

/-- A duplicate token admission is erased state-dependently as supply. -/
theorem token_array_replay (h : List Derivation.TEvent) (t : Derivation.TRegime) :
    arrayReplay (Derivation.eraseHistory t h) (encode t.erase) =
      ((Derivation.replayT h t).map Derivation.TRegime.erase).map encode := by
  apply Option.map_injective decode_injective
  rw [array_replay_commutes, decode_encode, Derivation.erase_replay]
  cases Derivation.replayE (Derivation.eraseHistory t h) t.erase <;> simp

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

theorem source_step_nondecreasing {r s : Derivation.Regime} {e : Derivation.Event}
    (h : Derivation.stepE r e = some s) : potential r ≤ potential s := by
  have hs : SecondRun.Sealed.stepE (secondRegime r) (secondEvent e) = some (secondRegime s) := by
    rw [← second_step_commutes, h]; rfl
  exact SecondRun.Run.stepE_elems_le hs

theorem source_change_strict {r s : Derivation.Regime} {e : Derivation.Event}
    (h : Derivation.stepE r e = some s) (hne : s ≠ r) : potential r < potential s := by
  have hs : SecondRun.Sealed.stepE (secondRegime r) (secondEvent e) = some (secondRegime s) := by
    rw [← second_step_commutes, h]; rfl
  exact SecondRun.Run.stepE_elems_lt_of_ne hs (fun he => hne (secondRegime_injective he))

/-- Both declared readings are retained, with all requirement coordinates. -/
theorem reading_arrays :
    encode Derivation.R2L = ⟨2, #[], #[], #[], #[(0, 1)]⟩ ∧
    encode Derivation.R2F = ⟨3, #[], #[], #[], #[(1, 2)]⟩ := by decide

theorem invalid_after_supply :
    Derivation.replayE [.supply 9, .admitForm 0, .admitDatum] Derivation.R2L = none := by decide

end CampaignGenesisReplayRefinement

#print axioms CampaignGenesisReplayRefinement.source_copy
#print axioms CampaignGenesisReplayRefinement.copy_source
#print axioms CampaignGenesisReplayRefinement.source_copy_event
#print axioms CampaignGenesisReplayRefinement.copy_source_event
#print axioms CampaignGenesisReplayRefinement.sourceRegime_injective
#print axioms CampaignGenesisReplayRefinement.copy_step_commutes
#print axioms CampaignGenesisReplayRefinement.copy_replay_commutes
#print axioms CampaignGenesisReplayRefinement.decode_encode
#print axioms CampaignGenesisReplayRefinement.encode_decode
#print axioms CampaignGenesisReplayRefinement.decode_injective
#print axioms CampaignGenesisReplayRefinement.arrayInsert_toList
#print axioms CampaignGenesisReplayRefinement.array_step_commutes
#print axioms CampaignGenesisReplayRefinement.array_replay_commutes
#print axioms CampaignGenesisReplayRefinement.array_replay_exact
#print axioms CampaignGenesisReplayRefinement.array_failure_exact
#print axioms CampaignGenesisReplayRefinement.source_supply_no_op
#print axioms CampaignGenesisReplayRefinement.array_supply_no_op
#print axioms CampaignGenesisReplayRefinement.source_supply_erasure
#print axioms CampaignGenesisReplayRefinement.array_supply_erasure
#print axioms CampaignGenesisReplayRefinement.token_array_replay
#print axioms CampaignGenesisReplayRefinement.secondRegime_injective
#print axioms CampaignGenesisReplayRefinement.second_step_commutes
#print axioms CampaignGenesisReplayRefinement.source_step_nondecreasing
#print axioms CampaignGenesisReplayRefinement.source_change_strict
#print axioms CampaignGenesisReplayRefinement.reading_arrays
#print axioms CampaignGenesisReplayRefinement.invalid_after_supply
#print axioms Derivation.erase_step
#print axioms Derivation.erase_replay
