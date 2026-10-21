import Mathlib.Data.Finset.Card
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Algebra.Order.Group.Nat
import Mathlib.Tactic.Linarith

/-!
# Finite demand accounting `s_next = s - d + b` and its hypotheses

AuthorityEffect: None.  Scope: finite sets (`Finset`) of active demands `W`, a discharged set `D` and a
set of births `B`; the next register is `(W \ D) ∪ B`.  Every theorem is a general statement over an
arbitrary type with decidable equality; the explicit small sets are instances only.

* `demand_accounting` is the stated identity and needs exactly two hypotheses: `D ⊆ W` and
  `Disjoint (W \ D) B`.
* `card_next_exact` is the exact cardinality of the next register with no hypothesis, and
  `formula_iff` says the identity holds if and only if `|D \ W| = |(W \ D) ∩ B|`.  A violated hypothesis
  can therefore be masked only by an exactly cancelling excess of the other violation.
* `list_length_no_disjointness`: the list-length reading of the identity (source `Paper.lean`) does not
  need disjointness, because it counts multiplicity; the `Nodup` conjunct of the source `Paper001.lean`
  statement is what needs it (`list_overlap_not_nodup`).
* `every_step_is_an_accounting`: every pair of counts `(s, s')` arises from some admissible `(W, D, B)`,
  so a displayed survivor sequence is not a law; it is a chosen ledger example.

Nothing here concerns which demands an engine actually carries, nor any physical reading.
-/

namespace DemandAccounting

variable {α : Type*} [DecidableEq α]

/-- The next active register. -/
def next (W D B : Finset α) : Finset α := (W \ D) ∪ B

/-- `|W \ D| + |W ∩ D| = |W|`, always. -/
theorem card_sdiff_split (W D : Finset α) : (W \ D).card + (W ∩ D).card = W.card :=
  Finset.card_sdiff_add_card_inter W D

/-- Exact next cardinality, no hypothesis: `|(W\D) ∪ B| + |(W\D) ∩ B| = |W\D| + |B|`. -/
theorem card_union_split (W D B : Finset α) :
    (next W D B).card + ((W \ D) ∩ B).card = (W \ D).card + B.card :=
  Finset.card_union_add_card_inter (W \ D) B

/-- The exact count of the next register, in the integers, with no hypothesis at all. -/
theorem card_next_exact (W D B : Finset α) :
    ((next W D B).card : ℤ) = W.card - (W ∩ D).card + B.card - ((W \ D) ∩ B).card := by
  have h1 := card_sdiff_split W D
  have h2 := card_union_split W D B
  omega

/-- `|D| = |W ∩ D| + |D \ W|`, always. -/
theorem card_D_split (W D : Finset α) : (D ∩ W).card + (D \ W).card = D.card :=
  Finset.card_inter_add_card_sdiff D W

/-- The identity `s - d + b` holds exactly when the excess of `D` outside `W` equals the overlap of
the births with the surviving demands.  (Integer arithmetic, so no truncated subtraction.) -/
theorem formula_iff (W D B : Finset α) :
    ((next W D B).card : ℤ) = W.card - D.card + B.card ↔ (D \ W).card = ((W \ D) ∩ B).card := by
  have h := card_next_exact W D B
  have h3 := card_D_split W D
  have h4 : (D ∩ W) = (W ∩ D) := Finset.inter_comm D W
  rw [h4] at h3
  omega

/-- The stated identity, with exactly the two hypotheses of the source. -/
theorem demand_accounting (W D B : Finset α) (hsub : D ⊆ W) (hdisj : Disjoint (W \ D) B) :
    (next W D B).card = W.card - D.card + B.card := by
  have h1 : (D \ W).card = ((W \ D) ∩ B).card := by
    rw [Finset.sdiff_eq_empty_iff_subset.mpr hsub, Finset.disjoint_iff_inter_eq_empty.mp hdisj]
  have h2 := (formula_iff W D B).mpr h1
  have h3 : D.card ≤ W.card := Finset.card_le_card hsub
  omega

