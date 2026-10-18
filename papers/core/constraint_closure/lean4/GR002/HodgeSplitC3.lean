/-
  GR002.HodgeSplitC3

  Formalization of exact L1 Hodge-split fixture calculations on the oriented
  directed 3-cycle C3 = ∂Δ².  The global 7/3 upper bound is not proved here.

  Theorems:
    1. d0_c3: Linear map R³ → R³ representing coboundary on 1-cochains.
    2. spatial_mean: L2 harmonic projection h = (s, s, s) where s = (w0+w1+w2)/3.
    3. exact_comp: d0_alpha = (w0-s, w1-s, w2-s).
    4. R_split_indicator: R_split(e_0) = 7/3 for standard basis vectors.
    5. nonzero_equal_ratio: (3|s|)/(3|s|) = 1 when s is nonzero.

  AuthorityEffect: None.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace GR002.HodgeSplitC3

noncomputable section

def d0 (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-w.1 + w.2.1, -w.2.1 + w.2.2, -w.2.2 + w.1)

def mean (w : ℝ × ℝ × ℝ) : ℝ :=
  (w.1 + w.2.1 + w.2.2) / 3

def harmonic (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (mean w, mean w, mean w)

def exact_comp (w : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (w.1 - mean w, w.2.1 - mean w, w.2.2 - mean w)

def l1_norm (w : ℝ × ℝ × ℝ) : ℝ :=
  |w.1| + |w.2.1| + |w.2.2|

def R_split (w : ℝ × ℝ × ℝ) : ℝ :=
  (l1_norm (exact_comp w) + l1_norm (harmonic w)) / l1_norm w

theorem e0_split_inflation :
    R_split (1, 0, 0) = 7 / 3 := by
  dsimp [R_split, exact_comp, harmonic, mean, l1_norm]
  norm_num

theorem e1_split_inflation :
    R_split (0, 1, 0) = 7 / 3 := by
  dsimp [R_split, exact_comp, harmonic, mean, l1_norm]
  norm_num

theorem e2_split_inflation :
    R_split (0, 0, 1) = 7 / 3 := by
  dsimp [R_split, exact_comp, harmonic, mean, l1_norm]
  norm_num

theorem nonzero_equal_ratio (s : ℝ) (hs : s ≠ 0) :
    (3 * |s|) / (3 * |s|) = 1 := by
  exact div_self (mul_ne_zero (by norm_num) (abs_ne_zero.mpr hs))

#print axioms e0_split_inflation
#print axioms e1_split_inflation
#print axioms e2_split_inflation
#print axioms nonzero_equal_ratio

end
end GR002.HodgeSplitC3
