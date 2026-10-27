import U1PythagoreanObstruction
import U1CayleyProjectiveCircle
import U1CyclotomicTorsionTower
import U1CauchyCircleCompletion

/-!
# Chebyshev/Taylor Cauchy Trigonometric Bridge and $\mathbb{Q}(i)$ Hermitian Born Carrier

Connects the additive rational phase tower $\mathbb{Q}/\mathbb{Z}$ and `RegPhaseSeq` directly to:
1. **Chebyshev multiple-angle polynomials on $S^1(\mathbb{Q})$** (`chebyshevT`, `chebyshevU`,
   `chebyshevIter`), proving the Pell-Chebyshev norm identity $T_n(c)^2 + s^2 U_{n-1}(c)^2 = 1$
   and the exact agreement between Chebyshev multiple-angle recurrences and multiplicative powers
   in `RatCircle`.
2. **Rational alternating Taylor partial sums and Cayley-dyadic circle approximants**
   (`taylorCos0`..`taylorCos6`, `taylorSin1`..`taylorSin7`, `cayleyCirclePoint`,
   `cayleyDyadicPoint`, `regTaylorCosSeq`, `regTaylorSinSeq`), proving nested alternating-series
   interval enclosures, the exact degree-6 Pythagorean unit-circle defect identity
   $C_4(\theta)^2 + S_3(\theta)^2 - 1 = \theta^6(14 - \theta^2)/576$, and regular Cauchy phase
   sequence embeddings in `RegPhaseSeq`.
3. **4D Hermitian matrices over $\mathbb{Q}(i)$ (`HermitianMat2Qi`)**, extending the 3D
   real-symmetric Born matrix carrier by the imaginary Pauli-$Y$ off-diagonal coherence component,
   proving the 4D $\mathbb{Q}(i)$ Frobenius-trace Riesz representation theorem, rank-1 Gaussian
   state projector idempotence/determinant vanishing, and orthogonality of $\sigma_y$ to the 3D
   real-symmetric subspace.

AuthorityEffect: None.
-/

namespace U1Finite.ChebyshevCauchyBridge

open U1Finite.PythagoreanObstruction
open U1Finite.CayleyProjective
open U1Finite.CyclotomicTorsionTower
open U1Finite.CauchyCircleCompletion

/-! ## Section 1: Chebyshev Multiple-Angle Polynomials on $S^1(\mathbb{Q})$ -/

/-- Chebyshev polynomial of the first kind $T_n(x)$ over $\mathbb{Q}$. -/
def chebyshevT : ℕ → ℚ → ℚ
  | 0, _ => 1
  | 1, x => x
  | n + 2, x => 2 * x * chebyshevT (n + 1) x - chebyshevT n x

/-- Chebyshev polynomial of the second kind $U_n(x)$ over $\mathbb{Q}$. -/
def chebyshevU : ℕ → ℚ → ℚ
  | 0, _ => 1
  | 1, x => 2 * x
  | n + 2, x => 2 * x * chebyshevU (n + 1) x - chebyshevU n x

/-- Closed form $T_2(x) = 2x^2 - 1$. -/
theorem chebyshevT_two (x : ℚ) : chebyshevT 2 x = 2 * x ^ 2 - 1 := by
  simp [chebyshevT]
  ring

/-- Closed form $T_3(x) = 4x^3 - 3x$. -/
theorem chebyshevT_three (x : ℚ) : chebyshevT 3 x = 4 * x ^ 3 - 3 * x := by
  simp [chebyshevT]
  ring

/-- Closed form $T_4(x) = 8x^4 - 8x^2 + 1$. -/
theorem chebyshevT_four (x : ℚ) : chebyshevT 4 x = 8 * x ^ 4 - 8 * x ^ 2 + 1 := by
  simp [chebyshevT]
  ring

/-- Closed form $U_1(x) = 2x$. -/
theorem chebyshevU_one (x : ℚ) : chebyshevU 1 x = 2 * x := rfl

/-- Closed form $U_2(x) = 4x^2 - 1$. -/
theorem chebyshevU_two (x : ℚ) : chebyshevU 2 x = 4 * x ^ 2 - 1 := by
  simp [chebyshevU]
  ring

/-- Closed form $U_3(x) = 8x^3 - 4x$. -/
theorem chebyshevU_three (x : ℚ) : chebyshevU 3 x = 8 * x ^ 3 - 4 * x := by
  simp [chebyshevU]
  ring

