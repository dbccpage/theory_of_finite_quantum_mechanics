import HilbertPhaseVectors
/-!
Complex finite-function MUB family from trace-character data.

This file packages the computational basis and the quadratic phase bases into a
single `Option F` indexed family. The theorem is a Complex Hilbert-space family
statement for finite functions `F -> ℂ`: one computational basis plus one phase
basis for each slope.

It is still not the final Omega-family certificate. The theorem assumes a
primitive additive character and works over `ℂ`; it does not construct the
uniform algebraic coefficient field, algebraic transport object, or GTMUR loss
ledger needed by the Rust authority gate.
-/

namespace MUB

open scoped BigOperators

noncomputable def finiteFieldMubVector
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (basis : Option F) (label : F) : F -> ℂ :=
  match basis with
  | none => coordinateVector label
  | some a => quadraticPhaseVector ψ a label

theorem finiteFieldMub_basis_count
    (F : Type*) [Fintype F] :
    Fintype.card (Option F) = Fintype.card F + 1 := by
  exact Fintype.card_option

theorem finiteFieldMub_same_basis_inner
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (basis : Option F) (u v : F) :
    finiteHilbertInner (finiteFieldMubVector ψ basis u)
        (finiteFieldMubVector ψ basis v) =
      if u = v then 1 else 0 := by
  cases basis with
  | none =>
      simp [finiteFieldMubVector, coordinateVector_inner]
  | some a =>
      simp [finiteFieldMubVector,
        quadraticPhaseVector_same_slope_inner ψ hψ hchar a u v]

theorem phaseVector_coordinateVector_inner
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (a b y : F) :
    finiteHilbertInner (quadraticPhaseVector ψ a b) (coordinateVector y) =
      star (sqrtCardNormalizer F * ψ (a * y ^ 2 + b * y)) := by
  unfold finiteHilbertInner coordinateVector quadraticPhaseVector
  simp

theorem phaseVector_coordinateVector_inner_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b y : F) :
    finiteHilbertInner (quadraticPhaseVector ψ a b) (coordinateVector y) *
        star (finiteHilbertInner (quadraticPhaseVector ψ a b)
          (coordinateVector y)) =
      (Fintype.card F : ℂ)⁻¹ := by
  rw [phaseVector_coordinateVector_inner]
  rw [star_star]
  rw [mul_comm]
  rw [← coordinateVector_phaseVector_inner ψ a b y]
  exact coordinateVector_phaseVector_inner_normSq ψ hchar a b y

theorem finiteFieldMub_cross_basis_unbiased
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) {left right : Option F} (hneq : left ≠ right)
    (u v : F) :
    finiteHilbertInner (finiteFieldMubVector ψ left u)
        (finiteFieldMubVector ψ right v) *
        star (finiteHilbertInner (finiteFieldMubVector ψ left u)
          (finiteFieldMubVector ψ right v)) =
      (Fintype.card F : ℂ)⁻¹ := by
  cases left with
  | none =>
      cases right with
      | none => contradiction
      | some a =>
          simpa [finiteFieldMubVector] using
            coordinateVector_phaseVector_inner_normSq ψ hchar a v u
  | some a =>
      cases right with
      | none =>
          simpa [finiteFieldMubVector] using
            phaseVector_coordinateVector_inner_normSq ψ hchar a u v
      | some c =>
          have hac : a ≠ c := by
            intro h
            apply hneq
            simp [h]
          simpa [finiteFieldMubVector] using
            quadraticPhaseVector_cross_slope_inner_normSq ψ hψ hchar h2 hac
              (b := u) (d := v)

theorem finiteField_complex_mub_family
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) :
    Fintype.card (Option F) = Fintype.card F + 1 ∧
      (∀ basis u v,
        finiteHilbertInner (finiteFieldMubVector ψ basis u)
          (finiteFieldMubVector ψ basis v) =
          if u = v then 1 else 0) ∧
      (∀ {left right : Option F}, left ≠ right -> ∀ u v,
        finiteHilbertInner (finiteFieldMubVector ψ left u)
          (finiteFieldMubVector ψ right v) *
          star (finiteHilbertInner (finiteFieldMubVector ψ left u)
            (finiteFieldMubVector ψ right v)) =
          (Fintype.card F : ℂ)⁻¹) := by
  exact ⟨finiteFieldMub_basis_count F,
    finiteFieldMub_same_basis_inner ψ hψ hchar,
    fun hneq u v => finiteFieldMub_cross_basis_unbiased ψ hψ hchar h2 hneq u v⟩

theorem exists_finiteField_complex_mub_family
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (hchar : 0 < ringChar F) (h2 : (2 : F) ≠ 0) :
    ∃ ψ : AddChar F ℂ,
      ψ.IsPrimitive ∧
        Fintype.card (Option F) = Fintype.card F + 1 ∧
        (∀ basis u v,
          finiteHilbertInner (finiteFieldMubVector ψ basis u)
            (finiteFieldMubVector ψ basis v) =
            if u = v then 1 else 0) ∧
        (∀ {left right : Option F}, left ≠ right -> ∀ u v,
          finiteHilbertInner (finiteFieldMubVector ψ left u)
            (finiteFieldMubVector ψ right v) *
            star (finiteHilbertInner (finiteFieldMubVector ψ left u)
              (finiteFieldMubVector ψ right v)) =
            (Fintype.card F : ℂ)⁻¹) := by
  rcases finite_field_exists_primitive_complex_additive_character F with
    ⟨ψ, hψ⟩
  exact ⟨ψ, hψ, finiteField_complex_mub_family ψ hψ hchar h2⟩

end MUB

#print axioms MUB.finiteFieldMub_basis_count
#print axioms MUB.finiteFieldMub_same_basis_inner
#print axioms MUB.finiteFieldMub_cross_basis_unbiased
#print axioms MUB.finiteField_complex_mub_family
#print axioms MUB.exists_finiteField_complex_mub_family
