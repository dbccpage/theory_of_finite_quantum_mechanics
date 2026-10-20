import CatalogueGeometry

/-! Qubit state model as the real three-ball. Capacity is established from affine measurements,
not assigned without proof. This file does not identify the ball with Hermitian complex matrices. -/
noncomputable section
namespace FiniteQM.QubitModel
open Set Metric ReconstructionGeometry ClassicalExclusion CatalogueGeometry

/-- The two-outcome test along a unit Bloch vector, as an actual affine functional. -/
def axisFunctional (u : Space 3) : Space 3 →ᵃ[ℝ] ℝ :=
  (1/2 : ℝ) • (AffineMap.const ℝ (Space 3) 1 + (innerSL ℝ u).toLinearMap.toAffineMap)

theorem axisFunctional_apply (u x : Space 3) :
    axisFunctional u x = (1 + inner ℝ u x)/2 := by
  simp [axisFunctional]
  ring

theorem inner_bounds {u x : Space 3} (hu : ‖u‖ = 1) (hx : x ∈ ball3) :
    -1 ≤ inner ℝ u x ∧ inner ℝ u x ≤ 1 := by
  have hn : ‖x‖ ≤ 1 := by simpa [ball3, mem_closedBall, dist_zero_right] using hx
  have h := abs_real_inner_le_norm u x
  rw [hu, one_mul] at h
  have h' := abs_le.mp (h.trans hn)
  exact h'

def axisEffect (u : Space 3) (hu : ‖u‖ = 1) : Effect ball3 where
  functional := axisFunctional u
  nonnegative := by intro x hx; rw [axisFunctional_apply]; linarith [(inner_bounds hu hx).1]
  bounded := by intro x hx; rw [axisFunctional_apply]; linarith [(inner_bounds hu hx).2]

theorem unit_ne_neg {u : Space 3} (hu : ‖u‖ = 1) : u ≠ -u := by
  intro h
  have h' := congrArg (fun x => inner ℝ u x) h
  have hbad : (1 : ℝ) = -1 := by simpa [hu] using h'
  linarith

/-- Every antipodal pair is a perfectly distinguishable pure frame. -/
theorem unit_pair_frame (u : Space 3) (hu : ‖u‖ = 1) : Frame ball3 ![u, -u] := by
  have hne := unit_ne_neg hu
  refine ⟨?_, ?_, ?_⟩
  · intro i j h
    fin_cases i <;> fin_cases j <;> simp_all
  · intro i
    fin_cases i
    · exact (unit_isExposed hu).isExtreme.mem_extremePoints
    · exact (unit_isExposed (by simpa using hu : ‖-u‖ = 1)).isExtreme.mem_extremePoints
  · refine ⟨fun i => if i = 0 then axisEffect u hu else axisEffect (-u) (by simpa using hu), ?_, ?_⟩
    · intro x hx
      simp [Fin.sum_univ_two, axisEffect, axisFunctional_apply]
      ring
    · intro i j
      fin_cases i <;> fin_cases j <;>
        simp [axisEffect, axisFunctional_apply, hu]

theorem frame_bound {m : ℕ} (f : Fin m → Space 3) (hf : Frame ball3 f) : m ≤ 2 := by
  apply symmetric_frame_bound ball3 (by simp [ball3]) (fun x hx => ?_) f hf
  simpa [ball3, mem_closedBall, dist_zero_right] using hx

def system : System 3 where
  states := ball3
  nonempty := ⟨0, by simp [ball3]⟩
  convex := convex_closedBall 0 1
  compact := isCompact_closedBall 0 1
  full := by
    have hb : affineSpan ℝ (Metric.ball (0 : Space 3) 1) = ⊤ :=
      isOpen_ball.affineSpan_eq_top (Metric.nonempty_ball.mpr (by norm_num))
    apply top_unique
    calc
      ⊤ = affineSpan ℝ (Metric.ball (0 : Space 3) 1) := hb.symm
      _ ≤ affineSpan ℝ ball3 := affineSpan_mono ℝ ball_subset_closedBall
  rank := 2
  rank_pos := by decide
  frame_bound := fun _ f hf => frame_bound f hf
  frame_attained := ⟨![circlePoint 0, -circlePoint 0], unit_pair_frame _ (circlePoint_norm 0)⟩

theorem rank_eq : system.rank = 2 := rfl
theorem dim_eq : system.dim = 4 := rfl
theorem state_chart : (AffineEquiv.refl ℝ (Space 3)) '' system.states = ball3 := by simp [system]

/-- Exact diameter mixing with admissible coefficients, including r=1, r=-1 and r=0. -/
theorem diameter_mem (u : Space 3) (r : ℝ) (hr0 : -1 ≤ r) (hr1 : r ≤ 1) :
    r • u ∈ convexHull ℝ (range ![u, -u]) := by
  have hu : u ∈ convexHull ℝ (range ![u, -u]) := subset_convexHull ℝ _ ⟨0, rfl⟩
  have hn : -u ∈ convexHull ℝ (range ![u, -u]) := subset_convexHull ℝ _ ⟨1, rfl⟩
  have h := (convex_convexHull ℝ (range ![u,-u])) hu hn
    (a := (1+r)/2) (b := (1-r)/2) (by linarith) (by linarith) (by ring)
  have heq : ((1+r)/2) • u + ((1-r)/2) • (-u) = r • u := by module
  rwa [heq] at h

theorem spectral : system.Spectral := by
  intro x hx
  by_cases hz : x = 0
  · subst x
    refine ⟨2, ![circlePoint 0, -circlePoint 0], unit_pair_frame _ (circlePoint_norm 0), ?_⟩
    simpa using diameter_mem (circlePoint 0) 0 (by norm_num) (by norm_num)
  · have hn : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hz
    let u : Space 3 := ‖x‖⁻¹ • x
    have hu : ‖u‖ = 1 := by simp [u, norm_smul, abs_inv, abs_norm, hn]
    refine ⟨2, ![u,-u], unit_pair_frame u hu, ?_⟩
    have hxnorm : ‖x‖ ≤ 1 := by simpa [system, ball3, mem_closedBall, dist_zero_right] using hx
    have h := diameter_mem u ‖x‖ (by linarith [norm_nonneg x]) hxnorm
    have heq : ‖x‖ • u = x := by simp [u, smul_smul, hn]
    rwa [heq] at h

theorem pure_eq_sphere : system.states.extremePoints ℝ = Metric.sphere 0 1 :=
  StrictConvexSpace.extremePoints_closedBall_eq_sphere

#print axioms pure_eq_sphere
#print axioms axisFunctional_apply
#print axioms inner_bounds
#print axioms axisEffect
#print axioms unit_ne_neg
#print axioms unit_pair_frame
#print axioms frame_bound
#print axioms system
#print axioms rank_eq
#print axioms dim_eq
#print axioms state_chart
#print axioms diameter_mem
#print axioms spectral
end FiniteQM.QubitModel