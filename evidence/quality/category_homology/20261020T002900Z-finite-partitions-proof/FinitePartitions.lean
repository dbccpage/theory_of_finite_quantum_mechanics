import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.GroupTheory.Perm.Centralizer

/-! AuthorityEffect: None. Positive Rust row lists map to actual Nat.Partition.
Mathlib's actual symmetric-group conjugacy formula and its integral denominator
are used, including the separate fixed-point factorial. DP/DFS index, progress
and ordered admission facts supplement the source invariant proof. The complete
Rust DP/explicit-stack refinement and allocator behavior are not extracted. -/
namespace TFQM.FinitePartitions
open scoped BigOperators

def ofPositiveList (parts : List Nat) (hp : ∀ x ∈ parts, 0 < x) : Nat.Partition parts.sum where
  parts := parts
  parts_pos := by simpa using hp
  parts_sum := by simp

theorem admitted_parts (parts : List Nat) (hp : ∀ x ∈ parts, 0 < x) :
    (ofPositiveList parts hp).parts = (parts : Multiset Nat) := rfl

theorem admitted_sum (parts : List Nat) (hp : ∀ x ∈ parts, 0 < x) :
    (ofPositiveList parts hp).parts.sum = parts.sum := (ofPositiveList parts hp).parts_sum

theorem member_bounded (parts : List Nat) (hp : ∀ x ∈ parts, 0 < x) (x : Nat) (hx : x ∈ parts) :
    x ≤ parts.sum := Nat.Partition.le_of_mem_parts (p := ofPositiveList parts hp) (by simpa using hx)

theorem dp_previous_index (part total n : Nat) (hp : 0 < part) (hpt : part ≤ total) (ht : total ≤ n) :
    total - part < total ∧ total < n + 1 := by omega

theorem dfs_child_smaller (remaining part : Nat) (hp : 0 < part) (hr : part ≤ remaining) :
    remaining - part < remaining := by omega

theorem dfs_preserves_sum (prefixSum remaining part total : Nat)
    (hs : prefixSum + remaining = total) (hr : part ≤ remaining) :
    (prefixSum + part) + (remaining - part) = total := by omega

theorem descending_child (remaining part : Nat) : min remaining part ≤ remaining ∧ min remaining part ≤ part := by omega

theorem part_cursor_decreases (part : Nat) (hp : 0 < part) : part - 1 < part := by omega

inductive Refusal where
  | rows | cells
  deriving DecidableEq

def admit (n count limit cellLimit : Nat) : Except Refusal Unit :=
  if limit < count then .error .rows
  else if cellLimit < count * n then .error .cells
  else .ok ()

theorem admission_exact (n c l b : Nat) : admit n c l b = .ok () ↔ c ≤ l ∧ c * n ≤ b := by
  unfold admit
  split_ifs <;> simp_all <;> omega

theorem rows_before_cells (n c l b : Nat) (h : l < c) : admit n c l b = .error .rows := by simp [admit, h]

theorem cell_refusal (n c l b : Nat) (hc : c ≤ l) (hb : b < c * n) :
    admit n c l b = .error .cells := by simp [admit, Nat.not_lt_of_ge hc, hb]

theorem grouped_denominator (parts : Multiset Nat) :
    (∏ j ∈ parts.toFinset, j ^ parts.count j * (parts.count j).factorial) =
      parts.prod * (∏ j ∈ parts.toFinset, (parts.count j).factorial) := by
  rw [Finset.prod_mul_distrib, ← Finset.prod_multiset_count]

theorem actual_conjugacy_size (n : Nat) (g : Equiv.Perm (Fin n)) :
    Nat.card {h : Equiv.Perm (Fin n) | IsConj g h} =
      n.factorial / ((n - g.cycleType.sum).factorial * g.cycleType.prod *
        (∏ j ∈ g.cycleType.toFinset, (g.cycleType.count j).factorial)) := by
  simpa using Equiv.Perm.card_isConj_eq g

theorem conjugacy_denominator_divides (n : Nat) (g : Equiv.Perm (Fin n)) :
    ((n - g.cycleType.sum).factorial * g.cycleType.prod *
        (∏ j ∈ g.cycleType.toFinset, (g.cycleType.count j).factorial)) ∣ n.factorial := by
  refine ⟨Nat.card {h : Equiv.Perm (Fin n) | IsConj g h}, ?_⟩
  simpa [Nat.mul_comm] using (Equiv.Perm.card_isConj_mul_eq g).symm

theorem cycle_realization (n : Nat) (cycles : Multiset Nat)
    (hs : cycles.sum ≤ n) (hp : ∀ j ∈ cycles, 2 ≤ j) :
    ∃ g : Equiv.Perm (Fin n), g.cycleType = cycles := by
  exact (Equiv.Perm.exists_with_cycleType_iff (Fin n)).mpr (by simpa using And.intro hs hp)

#print axioms admitted_parts
#print axioms admitted_sum
#print axioms member_bounded
#print axioms dp_previous_index
#print axioms dfs_child_smaller
#print axioms dfs_preserves_sum
#print axioms descending_child
#print axioms part_cursor_decreases
#print axioms admission_exact
#print axioms rows_before_cells
#print axioms cell_refusal
#print axioms grouped_denominator
#print axioms actual_conjugacy_size
#print axioms conjugacy_denominator_divides
#print axioms cycle_realization
end TFQM.FinitePartitions
