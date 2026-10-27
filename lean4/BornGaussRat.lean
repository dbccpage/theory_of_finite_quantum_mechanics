import Mathlib.Algebra.Algebra.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Algebra.CharZero.Defs
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.Order.Ring.Unbundled.Basic
import Mathlib.Algebra.Star.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-
Gaussian rationals ℚ(i) as a concrete structure; AuthorityEffect: None; supplied carrier arithmetic, no physical claim.

`GaussRat` is the pair type `⟨re, im⟩` over ℚ with the usual complex arithmetic, conjugation
`star ⟨a, b⟩ = ⟨a, -b⟩`, the unit `I = ⟨0, 1⟩`, and `normSq z = z.re ^ 2 + z.im ^ 2`.  It carries
`CommRing`, `StarRing`, `Algebra ℚ`, `Field`, `Nontrivial` and `CharZero` instances, componentwise
simp lemmas, the positivity facts `normSq_nonneg` / `normSq_eq_zero_iff` / `star_mul_self`, and
the ℚ-linearity of the real part over finite sums (`re_sum`, `im_sum`).  Everything is exact
arithmetic over ℚ; nothing here is a physical statement.
-/

namespace BornFinite

/-- The Gaussian rationals ℚ(i), stored as a real and an imaginary rational part. -/
@[ext]
structure GaussRat where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Inhabited

namespace GaussRat

/-! ### Primitive operations -/

instance instZero : Zero GaussRat := ⟨⟨0, 0⟩⟩
instance instOne : One GaussRat := ⟨⟨1, 0⟩⟩
instance instAdd : Add GaussRat := ⟨fun z w => ⟨z.re + w.re, z.im + w.im⟩⟩
instance instNeg : Neg GaussRat := ⟨fun z => ⟨-z.re, -z.im⟩⟩
instance instSub : Sub GaussRat := ⟨fun z w => ⟨z.re - w.re, z.im - w.im⟩⟩
instance instMul : Mul GaussRat :=
  ⟨fun z w => ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩⟩
instance instSMul : SMul ℚ GaussRat := ⟨fun q z => ⟨q * z.re, q * z.im⟩⟩
instance instNatSMul : SMul ℕ GaussRat := ⟨fun n z => ⟨n * z.re, n * z.im⟩⟩
instance instIntSMul : SMul ℤ GaussRat := ⟨fun n z => ⟨n * z.re, n * z.im⟩⟩
instance instStar : Star GaussRat := ⟨fun z => ⟨z.re, -z.im⟩⟩
instance instNatCast : NatCast GaussRat := ⟨fun n => ⟨n, 0⟩⟩
instance instIntCast : IntCast GaussRat := ⟨fun n => ⟨n, 0⟩⟩
instance instRatCast : RatCast GaussRat := ⟨fun q => ⟨q, 0⟩⟩

/-- The imaginary unit `i = ⟨0, 1⟩`. -/
def I : GaussRat := ⟨0, 1⟩

/-- The squared modulus `re ^ 2 + im ^ 2`, a rational number. -/
def normSq (z : GaussRat) : ℚ := z.re ^ 2 + z.im ^ 2

/-! ### Componentwise simp lemmas -/

