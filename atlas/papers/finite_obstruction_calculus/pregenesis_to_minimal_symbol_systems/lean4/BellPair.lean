import Paper
import Init.Data.Rat

/-! Exact rational uniform-marginal pair distributions for the missed CHSH
orientation. Boolean output labels are connected explicitly to integer signs.
No physical realization or unrestricted contextuality theorem is asserted. -/
namespace PreMssn.BellPair

def sign (b : Bool) : Int := if b then -1 else 1

theorem sign_xor (a b : Bool) : sign (Bool.xor a b) = sign a * sign b := by
  cases a <;> cases b <;> decide

theorem integer_sign_product (a0 a1 b0 b1 : Bool) :
    (sign a0 * sign b0) * (sign a0 * sign b1) *
      (sign a1 * sign b0) * (sign a1 * sign b1) = 1 := by
  rw [Int.mul_assoc ((sign a0 * sign b0) * (sign a0 * sign b1))
    (sign a1 * sign b0) (sign a1 * sign b1)]
  rw [← sign_xor, ← sign_xor, ← sign_xor, ← sign_xor,
    ← sign_xor, ← sign_xor, ← sign_xor, deterministic_sign_product]
  rfl

theorem sign_representation (x : Int) (h : x = 1 ∨ x = -1) : ∃ b, sign b = x := by
  rcases h with h | h
  · exact ⟨false, h.symm⟩
  · exact ⟨true, h.symm⟩

theorem arbitrary_integer_sign_product (a0 a1 b0 b1 : Int)
    (ha0 : a0 = 1 ∨ a0 = -1) (ha1 : a1 = 1 ∨ a1 = -1)
    (hb0 : b0 = 1 ∨ b0 = -1) (hb1 : b1 = 1 ∨ b1 = -1) :
    (a0*b0) * (a0*b1) * (a1*b0) * (a1*b1) = 1 := by
  obtain ⟨a, rfl⟩ := sign_representation a0 ha0
  obtain ⟨a', rfl⟩ := sign_representation a1 ha1
  obtain ⟨b, rfl⟩ := sign_representation b0 hb0
  obtain ⟨b', rfl⟩ := sign_representation b1 hb1
  exact integer_sign_product a a' b b'

theorem target_has_no_deterministic_integer_assignment (a0 a1 b0 b1 : Int)
    (ha0 : a0 = 1 ∨ a0 = -1) (ha1 : a1 = 1 ∨ a1 = -1)
    (hb0 : b0 = 1 ∨ b0 = -1) (hb1 : b1 = 1 ∨ b1 = -1) :
    ¬(a0*b0 = 1 ∧ a0*b1 = 1 ∧ a1*b0 = -1 ∧ a1*b1 = 1) := by
  rintro ⟨h00, h01, h10, h11⟩
  have hp := arbitrary_integer_sign_product a0 a1 b0 b1 ha0 ha1 hb0 hb1
  rw [h00, h01, h10, h11] at hp
  contradiction

structure PairDistribution where
  probability : Bool → Bool → Rat
  nonnegative : ∀ a b, 0 ≤ probability a b
  normalized : probability false false + probability false true +
    probability true false + probability true true = 1

def pairProbability (negative a b : Bool) : Rat :=
  if Bool.xor a b == negative then (1 : Rat) / 2 else 0

def pairDistribution (negative : Bool) : PairDistribution where
  probability := pairProbability negative
  nonnegative a b := by cases negative <;> cases a <;> cases b <;> decide +kernel
  normalized := by cases negative <;> decide +kernel

theorem uniform_first_marginal (negative a : Bool) :
    (pairDistribution negative).probability a false +
      (pairDistribution negative).probability a true = (1 : Rat) / 2 := by
  cases negative <;> cases a <;> decide +kernel

theorem uniform_second_marginal (negative b : Bool) :
    (pairDistribution negative).probability false b +
      (pairDistribution negative).probability true b = (1 : Rat) / 2 := by
  cases negative <;> cases b <;> decide +kernel

def expectation (p : PairDistribution) : Rat :=
  (sign false : Rat) * (sign false : Rat) * p.probability false false +
  (sign false : Rat) * (sign true : Rat) * p.probability false true +
  (sign true : Rat) * (sign false : Rat) * p.probability true false +
  (sign true : Rat) * (sign true : Rat) * p.probability true true

theorem pair_correlation (negative : Bool) :
    expectation (pairDistribution negative) = (sign negative : Rat) := by
  cases negative <;> decide +kernel

def model (x y : Bool) : PairDistribution := pairDistribution (x && !y)

theorem model_correlations :
    (expectation (model false false), expectation (model false true),
      expectation (model true false), expectation (model true true)) =
    ((1 : Rat), (1 : Rat), (-1 : Rat), (1 : Rat)) := by decide +kernel

theorem model_uniform_marginals (x y a b : Bool) :
    ((model x y).probability a false + (model x y).probability a true = (1 : Rat) / 2) ∧
    ((model x y).probability false b + (model x y).probability true b = (1 : Rat) / 2) :=
  ⟨uniform_first_marginal _ _, uniform_second_marginal _ _⟩

/-- Replay order is (false,false), (false,true), (true,false), (true,true),
with common denominator 2. -/
def numerators (negative : Bool) : List Int :=
  if negative then [0,1,1,0] else [1,0,0,1]

theorem numerators_represent_distribution (negative : Bool) :
    (pairDistribution negative).probability false false = ((numerators negative).getD 0 0 : Rat) / 2 ∧
    (pairDistribution negative).probability false true = ((numerators negative).getD 1 0 : Rat) / 2 ∧
    (pairDistribution negative).probability true false = ((numerators negative).getD 2 0 : Rat) / 2 ∧
    (pairDistribution negative).probability true true = ((numerators negative).getD 3 0 : Rat) / 2 := by
  cases negative <;> decide +kernel

end PreMssn.BellPair
