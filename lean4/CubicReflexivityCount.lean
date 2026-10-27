-- TFQ-0184. Not a default target.
-- Nat arithmetic for the cubic reflexivity bound and one elimination product.
-- A tetron-homology reading, README custody, the F004 gap, noise sweeps,
-- and the evaluator role stay outside this module.
-- AuthorityEffect: None.

namespace CubicReflexivityCount

theorem cubicReflexivity (n : Nat) : n * n * n ≤ n * n * n :=
  Nat.le_refl _

private theorem twoSub (k : Nat) : 2 * (k + 1) - 1 = 2 * k + 1 := by
  omega

private theorem threeSub (k : Nat) : 3 * (k + 1) - 1 = 3 * k + 2 := by
  omega

private theorem succSquare (k : Nat) : (k + 1) * (k + 1) = k * k + 2 * k + 1 := by
  calc
    (k + 1) * (k + 1) = k * (k + 1) + 1 * (k + 1) := by rw [Nat.add_mul]
    _ = k * k + k * 1 + (k + 1) := by rw [Nat.mul_add, Nat.one_mul]
    _ = k * k + k + (k + 1) := by rw [Nat.mul_one]
    _ = k * k + 2 * k + 1 := by omega

private theorem succCube (k : Nat) :
    (k + 1) * (k + 1) * (k + 1) = k * k * k + 3 * (k * k) + 3 * k + 1 := by
  calc
    (k + 1) * (k + 1) * (k + 1) = (k * k + 2 * k + 1) * (k + 1) := by rw [succSquare]
    _ = (k * k + 2 * k + 1) * k + (k * k + 2 * k + 1) := by
      rw [Nat.mul_add, Nat.mul_one]
    _ = (k * k + 2 * k) * k + 1 * k + (k * k + 2 * k + 1) := by
      rw [Nat.add_mul]
    _ = k * k * k + (2 * k) * k + k + (k * k + 2 * k + 1) := by
      rw [Nat.add_mul, Nat.one_mul]
    _ = k * k * k + 2 * (k * k) + k + k * k + 2 * k + 1 := by
      rw [Nat.mul_assoc 2 k k]; omega
    _ = k * k * k + 3 * (k * k) + 3 * k + 1 := by omega

private theorem scaledCube (k : Nat) :
    2 * (k * k * k + 3 * (k * k) + 3 * k + 1) = 2 * (k * k * k) + 6 * (k * k) + 6 * k + 2 := by
  calc
    2 * (k * k * k + 3 * (k * k) + 3 * k + 1)
        = 2 * (k * k * k + 3 * (k * k) + 3 * k) + 2 := by
      rw [Nat.mul_add, Nat.mul_one]
    _ = 2 * (k * k * k + 3 * (k * k)) + 2 * (3 * k) + 2 := by rw [Nat.mul_add]
    _ = 2 * (k * k * k) + 2 * (3 * (k * k)) + 2 * (3 * k) + 2 := by rw [Nat.mul_add]
    _ = 2 * (k * k * k) + 6 * (k * k) + 6 * k + 2 := by omega

private theorem rowProduct (k : Nat) : (k + 1) * (2 * k + 1) = 2 * (k * k) + 3 * k + 1 := by
  calc
    (k + 1) * (2 * k + 1) = k * (2 * k + 1) + (2 * k + 1) := by
      rw [Nat.add_mul, Nat.one_mul]
    _ = k * (2 * k) + k * 1 + 2 * k + 1 := by
      rw [Nat.mul_add]; omega
    _ = (2 * k) * k + k + 2 * k + 1 := by rw [Nat.mul_one, Nat.mul_comm k (2 * k)]
    _ = 2 * (k * k) + 3 * k + 1 := by
      rw [Nat.mul_assoc]; omega