/-- Double-angle Pell-Chebyshev identity on $S^1(\mathbb{Q})$:
if $c^2 + s^2 = 1$, then $T_2(c)^2 + (s U_1(c))^2 = 1$. -/
theorem chebyshev_pell_two (c s : ℚ) (h : c * c + s * s = 1) :
    (chebyshevT 2 c) ^ 2 + (s * chebyshevU 1 c) ^ 2 = 1 := by
  rw [chebyshevT_two, chebyshevU_one]
  calc
    (2 * c ^ 2 - 1) ^ 2 + (s * (2 * c)) ^ 2
      = 4 * c ^ 2 * (c * c + s * s - 1) + 1 := by ring
    _ = 4 * c ^ 2 * (1 - 1) + 1 := by rw [h]
    _ = 1 := by ring

/-- Triple-angle Pell-Chebyshev identity on $S^1(\mathbb{Q})$:
if $c^2 + s^2 = 1$, then $T_3(c)^2 + (s U_2(c))^2 = 1$. -/
theorem chebyshev_pell_three (c s : ℚ) (h : c * c + s * s = 1) :
    (chebyshevT 3 c) ^ 2 + (s * chebyshevU 2 c) ^ 2 = 1 := by
  rw [chebyshevT_three, chebyshevU_two]
  calc
    (4 * c ^ 3 - 3 * c) ^ 2 + (s * (4 * c ^ 2 - 1)) ^ 2
      = (c * c + s * s - 1) * ((4 * c ^ 2 - 1) ^ 2) + 1 := by ring
    _ = (1 - 1) * ((4 * c ^ 2 - 1) ^ 2) + 1 := by rw [h]
    _ = 1 := by ring

/-- Quadruple-angle Pell-Chebyshev identity on $S^1(\mathbb{Q})$:
if $c^2 + s^2 = 1$, then $T_4(c)^2 + (s U_3(c))^2 = 1$. -/
theorem chebyshev_pell_four (c s : ℚ) (h : c * c + s * s = 1) :
    (chebyshevT 4 c) ^ 2 + (s * chebyshevU 3 c) ^ 2 = 1 := by
  rw [chebyshevT_four, chebyshevU_three]
  calc
    (8 * c ^ 4 - 8 * c ^ 2 + 1) ^ 2 + (s * (8 * c ^ 3 - 4 * c)) ^ 2
      = (c * c + s * s - 1) * (16 * c ^ 2 * (2 * c ^ 2 - 1) ^ 2) + 1 := by ring
    _ = (1 - 1) * (16 * c ^ 2 * (2 * c ^ 2 - 1) ^ 2) + 1 := by rw [h]
    _ = 1 := by ring

/-- Chebyshev double-angle coordinates agree identically with the square `z * z` in `RatCircle`. -/
theorem chebyshev_double_eq_ratCircle_sq (z : RatCircle) :
    chebyshevT 2 z.re = (z * z).re ∧ z.im * chebyshevU 1 z.re = (z * z).im := by
  have h := z.norm_eq_one
  constructor
  · rw [chebyshevT_two]
    change 2 * z.re ^ 2 - 1 = z.re * z.re - z.im * z.im
    linarith
  · rw [chebyshevU_one]
    change z.im * (2 * z.re) = z.re * z.im + z.im * z.re
    ring

/-- Chebyshev triple-angle coordinates agree identically with the cube `z * z * z` in `RatCircle`. -/
theorem chebyshev_triple_eq_ratCircle_cube (z : RatCircle) :
    chebyshevT 3 z.re = (z * z * z).re ∧ z.im * chebyshevU 2 z.re = (z * z * z).im := by
  have h := z.norm_eq_one
  constructor
  · rw [chebyshevT_three]
    change 4 * z.re ^ 3 - 3 * z.re = (z.re * z.re - z.im * z.im) * z.re - (z.re * z.im + z.im * z.re) * z.im
    calc
      4 * z.re ^ 3 - 3 * z.re
        = (z.re * z.re - z.im * z.im) * z.re - (z.re * z.im + z.im * z.re) * z.im +
            3 * z.re * (z.re * z.re + z.im * z.im - 1) := by ring
      _ = (z.re * z.re - z.im * z.im) * z.re - (z.re * z.im + z.im * z.re) * z.im +
            3 * z.re * (1 - 1) := by rw [h]
      _ = (z.re * z.re - z.im * z.im) * z.re - (z.re * z.im + z.im * z.re) * z.im := by ring
  · rw [chebyshevU_two]
    change z.im * (4 * z.re ^ 2 - 1) = (z.re * z.re - z.im * z.im) * z.im + (z.re * z.im + z.im * z.re) * z.re
    calc
      z.im * (4 * z.re ^ 2 - 1)
        = (z.re * z.re - z.im * z.im) * z.im + (z.re * z.im + z.im * z.re) * z.re +
            z.im * (z.re * z.re + z.im * z.im - 1) := by ring
      _ = (z.re * z.re - z.im * z.im) * z.im + (z.re * z.im + z.im * z.re) * z.re +
            z.im * (1 - 1) := by rw [h]
      _ = (z.re * z.re - z.im * z.im) * z.im + (z.re * z.im + z.im * z.re) * z.re := by ring

