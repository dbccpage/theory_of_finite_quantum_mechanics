import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Algebra.Group.Defs
import Mathlib.Data.Rat.Lemmas

namespace U1Fable.PythagoreanObstruction

/-!
# Rational Unit Circle and the Half-Angle Pythagorean Obstruction

This module mechanizes the rational unit circle carrier $S^1(\mathbb{Q})$ and proves:
1. $S^1(\mathbb{Q})$ forms a commutative group under Brahmagupta-Fibonacci multiplication.
2. Any square root $z \in S^1(\mathbb{Q})$ of the $(3/5, 4/5)$ Pythagorean phase must satisfy
   $z_{\mathrm{re}}^2 = 4/5$ and $z_{\mathrm{im}}^2 = 1/5$.
3. By unbounded 5-adic infinite descent over $\mathbb{N}$ and $\mathbb{Z}$, neither $4/5$ nor $1/5$
   is a square in $\mathbb{Q}$.
4. Consequently, $u_{345} = (3/5, 4/5)$ has no square root in $S^1(\mathbb{Q})$, $S^1(\mathbb{Q})$
   is not 2-divisible, and no homomorphism $\varphi : (\mathbb{Q}, +) \to S^1(\mathbb{Q})$ can hit
   $u_{345}$ at $1$.
-/

/-- The rational unit circle $S^1(\mathbb{Q}) = \{(a, b) \in \mathbb{Q}^2 \mid a^2 + b^2 = 1\}$. -/
@[ext]
structure RatCircle where
  re : ℚ
  im : ℚ
  norm_eq_one : re * re + im * im = 1
  deriving DecidableEq, Repr

/-- The multiplicative identity $(1, 0) \in S^1(\mathbb{Q})$. -/
def one : RatCircle := ⟨1, 0, by norm_num⟩

/-- The half-turn phase $(-1, 0) \in S^1(\mathbb{Q})$. -/
def negOne : RatCircle := ⟨-1, 0, by norm_num⟩

/-- The quarter-turn phase $(0, 1) \in S^1(\mathbb{Q})$. -/
def iUnit : RatCircle := ⟨0, 1, by norm_num⟩

/-- The inverse quarter-turn phase $(0, -1) \in S^1(\mathbb{Q})$. -/
def negIUnit : RatCircle := ⟨0, -1, by norm_num⟩

/-- The primitive $(3, 4, 5)$ Pythagorean phase $(3/5, 4/5) \in S^1(\mathbb{Q})$. -/
def u345 : RatCircle := ⟨3 / 5, 4 / 5, by norm_num⟩

/-- Brahmagupta-Fibonacci identity for two-square norm multiplicativity. -/
theorem brahmagupta_fibonacci (a b c d : ℚ) :
    (a * c - b * d) * (a * c - b * d) + (a * d + b * c) * (a * d + b * c) =
      (a * a + b * b) * (c * c + d * d) := by
  ring

/-- Unit norm conservation under complex multiplication on $S^1(\mathbb{Q})$. -/
theorem mul_norm_eq_one (z w : RatCircle) :
    (z.re * w.re - z.im * w.im) * (z.re * w.re - z.im * w.im) +
      (z.re * w.im + z.im * w.re) * (z.re * w.im + z.im * w.re) = 1 := by
  rw [brahmagupta_fibonacci, z.norm_eq_one, w.norm_eq_one, _root_.mul_one]

/-- Multiplication on $S^1(\mathbb{Q})$. -/
def mul (z w : RatCircle) : RatCircle :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re, mul_norm_eq_one z w⟩

/-- Unit norm conservation under conjugation on $S^1(\mathbb{Q})$. -/
theorem inv_norm_eq_one (z : RatCircle) :
    z.re * z.re + (-z.im) * (-z.im) = 1 := by
  calc
    z.re * z.re + (-z.im) * (-z.im) = z.re * z.re + z.im * z.im := by ring
    _ = 1 := z.norm_eq_one

