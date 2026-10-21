import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Sum
import Mathlib.Data.Finset.Card
import Mathlib.Logic.Relation
import Mathlib.Data.List.Infix
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Nat.Log
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Genesis to universal computation: the word-rewriting core (C1 to C4, C8)

AuthorityEffect: None.

This module is the algebraic core of the chain from the inert mark `<>` toward
a universal machine.  It states, and kernel-checks, the following steps.

* C1  A finite alphabet is a set of admitted, pairwise separated marks.  The
  Genesis event semantics `stepE` is copied unchanged from a staged source (custody note below),
  the minimal regime with two separated marks is replayed, and the identity
  convention (PGW-IDENTITY-CONVENTION-UNDECIDABLE) is carried as an explicit
  declared input, never derived.
* C2  Words are `List α` (the free monoid).  A rewriting rule is a one-hole
  context plus a replacement; `Step` is the one-step relation and `Reach` its
  reflexive-transitive closure.  Letter renaming commutes with `Step` and
  `Reach` (the analogue of Genesis `Step.rename` and `Reach.rename`).  The
  Genesis notion of context (TFQ-0433, slot tuple with holes, a datum plugged
  into every hole) is mirrored by `GCtx` and related to one-hole word contexts
  by `oneHole_iff_split` and `plug1_ofSplit`.  Genesis `Step3` (staged source
  `dag/results/PG-GEN-REWRITING-COMMUTATION/.../Second/Rename.lean`) is a different relation, on
  states `(T, A, a, b)` of a finite term set, a finite assertion set and two named terms, with
  three moves: add a fresh term, add an assertion, identify two terms (a merge, which is not
  injective).  It has no order on terms and no user-supplied rule list.  It is therefore narrower
  and different from a semi-Thue step, and NO embedding of `Step3` into word rewriting is proved
  here; what is proved is the same commutation law for letter renaming (`Step.map`,
  `Reach.map`, `Reach.of_map`).
* C3  Bounded regimes: with finitely many marks and a declared word-length
  bound `L`, the reachability relation `ReachB` is decidable by an explicit
  procedure (`decideReachB_iff`), and the three-valued `verdict` is sound for
  the unbounded relation.  This decides rewriting steps and bounded reachability; the
  decision procedure over all Genesis contexts asked by TFQ-0497 is NOT built (only the unary
  hole-only mirror `UnarySep` is decidable).
* C4  Unbounded supply is an explicit import.  Genesis `stepE` has no cap on
  `admitDatum` (`replay_admitDatum_replicate`), so unbounded admission is
  PERMITTED by the event semantics, but every such event is host supplied
  (TFQ-0451, TFQ-0504); `UnboundedSupply` states the property that a regime reaches
  arbitrarily long words, which is the declared form of the import.
* C8  Binary coding of any finite alphabet and its decoder.

Nothing here derives the identity convention, the existence of more than two
separated marks beyond the declared construction, or the unbounded supply.
-/

namespace GenesisComputation

/-! ## Genesis custody copy -/

namespace GenesisCopy

/-- Copy of the sealed Genesis event semantics (19L57G1 `lean4/Derivation/Basic.lean`),
as staged byte for byte in
`dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean`
between its BEGIN COPY and END COPY markers. -/
abbrev Inst := Nat × List Nat

def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

structure Regime where
  data  : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs  : List (Nat × Nat)
deriving Repr, DecidableEq

inductive Event where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
deriving Repr, DecidableEq

def stepE (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none
  | .admitInst f args =>
      if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none

def replayE (h : List Event) (base : Regime) : Option Regime :=
  h.foldlM stepE base

end GenesisCopy

open GenesisCopy

/-! ## C1: alphabet from separation -/

/-- The empty regime. -/
def emptyRegime : Regime := ⟨0, [], [], [], []⟩

/-- Datum `i` is told apart from datum `j` by a unary form instance: some admitted unary
form has an instance on exactly one of them.  This is the unary, hole-only special case of
the Genesis `separable` (TFQ-0433) with derivability by instance membership; it is a mirror
defined here, not the external definition. -/
def UnarySep (r : Regime) (i j : Nat) : Prop :=
  ∃ f, f < r.forms.length ∧ r.forms.getD f 0 = 1 ∧
    ((f, [i]) ∈ r.insts ∧ (f, [j]) ∉ r.insts ∨ (f, [j]) ∈ r.insts ∧ (f, [i]) ∉ r.insts)

theorem unarySep_iff (r : Regime) (i j : Nat) :
    UnarySep r i j ↔ ∃ f ∈ List.range r.forms.length, r.forms.getD f 0 = 1 ∧
      ((f, [i]) ∈ r.insts ∧ (f, [j]) ∉ r.insts ∨ (f, [j]) ∈ r.insts ∧ (f, [i]) ∉ r.insts) := by
  simp [UnarySep]

/-- The unary separation test is decidable by a bounded search over the admitted forms. -/
instance (r : Regime) (i j : Nat) : Decidable (UnarySep r i j) :=
  decidable_of_iff _ (unarySep_iff r i j).symm

/-- Collapse (neither direction told apart) is decidable on a finite regime. -/
def Collapsed (r : Regime) (i j : Nat) : Prop :=
  ¬ UnarySep r i j ∧ ¬ UnarySep r j i

instance (r : Regime) (i j : Nat) : Decidable (Collapsed r i j) := by
  unfold Collapsed; infer_instance

/-- Every two distinct admitted marks of the regime are told apart. -/
def PairwiseSeparated (r : Regime) : Prop :=
  ∀ i j, i < r.data → j < r.data → i ≠ j → UnarySep r i j

theorem pairwiseSeparated_iff (r : Regime) :
    PairwiseSeparated r ↔ ∀ i ∈ List.range r.data, ∀ j ∈ List.range r.data, i ≠ j → UnarySep r i j := by
  simp only [PairwiseSeparated, List.mem_range]
  constructor
  · intro h i hi j hj hij; exact h i j hi hj hij
  · intro h i j hi hj hij; exact h i hi j hj hij

/-- Pairwise separation of a finite regime is decidable. -/
instance (r : Regime) : Decidable (PairwiseSeparated r) :=
  decidable_of_iff _ (pairwiseSeparated_iff r).symm

/-- The Genesis history that admits two marks, one unary form and one instance on mark 0,
and demands the pair `(0,1)`: the cost-two shape of the first separation (one form, one
instance).  The cost-two minimum itself is TFQ-0381 (its Lean twin is not in this checkout). -/
def firstSeparationHistory : List Event :=
  [.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0], .impose 0 1]

/-- The regime reached by the first-separation history. -/
def firstSeparationRegime : Regime :=
  ⟨2, [1], [(0, [0])], [], [(0, 1)]⟩

theorem first_separation_replay :
    replayE firstSeparationHistory emptyRegime = some firstSeparationRegime := by
  decide

