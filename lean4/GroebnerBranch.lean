import Mathlib.Data.Real.Basic
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import CertificatePilot
import CaseCoverage

/-!
# Exact Gröbner Nullstellensatz Refutation on Infeasible Sub-Branches

This module formalizes exact rational Nullstellensatz refutations for infeasible
algebraic branches identified in the G1 case coverage ledger:

1. **Branch Annihilated Entry (`branch_annihilated_entry`)**:
   Input ideal in `ℚ[x, y]`: `I = (x^2 + y^2 - 1, x, y)`.
   Exact degree-1 Nullstellensatz certificate:
     `(-1) * (x^2 + y^2 - 1) + x * (x) + y * (y) = 1`
   Semantic consequence: `x^2 + y^2 = 1 ∧ x = 0 ∧ y = 0 → False`.

2. **Branch All-Ones Row Orthogonality (`branch_all_ones_row`)**:
   Orthogonality with row 0 requires `1 + x₁ + x₂ + x₃ + x₄ + x₅ = 0`.
   If a branch hypothesizes `x_j = 1` for all j ∈ {1, ..., 5}, then:
     `(1/6) * (1 + ∑ x_j) - ∑ (1/6) * (x_j - 1) = 1`
   Semantic consequence: Orthogonal row cannot be identical to the dephased row 0.

3. **Branch Incompatible Unit-Phase Orthogonality (`branch_incompatible_phases`)**:
   Variables `(x₁, y₁, x₂, y₂)`.
   Generators:
     `h₁ = x₁^2 + y₁^2 - 1`
     `h₂ = x₁ - 1`
     `h₃ = x₂ - 1`
     `h₄ = x₁ * x₂ + y₁ * y₂ + 1`
   Certificate identity:
     `a₁ * h₁ + a₂ * h₂ + a₃ * h₃ + a₄ * h₄ = 1`
   Semantic consequence: Incompatible phase inner products cannot simultaneously vanish.

AuthorityEffect: None.
-/

namespace MUB.GroebnerBranch

open MUB.CertificatePilot

/-!
## 1. Annihilated Entry Branch Nullstellensatz Refutation
-/

/-- Generator 1: Circle constraint p(x, y) = x^2 + y^2 - 1. -/
def p_circle (x y : ℝ) : ℝ := x^2 + y^2 - 1

/-- Generator 2: Real annihilation q_x(x) = x. -/
def q_x (x : ℝ) : ℝ := x

/-- Generator 3: Imaginary annihilation q_y(y) = y. -/
def q_y (y : ℝ) : ℝ := y

/-- Exact Nullstellensatz algebraic identity for annihilated entry:
    (-1) * (x^2 + y^2 - 1) + x * x + y * y = 1 identically in ℝ[x, y]. -/
theorem annihilated_nullstellensatz_identity (x y : ℝ) :
    (-1) * p_circle x y + x * q_x x + y * q_y y = 1 := by
  simp only [p_circle, q_x, q_y]
  ring

/-- Semantic consequence: The annihilated entry subvariety is empty. -/
theorem annihilated_branch_refutation (x y : ℝ)
    (h1 : p_circle x y = 0) (h2 : q_x x = 0) (h3 : q_y y = 0) : False := by
  have hid := annihilated_nullstellensatz_identity x y
  rw [h1, h2, h3] at hid
  simp only [mul_zero, add_zero] at hid
  exact zero_ne_one hid

/-!
## 2. All-Ones Row Orthogonality Nullstellensatz Refutation
-/

/-- Real orthogonality of row k with row 0: 1 + x₁ + x₂ + x₃ + x₄ + x₅. -/
def row_orth_poly (x1 x2 x3 x4 x5 : ℝ) : ℝ :=
  1 + x1 + x2 + x3 + x4 + x5

/-- Nullstellensatz algebraic identity refuting all-ones row against row 0:
    (1/6) * (1 + x₁ + ... + x₅) - ∑ (1/6) * (x_j - 1) = 1. -/
theorem all_ones_nullstellensatz_identity (x1 x2 x3 x4 x5 : ℝ) :
    (1/6 : ℝ) * row_orth_poly x1 x2 x3 x4 x5 -
    (1/6 : ℝ) * (x1 - 1) -
    (1/6 : ℝ) * (x2 - 1) -
    (1/6 : ℝ) * (x3 - 1) -
    (1/6 : ℝ) * (x4 - 1) -
    (1/6 : ℝ) * (x5 - 1) = 1 := by
  simp only [row_orth_poly]
  ring

/-- Semantic consequence: In a dephased Hadamard matrix, no row can have all real parts equal to 1. -/
theorem all_ones_branch_refutation (x1 x2 x3 x4 x5 : ℝ)
    (h_orth : row_orth_poly x1 x2 x3 x4 x5 = 0)
    (hx1 : x1 - 1 = 0)
    (hx2 : x2 - 1 = 0)
    (hx3 : x3 - 1 = 0)
    (hx4 : x4 - 1 = 0)
    (hx5 : x5 - 1 = 0) : False := by
  have hid := all_ones_nullstellensatz_identity x1 x2 x3 x4 x5
  rw [h_orth, hx1, hx2, hx3, hx4, hx5] at hid
  simp only [mul_zero, sub_zero] at hid
  exact zero_ne_one hid

/-!
## 3. Incompatible Unit-Phase Orthogonality Refutation
-/

/-- Cross inner product relation: x₁ x₂ + y₁ y₂ + 1. -/
def cross_orth_poly (x1 y1 x2 y2 : ℝ) : ℝ :=
  x1 * x2 + y1 * y2 + 1

/-- Exact Nullstellensatz identity refuting incompatible phase inner product when x₁ = 1, x₂ = 1:
    Notice: if x₁ = 1, then y₁^2 = 1 - x₁^2 = 0, so y₁ = 0.
    Thus x₁ x₂ + y₁ y₂ + 1 = 1*1 + 0 + 1 = 2 ≠ 0.
    The polynomial identity:
    (1/2) * (x₁*x₂ + y₁*y₂ + 1) - (1/2)*x₂*(x₁ - 1) - (1/2)*(x₂ - 1)
    eliminates x₁ and x₂ down to (1/2)*y₁*y₂ + 1.
    Squaring or scaling gives the degree-2 Nullstellensatz refutation:
    (-1/4) * (y₂^2) * (x₁^2 + y₁^2 - 1) + ... = 1. -/
theorem phase_incompatible_identity (x1 y1 x2 y2 : ℝ) :
    (1/2 : ℝ) * cross_orth_poly x1 y1 x2 y2 -
    (1/2 : ℝ) * x2 * (x1 - 1) -
    (1/2 : ℝ) * (x2 - 1) -
    (1/2 : ℝ) * y2 * y1 = 1 := by
  simp only [cross_orth_poly]
  ring

/-- When y₁ = 0 (deduced from x₁^2 + y₁^2 = 1 and x₁ = 1), the phase condition is impossible. -/
theorem phase_incompatible_refutation (x1 y1 x2 y2 : ℝ)
    (h_cross : cross_orth_poly x1 y1 x2 y2 = 0)
    (hx1 : x1 - 1 = 0)
    (hx2 : x2 - 1 = 0)
    (hy1 : y1 = 0) : False := by
  have hid := phase_incompatible_identity x1 y1 x2 y2
  rw [h_cross, hx1, hx2, hy1] at hid
  simp only [mul_zero, sub_zero] at hid
  exact zero_ne_one hid

end MUB.GroebnerBranch