/-- Inverse (complex conjugate) on $S^1(\mathbb{Q})$. -/
def inv (z : RatCircle) : RatCircle :=
  ⟨z.re, -z.im, inv_norm_eq_one z⟩

instance instOneRatCircle : One RatCircle := ⟨one⟩
instance instMulRatCircle : Mul RatCircle := ⟨mul⟩
instance instInvRatCircle : Inv RatCircle := ⟨inv⟩

@[simp] theorem one_re : (1 : RatCircle).re = 1 := rfl
@[simp] theorem one_im : (1 : RatCircle).im = 0 := rfl
@[simp] theorem mul_re (z w : RatCircle) : (z * w).re = z.re * w.re - z.im * w.im := rfl
@[simp] theorem mul_im (z w : RatCircle) : (z * w).im = z.re * w.im + z.im * w.re := rfl
@[simp] theorem inv_re (z : RatCircle) : (z⁻¹).re = z.re := rfl
@[simp] theorem inv_im (z : RatCircle) : (z⁻¹).im = -z.im := rfl

theorem mul_assoc (a b c : RatCircle) : a * b * c = a * (b * c) := by
  ext <;> simp only [mul_re, mul_im] <;> ring

theorem mul_comm (a b : RatCircle) : a * b = b * a := by
  ext <;> simp only [mul_re, mul_im] <;> ring

theorem one_mul (a : RatCircle) : 1 * a = a := by
  ext <;> simp only [mul_re, mul_im, one_re, one_im] <;> ring

theorem mul_one (a : RatCircle) : a * 1 = a := by
  ext <;> simp only [mul_re, mul_im, one_re, one_im] <;> ring

theorem mul_left_inv (a : RatCircle) : a⁻¹ * a = 1 := by
  ext
  · simp only [mul_re, inv_re, inv_im, one_re]
    calc
      a.re * a.re - -a.im * a.im = a.re * a.re + a.im * a.im := by ring
      _ = 1 := a.norm_eq_one
  · simp only [mul_im, inv_re, inv_im, one_im]
    ring

theorem mul_right_inv (a : RatCircle) : a * a⁻¹ = 1 := by
  rw [mul_comm, mul_left_inv]

instance instCommGroupRatCircle : CommGroup RatCircle where
  mul := mul
  mul_assoc := mul_assoc
  one := one
  one_mul := one_mul
  mul_one := mul_one
  inv := inv
  inv_mul_cancel := mul_left_inv
  mul_comm := mul_comm

/-! ## Half-Angle Constraint on $S^1(\mathbb{Q})$ -/

theorem sq_re (z : RatCircle) : (z * z).re = z.re * z.re - z.im * z.im := rfl

theorem sq_im (z : RatCircle) : (z * z).im = 2 * z.re * z.im := by
  simp only [mul_im]
  ring

theorem u345_sqrt_re_sq (z : RatCircle) (hz : z * z = u345) : z.re * z.re = 4 / 5 := by
  have hre : (z * z).re = u345.re := congrArg RatCircle.re hz
  have h1 : z.re * z.re - z.im * z.im = 3 / 5 := by
    simpa [sq_re, u345] using hre
  have h2 : z.re * z.re + z.im * z.im = 1 := z.norm_eq_one
  linarith

theorem u345_sqrt_im_sq (z : RatCircle) (hz : z * z = u345) : z.im * z.im = 1 / 5 := by
  have hre : (z * z).re = u345.re := congrArg RatCircle.re hz
  have h1 : z.re * z.re - z.im * z.im = 3 / 5 := by
    simpa [sq_re, u345] using hre
  have h2 : z.re * z.re + z.im * z.im = 1 := z.norm_eq_one
  linarith

/-! ## Unbounded 5-adic Non-Square Proofs over $\mathbb{N}$, $\mathbb{Z}$, and $\mathbb{Q}$ -/

