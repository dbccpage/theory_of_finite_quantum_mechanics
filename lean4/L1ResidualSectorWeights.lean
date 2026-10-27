-- Narrowed slice of L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.
-- One pair of sector weights and two length-4 holonomy checks.
-- No weighted masses and no general n-cycle.

def weightA : Nat × Nat := (2, 0)
def weightB : Nat × Nat := (0, 2)

def coordSum (w : Nat × Nat) : Nat := w.1 + w.2

theorem same_phi1 : coordSum weightA = 2 ∧ coordSum weightB = 2 := by
  decide

theorem weights_differ : weightA ≠ weightB := by
  decide

theorem holonomy_two_not_divisible : ∀ k : Nat, 4 * k ≠ 2 := by
  intro k
  omega

theorem holonomy_four_divisible : 4 * 1 = 4 := by
  decide

#print axioms same_phi1
#print axioms weights_differ
#print axioms holonomy_two_not_divisible
#print axioms holonomy_four_divisible
