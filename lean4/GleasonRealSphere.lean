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

/-- The third basis vector. -/
def e3 : Fin 3 → ℝ := ![0, 0, 1]

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

lemma e3_ne_zero : e3 ≠ 0 := ne_zero_of_apply_ne (i := 2) (by simp [e3])

lemma dot3_e3_self : dot3 e3 e3 = 1 := by simp [dot3, e3]

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

lemma dot3_smul_left (c : ℝ) (u v : Fin 3 → ℝ) : dot3 (c • u) v = c * dot3 u v := by
  simp [dot3]; ring

lemma dot3_smul_right (c : ℝ) (u v : Fin 3 → ℝ) : dot3 u (c • v) = c * dot3 u v := by
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


/-! ### Orthonormal frames and transport of frame functions -/

/-- Orthonormality of a triple. -/
structure IsOrthonormal (p q r : Fin 3 → ℝ) : Prop where
  pp : dot3 p p = 1
  qq : dot3 q q = 1
  rr : dot3 r r = 1
  pq : dot3 p q = 0
  pr : dot3 p r = 0
  qr : dot3 q r = 0

/-- Coordinates `v` in the frame `(p, q, r)` to the vector `v 0 • p + v 1 • q + v 2 • r`. -/
def ofFrame (p q r : Fin 3 → ℝ) (v : Fin 3 → ℝ) : Fin 3 → ℝ := v 0 • p + v 1 • q + v 2 • r

/-- The coordinates of `w` in the frame `(p, q, r)`. -/
def toFrame (p q r : Fin 3 → ℝ) (w : Fin 3 → ℝ) : Fin 3 → ℝ := ![dot3 w p, dot3 w q, dot3 w r]

lemma ofFrame_apply (p q r v : Fin 3 → ℝ) (i : Fin 3) :
    ofFrame p q r v i = v 0 * p i + v 1 * q i + v 2 * r i := by
  simp [ofFrame]

