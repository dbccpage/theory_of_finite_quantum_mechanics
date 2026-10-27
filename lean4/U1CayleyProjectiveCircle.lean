import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Rat.Lemmas

/-!
# Exact Rational Cayley Stereographic Parameterization & Projective Circle Completion

This module mechanizes the algebraic and projective structure of the rational circle
$S^1(\mathbb{Q}) = \{(x, y) \in \mathbb{Q}^2 \mid x^2 + y^2 = 1\}$:

1. **Affine Rational Cayley Parameterization & South-Pole Puncture**:
   The affine map $t \mapsto \left(\frac{1-t^2}{1+t^2}, \frac{2t}{1+t^2}\right)$ maps
   $\mathbb{Q}$ bijectively onto the punctured rational circle $S^1(\mathbb{Q}) \setminus \{(-1, 0)\}$,
   with inverse $(x, y) \mapsto \frac{y}{x+1}$.
2. **Affine Cayley Tangent Group Law & Pole Collision**:
   Circle multiplication $(x_1, y_1) \cdot (x_2, y_2) = (x_1 x_2 - y_1 y_2, x_1 y_2 + y_1 x_2)$
   pulls back along `cayley` to the rational tangent addition formula $\frac{t_1 + t_2}{1 - t_1 t_2}$
   whenever $1 - t_1 t_2 \neq 0$, and collides with the punctured south pole $(-1, 0)$ whenever
   $t_1 t_2 = 1$.
3. **Homogeneous Projective Line $\mathbb{P}^1(\mathbb{Q})$ One-Point Compactification**:
   Lifting to homogeneous coordinates $[u : v] \in \mathbb{P}^1(\mathbb{Q})$ with $(u, v) \neq (0, 0)$
   resolves the affine pole singularity: $[1 : t]$ recovers the affine chart, $[0 : 1]$ maps
   to the south pole $(-1, 0)$, the homogeneous Cayley map is scale-invariant and surjective
   onto all of $S^1(\mathbb{Q})$, and homogeneous Gaussian multiplication $[u_1 u_2 - v_1 v_2 : u_1 v_2 + v_1 u_2]$
   makes `homCayley` a globally defined group homomorphism without pole exceptions.
4. **Elliptic Anisotropy vs. Hyperbolic Split-Complex Zero Divisors**:
   The elliptic quadratic form $u^2 + v^2$ is anisotropic over $\mathbb{Q}$ ($u^2 + v^2 = 0 \implies u = v = 0$),
   guaranteeing non-vanishing projective denominators everywhere on $\mathbb{P}^1(\mathbb{Q})$, in sharp
   contrast to the hyperbolic split-complex form $u^2 - v^2$ which has non-trivial null vectors $(1, 1)$.
-/

namespace U1Finite.CayleyProjective

/-! ## Section 1: Elliptic Norm Anisotropy & Affine Cayley Parameterization -/

/-- The elliptic quadratic form `u * u + v * v` over `ℚ` is anisotropic:
    it vanishes if and only if both coordinates vanish. -/
theorem elliptic_norm_anisotropic (u v : ℚ) (h : u * u + v * v = 0) : u = 0 ∧ v = 0 := by
  have hu : 0 ≤ u * u := mul_self_nonneg u
  have hv : 0 ≤ v * v := mul_self_nonneg v
  have hu0 : u * u = 0 := by linarith
  have hv0 : v * v = 0 := by linarith
  exact ⟨mul_self_eq_zero.mp hu0, mul_self_eq_zero.mp hv0⟩

/-- In contrast, the hyperbolic split-complex norm `u * u - v * v` admits non-zero null vectors
    (zero divisors) at `(1, 1)`. -/
theorem hyperbolic_split_zero_divisor :
    (1 : ℚ) * 1 - 1 * 1 = 0 ∧ ((1 : ℚ), (1 : ℚ)) ≠ (0, 0) := by
  refine ⟨by norm_num, ?_⟩
  intro h
  have h1 : (1 : ℚ) = 0 := congrArg Prod.fst h
  norm_num at h1

