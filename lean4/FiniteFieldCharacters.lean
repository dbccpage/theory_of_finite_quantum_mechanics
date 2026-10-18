import AdditiveCharacter
import Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality
import Mathlib.NumberTheory.LegendreSymbol.AddCharacter

/-!
Finite-field additive-character orthogonality for the MUB run.

The odd-prime-power Weyl route needs a dimension-parametric theorem saying
nontrivial additive characters cancel over finite fields, and primitive
characters give the expected linear orthogonality relation. This module records
that step against mathlib's `AddChar` API. It still does not prove the
quadratic Gauss-norm theorem or construct the Hilbert/GTMUR family.
-/

namespace MUB

open scoped BigOperators

theorem finite_additive_character_sum_zero_of_ne_one
    {A R : Type*} [AddGroup A] [Fintype A] [CommRing R] [IsDomain R]
    (ψ : AddChar A R) (hψ : ψ ≠ 1) :
    (∑ x : A, ψ x) = 0 := by
  exact AddChar.sum_eq_zero_of_ne_one hψ

theorem finite_field_additive_character_sum_zero_from_nontrivial_value
    {F R : Type*} [Field F] [Fintype F] [Field R]
    (ψ : AddChar F R) {a : F} (ha : ψ a ≠ 1) :
    (∑ x : F, ψ x) = 0 := by
  refine finite_character_sum_vanishes_from_nontrivial_translation
    (Equiv.addLeft a) ψ (ψ a) ?_ ha
  intro x
  exact AddChar.map_add_eq_mul ψ a x

theorem finite_field_nontrivial_additive_character_is_primitive
    {F R : Type*} [Field F] [CommMonoid R]
    (ψ : AddChar F R) (hψ : ψ ≠ 1) :
    ψ.IsPrimitive := by
  exact AddChar.IsPrimitive.of_ne_one hψ

theorem finite_field_exists_nontrivial_complex_additive_character
    (F : Type*) [Field F] [Fintype F] :
    ∃ ψ : AddChar F ℂ, ψ ≠ 1 := by
  classical
  rcases (AddChar.exists_apply_ne_zero (α := F) (a := (1 : F))).2
      (one_ne_zero : (1 : F) ≠ 0) with
    ⟨ψ, hψ⟩
  refine ⟨ψ, fun htrivial => hψ ?_⟩
  rw [htrivial]
  rfl

theorem finite_field_exists_primitive_complex_additive_character
    (F : Type*) [Field F] [Fintype F] :
    ∃ ψ : AddChar F ℂ, ψ.IsPrimitive := by
  rcases finite_field_exists_nontrivial_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, finite_field_nontrivial_additive_character_is_primitive ψ hψ⟩

theorem finite_field_primitive_additive_character_linear_orthogonality
    {F R : Type*} [Field F] [Fintype F] [DecidableEq F]
    [CommRing R] [IsDomain R]
    (ψ : AddChar F R) (hψ : ψ.IsPrimitive) (b : F) :
    (∑ x : F, ψ (x * b)) = if b = 0 then Fintype.card F else 0 := by
  exact AddChar.sum_mulShift b hψ

theorem finite_field_nontrivial_additive_character_linear_orthogonality
    {F R : Type*} [Field F] [Fintype F] [DecidableEq F]
    [CommRing R] [IsDomain R]
    (ψ : AddChar F R) (hψ : ψ ≠ 1) (b : F) :
    (∑ x : F, ψ (x * b)) = if b = 0 then Fintype.card F else 0 := by
  exact AddChar.sum_mulShift b
    (finite_field_nontrivial_additive_character_is_primitive ψ hψ)

end MUB

#print axioms MUB.finite_additive_character_sum_zero_of_ne_one
#print axioms MUB.finite_field_additive_character_sum_zero_from_nontrivial_value
#print axioms MUB.finite_field_nontrivial_additive_character_is_primitive
#print axioms MUB.finite_field_exists_nontrivial_complex_additive_character
#print axioms MUB.finite_field_exists_primitive_complex_additive_character
#print axioms MUB.finite_field_primitive_additive_character_linear_orthogonality
#print axioms MUB.finite_field_nontrivial_additive_character_linear_orthogonality
