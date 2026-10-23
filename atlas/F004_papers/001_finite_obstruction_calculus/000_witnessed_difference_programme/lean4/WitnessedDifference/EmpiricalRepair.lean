/-
Core-only finite integer primal/dual weak duality. This is the algebraic
certificate milestone for the rational native LP, not a Lean simplex or
measure-theoretic iid theorem. No admitted proofs or custom axioms.
-/
import Lean

namespace WitnessedDifference.EmpiricalRepair

def sum (n : Nat) (f : Nat → Int) : Int :=
  match n with
  | 0 => 0
  | n + 1 => sum n f + f n

theorem sum_add (n : Nat) (f g : Nat → Int) :
    sum n (fun j => f j + g j) = sum n f + sum n g := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sum, ih]; omega

theorem sum_mul (n : Nat) (f : Nat → Int) (a : Int) :
    sum n (fun j => f j * a) = sum n f * a := by
  induction n with
  | zero => simp [sum]
  | succ n ih => simp only [sum, ih, Int.add_mul]

theorem sum_congr (n : Nat) (f g : Nat → Int)
    (h : ∀ j, j < n → f j = g j) : sum n f = sum n g := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [sum, sum, ih (fun j hj => h j (by omega)), h n (by omega)]

theorem sum_le (n : Nat) (f g : Nat → Int)
    (h : ∀ j, j < n → f j ≤ g j) : sum n f ≤ sum n g := by
  induction n with
  | zero => exact Int.le_refl 0
  | succ n ih =>
    exact Int.add_le_add (ih (fun j hj => h j (by omega))) (h n (by omega))

theorem sum_zero (n : Nat) : sum n (fun _ => 0) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [sum, ih, Int.add_zero]

theorem sum_swap (m n : Nat) (f : Nat → Nat → Int) :
    sum m (fun i => sum n (f i)) = sum n (fun j => sum m (fun i => f i j)) := by
  induction m with
  | zero => simp only [sum, sum_zero]
  | succ m ih =>
    simp only [sum]
    rw [ih, ← sum_add]

theorem transpose_pairing (m n : Nat) (a : Nat → Nat → Int)
    (x y : Nat → Int) :
    sum m (fun i => y i * sum n (fun j => a i j * x j)) =
    sum n (fun j => sum m (fun i => y i * a i j) * x j) := by
  calc
    _ = sum m (fun i => sum n (fun j => y i * a i j * x j)) := by
      apply sum_congr
      intro i hi
      rw [Int.mul_comm, ← sum_mul]
      apply sum_congr
      intro j hj
      rw [Int.mul_comm (a i j * x j) (y i), Int.mul_assoc]
    _ = sum n (fun j => sum m (fun i => y i * a i j * x j)) := sum_swap m n _
    _ = _ := by
      apply sum_congr
      intro j hj
      exact sum_mul m _ _

theorem weak_duality (m n : Nat) (a : Nat → Nat → Int)
    (b c x y : Nat → Int)
    (nonnegative : ∀ j, j < n → 0 ≤ x j)
    (primal : ∀ i, i < m → sum n (fun j => a i j * x j) = b i)
    (dual : ∀ j, j < n → sum m (fun i => y i * a i j) ≤ c j) :
    sum m (fun i => y i * b i) ≤ sum n (fun j => c j * x j) := by
  calc
    _ = sum m (fun i => y i * sum n (fun j => a i j * x j)) := by
      apply sum_congr
      intro i hi
      rw [primal i hi]
    _ = sum n (fun j => sum m (fun i => y i * a i j) * x j) :=
      transpose_pairing m n a x y
    _ ≤ _ := by
      apply sum_le
      intro j hj
      exact Int.mul_le_mul_of_nonneg_right (dual j hj) (nonnegative j hj)

theorem matching_objective_lower_bound (m n : Nat) (a : Nat → Nat → Int)
    (b c x y : Nat → Int)
    (dual : ∀ j, j < n → sum m (fun i => y i * a i j) ≤ c j)
    (matching : sum n (fun j => c j * x j) = sum m (fun i => y i * b i)) :
    ∀ z : Nat → Int,
      (∀ j, j < n → 0 ≤ z j) →
      (∀ i, i < m → sum n (fun j => a i j * z j) = b i) →
      sum n (fun j => c j * x j) ≤ sum n (fun j => c j * z j) := by
  intro z hz ha
  rw [matching]
  exact weak_duality m n a b c z y hz ha dual

theorem matching_certificate_optimal (m n : Nat) (a : Nat → Nat → Int)
    (b c x y : Nat → Int)
    (nonnegative : ∀ j, j < n → 0 ≤ x j)
    (primal : ∀ i, i < m → sum n (fun j => a i j * x j) = b i)
    (dual : ∀ j, j < n → sum m (fun i => y i * a i j) ≤ c j)
    (matching : sum n (fun j => c j * x j) = sum m (fun i => y i * b i)) :
    (∀ j, j < n → 0 ≤ x j) ∧
    (∀ i, i < m → sum n (fun j => a i j * x j) = b i) ∧
    ∀ z : Nat → Int,
      (∀ j, j < n → 0 ≤ z j) →
      (∀ i, i < m → sum n (fun j => a i j * z j) = b i) →
      sum n (fun j => c j * x j) ≤ sum n (fun j => c j * z j) := by
  exact ⟨nonnegative, primal, matching_objective_lower_bound m n a b c x y dual matching⟩

#print axioms sum_add
#print axioms sum_mul
#print axioms sum_congr
#print axioms sum_le
#print axioms sum_zero
#print axioms sum_swap
#print axioms transpose_pairing
#print axioms weak_duality
#print axioms matching_objective_lower_bound
#print axioms matching_certificate_optimal

end WitnessedDifference.EmpiricalRepair