lemma dot3_ofFrame {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (u v : Fin 3 → ℝ) :
    dot3 (ofFrame p q r u) (ofFrame p q r v) = dot3 u v := by
  have hpp := h.pp; have hqq := h.qq; have hrr := h.rr
  have hpq := h.pq; have hpr := h.pr; have hqr := h.qr
  simp only [dot3, ofFrame_apply] at *
  linear_combination (u 0 * v 0) * hpp + (u 1 * v 1) * hqq + (u 2 * v 2) * hrr +
    (u 0 * v 1 + u 1 * v 0) * hpq + (u 0 * v 2 + u 2 * v 0) * hpr + (u 1 * v 2 + u 2 * v 1) * hqr

lemma ofFrame_smul (p q r : Fin 3 → ℝ) (c : ℝ) (v : Fin 3 → ℝ) :
    ofFrame p q r (c • v) = c • ofFrame p q r v := by
  ext i; simp [ofFrame_apply]; ring

lemma ofFrame_ne_zero {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) {v : Fin 3 → ℝ}
    (hv : v ≠ 0) : ofFrame p q r v ≠ 0 :=
  ne_zero_of_dot3_self_pos (by rw [dot3_ofFrame h]; exact dot3_self_pos hv)

lemma continuous_ofFrame (p q r : Fin 3 → ℝ) : Continuous (ofFrame p q r) := by
  unfold ofFrame; fun_prop

lemma dot3_ofFrame_left {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (v : Fin 3 → ℝ) :
    dot3 (ofFrame p q r v) p = v 0 ∧ dot3 (ofFrame p q r v) q = v 1 ∧
      dot3 (ofFrame p q r v) r = v 2 := by
  have hpp := h.pp; have hqq := h.qq; have hrr := h.rr
  have hpq := h.pq; have hpr := h.pr; have hqr := h.qr
  simp only [dot3, ofFrame_apply] at *
  refine ⟨?_, ?_, ?_⟩
  · linear_combination (v 0) * hpp + (v 1) * hpq + (v 2) * hpr
  · linear_combination (v 0) * hpq + (v 1) * hqq + (v 2) * hqr
  · linear_combination (v 0) * hpr + (v 1) * hqr + (v 2) * hrr

lemma toFrame_ofFrame {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (v : Fin 3 → ℝ) :
    toFrame p q r (ofFrame p q r v) = v := by
  obtain ⟨h0, h1, h2⟩ := dot3_ofFrame_left h v
  ext i; fin_cases i <;> simp [toFrame, h0, h1, h2]

/-- Completeness: the columns of an orthogonal matrix are orthonormal, hence so are the rows. -/
lemma completeness {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (j k : Fin 3) :
    p j * p k + q j * q k + r j * r k = if j = k then 1 else 0 := by
  let M : Matrix (Fin 3) (Fin 3) ℝ := Matrix.of fun i l => (![p, q, r] l) i
  have h1 : Matrix.transpose M * M = 1 := by
    have hpp := h.pp; have hqq := h.qq; have hrr := h.rr
    have hpq := h.pq; have hpr := h.pr; have hqr := h.qr
    simp only [dot3] at hpp hqq hrr hpq hpr hqr
    ext a b
    fin_cases a <;> fin_cases b <;>
      simp [M, Matrix.mul_apply, Fin.sum_univ_three] <;> linarith
  have h2 : M * Matrix.transpose M = 1 := mul_eq_one_comm.1 h1
  have := congrFun (congrFun h2 j) k
  simpa [M, Matrix.mul_apply, Fin.sum_univ_three, Matrix.one_apply] using this

/-- The six completeness identities, spelled out. -/
lemma completeness' {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) :
    (p 0 * p 0 + q 0 * q 0 + r 0 * r 0 = 1) ∧ (p 1 * p 1 + q 1 * q 1 + r 1 * r 1 = 1) ∧
    (p 2 * p 2 + q 2 * q 2 + r 2 * r 2 = 1) ∧ (p 0 * p 1 + q 0 * q 1 + r 0 * r 1 = 0) ∧
    (p 0 * p 2 + q 0 * q 2 + r 0 * r 2 = 0) ∧ (p 1 * p 2 + q 1 * q 2 + r 1 * r 2 = 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simpa using completeness h 0 0
  · simpa using completeness h 1 1
  · simpa using completeness h 2 2
  · simpa using completeness h 0 1
  · simpa using completeness h 0 2
  · simpa using completeness h 1 2

lemma ofFrame_toFrame {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (w : Fin 3 → ℝ) :
    ofFrame p q r (toFrame p q r w) = w := by
  obtain ⟨c00, c11, c22, c01, c02, c12⟩ := completeness' h
  ext i
  fin_cases i
  · simp [ofFrame_apply, toFrame, dot3]
    linear_combination (w 0) * c00 + (w 1) * c01 + (w 2) * c02
  · simp [ofFrame_apply, toFrame, dot3]
    linear_combination (w 0) * c01 + (w 1) * c11 + (w 2) * c12
  · simp [ofFrame_apply, toFrame, dot3]
    linear_combination (w 0) * c02 + (w 1) * c12 + (w 2) * c22

lemma toFrame_ne_zero {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) {w : Fin 3 → ℝ}
    (hw : w ≠ 0) : toFrame p q r w ≠ 0 := by
  intro h0; apply hw; rw [← ofFrame_toFrame h w, h0]; ext i; simp [ofFrame_apply]

lemma dot3_toFrame_self {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (w : Fin 3 → ℝ) :
    dot3 (toFrame p q r w) (toFrame p q r w) = dot3 w w := by
  conv_rhs => rw [← ofFrame_toFrame h w]
  rw [dot3_ofFrame h]

/-- Transport of frame functions along an orthonormal frame. -/
theorem IsFrameFunction.comp_ofFrame {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) :
    IsFrameFunction (fun v => f (ofFrame p q r v)) W where
  scale v hv c hc := by
    rw [ofFrame_smul, hf.scale _ (ofFrame_ne_zero h hv) c hc]
  frame u v w hu hv hw huv huw hvw := by
    exact hf.frame _ _ _ (ofFrame_ne_zero h hu) (ofFrame_ne_zero h hv) (ofFrame_ne_zero h hw)
      (by rw [dot3_ofFrame h]; exact huv) (by rw [dot3_ofFrame h]; exact huw)
      (by rw [dot3_ofFrame h]; exact hvw)

theorem continuousOn_comp_ofFrame {f : (Fin 3 → ℝ) → ℝ} (hc : ContinuousOn f {v | v ≠ 0})
    {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) :
    ContinuousOn (fun v => f (ofFrame p q r v)) {v | v ≠ 0} :=
  hc.comp (continuous_ofFrame p q r).continuousOn (fun _ hv => ofFrame_ne_zero h hv)

/-- Every unit vector is part of an orthonormal frame (Householder completion). -/
theorem exists_orthonormal_completion {p : Fin 3 → ℝ} (hp : dot3 p p = 1) :
    ∃ q r : Fin 3 → ℝ, IsOrthonormal p q r := by
  have hp' : p 0 * p 0 + p 1 * p 1 + p 2 * p 2 = 1 := hp
  by_cases h1 : p 0 = 1
  · have h10 : p 1 = 0 := by nlinarith [mul_self_nonneg (p 1), mul_self_nonneg (p 2)]
    have h20 : p 2 = 0 := by nlinarith [mul_self_nonneg (p 1), mul_self_nonneg (p 2)]
    exact ⟨![0, 1, 0], ![0, 0, 1], ⟨hp, by simp [dot3], by simp [dot3], by simp [dot3, h10],
      by simp [dot3, h20], by simp [dot3]⟩⟩
  · have hle : p 0 ≤ 1 := by nlinarith [mul_self_nonneg (p 1), mul_self_nonneg (p 2)]
    have hc : 0 < 1 - p 0 := by
      rcases lt_or_eq_of_le hle with h | h
      · linarith
      · exact absurd h h1
    set c := 1 - p 0 with hcdef
    set x : Fin 3 → ℝ := ![p 1 * c, c - p 1 ^ 2, -(p 1 * p 2)] with hx
    set y : Fin 3 → ℝ := ![p 2 * c, -(p 1 * p 2), c - p 2 ^ 2] with hy
    have hxx : dot3 x x = c ^ 2 := by
      simp [dot3, hx, hcdef]; linear_combination (p 1 ^ 2) * hp'
    have hyy : dot3 y y = c ^ 2 := by
      simp [dot3, hy, hcdef]; linear_combination (p 2 ^ 2) * hp'
    have hpx : dot3 p x = 0 := by
      simp [dot3, hx, hcdef]; linear_combination (-(p 1)) * hp'
    have hpy : dot3 p y = 0 := by
      simp [dot3, hy, hcdef]; linear_combination (-(p 2)) * hp'
    have hxy : dot3 x y = 0 := by
      simp [dot3, hx, hy, hcdef]; linear_combination (p 1 * p 2) * hp'
    refine ⟨(1 / c) • x, (1 / c) • y, ⟨hp, ?_, ?_, ?_, ?_, ?_⟩⟩
    · rw [dot3_smul_smul, hxx]; field_simp
    · rw [dot3_smul_smul, hyy]; field_simp
    · rw [dot3_smul_right, hpx, mul_zero]
    · rw [dot3_smul_right, hpy, mul_zero]
    · rw [dot3_smul_left, dot3_smul_right, hxy, mul_zero, mul_zero]

/-- An orthonormal pair extends by the cross product. -/
theorem isOrthonormal_cross {p r : Fin 3 → ℝ} (hp : dot3 p p = 1) (hr : dot3 r r = 1)
    (hpr : dot3 p r = 0) : IsOrthonormal p (cross3 p r) r := by
  have hp' : p 0 * p 0 + p 1 * p 1 + p 2 * p 2 = 1 := hp
  have hr' : r 0 * r 0 + r 1 * r 1 + r 2 * r 2 = 1 := hr
  have hpr' : p 0 * r 0 + p 1 * r 1 + p 2 * r 2 = 0 := hpr
  refine ⟨hp, ?_, hr, by simp [dot3, cross3]; ring, hpr, by simp [dot3, cross3]; ring⟩
  simp [dot3, cross3]
  linear_combination (r 0 * r 0 + r 1 * r 1 + r 2 * r 2) * hp' + hr' -
    (p 0 * r 0 + p 1 * r 1 + p 2 * r 2) * hpr'


lemma ofFrame_e1 (p q r : Fin 3 → ℝ) : ofFrame p q r e1 = p := by
  ext i; simp [ofFrame_apply, e1]

lemma ofFrame_e3 (p q r : Fin 3 → ℝ) : ofFrame p q r e3 = r := by
  ext i; simp [ofFrame_apply, e3]

/-- Parseval for an orthonormal frame. -/
lemma sum_sq_dot3_eq {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) (x : Fin 3 → ℝ) :
    dot3 x p ^ 2 + dot3 x q ^ 2 + dot3 x r ^ 2 = dot3 x x := by
  obtain ⟨c00, c11, c22, c01, c02, c12⟩ := completeness' h
  simp only [dot3]
  linear_combination (x 0 * x 0) * c00 + (x 1 * x 1) * c11 + (x 2 * x 2) * c22 +
    (2 * x 0 * x 1) * c01 + (2 * x 0 * x 2) * c02 + (2 * x 1 * x 2) * c12

lemma sq_div_dot3_smul {c : ℝ} (hc : c ≠ 0) (u p : Fin 3 → ℝ) :
    dot3 (c • u) p ^ 2 / dot3 (c • u) (c • u) = dot3 u p ^ 2 / dot3 u u := by
  rw [dot3_smul_left, dot3_smul_smul, mul_pow, mul_div_mul_left _ _ (pow_ne_zero 2 hc)]

/-- The latitudes of an orthogonal triple with respect to any direction `p` sum to `⟨p, p⟩`. -/
theorem sum_lat_eq {u v w : Fin 3 → ℝ} (hu : u ≠ 0) (hv : v ≠ 0) (hw : w ≠ 0)
    (huv : dot3 u v = 0) (huw : dot3 u w = 0) (hvw : dot3 v w = 0) (p : Fin 3 → ℝ) :
    dot3 u p ^ 2 / dot3 u u + dot3 v p ^ 2 / dot3 v v + dot3 w p ^ 2 / dot3 w w = dot3 p p := by
  obtain ⟨cu, hcu, hcuu⟩ := exists_unit_smul hu
  obtain ⟨cv, hcv, hcvv⟩ := exists_unit_smul hv
  obtain ⟨cw, hcw, hcww⟩ := exists_unit_smul hw
  have h : IsOrthonormal (cu • u) (cv • v) (cw • w) :=
    ⟨hcuu, hcvv, hcww, by rw [dot3_smul_left, dot3_smul_right, huv]; ring,
      by rw [dot3_smul_left, dot3_smul_right, huw]; ring,
      by rw [dot3_smul_left, dot3_smul_right, hvw]; ring⟩
  have key := sum_sq_dot3_eq h p
  have eu := sq_div_dot3_smul hcu u p
  have ev := sq_div_dot3_smul hcv v p
  have ew := sq_div_dot3_smul hcw w p
  rw [show dot3 (cu • u) (cu • u) = 1 from hcuu, div_one] at eu
  rw [show dot3 (cv • v) (cv • v) = 1 from hcvv, div_one] at ev
  rw [show dot3 (cw • w) (cw • w) = 1 from hcww, div_one] at ew
  rw [← eu, ← ev, ← ew, dot3_comm (cu • u), dot3_comm (cv • v), dot3_comm (cw • w)]
  exact key

/-- **Proposition 1 at an arbitrary unit pole.** -/
theorem prop1 {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) {p : Fin 3 → ℝ} (hp : dot3 p p = 1)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v p = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f p - m) * (dot3 v p ^ 2 / dot3 v v) := by
  obtain ⟨q, r, h⟩ := exists_orthonormal_completion hp
  have hF := hf.comp_ofFrame h
  have hcF := continuousOn_comp_ofFrame hc h
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv
    simp only [ofFrame_e1]
    exact hmax _ (ofFrame_ne_zero h hv)
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → (fun v => f (ofFrame p q r v)) v = m := by
    intro v hv hv0
    exact heq _ (ofFrame_ne_zero h hv) (by rw [(dot3_ofFrame_left h v).1]; exact hv0)
  have key := prop1_pole hF hcF hmaxF heqF
  intro w hw
  have := key (toFrame p q r w) (toFrame_ne_zero h hw)
  simp only [ofFrame_e1, ofFrame_toFrame h] at this
  rw [this, lat, dot3_toFrame_self h]
  simp [toFrame]

/-- Lemma 1(iv) at the pole: when the maximum is at `e1`, the minimum is attained on the
equator. -/
theorem exists_min_on_equator_pole {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1) :
    ∃ r : Fin 3 → ℝ, r ≠ 0 ∧ r 0 = 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v := by
  obtain ⟨s, hs, hmin⟩ := exists_min hf hc
  by_cases hrs : s 1 ^ 2 + s 2 ^ 2 = 0
  · -- `s` is a multiple of the pole, so `f` is constant
    have hs1 : s 1 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs2 : s 2 = 0 := by nlinarith [sq_nonneg (s 1), sq_nonneg (s 2)]
    have hs0 : s 0 ≠ 0 := by
      intro h0; apply hs; ext i; fin_cases i <;> simp [h0, hs1, hs2]
    have hse : s = (s 0) • e1 := by ext i; fin_cases i <;> simp [e1, hs1, hs2]
    have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
    refine ⟨![0, 1, 0], he2, by simp, fun v hv => ?_⟩
    have h1 := hmax ![0, 1, 0] he2
    have h2 := hmin v hv
    rw [hse, hf.scale e1 e1_ne_zero (s 0) hs0] at h2
    have h3 := hmax v hv
    linarith
  · let s' : Fin 3 → ℝ := ![0, s 1, s 2]
    let s'' : Fin 3 → ℝ := ![s 1 ^ 2 + s 2 ^ 2, -(s 0 * s 1), -(s 0 * s 2)]
    let n : Fin 3 → ℝ := ![0, -(s 2), s 1]
    have hs' : s' ≠ 0 := ne_zero_of_transverse_ne (by simpa [s'] using hrs)
    have hs'' : s'' ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [s''] using hrs)
    have hn : n ≠ 0 := ne_zero_of_transverse_ne (by simp [n]; intro h; apply hrs; linarith)
    have key := pair_sum_eq_of_common_normal hf e1_ne_zero hs' hs hs'' hn
      (by simp [dot3, e1, s']) (by simp [dot3, e1, n]) (by simp [dot3, s', n]; ring)
      (by simp [dot3, s'']; ring) (by simp [dot3, n]; ring) (by simp [dot3, s'', n]; ring)
    have h2 := hmax s'' hs''
    refine ⟨s', hs', by simp [s'], fun v hv => ?_⟩
    have := hmin v hv
    linarith

/-- Lemma 1(iv): when the maximum is at the unit vector `p`, the minimum is attained at a unit
vector orthogonal to `p`. -/
theorem exists_min_perp {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) {p : Fin 3 → ℝ} (hp : dot3 p p = 1)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p) :
    ∃ r : Fin 3 → ℝ, dot3 r r = 1 ∧ dot3 p r = 0 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f r ≤ f v := by
  obtain ⟨q, r, h⟩ := exists_orthonormal_completion hp
  have hF := hf.comp_ofFrame h
  have hcF := continuousOn_comp_ofFrame hc h
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv
    simp only [ofFrame_e1]
    exact hmax _ (ofFrame_ne_zero h hv)
  obtain ⟨r₀, hr₀, hr₀0, hminF⟩ := exists_min_on_equator_pole hF hcF hmaxF
  have hw : ofFrame p q r r₀ ≠ 0 := ofFrame_ne_zero h hr₀
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hw
  refine ⟨c • ofFrame p q r r₀, hcu, ?_, fun v hv => ?_⟩
  · rw [dot3_smul_right, dot3_comm, (dot3_ofFrame_left h r₀).1, hr₀0, mul_zero]
  · rw [hf.scale _ hw c hc0]
    have := hminF (toFrame p q r v) (toFrame_ne_zero h hv)
    simpa only [ofFrame_toFrame h] using this


/-! ### §4.4: quarter turns, the identities (4.5) and (4.6), and the six circles -/

/-- Quarter turn about `e1`: `(x, y, z) ↦ (x, -z, y)`. -/
def phat (v : Fin 3 → ℝ) : Fin 3 → ℝ := ![v 0, -(v 2), v 1]

/-- Quarter turn about `e3`: `(x, y, z) ↦ (-y, x, z)`. -/
def rhat (v : Fin 3 → ℝ) : Fin 3 → ℝ := ![-(v 1), v 0, v 2]

lemma dot3_phat (u v : Fin 3 → ℝ) : dot3 (phat u) (phat v) = dot3 u v := by
  simp [dot3, phat]; ring

lemma dot3_rhat (u v : Fin 3 → ℝ) : dot3 (rhat u) (rhat v) = dot3 u v := by
  simp [dot3, rhat]; ring

lemma phat_smul (c : ℝ) (v : Fin 3 → ℝ) : phat (c • v) = c • phat v := by
  ext i; fin_cases i <;> simp [phat]

lemma rhat_smul (c : ℝ) (v : Fin 3 → ℝ) : rhat (c • v) = c • rhat v := by
  ext i; fin_cases i <;> simp [rhat]

lemma phat_ne_zero {v : Fin 3 → ℝ} (hv : v ≠ 0) : phat v ≠ 0 :=
  ne_zero_of_dot3_self_pos (by rw [dot3_phat]; exact dot3_self_pos hv)

lemma rhat_ne_zero {v : Fin 3 → ℝ} (hv : v ≠ 0) : rhat v ≠ 0 :=
  ne_zero_of_dot3_self_pos (by rw [dot3_rhat]; exact dot3_self_pos hv)

lemma continuous_phat : Continuous phat := by
  unfold phat; fun_prop

lemma continuous_rhat : Continuous rhat := by
  unfold rhat; fun_prop

lemma phat_e1 : phat e1 = e1 := by ext i; fin_cases i <;> simp [phat, e1]

lemma rhat_e3 : rhat e3 = e3 := by ext i; fin_cases i <;> simp [rhat, e3]

/-- Algebra of frame functions. -/
theorem IsFrameFunction.add {f g : (Fin 3 → ℝ) → ℝ} {W W' : ℝ} (hf : IsFrameFunction f W)
    (hg : IsFrameFunction g W') : IsFrameFunction (fun v => f v + g v) (W + W') where
  scale v hv c hc := by
    show f (c • v) + g (c • v) = f v + g v
    rw [hf.scale v hv c hc, hg.scale v hv c hc]
  frame u v w hu hv hw huv huw hvw := by
    have := hf.frame u v w hu hv hw huv huw hvw
    have := hg.frame u v w hu hv hw huv huw hvw
    show f u + g u + (f v + g v) + (f w + g w) = W + W'
    linarith

theorem IsFrameFunction.neg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W) :
    IsFrameFunction (fun v => -f v) (-W) where
  scale v hv c hc := by
    show -f (c • v) = -f v
    rw [hf.scale v hv c hc]
  frame u v w hu hv hw huv huw hvw := by
    have := hf.frame u v w hu hv hw huv huw hvw
    show -f u + -f v + -f w = -W
    linarith

theorem IsFrameFunction.sub {f g : (Fin 3 → ℝ) → ℝ} {W W' : ℝ} (hf : IsFrameFunction f W)
    (hg : IsFrameFunction g W') : IsFrameFunction (fun v => f v - g v) (W - W') where
  scale v hv c hc := by
    show f (c • v) - g (c • v) = f v - g v
    rw [hf.scale v hv c hc, hg.scale v hv c hc]
  frame u v w hu hv hw huv huw hvw := by
    have := hf.frame u v w hu hv hw huv huw hvw
    have := hg.frame u v w hu hv hw huv huw hvw
    show f u - g u + (f v - g v) + (f w - g w) = W - W'
    linarith

theorem IsFrameFunction.comp_phat {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W) :
    IsFrameFunction (fun v => f (phat v)) W where
  scale v hv c hc := by
    show f (phat (c • v)) = f (phat v)
    rw [phat_smul, hf.scale _ (phat_ne_zero hv) c hc]
  frame u v w hu hv hw huv huw hvw :=
    hf.frame _ _ _ (phat_ne_zero hu) (phat_ne_zero hv) (phat_ne_zero hw)
      (by rw [dot3_phat]; exact huv) (by rw [dot3_phat]; exact huw) (by rw [dot3_phat]; exact hvw)

theorem IsFrameFunction.comp_rhat {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W) :
    IsFrameFunction (fun v => f (rhat v)) W where
  scale v hv c hc := by
    show f (rhat (c • v)) = f (rhat v)
    rw [rhat_smul, hf.scale _ (rhat_ne_zero hv) c hc]
  frame u v w hu hv hw huv huw hvw :=
    hf.frame _ _ _ (rhat_ne_zero hu) (rhat_ne_zero hv) (rhat_ne_zero hw)
      (by rw [dot3_rhat]; exact huv) (by rw [dot3_rhat]; exact huw) (by rw [dot3_rhat]; exact hvw)

theorem continuousOn_comp_phat {f : (Fin 3 → ℝ) → ℝ} (hc : ContinuousOn f {v | v ≠ 0}) :
    ContinuousOn (fun v => f (phat v)) {v | v ≠ 0} :=
  hc.comp continuous_phat.continuousOn (fun _ hv => phat_ne_zero hv)

theorem continuousOn_comp_rhat {f : (Fin 3 → ℝ) → ℝ} (hc : ContinuousOn f {v | v ≠ 0}) :
    ContinuousOn (fun v => f (rhat v)) {v | v ≠ 0} :=
  hc.comp continuous_rhat.continuousOn (fun _ hv => rhat_ne_zero hv)

/-- (4.5): with the maximum at `e1`, `f + f ∘ phat` is an explicit function of the latitude. -/
theorem sum_phat {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (phat v) = (W - f e1) + (3 * f e1 - W) * lat v := by
  have hF : IsFrameFunction (fun v => f v + f (phat v)) (W + W) := hf.add hf.comp_phat
  have hcF : ContinuousOn (fun v => f v + f (phat v)) {v | v ≠ 0} :=
    hc.add (continuousOn_comp_phat hc)
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f v + f (phat v)) v ≤ (fun v => f v + f (phat v)) e1 := by
    intro v hv; simp only [phat_e1]
    linarith [hmax v hv, hmax (phat v) (phat_ne_zero hv)]
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 →
      (fun v => f v + f (phat v)) v = W - f e1 := by
    intro v hv hv0
    have := hf.frame e1 v (phat v) e1_ne_zero hv (phat_ne_zero hv)
      (by simp [dot3, e1, hv0]) (by simp [dot3, e1, phat, hv0]) (by simp [dot3, phat, hv0]; ring)
    show f v + f (phat v) = W - f e1
    linarith
  have key := prop1_pole hF hcF hmaxF heqF
  intro v hv
  have := key v hv
  simp only [phat_e1] at this
  rw [this]; ring

/-- (4.6): with the minimum at `e3`, `f + f ∘ rhat` is an explicit function of `v 2 ^ 2`. -/
theorem sum_rhat {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (rhat v) = (W - f e3) + (3 * f e3 - W) * (v 2 ^ 2 / dot3 v v) := by
  have hG : IsFrameFunction (fun v => -(f v + f (rhat v))) (-(W + W)) := (hf.add hf.comp_rhat).neg
  have hcG : ContinuousOn (fun v => -(f v + f (rhat v))) {v | v ≠ 0} :=
    (hc.add (continuousOn_comp_rhat hc)).neg
  have hmaxG : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => -(f v + f (rhat v))) v ≤ (fun v => -(f v + f (rhat v))) e3 := by
    intro v hv; simp only [rhat_e3]
    linarith [hmin v hv, hmin (rhat v) (rhat_ne_zero hv)]
  have heqG : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v e3 = 0 →
      (fun v => -(f v + f (rhat v))) v = -(W - f e3) := by
    intro v hv hv2
    have hv2' : v 2 = 0 := by simpa [dot3, e3] using hv2
    have := hf.frame e3 v (rhat v) e3_ne_zero hv (rhat_ne_zero hv)
      (by simp [dot3, e3, hv2']) (by simp [dot3, e3, rhat, hv2']) (by simp [dot3, rhat, hv2']; ring)
    show -(f v + f (rhat v)) = -(W - f e3)
    linarith
  have key := prop1 hG hcG dot3_e3_self hmaxG heqG
  intro v hv
  have := key v hv
  simp only [rhat_e3] at this
  have e : dot3 v e3 = v 2 := by simp [dot3, e3]
  rw [e] at this
  linarith

/-- The quadratic frame function with values `M, α, m` on `e1, e2, e3`. -/
noncomputable def stdQuad (M α m : ℝ) (v : Fin 3 → ℝ) : ℝ :=
  (M * v 0 ^ 2 + α * v 1 ^ 2 + m * v 2 ^ 2) / dot3 v v

theorem isFrameFunction_stdQuad (M α m : ℝ) : IsFrameFunction (stdQuad M α m) (M + α + m) where
  scale v hv c hc := by
    simp only [stdQuad, dot3_smul_smul, Pi.smul_apply, smul_eq_mul]
    have := dot3_self_pos hv
    field_simp
  frame u v w hu hv hw huv huw hvw := by
    have h1 := sum_lat_eq hu hv hw huv huw hvw e1
    have h2 := sum_lat_eq hu hv hw huv huw hvw ![0, 1, 0]
    have h3 := sum_lat_eq hu hv hw huv huw hvw e3
    simp [dot3, e1, e3] at h1 h2 h3
    have hu' := dot3_self_pos hu
    have hv' := dot3_self_pos hv
    have hw' := dot3_self_pos hw
    simp only [stdQuad]
    simp only [dot3] at *
    rw [add_div, add_div, add_div, add_div, add_div, add_div]
    linear_combination M * h1 + α * h2 + m * h3

theorem continuousOn_stdQuad (M α m : ℝ) : ContinuousOn (stdQuad M α m) {v | v ≠ 0} := by
  apply ContinuousOn.div
  · fun_prop
  · exact continuous_dot3_self.continuousOn
  · intro v hv; exact (dot3_self_pos hv).ne'

lemma stdQuad_add_phat (M α m : ℝ) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    stdQuad M α m v + stdQuad M α m (phat v) = (α + m) + (2 * M - α - m) * lat v := by
  have hD : v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2 ≠ 0 := by
    have := dot3_self_pos hv; simp only [dot3] at this; nlinarith
  simp only [stdQuad, lat, dot3_phat]
  have e0 : phat v 0 = v 0 := by simp [phat]
  have e1' : phat v 1 = -(v 2) := by simp [phat]
  have e2 : phat v 2 = v 1 := by simp [phat]
  rw [e0, e1', e2]
  simp only [dot3]
  field_simp
  ring

lemma stdQuad_add_rhat (M α m : ℝ) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    stdQuad M α m v + stdQuad M α m (rhat v) = (M + α) + (2 * m - M - α) * (v 2 ^ 2 / dot3 v v) := by
  have hD : v 0 ^ 2 + v 1 ^ 2 + v 2 ^ 2 ≠ 0 := by
    have := dot3_self_pos hv; simp only [dot3] at this; nlinarith
  simp only [stdQuad, dot3_rhat]
  have e0 : rhat v 0 = -(v 1) := by simp [rhat]
  have e1' : rhat v 1 = v 0 := by simp [rhat]
  have e2 : rhat v 2 = v 2 := by simp [rhat]
  rw [e0, e1', e2]
  simp only [dot3]
  field_simp
  ring

lemma stdQuad_e1 (M α m : ℝ) : stdQuad M α m e1 = M := by simp [stdQuad, e1, dot3]
lemma stdQuad_e3 (M α m : ℝ) : stdQuad M α m e3 = m := by simp [stdQuad, e3, dot3]

/-- Lemma 8 (standard position): with the maximum at `e1` and the minimum at `e3`, `f` agrees
with the quadratic `stdQuad (f e1) (W - f e1 - f e3) (f e3)` on the six great circles
`x = ±y`, `x = ±z`, `y = ±z`. -/
theorem eq_stdQuad_on_six_circles {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      f v = stdQuad (f e1) (W - f e1 - f e3) (f e3) v := by
  set M := f e1 with hM
  set m := f e3 with hm
  set α := W - M - m with hα
  set g := stdQuad M α m with hg
  set h : (Fin 3 → ℝ) → ℝ := fun v => f v - g v with hh
  have hhf : IsFrameFunction h 0 := by
    have := hf.sub (isFrameFunction_stdQuad M α m)
    rwa [show W - (M + α + m) = 0 by rw [hα]; ring] at this
  -- the two sign-flip identities
  have hp : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (phat v) = -h v := by
    intro v hv
    have h1 := sum_phat hf hc hmax v hv
    have h2 := stdQuad_add_phat M α m hv
    simp only [hh, hg]
    rw [← hM] at h1
    linarith
  have hr : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (rhat v) = -h v := by
    intro v hv
    have h1 := sum_rhat hf hc hmin v hv
    have h2 := stdQuad_add_rhat M α m hv
    simp only [hh, hg]
    rw [← hm] at h1
    linarith
  have hneg : ∀ v : Fin 3 → ℝ, v ≠ 0 → h ((-1 : ℝ) • v) = h v :=
    fun v hv => hhf.scale v hv (-1) (by norm_num)
  -- an odd word sending `v` to `-v` forces `h v = 0`
  intro v hv hcirc
  suffices hz : h v = 0 by simp only [hh, hg] at hz; linarith
  rcases hcirc with h01 | h01 | h02 | h02 | h12 | h12
  · -- x = y: phat (phat (rhat v)) = -v
    have e : phat (phat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hp _ (phat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · -- x = -y: rhat (phat (phat v)) = -v
    have e : rhat (phat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hr _ (phat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hp _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · -- x = z: rhat (phat (phat (phat (rhat v)))) = -v
    have e : rhat (phat (phat (phat (rhat v)))) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hr _ (phat_ne_zero (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))))
    rw [e, hneg v hv, hp _ (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))),
      hp _ (phat_ne_zero (rhat_ne_zero hv)), hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · -- x = -z: phat (rhat (phat v)) = -v
    have e : phat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hp _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · -- y = z: phat (rhat (rhat v)) = -v
    have e : phat (rhat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hp _ (rhat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hr _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · -- y = -z: rhat (rhat (phat v)) = -v
    have e : rhat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hr _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith


/-! ### Zero counting by a tight frame, and the real Gleason theorem -/

lemma dot3_add_left (u v w : Fin 3 → ℝ) : dot3 (u + v) w = dot3 u w + dot3 v w := by
  simp [dot3]; ring

lemma dot3_sub_left (u v w : Fin 3 → ℝ) : dot3 (u - v) w = dot3 u w - dot3 v w := by
  simp [dot3]; ring

lemma dot3_cross3_left (a b : Fin 3 → ℝ) : dot3 a (cross3 a b) = 0 := by
  simp [dot3, cross3]; ring

lemma dot3_cross3_right (a b : Fin 3 → ℝ) : dot3 b (cross3 a b) = 0 := by
  simp [dot3, cross3]; ring

lemma dot3_cross3_self (a b : Fin 3 → ℝ) :
    dot3 (cross3 a b) (cross3 a b) = dot3 a a * dot3 b b - dot3 a b ^ 2 := by
  simp [dot3, cross3]; ring

theorem exists_max_unit {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) :
    ∃ p : Fin 3 → ℝ, dot3 p p = 1 ∧ ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p := by
  obtain ⟨p, hp, hmax⟩ := exists_max hf hc
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hp
  exact ⟨c • p, hcu, fun v hv => by rw [hf.scale p hp c hc0]; exact hmax v hv⟩

/-- The six normals `(1,∓1,0), (1,0,∓1), (0,1,∓1)` form a tight frame. -/
lemma six_normals_tight (x : Fin 3 → ℝ) :
    dot3 x ![1, -1, 0] ^ 2 + dot3 x ![1, 1, 0] ^ 2 + dot3 x ![1, 0, -1] ^ 2 +
      dot3 x ![1, 0, 1] ^ 2 + dot3 x ![0, 1, -1] ^ 2 + dot3 x ![0, 1, 1] ^ 2 = 4 * dot3 x x := by
  simp [dot3]; ring

/-- **Zero counting.**  A continuous frame function of weight zero vanishing on the six great
circles `x = ±y`, `x = ±z`, `y = ±z` vanishes identically. -/
theorem eq_zero_of_vanishes_on_six_circles {h : (Fin 3 → ℝ) → ℝ} (hh : IsFrameFunction h 0)
    (hc : ContinuousOn h {v | v ≠ 0})
    (h6 : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) → h v = 0) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → h v = 0 := by
  obtain ⟨p, hp, hmax⟩ := exists_max_unit hh hc
  obtain ⟨r, hr, hpr, hmin⟩ := exists_min_perp hh hc hp hmax
  set q := cross3 p r with hq
  have hfr : IsOrthonormal p q r := isOrthonormal_cross hp hr hpr
  have hp0 : p ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hp]; exact one_pos)
  have hq0 : q ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr.qq]; exact one_pos)
  have hr0 : r ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hr]; exact one_pos)
  have hsum : h p + h q + h r = 0 := hh.frame p q r hp0 hq0 hr0 hfr.pq hfr.pr hfr.qr
  -- Lemma 8 for `h` in the frame `(p, q, r)`
  have hH := hh.comp_ofFrame hfr
  have hcH := continuousOn_comp_ofFrame hc hfr
  have hmaxH : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => h (ofFrame p q r v)) v ≤ (fun v => h (ofFrame p q r v)) e1 := by
    intro v hv; simp only [ofFrame_e1]; exact hmax _ (ofFrame_ne_zero hfr hv)
  have hminH : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => h (ofFrame p q r v)) e3 ≤ (fun v => h (ofFrame p q r v)) v := by
    intro v hv; simp only [ofFrame_e3]; exact hmin _ (ofFrame_ne_zero hfr hv)
  have hL8 := eq_stdQuad_on_six_circles hH hcH hmaxH hminH
  simp only [ofFrame_e1, ofFrame_e3] at hL8
  -- `h q` is the maximum of `h` on the equator of `p` and the minimum on the equator of `r`
  have hEp : ∀ e : Fin 3 → ℝ, e ≠ 0 → dot3 e p = 0 → h e ≤ h q := by
    intro e he hep
    have he' : cross3 p e ≠ 0 := ne_zero_of_dot3_self_pos (by
      rw [dot3_cross3_self, hp, dot3_comm p e, hep, one_mul]; simpa using dot3_self_pos he)
    have h1 := hh.frame p e (cross3 p e) hp0 he he' (by rw [dot3_comm]; exact hep)
      (dot3_cross3_left p e) (dot3_cross3_right p e)
    have h2 := hmin _ he'
    linarith
  have hEr : ∀ e : Fin 3 → ℝ, e ≠ 0 → dot3 e r = 0 → h q ≤ h e := by
    intro e he her
    have he' : cross3 r e ≠ 0 := ne_zero_of_dot3_self_pos (by
      rw [dot3_cross3_self, hr, dot3_comm r e, her, one_mul]; simpa using dot3_self_pos he)
    have h1 := hh.frame r e (cross3 r e) hr0 he he' (by rw [dot3_comm]; exact her)
      (dot3_cross3_left r e) (dot3_cross3_right r e)
    have h2 := hmax _ he'
    linarith
  -- the circle `x = y` meets both equators in zeros of `h`
  have hzero_perp : ∀ s : Fin 3 → ℝ, ∃ e : Fin 3 → ℝ, e ≠ 0 ∧ dot3 e s = 0 ∧ h e = 0 := by
    intro s
    by_cases hcr : cross3 s ![1, -1, 0] = 0
    · have hs2 : s 2 = 0 := by have := congrFun hcr 0; simpa [cross3] using this
      exact ⟨e3, e3_ne_zero, by simp [dot3, e3, hs2], h6 e3 e3_ne_zero (Or.inl (by simp [e3]))⟩
    · refine ⟨cross3 s ![1, -1, 0], hcr, by rw [dot3_comm]; exact dot3_cross3_left _ _,
        h6 _ hcr (Or.inl ?_)⟩
      simp [cross3]
  obtain ⟨ep, hep0, hep, hepz⟩ := hzero_perp p
  obtain ⟨er, her0, her, herz⟩ := hzero_perp r
  have hα0 : h q = 0 :=
    le_antisymm (by have := hEr er her0 her; linarith) (by have := hEp ep hep0 hep; linarith)
  have hm0 : h r = -h p := by linarith
  -- tight-frame counting on the circle `x' = y'` of the frame `(p, q, r)`
  set a := p + q with ha
  have hap : dot3 a p = 1 := by rw [ha, dot3_add_left, hp, dot3_comm q p, hfr.pq]; ring
  have haq : dot3 a q = 1 := by rw [ha, dot3_add_left, hfr.pq, hfr.qq]; ring
  have har : dot3 a r = 0 := by rw [ha, dot3_add_left, hfr.pr, hfr.qr]; ring
  have haa : dot3 a a = 2 := by
    rw [ha, dot3_add_left, dot3_comm p, dot3_comm q, dot3_add_left, dot3_add_left, hp, hfr.qq,
      hfr.pq, dot3_comm q p, hfr.pq]; ring
  have key : ∀ n : Fin 3 → ℝ, (∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v n = 0 → h v = 0) →
      h p * (dot3 r n ^ 2 - dot3 a n ^ 2) = 0 := by
    intro n hn
    set β := dot3 r n with hβ
    set γ := dot3 a n with hγ
    set vi := β • a - γ • r with hvi
    have hvin : dot3 vi n = 0 := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, ← hβ, ← hγ]; ring
    have hvp : dot3 vi p = β := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, hap, dot3_comm r p, hpr]; ring
    have hvq : dot3 vi q = β := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, haq, dot3_comm r q, hfr.qr]; ring
    have hvr : dot3 vi r = -γ := by
      rw [hvi, dot3_sub_left, dot3_smul_left, dot3_smul_left, har, hr]; ring
    by_cases hv0 : vi = 0
    · have hβ0 : β = 0 := by rw [← hvp, hv0]; simp [dot3]
      have hγ0 : γ = 0 := by
        have := hvr; rw [hv0] at this; simp [dot3] at this; linarith
      rw [hβ0, hγ0]; ring
    · have h1 : h vi = 0 := hn vi hv0 hvin
      have htf : toFrame p q r vi = ![β, β, -γ] := by
        simp [toFrame, hvp, hvq, hvr]
      have h2 := hL8 (toFrame p q r vi) (toFrame_ne_zero hfr hv0)
        (Or.inl (by rw [htf]; simp))
      rw [ofFrame_toFrame hfr, h1, htf] at h2
      have hD : (β ^ 2 + β ^ 2 + γ ^ 2) ≠ 0 := by
        have := dot3_self_pos (toFrame_ne_zero hfr hv0)
        rw [htf] at this; simp [dot3] at this; nlinarith
      simp only [stdQuad, dot3] at h2
      simp at h2
      rw [eq_comm, div_eq_zero_iff] at h2
      rcases h2 with h2 | h2
      · rw [hm0] at h2; linear_combination h2
      · exfalso; apply hD; linarith
  have k1 := key ![1, -1, 0] (fun v hv hvn => h6 v hv (Or.inl (by simp [dot3] at hvn; linarith)))
  have k2 := key ![1, 1, 0] (fun v hv hvn => h6 v hv (Or.inr (Or.inl (by simp [dot3] at hvn; linarith))))
  have k3 := key ![1, 0, -1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith)))))
  have k4 := key ![1, 0, 1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith))))))
  have k5 := key ![0, 1, -1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (by simp [dot3] at hvn; linarith)))))))
  have k6 := key ![0, 1, 1] (fun v hv hvn => h6 v hv (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (by simp [dot3] at hvn; linarith)))))))
  have htr := six_normals_tight r
  have hta := six_normals_tight a
  have hM0 : h p = 0 := by
    have : h p * (4 * dot3 r r - 4 * dot3 a a) = 0 := by
      linear_combination k1 + k2 + k3 + k4 + k5 + k6 - h p * htr + h p * hta
    rw [hr, haa] at this
    linarith
  -- `h ≤ 0` and weight zero force `h = 0`
  intro v hv
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hv
  obtain ⟨q', r', hfr'⟩ := exists_orthonormal_completion hcu
  have hu0 : c • v ≠ 0 := ne_zero_of_dot3_self_pos (by rw [show dot3 (c • v) (c • v) = 1 from hcu]; exact one_pos)
  have hq'0 : q' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.qq]; exact one_pos)
  have hr'0 : r' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.rr]; exact one_pos)
  have hfs := hh.frame _ q' r' hu0 hq'0 hr'0 hfr'.pq hfr'.pr hfr'.qr
  have h1 := hmax _ hu0
  have h2 := hmax _ hq'0
  have h3 := hmax _ hr'0
  rw [← hh.scale v hv c hc0]
  linarith

