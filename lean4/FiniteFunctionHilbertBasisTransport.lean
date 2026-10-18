import FiniteFunctionTerminalizer
/-!
Finite-function Hilbert-basis transport object.

The previous finite-function files prove and ledger coordinate-equivalence
transport one layer at a time. This module packages those layers as a Hilbert
basis transport object: a coordinate equivalence, the transported complete MUB
family, basis/label counts, same-basis and cross-basis Hilbert identities, and
the exact inner-product, ZeroRel, and squared-overlap preservation profile.

This is still a finite-function Complex object. It is intentionally not the
final algebraic coefficient-field transport theorem, and it does not close the
dimension-parametric GTMUR or terminalizer obligations. It records the formal
finite Hilbert-basis transport shape that those stronger theorem families must
extend.
-/

namespace MUB

open scoped BigOperators

structure FiniteFunctionHilbertBasisTransport (α β B L : Type*) [Fintype α]
    [Fintype β] [Fintype B] [Fintype L] [DecidableEq B]
    [DecidableEq L] where
  coordinateEquiv : α ≃ β
  terminalizer : FiniteFunctionTerminalizerLedger α β B L
  target_vector_eq_transport : ∀ b l,
    terminalizer.gtmur.target.vector b l =
      transportVector coordinateEquiv (terminalizer.gtmur.source.vector b l)
  coordinate_card_preserved : Fintype.card β = Fintype.card α
  source_complete_basis_count : Fintype.card B = Fintype.card α + 1
  target_complete_basis_count : Fintype.card B = Fintype.card β + 1
  source_label_count : Fintype.card L = Fintype.card α
  target_label_count : Fintype.card L = Fintype.card β
  source_same_basis_inner : ∀ b u v,
    finiteHilbertInner (terminalizer.gtmur.source.vector b u)
        (terminalizer.gtmur.source.vector b v) = if u = v then 1 else 0
  target_same_basis_inner : ∀ b u v,
    finiteHilbertInner (terminalizer.gtmur.target.vector b u)
        (terminalizer.gtmur.target.vector b v) = if u = v then 1 else 0
  source_cross_basis_unbiased : ∀ {b c : B}, b ≠ c -> ∀ u v,
    finiteHilbertInner (terminalizer.gtmur.source.vector b u)
      (terminalizer.gtmur.source.vector c v) *
      star (finiteHilbertInner (terminalizer.gtmur.source.vector b u)
        (terminalizer.gtmur.source.vector c v)) =
        (Fintype.card α : ℂ)⁻¹
  target_cross_basis_unbiased : ∀ {b c : B}, b ≠ c -> ∀ u v,
    finiteHilbertInner (terminalizer.gtmur.target.vector b u)
      (terminalizer.gtmur.target.vector c v) *
      star (finiteHilbertInner (terminalizer.gtmur.target.vector b u)
        (terminalizer.gtmur.target.vector c v)) =
        (Fintype.card β : ℂ)⁻¹
  inner_profile_preserved : ∀ b c u v,
    finiteHilbertInner (terminalizer.gtmur.target.vector b u)
      (terminalizer.gtmur.target.vector c v) =
    finiteHilbertInner (terminalizer.gtmur.source.vector b u)
      (terminalizer.gtmur.source.vector c v)
  zeroRel_preserved : ∀ b c u v,
    finiteHilbertInner (terminalizer.gtmur.source.vector b u)
      (terminalizer.gtmur.source.vector c v) = 0 ->
    finiteHilbertInner (terminalizer.gtmur.target.vector b u)
      (terminalizer.gtmur.target.vector c v) = 0
  normSq_profile_preserved : ∀ b c u v,
    finiteHilbertInner (terminalizer.gtmur.target.vector b u)
        (terminalizer.gtmur.target.vector c v) *
        star (finiteHilbertInner (terminalizer.gtmur.target.vector b u)
          (terminalizer.gtmur.target.vector c v)) =
      finiteHilbertInner (terminalizer.gtmur.source.vector b u)
        (terminalizer.gtmur.source.vector c v) *
        star (finiteHilbertInner (terminalizer.gtmur.source.vector b u)
          (terminalizer.gtmur.source.vector c v))

noncomputable def coordinateTransportFiniteFunctionHilbertBasisTransport
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (source : FiniteComplexMubFamily α B L) :
    FiniteFunctionHilbertBasisTransport α β B L where
  coordinateEquiv := e
  terminalizer := coordinateTransportFiniteFunctionTerminalizerLedger e source
  target_vector_eq_transport := by
    intro b l
    rfl
  coordinate_card_preserved :=
    (coordinateTransportFiniteFunctionTerminalizerLedger e source).coordinate_card_preserved
  source_complete_basis_count := source.basis_count
  target_complete_basis_count := (source.transport e).basis_count
  source_label_count := source.label_count
  target_label_count := (source.transport e).label_count
  source_same_basis_inner := source.same_basis_inner
  target_same_basis_inner := (source.transport e).same_basis_inner
  source_cross_basis_unbiased := by
    intro b c hbc u v
    exact source.cross_basis_unbiased hbc u v
  target_cross_basis_unbiased := by
    intro b c hbc u v
    exact (source.transport e).cross_basis_unbiased hbc u v
  inner_profile_preserved := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionTerminalizerLedger e source).terminal_inner_profile_preserved b c u v
  zeroRel_preserved := by
    intro b c u v hzero
    exact (coordinateTransportFiniteFunctionTerminalizerLedger e source).terminal_zeroRel_preserved b c u v hzero
  normSq_profile_preserved := by
    intro b c u v
    exact (coordinateTransportFiniteFunctionTerminalizerLedger e source).terminal_normSq_profile_preserved b c u v

noncomputable def finiteFieldCoordinateHilbertBasisTransport
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    FiniteFunctionHilbertBasisTransport F β (Option F) F :=
  coordinateTransportFiniteFunctionHilbertBasisTransport e
    (finiteFieldComplexMubFamily ψ hψ hchar h2)

theorem exists_finiteFieldCoordinateHilbertBasisTransport
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteFunctionHilbertBasisTransport F β (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨finiteFieldCoordinateHilbertBasisTransport e ψ hψ hchar h2⟩⟩

end MUB

#print axioms MUB.coordinateTransportFiniteFunctionHilbertBasisTransport
#print axioms MUB.finiteFieldCoordinateHilbertBasisTransport
#print axioms MUB.exists_finiteFieldCoordinateHilbertBasisTransport
