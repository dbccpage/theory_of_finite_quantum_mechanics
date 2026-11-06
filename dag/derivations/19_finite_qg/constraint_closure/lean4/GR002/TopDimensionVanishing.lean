



import Lean.Elab.Tactic.Omega
import Mathlib.Data.Real.Basic

namespace GR002.TopDimensionVanishing

def num_k_simplices (D : ℕ) (k : ℕ) : ℕ :=
  if k ≤ D then 1 else 0

theorem cochain_dim_zero_above_top (D k : ℕ) (hk : k > D) :
    num_k_simplices D k = 0 := by
  dsimp [num_k_simplices]
  split_ifs with h
  · omega
  · rfl

theorem dim_3_cochains_vanish_on_2_complex :
    num_k_simplices 2 3 = 0 := by
  exact cochain_dim_zero_above_top 2 3 (by norm_num)

#print axioms cochain_dim_zero_above_top
#print axioms dim_3_cochains_vanish_on_2_complex

end GR002.TopDimensionVanishing
