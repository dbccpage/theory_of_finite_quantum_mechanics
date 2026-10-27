import Mathlib.Algebra.Group.AddChar
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Star.Basic
import Mathlib.Algebra.Star.BigOperators
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/-!
# A complete family of `q + 1` mutually unbiased bases for every odd prime power `q`

AuthorityEffect: None.

Setting.  `F` is a finite field with `q` elements and `2 ≠ 0` in `F` (odd characteristic).
`R` is a commutative domain with an involution `star` (for the intended reading `R = ℂ`,
`star` is complex conjugation).  `ψ : AddChar F R` is an additive character that is nontrivial
(`ψ ≠ 1`) and *unitary* (`star (ψ t) = ψ (-t)`).  Over `ℂ` the character
`ψ(t) = exp(2πi · Tr_{F/𝔽_p}(t) / p)` has both properties; that instance is not constructed in
this file, which treats `ψ` as a parameter.

Vectors are functions `F → R`; `pair u v = ∑ x, star (u x) * v x` is the Hermitian pairing.
The `q + 1` bases are indexed by `Option F`:
* `none` is the standard basis `stdvec y = (x ↦ [x = y])`;
* `some a` is the quadratic-phase basis `qvec a b = (x ↦ ψ (a x² + b x))`, `b ∈ F`.

Main results (all unnormalised, so no square roots are needed).
* `pair_qvec_same`: within the basis `some a`, `pair (qvec a b) (qvec a b') = [b = b'] · q`.
* `pair_std`: within the standard basis, `pair (stdvec y) (stdvec y') = [y = y']`.
* `pair_qvec_cross_mul_star`: for `a ≠ a'`,
  `pair (qvec a b) (qvec a' b') * star (pair (qvec a b) (qvec a' b')) = q`.
* `pair_std_qvec_mul_star`: `pair (stdvec y) (qvec a b) * star (…) = 1`.
* `mub_family`: the packaged statement.  For bases `i ≠ j` and members `u, v`,
  `|pair u v|² · q = pair u u · pair v v`, which after normalisation by the norms is the
  unbiasedness relation `|⟨u, v⟩|² = 1/q`; and each basis is orthogonal with all norms equal to
  `q` (quadratic-phase) or `1` (standard), hence nonzero when `q ≠ 0` in `R`.

The proof of the cross relation is the standard Weil-sum computation: with `c = a' - a ≠ 0` and
`d = b' - b`, `|∑ₓ ψ(c x² + d x)|² = ∑ₜ ψ(c t² + d t) ∑_y ψ(2 c t y) = q`, because the inner
sum vanishes unless `2 c t = 0`, i.e. `t = 0`.  Odd characteristic enters exactly through
`2 c ≠ 0`.  Characteristic two is not treated here.  Nothing here is a statement about physics.
-/

namespace MubPrimePower.PrimePowerOdd

open Finset

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]
variable {R : Type*} [CommRing R] [IsDomain R] [StarRing R]

/-- The Hermitian pairing `∑ x, star (u x) * v x`. -/
def pair (u v : F → R) : R := ∑ x, star (u x) * v x

/-- The standard basis vector concentrated at `y`. -/
def stdvec (y : F) : F → R := fun x => if x = y then 1 else 0

/-- The quadratic-phase vector `x ↦ ψ (a x² + b x)`. -/
def qvec (ψ : AddChar F R) (a b : F) : F → R := fun x => ψ (a * x ^ 2 + b * x)

/-- The `q + 1` bases: `none` is the standard basis, `some a` the quadratic-phase basis. -/
def basisVec (ψ : AddChar F R) : Option F → F → (F → R)
  | none, y => stdvec y
  | some a, b => qvec ψ a b

/-! ### Character sums -/