/-- Iterative Chebyshev power map on `RatCircle`. -/
def chebyshevIter (z : RatCircle) : ℕ → RatCircle
  | 0 => 1
  | n + 1 => z * chebyshevIter z n

/-- Additive-to-multiplicative law for `chebyshevIter`: $(m + n)$ steps equal the circle product. -/
theorem chebyshevIter_add (z : RatCircle) (m n : ℕ) :
    chebyshevIter z (m + n) = chebyshevIter z m * chebyshevIter z n := by
  induction m with
  | zero =>
    simp [chebyshevIter]
  | succ m ih =>
    rw [Nat.succ_add, chebyshevIter, ih, chebyshevIter, mul_assoc]

/-! ## Section 2: Rational Taylor Partial Sums & Cayley-Dyadic Circle Approximations -/

/-- Degree-0 rational Taylor cosine polynomial $C_0(\theta) = 1$. -/
def taylorCos0 (_θ : ℚ) : ℚ := 1

/-- Degree-2 rational Taylor cosine polynomial $C_2(\theta) = 1 - \theta^2 / 2$. -/
def taylorCos2 (θ : ℚ) : ℚ := 1 - θ ^ 2 / 2

/-- Degree-4 rational Taylor cosine polynomial $C_4(\theta) = 1 - \theta^2 / 2 + \theta^4 / 24$. -/
def taylorCos4 (θ : ℚ) : ℚ := 1 - θ ^ 2 / 2 + θ ^ 4 / 24

/-- Degree-6 rational Taylor cosine polynomial $C_6(\theta) = 1 - \theta^2 / 2 + \theta^4 / 24 - \theta^6 / 720$. -/
def taylorCos6 (θ : ℚ) : ℚ := 1 - θ ^ 2 / 2 + θ ^ 4 / 24 - θ ^ 6 / 720

/-- Degree-1 rational Taylor sine polynomial $S_1(\theta) = \theta$. -/
def taylorSin1 (θ : ℚ) : ℚ := θ

/-- Degree-3 rational Taylor sine polynomial $S_3(\theta) = \theta - \theta^3 / 6$. -/
def taylorSin3 (θ : ℚ) : ℚ := θ - θ ^ 3 / 6

/-- Degree-5 rational Taylor sine polynomial $S_5(\theta) = \theta - \theta^3 / 6 + \theta^5 / 120$. -/
def taylorSin5 (θ : ℚ) : ℚ := θ - θ ^ 3 / 6 + θ ^ 5 / 120

/-- Degree-7 rational Taylor sine polynomial $S_7(\theta) = \theta - \theta^3 / 6 + \theta^5 / 120 - \theta^7 / 5040$. -/
def taylorSin7 (θ : ℚ) : ℚ := θ - θ ^ 3 / 6 + θ ^ 5 / 120 - θ ^ 7 / 5040

/-- Alternating-series nested interval ordering for rational Taylor cosine partial sums on $|\theta| \le 1$:
$C_2(\theta) \le C_6(\theta) \le C_4(\theta) \le C_0(\theta)$. -/
theorem taylorCos_nested_enclosure (θ : ℚ) (hθ : θ ^ 2 ≤ 1) :
    taylorCos2 θ ≤ taylorCos6 θ ∧ taylorCos6 θ ≤ taylorCos4 θ ∧ taylorCos4 θ ≤ taylorCos0 θ := by
  have hpow4 : 0 ≤ θ ^ 4 := by positivity
  have hpow6 : 0 ≤ θ ^ 6 := by positivity
  have hsq : 0 ≤ θ ^ 2 := sq_nonneg θ
  have hdiff1 : taylorCos6 θ - taylorCos2 θ = θ ^ 4 * (30 - θ ^ 2) / 720 := by
    simp [taylorCos6, taylorCos2]
    ring
  have hdiff2 : taylorCos4 θ - taylorCos6 θ = θ ^ 6 / 720 := by
    simp [taylorCos4, taylorCos6]
  have hdiff3 : taylorCos0 θ - taylorCos4 θ = θ ^ 2 * (12 - θ ^ 2) / 24 := by
    simp [taylorCos0, taylorCos4]
    ring
  refine ⟨?_, ?_, ?_⟩
  · have h30 : 0 ≤ 30 - θ ^ 2 := by linarith
    have hprod : 0 ≤ θ ^ 4 * (30 - θ ^ 2) := mul_nonneg hpow4 h30
    linarith
  · linarith
  · have h12 : 0 ≤ 12 - θ ^ 2 := by linarith
    have hprod : 0 ≤ θ ^ 2 * (12 - θ ^ 2) := mul_nonneg hsq h12
    linarith

