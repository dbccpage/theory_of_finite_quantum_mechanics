import Mathlib.Data.Nat.Choose.Basic

/-! AuthorityEffect: None. Exact factorial/binomial recurrences, composition
count identity, ordered resource admission and pivot arithmetic. The Rust
iterator representation, lexicographic completeness and source correspondence
are reviewed separately; these are not extracted Rust or allocator proofs. -/
namespace TFQM.FiniteEnumeration

def factorialLoop : Nat → Nat
  | 0 => 1
  | n + 1 => factorialLoop n * (n + 1)

theorem factorial_exact (n : Nat) : factorialLoop n = n.factorial := by
  induction n with
  | zero => rfl
  | succ n ih => simp [factorialLoop, ih, Nat.factorial_succ, Nat.mul_comm]

theorem binomial_step (a i : Nat) :
    ((a + i).choose i * (a + i + 1)) / (i + 1) = (a + i + 1).choose (i + 1) := by
  rw [Nat.mul_comm ((a + i).choose i), Nat.add_one_mul_choose_eq]
  exact Nat.mul_div_left _ (Nat.zero_lt_succ i)

theorem binomial_step_integral (a i : Nat) :
    (i + 1) ∣ (a + i).choose i * (a + i + 1) := by
  rw [Nat.mul_comm ((a + i).choose i), Nat.add_one_mul_choose_eq]
  exact Nat.dvd_mul_left _ _

def binomialLoop (a : Nat) : Nat → Nat
  | 0 => 1
  | i + 1 => binomialLoop a i * (a + i + 1) / (i + 1)

theorem binomial_loop_exact (a i : Nat) : binomialLoop a i = (a + i).choose i := by
  induction i with
  | zero => simp [binomialLoop]
  | succ i ih => rw [binomialLoop, ih, binomial_step]

theorem binomial_final (n m : Nat) (hm : m ≤ n) :
    binomialLoop (n - m) m = n.choose m := by
  rw [binomial_loop_exact, Nat.sub_add_cancel hm]

theorem symmetric_choice (n k : Nat) (hk : k ≤ n) :
    n.choose (min k (n - k)) = n.choose k := by
  by_cases h : k ≤ n - k
  · rw [Nat.min_eq_left h]
  · rw [Nat.min_eq_right (by omega)]
    exact Nat.choose_symm hk

theorem choose_outside (n k : Nat) (h : n < k) : n.choose k = 0 :=
  Nat.choose_eq_zero_of_lt h

theorem numerator_fits (n m i bound : Nat) (hm : m ≤ n) (hi : i ≤ m) (hn : n ≤ bound) :
    n - m + i ≤ bound := by omega

theorem composition_count (total parts : Nat) (hp : 0 < parts) :
    parts.multichoose total = (total + parts - 1).choose (parts - 1) := by
  rw [Nat.multichoose_eq]
  have ht : total ≤ parts + total - 1 := by omega
  have he : parts + total - 1 - total = parts - 1 := by omega
  have hs := Nat.choose_symm ht
  rw [he] at hs
  rw [← hs]
  congr 1 <;> omega

theorem no_parts_nonzero (total : Nat) (h : 0 < total) : Nat.multichoose 0 total = 0 := by
  cases total with
  | zero => omega
  | succ n => exact Nat.multichoose_zero_succ n

theorem empty_composition : Nat.multichoose 0 0 = 1 := Nat.multichoose_zero_right 0

inductive Refusal where
  | width | rows | cells
  deriving DecidableEq

def admit (width maxWidth count maxRows maxCells : Nat) : Except Refusal Unit :=
  if maxWidth < width then .error .width
  else if maxRows < count then .error .rows
  else if maxCells < count * width then .error .cells
  else .ok ()

theorem admission_exact (w mw c mr mc : Nat) :
    admit w mw c mr mc = .ok () ↔ w ≤ mw ∧ c ≤ mr ∧ c * w ≤ mc := by
  simp [admit]
  omega

theorem width_first (w mw c mr mc : Nat) (h : mw < w) :
    admit w mw c mr mc = .error .width := by simp [admit, h]

theorem rows_before_cells (w mw c mr mc : Nat) (hw : w ≤ mw) (hc : mr < c) :
    admit w mw c mr mc = .error .rows := by simp [admit, Nat.not_lt_of_ge hw, hc]

theorem cells_refused (w mw c mr mc : Nat) (hw : w ≤ mw) (hc : c ≤ mr) (hm : mc < c * w) :
    admit w mw c mr mc = .error .cells := by
  simp [admit, Nat.not_lt_of_ge hw, Nat.not_lt_of_ge hc, hm]

theorem pivot_sum (prefix left pivot : Nat) (hp : 0 < pivot) :
    prefix + ((left + 1) + (pivot - 1)) = prefix + (left + pivot) := by omega

theorem pivot_increment_fits (left pivot total bound : Nat)
    (hp : 0 < pivot) (hs : left + pivot ≤ total) (ht : total ≤ bound) :
    left + 1 ≤ bound := by omega

theorem pivot_remainder_lt (pivot : Nat) (hp : 0 < pivot) : pivot - 1 < pivot := by omega

theorem subset_increment_fits (n k i value : Nat) (hk : k ≤ n) (hi : i < k)
    (hv : value < n - k + i) : value + 1 < n := by omega

#print axioms factorial_exact
#print axioms binomial_step
#print axioms binomial_step_integral
#print axioms binomial_loop_exact
#print axioms binomial_final
#print axioms symmetric_choice
#print axioms choose_outside
#print axioms numerator_fits
#print axioms composition_count
#print axioms no_parts_nonzero
#print axioms empty_composition
#print axioms admission_exact
#print axioms width_first
#print axioms rows_before_cells
#print axioms cells_refused
#print axioms pivot_sum
#print axioms pivot_increment_fits
#print axioms pivot_remainder_lt
#print axioms subset_increment_fits
end TFQM.FiniteEnumeration