omit [DecidableEq F] [StarRing R] in
/-- A nontrivial additive character on a field, composed with multiplication by `c ≠ 0`, sums
to zero. -/
theorem sum_mulShift_eq_zero {ψ : AddChar F R} (hψ : ψ ≠ 1) {c : F} (hc : c ≠ 0) :
    ∑ x, ψ (c * x) = 0 := by
  obtain ⟨b, hb⟩ := AddChar.ne_one_iff.1 hψ
  have h₁ : ∑ x, ψ (c * (c⁻¹ * b + x)) = ∑ x, ψ (c * x) :=
    Fintype.sum_equiv (Equiv.addLeft (c⁻¹ * b)) _ _ fun x => rfl
  have h₂ : ∀ x, ψ (c * (c⁻¹ * b + x)) = ψ b * ψ (c * x) := by
    intro x
    rw [mul_add, mul_inv_cancel_left₀ hc, AddChar.map_add_eq_mul]
  simp_rw [h₂, ← Finset.mul_sum] at h₁
  have h₃ : (ψ b - 1) * ∑ x, ψ (c * x) = 0 := by rw [sub_mul, one_mul, h₁, sub_self]
  rcases mul_eq_zero.1 h₃ with h | h
  · exact absurd (sub_eq_zero.1 h) hb
  · exact h

omit [StarRing R] in
/-- `∑ x, ψ (c * x)` is `q` for `c = 0` and `0` otherwise. -/
theorem sum_mulShift {ψ : AddChar F R} (hψ : ψ ≠ 1) (c : F) :
    ∑ x, ψ (c * x) = if c = 0 then (Fintype.card F : R) else 0 := by
  split_ifs with hc
  · simp [hc]
  · exact sum_mulShift_eq_zero hψ hc

/-! ### Pairings inside one basis -/

omit [Field F] [IsDomain R] in
theorem pair_std (y y' : F) : pair (stdvec y : F → R) (stdvec y') = if y = y' then 1 else 0 := by
  unfold pair stdvec
  rw [Finset.sum_eq_single y (fun x _ hx => by simp [hx]) (fun h => absurd (Finset.mem_univ y) h)]
  simp

