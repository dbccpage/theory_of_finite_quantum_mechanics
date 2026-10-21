import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Pi

/-!
# The obligation monoid: counter vectors, the free commutative monoid, traces and the ledger

AuthorityEffect: None.  Scope: (1) the commutative monoid `Ob k = Fin k -> Nat` of obligation counters under
pointwise sum, which is the free commutative monoid on `k` obligation ids (universal property proved);
(2) the source 3-counter `traceObligation` of `DerivationDagQMClosure.lean` (lines 13-56) re-proved as a monoid
homomorphism from event lists, with two sharper observations about the source;
(3) the ledger discharge rule of `obligation.rs` (lines 190-206) on a finite id alphabet, and the partial `combine` with a
count bound (`CountOverflow`).

NOT established here, and not claimed: that Genesis events or `S(n)` maps are monoid morphisms into this monoid
(TFQ-0342 / PG-GAP-EVENT-OBLIGATION).  `trace` is a homomorphism from *lists of the four declared events*
only; the event-to-vector table `evOb` is a definition copied from the source, not derived.
-/

namespace ObligationMonoid

/-- Counter vectors on `k` obligation ids; `combine` is `+` (pointwise), `empty` is `0`. -/
abbrev Ob (k : Nat) := Fin k → Nat

variable {k : Nat}

theorem combine_apply (x y : Ob k) (i : Fin k) : (x + y) i = x i + y i := rfl

theorem combine_assoc (x y z : Ob k) : (x + y) + z = x + (y + z) := by
  funext i; simp only [combine_apply]; omega

theorem combine_comm (x y : Ob k) : x + y = y + x := by
  funext i; simp only [combine_apply]; omega

theorem combine_empty (x : Ob k) : x + 0 = x ∧ 0 + x = x := by
  constructor <;> (funext i; simp)

/-- Cancellation holds: the monoid is cancellative (it embeds in `Z^k`). -/
theorem combine_cancel (x y z : Ob k) (h : x + z = y + z) : x = y := by
  funext i
  have := congrFun h i
  simp only [combine_apply] at this
  omega

/-- It is not a group: a nonzero vector has no inverse. -/
theorem no_inverse (x y : Ob k) (hx : x ≠ 0) : x + y ≠ 0 := by
  intro h
  apply hx
  funext i
  have := congrFun h i
  simp only [combine_apply, Pi.zero_apply] at this
  simp only [Pi.zero_apply]
  omega

/-- Basis vector for obligation id `i`. -/
def single (i : Fin k) : Ob k := Pi.single i 1

/-- Universal property, existence: the extension of an assignment of ids to a commutative monoid. -/
def lift {M : Type} [AddCommMonoid M] (f : Fin k → M) : Ob k →+ M where
  toFun x := ∑ i, x i • f i
  map_zero' := by simp
  map_add' x y := by simp [add_nsmul, Finset.sum_add_distrib]

theorem lift_single {M : Type} [AddCommMonoid M] (f : Fin k → M) (i : Fin k) : lift f (single i) = f i := by
  simp [lift, single, Pi.single_apply, one_nsmul]

theorem vec_eq_sum_singles (x : Ob k) : x = ∑ i, x i • single i := by
  funext j
  simp [single, Finset.sum_apply, Pi.single_apply]

/-- Universal property, uniqueness: any monoid homomorphism agreeing on the basis equals `lift`. -/
theorem lift_unique {M : Type} [AddCommMonoid M] (f : Fin k → M) (g : Ob k →+ M)
    (hg : ∀ i, g (single i) = f i) : g = lift f := by
  refine AddMonoidHom.ext (fun x => ?_)
  calc g x = g (∑ i, x i • single i) := congrArg g (vec_eq_sum_singles x)
    _ = ∑ i, x i • f i := by
      rw [map_sum]
      exact Finset.sum_congr rfl (fun i _ => by rw [map_nsmul, hg])

/-! ### The source 3-counter trace -/

inductive Ev | declareTerm | assertDiff | removeDiff | identifyTerms
  deriving DecidableEq

/-- Event table copied from `eventObligation` (source line 29); a definition, not a derivation. -/
def evOb : Ev → Ob 3
  | .declareTerm => ![1, 0, 0]
  | .assertDiff => ![0, 1, 0]
  | .removeDiff => ![0, 0, 1]
  | .identifyTerms => ![0, 0, 1]

def trace (l : List Ev) : Ob 3 := (l.map evOb).sum

theorem trace_nil : trace [] = 0 := rfl

