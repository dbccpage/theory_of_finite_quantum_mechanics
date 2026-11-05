import WitnessedDifference.GuardedHistoryCoherence

/-!
# Exact count guards for the legal schedule complex

A `false` endpoint starts a task (the native Remove event); a `true` endpoint
finishes a task (the native AddAssertion event). A start consumes one available
count and is refused at zero. This file proves the operational prefix criterion
and the all-refinements capacity test used in the schedule-complex construction.
It does not formalize the nerve lemma or the arrangement-complement homotopy.
-/

namespace WitnessedDifference.GuardedScheduleTopology

open GuardedHistoryCoherence

/-- Number of task starts (native removals). -/
def starts (word : List Bool) : Nat := word.count false

/-- Number of task finishes (native additions). -/
def finishes (word : List Bool) : Nat := word.count true

@[simp] theorem starts_nil : starts [] = 0 := rfl
@[simp] theorem finishes_nil : finishes [] = 0 := rfl
@[simp] theorem starts_start (word : List Bool) : starts (false :: word) = starts word + 1 := by
  simp [starts]
@[simp] theorem starts_finish (word : List Bool) : starts (true :: word) = starts word := by
  simp [starts]
@[simp] theorem finishes_start (word : List Bool) : finishes (false :: word) = finishes word := by
  simp [finishes]
@[simp] theorem finishes_finish (word : List Bool) : finishes (true :: word) = finishes word + 1 := by
  simp [finishes]
@[simp] theorem starts_append (left right : List Bool) :
    starts (left ++ right) = starts left + starts right := List.count_append
@[simp] theorem finishes_append (left right : List Bool) :
    finishes (left ++ right) = finishes left + finishes right := List.count_append

/-- Every prefix uses at most the initial supply plus the finishes already seen. -/
def PrefixSafe (supply : Nat) (word : List Bool) : Prop :=
  ∀ pre post, word = pre ++ post → starts pre ≤ supply + finishes pre

theorem prefixSafe_nil (supply : Nat) : PrefixSafe supply [] := by
  intro pre post h
  cases pre with
  | nil => simp
  | cons e tail => cases h

theorem prefixSafe_start (supply : Nat) (word : List Bool) :
    PrefixSafe supply (false :: word) ↔
      0 < supply ∧ PrefixSafe (supply - 1) word := by
  constructor
  · intro safe
    have positive := safe [false] word rfl
    simp only [starts_start, starts_nil, finishes_start, finishes_nil, Nat.add_zero] at positive
    refine ⟨by omega, ?_⟩
    intro pre post h
    have hp := safe (false :: pre) post (by simp [h])
    simp only [starts_start, finishes_start] at hp
    omega
  · rintro ⟨positive, safe⟩ pre post h
    cases pre with
    | nil => simp
    | cons e tail =>
      have he : e = false := (List.cons.inj h).1.symm
      have ht : word = tail ++ post := (List.cons.inj h).2
      subst e
      have hp := safe tail post ht
      simp only [starts_start, finishes_start]
      omega

theorem prefixSafe_finish (supply : Nat) (word : List Bool) :
    PrefixSafe supply (true :: word) ↔ PrefixSafe (supply + 1) word := by
  constructor
  · intro safe pre post h
    have hp := safe (true :: pre) post (by simp [h])
    simp only [starts_finish, finishes_finish] at hp
    omega
  · intro safe pre post h
    cases pre with
    | nil => simp
    | cons e tail =>
      have he : e = true := (List.cons.inj h).1.symm
      have ht : word = tail ++ post := (List.cons.inj h).2
      subst e
      have hp := safe tail post ht
      simp only [starts_finish, finishes_finish]
      omega

