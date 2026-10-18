import AlgebraicCoefficientFieldContract
import HilbertMubStructure
/-!
Algebraic Hilbert-basis transport contract.

The finite-function MUB family is currently proved over `ℂ`. This module
records the contract required to lift that family to an algebraic coefficient
field `K`: algebraic vectors, an algebraic inner-product operation, and exact
evaluation equations into the Complex family.

This is not the dimension-parametric transport theorem. It does not construct
the algebraic vectors, prove their existence for all odd prime powers, or close
the GTMUR loss ledger. It only fixes the object-level obligations that a future
transport theorem must satisfy.
-/

namespace MUB

open scoped BigOperators

structure AlgebraicHilbertBasisTransportContract
    (F K ι B L : Type*) [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  coefficientField : AlgebraicCoefficientFieldContract F K
  complexFamily : FiniteComplexMubFamily ι B L
  algebraicVector : B -> L -> ι -> K
  vector_eval : ∀ b l x,
    coefficientField.toComplex (algebraicVector b l x) =
      complexFamily.vector b l x
  algebraicInner : (ι -> K) -> (ι -> K) -> K
  inner_eval : ∀ b c u v,
    coefficientField.toComplex
        (algebraicInner (algebraicVector b u) (algebraicVector c v)) =
      finiteHilbertInner (complexFamily.vector b u) (complexFamily.vector c v)

namespace AlgebraicHilbertBasisTransportContract

theorem basis_count
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L) :
    Fintype.card B = Fintype.card ι + 1 :=
  T.complexFamily.basis_count

theorem label_count
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L) :
    Fintype.card L = Fintype.card ι :=
  T.complexFamily.label_count

theorem same_basis_inner_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L)
    (b : B) (u v : L) :
    T.coefficientField.toComplex
        (T.algebraicInner (T.algebraicVector b u)
          (T.algebraicVector b v)) =
      if u = v then 1 else 0 := by
  rw [T.inner_eval]
  exact T.complexFamily.same_basis_inner b u v

theorem same_basis_zeroRel_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L)
    (b : B) {u v : L} (huv : u ≠ v) :
    T.coefficientField.toComplex
        (T.algebraicInner (T.algebraicVector b u)
          (T.algebraicVector b v)) = 0 := by
  simpa [huv] using T.same_basis_inner_eval b u v

theorem cross_basis_unbiased_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L)
    {b c : B} (hbc : b ≠ c) (u v : L) :
    T.coefficientField.toComplex
          (T.algebraicInner (T.algebraicVector b u)
            (T.algebraicVector c v)) *
        star (T.coefficientField.toComplex
          (T.algebraicInner (T.algebraicVector b u)
            (T.algebraicVector c v))) =
      (Fintype.card ι : ℂ)⁻¹ := by
  rw [T.inner_eval]
  exact T.complexFamily.cross_basis_unbiased hbc u v

theorem algebraicVector_eq_zero_of_eval_zero
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L)
    {b : B} {l : L} {x : ι} (h : T.complexFamily.vector b l x = 0) :
    T.algebraicVector b l x = 0 :=
  T.coefficientField.toComplex_injective (by
    rw [T.vector_eval, h, map_zero])

end AlgebraicHilbertBasisTransportContract

theorem nonempty_finiteComplexMubFamily_of_algebraicHilbertContract
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L) :
    Nonempty (FiniteComplexMubFamily ι B L) :=
  ⟨T.complexFamily⟩

end MUB

#print axioms MUB.AlgebraicHilbertBasisTransportContract.basis_count
#print axioms MUB.AlgebraicHilbertBasisTransportContract.label_count
#print axioms MUB.AlgebraicHilbertBasisTransportContract.same_basis_inner_eval
#print axioms MUB.AlgebraicHilbertBasisTransportContract.same_basis_zeroRel_eval
#print axioms MUB.AlgebraicHilbertBasisTransportContract.cross_basis_unbiased_eval
#print axioms MUB.AlgebraicHilbertBasisTransportContract.algebraicVector_eq_zero_of_eval_zero
#print axioms MUB.nonempty_finiteComplexMubFamily_of_algebraicHilbertContract
