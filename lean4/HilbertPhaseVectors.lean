import HilbertPhaseNormalization
/-!
Finite-function Hilbert transport for trace-character phase vectors.

The previous files prove the finite-field overlap kernel and its Complex
normalization. This file turns those scalar identities into vector identities
for functions `F -> ℂ`, using the standard finite coordinate inner product.

The result is still not the full Omega transport theorem: it does not construct
a uniform algebraic coefficient field, a linear-isometry API object, or a GTMUR
loss ledger. It does prove the Hilbert-vector identities that those later
transport layers need to preserve.
-/

namespace MUB

open scoped BigOperators

noncomputable def finiteHilbertInner
    {ι : Type*} [Fintype ι] (v w : ι -> ℂ) : ℂ :=
  ∑ x : ι, star (v x) * w x

noncomputable def coordinateVector
    {F : Type*} [DecidableEq F] (label : F) : F -> ℂ :=
  fun x => if x = label then 1 else 0

noncomputable def quadraticPhaseVector
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (a b : F) : F -> ℂ :=
  fun x => sqrtCardNormalizer F * ψ (a * x ^ 2 + b * x)

theorem coordinateVector_inner
    {F : Type*} [Fintype F] [DecidableEq F]
    (u v : F) :
    finiteHilbertInner (coordinateVector u) (coordinateVector v) =
      if u = v then 1 else 0 := by
  unfold finiteHilbertInner coordinateVector
  by_cases huv : u = v
  · subst v
    simp
  · have hvu : ¬ v = u := fun h => huv h.symm
    simp [huv, hvu]

theorem quadraticPhaseVector_inner_eq_normalizedOverlap
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (a b c d : F) :
    finiteHilbertInner (quadraticPhaseVector ψ a b) (quadraticPhaseVector ψ c d) =
      normalizedQuadraticPhaseOverlap ψ a b c d := by
  unfold finiteHilbertInner quadraticPhaseVector normalizedQuadraticPhaseOverlap
    quadraticPhaseOverlap
  calc
    (∑ x : F, star (sqrtCardNormalizer F * ψ (a * x ^ 2 + b * x)) *
        (sqrtCardNormalizer F * ψ (c * x ^ 2 + d * x)))
        = ∑ x : F, (star (sqrtCardNormalizer F) * sqrtCardNormalizer F) *
            (star (ψ (a * x ^ 2 + b * x)) * ψ (c * x ^ 2 + d * x)) := by
          apply Finset.sum_congr rfl
          intro x _hx
          rw [star_mul]
          ring
    _ = (star (sqrtCardNormalizer F) * sqrtCardNormalizer F) *
          ∑ x : F, star (ψ (a * x ^ 2 + b * x)) *
            ψ (c * x ^ 2 + d * x) := by
          rw [Finset.mul_sum]
    _ = (Fintype.card F : ℂ)⁻¹ *
          ∑ x : F, star (ψ (a * x ^ 2 + b * x)) *
            ψ (c * x ^ 2 + d * x) := by
          rw [sqrtCardNormalizer_star_mul]

theorem quadraticPhaseVector_inner_self
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b : F) :
    finiteHilbertInner (quadraticPhaseVector ψ a b)
        (quadraticPhaseVector ψ a b) = 1 := by
  rw [quadraticPhaseVector_inner_eq_normalizedOverlap]
  exact normalizedQuadraticPhaseOverlap_self ψ hchar a b

theorem quadraticPhaseVector_same_slope_orthogonal
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (a b d : F) (hbd : b ≠ d) :
    finiteHilbertInner (quadraticPhaseVector ψ a b)
        (quadraticPhaseVector ψ a d) = 0 := by
  rw [quadraticPhaseVector_inner_eq_normalizedOverlap]
  exact normalizedQuadraticPhaseOverlap_same_slope_orthogonal ψ hψ hchar a b d hbd

theorem quadraticPhaseVector_same_slope_inner
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (a b d : F) :
    finiteHilbertInner (quadraticPhaseVector ψ a b)
        (quadraticPhaseVector ψ a d) =
      if b = d then 1 else 0 := by
  by_cases hbd : b = d
  · subst d
    simp [quadraticPhaseVector_inner_self ψ hchar a b]
  · simp [hbd, quadraticPhaseVector_same_slope_orthogonal ψ hψ hchar a b d hbd]

theorem quadraticPhaseVector_cross_slope_inner_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) {a c b d : F} (hac : a ≠ c) :
    finiteHilbertInner (quadraticPhaseVector ψ a b)
        (quadraticPhaseVector ψ c d) *
        star (finiteHilbertInner (quadraticPhaseVector ψ a b)
          (quadraticPhaseVector ψ c d)) =
      (Fintype.card F : ℂ)⁻¹ := by
  rw [quadraticPhaseVector_inner_eq_normalizedOverlap]
  exact normalizedQuadraticPhaseOverlap_cross_slope_normSq ψ hψ hchar h2 hac

theorem coordinateVector_phaseVector_inner
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (a b y : F) :
    finiteHilbertInner (coordinateVector y) (quadraticPhaseVector ψ a b) =
      sqrtCardNormalizer F * ψ (a * y ^ 2 + b * y) := by
  unfold finiteHilbertInner coordinateVector quadraticPhaseVector
  simp

theorem coordinateVector_phaseVector_inner_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b y : F) :
    finiteHilbertInner (coordinateVector y) (quadraticPhaseVector ψ a b) *
        star (finiteHilbertInner (coordinateVector y)
          (quadraticPhaseVector ψ a b)) =
      (Fintype.card F : ℂ)⁻¹ := by
  rw [coordinateVector_phaseVector_inner]
  rw [star_mul]
  let t : F := a * y ^ 2 + b * y
  have hstar_phase : star (ψ t) = ψ (-t) := by
    change (starRingEnd ℂ) (ψ t) = ψ (-t)
    rw [AddChar.starComp_apply hchar (φ := ψ)]
    rfl
  have hphase_unit : ψ t * star (ψ t) = 1 := by
    rw [hstar_phase]
    rw [← AddChar.map_add_eq_mul]
    simp [t]
  have hnorm := sqrtCardNormalizer_star_mul F
  calc
    sqrtCardNormalizer F * ψ (a * y ^ 2 + b * y) *
        (star (ψ (a * y ^ 2 + b * y)) * star (sqrtCardNormalizer F))
        = (star (sqrtCardNormalizer F) * sqrtCardNormalizer F) *
            (ψ t * star (ψ t)) := by
          simp only [t]
          ring
    _ = (Fintype.card F : ℂ)⁻¹ := by
          rw [hphase_unit, mul_one, hnorm]

end MUB

#print axioms MUB.coordinateVector_inner
#print axioms MUB.quadraticPhaseVector_inner_eq_normalizedOverlap
#print axioms MUB.quadraticPhaseVector_inner_self
#print axioms MUB.quadraticPhaseVector_same_slope_inner
#print axioms MUB.quadraticPhaseVector_cross_slope_inner_normSq
#print axioms MUB.coordinateVector_phaseVector_inner_normSq