/-- The source `traceObligation_append`, general: `trace` turns append into combine. -/
theorem trace_append (a b : List Ev) : trace (a ++ b) = trace a + trace b := by
  simp [trace, List.sum_append]

theorem trace_cons (e : Ev) (l : List Ev) : trace (e :: l) = evOb e + trace l := by
  simp [trace]

/-- Counters are occurrence counts, and the total cost is the length: every event costs exactly 1. -/
theorem trace_total (l : List Ev) : (trace l) 0 + (trace l) 1 + (trace l) 2 = l.length := by
  induction l with
  | nil => rfl
  | cons e l ih =>
    rw [trace_cons]
    simp only [combine_apply]
    cases e <;> simp [evOb] <;> omega

theorem trace_terms (l : List Ev) : (trace l) 0 = l.count .declareTerm := by
  induction l with
  | nil => rfl
  | cons e l ih => rw [trace_cons]; cases e <;> simp [evOb, ih] <;> omega

theorem trace_assertions (l : List Ev) : (trace l) 1 = l.count .assertDiff := by
  induction l with
  | nil => rfl
  | cons e l ih => rw [trace_cons]; cases e <;> simp [evOb, ih] <;> omega

theorem trace_destructive (l : List Ev) : (trace l) 2 = l.count .removeDiff + l.count .identifyTerms := by
  induction l with
  | nil => rfl
  | cons e l ih => rw [trace_cons]; cases e <;> simp [evOb, ih] <;> omega

/-- The source `ValidFreshAssertionTrace`: counters only. -/
def ValidFresh (l : List Ev) : Prop := (trace l) 0 ≥ 1 ∧ (trace l) 1 ≥ 1

/-- The source `declare_then_assert_cost_floor`, general: a pure counter inequality. -/
theorem cost_floor (l : List Ev) (h : ValidFresh l) : l.length ≥ 2 := by
  have := trace_total l
  obtain ⟨h0, h1⟩ := h
  omega

/-- The hypothesis is order blind: an assertion before the declaration is "valid fresh". -/
theorem valid_fresh_order_blind : ValidFresh [.assertDiff, .declareTerm] := by
  unfold ValidFresh
  decide

/-- The commutative image forgets order. -/
theorem trace_swap : trace [.declareTerm, .assertDiff] = trace [.assertDiff, .declareTerm] ∧
    ([Ev.declareTerm, .assertDiff] : List Ev) ≠ [.assertDiff, .declareTerm] := by
  refine ⟨by decide, by decide⟩

/-- Two distinct events give the same obligation vector: the event table is not injective. -/
theorem event_table_not_injective : evOb .removeDiff = evOb .identifyTerms ∧ Ev.removeDiff ≠ Ev.identifyTerms := by
  refine ⟨rfl, by decide⟩

/-! ### Partial `combine` with a count bound (the `CountOverflow` error) and the ledger -/

/-- `combine` that refuses (returns `none`) when some count would exceed the bound `M` (u64 in the Rust source). -/
def combineB (M : Nat) (x y : Ob k) : Option (Ob k) :=
  if ∀ i, x i + y i ≤ M then some (x + y) else none

theorem combineB_assoc (M : Nat) (x y z : Ob k) :
    (combineB M x y).bind (fun s => combineB M s z) = (combineB M y z).bind (fun t => combineB M x t) := by
  have hl : (combineB M x y).bind (fun s => combineB M s z) =
      if ∀ i, x i + y i + z i ≤ M then some (x + y + z) else none := by
    unfold combineB
    by_cases h1 : ∀ i, x i + y i ≤ M
    · by_cases h2 : ∀ i, x i + y i + z i ≤ M
      · simp [h1, h2, combine_apply]
      · simp only [h1, h2, if_true, if_false, Option.bind_some, combine_apply]
        simp [h2]
    · have h2 : ¬ ∀ i, x i + y i + z i ≤ M := fun h => h1 fun i => by have := h i; omega
      simp [h1, h2]
  have hr : (combineB M y z).bind (fun t => combineB M x t) =
      if ∀ i, x i + y i + z i ≤ M then some (x + y + z) else none := by
    unfold combineB
    by_cases h1 : ∀ i, y i + z i ≤ M
    · by_cases h2 : ∀ i, x i + y i + z i ≤ M
      · have h3 : ∀ i, x i + (y i + z i) ≤ M := fun i => by have := h2 i; omega
        simp [h1, h2, h3, combine_assoc]
      · have h3 : ¬ ∀ i, x i + (y i + z i) ≤ M := fun h => h2 fun i => by have := h i; omega
        simp [h1, h2, h3, combine_apply]
    · have h2 : ¬ ∀ i, x i + y i + z i ≤ M := fun h => h1 fun i => by have := h i; omega
      simp [h1, h2]
  rw [hl, hr]

