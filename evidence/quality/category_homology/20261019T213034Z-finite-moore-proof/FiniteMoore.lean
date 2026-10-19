import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Actual all-word total Moore behavior and greatest
readout congruence as a stable finite-depth refinement,plus surjective factor
uniqueness. Rust canonical IDs,finite strict-split termination,chain/storage
replay and disjoint-union implementation are refined separately. -/
namespace TFQM.FiniteMoore

variable {S A R T Q : Type}

def run (step : S → A → S) : S → List A → S
  | state, [] => state
  | state, a :: word => run step (step state a) word

theorem run_append (step : S → A → S) (state : S) (first second : List A) :
    run step state (first ++ second) = run step (run step state first) second := by
  induction first generalizing state with
  | nil => rfl
  | cons a word ih => exact ih (step state a)

def FutureEqual (step : S → A → S) (report : S → R) (x y : S) : Prop :=
  ∀ word, report (run step x word) = report (run step y word)

theorem future_refl (step : S → A → S) (report : S → R) (x : S) :
    FutureEqual step report x x := fun _ => rfl

theorem future_symm (step : S → A → S) (report : S → R) (x y : S)
    (h : FutureEqual step report x y) : FutureEqual step report y x := fun word => (h word).symm

theorem future_trans (step : S → A → S) (report : S → R) (x y z : S)
    (h : FutureEqual step report x y) (k : FutureEqual step report y z) :
    FutureEqual step report x z := fun word => (h word).trans (k word)

theorem future_congruence (step : S → A → S) (report : S → R) (x y : S)
    (h : FutureEqual step report x y) :
    report x = report y ∧ ∀ a, FutureEqual step report (step x a) (step y a) :=
  ⟨h [], fun a word => h (a :: word)⟩

theorem congruence_future (step : S → A → S) (report : S → R) (rel : S → S → Prop)
    (compatible : ∀ x y, rel x y → report x = report y ∧ ∀ a, rel (step x a) (step y a))
    (x y : S) (h : rel x y) : FutureEqual step report x y := by
  intro word
  induction word generalizing x y with
  | nil => exact (compatible x y h).1
  | cons a word ih => exact ih _ _ ((compatible x y h).2 a)

def depth (step : S → A → S) (report : S → R) : Nat → S → S → Prop
  | 0, x, y => report x = report y
  | k + 1, x, y => depth step report k x y ∧ ∀ a, depth step report k (step x a) (step y a)

theorem depth_refines (step : S → A → S) (report : S → R) (k : Nat) (x y : S)
    (h : depth step report (k + 1) x y) : depth step report k x y := h.1

theorem depth_readout (step : S → A → S) (report : S → R) (k : Nat) (x y : S)
    (h : depth step report k x y) : report x = report y := by
  induction k with
  | zero => exact h
  | succ k ih => exact ih h.1

theorem future_in_depth (step : S → A → S) (report : S → R) (k : Nat) (x y : S)
    (h : FutureEqual step report x y) : depth step report k x y := by
  induction k generalizing x y with
  | zero => exact h []
  | succ k ih => exact ⟨ih _ _ h, fun a => ih _ _ ((future_congruence step report x y h).2 a)⟩

theorem fixed_point_exact (step : S → A → S) (report : S → R) (k : Nat)
    (stable : ∀ x y, depth step report (k + 1) x y ↔ depth step report k x y) (x y : S) :
    depth step report k x y ↔ FutureEqual step report x y := by
  constructor
  · intro h
    exact congruence_future step report (depth step report k)
      (fun a b related => ⟨depth_readout step report k a b related, ((stable a b).mpr related).2⟩) x y h
  · exact future_in_depth step report k x y

theorem preserving_run (source : S → A → S) (target : T → A → T) (f : S → T)
    (preserves : ∀ s a, f (source s a) = target (f s) a) (s : S) (word : List A) :
    f (run source s word) = run target (f s) word := by
  induction word generalizing s with
  | nil => rfl
  | cons a word ih => exact (ih (source s a)).trans (congrArg (fun t => run target t word) (preserves s a))

theorem map_kernel_future (source : S → A → S) (target : T → A → T)
    (sourceReport : S → R) (targetReport : T → R) (f : S → T)
    (updates : ∀ s a, f (source s a) = target (f s) a)
    (reports : ∀ s, sourceReport s = targetReport (f s)) (x y : S) (same : f x = f y) :
    FutureEqual source sourceReport x y := by
  intro word
  rw [reports, reports, preserving_run source target f updates, preserving_run source target f updates, same]

noncomputable def factor (f : S → T) (onto : Function.Surjective f) (q : S → Q) (t : T) : Q :=
  q (Classical.choose (onto t))

theorem factor_spec (f : S → T) (onto : Function.Surjective f) (q : S → Q)
    (constant : ∀ x y, f x = f y → q x = q y) (s : S) :
    factor f onto q (f s) = q s := constant _ _ (Classical.choose_spec (onto (f s)))

theorem factor_unique (f : S → T) (onto : Function.Surjective f) (q : S → Q)
    (g h : T → Q) (left : ∀ s, g (f s) = q s) (right : ∀ s, h (f s) = q s) : g = h := by
  funext t
  obtain ⟨s, rfl⟩ := onto t
  exact (left s).trans (right s).symm

theorem split_counter_bound (before after states : Nat)
    (strict : before < after) (bounded : after ≤ states) : before + 1 ≤ states :=
  Nat.le_trans (Nat.succ_le_of_lt strict) bounded

end TFQM.FiniteMoore

#print axioms TFQM.FiniteMoore.run_append
#print axioms TFQM.FiniteMoore.future_refl
#print axioms TFQM.FiniteMoore.future_symm
#print axioms TFQM.FiniteMoore.future_trans
#print axioms TFQM.FiniteMoore.future_congruence
#print axioms TFQM.FiniteMoore.congruence_future
#print axioms TFQM.FiniteMoore.depth_refines
#print axioms TFQM.FiniteMoore.depth_readout
#print axioms TFQM.FiniteMoore.future_in_depth
#print axioms TFQM.FiniteMoore.fixed_point_exact
#print axioms TFQM.FiniteMoore.preserving_run
#print axioms TFQM.FiniteMoore.map_kernel_future
#print axioms TFQM.FiniteMoore.factor
#print axioms TFQM.FiniteMoore.factor_spec
#print axioms TFQM.FiniteMoore.factor_unique
#print axioms TFQM.FiniteMoore.split_counter_bound
