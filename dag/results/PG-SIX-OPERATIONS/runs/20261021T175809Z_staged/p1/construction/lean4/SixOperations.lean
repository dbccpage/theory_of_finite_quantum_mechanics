import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Union
import Mathlib.Data.Fintype.Basic

/-!
# Six operations and the admitted state

AuthorityEffect: None.  Scope: a small state machine whose state records what has been mentioned,
supplied, designated, admitted, retained and produced by operation, and the six operations Mention,
Supply, Designate, Admit, Retain, Operate acting on one item.  The source theorem
`pg_six_operations_and_primdiff_admission_gate` only models a COUNTER `admittedCount : Nat` that every
Admit increments (even a repeated one) and proves `applyPreGenOp op n != n <-> op = admit`; its second
conjunct is a fixed `Fin 4` tautology.  Here the admitted component is a Finset, the other five operations
are proved to leave it unchanged for every state, and the iff is proved for single steps and for every
finite trace.  The conflated models (supply or other operations also admitting, designation also retaining)
are explicit counter-models: they change the admitted state or the retained set where the six-operation
reading does not.  This is a definitional-separation model; it does not derive the Reading L / Reading F
split of Genesis; it only compares two machines (Supply as a no-op versus Supply also admitting), in which the two readings end in different, respectively the same, admitted state.  That each operation writes its own state field, and so that the six operations are pairwise distinguishable, holds by construction of the machine.
Cross-reference (not imported): node PG-INERT-DIAMOND carries the inert-inscription model.
-/

namespace SixOperations

variable {I : Type} [DecidableEq I]

/-- The six operations, each acting on one item. -/
inductive Op (I : Type) where
  | mention (x : I)
  | supply (x : I)
  | designate (x : I)
  | admit (x : I)
  | retain (x : I)
  | operate (x : I)
  deriving DecidableEq

/-- Host state: mentioned, supplied, designated (at most one), admitted, retained, produced items. -/
structure St (I : Type) where
  mentioned : Finset I
  supplied : Finset I
  designated : Option I
  admitted : Finset I
  retained : Finset I
  outputs : Finset I
  deriving DecidableEq

/-- The empty host state. -/
def St.empty : St I := ⟨∅, ∅, none, ∅, ∅, ∅⟩

/-- One step.  Retain and Operate act only on admitted items (they are refused otherwise). -/
def step (s : St I) : Op I → St I
  | .mention x => { s with mentioned := insert x s.mentioned }
  | .supply x => { s with supplied := insert x s.supplied }
  | .designate x => { s with designated := some x }
  | .admit x => { s with admitted := insert x s.admitted }
  | .retain x => if x ∈ s.admitted then { s with retained := insert x s.retained } else s
  | .operate x => if x ∈ s.admitted then { s with outputs := insert x s.outputs } else s

/-- Run a trace left to right. -/
def run (s : St I) (tr : List (Op I)) : St I := tr.foldl step s

/-- The item admitted by an operation, if it is an Admit. -/
def admitItem : Op I → Option I
  | .admit x => some x
  | _ => none

theorem step_admit (s : St I) (x : I) : (step s (.admit x)).admitted = insert x s.admitted := rfl

/-- Supply does not admit: the frame lemma of this machine for every state (the external Genesis `supply_no_op` was not read or imported here). -/
theorem supply_keeps_admitted (s : St I) (x : I) : (step s (.supply x)).admitted = s.admitted := rfl

/-- Each of the other five operations leaves the admitted component unchanged, in every state. -/
theorem step_admitted_of_ne_admit (s : St I) (op : Op I) (h : ∀ x, op ≠ .admit x) :
    (step s op).admitted = s.admitted := by
  cases op with
  | mention x => rfl
  | supply x => rfl
  | designate x => rfl
  | admit x => exact absurd rfl (h x)
  | retain x => by_cases hx : x ∈ s.admitted <;> simp [step, hx]
  | operate x => by_cases hx : x ∈ s.admitted <;> simp [step, hx]