/-- The affine Cayley denominator `1 + t * t` is strictly positive for every `t : ℚ`. -/
theorem cayleyDenom_pos (t : ℚ) : 0 < 1 + t * t := by
  have hsq : 0 ≤ t * t := mul_self_nonneg t
  linarith

/-- The affine Cayley denominator `1 + t * t` is never zero over `ℚ`. -/
theorem cayleyDenom_ne_zero (t : ℚ) : 1 + t * t ≠ 0 :=
  ne_of_gt (cayleyDenom_pos t)

/-- The affine rational Cayley stereographic parameterization of the unit circle. -/
def cayley (t : ℚ) : ℚ × ℚ :=
  ((1 - t * t) / (1 + t * t), (2 * t) / (1 + t * t))

/-- Polynomial cleared-denominator Pythagorean identity underlying the Cayley map. -/
theorem cayley_cleared_identity (t : ℚ) :
    (1 - t * t) ^ 2 + (2 * t) ^ 2 = (1 + t * t) ^ 2 := by
  ring

/-- Every point in the image of `cayley` lies on the unit circle $x^2 + y^2 = 1$. -/
theorem cayley_unit_norm (t : ℚ) : (cayley t).1 ^ 2 + (cayley t).2 ^ 2 = 1 := by
  have hne : 1 + t * t ≠ 0 := cayleyDenom_ne_zero t
  unfold cayley
  dsimp
  field_simp [hne]
  ring

/-- Identity for `(cayley t).1 + 1`, showing it is always strictly positive. -/
theorem cayley_re_add_one (t : ℚ) : (cayley t).1 + 1 = 2 / (1 + t * t) := by
  have hne : 1 + t * t ≠ 0 := cayleyDenom_ne_zero t
  unfold cayley
  dsimp
  field_simp [hne]
  ring

/-- The first coordinate of `cayley t` never equals `-1`. -/
theorem cayley_re_ne_neg_one (t : ℚ) : (cayley t).1 ≠ -1 := by
  intro h
  have hadd : (cayley t).1 + 1 = 0 := by linarith
  rw [cayley_re_add_one] at hadd
  have hpos : 0 < 2 / (1 + t * t) := div_pos (by norm_num) (cayleyDenom_pos t)
  linarith

/-- The affine Cayley parameterization misses the south pole `(-1, 0)`. -/
theorem cayley_misses_south_pole (t : ℚ) : cayley t ≠ (-1, 0) := by
  intro h
  exact cayley_re_ne_neg_one t (congrArg Prod.fst h)

/-- Stereographic inverse map from the punctured circle $S^1(\mathbb{Q}) \setminus \{(-1, 0)\}$ to $\mathbb{Q}$. -/
def inverseCayley (p : ℚ × ℚ) : ℚ :=
  p.2 / (p.1 + 1)

/-- `inverseCayley` is a left inverse to `cayley` on all of `ℚ`. -/
theorem inverseCayley_cayley (t : ℚ) : inverseCayley (cayley t) = t := by
  have hne : 1 + t * t ≠ 0 := cayleyDenom_ne_zero t
  unfold inverseCayley
  rw [cayley_re_add_one]
  change (2 * t / (1 + t * t)) / (2 / (1 + t * t)) = t
  field_simp [hne]

/-- `inverseCayley` is a right inverse to `cayley` on the punctured rational unit circle. -/
theorem cayley_inverseCayley (x y : ℚ) (hunit : x * x + y * y = 1) (hne : x ≠ -1) :
    cayley (inverseCayley (x, y)) = (x, y) := by
  have hx1 : x + 1 ≠ 0 := by
    intro h
    apply hne
    linarith
  have hdenom : 1 + y / (x + 1) * (y / (x + 1)) ≠ 0 :=
    cayleyDenom_ne_zero (y / (x + 1))
  have hy : y ^ 2 = 1 - x * x := by
    calc
      y ^ 2 = y * y := by ring
      _ = 1 - x * x := by linarith [hunit]
  unfold cayley inverseCayley
  ext
  · dsimp
    rw [div_eq_iff hdenom]
    field_simp [hx1]
    rw [hy]
    ring
  · dsimp
    rw [div_eq_iff hdenom]
    field_simp [hx1]
    rw [hy]
    ring

