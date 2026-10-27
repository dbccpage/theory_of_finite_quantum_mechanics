-- FQ-GAP-CONTINUUM-HILBERT-LIFT. Not a default target.
-- Integer slice: 2 * a = 1 has no integer solution, and t * t - t - 1 has no integer root.
-- Scalar-field selection, l2 uniformity, and a completion stay outside this module.


namespace ContinuumHilbertLiftIntegerSlice
theorem twoMulNeOne (a : Int) : 2 * a ≠ 1 := by
  omega

theorem fourMulSquare (t : Int) : (2 * t) * (2 * t) = 4 * (t * t) := by
  calc
    (2 * t) * (2 * t) = 2 * (t * (2 * t)) := by rw [Int.mul_assoc]
    _ = 2 * (t * (t * 2)) := by rw [Int.mul_comm 2 t]
    _ = 2 * ((t * t) * 2) := by rw [← Int.mul_assoc t t 2]
    _ = 2 * (2 * (t * t)) := by rw [Int.mul_comm (t * t) 2]
    _ = (2 * 2) * (t * t) := by rw [← Int.mul_assoc 2 2 (t * t)]
    _ = 4 * (t * t) := by rw [show (2 : Int) * 2 = 4 by decide]

theorem discIdentity (t : Int) :
    4 * (t * t - t - 1) + 5 = (2 * t - 1) * (2 * t - 1) := by
  have hR : (2 * t - 1) * (2 * t - 1) = 4 * (t * t) - 4 * t + 1 := by
    calc
      (2 * t - 1) * (2 * t - 1)
          = (2 * t) * (2 * t - 1) - 1 * (2 * t - 1) := by rw [Int.sub_mul]
      _ = ((2 * t) * (2 * t) - (2 * t) * 1) - (1 * (2 * t) - 1 * 1) := by
            rw [Int.mul_sub, Int.mul_sub]
      _ = ((2 * t) * (2 * t) - 2 * t) - (2 * t - 1 * 1) := by
            rw [Int.mul_one, Int.one_mul]
      _ = ((2 * t) * (2 * t) - 2 * t) - (2 * t - 1) := by
            rw [Int.mul_one]
      _ = (4 * (t * t) - 2 * t) - (2 * t - 1) := by
            rw [fourMulSquare t]
      _ = 4 * (t * t) - 4 * t + 1 := by omega
  have hL : 4 * (t * t - t - 1) + 5 = 4 * (t * t) - 4 * t + 1 := by
    have h4 : 4 * (t * t - t - 1) = 4 * (t * t) - 4 * t - 4 := by
      calc
        4 * (t * t - t - 1) = 4 * (t * t - t) - 4 * 1 := by rw [Int.mul_sub]
        _ = (4 * (t * t) - 4 * t) - 4 := by rw [Int.mul_sub, Int.mul_one]
    omega
  exact hL.trans hR.symm

theorem natSqNeFive (k : Nat) : k * k ≠ 5 := by
  cases k with
  | zero => decide
  | succ k1 =>
    cases k1 with
    | zero => decide
    | succ k2 =>
      cases k2 with
      | zero => decide
      | succ k3 =>
        have h3 : (3 : Nat) ≤ k3 + 3 := by omega
        have hmul : 3 * 3 ≤ (k3 + 3) * (k3 + 3) := Nat.mul_le_mul h3 h3
        have h9 : 9 ≤ (k3 + 3) * (k3 + 3) := by
          simpa [show (3 : Nat) * 3 = 9 by decide] using hmul
        have hlt : 5 < (k3 + 3) * (k3 + 3) :=
          Nat.lt_of_lt_of_le (by decide : (5 : Nat) < 9) h9
        exact Nat.ne_of_gt hlt

theorem intSqNeFive (n : Int) : n * n ≠ 5 := by
  intro h
  have hnat : n.natAbs * n.natAbs = 5 := by
    have eqAbs : (n * n).natAbs = Int.natAbs 5 := congrArg Int.natAbs h
    rw [Int.natAbs_mul] at eqAbs
    exact eqAbs
  exact natSqNeFive n.natAbs hnat

theorem intPolyNeZero (t : Int) : t * t - t - 1 ≠ 0 := by
  intro h
  have hid : 4 * (t * t - t - 1) + 5 = (2 * t - 1) * (2 * t - 1) := discIdentity t
  have hsq : (2 * t - 1) * (2 * t - 1) = 5 := by
    rw [h] at hid
    omega
  exact intSqNeFive (2 * t - 1) hsq

#print axioms twoMulNeOne
#print axioms discIdentity
#print axioms intSqNeFive
#print axioms intPolyNeZero

end ContinuumHilbertLiftIntegerSlice
