/-!
# Finite results behind the Threads replies

Core Lean 4 only (no Mathlib). Every statement is about finite carriers:
records, reports and verdicts. Each theorem matches one card of the markup board.

* `records_do_not_fix_identity`: two records, standing/standing then standing/flat,
  admit two one-to-one matchings of the lines that imply different histories.
  Which line fell is supplied.
* `same_report_same_verdict`: an evaluator that sees only the report cannot split
  two states with the same report.
* `one_channel_not_every_channel`: equal on one channel does not mean equal on another.
* `same_report_not_same_likelihood`: two hypotheses can both produce a report and still
  give it different weights. Equal reports do not give a Bayes factor of 1.
* `same_weights_same_likelihood`: the condition that does give it, for any finite data set.
* `pigeonhole`: with more states than reports, two states share a report.
  The condition `m < n` is part of the statement.
* `small_domain_all_reported`: with `n ≤ m`, every state can be reported.
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

/-- The history a matching implies: the line of record 1 that is flat in record 2. -/
def fallenUnder (σ : Fin 2 → Fin 2) : Fin 2 := if R2 (σ 0) = .flat then 0 else 1

/-- Both matchings are one-to-one, both start from two upright lines, and they imply
different histories: under the identity line 1 fell, under the swap line 0 fell.
The two records alone do not decide which line fell. -/
theorem records_do_not_fix_identity :
    ∃ σ τ : Fin 2 → Fin 2,
      (∀ i j, σ i = σ j → i = j) ∧ (∀ i j, τ i = τ j → i = j) ∧
      fallenUnder σ ≠ fallenUnder τ := by
  refine ⟨id, swap, fun _ _ h => h, by decide, by decide⟩

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

/-- Hypotheses as weights over reports, each normalized to a total of 10.
Both hypotheses can produce report `true`, so a single report `true` fits both,
yet they weigh it 9 and 5: equal reports do not give equal likelihoods. -/
theorem same_report_not_same_likelihood :
    ∃ (hA hB : Bool → Nat),
      hA true + hA false = 10 ∧ hB true + hB false = 10 ∧
      0 < hA true ∧ 0 < hB true ∧ hA true ≠ hB true :=
  ⟨fun b => if b then 9 else 1, fun _ => 5, by decide, by decide, by decide, by decide, by decide⟩

/-- Likelihood of a whole data set: the product of the weights of its reports. -/
def likelihood {R : Type} (h : R → Nat) (D : List R) : Nat := (D.map h).foldl (· * ·) 1

/-- The condition that does give a Bayes factor of 1: equal weights on every report
make every finite data set equally likely under both hypotheses. -/
theorem same_weights_same_likelihood {R : Type} (hA hB : R → Nat) (h : ∀ r, hA r = hB r)
    (D : List R) : likelihood hA D = likelihood hB D := by
  have : hA = hB := funext h
  rw [this]

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

/-- Without the condition, every state can be reported: whenever there are at least
as many reports as states (`n ≤ m`), some report map separates all states. -/
theorem small_domain_all_reported {n m : Nat} (h : n ≤ m) :
    ∃ q : Fin n → Fin m, ∀ x y, q x = q y → x = y :=
  ⟨Fin.castLE h, fun x y hxy => Fin.ext (by simpa using congrArg Fin.val hxy)⟩

end ThreadsReply