/-! ## Section 2: Affine Cayley Tangent Group Law & Pole Singularity -/

/-- Exact rational group multiplication on $S^1(\mathbb{Q})$ induced by Gaussian multiplication
    $(x_1 + i y_1)(x_2 + i y_2) = (x_1 x_2 - y_1 y_2) + i(x_1 y_2 + y_1 x_2)$. -/
def circleMul (p q : ℚ × ℚ) : ℚ × ℚ :=
  (p.1 * q.1 - p.2 * q.2, p.1 * q.2 + p.2 * q.1)

/-- Regular affine Cayley group law: away from the pole locus `1 - t₁ * t₂ = 0`,
    multiplication on the circle corresponds to the tangent addition law `(t₁ + t₂) / (1 - t₁ * t₂)`. -/
theorem cayley_mul_regular (t₁ t₂ : ℚ) (h : 1 - t₁ * t₂ ≠ 0) :
    circleMul (cayley t₁) (cayley t₂) = cayley ((t₁ + t₂) / (1 - t₁ * t₂)) := by
  have h1 : 1 + t₁ * t₁ ≠ 0 := cayleyDenom_ne_zero t₁
  have h2 : 1 + t₂ * t₂ ≠ 0 := cayleyDenom_ne_zero t₂
  have h3 : 1 + (t₁ + t₂) / (1 - t₁ * t₂) * ((t₁ + t₂) / (1 - t₁ * t₂)) ≠ 0 :=
    cayleyDenom_ne_zero ((t₁ + t₂) / (1 - t₁ * t₂))
  unfold circleMul cayley
  ext <;> dsimp <;> field_simp [h, h1, h2, h3] <;> ring

/-- Pole collision theorem: whenever `t₁ * t₂ = 1` (e.g. `t₁ = t₂ = 1`), the product of two
    affine Cayley points escapes the affine chart and lands at the punctured south pole `(-1, 0)`. -/
theorem cayley_mul_pole_collision (t₁ t₂ : ℚ) (h : t₁ * t₂ = 1) :
    circleMul (cayley t₁) (cayley t₂) = (-1, 0) := by
  have hprod : (1 + t₁ * t₁) * (1 + t₂ * t₂) ≠ 0 :=
    mul_ne_zero (cayleyDenom_ne_zero t₁) (cayleyDenom_ne_zero t₂)
  have h_re : (1 - t₁ * t₁) * (1 - t₂ * t₂) - 2 * t₁ * (2 * t₂) =
      -1 * ((1 + t₁ * t₁) * (1 + t₂ * t₂)) := by
    calc
      (1 - t₁ * t₁) * (1 - t₂ * t₂) - 2 * t₁ * (2 * t₂)
        = -1 * ((1 + t₁ * t₁) * (1 + t₂ * t₂)) + 2 * (t₁ * t₂ - 1) ^ 2 := by ring
      _ = -1 * ((1 + t₁ * t₁) * (1 + t₂ * t₂)) + 2 * (1 - 1) ^ 2 := by rw [h]
      _ = -1 * ((1 + t₁ * t₁) * (1 + t₂ * t₂)) := by ring
  have h_im : (1 - t₁ * t₁) * (2 * t₂) + 2 * t₁ * (1 - t₂ * t₂) = 0 := by
    calc
      (1 - t₁ * t₁) * (2 * t₂) + 2 * t₁ * (1 - t₂ * t₂)
        = 2 * (t₁ + t₂) * (1 - t₁ * t₂) := by ring
      _ = 2 * (t₁ + t₂) * (1 - 1) := by rw [h]
      _ = 0 := by ring
  unfold circleMul cayley
  ext
  · dsimp
    rw [div_mul_div_comm, div_mul_div_comm, ← sub_div, h_re, mul_div_cancel_right₀ (-1) hprod]
  · dsimp
    rw [div_mul_div_comm, div_mul_div_comm, ← add_div, h_im, zero_div]

