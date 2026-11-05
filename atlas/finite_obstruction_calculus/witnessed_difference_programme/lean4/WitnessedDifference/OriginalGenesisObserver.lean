/-!
# Original Genesis observer: unbounded histories and paid descent

This is the exact six-field signature of recovered original source part 001
lines 983–1004: `(M,U,p,rho,G,T)`, including a distinguished initial memory
state. Histories range over all finite words, with no length bound. Source
update `M × D → M` is curried as `D → M → M`. Grammar is a type parameter;
terminal labels are the original five tags, without operational authority.

The mathematical statements require total declared functions. No finite
sampling is used to infer arbitrary context totality or all-word descent.
The source O1/O2 criterion predicates, not phenomenological classifications,
are invariant under grammar and terminal-interface replacement. This refutes
the stronger historical T1 claim if classification uses those criteria.
-/

namespace WitnessedDifference.OriginalGenesisObserver

universe u v w z g g' e a

inductive GenesisTerm where
  | proved | refuted | unresolved | outside | refused

structure Observer (Memory : Type u) (Distinction : Type v) (Report : Type w)
    (Context : Type z) (Grammar : Type g) where
  initial : Memory
  update : Distinction → Memory → Memory
  profile : Memory → Report
  context : Context → List Distinction → List Distinction
  terminal : Grammar → GenesisTerm

/-- Free history extension, processing the head before the remaining word. -/
def historyUpdate {M : Type u} {D : Type v}
    (update : D → M → M) : List D → M → M
  | [], state => state
  | d :: word, state => historyUpdate update word (update d state)

theorem history_update_empty {M : Type u} {D : Type v}
    (update : D → M → M) (state : M) : historyUpdate update [] state = state := rfl

/-- Word concatenation composes the free extension in execution order. -/
theorem history_update_append {M : Type u} {D : Type v}
    (update : D → M → M) (firstWord secondWord : List D) (state : M) :
    historyUpdate update (firstWord ++ secondWord) state =
      historyUpdate update secondWord (historyUpdate update firstWord state) := by
  induction firstWord generalizing state with
  | nil => rfl
  | cons d firstWord ih => exact ih (update d state)

/-- The exact right-append recurrence stated by the original source. -/
theorem history_update_snoc {M : Type u} {D : Type v}
    (update : D → M → M) (word : List D) (d : D) (state : M) :
    historyUpdate update (word ++ [d]) state = update d (historyUpdate update word state) := by
  rw [history_update_append]
  rfl

/-- Empty-word and right-append laws determine the free extension uniquely
over all word lengths. -/
theorem history_extension_unique {M : Type u} {D : Type v}
    (update : D → M → M) (extension : List D → M → M)
    (hempty : ∀ state, extension [] state = state)
    (hsnoc : ∀ word d state, extension (word ++ [d]) state = update d (extension word state)) :
    extension = historyUpdate update := by
  funext word state
  have hreverse : ∀ reversed : List D,
      extension reversed.reverse state = historyUpdate update reversed.reverse state := by
    intro reversed
    induction reversed with
    | nil => exact hempty state
    | cons d reversed ih =>
      rw [List.reverse_cons, hsnoc, history_update_snoc, ih]
  simpa using hreverse word.reverse

def reached {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) (word : List D) : M :=
  historyUpdate observer.update word observer.initial

def historyProfile {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) (word : List D) : R :=
  observer.profile (reached observer word)

/-- The source memory, history presentation, contexts and grammar terminal
interface are preserved separately. A mathematical evaluator and action policy
are optional paid target layers, absent in this source-only adapter. -/
structure TypedLayers (M : Type u) (D : Type v) (R : Type w) (C : Type z)
    (G : Type g) (Evaluator : Type e) (Action : Type a) where
  memoryInitial : M
  memoryUpdate : D → M → M
  memoryReadout : M → R
  historyReaccess : List D → M
  presentationReport : List D → R
  inputContexts : C → List D → List D
  grammarTerminal : G → GenesisTerm
  evaluator : Option Evaluator
  policy : Option (GenesisTerm → Action)

def adaptOriginal
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    {Evaluator : Type e} {Action : Type a} (observer : Observer M D R C G) :
    TypedLayers M D R C G Evaluator Action where
  memoryInitial := observer.initial
  memoryUpdate := observer.update
  memoryReadout := observer.profile
  historyReaccess := reached observer
  presentationReport := historyProfile observer
  inputContexts := observer.context
  grammarTerminal := observer.terminal
  evaluator := none
  policy := none

