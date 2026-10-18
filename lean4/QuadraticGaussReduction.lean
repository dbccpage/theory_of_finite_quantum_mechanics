import FiniteFieldCharacters
import Mathlib.NumberTheory.LegendreSymbol.Complex

/-!
Algebraic reductions for quadratic Gauss sums.

The MUB odd-prime-power route needs a finite-field theorem saying every
nondegenerate quadratic additive-character sum has squared norm equal to the
field cardinality. This module proves the coordinate-free algebraic reductions
that feed that theorem:

* completing the square reduces a linear term to a constant phase times a
  canonical quadratic sum;
* the two-variable Gauss-norm phase difference factors through the invertible
  odd-characteristic `(x, y) <-> (x - y, x + y)` change of variables;
* the resulting complex-valued quadratic Gauss squared-norm theorem.
-/

namespace MUB

open scoped BigOperators

noncomputable def quadraticGaussSum
    {F R : Type*} [Field F] [Fintype F] [CommRing R]
    (ψ : AddChar F R) (a b : F) : R :=
  ∑ x : F, ψ (a * x ^ 2 + b * x)

theorem quadratic_phase_complete_square
    {F : Type*} [Field F] {a b x : F} (ha : a ≠ 0) (h2 : (2 : F) ≠ 0) :
    a * x ^ 2 + b * x =
      a * (x + b / (2 * a)) ^ 2 - b ^ 2 / (4 * a) := by
  have h4 : (4 : F) ≠ 0 := by
    rw [show (4 : F) = (2 : F) * (2 : F) by norm_num]
    exact mul_ne_zero h2 h2
  field_simp [ha, h2, h4, pow_two]
  ring_nf

theorem quadraticGaussSum_complete_square
    {F R : Type*} [Field F] [Fintype F] [CommRing R]
    (ψ : AddChar F R) {a b : F} (ha : a ≠ 0) (h2 : (2 : F) ≠ 0) :
    quadraticGaussSum ψ a b =
      ψ (-(b ^ 2 / (4 * a))) * quadraticGaussSum ψ a 0 := by
  let c : F := b / (2 * a)
  let k : F := b ^ 2 / (4 * a)
  have hphase : ∀ x : F, a * x ^ 2 + b * x = a * (x + c) ^ 2 - k := by
    intro x
    simpa [c, k] using quadratic_phase_complete_square (a := a) (b := b) (x := x) ha h2
  calc
    quadraticGaussSum ψ a b
        = ∑ x : F, ψ (a * (x + c) ^ 2 - k) := by
            unfold quadraticGaussSum
            apply Finset.sum_congr rfl
            intro x _hx
            rw [hphase x]
    _ = ∑ y : F, ψ (a * y ^ 2 - k) := by
            refine Fintype.sum_equiv (Equiv.addRight c) _ _ ?_
            intro x
            rfl
    _ = ∑ y : F, ψ (-k) * ψ (a * y ^ 2) := by
            apply Finset.sum_congr rfl
            intro y _hy
            rw [sub_eq_add_neg, add_comm, AddChar.map_add_eq_mul]
    _ = ψ (-k) * quadraticGaussSum ψ a 0 := by
            unfold quadraticGaussSum
            change (∑ y : F, ψ (-k) * ψ (a * y ^ 2)) =
              ψ (-k) * ∑ y : F, ψ (a * y ^ 2 + 0 * y)
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro y _hy
            simp

theorem quadratic_phase_difference_uv
    {F : Type*} [CommRing F] (a b x y : F) :
    (a * x ^ 2 + b * x) - (a * y ^ 2 + b * y) =
      (x - y) * (a * (x + y) + b) := by
  ring

noncomputable def oddCharTwoLinearEquiv
    {F : Type*} [Field F] (h2 : (2 : F) ≠ 0) : F × F ≃ F × F where
  toFun p := (p.1 - p.2, p.1 + p.2)
  invFun p := ((p.1 + p.2) / 2, (p.2 - p.1) / 2)
  left_inv := by
    intro p
    ext <;> field_simp [h2] <;> ring
  right_inv := by
    intro p
    ext <;> field_simp [h2] <;> ring

theorem quadratic_phase_difference_uv_equiv
    {F : Type*} [Field F] (h2 : (2 : F) ≠ 0) (a b : F) (p : F × F) :
    (a * p.1 ^ 2 + b * p.1) - (a * p.2 ^ 2 + b * p.2) =
      (oddCharTwoLinearEquiv h2 p).1 *
        (a * (oddCharTwoLinearEquiv h2 p).2 + b) := by
  exact quadratic_phase_difference_uv a b p.1 p.2

