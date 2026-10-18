

namespace FableHilbertWalk20260819.H028

theorem one_pow_int (k : Nat) : (1 : Int) ^ k = 1 := by
  induction k with
  | zero => rfl
  | succ n ih =>
    show (1 : Int) ^ n * 1 = 1
    rw [ih, Int.mul_one]

theorem sphere_power_reduction (x y : Int) (h : x * x + y * y = 1) (k : Nat) :
    (x * x + y * y) ^ k = 1 := by
  rw [h]
  exact one_pow_int k

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

theorem deg4_reduction_on_circle (x y c4 c3 c0 : Int) (h : x * x + y * y = 1) :
    c4 * (x * x * x * x) + c3 * (x * x * x * y) + (c4 + c0) * (x * x * y * y) + c3 * (x * y * y * y) + c0 * (y * y * y * y) =
    c4 * (x * x) + c3 * (x * y) + c0 * (y * y) := by
  have hf := deg4_frame_additive_factorization x y c4 c3 c0
  rw [hf, h, Int.one_mul]

theorem arbitrary_degree_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) (m : Nat) :
    (x * x + y * y) ^ m * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) := by
  have hs : (x * x + y * y) ^ m = 1 := sphere_power_reduction x y h m
  rw [hs, Int.one_mul]

theorem deg4_explicit_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) :
    (x * x + y * y) ^ 1 * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) :=
  arbitrary_degree_reduction x y c20 c11 c02 h 1

theorem deg6_explicit_reduction (x y c20 c11 c02 : Int) (h : x * x + y * y = 1) :
    (x * x + y * y) ^ 2 * (c20 * (x * x) + c11 * (x * y) + c02 * (y * y)) =
    c20 * (x * x) + c11 * (x * y) + c02 * (y * y) :=
  arbitrary_degree_reduction x y c20 c11 c02 h 2

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

private def l5aProvenance : String :=
  "Origin: lean4/H028ArbitraryDegreePolynomialReduction.lean Claim: one_pow_int AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
