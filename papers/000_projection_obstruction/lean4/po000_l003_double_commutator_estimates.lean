/-
  Formalization of the double-commutator estimates of PO-000 Appendix B
  (the quantitative source of the reduced-state derivative bounds 2g / 8g² / 24g²).

  Paper statements (support counting for a k-local observable A):

    ‖[H, A]‖_∞ ≤ 2 k g ‖A‖_∞

    ‖[H, [H, A]]‖_∞ ≤ 4 k (k + 1) g² ‖A‖_∞

  where g is the full local interaction norm
  (max over vertices of the sum of operator norms of interaction terms
  incident to that vertex).

  Status of this module (AuthorityEffect: None):
  - MECHANIZED-LOCAL.
  - The numerical factors 2k and 4k(k+1) are verified arithmetic.
  - The record `DoubleCommutatorBounds` packages scalar factor nonnegativity arithmetic
    (firstOrderFactor k g * A_norm ≥ 0) rather than operator-norm bounds with actual commutators
    on the left-hand side. The operator-norm / support-expansion argument remains paper-resident.
  - No matrices, no partial traces, no Schatten norms, no continuum.
  - This module feeds factor arithmetic to the `ReducedStateBounds` structure;
    it does **not** upgrade the claim status of Theorem 5.1.

  Relation to companion modules:
  - `po000_l003_second_deriv_bound.lean` consumes the numbers 2g / 8g² / 24g².
  - `po000_l003_short_time_defect_bound.lean` consumes the assembled M ≤ 48 g².
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace PO000.DoubleCommutatorEstimates

/-! ## 1. Numerical factors (pure arithmetic, kernel-checked) -/

/-- First-order factor: 2 k g. -/
def firstOrderFactor (k g : ℝ) : ℝ := 2 * k * g

/-- Second-order (double-commutator) factor: 4 k (k+1) g². -/
def doubleCommutatorFactor (k g : ℝ) : ℝ := 4 * k * (k + 1) * g ^ 2

lemma first_order_k1 (g : ℝ) : firstOrderFactor 1 g = 2 * g := by
  dsimp [firstOrderFactor]
  ring

lemma first_order_k2 (g : ℝ) : firstOrderFactor 2 g = 4 * g := by
  dsimp [firstOrderFactor]
  ring

lemma double_factor_k1 (g : ℝ) : doubleCommutatorFactor 1 g = 8 * g ^ 2 := by
  dsimp [doubleCommutatorFactor]
  ring

lemma double_factor_k2 (g : ℝ) : doubleCommutatorFactor 2 g = 24 * g ^ 2 := by
  dsimp [doubleCommutatorFactor]
  ring

/-! ## 2. Structured hypothesis record for scalar factor nonnegativity and arithmetic
Note: DoubleCommutatorBounds packages scalar multiplier nonnegativity (factor * A_norm ≥ 0)
rather than actual operator commutator norm bounds (‖[H, A]‖ ≤ ...).
-/

structure DoubleCommutatorBounds (k : ℕ) (g : ℝ) where
  hg : 0 ≤ g
  first_bound :
    ∀ (A_norm : ℝ), 0 ≤ A_norm →
      firstOrderFactor k g * A_norm ≥ 0
  double_bound :
    ∀ (A_norm : ℝ), 0 ≤ A_norm →
      doubleCommutatorFactor k g * A_norm ≥ 0

/-- Concrete instance for the paper’s k=1 (one-site) bounds. -/
def oneSiteBounds (g : ℝ) (hg : 0 ≤ g) : DoubleCommutatorBounds 1 g where
  hg := hg
  first_bound := fun A_norm _hA => by
    dsimp [firstOrderFactor]
    positivity
  double_bound := fun A_norm _hA => by
    dsimp [doubleCommutatorFactor]
    positivity

/-- Concrete instance for the paper’s k=2 (two-site) bounds. -/
def twoSiteBounds (g : ℝ) (hg : 0 ≤ g) : DoubleCommutatorBounds 2 g where
  hg := hg
  first_bound := fun A_norm _hA => by
    dsimp [firstOrderFactor]
    positivity
  double_bound := fun A_norm _hA => by
    dsimp [doubleCommutatorFactor]
    positivity

/-! ## 3. Link from double-commutator factors to reduced-state derivative bounds -/

theorem second_deriv_from_double_factor
    (k : ℕ) (g : ℝ) (_hg : 0 ≤ g)
    (_B : DoubleCommutatorBounds k g)
    :
    doubleCommutatorFactor k g = 4 * k * (k + 1) * g ^ 2 := by
  rfl

lemma one_site_second_from_double (g : ℝ) (_hg : 0 ≤ g) :
    doubleCommutatorFactor 1 g = 8 * g ^ 2 :=
  double_factor_k1 g

lemma two_site_second_from_double (g : ℝ) (_hg : 0 ≤ g) :
    doubleCommutatorFactor 2 g = 24 * g ^ 2 :=
  double_factor_k2 g

lemma one_site_first_from_double (g : ℝ) :
    firstOrderFactor 1 g = 2 * g :=
  first_order_k1 g

/-! ## 4. Abstract support-counting justification (combinatorial core) -/

theorem first_order_counting_origin (k : ℕ) (g : ℝ) (_hg : 0 ≤ g) :
    firstOrderFactor k g = 2 * k * g := by
  rfl

theorem double_factor_counting_origin (k : ℕ) (g : ℝ) (_hg : 0 ≤ g) :
    doubleCommutatorFactor k g = 4 * k * (k + 1) * g ^ 2 := by
  rfl

/-! ## 5. Axiom audit -/

#print axioms first_order_k1
#print axioms double_factor_k1
#print axioms double_factor_k2
#print axioms one_site_second_from_double
#print axioms two_site_second_from_double

end PO000.DoubleCommutatorEstimates
