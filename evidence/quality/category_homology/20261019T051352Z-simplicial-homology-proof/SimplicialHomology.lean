import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.Algebra.Field.Rat

/-! AuthorityEffect: None. The rational homology quotient and Betti formula.
The zero-composition premise is established separately by signed-face pairing.
Dimensions of the concrete matrices require the source/basis correspondence;
returned ranks require the separate split-map certificate theorem. No Rust/MIR
extraction, integral torsion computation or allocator-totality claim is made.
-/
namespace TFQM.SimplicialHomology

variable {V₀ V₁ V₂ : Type}
  [AddCommGroup V₀] [AddCommGroup V₁] [AddCommGroup V₂]
  [Module ℚ V₀] [Module ℚ V₁] [Module ℚ V₂]
  [FiniteDimensional ℚ V₁]

omit [FiniteDimensional ℚ V₁] in
theorem range_in_cycles (lower : V₁ →ₗ[ℚ] V₀) (upper : V₂ →ₗ[ℚ] V₁)
    (square : lower.comp upper = 0) : LinearMap.range upper ≤ LinearMap.ker lower := by
  rintro value ⟨preimage, rfl⟩
  change lower (upper preimage) = 0
  exact LinearMap.congr_fun square preimage

theorem rank_sum_bound (lower : V₁ →ₗ[ℚ] V₀) (upper : V₂ →ₗ[ℚ] V₁)
    (square : lower.comp upper = 0) :
    Module.finrank ℚ (LinearMap.range lower) + Module.finrank ℚ (LinearMap.range upper) ≤
      Module.finrank ℚ V₁ := by
  have inclusion := Submodule.finrank_mono (range_in_cycles lower upper square)
  have dimensions := LinearMap.finrank_range_add_finrank_ker lower
  omega

theorem betti_dimension (lower : V₁ →ₗ[ℚ] V₀) (upper : V₂ →ₗ[ℚ] V₁)
    (square : lower.comp upper = 0) :
    Module.finrank ℚ ((LinearMap.ker lower) ⧸
      (LinearMap.range upper).comap (LinearMap.ker lower).subtype) =
      Module.finrank ℚ V₁ - Module.finrank ℚ (LinearMap.range lower) -
        Module.finrank ℚ (LinearMap.range upper) := by
  have inside := Submodule.comapSubtypeEquivOfLe (range_in_cycles lower upper square)
  have same_dimension := inside.finrank_eq
  rw [Submodule.finrank_quotient, same_dimension]
  have dimensions := LinearMap.finrank_range_add_finrank_ker lower
  omega

#print axioms range_in_cycles
#print axioms rank_sum_bound
#print axioms betti_dimension

end TFQM.SimplicialHomology
