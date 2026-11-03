/-
# Continuous frame functions on the real sphere: the Cooke–Keane–Moran core

This module formalizes the analytic half of the Gleason-type argument on `ℝ³`,
following Cooke, Keane and Moran (1985).  Vectors are `Fin 3 → ℝ`; a frame
function is a degree-zero function on nonzero vectors (so it is a function on
rays) whose values on every orthogonal triple sum to a fixed weight.

Contents (pole `e1 = ![1, 0, 0]`):

* `IsFrameFunction`: degree-zero on nonzero vectors, constant sum on orthogonal triples.
* Lemma 1(iii): two orthogonal pairs sharing a normal have the same sum.
* Lemma 3 (descent): if `f` is constant `m` on the equator `{v 0 = 0}` and `f ≥ m`,
  then one tangent step `a ↦ a + t • (0, -a 2, a 1)` does not increase `f`.
* Lemma 5 (Piron chains): every complex `m` with `‖m‖ > 1` is a finite product of
  factors `1 + t * I`, so every lower latitude is reached by tangent steps.
* Latitude monotonicity, latitude constancy (by continuity), the frame identity
  for the latitude profile, Cauchy's equation on `[0,1]`, and Proposition 1:
  a continuous frame function with its maximum at `e1` and constant on the
  equator is `m + (M - m) · lat`, with `lat v = (v 0)² / ⟨v, v⟩`.
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.SpecialFunctions.Complex.Arg
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Order.DenselyOrdered
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

namespace GleasonReal

open Real Filter Topology

/-- Dot product on `Fin 3 → ℝ`, written out so that `ring` can see it. -/
def dot3 (u v : Fin 3 → ℝ) : ℝ := u 0 * v 0 + u 1 * v 1 + u 2 * v 2

/-- Cross product on `Fin 3 → ℝ`. -/
def cross3 (u v : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![u 1 * v 2 - u 2 * v 1, u 2 * v 0 - u 0 * v 2, u 0 * v 1 - u 1 * v 0]

/-- The pole. -/
def e1 : Fin 3 → ℝ := ![1, 0, 0]

/-- Latitude of a nonzero vector with respect to the pole `e1`. -/
noncomputable def lat (v : Fin 3 → ℝ) : ℝ := (v 0) ^ 2 / dot3 v v

/-- A frame function of weight `W`: degree zero on nonzero vectors and summing to `W`
on every orthogonal triple of nonzero vectors. -/
structure IsFrameFunction (f : (Fin 3 → ℝ) → ℝ) (W : ℝ) : Prop where
  scale : ∀ v : Fin 3 → ℝ, v ≠ 0 → ∀ c : ℝ, c ≠ 0 → f (c • v) = f v
  frame : ∀ u v w : Fin 3 → ℝ, u ≠ 0 → v ≠ 0 → w ≠ 0 →
    dot3 u v = 0 → dot3 u w = 0 → dot3 v w = 0 → f u + f v + f w = W

lemma dot3_comm (u v : Fin 3 → ℝ) : dot3 u v = dot3 v u := by unfold dot3; ring

lemma dot3_self_nonneg (v : Fin 3 → ℝ) : 0 ≤ dot3 v v := by
  unfold dot3; nlinarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2)]

lemma ne_zero_iff_dot3_self_pos (v : Fin 3 → ℝ) : v ≠ 0 ↔ 0 < dot3 v v := by
  constructor
  · intro hv
    rcases Function.ne_iff.mp hv with ⟨i, hi⟩
    have hsq : 0 < v i ^ 2 := lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 hi))
    unfold dot3
    fin_cases i <;> simp at hsq <;> nlinarith [sq_nonneg (v 0), sq_nonneg (v 1), sq_nonneg (v 2)]
  · intro h hv
    subst hv
    simp [dot3] at h

lemma dot3_self_pos {v : Fin 3 → ℝ} (hv : v ≠ 0) : 0 < dot3 v v :=
  (ne_zero_iff_dot3_self_pos v).mp hv

lemma ne_zero_of_dot3_self_pos {v : Fin 3 → ℝ} (h : 0 < dot3 v v) : v ≠ 0 :=
  (ne_zero_iff_dot3_self_pos v).mpr h

/-- A vector with a nonzero coordinate is nonzero. -/
lemma ne_zero_of_apply_ne {v : Fin 3 → ℝ} {i : Fin 3} (h : v i ≠ 0) : v ≠ 0 :=
  fun hv => h (by simp [hv])

lemma ne_zero_of_transverse_ne {v : Fin 3 → ℝ} (hr : v 1 ^ 2 + v 2 ^ 2 ≠ 0) : v ≠ 0 :=
  fun h => hr (by simp [h])

lemma e1_ne_zero : e1 ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simp [e1])

lemma dot3_e1_self : dot3 e1 e1 = 1 := by simp [dot3, e1]

lemma lat_e1 : lat e1 = 1 := by simp [lat, e1, dot3]

lemma lat_nonneg (v : Fin 3 → ℝ) : 0 ≤ lat v := by
  unfold lat; exact div_nonneg (sq_nonneg _) (dot3_self_nonneg v)

lemma lat_le_one {v : Fin 3 → ℝ} (hv : v ≠ 0) : lat v ≤ 1 := by
  unfold lat
  rw [div_le_one (dot3_self_pos hv)]
  unfold dot3; nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]

lemma lat_smul (v : Fin 3 → ℝ) {c : ℝ} (hc : c ≠ 0) : lat (c • v) = lat v := by
  unfold lat dot3
  simp only [Pi.smul_apply, smul_eq_mul]
  have : c ^ 2 ≠ 0 := pow_ne_zero 2 hc
  field_simp

/-- Latitude comparison in cleared-denominator form. -/
lemma lat_lt_iff {a b : Fin 3 → ℝ} (ha : a ≠ 0) (hb : b ≠ 0) :
    lat b < lat a ↔ (b 0) ^ 2 * (a 1 ^ 2 + a 2 ^ 2) < (a 0) ^ 2 * (b 1 ^ 2 + b 2 ^ 2) := by
  unfold lat
  rw [div_lt_div_iff₀ (dot3_self_pos hb) (dot3_self_pos ha)]
  unfold dot3
  constructor <;> intro h <;> nlinarith [h]

