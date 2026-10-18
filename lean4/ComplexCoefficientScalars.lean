import HilbertPhaseNormalization
/-!
Complex coefficient scalar package.

The odd-prime-power Hilbert construction currently lives over `ℂ`: it uses a
primitive Complex additive character and the analytic `1 / sqrt(card F)`
normalizer. This module packages those scalar inputs and their exact norm
identity as a named Lean object.

This is a coefficient-field precursor, not the final coefficient-field theorem.
It does not construct a uniform algebraic field such as `Q(ζ_p, sqrt(p^k))`,
nor does it prove that all phase and normalizer scalars land in such a field.
-/

namespace MUB

structure ComplexCoefficientScalarPackage (F : Type*) [Field F] [Fintype F] where
  character : AddChar F ℂ
  primitive_character : character.IsPrimitive
  normalizer : ℂ
  normalizer_eq : normalizer = sqrtCardNormalizer F
  normalizer_normSq : star normalizer * normalizer = (Fintype.card F : ℂ)⁻¹

noncomputable def complexCoefficientScalarPackage
    (F : Type*) [Field F] [Fintype F] [DecidableEq F] :
    ComplexCoefficientScalarPackage F := by
  classical
  let ψ :=
    Classical.choose (finite_field_exists_primitive_complex_additive_character F)
  have hψ :=
    Classical.choose_spec (finite_field_exists_primitive_complex_additive_character F)
  exact {
    character := ψ
    primitive_character := hψ
    normalizer := sqrtCardNormalizer F
    normalizer_eq := rfl
    normalizer_normSq := sqrtCardNormalizer_star_mul F
  }

theorem exists_complexCoefficientScalarPackage
    (F : Type*) [Field F] [Fintype F] [DecidableEq F] :
    Nonempty (ComplexCoefficientScalarPackage F) :=
  ⟨complexCoefficientScalarPackage F⟩

end MUB

#print axioms MUB.complexCoefficientScalarPackage
#print axioms MUB.exists_complexCoefficientScalarPackage
