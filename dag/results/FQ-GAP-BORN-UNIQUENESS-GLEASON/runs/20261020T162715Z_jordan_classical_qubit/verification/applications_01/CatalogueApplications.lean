import SupportedJordanCatalogue
import JordanConeSquares

/-! Concrete vertical slices connecting the new models to the earlier exclusion theorem
and to their actual Jordan-square state cones. No classification bridge is used. -/
noncomputable section
namespace FiniteQM.CatalogueApplications
open ReconstructionGeometry ClassicalExclusion ConcreteJordanProducts JordanConeSquares

/-- A system with a qubit marginal cannot itself be any finite classical simplex. -/
theorem no_classical_composite (n k : ℕ) :
    ¬ Nonempty (Composite (ClassicalModel.system n) QubitModel.system (ClassicalModel.system k)) := by
  rintro ⟨C⟩
  exact C.no_polytope_composite_with_ball (AffineEquiv.refl ℝ (Space 3)) QubitModel.state_chart
    (ClassicalModel.finite_polytope k)

/-- Classical states are exactly trace-one Jordan squares in probability coordinates. -/
theorem classical_states_are_normalized_squares (n : ℕ) (x : Space n) :
    x ∈ (ClassicalModel.system n).states ↔
      (∃ b, classicalMul b b = (ClassicalModel.basis n).coords x) ∧
        classicalTrace ((ClassicalModel.basis n).coords x) = 1 := by
  rw [← classical_positive_iff_square]
  change x ∈ ClassicalModel.states n ↔ _
  simp only [ClassicalModel.states, (ClassicalModel.basis n).convexHull_eq_nonneg_coord,
    Set.mem_setOf_eq, classicalPositive, classicalTrace, AffineBasis.coords_apply,
    (ClassicalModel.basis n).sum_coord_apply_eq_one, and_true]

/-- Qubit states are exactly the Jordan squares of trace-one Bloch spin elements. -/
theorem qubit_states_are_normalized_squares (x : Space 3) :
    x ∈ QubitModel.system.states ↔ ∃ b, spinMul b b = blochState x := by
  calc
    x ∈ QubitModel.system.states ↔ ‖x‖ ≤ 1 := by
      simp [QubitModel.system, ball3, Metric.mem_closedBall, dist_zero_right]
    _ ↔ spinPositive (blochState x) := (bloch_positive_iff x).symm
    _ ↔ ∃ b, spinMul b b = blochState x := spin_positive_iff_square _

#print axioms no_classical_composite
#print axioms classical_states_are_normalized_squares
#print axioms qubit_states_are_normalized_squares
end FiniteQM.CatalogueApplications