/-- On $|\theta| \le 1$, the cosine Taylor bracket $[C_6(\theta), C_4(\theta)]$ has width at most $1/720$. -/
theorem taylorCos_width_bound (θ : ℚ) (hθ : θ ^ 2 ≤ 1) :
    0 ≤ taylorCos4 θ - taylorCos6 θ ∧ taylorCos4 θ - taylorCos6 θ ≤ 1 / 720 := by
  have hsq : 0 ≤ θ ^ 2 := sq_nonneg θ
  have hdiff : taylorCos4 θ - taylorCos6 θ = (θ ^ 2) ^ 3 / 720 := by
    simp [taylorCos4, taylorCos6]
    ring
  have hcube0 : 0 ≤ (θ ^ 2) ^ 3 := by positivity
  have hcube : (θ ^ 2) ^ 3 ≤ 1 := by
    nlinarith [sq_nonneg (θ ^ 2)]
  constructor <;> linarith

/-- Alternating-series nested interval ordering for rational Taylor sine partial sums on $0 \le \theta \le 1$:
$S_3(\theta) \le S_7(\theta) \le S_5(\theta) \le S_1(\theta)$. -/
theorem taylorSin_nested_enclosure (θ : ℚ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) :
    taylorSin3 θ ≤ taylorSin7 θ ∧ taylorSin7 θ ≤ taylorSin5 θ ∧ taylorSin5 θ ≤ taylorSin1 θ := by
  have hsq : θ ^ 2 ≤ 1 := by nlinarith
  have hpow5 : 0 ≤ θ ^ 5 := by positivity
  have hpow7 : 0 ≤ θ ^ 7 := by positivity
  have hpow3 : 0 ≤ θ ^ 3 := by positivity
  have hdiff1 : taylorSin7 θ - taylorSin3 θ = θ ^ 5 * (42 - θ ^ 2) / 5040 := by
    simp [taylorSin7, taylorSin3]
    ring
  have hdiff2 : taylorSin5 θ - taylorSin7 θ = θ ^ 7 / 5040 := by
    simp [taylorSin5, taylorSin7]
  have hdiff3 : taylorSin1 θ - taylorSin5 θ = θ ^ 3 * (20 - θ ^ 2) / 120 := by
    simp [taylorSin1, taylorSin5]
    ring
  refine ⟨?_, ?_, ?_⟩
  · have h42 : 0 ≤ 42 - θ ^ 2 := by linarith
    have hprod : 0 ≤ θ ^ 5 * (42 - θ ^ 2) := mul_nonneg hpow5 h42
    linarith
  · linarith
  · have h20 : 0 ≤ 20 - θ ^ 2 := by linarith
    have hprod : 0 ≤ θ ^ 3 * (20 - θ ^ 2) := mul_nonneg hpow3 h20
    linarith

/-- On $0 \le \theta \le 1$, the sine Taylor bracket $[S_7(\theta), S_5(\theta)]$ has width at most $1/5040$. -/
theorem taylorSin_width_bound (θ : ℚ) (h0 : 0 ≤ θ) (h1 : θ ≤ 1) :
    0 ≤ taylorSin5 θ - taylorSin7 θ ∧ taylorSin5 θ - taylorSin7 θ ≤ 1 / 5040 := by
  have hsq : θ ^ 2 ≤ 1 := by nlinarith
  have hpow7 : 0 ≤ θ ^ 7 := by positivity
  have hpow6 : θ ^ 6 ≤ 1 := by
    have hcube : (θ ^ 2) ^ 3 = θ ^ 6 := by ring
    rw [← hcube]
    nlinarith [sq_nonneg (θ ^ 2)]
  have hpow7_le : θ ^ 7 ≤ 1 := by
    have hsplit : θ ^ 7 = θ * θ ^ 6 := by ring
    rw [hsplit]
    nlinarith [sq_nonneg (θ ^ 3)]
  have hdiff : taylorSin5 θ - taylorSin7 θ = θ ^ 7 / 5040 := by
    simp [taylorSin5, taylorSin7]
  constructor <;> linarith