/-! ## Section 3: Homogeneous Projective Line $\mathbb{P}^1(\mathbb{Q})$ Completion -/

/-- Non-zero homogeneous coordinate pairs `(u, v)` representing points `[u : v]` on the
    rational projective line $\mathbb{P}^1(\mathbb{Q})$. -/
structure ProjRatLine where
  u : ℚ
  v : ℚ
  not_both_zero : u ≠ 0 ∨ v ≠ 0

/-- By elliptic anisotropy over `ℚ`, the homogeneous denominator `p.u * p.u + p.v * p.v`
    is never zero for any `p : ProjRatLine`. -/
theorem projDenom_ne_zero (p : ProjRatLine) : p.u * p.u + p.v * p.v ≠ 0 := by
  intro h
  have ⟨hu, hv⟩ := elliptic_norm_anisotropic p.u p.v h
  rcases p.not_both_zero with hne | hne
  · exact hne hu
  · exact hne hv

/-- The homogeneous denominator `p.u * p.u + p.v * p.v` is strictly positive for any `p : ProjRatLine`. -/
theorem projDenom_pos (p : ProjRatLine) : 0 < p.u * p.u + p.v * p.v := by
  have hnonneg : 0 ≤ p.u * p.u + p.v * p.v :=
    add_nonneg (mul_self_nonneg p.u) (mul_self_nonneg p.v)
  exact lt_of_le_of_ne hnonneg (Ne.symm (projDenom_ne_zero p))

/-- The homogeneous Cayley parameterization $\mathbb{P}^1(\mathbb{Q}) \to S^1(\mathbb{Q})$. -/
def homCayley (p : ProjRatLine) : ℚ × ℚ :=
  ((p.u * p.u - p.v * p.v) / (p.u * p.u + p.v * p.v),
   (2 * p.u * p.v) / (p.u * p.u + p.v * p.v))

/-- Every point in the image of `homCayley` lies on the unit circle $x^2 + y^2 = 1$. -/
theorem homCayley_unit_norm (p : ProjRatLine) :
    (homCayley p).1 ^ 2 + (homCayley p).2 ^ 2 = 1 := by
  have hne : (p.u * p.u + p.v * p.v) ^ 2 ≠ 0 := pow_ne_zero 2 (projDenom_ne_zero p)
  unfold homCayley
  dsimp
  rw [div_pow, div_pow, ← add_div, div_eq_iff hne]
  ring

/-- Canonical affine chart embedding $t \mapsto [1 : t]$ into $\mathbb{P}^1(\mathbb{Q})$. -/
def ofAffine (t : ℚ) : ProjRatLine :=
  ⟨1, t, Or.inl one_ne_zero⟩

/-- The projective point at infinity $[0 : 1] \in \mathbb{P}^1(\mathbb{Q})$ that closes the south-pole puncture. -/
def infinityPt : ProjRatLine :=
  ⟨0, 1, Or.inr one_ne_zero⟩

/-- On the affine chart `[1 : t]`, `homCayley` agrees with the affine `cayley` parameterization. -/
theorem homCayley_ofAffine (t : ℚ) : homCayley (ofAffine t) = cayley t := by
  unfold homCayley ofAffine cayley
  ext <;> dsimp <;> ring

/-- The point at infinity `[0 : 1]` maps directly to the south pole `(-1, 0)`, closing the puncture. -/
theorem homCayley_infinity : homCayley infinityPt = (-1, 0) := by
  unfold homCayley infinityPt
  ext <;> dsimp <;> norm_num