/-- **Gleason's theorem on the real sphere.**  Every continuous frame function on nonzero
vectors of `ℝ³` is a quadratic form divided by `⟨v, v⟩`, diagonal in an orthonormal frame. -/
theorem gleason_real {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hc : ContinuousOn f {v | v ≠ 0}) :
    ∃ p q r : Fin 3 → ℝ, IsOrthonormal p q r ∧ ∃ M α m : ℝ, ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v = (M * dot3 v p ^ 2 + α * dot3 v q ^ 2 + m * dot3 v r ^ 2) / dot3 v v := by
  obtain ⟨p, hp, hmax⟩ := exists_max_unit hf hc
  obtain ⟨r, hr, hpr, hmin⟩ := exists_min_perp hf hc hp hmax
  set q := cross3 p r with hq
  have hfr : IsOrthonormal p q r := isOrthonormal_cross hp hr hpr
  refine ⟨p, q, r, hfr, f p, W - f p - f r, f r, ?_⟩
  have hF := hf.comp_ofFrame hfr
  have hcF := continuousOn_comp_ofFrame hc hfr
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv; simp only [ofFrame_e1]; exact hmax _ (ofFrame_ne_zero hfr hv)
  have hminF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) e3 ≤ (fun v => f (ofFrame p q r v)) v := by
    intro v hv; simp only [ofFrame_e3]; exact hmin _ (ofFrame_ne_zero hfr hv)
  have hg := isFrameFunction_stdQuad (f p) (W - f p - f r) (f r)
  have hhf : IsFrameFunction
      (fun v => (fun v => f (ofFrame p q r v)) v - stdQuad (f p) (W - f p - f r) (f r) v) 0 := by
    have := hF.sub hg
    rwa [show W - (f p + (W - f p - f r) + f r) = 0 by ring] at this
  have hhc : ContinuousOn
      (fun v => (fun v => f (ofFrame p q r v)) v - stdQuad (f p) (W - f p - f r) (f r) v)
      {v | v ≠ 0} :=
    hcF.sub (continuousOn_stdQuad _ _ _)
  have h6 : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      (fun v => (fun v => f (ofFrame p q r v)) v - stdQuad (f p) (W - f p - f r) (f r) v) v = 0 := by
    intro v hv hcirc
    have := eq_stdQuad_on_six_circles hF hcF hmaxF hminF v hv hcirc
    simp only [ofFrame_e1, ofFrame_e3] at this
    simp only
    rw [this, sub_self]
  have hz := eq_zero_of_vanishes_on_six_circles hhf hhc h6
  intro w hw
  have := hz (toFrame p q r w) (toFrame_ne_zero hfr hw)
  simp only [ofFrame_toFrame hfr] at this
  rw [sub_eq_zero] at this
  rw [this, stdQuad, dot3_toFrame_self hfr]
  simp [toFrame]

