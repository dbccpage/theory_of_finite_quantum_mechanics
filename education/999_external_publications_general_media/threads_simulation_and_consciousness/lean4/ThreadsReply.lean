/-!
# Finite results behind the Threads replies

Core Lean 4 only (no Mathlib). Every statement is about finite carriers:
records, reports and verdicts. Each theorem matches one card of the markup board.

* `records_do_not_fix_identity`: two records, standing/standing then standing/flat,
  are consistent with two different matchings of the lines. Which line fell is supplied.
* `same_report_same_verdict`: an evaluator that sees only the report cannot split
  two states with the same report.
* `one_channel_not_every_channel`: equal on one channel does not mean equal on another.
* `same_report_not_same_likelihood`: two hypotheses can both produce a report and still
  give it different weights. Equal reports do not give a Bayes factor of 1.
* `same_weights_same_likelihood`: the condition that does give it.
* `pigeonhole`: with more states than reports, two states share a report.
  The condition `m < n` is part of the statement.
* `small_domain_all_reported`: without that condition, every state can be reported.
-/

namespace ThreadsReply

/-! ## Picture 1: the tree -/

inductive Pose | up | flat
  deriving DecidableEq, Repr

/-- Record 1: two lines, both upright. -/
def R1 : Fin 2 → Pose := fun _ => .up
/-- Record 2: one upright, one flat. -/
def R2 : Fin 2 → Pose := fun i => if i = 0 then .up else .flat

/-- A matching says which line in record 2 is which line in record 1. -/
def swap : Fin 2 → Fin 2 := fun i => if i = 0 then 1 else 0

/-- Under the identity matching line 1 fell; under the swap, line 0 fell.
Both matchings are one-to-one, and the records alone do not choose between them. -/
theorem records_do_not_fix_identity :
    (∀ i j : Fin 2, swap i = swap j → i = j) ∧
    R2 (id 1) = .flat ∧ R2 (swap 0) = .flat ∧ (id (1 : Fin 2)) ≠ (0 : Fin 2) ∧
    (∀ i, R1 i = .up) := by
  refine ⟨by decide, by decide, by decide, by decide, fun _ => rfl⟩

/-! ## Picture 2: the rendering claim -/

/-- Same report, same verdict, for any evaluator that reads only the report. -/
theorem same_report_same_verdict {X P V : Type} (q : X → P) (E : P → V) {a b : X}
    (h : q a = q b) : E (q a) = E (q b) := by
  rw [h]

/-- Two worlds: `true` has one extra hidden object, `false` does not.
Channel 1 (the viewport) reports nothing about it; channel 2 (a probe) does. -/
theorem one_channel_not_every_channel :
    ∃ (q₁ : Bool → Unit) (q₂ : Bool → Bool), q₁ true = q₁ false ∧ q₂ true ≠ q₂ false :=
  ⟨fun _ => (), id, rfl, by decide⟩

/-- Hypotheses as weights over reports (out of 10). Both hypotheses can produce
report `true`, so a single report `true` fits both, yet they weigh it 9 and 5. -/
theorem same_report_not_same_likelihood :
    ∃ (hA hB : Bool → Nat), 0 < hA true ∧ 0 < hB true ∧ hA true ≠ hB true :=
  ⟨fun b => if b then 9 else 1, fun _ => 5, by decide, by decide, by decide⟩

/-- The condition that does give a Bayes factor of 1: equal weights on every report. -/
theorem same_weights_same_likelihood {R : Type} (hA hB : R → Nat) (h : ∀ r, hA r = hB r)
    (d : R) : hA d = hB d :=
  h d

/-! ## Supporting: the pigeonhole limit, with its condition -/

/-- With more states than reports (`m < n`), some two states share a report. -/
theorem pigeonhole {n m : Nat} (q : Fin n → Fin m) (h : m < n) :
    ∃ x y : Fin n, x ≠ y ∧ q x = q y := by
  apply Classical.byContradiction
  intro hne
  have inj : ∀ x y : Fin n, x ≠ y → q x ≠ q y :=
    fun x y hxy hq => hne ⟨x, y, hxy, hq⟩
  have nd : ((List.finRange n).map q).Nodup :=
    List.Pairwise.map q inj (List.nodup_finRange n)
  have sub : (List.finRange n).map q ⊆ List.finRange m :=
    fun a _ => List.mem_finRange a
  have hle := nd.length_le_of_subset sub
  simp at hle
  omega

/-- Without the condition, a finite observer can report every state:
the identity report on a small domain separates all states. -/
theorem small_domain_all_reported (n : Nat) :
    ∃ q : Fin n → Fin n, ∀ x y, q x = q y → x = y :=
  ⟨id, fun _ _ h => h⟩

end ThreadsReply