@[simp] theorem re_zero : (0 : GaussRat).re = 0 := rfl
@[simp] theorem im_zero : (0 : GaussRat).im = 0 := rfl
@[simp] theorem re_one : (1 : GaussRat).re = 1 := rfl
@[simp] theorem im_one : (1 : GaussRat).im = 0 := rfl
@[simp] theorem re_add (z w : GaussRat) : (z + w).re = z.re + w.re := rfl
@[simp] theorem im_add (z w : GaussRat) : (z + w).im = z.im + w.im := rfl
@[simp] theorem re_neg (z : GaussRat) : (-z).re = -z.re := rfl
@[simp] theorem im_neg (z : GaussRat) : (-z).im = -z.im := rfl
@[simp] theorem re_sub (z w : GaussRat) : (z - w).re = z.re - w.re := rfl
@[simp] theorem im_sub (z w : GaussRat) : (z - w).im = z.im - w.im := rfl
@[simp] theorem re_mul (z w : GaussRat) : (z * w).re = z.re * w.re - z.im * w.im := rfl
@[simp] theorem im_mul (z w : GaussRat) : (z * w).im = z.re * w.im + z.im * w.re := rfl
@[simp] theorem re_smul (q : ℚ) (z : GaussRat) : (q • z).re = q * z.re := rfl
@[simp] theorem im_smul (q : ℚ) (z : GaussRat) : (q • z).im = q * z.im := rfl
@[simp] theorem re_nsmul (n : ℕ) (z : GaussRat) : (n • z).re = n * z.re := rfl
@[simp] theorem im_nsmul (n : ℕ) (z : GaussRat) : (n • z).im = n * z.im := rfl
@[simp] theorem re_zsmul (n : ℤ) (z : GaussRat) : (n • z).re = n * z.re := rfl
@[simp] theorem im_zsmul (n : ℤ) (z : GaussRat) : (n • z).im = n * z.im := rfl
@[simp] theorem re_star (z : GaussRat) : (star z).re = z.re := rfl
@[simp] theorem im_star (z : GaussRat) : (star z).im = -z.im := rfl
@[simp] theorem re_I : I.re = 0 := rfl
@[simp] theorem im_I : I.im = 1 := rfl
@[simp] theorem re_natCast (n : ℕ) : (n : GaussRat).re = n := rfl
@[simp] theorem im_natCast (n : ℕ) : (n : GaussRat).im = 0 := rfl
@[simp] theorem re_intCast (n : ℤ) : (n : GaussRat).re = n := rfl
@[simp] theorem im_intCast (n : ℤ) : (n : GaussRat).im = 0 := rfl
@[simp] theorem re_ratCast (q : ℚ) : (q : GaussRat).re = q := rfl
@[simp] theorem im_ratCast (q : ℚ) : (q : GaussRat).im = 0 := rfl

@[simp] theorem smul_mk (q a b : ℚ) : q • (⟨a, b⟩ : GaussRat) = ⟨q * a, q * b⟩ := rfl

/-! ### Commutative ring structure -/

instance instCommRing : CommRing GaussRat where
  add_assoc a b c := by ext <;> simp <;> ring
  zero_add a := by ext <;> simp
  add_zero a := by ext <;> simp
  nsmul_zero z := by ext <;> simp
  nsmul_succ n z := by
    ext
    · simp only [re_nsmul, re_add, Nat.cast_succ]
      ring
    · simp only [im_nsmul, im_add, Nat.cast_succ]
      ring
  sub_eq_add_neg a b := by ext <;> simp <;> ring
  zsmul_zero' z := by ext <;> simp
  zsmul_succ' n z := by
    ext
    · simp only [re_zsmul, re_add]
      push_cast
      ring
    · simp only [im_zsmul, im_add]
      push_cast
      ring
  zsmul_neg' n z := by
    ext
    · simp only [re_zsmul, re_neg, Int.cast_negSucc]
      push_cast
      ring
    · simp only [im_zsmul, im_neg, Int.cast_negSucc]
      push_cast
      ring
  neg_add_cancel a := by ext <;> simp
  add_comm a b := by ext <;> simp <;> ring
  left_distrib a b c := by ext <;> simp <;> ring
  right_distrib a b c := by ext <;> simp <;> ring
  zero_mul a := by ext <;> simp
  mul_zero a := by ext <;> simp
  mul_assoc a b c := by ext <;> simp <;> ring
  one_mul a := by ext <;> simp
  mul_one a := by ext <;> simp
  natCast_zero := by ext <;> simp
  natCast_succ n := by ext <;> simp
  intCast_ofNat n := by ext <;> simp
  intCast_negSucc n := by ext <;> simp
  mul_comm a b := by ext <;> simp <;> ring

@[simp] theorem re_ofNat (n : ℕ) [n.AtLeastTwo] : (ofNat(n) : GaussRat).re = ofNat(n) := rfl
@[simp] theorem im_ofNat (n : ℕ) [n.AtLeastTwo] : (ofNat(n) : GaussRat).im = 0 := rfl

instance instNontrivial : Nontrivial GaussRat :=
  ⟨⟨0, 1, fun h => zero_ne_one (congrArg re h)⟩⟩