/-- No report-to-grammar encoding is invented: the original terminal rule
still acts on G, not on the profile alphabet R. -/
def originalFields
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    {Evaluator : Type e} {Action : Type a} (layers : TypedLayers M D R C G Evaluator Action) :
    Observer M D R C G where
  initial := layers.memoryInitial
  update := layers.memoryUpdate
  profile := layers.memoryReadout
  context := layers.inputContexts
  terminal := layers.grammarTerminal

theorem original_adapter_recovers_exact_source_fields
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (Evaluator : Type e) (Action : Type a) (observer : Observer M D R C G) :
    originalFields (adaptOriginal (Evaluator := Evaluator) (Action := Action) observer) = observer := by
  cases observer
  rfl

theorem original_adapter_preserves_all_histories
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (Evaluator : Type e) (Action : Type a) (observer : Observer M D R C G)
    (word : List D) :
    let layers := adaptOriginal (Evaluator := Evaluator) (Action := Action) observer
    layers.historyReaccess word = historyUpdate observer.update word observer.initial ∧
      layers.presentationReport word = observer.profile (layers.historyReaccess word) := ⟨rfl, rfl⟩

theorem original_adapter_does_not_invent_missing_layers
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (Evaluator : Type e) (Action : Type a) (observer : Observer M D R C G) :
    let layers := adaptOriginal (Evaluator := Evaluator) (Action := Action) observer
    layers.evaluator = none ∧ layers.policy = none := ⟨rfl, rfl⟩

/-- Restrict the target memory carrier to states actually reachable from m0. -/
def Reachable {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) :=
  { state : M // ∃ word : List D, reached observer word = state }

def reachPresentation {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) (word : List D) : Reachable observer :=
  ⟨reached observer word, word, rfl⟩

theorem reach_presentation_onto
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) :
    ∀ state : Reachable observer, ∃ word, reachPresentation observer word = state := by
  intro state
  obtain ⟨word, hword⟩ := state.property
  exact ⟨word, Subtype.ext hword⟩

def StateContextCompatible
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) : Prop :=
  ∀ c left right, reached observer left = reached observer right →
    reached observer (observer.context c left) = reached observer (observer.context c right)

/-- Contexts descend to the reachable-memory quotient exactly when
they preserve reached-state fibers. A source context need not satisfy this. -/
theorem unique_reachable_context_adapter_iff
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) :
    (∃ adapted : C → Reachable observer → Reachable observer,
      (∀ c word, adapted c (reachPresentation observer word) =
        reachPresentation observer (observer.context c word)) ∧
      (∀ other : C → Reachable observer → Reachable observer,
        (∀ c word, other c (reachPresentation observer word) =
          reachPresentation observer (observer.context c word)) → other = adapted)) ↔
      StateContextCompatible observer := by
  constructor
  · intro h
    obtain ⟨adapted, hcommutes, _⟩ := h
    intro c left right hequal
    have hpresent : reachPresentation observer left = reachPresentation observer right := Subtype.ext hequal
    have htarget : reachPresentation observer (observer.context c left) =
        reachPresentation observer (observer.context c right) := by
      exact (hcommutes c left).symm.trans
        ((congrArg (adapted c) hpresent).trans (hcommutes c right))
    exact congrArg Subtype.val htarget
  · intro hcompatible
    let wordOf : Reachable observer → List D := fun state => Classical.choose state.property
    have hwordOf : ∀ state, reached observer (wordOf state) = state.val :=
      fun state => Classical.choose_spec state.property
    let adapted : C → Reachable observer → Reachable observer :=
      fun c state => reachPresentation observer (observer.context c (wordOf state))
    have hcommutes : ∀ c word, adapted c (reachPresentation observer word) =
        reachPresentation observer (observer.context c word) := by
      intro c word
      apply Subtype.ext
      exact hcompatible c (wordOf (reachPresentation observer word)) word
        (hwordOf (reachPresentation observer word))
    refine ⟨adapted, hcommutes, ?_⟩
    intro other hother
    funext c state
    obtain ⟨word, hword⟩ := reach_presentation_onto observer state
    subst state
    exact (hother c word).trans (hcommutes c word).symm

def O1Criterion
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) : Prop :=
  ∃ left right : List D, historyProfile observer left ≠ historyProfile observer right

def O2Criterion
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) : Prop :=
  ∃ c left right, historyProfile observer left = historyProfile observer right ∧
    historyProfile observer (observer.context c left) ≠ historyProfile observer (observer.context c right)

