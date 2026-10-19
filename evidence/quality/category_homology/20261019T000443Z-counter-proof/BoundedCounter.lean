import Mathlib.Data.Nat.Basic

/-! AuthorityEffect: None. Finite-horizon future-legality quotient model.
Nat is the unbounded native counter. The source relation to checked usize
storage and standard Rust iteration is reviewed separately, not extracted.
-/
namespace TFQM.BoundedCounter

def clip (remaining count : Nat) : Nat := min count remaining

theorem clip_bound (remaining count : Nat) : clip remaining count ≤ remaining := by
  simp [clip]

theorem guard_exact (remaining count : Nat) (budget : 0 < remaining) :
    clip remaining count = 0 ↔ count = 0 := by
  unfold clip
  omega

theorem increment_step (remaining count : Nat) (budget : 0 < remaining) :
    clip (remaining - 1) (count + 1) =
      if clip remaining count ≥ remaining - 1 then remaining - 1
      else clip remaining count + 1 := by
  unfold clip
  split <;> omega

theorem decrement_step (remaining count : Nat) (budget : 0 < remaining)
    (positive : 0 < count) :
    clip (remaining - 1) (count - 1) = min (clip remaining count - 1) (remaining - 1) := by
  unfold clip
  omega

theorem increment_branch_bound (remaining clipped : Nat)
    (branch : clipped < remaining - 1) : clipped + 1 ≤ remaining - 1 := by
  omega

theorem separator_bound (remaining left right : Nat)
    (left_bound : left ≤ remaining) (right_bound : right ≤ remaining)
    (distinct : left ≠ right) : min left right + 1 ≤ remaining := by
  omega

theorem decrement_separator (remaining left right : Nat)
    (ordered : left < right) (right_bound : right ≤ remaining) :
    left + 1 > left ∧ left + 1 ≤ right ∧ left + 1 ≤ remaining ∧
      ∀ shorter < left + 1, shorter ≤ left ∧ shorter ≤ right := by
  omega

inductive Event where | increment | decrement

def native (count : Nat) : List Event → Option Nat
  | [] => some count
  | .increment :: rest => native (count + 1) rest
  | .decrement :: rest => match count with
      | 0 => none
      | n + 1 => native n rest

theorem short_words_legal (word : List Event) (count : Nat)
    (enough : word.length ≤ count) : ∃ result, native count word = some result := by
  induction word generalizing count with
  | nil => exact ⟨count, rfl⟩
  | cons event rest ih =>
    cases event with
    | increment =>
      simpa [native] using ih (count + 1) (by simp_all; omega)
    | decrement =>
      cases count with
      | zero => simp_all
      | succ n => simpa [native] using ih n (by simp_all; omega)

#print axioms clip_bound
#print axioms guard_exact
#print axioms increment_step
#print axioms decrement_step
#print axioms increment_branch_bound
#print axioms separator_bound
#print axioms decrement_separator
#print axioms short_words_legal

end TFQM.BoundedCounter
