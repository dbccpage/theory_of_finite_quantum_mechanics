import Mathlib.LinearAlgebra.Dimension.DivisionRing
import Mathlib.Algebra.Field.Rat

/-! AuthorityEffect: None. The admitted carrier's quotient dimension and
natural-number subtraction bounds. Certified matrix-rank correspondence and
the cochain zero-product/homology relation are checked in separate models.
This does not assume a value for the quotient dimension or certify metadata.
-/
namespace TFQM.CarrierDimensions

theorem quotient_dimension {V₀ V₁ : Type} [AddCommGroup V₀] [AddCommGroup V₁]
    [Module ℚ V₀] [Module ℚ V₁] [Module.Finite ℚ V₁] (map : V₀ →ₗ[ℚ] V₁) :
    Module.finrank ℚ (V₁ ⧸ LinearMap.range map) =
      Module.finrank ℚ V₁ - Module.finrank ℚ (LinearMap.range map) :=
  Submodule.finrank_quotient (LinearMap.range map)

theorem admitted_subtraction_bounds (dimension lowerRank upperRank : Nat)
    (upperBound : upperRank ≤ dimension)
    (inclusion : lowerRank ≤ dimension - upperRank) :
    upperRank + lowerRank ≤ dimension ∧
      (dimension - upperRank - lowerRank) + lowerRank + upperRank = dimension ∧
      (dimension - lowerRank) + lowerRank = dimension := by
  omega

#print axioms quotient_dimension
#print axioms admitted_subtraction_bounds

end TFQM.CarrierDimensions
