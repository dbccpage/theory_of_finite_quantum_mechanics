import Mathlib.Data.Real.Basic
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import CaseCoverage

/-!
# Real Semialgebraic Branch Positivstellensatz & Sign Obstruction

This module formalizes exact rational Positivstellensatz certificates for real
semialgebraic branches where complex solutions exist, but real solutions are
strictly precluded by signs and sum-of-squares (SOS) relations (Prompt 08):

1. **Upper Real Boundary Obstruction (`x ≥ 2`)**:
   Constraint: `f(x, y) = x^2 + y^2 - 1 = 0`, `g(x) = x - 2 ≥ 0`.
   Positivstellensatz identity:
     `-1 = (-1/3) * (x^2 + y^2 - 1) + [(1/3)*(x - 2)^2 + (1/3)*y^2] + (4/3) * (x - 2)`
   where:
     - `a = -1/3`
     - `σ₀(x, y) = (1/3)*(x - 2)^2 + (1/3)*y^2 ≥ 0` (sum of squares)
     - `σ₁ = 4/3 ≥ 0` (positive scalar SOS)
   Refutation: `f = 0 ∧ g ≥ 0 → -1 ≥ 0 → False`.

2. **Lower Real Boundary Obstruction (`x ≤ -2`)**:
   Constraint: `f(x, y) = x^2 + y^2 - 1 = 0`, `g(x) = -2 - x ≥ 0`.
   Positivstellensatz identity:
     `-1 = (-1/3) * (x^2 + y^2 - 1) + [(1/3)*(x + 2)^2 + (1/3)*y^2] + (4/3) * (-2 - x)`
   Refutation: `f = 0 ∧ g ≥ 0 → -1 ≥ 0 → False`.

3. **General Stengle Positivstellensatz Evaluation Soundness**:
   Any identity `-1 = a * f + σ₀ + σ₁ * g` with `σ₀ ≥ 0` and `σ₁ ≥ 0` refutes
   the conjunction `f = 0 ∧ g ≥ 0`.

AuthorityEffect: None.
-/

namespace MUB.CADBranch

open MUB.CaseCoverage

/-!
## 1. General Stengle Positivstellensatz Soundness in ℝ
-/

/-- General evaluation soundness for a degree-1 Stengle Positivstellensatz certificate:
    If -1 = a * f + σ₀ + σ₁ * g with σ₀ ≥ 0 and σ₁ ≥ 0, then f = 0 and g ≥ 0 cannot hold. -/
theorem positivstellensatz_soundness (a f sigma0 sigma1 g : ℝ)
    (hid : -1 = a * f + sigma0 + sigma1 * g)
    (h_sigma0 : 0 ≤ sigma0)
    (h_sigma1 : 0 ≤ sigma1)
    (hf : f = 0)
    (hg : 0 ≤ g) : False := by
  have h_prod : 0 ≤ sigma1 * g := mul_nonneg h_sigma1 hg
  have h_rhs_nonneg : 0 ≤ a * f + sigma0 + sigma1 * g := by
    rw [hf, mul_zero, zero_add]
    linarith
  rw [← hid] at h_rhs_nonneg
  linarith

/-!
## 2. Upper Real Boundary Leaf: x ≥ 2 with Circle Constraint
-/

/-- Equality generator: circle equation x^2 + y^2 - 1. -/
def f_circle (x y : ℝ) : ℝ := x^2 + y^2 - 1

/-- Inequality guard: x - 2 ≥ 0. -/
def g_upper (x : ℝ) : ℝ := x - 2

/-- Sum-of-squares component σ₀(x, y) = (1/3)*(x - 2)^2 + (1/3)*y^2. -/
noncomputable def sigma0_upper (x y : ℝ) : ℝ :=
  (1/3 : ℝ) * (x - 2)^2 + (1/3 : ℝ) * y^2

/-- Constant sum-of-squares multiplier σ₁ = 4/3. -/
noncomputable def sigma1_upper : ℝ := (4/3 : ℝ)

/-- Exact rational Positivstellensatz algebraic identity for upper boundary:
    -1 = (-1/3) * f + σ₀ + σ₁ * g identically in ℝ[x, y]. -/
theorem positivstellensatz_upper_identity (x y : ℝ) :
    -1 = (-1/3 : ℝ) * f_circle x y + sigma0_upper x y + sigma1_upper * g_upper x := by
  simp only [f_circle, g_upper, sigma0_upper, sigma1_upper]
  ring

/-- Sum-of-squares term is non-negative everywhere in ℝ^2. -/
theorem sigma0_upper_nonneg (x y : ℝ) : 0 ≤ sigma0_upper x y := by
  simp only [sigma0_upper]
  have h1 : 0 ≤ (x - 2)^2 := sq_nonneg (x - 2)
  have h2 : 0 ≤ y^2 := sq_nonneg y
  linarith

/-- Multiplier is positive. -/
theorem sigma1_upper_nonneg : 0 ≤ sigma1_upper := by
  norm_num [sigma1_upper]

/-- Semantic consequence: Real variety with x^2 + y^2 = 1 and x ≥ 2 is empty. -/
theorem upper_boundary_real_infeasible (x y : ℝ)
    (hf : f_circle x y = 0)
    (hg : 0 ≤ g_upper x) : False := by
  exact positivstellensatz_soundness
    (-1/3 : ℝ) (f_circle x y) (sigma0_upper x y) sigma1_upper (g_upper x)
    (positivstellensatz_upper_identity x y)
    (sigma0_upper_nonneg x y)
    sigma1_upper_nonneg
    hf
    hg

/-!
## 3. Lower Real Boundary Leaf: x ≤ -2 with Circle Constraint
-/

/-- Inequality guard for lower boundary: -2 - x ≥ 0. -/
def g_lower (x : ℝ) : ℝ := -2 - x

/-- Sum-of-squares component σ₀(x, y) = (1/3)*(x + 2)^2 + (1/3)*y^2. -/
noncomputable def sigma0_lower (x y : ℝ) : ℝ :=
  (1/3 : ℝ) * (x + 2)^2 + (1/3 : ℝ) * y^2

/-- Exact rational Positivstellensatz algebraic identity for lower boundary:
    -1 = (-1/3) * f + σ₀ + σ₁ * g identically in ℝ[x, y]. -/
theorem positivstellensatz_lower_identity (x y : ℝ) :
    -1 = (-1/3 : ℝ) * f_circle x y + sigma0_lower x y + sigma1_upper * g_lower x := by
  simp only [f_circle, g_lower, sigma0_lower, sigma1_upper]
  ring

/-- Sum-of-squares term is non-negative everywhere in ℝ^2. -/
theorem sigma0_lower_nonneg (x y : ℝ) : 0 ≤ sigma0_lower x y := by
  simp only [sigma0_lower]
  have h1 : 0 ≤ (x + 2)^2 := sq_nonneg (x + 2)
  have h2 : 0 ≤ y^2 := sq_nonneg y
  linarith

/-- Semantic consequence: Real variety with x^2 + y^2 = 1 and x ≤ -2 is empty. -/
theorem lower_boundary_real_infeasible (x y : ℝ)
    (hf : f_circle x y = 0)
    (hg : 0 ≤ g_lower x) : False := by
  exact positivstellensatz_soundness
    (-1/3 : ℝ) (f_circle x y) (sigma0_lower x y) sigma1_upper (g_lower x)
    (positivstellensatz_lower_identity x y)
    (sigma0_lower_nonneg x y)
    sigma1_upper_nonneg
    hf
    hg

end MUB.CADBranch
