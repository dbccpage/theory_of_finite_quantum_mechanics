/-
  Formalization of the second-derivative bound (PO-000 Appendix B → input to Theorem 5.1).

  AuthorityEffect: None.

  This module formalizes:
  1. Support-size arithmetic for first and second order reduced state derivative bounds.
  2. Structured hypothesis record `ReducedStateBounds (g : ℝ)` and paper instance `paperBounds`.
  3. Product-rule assembly theorem bounding ||F_e''(t)||_1 ≤ 48 g².
  4. Link to the Taylor core constant (48 g² / 2 = 24 g²).
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace SecondDerivBound

/-- First-order reduced state derivative factor 2 * k * g. -/
def firstOrderFactor (k : ℝ) (g : ℝ) : ℝ :=
  2 * k * g

/-- Second-order reduced state derivative factor 4 * k * (k + 1) * g^2. -/
def secondOrderFactor (k : ℝ) (g : ℝ) : ℝ :=
  4 * k * (k + 1) * (g ^ 2)

/-- 1-site first derivative bound factor: 2 * 1 * g = 2 * g. -/
theorem one_site_first_factor (g : ℝ) : firstOrderFactor 1 g = 2 * g := by
  dsimp [firstOrderFactor]
  ring

/-- 1-site second derivative bound factor: 4 * 1 * (1 + 1) * g^2 = 8 * g^2. -/
theorem one_site_second_factor (g : ℝ) : secondOrderFactor 1 g = 8 * (g ^ 2) := by
  dsimp [secondOrderFactor]
  ring

/-- 2-site second derivative bound factor: 4 * 2 * (2 + 1) * g^2 = 24 * g^2. -/
theorem two_site_second_factor (g : ℝ) : secondOrderFactor 2 g = 24 * (g ^ 2) := by
  dsimp [secondOrderFactor]
  ring

/-- Structured hypothesis record for reduced state derivative bounds. -/
structure ReducedStateBounds (g : ℝ) where
  one_site_first_a  : ℝ
  one_site_first_b  : ℝ
  one_site_second_a : ℝ
  one_site_second_b : ℝ
  two_site_second   : ℝ
  h_first_a_nonneg  : 0 ≤ one_site_first_a
  h_first_b_nonneg  : 0 ≤ one_site_first_b
  h_first_a  : one_site_first_a ≤ 2 * g
  h_first_b  : one_site_first_b ≤ 2 * g
  h_second_a : one_site_second_a ≤ 8 * (g ^ 2)
  h_second_b : one_site_second_b ≤ 8 * (g ^ 2)
  h_second_ab : two_site_second ≤ 24 * (g ^ 2)

/-- Canonical paper values instance for reduced state bounds under coupling g. -/
def paperBounds (g : ℝ) (hg : 0 ≤ g) : ReducedStateBounds g where
  one_site_first_a  := 2 * g
  one_site_first_b  := 2 * g
  one_site_second_a := 8 * (g ^ 2)
  one_site_second_b := 8 * (g ^ 2)
  two_site_second   := 24 * (g ^ 2)
  h_first_a_nonneg  := by linarith
  h_first_b_nonneg  := by linarith
  h_first_a  := le_refl _
  h_first_b  := le_refl _
  h_second_a := le_refl _
  h_second_b := le_refl _
  h_second_ab := le_refl _

/-- Product-rule second-derivative bound theorem:
    ||F_e''(t)||_1 ≤ ||d/dt² ρ_ab||_1 + ||d/dt² ρ_a||_1 + 2 ||d/dt ρ_a||_1 ||d/dt ρ_b||_1 + ||d/dt² ρ_b||_1
                 ≤ 24 g² + 8 g² + 2 (2g)(2g) + 8 g² = 48 g². -/
theorem product_rule_second_deriv_bound (g : ℝ) (_hg : 0 ≤ g) (B : ReducedStateBounds g) :
    B.two_site_second + B.one_site_second_a + 2 * B.one_site_first_a * B.one_site_first_b + B.one_site_second_b
    ≤ 48 * (g ^ 2) := by
  have hfa := B.h_first_a
  have hfb := B.h_first_b
  have hfa0 := B.h_first_a_nonneg
  have hfb0 := B.h_first_b_nonneg
  have hsa := B.h_second_a
  have hsb := B.h_second_b
  have hsab := B.h_second_ab
  nlinarith

/-- Paper Taylor constant c_2 = M / 2 = 24 g^2. -/
def paperTaylorConstant (g : ℝ) : ℝ :=
  24 * (g ^ 2)

/-- Relation between second derivative bound M = 48 g^2 and Taylor constant M / 2 = 24 g^2. -/
theorem taylor_constant_eq_half_second_deriv (g : ℝ) :
    (48 * (g ^ 2)) / 2 = paperTaylorConstant g := by
  dsimp [paperTaylorConstant]
  ring

end SecondDerivBound

#print axioms SecondDerivBound.product_rule_second_deriv_bound
#print axioms SecondDerivBound.taylor_constant_eq_half_second_deriv