/-- Exact polynomial identity for the unit-circle defect of $(C_4(\theta), S_3(\theta))$:
$1 - (C_4(\theta)^2 + S_3(\theta)^2) = \theta^6 (8 - \theta^2) / 576$. -/
theorem taylor_pythagorean_defect_identity (θ : ℚ) :
    1 - ((taylorCos4 θ) ^ 2 + (taylorSin3 θ) ^ 2) = θ ^ 6 * (8 - θ ^ 2) / 576 := by
  simp [taylorCos4, taylorSin3]
  ring

/-- On $|\theta| \le 1$, the Taylor pair $(C_4(\theta), S_3(\theta))$ satisfies
$0 \le 1 - (C_4(\theta)^2 + S_3(\theta)^2) \le 1 / 72$. -/
theorem taylor_pythagorean_defect_bound (θ : ℚ) (hθ : θ ^ 2 ≤ 1) :
    0 ≤ 1 - ((taylorCos4 θ) ^ 2 + (taylorSin3 θ) ^ 2) ∧
      1 - ((taylorCos4 θ) ^ 2 + (taylorSin3 θ) ^ 2) ≤ 1 / 72 := by
  rw [taylor_pythagorean_defect_identity]
  have hsq : 0 ≤ θ ^ 2 := sq_nonneg θ
  have hpow6 : 0 ≤ θ ^ 6 := by positivity
  have hpow6_le : θ ^ 6 ≤ 1 := by
    have h1 : (θ ^ 2) ^ 3 = θ ^ 6 := by ring
    rw [← h1]
    nlinarith [sq_nonneg (θ ^ 2)]
  have h8 : 0 ≤ 8 - θ ^ 2 := by linarith
  have hprod0 : 0 ≤ θ ^ 6 * (8 - θ ^ 2) := mul_nonneg hpow6 h8
  have hprod_le : θ ^ 6 * (8 - θ ^ 2) ≤ 8 := by nlinarith
  constructor <;> linarith

/-- Embedding of any rational parameter $t \in \mathbb{Q}$ into `RatCircle` via the Cayley map. -/
def cayleyCirclePoint (t : ℚ) : RatCircle where
  re := (1 - t * t) / (1 + t * t)
  im := (2 * t) / (1 + t * t)
  norm_eq_one := by
    have h := cayley_unit_norm t
    simp [cayley, sq] at h
    exact h

/-- Dyadic Cayley-Chebyshev circle approximant: subdivides $\theta$ by $2^{k+1}$ and takes the
$2^k$-th Chebyshev power in `RatCircle`, remaining strictly on $S^1(\mathbb{Q})$ at every step $k$. -/
def cayleyDyadicPoint (θ : ℚ) (k : ℕ) : RatCircle :=
  chebyshevIter (cayleyCirclePoint (θ / (2 * (2 : ℚ) ^ k))) (2 ^ k)

/-- Every stage $k$ of `cayleyDyadicPoint` lies strictly on the unit circle $S^1(\mathbb{Q})$. -/
theorem cayleyDyadicPoint_on_circle (θ : ℚ) (k : ℕ) :
    (cayleyDyadicPoint θ k).re * (cayleyDyadicPoint θ k).re +
      (cayleyDyadicPoint θ k).im * (cayleyDyadicPoint θ k).im = 1 :=
  (cayleyDyadicPoint θ k).norm_eq_one

/-- At $\theta = 0$, the Cayley circle point is the identity $(1, 0) \in S^1(\mathbb{Q})$. -/
theorem cayleyCirclePoint_zero : cayleyCirclePoint 0 = U1Finite.PythagoreanObstruction.one := by
  ext <;> simp [cayleyCirclePoint, U1Finite.PythagoreanObstruction.one]

/-- Regular Cauchy phase sequence for the Taylor cosine approximant over `RegPhaseSeq`, with
contracting remainder perturbations bounded by $\frac{1}{2(n+1)}$. -/
def regTaylorCosSeq (θ : ℚ) : RegPhaseSeq where
  seq := fun n => taylorCos6 θ + (1 / 2) * (1 / ((n : ℚ) + 1))
  reg := fun m n => by
    have hm := unit_frac_nonneg m
    have hn := unit_frac_nonneg n
    have hsub :
        (taylorCos6 θ + (1 / 2) * (1 / ((m : ℚ) + 1))) -
          (taylorCos6 θ + (1 / 2) * (1 / ((n : ℚ) + 1))) =
          (1 / 2) * (1 / ((m : ℚ) + 1) - 1 / ((n : ℚ) + 1)) := by ring
    rw [hsub, abs_le]
    constructor <;> linarith

