/- Conditional policy-evaluation laws. AuthorityEffect: None.
   No source authenticity or signed-matrix identities are assumed proved here.
   The executable bridge checks those identities on its exact finite inputs. -/
import Std

namespace WitnessedDifference.PolicyObserverAdapter

universe u v w

def LowerBound {A : Type u} {V : Type v}
    (le : V → V → Prop) (cost : A → V) (value : V) : Prop :=
  ∀ a, le value (cost a)

def IsInfimum {A : Type u} {V : Type v}
    (le : V → V → Prop) (cost : A → V) (value : V) : Prop :=
  LowerBound le cost value ∧ ∀ lower, LowerBound le cost lower → le lower value

/-- A surjective repair reindexing leaves the lower bounds unchanged. -/
theorem lowerBound_reindex_iff
    {A : Type u} {V : Type v} (le : V → V → Prop) (cost : A → V)
    (f : A → A) (onto : ∀ b, ∃ a, f a = b) (value : V) :
    LowerBound le (fun a => cost (f a)) value ↔ LowerBound le cost value := by
  constructor
  · intro bound b
    obtain ⟨a, ha⟩ := onto b
    rw [← ha]
    exact bound a
  · intro bound a
    exact bound (f a)

/-- The infimum law needs neither norm separation nor a chosen minimizer. -/
theorem infimum_reindex_iff
    {A : Type u} {V : Type v} (le : V → V → Prop) (cost : A → V)
    (f : A → A) (onto : ∀ b, ∃ a, f a = b) (value : V) :
    IsInfimum le (fun a => cost (f a)) value ↔ IsInfimum le cost value := by
  constructor
  · intro h
    constructor
    · exact (lowerBound_reindex_iff le cost f onto value).mp h.1
    · intro lower bound
      exact h.2 lower ((lowerBound_reindex_iff le cost f onto lower).mpr bound)
  · intro h
    constructor
    · exact (lowerBound_reindex_iff le cost f onto value).mpr h.1
    · intro lower bound
      exact h.2 lower ((lowerBound_reindex_iff le cost f onto lower).mp bound)

theorem infimum_unique
    {A : Type u} {V : Type v} (le : V → V → Prop)
    (antisymm : ∀ a b, le a b → le b a → a = b)
    (cost : A → V) (a b : V)
    (ha : IsInfimum le cost a) (hb : IsInfimum le cost b) : a = b := by
  exact antisymm a b (hb.2 a ha.1) (ha.2 b hb.1)

/-- If gauge transport bijects repairs and preserves their costs, the actual
    two quotient evaluations agree. A status follows only through declared T. -/
theorem gauge_evaluation_invariant
    {A : Type u} {V : Type v} (le : V → V → Prop)
    (antisymm : ∀ a b, le a b → le b a → a = b)
    (cost transformedCost : A → V) (f : A → A)
    (onto : ∀ b, ∃ a, f a = b)
    (equivariant : ∀ a, transformedCost a = cost (f a))
    (originalValue transformedValue : V)
    (original : IsInfimum le cost originalValue)
    (transformed : IsInfimum le transformedCost transformedValue) :
    originalValue = transformedValue := by
  have heq : transformedCost = (fun a => cost (f a)) := funext equivariant
  rw [heq] at transformed
  have reindexed := (infimum_reindex_iff le cost f onto transformedValue).mp transformed
  exact infimum_unique le antisymm cost originalValue transformedValue original reindexed

theorem status_requires_declared_terminalizer
    {V : Type u} {S : Type v} (terminal : V → S) (a b : V) (same : a = b) :
    terminal a = terminal b := congrArg terminal same

/-- Common carrier/evaluator data cannot determine an undeclared terminal rule.
    This is a quantified no-default theorem, not a status-label convention. -/
theorem no_terminal_default :
    ¬ ∃ infer : Unit → Bool, ∀ declared : Unit → Bool,
      ∀ value, infer value = declared value := by
  intro h
  obtain ⟨infer, uniform⟩ := h
  have left := uniform (fun _ => false) ()
  have right := uniform (fun _ => true) ()
  have impossible : false = true := left.symm.trans right
  cases impossible

def directedComparison (a b : Bool) : Prop := a = false ∧ b = true

/-- The reverse edge accepted by symmetric closure is absent from the actual
    declared relation. The Python/native store bridge must not add that edge. -/
theorem symmetrization_changes_declared_comparison :
    (directedComparison true false ∨ directedComparison false true) ∧
      ¬ directedComparison true false := by
  simp [directedComparison]

theorem reflexivization_changes_declared_comparison :
    false = false ∧ ¬ directedComparison false false := by
  simp [directedComparison]

#print axioms lowerBound_reindex_iff
#print axioms infimum_reindex_iff
#print axioms infimum_unique
#print axioms gauge_evaluation_invariant
#print axioms status_requires_declared_terminalizer
#print axioms no_terminal_default
#print axioms symmetrization_changes_declared_comparison
#print axioms reflexivization_changes_declared_comparison

end WitnessedDifference.PolicyObserverAdapter