/-! ### Target 2: Nonnegativity bounds, Piron tangent-step inequalities, and continuity-free reductions -/

/-- A nonnegative frame function of weight `W` on `ℝ³ \ {0}`. -/
structure IsNonnegFrameFunction (f : (Fin 3 → ℝ) → ℝ) (W : ℝ) : Prop extends IsFrameFunction f W where
  nonneg : ∀ v : Fin 3 → ℝ, v ≠ 0 → 0 ≤ f v

/-- Transport of nonnegative frame functions along an orthonormal frame. -/
theorem IsNonnegFrameFunction.comp_ofFrame {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p q r : Fin 3 → ℝ} (h : IsOrthonormal p q r) :
    IsNonnegFrameFunction (fun v => f (ofFrame p q r v)) W where
  toIsFrameFunction := hf.toIsFrameFunction.comp_ofFrame h
  nonneg v hv := hf.nonneg (ofFrame p q r v) (ofFrame_ne_zero h hv)

/-- The weight `W` of a nonnegative frame function on `ℝ³ \ {0}` is nonnegative. -/
theorem weight_nonneg_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) : 0 ≤ W := by
  have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
  have hsum := hf.frame e1 ![0, 1, 0] e3 e1_ne_zero he2 e3_ne_zero
    (by simp [dot3, e1]) (by simp [dot3, e1, e3]) (by simp [dot3, e3])
  linarith [hf.nonneg e1 e1_ne_zero, hf.nonneg ![0, 1, 0] he2, hf.nonneg e3 e3_ne_zero]

