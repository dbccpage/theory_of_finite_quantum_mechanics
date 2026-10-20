import ReconstructionGeometry
import Mathlib.Analysis.Convex.Combination
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Normed.Affine.AddTorsorBases
import Mathlib.LinearAlgebra.AffineSpace.Midpoint

noncomputable section
namespace FiniteQM.CatalogueGeometry
open Set ReconstructionGeometry

/-- Affine maps preserve every two-term combination whose coefficients sum to one. -/
theorem affine_combo {n : ℕ} (f : Space n →ᵃ[ℝ] ℝ) (x y : Space n)
    (a b : ℝ) (hab : a + b = 1) :
    f (a • x + b • y) = a * f x + b * f y := by
  have ha : 1 - b = a := by linarith
  simpa [AffineMap.lineMap_apply_module, smul_eq_mul, ha] using f.apply_lineMap x y b

/-- A unique affine maximizer is an extreme point; convexity of S is not needed. -/
theorem extreme_of_unique_affine_max {n : ℕ} (S : Set (Space n))
    (f : Space n →ᵃ[ℝ] ℝ) (z : Space n) (hz : z ∈ S)
    (bound : ∀ x ∈ S, f x ≤ f z)
    (unique : ∀ x ∈ S, f x = f z → x = z) : z ∈ S.extremePoints ℝ := by
  refine ⟨hz, ?_⟩
  rintro x hx y hy ⟨a, b, ha, hb, hab, hxy⟩
  have h := affine_combo f x y a b hab
  rw [hxy] at h
  have hd : a * (f z - f x) + b * (f z - f y) = 0 := by
    calc
      _ = (a+b)*f z - (a*f x+b*f y) := by ring
      _ = 0 := by rw [hab, ← h]; ring
  have hn := mul_nonneg (le_of_lt hb) (sub_nonneg.mpr (bound y hy))
  have hn' := mul_nonneg (le_of_lt ha) (sub_nonneg.mpr (bound x hx))
  have hzero : a * (f z - f x) = 0 := by linarith
  have hxval : f x = f z := (sub_eq_zero.mp ((mul_eq_zero.mp hzero).resolve_left (ne_of_gt ha))).symm
  exact unique x hx hxval

/-- Central reflection of an affine functional about the origin. -/
theorem affine_reflection {n : ℕ} (f : Space n →ᵃ[ℝ] ℝ) (x : Space n) :
    f (-x) + f x = 2 * f 0 := by
  have h := f.map_midpoint x (-x)
  rw [midpoint_self_neg] at h
  simp only [midpoint_eq_smul_add, invOf_eq_inv, smul_eq_mul] at h
  linarith

/-- Any centrally symmetric normalized state set has capacity at most two under full affine
measurements. This bound does not assume purity, a Jordan representation, or a labelled rank. -/
theorem symmetric_frame_bound {n m : ℕ} (S : Set (Space n)) (zero_mem : (0 : Space n) ∈ S)
    (symmetric : ∀ x ∈ S, -x ∈ S) (f : Fin m → Space n) (hf : Frame S f) : m ≤ 2 := by
  obtain ⟨e, norm, delta⟩ := hf.distinguishable
  have bound : ∀ i, (1 : ℝ) ≤ 2 * (e i).functional 0 := by
    intro i
    have hm := (e i).nonnegative (-f i) (symmetric (f i) (hf.pure i).1)
    have h := affine_reflection (e i).functional (f i)
    have hd := delta i i
    simp at hd
    linarith
  have hs : (m : ℝ) ≤ 2 := by
    calc
      (m : ℝ) = ∑ i : Fin m, (1 : ℝ) := by simp
      _ ≤ ∑ i : Fin m, 2 * (e i).functional 0 := Finset.sum_le_sum fun i _ => bound i
      _ = 2 := by rw [← Finset.mul_sum, norm 0 zero_mem]; ring
  exact_mod_cast hs

#print axioms affine_combo
#print axioms extreme_of_unique_affine_max
#print axioms affine_reflection
#print axioms symmetric_frame_bound
end FiniteQM.CatalogueGeometry