theorem first_separation_pairwise : PairwiseSeparated firstSeparationRegime := by
  intro i j hi hj hij
  have hi2 : i < 2 := hi
  have hj2 : j < 2 := hj
  refine ⟨0, by decide, by decide, ?_⟩
  have hi01 : i = 0 ∨ i = 1 := by omega
  have hj01 : j = 0 ∨ j = 1 := by omega
  rcases hi01 with rfl | rfl <;> rcases hj01 with rfl | rfl <;> first | exact absurd rfl hij | decide

/-- The two marks of the minimal case. -/
inductive Mark2 | mark0 | mark1
  deriving DecidableEq, Repr

instance : Fintype Mark2 :=
  ⟨{Mark2.mark0, Mark2.mark1}, by intro x; cases x <;> simp⟩

theorem Mark2.card : Fintype.card Mark2 = 2 := rfl

theorem mark0_ne_mark1 : Mark2.mark0 ≠ Mark2.mark1 := by decide

/-- The two marks of `Mark2` are the data `0` and `1` of the first-separation regime. -/
def Mark2.toDatum : Mark2 → Fin firstSeparationRegime.data
  | .mark0 => ⟨0, by decide⟩
  | .mark1 => ⟨1, by decide⟩

theorem Mark2.toDatum_bijective : Function.Bijective Mark2.toDatum := by
  refine ⟨?_, ?_⟩
  · intro a b h; cases a <;> cases b <;> simp_all [Mark2.toDatum]
  · intro d
    obtain ⟨d, hd⟩ := d
    have : d = 0 ∨ d = 1 := by
      have : d < 2 := hd
      omega
    rcases this with rfl | rfl
    · exact ⟨.mark0, rfl⟩
    · exact ⟨.mark1, rfl⟩

/-- The canonical regime on `n` marks: `n` data, `n-1` unary forms, and the instance
`(i,[i])` for `i < n-1`. -/
def canonicalRegime (n : Nat) : Regime :=
  ⟨n, List.replicate (n - 1) 1, (List.range (n - 1)).map (fun i => (i, [i])), [], []⟩

theorem canonicalRegime_pairwise (n : Nat) : PairwiseSeparated (canonicalRegime n) := by
  intro i j hi hj hij
  have hi' : i < n := hi
  have hj' : j < n := hj
  have key : ∀ a b, a < n → b < n → a < n - 1 → a ≠ b → UnarySep (canonicalRegime n) a b := by
    intro a b ha hb ha1 hab
    refine ⟨a, ?_, ?_, Or.inl ⟨?_, ?_⟩⟩
    · simpa [canonicalRegime] using ha1
    · simp [canonicalRegime, ha1]
    · simp [canonicalRegime, ha1]
    · simp [canonicalRegime, Ne.symm hab]
  by_cases h : i < n - 1
  · exact key i j hi' hj' h hij
  · have hj1 : j < n - 1 := by omega
    obtain ⟨f, hf1, hf2, hf3⟩ := key j i hj' hi' hj1 (Ne.symm hij)
    exact ⟨f, hf1, hf2, hf3.symm⟩

/-- Decided by the bounded search: the canonical regime on four marks is pairwise separated. -/
theorem canonicalRegime_four_pairwise_decide : PairwiseSeparated (canonicalRegime 4) := by
  decide

/-- Decided by the bounded search: two admitted marks with no form at all are collapsed
(here the opaque identity convention leaves `<>` and its successor unseparated). -/
theorem two_marks_without_forms_collapsed : Collapsed ⟨2, [], [], [], []⟩ 0 1 := by
  decide

/-- The identity conventions are not derived: this is the declared input of C1
(PGW-IDENTITY-CONVENTION-UNDECIDABLE).  The opaque convention identifies marks the regime
cannot tell apart; the exact-inscription convention keeps every distinct inscription. -/
inductive IdentityConvention | opaqueConv | exactInscription
  deriving DecidableEq, Repr

/-- Under the opaque convention, a pairwise separated alphabet has no identifications, so
both conventions give the same set of marks on a separated alphabet.  Blank and state
marks must therefore be admitted as separated marks as well, or the convention must be
declared. -/
theorem separated_marks_not_collapsed {r : Regime} (h : PairwiseSeparated r) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) (hij : i ≠ j) : ¬ Collapsed r i j :=
  fun hc => hc.1 (h i j hi hj hij)

/-! ## C2: words, contexts, semi-Thue systems -/

section Rewriting

variable {α β : Type*}

/-- A one-hole context over words. -/
abbrev Ctx (α : Type*) := List α × List α

def Ctx.plug (c : Ctx α) (w : List α) : List α := c.1 ++ w ++ c.2

