import Std

/- All-order natural-number arithmetic for the Taylor constants.
   No matrix norm, quantum dynamics, Taylor theorem or analytic limit is
   formalized here. Those arguments remain in the manuscript. -/
namespace PO000.ShortTimeJets

def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n

def rising (k : Nat) : Nat → Nat
  | 0 => 1
  | n + 1 => (k + n) * rising k n

def jetFactor (n : Nat) : Nat := 2 ^ (n + 1) * factorial (n + 1)
def normalizedFactor (n : Nat) : Nat := 2 ^ (n + 1) * (n + 1)
def remainderFactor (j : Nat) : Nat := 2 ^ (j + 2) * (j + 2)

theorem one_site_rising (n : Nat) : rising 1 n = factorial n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [rising, factorial, ih, Nat.add_comm]

theorem two_site_rising (n : Nat) : rising 2 n = factorial (n + 1) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp [rising, factorial, ih, Nat.add_comm, Nat.add_left_comm]

theorem one_site_factor (n : Nat) :
    2 ^ n * rising 1 n = 2 ^ n * factorial n := by
  rw [one_site_rising]

theorem two_site_factor (n : Nat) :
    2 ^ n * rising 2 n = 2 ^ n * factorial (n + 1) := by
  rw [two_site_rising]

theorem sum_of_two_equal_bounds (n : Nat) :
    2 * (2 ^ n * factorial (n + 1)) = jetFactor n := by
  simp [jetFactor, Nat.pow_succ, Nat.mul_comm, Nat.mul_assoc]

theorem factorial_normalization (n : Nat) :
    jetFactor n = normalizedFactor n * factorial n := by
  simp [jetFactor, normalizedFactor, factorial, Nat.mul_assoc]

theorem integral_remainder_normalization (j : Nat) :
    jetFactor (j + 1) = remainderFactor j * factorial (j + 1) := by
  simp [jetFactor, remainderFactor, factorial, Nat.mul_assoc, Nat.add_assoc]

theorem first_remainder : remainderFactor 1 = 24 := by decide
theorem second_remainder : remainderFactor 2 = 64 := by decide
theorem third_remainder : remainderFactor 3 = 160 := by decide

end PO000.ShortTimeJets

#print axioms PO000.ShortTimeJets.one_site_rising
#print axioms PO000.ShortTimeJets.two_site_rising
#print axioms PO000.ShortTimeJets.one_site_factor
#print axioms PO000.ShortTimeJets.two_site_factor
#print axioms PO000.ShortTimeJets.sum_of_two_equal_bounds
#print axioms PO000.ShortTimeJets.factorial_normalization
#print axioms PO000.ShortTimeJets.integral_remainder_normalization
#print axioms PO000.ShortTimeJets.first_remainder
#print axioms PO000.ShortTimeJets.second_remainder
#print axioms PO000.ShortTimeJets.third_remainder
