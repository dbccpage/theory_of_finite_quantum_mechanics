import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Exact partial-step simulation lifts to every encoded
word; extension mode preserves old steps and explicitly permits added availability.
Rust finite carrier/map/macro admission and cell estimates remain separate. -/
namespace TFQM.FiniteSimulation

variable {S T I J : Type}

def run (step : S → I → Option S) (s : S) : List I → Option S
  | [] => some s
  | a :: w => (step s a).bind (fun t => run step t w)

theorem run_empty (step : S → I → Option S) (s : S) : run step s [] = some s := rfl

theorem run_unavailable (step : S → I → Option S) (s : S) (a : I) (w : List I)
    (missing : step s a = none) : run step s (a :: w) = none := by simp [run, missing]

theorem run_append (step : S → I → Option S) (s : S) (u v : List I) :
    run step s (u ++ v) = (run step s u).bind (fun t => run step t v) := by
  induction u generalizing s with
  | nil => rfl
  | cons a u ih =>
    cases h : step s a <;> simp [run, h, ih]

theorem exact_macro_words (source : S → I → Option S) (target : T → J → Option T)
    (map : S → T) (encode : I → List J)
    (steps : ∀ s a, (source s a).map map = run target (map s) (encode a))
    (s : S) (w : List I) :
    (run source s w).map map = run target (map s) (w.flatMap encode) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
    cases h : source s a with
    | none =>
      have ht : run target (map s) (encode a) = none := by
        simpa [h] using (steps s a).symm
      simp [run, List.flatMap_cons, run_append, h, ht]
    | some next =>
      have ht : run target (map s) (encode a) = some (map next) := by
        simpa [h] using (steps s a).symm
      simp [run, List.flatMap_cons, run_append, h, ht, ih]

def Allowed (extension : Bool) (expected actual : Option T) : Prop :=
  expected = actual ∨ (extension = true ∧ expected = none ∧ actual ≠ none)

theorem exact_iff (expected actual : Option T) :
    Allowed false expected actual ↔ expected = actual := by simp [Allowed]

theorem extension_preserves_defined (t : T) (actual : Option T)
    (h : Allowed true (some t) actual) : actual = some t := by
  rcases h with h | ⟨_, impossible, _⟩
  · exact h.symm
  · cases impossible

theorem extension_absent (actual : Option T) : Allowed true none actual := by
  cases actual <;> simp [Allowed]

theorem extension_does_not_drop (t : T) : ¬ Allowed true (some t) none := by
  simp [Allowed]

theorem extension_does_not_change (a b : T) (ne : a ≠ b) :
    ¬ Allowed true (some a) (some b) := by simp [Allowed, ne]

def added (extension : Bool) (expected actual : Option T) : Prop :=
  extension = true ∧ expected = none ∧ actual ≠ none

theorem added_is_allowed (extension : Bool) (expected actual : Option T)
    (h : added extension expected actual) : Allowed extension expected actual := Or.inr h

theorem added_changes_availability (extension : Bool) (expected actual : Option T)
    (h : added extension expected actual) : expected = none ∧ actual ≠ none := ⟨h.2.1, h.2.2⟩

inductive Refusal where
  | invalidMap | invalidEncoding | workLimit
  deriving DecidableEq

def admission (mapOK encodingOK budgetOK : Bool) : Option Refusal :=
  if !mapOK then some .invalidMap
  else if !encodingOK then some .invalidEncoding
  else if !budgetOK then some .workLimit
  else none

theorem map_first (e b : Bool) : admission false e b = some .invalidMap := by simp [admission]
theorem encoding_second (b : Bool) : admission true false b = some .invalidEncoding := by simp [admission]
theorem budget_third : admission true true false = some .workLimit := by simp [admission]
theorem admission_success (m e b : Bool) :
    admission m e b = none ↔ m = true ∧ e = true ∧ b = true := by
  cases m <;> cases e <;> cases b <;> simp [admission]

def replay [DecidableEq T] (expected supplied : T) : Bool := decide (expected = supplied)
theorem replay_success [DecidableEq T] (expected supplied : T) :
    replay expected supplied = true ↔ expected = supplied := by simp [replay]

end TFQM.FiniteSimulation

#print axioms TFQM.FiniteSimulation.run_empty
#print axioms TFQM.FiniteSimulation.run_unavailable
#print axioms TFQM.FiniteSimulation.run_append
#print axioms TFQM.FiniteSimulation.exact_macro_words
#print axioms TFQM.FiniteSimulation.exact_iff
#print axioms TFQM.FiniteSimulation.extension_preserves_defined
#print axioms TFQM.FiniteSimulation.extension_absent
#print axioms TFQM.FiniteSimulation.extension_does_not_drop
#print axioms TFQM.FiniteSimulation.extension_does_not_change
#print axioms TFQM.FiniteSimulation.added_is_allowed
#print axioms TFQM.FiniteSimulation.added_changes_availability
#print axioms TFQM.FiniteSimulation.map_first
#print axioms TFQM.FiniteSimulation.encoding_second
#print axioms TFQM.FiniteSimulation.budget_third
#print axioms TFQM.FiniteSimulation.admission_success
#print axioms TFQM.FiniteSimulation.replay_success
