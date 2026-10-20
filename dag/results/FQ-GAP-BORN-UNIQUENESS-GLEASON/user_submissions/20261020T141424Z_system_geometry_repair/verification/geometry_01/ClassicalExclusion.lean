import Mathlib.Analysis.Convex.Strict.Extreme
import Mathlib.Analysis.Convex.Exposed
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Tactic

/-! Concrete real geometry for classical exclusion. No reconstruction bridge is imported. -/
namespace FiniteQM.ClassicalExclusion
open Set Metric

variable {E F : Type*} [AddCommGroup E] [Module ℝ E]
  [AddCommGroup F] [Module ℝ F]

/-- Finite convex generation; includes every finite simplex, but does not assume independence. -/
def FinitePolytope (S : Set E) : Prop :=
  ∃ vertices : Set E, vertices.Finite ∧ S = convexHull ℝ vertices

/-- RC-L1: exact affine transport, including empty vertex sets. -/
theorem affine_image_finite_polytope (f : E →ᵃ[ℝ] F) {S : Set E}
    (h : FinitePolytope S) : FinitePolytope (f '' S) := by
  obtain ⟨v, hv, rfl⟩ := h
  exact ⟨f '' v, hv.image f, f.image_convexHull v⟩

/-- RC-L2: a section gives exactly the required image; no purity assumptions are used. -/
theorem image_eq_of_section {S : Set E} {T : Set F} (f : E → F)
    (maps : MapsTo f S T) (sectionMap : F → E)
    (section_mem : ∀ y ∈ T, sectionMap y ∈ S)
    (section_law : ∀ y ∈ T, f (sectionMap y) = y) : f '' S = T := by
  apply Subset.antisymm maps.image_subset
  intro y hy
  exact ⟨sectionMap y, section_mem y hy, section_law y hy⟩

/-- RC-L4: a finitely generated convex set has finitely many extreme points. -/
theorem finite_extremePoints {S : Set E} (h : FinitePolytope S) :
    (S.extremePoints ℝ).Finite := by
  obtain ⟨v, hv, rfl⟩ := h
  exact hv.subset extremePoints_convexHull_subset

abbrev R3 := EuclideanSpace ℝ (Fin 3)
def ball3 : Set R3 := closedBall 0 1

def circlePoint (t : ℝ) : R3 :=
  WithLp.toLp 2 ![(1 - t^2) / (1 + t^2), 2*t / (1 + t^2), 0]

theorem circlePoint_norm (t : ℝ) : ‖circlePoint t‖ = 1 := by
  have hd : 1 + t^2 ≠ 0 := by positivity
  have hs : ‖circlePoint t‖^2 = 1 := by
    rw [EuclideanSpace.real_norm_sq_eq]
    simp [circlePoint, Fin.sum_univ_succ]
    field_simp
    <;> ring
  nlinarith [norm_nonneg (circlePoint t)]

theorem circlePoint_recover (t : ℝ) :
    circlePoint t 1 / (1 + circlePoint t 0) = t := by
  have hd : 1 + t^2 ≠ 0 := by positivity
  have he : 1 + (1-t^2)/(1+t^2) = 2/(1+t^2) := by field_simp; ring
  change (2*t/(1+t^2)) / (1+(1-t^2)/(1+t^2)) = t
  rw [he]
  field_simp

/-- An explicit injection; restricting it to natural parameters already suffices. -/
theorem circlePoint_injective : Function.Injective circlePoint := by
  intro s t h
  have hs := circlePoint_recover s
  have ht := circlePoint_recover t
  rw [h] at hs
  exact hs.symm.trans ht

/-- RC-L3: infinitely many genuine extreme points of the real three-ball. -/
theorem ball3_infinite_extremePoints : (ball3.extremePoints ℝ).Infinite := by
  have hi : Function.Injective (fun n : ℕ => circlePoint (n : ℝ)) := by
    intro m n h
    exact_mod_cast circlePoint_injective h
  apply (Set.infinite_range_of_injective hi).mono
  rintro x ⟨n, rfl⟩
  apply StrictConvexSpace.sphere_subset_extremePoints_closedBall (0 : R3) one_ne_zero
  simpa [Metric.mem_sphere, dist_zero_right] using circlePoint_norm (n : ℝ)

/-- RC-L4 specialized to the qubit's Bloch ball; a geometric theorem, not a dimension count. -/
theorem ball3_not_finite_polytope : ¬ FinitePolytope ball3 := by
  intro h
  exact ball3_infinite_extremePoints.not_finite (finite_extremePoints h)

/-- RC-L5: any affine marginal onto the ball rules out a classical/polytope composite. -/
theorem no_polytope_with_ball_marginal {S : Set E} (marginal : E →ᵃ[ℝ] R3)
    (maps : MapsTo marginal S ball3) (sectionMap : R3 → E)
    (section_mem : ∀ b ∈ ball3, sectionMap b ∈ S)
    (section_law : ∀ b ∈ ball3, marginal (sectionMap b) = b) :
    ¬ FinitePolytope S := by
  intro h
  apply ball3_not_finite_polytope
  rw [← image_eq_of_section marginal maps sectionMap section_mem section_law]
  exact affine_image_finite_polytope marginal h

#print axioms affine_image_finite_polytope
#print axioms image_eq_of_section
#print axioms finite_extremePoints
#print axioms circlePoint_norm
#print axioms circlePoint_recover
#print axioms circlePoint_injective
#print axioms ball3_infinite_extremePoints
#print axioms ball3_not_finite_polytope
#print axioms no_polytope_with_ball_marginal
end FiniteQM.ClassicalExclusion