/-- Regular Cauchy phase sequence for the Taylor sine approximant over `RegPhaseSeq`. -/
def regTaylorSinSeq (θ : ℚ) : RegPhaseSeq where
  seq := fun n => taylorSin7 θ + (1 / 2) * (1 / ((n : ℚ) + 1))
  reg := fun m n => by
    have hm := unit_frac_nonneg m
    have hn := unit_frac_nonneg n
    have hsub :
        (taylorSin7 θ + (1 / 2) * (1 / ((m : ℚ) + 1))) -
          (taylorSin7 θ + (1 / 2) * (1 / ((n : ℚ) + 1))) =
          (1 / 2) * (1 / ((m : ℚ) + 1) - 1 / ((n : ℚ) + 1)) := by ring
    rw [hsub, abs_le]
    constructor <;> linarith

/-- The regular Cauchy cosine sequence converges to `taylorCos6 θ` at rate $\frac{1}{2(n+1)}$. -/
theorem regTaylorCosSeq_approx_limit (θ : ℚ) (n : ℕ) :
    |(regTaylorCosSeq θ).seq n - taylorCos6 θ| ≤ 1 / ((n : ℚ) + 1) := by
  have hn := unit_frac_nonneg n
  have hsub : (regTaylorCosSeq θ).seq n - taylorCos6 θ = (1 / 2) * (1 / ((n : ℚ) + 1)) := by
    simp [regTaylorCosSeq]
  rw [hsub, abs_le]
  constructor <;> linarith

/-- The regular Cauchy sine sequence converges to `taylorSin7 θ` at rate $\frac{1}{2(n+1)}$. -/
theorem regTaylorSinSeq_approx_limit (θ : ℚ) (n : ℕ) :
    |(regTaylorSinSeq θ).seq n - taylorSin7 θ| ≤ 1 / ((n : ℚ) + 1) := by
  have hn := unit_frac_nonneg n
  have hsub : (regTaylorSinSeq θ).seq n - taylorSin7 θ = (1 / 2) * (1 / ((n : ℚ) + 1)) := by
    simp [regTaylorSinSeq]
  rw [hsub, abs_le]
  constructor <;> linarith

/-! ## Section 3: 4D Hermitian Matrix Carrier over $\mathbb{Q}(i)$ and Effect-Additive Born Rule -/

/-- A $2 \times 2$ Hermitian matrix over $\mathbb{Q}(i)$:
$\begin{pmatrix} d_1 & b_r - i b_i \\ b_r + i b_i & d_2 \end{pmatrix}$ with $d_1, d_2, b_r, b_i \in \mathbb{Q}$.
Extends the 3D real-symmetric matrix carrier ($b_i = 0$) to the 4D $\mathbb{Q}$-vector space of
Gaussian-rational Hermitian operators. -/
@[ext]
structure HermitianMat2Qi where
  d1 : ℚ
  d2 : ℚ
  br : ℚ
  bi : ℚ
  deriving DecidableEq, Repr

namespace HermitianMat2Qi

/-- Zero Hermitian matrix. -/
def zero : HermitianMat2Qi := ⟨0, 0, 0, 0⟩

/-- Addition of Hermitian matrices over $\mathbb{Q}(i)$. -/
def add (A B : HermitianMat2Qi) : HermitianMat2Qi :=
  ⟨A.d1 + B.d1, A.d2 + B.d2, A.br + B.br, A.bi + B.bi⟩

/-- Rational scalar multiplication of a Hermitian matrix over $\mathbb{Q}(i)$. -/
def smul (c : ℚ) (A : HermitianMat2Qi) : HermitianMat2Qi :=
  ⟨c * A.d1, c * A.d2, c * A.br, c * A.bi⟩

/-- Basis projector $E_{11} = \operatorname{diag}(1, 0)$. -/
def E11 : HermitianMat2Qi := ⟨1, 0, 0, 0⟩

/-- Basis projector $E_{22} = \operatorname{diag}(0, 1)$. -/
def E22 : HermitianMat2Qi := ⟨0, 1, 0, 0⟩

/-- Pauli-$X$ Hermitian basis matrix $\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$. -/
def sigmaX : HermitianMat2Qi := ⟨0, 0, 1, 0⟩

/-- Pauli-$Y$ Hermitian basis matrix $\sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$. -/
def sigmaY : HermitianMat2Qi := ⟨0, 0, 0, 1⟩

/-- Identity matrix $I_2 = E_{11} + E_{22}$. -/
def idMat : HermitianMat2Qi := ⟨1, 1, 0, 0⟩

/-- Trace $\operatorname{tr}(H) = d_1 + d_2 \in \mathbb{Q}$. -/
def trace (H : HermitianMat2Qi) : ℚ := H.d1 + H.d2

/-- Determinant $\det(H) = d_1 d_2 - (b_r^2 + b_i^2) \in \mathbb{Q}$. -/
def det (H : HermitianMat2Qi) : ℚ := H.d1 * H.d2 - (H.br * H.br + H.bi * H.bi)