/-- Grammar and terminal interfaces are irrelevant to the stated O1/O2
criteria, including when the grammar carrier itself is changed. -/
theorem grammar_terminal_replacement_preserves_O1_O2
    {M : Type u} {D : Type v} {R : Type w} {C : Type z}
    {G : Type g} {H : Type g'}
    (left : Observer M D R C G) (right : Observer M D R C H)
    (hinitial : left.initial = right.initial) (hupdate : left.update = right.update)
    (hprofile : left.profile = right.profile) (hcontext : left.context = right.context) :
    (O1Criterion left ↔ O1Criterion right) ∧ (O2Criterion left ↔ O2Criterion right) := by
  have hprofiles : ∀ word, historyProfile left word = historyProfile right word := by
    intro word
    simp only [historyProfile, reached, hinitial, hupdate, hprofile]
  constructor
  · simp only [O1Criterion, hprofiles]
  · simp only [O2Criterion, hprofiles, hcontext]

/-- The pair of original source criterion values factors through the four
fields `(m0,U,p,rho)`; terminal/grammar cannot change that pair in isolation. -/
theorem full_six_classification_independence_fails
    {M : Type u} {D : Type v} {R : Type w} {C : Type z}
    {G : Type g} {H : Type g'}
    (left : Observer M D R C G) (right : Observer M D R C H)
    (hinitial : left.initial = right.initial) (hupdate : left.update = right.update)
    (hprofile : left.profile = right.profile) (hcontext : left.context = right.context) :
    ¬ ((O1Criterion left ∧ ¬ O1Criterion right) ∨
       (O1Criterion right ∧ ¬ O1Criterion left) ∨
       (O2Criterion left ∧ ¬ O2Criterion right) ∨
       (O2Criterion right ∧ ¬ O2Criterion left)) := by
  obtain ⟨ho1, ho2⟩ := grammar_terminal_replacement_preserves_O1_O2
    left right hinitial hupdate hprofile hcontext
  intro h
  rcases h with h | h | h | h
  · exact h.2 (ho1.mp h.1)
  · exact h.2 (ho1.mpr h.1)
  · exact h.2 (ho2.mp h.1)
  · exact h.2 (ho2.mpr h.1)

/-- A concrete finite memory with unbounded unary histories. -/
def parityObserver (contextAction : Unit → List Unit → List Unit)
    (terminal : Unit → GenesisTerm) : Observer Bool Unit Bool Unit Unit where
  initial := false
  update := fun _ state => !state
  profile := id
  context := contextAction
  terminal := terminal

theorem parity_observer_satisfies_O1
    (contextAction : Unit → List Unit → List Unit) (terminal : Unit → GenesisTerm) :
    O1Criterion (parityObserver contextAction terminal) := by
  refine ⟨[], [()], ?_⟩
  change false ≠ true
  intro impossible
  cases impossible

theorem identity_context_parity_observer_not_O2 (terminal : Unit → GenesisTerm) :
    ¬ O2Criterion (parityObserver (fun _ word => word) terminal) := by
  intro h
  obtain ⟨c, left, right, hequal, hdifferent⟩ := h
  exact hdifferent hequal

/-- This total, computable word context uses a distinction forgotten by the
parity memory: empty and length-two words reach the same state, but transform
to histories reaching different states. It must not be silently quotiented. -/
def forgottenHistoryContext (_ : Unit) (word : List Unit) : List Unit :=
  if word.isEmpty then [()] else []

theorem total_context_need_not_descend_to_reachable_memory :
    ¬ StateContextCompatible (parityObserver forgottenHistoryContext (fun _ => .unresolved)) := by
  intro hcompatible
  have impossible : true = false := hcompatible () [] [(), ()] rfl
  cases impossible

theorem forgotten_history_context_satisfies_O2 :
    O2Criterion (parityObserver forgottenHistoryContext (fun _ => .unresolved)) := by
  refine ⟨(), [], [(), ()], rfl, ?_⟩
  change true ≠ false
  intro impossible
  cases impossible

theorem constant_profile_refutes_O1
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) (value : R)
    (hconstant : ∀ state, observer.profile state = value) : ¬ O1Criterion observer := by
  intro h
  obtain ⟨left, right, hdifferent⟩ := h
  exact hdifferent ((hconstant (reached observer left)).trans (hconstant (reached observer right)).symm)

theorem identity_updates_refute_O1
    {M : Type u} {D : Type v} {R : Type w} {C : Type z} {G : Type g}
    (observer : Observer M D R C G) (hidentity : ∀ d state, observer.update d state = state) :
    ¬ O1Criterion observer := by
  have hrun : ∀ word state, historyUpdate observer.update word state = state := by
    intro word
    induction word with
    | nil => exact fun _ => rfl
    | cons d word ih =>
      intro state
      change historyUpdate observer.update word (observer.update d state) = state
      rw [hidentity d state]
      exact ih state
  intro h
  obtain ⟨left, right, hdifferent⟩ := h
  have hleft : historyProfile observer left = observer.profile observer.initial :=
    congrArg observer.profile (hrun left observer.initial)
  have hright : historyProfile observer right = observer.profile observer.initial :=
    congrArg observer.profile (hrun right observer.initial)
  exact hdifferent (hleft.trans hright.symm)

/-- The original archival corollary "U independent of its distinction
argument implies O0" is false even with two distinct input labels. Such
updates can retain history length; identity updates are a stronger condition. -/
theorem input_independent_updates_can_satisfy_O1 :
    ∃ observer : Observer Bool Bool Bool Unit Unit,
      (∀ state left right, observer.update left state = observer.update right state) ∧
      O1Criterion observer := by
  let observer : Observer Bool Bool Bool Unit Unit := {
    initial := false
    update := fun _ state => !state
    profile := id
    context := fun _ word => word
    terminal := fun _ => .unresolved
  }
  refine ⟨observer, fun _ _ _ => rfl, [], [false], ?_⟩
  change false ≠ true
  intro impossible
  cases impossible

end WitnessedDifference.OriginalGenesisObserver

#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer
#print axioms WitnessedDifference.OriginalGenesisObserver.historyUpdate
#print axioms WitnessedDifference.OriginalGenesisObserver.history_update_empty
#print axioms WitnessedDifference.OriginalGenesisObserver.history_update_append
#print axioms WitnessedDifference.OriginalGenesisObserver.history_update_snoc
#print axioms WitnessedDifference.OriginalGenesisObserver.history_extension_unique
#print axioms WitnessedDifference.OriginalGenesisObserver.reached
#print axioms WitnessedDifference.OriginalGenesisObserver.historyProfile
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers
#print axioms WitnessedDifference.OriginalGenesisObserver.adaptOriginal
#print axioms WitnessedDifference.OriginalGenesisObserver.originalFields
#print axioms WitnessedDifference.OriginalGenesisObserver.original_adapter_recovers_exact_source_fields
#print axioms WitnessedDifference.OriginalGenesisObserver.original_adapter_preserves_all_histories
#print axioms WitnessedDifference.OriginalGenesisObserver.original_adapter_does_not_invent_missing_layers
#print axioms WitnessedDifference.OriginalGenesisObserver.Reachable
#print axioms WitnessedDifference.OriginalGenesisObserver.reachPresentation
#print axioms WitnessedDifference.OriginalGenesisObserver.reach_presentation_onto
#print axioms WitnessedDifference.OriginalGenesisObserver.StateContextCompatible
#print axioms WitnessedDifference.OriginalGenesisObserver.unique_reachable_context_adapter_iff
#print axioms WitnessedDifference.OriginalGenesisObserver.O1Criterion
#print axioms WitnessedDifference.OriginalGenesisObserver.O2Criterion
#print axioms WitnessedDifference.OriginalGenesisObserver.grammar_terminal_replacement_preserves_O1_O2
#print axioms WitnessedDifference.OriginalGenesisObserver.full_six_classification_independence_fails
#print axioms WitnessedDifference.OriginalGenesisObserver.parityObserver
#print axioms WitnessedDifference.OriginalGenesisObserver.parity_observer_satisfies_O1
#print axioms WitnessedDifference.OriginalGenesisObserver.identity_context_parity_observer_not_O2
#print axioms WitnessedDifference.OriginalGenesisObserver.forgottenHistoryContext
#print axioms WitnessedDifference.OriginalGenesisObserver.total_context_need_not_descend_to_reachable_memory
#print axioms WitnessedDifference.OriginalGenesisObserver.forgotten_history_context_satisfies_O2
#print axioms WitnessedDifference.OriginalGenesisObserver.constant_profile_refutes_O1
#print axioms WitnessedDifference.OriginalGenesisObserver.identity_updates_refute_O1
#print axioms WitnessedDifference.OriginalGenesisObserver.input_independent_updates_can_satisfy_O1
#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm.proved
#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm.refuted
#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm.unresolved
#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm.outside
#print axioms WitnessedDifference.OriginalGenesisObserver.GenesisTerm.refused
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.mk
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.initial
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.update
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.profile
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.context
#print axioms WitnessedDifference.OriginalGenesisObserver.Observer.terminal
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.mk
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.memoryInitial
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.memoryUpdate
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.memoryReadout
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.historyReaccess
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.presentationReport
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.inputContexts
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.grammarTerminal
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.evaluator
#print axioms WitnessedDifference.OriginalGenesisObserver.TypedLayers.policy