/-- The disjoint-union step (the source proof's second sentence). -/
theorem card_next_of_disjoint (W D B : Finset α) (hdisj : Disjoint (W \ D) B) :
    (next W D B).card = (W \ D).card + B.card :=
  Finset.card_union_of_disjoint hdisj

/-- Boundary 1: dropping `D ⊆ W` breaks the identity (instance `W = {0}`, `D = {1}`, `B = ∅`). -/
theorem fails_without_subset :
    ∃ (W D B : Finset ℕ), Disjoint (W \ D) B ∧ ¬ D ⊆ W ∧
      (next W D B).card ≠ W.card - D.card + B.card :=
  ⟨{0}, {1}, ∅, by decide, by decide, by decide⟩

/-- Boundary 2: dropping disjointness breaks the identity (instance `W = {0,1}`, `D = {0}`, `B = {1}`). -/
theorem fails_without_disjoint :
    ∃ (W D B : Finset ℕ), D ⊆ W ∧ ¬ Disjoint (W \ D) B ∧
      (next W D B).card ≠ W.card - D.card + B.card :=
  ⟨{0, 1}, {0}, {1}, by decide, by decide, by decide⟩

/-- Boundary 3: both hypotheses violated at once and the identity still holds, because the excess of
`D` outside `W` (one element) is cancelled by the overlap (one element).  The identity holding does not
certify the hypotheses.  Instance `W = {0}`, `D = {1}`, `B = {0}`. -/
theorem holds_accidentally_without_hypotheses :
    ∃ (W D B : Finset ℕ), ¬ D ⊆ W ∧ ¬ Disjoint (W \ D) B ∧
      (next W D B).card = W.card - D.card + B.card :=
  ⟨{0}, {1}, {0}, by decide, by decide, by decide⟩

/-- With `D ⊄ W` and no overlap the integer identity fails (no truncation in `ℤ`). -/
theorem fails_of_excess_without_overlap (W D B : Finset α) (hdisj : Disjoint (W \ D) B)
    (hnot : ¬ D ⊆ W) : ((next W D B).card : ℤ) ≠ W.card - D.card + B.card := by
  intro h
  obtain ⟨x, hxD, hxW⟩ := Finset.not_subset.mp hnot
  have hpos : 0 < (D \ W).card := Finset.card_pos.mpr ⟨x, Finset.mem_sdiff.mpr ⟨hxD, hxW⟩⟩
  have h5 := (formula_iff W D B).mp h
  have hov : ((W \ D) ∩ B).card = 0 := by
    rw [Finset.disjoint_iff_inter_eq_empty.mp hdisj]; simp
  omega

/-- Exactly one violated hypothesis never permits the integer identity (universal; the disjointness-alone half is
the corollary of `formula_iff` with `D ⊆ W`, so `|D \ W| = 0`). -/
theorem single_violation_fails (W D B : Finset α)
    (h : (¬ D ⊆ W ∧ Disjoint (W \ D) B) ∨ (D ⊆ W ∧ ¬ Disjoint (W \ D) B)) :
    ((next W D B).card : ℤ) ≠ W.card - D.card + B.card := by
  rcases h with ⟨hn, hd⟩ | ⟨hs, hn⟩
  · exact fails_of_excess_without_overlap W D B hd hn
  · intro hh
    have h5 := (formula_iff W D B).mp hh
    have h0 : (D \ W).card = 0 := by
      rw [Finset.sdiff_eq_empty_iff_subset.mpr hs]; rfl
    have hov : ((W \ D) ∩ B).card = 0 := by omega
    exact hn (Finset.disjoint_iff_inter_eq_empty.mpr (Finset.card_eq_zero.mp hov))

/-- The truncated `ℕ` reading of the identity can hold although `D ⊄ W`: when `D` is strictly larger than
`W`, `W.card - D.card` truncates to `0` (instance `W = {0}`, `D = {0,1}`, `B = ∅`).  This is why the source
statement carries `D ⊆ W` and why the exact check here is made in `ℤ`. -/
theorem nat_truncation_masks_subset_violation :
    ∃ (W D B : Finset ℕ), Disjoint (W \ D) B ∧ ¬ D ⊆ W ∧
      (next W D B).card = W.card - D.card + B.card ∧
      ((next W D B).card : ℤ) ≠ W.card - D.card + B.card :=
  ⟨{0}, {0, 1}, ∅, by decide, by decide, by decide, by decide⟩

/-- Every pair of counts is the result of an admissible accounting step, so the recurrence imposes no
constraint on a sequence of counts: it is bookkeeping, not a law. -/
theorem every_step_is_an_accounting (s s' : ℕ) :
    ∃ (W D B : Finset ℕ), D ⊆ W ∧ Disjoint (W \ D) B ∧ W.card = s ∧ (next W D B).card = s' := by
  refine ⟨Finset.range s, Finset.Ico s' s, Finset.Ico s s', ?_, ?_, Finset.card_range s, ?_⟩
  · intro x hx
    simp only [Finset.mem_Ico, Finset.mem_range] at hx ⊢
    omega
  · rw [Finset.disjoint_left]
    intro x hx hxB
    simp only [Finset.mem_sdiff, Finset.mem_Ico, Finset.mem_range] at hx hxB
    omega
  · have hD : Finset.Ico s' s ⊆ Finset.range s := by
      intro x hx
      simp only [Finset.mem_Ico, Finset.mem_range] at hx ⊢
      omega
    have hdisj : Disjoint (Finset.range s \ Finset.Ico s' s) (Finset.Ico s s') := by
      rw [Finset.disjoint_left]
      intro x hx hxB
      simp only [Finset.mem_sdiff, Finset.mem_Ico, Finset.mem_range] at hx hxB
      omega
    have := demand_accounting (Finset.range s) (Finset.Ico s' s) (Finset.Ico s s') hD hdisj
    rw [this, Finset.card_range, Nat.card_Ico, Nat.card_Ico]
    omega

/-- Two different admissible `(d, b)` splits give the same counts: `s = 1`, `s' = 1`
(instances `(d,b) = (0,0)` and `(1,1)`).  The count sequence does not determine the accounting. -/
theorem split_not_determined :
    ∃ (W D B D' B' : Finset ℕ), D ⊆ W ∧ Disjoint (W \ D) B ∧ D' ⊆ W ∧ Disjoint (W \ D') B' ∧
      W.card = 1 ∧ (next W D B).card = 1 ∧ (next W D' B').card = 1 ∧ D.card ≠ D'.card :=
  ⟨{0}, ∅, ∅, {0}, {1}, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide⟩

/-! ### List-valued register (source `Paper.lean` / `Paper001.lean` readings) -/

omit [DecidableEq α] in
/-- Length of the filtered register: no disjointness, no duplicates-freedom needed. -/
theorem list_length_no_disjointness (active births : List α) (discharged : α → Bool) :
    ((active.filter (fun a => !(discharged a))) ++ births).length =
      active.length - (active.filter discharged).length + births.length := by
  have hp : (active.filter discharged).length + (active.filter (fun a => !(discharged a))).length = active.length := by
    induction active with
    | nil => rfl
    | cons a xs ih =>
      cases hd : discharged a <;> simp [List.filter, hd] at * <;> omega
  simp only [List.length_append]
  omega

omit [DecidableEq α] in
/-- For duplicate-free inputs the list register is duplicate-free exactly when the births avoid the survivors
(the `Nodup` conjunct of the source, for the filter-based register; the `erase`-based `removeAll` of
`Paper001.lean` is not re-proved here). -/
theorem list_register_nodup_iff (active births : List α) (discharged : α → Bool)
    (ha : active.Nodup) (hb : births.Nodup) :
    ((active.filter (fun a => !(discharged a))) ++ births).Nodup ↔
      ∀ a ∈ active.filter (fun a => !(discharged a)), ∀ b ∈ births, a ≠ b := by
  rw [List.nodup_append]
  constructor
  · exact fun h => h.2.2
  · exact fun h => ⟨ha.filter _, hb, h⟩

/-- The list reading counts multiplicity: births overlapping a survivor keep the length identity but
the register is no longer duplicate-free (instance `[0,1]`, discharge `0`, births `[1]`). -/
theorem list_overlap_not_nodup :
    let W : List ℕ := [0, 1]
    let B : List ℕ := [1]
    (W.filter (fun a => !(a == 0)) ++ B).length = W.length - (W.filter (fun a => a == 0)).length + B.length ∧
      ¬ (W.filter (fun a => !(a == 0)) ++ B).Nodup := by
  decide

end DemandAccounting

#print axioms DemandAccounting.demand_accounting
#print axioms DemandAccounting.card_next_exact
#print axioms DemandAccounting.formula_iff
#print axioms DemandAccounting.fails_without_subset
#print axioms DemandAccounting.fails_without_disjoint
#print axioms DemandAccounting.holds_accidentally_without_hypotheses
#print axioms DemandAccounting.fails_of_excess_without_overlap
#print axioms DemandAccounting.single_violation_fails
#print axioms DemandAccounting.list_register_nodup_iff
#print axioms DemandAccounting.nat_truncation_masks_subset_violation
#print axioms DemandAccounting.every_step_is_an_accounting
#print axioms DemandAccounting.split_not_determined
#print axioms DemandAccounting.list_length_no_disjointness
#print axioms DemandAccounting.list_overlap_not_nodup