lemma lat_eq_iff {a b : Fin 3 → ℝ} (ha : a ≠ 0) (hb : b ≠ 0) :
    lat b = lat a ↔ (b 0) ^ 2 * (a 1 ^ 2 + a 2 ^ 2) = (a 0) ^ 2 * (b 1 ^ 2 + b 2 ^ 2) := by
  unfold lat
  rw [div_eq_div_iff (dot3_self_pos hb).ne' (dot3_self_pos ha).ne']
  unfold dot3
  constructor <;> intro h <;> nlinarith [h]


/-! ### Lemma 1(iii): two orthogonal pairs with a common normal have equal sums -/

lemma pair_sum_eq_of_common_normal {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    {a a₂ b b₂ n : Fin 3 → ℝ} (ha : a ≠ 0) (ha₂ : a₂ ≠ 0) (hb : b ≠ 0) (hb₂ : b₂ ≠ 0) (hn : n ≠ 0)
    (haa : dot3 a a₂ = 0) (han : dot3 a n = 0) (ha₂n : dot3 a₂ n = 0)
    (hbb : dot3 b b₂ = 0) (hbn : dot3 b n = 0) (hb₂n : dot3 b₂ n = 0) :
    f a + f a₂ = f b + f b₂ := by
  have h1 := hf.frame a a₂ n ha ha₂ hn haa han ha₂n
  have h2 := hf.frame b b₂ n hb hb₂ hn hbb hbn hb₂n
  linarith

/-! ### Lemma 3: one tangent step at the pole `e1` does not increase `f` -/

/-- The tangent direction to the latitude circle through `a` (pole `e1`). -/
def tangentDir (a : Fin 3 → ℝ) : Fin 3 → ℝ := ![0, -a 2, a 1]

/-- One tangent step from `a`: the ray of `a + t • tangentDir a`.  In the complex
coordinate `w = a 1 + a 2 * I` this multiplies `w` by `1 + t * I`. -/
def tangentStep (a : Fin 3 → ℝ) (t : ℝ) : Fin 3 → ℝ := a + t • tangentDir a

lemma tangentStep_apply (a : Fin 3 → ℝ) (t : ℝ) :
    tangentStep a t = ![a 0, a 1 - t * a 2, a 2 + t * a 1] := by
  ext i; fin_cases i <;> simp [tangentStep, tangentDir, sub_eq_add_neg]

/-- Lemma 3 (descent, exact form).  If `f` is constant `m` on the equator and `f ≥ m`
everywhere, a tangent step never increases `f`. -/
theorem tangentStep_le {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v)
    (a : Fin 3 → ℝ) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0) (t : ℝ) :
    f (tangentStep a t) ≤ f a := by
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  -- the tangent direction `u`, the common normal `n`, the stepped point `b`
  -- and its orthogonal partner `b₂` on the same great circle
  let u : Fin 3 → ℝ := ![0, -a 2, a 1]
  let n : Fin 3 → ℝ := ![a 1 ^ 2 + a 2 ^ 2, -(a 0 * a 1), -(a 0 * a 2)]
  let b : Fin 3 → ℝ := ![a 0, a 1 - t * a 2, a 2 + t * a 1]
  let b₂ : Fin 3 → ℝ := ![-(t * (a 1 ^ 2 + a 2 ^ 2)) * a 0,
    -(a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 2 - t * (a 1 ^ 2 + a 2 ^ 2) * a 1,
    (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 1 - t * (a 1 ^ 2 + a 2 ^ 2) * a 2]
  have hb : tangentStep a t = b := by rw [tangentStep_apply]
  have ha0 : a ≠ 0 := ne_zero_of_dot3_self_pos (by unfold dot3; nlinarith [sq_nonneg (a 0)])
  have hu0 : u ≠ 0 := ne_zero_of_dot3_self_pos (by simp only [dot3, u]; simp; nlinarith)
  have hn0 : n ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [n] using hr)
  have hb0 : b ≠ 0 := ne_zero_of_dot3_self_pos (by
    simp only [dot3, b]; simp
    nlinarith [sq_nonneg (a 0), mul_nonneg (sq_nonneg t) hr'.le])
  have hb₂0 : b₂ ≠ 0 := by
    -- its second and third coordinates are `|a|² • (-(a 2), a 1)` shifted by a multiple of `(a 1, a 2)`;
    -- the dot product with `(-(a 2), a 1)` is `|a|² (a 1² + a 2²) > 0`.
    intro h
    have h1 := congrFun h 1
    have h2 := congrFun h 2
    simp [b₂] at h1 h2
    have : (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * (a 1 ^ 2 + a 2 ^ 2) = 0 := by
      linear_combination (-(a 2)) * h1 + a 1 * h2
    rcases mul_eq_zero.mp this with h3 | h3
    · nlinarith [sq_nonneg (a 0)]
    · exact hr h3
  have key := pair_sum_eq_of_common_normal hf ha0 hu0 hb0 hb₂0 hn0
    (by simp [dot3, u]; ring) (by simp [dot3, n]; ring) (by simp [dot3, u, n]; ring)
    (by simp [dot3, b, b₂]; ring) (by simp [dot3, b, n]; ring) (by simp [dot3, b₂, n]; ring)
  have hum : f u = m := heq u hu0 (by simp [u])
  have hb₂m : m ≤ f b₂ := hmin b₂ hb₂0
  rw [hb]; linarith

/-! ### Chains of tangent steps -/

/-- The point with first coordinate `x` and complex transverse coordinate `w`. -/
noncomputable def pt (x : ℝ) (w : ℂ) : Fin 3 → ℝ := ![x, w.re, w.im]

lemma pt_ne_zero_of_ne {x : ℝ} {w : ℂ} (hw : w ≠ 0) : pt x w ≠ 0 := by
  intro h
  apply hw
  apply Complex.ext
  · have := congrFun h 1; simpa [pt] using this
  · have := congrFun h 2; simpa [pt] using this

lemma pt_transverse_ne {x : ℝ} {w : ℂ} (hw : w ≠ 0) :
    (pt x w) 1 ^ 2 + (pt x w) 2 ^ 2 ≠ 0 := by
  simp only [pt]
  simp
  intro h
  apply hw
  apply Complex.ext <;> simp <;> nlinarith [sq_nonneg w.re, sq_nonneg w.im]

lemma tangentStep_pt (x : ℝ) (w : ℂ) (t : ℝ) :
    tangentStep (pt x w) t = pt x (w * (1 + t * Complex.I)) := by
  rw [tangentStep_apply]
  ext i; fin_cases i <;> simp [pt] <;> ring

/-- Lemma 3 iterated along a list of tangent steps. -/
theorem chain_le {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v) (x : ℝ) :
    ∀ (ts : List ℝ) (w : ℂ), w ≠ 0 →
      f (pt x (w * (ts.map (fun t : ℝ => (1 : ℂ) + t * Complex.I)).prod)) ≤ f (pt x w) := by
  intro ts
  induction ts with
  | nil => intro w _; simp
  | cons t rest ih =>
    intro w hw
    have hfac : (1 : ℂ) + t * Complex.I ≠ 0 := by
      intro h
      have := congrArg Complex.re h
      simp at this
    have h1 := ih (w * (1 + t * Complex.I)) (mul_ne_zero hw hfac)
    have h2 : f (pt x (w * (1 + t * Complex.I))) ≤ f (pt x w) := by
      rw [← tangentStep_pt]
      exact tangentStep_le hf heq hmin (pt x w) (pt_transverse_ne hw) t
    calc f (pt x (w * ((List.map (fun t : ℝ => (1 : ℂ) + t * Complex.I) (t :: rest)).prod)))
        = f (pt x (w * (1 + t * Complex.I) *
            (List.map (fun t : ℝ => (1 : ℂ) + t * Complex.I) rest).prod)) := by
          simp [List.map_cons, List.prod_cons, mul_assoc]
      _ ≤ f (pt x (w * (1 + t * Complex.I))) := h1
      _ ≤ f (pt x w) := h2


/-! ### Lemma 5: every multiplier of modulus `> 1` is a product of factors `1 + t * I` -/

lemma one_add_tan_mul_I (φ : ℝ) (h : 0 < Real.cos φ) :
    (1 : ℂ) + (Real.tan φ : ℂ) * Complex.I =
      (((Real.cos φ)⁻¹ : ℝ) : ℂ) * Complex.exp (φ * Complex.I) := by
  rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin, Real.tan_eq_sin_div_cos]
  have hc : (Real.cos φ : ℂ) ≠ 0 := by exact_mod_cast h.ne'
  rw [Complex.ofReal_div, Complex.ofReal_inv]
  field_simp

/-- Lemma 5 in multiplier form: a complex number of modulus greater than one is a finite
product of factors `1 + t * I` with `t` real.  The factors are `n` copies of
`1 + tan (θ / n) * I` (which rotate by `θ = arg m` and expand by `cos (θ / n) ^ (-n)`)
followed by the conjugate pair `1 ± s * I`, which fixes the modulus.  The choice of `n`
uses `cos x ≥ 1 - x² / 2` and Bernoulli's inequality. -/
theorem exists_chain_eq (m : ℂ) (hm : 1 < ‖m‖) :
    ∃ ts : List ℝ, (ts.map (fun t : ℝ => (1 : ℂ) + t * Complex.I)).prod = m := by
  set θ := Complex.arg m with hθdef
  have hθ : |θ| ≤ π := Complex.abs_arg_le_pi m
  set r := ‖m‖ with hrdef
  have hr0 : 0 < r := by linarith
  have hr1 : 0 < 1 - 1 / r := by
    rw [sub_pos, div_lt_one hr0]; exact hm
  obtain ⟨n, hn3, hnθ, hnbig⟩ : ∃ n : ℕ, 3 ≤ n ∧ |θ| ≤ n ∧ θ ^ 2 / (2 * (1 - 1 / r)) ≤ n := by
    refine ⟨3 + ⌈|θ|⌉₊ + ⌈θ ^ 2 / (2 * (1 - 1 / r))⌉₊, by omega, ?_, ?_⟩
    · push_cast
      linarith [Nat.le_ceil |θ|, (Nat.cast_nonneg (⌈θ ^ 2 / (2 * (1 - 1 / r))⌉₊) : (0:ℝ) ≤ _)]
    · push_cast
      linarith [Nat.le_ceil (θ ^ 2 / (2 * (1 - 1 / r))), (Nat.cast_nonneg ⌈|θ|⌉₊ : (0:ℝ) ≤ _)]
  have hnpos : (0 : ℝ) < n := by exact_mod_cast (by omega : 0 < n)
  have hn3' : (3 : ℝ) ≤ n := by exact_mod_cast hn3
  set φ := θ / n with hφdef
  have hφabs : |φ| ≤ |θ| / n := by
    rw [hφdef, abs_div, abs_of_pos hnpos]
  have hφ3 : |φ| ≤ π / 3 := by
    calc |φ| ≤ |θ| / n := hφabs
      _ ≤ π / 3 := by
          rw [div_le_div_iff₀ hnpos (by norm_num)]
          nlinarith [abs_nonneg θ]
  have hφ1 : |φ| ≤ 1 := by
    calc |φ| ≤ |θ| / n := hφabs
      _ ≤ 1 := by rw [div_le_one hnpos]; exact hnθ
  have hcos : 0 < Real.cos φ := by
    apply Real.cos_pos_of_mem_Ioo
    constructor <;> linarith [abs_le.mp hφ3, Real.pi_pos]
  have hc1 : 1 - φ ^ 2 / 2 ≤ Real.cos φ := Real.one_sub_sq_div_two_le_cos
  have hφsq : φ ^ 2 ≤ 1 := by
    have := abs_le.mp hφ1; nlinarith
  have hc0 : 0 ≤ 1 - φ ^ 2 / 2 := by linarith
  have hpow : (1 - φ ^ 2 / 2) ^ n ≤ Real.cos φ ^ n := pow_le_pow_left₀ hc0 hc1 n
  have hbern : 1 + n * (-(φ ^ 2 / 2)) ≤ (1 + -(φ ^ 2 / 2)) ^ n :=
    one_add_mul_le_pow (by linarith) n
  have hnφ : (n : ℝ) * (φ ^ 2 / 2) = θ ^ 2 / (2 * n) := by
    rw [hφdef]; field_simp
  have hθn : θ ^ 2 / (2 * n) ≤ 1 - 1 / r := by
    rw [div_le_iff₀ (by positivity)]
    rw [div_le_iff₀ (by positivity)] at hnbig
    linarith
  have hcn : 1 / r ≤ Real.cos φ ^ n := by
    have h1 : (1 : ℝ) + -(φ ^ 2 / 2) = 1 - φ ^ 2 / 2 := by ring
    rw [h1] at hbern
    nlinarith
  set c := Real.cos φ ^ n with hcdef
  have hcpos : 0 < c := pow_pos hcos n
  have hrc : 1 ≤ r * c := by
    rw [div_le_iff₀ hr0] at hcn; linarith
  set s := Real.sqrt (r * c - 1) with hsdef
  have hs2 : s ^ 2 = r * c - 1 := Real.sq_sqrt (by linarith)
  refine ⟨List.replicate n (Real.tan φ) ++ [s, -s], ?_⟩
  rw [List.map_append, List.prod_append, List.map_replicate, List.prod_replicate]
  simp only [List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, mul_one]
  rw [one_add_tan_mul_I φ hcos, mul_pow, ← Complex.exp_nat_mul]
  have hs : ((1 : ℂ) + (s : ℂ) * Complex.I) * (1 + ((-s : ℝ) : ℂ) * Complex.I) =
      ((r * c : ℝ) : ℂ) := by
    have : ((1 : ℂ) + (s : ℂ) * Complex.I) * (1 + ((-s : ℝ) : ℂ) * Complex.I)
        = 1 + (s : ℂ) ^ 2 := by
      push_cast; linear_combination (-(s : ℂ) ^ 2) * Complex.I_sq
    rw [this, ← Complex.ofReal_pow, hs2]; push_cast; ring
  have hexp : Complex.exp ((n : ℂ) * ((φ : ℂ) * Complex.I)) = Complex.exp ((θ : ℂ) * Complex.I) := by
    congr 1
    have hnC : (n : ℂ) ≠ 0 := by exact_mod_cast hnpos.ne'
    rw [hφdef]; push_cast
    field_simp
  rw [hs, hexp]
  have hcc : ((((Real.cos φ)⁻¹ : ℝ) : ℂ) ^ n) * ((r * c : ℝ) : ℂ) = (r : ℂ) := by
    have hcC : Complex.cos (φ : ℂ) ^ n ≠ 0 := by
      rw [← Complex.ofReal_cos, ← Complex.ofReal_pow]; exact_mod_cast (pow_pos hcos n).ne'
    rw [hcdef]; push_cast
    rw [inv_pow]
    field_simp
  calc ((((Real.cos φ)⁻¹ : ℝ) : ℂ) ^ n) * Complex.exp ((θ : ℂ) * Complex.I) * ((r * c : ℝ) : ℂ)
      = (((((Real.cos φ)⁻¹ : ℝ) : ℂ) ^ n) * ((r * c : ℝ) : ℂ)) *
          Complex.exp ((θ : ℂ) * Complex.I) := by ring
    _ = (r : ℂ) * Complex.exp ((θ : ℂ) * Complex.I) := by rw [hcc]
    _ = m := Complex.norm_mul_exp_arg_mul_I m


/-! ### Latitude monotonicity and, with continuity, latitude constancy -/

lemma pt_eq_self (a : Fin 3 → ℝ) : pt (a 0) ((a 1 : ℂ) + (a 2 : ℂ) * Complex.I) = a := by
  ext i; fin_cases i <;> simp [pt]

lemma norm_sq_transverse (a : Fin 3 → ℝ) :
    ‖((a 1 : ℂ) + (a 2 : ℂ) * Complex.I)‖ ^ 2 = a 1 ^ 2 + a 2 ^ 2 := by
  rw [Complex.sq_norm, Complex.normSq_apply]; simp; ring

/-- Lemma 3 + Lemma 5: a lower latitude never carries a larger value. -/
theorem le_of_lat_lt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v)
    {a b : Fin 3 → ℝ} (ha : a ≠ 0) (hb : b ≠ 0) (hlt : lat b < lat a) : f b ≤ f a := by
  rw [lat_lt_iff ha hb] at hlt
  by_cases hb0 : b 0 = 0
  · rw [heq b hb hb0]; exact hmin a ha
  have ha0 : a 0 ≠ 0 := by
    intro h; rw [h] at hlt; nlinarith [sq_nonneg (b 0), sq_nonneg (a 1), sq_nonneg (a 2)]
  by_cases hra : a 1 ^ 2 + a 2 ^ 2 = 0
  · -- `a` is a multiple of the pole
    have ha1 : a 1 = 0 := by nlinarith [sq_nonneg (a 1), sq_nonneg (a 2)]
    have ha2 : a 2 = 0 := by nlinarith [sq_nonneg (a 1), sq_nonneg (a 2)]
    have hae : a = (a 0) • e1 := by ext i; fin_cases i <;> simp [e1, ha1, ha2]
    rw [hae, hf.scale e1 e1_ne_zero (a 0) ha0]
    exact hmax b hb
  have hrb : b 1 ^ 2 + b 2 ^ 2 ≠ 0 := by
    intro h; rw [h] at hlt; nlinarith [sq_nonneg (b 0), sq_nonneg (a 1), sq_nonneg (a 2)]
  set w : ℂ := (a 1 : ℂ) + (a 2 : ℂ) * Complex.I with hw
  set w' : ℂ := (b 1 : ℂ) + (b 2 : ℂ) * Complex.I with hw'
  have hwn : ‖w‖ ^ 2 = a 1 ^ 2 + a 2 ^ 2 := norm_sq_transverse a
  have hw'n : ‖w'‖ ^ 2 = b 1 ^ 2 + b 2 ^ 2 := norm_sq_transverse b
  have hw0 : w ≠ 0 := by
    intro h; apply hra; rw [← hwn, h, norm_zero]; ring
  have hw'0 : w' ≠ 0 := by
    intro h; apply hrb; rw [← hw'n, h, norm_zero]; ring
  set mc : ℂ := ((a 0 / b 0 : ℝ) : ℂ) * (w' / w) with hmc
  have hmc1 : 1 < ‖mc‖ := by
    have hnorm : ‖mc‖ = (|a 0| / |b 0|) * (‖w'‖ / ‖w‖) := by
      rw [hmc, Complex.norm_mul, Complex.norm_div, Complex.norm_real, Real.norm_eq_abs, abs_div]
    rw [hnorm]
    have hwpos : 0 < ‖w‖ := norm_pos_iff.mpr hw0
    have hb0' : 0 < |b 0| := abs_pos.mpr hb0
    rw [div_mul_div_comm, one_lt_div (by positivity)]
    have hsq : (|b 0| * ‖w‖) ^ 2 < (|a 0| * ‖w'‖) ^ 2 := by
      rw [mul_pow, mul_pow, sq_abs, sq_abs, hwn, hw'n]; exact hlt
    exact (pow_lt_pow_iff_left₀ (by positivity) (by positivity) (by norm_num)).mp hsq
  obtain ⟨ts, hts⟩ := exists_chain_eq mc hmc1
  have hchain := chain_le hf heq hmin (a 0) ts w hw0
  rw [hts, pt_eq_self] at hchain
  have hpt : pt (a 0) (w * mc) = (a 0 / b 0) • b := by
    have : w * mc = ((a 0 / b 0 : ℝ) : ℂ) * w' := by
      rw [hmc]; field_simp
    rw [this]
    ext i; fin_cases i
    · simp [pt]; field_simp
    · simp [pt, hw']
    · simp [pt, hw']
  rw [hpt, hf.scale b hb (a 0 / b 0) (div_ne_zero ha0 hb0)] at hchain
  exact hchain

/-- Raising the first coordinate raises the latitude. -/
lemma lat_lt_lat_add_smul_e1 {a : Fin 3 → ℝ} (ha0 : a 0 ≠ 0) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0)
    {ε : ℝ} (hε : 0 < ε) : lat a < lat (a + (ε * a 0) • e1) := by
  have ha : a ≠ 0 := ne_zero_of_apply_ne ha0
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  have h0 : (a + (ε * a 0) • e1) 0 = a 0 * (1 + ε) := by simp [e1]; ring
  have h1 : (a + (ε * a 0) • e1) 1 = a 1 := by simp [e1]
  have h2 : (a + (ε * a 0) • e1) 2 = a 2 := by simp [e1]
  have hb : a + (ε * a 0) • e1 ≠ 0 :=
    ne_zero_of_apply_ne (i := 0) (by rw [h0]; exact mul_ne_zero ha0 (by linarith))
  rw [lat_lt_iff hb ha, h0, h1, h2]
  have hpos : 0 < a 0 ^ 2 * (a 1 ^ 2 + a 2 ^ 2) := by positivity
  have h1 : 1 < (1 + ε) ^ 2 := by nlinarith
  have key : (a 0 * (1 + ε)) ^ 2 * (a 1 ^ 2 + a 2 ^ 2) =
      a 0 ^ 2 * (a 1 ^ 2 + a 2 ^ 2) * (1 + ε) ^ 2 := by ring
  rw [key]
  have := mul_lt_mul_of_pos_left h1 hpos
  linarith

/-- With continuity, equal latitudes carry equal values. -/
theorem eq_of_lat_eq {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0})
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v)
    {a b : Fin 3 → ℝ} (ha : a ≠ 0) (hb : b ≠ 0) (h : lat b = lat a) : f b = f a := by
  -- it suffices to prove `f b ≤ f a` for every such pair
  suffices key : ∀ a b : Fin 3 → ℝ, a ≠ 0 → b ≠ 0 → lat b = lat a → f b ≤ f a from
    le_antisymm (key a b ha hb h) (key b a hb ha h.symm)
  intro a b ha hb h
  by_cases ha0 : a 0 = 0
  · -- both on the equator
    have hb0 : b 0 = 0 := by
      have hla : lat a = 0 := by simp [lat, ha0]
      rw [hla, lat, div_eq_zero_iff] at h
      rcases h with h | h
      · exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h
      · exact absurd h (dot3_self_pos hb).ne'
    rw [heq a ha ha0, heq b hb hb0]
  by_cases hra : a 1 ^ 2 + a 2 ^ 2 = 0
  · -- `a` is a multiple of the pole, hence so is `b`
    have ha1 : a 1 = 0 := by nlinarith [sq_nonneg (a 1), sq_nonneg (a 2)]
    have ha2 : a 2 = 0 := by nlinarith [sq_nonneg (a 1), sq_nonneg (a 2)]
    rw [lat_eq_iff ha hb, ha1, ha2] at h
    have hrb : b 1 ^ 2 + b 2 ^ 2 = 0 := by
      have : a 0 ^ 2 * (b 1 ^ 2 + b 2 ^ 2) = 0 := by linarith
      rcases mul_eq_zero.mp this with h' | h'
      · exact absurd (pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h') ha0
      · exact h'
    have hb1 : b 1 = 0 := by nlinarith [sq_nonneg (b 1), sq_nonneg (b 2)]
    have hb2 : b 2 = 0 := by nlinarith [sq_nonneg (b 1), sq_nonneg (b 2)]
    have hb0 : b 0 ≠ 0 := by
      intro h0; apply hb; ext i; fin_cases i <;> simp [h0, hb1, hb2]
    have hae : a = (a 0) • e1 := by ext i; fin_cases i <;> simp [e1, ha1, ha2]
    have hbe : b = (b 0) • e1 := by ext i; fin_cases i <;> simp [e1, hb1, hb2]
    rw [hae, hbe, hf.scale e1 e1_ne_zero (a 0) ha0, hf.scale e1 e1_ne_zero (b 0) hb0]
  -- generic case: approach `a` from strictly higher latitudes along the pole direction
  have hne : ∀ ε : ℝ, a + (ε * a 0) • e1 ≠ 0 := fun ε =>
    ne_zero_of_transverse_ne (by simpa [e1] using hra)
  have hstep : ∀ ε : ℝ, 0 < ε → f b ≤ f (a + (ε * a 0) • e1) := by
    intro ε hε
    have hlt : lat b < lat (a + (ε * a 0) • e1) := h ▸ lat_lt_lat_add_smul_e1 ha0 hra hε
    exact le_of_lat_lt hf hmax heq hmin (hne ε) hb hlt
  have hlim : Tendsto (fun ε : ℝ => f (a + (ε * a 0) • e1)) (𝓝[>] 0) (𝓝 (f a)) := by
    have hcont : ContinuousWithinAt f {v | v ≠ 0} a := hc a ha
    have hpath : Tendsto (fun ε : ℝ => a + (ε * a 0) • e1) (𝓝[>] 0) (𝓝[{v | v ≠ 0}] a) := by
      rw [tendsto_nhdsWithin_iff]
      constructor
      · have : Tendsto (fun ε : ℝ => a + (ε * a 0) • e1) (𝓝 0) (𝓝 (a + (0 * a 0) • e1)) :=
          ((continuous_const.add ((continuous_id.mul continuous_const).smul
            continuous_const)).tendsto 0)
        simpa using this.mono_left nhdsWithin_le_nhds
      · exact eventually_nhdsWithin_of_forall fun ε _ => hne ε
    exact hcont.tendsto.comp hpath
  exact ge_of_tendsto hlim (eventually_nhdsWithin_of_forall fun ε hε => hstep ε hε)


/-! ### Extreme values: the unit sphere is compact -/

/-- The unit sphere. -/
def sphere3 : Set (Fin 3 → ℝ) := {v | dot3 v v = 1}

lemma sq_le_dot3_self (v : Fin 3 → ℝ) (i : Fin 3) : v i ^ 2 ≤ dot3 v v := by
  unfold dot3
  fin_cases i <;> simp <;> nlinarith [mul_self_nonneg (v 0), mul_self_nonneg (v 1), mul_self_nonneg (v 2)]

lemma continuous_dot3_self : Continuous fun v : Fin 3 → ℝ => dot3 v v := by
  unfold dot3; fun_prop

lemma isCompact_sphere3 : IsCompact sphere3 := by
  apply Metric.isCompact_of_isClosed_isBounded
  · exact isClosed_eq continuous_dot3_self continuous_const
  · apply (Metric.isBounded_closedBall (x := (0 : Fin 3 → ℝ)) (r := 1)).subset
    intro v hv
    rw [Metric.mem_closedBall, dist_zero_right, pi_norm_le_iff_of_nonneg zero_le_one]
    intro i
    rw [Real.norm_eq_abs]
    apply abs_le_of_sq_le_sq _ zero_le_one
    rw [one_pow, ← show dot3 v v = 1 from hv]
    exact sq_le_dot3_self v i

lemma e1_mem_sphere3 : e1 ∈ sphere3 := dot3_e1_self

lemma sphere3_subset : sphere3 ⊆ {v : Fin 3 → ℝ | v ≠ 0} := fun v hv =>
  ne_zero_of_dot3_self_pos (by rw [show dot3 v v = 1 from hv]; exact one_pos)

lemma dot3_smul_smul (c : ℝ) (v : Fin 3 → ℝ) : dot3 (c • v) (c • v) = c ^ 2 * dot3 v v := by
  simp [dot3]; ring

/-- Normalisation: every nonzero vector is a positive multiple of a unit vector. -/
lemma exists_unit_smul {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    ∃ c : ℝ, c ≠ 0 ∧ c • v ∈ sphere3 := by
  refine ⟨1 / Real.sqrt (dot3 v v), ?_, ?_⟩
  · exact one_div_ne_zero (Real.sqrt_pos.mpr (dot3_self_pos hv)).ne'
  · show dot3 _ _ = 1
    rw [dot3_smul_smul, div_pow, one_pow, Real.sq_sqrt (dot3_self_nonneg v)]
    exact div_mul_cancel₀ 1 (dot3_self_pos hv).ne'

theorem exists_min {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) :
    ∃ s : Fin 3 → ℝ, s ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f s ≤ f v := by
  obtain ⟨s, hs, hmin⟩ := isCompact_sphere3.exists_isMinOn ⟨e1, e1_mem_sphere3⟩
    (hc.mono sphere3_subset)
  refine ⟨s, sphere3_subset hs, fun v hv => ?_⟩
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
  have : f s ≤ f (c • v) := hmin hcv
  rwa [hf.scale v hv c hc0] at this

theorem exists_max {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) :
    ∃ p : Fin 3 → ℝ, p ≠ 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p := by
  obtain ⟨p, hp, hmax⟩ := isCompact_sphere3.exists_isMaxOn ⟨e1, e1_mem_sphere3⟩
    (hc.mono sphere3_subset)
  refine ⟨p, sphere3_subset hp, fun v hv => ?_⟩
  obtain ⟨c, hc0, hcv⟩ := exists_unit_smul hv
  have : f (c • v) ≤ f p := hmax hcv
  rwa [hf.scale v hv c hc0] at this

/-- Lemma 1(iv) at the pole: if the maximum is at `e1` and `f` is constant `m` on the
equator, then `m` is the minimum. -/
theorem equator_const_is_min {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0})
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v := by
  obtain ⟨s, hs, hmin⟩ := exists_min hf hc
  intro v hv
  refine le_trans ?_ (hmin v hv)
  by_cases hrs : s 1 ^ 2 + s 2 ^ 2 = 0
  · -- `s` is a multiple of the pole, so `f` is constant
    have hs1 : s 1 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs2 : s 2 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs0 : s 0 ≠ 0 := by
      intro h0; apply hs; ext i; fin_cases i <;> simp [h0, hs1, hs2]
    have hse : s = (s 0) • e1 := by ext i; fin_cases i <;> simp [e1, hs1, hs2]
    have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
    have h1 := heq ![0, 1, 0] he2 (by simp)
    have h2 := hmax ![0, 1, 0] he2
    rw [hse, hf.scale e1 e1_ne_zero (s 0) hs0]
    linarith
  · -- the great circle through `e1` and `s`
    let s' : Fin 3 → ℝ := ![0, s 1, s 2]
    let s'' : Fin 3 → ℝ := ![s 1 ^ 2 + s 2 ^ 2, -(s 0 * s 1), -(s 0 * s 2)]
    let n : Fin 3 → ℝ := ![0, -(s 2), s 1]
    have hs' : s' ≠ 0 := ne_zero_of_transverse_ne (by simpa [s'] using hrs)
    have hs'' : s'' ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [s''] using hrs)
    have hn : n ≠ 0 := ne_zero_of_transverse_ne (by simp [n]; intro h; apply hrs; linarith)
    have key := pair_sum_eq_of_common_normal hf e1_ne_zero hs' hs hs'' hn
      (by simp [dot3, e1, s']) (by simp [dot3, e1, n]) (by simp [dot3, s', n]; ring)
      (by simp [dot3, s'']; ring) (by simp [dot3, n]; ring) (by simp [dot3, s'', n]; ring)
    have h1 := heq s' hs' (by simp [s'])
    have h2 := hmax s'' hs''
    linarith

/-! ### The latitude profile and Cauchy's equation on `[0, 1]` -/

/-- A reference point of latitude `l` (for `0 ≤ l ≤ 1`). -/
noncomputable def refPt (l : ℝ) : Fin 3 → ℝ := ![Real.sqrt l, Real.sqrt (1 - l), 0]

lemma refPt_dot3 {l : ℝ} (h0 : 0 ≤ l) (h1 : l ≤ 1) : dot3 (refPt l) (refPt l) = 1 := by
  simp [dot3, refPt, ← sq, Real.sq_sqrt h0, Real.sq_sqrt (sub_nonneg.mpr h1)]

lemma refPt_ne_zero {l : ℝ} (h0 : 0 ≤ l) (h1 : l ≤ 1) : refPt l ≠ 0 :=
  ne_zero_of_dot3_self_pos (by rw [refPt_dot3 h0 h1]; exact one_pos)

lemma lat_refPt {l : ℝ} (h0 : 0 ≤ l) (h1 : l ≤ 1) : lat (refPt l) = l := by
  rw [lat, refPt_dot3 h0 h1, div_one]; simp [refPt, Real.sq_sqrt h0]

lemma refPt_zero : refPt 0 = ![0, 1, 0] := by simp [refPt]

lemma refPt_one : refPt 1 = e1 := by simp [refPt, e1]

/-- Cauchy's equation on `[0, 1]`: a monotone additive function is linear. -/
theorem linear_of_monotone_additive (ψ : ℝ → ℝ)
    (hmono : ∀ x y : ℝ, 0 ≤ x → x ≤ y → y ≤ 1 → ψ x ≤ ψ y)
    (hadd : ∀ x y : ℝ, 0 ≤ x → 0 ≤ y → x + y ≤ 1 → ψ (x + y) = ψ x + ψ y) :
    ∀ x : ℝ, 0 ≤ x → x ≤ 1 → ψ x = x * ψ 1 := by
  have h0 : ψ 0 = 0 := by
    have := hadd 0 0 le_rfl le_rfl (by norm_num); simp at this; linarith
  have hψ1 : 0 ≤ ψ 1 := by have := hmono 0 1 le_rfl zero_le_one le_rfl; linarith
  -- values at the rationals `k / n`
  have hrat : ∀ n : ℕ, 0 < n → ∀ k : ℕ, k ≤ n → ψ ((k : ℝ) / n) = k * ψ (1 / n) := by
    intro n hn k
    induction k with
    | zero => intro _; simp [h0]
    | succ k ih =>
      intro hk
      have hn' : (0 : ℝ) < n := by exact_mod_cast hn
      have hk' : (k : ℝ) + 1 ≤ n := by exact_mod_cast hk
      have e : ((k + 1 : ℕ) : ℝ) / n = (k : ℝ) / n + 1 / n := by push_cast; ring
      rw [e, hadd _ _ (by positivity) (by positivity) (by
        rw [← add_div, div_le_one hn']; exact hk'), ih (by omega)]
      push_cast; ring
  have hunit : ∀ n : ℕ, 0 < n → ψ (1 / n) = ψ 1 / n := by
    intro n hn
    have hn' : (0 : ℝ) < n := by exact_mod_cast hn
    have := hrat n hn n le_rfl
    rw [div_self hn'.ne'] at this
    rw [this]; field_simp
  have hrat' : ∀ n : ℕ, 0 < n → ∀ k : ℕ, k ≤ n → ψ ((k : ℝ) / n) = (k : ℝ) / n * ψ 1 := by
    intro n hn k hk
    rw [hrat n hn k hk, hunit n hn]; ring
  intro x hx0 hx1
  -- sandwich between consecutive rationals
  have hbound : ∀ n : ℕ, 0 < n → |ψ x - x * ψ 1| ≤ ψ 1 / n := by
    intro n hn
    have hn' : (0 : ℝ) < n := by exact_mod_cast hn
    set k := ⌊(n : ℝ) * x⌋₊ with hk
    have hk0 : (k : ℝ) ≤ n * x := Nat.floor_le (by positivity)
    have hk1 : (n : ℝ) * x < k + 1 := Nat.lt_floor_add_one _
    have hkn : k ≤ n := by
      have : (k : ℝ) ≤ n := le_trans hk0 (by nlinarith)
      exact_mod_cast this
    have hlow : (k : ℝ) / n * ψ 1 ≤ ψ x := by
      rw [← hrat' n hn k hkn]
      exact hmono _ _ (by positivity) (by rw [div_le_iff₀ hn']; linarith) hx1
    have hup : ψ x ≤ ((k : ℝ) + 1) / n * ψ 1 := by
      by_cases hkn' : k + 1 ≤ n
      · have := hrat' n hn (k + 1) hkn'
        push_cast at this
        rw [← this]
        exact hmono _ _ hx0 (by rw [le_div_iff₀ hn']; linarith)
          (by rw [div_le_one hn']; exact_mod_cast hkn')
      · -- then `k = n` and `x = 1`
        have hkn'' : k = n := by omega
        have hx : x = 1 := by
          rw [hkn''] at hk0
          have : (n : ℝ) * 1 ≤ n * x := by linarith
          exact le_antisymm hx1 (le_of_mul_le_mul_left this hn')
        rw [hx, hkn'']
        have : ((n : ℝ) + 1) / n * ψ 1 = ψ 1 + ψ 1 / n := by field_simp
        rw [this]; linarith [div_nonneg hψ1 hn'.le]
    rw [abs_le]
    constructor
    · have : x * ψ 1 ≤ ((k : ℝ) + 1) / n * ψ 1 := by
        apply mul_le_mul_of_nonneg_right _ hψ1
        rw [le_div_iff₀ hn']; linarith
      have e : ((k : ℝ) + 1) / n * ψ 1 - (k : ℝ) / n * ψ 1 = ψ 1 / n := by field_simp; ring
      linarith
    · have : (k : ℝ) / n * ψ 1 ≤ x * ψ 1 := by
        apply mul_le_mul_of_nonneg_right _ hψ1
        rw [div_le_iff₀ hn']; linarith
      have e : ((k : ℝ) + 1) / n * ψ 1 - (k : ℝ) / n * ψ 1 = ψ 1 / n := by field_simp; ring
      linarith
  -- the bound holds for every `n`, so the difference is zero
  by_contra hne
  have hpos : 0 < |ψ x - x * ψ 1| := abs_pos.mpr (sub_ne_zero.mpr hne)
  obtain ⟨n, hn⟩ := exists_nat_gt (ψ 1 / |ψ x - x * ψ 1|)
  have hn0 : 0 < n := by
    have : (0 : ℝ) ≤ ψ 1 / |ψ x - x * ψ 1| := div_nonneg hψ1 hpos.le
    exact_mod_cast lt_of_le_of_lt this hn
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn0
  have h1 := hbound n hn0
  rw [div_lt_iff₀ hpos] at hn
  rw [le_div_iff₀ hn'] at h1
  linarith


/-! ### A frame with prescribed latitudes, and Proposition 1 at the pole -/

/-- For `x, y, z ≥ 0` with `x + y + z = 1` there is an orthogonal triple with latitudes
`x, y, z`: the rows of the Householder reflection taking `e1` to `(√x, √y, √z)`. -/
theorem exists_frame_with_lat {x y z : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hz : 0 ≤ z)
    (hsum : x + y + z = 1) :
    ∃ u v w : Fin 3 → ℝ, u ≠ 0 ∧ v ≠ 0 ∧ w ≠ 0 ∧
      dot3 u v = 0 ∧ dot3 u w = 0 ∧ dot3 v w = 0 ∧ lat u = x ∧ lat v = y ∧ lat w = z := by
  by_cases hx1 : x = 1
  · have hy0 : y = 0 := by linarith
    have hz0 : z = 0 := by linarith
    refine ⟨e1, ![0, 1, 0], ![0, 0, 1], e1_ne_zero, ne_zero_of_apply_ne (i := 1) (by simp),
      ne_zero_of_apply_ne (i := 2) (by simp), by simp [dot3, e1], by simp [dot3, e1],
      by simp [dot3], ?_, ?_, ?_⟩
    · rw [lat_e1, hx1]
    · simp [lat, dot3, hy0]
    · simp [lat, dot3, hz0]
  · set p := Real.sqrt x with hp
    set q := Real.sqrt y with hq
    set r := Real.sqrt z with hr
    have hp2 : p ^ 2 = x := Real.sq_sqrt hx
    have hq2 : q ^ 2 = y := Real.sq_sqrt hy
    have hr2 : r ^ 2 = z := Real.sq_sqrt hz
    have hunit : p ^ 2 + q ^ 2 + r ^ 2 = 1 := by rw [hp2, hq2, hr2]; exact hsum
    have hp1 : p < 1 := by
      have hxlt : x < 1 := lt_of_le_of_ne (by linarith) hx1
      rw [hp, show (1 : ℝ) = Real.sqrt 1 by simp]
      exact Real.sqrt_lt_sqrt hx hxlt
    have h1p : 0 < 1 - p := by linarith
    let u : Fin 3 → ℝ := ![p, q, r]
    let v : Fin 3 → ℝ := ![q * (1 - p), 1 - p - q ^ 2, -(q * r)]
    let w : Fin 3 → ℝ := ![r * (1 - p), -(q * r), 1 - p - r ^ 2]
    have huu : dot3 u u = 1 := by simp [dot3, u, ← sq]; exact hunit
    have hvv : dot3 v v = (1 - p) ^ 2 := by
      simp [dot3, v]; linear_combination q ^ 2 * hunit
    have hww : dot3 w w = (1 - p) ^ 2 := by
      simp [dot3, w]; linear_combination r ^ 2 * hunit
    refine ⟨u, v, w, ne_zero_of_dot3_self_pos (by rw [huu]; exact one_pos),
      ne_zero_of_dot3_self_pos (by rw [hvv]; positivity),
      ne_zero_of_dot3_self_pos (by rw [hww]; positivity), ?_, ?_, ?_, ?_, ?_, ?_⟩
    · simp [dot3, u, v]; linear_combination (-q) * hunit
    · simp [dot3, u, w]; linear_combination (-r) * hunit
    · simp [dot3, v, w]; linear_combination (q * r) * hunit
    · rw [lat, huu, div_one]; simpa [u] using hp2
    · rw [lat, hvv]; simp only [v]; simp
      rw [mul_pow, mul_div_assoc, div_self (by positivity), mul_one]; exact hq2
    · rw [lat, hww]; simp only [w]; simp
      rw [mul_pow, mul_div_assoc, div_self (by positivity), mul_one]; exact hr2

/-- **Proposition 1 at the pole.**  A continuous frame function with its maximum at `e1`
and constant on the equator `{v 0 = 0}` is `m + (M - m) · lat`. -/
theorem prop1_pole {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0})
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f e1 - m) * lat v := by
  have hmin := equator_const_is_min hf hc hmax heq
  -- the latitude profile
  set φ : ℝ → ℝ := fun l => f (refPt l) with hφ
  have hprof : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = φ (lat v) := fun v hv =>
    eq_of_lat_eq hf hc hmax heq hmin (refPt_ne_zero (lat_nonneg v) (lat_le_one hv)) hv
      (lat_refPt (lat_nonneg v) (lat_le_one hv)).symm
  have hφ0 : φ 0 = m := by
    simp only [hφ]; rw [refPt_zero]
    exact heq _ (ne_zero_of_apply_ne (i := 1) (by simp)) (by simp)
  have hφ1 : φ 1 = f e1 := by simp only [hφ]; rw [refPt_one]
  have hmono : ∀ x y : ℝ, 0 ≤ x → x ≤ y → y ≤ 1 → φ x ≤ φ y := by
    intro x y hx hxy hy
    rcases eq_or_lt_of_le hxy with h | h
    · rw [h]
    · simp only [hφ]
      exact le_of_lat_lt hf hmax heq hmin (refPt_ne_zero (by linarith) hy)
        (refPt_ne_zero hx (by linarith)) (by rw [lat_refPt hx (by linarith), lat_refPt (by linarith) hy]; exact h)
  have hframe : ∀ x y z : ℝ, 0 ≤ x → 0 ≤ y → 0 ≤ z → x + y + z = 1 → φ x + φ y + φ z = W := by
    intro x y z hx hy hz hsum
    obtain ⟨u, v, w, hu, hv, hw, huv, huw, hvw, hlu, hlv, hlw⟩ := exists_frame_with_lat hx hy hz hsum
    have := hf.frame u v w hu hv hw huv huw hvw
    rwa [hprof u hu, hprof v hv, hprof w hw, hlu, hlv, hlw] at this
  -- Cauchy's equation for `ψ = φ - m`
  set ψ : ℝ → ℝ := fun l => φ l - m with hψ
  have hψmono : ∀ x y : ℝ, 0 ≤ x → x ≤ y → y ≤ 1 → ψ x ≤ ψ y := by
    intro x y hx hxy hy; simp only [hψ]; linarith [hmono x y hx hxy hy]
  have hψadd : ∀ x y : ℝ, 0 ≤ x → 0 ≤ y → x + y ≤ 1 → ψ (x + y) = ψ x + ψ y := by
    intro x y hx hy hxy
    have h1 := hframe (x + y) 0 (1 - x - y) (by linarith) le_rfl (by linarith) (by ring)
    have h2 := hframe x y (1 - x - y) hx hy (by linarith) (by ring)
    simp only [hψ]; linarith
  have hlin := linear_of_monotone_additive ψ hψmono hψadd
  intro v hv
  have h := hlin (lat v) (lat_nonneg v) (lat_le_one hv)
  simp only [hψ, hφ1] at h
  rw [hprof v hv]
  linarith

end GleasonReal
