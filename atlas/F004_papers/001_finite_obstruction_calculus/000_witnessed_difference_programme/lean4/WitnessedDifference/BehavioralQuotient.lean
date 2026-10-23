/-!
# Behavioral quotients from finite context words

For a declared total deterministic action and a declared readout, two states
are behaviorally equivalent precisely when every finite context word has the
same readout from both states. This is the greatest context-invariant relation
contained in immediate readout equality. It is an equivalence relation and
therefore supplies a genuine quotient with a well-defined action and readout.

The quotient is coarsest among readout-respecting transition congruences: every
other such quotient has a unique comparison map to it. The order direction is
intentional. This is not the initiality conjecture for constructor increments
in WDP-CH04-O01. No chronology, metric tolerance, convergence, or finite
algorithmic stabilization bound is assumed or derived here. Context words are
finite generated terms; the state, context, and readout types may be arbitrary.
-/

namespace WitnessedDifference.BehavioralQuotient

universe u v w

/-- Execute a word from left to right, with its head acting first. -/
def run {State : Type u} {Context : Type v}
    (action : Context → State → State) : List Context → State → State
  | [], x => x
  | c :: word, x => run action word (action c x)

/-- Equality of all finite-word readouts, including the empty word. -/
def BehavioralEq {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (x y : State) : Prop :=
  ∀ word : List Context, observe (run action word x) = observe (run action word y)

/-- Immediate observation equality is the empty-word instance. -/
theorem behavioral_eq_observation
    {State : Type u} {Context : Type v} {Readout : Type w}
    {action : Context → State → State} {observe : State → Readout}
    {x y : State} (h : BehavioralEq action observe x y) : observe x = observe y :=
  h []

/-- Behavioral equivalence is preserved by each declared context. -/
theorem behavioral_eq_action
    {State : Type u} {Context : Type v} {Readout : Type w}
    {action : Context → State → State} {observe : State → Readout}
    {x y : State} (h : BehavioralEq action observe x y) (c : Context) :
    BehavioralEq action observe (action c x) (action c y) := by
  intro word
  exact h (c :: word)

/-- Any relation respecting immediate readout and every context lies inside
behavioral equivalence. The candidate relation need not itself be an
equivalence relation. -/
theorem greatest_invariant_relation
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : State → State → Prop)
    (hobserve : ∀ x y, R x y → observe x = observe y)
    (haction : ∀ c x y, R x y → R (action c x) (action c y)) :
    ∀ x y, R x y → BehavioralEq action observe x y := by
  intro x y hxy word
  induction word generalizing x y with
  | nil => exact hobserve x y hxy
  | cons c word ih => exact ih (action c x) (action c y) (haction c x y hxy)

/-- Behavioral equality restricted to words of length at most `depth`. -/
def BoundedBehavioralEq {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (depth : Nat) (x y : State) : Prop :=
  ∀ word : List Context, word.length ≤ depth →
    observe (run action word x) = observe (run action word y)

/-- Depth zero tests only the immediate readout. -/
theorem bounded_zero_iff_observation
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) (x y : State) :
    BoundedBehavioralEq action observe 0 x y ↔ observe x = observe y := by
  constructor
  · intro h
    exact h [] (Nat.le_refl 0)
  · intro h word hlength
    cases word with
    | nil => exact h
    | cons c word => exact False.elim (Nat.not_succ_le_zero word.length hlength)

/-- A refinement step tests the old readout and every one-context successor
through the preceding depth. This is the finite-word semantic recurrence. -/
theorem bounded_succ_iff
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (depth : Nat) (x y : State) :
    BoundedBehavioralEq action observe (depth + 1) x y ↔
      observe x = observe y ∧
      ∀ c, BoundedBehavioralEq action observe depth (action c x) (action c y) := by
  constructor
  · intro h
    refine ⟨h [] (Nat.zero_le (depth + 1)), ?_⟩
    intro c word hlength
    exact h (c :: word) (Nat.succ_le_succ hlength)
  · intro h word hlength
    cases word with
    | nil => exact h.1
    | cons c word => exact h.2 c word (Nat.le_of_succ_le_succ hlength)

/-- Unbounded behavior implies every bounded test. -/
theorem behavioral_eq_implies_bounded
    {State : Type u} {Context : Type v} {Readout : Type w}
    {action : Context → State → State} {observe : State → Readout}
    {x y : State} (h : BehavioralEq action observe x y) (depth : Nat) :
    BoundedBehavioralEq action observe depth x y := by
  intro word _
  exact h word