/-- Non-zero scaling preserves the non-vanishing condition of homogeneous coordinates. -/
theorem scale_not_both_zero (k : ℚ) (hk : k ≠ 0) (p : ProjRatLine) :
    k * p.u ≠ 0 ∨ k * p.v ≠ 0 := by
  rcases p.not_both_zero with hu | hv
  · exact Or.inl (mul_ne_zero hk hu)
  · exact Or.inr (mul_ne_zero hk hv)

/-- Rescaling a projective representative by a non-zero rational scalar `k ≠ 0`. -/
def scaleProj (k : ℚ) (hk : k ≠ 0) (p : ProjRatLine) : ProjRatLine :=
  ⟨k * p.u, k * p.v, scale_not_both_zero k hk p⟩

/-- Projective scale invariance: `homCayley` is invariant under rescaling `(u, v) mapsto (k * u, k * v)`
    for any `k ≠ 0`, hence descends to a well-defined map on $\mathbb{P}^1(\mathbb{Q})$. -/
theorem homCayley_scale (k : ℚ) (hk : k ≠ 0) (p : ProjRatLine)
    (h : k * p.u ≠ 0 ∨ k * p.v ≠ 0 := scale_not_both_zero k hk p) :
    homCayley ⟨k * p.u, k * p.v, h⟩ = homCayley p := by
  have hp : p.u * p.u + p.v * p.v ≠ 0 := projDenom_ne_zero p
  have hkp : k * p.u * (k * p.u) + k * p.v * (k * p.v) ≠ 0 :=
    projDenom_ne_zero ⟨k * p.u, k * p.v, h⟩
  unfold homCayley
  ext <;> dsimp <;> field_simp [hp, hkp]

/-- Surjectivity of `homCayley` onto the entire rational circle $S^1(\mathbb{Q})$:
    every rational point `(x, y)` with `x * x + y * y = 1` is in the image of `homCayley`
    (with `(-1, 0)` hit by `infinityPt` and all other points hit by `ofAffine (inverseCayley (x, y))`). -/
theorem homCayley_surjective (x y : ℚ) (hunit : x * x + y * y = 1) :
    ∃ p : ProjRatLine, homCayley p = (x, y) := by
  by_cases h : x = -1
  · refine ⟨infinityPt, ?_⟩
    rw [homCayley_infinity]
    have hy0 : y * y = 0 := by
      have h1 : (-1) * (-1) + y * y = 1 := by rw [← h]; exact hunit
      linarith
    have hy : y = 0 := mul_self_eq_zero.mp hy0
    exact Prod.ext h.symm hy.symm
  · refine ⟨ofAffine (inverseCayley (x, y)), ?_⟩
    rw [homCayley_ofAffine]
    exact cayley_inverseCayley x y hunit h

/-- Brahmagupta-Fibonacci two-square identity: the elliptic norm is multiplicative under
    Gaussian coordinate multiplication. -/
theorem brahmagupta_fibonacci (u₁ v₁ u₂ v₂ : ℚ) :
    (u₁ * u₂ - v₁ * v₂) * (u₁ * u₂ - v₁ * v₂) + (u₁ * v₂ + v₁ * u₂) * (u₁ * v₂ + v₁ * u₂) =
      (u₁ * u₁ + v₁ * v₁) * (u₂ * u₂ + v₂ * v₂) := by
  ring

/-- The homogeneous product of two non-zero pairs is non-zero, guaranteed by
    Brahmagupta-Fibonacci norm multiplicativity and elliptic anisotropy. -/
theorem projMul_not_both_zero (p q : ProjRatLine) :
    p.u * q.u - p.v * q.v ≠ 0 ∨ p.u * q.v + p.v * q.u ≠ 0 := by
  by_cases h1 : p.u * q.u - p.v * q.v = 0
  · right
    intro h2
    have hpos : 0 < (p.u * p.u + p.v * p.v) * (q.u * q.u + q.v * q.v) :=
      mul_pos (projDenom_pos p) (projDenom_pos q)
    have hbf := brahmagupta_fibonacci p.u p.v q.u q.v
    rw [h1, h2] at hbf
    linarith
  · exact Or.inl h1

