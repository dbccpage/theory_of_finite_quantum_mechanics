import AlgebraicHilbertBasisTransportContract
/-!
Algebraic GTMUR loss-ledger contract.

`AlgebraicHilbertBasisTransportContract` records an algebraic lift of a finite
Complex MUB family. This module packages the GTMUR-facing loss ledger that such
a lift must expose: complete basis and label profiles, vector and inner-product
evaluation loss zero, same-basis ZeroRel, and cross-basis squared-overlap
profiles.

This is still a contract surface. It does not construct a uniform
dimension-parametric GTMUR ledger over all odd prime powers, and it does not
compare all Omega representation regimes.
-/

namespace MUB

open scoped BigOperators

structure AlgebraicGtmurLossLedgerContract
    (F K ι B L : Type*) [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  transport : AlgebraicHilbertBasisTransportContract F K ι B L
  complete_basis_profile : Fintype.card B = Fintype.card ι + 1
  label_profile : Fintype.card L = Fintype.card ι
  vector_eval_loss_zero : ∀ b l x,
    transport.coefficientField.toComplex (transport.algebraicVector b l x) =
      transport.complexFamily.vector b l x
  inner_eval_loss_zero : ∀ b c u v,
    transport.coefficientField.toComplex
        (transport.algebraicInner (transport.algebraicVector b u)
          (transport.algebraicVector c v)) =
      finiteHilbertInner (transport.complexFamily.vector b u)
        (transport.complexFamily.vector c v)
  same_basis_zeroRel_loss_zero : ∀ b {u v : L}, u ≠ v ->
    transport.coefficientField.toComplex
        (transport.algebraicInner (transport.algebraicVector b u)
          (transport.algebraicVector b v)) = 0
  cross_basis_normSq_loss_zero : ∀ {b c : B}, b ≠ c -> ∀ u v,
    transport.coefficientField.toComplex
          (transport.algebraicInner (transport.algebraicVector b u)
            (transport.algebraicVector c v)) *
        star (transport.coefficientField.toComplex
          (transport.algebraicInner (transport.algebraicVector b u)
            (transport.algebraicVector c v))) =
      (Fintype.card ι : ℂ)⁻¹

namespace AlgebraicGtmurLossLedgerContract

theorem same_basis_zeroRel
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (G : AlgebraicGtmurLossLedgerContract F K ι B L)
    (b : B) {u v : L} (huv : u ≠ v) :
    G.transport.algebraicInner (G.transport.algebraicVector b u)
        (G.transport.algebraicVector b v) = 0 := by
  apply G.transport.coefficientField.toComplex_injective
  rw [map_zero]
  exact G.same_basis_zeroRel_loss_zero b huv

theorem cross_basis_unbiased_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (G : AlgebraicGtmurLossLedgerContract F K ι B L)
    {b c : B} (hbc : b ≠ c) (u v : L) :
    G.transport.coefficientField.toComplex
          (G.transport.algebraicInner (G.transport.algebraicVector b u)
            (G.transport.algebraicVector c v)) *
        star (G.transport.coefficientField.toComplex
          (G.transport.algebraicInner (G.transport.algebraicVector b u)
            (G.transport.algebraicVector c v))) =
      (Fintype.card ι : ℂ)⁻¹ :=
  G.cross_basis_normSq_loss_zero hbc u v

end AlgebraicGtmurLossLedgerContract

noncomputable def algebraicHilbertBasisTransportGtmurLossLedgerContract
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L) :
    AlgebraicGtmurLossLedgerContract F K ι B L where
  transport := T
  complete_basis_profile := T.basis_count
  label_profile := T.label_count
  vector_eval_loss_zero := T.vector_eval
  inner_eval_loss_zero := T.inner_eval
  same_basis_zeroRel_loss_zero := by
    intro b u v huv
    exact T.same_basis_zeroRel_eval b huv
  cross_basis_normSq_loss_zero := by
    intro b c hbc u v
    exact T.cross_basis_unbiased_eval hbc u v

theorem nonempty_algebraicGtmurLossLedgerContract_of_hilbertContract
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicHilbertBasisTransportContract F K ι B L) :
    Nonempty (AlgebraicGtmurLossLedgerContract F K ι B L) :=
  ⟨algebraicHilbertBasisTransportGtmurLossLedgerContract T⟩

end MUB

#print axioms MUB.AlgebraicGtmurLossLedgerContract.same_basis_zeroRel
#print axioms MUB.AlgebraicGtmurLossLedgerContract.cross_basis_unbiased_eval
#print axioms MUB.algebraicHilbertBasisTransportGtmurLossLedgerContract
#print axioms MUB.nonempty_algebraicGtmurLossLedgerContract_of_hilbertContract
