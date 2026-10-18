import FiniteFunctionHilbertBasisTransport
/-!
Finite-function GTMUR loss ledger.

This module packages the coordinate-equivalence Hilbert-basis transport object
as a zero-loss finite-function GTMUR ledger. It records that coordinate
cardinality, complete basis counts, label counts, transported vectors,
Hilbert inner products, ZeroRel equations, same-basis orthogonality, and
cross-basis squared-overlap identities are all preserved by the coordinate
equivalence.

This is not the final dimension-parametric GTMUR loss ledger. It only covers
finite-function Complex coordinate reindexing. The stronger Omega theorem must
still compare the algebraic, Weyl/projector, Hilbert, and certificate
representations uniformly across the declared dimension family.
-/

namespace MUB

open scoped BigOperators

structure FiniteFunctionGtmurLossLedger (α β B L : Type*) [Fintype α]
    [Fintype β] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  transport : FiniteFunctionHilbertBasisTransport α β B L
  coordinate_card_loss_zero : Fintype.card β = Fintype.card α
  source_complete_basis_profile : Fintype.card B = Fintype.card α + 1
  target_complete_basis_profile : Fintype.card B = Fintype.card β + 1
  source_label_profile : Fintype.card L = Fintype.card α
  target_label_profile : Fintype.card L = Fintype.card β
  vector_transport_loss_zero : ∀ b l,
    transport.terminalizer.gtmur.target.vector b l =
      transportVector transport.coordinateEquiv
        (transport.terminalizer.gtmur.source.vector b l)
  inner_loss_zero : ∀ b c u v,
    finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
      (transport.terminalizer.gtmur.target.vector c v) =
    finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
      (transport.terminalizer.gtmur.source.vector c v)
  zeroRel_loss_zero : ∀ b c u v,
    finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
      (transport.terminalizer.gtmur.source.vector c v) = 0 ->
    finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
      (transport.terminalizer.gtmur.target.vector c v) = 0
  normSq_loss_zero : ∀ b c u v,
    finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
        (transport.terminalizer.gtmur.target.vector c v) *
        star (finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
          (transport.terminalizer.gtmur.target.vector c v)) =
      finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
        (transport.terminalizer.gtmur.source.vector c v) *
        star (finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
          (transport.terminalizer.gtmur.source.vector c v))
  source_same_basis_zeroRel : ∀ b u v,
    u ≠ v -> finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
      (transport.terminalizer.gtmur.source.vector b v) = 0
  target_same_basis_zeroRel : ∀ b u v,
    u ≠ v -> finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
      (transport.terminalizer.gtmur.target.vector b v) = 0
  source_cross_basis_unbiased : ∀ {b c : B}, b ≠ c -> ∀ u v,
    finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
      (transport.terminalizer.gtmur.source.vector c v) *
      star (finiteHilbertInner (transport.terminalizer.gtmur.source.vector b u)
        (transport.terminalizer.gtmur.source.vector c v)) =
        (Fintype.card α : ℂ)⁻¹
  target_cross_basis_unbiased : ∀ {b c : B}, b ≠ c -> ∀ u v,
    finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
      (transport.terminalizer.gtmur.target.vector c v) *
      star (finiteHilbertInner (transport.terminalizer.gtmur.target.vector b u)
        (transport.terminalizer.gtmur.target.vector c v)) =
        (Fintype.card β : ℂ)⁻¹

noncomputable def coordinateTransportFiniteFunctionGtmurLossLedger
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (source : FiniteComplexMubFamily α B L) :
    FiniteFunctionGtmurLossLedger α β B L where
  transport := coordinateTransportFiniteFunctionHilbertBasisTransport e source
  coordinate_card_loss_zero :=
    (coordinateTransportFiniteFunctionHilbertBasisTransport e source).coordinate_card_preserved
  source_complete_basis_profile := source.basis_count
  target_complete_basis_profile := (source.transport e).basis_count
  source_label_profile := source.label_count
  target_label_profile := (source.transport e).label_count
  vector_transport_loss_zero := by
    intro b l
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).target_vector_eq_transport b l
  inner_loss_zero := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).inner_profile_preserved b c u v
  zeroRel_loss_zero := by
    intro b c u v hzero
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).zeroRel_preserved b c u v hzero
  normSq_loss_zero := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).normSq_profile_preserved b c u v
  source_same_basis_zeroRel := by
    intro b u v huv
    simpa [huv] using
      (coordinateTransportFiniteFunctionHilbertBasisTransport e source).source_same_basis_inner b u v
  target_same_basis_zeroRel := by
    intro b u v huv
    simpa [huv] using
      (coordinateTransportFiniteFunctionHilbertBasisTransport e source).target_same_basis_inner b u v
  source_cross_basis_unbiased := by
    intro b c hbc u v
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).source_cross_basis_unbiased hbc u v
  target_cross_basis_unbiased := by
    intro b c hbc u v
    exact (coordinateTransportFiniteFunctionHilbertBasisTransport e source).target_cross_basis_unbiased hbc u v

noncomputable def finiteFieldCoordinateGtmurLossLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    FiniteFunctionGtmurLossLedger F β (Option F) F :=
  coordinateTransportFiniteFunctionGtmurLossLedger e
    (finiteFieldComplexMubFamily ψ hψ hchar h2)

theorem exists_finiteFieldCoordinateGtmurLossLedger
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteFunctionGtmurLossLedger F β (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨finiteFieldCoordinateGtmurLossLedger e ψ hψ hchar h2⟩⟩

end MUB

#print axioms MUB.coordinateTransportFiniteFunctionGtmurLossLedger
#print axioms MUB.finiteFieldCoordinateGtmurLossLedger
#print axioms MUB.exists_finiteFieldCoordinateGtmurLossLedger
