namespace L1MinkowskiSquareExpansion

theorem square_expansion (a b : Nat) :
    (a + b) * (a + b) = a * a + b * b + 2 * (a * b) := by
  calc
    (a + b) * (a + b) = a * (a + b) + b * (a + b) := Nat.add_mul a b (a + b)
    _ = (a * a + a * b) + (b * a + b * b) := by rw [Nat.mul_add, Nat.mul_add]
    _ = a * a + b * b + 2 * (a * b) := by
      rw [Nat.mul_comm b a]
      omega

theorem cross_positive (a b : Nat) (ha : a > 0) (hb : b > 0) : 2 * (a * b) > 0 := by
  have hab : a * b > 0 := Nat.mul_pos ha hb
  omega

theorem square_strict (a b : Nat) (ha : a > 0) (hb : b > 0) :
    a * a + b * b < (a + b) * (a + b) := by
  have hexp := square_expansion a b
  have hpos := cross_positive a b ha hb
  omega

theorem cross_zero_left (b : Nat) : 2 * ((0 : Nat) * b) = 0 := by
  omega

theorem cross_zero_right (a : Nat) : 2 * (a * (0 : Nat)) = 0 := by
  omega

theorem square_eq_left_zero (b : Nat) : (0 + b) * (0 + b) = b * b := by
  have hexp := square_expansion 0 b
  have hzero := cross_zero_left b
  omega

theorem square_eq_right_zero (a : Nat) : (a + 0) * (a + 0) = a * a := by
  have hexp := square_expansion a 0
  have hzero := cross_zero_right a
  omega

theorem cubic_sum (a b : Nat) :
    (a + b) * (a + b) * (a + b) = a * a * a + b * b * b + 3 * a * b * (a + b) := by
  have hsq := square_expansion a b
  rw [hsq, Nat.mul_add]
  have expand (c : Nat) :
      (a * a + b * b + 2 * (a * b)) * c = a * a * c + b * b * c + 2 * ((a * b) * c) := by
    calc
      (a * a + b * b + 2 * (a * b)) * c
          = (a * a + b * b) * c + (2 * (a * b)) * c := by rw [Nat.add_mul]
      _ = a * a * c + b * b * c + (2 * (a * b)) * c := by rw [Nat.add_mul]
      _ = a * a * c + b * b * c + 2 * ((a * b) * c) := by rw [Nat.mul_assoc 2 (a * b) c]
  rw [expand a, expand b]
  have hcross : 3 * a * b * (a + b) = (3 * (a * b)) * a + (3 * (a * b)) * b := by
    calc
      3 * a * b * (a + b) = 3 * a * b * a + 3 * a * b * b := by rw [Nat.mul_add]
      _ = (3 * (a * b)) * a + (3 * (a * b)) * b := by rw [Nat.mul_assoc 3 a b]
  rw [hcross, Nat.mul_assoc 3 (a * b) a, Nat.mul_assoc 3 (a * b) b]
  have hcommA : b * b * a = a * b * b := by
    calc
      b * b * a = b * (b * a) := by rw [Nat.mul_assoc]
      _ = b * (a * b) := by rw [Nat.mul_comm b a]
      _ = b * a * b := by rw [← Nat.mul_assoc]
      _ = a * b * b := by rw [Nat.mul_comm b a]
  have hcommB : a * a * b = a * b * a := by
    calc
      a * a * b = a * (a * b) := by rw [Nat.mul_assoc]
      _ = a * (b * a) := by rw [Nat.mul_comm a b]
      _ = a * b * a := by rw [← Nat.mul_assoc]
  have htwo (t : Nat) : 2 * t = t + t := by omega
  have hthree (t : Nat) : 3 * t = t + t + t := by omega
  rw [htwo (a * b * a), htwo (a * b * b), hthree (a * b * a), hthree (a * b * b), hcommA, hcommB]
  omega

theorem disjoint_pair_squares (x y : Nat) :
    (x + 0) * (x + 0) + (0 + y) * (0 + y) = x * x + y * y := by
  rw [Nat.add_zero, Nat.zero_add]

end L1MinkowskiSquareExpansion

#print axioms L1MinkowskiSquareExpansion.square_expansion
#print axioms L1MinkowskiSquareExpansion.cross_positive
#print axioms L1MinkowskiSquareExpansion.square_strict
#print axioms L1MinkowskiSquareExpansion.cross_zero_left
#print axioms L1MinkowskiSquareExpansion.cross_zero_right
#print axioms L1MinkowskiSquareExpansion.square_eq_left_zero
#print axioms L1MinkowskiSquareExpansion.square_eq_right_zero
#print axioms L1MinkowskiSquareExpansion.cubic_sum
#print axioms L1MinkowskiSquareExpansion.disjoint_pair_squares