theorem nat_sq_mod_five_eq_zero (y : ℕ) (h : (y * y) % 5 = 0) : y % 5 = 0 := by
  have hmul : (y * y) % 5 = ((y % 5) * (y % 5)) % 5 := Nat.mul_mod y y 5
  rw [hmul] at h
  have hcases : y % 5 = 0 ∨ y % 5 = 1 ∨ y % 5 = 2 ∨ y % 5 = 3 ∨ y % 5 = 4 := by omega
  rcases hcases with h0 | h1 | h2 | h3 | h4
  · exact h0
  · rw [h1] at h; omega
  · rw [h2] at h; omega
  · rw [h3] at h; omega
  · rw [h4] at h; omega

theorem nat_four_mul_sq_mod_five_eq_zero (y : ℕ) (h : (4 * (y * y)) % 5 = 0) : y % 5 = 0 := by
  have hmul1 : (4 * (y * y)) % 5 = ((4 % 5) * ((y * y) % 5)) % 5 := Nat.mul_mod 4 (y * y) 5
  have hmul2 : (y * y) % 5 = ((y % 5) * (y % 5)) % 5 := Nat.mul_mod y y 5
  rw [hmul1, hmul2] at h
  have hcases : y % 5 = 0 ∨ y % 5 = 1 ∨ y % 5 = 2 ∨ y % 5 = 3 ∨ y % 5 = 4 := by omega
  rcases hcases with h0 | h1 | h2 | h3 | h4
  · exact h0
  · rw [h1] at h; omega
  · rw [h2] at h; omega
  · rw [h3] at h; omega
  · rw [h4] at h; omega

theorem nat_five_mul_sq_eq_four_mul_sq (x y : ℕ) (h : 5 * (x * x) = 4 * (y * y)) :
    x = 0 ∧ y = 0 := by
  by_cases hy0 : y = 0
  · subst hy0
    have hx2 : x * x = 0 := by omega
    rcases Nat.mul_eq_zero.mp hx2 with hx | hx <;> exact ⟨hx, rfl⟩
  · have hmod_y : (4 * (y * y)) % 5 = 0 := by omega
    have hy5 : y % 5 = 0 := nat_four_mul_sq_mod_five_eq_zero y hmod_y
    set y' : ℕ := y / 5
    have hy_eq : y = 5 * y' := by omega
    have hx_sq : x * x = 5 * (4 * (y' * y')) := by
      have hsub : 5 * (x * x) = 5 * (5 * (4 * (y' * y'))) := by
        calc
          5 * (x * x) = 4 * (y * y) := h
          _ = 4 * ((5 * y') * (5 * y')) := by rw [hy_eq]
          _ = 5 * (5 * (4 * (y' * y'))) := by ring
      omega
    have hmod_x : (x * x) % 5 = 0 := by omega
    have hx5 : x % 5 = 0 := nat_sq_mod_five_eq_zero x hmod_x
    set x' : ℕ := x / 5
    have hx_eq : x = 5 * x' := by omega
    have hdesc : 5 * (x' * x') = 4 * (y' * y') := by
      have hsub2 : 5 * (5 * (x' * x')) = 5 * (4 * (y' * y')) := by
        calc
          5 * (5 * (x' * x')) = (5 * x') * (5 * x') := by ring
          _ = x * x := by rw [← hx_eq]
          _ = 5 * (4 * (y' * y')) := hx_sq
      omega
    have hy'_lt : y' < y := by omega
    have ih := nat_five_mul_sq_eq_four_mul_sq x' y' hdesc
    omega
termination_by y