private theorem distributedRow (k : Nat) :
    k * (2 * (k * k) + 3 * k + 1) = 2 * (k * k * k) + 3 * (k * k) + k := by
  calc
    k * (2 * (k * k) + 3 * k + 1) = k * (2 * (k * k) + 3 * k) + k := by
      rw [Nat.mul_add, Nat.mul_one]
    _ = k * (2 * (k * k)) + k * (3 * k) + k := by rw [Nat.mul_add]
    _ = 2 * (k * (k * k)) + 3 * (k * k) + k := by
      rw [Nat.mul_left_comm, Nat.mul_left_comm k 3 k]
    _ = 2 * (k * k * k) + 3 * (k * k) + k := by
      rw [← Nat.mul_assoc k k k]

private theorem tailProduct (k : Nat) : (k + 1) * (3 * k + 2) = 3 * (k * k) + 5 * k + 2 := by
  calc
    (k + 1) * (3 * k + 2) = k * (3 * k + 2) + (3 * k + 2) := by
      rw [Nat.add_mul, Nat.one_mul]
    _ = k * (3 * k) + k * 2 + 3 * k + 2 := by
      rw [Nat.mul_add]; omega
    _ = 3 * (k * k) + 5 * k + 2 := by
      rw [Nat.mul_left_comm k 3 k, Nat.mul_comm k 2]; omega

private theorem elimExpanded (k : Nat) :
    k * (k + 1) * (2 * k + 1) + (k + 1) * (3 * k + 2)
      = 2 * (k * k * k) + 6 * (k * k) + 6 * k + 2 := by
  calc
    k * (k + 1) * (2 * k + 1) + (k + 1) * (3 * k + 2)
        = k * ((k + 1) * (2 * k + 1)) + (k + 1) * (3 * k + 2) := by rw [Nat.mul_assoc]
    _ = k * (2 * (k * k) + 3 * k + 1) + (3 * (k * k) + 5 * k + 2) := by
      rw [rowProduct, tailProduct]
    _ = 2 * (k * k * k) + 6 * (k * k) + 6 * k + 2 := by
      rw [distributedRow]; omega

theorem eliminationSplit (n : Nat) (hn : 1 ≤ n) :
    2 * (n * n * n) = (n - 1) * n * (2 * n - 1) + n * (3 * n - 1) := by
  match n with
  | 0 => omega
  | k + 1 =>
    have hk : (k + 1) - 1 = k := by omega
    rw [hk, twoSub k, threeSub k, succCube k, scaledCube k]
    exact (elimExpanded k).symm

theorem gapAtLeastTwo (n : Nat) (hn : 1 ≤ n) : 2 ≤ n * (3 * n - 1) := by
  have h3 : 2 ≤ 3 * n - 1 := by omega
  exact Nat.mul_le_mul hn h3

theorem eliminationBelowTwiceCube (n : Nat) (hn : 1 ≤ n) :
    (n - 1) * n * (2 * n - 1) < 2 * (n * n * n) := by
  have hgap : 0 < n * (3 * n - 1) := by
    have h2 := gapAtLeastTwo n hn
    omega
  have hlt :
      (n - 1) * n * (2 * n - 1)
        < (n - 1) * n * (2 * n - 1) + n * (3 * n - 1) :=
    Nat.lt_add_of_pos_right hgap
  rw [eliminationSplit n hn]
  exact hlt

theorem fourCube : (4 : Nat) * 4 * 4 = 64 := by
  decide

theorem fourSumOfSquares : (1 * 1 + 2 * 2 + 3 * 3 : Nat) = 14 := by
  decide

theorem fourClosedForm : (3 * 4 * (2 * 4 - 1)) / 6 = 14 := by
  decide

theorem fourCountBelowCube : (14 : Nat) < 64 := by
  decide

#print axioms cubicReflexivity
#print axioms eliminationSplit
#print axioms gapAtLeastTwo
#print axioms eliminationBelowTwiceCube
#print axioms fourCube
#print axioms fourSumOfSquares
#print axioms fourClosedForm
#print axioms fourCountBelowCube

end CubicReflexivityCount