/-- If a bounded relation has stabilized under one further refinement, it
already agrees with all finite-word behavior. This proves stabilization
correctness when supplied; it does not assume finiteness or bound its time. -/
theorem stabilized_bounded_relation_iff_behavioral
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) (depth : Nat)
    (hstable : ∀ x y, BoundedBehavioralEq action observe depth x y →
      BoundedBehavioralEq action observe (depth + 1) x y) (x y : State) :
    BoundedBehavioralEq action observe depth x y ↔ BehavioralEq action observe x y := by
  constructor
  · intro hxy
    apply greatest_invariant_relation action observe
      (BoundedBehavioralEq action observe depth) ?_ ?_ x y hxy
    · intro a b hab
      exact hab [] (Nat.zero_le depth)
    · intro c a b hab
      exact ((bounded_succ_iff action observe depth a b).mp (hstable a b hab)).2 c
  · intro hxy
    exact behavioral_eq_implies_bounded hxy depth

/-- Exact readout equality after all words defines an equivalence relation. -/
def behavioralSetoid {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) : Setoid State where
  r := BehavioralEq action observe
  iseqv := {
    refl := fun _ _ => rfl
    symm := fun h word => (h word).symm
    trans := fun hxy hyz word => (hxy word).trans (hyz word)
  }

/-- The canonical behavioral state type. -/
abbrev BehavioralState {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) :=
  Quotient (behavioralSetoid action observe)

/-- Each context descends to behavioral classes. -/
def quotientAction {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (c : Context) : BehavioralState action observe → BehavioralState action observe :=
  Quotient.lift
    (fun x => Quotient.mk (behavioralSetoid action observe) (action c x))
    (fun _ _ h => Quotient.sound (behavioral_eq_action h c))

/-- The readout descends because the empty word is included. -/
def quotientObserve {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) :
    BehavioralState action observe → Readout :=
  Quotient.lift observe (fun _ _ h => behavioral_eq_observation h)

/-- Execution commutes with the quotient map for every finite context word. -/
theorem quotient_run
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (word : List Context) (x : State) :
    run (quotientAction action observe) word
      (Quotient.mk (behavioralSetoid action observe) x) =
      Quotient.mk (behavioralSetoid action observe) (run action word x) := by
  induction word generalizing x with
  | nil => rfl
  | cons c word ih => exact ih (action c x)

/-- Quotient execution retains exactly the declared word readouts. -/
theorem quotient_word_observation
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (word : List Context) (x : State) :
    quotientObserve action observe
      (run (quotientAction action observe) word
        (Quotient.mk (behavioralSetoid action observe) x)) =
      observe (run action word x) := by
  rw [quotient_run]
  rfl

/-- Equality of quotient states is exactly finite-word behavioral equality. -/
theorem quotient_eq_iff_behavioral_eq
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout) (x y : State) :
    Quotient.mk (behavioralSetoid action observe) x =
      Quotient.mk (behavioralSetoid action observe) y ↔ BehavioralEq action observe x y := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Two unequal quotient classes have a finite distinguishing word.
Existence is classical; this theorem supplies no search bound. -/
theorem unequal_classes_have_distinguishing_word
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (x y : State)
    (hne : Quotient.mk (behavioralSetoid action observe) x ≠
      Quotient.mk (behavioralSetoid action observe) y) :
    ∃ word : List Context, observe (run action word x) ≠ observe (run action word y) := by
  apply Classical.byContradiction
  intro hnoword
  apply hne
  apply Quotient.sound
  intro word
  apply Classical.byContradiction
  intro hneword
  exact hnoword ⟨word, hneword⟩

/-- The comparison map from any declared observation-respecting transition
congruence to the behavioral quotient. -/
def comparisonMap
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y)) :
    Quotient R → BehavioralState action observe :=
  Quotient.lift (Quotient.mk (behavioralSetoid action observe))
    (fun x y h => Quotient.sound
      (greatest_invariant_relation action observe R.r hobserve haction x y h))

/-- Action on a separately declared transition congruence quotient. -/
def congruenceAction
    {State : Type u} {Context : Type v}
    (action : Context → State → State) (R : Setoid State)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y))
    (c : Context) : Quotient R → Quotient R :=
  Quotient.lift (fun x => Quotient.mk R (action c x))
    (fun x y h => Quotient.sound (haction c x y h))

/-- Readout on a separately declared observation-respecting quotient. -/
def congruenceObserve
    {State : Type u} {Readout : Type w}
    (observe : State → Readout) (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y) : Quotient R → Readout :=
  Quotient.lift observe hobserve

/-- The canonical comparison is a readout-preserving map. -/
theorem comparison_preserves_readout
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y)) (q : Quotient R) :
    quotientObserve action observe (comparisonMap action observe R hobserve haction q) =
      congruenceObserve observe R hobserve q := by
  refine Quotient.inductionOn q ?_
  intro x
  rfl