/-- A ledger on `k` ids: generated and discharged counts. -/
structure Ledger (k : Nat) where
  gen : Ob k
  dis : Ob k

def Ledger.Valid (L : Ledger k) : Prop := ∀ i, L.dis i ≤ L.gen i

inductive Res (k : Nat)
  | ok (L : Ledger k)
  | neverGenerated (i : Fin k)
  | overDischarge (i : Fin k) (requested outstanding : Nat)

/-- The discharge rule of `obligation.rs`: zero is a no-op, then never-generated, then over-discharge. -/
def discharge (L : Ledger k) (i : Fin k) (c : Nat) : Res k :=
  if c = 0 then .ok L
  else if L.gen i = 0 then .neverGenerated i
  else if L.gen i - L.dis i < c then .overDischarge i c (L.gen i - L.dis i)
  else .ok ⟨L.gen, L.dis + c • single i⟩

theorem discharge_valid (L : Ledger k) (hv : L.Valid) (i : Fin k) (c : Nat) (L' : Ledger k)
    (h : discharge L i c = .ok L') : L'.Valid := by
  unfold discharge at h
  by_cases h0 : c = 0
  · simp only [h0, if_true, Res.ok.injEq] at h; subst h; exact hv
  · by_cases h1 : L.gen i = 0
    · simp [h0, h1] at h
    · by_cases h2 : L.gen i - L.dis i < c
      · simp [h0, h1, h2] at h
      · simp only [h0, h1, h2, if_false, Res.ok.injEq] at h
        subst h
        intro j
        by_cases hj : j = i
        · subst hj
          have := hv j
          simp [Ledger.Valid, single]
          omega
        · have := hv j
          simp [single, Pi.single_apply, hj]
          exact this

/-- Completeness: with a valid ledger, discharge succeeds exactly when the request fits the outstanding count. -/
theorem discharge_ok_iff (L : Ledger k) (hv : L.Valid) (i : Fin k) (c : Nat) :
    (∃ L', discharge L i c = .ok L') ↔ c ≤ L.gen i - L.dis i := by
  have hvi := hv i
  unfold discharge
  by_cases h0 : c = 0
  · simp [h0]
  · by_cases h1 : L.gen i = 0
    · have : L.gen i - L.dis i = 0 := by omega
      simp [h0, h1, this]
    · by_cases h2 : L.gen i - L.dis i < c
      · simp [h0, h1, h2]
      · simp [h0, h1, h2]
        omega

theorem discharge_never_generated (L : Ledger k) (i : Fin k) (c : Nat) (hc : c ≠ 0) (hg : L.gen i = 0) :
    discharge L i c = .neverGenerated i := by
  simp [discharge, hc, hg]

/-- The two failure modes are distinct: over-discharge needs a positive generated count. -/
theorem over_discharge_needs_generated (L : Ledger k) (hv : L.Valid) (i : Fin k) (c r o : Nat)
    (h : discharge L i c = .overDischarge i r o) : 0 < L.gen i ∧ o = L.gen i - L.dis i ∧ o < r := by
  unfold discharge at h
  by_cases h0 : c = 0
  · simp [h0] at h
  · by_cases h1 : L.gen i = 0
    · simp [h0, h1] at h
    · by_cases h2 : L.gen i - L.dis i < c
      · simp only [h0, h1, h2, if_false, if_true, Res.overDischarge.injEq] at h
        obtain ⟨_, hr, ho⟩ := h
        subst hr; subst ho
        exact ⟨Nat.pos_of_ne_zero h1, rfl, h2⟩
      · simp [h0, h1, h2] at h

/-! ### Whole traces: generation, runs and the invariant -/

/-- A ledger operation on `k` ids. -/
inductive Op (k : Nat)
  | gen (i : Fin k) (c : Nat)
  | dis (i : Fin k) (c : Nat)

/-- Unbounded generation adds to the generated vector; discharge is `discharge`. -/
def step (L : Ledger k) : Op k → Res k
  | .gen i c => .ok ⟨L.gen + c • single i, L.dis⟩
  | .dis i c => discharge L i c

/-- Run a trace; the first refusal stops the run. -/
def run : Ledger k → List (Op k) → Res k
  | L, [] => .ok L
  | L, o :: os =>
    match step L o with
    | .ok L' => run L' os
    | e => e

theorem empty_valid : (⟨0, 0⟩ : Ledger k).Valid := fun _ => Nat.le_refl _

theorem step_valid (L : Ledger k) (hv : L.Valid) (o : Op k) (L' : Ledger k) (h : step L o = .ok L') : L'.Valid := by
  cases o with
  | gen i c =>
    simp only [step, Res.ok.injEq] at h
    subst h
    intro j
    have := hv j
    simp only [combine_apply]
    omega
  | dis i c => exact discharge_valid L hv i c L' h

/-- Trace-level invariant: every successful run from a valid ledger (in particular from the empty ledger) ends valid,
i.e. discharged never exceeds generated, for every trace and every number of ids. -/
theorem run_valid : ∀ (os : List (Op k)) (L : Ledger k), L.Valid → ∀ L', run L os = .ok L' → L'.Valid
  | [], L, hv, L', h => by
    simp only [run, Res.ok.injEq] at h
    subst h
    exact hv
  | o :: os, L, hv, L', h => by
    unfold run at h
    cases hs : step L o with
    | ok L1 =>
      rw [hs] at h
      exact run_valid os L1 (step_valid L hv o L1 hs) L' h
    | neverGenerated i => rw [hs] at h; cases h
    | overDischarge i r o' => rw [hs] at h; cases h

theorem run_from_empty_valid (os : List (Op k)) (L' : Ledger k) (h : run ⟨0, 0⟩ os = .ok L') : L'.Valid :=
  run_valid os _ empty_valid L' h

/-- Bounded generation: the `CountOverflow` refusal is exactly `combineB` returning `none`. -/
def genB (M : Nat) (L : Ledger k) (i : Fin k) (c : Nat) : Option (Ledger k) :=
  (combineB M L.gen (c • single i)).map fun g => ⟨g, L.dis⟩

theorem genB_valid (M : Nat) (L : Ledger k) (hv : L.Valid) (i : Fin k) (c : Nat) (L' : Ledger k)
    (h : genB M L i c = some L') : L'.Valid := by
  unfold genB combineB at h
  by_cases hb : ∀ j, L.gen j + (c • single i) j ≤ M
  · rw [if_pos hb] at h
    simp only [Option.map_some, Option.some.injEq] at h
    subst h
    intro j
    have := hv j
    simp only [combine_apply]
    omega
  · rw [if_neg hb] at h
    simp at h

theorem genB_none_iff (M : Nat) (L : Ledger k) (i : Fin k) (c : Nat) :
    genB M L i c = none ↔ ∃ j, M < L.gen j + (c • single i) j := by
  unfold genB combineB
  by_cases hb : ∀ j, L.gen j + (c • single i) j ≤ M
  · rw [if_pos hb]
    simp only [Option.map_some]
    constructor
    · intro h; cases h
    · rintro ⟨j, hj⟩; have := hb j; omega
  · rw [if_neg hb]
    simp only [Option.map_none, true_iff]
    push Not at hb
    exact hb

/-- Labelled fixed instance: three ids, generate 2 of id 0, discharge 3. -/
theorem overdischarge_instance :
    discharge (k := 3) ⟨![2, 0, 0], 0⟩ 0 3 = .overDischarge 0 3 2 := by
  simp [discharge]

end ObligationMonoid

#print axioms ObligationMonoid.combine_assoc
#print axioms ObligationMonoid.combine_comm
#print axioms ObligationMonoid.combine_empty
#print axioms ObligationMonoid.combine_cancel
#print axioms ObligationMonoid.no_inverse
#print axioms ObligationMonoid.lift_single
#print axioms ObligationMonoid.lift_unique
#print axioms ObligationMonoid.trace_append
#print axioms ObligationMonoid.trace_total
#print axioms ObligationMonoid.trace_terms
#print axioms ObligationMonoid.trace_assertions
#print axioms ObligationMonoid.trace_destructive
#print axioms ObligationMonoid.cost_floor
#print axioms ObligationMonoid.valid_fresh_order_blind
#print axioms ObligationMonoid.trace_swap
#print axioms ObligationMonoid.event_table_not_injective
#print axioms ObligationMonoid.combineB_assoc
#print axioms ObligationMonoid.discharge_valid
#print axioms ObligationMonoid.discharge_ok_iff
#print axioms ObligationMonoid.discharge_never_generated
#print axioms ObligationMonoid.over_discharge_needs_generated
#print axioms ObligationMonoid.run_valid
#print axioms ObligationMonoid.run_from_empty_valid
#print axioms ObligationMonoid.genB_valid
#print axioms ObligationMonoid.genB_none_iff
#print axioms ObligationMonoid.overdischarge_instance