theorem quadraticGauss_autocorrelation_sum
    {F R : Type*} [Field F] [Fintype F] [DecidableEq F]
    [CommRing R] [IsDomain R]
    (ψ : AddChar F R) (hψ : ψ.IsPrimitive) {a b : F} (ha : a ≠ 0)
    (h2 : (2 : F) ≠ 0) :
    (∑ p : F × F,
      ψ ((a * p.1 ^ 2 + b * p.1) - (a * p.2 ^ 2 + b * p.2))) =
      Fintype.card F := by
  have hinner :
      ∀ u : F, (∑ v : F, ψ (u * (a * v + b))) =
        (if u = 0 then (Fintype.card F : R) else 0) := by
    intro u
    by_cases hu : u = 0
    · subst u
      simp
    · have hau : a * u ≠ 0 := mul_ne_zero ha hu
      calc
        (∑ v : F, ψ (u * (a * v + b)))
            = ∑ v : F, ψ (u * b) * ψ (v * (a * u)) := by
                apply Finset.sum_congr rfl
                intro v _hv
                have harg : u * (a * v + b) = u * b + v * (a * u) := by
                  ring
                rw [harg, AddChar.map_add_eq_mul]
        _ = ψ (u * b) * ∑ v : F, ψ (v * (a * u)) := by
                rw [Finset.mul_sum]
        _ = 0 := by
                rw [finite_field_primitive_additive_character_linear_orthogonality
                  ψ hψ (a * u)]
                simp [hau]
        _ = (if u = 0 then (Fintype.card F : R) else 0) := by
                simp [hu]
  calc
    (∑ p : F × F,
      ψ ((a * p.1 ^ 2 + b * p.1) - (a * p.2 ^ 2 + b * p.2)))
        = ∑ uv : F × F, ψ (uv.1 * (a * uv.2 + b)) := by
            refine Fintype.sum_equiv (oddCharTwoLinearEquiv h2) _ _ ?_
            intro p
            rw [quadratic_phase_difference_uv_equiv]
    _ = ∑ u : F, ∑ v : F, ψ (u * (a * v + b)) := by
            rw [Fintype.sum_prod_type]
    _ = ∑ u : F, (if u = 0 then Fintype.card F else 0 : R) := by
            apply Finset.sum_congr rfl
            intro u _hu
            exact hinner u
    _ = Fintype.card F := by
            simp

theorem quadraticGauss_complex_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    {a b : F} (ha : a ≠ 0) (h2 : (2 : F) ≠ 0) :
    quadraticGaussSum ψ a b * star (quadraticGaussSum ψ a b) =
      Fintype.card F := by
  let Q : F → F := fun x => a * x ^ 2 + b * x
  have hstar :
      star (quadraticGaussSum ψ a b) = ∑ y : F, ψ (-Q y) := by
    unfold quadraticGaussSum
    show (starRingEnd ℂ) (∑ x : F, ψ (Q x)) = ∑ y : F, ψ (-Q y)
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro y _hy
    rw [AddChar.starComp_apply hchar (φ := ψ)]
    rfl
  calc
    quadraticGaussSum ψ a b * star (quadraticGaussSum ψ a b)
        = (∑ x : F, ψ (Q x)) * (∑ y : F, ψ (-Q y)) := by
            rw [hstar]
            simp [quadraticGaussSum, Q]
    _ = ∑ x : F, ∑ y : F, ψ (Q x) * ψ (-Q y) := by
            rw [Finset.sum_mul_sum]
    _ = ∑ p : F × F, ψ (Q p.1 - Q p.2) := by
            rw [Fintype.sum_prod_type]
            apply Finset.sum_congr rfl
            intro x _hx
            apply Finset.sum_congr rfl
            intro y _hy
            simpa [sub_eq_add_neg] using
              (AddChar.map_add_eq_mul ψ (Q x) (-Q y)).symm
    _ = Fintype.card F := by
            exact quadraticGauss_autocorrelation_sum ψ hψ ha h2

end MUB

#print axioms MUB.quadratic_phase_complete_square
#print axioms MUB.quadraticGaussSum_complete_square
#print axioms MUB.quadratic_phase_difference_uv
#print axioms MUB.oddCharTwoLinearEquiv
#print axioms MUB.quadratic_phase_difference_uv_equiv
#print axioms MUB.quadraticGauss_autocorrelation_sum
#print axioms MUB.quadraticGauss_complex_normSq