theorem nat_five_mul_sq_eq_sq (x y : ℕ) (h : 5 * (x * x) = y * y) :
    x = 0 ∧ y = 0 := by
  by_cases hy0 : y = 0
  · subst hy0
    have hx2 : x * x = 0 := by omega
    rcases Nat.mul_eq_zero.mp hx2 with hx | hx <;> exact ⟨hx, rfl⟩
  · have hmod_y : (y * y) % 5 = 0 := by omega
    have hy5 : y % 5 = 0 := nat_sq_mod_five_eq_zero y hmod_y
    set y' : ℕ := y / 5
    have hy_eq : y = 5 * y' := by omega
    have hx_sq : x * x = 5 * (y' * y') := by
      have hsub : 5 * (x * x) = 5 * (5 * (y' * y')) := by
        calc
          5 * (x * x) = y * y := h
          _ = (5 * y') * (5 * y') := by rw [hy_eq]
          _ = 5 * (5 * (y' * y')) := by ring
      omega
    have hmod_x : (x * x) % 5 = 0 := by omega
    have hx5 : x % 5 = 0 := nat_sq_mod_five_eq_zero x hmod_x
    set x' : ℕ := x / 5
    have hx_eq : x = 5 * x' := by omega
    have hdesc : 5 * (x' * x') = y' * y' := by
      have hsub2 : 5 * (5 * (x' * x')) = 5 * (y' * y') := by
        calc
          5 * (5 * (x' * x')) = (5 * x') * (5 * x') := by ring
          _ = x * x := by rw [← hx_eq]
          _ = 5 * (y' * y') := hx_sq
      omega
    have hy'_lt : y' < y := by omega
    have ih := nat_five_mul_sq_eq_sq x' y' hdesc
    omega
termination_by y

theorem int_natAbs_sq (x : ℤ) : (x.natAbs : ℤ) * (x.natAbs : ℤ) = x * x := by
  rcases Int.natAbs_eq x with h | h
  · rw [← h]
  · calc
      (x.natAbs : ℤ) * (x.natAbs : ℤ) = (-(x.natAbs : ℤ)) * (-(x.natAbs : ℤ)) := by ring
      _ = x * x := by rw [← h]

theorem int_five_mul_sq_eq_four_mul_sq (x y : ℤ) (h : 5 * (x * x) = 4 * (y * y)) :
    x = 0 ∧ y = 0 := by
  have hx : (x.natAbs : ℤ) * (x.natAbs : ℤ) = x * x := int_natAbs_sq x
  have hy : (y.natAbs : ℤ) * (y.natAbs : ℤ) = y * y := int_natAbs_sq y
  have hnat : 5 * (x.natAbs * x.natAbs) = 4 * (y.natAbs * y.natAbs) := by
    have hint : (5 : ℤ) * ((x.natAbs : ℤ) * (x.natAbs : ℤ)) =
        4 * ((y.natAbs : ℤ) * (y.natAbs : ℤ)) := by
      rw [hx, hy, h]
    exact_mod_cast hint
  have hzero := nat_five_mul_sq_eq_four_mul_sq x.natAbs y.natAbs hnat
  omega

theorem int_five_mul_sq_eq_sq (x y : ℤ) (h : 5 * (x * x) = y * y) :
    x = 0 ∧ y = 0 := by
  have hx : (x.natAbs : ℤ) * (x.natAbs : ℤ) = x * x := int_natAbs_sq x
  have hy : (y.natAbs : ℤ) * (y.natAbs : ℤ) = y * y := int_natAbs_sq y
  have hnat : 5 * (x.natAbs * x.natAbs) = y.natAbs * y.natAbs := by
    have hint : (5 : ℤ) * ((x.natAbs : ℤ) * (x.natAbs : ℤ)) =
        (y.natAbs : ℤ) * (y.natAbs : ℤ) := by
      rw [hx, hy, h]
    exact_mod_cast hint
  have hzero := nat_five_mul_sq_eq_sq x.natAbs y.natAbs hnat
  omega