/-- Every value of a nonnegative frame function on `ℝ³ \ {0}` is bounded above by the weight `W`. -/
theorem le_weight_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) : f v ≤ W := by
  obtain ⟨c, hc0, hcu⟩ := exists_unit_smul hv
  obtain ⟨q', r', hfr'⟩ := exists_orthonormal_completion hcu
  have hu0 : c • v ≠ 0 :=
    ne_zero_of_dot3_self_pos (by rw [show dot3 (c • v) (c • v) = 1 from hcu]; exact one_pos)
  have hq'0 : q' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.qq]; exact one_pos)
  have hr'0 : r' ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hfr'.rr]; exact one_pos)
  have hfs := hf.frame _ q' r' hu0 hq'0 hr'0 hfr'.pq hfr'.pr hfr'.qr
  rw [hf.scale v hv c hc0] at hfs
  linarith [hf.nonneg q' hq'0, hf.nonneg r' hr'0]

/-- Automatic `[0, W]` boundedness of a nonnegative frame function on `ℝ³ \ {0}` (without continuity). -/
theorem bounded_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {v : Fin 3 → ℝ} (hv : v ≠ 0) :
    0 ≤ f v ∧ f v ≤ W :=
  ⟨hf.nonneg v hv, le_weight_of_nonneg hf hv⟩

/-- Orthogonal pair subadditivity: `f u + f v ≤ W` for orthogonal nonzero `u, v ∈ ℝ³ \ {0}`. -/
theorem ortho_add_le_weight_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {u v : Fin 3 → ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dot3 u v = 0) :
    f u + f v ≤ W := by
  have hcr : cross3 u v ≠ 0 := by
    apply ne_zero_of_dot3_self_pos
    rw [dot3_cross3_self, huv]
    have hu' := dot3_self_pos hu
    have hv' := dot3_self_pos hv
    nlinarith
  have hsum := hf.frame u v (cross3 u v) hu hv hcr huv (dot3_cross3_left u v) (dot3_cross3_right u v)
  linarith [hf.nonneg (cross3 u v) hcr]

/-- Orthogonal pair bound: `f v ≤ W - f u` for orthogonal nonzero `u, v ∈ ℝ³ \ {0}`. -/
theorem ortho_le_weight_sub_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {u v : Fin 3 → ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) (huv : dot3 u v = 0) :
    f v ≤ W - f u := by
  linarith [ortho_add_le_weight_of_nonneg hf hu hv huv]

/-- Equatorial vanishing at a pole attaining weight `W`: if `f p = W`, then `f v = 0` for all
nonzero `v ⊥ p`. -/
theorem eq_zero_on_perp_of_pole_eq_weight {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p : Fin 3 → ℝ} (hp : p ≠ 0) (hpW : f p = W)
    {v : Fin 3 → ℝ} (hv : v ≠ 0) (hvp : dot3 v p = 0) :
    f v = 0 := by
  have hpv : dot3 p v = 0 := by rw [dot3_comm]; exact hvp
  have hle := ortho_add_le_weight_of_nonneg hf hp hv hpv
  have hnn := hf.nonneg v hv
  linarith