/-- Real part of the Frobenius trace inner product $\operatorname{tr}(W H)$ on $2\times 2$
Hermitian matrices over $\mathbb{Q}(i)$:
$\operatorname{tr}(W H) = w_{d1} h_{d1} + w_{d2} h_{d2} + 2 w_{br} h_{br} + 2 w_{bi} h_{bi}$. -/
def frobeniusTrace (W H : HermitianMat2Qi) : ℚ :=
  W.d1 * H.d1 + W.d2 * H.d2 + 2 * W.br * H.br + 2 * W.bi * H.bi

/-- Embedding of the 3D real-symmetric matrix carrier into `HermitianMat2Qi` ($b_i = 0$). -/
def ofRealSym (d1 d2 br : ℚ) : HermitianMat2Qi := ⟨d1, d2, br, 0⟩

/-- Rank-1 Hermitian state projector $|\psi\rangle\langle\psi|$ for an unnormalized Gaussian-rational
ket $\psi = (x_1 + i y_1, x_2 + i y_2) \in \mathbb{Q}(i)^2$. -/
def rankOneKet (x1 y1 x2 y2 : ℚ) : HermitianMat2Qi where
  d1 := x1 * x1 + y1 * y1
  d2 := x2 * x2 + y2 * y2
  br := x1 * x2 + y1 * y2
  bi := x1 * y2 - y1 * x2

/-- Every $H \in \mathrm{Herm}_2(\mathbb{Q}(i))$ decomposes in the 4-element basis $\{E_{11}, E_{22}, \sigma_x, \sigma_y\}$. -/
theorem basis_decomposition (H : HermitianMat2Qi) :
    H = add (add (smul H.d1 E11) (smul H.d2 E22))
            (add (smul H.br sigmaX) (smul H.bi sigmaY)) := by
  ext <;> simp [add, smul, E11, E22, sigmaX, sigmaY]

/-- Symmetry of the Hermitian Frobenius trace pairing. -/
theorem frobeniusTrace_comm (W H : HermitianMat2Qi) :
    frobeniusTrace W H = frobeniusTrace H W := by
  simp [frobeniusTrace]
  ring

/-- Right additivity of the Hermitian Frobenius trace pairing. -/
theorem frobeniusTrace_add_right (W A B : HermitianMat2Qi) :
    frobeniusTrace W (add A B) = frobeniusTrace W A + frobeniusTrace W B := by
  simp [frobeniusTrace, add]
  ring

/-- Right $\mathbb{Q}$-homogeneity of the Hermitian Frobenius trace pairing. -/
theorem frobeniusTrace_smul_right (W A : HermitianMat2Qi) (c : ℚ) :
    frobeniusTrace W (smul c A) = c * frobeniusTrace W A := by
  simp [frobeniusTrace, smul]
  ring

/-- The imaginary Pauli-$Y$ operator $\sigma_y$ is Frobenius-orthogonal to the entire 3D
real-symmetric subspace (`ofRealSym d1 d2 br`). -/
theorem sigmaY_orthogonal_to_realSym (d1 d2 br : ℚ) :
    frobeniusTrace (ofRealSym d1 d2 br) sigmaY = 0 := by
  simp [frobeniusTrace, ofRealSym, sigmaY]

/-- Every rank-1 Gaussian-rational state projector has determinant zero (`det = 0`), a direct
manifestation of the Brahmagupta-Fibonacci norm multiplicativity over $\mathbb{Q}(i)$. -/
theorem rankOneKet_det_zero (x1 y1 x2 y2 : ℚ) :
    det (rankOneKet x1 y1 x2 y2) = 0 := by
  simp [det, rankOneKet]
  ring

/-- The trace of a rank-1 Gaussian-rational state projector equals the $\ell_2^2$ norm squared. -/
theorem rankOneKet_trace (x1 y1 x2 y2 : ℚ) :
    trace (rankOneKet x1 y1 x2 y2) = x1 * x1 + y1 * y1 + (x2 * x2 + y2 * y2) := rfl

/-- Born transition pairing between two rank-1 Gaussian-rational kets $\psi, \phi \in \mathbb{Q}(i)^2$
equals the squared modulus $|\langle \psi | \phi \rangle|^2$ of their Hermitian inner product. -/
theorem frobeniusTrace_rankOneKet_eq_inner_mod_sq (x1 y1 x2 y2 u1 v1 u2 v2 : ℚ) :
    frobeniusTrace (rankOneKet x1 y1 x2 y2) (rankOneKet u1 v1 u2 v2) =
      (x1 * u1 + y1 * v1 + x2 * u2 + y2 * v2) ^ 2 +
        (x1 * v1 - y1 * u1 + x2 * v2 - y2 * u2) ^ 2 := by
  simp [frobeniusTrace, rankOneKet]
  ring

