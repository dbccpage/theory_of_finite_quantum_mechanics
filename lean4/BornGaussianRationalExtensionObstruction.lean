import BornGaussianRationalFrameObstruction
import BornRationalRayObstruction
import Mathlib.Tactic.LinearCombination

/-!
A finite obstruction to extending the repository's exotic rational-ray frame function
to Gaussian-rational three-space. The 210 frames and 19 real-ray constraints below
are an exact integer-weighted certificate; no positivity or symmetry is assumed.
AuthorityEffect: None. This does not classify all Gaussian-rational frame functions.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

namespace BornFinite.GaussianExtension

open BornFinite.GaussianFrames

/-- These finitely many prescribed real-ray values already prevent a frame function. -/
theorem no_prescribed_frame_function (f : GVec → ℚ) (hF : IsFrameFunction f)
    (r0 : f (gv 0 0 1 0 (-2) 0) = (1 / 3 : ℚ))
    (r1 : f (gv 0 0 1 0 (-1) 0) = (2 / 3 : ℚ))
    (r2 : f (gv 0 0 1 0 1 0) = (0 : ℚ))
    (r3 : f (gv 0 0 1 0 2 0) = (1 / 3 : ℚ))
    (r4 : f (gv 0 0 1 0 3 0) = (2 / 3 : ℚ))
    (r5 : f (gv 0 0 2 0 (-1) 0) = (1 / 3 : ℚ))
    (r6 : f (gv 0 0 2 0 1 0) = (1 / 3 : ℚ))
    (r7 : f (gv 1 0 (-2) 0 0 0) = (1 / 3 : ℚ))
    (r8 : f (gv 1 0 0 0 (-2) 0) = (1 / 3 : ℚ))
    (r9 : f (gv 1 0 0 0 (-1) 0) = (2 / 3 : ℚ))
    (r10 : f (gv 1 0 0 0 0 0) = (1 / 3 : ℚ))
    (r11 : f (gv 1 0 0 0 1 0) = (0 : ℚ))
    (r12 : f (gv 1 0 0 0 2 0) = (1 / 3 : ℚ))
    (r13 : f (gv 1 0 0 0 3 0) = (2 / 3 : ℚ))
    (r14 : f (gv 1 0 2 0 0 0) = (1 / 3 : ℚ))
    (r15 : f (gv 2 0 (-1) 0 0 0) = (1 / 3 : ℚ))
    (r16 : f (gv 2 0 0 0 (-1) 0) = (1 / 3 : ℚ))
    (r17 : f (gv 2 0 0 0 1 0) = (1 / 3 : ℚ))
    (r18 : f (gv 2 0 1 0 0 0) = (1 / 3 : ℚ))
    : False := by
  have t0 := hF (gv 0 0 0 0 1 0) (gv 1 0 0 (-2) 0 0) (gv 2 0 0 1 0 0) (by
    exact ⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t1 := hF (gv 0 0 0 0 1 0) (gv 1 0 0 2 0 0) (gv 2 0 0 (-1) 0 0) (by
    exact ⟨nonZero_of_z (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t2 := hF (gv 0 0 1 0 (-2) 0) (gv 5 0 (-2) (-4) (-1) (-2)) (gv 5 0 2 4 1 2) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t3 := hF (gv 0 0 1 0 (-2) 0) (gv 5 0 (-2) 4 (-1) 2) (gv 5 0 2 (-4) 1 (-2)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t4 := hF (gv 0 0 1 0 (-1) 0) (gv 2 0 (-3) (-1) (-3) (-1)) (gv 10 0 3 1 3 1) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t5 := hF (gv 0 0 1 0 (-1) 0) (gv 2 0 (-1) 3 (-1) 3) (gv 10 0 1 (-3) 1 (-3)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t6 := hF (gv 0 0 1 0 (-1) 0) (gv 2 0 1 (-3) 1 (-3)) (gv 10 0 (-1) 3 (-1) 3) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t7 := hF (gv 0 0 1 0 (-1) 0) (gv 2 0 3 1 3 1) (gv 10 0 (-3) (-1) (-3) (-1)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t8 := hF (gv 0 0 1 0 0 (-2)) (gv 0 0 2 0 0 1) (gv 1 0 0 0 0 0) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t9 := hF (gv 0 0 1 0 0 (-2)) (gv 5 0 (-4) (-2) 1 (-2)) (gv 5 0 4 2 (-1) 2) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t10 := hF (gv 0 0 1 0 0 (-2)) (gv 5 0 (-2) (-6) 3 (-1)) (gv 10 0 2 6 (-3) 1) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t11 := hF (gv 0 0 1 0 0 0) (gv 1 0 0 0 0 (-2)) (gv 2 0 0 0 0 1) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t12 := hF (gv 0 0 1 0 0 0) (gv 1 0 0 0 0 2) (gv 2 0 0 0 0 (-1)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t13 := hF (gv 0 0 1 0 0 2) (gv 0 0 2 0 0 (-1)) (gv 1 0 0 0 0 0) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t14 := hF (gv 0 0 1 0 0 2) (gv 5 0 (-4) (-2) (-1) 2) (gv 5 0 4 2 1 (-2)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t15 := hF (gv 0 0 1 0 0 2) (gv 5 0 6 2 1 (-3)) (gv 10 0 (-6) (-2) (-1) 3) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t16 := hF (gv 0 0 1 0 1 0) (gv 1 0 (-1) (-1) 1 1) (gv 4 0 1 1 (-1) (-1)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t17 := hF (gv 0 0 1 0 1 0) (gv 1 0 (-1) 1 1 (-1)) (gv 4 0 1 (-1) (-1) 1) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t18 := hF (gv 0 0 1 0 2 0) (gv 5 0 (-6) (-2) 3 1) (gv 10 0 6 2 (-3) (-1)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t19 := hF (gv 0 0 1 0 2 0) (gv 5 0 (-2) (-6) 1 3) (gv 10 0 2 6 (-1) (-3)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t20 := hF (gv 0 0 1 0 2 0) (gv 5 0 (-2) (-4) 1 2) (gv 5 0 2 4 (-1) (-2)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t21 := hF (gv 0 0 1 0 2 0) (gv 5 0 (-2) 4 1 (-2)) (gv 5 0 2 (-4) (-1) 2) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t22 := hF (gv 0 0 1 0 2 0) (gv 5 0 2 (-6) (-1) 3) (gv 10 0 (-2) 6 1 (-3)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t23 := hF (gv 0 0 1 0 2 0) (gv 5 0 2 6 (-1) (-3)) (gv 10 0 (-2) (-6) 1 3) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t24 := hF (gv 0 0 1 0 2 0) (gv 5 0 6 2 (-3) (-1)) (gv 10 0 (-6) (-2) 3 1) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t25 := hF (gv 0 0 1 0 3 0) (gv 10 0 (-9) (-3) 3 1) (gv 10 0 9 3 (-3) (-1)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t26 := hF (gv 0 0 1 0 3 0) (gv 10 0 (-3) (-9) 1 3) (gv 10 0 3 9 (-1) (-3)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t27 := hF (gv 0 0 1 0 3 0) (gv 10 0 (-3) 9 1 (-3)) (gv 10 0 3 (-9) (-1) 3) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t28 := hF (gv 0 0 2 0 (-1) 0) (gv 5 0 1 (-3) 2 (-6)) (gv 10 0 (-1) 3 (-2) 6) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t29 := hF (gv 0 0 2 0 0 (-1)) (gv 5 0 3 (-1) 2 6) (gv 10 0 (-3) 1 (-2) (-6)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t30 := hF (gv 0 0 2 0 0 1) (gv 5 0 (-3) 1 2 6) (gv 10 0 3 (-1) (-2) (-6)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t31 := hF (gv 0 0 2 0 0 1) (gv 5 0 1 3 6 (-2)) (gv 10 0 (-1) (-3) (-6) 2) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t32 := hF (gv 0 0 2 0 0 1) (gv 5 0 3 (-1) (-2) (-6)) (gv 10 0 (-3) 1 2 6) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t33 := hF (gv 0 0 2 0 1 0) (gv 5 0 (-3) (-1) 6 2) (gv 10 0 3 1 (-6) (-2)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t34 := hF (gv 0 0 2 0 1 0) (gv 5 0 (-1) (-3) 2 6) (gv 10 0 1 3 (-2) (-6)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t35 := hF (gv 0 0 2 0 1 0) (gv 5 0 (-1) 3 2 (-6)) (gv 10 0 1 (-3) (-2) 6) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t36 := hF (gv 0 0 2 0 1 0) (gv 5 0 1 (-3) (-2) 6) (gv 10 0 (-1) 3 2 (-6)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t37 := hF (gv 0 0 2 0 1 0) (gv 5 0 1 3 (-2) (-6)) (gv 10 0 (-1) (-3) 2 6) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t38 := hF (gv 0 0 2 0 1 0) (gv 5 0 3 1 (-6) (-2)) (gv 10 0 (-3) (-1) 6 2) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t39 := hF (gv 0 0 3 0 1 0) (gv 10 0 (-3) (-1) 9 3) (gv 10 0 3 1 (-9) (-3)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t40 := hF (gv 0 0 3 0 1 0) (gv 10 0 (-1) (-3) 3 9) (gv 10 0 1 3 (-3) (-9)) (by
    exact ⟨nonZero_of_y (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t41 := hF (gv 1 0 (-3) (-1) (-3) 0) (gv 1 0 3 1 (-3) 0) (gv 3 0 0 0 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t42 := hF (gv 1 0 (-3) (-1) (-3) 0) (gv 4 0 3 1 (-2) 0) (gv 5 0 (-3) (-1) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t43 := hF (gv 1 0 (-3) (-1) (-2) 0) (gv 2 0 0 0 1 0) (gv 2 0 3 1 (-4) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t44 := hF (gv 1 0 (-3) (-1) (-2) 0) (gv 2 0 1 (-1) 0 2) (gv 4 0 0 2 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t45 := hF (gv 1 0 (-3) (-1) 1 0) (gv 1 0 0 0 (-1) 0) (gv 5 0 3 1 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t46 := hF (gv 1 0 (-3) (-1) 1 0) (gv 2 0 0 1 (-1) 3) (gv 13 0 5 (-1) 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t47 := hF (gv 1 0 (-3) (-1) 1 0) (gv 5 0 1 3 1 8) (gv 10 0 3 (-1) (-2) (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t48 := hF (gv 1 0 (-3) 1 0 (-2)) (gv 2 0 (-1) (-3) (-5) 1) (gv 10 0 3 1 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t49 := hF (gv 1 0 (-3) 1 0 (-2)) (gv 2 0 0 0 0 1) (gv 2 0 3 (-1) 0 (-4)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t50 := hF (gv 1 0 (-3) 1 2 0) (gv 2 0 0 0 (-1) 0) (gv 2 0 3 (-1) 4 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t51 := hF (gv 1 0 (-3) 1 2 0) (gv 2 0 1 1 0 2) (gv 4 0 0 (-2) (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t52 := hF (gv 1 0 (-2) 0 (-1) (-2)) (gv 1 0 (-2) 0 1 2) (gv 2 0 1 0 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t53 := hF (gv 1 0 (-2) 0 (-1) (-2)) (gv 2 0 (-1) (-1) 0 2) (gv 5 0 4 2 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t54 := hF (gv 1 0 (-2) 0 0 0) (gv 2 0 1 0 (-3) (-1)) (gv 4 0 2 0 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t55 := hF (gv 1 0 (-2) 0 0 0) (gv 2 0 1 0 (-1) (-3)) (gv 4 0 2 0 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t56 := hF (gv 1 0 (-2) 0 0 0) (gv 2 0 1 0 (-1) 2) (gv 2 0 1 0 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t57 := hF (gv 1 0 (-2) 0 0 0) (gv 2 0 1 0 (-1) 3) (gv 4 0 2 0 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t58 := hF (gv 1 0 (-2) 0 1 (-3)) (gv 2 0 (-4) 0 (-1) 3) (gv 2 0 1 0 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t59 := hF (gv 1 0 (-2) 0 1 (-3)) (gv 2 0 1 (-5) (-3) (-1)) (gv 10 0 1 3 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t60 := hF (gv 1 0 (-2) 0 1 2) (gv 2 0 (-1) (-1) 0 (-2)) (gv 5 0 4 2 (-1) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t61 := hF (gv 1 0 (-2) 0 1 3) (gv 2 0 (-4) 0 (-1) (-3)) (gv 2 0 1 0 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t62 := hF (gv 1 0 (-2) 0 1 3) (gv 2 0 0 (-2) 1 (-1)) (gv 4 0 1 3 (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t63 := hF (gv 1 0 (-2) 2 (-1) 0) (gv 5 0 (-1) (-3) 1 8) (gv 13 0 5 (-1) 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t64 := hF (gv 1 0 (-2) 2 (-1) 0) (gv 5 0 3 1 1 (-8)) (gv 13 0 1 (-5) 1 8) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t65 := hF (gv 1 0 (-1) (-3) (-3) 0) (gv 1 0 1 3 (-3) 0) (gv 3 0 0 0 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t66 := hF (gv 1 0 (-1) (-3) (-3) 0) (gv 4 0 1 3 (-2) 0) (gv 5 0 (-1) (-3) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t67 := hF (gv 1 0 (-1) (-3) (-2) 0) (gv 2 0 (-1) 1 0 (-2)) (gv 4 0 2 0 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t68 := hF (gv 1 0 (-1) (-3) (-2) 0) (gv 2 0 0 0 1 0) (gv 2 0 1 3 (-4) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t69 := hF (gv 1 0 (-1) (-3) 1 0) (gv 2 0 1 0 (-1) (-3)) (gv 13 0 (-1) 5 1 8) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t70 := hF (gv 1 0 (-1) (-3) 1 0) (gv 5 0 3 1 1 (-8)) (gv 10 0 (-1) 3 (-2) 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t71 := hF (gv 1 0 (-1) (-1) (-1) 1) (gv 2 0 (-1) 0 1 (-2)) (gv 2 0 2 1 0 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t72 := hF (gv 1 0 (-1) (-1) (-1) 1) (gv 2 0 0 (-1) 2 (-1)) (gv 2 0 1 2 (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t73 := hF (gv 1 0 (-1) (-1) (-1) 1) (gv 2 0 1 (-3) 4 0) (gv 10 0 2 6 (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t74 := hF (gv 1 0 (-1) (-1) (-1) 1) (gv 2 0 4 0 1 3) (gv 10 0 (-1) 3 2 (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t75 := hF (gv 1 0 (-1) (-1) 1 (-1)) (gv 2 0 (-3) 1 0 4) (gv 10 0 6 2 (-3) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t76 := hF (gv 1 0 (-1) (-1) 1 (-1)) (gv 2 0 (-1) 0 (-1) 2) (gv 2 0 2 1 0 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t77 := hF (gv 1 0 (-1) (-1) 1 (-1)) (gv 2 0 0 (-1) (-2) 1) (gv 2 0 1 2 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t78 := hF (gv 1 0 (-1) (-1) 1 1) (gv 2 0 1 (-3) 0 (-4)) (gv 10 0 2 6 (-3) 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t79 := hF (gv 1 0 (-1) 1 (-1) (-1)) (gv 2 0 0 1 2 1) (gv 2 0 1 (-2) (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t80 := hF (gv 1 0 (-1) 1 (-1) (-1)) (gv 2 0 4 0 1 (-3)) (gv 10 0 (-1) (-3) 2 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t81 := hF (gv 1 0 (-1) 1 1 (-1)) (gv 2 0 4 0 3 1) (gv 10 0 (-1) (-3) (-6) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t82 := hF (gv 1 0 (-1) 1 1 1) (gv 2 0 0 (-4) 3 (-1)) (gv 10 0 3 1 (-6) (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t83 := hF (gv 1 0 (-1) 1 1 1) (gv 2 0 0 1 (-2) (-1)) (gv 2 0 1 (-2) 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t84 := hF (gv 1 0 (-1) 3 (-2) 0) (gv 2 0 (-1) (-1) 0 2) (gv 4 0 2 0 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t85 := hF (gv 1 0 (-1) 3 (-2) 0) (gv 2 0 0 0 1 0) (gv 2 0 1 (-3) (-4) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t86 := hF (gv 1 0 (-1) 3 0 (-2)) (gv 2 0 (-1) (-1) (-2) 0) (gv 4 0 2 0 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t87 := hF (gv 1 0 (-1) 3 0 (-2)) (gv 2 0 0 0 0 1) (gv 2 0 1 (-3) 0 (-4)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t88 := hF (gv 1 0 (-1) 3 1 0) (gv 1 0 0 0 (-1) 0) (gv 5 0 1 (-3) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t89 := hF (gv 1 0 (-1) 3 1 0) (gv 2 0 1 0 (-1) 3) (gv 13 0 (-1) (-5) 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t90 := hF (gv 1 0 (-1) 3 2 0) (gv 2 0 0 0 (-1) 0) (gv 2 0 1 (-3) 4 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t91 := hF (gv 1 0 (-1) 3 2 0) (gv 2 0 3 1 (-1) 5) (gv 10 0 (-1) (-3) (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t92 := hF (gv 1 0 0 (-2) (-3) 1) (gv 2 0 (-5) 1 (-1) (-3)) (gv 10 0 3 1 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t93 := hF (gv 1 0 0 (-2) (-3) 1) (gv 2 0 0 (-4) 3 (-1)) (gv 2 0 0 1 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t94 := hF (gv 1 0 0 (-2) (-1) (-2)) (gv 1 0 0 (-2) 1 2) (gv 2 0 0 1 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t95 := hF (gv 1 0 0 (-2) (-1) (-2)) (gv 2 0 1 (-1) 0 2) (gv 5 0 (-2) 4 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t96 := hF (gv 1 0 0 (-2) (-1) 2) (gv 1 0 0 (-2) 1 (-2)) (gv 2 0 0 1 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t97 := hF (gv 1 0 0 (-2) (-1) 2) (gv 2 0 (-1) (-1) 0 (-2)) (gv 5 0 2 4 1 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t98 := hF (gv 1 0 0 (-2) (-1) 3) (gv 2 0 (-2) 0 (-1) (-1)) (gv 4 0 3 1 2 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t99 := hF (gv 1 0 0 (-2) (-1) 3) (gv 2 0 0 (-4) 1 (-3)) (gv 2 0 0 1 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t100 := hF (gv 1 0 0 (-2) 0 0) (gv 2 0 0 1 (-2) (-1)) (gv 2 0 0 1 2 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t101 := hF (gv 1 0 0 (-2) 0 0) (gv 2 0 0 1 (-2) 1) (gv 2 0 0 1 2 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t102 := hF (gv 1 0 0 (-2) 0 0) (gv 2 0 0 1 (-1) 3) (gv 4 0 0 2 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t103 := hF (gv 1 0 0 (-2) 1 (-2)) (gv 2 0 (-1) (-1) 0 2) (gv 5 0 2 4 (-1) (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t104 := hF (gv 1 0 0 (-2) 1 2) (gv 2 0 1 (-1) 0 (-2)) (gv 5 0 (-2) 4 (-1) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t105 := hF (gv 1 0 0 0 (-2) 0) (gv 2 0 (-3) (-1) 1 0) (gv 4 0 3 1 2 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t106 := hF (gv 1 0 0 0 (-2) 0) (gv 2 0 (-1) (-2) 1 0) (gv 2 0 1 2 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t107 := hF (gv 1 0 0 0 (-2) 0) (gv 2 0 (-1) 2 1 0) (gv 2 0 1 (-2) 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t108 := hF (gv 1 0 0 0 (-1) 0) (gv 1 0 1 (-3) 1 0) (gv 5 0 (-1) 3 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t109 := hF (gv 1 0 0 0 (-1) 0) (gv 1 0 3 1 1 0) (gv 5 0 (-3) (-1) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t110 := hF (gv 1 0 0 0 0 (-2)) (gv 2 0 (-2) (-1) 0 1) (gv 2 0 2 1 0 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t111 := hF (gv 1 0 0 0 0 (-2)) (gv 2 0 1 (-3) 0 1) (gv 4 0 (-1) 3 0 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t112 := hF (gv 1 0 0 0 0 2) (gv 2 0 (-2) (-1) 0 (-1)) (gv 2 0 2 1 0 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t113 := hF (gv 1 0 0 0 1 0) (gv 1 0 2 (-2) (-1) 0) (gv 2 0 (-1) 1 (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t114 := hF (gv 1 0 0 0 1 0) (gv 1 0 2 2 (-1) 0) (gv 2 0 (-1) (-1) (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t115 := hF (gv 1 0 0 0 2 0) (gv 2 0 (-3) (-1) (-1) 0) (gv 4 0 3 1 (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t116 := hF (gv 1 0 0 0 2 0) (gv 2 0 (-1) (-3) (-1) 0) (gv 4 0 1 3 (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t117 := hF (gv 1 0 0 0 2 0) (gv 2 0 (-1) (-2) (-1) 0) (gv 2 0 1 2 (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t118 := hF (gv 1 0 0 0 2 0) (gv 2 0 (-1) 2 (-1) 0) (gv 2 0 1 (-2) (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t119 := hF (gv 1 0 0 0 2 0) (gv 2 0 1 3 (-1) 0) (gv 4 0 (-1) (-3) (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t120 := hF (gv 1 0 0 0 2 0) (gv 2 0 3 1 (-1) 0) (gv 4 0 (-3) (-1) (-2) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t121 := hF (gv 1 0 0 0 3 0) (gv 3 0 (-3) (-1) (-1) 0) (gv 3 0 3 1 (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t122 := hF (gv 1 0 0 0 3 0) (gv 3 0 (-1) (-3) (-1) 0) (gv 3 0 1 3 (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t123 := hF (gv 1 0 0 0 3 0) (gv 3 0 (-1) 3 (-1) 0) (gv 3 0 1 (-3) (-1) 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t124 := hF (gv 1 0 0 2 (-1) (-2)) (gv 1 0 0 2 1 2) (gv 2 0 0 (-1) 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t125 := hF (gv 1 0 0 2 (-1) (-2)) (gv 2 0 (-1) 1 0 2) (gv 5 0 2 (-4) 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t126 := hF (gv 1 0 0 2 (-1) 2) (gv 1 0 0 2 1 (-2)) (gv 2 0 0 (-1) 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t127 := hF (gv 1 0 0 2 (-1) 2) (gv 2 0 1 1 0 (-2)) (gv 5 0 (-2) (-4) 1 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t128 := hF (gv 1 0 0 2 0 0) (gv 2 0 0 (-1) (-2) (-1)) (gv 2 0 0 (-1) 2 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t129 := hF (gv 1 0 0 2 0 0) (gv 2 0 0 (-1) (-2) 1) (gv 2 0 0 (-1) 2 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t130 := hF (gv 1 0 0 2 0 0) (gv 2 0 0 (-1) (-1) 3) (gv 4 0 0 (-2) 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t131 := hF (gv 1 0 0 2 0 0) (gv 2 0 0 (-1) 1 3) (gv 4 0 0 (-2) (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t132 := hF (gv 1 0 0 2 1 (-2)) (gv 2 0 1 1 0 2) (gv 5 0 (-2) (-4) (-1) (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t133 := hF (gv 1 0 0 2 1 2) (gv 2 0 (-1) 1 0 (-2)) (gv 5 0 2 (-4) (-1) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t134 := hF (gv 1 0 0 2 3 (-1)) (gv 2 0 0 (-1) 0 0) (gv 2 0 0 4 (-3) 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t135 := hF (gv 1 0 0 2 3 (-1)) (gv 2 0 5 (-1) 1 3) (gv 10 0 (-3) (-1) (-3) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t136 := hF (gv 1 0 1 (-3) (-2) 0) (gv 2 0 (-3) (-1) 1 (-5)) (gv 10 0 1 3 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t137 := hF (gv 1 0 1 (-3) (-2) 0) (gv 2 0 (-1) 3 (-4) 0) (gv 2 0 0 0 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t138 := hF (gv 1 0 1 (-3) 1 0) (gv 5 0 (-3) 1 1 8) (gv 10 0 1 3 (-2) (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t139 := hF (gv 1 0 1 (-1) (-1) (-1)) (gv 2 0 (-1) 2 (-1) 0) (gv 2 0 0 (-1) 2 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t140 := hF (gv 1 0 1 (-1) (-1) (-1)) (gv 2 0 0 4 (-3) 1) (gv 10 0 (-3) (-1) 6 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t141 := hF (gv 1 0 1 (-1) 1 1) (gv 2 0 (-4) 0 (-1) 3) (gv 10 0 1 3 (-2) (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t142 := hF (gv 1 0 1 (-1) 1 1) (gv 2 0 (-1) (-3) (-4) 0) (gv 10 0 (-2) 6 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t143 := hF (gv 1 0 1 (-1) 1 1) (gv 2 0 (-1) 2 1 0) (gv 2 0 0 (-1) (-2) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t144 := hF (gv 1 0 1 1 (-1) (-1)) (gv 2 0 0 (-4) 1 (-3)) (gv 10 0 (-3) 1 2 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t145 := hF (gv 1 0 1 1 (-1) (-1)) (gv 2 0 3 (-1) 4 0) (gv 10 0 (-6) (-2) (-1) 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t146 := hF (gv 1 0 1 1 (-1) 1) (gv 2 0 (-2) (-1) 0 1) (gv 2 0 1 0 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t147 := hF (gv 1 0 1 1 (-1) 1) (gv 2 0 (-1) (-2) (-1) 0) (gv 2 0 0 1 2 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t148 := hF (gv 1 0 1 1 (-1) 1) (gv 2 0 3 (-1) 0 (-4)) (gv 10 0 (-6) (-2) 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t149 := hF (gv 1 0 1 1 1 (-1)) (gv 2 0 (-4) 0 (-1) (-3)) (gv 10 0 1 (-3) (-2) 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t150 := hF (gv 1 0 1 1 1 (-1)) (gv 2 0 (-2) (-1) 0 (-1)) (gv 2 0 1 0 (-1) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t151 := hF (gv 1 0 1 1 1 (-1)) (gv 2 0 (-1) (-2) 1 0) (gv 2 0 0 1 (-2) 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t152 := hF (gv 1 0 1 1 1 (-1)) (gv 2 0 (-1) 3 (-4) 0) (gv 10 0 (-2) (-6) 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t153 := hF (gv 1 0 1 3 (-3) 0) (gv 4 0 (-1) (-3) (-2) 0) (gv 5 0 1 3 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t154 := hF (gv 1 0 1 3 (-2) 0) (gv 2 0 (-3) 1 1 5) (gv 10 0 1 (-3) 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t155 := hF (gv 1 0 1 3 (-2) 0) (gv 2 0 (-1) (-3) (-4) 0) (gv 2 0 0 0 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t156 := hF (gv 1 0 1 3 (-2) 0) (gv 2 0 1 (-1) 0 (-2)) (gv 4 0 (-2) 0 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t157 := hF (gv 1 0 1 3 1 0) (gv 2 0 (-1) 0 (-1) (-3)) (gv 13 0 1 (-5) 1 8) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t158 := hF (gv 1 0 1 3 1 0) (gv 5 0 (-3) (-1) 1 (-8)) (gv 10 0 1 (-3) (-2) 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t159 := hF (gv 1 0 2 (-2) (-1) 0) (gv 5 0 (-3) (-1) 1 (-8)) (gv 13 0 (-1) 5 1 8) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t160 := hF (gv 1 0 2 (-2) (-1) 0) (gv 5 0 1 3 1 8) (gv 13 0 (-5) 1 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t161 := hF (gv 1 0 2 0 (-3) (-1)) (gv 2 0 (-1) 0 0 0) (gv 2 0 4 0 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t162 := hF (gv 1 0 2 0 (-3) (-1)) (gv 2 0 0 (-2) 1 (-1)) (gv 4 0 (-1) 3 0 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t163 := hF (gv 1 0 2 0 (-1) (-3)) (gv 2 0 (-1) (-5) 3 (-1)) (gv 10 0 (-1) 3 (-1) 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t164 := hF (gv 1 0 2 0 (-1) (-3)) (gv 2 0 (-1) 0 0 0) (gv 2 0 4 0 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t165 := hF (gv 1 0 2 0 (-1) (-2)) (gv 1 0 2 0 1 2) (gv 2 0 (-1) 0 0 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t166 := hF (gv 1 0 2 0 (-1) (-2)) (gv 2 0 1 1 0 2) (gv 5 0 (-4) (-2) 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t167 := hF (gv 1 0 2 0 (-1) 3) (gv 2 0 (-1) 0 0 0) (gv 2 0 4 0 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t168 := hF (gv 1 0 2 0 (-1) 3) (gv 2 0 (-1) 5 3 1) (gv 10 0 (-1) (-3) (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t169 := hF (gv 1 0 2 0 0 0) (gv 2 0 (-1) 0 (-1) (-3)) (gv 4 0 (-2) 0 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t170 := hF (gv 1 0 2 0 0 0) (gv 2 0 (-1) 0 (-1) 2) (gv 2 0 (-1) 0 1 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t171 := hF (gv 1 0 2 0 1 2) (gv 2 0 1 1 0 (-2)) (gv 5 0 (-4) (-2) (-1) 2) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t172 := hF (gv 1 0 2 2 (-1) 0) (gv 5 0 (-3) 1 1 8) (gv 13 0 (-1) (-5) 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t173 := hF (gv 1 0 3 (-1) 0 2) (gv 2 0 (-3) 1 0 4) (gv 2 0 0 0 0 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t174 := hF (gv 1 0 3 (-1) 0 2) (gv 2 0 1 3 5 (-1)) (gv 10 0 (-3) (-1) (-3) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t175 := hF (gv 1 0 3 1 (-3) 0) (gv 4 0 (-3) (-1) (-2) 0) (gv 5 0 3 1 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t176 := hF (gv 1 0 3 1 (-2) 0) (gv 2 0 (-3) (-1) (-4) 0) (gv 2 0 0 0 1 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t177 := hF (gv 1 0 3 1 (-2) 0) (gv 2 0 (-1) 1 0 2) (gv 4 0 0 (-2) 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t178 := hF (gv 1 0 3 1 1 0) (gv 2 0 0 (-1) (-1) 3) (gv 13 0 (-5) 1 1 (-8)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t179 := hF (gv 1 0 3 1 1 0) (gv 5 0 (-1) (-3) 1 8) (gv 10 0 (-3) 1 (-2) (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t180 := hF (gv 2 0 (-5) 1 (-1) (-3)) (gv 2 0 1 3 5 (-1)) (gv 4 0 1 (-1) (-1) 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t181 := hF (gv 2 0 (-3) (-1) (-4) 0) (gv 3 0 3 1 (-1) 0) (gv 5 0 (-3) (-1) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t182 := hF (gv 2 0 (-3) (-1) (-3) (-1)) (gv 5 0 (-3) (-1) 6 2) (gv 10 0 9 3 (-3) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t183 := hF (gv 2 0 (-3) (-1) (-3) (-1)) (gv 5 0 6 2 (-3) (-1)) (gv 10 0 (-3) (-1) 9 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t184 := hF (gv 2 0 (-3) (-1) (-1) 0) (gv 2 0 1 1 0 (-2)) (gv 5 0 3 (-1) 2 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t185 := hF (gv 2 0 (-3) (-1) 1 (-5)) (gv 2 0 (-1) 5 3 1) (gv 4 0 1 (-1) (-1) 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t186 := hF (gv 2 0 (-3) (-1) 1 0) (gv 2 0 1 1 0 2) (gv 5 0 3 (-1) (-2) (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t187 := hF (gv 2 0 (-3) 1 1 5) (gv 2 0 (-1) (-5) 3 (-1)) (gv 4 0 1 1 (-1) (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t188 := hF (gv 2 0 (-2) 0 (-1) (-1)) (gv 2 0 0 (-1) 1 3) (gv 5 0 6 2 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t189 := hF (gv 2 0 (-1) (-3) (-5) 1) (gv 2 0 5 (-1) 1 3) (gv 4 0 (-1) 1 1 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t190 := hF (gv 2 0 (-1) (-3) (-4) 0) (gv 3 0 1 3 (-1) 0) (gv 5 0 (-1) (-3) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t191 := hF (gv 2 0 (-1) (-3) (-1) (-3)) (gv 5 0 (-1) (-3) 2 6) (gv 10 0 3 9 (-1) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t192 := hF (gv 2 0 (-1) (-3) (-1) (-3)) (gv 5 0 2 6 (-1) (-3)) (gv 10 0 (-1) (-3) 3 9) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t193 := hF (gv 2 0 (-1) (-3) (-1) 0) (gv 2 0 1 1 0 2) (gv 5 0 (-1) 3 2 (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t194 := hF (gv 2 0 (-1) (-1) 0 (-2)) (gv 2 0 3 1 (-1) 0) (gv 5 0 (-3) 1 2 6) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t195 := hF (gv 2 0 (-1) (-1) 0 2) (gv 2 0 1 3 (-1) 0) (gv 5 0 1 (-3) 2 (-6)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t196 := hF (gv 2 0 (-1) 0 (-1) (-3)) (gv 2 0 0 2 1 1) (gv 5 0 2 (-6) (-1) 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t197 := hF (gv 2 0 (-1) 1 (-2) 0) (gv 2 0 1 (-3) 0 1) (gv 5 0 1 3 6 (-2)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t198 := hF (gv 2 0 (-1) 3 (-4) 0) (gv 3 0 1 (-3) (-1) 0) (gv 5 0 (-1) 3 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t199 := hF (gv 2 0 (-1) 3 (-1) 3) (gv 5 0 (-1) 3 2 (-6)) (gv 10 0 3 (-9) (-1) 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t200 := hF (gv 2 0 0 2 1 1) (gv 2 0 1 0 (-3) (-1)) (gv 5 0 (-2) (-6) 3 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t201 := hF (gv 2 0 1 (-5) (-3) (-1)) (gv 2 0 3 1 (-1) 5) (gv 4 0 (-1) 1 1 (-1)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t202 := hF (gv 2 0 1 (-3) (-4) 0) (gv 3 0 (-1) 3 (-1) 0) (gv 5 0 1 (-3) 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t203 := hF (gv 2 0 1 (-3) 1 (-3)) (gv 5 0 1 (-3) (-2) 6) (gv 10 0 (-3) 9 1 (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t204 := hF (gv 2 0 1 3 (-4) 0) (gv 3 0 (-1) (-3) (-1) 0) (gv 5 0 1 3 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t205 := hF (gv 2 0 1 3 1 3) (gv 5 0 (-2) (-6) 1 3) (gv 10 0 1 3 (-3) (-9)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t206 := hF (gv 2 0 1 3 1 3) (gv 5 0 1 3 (-2) (-6)) (gv 10 0 (-3) (-9) 1 3) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t207 := hF (gv 2 0 3 1 (-4) 0) (gv 3 0 (-3) (-1) (-1) 0) (gv 5 0 3 1 5 0) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t208 := hF (gv 2 0 3 1 3 1) (gv 5 0 (-6) (-2) 3 1) (gv 10 0 3 1 (-9) (-3)) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have t209 := hF (gv 2 0 3 1 3 1) (gv 5 0 3 1 (-6) (-2)) (gv 10 0 (-9) (-3) 3 1) (by
    exact ⟨nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), nonZero_of_x (by norm_num [gv]), by gauss_arith, by gauss_arith, by gauss_arith⟩)
  have contradiction : (0 : ℚ) = 32 / 3 := by
    linear_combination ((-2) : ℚ) * t0 +
      (2 : ℚ) * t1 +
      ((-2) : ℚ) * t2 +
      (1 : ℚ) * t3 +
      ((-2) : ℚ) * t4 +
      ((-2) : ℚ) * t5 +
      ((-2) : ℚ) * t6 +
      ((-2) : ℚ) * t7 +
      ((-5) : ℚ) * t8 +
      (3 : ℚ) * t9 +
      (2 : ℚ) * t10 +
      ((-1) : ℚ) * t11 +
      (1 : ℚ) * t12 +
      (1 : ℚ) * t13 +
      (3 : ℚ) * t14 +
      ((-4) : ℚ) * t15 +
      (2 : ℚ) * t16 +
      (2 : ℚ) * t17 +
      ((-1) : ℚ) * t18 +
      (1 : ℚ) * t19 +
      ((-2) : ℚ) * t20 +
      (1 : ℚ) * t21 +
      ((-2) : ℚ) * t22 +
      (1 : ℚ) * t23 +
      ((-1) : ℚ) * t24 +
      ((-1) : ℚ) * t25 +
      ((-1) : ℚ) * t26 +
      ((-2) : ℚ) * t27 +
      (1 : ℚ) * t28 +
      ((-1) : ℚ) * t29 +
      ((-1) : ℚ) * t30 +
      (2 : ℚ) * t31 +
      (4 : ℚ) * t32 +
      ((-1) : ℚ) * t33 +
      ((-1) : ℚ) * t34 +
      ((-3) : ℚ) * t35 +
      ((-2) : ℚ) * t36 +
      ((-1) : ℚ) * t37 +
      ((-1) : ℚ) * t38 +
      ((-1) : ℚ) * t39 +
      (1 : ℚ) * t40 +
      ((-1) : ℚ) * t41 +
      (1 : ℚ) * t42 +
      ((-1) : ℚ) * t43 +
      (1 : ℚ) * t44 +
      ((-2) : ℚ) * t45 +
      (1 : ℚ) * t46 +
      (1 : ℚ) * t47 +
      (1 : ℚ) * t48 +
      ((-1) : ℚ) * t49 +
      ((-4) : ℚ) * t50 +
      (4 : ℚ) * t51 +
      (3 : ℚ) * t52 +
      ((-3) : ℚ) * t53 +
      (2 : ℚ) * t54 +
      ((-1) : ℚ) * t55 +
      ((-1) : ℚ) * t56 +
      ((-2) : ℚ) * t57 +
      (1 : ℚ) * t58 +
      ((-1) : ℚ) * t59 +
      ((-3) : ℚ) * t60 +
      ((-2) : ℚ) * t61 +
      (2 : ℚ) * t62 +
      ((-1) : ℚ) * t63 +
      (1 : ℚ) * t64 +
      (1 : ℚ) * t65 +
      ((-1) : ℚ) * t66 +
      (1 : ℚ) * t67 +
      ((-1) : ℚ) * t68 +
      (1 : ℚ) * t69 +
      ((-1) : ℚ) * t70 +
      (1 : ℚ) * t71 +
      ((-2) : ℚ) * t72 +
      ((-1) : ℚ) * t73 +
      (2 : ℚ) * t74 +
      (1 : ℚ) * t75 +
      (1 : ℚ) * t76 +
      ((-2) : ℚ) * t77 +
      ((-2) : ℚ) * t78 +
      ((-1) : ℚ) * t79 +
      (1 : ℚ) * t80 +
      ((-2) : ℚ) * t81 +
      (1 : ℚ) * t82 +
      ((-1) : ℚ) * t83 +
      (2 : ℚ) * t84 +
      ((-2) : ℚ) * t85 +
      ((-2) : ℚ) * t86 +
      (2 : ℚ) * t87 +
      ((-2) : ℚ) * t88 +
      (2 : ℚ) * t89 +
      (1 : ℚ) * t90 +
      ((-1) : ℚ) * t91 +
      (1 : ℚ) * t92 +
      ((-1) : ℚ) * t93 +
      (1 : ℚ) * t94 +
      ((-1) : ℚ) * t95 +
      ((-2) : ℚ) * t96 +
      (2 : ℚ) * t97 +
      ((-4) : ℚ) * t98 +
      (4 : ℚ) * t99 +
      (1 : ℚ) * t100 +
      (2 : ℚ) * t101 +
      ((-1) : ℚ) * t102 +
      (2 : ℚ) * t103 +
      ((-1) : ℚ) * t104 +
      (4 : ℚ) * t105 +
      (2 : ℚ) * t106 +
      (1 : ℚ) * t107 +
      ((-2) : ℚ) * t108 +
      ((-2) : ℚ) * t109 +
      ((-1) : ℚ) * t110 +
      (2 : ℚ) * t111 +
      ((-1) : ℚ) * t112 +
      (2 : ℚ) * t113 +
      (2 : ℚ) * t114 +
      ((-1) : ℚ) * t115 +
      ((-1) : ℚ) * t116 +
      (2 : ℚ) * t117 +
      (1 : ℚ) * t118 +
      (1 : ℚ) * t119 +
      ((-1) : ℚ) * t120 +
      ((-1) : ℚ) * t121 +
      ((-1) : ℚ) * t122 +
      ((-2) : ℚ) * t123 +
      (1 : ℚ) * t124 +
      ((-1) : ℚ) * t125 +
      ((-2) : ℚ) * t126 +
      (2 : ℚ) * t127 +
      (1 : ℚ) * t128 +
      (2 : ℚ) * t129 +
      ((-1) : ℚ) * t130 +
      ((-4) : ℚ) * t131 +
      (2 : ℚ) * t132 +
      ((-1) : ℚ) * t133 +
      ((-1) : ℚ) * t134 +
      (1 : ℚ) * t135 +
      (1 : ℚ) * t136 +
      ((-1) : ℚ) * t137 +
      (2 : ℚ) * t138 +
      ((-1) : ℚ) * t139 +
      (1 : ℚ) * t140 +
      ((-1) : ℚ) * t141 +
      (2 : ℚ) * t142 +
      ((-1) : ℚ) * t143 +
      ((-4) : ℚ) * t144 +
      (4 : ℚ) * t145 +
      (1 : ℚ) * t146 +
      ((-2) : ℚ) * t147 +
      (1 : ℚ) * t148 +
      (2 : ℚ) * t149 +
      (1 : ℚ) * t150 +
      ((-2) : ℚ) * t151 +
      ((-1) : ℚ) * t152 +
      ((-1) : ℚ) * t153 +
      (2 : ℚ) * t154 +
      ((-3) : ℚ) * t155 +
      (1 : ℚ) * t156 +
      ((-1) : ℚ) * t157 +
      (1 : ℚ) * t158 +
      ((-1) : ℚ) * t159 +
      ((-1) : ℚ) * t160 +
      (2 : ℚ) * t161 +
      ((-2) : ℚ) * t162 +
      (2 : ℚ) * t163 +
      ((-2) : ℚ) * t164 +
      (3 : ℚ) * t165 +
      ((-3) : ℚ) * t166 +
      ((-1) : ℚ) * t167 +
      (1 : ℚ) * t168 +
      ((-1) : ℚ) * t169 +
      ((-1) : ℚ) * t170 +
      ((-3) : ℚ) * t171 +
      ((-2) : ℚ) * t172 +
      ((-1) : ℚ) * t173 +
      (1 : ℚ) * t174 +
      (1 : ℚ) * t175 +
      ((-1) : ℚ) * t176 +
      (1 : ℚ) * t177 +
      (1 : ℚ) * t178 +
      (1 : ℚ) * t179 +
      ((-1) : ℚ) * t180 +
      (1 : ℚ) * t181 +
      (1 : ℚ) * t182 +
      (1 : ℚ) * t183 +
      (1 : ℚ) * t184 +
      ((-1) : ℚ) * t185 +
      ((-4) : ℚ) * t186 +
      ((-2) : ℚ) * t187 +
      (4 : ℚ) * t188 +
      ((-1) : ℚ) * t189 +
      (1 : ℚ) * t190 +
      (1 : ℚ) * t191 +
      ((-1) : ℚ) * t192 +
      (1 : ℚ) * t193 +
      (1 : ℚ) * t194 +
      ((-1) : ℚ) * t195 +
      (2 : ℚ) * t196 +
      ((-2) : ℚ) * t197 +
      (2 : ℚ) * t198 +
      (2 : ℚ) * t199 +
      ((-2) : ℚ) * t200 +
      (1 : ℚ) * t201 +
      (2 : ℚ) * t202 +
      (2 : ℚ) * t203 +
      (1 : ℚ) * t204 +
      ((-1) : ℚ) * t205 +
      (1 : ℚ) * t206 +
      (1 : ℚ) * t207 +
      (1 : ℚ) * t208 +
      (1 : ℚ) * t209 +
      (1 : ℚ) * r0 +
      (8 : ℚ) * r1 +
      ((-4) : ℚ) * r2 +
      (3 : ℚ) * r3 +
      (4 : ℚ) * r4 +
      ((-1) : ℚ) * r5 +
      (9 : ℚ) * r6 +
      (2 : ℚ) * r7 +
      ((-7) : ℚ) * r8 +
      (8 : ℚ) * r9 +
      (4 : ℚ) * r10 +
      ((-4) : ℚ) * r11 +
      ((-1) : ℚ) * r12 +
      (4 : ℚ) * r13 +
      (2 : ℚ) * r14 +
      ((-2) : ℚ) * r15 +
      (3 : ℚ) * r16 +
      (9 : ℚ) * r17 +
      ((-2) : ℚ) * r18
  norm_num at contradiction

/-- The exotic function on all rational rays has no signed extension to Q(i)^3. -/
theorem no_exotic_extension (f : GVec → ℚ) (hF : IsFrameFunction f)
    (hreal : ∀ a b c : ℤ, BornFinite.RationalRays.Vec3.IsRay ⟨a, b, c⟩ →
      f (gv a 0 b 0 c 0) = BornFinite.RationalRays.exotic ⟨a, b, c⟩) : False := by
  apply no_prescribed_frame_function f hF
  · have h := hreal 0 1 (-2) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 1 (-1) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 1 1 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 1 2 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 1 3 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 2 (-1) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 0 2 1 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 (-2) 0 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 (-2) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 (-1) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 0 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 1 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 2 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 0 3 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 1 2 0 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 2 (-1) 0 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 2 0 (-1) (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 2 0 1 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h
  · have h := hreal 2 1 0 (by norm_num [BornFinite.RationalRays.Vec3.IsRay])
    norm_num [BornFinite.RationalRays.exotic, BornFinite.RationalRays.sgn,
      BornFinite.RationalRays.pairSign] at h
    exact h

end BornFinite.GaussianExtension

#print axioms BornFinite.GaussianExtension.no_prescribed_frame_function
#print axioms BornFinite.GaussianExtension.no_exotic_extension