theorem four_fifths_not_rat_square : ¬ ∃ q : ℚ, q * q = 4 / 5 := by
  rintro ⟨q, hq⟩
  have hden_nz : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr q.den_nz
  have hnum : q * (q.den : ℚ) = (q.num : ℚ) := by
    calc
      q * (q.den : ℚ) = ((q.num : ℚ) / (q.den : ℚ)) * (q.den : ℚ) := by
        rw [Rat.num_div_den q]
      _ = (q.num : ℚ) := div_mul_cancel₀ (q.num : ℚ) hden_nz
  have hrat : (5 : ℚ) * ((q.num : ℚ) * (q.num : ℚ)) =
      4 * ((q.den : ℚ) * (q.den : ℚ)) := by
    calc
      (5 : ℚ) * ((q.num : ℚ) * (q.num : ℚ))
        = 5 * ((q * (q.den : ℚ)) * (q * (q.den : ℚ))) := by rw [hnum]
      _ = 5 * (q * q) * ((q.den : ℚ) * (q.den : ℚ)) := by ring
      _ = 5 * (4 / 5) * ((q.den : ℚ) * (q.den : ℚ)) := by rw [hq]
      _ = 4 * ((q.den : ℚ) * (q.den : ℚ)) := by ring
  have hint : 5 * (q.num * q.num) = 4 * ((q.den : ℤ) * (q.den : ℤ)) := by
    exact_mod_cast hrat
  have hzero := int_five_mul_sq_eq_four_mul_sq q.num (q.den : ℤ) hint
  have hden0 : q.den = 0 := by omega
  exact q.den_nz hden0

theorem one_fifth_not_rat_square : ¬ ∃ q : ℚ, q * q = 1 / 5 := by
  rintro ⟨q, hq⟩
  have hden_nz : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr q.den_nz
  have hnum : q * (q.den : ℚ) = (q.num : ℚ) := by
    calc
      q * (q.den : ℚ) = ((q.num : ℚ) / (q.den : ℚ)) * (q.den : ℚ) := by
        rw [Rat.num_div_den q]
      _ = (q.num : ℚ) := div_mul_cancel₀ (q.num : ℚ) hden_nz
  have hrat : (5 : ℚ) * ((q.num : ℚ) * (q.num : ℚ)) =
      (q.den : ℚ) * (q.den : ℚ) := by
    calc
      (5 : ℚ) * ((q.num : ℚ) * (q.num : ℚ))
        = 5 * ((q * (q.den : ℚ)) * (q * (q.den : ℚ))) := by rw [hnum]
      _ = 5 * (q * q) * ((q.den : ℚ) * (q.den : ℚ)) := by ring
      _ = 5 * (1 / 5) * ((q.den : ℚ) * (q.den : ℚ)) := by rw [hq]
      _ = (q.den : ℚ) * (q.den : ℚ) := by ring
  have hint : 5 * (q.num * q.num) = (q.den : ℤ) * (q.den : ℤ) := by
    exact_mod_cast hrat
  have hzero := int_five_mul_sq_eq_sq q.num (q.den : ℤ) hint
  have hden0 : q.den = 0 := by omega
  exact q.den_nz hden0

/-! ## Main Obstruction Theorems -/

theorem u345_no_rat_circle_sqrt : ¬ ∃ z : RatCircle, z * z = u345 := by
  rintro ⟨z, hz⟩
  exact four_fifths_not_rat_square ⟨z.re, u345_sqrt_re_sq z hz⟩

theorem rat_circle_not_two_divisible : ¬ ∀ w : RatCircle, ∃ z : RatCircle, z * z = w := by
  intro hdiv
  exact u345_no_rat_circle_sqrt (hdiv u345)

theorem no_rat_add_to_rat_circle_hom_u345 :
    ¬ ∃ φ : ℚ → RatCircle, (∀ p q : ℚ, φ (p + q) = φ p * φ q) ∧ φ 1 = u345 := by
  rintro ⟨φ, hhom, h1⟩
  have hhalf : φ (1 / 2) * φ (1 / 2) = u345 := by
    have hadd : (1 / 2 : ℚ) + 1 / 2 = 1 := by norm_num
    calc
      φ (1 / 2) * φ (1 / 2) = φ (1 / 2 + 1 / 2) := (hhom (1 / 2) (1 / 2)).symm
      _ = φ 1 := by rw [hadd]
      _ = u345 := h1
  exact u345_no_rat_circle_sqrt ⟨φ (1 / 2), hhalf⟩

