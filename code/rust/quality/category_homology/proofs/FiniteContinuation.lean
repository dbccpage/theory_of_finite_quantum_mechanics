import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. All-word partial dynamics,observable absorbing sink,
closed pair exploration,replay and bounded charge. Rust FIFO/first-discovery
shortest ordering,finite Moore refinement and predecessor storage are separate. -/
namespace TFQM.FiniteContinuation

variable {S A R : Type}

def next (step : S → A → Option S) (state : Option S) (input : A) : Option S :=
  state.bind fun s => step s input

def run (step : S → A → Option S) : Option S → List A → Option S
  | state, [] => state
  | state, input :: word => run step (next step state input) word

def observe (report : S → R) (state : Option S) : Option R := state.map report

theorem run_empty (step : S → A → Option S) (state : Option S) :
    run step state [] = state := rfl

theorem next_unavailable (step : S → A → Option S) (input : A) :
    next step none input = none := rfl

theorem run_unavailable (step : S → A → Option S) (word : List A) :
    run step none word = none := by
  induction word with
  | nil => rfl
  | cons a word ih => exact ih

theorem run_append (step : S → A → Option S) (state : Option S) (first second : List A) :
    run step state (first ++ second) = run step (run step state first) second := by
  induction first generalizing state with
  | nil => rfl
  | cons a word ih => exact ih (next step state a)

theorem sink_observably_distinct (report : S → R) (state : S) :
    observe report none ≠ observe report (some state) := by simp [observe]

def FutureEqual (step : S → A → Option S) (report : S → R) (left right : Option S) : Prop :=
  ∀ word, observe report (run step left word) = observe report (run step right word)

theorem future_refl (step : S → A → Option S) (report : S → R) (state : Option S) :
    FutureEqual step report state state := fun _ => rfl

theorem future_symm (step : S → A → Option S) (report : S → R) (left right : Option S)
    (h : FutureEqual step report left right) : FutureEqual step report right left :=
  fun word => (h word).symm

theorem future_trans (step : S → A → Option S) (report : S → R) (left middle right : Option S)
    (h : FutureEqual step report left middle) (k : FutureEqual step report middle right) :
    FutureEqual step report left right := fun word => (h word).trans (k word)

theorem closed_pairs_no_distinction (step : S → A → Option S) (report : S → R)
    (seen : Option S → Option S → Prop)
    (closed : ∀ l r, seen l r → ∀ a, seen (next step l a) (next step r a))
    (equal : ∀ l r, seen l r → observe report l = observe report r)
    (left right : Option S) (start : seen left right) : FutureEqual step report left right := by
  intro word
  have invariant : ∀ word l r, seen l r → seen (run step l word) (run step r word) := by
    intro word
    induction word with
    | nil => exact fun _ _ h => h
    | cons a word ih => exact fun l r h => ih _ _ (closed l r h a)
  exact equal _ _ (invariant word left right start)

def ReplayOK (step : S → A → Option S) (report : S → R)
    (left right : Option S) (word : List A) (savedLeft savedRight : Option R) : Prop :=
  observe report (run step left word) ≠ observe report (run step right word) ∧
  observe report (run step left word) = savedLeft ∧
  observe report (run step right word) = savedRight

theorem replay_distinguishes (step : S → A → Option S) (report : S → R)
    (left right : Option S) (word : List A) (savedLeft savedRight : Option R)
    (h : ReplayOK step report left right word savedLeft savedRight) :
    ¬FutureEqual step report left right := fun equal => h.1 (equal word)

theorem replay_saved_answers (step : S → A → Option S) (report : S → R)
    (left right : Option S) (word : List A) (savedLeft savedRight : Option R)
    (h : ReplayOK step report left right word savedLeft savedRight) :
    savedLeft ≠ savedRight := by
  intro same
  exact h.1 (h.2.1.trans (same.trans h.2.2.symm))

theorem predecessor_length (word : List A) (input : A) :
    (word ++ [input]).length = word.length + 1 := by simp

def charge (seen maximum : Nat) : Option Nat :=
  if seen < maximum then some (seen + 1) else none

theorem charge_success (seen maximum : Nat) (room : seen < maximum) :
    charge seen maximum = some (seen + 1) := by simp [charge, room]

theorem charge_refused (seen maximum : Nat) (full : maximum ≤ seen) :
    charge seen maximum = none := by simp [charge, Nat.not_lt.mpr full]

theorem charge_bounded (seen maximum : Nat) (room : seen < maximum) :
    seen + 1 ≤ maximum := Nat.succ_le_of_lt room

end TFQM.FiniteContinuation

#print axioms TFQM.FiniteContinuation.run_empty
#print axioms TFQM.FiniteContinuation.next_unavailable
#print axioms TFQM.FiniteContinuation.run_unavailable
#print axioms TFQM.FiniteContinuation.run_append
#print axioms TFQM.FiniteContinuation.sink_observably_distinct
#print axioms TFQM.FiniteContinuation.future_refl
#print axioms TFQM.FiniteContinuation.future_symm
#print axioms TFQM.FiniteContinuation.future_trans
#print axioms TFQM.FiniteContinuation.closed_pairs_no_distinction
#print axioms TFQM.FiniteContinuation.replay_distinguishes
#print axioms TFQM.FiniteContinuation.replay_saved_answers
#print axioms TFQM.FiniteContinuation.predecessor_length
#print axioms TFQM.FiniteContinuation.charge_success
#print axioms TFQM.FiniteContinuation.charge_refused
#print axioms TFQM.FiniteContinuation.charge_bounded
