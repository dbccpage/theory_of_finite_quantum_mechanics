/-
  Unified Paper Constants for PO-000 (Appendix B & Theorem 5.1).

  AuthorityEffect: None.

  This module packages the exact numerical constants derived across Appendix B:
    - 1-site first-order derivative factor: 2g
    - 1-site double-commutator factor: 8g²
    - 2-site double-commutator factor: 24g²
    - Product-rule second-derivative bound M: 48g²
    - Taylor remainder constant c₂ = M/2: 24g²
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace PO000.PaperConstants

/-- Unified constants structure for PO-000 under coupling parameter g ≥ 0. -/
structure Constants (g : ℝ) where
  one_site_first   : ℝ := 2 * g
  one_site_second  : ℝ := 8 * (g ^ 2)
  two_site_second  : ℝ := 24 * (g ^ 2)
  max_second_deriv : ℝ := 48 * (g ^ 2)
  taylor_constant  : ℝ := 24 * (g ^ 2)

/-- Canonical paper constants constructor for coupling g. -/
def paper (g : ℝ) : Constants g := {}

/-- Theorem: Product-rule sum (24g² + 8g² + 2*(2g)*(2g) + 8g²) equals max_second_deriv (48g²). -/
theorem product_rule_sum_eq_48 (g : ℝ) :
    24 * (g ^ 2) + 8 * (g ^ 2) + 2 * (2 * g) * (2 * g) + 8 * (g ^ 2) = (paper g).max_second_deriv := by
  dsimp [paper]
  ring

/-- Theorem: Taylor constant c₂ is exactly half of max_second_deriv M. -/
theorem taylor_eq_half_max (g : ℝ) :
    (paper g).taylor_constant = (paper g).max_second_deriv / 2 := by
  dsimp [paper]
  ring

end PO000.PaperConstants

#print axioms PO000.PaperConstants.product_rule_sum_eq_48
#print axioms PO000.PaperConstants.taylor_eq_half_max