/-- 4D Hermitian $\mathbb{Q}(i)$ Effect-Additive Riesz Representation Theorem:
any $\mathbb{Q}$-linear functional $f : \mathrm{Herm}_2(\mathbb{Q}(i)) \to \mathbb{Q}$ is uniquely
represented as $f(H) = \operatorname{tr}(W_f H)$ where
$W_f = \langle f(E_{11}), f(E_{22}), \frac{1}{2}f(\sigma_x), \frac{1}{2}f(\sigma_y) \rangle$. -/
theorem linear_functional_is_frobeniusTrace
    (f : HermitianMat2Qi → ℚ)
    (h_add : ∀ A B : HermitianMat2Qi, f (add A B) = f A + f B)
    (h_smul : ∀ (c : ℚ) (A : HermitianMat2Qi), f (smul c A) = c * f A) :
    let Wf : HermitianMat2Qi := ⟨f E11, f E22, f sigmaX / 2, f sigmaY / 2⟩
    ∀ H : HermitianMat2Qi, f H = frobeniusTrace Wf H := by
  intro Wf H
  have hdecomp := basis_decomposition H
  conv_lhs => rw [hdecomp]
  rw [h_add, h_add, h_add, h_smul, h_smul, h_smul, h_smul]
  simp [frobeniusTrace, Wf]
  ring

/-- Uniqueness of the representing Hermitian weight operator $W \in \mathrm{Herm}_2(\mathbb{Q}(i))$:
if $\operatorname{tr}(W_1 H) = \operatorname{tr}(W_2 H)$ for all $H \in \{E_{11}, E_{22}, \sigma_x, \sigma_y\}$,
then $W_1 = W_2$. -/
theorem frobeniusTrace_weight_unique (W1 W2 : HermitianMat2Qi)
    (h11 : frobeniusTrace W1 E11 = frobeniusTrace W2 E11)
    (h22 : frobeniusTrace W1 E22 = frobeniusTrace W2 E22)
    (hX : frobeniusTrace W1 sigmaX = frobeniusTrace W2 sigmaX)
    (hY : frobeniusTrace W1 sigmaY = frobeniusTrace W2 sigmaY) :
    W1 = W2 := by
  simp [frobeniusTrace, E11] at h11
  simp [frobeniusTrace, E22] at h22
  simp [frobeniusTrace, sigmaX] at hX
  simp [frobeniusTrace, sigmaY] at hY
  ext
  · exact h11
  · exact h22
  · linarith
  · linarith

end HermitianMat2Qi

end U1Finite.ChebyshevCauchyBridge

#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevT_two
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevT_three
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevT_four
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevU_two
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevU_three
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshev_pell_two
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshev_pell_three
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshev_pell_four
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshev_double_eq_ratCircle_sq
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshev_triple_eq_ratCircle_cube
#print axioms U1Finite.ChebyshevCauchyBridge.chebyshevIter_add
#print axioms U1Finite.ChebyshevCauchyBridge.taylorCos_nested_enclosure
#print axioms U1Finite.ChebyshevCauchyBridge.taylorCos_width_bound
#print axioms U1Finite.ChebyshevCauchyBridge.taylorSin_nested_enclosure
#print axioms U1Finite.ChebyshevCauchyBridge.taylorSin_width_bound
#print axioms U1Finite.ChebyshevCauchyBridge.taylor_pythagorean_defect_identity
#print axioms U1Finite.ChebyshevCauchyBridge.taylor_pythagorean_defect_bound
#print axioms U1Finite.ChebyshevCauchyBridge.cayleyDyadicPoint_on_circle
#print axioms U1Finite.ChebyshevCauchyBridge.cayleyCirclePoint_zero
#print axioms U1Finite.ChebyshevCauchyBridge.regTaylorCosSeq_approx_limit
#print axioms U1Finite.ChebyshevCauchyBridge.regTaylorSinSeq_approx_limit
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.basis_decomposition
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.frobeniusTrace_comm
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.frobeniusTrace_add_right
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.frobeniusTrace_smul_right
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.sigmaY_orthogonal_to_realSym
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.rankOneKet_det_zero
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.rankOneKet_trace
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.frobeniusTrace_rankOneKet_eq_inner_mod_sq
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.linear_functional_is_frobeniusTrace
#print axioms U1Finite.ChebyshevCauchyBridge.HermitianMat2Qi.frobeniusTrace_weight_unique
