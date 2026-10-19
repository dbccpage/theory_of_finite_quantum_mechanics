import Mathlib.Data.Finset.Card
import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Basic

/-! AuthorityEffect: None. Worklist closure, cardinality/work bounds and
ordered face erasure. Native BTreeSet/Vec, input admission and concrete face
generation correspondence require separate source review. No Rust/MIR or
allocator-totality theorem is claimed.
-/
namespace TFQM.SimplicialClosure

variable {α : Type} [DecidableEq α]

def Covers (seen : Finset α) (pending : List α) (required : α → Prop) : Prop :=
  ∀ value, required value → value ∈ seen ∨ value ∈ pending

def Frontier (next : α → List α) (seen : Finset α) (pending : List α) : Prop :=
  ∀ value ∈ seen, Covers seen pending (fun child => child ∈ next value)

theorem initial_cover (seeds : List α) : Covers ∅ seeds (fun value => value ∈ seeds) := by
  intro value present
  exact Or.inr present

theorem initial_frontier (next : α → List α) (seeds : List α) : Frontier next ∅ seeds := by
  intro value impossible
  simp at impossible

theorem duplicate_cover (seen : Finset α) (value : α) (tail : List α)
    (required : α → Prop) (present : value ∈ seen)
    (covered : Covers seen (value :: tail) required) : Covers seen tail required := by
  intro item needed
  rcases covered item needed with old | queued
  · exact Or.inl old
  · rcases List.mem_cons.mp queued with same | remaining
    · subst item; exact Or.inl present
    · exact Or.inr remaining

theorem fresh_cover (next : α → List α) (seen : Finset α) (value : α) (tail : List α)
    (required : α → Prop) (covered : Covers seen (value :: tail) required) :
    Covers (insert value seen) (next value ++ tail) required := by
  intro item needed
  rcases covered item needed with old | queued
  · exact Or.inl (Finset.mem_insert_of_mem old)
  · rcases List.mem_cons.mp queued with same | remaining
    · subst item; exact Or.inl (Finset.mem_insert_self _ _)
    · exact Or.inr (List.mem_append.mpr (Or.inr remaining))

theorem duplicate_frontier (next : α → List α) (seen : Finset α)
    (value : α) (tail : List α) (present : value ∈ seen)
    (frontier : Frontier next seen (value :: tail)) : Frontier next seen tail := by
  intro item old
  exact duplicate_cover seen value tail _ present (frontier item old)

theorem fresh_frontier (next : α → List α) (seen : Finset α)
    (value : α) (tail : List α) (frontier : Frontier next seen (value :: tail)) :
    Frontier next (insert value seen) (next value ++ tail) := by
  intro item old child member
  rcases Finset.mem_insert.mp old with same | previous
  · subst item
    exact Or.inr (List.mem_append.mpr (Or.inl member))
  · exact fresh_cover next seen value tail _ (frontier item previous) child member

theorem fresh_sound (next : α → List α) (seen : Finset α) (value : α) (tail : List α)
    (valid : α → Prop) (old : ∀ item ∈ seen, valid item)
    (queued : ∀ item ∈ value :: tail, valid item)
    (closed : ∀ item, valid item → ∀ child ∈ next item, valid child) :
    (∀ item ∈ insert value seen, valid item) ∧
      (∀ item ∈ next value ++ tail, valid item) := by
  have current : valid value := queued value (by simp)
  constructor
  · intro item member
    rcases Finset.mem_insert.mp member with same | prior
    · simpa [same] using current
    · exact old item prior
  · intro item member
    rcases List.mem_append.mp member with child | remaining
    · exact closed value current item child
    · exact queued item (by simp [remaining])

theorem finish_contains (seen : Finset α) (required : α → Prop)
    (covered : Covers seen [] required) : ∀ item, required item → item ∈ seen := by
  intro item needed
  simpa using covered item needed

theorem finish_closed (next : α → List α) (seen : Finset α)
    (frontier : Frontier next seen []) : ∀ item ∈ seen, ∀ child ∈ next item, child ∈ seen := by
  intro item present child member
  simpa using frontier item present child member

theorem fresh_card_bound (seen : Finset α) (value : α) (limit : Nat)
    (unseen : value ∉ seen) (bounded : seen.card ≤ limit) (space : seen.card ≠ limit) :
    (insert value seen).card ≤ limit := by
  rw [Finset.card_insert_of_notMem unseen]
  omega

theorem duplicate_potential (limit width count pending : Nat) (work : 0 < pending) :
    (limit - count) * width + (pending - 1) < (limit - count) * width + pending := by
  omega

theorem fresh_potential (limit width count pending added : Nat)
    (space : count < limit) (work : 0 < pending) (children : added ≤ width) :
    (limit - (count + 1)) * width + (pending - 1 + added) <
      (limit - count) * width + pending := by
  have gap : limit - count = limit - (count + 1) + 1 := by omega
  rw [gap, Nat.add_mul, Nat.one_mul]
  omega

theorem erase_commute {β : Type} (values : List β) (i j : Nat) (order : j ≤ i) :
    (values.eraseIdx j).eraseIdx i = (values.eraseIdx (i + 1)).eraseIdx j := by
  induction values generalizing i j with
  | nil => simp
  | cons head tail ih =>
    cases j with
    | zero => simp
    | succ j =>
      cases i with
      | zero => omega
      | succ i =>
        simp only [List.eraseIdx_cons_succ]
        congr 1
        exact ih i j (by omega)

theorem erase_preserves_distinct {β : Type} (values : List β) (index : Nat)
    (distinct : values.Nodup) : (values.eraseIdx index).Nodup := distinct.eraseIdx index

theorem erase_preserves_order (values : List Nat) (index : Nat)
    (ordered : values.Pairwise (· < ·)) : (values.eraseIdx index).Pairwise (· < ·) :=
  ordered.eraseIdx index

#print axioms initial_cover
#print axioms initial_frontier
#print axioms duplicate_cover
#print axioms fresh_cover
#print axioms duplicate_frontier
#print axioms fresh_frontier
#print axioms fresh_sound
#print axioms finish_contains
#print axioms finish_closed
#print axioms fresh_card_bound
#print axioms duplicate_potential
#print axioms fresh_potential
#print axioms erase_commute
#print axioms erase_preserves_distinct
#print axioms erase_preserves_order

end TFQM.SimplicialClosure
