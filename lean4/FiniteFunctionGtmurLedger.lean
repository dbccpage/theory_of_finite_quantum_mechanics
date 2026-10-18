import HilbertMubStructure
/-!
Finite-function GTMUR ledger for coordinate-equivalence transport.

This module records the loss ledger that is available after the finite Complex
MUB family object: when a finite-function MUB family is reindexed along a
coordinate equivalence, cardinality, Hilbert inner products, ZeroRel equations,
and squared-overlap values are preserved.

This is deliberately narrower than the final Omega GTMUR obligation. It does
not construct algebraic coefficient fields, compare different representation
regimes, prove terminalizer preservation, or supply a dimension-parametric
loss ledger for all prime-power schemas. It is the Lean-backed finite-function
ledger that those stronger objects must extend.
-/

namespace MUB

open scoped BigOperators

structure FiniteFunctionGtmurLedger (α β B L : Type*) [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L] where
  source : FiniteComplexMubFamily α B L
  target : FiniteComplexMubFamily β B L
  coordinate_card_preserved : Fintype.card β = Fintype.card α
  inner_preserved : ∀ b c u v,
    finiteHilbertInner (target.vector b u) (target.vector c v) =
      finiteHilbertInner (source.vector b u) (source.vector c v)
  zeroRel_preserved : ∀ b c u v,
    finiteHilbertInner (source.vector b u) (source.vector c v) = 0 ->
      finiteHilbertInner (target.vector b u) (target.vector c v) = 0
  normSq_preserved : ∀ b c u v,
    finiteHilbertInner (target.vector b u) (target.vector c v) *
        star (finiteHilbertInner (target.vector b u) (target.vector c v)) =
      finiteHilbertInner (source.vector b u) (source.vector c v) *
        star (finiteHilbertInner (source.vector b u) (source.vector c v))

noncomputable def coordinateTransportFiniteFunctionGtmurLedger
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (source : FiniteComplexMubFamily α B L) :
    FiniteFunctionGtmurLedger α β B L where
  source := source
  target := source.transport e
  coordinate_card_preserved := (Fintype.card_congr e).symm
  inner_preserved := by
    intro b c u v
    rw [FiniteComplexMubFamily.transport_vector]
    rw [FiniteComplexMubFamily.transport_vector]
    rw [finiteHilbertInner_transportVector]
  zeroRel_preserved := by
    intro b c u v hzero
    rw [FiniteComplexMubFamily.transport_vector]
    rw [FiniteComplexMubFamily.transport_vector]
    rw [finiteHilbertInner_transportVector]
    exact hzero
  normSq_preserved := by
    intro b c u v
    rw [FiniteComplexMubFamily.transport_vector]
    rw [FiniteComplexMubFamily.transport_vector]
    rw [finiteHilbertInner_transportVector]

noncomputable def finiteFieldCoordinateGtmurLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    FiniteFunctionGtmurLedger F β (Option F) F :=
  coordinateTransportFiniteFunctionGtmurLedger e
    (finiteFieldComplexMubFamily ψ hψ hchar h2)

theorem exists_finiteFieldCoordinateGtmurLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteFunctionGtmurLedger F β (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨finiteFieldCoordinateGtmurLedger e ψ hψ hchar h2⟩⟩

end MUB

#print axioms MUB.coordinateTransportFiniteFunctionGtmurLedger
#print axioms MUB.finiteFieldCoordinateGtmurLedger
#print axioms MUB.exists_finiteFieldCoordinateGtmurLedger