/-- Exact equivalence with the native partial count execution, including its
returned value. Prefix safety is an arithmetic property of every cut, not an
assumed successful replay. -/
theorem replay_iff_prefixSafe (supply : Nat) (word : List Bool) (result : Nat) :
    run countStep supply word = some result ↔
      PrefixSafe supply word ∧ result = supply + finishes word - starts word := by
  induction word generalizing supply with
  | nil =>
    simp only [run, Option.some.injEq, finishes_nil, starts_nil, Nat.add_zero, Nat.sub_zero]
    exact ⟨fun h => ⟨prefixSafe_nil supply, h.symm⟩, fun h => h.2.symm⟩
  | cons event word ih =>
    cases event with
    | false =>
      by_cases positive : 0 < supply
      · have transition : countStep supply false = some (supply - 1) := by
          simp [countStep, positive]
        rw [run_cons_some countStep transition, ih, prefixSafe_start]
        simp only [starts_start, finishes_start]
        constructor
        · rintro ⟨safe, value⟩
          refine ⟨⟨positive, safe⟩, ?_⟩
          omega
        · rintro ⟨⟨_, safe⟩, value⟩
          refine ⟨safe, ?_⟩
          omega
      · rw [run_cons_none countStep (by simp [countStep, positive]), prefixSafe_start]
        simp [positive]
    | true =>
      have transition : countStep supply true = some (supply + 1) := by simp [countStep]
      rw [run_cons_some countStep transition, ih, prefixSafe_finish]
      simp only [starts_finish, finishes_finish]
      constructor <;> rintro ⟨safe, value⟩ <;> refine ⟨safe, ?_⟩ <;> omega

/-- A schedule has a successful native replay exactly when every cut passes. -/
theorem replay_exists_iff_prefixSafe (supply : Nat) (word : List Bool) :
    (∃ result, run countStep supply word = some result) ↔ PrefixSafe supply word := by
  constructor
  · rintro ⟨result, h⟩
    exact ((replay_iff_prefixSafe supply word result).mp h).1
  · intro safe
    exact ⟨_, (replay_iff_prefixSafe supply word _).mpr ⟨safe, rfl⟩⟩

/-- Supplying at least all starts makes every ordering safe. -/
theorem prefixSafe_of_total_starts_le (supply : Nat) (word : List Bool)
    (bound : starts word ≤ supply) : PrefixSafe supply word := by
  intro pre post h
  rw [h, starts_append] at bound
  omega

/-- The extremal ordering puts every start before every finish. -/
def startsFirst (word : List Bool) : List Bool :=
  List.replicate (starts word) false ++ List.replicate (finishes word) true

theorem startsFirst_perm (word : List Bool) : (startsFirst word).Perm word := by
  induction word with
  | nil => exact List.Perm.refl _
  | cons event word ih =>
    cases event with
    | false => simpa [startsFirst, List.replicate_succ] using ih.cons false
    | true =>
      simp only [startsFirst, starts_finish, finishes_finish, List.replicate_succ]
      exact List.perm_middle.trans (ih.cons true)

/-- All linear refinements of a block pass the native guard exactly when its
number of starts is no greater than the supply before that block. -/
theorem all_refinements_safe_iff (supply : Nat) (block : List Bool) :
    (∀ order, order.Perm block → PrefixSafe supply order) ↔ starts block ≤ supply := by
  constructor
  · intro all
    have safe := all (startsFirst block) (startsFirst_perm block)
    have bound := safe (List.replicate (starts block) false)
      (List.replicate (finishes block) true) rfl
    simpa [starts, finishes, List.count_replicate] using bound
  · intro bound order permutation
    apply prefixSafe_of_total_starts_le
    rw [show starts order = starts block from permutation.count_eq false]
    exact bound

/-- Operational version of the all-refinements test. -/
theorem all_refinements_replay_iff (supply : Nat) (block : List Bool) :
    (∀ order, order.Perm block → ∃ result, run countStep supply order = some result) ↔
      starts block ≤ supply := by
  constructor
  · intro all
    apply (all_refinements_safe_iff supply block).mp
    intro order permutation
    exact (replay_exists_iff_prefixSafe supply order).mp (all order permutation)
  · intro bound order permutation
    apply (replay_exists_iff_prefixSafe supply order).mpr
    exact (all_refinements_safe_iff supply block).mpr bound order permutation