/-- One step changes the admitted component iff the operation is an Admit of a new item. -/
theorem step_changes_admitted_iff (s : St I) (op : Op I) :
    (step s op).admitted ≠ s.admitted ↔ ∃ x, op = .admit x ∧ x ∉ s.admitted := by
  constructor
  · intro h
    by_contra hne
    apply h
    apply step_admitted_of_ne_admit
    intro x hx
    exact hne ⟨x, hx, by
      intro hmem
      apply h
      rw [hx, step_admit, Finset.insert_eq_of_mem hmem]⟩
  · rintro ⟨x, rfl, hx⟩ h
    rw [step_admit] at h
    have : x ∈ s.admitted := by
      rw [← h]; exact Finset.mem_insert_self x s.admitted
    exact hx this

/-- The admitted set after a trace is the old one together with every admitted item of the trace. -/
theorem run_admitted (s : St I) (tr : List (Op I)) :
    (run s tr).admitted = s.admitted ∪ (tr.filterMap admitItem).toFinset := by
  induction tr generalizing s with
  | nil => simp [run]
  | cons op tr ih =>
    have h := ih (step s op)
    have e : run s (op :: tr) = run (step s op) tr := rfl
    rw [e, h]
    by_cases hadm : ∃ x, op = .admit x
    · obtain ⟨x, rfl⟩ := hadm
      ext y; simp [step, admitItem]
    · push Not at hadm
      rw [step_admitted_of_ne_admit s op hadm]
      cases op with
      | admit x => exact absurd rfl (hadm x)
      | mention x => rfl
      | supply x => rfl
      | designate x => rfl
      | retain x => rfl
      | operate x => rfl

/-- A trace changes the admitted state iff it contains an Admit of an item not already admitted. -/
theorem run_changes_admitted_iff (s : St I) (tr : List (Op I)) :
    (run s tr).admitted ≠ s.admitted ↔ ∃ x, Op.admit x ∈ tr ∧ x ∉ s.admitted := by
  rw [run_admitted]
  constructor
  · intro h
    by_contra hne
    apply h
    apply Finset.union_eq_left.mpr
    intro y hy
    simp only [List.mem_toFinset, List.mem_filterMap] at hy
    obtain ⟨op, hop, hy⟩ := hy
    cases op with
    | admit x =>
      have hxy : x = y := by simpa [admitItem] using hy
      by_contra hmem
      exact hne ⟨x, hop, fun hx => hmem (hxy ▸ hx)⟩
    | mention x => simp [admitItem] at hy
    | supply x => simp [admitItem] at hy
    | designate x => simp [admitItem] at hy
    | retain x => simp [admitItem] at hy
    | operate x => simp [admitItem] at hy
  · rintro ⟨x, hx, hn⟩ h
    apply hn
    have : x ∈ s.admitted ∪ (tr.filterMap admitItem).toFinset := by
      apply Finset.mem_union_right
      simp only [List.mem_toFinset, List.mem_filterMap]
      exact ⟨Op.admit x, hx, rfl⟩
    rw [h] at this
    exact this

/-- Only Admit changes the admitted state, over every trace that contains no Admit. -/
theorem run_without_admit (s : St I) (tr : List (Op I)) (h : ∀ x, Op.admit x ∉ tr) :
    (run s tr).admitted = s.admitted := by
  by_contra hne
  obtain ⟨x, hx, _⟩ := (run_changes_admitted_iff s tr).mp hne
  exact h x hx

/-! ## The six operations are pairwise distinguishable -/

/-- The six operations on the item `0`, indexed by `Fin 6`. -/
def opAt (k : Fin 6) : Op Nat :=
  match k.val with
  | 0 => .mention 0
  | 1 => .supply 0
  | 2 => .designate 0
  | 3 => .admit 0
  | 4 => .retain 0
  | _ => .operate 0

/-- A probe state in which the item `0` is already admitted. -/
def probe : St Nat := ⟨∅, ∅, none, {0}, ∅, ∅⟩

/-- INSTANCE (Nat items, item 0): at the probe, the six operations have six pairwise different results; this holds by construction, each operation writing its own field. -/
theorem six_results_pairwise_distinct : Function.Injective (fun k : Fin 6 => step probe (opAt k)) := by
  decide

/-! ## Conflated models: counter-models to the six-operation reading -/

