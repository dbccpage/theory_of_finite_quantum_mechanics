import HilbertTransportEquiv
/-!
Finite Complex MUB family objects.

The previous files prove the scalar, vector, finite-field, and
coordinate-equivalence identities. This file packages those identities into a
small reusable structure: a finite coordinate carrier, a finite set of bases, a
finite label set for vectors in each basis, and the orthonormality/unbiasedness
proofs.

The structure is intentionally analytic and finite-function based. It is not
the final Omega algebraic coefficient-field object, and it is not a GTMUR loss
ledger. It is a Lean-backed Hilbert-family object that can be transported
losslessly along coordinate equivalences.
-/

namespace MUB

open scoped BigOperators

structure FiniteComplexMubFamily (ι B L : Type*) [Fintype ι]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L] where
  vector : B -> L -> ι -> ℂ
  basis_count : Fintype.card B = Fintype.card ι + 1
  label_count : Fintype.card L = Fintype.card ι
  same_basis_inner : ∀ b u v,
    finiteHilbertInner (vector b u) (vector b v) = if u = v then 1 else 0
  cross_basis_unbiased : ∀ {b c : B}, b ≠ c -> ∀ u v,
    finiteHilbertInner (vector b u) (vector c v) *
      star (finiteHilbertInner (vector b u) (vector c v)) =
        (Fintype.card ι : ℂ)⁻¹

namespace FiniteComplexMubFamily

noncomputable def transport
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (family : FiniteComplexMubFamily α B L) :
    FiniteComplexMubFamily β B L where
  vector b l := transportVector e (family.vector b l)
  basis_count := by
    rw [family.basis_count, Fintype.card_congr e]
  label_count := by
    rw [family.label_count, Fintype.card_congr e]
  same_basis_inner := by
    intro b u v
    rw [finiteHilbertInner_transportVector]
    exact family.same_basis_inner b u v
  cross_basis_unbiased := by
    intro b c hbc u v
    rw [finiteHilbertInner_transportVector]
    simpa [Fintype.card_congr e] using family.cross_basis_unbiased hbc u v

theorem transport_vector
    {α β B L : Type*} [Fintype α] [Fintype β]
    [Fintype B] [Fintype L] [DecidableEq B] [DecidableEq L]
    (e : α ≃ β) (family : FiniteComplexMubFamily α B L)
    (b : B) (l : L) :
    (family.transport e).vector b l = transportVector e (family.vector b l) :=
  rfl

end FiniteComplexMubFamily

noncomputable def finiteFieldComplexMubFamily
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) :
    FiniteComplexMubFamily F (Option F) F where
  vector := finiteFieldMubVector ψ
  basis_count := finiteFieldMub_basis_count F
  label_count := rfl
  same_basis_inner := finiteFieldMub_same_basis_inner ψ hψ hchar
  cross_basis_unbiased := by
    intro b c hbc u v
    exact finiteFieldMub_cross_basis_unbiased ψ hψ hchar h2 hbc u v

noncomputable def transportedFiniteFieldComplexMubFamily
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    FiniteComplexMubFamily β (Option F) F :=
  (finiteFieldComplexMubFamily ψ hψ hchar h2).transport e

theorem exists_finiteFieldComplexMubFamily
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteComplexMubFamily F (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨finiteFieldComplexMubFamily ψ hψ hchar h2⟩⟩

theorem exists_transportedFiniteFieldComplexMubFamily
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧ Nonempty (FiniteComplexMubFamily β (Option F) F) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, ⟨transportedFiniteFieldComplexMubFamily e ψ hψ hchar h2⟩⟩

end MUB

#print axioms MUB.FiniteComplexMubFamily.transport
#print axioms MUB.FiniteComplexMubFamily.transport_vector
#print axioms MUB.finiteFieldComplexMubFamily
#print axioms MUB.transportedFiniteFieldComplexMubFamily
#print axioms MUB.exists_finiteFieldComplexMubFamily
#print axioms MUB.exists_transportedFiniteFieldComplexMubFamily
