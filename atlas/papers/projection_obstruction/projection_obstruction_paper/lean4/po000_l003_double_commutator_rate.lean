/-
  Toy Control Model: Real-Scalar Commutator Rate (LEAN_TOY).

  This module formalizes an algebraic toy control model for the conditional relation:
  - If a double bracket were non-zero, the quadratic prefactor c_2 = (1/2) * |[[H, A], H]|
    would be strictly positive.
  - Note (C21): In this real-scalar model (carrier ℝ), multiplication is commutative,
    so bracket(A, B) = A * B - B * A vanishes identically (bracket A B = 0) and
    doubleBracket H A = 0. The hypothesis doubleBracket H A ≠ 0 has no positive instances
    in ℝ. This file is retained as an explicit commutative zero-commutator toy control model,
    not an operator or physical mechanization of Theorem 5.1.
-/
import Mathlib.Data.Real.Basic

namespace DoubleCommutatorRate

/-- Lie algebra commutator bracket [A, B] = A * B - B * A on real algebra.
    Note (C21): On ℝ this bracket is identically zero. -/
def bracket (A B : ℝ) : ℝ :=
  A * B - B * A

/-- Double commutator [[H, A], H]. -/
def doubleBracket (H A : ℝ) : ℝ :=
  bracket (bracket H A) H

/-- Short-time quadratic prefactor function c_2(H, A) = half * |[[H, A], H]|. -/
def shortTimeRatePrefactor (H A half : ℝ) : ℝ :=
  half * |doubleBracket H A|

/-- Core Rate Theorem: If the double commutator [[H, A], H] is non-zero, then for any positive
    half-scalar (half > 0), the short-time quadratic prefactor c_2 is strictly positive. -/
theorem short_time_rate_positive (H A half : ℝ) (h_half_pos : 0 < half)
    (h_non_zero : doubleBracket H A ≠ 0) :
    0 < shortTimeRatePrefactor H A half := by
  dsimp [shortTimeRatePrefactor]
  have h_abs_pos : 0 < |doubleBracket H A| := abs_pos.mpr h_non_zero
  exact mul_pos h_half_pos h_abs_pos

/-- Product-state defect lower bound at short time t: c_2 * t^2 >= 0. -/
theorem short_time_defect_lower_bound (c2 t : ℝ) (hc2 : 0 ≤ c2) :
    0 ≤ c2 * (t * t) := by
  have ht2 : 0 ≤ t * t := mul_self_nonneg t
  exact mul_nonneg hc2 ht2

end DoubleCommutatorRate

#print axioms DoubleCommutatorRate.short_time_defect_lower_bound
#print axioms DoubleCommutatorRate.short_time_rate_positive