/-- Conflation 1: Supply also admits (a delivered payload is taken as adopted). -/
def stepSupplyAdmits (s : St I) : Op I → St I
  | .supply x => step (step s (.admit x)) (.supply x)
  | op => step s op

/-- Conflation 2: Designate also retains (the designated item is kept). -/
def stepDesignateRetains (s : St I) : Op I → St I
  | .designate x => step (step s (.retain x)) (.designate x)
  | op => step s op

def runWith (f : St I → Op I → St I) (s : St I) (tr : List (Op I)) : St I := tr.foldl f s

/-- Reading L: the token `t` is supplied but unadmitted. -/
def readingL (t : I) : List (Op I) := [.supply t]

/-- Reading F: the token `t` is supplied and then admitted. -/
def readingF (t : I) : List (Op I) := [.supply t, .admit t]

/-- Six-operation machine: Readings L and F end in different admitted states, for every token. -/
theorem readings_separated_six_ops (t : I) :
    (run St.empty (readingL t)).admitted ≠ (run St.empty (readingF t)).admitted := by
  intro h
  have h1 : (run (St.empty : St I) (readingL t)).admitted = ∅ := by simp [run, readingL, step, St.empty]
  have h2 : t ∈ (run (St.empty : St I) (readingF t)).admitted := by
    simp [run, readingF, step, St.empty]
  rw [h1] at h
  rw [← h] at h2
  exact absurd h2 (Finset.notMem_empty t)

/-- Machine in which Supply also admits: the two readings end in the same admitted state, for every token. -/
theorem readings_collapse_when_supply_admits (t : I) :
    (runWith stepSupplyAdmits St.empty (readingL t)).admitted
      = (runWith stepSupplyAdmits St.empty (readingF t)).admitted := by
  simp [runWith, readingL, readingF, stepSupplyAdmits, step, St.empty]

/-- Supply = Admit changes the admitted state on a trace the six-operation reading leaves unchanged. -/
theorem supply_admits_conflation_separates (t : I) :
    (runWith stepSupplyAdmits St.empty [.supply t]).admitted ≠ (run St.empty [.supply t]).admitted := by
  intro h
  have : t ∈ (runWith stepSupplyAdmits (St.empty : St I) [.supply t]).admitted := by
    simp [runWith, stepSupplyAdmits, step, St.empty]
  rw [h] at this
  simp [run, step, St.empty] at this

/-- Designate = Retain: two designations in turn leave only the last designated, but the conflated model
retains both admitted items, so designation is permanent there and overwritten in the six-operation reading.
(Instance with the items 0 and 1.) -/
theorem designate_retains_conflation_separates :
    (runWith stepDesignateRetains (St.empty : St Nat) [.admit 0, .admit 1, .designate 0, .designate 1]).retained
      ≠ (run (St.empty : St Nat) [.admit 0, .admit 1, .designate 0, .designate 1]).retained := by
  decide

/-- In the six-operation model the second designation replaces the first. -/
theorem designation_is_overwritten :
    (run (St.empty : St Nat) [.designate 0, .designate 1]).designated = some 1 := by decide

/-! ## Instance: the source counter versus the set model -/

/-- The source models admission by a counter incremented at every Admit; with a set, re-admitting an item
changes nothing.  Instance (not general): admitting `0` twice gives card 1, not 2. -/
theorem repeated_admit_does_not_grow_set :
    (run (St.empty : St Nat) [.admit 0, .admit 0]).admitted.card = 1 := by decide

end SixOperations

#print axioms SixOperations.supply_keeps_admitted
#print axioms SixOperations.step_admitted_of_ne_admit
#print axioms SixOperations.step_changes_admitted_iff
#print axioms SixOperations.run_admitted
#print axioms SixOperations.run_changes_admitted_iff
#print axioms SixOperations.run_without_admit
#print axioms SixOperations.six_results_pairwise_distinct
#print axioms SixOperations.readings_separated_six_ops
#print axioms SixOperations.readings_collapse_when_supply_admits
#print axioms SixOperations.supply_admits_conflation_separates
#print axioms SixOperations.designate_retains_conflation_separates
#print axioms SixOperations.designation_is_overwritten
#print axioms SixOperations.repeated_admit_does_not_grow_set
