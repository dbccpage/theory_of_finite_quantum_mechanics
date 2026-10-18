/-
  GR002.TopDimensionVanishing

  A declared dimension-indicator fixture.  This is not a construction of a
  simplicial complex or its cochain spaces.

  Theorems:
    1. The declared indicator is zero above its supplied top dimension.

  AuthorityEffect: None.
-/

import Lean.Elab.Tactic.Omega
import Mathlib.Data.Real.Basic

namespace GR002.TopDimensionVanishing

-- This is an indicator, not the dimension of a constructed cochain space.
def num_k_simplices (D : ℕ) (k : ℕ) : ℕ :=
  if k ≤ D then 1 else 0  -- simplified indicator for k-cochains

theorem cochain_dim_zero_above_top (D k : ℕ) (hk : k > D) :
    num_k_simplices D k = 0 := by
  dsimp [num_k_simplices]
  split_ifs with h
  · omega
  · rfl

-- For D = 2 (2-complex), cochain dimension for k = 3 is 0
theorem dim_3_cochains_vanish_on_2_complex :
    num_k_simplices 2 3 = 0 := by
  exact cochain_dim_zero_above_top 2 3 (by norm_num)

#print axioms cochain_dim_zero_above_top
#print axioms dim_3_cochains_vanish_on_2_complex

end GR002.TopDimensionVanishing