instance instCharZero : CharZero GaussRat where
  cast_injective := by
    intro m n h
    have h' : (m : ℚ) = (n : ℚ) := congrArg re h
    exact Nat.cast_injective h'

/-! ### Star ring structure (complex conjugation) -/

instance instStarRing : StarRing GaussRat where
  star_involutive z := by ext <;> simp
  star_mul z w := by ext <;> simp <;> ring
  star_add z w := by
    ext
    · rfl
    · simp only [im_star, im_add]
      ring

theorem star_I : star I = -I := by ext <;> simp

/-! ### ℚ-algebra structure -/

/-- The canonical ring embedding `ℚ →+* ℚ(i)`, `q ↦ ⟨q, 0⟩`. -/
def ofRat : ℚ →+* GaussRat where
  toFun q := ⟨q, 0⟩
  map_one' := rfl
  map_mul' q r := by ext <;> simp
  map_zero' := rfl
  map_add' q r := by ext <;> simp

@[simp] theorem re_ofRat (q : ℚ) : (ofRat q).re = q := rfl
@[simp] theorem im_ofRat (q : ℚ) : (ofRat q).im = 0 := rfl

instance instAlgebra : Algebra ℚ GaussRat where
  algebraMap := ofRat
  commutes' q z := mul_comm (ofRat q) z
  smul_def' q z := by ext <;> simp

@[simp] theorem re_algebraMap (q : ℚ) : (algebraMap ℚ GaussRat q).re = q := rfl
@[simp] theorem im_algebraMap (q : ℚ) : (algebraMap ℚ GaussRat q).im = 0 := rfl
theorem algebraMap_eq_ratCast (q : ℚ) : algebraMap ℚ GaussRat q = (q : GaussRat) := rfl

theorem I_mul_I : I * I = -1 := by ext <;> simp

theorem mk_eq_add_mul_I (a b : ℚ) :
    (⟨a, b⟩ : GaussRat) = algebraMap ℚ GaussRat a + algebraMap ℚ GaussRat b * I := by
  ext <;> simp

/-! ### The squared modulus and Hermitian products -/

theorem normSq_nonneg (z : GaussRat) : 0 ≤ normSq z :=
  add_nonneg (sq_nonneg _) (sq_nonneg _)

theorem normSq_eq_zero_iff (z : GaussRat) : normSq z = 0 ↔ z = 0 := by
  rw [normSq, sq, sq, mul_self_add_mul_self_eq_zero, GaussRat.ext_iff, re_zero, im_zero]

theorem normSq_mul (z w : GaussRat) : normSq (z * w) = normSq z * normSq w := by
  simp only [normSq, re_mul, im_mul]
  ring

@[simp] theorem normSq_natCast (n : ℕ) : normSq (n : GaussRat) = (n : ℚ) ^ 2 := by
  rw [normSq, re_natCast, im_natCast]
  ring

theorem star_mul_self (z : GaussRat) : star z * z = algebraMap ℚ GaussRat (normSq z) := by
  ext
  · rw [re_mul, re_star, im_star, re_algebraMap, normSq]
    ring
  · rw [im_mul, re_star, im_star, im_algebraMap]
    ring

theorem re_star_mul_self (z : GaussRat) : (star z * z).re = normSq z := by
  rw [GaussRat.star_mul_self, re_algebraMap]

theorem im_star_mul_self (z : GaussRat) : (star z * z).im = 0 := by
  rw [GaussRat.star_mul_self, im_algebraMap]

theorem re_star_mul (z w : GaussRat) : (star z * w).re = z.re * w.re + z.im * w.im := by
  rw [re_mul, re_star, im_star]
  ring

theorem im_star_mul (z w : GaussRat) : (star z * w).im = z.re * w.im - z.im * w.re := by
  rw [im_mul, re_star, im_star]
  ring

theorem re_star_mul_comm (z w : GaussRat) : (star z * w).re = (star w * z).re := by
  rw [re_star_mul, re_star_mul]
  ring

theorem im_star_mul_comm (z w : GaussRat) : (star z * w).im = -(star w * z).im := by
  rw [im_star_mul, im_star_mul]
  ring