/-- With `active` tasks already open, a block is legal in every refinement
exactly when `active + starts ≤ capacity`. The premise prevents truncated
subtraction from misrepresenting an already over-capacity source. -/
theorem block_capacity_iff (capacity active : Nat) (block : List Bool)
    (admitted : active ≤ capacity) :
    (∀ order, order.Perm block →
      ∃ result, run countStep (capacity - active) order = some result) ↔
        active + starts block ≤ capacity := by
  constructor
  · intro all
    have bound := (all_refinements_replay_iff (capacity - active) block).mp all
    clear all
    omega
  · intro bound
    apply (all_refinements_replay_iff (capacity - active) block).mpr
    omega

/-- There is a finish before a later start. -/
def EarlyFinish (word : List Bool) : Prop :=
  ∃ pre post, word = pre ++ true :: post ∧ 0 < starts post

theorem earlyFinish_starts_positive {word : List Bool} (early : EarlyFinish word) :
    0 < starts word := by
  rcases early with ⟨pre, post, h, positive⟩
  rw [h, starts_append, starts_finish]
  omega

theorem earlyFinish_start (word : List Bool) :
    EarlyFinish (false :: word) ↔ EarlyFinish word := by
  constructor
  · rintro ⟨pre, post, h, positive⟩
    cases pre with
    | nil => cases h
    | cons event tail =>
      have ht : word = tail ++ true :: post := (List.cons.inj h).2
      exact ⟨tail, post, ht, positive⟩
  · rintro ⟨pre, post, h, positive⟩
    exact ⟨false :: pre, post, by simp [h], positive⟩

theorem earlyFinish_finish (word : List Bool) :
    EarlyFinish (true :: word) ↔ 0 < starts word := by
  constructor
  · intro h
    simpa using earlyFinish_starts_positive h
  · intro positive
    exact ⟨[], word, rfl, positive⟩

/-- If there are `n > 0` starts, initial supply `n-1` succeeds precisely
when one finish occurs before a later start. Pairing and unique event tags are
not needed for this stronger count-word statement. -/
theorem maximal_capacity_safe_iff (word : List Bool) (positive : 0 < starts word) :
    PrefixSafe (starts word - 1) word ↔ EarlyFinish word := by
  induction word with
  | nil => simp at positive
  | cons event word ih =>
    cases event with
    | false =>
      simp only [starts_start, Nat.add_sub_cancel, prefixSafe_start, earlyFinish_start]
      by_cases h : 0 < starts word
      · exact ⟨fun safe => (ih h).mp safe.2, fun early => ⟨h, (ih h).mpr early⟩⟩
      · constructor
        · intro safe
          exact False.elim (h safe.1)
        · intro early
          exact False.elim (h (earlyFinish_starts_positive early))
    | true =>
      simp only [starts_finish] at positive ⊢
      rw [prefixSafe_finish, earlyFinish_finish]
      have supply : starts word - 1 + 1 = starts word := by omega
      rw [supply]
      exact ⟨fun _ => positive, fun _ => prefixSafe_of_total_starts_le _ _ (Nat.le_refl _)⟩

/-- Native replay form of the extremal-capacity characterization. -/
theorem maximal_capacity_replay_iff (word : List Bool) (positive : 0 < starts word) :
    (∃ result, run countStep (starts word - 1) word = some result) ↔ EarlyFinish word := by
  rw [replay_exists_iff_prefixSafe]
  exact maximal_capacity_safe_iff word positive

/-- Sorting distinct tagged events by their endpoint role preserves every tag.
This does not erase the tags from the permutation statement. -/
def taggedStartsFirst {Event : Type} (isFinish : Event → Bool) (block : List Event) :
    List Event := block.filter (fun event => !(isFinish event)) ++ block.filter isFinish

theorem taggedStartsFirst_perm {Event : Type} (isFinish : Event → Bool)
    (block : List Event) : (taggedStartsFirst isFinish block).Perm block := by
  simpa [taggedStartsFirst] using List.filter_append_perm (fun event => !(isFinish event)) block

