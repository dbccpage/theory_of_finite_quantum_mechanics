import HilbertMubFamily
/-!
Coordinate-equivalence transport for finite-function Hilbert MUBs.

`MUB.HilbertMubFamily` proves the Complex finite-function MUB identities on
the finite-field coordinate type `F`. This file proves the representation
transport theorem for any finite coordinate carrier `β` equivalent to `F`: the
standard finite inner product, ZeroRel equations, squared overlaps, and the
existential `q+1` MUB family are preserved by reindexing coordinates along an
equivalence.

This is still not the final Omega transport object. It does not construct an
algebraic coefficient field, a full Hilbert-basis API object, a GTMUR loss
ledger, or terminalizer preservation. It proves a lossless finite-function
transport layer that those later objects must subsume.
-/

namespace MUB

open scoped BigOperators

noncomputable def transportVector
    {α β : Type*} (e : α ≃ β) (v : α -> ℂ) : β -> ℂ :=
  fun y => v (e.symm y)

theorem finiteHilbertInner_transportVector
    {α β : Type*} [Fintype α] [Fintype β]
    (e : α ≃ β) (v w : α -> ℂ) :
    finiteHilbertInner (transportVector e v) (transportVector e w) =
      finiteHilbertInner v w := by
  unfold finiteHilbertInner transportVector
  simpa using (Fintype.sum_equiv e.symm
    (fun y : β => star (v (e.symm y)) * w (e.symm y))
    (fun x : α => star (v x) * w x) (by intro y; rfl))

theorem finiteHilbertInner_transportVector_zeroRel
    {α β : Type*} [Fintype α] [Fintype β]
    (e : α ≃ β) {v w : α -> ℂ}
    (hzero : finiteHilbertInner v w = 0) :
    finiteHilbertInner (transportVector e v) (transportVector e w) = 0 := by
  rw [finiteHilbertInner_transportVector, hzero]

theorem finiteHilbertInner_transportVector_normSq
    {α β : Type*} [Fintype α] [Fintype β]
    (e : α ≃ β) (v w : α -> ℂ) :
    finiteHilbertInner (transportVector e v) (transportVector e w) *
        star (finiteHilbertInner (transportVector e v) (transportVector e w)) =
      finiteHilbertInner v w * star (finiteHilbertInner v w) := by
  rw [finiteHilbertInner_transportVector]

noncomputable def transportedFiniteFieldMubVector
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F]
    (e : F ≃ β) (ψ : AddChar F ℂ) (basis : Option F) (label : F) :
    β -> ℂ :=
  transportVector e (finiteFieldMubVector ψ basis label)

theorem transportedFiniteFieldMub_basis_count
    {F β : Type*} [Fintype F] [Fintype β] (e : F ≃ β) :
    Fintype.card (Option F) = Fintype.card β + 1 := by
  rw [Fintype.card_option]
  rw [Fintype.card_congr e]

theorem transportedFiniteFieldMub_same_basis_inner
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (basis : Option F) (u v : F) :
    finiteHilbertInner (transportedFiniteFieldMubVector e ψ basis u)
        (transportedFiniteFieldMubVector e ψ basis v) =
      if u = v then 1 else 0 := by
  unfold transportedFiniteFieldMubVector
  rw [finiteHilbertInner_transportVector]
  exact finiteFieldMub_same_basis_inner ψ hψ hchar basis u v

theorem transportedFiniteFieldMub_cross_basis_unbiased
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0)
    {left right : Option F} (hneq : left ≠ right) (u v : F) :
    finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
        (transportedFiniteFieldMubVector e ψ right v) *
        star (finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
          (transportedFiniteFieldMubVector e ψ right v)) =
      (Fintype.card β : ℂ)⁻¹ := by
  have h := finiteFieldMub_cross_basis_unbiased ψ hψ hchar h2 hneq u v
  unfold transportedFiniteFieldMubVector
  rw [finiteHilbertInner_transportVector]
  simpa [Fintype.card_congr e] using h

theorem transportedFiniteField_complex_mub_family
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive)
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    Fintype.card (Option F) = Fintype.card β + 1 ∧
      (∀ basis u v,
        finiteHilbertInner (transportedFiniteFieldMubVector e ψ basis u)
          (transportedFiniteFieldMubVector e ψ basis v) =
          if u = v then 1 else 0) ∧
      (∀ {left right : Option F}, left ≠ right -> ∀ u v,
        finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
          (transportedFiniteFieldMubVector e ψ right v) *
          star (finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
            (transportedFiniteFieldMubVector e ψ right v)) =
          (Fintype.card β : ℂ)⁻¹) := by
  exact ⟨transportedFiniteFieldMub_basis_count e,
    transportedFiniteFieldMub_same_basis_inner e ψ hψ hchar,
    fun hneq u v =>
      transportedFiniteFieldMub_cross_basis_unbiased e ψ hψ hchar h2 hneq u v⟩

theorem exists_transportedFiniteField_complex_mub_family
    {F β : Type*} [Field F] [Fintype F] [DecidableEq F] [Fintype β]
    (e : F ≃ β) (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧
        Fintype.card (Option F) = Fintype.card β + 1 ∧
        (∀ basis u v,
          finiteHilbertInner (transportedFiniteFieldMubVector e ψ basis u)
            (transportedFiniteFieldMubVector e ψ basis v) =
            if u = v then 1 else 0) ∧
        (∀ {left right : Option F}, left ≠ right -> ∀ u v,
          finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
            (transportedFiniteFieldMubVector e ψ right v) *
            star (finiteHilbertInner (transportedFiniteFieldMubVector e ψ left u)
              (transportedFiniteFieldMubVector e ψ right v)) =
            (Fintype.card β : ℂ)⁻¹) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, transportedFiniteField_complex_mub_family e ψ hψ hchar h2⟩

end MUB

#print axioms MUB.finiteHilbertInner_transportVector
#print axioms MUB.finiteHilbertInner_transportVector_zeroRel
#print axioms MUB.finiteHilbertInner_transportVector_normSq
#print axioms MUB.transportedFiniteFieldMub_same_basis_inner
#print axioms MUB.transportedFiniteFieldMub_cross_basis_unbiased
#print axioms MUB.transportedFiniteField_complex_mub_family
#print axioms MUB.exists_transportedFiniteField_complex_mub_family