theorem re_smul_rat (q : ℚ) (z : GaussRat) : (q • z).re = q * z.re := rfl

theorem re_algebraMap_mul (q : ℚ) (z : GaussRat) :
    (algebraMap ℚ GaussRat q * z).re = q * z.re := by
  rw [re_mul, re_algebraMap, im_algebraMap, zero_mul, sub_zero]

/-! ### The real and imaginary parts are additive (hence ℚ-linear) -/

/-- The real part as an additive monoid homomorphism `ℚ(i) →+ ℚ`. -/
def reAddMonoidHom : GaussRat →+ ℚ where
  toFun := re
  map_zero' := rfl
  map_add' _ _ := rfl

/-- The imaginary part as an additive monoid homomorphism `ℚ(i) →+ ℚ`. -/
def imAddMonoidHom : GaussRat →+ ℚ where
  toFun := im
  map_zero' := rfl
  map_add' _ _ := rfl

@[simp] theorem reAddMonoidHom_apply (z : GaussRat) : reAddMonoidHom z = z.re := rfl
@[simp] theorem imAddMonoidHom_apply (z : GaussRat) : imAddMonoidHom z = z.im := rfl

@[simp] theorem re_sum {ι : Type*} (s : Finset ι) (f : ι → GaussRat) :
    (∑ i ∈ s, f i).re = ∑ i ∈ s, (f i).re :=
  map_sum reAddMonoidHom f s

@[simp] theorem im_sum {ι : Type*} (s : Finset ι) (f : ι → GaussRat) :
    (∑ i ∈ s, f i).im = ∑ i ∈ s, (f i).im :=
  map_sum imAddMonoidHom f s

/-! ### Field structure -/

instance instInv : Inv GaussRat := ⟨fun z => (normSq z)⁻¹ • star z⟩

@[simp] theorem re_inv (z : GaussRat) : z⁻¹.re = (normSq z)⁻¹ * z.re := rfl
@[simp] theorem im_inv (z : GaussRat) : z⁻¹.im = (normSq z)⁻¹ * -z.im := rfl

protected theorem inv_zero : (0 : GaussRat)⁻¹ = 0 := by ext <;> simp

protected theorem mul_inv_cancel (z : GaussRat) (hz : z ≠ 0) : z * z⁻¹ = 1 := by
  have h : normSq z ≠ 0 := fun h0 => hz ((normSq_eq_zero_iff z).mp h0)
  have h2 : z.re * ((normSq z)⁻¹ * z.re) - z.im * ((normSq z)⁻¹ * -z.im) =
      (normSq z)⁻¹ * normSq z := by
    unfold normSq
    ring
  ext
  · rw [re_mul, re_inv, im_inv, re_one, h2, inv_mul_cancel₀ h]
  · rw [im_mul, re_inv, im_inv, im_one]
    ring

instance instDivInvMonoid : DivInvMonoid GaussRat where

instance instField : Field GaussRat where
  mul_inv_cancel := GaussRat.mul_inv_cancel
  inv_zero := GaussRat.inv_zero
  nnqsmul := _
  qsmul := (· • ·)
  qsmul_def q z := by ext <;> simp
  ratCast_def q := by
    have hd : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr q.den_ne_zero
    have h2 : ((q.den : ℚ) ^ 2)⁻¹ * (q.den : ℚ) = (q.den : ℚ)⁻¹ := by
      rw [sq, mul_inv, mul_assoc, inv_mul_cancel₀ hd, mul_one]
    ext
    · simp only [re_ratCast, div_eq_mul_inv, re_mul, re_inv, im_inv, re_intCast, im_intCast,
        re_natCast, im_natCast, normSq_natCast, zero_mul, sub_zero]
      rw [h2, ← div_eq_mul_inv, Rat.num_div_den]
    · simp [div_eq_mul_inv]

/-! ### Instance sanity checks -/

example : Module ℚ GaussRat := inferInstance
example : IsScalarTower ℚ GaussRat GaussRat := inferInstance
example : SMulCommClass ℚ GaussRat GaussRat := inferInstance
example : ((⟨3, 4⟩ : GaussRat) * star ⟨3, 4⟩).re = 25 := by norm_num
example : normSq ⟨3, 4⟩ = 25 := by norm_num [normSq]