/-- One rewriting step: a rule `l → r` of the rule predicate `R` applied inside a one-hole
context. -/
def Step (R : List α → List α → Prop) (w w' : List α) : Prop :=
  ∃ l r u v, R l r ∧ w = u ++ l ++ v ∧ w' = u ++ r ++ v

/-- Reachability: the reflexive-transitive closure of `Step`. -/
def Reach (R : List α → List α → Prop) : List α → List α → Prop :=
  Relation.ReflTransGen (Step R)

theorem step_iff_plug {R : List α → List α → Prop} {w w' : List α} :
    Step R w w' ↔ ∃ l r, ∃ c : Ctx α, R l r ∧ w = c.plug l ∧ w' = c.plug r := by
  constructor
  · rintro ⟨l, r, u, v, h, rfl, rfl⟩; exact ⟨l, r, (u, v), h, rfl, rfl⟩
  · rintro ⟨l, r, ⟨u, v⟩, h, rfl, rfl⟩; exact ⟨l, r, u, v, h, rfl, rfl⟩

theorem Step.context {R : List α → List α → Prop} {w w' : List α} (h : Step R w w')
    (u v : List α) : Step R (u ++ w ++ v) (u ++ w' ++ v) := by
  obtain ⟨l, r, u', v', hr, rfl, rfl⟩ := h
  exact ⟨l, r, u ++ u', v' ++ v, hr, by simp, by simp⟩

theorem Reach.context {R : List α → List α → Prop} {w w' : List α} (h : Reach R w w')
    (u v : List α) : Reach R (u ++ w ++ v) (u ++ w' ++ v) := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hs ih => exact ih.tail (hs.context u v)

theorem Step.mono {R S : List α → List α → Prop} (hRS : ∀ l r, R l r → S l r) {w w' : List α}
    (h : Step R w w') : Step S w w' := by
  obtain ⟨l, r, u, v, hr, rfl, rfl⟩ := h
  exact ⟨l, r, u, v, hRS l r hr, rfl, rfl⟩

theorem Reach.mono {R S : List α → List α → Prop} (hRS : ∀ l r, R l r → S l r) {w w' : List α}
    (h : Reach R w w') : Reach S w w' :=
  by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hs ih => exact ih.tail (Step.mono hRS hs)

/-- The rule predicate transported along a letter map. -/
def mapRule (f : α → β) (R : List α → List α → Prop) : List β → List β → Prop :=
  fun l' r' => ∃ l r, R l r ∧ l' = l.map f ∧ r' = r.map f

/-- Letter maps carry steps to steps (analogue of Genesis `Step.rename`). -/
theorem Step.map (f : α → β) {R : List α → List α → Prop} {w w' : List α}
    (h : Step R w w') : Step (mapRule f R) (w.map f) (w'.map f) := by
  obtain ⟨l, r, u, v, hr, rfl, rfl⟩ := h
  exact ⟨l.map f, r.map f, u.map f, v.map f, ⟨l, r, hr, rfl, rfl⟩, by simp, by simp⟩

/-- Letter maps carry sequences of steps to sequences of steps (analogue of `Reach.rename`). -/
theorem Reach.map (f : α → β) {R : List α → List α → Prop} {w w' : List α}
    (h : Reach R w w') : Reach (mapRule f R) (w.map f) (w'.map f) := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hs ih => exact ih.tail (hs.map f)

/-- For an injective letter map a step from a renamed word comes from a step on the
original word. -/
theorem Step.exists_of_map {f : α → β} (hf : Function.Injective f)
    {R : List α → List α → Prop} {w : List α} {z : List β}
    (h : Step (mapRule f R) (w.map f) z) : ∃ w2, z = w2.map f ∧ Step R w w2 := by
  obtain ⟨l', r', u', v', ⟨l, r, hr, rfl, rfl⟩, h1, h2⟩ := h
  have hm := List.map_injective_iff.2 hf
  have h1' : w.map f = (u' ++ l.map f) ++ v' := by simpa [List.append_assoc] using h1
  obtain ⟨a, v, hw, ha, hv⟩ := List.map_eq_append_iff.1 h1'
  obtain ⟨u, l2, hw2, hu, hl⟩ := List.map_eq_append_iff.1 ha
  have hl2 : l2 = l := hm hl
  subst hl2
  subst hw2
  refine ⟨u ++ r ++ v, ?_, ⟨l2, r, u, v, hr, by simpa using hw, rfl⟩⟩
  rw [h2]; simp [hu, hv]

theorem Reach.exists_of_map {f : α → β} (hf : Function.Injective f)
    {R : List α → List α → Prop} {w : List α} {y : List β}
    (h : Reach (mapRule f R) (w.map f) y) : ∃ w2, y = w2.map f ∧ Reach R w w2 := by
  induction h with
  | refl => exact ⟨w, rfl, Relation.ReflTransGen.refl⟩
  | tail _ hs ih =>
      obtain ⟨w2, rfl, hw2⟩ := ih
      obtain ⟨w3, hz, hs3⟩ := Step.exists_of_map hf hs
      exact ⟨w3, hz, hw2.tail hs3⟩

theorem Reach.of_map {f : α → β} (hf : Function.Injective f) {R : List α → List α → Prop}
    {w w' : List α} (h : Reach (mapRule f R) (w.map f) (w'.map f)) : Reach R w w' := by
  obtain ⟨w2, h2, hw⟩ := Reach.exists_of_map hf h
  have := (List.map_injective_iff.2 hf) h2
  subst this
  exact hw

end Rewriting

/-! ### Genesis contexts and one-hole word contexts (TFQ-0433) -/

section GenesisContexts

variable {α : Type*}

/-- A Genesis-style context: a tuple of slots, each a datum or a hole (`none`). -/
abbrev GCtx (α : Type*) := List (Option α)

/-- Plugging one datum into every hole, as in TFQ-0433. -/
def plug1 (d : α) (c : GCtx α) : List α := c.map (fun o => o.getD d)

/-- The number of holes of a context. -/
def holes (c : GCtx α) : ℕ := c.countP Option.isNone

/-- The context with letters `u`, one hole, then letters `v`. -/
def ofSplit (u v : List α) : GCtx α := u.map some ++ none :: v.map some

theorem plug1_ofSplit (d : α) (u v : List α) : plug1 d (ofSplit u v) = u ++ d :: v := by
  simp [plug1, ofSplit, List.map_map, Function.comp_def]

theorem plug1_ofSplit_eq_plug (d : α) (u v : List α) :
    plug1 d (ofSplit u v) = Ctx.plug (u, v) [d] := by
  simp [plug1_ofSplit, Ctx.plug]

private theorem holes_map_some (l : List α) : (l.map some).countP Option.isNone = 0 := by
  induction l with
  | nil => rfl
  | cons a l ih => simpa [List.countP_cons] using ih

theorem holes_ofSplit (u v : List α) : holes (ofSplit u v) = 1 := by
  unfold holes ofSplit
  rw [List.countP_append, holes_map_some, List.countP_cons, holes_map_some]
  simp

private theorem exists_allSome (c : GCtx α) (h : holes c = 0) : ∃ v : List α, c = v.map some := by
  induction c with
  | nil => exact ⟨[], rfl⟩
  | cons o c ih =>
      cases o with
      | none => simp [holes, List.countP_cons] at h
      | some a =>
          have h' : holes c = 0 := by simpa [holes, List.countP_cons] using h
          obtain ⟨v, rfl⟩ := ih h'
          exact ⟨a :: v, rfl⟩

/-- A context has exactly one hole iff it is `ofSplit u v` for some letters `u`, `v`. -/
theorem oneHole_iff_split (c : GCtx α) : holes c = 1 ↔ ∃ u v : List α, c = ofSplit u v := by
  constructor
  · intro h
    induction c with
    | nil => simp [holes] at h
    | cons o c ih =>
        cases o with
        | none =>
            have h' : holes c = 0 := by simpa [holes, List.countP_cons] using h
            obtain ⟨v, rfl⟩ := exists_allSome c h'
            exact ⟨[], v, rfl⟩
        | some a =>
            have h' : holes c = 1 := by simpa [holes, List.countP_cons] using h
            obtain ⟨u, v, rfl⟩ := ih h'
            exact ⟨a :: u, v, by simp [ofSplit]⟩
  · rintro ⟨u, v, rfl⟩; exact holes_ofSplit u v

/-- The split of a one-hole context is unique. -/
theorem ofSplit_injective {u u' v v' : List α} (h : ofSplit u v = ofSplit u' v') :
    u = u' ∧ v = v' := by
  induction u generalizing u' with
  | nil =>
      cases u' with
      | nil => simp [ofSplit] at h; exact ⟨rfl, List.map_injective_iff.2 (Option.some_injective _) h⟩
      | cons a u' => simp [ofSplit] at h
  | cons a u ih =>
      cases u' with
      | nil => simp [ofSplit] at h
      | cons a' u' =>
          simp only [ofSplit, List.map_cons, List.cons_append, List.cons.injEq,
            Option.some.injEq] at h
          obtain ⟨rfl, h2⟩ := h
          obtain ⟨h3, h4⟩ := ih (u' := u') (by simpa [ofSplit] using h2)
          exact ⟨by rw [h3], h4⟩

/-- All contexts of a given arity over the letters `xs`. -/
def allCtxs (xs : List α) : ℕ → List (GCtx α)
  | 0 => [[]]
  | a + 1 => (none :: xs.map some).flatMap fun o => (allCtxs xs a).map (o :: ·)

end GenesisContexts

/-- Contexts of arity 3 over 2 data with at least one hole: `(2+1)^3 - 2^3 = 19`
(the TFQ-0436 count). -/
theorem genesis_context_count_n2_a3 :
    ((allCtxs [0, 1] 3 : List (GCtx Nat)).filter (fun c => 0 < holes c)).length = 19 := by
  decide

/-- Of those, the contexts with exactly one hole number `3 * 2^2 = 12`, the pairs `(u, v)`
with `|u| + |v| = 2`. -/
theorem genesis_one_hole_count_n2_a3 :
    ((allCtxs [0, 1] 3 : List (GCtx Nat)).filter (fun c => holes c == 1)).length = 12 := by
  decide

/-! ## C3: bounded regimes -/

section Closure

variable {β : Type*} [DecidableEq β]

/-- States reachable in at most `n` steps of the successor map `s`. -/
def reachN (s : β → Finset β) : ℕ → β → Finset β
  | 0, a => {a}
  | n + 1, a => reachN s n a ∪ (reachN s n a).biUnion s

theorem reachN_succ_subset (s : β → Finset β) (n : ℕ) (a : β) :
    reachN s n a ⊆ reachN s (n + 1) a := Finset.subset_union_left

theorem reachN_mono (s : β → Finset β) {m n : ℕ} (h : m ≤ n) (a : β) :
    reachN s m a ⊆ reachN s n a := by
  induction h with
  | refl => exact Finset.Subset.refl _
  | step _ ih => exact ih.trans (reachN_succ_subset s _ a)

theorem mem_reachN_self (s : β → Finset β) (n : ℕ) (a : β) : a ∈ reachN s n a :=
  reachN_mono s (Nat.zero_le n) a (Finset.mem_singleton_self a)

theorem mem_reachN_step (s : β → Finset β) {n : ℕ} {a b c : β} (hb : b ∈ reachN s n a)
    (hc : c ∈ s b) : c ∈ reachN s (n + 1) a :=
  Finset.mem_union_right _ (Finset.mem_biUnion.2 ⟨b, hb, hc⟩)

theorem rtg_of_mem_reachN (s : β → Finset β) {n : ℕ} {a b : β} (h : b ∈ reachN s n a) :
    Relation.ReflTransGen (fun x y => y ∈ s x) a b := by
  induction n generalizing b with
  | zero => rw [reachN, Finset.mem_singleton] at h; subst h; exact Relation.ReflTransGen.refl
  | succ n ih =>
      rcases Finset.mem_union.1 h with h | h
      · exact ih h
      · obtain ⟨x, hx, hb⟩ := Finset.mem_biUnion.1 h
        exact (ih hx).tail hb

theorem exists_mem_reachN_of_rtg (s : β → Finset β) {a b : β}
    (h : Relation.ReflTransGen (fun x y => y ∈ s x) a b) : ∃ n, b ∈ reachN s n a := by
  induction h with
  | refl => exact ⟨0, Finset.mem_singleton_self a⟩
  | tail _ hs ih =>
      obtain ⟨n, hn⟩ := ih
      exact ⟨n + 1, mem_reachN_step s hn hs⟩

theorem reachN_stable_all (s : β → Finset β) (a : β) (m : ℕ)
    (h : reachN s m a = reachN s (m + 1) a) : ∀ k, reachN s (m + k) a = reachN s m a := by
  intro k
  induction k with
  | zero => rfl
  | succ k ih =>
      calc reachN s (m + k + 1) a
          = reachN s (m + k) a ∪ (reachN s (m + k) a).biUnion s := rfl
        _ = reachN s m a ∪ (reachN s m a).biUnion s := by rw [ih]
        _ = reachN s (m + 1) a := rfl
        _ = reachN s m a := h.symm

theorem reachN_grow (s : β → Finset β) (a : β) (n : ℕ) :
    reachN s n a = reachN s (n + 1) a ∨ n + 1 ≤ (reachN s n a).card := by
  induction n with
  | zero => right; simp [reachN]
  | succ n ih =>
      by_cases h : reachN s (n + 1) a = reachN s (n + 1 + 1) a
      · left; exact h
      · right
        have hne : reachN s n a ≠ reachN s (n + 1) a := by
          intro heq
          apply h
          have h1 := reachN_stable_all s a n heq 1
          have h2 := reachN_stable_all s a n heq 2
          rw [show n + 1 + 1 = n + 2 from rfl, h2]
          exact h1
        rcases ih with heq | hcard
        · exact absurd heq hne
        · have hss : reachN s n a ⊂ reachN s (n + 1) a :=
            Finset.ssubset_iff_subset_ne.2 ⟨reachN_succ_subset s n a, hne⟩
          have := Finset.card_lt_card hss
          omega

/-- With a finite universe `U` closed under `s`, the closure stabilises after `|U|` rounds. -/
theorem reachN_card_stable (s : β → Finset β) (U : Finset β) (hU : ∀ x ∈ U, s x ⊆ U)
    {a : β} (ha : a ∈ U) : reachN s U.card a = reachN s (U.card + 1) a := by
  have hsub : ∀ n, reachN s n a ⊆ U := by
    intro n
    induction n with
    | zero => simpa [reachN] using ha
    | succ n ih =>
        intro x hx
        rcases Finset.mem_union.1 hx with hx | hx
        · exact ih hx
        · obtain ⟨y, hy, hxy⟩ := Finset.mem_biUnion.1 hx
          exact hU y (ih hy) hxy
  rcases reachN_grow s a U.card with h | h
  · exact h
  · have := Finset.card_le_card (hsub U.card)
    omega

theorem rtg_iff_mem_reachN_card (s : β → Finset β) (U : Finset β) (hU : ∀ x ∈ U, s x ⊆ U)
    {a : β} (ha : a ∈ U) (b : β) :
    Relation.ReflTransGen (fun x y => y ∈ s x) a b ↔ b ∈ reachN s U.card a := by
  constructor
  · intro h
    obtain ⟨n, hn⟩ := exists_mem_reachN_of_rtg s h
    by_cases hle : n ≤ U.card
    · exact reachN_mono s hle a hn
    · obtain ⟨k, hk⟩ := Nat.exists_eq_add_of_le (Nat.le_of_not_le hle)
      have := reachN_stable_all s a U.card (reachN_card_stable s U hU ha) k
      rw [hk, this] at hn
      exact hn
  · exact rtg_of_mem_reachN s

end Closure

section Bounded

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- All words of length at most `n`. -/
def wordsLE (α : Type*) [Fintype α] [DecidableEq α] : ℕ → Finset (List α)
  | 0 => {[]}
  | n + 1 => insert [] (Finset.univ.biUnion fun a => (wordsLE α n).image (List.cons a))

theorem mem_wordsLE {n : ℕ} {w : List α} : w ∈ wordsLE α n ↔ w.length ≤ n := by
  induction n generalizing w with
  | zero => simp [wordsLE]
  | succ n ih =>
      cases w with
      | nil => simp [wordsLE]
      | cons a w => simp [wordsLE, ih]

/-- The configuration space of a bounded regime has exactly `1 + k + ... + k^L` words,
where `k` is the number of marks. -/
theorem card_wordsLE (n : ℕ) :
    (wordsLE α n).card = ∑ i ∈ Finset.range (n + 1), Fintype.card α ^ i := by
  induction n with
  | zero => simp [wordsLE]
  | succ n ih =>
      have hnot : ([] : List α) ∉ Finset.univ.biUnion fun a => (wordsLE α n).image (List.cons a) := by
        simp
      rw [wordsLE, Finset.card_insert_of_notMem hnot]
      rw [Finset.card_biUnion]
      · have : ∀ a : α, ((wordsLE α n).image (List.cons a)).card = (wordsLE α n).card := by
          intro a
          exact Finset.card_image_of_injective _ (List.cons_injective)
        simp only [this, Finset.sum_const, Finset.card_univ, smul_eq_mul]
        rw [ih, Finset.sum_range_succ' _ (n + 1), Finset.mul_sum]
        simp [pow_succ, mul_comm, add_comm]
      · intro a _ b _ hab
        simp only [Function.onFun]
        rw [Finset.disjoint_left]
        intro w hwa hwb
        obtain ⟨x, _, hx⟩ := Finset.mem_image.1 hwa
        obtain ⟨y, _, hy⟩ := Finset.mem_image.1 hwb
        exact hab (List.cons.inj (hx.trans hy.symm)).1

/-- A finite list of rules `l → r`. -/
abbrev RuleList (α : Type*) := List (List α × List α)

/-- The rule predicate of a rule list. -/
def inRules (RL : RuleList α) : List α → List α → Prop := fun l r => (l, r) ∈ RL

/-- Every word reachable from `w` by one step of the rule list, computed by scanning the
positions of `w`. -/
def succList (RL : RuleList α) (w : List α) : List (List α) :=
  RL.flatMap fun p => (List.range (w.length + 1)).filterMap fun i =>
    if p.1 <+: w.drop i then some (w.take i ++ p.2 ++ w.drop (i + p.1.length)) else none

theorem mem_succList {RL : RuleList α} {w w' : List α} :
    w' ∈ succList RL w ↔ Step (inRules RL) w w' := by
  constructor
  · intro h
    simp only [succList, List.mem_flatMap, List.mem_filterMap, List.mem_range] at h
    obtain ⟨p, hp, i, hi, hx⟩ := h
    by_cases hpre : p.1 <+: w.drop i
    · simp only [hpre, ↓reduceIte] at hx
      have hw' : w' = w.take i ++ p.2 ++ w.drop (i + p.1.length) := (Option.some.inj hx).symm
      obtain ⟨t, ht⟩ := hpre
      have h1 : w.drop (i + p.1.length) = t := by
        have := congrArg (List.drop p.1.length) ht
        rw [List.drop_append_of_le_length le_rfl] at this
        simpa [List.drop_drop, Nat.add_comm] using this.symm
      refine ⟨p.1, p.2, w.take i, t, hp, ?_, ?_⟩
      · rw [List.append_assoc, ht, List.take_append_drop]
      · rw [hw', h1]
    · simp only [hpre, ↓reduceIte] at hx; cases hx
  · rintro ⟨l, r, u, v, hr, rfl, rfl⟩
    simp only [succList, List.mem_flatMap, List.mem_filterMap, List.mem_range]
    refine ⟨(l, r), hr, u.length, by simp only [List.length_append]; omega, ?_⟩
    have h1 : (u ++ l ++ v).drop u.length = l ++ v := by simp
    have h2 : (u ++ l ++ v).take u.length = u := by simp
    have h3 : (u ++ l ++ v).drop (u.length + l.length) = v := by simp
    simp [h1, h2, h3]

/-- The words of length at most `L` one step from `w` inside the bound. -/
def sB (RL : RuleList α) (L : ℕ) (w : List α) : Finset (List α) :=
  ((succList RL w).filter (fun x => decide (x.length ≤ L))).toFinset

/-- One step of the bounded regime: both words respect the declared length bound `L`. -/
def StepB (RL : RuleList α) (L : ℕ) (w w' : List α) : Prop :=
  w.length ≤ L ∧ w'.length ≤ L ∧ Step (inRules RL) w w'

/-- Bounded reachability. -/
def ReachB (RL : RuleList α) (L : ℕ) : List α → List α → Prop :=
  Relation.ReflTransGen (StepB RL L)

theorem stepB_iff {RL : RuleList α} {L : ℕ} {w w' : List α} :
    StepB RL L w w' ↔ w.length ≤ L ∧ w' ∈ sB RL L w := by
  have hmem : w' ∈ sB RL L w ↔ w'.length ≤ L ∧ Step (inRules RL) w w' := by
    simp [sB, mem_succList, and_comm]
  rw [hmem]
  unfold StepB
  tauto

theorem sB_subset {RL : RuleList α} {L : ℕ} : ∀ x ∈ wordsLE α L, sB RL L x ⊆ wordsLE α L := by
  intro x _ y hy
  simp only [sB, List.mem_toFinset, List.mem_filter, decide_eq_true_eq] at hy
  exact mem_wordsLE.2 hy.2

/-- The set of words reachable from `a` inside the bound `L`. -/
def reachSet (RL : RuleList α) (L : ℕ) (a : List α) : Finset (List α) :=
  reachN (sB RL L) (wordsLE α L).card a

theorem reachB_iff {RL : RuleList α} {L : ℕ} {a b : List α} (ha : a.length ≤ L) :
    ReachB RL L a b ↔ b ∈ reachSet RL L a := by
  unfold reachSet
  rw [← rtg_iff_mem_reachN_card (sB RL L) (wordsLE α L) sB_subset (mem_wordsLE.2 ha)]
  constructor
  · intro h
    induction h with
    | refl => exact Relation.ReflTransGen.refl
    | tail _ hs ih => exact ih.tail (stepB_iff.1 hs).2
  · intro h
    have key : ∀ b, Relation.ReflTransGen (fun x y => y ∈ sB RL L x) a b →
        b.length ≤ L ∧ ReachB RL L a b := by
      intro b h
      induction h with
      | refl => exact ⟨ha, Relation.ReflTransGen.refl⟩
      | tail _ hs ih =>
          obtain ⟨hl, hr⟩ := ih
          have : StepB RL L _ _ := stepB_iff.2 ⟨hl, hs⟩
          exact ⟨this.2.1, hr.tail this⟩
    exact (key b h).2

/-- The bounded reachability relation is decidable, with an explicit procedure. -/
def decideReachB (RL : RuleList α) (L : ℕ) (a b : List α) : Bool :=
  decide (b ∈ reachSet RL L a)

theorem decideReachB_iff {RL : RuleList α} {L : ℕ} {a b : List α} (ha : a.length ≤ L) :
    decideReachB RL L a b = true ↔ ReachB RL L a b := by
  simp [decideReachB, reachB_iff ha]

/-- The bounded configuration space is finite: at most `1 + k + ... + k^L` words are
reachable from any start. -/
theorem reachSet_card_le (RL : RuleList α) (L : ℕ) {a : List α} (ha : a.length ≤ L) :
    (reachSet RL L a).card ≤ ∑ i ∈ Finset.range (L + 1), Fintype.card α ^ i := by
  rw [← card_wordsLE]
  apply Finset.card_le_card
  intro x hx
  have := (reachB_iff ha).2 hx
  have key : ∀ b, ReachB RL L a b → b.length ≤ L := by
    intro b h
    cases h with
    | refl => exact ha
    | tail _ hs => exact hs.2.1
  exact mem_wordsLE.2 (key x this)

/-- Bounded reachability is sound for unbounded reachability. -/
theorem ReachB.reach {RL : RuleList α} {L : ℕ} {a b : List α} (h : ReachB RL L a b) :
    Reach (inRules RL) a b := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hs ih => exact ih.tail hs.2.2

theorem ReachB.mono_bound {RL : RuleList α} {L L' : ℕ} (hL : L ≤ L') {a b : List α}
    (h : ReachB RL L a b) : ReachB RL L' a b := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hs ih => exact ih.tail ⟨hs.1.trans hL, hs.2.1.trans hL, hs.2.2⟩

theorem ReachB.length_le {RL : RuleList α} {L : ℕ} {a b : List α} (ha : a.length ≤ L)
    (h : ReachB RL L a b) : b.length ≤ L := by
  cases h with
  | refl => exact ha
  | tail _ hs => exact hs.2.1

/-- Every unbounded reach is a bounded reach for some bound: unbounded reachability is the
directed union of the decidable bounded relations. -/
theorem Reach.exists_bound {RL : RuleList α} {a b : List α} (h : Reach (inRules RL) a b) :
    ∃ L, a.length ≤ L ∧ ReachB RL L a b := by
  induction h with
  | refl => exact ⟨a.length, le_rfl, Relation.ReflTransGen.refl⟩
  | @tail b c _ hs ih =>
      obtain ⟨L, haL, hL⟩ := ih
      have hbL := ReachB.length_le haL hL
      refine ⟨max L c.length, haL.trans (le_max_left _ _), ?_⟩
      exact (hL.mono_bound (le_max_left _ _)).tail
        ⟨hbL.trans (le_max_left _ _), le_max_right _ _, hs⟩

end Bounded


section Verdict

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- No word reachable inside the bound has a step that leaves the bound. -/
def Closed (RL : RuleList α) (L : ℕ) (a : List α) : Prop :=
  ∀ w ∈ reachSet RL L a, ∀ w' ∈ succList RL w, w'.length ≤ L

instance (RL : RuleList α) (L : ℕ) (a : List α) : Decidable (Closed RL L a) := by
  unfold Closed; infer_instance

/-- The verdicts of the bounded decider on the question "is `b` reachable from `a`?". -/
inductive Verdict
  | reachable
  | unreachable
  | boundExceeded
  deriving DecidableEq, Repr

/-- The three-valued bounded decider. `boundExceeded` is returned only when some word reached
inside the bound has a step that would leave the bound, so the bounded search cannot settle
the unbounded question. -/
def verdict (RL : RuleList α) (L : ℕ) (a b : List α) : Verdict :=
  if b ∈ reachSet RL L a then .reachable
  else if Closed RL L a then .unreachable
  else .boundExceeded

theorem closed_reach {RL : RuleList α} {L : ℕ} {a : List α} (ha : a.length ≤ L)
    (hc : Closed RL L a) {b : List α} (h : Reach (inRules RL) a b) : b ∈ reachSet RL L a := by
  induction h with
  | refl => exact mem_reachN_self _ _ _
  | @tail b c _ hs ih =>
      have hlen : c.length ≤ L := hc b ih c (mem_succList.2 hs)
      have hc' : c ∈ sB RL L b := by
        simp only [sB, List.mem_toFinset, List.mem_filter, decide_eq_true_eq]
        exact ⟨mem_succList.2 hs, hlen⟩
      have h1 := mem_reachN_step (sB RL L) ih hc'
      have h2 := reachN_card_stable (sB RL L) (wordsLE α L) sB_subset (mem_wordsLE.2 ha)
      unfold reachSet
      rw [h2]
      exact h1

/-- When the bounded search is closed, unbounded and bounded reachability agree. -/
theorem reach_iff_reachB_of_closed {RL : RuleList α} {L : ℕ} {a : List α}
    (ha : a.length ≤ L) (hc : Closed RL L a) (b : List α) :
    Reach (inRules RL) a b ↔ ReachB RL L a b :=
  ⟨fun h => (reachB_iff ha).2 (closed_reach ha hc h), ReachB.reach⟩

theorem verdict_reachable_sound {RL : RuleList α} {L : ℕ} {a b : List α} (ha : a.length ≤ L)
    (h : verdict RL L a b = .reachable) : Reach (inRules RL) a b := by
  unfold verdict at h
  split_ifs at h with hb
  exact ((reachB_iff ha).2 hb).reach

theorem verdict_unreachable_sound {RL : RuleList α} {L : ℕ} {a b : List α} (ha : a.length ≤ L)
    (h : verdict RL L a b = .unreachable) : ¬ Reach (inRules RL) a b := by
  unfold verdict at h
  split_ifs at h with hb hc
  intro hr
  exact hb (closed_reach ha hc hr)

theorem verdict_boundExceeded_witness {RL : RuleList α} {L : ℕ} {a b : List α}
    (h : verdict RL L a b = .boundExceeded) :
    ∃ w ∈ reachSet RL L a, ∃ w', Step (inRules RL) w w' ∧ L < w'.length := by
  unfold verdict at h
  split_ifs at h with hb hc
  unfold Closed at hc
  simp only [not_forall, not_le] at hc
  obtain ⟨w, hw, w', hw', hlen⟩ := hc
  exact ⟨w, hw, w', mem_succList.1 hw', hlen⟩

/-- A regime that reaches arbitrarily long words is never closed at any bound: the bounded
decider returns `boundExceeded` or `reachable`, never `unreachable`.  This is the declared
shape of the unbounded-supply import (C4). -/
def UnboundedSupply (RL : RuleList α) (a : List α) : Prop :=
  ∀ L, ∃ w, Reach (inRules RL) a w ∧ L < w.length

theorem not_closed_of_unbounded {RL : RuleList α} {a : List α} (hu : UnboundedSupply RL a)
    {L : ℕ} (ha : a.length ≤ L) : ¬ Closed RL L a := by
  intro hc
  obtain ⟨w, hw, hlen⟩ := hu L
  have hmem := closed_reach ha hc hw
  have := ((reachB_iff ha).2 hmem).length_le ha
  omega

/-- Bounded regimes cannot be unbounded: a closed bounded search has only words of length at
most `L` reachable. -/
theorem closed_bounds_reach {RL : RuleList α} {L : ℕ} {a : List α} (ha : a.length ≤ L)
    (hc : Closed RL L a) {w : List α} (h : Reach (inRules RL) a w) : w.length ≤ L :=
  ((reachB_iff ha).2 (closed_reach ha hc h)).length_le ha

end Verdict

/-! ## C4: unbounded supply as a declared import -/

section Supply

open GenesisCopy

theorem replayE_cons (e : Event) (h : List Event) (base : Regime) :
    replayE (e :: h) base = (stepE base e).bind (fun r => replayE h r) := rfl

/-- The Genesis event semantics has no cap on admission: `k` copies of `admitDatum` admit `k`
data.  Unbounded admission is permitted by `stepE`; every such event is host supplied
(TFQ-0451, TFQ-0504). -/
theorem replay_admitDatum_replicate (k : ℕ) (base : Regime) :
    replayE (List.replicate k .admitDatum) base = some { base with data := base.data + k } := by
  induction k generalizing base with
  | zero => rfl
  | succ k ih =>
      rw [List.replicate_succ, replayE_cons]
      show replayE (List.replicate k .admitDatum) { base with data := base.data + 1 } = _
      rw [ih]
      simp [Nat.add_assoc, Nat.add_comm 1 k]

theorem genesis_unbounded_admission (n : ℕ) :
    ∃ h : List Event, ∃ r, replayE h emptyRegime = some r ∧ n ≤ r.data :=
  ⟨List.replicate n .admitDatum, _, replay_admitDatum_replicate n emptyRegime, by simp [emptyRegime]⟩

/-- No Genesis event lowers the number of admitted data. -/
theorem stepE_data_mono {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r.data ≤ r'.data := by
  cases e <;> simp only [stepE] at h <;> (try split_ifs at h) <;> (cases h; simp)

/-- The arithmetic of the supply term in the demand accounting `s' = s - d + b`
(PG-DEMAND-ACCOUNTING): if every round has strictly more births than discharges, the active
count grows without bound.  The births are an input; Genesis does not derive them. -/
theorem supply_growth (s d b : ℕ → ℕ) (hd : ∀ n, d n ≤ s n)
    (hs : ∀ n, s (n + 1) = s n - d n + b n) (hb : ∀ n, d n < b n) :
    ∀ n, s 0 + n ≤ s n := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      have h1 := hs n
      have h2 := hd n
      have h3 := hb n
      omega

end Supply

/-! ## C8: binary coding of any finite alphabet -/

noncomputable section Binary

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Width of the fixed-length binary code of an alphabet; at least one. -/
def codeWidth (α : Type*) [Fintype α] : ℕ := Nat.clog 2 (Fintype.card α) + 1

theorem card_lt_two_pow_codeWidth : Fintype.card α < 2 ^ codeWidth α := by
  have h1 : Fintype.card α ≤ 2 ^ Nat.clog 2 (Fintype.card α) := Nat.le_pow_clog one_lt_two _
  have h2 : 2 ^ Nat.clog 2 (Fintype.card α) < 2 ^ codeWidth α :=
    Nat.pow_lt_pow_right one_lt_two (Nat.lt_succ_self _)
  exact lt_of_le_of_lt h1 h2

/-- The `k` low binary digits of `n`, least significant first. -/
def bits (k n : ℕ) : List Bool := List.ofFn fun j : Fin k => n.testBit j

theorem bits_length (k n : ℕ) : (bits k n).length = k := by simp [bits]

theorem bits_injective {k n m : ℕ} (hn : n < 2 ^ k) (hm : m < 2 ^ k)
    (h : bits k n = bits k m) : n = m := by
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < k
  · have := congrArg (fun l => l[i]?) h
    simpa [bits, hi] using this
  · have hi' : k ≤ i := Nat.le_of_not_lt hi
    have h1 : n < 2 ^ i := lt_of_lt_of_le hn (Nat.pow_le_pow_right two_pos hi')
    have h2 : m < 2 ^ i := lt_of_lt_of_le hm (Nat.pow_le_pow_right two_pos hi')
    rw [Nat.testBit_lt_two_pow h1, Nat.testBit_lt_two_pow h2]

/-- The binary codeword of a mark: the digits of its index. -/
def enc (a : α) : List Bool := bits (codeWidth α) (Fintype.equivFin α a).val

theorem enc_length (a : α) : (enc a).length = codeWidth α := bits_length _ _

theorem enc_injective : Function.Injective (enc (α := α)) := by
  intro a b h
  have hlt : ∀ x : α, (Fintype.equivFin α x).val < 2 ^ codeWidth α := fun x =>
    lt_trans (Fintype.equivFin α x).isLt card_lt_two_pow_codeWidth
  have := bits_injective (hlt a) (hlt b) h
  exact (Fintype.equivFin α).injective (Fin.ext this)

/-- Encode a word over the alphabet as a word over the two marks, letter by letter. -/
def encodeWord (w : List α) : List Bool := w.flatMap enc

theorem encodeWord_append (w w' : List α) :
    encodeWord (w ++ w') = encodeWord w ++ encodeWord w' := by
  simp [encodeWord]

theorem encodeWord_length (w : List α) : (encodeWord w).length = codeWidth α * w.length := by
  induction w with
  | nil => simp [encodeWord]
  | cons a w ih =>
      simp only [encodeWord, List.flatMap_cons, List.length_append, enc_length,
        List.length_cons] at ih ⊢
      rw [ih]; ring

/-- Decode one codeword: the index with those digits, if any. -/
def dec1 (c : List Bool) : Option α :=
  ((List.finRange (Fintype.card α)).find? (fun i => bits (codeWidth α) i.val == c)).map
    (Fintype.equivFin α).symm

theorem dec1_enc (a : α) : dec1 (enc a) = some a := by
  unfold dec1 enc
  have hsome : ((List.finRange (Fintype.card α)).find?
      (fun i => bits (codeWidth α) i.val == bits (codeWidth α) (Fintype.equivFin α a).val)).isSome = true := by
    rw [List.find?_isSome]
    exact ⟨Fintype.equivFin α a, List.mem_finRange _, by simp⟩
  obtain ⟨i, hi⟩ := Option.isSome_iff_exists.1 hsome
  have hpi := List.find?_some hi
  simp only [beq_iff_eq] at hpi
  have hlt : ∀ x : Fin (Fintype.card α), x.val < 2 ^ codeWidth α := fun x =>
    lt_trans x.isLt card_lt_two_pow_codeWidth
  have := bits_injective (hlt i) (lt_trans (Fintype.equivFin α a).isLt card_lt_two_pow_codeWidth) hpi
  have hi' : i = Fintype.equivFin α a := Fin.ext this
  rw [hi, hi']
  simp

/-- Decode a binary word chunk by chunk with a fuel bound. -/
def decodeFuel (k : ℕ) : ℕ → List Bool → List α
  | 0, _ => []
  | n + 1, l =>
      if l.isEmpty then []
      else match dec1 (l.take k) with
        | some a => a :: decodeFuel k n (l.drop k)
        | none => []

/-- Decode a binary word. -/
def decodeWord (l : List Bool) : List α := decodeFuel (codeWidth α) l.length l

theorem decodeFuel_encode (w : List α) :
    ∀ n, w.length ≤ n → decodeFuel (codeWidth α) n (encodeWord w) = w := by
  induction w with
  | nil =>
      intro n _
      cases n <;> simp [decodeFuel, encodeWord]
  | cons a w ih =>
      intro n hn
      obtain ⟨n, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by simp at hn; omega⟩
      have hne : (enc a).isEmpty = false := by
        have : 0 < (enc a).length := by rw [enc_length]; unfold codeWidth; omega
        cases h : enc a with
        | nil => simp [h] at this
        | cons x xs => rfl
      have hne' : (enc a ++ encodeWord w).isEmpty = false := by
        have : 0 < (enc a).length := by rw [enc_length]; unfold codeWidth; omega
        cases h : enc a with
        | nil => simp [h] at this
        | cons x xs => simp
      have hcons : encodeWord (a :: w) = enc a ++ encodeWord w := by simp [encodeWord]
      have htake : (enc a ++ encodeWord w).take (codeWidth α) = enc a := by
        rw [List.take_append_of_le_length (by rw [enc_length])]
        rw [← enc_length a]; simp
      have hdrop : (enc a ++ encodeWord w).drop (codeWidth α) = encodeWord w := by
        rw [← enc_length a, List.drop_left]
      rw [hcons]
      simp only [decodeFuel, hne', Bool.false_eq_true, ↓reduceIte]
      rw [htake, dec1_enc, hdrop]
      simp only
      rw [ih n (by simpa using hn)]

/-- Decoding inverts encoding: every word over the finite alphabet is recovered from its
binary code. -/
theorem decode_encode (w : List α) : decodeWord (encodeWord w) = w := by
  unfold decodeWord
  apply decodeFuel_encode
  rw [encodeWord_length]
  have : 1 ≤ codeWidth α := by unfold codeWidth; omega
  nlinarith

/-- The binary code is injective on words. -/
theorem encodeWord_injective : Function.Injective (encodeWord (α := α)) := by
  intro w w' h
  have := congrArg (decodeWord (α := α)) h
  rwa [decode_encode w, decode_encode w'] at this

/-- The two-mark alphabet is the Booleans. -/
def boolMark : Bool → Mark2
  | false => .mark0
  | true => .mark1

def markBool : Mark2 → Bool
  | .mark0 => false
  | .mark1 => true

theorem markBool_boolMark (b : Bool) : markBool (boolMark b) = b := by cases b <;> rfl
theorem boolMark_markBool (m : Mark2) : boolMark (markBool m) = m := by cases m <;> rfl

/-- Every word over any finite alphabet embeds injectively into the free monoid on the two
separated marks `mark0`, `mark1`, with an explicit decoder. -/
def encodeMarks (w : List α) : List Mark2 := (encodeWord w).map boolMark

def decodeMarks (l : List Mark2) : List α := decodeWord (l.map markBool)

theorem decodeMarks_encodeMarks (w : List α) : decodeMarks (encodeMarks w) = w := by
  simp only [decodeMarks, encodeMarks, List.map_map]
  have : (markBool ∘ boolMark) = id := funext markBool_boolMark
  rw [this, List.map_id]
  exact decode_encode w

theorem encodeMarks_injective : Function.Injective (encodeMarks (α := α)) := by
  intro w w' h
  have := congrArg (decodeMarks (α := α)) h
  rwa [decodeMarks_encodeMarks w, decodeMarks_encodeMarks w'] at this

theorem encodeMarks_append (w w' : List α) :
    encodeMarks (w ++ w') = encodeMarks w ++ encodeMarks w' := by
  simp [encodeMarks, encodeWord_append]

end Binary

end GenesisComputation

#print axioms GenesisComputation.first_separation_replay
#print axioms GenesisComputation.first_separation_pairwise
#print axioms GenesisComputation.canonicalRegime_pairwise
#print axioms GenesisComputation.Mark2.toDatum_bijective
#print axioms GenesisComputation.separated_marks_not_collapsed
#print axioms GenesisComputation.unarySep_iff
#print axioms GenesisComputation.pairwiseSeparated_iff
#print axioms GenesisComputation.canonicalRegime_four_pairwise_decide
#print axioms GenesisComputation.two_marks_without_forms_collapsed
#print axioms GenesisComputation.Step.context
#print axioms GenesisComputation.Reach.context
#print axioms GenesisComputation.Reach.map
#print axioms GenesisComputation.Reach.of_map
#print axioms GenesisComputation.Step.exists_of_map
#print axioms GenesisComputation.plug1_ofSplit
#print axioms GenesisComputation.holes_ofSplit
#print axioms GenesisComputation.oneHole_iff_split
#print axioms GenesisComputation.ofSplit_injective
#print axioms GenesisComputation.genesis_context_count_n2_a3
#print axioms GenesisComputation.genesis_one_hole_count_n2_a3
#print axioms GenesisComputation.rtg_iff_mem_reachN_card
#print axioms GenesisComputation.card_wordsLE
#print axioms GenesisComputation.mem_succList
#print axioms GenesisComputation.reachB_iff
#print axioms GenesisComputation.decideReachB_iff
#print axioms GenesisComputation.reachSet_card_le
#print axioms GenesisComputation.ReachB.reach
#print axioms GenesisComputation.Reach.exists_bound
#print axioms GenesisComputation.reach_iff_reachB_of_closed
#print axioms GenesisComputation.verdict_reachable_sound
#print axioms GenesisComputation.verdict_unreachable_sound
#print axioms GenesisComputation.verdict_boundExceeded_witness
#print axioms GenesisComputation.not_closed_of_unbounded
#print axioms GenesisComputation.closed_bounds_reach
#print axioms GenesisComputation.replay_admitDatum_replicate
#print axioms GenesisComputation.genesis_unbounded_admission
#print axioms GenesisComputation.stepE_data_mono
#print axioms GenesisComputation.supply_growth
#print axioms GenesisComputation.decode_encode
#print axioms GenesisComputation.encodeWord_injective
#print axioms GenesisComputation.decodeMarks_encodeMarks
#print axioms GenesisComputation.encodeMarks_injective
#print axioms GenesisComputation.encodeMarks_append
