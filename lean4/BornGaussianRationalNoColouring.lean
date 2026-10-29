import BornGaussianRationalFrameObstruction

/-!
# No two-valued frame function on all Gaussian-rational rays

AuthorityEffect: None.

The finite obstruction uses primitive real integer rays in [-2,2]^3. Orthogonal
pairs are completed by their integer cross products; the completing ray need
not belong to the box. This distinction is essential: internal triples alone
are colourable. All constraints below are proved from `IsFrameFunction`, and
the finite binary case split is replayed by Lean linear arithmetic.

This settles only the {0,1}-valued variant, not quadratic rigidity for arbitrary
signed or nonnegative rational-valued frame functions.
-/

namespace BornFinite.GaussianFrames.NoColouring

open BornFinite.GaussianFrames

private theorem binary_nonneg {f : GVec → ℚ}
    (hB : ∀ v, v.NonZero → f v = 0 ∨ f v = 1)
    {v : GVec} (hv : v.NonZero) : 0 ≤ f v := by
  rcases hB v hv with h | h <;> rw [h] <;> norm_num

private theorem orthogonal_pair_bound {f : GVec → ℚ}
    (hF : IsFrameFunction f)
    (hB : ∀ v, v.NonZero → f v = 0 ∨ f v = 1)
    {u v w : GVec} (h : IsFrame u v w) : f u + f v ≤ 1 := by
  have hn := binary_nonneg hB h.2.2.1
  have hs := hF u v w h
  linarith