end GaussRat

end BornFinite

#print axioms BornFinite.GaussRat.instCommRing
#print axioms BornFinite.GaussRat.instStarRing
#print axioms BornFinite.GaussRat.instAlgebra
#print axioms BornFinite.GaussRat.instField
#print axioms BornFinite.GaussRat.instNontrivial
#print axioms BornFinite.GaussRat.instCharZero
#print axioms BornFinite.GaussRat.re_zero
#print axioms BornFinite.GaussRat.im_zero
#print axioms BornFinite.GaussRat.re_one
#print axioms BornFinite.GaussRat.im_one
#print axioms BornFinite.GaussRat.re_add
#print axioms BornFinite.GaussRat.im_add
#print axioms BornFinite.GaussRat.re_neg
#print axioms BornFinite.GaussRat.im_neg
#print axioms BornFinite.GaussRat.re_sub
#print axioms BornFinite.GaussRat.im_sub
#print axioms BornFinite.GaussRat.re_mul
#print axioms BornFinite.GaussRat.im_mul
#print axioms BornFinite.GaussRat.re_smul
#print axioms BornFinite.GaussRat.im_smul
#print axioms BornFinite.GaussRat.re_star
#print axioms BornFinite.GaussRat.im_star
#print axioms BornFinite.GaussRat.re_I
#print axioms BornFinite.GaussRat.im_I
#print axioms BornFinite.GaussRat.re_natCast
#print axioms BornFinite.GaussRat.im_natCast
#print axioms BornFinite.GaussRat.re_intCast
#print axioms BornFinite.GaussRat.im_intCast
#print axioms BornFinite.GaussRat.re_ratCast
#print axioms BornFinite.GaussRat.im_ratCast
#print axioms BornFinite.GaussRat.smul_mk
#print axioms BornFinite.GaussRat.re_nsmul
#print axioms BornFinite.GaussRat.im_nsmul
#print axioms BornFinite.GaussRat.re_zsmul
#print axioms BornFinite.GaussRat.im_zsmul
#print axioms BornFinite.GaussRat.re_ofNat
#print axioms BornFinite.GaussRat.im_ofNat
#print axioms BornFinite.GaussRat.star_I
#print axioms BornFinite.GaussRat.re_ofRat
#print axioms BornFinite.GaussRat.im_ofRat
#print axioms BornFinite.GaussRat.re_algebraMap
#print axioms BornFinite.GaussRat.im_algebraMap
#print axioms BornFinite.GaussRat.algebraMap_eq_ratCast
#print axioms BornFinite.GaussRat.I_mul_I
#print axioms BornFinite.GaussRat.mk_eq_add_mul_I
#print axioms BornFinite.GaussRat.normSq_nonneg
#print axioms BornFinite.GaussRat.normSq_eq_zero_iff
#print axioms BornFinite.GaussRat.normSq_mul
#print axioms BornFinite.GaussRat.normSq_natCast
#print axioms BornFinite.GaussRat.star_mul_self
#print axioms BornFinite.GaussRat.re_star_mul_self
#print axioms BornFinite.GaussRat.im_star_mul_self
#print axioms BornFinite.GaussRat.re_star_mul
#print axioms BornFinite.GaussRat.im_star_mul
#print axioms BornFinite.GaussRat.re_star_mul_comm
#print axioms BornFinite.GaussRat.im_star_mul_comm
#print axioms BornFinite.GaussRat.re_smul_rat
#print axioms BornFinite.GaussRat.re_algebraMap_mul
#print axioms BornFinite.GaussRat.reAddMonoidHom_apply
#print axioms BornFinite.GaussRat.imAddMonoidHom_apply
#print axioms BornFinite.GaussRat.re_sum
#print axioms BornFinite.GaussRat.im_sum
#print axioms BornFinite.GaussRat.re_inv
#print axioms BornFinite.GaussRat.im_inv
#print axioms BornFinite.GaussRat.inv_zero
#print axioms BornFinite.GaussRat.mul_inv_cancel