end U1Fable.PythagoreanObstruction

#print axioms U1Fable.PythagoreanObstruction.RatCircle
#print axioms U1Fable.PythagoreanObstruction.one
#print axioms U1Fable.PythagoreanObstruction.negOne
#print axioms U1Fable.PythagoreanObstruction.iUnit
#print axioms U1Fable.PythagoreanObstruction.negIUnit
#print axioms U1Fable.PythagoreanObstruction.u345
#print axioms U1Fable.PythagoreanObstruction.brahmagupta_fibonacci
#print axioms U1Fable.PythagoreanObstruction.mul_norm_eq_one
#print axioms U1Fable.PythagoreanObstruction.mul
#print axioms U1Fable.PythagoreanObstruction.inv_norm_eq_one
#print axioms U1Fable.PythagoreanObstruction.inv
#print axioms U1Fable.PythagoreanObstruction.instOneRatCircle
#print axioms U1Fable.PythagoreanObstruction.instMulRatCircle
#print axioms U1Fable.PythagoreanObstruction.instInvRatCircle
#print axioms U1Fable.PythagoreanObstruction.one_re
#print axioms U1Fable.PythagoreanObstruction.one_im
#print axioms U1Fable.PythagoreanObstruction.mul_re
#print axioms U1Fable.PythagoreanObstruction.mul_im
#print axioms U1Fable.PythagoreanObstruction.inv_re
#print axioms U1Fable.PythagoreanObstruction.inv_im
#print axioms U1Fable.PythagoreanObstruction.mul_assoc
#print axioms U1Fable.PythagoreanObstruction.mul_comm
#print axioms U1Fable.PythagoreanObstruction.one_mul
#print axioms U1Fable.PythagoreanObstruction.mul_one
#print axioms U1Fable.PythagoreanObstruction.mul_left_inv
#print axioms U1Fable.PythagoreanObstruction.mul_right_inv
#print axioms U1Fable.PythagoreanObstruction.instCommGroupRatCircle
#print axioms U1Fable.PythagoreanObstruction.sq_re
#print axioms U1Fable.PythagoreanObstruction.sq_im
#print axioms U1Fable.PythagoreanObstruction.u345_sqrt_re_sq
#print axioms U1Fable.PythagoreanObstruction.u345_sqrt_im_sq
#print axioms U1Fable.PythagoreanObstruction.nat_sq_mod_five_eq_zero
#print axioms U1Fable.PythagoreanObstruction.nat_four_mul_sq_mod_five_eq_zero
#print axioms U1Fable.PythagoreanObstruction.nat_five_mul_sq_eq_four_mul_sq
#print axioms U1Fable.PythagoreanObstruction.nat_five_mul_sq_eq_sq
#print axioms U1Fable.PythagoreanObstruction.int_natAbs_sq
#print axioms U1Fable.PythagoreanObstruction.int_five_mul_sq_eq_four_mul_sq
#print axioms U1Fable.PythagoreanObstruction.int_five_mul_sq_eq_sq
#print axioms U1Fable.PythagoreanObstruction.four_fifths_not_rat_square
#print axioms U1Fable.PythagoreanObstruction.one_fifth_not_rat_square
#print axioms U1Fable.PythagoreanObstruction.u345_no_rat_circle_sqrt
#print axioms U1Fable.PythagoreanObstruction.rat_circle_not_two_divisible
#print axioms U1Fable.PythagoreanObstruction.no_rat_add_to_rat_circle_hom_u345

private def l5aProvenance : String :=
  "Origin: lean4/U1PythagoreanObstruction.lean Claim: u345_no_rat_circle_sqrt AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
