import ComplexCoefficientScalars
/-!
Algebraic coefficient-field contract.

The Complex scalar package proves the analytic scalar layer used by the
finite-function odd-prime-power construction. This file records the stronger
contract required before that layer can be promoted to an Omega coefficient
field: an algebraic field with an embedding into `ℂ`, a lifted primitive
additive character, and a lifted normalizer whose Complex evaluation matches
the existing scalar package.

This is a contract surface, not an existence theorem. It does not construct a
uniform field such as `Q(ζ_p, sqrt(p^k))`, and it does not prove that every
odd-prime-power Hilbert family has such a carrier.
-/

namespace MUB

structure AlgebraicCoefficientFieldContract
    (F K : Type*) [Field F] [Fintype F] [Field K] where
  complexScalars : ComplexCoefficientScalarPackage F
  toComplex : K →+* ℂ
  toComplex_injective : Function.Injective toComplex
  characterLift : AddChar F K
  characterLift_primitive : characterLift.IsPrimitive
  character_eval : ∀ x : F, toComplex (characterLift x) = complexScalars.character x
  normalizerLift : K
  normalizer_eval : toComplex normalizerLift = complexScalars.normalizer

namespace AlgebraicCoefficientFieldContract

theorem complex_character_primitive
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) :
    C.complexScalars.character.IsPrimitive :=
  C.complexScalars.primitive_character

theorem normalizerLift_eval_normSq
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) :
    star (C.toComplex C.normalizerLift) * C.toComplex C.normalizerLift =
      (Fintype.card F : ℂ)⁻¹ := by
  rw [C.normalizer_eval]
  exact C.complexScalars.normalizer_normSq

theorem characterLift_eval_zero
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) :
    C.toComplex (C.characterLift 0) = 1 := by
  rw [C.character_eval]
  exact AddChar.map_zero_eq_one C.complexScalars.character

theorem characterLift_eval_add
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) (x y : F) :
    C.toComplex (C.characterLift (x + y)) =
      C.toComplex (C.characterLift x) * C.toComplex (C.characterLift y) := by
  calc
    C.toComplex (C.characterLift (x + y)) =
        C.toComplex (C.characterLift x * C.characterLift y) := by
          rw [AddChar.map_add_eq_mul]
    _ = C.toComplex (C.characterLift x) *
        C.toComplex (C.characterLift y) := by
          exact map_mul C.toComplex (C.characterLift x) (C.characterLift y)

theorem characterLift_eq_of_eval_eq
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) {x y : F}
    (h :
      C.toComplex (C.characterLift x) =
        C.toComplex (C.characterLift y)) :
    C.characterLift x = C.characterLift y :=
  C.toComplex_injective h

end AlgebraicCoefficientFieldContract

theorem nonempty_complexCoefficientScalarPackage_of_algebraicContract
    {F K : Type*} [Field F] [Fintype F] [Field K]
    (C : AlgebraicCoefficientFieldContract F K) :
    Nonempty (ComplexCoefficientScalarPackage F) :=
  ⟨C.complexScalars⟩

end MUB

#print axioms MUB.AlgebraicCoefficientFieldContract.complex_character_primitive
#print axioms MUB.AlgebraicCoefficientFieldContract.normalizerLift_eval_normSq
#print axioms MUB.AlgebraicCoefficientFieldContract.characterLift_eval_zero
#print axioms MUB.AlgebraicCoefficientFieldContract.characterLift_eval_add
#print axioms MUB.AlgebraicCoefficientFieldContract.characterLift_eq_of_eval_eq
#print axioms MUB.nonempty_complexCoefficientScalarPackage_of_algebraicContract