set_option maxHeartbeats 4000000 in
/-- No function on nonzero `ℚ(i)³` vectors is both a frame function and {0,1}-valued.
Every vector used in this proof is real, so the same finite obstruction applies to `ℚ³`. -/
theorem no_zero_one_frame_function (f : GVec → ℚ) (hF : IsFrameFunction f)
    (hB : ∀ v, v.NonZero → f v = 0 ∨ f v = 1) : False := by
  have n0 : 0 ≤ f (gv 0 0 0 0 1 0) := binary_nonneg hB (nonZero_of_z (by norm_num [gv]))
  have n1 : 0 ≤ f (gv 0 0 1 0 (-2) 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n2 : 0 ≤ f (gv 0 0 1 0 (-1) 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n3 : 0 ≤ f (gv 0 0 1 0 0 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n4 : 0 ≤ f (gv 0 0 1 0 1 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n5 : 0 ≤ f (gv 0 0 1 0 2 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n6 : 0 ≤ f (gv 0 0 2 0 (-1) 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n7 : 0 ≤ f (gv 0 0 2 0 1 0) := binary_nonneg hB (nonZero_of_y (by norm_num [gv]))
  have n8 : 0 ≤ f (gv 1 0 (-2) 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n9 : 0 ≤ f (gv 1 0 (-2) 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n10 : 0 ≤ f (gv 1 0 (-2) 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n11 : 0 ≤ f (gv 1 0 (-2) 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n12 : 0 ≤ f (gv 1 0 (-2) 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n13 : 0 ≤ f (gv 1 0 (-1) 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n14 : 0 ≤ f (gv 1 0 (-1) 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n15 : 0 ≤ f (gv 1 0 (-1) 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n16 : 0 ≤ f (gv 1 0 (-1) 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n17 : 0 ≤ f (gv 1 0 (-1) 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n18 : 0 ≤ f (gv 1 0 0 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n19 : 0 ≤ f (gv 1 0 0 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n20 : 0 ≤ f (gv 1 0 0 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n21 : 0 ≤ f (gv 1 0 0 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n22 : 0 ≤ f (gv 1 0 0 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n23 : 0 ≤ f (gv 1 0 1 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n24 : 0 ≤ f (gv 1 0 1 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n25 : 0 ≤ f (gv 1 0 1 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n26 : 0 ≤ f (gv 1 0 1 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n27 : 0 ≤ f (gv 1 0 1 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n28 : 0 ≤ f (gv 1 0 2 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n29 : 0 ≤ f (gv 1 0 2 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n30 : 0 ≤ f (gv 1 0 2 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n31 : 0 ≤ f (gv 1 0 2 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n32 : 0 ≤ f (gv 1 0 2 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n33 : 0 ≤ f (gv 2 0 (-2) 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n34 : 0 ≤ f (gv 2 0 (-2) 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n35 : 0 ≤ f (gv 2 0 (-1) 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n36 : 0 ≤ f (gv 2 0 (-1) 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n37 : 0 ≤ f (gv 2 0 (-1) 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n38 : 0 ≤ f (gv 2 0 (-1) 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n39 : 0 ≤ f (gv 2 0 (-1) 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n40 : 0 ≤ f (gv 2 0 0 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n41 : 0 ≤ f (gv 2 0 0 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n42 : 0 ≤ f (gv 2 0 1 0 (-2) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n43 : 0 ≤ f (gv 2 0 1 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n44 : 0 ≤ f (gv 2 0 1 0 0 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n45 : 0 ≤ f (gv 2 0 1 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n46 : 0 ≤ f (gv 2 0 1 0 2 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n47 : 0 ≤ f (gv 2 0 2 0 (-1) 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have n48 : 0 ≤ f (gv 2 0 2 0 1 0) := binary_nonneg hB (nonZero_of_x (by norm_num [gv]))
  have p_0_3 : f (gv 0 0 0 0 1 0) + f (gv 0 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 0 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_10 : f (gv 0 0 0 0 1 0) + f (gv 1 0 (-2) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 1 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_15 : f (gv 0 0 0 0 1 0) + f (gv 1 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 1 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_20 : f (gv 0 0 0 0 1 0) + f (gv 1 0 0 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 1 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_25 : f (gv 0 0 0 0 1 0) + f (gv 1 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 1 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_30 : f (gv 0 0 0 0 1 0) + f (gv 1 0 2 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 1 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_37 : f (gv 0 0 0 0 1 0) + f (gv 2 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 2 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_0_44 : f (gv 0 0 0 0 1 0) + f (gv 2 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 2 0 0 0)) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_1_9 : f (gv 0 0 1 0 (-2) 0) + f (gv 1 0 (-2) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-5) 0 (-2) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_1_31 : f (gv 0 0 1 0 (-2) 0) + f (gv 1 0 2 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 5 0 (-2) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_1_33 : f (gv 0 0 1 0 (-2) 0) + f (gv 2 0 (-2) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-5) 0 (-4) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_1_48 : f (gv 0 0 1 0 (-2) 0) + f (gv 2 0 2 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 5 0 (-4) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_4 : f (gv 0 0 1 0 (-1) 0) + f (gv 0 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 0 0 0 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_8 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 (-2) 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 (-1) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_14 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 (-1) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-1) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_20 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 0 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 (-1) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_26 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-1) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_32 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 2 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 (-1) 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_36 : f (gv 0 0 1 0 (-1) 0) + f (gv 2 0 (-1) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-2) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_2_45 : f (gv 0 0 1 0 (-1) 0) + f (gv 2 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-2) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_18 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 0 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_19 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 0 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_20 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 0 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_21 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 0 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_22 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 0 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_40 : f (gv 0 0 1 0 0 0) + f (gv 2 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 0 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_3_41 : f (gv 0 0 1 0 0 0) + f (gv 2 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 0 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_4_12 : f (gv 0 0 1 0 1 0) + f (gv 1 0 (-2) 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 1 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_4_28 : f (gv 0 0 1 0 1 0) + f (gv 1 0 2 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 1 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_5_11 : f (gv 0 0 1 0 2 0) + f (gv 1 0 (-2) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 5 0 2 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_5_29 : f (gv 0 0 1 0 2 0) + f (gv 1 0 2 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-5) 0 2 0 (-1) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_6_13 : f (gv 0 0 2 0 (-1) 0) + f (gv 1 0 (-1) 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-5) 0 (-1) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_6_27 : f (gv 0 0 2 0 (-1) 0) + f (gv 1 0 1 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 5 0 (-1) 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_7_17 : f (gv 0 0 2 0 1 0) + f (gv 1 0 (-1) 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 5 0 1 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_7_23 : f (gv 0 0 2 0 1 0) + f (gv 1 0 1 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-5) 0 1 0 (-2) 0)) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_8_41 : f (gv 1 0 (-2) 0 (-2) 0) + f (gv 2 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-5) 0 4 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_8_44 : f (gv 1 0 (-2) 0 (-2) 0) + f (gv 2 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-4) 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_9_44 : f (gv 1 0 (-2) 0 (-1) 0) + f (gv 2 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 (-2) 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_10_42 : f (gv 1 0 (-2) 0 0 0) + f (gv 2 0 1 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 2 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_10_43 : f (gv 1 0 (-2) 0 0 0) + f (gv 2 0 1 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 1 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_10_45 : f (gv 1 0 (-2) 0 0 0) + f (gv 2 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-1) 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_10_46 : f (gv 1 0 (-2) 0 0 0) + f (gv 2 0 1 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 (-2) 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_11_44 : f (gv 1 0 (-2) 0 1 0) + f (gv 2 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 2 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_12_40 : f (gv 1 0 (-2) 0 2 0) + f (gv 2 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 5 0 4 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_12_44 : f (gv 1 0 (-2) 0 2 0) + f (gv 2 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 4 0 5 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_13_41 : f (gv 1 0 (-1) 0 (-2) 0) + f (gv 2 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 (-5) 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_14_45 : f (gv 1 0 (-1) 0 (-1) 0) + f (gv 2 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 (-3) 0 3 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_23 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 2 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_24 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 1 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_25 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 0 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_z (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_26 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 (-1) 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_27 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-2) 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_47 : f (gv 1 0 (-1) 0 0 0) + f (gv 2 0 2 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 1 0 4 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_15_48 : f (gv 1 0 (-1) 0 0 0) + f (gv 2 0 2 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 (-1) 0 4 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_16_43 : f (gv 1 0 (-1) 0 1 0) + f (gv 2 0 1 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 3 0 3 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_17_40 : f (gv 1 0 (-1) 0 2 0) + f (gv 2 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 5 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_18_34 : f (gv 1 0 0 0 (-2) 0) + f (gv 2 0 (-2) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 (-5) 0 (-2) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_18_38 : f (gv 1 0 0 0 (-2) 0) + f (gv 2 0 (-1) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-5) 0 (-1) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_18_45 : f (gv 1 0 0 0 (-2) 0) + f (gv 2 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-5) 0 1 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_18_48 : f (gv 1 0 0 0 (-2) 0) + f (gv 2 0 2 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 (-5) 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_19_26 : f (gv 1 0 0 0 (-1) 0) + f (gv 1 0 1 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 (-2) 0 1 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_21_24 : f (gv 1 0 0 0 1 0) + f (gv 1 0 1 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 2 0 1 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_22_33 : f (gv 1 0 0 0 2 0) + f (gv 2 0 (-2) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 5 0 (-2) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_22_36 : f (gv 1 0 0 0 2 0) + f (gv 2 0 (-1) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 5 0 (-1) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_22_43 : f (gv 1 0 0 0 2 0) + f (gv 2 0 1 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 5 0 1 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_22_47 : f (gv 1 0 0 0 2 0) + f (gv 2 0 2 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 5 0 2 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_23_41 : f (gv 1 0 1 0 (-2) 0) + f (gv 2 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 (-5) 0 (-2) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_24_38 : f (gv 1 0 1 0 (-1) 0) + f (gv 2 0 (-1) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 (-3) 0 (-3) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_25_33 : f (gv 1 0 1 0 0 0) + f (gv 2 0 (-2) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 1 0 (-4) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_25_34 : f (gv 1 0 1 0 0 0) + f (gv 2 0 (-2) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 (-1) 0 (-4) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_26_36 : f (gv 1 0 1 0 1 0) + f (gv 2 0 (-1) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 0 0 3 0 (-3) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_27_40 : f (gv 1 0 1 0 2 0) + f (gv 2 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 5 0 (-2) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_28_37 : f (gv 1 0 2 0 (-2) 0) + f (gv 2 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 (-4) 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_28_41 : f (gv 1 0 2 0 (-2) 0) + f (gv 2 0 0 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-5) 0 (-4) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_29_37 : f (gv 1 0 2 0 (-1) 0) + f (gv 2 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-1) 0 (-2) 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_30_35 : f (gv 1 0 2 0 0 0) + f (gv 2 0 (-1) 0 (-2) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-4) 0 2 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_30_36 : f (gv 1 0 2 0 0 0) + f (gv 2 0 (-1) 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 1 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_30_38 : f (gv 1 0 2 0 0 0) + f (gv 2 0 (-1) 0 1 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 (-1) 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_30_39 : f (gv 1 0 2 0 0 0) + f (gv 2 0 (-1) 0 2 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 4 0 (-2) 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_31_37 : f (gv 1 0 2 0 1 0) + f (gv 2 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 1 0 2 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_32_37 : f (gv 1 0 2 0 2 0) + f (gv 2 0 (-1) 0 0 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv 2 0 4 0 (-5) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have p_32_40 : f (gv 1 0 2 0 2 0) + f (gv 2 0 0 0 (-1) 0) ≤ 1 :=
    orthogonal_pair_bound hF hB (w := (gv (-2) 0 5 0 (-4) 0)) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_0_3_20 : f (gv 0 0 0 0 1 0) + f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 0 0) = 1 :=
    hF (gv 0 0 0 0 1 0) (gv 0 0 1 0 0 0) (gv 1 0 0 0 0 0) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_0_10_44 : f (gv 0 0 0 0 1 0) + f (gv 1 0 (-2) 0 0 0) + f (gv 2 0 1 0 0 0) = 1 :=
    hF (gv 0 0 0 0 1 0) (gv 1 0 (-2) 0 0 0) (gv 2 0 1 0 0 0) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_0_15_25 : f (gv 0 0 0 0 1 0) + f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 0 0) = 1 :=
    hF (gv 0 0 0 0 1 0) (gv 1 0 (-1) 0 0 0) (gv 1 0 1 0 0 0) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_0_30_37 : f (gv 0 0 0 0 1 0) + f (gv 1 0 2 0 0 0) + f (gv 2 0 (-1) 0 0 0) = 1 :=
    hF (gv 0 0 0 0 1 0) (gv 1 0 2 0 0 0) (gv 2 0 (-1) 0 0 0) (⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_1_7_20 : f (gv 0 0 1 0 (-2) 0) + f (gv 0 0 2 0 1 0) + f (gv 1 0 0 0 0 0) = 1 :=
    hF (gv 0 0 1 0 (-2) 0) (gv 0 0 2 0 1 0) (gv 1 0 0 0 0 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_2_4_20 : f (gv 0 0 1 0 (-1) 0) + f (gv 0 0 1 0 1 0) + f (gv 1 0 0 0 0 0) = 1 :=
    hF (gv 0 0 1 0 (-1) 0) (gv 0 0 1 0 1 0) (gv 1 0 0 0 0 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_2_14_45 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 (-1) 0 (-1) 0) + f (gv 2 0 1 0 1 0) = 1 :=
    hF (gv 0 0 1 0 (-1) 0) (gv 1 0 (-1) 0 (-1) 0) (gv 2 0 1 0 1 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_2_26_36 : f (gv 0 0 1 0 (-1) 0) + f (gv 1 0 1 0 1 0) + f (gv 2 0 (-1) 0 (-1) 0) = 1 :=
    hF (gv 0 0 1 0 (-1) 0) (gv 1 0 1 0 1 0) (gv 2 0 (-1) 0 (-1) 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_3_18_41 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 (-2) 0) + f (gv 2 0 0 0 1 0) = 1 :=
    hF (gv 0 0 1 0 0 0) (gv 1 0 0 0 (-2) 0) (gv 2 0 0 0 1 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_3_19_21 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 (-1) 0) + f (gv 1 0 0 0 1 0) = 1 :=
    hF (gv 0 0 1 0 0 0) (gv 1 0 0 0 (-1) 0) (gv 1 0 0 0 1 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_3_22_40 : f (gv 0 0 1 0 0 0) + f (gv 1 0 0 0 2 0) + f (gv 2 0 0 0 (-1) 0) = 1 :=
    hF (gv 0 0 1 0 0 0) (gv 1 0 0 0 2 0) (gv 2 0 0 0 (-1) 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_4_16_43 : f (gv 0 0 1 0 1 0) + f (gv 1 0 (-1) 0 1 0) + f (gv 2 0 1 0 (-1) 0) = 1 :=
    hF (gv 0 0 1 0 1 0) (gv 1 0 (-1) 0 1 0) (gv 2 0 1 0 (-1) 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_4_24_38 : f (gv 0 0 1 0 1 0) + f (gv 1 0 1 0 (-1) 0) + f (gv 2 0 (-1) 0 1 0) = 1 :=
    hF (gv 0 0 1 0 1 0) (gv 1 0 1 0 (-1) 0) (gv 2 0 (-1) 0 1 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_5_6_20 : f (gv 0 0 1 0 2 0) + f (gv 0 0 2 0 (-1) 0) + f (gv 1 0 0 0 0 0) = 1 :=
    hF (gv 0 0 1 0 2 0) (gv 0 0 2 0 (-1) 0) (gv 1 0 0 0 0 0) (⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_8_39_47 : f (gv 1 0 (-2) 0 (-2) 0) + f (gv 2 0 (-1) 0 2 0) + f (gv 2 0 2 0 (-1) 0) = 1 :=
    hF (gv 1 0 (-2) 0 (-2) 0) (gv 2 0 (-1) 0 2 0) (gv 2 0 2 0 (-1) 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_9_21_24 : f (gv 1 0 (-2) 0 (-1) 0) + f (gv 1 0 0 0 1 0) + f (gv 1 0 1 0 (-1) 0) = 1 :=
    hF (gv 1 0 (-2) 0 (-1) 0) (gv 1 0 0 0 1 0) (gv 1 0 1 0 (-1) 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_11_19_26 : f (gv 1 0 (-2) 0 1 0) + f (gv 1 0 0 0 (-1) 0) + f (gv 1 0 1 0 1 0) = 1 :=
    hF (gv 1 0 (-2) 0 1 0) (gv 1 0 0 0 (-1) 0) (gv 1 0 1 0 1 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_12_35_48 : f (gv 1 0 (-2) 0 2 0) + f (gv 2 0 (-1) 0 (-2) 0) + f (gv 2 0 2 0 1 0) = 1 :=
    hF (gv 1 0 (-2) 0 2 0) (gv 2 0 (-1) 0 (-2) 0) (gv 2 0 2 0 1 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_13_16_25 : f (gv 1 0 (-1) 0 (-2) 0) + f (gv 1 0 (-1) 0 1 0) + f (gv 1 0 1 0 0 0) = 1 :=
    hF (gv 1 0 (-1) 0 (-2) 0) (gv 1 0 (-1) 0 1 0) (gv 1 0 1 0 0 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_14_17_25 : f (gv 1 0 (-1) 0 (-1) 0) + f (gv 1 0 (-1) 0 2 0) + f (gv 1 0 1 0 0 0) = 1 :=
    hF (gv 1 0 (-1) 0 (-1) 0) (gv 1 0 (-1) 0 2 0) (gv 1 0 1 0 0 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_14_21_29 : f (gv 1 0 (-1) 0 (-1) 0) + f (gv 1 0 0 0 1 0) + f (gv 1 0 2 0 (-1) 0) = 1 :=
    hF (gv 1 0 (-1) 0 (-1) 0) (gv 1 0 0 0 1 0) (gv 1 0 2 0 (-1) 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_15_23_26 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 (-2) 0) + f (gv 1 0 1 0 1 0) = 1 :=
    hF (gv 1 0 (-1) 0 0 0) (gv 1 0 1 0 (-2) 0) (gv 1 0 1 0 1 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_15_24_27 : f (gv 1 0 (-1) 0 0 0) + f (gv 1 0 1 0 (-1) 0) + f (gv 1 0 1 0 2 0) = 1 :=
    hF (gv 1 0 (-1) 0 0 0) (gv 1 0 1 0 (-1) 0) (gv 1 0 1 0 2 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_16_19_31 : f (gv 1 0 (-1) 0 1 0) + f (gv 1 0 0 0 (-1) 0) + f (gv 1 0 2 0 1 0) = 1 :=
    hF (gv 1 0 (-1) 0 1 0) (gv 1 0 0 0 (-1) 0) (gv 1 0 2 0 1 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_28_33_46 : f (gv 1 0 2 0 (-2) 0) + f (gv 2 0 (-2) 0 (-1) 0) + f (gv 2 0 1 0 2 0) = 1 :=
    hF (gv 1 0 2 0 (-2) 0) (gv 2 0 (-2) 0 (-1) 0) (gv 2 0 1 0 2 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t_32_34_42 : f (gv 1 0 2 0 2 0) + f (gv 2 0 (-2) 0 1 0) + f (gv 2 0 1 0 (-2) 0) = 1 :=
    hF (gv 1 0 2 0 2 0) (gv 2 0 (-2) 0 1 0) (gv 2 0 1 0 (-2) 0) (⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  rcases hB (gv 0 0 0 0 1 0) (nonZero_of_z (by norm_num [gv])) with a0 | a0
  ·
    rcases hB (gv 0 0 1 0 (-1) 0) (nonZero_of_y (by norm_num [gv])) with a2 | a2
    ·
      rcases hB (gv 0 0 1 0 0 0) (nonZero_of_y (by norm_num [gv])) with a3 | a3
      ·
        have a20 : f (gv 1 0 0 0 0 0) = 1 := by linarith only [t_0_3_20, a0, a3, n20]
        have a1 : f (gv 0 0 1 0 (-2) 0) = 0 := by linarith only [t_1_7_20, n7, a20, n1]
        have a7 : f (gv 0 0 2 0 1 0) = 0 := by linarith only [t_1_7_20, a1, a20, n7]
        have a4 : f (gv 0 0 1 0 1 0) = 0 := by linarith only [t_2_4_20, a2, a20, n4]
        have a5 : f (gv 0 0 1 0 2 0) = 0 := by linarith only [t_5_6_20, n6, a20, n5]
        have a6 : f (gv 0 0 2 0 (-1) 0) = 0 := by linarith only [t_5_6_20, a5, a20, n6]
        rcases hB (gv 1 0 (-1) 0 0 0) (nonZero_of_x (by norm_num [gv])) with a15 | a15
        ·
          have a25 : f (gv 1 0 1 0 0 0) = 1 := by linarith only [t_0_15_25, a0, a15, n25]
          have a13 : f (gv 1 0 (-1) 0 (-2) 0) = 0 := by linarith only [t_13_16_25, n16, a25, n13]
          have a16 : f (gv 1 0 (-1) 0 1 0) = 0 := by linarith only [t_13_16_25, a13, a25, n16]
          have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 0 := by linarith only [t_14_17_25, n17, a25, n14]
          have a17 : f (gv 1 0 (-1) 0 2 0) = 0 := by linarith only [t_14_17_25, a14, a25, n17]
          have a33 : f (gv 2 0 (-2) 0 (-1) 0) = 0 := by linarith only [p_25_33, a25, n33]
          have a34 : f (gv 2 0 (-2) 0 1 0) = 0 := by linarith only [p_25_34, a25, n34]
          have a45 : f (gv 2 0 1 0 1 0) = 1 := by linarith only [t_2_14_45, a2, a14, n45]
          have a43 : f (gv 2 0 1 0 (-1) 0) = 1 := by linarith only [t_4_16_43, a4, a16, n43]
          have a10 : f (gv 1 0 (-2) 0 0 0) = 0 := by linarith only [p_10_45, a45, n10]
          have a18 : f (gv 1 0 0 0 (-2) 0) = 0 := by linarith only [p_18_45, a45, n18]
          have a22 : f (gv 1 0 0 0 2 0) = 0 := by linarith only [p_22_43, a43, n22]
          have a44 : f (gv 2 0 1 0 0 0) = 1 := by linarith only [t_0_10_44, a0, a10, n44]
          have a41 : f (gv 2 0 0 0 1 0) = 1 := by linarith only [t_3_18_41, a3, a18, n41]
          have a40 : f (gv 2 0 0 0 (-1) 0) = 1 := by linarith only [t_3_22_40, a3, a22, n40]
          have a8 : f (gv 1 0 (-2) 0 (-2) 0) = 0 := by linarith only [p_8_44, a44, n8]
          have a9 : f (gv 1 0 (-2) 0 (-1) 0) = 0 := by linarith only [p_9_44, a44, n9]
          have a11 : f (gv 1 0 (-2) 0 1 0) = 0 := by linarith only [p_11_44, a44, n11]
          have a12 : f (gv 1 0 (-2) 0 2 0) = 0 := by linarith only [p_12_44, a44, n12]
          have a23 : f (gv 1 0 1 0 (-2) 0) = 0 := by linarith only [p_23_41, a41, n23]
          have a28 : f (gv 1 0 2 0 (-2) 0) = 0 := by linarith only [p_28_41, a41, n28]
          have a27 : f (gv 1 0 1 0 2 0) = 0 := by linarith only [p_27_40, a40, n27]
          have a32 : f (gv 1 0 2 0 2 0) = 0 := by linarith only [p_32_40, a40, n32]
          have a26 : f (gv 1 0 1 0 1 0) = 1 := by linarith only [t_15_23_26, a15, a23, n26]
          have a24 : f (gv 1 0 1 0 (-1) 0) = 1 := by linarith only [t_15_24_27, a15, a27, n24]
          have a46 : f (gv 2 0 1 0 2 0) = 1 := by linarith only [t_28_33_46, a28, a33, n46]
          have a42 : f (gv 2 0 1 0 (-2) 0) = 1 := by linarith only [t_32_34_42, a32, a34, n42]
          have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [p_19_26, a26, n19]
          have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_26_36, a26, n36]
          have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [p_21_24, a24, n21]
          have a38 : f (gv 2 0 (-1) 0 1 0) = 0 := by linarith only [p_24_38, a24, n38]
          linarith only [t_3_19_21, a3, a19, a21]
        ·
          have a23 : f (gv 1 0 1 0 (-2) 0) = 0 := by linarith only [p_15_23, a15, n23]
          have a24 : f (gv 1 0 1 0 (-1) 0) = 0 := by linarith only [p_15_24, a15, n24]
          have a25 : f (gv 1 0 1 0 0 0) = 0 := by linarith only [p_15_25, a15, n25]
          have a26 : f (gv 1 0 1 0 1 0) = 0 := by linarith only [p_15_26, a15, n26]
          have a27 : f (gv 1 0 1 0 2 0) = 0 := by linarith only [p_15_27, a15, n27]
          have a47 : f (gv 2 0 2 0 (-1) 0) = 0 := by linarith only [p_15_47, a15, n47]
          have a48 : f (gv 2 0 2 0 1 0) = 0 := by linarith only [p_15_48, a15, n48]
          have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 1 := by linarith only [t_2_26_36, a2, a26, n36]
          have a38 : f (gv 2 0 (-1) 0 1 0) = 1 := by linarith only [t_4_24_38, a4, a24, n38]
          have a22 : f (gv 1 0 0 0 2 0) = 0 := by linarith only [p_22_36, a36, n22]
          have a30 : f (gv 1 0 2 0 0 0) = 0 := by linarith only [p_30_36, a36, n30]
          have a18 : f (gv 1 0 0 0 (-2) 0) = 0 := by linarith only [p_18_38, a38, n18]
          have a37 : f (gv 2 0 (-1) 0 0 0) = 1 := by linarith only [t_0_30_37, a0, a30, n37]
          have a41 : f (gv 2 0 0 0 1 0) = 1 := by linarith only [t_3_18_41, a3, a18, n41]
          have a40 : f (gv 2 0 0 0 (-1) 0) = 1 := by linarith only [t_3_22_40, a3, a22, n40]
          have a28 : f (gv 1 0 2 0 (-2) 0) = 0 := by linarith only [p_28_37, a37, n28]
          have a29 : f (gv 1 0 2 0 (-1) 0) = 0 := by linarith only [p_29_37, a37, n29]
          have a31 : f (gv 1 0 2 0 1 0) = 0 := by linarith only [p_31_37, a37, n31]
          have a32 : f (gv 1 0 2 0 2 0) = 0 := by linarith only [p_32_37, a37, n32]
          have a8 : f (gv 1 0 (-2) 0 (-2) 0) = 0 := by linarith only [p_8_41, a41, n8]
          have a13 : f (gv 1 0 (-1) 0 (-2) 0) = 0 := by linarith only [p_13_41, a41, n13]
          have a12 : f (gv 1 0 (-2) 0 2 0) = 0 := by linarith only [p_12_40, a40, n12]
          have a17 : f (gv 1 0 (-1) 0 2 0) = 0 := by linarith only [p_17_40, a40, n17]
          have a39 : f (gv 2 0 (-1) 0 2 0) = 1 := by linarith only [t_8_39_47, a8, a47, n39]
          have a35 : f (gv 2 0 (-1) 0 (-2) 0) = 1 := by linarith only [t_12_35_48, a12, a48, n35]
          have a16 : f (gv 1 0 (-1) 0 1 0) = 1 := by linarith only [t_13_16_25, a13, a25, n16]
          have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 1 := by linarith only [t_14_17_25, a17, a25, n14]
          have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [t_14_21_29, a14, a29, n21]
          have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [t_16_19_31, a16, a31, n19]
          have a43 : f (gv 2 0 1 0 (-1) 0) = 0 := by linarith only [p_16_43, a16, n43]
          have a45 : f (gv 2 0 1 0 1 0) = 0 := by linarith only [p_14_45, a14, n45]
          linarith only [t_3_19_21, a3, a19, a21]
      ·
        have a18 : f (gv 1 0 0 0 (-2) 0) = 0 := by linarith only [p_3_18, a3, n18]
        have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [p_3_19, a3, n19]
        have a20 : f (gv 1 0 0 0 0 0) = 0 := by linarith only [p_3_20, a3, n20]
        have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [p_3_21, a3, n21]
        have a22 : f (gv 1 0 0 0 2 0) = 0 := by linarith only [p_3_22, a3, n22]
        have a40 : f (gv 2 0 0 0 (-1) 0) = 0 := by linarith only [p_3_40, a3, n40]
        have a41 : f (gv 2 0 0 0 1 0) = 0 := by linarith only [p_3_41, a3, n41]
        have a4 : f (gv 0 0 1 0 1 0) = 1 := by linarith only [t_2_4_20, a2, a20, n4]
        have a16 : f (gv 1 0 (-1) 0 1 0) = 0 := by linarith only [t_4_16_43, a4, n43, n16]
        have a43 : f (gv 2 0 1 0 (-1) 0) = 0 := by linarith only [t_4_16_43, a4, a16, n43]
        have a24 : f (gv 1 0 1 0 (-1) 0) = 0 := by linarith only [t_4_24_38, a4, n38, n24]
        have a38 : f (gv 2 0 (-1) 0 1 0) = 0 := by linarith only [t_4_24_38, a4, a24, n38]
        have a9 : f (gv 1 0 (-2) 0 (-1) 0) = 1 := by linarith only [t_9_21_24, a21, a24, n9]
        have a31 : f (gv 1 0 2 0 1 0) = 1 := by linarith only [t_16_19_31, a16, a19, n31]
        have a12 : f (gv 1 0 (-2) 0 2 0) = 0 := by linarith only [p_4_12, a4, n12]
        have a28 : f (gv 1 0 2 0 (-2) 0) = 0 := by linarith only [p_4_28, a4, n28]
        have a1 : f (gv 0 0 1 0 (-2) 0) = 0 := by linarith only [p_1_9, a9, n1]
        have a44 : f (gv 2 0 1 0 0 0) = 0 := by linarith only [p_9_44, a9, n44]
        have a37 : f (gv 2 0 (-1) 0 0 0) = 0 := by linarith only [p_31_37, a31, n37]
        have a10 : f (gv 1 0 (-2) 0 0 0) = 1 := by linarith only [t_0_10_44, a0, a44, n10]
        have a30 : f (gv 1 0 2 0 0 0) = 1 := by linarith only [t_0_30_37, a0, a37, n30]
        have a7 : f (gv 0 0 2 0 1 0) = 1 := by linarith only [t_1_7_20, a1, a20, n7]
        have a42 : f (gv 2 0 1 0 (-2) 0) = 0 := by linarith only [p_10_42, a10, n42]
        have a45 : f (gv 2 0 1 0 1 0) = 0 := by linarith only [p_10_45, a10, n45]
        have a46 : f (gv 2 0 1 0 2 0) = 0 := by linarith only [p_10_46, a10, n46]
        have a35 : f (gv 2 0 (-1) 0 (-2) 0) = 0 := by linarith only [p_30_35, a30, n35]
        have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_30_36, a30, n36]
        have a39 : f (gv 2 0 (-1) 0 2 0) = 0 := by linarith only [p_30_39, a30, n39]
        have a17 : f (gv 1 0 (-1) 0 2 0) = 0 := by linarith only [p_7_17, a7, n17]
        have a23 : f (gv 1 0 1 0 (-2) 0) = 0 := by linarith only [p_7_23, a7, n23]
        have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 1 := by linarith only [t_2_14_45, a2, a45, n14]
        have a26 : f (gv 1 0 1 0 1 0) = 1 := by linarith only [t_2_26_36, a2, a36, n26]
        have a11 : f (gv 1 0 (-2) 0 1 0) = 0 := by linarith only [t_11_19_26, a19, a26, n11]
        have a48 : f (gv 2 0 2 0 1 0) = 1 := by linarith only [t_12_35_48, a12, a35, n48]
        have a25 : f (gv 1 0 1 0 0 0) = 0 := by linarith only [t_14_17_25, a14, a17, n25]
        have a29 : f (gv 1 0 2 0 (-1) 0) = 0 := by linarith only [t_14_21_29, a14, a21, n29]
        have a15 : f (gv 1 0 (-1) 0 0 0) = 0 := by linarith only [t_15_23_26, a23, a26, n15]
        have a27 : f (gv 1 0 1 0 2 0) = 1 := by linarith only [t_15_24_27, a15, a24, n27]
        have a33 : f (gv 2 0 (-2) 0 (-1) 0) = 1 := by linarith only [t_28_33_46, a28, a46, n33]
        have a6 : f (gv 0 0 2 0 (-1) 0) = 0 := by linarith only [p_6_27, a27, n6]
        linarith only [t_0_15_25, a0, a15, a25]
    ·
      have a4 : f (gv 0 0 1 0 1 0) = 0 := by linarith only [p_2_4, a2, n4]
      have a8 : f (gv 1 0 (-2) 0 (-2) 0) = 0 := by linarith only [p_2_8, a2, n8]
      have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_2_14, a2, n14]
      have a20 : f (gv 1 0 0 0 0 0) = 0 := by linarith only [p_2_20, a2, n20]
      have a26 : f (gv 1 0 1 0 1 0) = 0 := by linarith only [p_2_26, a2, n26]
      have a32 : f (gv 1 0 2 0 2 0) = 0 := by linarith only [p_2_32, a2, n32]
      have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_2_36, a2, n36]
      have a45 : f (gv 2 0 1 0 1 0) = 0 := by linarith only [p_2_45, a2, n45]
      have a3 : f (gv 0 0 1 0 0 0) = 1 := by linarith only [t_0_3_20, a0, a20, n3]
      have a18 : f (gv 1 0 0 0 (-2) 0) = 0 := by linarith only [t_3_18_41, a3, n41, n18]
      have a41 : f (gv 2 0 0 0 1 0) = 0 := by linarith only [t_3_18_41, a3, a18, n41]
      have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [t_3_19_21, a3, n21, n19]
      have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [t_3_19_21, a3, a19, n21]
      have a22 : f (gv 1 0 0 0 2 0) = 0 := by linarith only [t_3_22_40, a3, n40, n22]
      have a40 : f (gv 2 0 0 0 (-1) 0) = 0 := by linarith only [t_3_22_40, a3, a22, n40]
      have a11 : f (gv 1 0 (-2) 0 1 0) = 1 := by linarith only [t_11_19_26, a19, a26, n11]
      have a29 : f (gv 1 0 2 0 (-1) 0) = 1 := by linarith only [t_14_21_29, a14, a21, n29]
      have a5 : f (gv 0 0 1 0 2 0) = 0 := by linarith only [p_5_11, a11, n5]
      have a44 : f (gv 2 0 1 0 0 0) = 0 := by linarith only [p_11_44, a11, n44]
      have a37 : f (gv 2 0 (-1) 0 0 0) = 0 := by linarith only [p_29_37, a29, n37]
      have a10 : f (gv 1 0 (-2) 0 0 0) = 1 := by linarith only [t_0_10_44, a0, a44, n10]
      have a30 : f (gv 1 0 2 0 0 0) = 1 := by linarith only [t_0_30_37, a0, a37, n30]
      have a6 : f (gv 0 0 2 0 (-1) 0) = 1 := by linarith only [t_5_6_20, a5, a20, n6]
      have a42 : f (gv 2 0 1 0 (-2) 0) = 0 := by linarith only [p_10_42, a10, n42]
      have a43 : f (gv 2 0 1 0 (-1) 0) = 0 := by linarith only [p_10_43, a10, n43]
      have a46 : f (gv 2 0 1 0 2 0) = 0 := by linarith only [p_10_46, a10, n46]
      have a35 : f (gv 2 0 (-1) 0 (-2) 0) = 0 := by linarith only [p_30_35, a30, n35]
      have a38 : f (gv 2 0 (-1) 0 1 0) = 0 := by linarith only [p_30_38, a30, n38]
      have a39 : f (gv 2 0 (-1) 0 2 0) = 0 := by linarith only [p_30_39, a30, n39]
      have a13 : f (gv 1 0 (-1) 0 (-2) 0) = 0 := by linarith only [p_6_13, a6, n13]
      have a27 : f (gv 1 0 1 0 2 0) = 0 := by linarith only [p_6_27, a6, n27]
      have a16 : f (gv 1 0 (-1) 0 1 0) = 1 := by linarith only [t_4_16_43, a4, a43, n16]
      have a24 : f (gv 1 0 1 0 (-1) 0) = 1 := by linarith only [t_4_24_38, a4, a38, n24]
      have a47 : f (gv 2 0 2 0 (-1) 0) = 1 := by linarith only [t_8_39_47, a8, a39, n47]
      have a9 : f (gv 1 0 (-2) 0 (-1) 0) = 0 := by linarith only [t_9_21_24, a21, a24, n9]
      have a25 : f (gv 1 0 1 0 0 0) = 0 := by linarith only [t_13_16_25, a13, a16, n25]
      have a17 : f (gv 1 0 (-1) 0 2 0) = 1 := by linarith only [t_14_17_25, a14, a25, n17]
      have a15 : f (gv 1 0 (-1) 0 0 0) = 0 := by linarith only [t_15_24_27, a24, a27, n15]
      have a31 : f (gv 1 0 2 0 1 0) = 0 := by linarith only [t_16_19_31, a16, a19, n31]
      have a34 : f (gv 2 0 (-2) 0 1 0) = 1 := by linarith only [t_32_34_42, a32, a42, n34]
      have a7 : f (gv 0 0 2 0 1 0) = 0 := by linarith only [p_7_17, a17, n7]
      linarith only [t_0_15_25, a0, a15, a25]
  ·
    have a3 : f (gv 0 0 1 0 0 0) = 0 := by linarith only [p_0_3, a0, n3]
    have a10 : f (gv 1 0 (-2) 0 0 0) = 0 := by linarith only [p_0_10, a0, n10]
    have a15 : f (gv 1 0 (-1) 0 0 0) = 0 := by linarith only [p_0_15, a0, n15]
    have a20 : f (gv 1 0 0 0 0 0) = 0 := by linarith only [p_0_20, a0, n20]
    have a25 : f (gv 1 0 1 0 0 0) = 0 := by linarith only [p_0_25, a0, n25]
    have a30 : f (gv 1 0 2 0 0 0) = 0 := by linarith only [p_0_30, a0, n30]
    have a37 : f (gv 2 0 (-1) 0 0 0) = 0 := by linarith only [p_0_37, a0, n37]
    have a44 : f (gv 2 0 1 0 0 0) = 0 := by linarith only [p_0_44, a0, n44]
    rcases hB (gv 0 0 1 0 (-1) 0) (nonZero_of_y (by norm_num [gv])) with a2 | a2
    ·
      have a4 : f (gv 0 0 1 0 1 0) = 1 := by linarith only [t_2_4_20, a2, a20, n4]
      have a16 : f (gv 1 0 (-1) 0 1 0) = 0 := by linarith only [t_4_16_43, a4, n43, n16]
      have a43 : f (gv 2 0 1 0 (-1) 0) = 0 := by linarith only [t_4_16_43, a4, a16, n43]
      have a24 : f (gv 1 0 1 0 (-1) 0) = 0 := by linarith only [t_4_24_38, a4, n38, n24]
      have a38 : f (gv 2 0 (-1) 0 1 0) = 0 := by linarith only [t_4_24_38, a4, a24, n38]
      have a13 : f (gv 1 0 (-1) 0 (-2) 0) = 1 := by linarith only [t_13_16_25, a16, a25, n13]
      have a27 : f (gv 1 0 1 0 2 0) = 1 := by linarith only [t_15_24_27, a15, a24, n27]
      have a12 : f (gv 1 0 (-2) 0 2 0) = 0 := by linarith only [p_4_12, a4, n12]
      have a28 : f (gv 1 0 2 0 (-2) 0) = 0 := by linarith only [p_4_28, a4, n28]
      have a6 : f (gv 0 0 2 0 (-1) 0) = 0 := by linarith only [p_6_13, a13, n6]
      have a41 : f (gv 2 0 0 0 1 0) = 0 := by linarith only [p_13_41, a13, n41]
      have a40 : f (gv 2 0 0 0 (-1) 0) = 0 := by linarith only [p_27_40, a27, n40]
      have a18 : f (gv 1 0 0 0 (-2) 0) = 1 := by linarith only [t_3_18_41, a3, a41, n18]
      have a22 : f (gv 1 0 0 0 2 0) = 1 := by linarith only [t_3_22_40, a3, a40, n22]
      have a5 : f (gv 0 0 1 0 2 0) = 1 := by linarith only [t_5_6_20, a6, a20, n5]
      have a34 : f (gv 2 0 (-2) 0 1 0) = 0 := by linarith only [p_18_34, a18, n34]
      have a45 : f (gv 2 0 1 0 1 0) = 0 := by linarith only [p_18_45, a18, n45]
      have a48 : f (gv 2 0 2 0 1 0) = 0 := by linarith only [p_18_48, a18, n48]
      have a33 : f (gv 2 0 (-2) 0 (-1) 0) = 0 := by linarith only [p_22_33, a22, n33]
      have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_22_36, a22, n36]
      have a47 : f (gv 2 0 2 0 (-1) 0) = 0 := by linarith only [p_22_47, a22, n47]
      have a11 : f (gv 1 0 (-2) 0 1 0) = 0 := by linarith only [p_5_11, a5, n11]
      have a29 : f (gv 1 0 2 0 (-1) 0) = 0 := by linarith only [p_5_29, a5, n29]
      have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 1 := by linarith only [t_2_14_45, a2, a45, n14]
      have a26 : f (gv 1 0 1 0 1 0) = 1 := by linarith only [t_2_26_36, a2, a36, n26]
      have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [t_11_19_26, a11, a26, n19]
      have a35 : f (gv 2 0 (-1) 0 (-2) 0) = 1 := by linarith only [t_12_35_48, a12, a48, n35]
      have a17 : f (gv 1 0 (-1) 0 2 0) = 0 := by linarith only [t_14_17_25, a14, a25, n17]
      have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [t_14_21_29, a14, a29, n21]
      have a23 : f (gv 1 0 1 0 (-2) 0) = 0 := by linarith only [t_15_23_26, a15, a26, n23]
      have a31 : f (gv 1 0 2 0 1 0) = 1 := by linarith only [t_16_19_31, a16, a19, n31]
      have a46 : f (gv 2 0 1 0 2 0) = 1 := by linarith only [t_28_33_46, a28, a33, n46]
      have a1 : f (gv 0 0 1 0 (-2) 0) = 0 := by linarith only [p_1_31, a31, n1]
      have a7 : f (gv 0 0 2 0 1 0) = 1 := by linarith only [t_1_7_20, a1, a20, n7]
      linarith only [t_3_19_21, a3, a19, a21]
    ·
      have a4 : f (gv 0 0 1 0 1 0) = 0 := by linarith only [p_2_4, a2, n4]
      have a8 : f (gv 1 0 (-2) 0 (-2) 0) = 0 := by linarith only [p_2_8, a2, n8]
      have a14 : f (gv 1 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_2_14, a2, n14]
      have a26 : f (gv 1 0 1 0 1 0) = 0 := by linarith only [p_2_26, a2, n26]
      have a32 : f (gv 1 0 2 0 2 0) = 0 := by linarith only [p_2_32, a2, n32]
      have a36 : f (gv 2 0 (-1) 0 (-1) 0) = 0 := by linarith only [p_2_36, a2, n36]
      have a45 : f (gv 2 0 1 0 1 0) = 0 := by linarith only [p_2_45, a2, n45]
      have a17 : f (gv 1 0 (-1) 0 2 0) = 1 := by linarith only [t_14_17_25, a14, a25, n17]
      have a23 : f (gv 1 0 1 0 (-2) 0) = 1 := by linarith only [t_15_23_26, a15, a26, n23]
      have a7 : f (gv 0 0 2 0 1 0) = 0 := by linarith only [p_7_17, a17, n7]
      have a40 : f (gv 2 0 0 0 (-1) 0) = 0 := by linarith only [p_17_40, a17, n40]
      have a41 : f (gv 2 0 0 0 1 0) = 0 := by linarith only [p_23_41, a23, n41]
      have a1 : f (gv 0 0 1 0 (-2) 0) = 1 := by linarith only [t_1_7_20, a7, a20, n1]
      have a18 : f (gv 1 0 0 0 (-2) 0) = 1 := by linarith only [t_3_18_41, a3, a41, n18]
      have a22 : f (gv 1 0 0 0 2 0) = 1 := by linarith only [t_3_22_40, a3, a40, n22]
      have a9 : f (gv 1 0 (-2) 0 (-1) 0) = 0 := by linarith only [p_1_9, a1, n9]
      have a31 : f (gv 1 0 2 0 1 0) = 0 := by linarith only [p_1_31, a1, n31]
      have a33 : f (gv 2 0 (-2) 0 (-1) 0) = 0 := by linarith only [p_1_33, a1, n33]
      have a48 : f (gv 2 0 2 0 1 0) = 0 := by linarith only [p_1_48, a1, n48]
      have a34 : f (gv 2 0 (-2) 0 1 0) = 0 := by linarith only [p_18_34, a18, n34]
      have a38 : f (gv 2 0 (-1) 0 1 0) = 0 := by linarith only [p_18_38, a18, n38]
      have a43 : f (gv 2 0 1 0 (-1) 0) = 0 := by linarith only [p_22_43, a22, n43]
      have a47 : f (gv 2 0 2 0 (-1) 0) = 0 := by linarith only [p_22_47, a22, n47]
      have a16 : f (gv 1 0 (-1) 0 1 0) = 1 := by linarith only [t_4_16_43, a4, a43, n16]
      have a24 : f (gv 1 0 1 0 (-1) 0) = 1 := by linarith only [t_4_24_38, a4, a38, n24]
      have a39 : f (gv 2 0 (-1) 0 2 0) = 1 := by linarith only [t_8_39_47, a8, a47, n39]
      have a21 : f (gv 1 0 0 0 1 0) = 0 := by linarith only [t_9_21_24, a9, a24, n21]
      have a13 : f (gv 1 0 (-1) 0 (-2) 0) = 0 := by linarith only [t_13_16_25, a16, a25, n13]
      have a29 : f (gv 1 0 2 0 (-1) 0) = 1 := by linarith only [t_14_21_29, a14, a21, n29]
      have a27 : f (gv 1 0 1 0 2 0) = 0 := by linarith only [t_15_24_27, a15, a24, n27]
      have a19 : f (gv 1 0 0 0 (-1) 0) = 0 := by linarith only [t_16_19_31, a16, a31, n19]
      have a42 : f (gv 2 0 1 0 (-2) 0) = 1 := by linarith only [t_32_34_42, a32, a34, n42]
      have a5 : f (gv 0 0 1 0 2 0) = 0 := by linarith only [p_5_29, a29, n5]
      linarith only [t_3_19_21, a3, a19, a21]

end BornFinite.GaussianFrames.NoColouring

#print axioms BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function