theorem starts_of_start_filter {Event : Type} (isFinish : Event → Bool)
    (block : List Event) :
    starts ((block.filter (fun event => !(isFinish event))).map isFinish) =
      starts (block.map isFinish) := by
  induction block with
  | nil => rfl
  | cons event tail ih =>
    cases h : isFinish event <;> simp [h, ih]

theorem finishes_of_start_filter {Event : Type} (isFinish : Event → Bool)
    (block : List Event) :
    finishes ((block.filter (fun event => !(isFinish event))).map isFinish) = 0 := by
  induction block with
  | nil => rfl
  | cons event tail ih =>
    cases h : isFinish event <;> simp [h, ih]

/-- Exact all-refinements test for tagged endpoints. In the schedule-complex
application, the supplied block has distinct tags and contains no start together
with its paired finish; the external job precedence then permits every block
permutation. The theorem checks the native count guard for all those actual
tagged permutations, rather than assuming an erasure is a faithful bijection. -/
theorem tagged_all_refinements_replay_iff {Event : Type}
    (isFinish : Event → Bool) (supply : Nat) (block : List Event) :
    (∀ order : List Event, order.Perm block →
      ∃ result, run countStep supply (order.map isFinish) = some result) ↔
        starts (block.map isFinish) ≤ supply := by
  constructor
  · intro all
    have replay := all (taggedStartsFirst isFinish block) (taggedStartsFirst_perm isFinish block)
    have safe := (replay_exists_iff_prefixSafe _ _).mp replay
    have bound := safe ((block.filter (fun event => !(isFinish event))).map isFinish)
      ((block.filter isFinish).map isFinish) (by simp [taggedStartsFirst])
    simpa only [starts_of_start_filter, finishes_of_start_filter, Nat.add_zero] using bound
  · intro bound order permutation
    apply (replay_exists_iff_prefixSafe _ _).mpr
    apply prefixSafe_of_total_starts_le
    have eq : starts (order.map isFinish) = starts (block.map isFinish) :=
      (permutation.map isFinish).count_eq false
    rw [eq]
    exact bound

/-- Every accepted refinement has the same exact count at the next block. -/
theorem tagged_refinement_endpoint {Event : Type} (isFinish : Event → Bool)
    (supply result : Nat) (block order : List Event) (permutation : order.Perm block)
    (accepted : run countStep supply (order.map isFinish) = some result) :
    result = supply + finishes (block.map isFinish) - starts (block.map isFinish) := by
  have value := ((replay_iff_prefixSafe _ _ _).mp accepted).2
  have startEq : starts (order.map isFinish) = starts (block.map isFinish) :=
    (permutation.map isFinish).count_eq false
  have finishEq : finishes (order.map isFinish) = finishes (block.map isFinish) :=
    (permutation.map isFinish).count_eq true
  rw [startEq, finishEq] at value
  exact value

/-- A nonempty directed path in a finite-or-infinite task constraint graph. -/
inductive ConstraintPath {Task : Type} (edge : Task → Task → Prop) : Task → Task → Prop
  | single {source target} : edge source target → ConstraintPath edge source target
  | extend {source middle target} : ConstraintPath edge source middle →
      edge middle target → ConstraintPath edge source target

/-- A strict ranking increases along every nonempty constraint path. -/
theorem rank_increases_on_path {Task : Type} (edge : Task → Task → Prop)
    (rank : Task → Nat) (strict : ∀ i j, edge i j → rank i < rank j)
    {source target : Task} (path : ConstraintPath edge source target) :
    rank source < rank target := by
  induction path with
  | single h => exact strict _ _ h
  | extend _ h ih => exact Nat.lt_trans ih (strict _ _ h)

/-- A realizable strict ranking excludes every directed cycle. This includes
2-cycles, not merely a check of self loops or adjacent inequalities. -/
theorem strict_rank_excludes_cycle {Task : Type} (edge : Task → Task → Prop)
    (rank : Task → Nat) (strict : ∀ i j, edge i j → rank i < rank j) (task : Task) :
    ¬ ConstraintPath edge task task := by
  intro path
  exact Nat.lt_irrefl _ (rank_increases_on_path edge rank strict path)