/-- General Piron tangent-step inequality for any nonnegative frame function (without assuming
`f` is constant on the equator): `f (tangentStep a t) ≤ f a + f (tangentDir a)`. -/
theorem tangentStep_le_add_equator_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (a : Fin 3 → ℝ) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0) (t : ℝ) :
    f (tangentStep a t) ≤ f a + f (tangentDir a) := by
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  let u : Fin 3 → ℝ := tangentDir a
  let n : Fin 3 → ℝ := ![a 1 ^ 2 + a 2 ^ 2, -(a 0 * a 1), -(a 0 * a 2)]
  let b : Fin 3 → ℝ := ![a 0, a 1 - t * a 2, a 2 + t * a 1]
  let b₂ : Fin 3 → ℝ := ![-(t * (a 1 ^ 2 + a 2 ^ 2)) * a 0,
    -(a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 2 - t * (a 1 ^ 2 + a 2 ^ 2) * a 1,
    (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * a 1 - t * (a 1 ^ 2 + a 2 ^ 2) * a 2]
  have hb : tangentStep a t = b := by rw [tangentStep_apply]
  have ha0 : a ≠ 0 := ne_zero_of_dot3_self_pos (by unfold dot3; nlinarith [sq_nonneg (a 0)])
  have hu0 : u ≠ 0 := ne_zero_of_dot3_self_pos (by simp only [dot3, u, tangentDir]; simp; nlinarith)
  have hn0 : n ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [n] using hr)
  have hb0 : b ≠ 0 := ne_zero_of_dot3_self_pos (by
    simp only [dot3, b]; simp
    nlinarith [sq_nonneg (a 0), mul_nonneg (sq_nonneg t) hr'.le])
  have hb₂0 : b₂ ≠ 0 := by
    intro h
    have h1 := congrFun h 1
    have h2 := congrFun h 2
    simp [b₂] at h1 h2
    have : (a 0 ^ 2 + a 1 ^ 2 + a 2 ^ 2) * (a 1 ^ 2 + a 2 ^ 2) = 0 := by
      linear_combination (-(a 2)) * h1 + a 1 * h2
    rcases mul_eq_zero.mp this with h3 | h3
    · nlinarith [sq_nonneg (a 0)]
    · exact hr h3
  have key := pair_sum_eq_of_common_normal hf.toIsFrameFunction ha0 hu0 hb0 hb₂0 hn0
    (by simp [dot3, u, tangentDir]; ring) (by simp [dot3, n]; ring)
    (by simp [dot3, u, tangentDir, n]; ring)
    (by simp [dot3, b, b₂]; ring) (by simp [dot3, b, n]; ring) (by simp [dot3, b₂, n]; ring)
  have hb₂_nn : 0 ≤ f b₂ := hf.nonneg b₂ hb₂0
  rw [hb]
  linarith

/-- General Piron tangent-step bound in terms of the pole deficit `W - f e1`: for any nonnegative
frame function, `f (tangentStep a t) - f a ≤ W - f e1`. -/
theorem tangentStep_sub_le_weight_sub_pole_of_nonneg {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) (a : Fin 3 → ℝ) (hr : a 1 ^ 2 + a 2 ^ 2 ≠ 0) (t : ℝ) :
    f (tangentStep a t) - f a ≤ W - f e1 := by
  have hstep := tangentStep_le_add_equator_of_nonneg hf a hr t
  have hr' : 0 < a 1 ^ 2 + a 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hr)
  have hu0 : tangentDir a ≠ 0 :=
    ne_zero_of_dot3_self_pos (by simp only [dot3, tangentDir]; simp; nlinarith)
  have heq : f (tangentDir a) ≤ W - f e1 :=
    ortho_le_weight_sub_of_nonneg hf e1_ne_zero hu0 (by simp [dot3, e1, tangentDir])
  linarith

/-- Continuity-free Lemma 1(iv) at the pole: if `f` has maximum at `e1` and is constant `m` on the
equator `{v 0 = 0}`, then `m ≤ f v` for every nonzero `v` (without assuming `ContinuousOn f`). -/
theorem equator_const_is_min_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → m ≤ f v := by
  intro v hv
  by_cases hrs : v 1 ^ 2 + v 2 ^ 2 = 0
  · have hv1 : v 1 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv2 : v 2 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv0 : v 0 ≠ 0 := by
      intro h0; apply hv; ext i; fin_cases i <;> simp [h0, hv1, hv2]
    have hve : v = (v 0) • e1 := by ext i; fin_cases i <;> simp [e1, hv1, hv2]
    have he2 : (![0, 1, 0] : Fin 3 → ℝ) ≠ 0 := ne_zero_of_apply_ne (i := 1) (by simp)
    have h1 := heq ![0, 1, 0] he2 (by simp)
    have h2 := hmax ![0, 1, 0] he2
    rw [hve, hf.scale e1 e1_ne_zero (v 0) hv0]
    linarith
  · let s' : Fin 3 → ℝ := ![0, v 1, v 2]
    let s'' : Fin 3 → ℝ := ![v 1 ^ 2 + v 2 ^ 2, -(v 0 * v 1), -(v 0 * v 2)]
    let n : Fin 3 → ℝ := ![0, -(v 2), v 1]
    have hs' : s' ≠ 0 := ne_zero_of_transverse_ne (by simpa [s'] using hrs)
    have hs'' : s'' ≠ 0 := ne_zero_of_apply_ne (i := 0) (by simpa [s''] using hrs)
    have hn : n ≠ 0 := ne_zero_of_transverse_ne (by simp [n]; intro h; apply hrs; linarith)
    have key := pair_sum_eq_of_common_normal hf e1_ne_zero hs' hv hs'' hn
      (by simp [dot3, e1, s']) (by simp [dot3, e1, n]) (by simp [dot3, s', n]; ring)
      (by simp [dot3, s'']; ring) (by simp [dot3, n]; ring) (by simp [dot3, s'', n]; ring)
    have h1 := heq s' hs' (by simp [s'])
    have h2 := hmax s'' hs''
    linarith

/-- Shared-normal frame construction for `x, y ≥ 0` with `0 < x + y ≤ 1`: in the plane spanned by
`q = refPt (x + y)` and `r = e3` (orthogonal to `w = ![√(1 - s), -√s, 0]`), the rotated pair
`u = √(x / s) • q + √(y / s) • r` and `v = √(y / s) • q - √(x / s) • r` is orthogonal, shares the
common normal `w` with `(refPt (x + y), e3)`, and has latitudes `lat u = x` and `lat v = y`. -/
theorem exists_common_normal_lat_add {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hs0 : 0 < x + y) (hs1 : x + y ≤ 1) :
    ∃ u v w : Fin 3 → ℝ, u ≠ 0 ∧ v ≠ 0 ∧ w ≠ 0 ∧
      dot3 (refPt (x + y)) e3 = 0 ∧ dot3 (refPt (x + y)) w = 0 ∧ dot3 e3 w = 0 ∧
      dot3 u v = 0 ∧ dot3 u w = 0 ∧ dot3 v w = 0 ∧
      lat u = x ∧ lat v = y := by
  set s := x + y with hs
  have hs_nonneg : 0 ≤ s := hs0.le
  have h1s_nonneg : 0 ≤ 1 - s := sub_nonneg.mpr hs1
  set a := Real.sqrt (x / s) with ha
  set b := Real.sqrt (y / s) with hb
  have ha2 : a ^ 2 = x / s := Real.sq_sqrt (div_nonneg hx hs_nonneg)
  have hb2 : b ^ 2 = y / s := Real.sq_sqrt (div_nonneg hy hs_nonneg)
  have hab : a ^ 2 + b ^ 2 = 1 := by
    rw [ha2, hb2, ← add_div, ← hs, div_self hs0.ne']
  let q : Fin 3 → ℝ := refPt s
  let w : Fin 3 → ℝ := ![Real.sqrt (1 - s), -Real.sqrt s, 0]
  let u : Fin 3 → ℝ := a • q + b • e3
  let v : Fin 3 → ℝ := b • q - a • e3
  have hqq : Real.sqrt s * Real.sqrt s + Real.sqrt (1 - s) * Real.sqrt (1 - s) = 1 := by
    have := refPt_dot3 hs_nonneg hs1
    simpa [dot3, refPt] using this
  have hww : dot3 w w = 1 := by
    simp [dot3, w, ← sq, Real.sq_sqrt hs_nonneg, Real.sq_sqrt h1s_nonneg]
  have huu : dot3 u u = 1 := by
    simp [u, q, refPt, e3, dot3]
    linear_combination a ^ 2 * hqq + hab
  have hvv : dot3 v v = 1 := by
    simp [v, q, refPt, e3, dot3]
    linear_combination b ^ 2 * hqq + hab
  have huv : dot3 u v = 0 := by
    simp [u, v, q, refPt, e3, dot3]
    linear_combination (a * b) * hqq
  have huw : dot3 u w = 0 := by
    simp [u, q, refPt, e3, w, dot3]; ring
  have hvw : dot3 v w = 0 := by
    simp [v, q, refPt, e3, w, dot3]; ring
  have hlu : lat u = x := by
    rw [lat, huu, div_one]
    have hu0 : u 0 = a * Real.sqrt s := by simp [u, q, refPt, e3]
    rw [hu0, mul_pow, ha2, Real.sq_sqrt hs_nonneg, div_mul_cancel₀ _ hs0.ne']
  have hlv : lat v = y := by
    rw [lat, hvv, div_one]
    have hv0 : v 0 = b * Real.sqrt s := by simp [v, q, refPt, e3]
    rw [hv0, mul_pow, hb2, Real.sq_sqrt hs_nonneg, div_mul_cancel₀ _ hs0.ne']
  refine ⟨u, v, w,
    ne_zero_of_dot3_self_pos (by rw [huu]; exact one_pos),
    ne_zero_of_dot3_self_pos (by rw [hvv]; exact one_pos),
    ne_zero_of_dot3_self_pos (by rw [hww]; exact one_pos),
    by simp [dot3, refPt, e3],
    by simp [dot3, refPt, w]; ring,
    by simp [dot3, e3, w],
    huv, huw, hvw, hlu, hlv⟩

/-- If `f` is constant `m` on the equator `{v 0 = 0}`, then for any `x, y ≥ 0` with `0 < x + y ≤ 1`
there exist nonzero vectors `u, v` with `lat u = x`, `lat v = y`, and
`(f u - m) + (f v - m) = f (refPt (x + y)) - m`. -/
theorem exists_lat_pair_sum_eq_refPt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (hs0 : 0 < x + y) (hs1 : x + y ≤ 1) :
    ∃ u v : Fin 3 → ℝ, u ≠ 0 ∧ v ≠ 0 ∧ lat u = x ∧ lat v = y ∧
      (f u - m) + (f v - m) = f (refPt (x + y)) - m := by
  obtain ⟨u, v, w, hu, hv, hw, hqe3, hqw, he3w, huv, huw, hvw, hlu, hlv⟩ :=
    exists_common_normal_lat_add hx hy hs0 hs1
  have hq : refPt (x + y) ≠ 0 := refPt_ne_zero hs0.le hs1
  have hsum := pair_sum_eq_of_common_normal hf hq e3_ne_zero hu hv hw hqe3 hqw he3w huv huw hvw
  have he3m : f e3 = m := heq e3 e3_ne_zero (by simp [e3])
  refine ⟨u, v, hu, hv, hlu, hlv, by linarith⟩

/-- Strict lower-latitude superadditivity of `l ↦ f (refPt l) - m` (without continuity). -/
lemma refPt_sub_add_le_of_lt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x' x y' y : ℝ} (hx' : 0 ≤ x') (hxx : x' < x) (hy' : 0 ≤ y') (hyy : y' < y)
    (hxy : x + y ≤ 1) :
    (f (refPt x') - m) + (f (refPt y') - m) ≤ f (refPt (x + y)) - m := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  obtain ⟨u, v, hu, hv, hlu, hlv, hsum⟩ :=
    exists_lat_pair_sum_eq_refPt hf heq (by linarith) (by linarith) (by linarith) hxy
  have hx1 : x' ≤ 1 := by linarith
  have hy1 : y' ≤ 1 := by linarith
  have hu_le : f (refPt x') ≤ f u :=
    le_of_lat_lt hf hmax heq hmin hu (refPt_ne_zero hx' hx1)
      (by rw [lat_refPt hx' hx1, hlu]; exact hxx)
  have hv_le : f (refPt y') ≤ f v :=
    le_of_lat_lt hf hmax heq hmin hv (refPt_ne_zero hy' hy1)
      (by rw [lat_refPt hy' hy1, hlv]; exact hyy)
  linarith

/-- Strict upper-latitude subadditivity of `l ↦ f (refPt l) - m` (without continuity). -/
lemma refPt_sub_le_add_of_lt {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {x x'' y y'' : ℝ} (hx : 0 < x) (hxx : x < x'') (hx1 : x'' ≤ 1)
    (hy : 0 < y) (hyy : y < y'') (hy1 : y'' ≤ 1) (hxy : x + y ≤ 1) :
    f (refPt (x + y)) - m ≤ (f (refPt x'') - m) + (f (refPt y'') - m) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  obtain ⟨u, v, hu, hv, hlu, hlv, hsum⟩ :=
    exists_lat_pair_sum_eq_refPt hf heq hx.le hy.le (by linarith) hxy
  have hx''0 : 0 ≤ x'' := by linarith
  have hy''0 : 0 ≤ y'' := by linarith
  have hu_le : f u ≤ f (refPt x'') :=
    le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hx''0 hx1) hu
      (by rw [lat_refPt hx''0 hx1, hlu]; exact hxx)
  have hv_le : f v ≤ f (refPt y'') :=
    le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hy''0 hy1) hv
      (by rw [lat_refPt hy''0 hy1, hlv]; exact hyy)
  linarith

/-- Iterated lower-latitude bound: for `k ≥ 1` and `0 ≤ a < b` with `k * b ≤ 1`,
`k * (f (refPt a) - m) ≤ f (refPt (k * b)) - m`. -/
lemma nat_mul_refPt_sub_le {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ k : ℕ, 0 < k → ∀ a b : ℝ, 0 ≤ a → a < b → (k : ℝ) * b ≤ 1 →
      (k : ℝ) * (f (refPt a) - m) ≤ f (refPt ((k : ℝ) * b)) - m := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  intro k
  induction k with
  | zero => intro hk; omega
  | succ k ih =>
    intro _ a b ha hab hkb
    by_cases hk0 : k = 0
    · subst hk0
      simp only [zero_add, Nat.cast_one, one_mul] at hkb ⊢
      have hb0 : 0 ≤ b := by linarith
      have ha1 : a ≤ 1 := by linarith
      have hle := le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hb0 hkb) (refPt_ne_zero ha ha1)
        (by rw [lat_refPt ha ha1, lat_refPt hb0 hkb]; exact hab)
      linarith
    · have hkpos : 0 < k := Nat.pos_of_ne_zero hk0
      have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hkpos
      set b' := (a + b) / 2 with hb'
      have hab' : a < b' := by linarith
      have hb'b : b' < b := by linarith
      have hb'0 : 0 ≤ b' := by linarith
      have hkb_split : (k : ℝ) * b + b = ((k + 1 : ℕ) : ℝ) * b := by push_cast; ring
      have hkb_le : (k : ℝ) * b' ≤ 1 := by
        have : (k : ℝ) * b' < (k : ℝ) * b := mul_lt_mul_of_pos_left hb'b hkR
        have : (k : ℝ) * b + b ≤ 1 := by linarith
        linarith
      have h1 := ih hkpos a b' ha hab' hkb_le
      have h2 := refPt_sub_add_le_of_lt hf hmax heq (mul_nonneg hkR.le hb'0)
        (mul_lt_mul_of_pos_left hb'b hkR) ha hab (by linarith)
      rw [hkb_split] at h2
      have hcast : ((k + 1 : ℕ) : ℝ) * (f (refPt a) - m) =
          (k : ℝ) * (f (refPt a) - m) + (f (refPt a) - m) := by push_cast; ring
      linarith

/-- Iterated upper-latitude bound: for `k ≥ 1` and `0 < a < b ≤ 1` with `k * a ≤ 1`,
`f (refPt (k * a)) - m ≤ k * (f (refPt b) - m)`. -/
lemma refPt_sub_le_nat_mul {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ k : ℕ, 0 < k → ∀ a b : ℝ, 0 < a → a < b → b ≤ 1 → (k : ℝ) * a ≤ 1 →
      f (refPt ((k : ℝ) * a)) - m ≤ (k : ℝ) * (f (refPt b) - m) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  intro k
  induction k with
  | zero => intro hk; omega
  | succ k ih =>
    intro _ a b ha hab hb1 hka
    by_cases hk0 : k = 0
    · subst hk0
      simp only [zero_add, Nat.cast_one, one_mul] at hka ⊢
      have hb0 : 0 ≤ b := by linarith
      have hle := le_of_lat_lt hf hmax heq hmin (refPt_ne_zero hb0 hb1) (refPt_ne_zero ha.le hka)
        (by rw [lat_refPt ha.le hka, lat_refPt hb0 hb1]; exact hab)
      linarith
    · have hkpos : 0 < k := Nat.pos_of_ne_zero hk0
      have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hkpos
      have hka_split : (k : ℝ) * a + a = ((k + 1 : ℕ) : ℝ) * a := by push_cast; ring
      have hka_lt1 : (k : ℝ) * a < 1 := by linarith
      have hkab : (k : ℝ) * a < (k : ℝ) * b := mul_lt_mul_of_pos_left hab hkR
      set M := min ((k : ℝ) * b) 1 with hM
      have hkaM : (k : ℝ) * a < M := lt_min hkab hka_lt1
      have hM1 : M ≤ 1 := min_le_right _ _
      have hMb : M ≤ (k : ℝ) * b := min_le_left _ _
      set x'' := ((k : ℝ) * a + M) / 2 with hx''
      have hx''_gt : (k : ℝ) * a < x'' := by linarith
      have hx''_lt : x'' < M := by linarith
      set a' := x'' / k with ha'
      have hka' : (k : ℝ) * a' = x'' := mul_div_cancel₀ x'' hkR.ne'
      have haa' : a < a' := by
        apply lt_of_mul_lt_mul_left _ hkR.le
        rw [hka']
        exact hx''_gt
      have ha'b : a' < b := by
        apply lt_of_mul_lt_mul_left _ hkR.le
        rw [hka']
        exact lt_of_lt_of_le hx''_lt hMb
      have h1 := ih hkpos a' b (by linarith) ha'b hb1 (by linarith)
      have hx''_gt' : (k : ℝ) * a < (k : ℝ) * a' := by rw [hka']; exact hx''_gt
      have hx''_le1 : (k : ℝ) * a' ≤ 1 := by linarith
      have h2 := refPt_sub_le_add_of_lt hf hmax heq (mul_pos hkR ha)
        hx''_gt' hx''_le1 ha hab hb1 (by linarith)
      rw [hka_split] at h2
      have hcast : ((k + 1 : ℕ) : ℝ) * (f (refPt b) - m) =
          (k : ℝ) * (f (refPt b) - m) + (f (refPt b) - m) := by push_cast; ring
      linarith

/-- Rational lower and upper bounds at any nonzero vector `w`: for `1 ≤ k ≤ n`,
if `k / n < lat w` then `(k / n) * (f e1 - m) ≤ f w - m`, and if `lat w < k / n` then
`f w - m ≤ (k / n) * (f e1 - m)` (without assuming `ContinuousOn f`). -/
lemma rat_mul_pole_sub_bounds_of_lat {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m)
    {n k : ℕ} (hn : 0 < n) (hk : 0 < k) (hkn : k ≤ n) {w : Fin 3 → ℝ} (hw : w ≠ 0) :
    ((k : ℝ) / n < lat w → (k : ℝ) / n * (f e1 - m) ≤ f w - m) ∧
    (lat w < (k : ℝ) / n → f w - m ≤ (k : ℝ) / n * (f e1 - m)) := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  have hnR : (0 : ℝ) < n := Nat.cast_pos.mpr hn
  have hkR : (0 : ℝ) < k := Nat.cast_pos.mpr hk
  have hknR : (k : ℝ) / n ≤ 1 := (div_le_one hnR).mpr (by exact_mod_cast hkn)
  have hxw0 : 0 ≤ lat w := lat_nonneg w
  have hxw1 : lat w ≤ 1 := lat_le_one hw
  constructor
  · intro hlt
    set b := ((k : ℝ) / n + lat w) / 2 with hb
    have hkb : (k : ℝ) / n < b := by linarith
    have hbw : b < lat w := by linarith
    have hb1 : b ≤ 1 := by linarith
    have hb_div : 1 / (n : ℝ) < b / k := by
      rw [div_lt_div_iff₀ hnR hkR]
      have : (k : ℝ) < b * n := (div_lt_iff₀ hnR).mp hkb
      linarith
    set a := (1 / (n : ℝ) + b / k) / 2 with ha
    have h1a : 1 / (n : ℝ) < a := by linarith
    have habk : a < b / k := by linarith
    have ha1 : a ≤ 1 := by
      have : b / k ≤ 1 := by
        rw [div_le_one hkR]
        have : (1 : ℝ) ≤ k := by exact_mod_cast hk
        linarith
      linarith
    have hlow1 : f e1 - m ≤ (n : ℝ) * (f (refPt a) - m) := by
      have := refPt_sub_le_nat_mul hf hmax heq n hn (1 / (n : ℝ)) a
        (div_pos one_pos hnR) h1a ha1 (by rw [mul_one_div_cancel hnR.ne'])
      rwa [mul_one_div_cancel hnR.ne', refPt_one] at this
    have hlow2 : (k : ℝ) * (f (refPt a) - m) ≤ f (refPt b) - m := by
      have := nat_mul_refPt_sub_le hf hmax heq k hk a (b / k) (by positivity) habk
        (by rw [mul_div_cancel₀ b hkR.ne']; exact hb1)
      rwa [mul_div_cancel₀ b hkR.ne'] at this
    have hlow3 : f (refPt b) ≤ f w :=
      le_of_lat_lt hf hmax heq hmin hw (refPt_ne_zero (by positivity) hb1)
        (by rw [lat_refPt (by positivity) hb1]; exact hbw)
    have hlow1' : (f e1 - m) / n ≤ f (refPt a) - m := (div_le_iff₀ hnR).mpr (by linarith)
    have hlow2' : (k : ℝ) * ((f e1 - m) / n) ≤ (k : ℝ) * (f (refPt a) - m) :=
      mul_le_mul_of_nonneg_left hlow1' hkR.le
    have h_eq : (k : ℝ) / n * (f e1 - m) = (k : ℝ) * ((f e1 - m) / n) := by ring
    linarith
  · intro hlt
    set a := (lat w + (k : ℝ) / n) / 2 with ha
    have hwa : lat w < a := by linarith
    have hak : a < (k : ℝ) / n := by linarith
    have ha0 : 0 < a := by positivity
    have ha1 : a ≤ 1 := by linarith
    have ha_div : a / k < 1 / (n : ℝ) := by
      rw [div_lt_div_iff₀ hkR hnR]
      have : a * n < (k : ℝ) := (lt_div_iff₀ hnR).mp hak
      linarith
    set b := (a / k + 1 / (n : ℝ)) / 2 with hb
    have hab : a / k < b := by linarith
    have hb1n : b < 1 / (n : ℝ) := by linarith
    have hb1 : b ≤ 1 := by
      have : 1 / (n : ℝ) ≤ 1 := div_le_one_of_le₀ (by exact_mod_cast hn) hnR.le
      linarith
    have hup1 : f w ≤ f (refPt a) :=
      le_of_lat_lt hf hmax heq hmin (refPt_ne_zero ha0.le ha1) hw
        (by rw [lat_refPt ha0.le ha1]; exact hwa)
    have hup2 : f (refPt a) - m ≤ (k : ℝ) * (f (refPt b) - m) := by
      have := refPt_sub_le_nat_mul hf hmax heq k hk (a / k) b (div_pos ha0 hkR) hab hb1
        (by rw [mul_div_cancel₀ a hkR.ne']; exact ha1)
      rwa [mul_div_cancel₀ a hkR.ne'] at this
    have hup3 : (n : ℝ) * (f (refPt b) - m) ≤ f e1 - m := by
      have := nat_mul_refPt_sub_le hf hmax heq n hn b (1 / (n : ℝ)) (by positivity) hb1n
        (by rw [mul_one_div_cancel hnR.ne'])
      rwa [mul_one_div_cancel hnR.ne', refPt_one] at this
    have hup3' : f (refPt b) - m ≤ (f e1 - m) / n := (le_div_iff₀ hnR).mpr (by linarith)
    have hup2' : (k : ℝ) * (f (refPt b) - m) ≤ (k : ℝ) * ((f e1 - m) / n) :=
      mul_le_mul_of_nonneg_left hup3' hkR.le
    have h_eq : (k : ℝ) / n * (f e1 - m) = (k : ℝ) * ((f e1 - m) / n) := by ring
    linarith

/-- **Continuity-free Proposition 1 at the pole.**  Every frame function on `ℝ³ \ {0}` with its
maximum at `e1` and constant `m` on the equator `{v 0 = 0}` equals `m + (f e1 - m) * lat v` on
all nonzero vectors, with zero continuity assumption on `f`. -/
theorem prop1_pole_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f e1 - m) * lat v := by
  have hmin := equator_const_is_min_of_max hf hmax heq
  have hM : 0 ≤ f e1 - m := by linarith [hmin e1 e1_ne_zero]
  intro v hv
  by_cases hv0 : v 0 = 0
  · have hlat0 : lat v = 0 := by simp [lat, hv0]
    rw [heq v hv hv0, hlat0]; ring
  by_cases hrv : v 1 ^ 2 + v 2 ^ 2 = 0
  · have hv1 : v 1 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hv2 : v 2 = 0 := by nlinarith [sq_nonneg (v 1), sq_nonneg (v 2)]
    have hve : v = (v 0) • e1 := by ext i; fin_cases i <;> simp [e1, hv1, hv2]
    rw [hve, hf.scale e1 e1_ne_zero (v 0) hv0, lat_smul e1 hv0, lat_e1]; ring
  -- Generic case: `0 < lat v < 1`, sandwiched by rationals `(k ± 1) / n`
  set x := lat v with hx
  have hx0 : 0 < x := div_pos (sq_pos_of_ne_zero hv0) (dot3_self_pos hv)
  have hx1 : x < 1 := by
    rw [hx, lat, div_lt_one (dot3_self_pos hv)]
    unfold dot3
    have : 0 < v 1 ^ 2 + v 2 ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hrv)
    nlinarith
  have hbound : ∀ n : ℕ, 0 < n → |(f v - m) - x * (f e1 - m)| ≤ 2 * (f e1 - m) / n := by
    intro n hn
    have hnR : (0 : ℝ) < n := Nat.cast_pos.mpr hn
    set k := ⌊(n : ℝ) * x⌋₊ with hk
    have hk0 : (k : ℝ) ≤ (n : ℝ) * x := Nat.floor_le (by positivity)
    have hk1 : (n : ℝ) * x < (k : ℝ) + 1 := Nat.lt_floor_add_one _
    have hlow : x * (f e1 - m) - (f v - m) ≤ 2 * (f e1 - m) / n := by
      by_cases hk_pos : 0 < k
      · by_cases hk1_pos : 0 < k - 1
        · have hkn1 : k - 1 ≤ n := by
            have : (k : ℝ) ≤ n := le_trans hk0 (by nlinarith)
            have hk_le : k ≤ n := by exact_mod_cast this
            omega
          have hk_sub : ((k - 1 : ℕ) : ℝ) + 1 = (k : ℝ) := by
            exact_mod_cast Nat.sub_add_cancel hk_pos
          have hlt : ((k - 1 : ℕ) : ℝ) / n < x := by
            rw [div_lt_iff₀ hnR]
            linarith
          have hb := (rat_mul_pole_sub_bounds_of_lat hf hmax heq hn hk1_pos hkn1 hv).1 hlt
          have hsub : x - ((k - 1 : ℕ) : ℝ) / n ≤ 2 / n := by
            have heq_sub : x - ((k - 1 : ℕ) : ℝ) / n = (x * n - ((k - 1 : ℕ) : ℝ)) / n := by
              field_simp
            rw [heq_sub, div_le_div_iff_of_pos_right hnR]
            linarith
          have hmul : (x - ((k - 1 : ℕ) : ℝ) / n) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
            mul_le_mul_of_nonneg_right hsub hM
          have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
          linarith
        · have hk_le1 : k ≤ 1 := by omega
          have hnx : (n : ℝ) * x < 2 := by
            have : (k : ℝ) ≤ 1 := by exact_mod_cast hk_le1
            linarith
          have hx_le : x ≤ 2 / n := (le_div_iff₀ hnR).mpr (by linarith)
          have hmul : x * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
            mul_le_mul_of_nonneg_right hx_le hM
          have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
          have hfv : 0 ≤ f v - m := by linarith [hmin v hv]
          linarith
      · have hk_eq0 : k = 0 := by omega
        have hnx : (n : ℝ) * x < 1 := by rw [hk_eq0] at hk1; simpa using hk1
        have hx_le : x ≤ 2 / n := (le_div_iff₀ hnR).mpr (by linarith)
        have hmul : x * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right hx_le hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        have hfv : 0 ≤ f v - m := by linarith [hmin v hv]
        linarith
    have hup : (f v - m) - x * (f e1 - m) ≤ 2 * (f e1 - m) / n := by
      by_cases hkn2 : k + 2 ≤ n
      · have hk_add : ((k + 2 : ℕ) : ℝ) = (k : ℝ) + 2 := by push_cast; ring
        have hlt : x < ((k + 2 : ℕ) : ℝ) / n := by
          rw [lt_div_iff₀ hnR]
          linarith
        have hb := (rat_mul_pole_sub_bounds_of_lat hf hmax heq hn (by omega) hkn2 hv).2 hlt
        have hsub : ((k + 2 : ℕ) : ℝ) / n - x ≤ 2 / n := by
          have heq_sub : ((k + 2 : ℕ) : ℝ) / n - x = (((k + 2 : ℕ) : ℝ) - x * n) / n := by
            field_simp
          rw [heq_sub, div_le_div_iff_of_pos_right hnR]
          linarith
        have hmul : (((k + 2 : ℕ) : ℝ) / n - x) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right hsub hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        linarith
      · have hn_le : n ≤ k + 1 := by omega
        have hnR_le : (n : ℝ) ≤ (k : ℝ) + 1 := by exact_mod_cast hn_le
        have h1x : 1 - x ≤ 2 / n := by
          rw [le_div_iff₀ hnR]
          linarith
        have hmul : (1 - x) * (f e1 - m) ≤ (2 / n) * (f e1 - m) :=
          mul_le_mul_of_nonneg_right h1x hM
        have heq_rhs : (2 / (n : ℝ)) * (f e1 - m) = 2 * (f e1 - m) / n := by ring
        have hfv : f v ≤ f e1 := hmax v hv
        linarith
    rw [abs_le]
    exact ⟨by linarith, hup⟩
  suffices h0 : (f v - m) - x * (f e1 - m) = 0 by linarith
  by_contra hne
  have hpos : 0 < |(f v - m) - x * (f e1 - m)| := abs_pos.mpr hne
  obtain ⟨n, hn⟩ := exists_nat_gt (2 * (f e1 - m) / |(f v - m) - x * (f e1 - m)|)
  have hn0 : 0 < n := by
    have : (0 : ℝ) ≤ 2 * (f e1 - m) / |(f v - m) - x * (f e1 - m)| :=
      div_nonneg (by linarith) hpos.le
    exact_mod_cast lt_of_le_of_lt this hn
  have hn' : (0 : ℝ) < n := Nat.cast_pos.mpr hn0
  have h1 := hbound n hn0
  rw [div_lt_iff₀ hpos] at hn
  rw [le_div_iff₀ hn'] at h1
  linarith

/-- Automatic continuity of any frame function on `ℝ³ \ {0}` that has its maximum at `e1` and is
constant on the equator `{v 0 = 0}`. -/
theorem continuousOn_of_max_and_equator_const {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ}
    (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → f v = m) :
    ContinuousOn f {v | v ≠ 0} := by
  refine (continuousOn_stdQuad (f e1) m m).congr fun v hv => ?_
  have hp := prop1_pole_of_max hf hmax heq v hv
  have hD : dot3 v v ≠ 0 := (dot3_self_pos hv).ne'
  rw [hp, stdQuad, lat]
  field_simp [hD]
  unfold dot3
  ring

/-- **Continuity-free Proposition 1 at an arbitrary unit pole `p`.**  Every frame function on
`ℝ³ \ {0}` with its maximum at a unit vector `p` and constant `m` on `p⊥` is
`m + (f p - m) * (⟨v, p⟩² / ⟨v, v⟩)`, without assuming continuity of `f`. -/
theorem prop1_of_max {f : (Fin 3 → ℝ) → ℝ} {W m : ℝ} (hf : IsFrameFunction f W)
    {p : Fin 3 → ℝ} (hp : dot3 p p = 1)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p)
    (heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v p = 0 → f v = m) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = m + (f p - m) * (dot3 v p ^ 2 / dot3 v v) := by
  obtain ⟨q, r, h⟩ := exists_orthonormal_completion hp
  have hF := hf.comp_ofFrame h
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f (ofFrame p q r v)) v ≤ (fun v => f (ofFrame p q r v)) e1 := by
    intro v hv
    simp only [ofFrame_e1]
    exact hmax _ (ofFrame_ne_zero h hv)
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 → (fun v => f (ofFrame p q r v)) v = m := by
    intro v hv hv0
    exact heq _ (ofFrame_ne_zero h hv) (by rw [(dot3_ofFrame_left h v).1]; exact hv0)
  have key := prop1_pole_of_max hF hmaxF heqF
  intro w hw
  have := key (toFrame p q r w) (toFrame_ne_zero h hw)
  simp only [ofFrame_e1, ofFrame_toFrame h] at this
  rw [this, lat, dot3_toFrame_self h]
  simp [toFrame]

/-- Continuity-free (4.5): with the maximum at `e1`, `f + f ∘ phat` is an explicit function of
`lat v` without assuming continuity of `f`. -/
theorem sum_phat_of_max {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (phat v) = (W - f e1) + (3 * f e1 - W) * lat v := by
  have hF : IsFrameFunction (fun v => f v + f (phat v)) (W + W) := hf.add hf.comp_phat
  have hmaxF : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => f v + f (phat v)) v ≤ (fun v => f v + f (phat v)) e1 := by
    intro v hv; simp only [phat_e1]
    linarith [hmax v hv, hmax (phat v) (phat_ne_zero hv)]
  have heqF : ∀ v : Fin 3 → ℝ, v ≠ 0 → v 0 = 0 →
      (fun v => f v + f (phat v)) v = W - f e1 := by
    intro v hv hv0
    have := hf.frame e1 v (phat v) e1_ne_zero hv (phat_ne_zero hv)
      (by simp [dot3, e1, hv0]) (by simp [dot3, e1, phat, hv0]) (by simp [dot3, phat, hv0]; ring)
    show f v + f (phat v) = W - f e1
    linarith
  have key := prop1_pole_of_max hF hmaxF heqF
  intro v hv
  have := key v hv
  simp only [phat_e1] at this
  rw [this]; ring

/-- Continuity-free (4.6): with the minimum at `e3`, `f + f ∘ rhat` is an explicit function of
`v 2 ^ 2 / ⟨v, v⟩` without assuming continuity of `f`. -/
theorem sum_rhat_of_min {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      f v + f (rhat v) = (W - f e3) + (3 * f e3 - W) * (v 2 ^ 2 / dot3 v v) := by
  have hG : IsFrameFunction (fun v => -(f v + f (rhat v))) (-(W + W)) := (hf.add hf.comp_rhat).neg
  have hmaxG : ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (fun v => -(f v + f (rhat v))) v ≤ (fun v => -(f v + f (rhat v))) e3 := by
    intro v hv; simp only [rhat_e3]
    linarith [hmin v hv, hmin (rhat v) (rhat_ne_zero hv)]
  have heqG : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v e3 = 0 →
      (fun v => -(f v + f (rhat v))) v = -(W - f e3) := by
    intro v hv hv2
    have hv2' : v 2 = 0 := by simpa [dot3, e3] using hv2
    have := hf.frame e3 v (rhat v) e3_ne_zero hv (rhat_ne_zero hv)
      (by simp [dot3, e3, hv2']) (by simp [dot3, e3, rhat, hv2']) (by simp [dot3, rhat, hv2']; ring)
    show -(f v + f (rhat v)) = -(W - f e3)
    linarith
  have key := prop1_of_max hG dot3_e3_self hmaxG heqG
  intro v hv
  have := key v hv
  simp only [rhat_e3] at this
  have e : dot3 v e3 = v 2 := by simp [dot3, e3]
  rw [e] at this
  linarith

/-- Continuity-free Lemma 8 (standard position): with the maximum at `e1` and the minimum at `e3`,
`f` agrees with `stdQuad (f e1) (W - f e1 - f e3) (f e3)` on the six great circles
`x = ±y`, `x = ±z`, `y = ±z` without assuming continuity of `f`. -/
theorem eq_stdQuad_on_six_circles_of_extrema {f : (Fin 3 → ℝ) → ℝ} {W : ℝ} (hf : IsFrameFunction f W)
    (hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f e1)
    (hmin : ∀ v : Fin 3 → ℝ, v ≠ 0 → f e3 ≤ f v) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 →
      (v 0 = v 1 ∨ v 0 = -v 1 ∨ v 0 = v 2 ∨ v 0 = -v 2 ∨ v 1 = v 2 ∨ v 1 = -v 2) →
      f v = stdQuad (f e1) (W - f e1 - f e3) (f e3) v := by
  set M := f e1 with hM
  set m := f e3 with hm
  set α := W - M - m with hα
  set g := stdQuad M α m with hg
  set h : (Fin 3 → ℝ) → ℝ := fun v => f v - g v with hh
  have hhf : IsFrameFunction h 0 := by
    have := hf.sub (isFrameFunction_stdQuad M α m)
    rwa [show W - (M + α + m) = 0 by rw [hα]; ring] at this
  have hp : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (phat v) = -h v := by
    intro v hv
    have h1 := sum_phat_of_max hf hmax v hv
    have h2 := stdQuad_add_phat M α m hv
    simp only [hh, hg]
    rw [← hM] at h1
    linarith
  have hr : ∀ v : Fin 3 → ℝ, v ≠ 0 → h (rhat v) = -h v := by
    intro v hv
    have h1 := sum_rhat_of_min hf hmin v hv
    have h2 := stdQuad_add_rhat M α m hv
    simp only [hh, hg]
    rw [← hm] at h1
    linarith
  have hneg : ∀ v : Fin 3 → ℝ, v ≠ 0 → h ((-1 : ℝ) • v) = h v :=
    fun v hv => hhf.scale v hv (-1) (by norm_num)
  intro v hv hcirc
  suffices hz : h v = 0 by simp only [hh, hg] at hz; linarith
  rcases hcirc with h01 | h01 | h02 | h02 | h12 | h12
  · have e : phat (phat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hp _ (phat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : rhat (phat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h01]
    have := hr _ (phat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hp _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · have e : rhat (phat (phat (phat (rhat v)))) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hr _ (phat_ne_zero (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))))
    rw [e, hneg v hv, hp _ (phat_ne_zero (phat_ne_zero (rhat_ne_zero hv))),
      hp _ (phat_ne_zero (rhat_ne_zero hv)), hp _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : phat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h02]
    have := hp _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith
  · have e : phat (rhat (rhat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hp _ (rhat_ne_zero (rhat_ne_zero hv))
    rw [e, hneg v hv, hr _ (rhat_ne_zero hv), hr v hv] at this
    linarith
  · have e : rhat (rhat (phat v)) = (-1 : ℝ) • v := by
      ext i; fin_cases i <;> simp [phat, rhat, h12]
    have := hr _ (rhat_ne_zero (phat_ne_zero hv))
    rw [e, hneg v hv, hr _ (phat_ne_zero hv), hp v hv] at this
    linarith

/-- **Pure-state continuity-free Gleason theorem on `ℝ³`.**  If a nonnegative frame function `f`
of weight `W` attains `W` at a unit vector `p`, then `f v = W * (⟨v, p⟩² / ⟨v, v⟩)` for every
nonzero `v ∈ ℝ³ \ {0}`, without assuming continuity of `f`. -/
theorem pure_state_nonneg_gleason_real {f : (Fin 3 → ℝ) → ℝ} {W : ℝ}
    (hf : IsNonnegFrameFunction f W) {p : Fin 3 → ℝ} (hp : dot3 p p = 1) (hpW : f p = W) :
    ∀ v : Fin 3 → ℝ, v ≠ 0 → f v = W * (dot3 v p ^ 2 / dot3 v v) := by
  have hp0 : p ≠ 0 := ne_zero_of_dot3_self_pos (by rw [hp]; exact one_pos)
  have hmax : ∀ v : Fin 3 → ℝ, v ≠ 0 → f v ≤ f p := by
    intro v hv
    rw [hpW]
    exact le_weight_of_nonneg hf hv
  have heq : ∀ v : Fin 3 → ℝ, v ≠ 0 → dot3 v p = 0 → f v = 0 :=
    fun v hv hvp => eq_zero_on_perp_of_pole_eq_weight hf hp0 hpW hv hvp
  intro v hv
  have := prop1_of_max hf.toIsFrameFunction hp hmax heq v hv
  rw [this, hpW]
  ring

end GleasonReal
