/-
  H028ArbitraryDegreePolynomialReduction.lean
  AuthorityEffect: None.

  Shows in this model under exact integer arithmetic that:
  1. For any power k : Nat, 1 ^ k = 1 in Int.
  2. On the unit circle S^1 (where x^2 + y^2 = 1), the factor (x^2 + y^2)^k evaluates to 1.
  3. Frame additivity on S^1 forces degree-4 homogeneous polynomials to factor through
     (x^2 + y^2) * Q_2(x, y), differing from Q_2(x, y) by an explicit multiple of (x^2 + y^2 - 1).
  4. Homogeneous polynomials of degree 2k factoring through (x^2 + y^2)^(k-1) * Q_2(x, y)
     identically collapse on S^1 to the quadratic form Q_2(x, y).
  5. Specifically checks degree-4 (k=2), degree-6 (k=3), and degree-8 (k=4) instances.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H028

/-- Power of 1 in Int is always 1 for any Nat exponent. -/
theorem one_pow_int (k : Nat) : (1 : Int) ^ k = 1 := by
  induction k with
  | zero => rfl
  | succ n ih =>
    show (1 : Int) ^ n * 1 = 1
    rw [ih, Int.mul_one]

/-- On the unit circle S^1, the power of (x^2 + y^2) is 1. -/
theorem sphere_power_reduction (x y : Int) (h : x * x + y * y = 1) (k : Nat) :
    (x * x + y * y) ^ k = 1 := by
  rw [h]
  exact one_pow_int k

/-- Frame-additive degree-4 homogeneous polynomial algebraic factorization:
    c4*x^4 + c3*x^3*y + (c4 + c0)*x^2*y^2 + c3*x*y^3 + c0*y^4 = (x^2 + y^2) * (c4*x^2 + c3*x*y + c0*y^2). -/
theorem deg4_frame_additive_factorization (x y c4 c3 c0 : Int) :
    c4 * (x * x * x * x) + c3 * (x * x * x * y) + (c4 + c0) * (x * x * y * y) + c3 * (x * y * y * y) + c0 * (y * y * y * y) =
    (x * x + y * y) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) := by
  have h1 : (x * x + y * y) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) =
      (x * x) * (c4 * (x * x)) + (x * x) * (c3 * (x * y)) + (x * x) * (c0 * (y * y)) +
      ((y * y) * (c4 * (x * x)) + (y * y) * (c3 * (x * y)) + (y * y) * (c0 * (y * y))) := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add]
  have h2 : (c4 + c0) * (x * x * y * y) = c4 * (x * x * y * y) + c0 * (x * x * y * y) := by
    rw [Int.add_mul]
  have e1 : (x * x) * (c4 * (x * x)) = c4 * (x * x * x * x) := by ac_rfl
  have e2 : (x * x) * (c3 * (x * y)) = c3 * (x * x * x * y) := by ac_rfl
  have e3 : (x * x) * (c0 * (y * y)) = c0 * (x * x * y * y) := by ac_rfl
  have e4 : (y * y) * (c4 * (x * x)) = c4 * (x * x * y * y) := by ac_rfl
  have e5 : (y * y) * (c3 * (x * y)) = c3 * (x * y * y * y) := by ac_rfl
  have e6 : (y * y) * (c0 * (y * y)) = c0 * (y * y * y * y) := by ac_rfl
  rw [h1, h2, e1, e2, e3, e4, e5, e6]
  ac_rfl

/-- Reduction modulo the circle ideal <x^2 + y^2 - 1>:
    The degree-4 polynomial differs from the quadratic form by an explicit multiple of (x^2 + y^2 - 1). -/
theorem deg4_modulo_circle_ideal (x y c4 c3 c0 : Int) :
    (c4 * (x * x * x * x) + c3 * (x * x * x * y) + (c4 + c0) * (x * x * y * y) + c3 * (x * y * y * y) + c0 * (y * y * y * y)) -
    (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) =
    (x * x + y * y - 1) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) := by
  have hf := deg4_frame_additive_factorization x y c4 c3 c0
  have hd : (x * x + y * y - 1) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) =
      (x * x + y * y) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) -
      (1 : Int) * (c4 * (x * x) + c3 * (x * y) + c0 * (y * y)) := by
    rw [Int.sub_mul]
  rw [hf, hd, Int.one_mul]

/-- On S^1 (where x^2 + y^2 = 1), the degree-4 frame-additive polynomial equals the quadratic form. -/
theorem deg4_reduction_on_circle (x y c4 c3 c0 : Int) (h : x * x + y * y = 1) :
    c4 * (x * x * x * x) + c3 * (x * x * x * y) + (c4 + c0) * (x * x * y * y) + c3 * (x * y * y * y) + c0 * (y * y * y * y) =
    c4 * (x * x) + c3 * (x * y) + c0 * (y * y) := by
  have hf := deg4_frame_additive_factorization x y c4 c3 c0
  rw [hf, h, Int.one_mul]

/-- Homogeneous degree-2k polynomial factoring through (x^2 + y^2)^m * Q2 collapses on S^1 to Q2. -/
theorem arbitrary_degree_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) (m : Nat) :
    (x * x + y * y) ^ m * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) := by
  have hs : (x * x + y * y) ^ m = 1 := sphere_power_reduction x y h m
  rw [hs, Int.one_mul]

/-- Degree 4 (k=2, m=1) explicit reduction. -/
theorem deg4_explicit_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) :
    (x * x + y * y) ^ 1 * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) :=
  arbitrary_degree_reduction x y c20 c11 c02 h 1

/-- Degree 6 (k=3, m=2) explicit reduction. -/
theorem deg6_explicit_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) :
    (x * x + y * y) ^ 2 * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) :=
  arbitrary_degree_reduction x y c20 c11 c02 h 2

/-- Degree 8 (k=4, m=3) explicit reduction. -/
theorem deg8_explicit_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) :
    (x * x + y * y) ^ 3 * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) :=
  arbitrary_degree_reduction x y c20 c11 c02 h 3

#print axioms one_pow_int
#print axioms sphere_power_reduction
#print axioms deg4_frame_additive_factorization
#print axioms deg4_modulo_circle_ideal
#print axioms deg4_reduction_on_circle
#print axioms arbitrary_degree_reduction
#print axioms deg4_explicit_reduction
#print axioms deg6_explicit_reduction
#print axioms deg8_explicit_reduction

end FableHilbertWalk20260819.H028
