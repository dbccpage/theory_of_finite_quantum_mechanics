import AlgebraicGtmurLossLedgerContract
/-!
Algebraic terminalizer-preservation contract.

`AlgebraicGtmurLossLedgerContract` records the lifted Hilbert/GTMUR loss
profile under Complex evaluation. This module packages the terminalizer-facing
part of that profile: complete basis and label counts, terminal inner-product
evaluation, same-basis ZeroRel, and cross-basis squared-overlap preservation.

This is still only a contract surface. It does not construct a uniform
coefficient-field family, dimension-parametric Hilbert-basis transport, or a
terminalizer-preservation theorem over every odd prime power.
-/

namespace MUB

open scoped BigOperators

structure AlgebraicTerminalizerPreservationContract
    (F K ι B L : Type*) [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  ledger : AlgebraicGtmurLossLedgerContract F K ι B L
  terminal_complete_basis_profile : Fintype.card B = Fintype.card ι + 1
  terminal_label_profile : Fintype.card L = Fintype.card ι
  terminal_inner_eval_preserved : ∀ b c u v,
    ledger.transport.coefficientField.toComplex
        (ledger.transport.algebraicInner (ledger.transport.algebraicVector b u)
          (ledger.transport.algebraicVector c v)) =
      finiteHilbertInner (ledger.transport.complexFamily.vector b u)
        (ledger.transport.complexFamily.vector c v)
  terminal_same_basis_zeroRel : ∀ b {u v : L}, u ≠ v ->
    ledger.transport.algebraicInner (ledger.transport.algebraicVector b u)
        (ledger.transport.algebraicVector b v) = 0
  terminal_cross_basis_normSq_eval : ∀ {b c : B}, b ≠ c -> ∀ u v,
    ledger.transport.coefficientField.toComplex
          (ledger.transport.algebraicInner (ledger.transport.algebraicVector b u)
            (ledger.transport.algebraicVector c v)) *
        star (ledger.transport.coefficientField.toComplex
          (ledger.transport.algebraicInner (ledger.transport.algebraicVector b u)
            (ledger.transport.algebraicVector c v))) =
      (Fintype.card ι : ℂ)⁻¹

namespace AlgebraicTerminalizerPreservationContract

theorem same_basis_zeroRel
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicTerminalizerPreservationContract F K ι B L)
    (b : B) {u v : L} (huv : u ≠ v) :
    T.ledger.transport.algebraicInner (T.ledger.transport.algebraicVector b u)
        (T.ledger.transport.algebraicVector b v) = 0 :=
  T.terminal_same_basis_zeroRel b huv

theorem same_basis_zeroRel_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicTerminalizerPreservationContract F K ι B L)
    (b : B) {u v : L} (huv : u ≠ v) :
    T.ledger.transport.coefficientField.toComplex
        (T.ledger.transport.algebraicInner
          (T.ledger.transport.algebraicVector b u)
          (T.ledger.transport.algebraicVector b v)) = 0 := by
  rw [T.same_basis_zeroRel b huv, map_zero]

theorem cross_basis_unbiased_eval
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (T : AlgebraicTerminalizerPreservationContract F K ι B L)
    {b c : B} (hbc : b ≠ c) (u v : L) :
    T.ledger.transport.coefficientField.toComplex
          (T.ledger.transport.algebraicInner (T.ledger.transport.algebraicVector b u)
            (T.ledger.transport.algebraicVector c v)) *
        star (T.ledger.transport.coefficientField.toComplex
          (T.ledger.transport.algebraicInner (T.ledger.transport.algebraicVector b u)
            (T.ledger.transport.algebraicVector c v))) =
      (Fintype.card ι : ℂ)⁻¹ :=
  T.terminal_cross_basis_normSq_eval hbc u v

end AlgebraicTerminalizerPreservationContract

noncomputable def algebraicGtmurTerminalizerPreservationContract
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (G : AlgebraicGtmurLossLedgerContract F K ι B L) :
    AlgebraicTerminalizerPreservationContract F K ι B L where
  ledger := G
  terminal_complete_basis_profile := G.complete_basis_profile
  terminal_label_profile := G.label_profile
  terminal_inner_eval_preserved := G.inner_eval_loss_zero
  terminal_same_basis_zeroRel := by
    intro b u v huv
    exact AlgebraicGtmurLossLedgerContract.same_basis_zeroRel G b huv
  terminal_cross_basis_normSq_eval := by
    intro b c hbc u v
    exact G.cross_basis_normSq_loss_zero hbc u v

theorem nonempty_algebraicTerminalizerPreservationContract_of_gtmurContract
    {F K ι B L : Type*} [Field F] [Fintype F] [Field K]
    [Fintype ι] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L]
    (G : AlgebraicGtmurLossLedgerContract F K ι B L) :
    Nonempty (AlgebraicTerminalizerPreservationContract F K ι B L) :=
  ⟨algebraicGtmurTerminalizerPreservationContract G⟩

end MUB

#print axioms MUB.AlgebraicTerminalizerPreservationContract.same_basis_zeroRel
#print axioms MUB.AlgebraicTerminalizerPreservationContract.same_basis_zeroRel_eval
#print axioms MUB.AlgebraicTerminalizerPreservationContract.cross_basis_unbiased_eval
#print axioms MUB.algebraicGtmurTerminalizerPreservationContract
#print axioms MUB.nonempty_algebraicTerminalizerPreservationContract_of_gtmurContract