/-- Ordered task endpoints realizing finish-before-start constraints give a
strict task ranking. Thus a nonempty intersection of these schedule constraints
cannot contain a directed cycle. -/
theorem endpoint_constraints_exclude_cycle {Task : Type}
    (start finish : Task → Nat) (edge : Task → Task → Prop)
    (paired : ∀ task, start task < finish task)
    (cross : ∀ i j, edge i j → finish i < start j) (task : Task) :
    ¬ ConstraintPath edge task task := by
  apply strict_rank_excludes_cycle edge start
  intro i j h
  exact Nat.lt_trans (paired i) (cross i j h)

/-- The finish-before-start inequality propagates along task constraints. -/
theorem endpoint_inequality_on_path {Task : Type}
    (start finish : Task → Nat) (edge : Task → Task → Prop)
    (paired : ∀ task, start task < finish task)
    (cross : ∀ i j, edge i j → finish i < start j)
    {source target : Task} (path : ConstraintPath edge source target) :
    finish source < start target := by
  induction path with
  | single h => exact cross _ _ h
  | extend _ h ih =>
    exact Nat.lt_trans ih (Nat.lt_trans (paired _) (cross _ _ h))

/-- Tasks simultaneously active at a cut form an antichain in the transitive
constraint relation, which is the input to a separate width bound. -/
theorem active_tasks_are_incomparable {Task : Type}
    (start finish : Task → Nat) (edge : Task → Task → Prop)
    (paired : ∀ task, start task < finish task)
    (cross : ∀ i j, edge i j → finish i < start j)
    (cut : Nat) {left right : Task}
    (leftActive : start left ≤ cut ∧ cut < finish left)
    (rightActive : start right ≤ cut ∧ cut < finish right) :
    ¬ ConstraintPath edge left right ∧ ¬ ConstraintPath edge right left := by
  constructor
  · intro path
    have bound := endpoint_inequality_on_path start finish edge paired cross path
    omega
  · intro path
    have bound := endpoint_inequality_on_path start finish edge paired cross path
    omega

/-- A strict task ranking constructs actual distinct endpoints for each task,
with every requested finish-before-start inequality. No endpoint realization
is assumed in this direction. -/
theorem strict_rank_constructs_endpoints {Task : Type}
    (edge : Task → Task → Prop) (rank : Task → Nat)
    (strict : ∀ i j, edge i j → rank i < rank j) :
    (∀ task, 2 * rank task < 2 * rank task + 1) ∧
      (∀ i j, edge i j → 2 * rank i + 1 < 2 * rank j) := by
  constructor
  · intro task
    omega
  · intro i j h
    have bound := strict i j h
    omega

/-- Injective rankings give pairwise disjoint task intervals. These are concrete
non-overlapping witnesses for any realizable strictly ranked constraint family. -/
theorem injective_rank_intervals_disjoint {Task : Type} (rank : Task → Nat)
    (injective : Function.Injective rank) {left right : Task} (different : left ≠ right) :
    2 * rank left + 1 < 2 * rank right ∨ 2 * rank right + 1 < 2 * rank left := by
  have unequal : rank left ≠ rank right := fun h => different (injective h)
  omega

/-- The extremal-capacity characterization cannot be used at an arbitrary lower
capacity. This three-task ordering has a finish before a later start but already
fails at its second start when the capacity is one. -/
theorem early_finish_does_not_suffice_at_lower_capacity :
    EarlyFinish [false, false, true, false, true, true] ∧
      run countStep 1 [false, false, true, false, true, true] = none := by
  constructor
  · refine ⟨[false, false], [false, true, true], rfl, ?_⟩
    simp
  · simp [run, countStep]

/-- Truncated subtraction cannot validate an over-capacity source: an empty
replay succeeds even when the claimed initial number of active tasks is invalid.
This is why `block_capacity_iff` requires `active ≤ capacity`. -/
theorem empty_replay_does_not_validate_source :
    run countStep (0 - 1) [] = some 0 ∧ ¬ (1 + starts [] ≤ 0) := by
  constructor <;> decide

end WitnessedDifference.GuardedScheduleTopology
