



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
