import FiniteFunctionGtmurLedger
/-!
Finite-function terminalizer ledger for coordinate-equivalence transport.

The GTMUR coordinate ledger proves lossless reindexing of finite-function
Hilbert inner products. This file packages the terminalizer boundary that is
available at that same finite-function level: the complete basis count, label
count, exact inner-product profile, ZeroRel boundary, and squared-overlap
profile are preserved by coordinate equivalence.

This remains deliberately narrower than the Omega terminalizer theorem. It does
not compare different representation regimes, construct algebraic coefficient
fields, or prove dimension-parametric terminalizer preservation across all
prime-power schemas. It records only the coordinate-transport terminalizer
ledger that a stronger theorem must extend.
-/

namespace MUB

open scoped BigOperators

structure FiniteFunctionTerminalizerLedger (α β B L : Type*) [Fintype α]
    [Fintype β] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  gtmur : FiniteFunctionGtmurLedger α β B L
  source_complete_basis_count : Fintype.card B = Fintype.card α + 1
  target_complete_basis_count : Fintype.card B = Fintype.card β + 1
  source_label_count : Fintype.card L = Fintype.card α
  target_label_count : Fintype.card L = Fintype.card β
  coordinate_card_preserved : Fintype.card β = Fintype.card α
  terminal_inner_profile_preserved : ∀ b c u v,
    finiteHilbertInner (gtmur.target.vector b u) (gtmur.target.vector c v) =
      finiteHilbertInner (gtmur.source.vector b u) (gtmur.source.vector c v)
  terminal_zeroRel_preserved : ∀ b c u v,
    finiteHilbertInner (gtmur.source.vector b u) (gtmur.source.vector c v) = 0 ->
      finiteHilbertInner (gtmur.target.vector b u) (gtmur.target.vector c v) = 0
  terminal_normSq_profile_preserved : ∀ b c u v,
    finiteHilbertInner (gtmur.target.vector b u) (gtmur.target.vector c v) *
        star (finiteHilbertInner (gtmur.target.vector b u) (gtmur.target.vector c v)) =
      finiteHilbertInner (gtmur.source.vector b u) (gtmur.source.vector c v) *
        star (finiteHilbertInner (gtmur.source.vector b u) (gtmur.source.vector c v))

noncomputable def coordinateTransportFiniteFunctionTerminalizerLedger
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (source : FiniteComplexMubFamily α B L) :
    FiniteFunctionTerminalizerLedger α β B L where
  gtmur := coordinateTransportFiniteFunctionGtmurLedger e source
  source_complete_basis_count := source.basis_count
  target_complete_basis_count := (source.transport e).basis_count
  source_label_count := source.label_count
  target_label_count := (source.transport e).label_count
  coordinate_card_preserved :=
    (coordinateTransportFiniteFunctionGtmurLedger e source).coordinate_card_preserved
  terminal_inner_profile_preserved := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionGtmurLedger e source).inner_preserved b c u v
  terminal_zeroRel_preserved := by
    intro b c u v hzero
    exact (coordinateTransportFiniteFunctionGtmurLedger e source).zeroRel_preserved b c u v hzero
  terminal_normSq_profile_preserved := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionGtmurLedger e source).normSq_preserved b c u v

noncomputable def finiteFieldCoordinateTerminalizerLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    FiniteFunctionTerminalizerLedger F β (Option F) F :=
  coordinateTransportFiniteFunctionTerminalizerLedger e
    (finiteFieldComplexMubFamily ψ hψ hchar h2)

theorem exists_finiteFieldCoordinateTerminalizerLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteFunctionTerminalizerLedger F β (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨finiteFieldCoordinateTerminalizerLedger e ψ hψ hchar h2⟩⟩

end MUB

#print axioms MUB.coordinateTransportFiniteFunctionTerminalizerLedger
#print axioms MUB.finiteFieldCoordinateTerminalizerLedger
#print axioms MUB.exists_finiteFieldCoordinateTerminalizerLedger