/-- The canonical comparison intertwines all context transitions. -/
theorem comparison_intertwines_action
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y))
    (c : Context) (q : Quotient R) :
    comparisonMap action observe R hobserve haction (congruenceAction action R haction c q) =
      quotientAction action observe c (comparisonMap action observe R hobserve haction q) := by
  refine Quotient.inductionOn q ?_
  intro x
  rfl

/-- The comparison map commutes with the source quotient maps. -/
theorem comparison_commutes
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y)) (x : State) :
    comparisonMap action observe R hobserve haction (Quotient.mk R x) =
      Quotient.mk (behavioralSetoid action observe) x := rfl

/-- The comparison is surjective, so the behavioral quotient is coarsest
among the declared congruence quotients. -/
theorem comparison_surjective
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y)) :
    ∀ q : BehavioralState action observe,
      ∃ p : Quotient R, comparisonMap action observe R hobserve haction p = q := by
  intro q
  refine Quotient.inductionOn q ?_
  intro x
  exact ⟨Quotient.mk R x, rfl⟩

/-- Any comparison map commuting with the quotient maps is unique. -/
theorem comparison_unique
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (R : Setoid State)
    (hobserve : ∀ x y, R.r x y → observe x = observe y)
    (haction : ∀ c x y, R.r x y → R.r (action c x) (action c y))
    (g : Quotient R → BehavioralState action observe)
    (hg : ∀ x, g (Quotient.mk R x) = Quotient.mk (behavioralSetoid action observe) x) :
    g = comparisonMap action observe R hobserve haction := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  exact hg x

/-- The behavioral quotient has no distinct behaviorally indistinguishable
states. Readouts after all finite words separate its states. -/
theorem quotient_is_observable
    {State : Type u} {Context : Type v} {Readout : Type w}
    (action : Context → State → State) (observe : State → Readout)
    (p q : BehavioralState action observe)
    (h : BehavioralEq (quotientAction action observe) (quotientObserve action observe) p q) :
    p = q := by
  induction p using Quotient.inductionOn with
  | h x =>
    induction q using Quotient.inductionOn with
    | h y =>
      apply Quotient.sound
      intro word
      have hw := h word
      rw [quotient_word_observation, quotient_word_observation] at hw
      exact hw

end WitnessedDifference.BehavioralQuotient

#print axioms WitnessedDifference.BehavioralQuotient.run
#print axioms WitnessedDifference.BehavioralQuotient.BehavioralEq
#print axioms WitnessedDifference.BehavioralQuotient.BoundedBehavioralEq
#print axioms WitnessedDifference.BehavioralQuotient.BehavioralState
#print axioms WitnessedDifference.BehavioralQuotient.behavioral_eq_observation
#print axioms WitnessedDifference.BehavioralQuotient.behavioral_eq_action
#print axioms WitnessedDifference.BehavioralQuotient.greatest_invariant_relation
#print axioms WitnessedDifference.BehavioralQuotient.bounded_zero_iff_observation
#print axioms WitnessedDifference.BehavioralQuotient.bounded_succ_iff
#print axioms WitnessedDifference.BehavioralQuotient.behavioral_eq_implies_bounded
#print axioms WitnessedDifference.BehavioralQuotient.stabilized_bounded_relation_iff_behavioral
#print axioms WitnessedDifference.BehavioralQuotient.behavioralSetoid
#print axioms WitnessedDifference.BehavioralQuotient.quotientAction
#print axioms WitnessedDifference.BehavioralQuotient.quotientObserve
#print axioms WitnessedDifference.BehavioralQuotient.quotient_run
#print axioms WitnessedDifference.BehavioralQuotient.quotient_word_observation
#print axioms WitnessedDifference.BehavioralQuotient.quotient_eq_iff_behavioral_eq
#print axioms WitnessedDifference.BehavioralQuotient.unequal_classes_have_distinguishing_word
#print axioms WitnessedDifference.BehavioralQuotient.comparisonMap
#print axioms WitnessedDifference.BehavioralQuotient.congruenceAction
#print axioms WitnessedDifference.BehavioralQuotient.congruenceObserve
#print axioms WitnessedDifference.BehavioralQuotient.comparison_preserves_readout
#print axioms WitnessedDifference.BehavioralQuotient.comparison_intertwines_action
#print axioms WitnessedDifference.BehavioralQuotient.comparison_commutes
#print axioms WitnessedDifference.BehavioralQuotient.comparison_surjective
#print axioms WitnessedDifference.BehavioralQuotient.comparison_unique
#print axioms WitnessedDifference.BehavioralQuotient.quotient_is_observable