/-- Globally defined homogeneous group multiplication on `ProjRatLine` without pole exceptions. -/
def projMul (p q : ProjRatLine) : ProjRatLine :=
  ⟨p.u * q.u - p.v * q.v, p.u * q.v + p.v * q.u, projMul_not_both_zero p q⟩

/-- Global homomorphism theorem: `homCayley` intertwines homogeneous multiplication `projMul`
    with `circleMul` for all `p, q : ProjRatLine`, with zero pole exceptions. -/
theorem homCayley_projMul (p q : ProjRatLine) :
    homCayley (projMul p q) = circleMul (homCayley p) (homCayley q) := by
  have hp : p.u * p.u + p.v * p.v ≠ 0 := projDenom_ne_zero p
  have hq : q.u * q.u + q.v * q.v ≠ 0 := projDenom_ne_zero q
  have hpq : (projMul p q).u * (projMul p q).u + (projMul p q).v * (projMul p q).v ≠ 0 :=
    projDenom_ne_zero (projMul p q)
  unfold homCayley projMul circleMul
  dsimp at hpq ⊢
  ext <;> dsimp <;> field_simp [hp, hq, hpq] <;> ring

end U1Finite.CayleyProjective

#print axioms U1Finite.CayleyProjective.elliptic_norm_anisotropic
#print axioms U1Finite.CayleyProjective.hyperbolic_split_zero_divisor
#print axioms U1Finite.CayleyProjective.cayleyDenom_pos
#print axioms U1Finite.CayleyProjective.cayleyDenom_ne_zero
#print axioms U1Finite.CayleyProjective.cayley
#print axioms U1Finite.CayleyProjective.cayley_cleared_identity
#print axioms U1Finite.CayleyProjective.cayley_unit_norm
#print axioms U1Finite.CayleyProjective.cayley_re_add_one
#print axioms U1Finite.CayleyProjective.cayley_re_ne_neg_one
#print axioms U1Finite.CayleyProjective.cayley_misses_south_pole
#print axioms U1Finite.CayleyProjective.inverseCayley
#print axioms U1Finite.CayleyProjective.inverseCayley_cayley
#print axioms U1Finite.CayleyProjective.cayley_inverseCayley
#print axioms U1Finite.CayleyProjective.circleMul
#print axioms U1Finite.CayleyProjective.cayley_mul_regular
#print axioms U1Finite.CayleyProjective.cayley_mul_pole_collision
#print axioms U1Finite.CayleyProjective.ProjRatLine
#print axioms U1Finite.CayleyProjective.projDenom_ne_zero
#print axioms U1Finite.CayleyProjective.projDenom_pos
#print axioms U1Finite.CayleyProjective.homCayley
#print axioms U1Finite.CayleyProjective.homCayley_unit_norm
#print axioms U1Finite.CayleyProjective.ofAffine
#print axioms U1Finite.CayleyProjective.infinityPt
#print axioms U1Finite.CayleyProjective.homCayley_ofAffine
#print axioms U1Finite.CayleyProjective.homCayley_infinity
#print axioms U1Finite.CayleyProjective.scale_not_both_zero
#print axioms U1Finite.CayleyProjective.scaleProj
#print axioms U1Finite.CayleyProjective.homCayley_scale
#print axioms U1Finite.CayleyProjective.homCayley_surjective
#print axioms U1Finite.CayleyProjective.brahmagupta_fibonacci
#print axioms U1Finite.CayleyProjective.projMul_not_both_zero
#print axioms U1Finite.CayleyProjective.projMul
#print axioms U1Finite.CayleyProjective.homCayley_projMul
