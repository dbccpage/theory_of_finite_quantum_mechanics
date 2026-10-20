import ClassicalExclusion

/-! The unary affine-substitution fragment used by the collected operation records.
These are real equations on affine image operations; a full many-arity operad is not asserted. -/
namespace FiniteQM.ConvexSubstitution
open Set ClassicalExclusion
variable {E F G H : Type*}
  [AddCommGroup E] [Module ℝ E] [AddCommGroup F] [Module ℝ F]
  [AddCommGroup G] [Module ℝ G] [AddCommGroup H] [Module ℝ H]

theorem image_unit (S : Set E) : (AffineMap.id ℝ E) '' S = S := by simp

theorem image_substitution (f : E →ᵃ[ℝ] F) (g : F →ᵃ[ℝ] G) (S : Set E) :
    (g.comp f) '' S = g '' (f '' S) := by rw [Set.image_image]; rfl

theorem image_associativity (f : E →ᵃ[ℝ] F) (g : F →ᵃ[ℝ] G)
    (h : G →ᵃ[ℝ] H) (S : Set E) :
    ((h.comp g).comp f) '' S = (h.comp (g.comp f)) '' S := rfl

theorem finite_polytope_substitution (f : E →ᵃ[ℝ] F) (g : F →ᵃ[ℝ] G)
    {S : Set E} (h : FinitePolytope S) : FinitePolytope ((g.comp f) '' S) := by
  rw [image_substitution]
  exact affine_image_finite_polytope g (affine_image_finite_polytope f h)

#print axioms image_unit
#print axioms image_substitution
#print axioms image_associativity
#print axioms finite_polytope_substitution
end FiniteQM.ConvexSubstitution