theorem pair_qvec_same {ψ : AddChar F R} (hψ : ψ ≠ 1) (hstar : ∀ t, star (ψ t) = ψ (-t))
    (a b b' : F) :
    pair (qvec ψ a b) (qvec ψ a b') = if b = b' then (Fintype.card F : R) else 0 := by
  unfold pair qvec
  have h : ∀ x, star (ψ (a * x ^ 2 + b * x)) * ψ (a * x ^ 2 + b' * x) = ψ ((b' - b) * x) := by
    intro x
    rw [hstar, ← AddChar.map_add_eq_mul]
    congr 1
    ring
  simp_rw [h]
  rw [sum_mulShift hψ]
  by_cases hb : b = b'
  · simp [hb]
  · have : b' - b ≠ 0 := sub_ne_zero.2 (Ne.symm hb)
    simp [hb, this]

/-! ### Pairings across two bases -/

omit [IsDomain R] in
theorem pair_std_qvec (ψ : AddChar F R) (y a b : F) :
    pair (stdvec y) (qvec ψ a b) = ψ (a * y ^ 2 + b * y) := by
  unfold pair stdvec qvec
  rw [Finset.sum_eq_single y (fun x _ hx => by simp [hx]) (fun h => absurd (Finset.mem_univ y) h)]
  simp

omit [IsDomain R] in
theorem pair_std_qvec_mul_star {ψ : AddChar F R} (hstar : ∀ t, star (ψ t) = ψ (-t))
    (y a b : F) :
    pair (stdvec y) (qvec ψ a b) * star (pair (stdvec y) (qvec ψ a b)) = 1 := by
  rw [pair_std_qvec, hstar, ← AddChar.map_add_eq_mul, add_neg_cancel, AddChar.map_zero_eq_one]

/-- The Weil-sum identity: for `c ≠ 0` (and `2 ≠ 0` in `F`),
`(∑ x, ψ (c x² + d x)) * star (∑ x, ψ (c x² + d x)) = q`. -/
theorem weil_sum_mul_star {ψ : AddChar F R} (hψ : ψ ≠ 1) (hstar : ∀ t, star (ψ t) = ψ (-t))
    (h2 : (2 : F) ≠ 0) {c : F} (hc : c ≠ 0) (d : F) :
    (∑ x, ψ (c * x ^ 2 + d * x)) * star (∑ x, ψ (c * x ^ 2 + d * x)) = (Fintype.card F : R) := by
  rw [star_sum]
  simp_rw [hstar]
  rw [Finset.sum_mul_sum]
  -- `∑ x ∑ y ψ(c x² + d x) ψ(-(c y² + d y))`; reindex `x = y + t`
  have hre : ∀ y : F, ∑ x, ψ (c * x ^ 2 + d * x) * ψ (-(c * y ^ 2 + d * y)) =
      ∑ t, ψ (c * t ^ 2 + d * t) * ψ ((2 * c * t) * y) := by
    intro y
    rw [← Fintype.sum_equiv (Equiv.addLeft y) (fun t => ψ (c * (y + t) ^ 2 + d * (y + t)) *
        ψ (-(c * y ^ 2 + d * y))) _ (fun t => rfl)]
    refine Finset.sum_congr rfl fun t _ => ?_
    rw [← AddChar.map_add_eq_mul, ← AddChar.map_add_eq_mul]
    congr 1
    ring
  rw [Finset.sum_comm]
  simp_rw [hre]
  rw [Finset.sum_comm]
  simp_rw [← Finset.mul_sum]
  have hin : ∀ t : F, ∑ y, ψ ((2 * c * t) * y) =
      if t = 0 then (Fintype.card F : R) else 0 := by
    intro t
    rw [sum_mulShift hψ]
    by_cases ht : t = 0
    · simp [ht]
    · have : 2 * c * t ≠ 0 := mul_ne_zero (mul_ne_zero h2 hc) ht
      simp [ht, this]
  simp_rw [hin]
  rw [Finset.sum_eq_single (0 : F) (fun x _ hx => by simp [hx])
    (fun h => absurd (Finset.mem_univ (0 : F)) h)]
  simp

theorem pair_qvec_cross_mul_star {ψ : AddChar F R} (hψ : ψ ≠ 1)
    (hstar : ∀ t, star (ψ t) = ψ (-t)) (h2 : (2 : F) ≠ 0) {a a' : F} (ha : a ≠ a') (b b' : F) :
    pair (qvec ψ a b) (qvec ψ a' b') * star (pair (qvec ψ a b) (qvec ψ a' b')) =
      (Fintype.card F : R) := by
  have h : pair (qvec ψ a b) (qvec ψ a' b') = ∑ x, ψ ((a' - a) * x ^ 2 + (b' - b) * x) := by
    unfold pair qvec
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [hstar, ← AddChar.map_add_eq_mul]
    congr 1
    ring
  rw [h]
  exact weil_sum_mul_star hψ hstar h2 (sub_ne_zero.2 (Ne.symm ha)) _

/-! ### The packaged statement -/

/-- The norm of a member of basis `i`: `1` for the standard basis, `q` for the others. -/
def basisNorm (i : Option F) : R := match i with
  | none => 1
  | some _ => (Fintype.card F : R)

/-- Every basis is orthogonal, with the stated norms. -/
theorem basis_orthogonal {ψ : AddChar F R} (hψ : ψ ≠ 1) (hstar : ∀ t, star (ψ t) = ψ (-t))
    (i : Option F) (u v : F) :
    pair (basisVec ψ i u) (basisVec ψ i v) = if u = v then basisNorm i else 0 := by
  cases i with
  | none => exact pair_std u v
  | some a => exact pair_qvec_same hψ hstar a u v

/-- Members of two different bases are unbiased:
`|pair u v|² · q = pair u u · pair v v`. -/
theorem basis_unbiased {ψ : AddChar F R} (hψ : ψ ≠ 1) (hstar : ∀ t, star (ψ t) = ψ (-t))
    (h2 : (2 : F) ≠ 0) {i j : Option F} (hij : i ≠ j) (u v : F) :
    pair (basisVec ψ i u) (basisVec ψ j v) * star (pair (basisVec ψ i u) (basisVec ψ j v)) *
      (Fintype.card F : R) =
      pair (basisVec ψ i u) (basisVec ψ i u) * pair (basisVec ψ j v) (basisVec ψ j v) := by
  rw [basis_orthogonal hψ hstar i u u, basis_orthogonal hψ hstar j v v]
  simp only [ite_true]
  cases i with
  | none =>
    cases j with
    | none => exact absurd rfl hij
    | some a =>
      simp only [basisVec, basisNorm]
      rw [pair_std_qvec_mul_star hstar, one_mul]
  | some a =>
    cases j with
    | none =>
      simp only [basisVec, basisNorm]
      have hswap : pair (qvec ψ a u) (stdvec v) = star (pair (stdvec v) (qvec ψ a u)) := by
        unfold pair
        rw [star_sum]
        refine Finset.sum_congr rfl fun x _ => ?_
        rw [star_mul, star_star, mul_comm]
      rw [hswap, star_star, mul_comm, mul_comm (star (pair (stdvec v) (qvec ψ a u))),
        pair_std_qvec_mul_star hstar, mul_one]
    | some a' =>
      have haa : a ≠ a' := fun h => hij (by rw [h])
      simp only [basisVec, basisNorm]
      rw [pair_qvec_cross_mul_star hψ hstar h2 haa]

/-- **Complete MUB family in odd characteristic.**  For a finite field `F` with `2 ≠ 0`, a
nontrivial unitary additive character `ψ : F → R`, and `q ≠ 0` in `R`: the `q + 1` bases
`basisVec ψ i` (`i : Option F`) are each orthogonal with nonzero norms, and any two members of
different bases satisfy `|pair u v|² · q = ‖u‖² ‖v‖²`. -/
theorem mub_family {ψ : AddChar F R} (hψ : ψ ≠ 1) (hstar : ∀ t, star (ψ t) = ψ (-t))
    (h2 : (2 : F) ≠ 0) (hq : (Fintype.card F : R) ≠ 0) :
    (∀ i : Option F, ∀ u v : F,
        pair (basisVec ψ i u) (basisVec ψ i v) = if u = v then basisNorm i else 0) ∧
    (∀ i : Option F, basisNorm (F := F) (R := R) i ≠ 0) ∧
    (∀ i j : Option F, i ≠ j → ∀ u v : F,
        pair (basisVec ψ i u) (basisVec ψ j v) * star (pair (basisVec ψ i u) (basisVec ψ j v)) *
          (Fintype.card F : R) =
        pair (basisVec ψ i u) (basisVec ψ i u) * pair (basisVec ψ j v) (basisVec ψ j v)) := by
  refine ⟨basis_orthogonal hψ hstar, ?_, fun i j hij u v => basis_unbiased hψ hstar h2 hij u v⟩
  intro i
  cases i with
  | none => exact one_ne_zero
  | some _ => exact hq

omit [Field F] [DecidableEq F] in
/-- The family has `q + 1` bases. -/
theorem card_bases : Fintype.card (Option F) = Fintype.card F + 1 := Fintype.card_option

end MubPrimePower.PrimePowerOdd

#print axioms MubPrimePower.PrimePowerOdd.sum_mulShift
#print axioms MubPrimePower.PrimePowerOdd.pair_std
#print axioms MubPrimePower.PrimePowerOdd.pair_qvec_same
#print axioms MubPrimePower.PrimePowerOdd.pair_std_qvec_mul_star
#print axioms MubPrimePower.PrimePowerOdd.weil_sum_mul_star
#print axioms MubPrimePower.PrimePowerOdd.pair_qvec_cross_mul_star
#print axioms MubPrimePower.PrimePowerOdd.basis_orthogonal
#print axioms MubPrimePower.PrimePowerOdd.basis_unbiased
#print axioms MubPrimePower.PrimePowerOdd.mub_family
#print axioms MubPrimePower.PrimePowerOdd.card_bases
