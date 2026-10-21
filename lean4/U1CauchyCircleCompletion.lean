import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Rat.Floor

/-!
# U(1) Cauchy & Algebraic Circle Completion (`FQ-GAP-U1-CIRCLE`)

This module mechanizes the resolution of the rational circle phase-halving obstruction
and the precompactness / Cauchy completion of the circle group:

1. **Algebraic Half-Angle Restoration in $\mathbb{Q}(\sqrt{5})(i)$ (`QuadSqrt5`)**:
   While the rational circle $S^1(\mathbb{Q})$ lacks a square root for the Pythagorean
   generator $u_{3,4,5} = (3/5, 4/5)$ (because $\sqrt{(1 + 3/5)/2} = 2/\sqrt{5} \notin \mathbb{Q}$),
   adjoining $\sqrt{5}$ in the quadratic extension `QuadSqrt5` ($\mathbb{Q}(\sqrt{5})$)
   restores the exact half-angle point
   $$w_{\mathrm{half}} = \left(\frac{2}{5}\sqrt{5},\, \frac{1}{5}\sqrt{5}\right) \in S^1(\mathbb{Q}(\sqrt{5})),$$
   satisfying $w_{\mathrm{half}}^2 = u_{3,4,5}$ with non-zero irrational $\sqrt{5}$-components.

2. **Nested Dyadic & Regular Cauchy Phase Completion (`NestedPhaseInterval`, `RegPhaseSeq`)**:
   Repeated phase bisection generates nested rational intervals $[a_n, b_n]$ with
   $b_n - a_n = 2^{-n}$ whose endpoints form Cauchy sequences (`nested_dyadic_cauchy`),
   completed by the metric space of regular Cauchy sequences `RegPhaseSeq` in $\mathbb{Q}$
   with rate $|x_m - x_n| \le \frac{1}{m+1} + \frac{1}{n+1}$.

3. **Precompactness / Total Boundedness by Finite $N$-Torsion Grids**:
   For every rational phase $q \in [0, 1]$ and every grid resolution $N \ge 1$,
   there exists a torsion index $k \in \{0, \dots, N\}$ such that $|q - k/N| \le 1/N$
   (`finite_torsion_grid_covers_unit_interval`). This establishes total boundedness of the
   unit phase interval by finite $N$-torsion grids $\mu_N$; combined with Cauchy completeness
   (`RegPhaseSeq`), total boundedness yields the compact circle group $\mathbb{R}/\mathbb{Z} \cong U(1)$.
-/

namespace U1Fable.CauchyCircleCompletion

/-! ## Section 1: Algebraic Half-Angle Restoration in $\mathbb{Q}(\sqrt{5})(i)$ -/

/-- Elements of the real quadratic field extension $\mathbb{Q}(\sqrt{5})$, represented as $a + b\sqrt{5}$. -/
@[ext]
structure QuadSqrt5 where
  a : ℚ
  b : ℚ
  deriving DecidableEq, Repr

namespace QuadSqrt5

/-- Zero element $0 + 0\sqrt{5}$. -/
def zero : QuadSqrt5 := ⟨0, 0⟩

/-- Unit element $1 + 0\sqrt{5}$. -/
def one : QuadSqrt5 := ⟨1, 0⟩

/-- Canonical embedding $\mathbb{Q} \hookrightarrow \mathbb{Q}(\sqrt{5})$. -/
def ofRat (q : ℚ) : QuadSqrt5 := ⟨q, 0⟩

/-- The quadratic generator $\sqrt{5} = 0 + 1\sqrt{5}$. -/
def sqrt5 : QuadSqrt5 := ⟨0, 1⟩

/-- Addition in $\mathbb{Q}(\sqrt{5})$. -/
def add (x y : QuadSqrt5) : QuadSqrt5 := ⟨x.a + y.a, x.b + y.b⟩

/-- Subtraction in $\mathbb{Q}(\sqrt{5})$. -/
def sub (x y : QuadSqrt5) : QuadSqrt5 := ⟨x.a - y.a, x.b - y.b⟩

/-- Negation in $\mathbb{Q}(\sqrt{5})$. -/
def neg (x : QuadSqrt5) : QuadSqrt5 := ⟨-x.a, -x.b⟩

/-- Multiplication in $\mathbb{Q}(\sqrt{5})$: $(a_1 + b_1\sqrt{5})(a_2 + b_2\sqrt{5}) = (a_1 a_2 + 5 b_1 b_2) + (a_1 b_2 + b_1 a_2)\sqrt{5}$. -/
def mul (x y : QuadSqrt5) : QuadSqrt5 :=
  ⟨x.a * y.a + 5 * x.b * y.b, x.a * y.b + x.b * y.a⟩

instance : Zero QuadSqrt5 := ⟨zero⟩
instance : One QuadSqrt5 := ⟨one⟩
instance : Add QuadSqrt5 := ⟨add⟩
instance : Sub QuadSqrt5 := ⟨sub⟩
instance : Neg QuadSqrt5 := ⟨neg⟩
instance : Mul QuadSqrt5 := ⟨mul⟩

@[simp] theorem zero_a : (0 : QuadSqrt5).a = 0 := rfl
@[simp] theorem zero_b : (0 : QuadSqrt5).b = 0 := rfl
@[simp] theorem one_a : (1 : QuadSqrt5).a = 1 := rfl
@[simp] theorem one_b : (1 : QuadSqrt5).b = 0 := rfl
@[simp] theorem add_a (x y : QuadSqrt5) : (x + y).a = x.a + y.a := rfl
@[simp] theorem add_b (x y : QuadSqrt5) : (x + y).b = x.b + y.b := rfl
@[simp] theorem sub_a (x y : QuadSqrt5) : (x - y).a = x.a - y.a := rfl
@[simp] theorem sub_b (x y : QuadSqrt5) : (x - y).b = x.b - y.b := rfl
@[simp] theorem neg_a (x : QuadSqrt5) : (-x).a = -x.a := rfl
@[simp] theorem neg_b (x : QuadSqrt5) : (-x).b = -x.b := rfl
@[simp] theorem mul_a (x y : QuadSqrt5) : (x * y).a = x.a * y.a + 5 * x.b * y.b := rfl
@[simp] theorem mul_b (x y : QuadSqrt5) : (x * y).b = x.a * y.b + x.b * y.a := rfl

theorem add_assoc (x y z : QuadSqrt5) : x + y + z = x + (y + z) := by
  ext <;> simp <;> ring

theorem add_comm (x y : QuadSqrt5) : x + y = y + x := by
  ext <;> simp <;> ring

theorem zero_add (x : QuadSqrt5) : 0 + x = x := by
  ext <;> simp

theorem add_zero (x : QuadSqrt5) : x + 0 = x := by
  ext <;> simp

theorem neg_add_cancel (x : QuadSqrt5) : -x + x = 0 := by
  ext <;> simp

theorem mul_assoc (x y z : QuadSqrt5) : x * y * z = x * (y * z) := by
  ext <;> simp <;> ring

theorem mul_comm (x y : QuadSqrt5) : x * y = y * x := by
  ext <;> simp <;> ring

theorem one_mul (x : QuadSqrt5) : 1 * x = x := by
  ext <;> simp

theorem mul_one (x : QuadSqrt5) : x * 1 = x := by
  ext <;> simp

theorem left_distrib (x y z : QuadSqrt5) : x * (y + z) = x * y + x * z := by
  ext <;> simp <;> ring

theorem right_distrib (x y z : QuadSqrt5) : (x + y) * z = x * z + y * z := by
  ext <;> simp <;> ring

/-- $(\sqrt{5})^2 = 5$ in $\mathbb{Q}(\sqrt{5})$. -/
theorem sqrt5_sq : sqrt5 * sqrt5 = ofRat 5 := by
  ext <;> simp [sqrt5, ofRat]

/-- Brahmagupta-Fibonacci identity in $\mathbb{Q}(\sqrt{5})$. -/
theorem norm_sq_mul (zr zi wr wi : QuadSqrt5) :
    (zr * wr - zi * wi) * (zr * wr - zi * wi) + (zr * wi + zi * wr) * (zr * wi + zi * wr) =
    (zr * zr + zi * zi) * (wr * wr + wi * wi) := by
  ext <;> simp <;> ring

end QuadSqrt5

/-- Points on the algebraic unit circle over $\mathbb{Q}(\sqrt{5})$, i.e., $\mathrm{re}^2 + \mathrm{im}^2 = 1$. -/
@[ext]
structure CircleQuadSqrt5 where
  re : QuadSqrt5
  im : QuadSqrt5
  unit : re * re + im * im = QuadSqrt5.one
  deriving DecidableEq, Repr

namespace CircleQuadSqrt5

/-- Complex group multiplication on $S^1(\mathbb{Q}(\sqrt{5}))$. -/
def mul (z w : CircleQuadSqrt5) : CircleQuadSqrt5 where
  re := z.re * w.re - z.im * w.im
  im := z.re * w.im + z.im * w.re
  unit := by
    change (z.re * w.re - z.im * w.im) * (z.re * w.re - z.im * w.im) +
      (z.re * w.im + z.im * w.re) * (z.re * w.im + z.im * w.re) = (1 : QuadSqrt5)
    rw [QuadSqrt5.norm_sq_mul, z.unit, w.unit]
    exact QuadSqrt5.one_mul 1

/-- Identity element $(1, 0)$ of $S^1(\mathbb{Q}(\sqrt{5}))$. -/
def one : CircleQuadSqrt5 where
  re := QuadSqrt5.one
  im := QuadSqrt5.zero
  unit := by
    ext <;> simp [QuadSqrt5.one, QuadSqrt5.zero]

/-- Complex conjugation / inverse $(x, -y)$ on $S^1(\mathbb{Q}(\sqrt{5}))$. -/
def inv (z : CircleQuadSqrt5) : CircleQuadSqrt5 where
  re := z.re
  im := -z.im
  unit := by
    have h := z.unit
    ext
    · have ha := congrArg QuadSqrt5.a h
      simp at ha ⊢
      linarith
    · have hb := congrArg QuadSqrt5.b h
      simp at hb ⊢
      linarith

end CircleQuadSqrt5

/-- The canonical Pythagorean rational circle point $u_{3,4,5} = (3/5, 4/5)$ embedded in $S^1(\mathbb{Q}(\sqrt{5}))$. -/
def u345Quad : CircleQuadSqrt5 where
  re := QuadSqrt5.ofRat (3 / 5)
  im := QuadSqrt5.ofRat (4 / 5)
  unit := by
    ext
    · simp [QuadSqrt5.ofRat, QuadSqrt5.one]
      norm_num
    · simp [QuadSqrt5.ofRat, QuadSqrt5.one]

/-- The exact algebraic half-angle circle point $w_{\mathrm{half}} = (\frac{2}{5}\sqrt{5}, \frac{1}{5}\sqrt{5}) \in S^1(\mathbb{Q}(\sqrt{5}))$. -/
def wHalf : CircleQuadSqrt5 where
  re := ⟨0, 2 / 5⟩
  im := ⟨0, 1 / 5⟩
  unit := by
    ext
    · simp [QuadSqrt5.one]
      norm_num
    · simp [QuadSqrt5.one]

/-- Squaring $w_{\mathrm{half}}$ in $S^1(\mathbb{Q}(\sqrt{5}))$ recovers $u_{3,4,5} = (3/5, 4/5)$. -/
theorem wHalf_sq_eq_u345 : CircleQuadSqrt5.mul wHalf wHalf = u345Quad := by
  ext <;> simp [CircleQuadSqrt5.mul, wHalf, u345Quad, QuadSqrt5.ofRat] <;> norm_num

/-- $w_{\mathrm{half}}$ lies strictly outside the rational sub-circle $S^1(\mathbb{Q})$ because both $\sqrt{5}$-components are non-zero. -/
theorem wHalf_not_rational : wHalf.re.b ≠ 0 ∧ wHalf.im.b ≠ 0 := by
  simp [wHalf]

/-! ## Section 2: Nested Dyadic & Regular Cauchy Phase Completion -/

/-- A sequence of nested rational phase intervals $[a_n, b_n]$ with $a_n \le a_{n+1} \le b_{n+1} \le b_n$. -/
structure NestedPhaseInterval where
  lo : ℕ → ℚ
  hi : ℕ → ℚ
  lo_le_hi : ∀ n, lo n ≤ hi n
  lo_mono : ∀ n, lo n ≤ lo (n + 1)
  hi_anti : ∀ n, hi (n + 1) ≤ hi n

/-- Monotonicity of lower endpoints by additive offset. -/
theorem nested_lo_mono_add (I : NestedPhaseInterval) (m k : ℕ) :
    I.lo m ≤ I.lo (m + k) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [← Nat.add_assoc]
    exact le_trans ih (I.lo_mono (m + k))

/-- Antitonicity of upper endpoints by additive offset. -/
theorem nested_hi_anti_add (I : NestedPhaseInterval) (m k : ℕ) :
    I.hi (m + k) ≤ I.hi m := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [← Nat.add_assoc]
    exact le_trans (I.hi_anti (m + k)) ih

/-- For $m \le n$, the nested interval $[a_n, b_n]$ is contained inside $[a_m, b_m]$. -/
theorem nested_lo_le_hi_of_le (I : NestedPhaseInterval) {m n : ℕ} (h : m ≤ n) :
    I.lo m ≤ I.lo n ∧ I.hi n ≤ I.hi m := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le h
  exact ⟨nested_lo_mono_add I m k, nested_hi_anti_add I m k⟩

/-- Every lower endpoint $a_m$ is bounded above by every upper endpoint $b_n$. -/
theorem nested_cross_le (I : NestedPhaseInterval) (m n : ℕ) :
    I.lo m ≤ I.hi n := by
  have hm : m ≤ m + n := Nat.le_add_right m n
  have hn : n ≤ m + n := Nat.le_add_left n m
  have h1 := (nested_lo_le_hi_of_le I hm).1
  have h2 := I.lo_le_hi (m + n)
  have h3 := (nested_lo_le_hi_of_le I hn).2
  linarith

/-- Dyadic bisection intervals of width $2^{-n}$ have Cauchy lower endpoints with rate $2^{-\min(m, n)}$. -/
theorem nested_dyadic_cauchy (I : NestedPhaseInterval)
    (h_width : ∀ k, I.hi k - I.lo k = 1 / (2 : ℚ) ^ k) (m n : ℕ) :
    |I.lo n - I.lo m| ≤ 1 / (2 : ℚ) ^ min m n := by
  rcases le_total m n with hmn | hnm
  · rw [Nat.min_eq_left hmn]
    have hlo : I.lo m ≤ I.lo n := (nested_lo_le_hi_of_le I hmn).1
    have hhi : I.lo n ≤ I.hi m := nested_cross_le I n m
    have hw : I.hi m - I.lo m = 1 / (2 : ℚ) ^ m := h_width m
    rw [abs_le]
    constructor <;> linarith
  · rw [Nat.min_eq_right hnm]
    have hlo : I.lo n ≤ I.lo m := (nested_lo_le_hi_of_le I hnm).1
    have hhi : I.lo m ≤ I.hi n := nested_cross_le I m n
    have hw : I.hi n - I.lo n = 1 / (2 : ℚ) ^ n := h_width n
    rw [abs_le]
    constructor <;> linarith

/-- A regular Cauchy sequence of rational phases with explicit modulus $|x_m - x_n| \le \frac{1}{m+1} + \frac{1}{n+1}$. -/
structure RegPhaseSeq where
  seq : ℕ → ℚ
  reg : ∀ m n : ℕ, |seq m - seq n| ≤ 1 / ((m : ℚ) + 1) + 1 / ((n : ℚ) + 1)

/-- Positivity helper for $\frac{1}{n+1}$ in $\mathbb{Q}$. -/
theorem unit_frac_nonneg (n : ℕ) : (0 : ℚ) ≤ 1 / ((n : ℚ) + 1) := by
  have hn : (0 : ℚ) ≤ (n : ℚ) := Nat.cast_nonneg n
  have hpos : (0 : ℚ) < (n : ℚ) + 1 := by linarith
  exact div_nonneg zero_le_one (le_of_lt hpos)

/-- Constant embedding of $\mathbb{Q}$ into regular Cauchy phase sequences. -/
def ofRatSeq (q : ℚ) : RegPhaseSeq where
  seq := fun _ => q
  reg := fun m n => by
    simp only [sub_self, abs_zero]
    have hm := unit_frac_nonneg m
    have hn := unit_frac_nonneg n
    linarith

/-- Metric density of $\mathbb{Q}$ inside `RegPhaseSeq`: the $N$-th rational term approximates $x$ within $\frac{1}{N+1} + \frac{1}{m+1}$. -/
theorem ofRatSeq_approx (x : RegPhaseSeq) (N : ℕ) :
    ∀ m : ℕ, |(ofRatSeq (x.seq N)).seq m - x.seq m| ≤ 1 / ((N : ℚ) + 1) + 1 / ((m : ℚ) + 1) := by
  intro m
  exact x.reg N m

/-- Negation of a regular Cauchy phase sequence. -/
def negSeq (x : RegPhaseSeq) : RegPhaseSeq where
  seq := fun n => -x.seq n
  reg := fun m n => by
    have hsub : -x.seq m - -x.seq n = -(x.seq m - x.seq n) := by ring
    rw [hsub, abs_neg]
    exact x.reg m n

/-- Midpoint average $(x + y)/2$ of two regular Cauchy phase sequences. -/
def avgSeq (x y : RegPhaseSeq) : RegPhaseSeq where
  seq := fun n => (x.seq n + y.seq n) / 2
  reg := fun m n => by
    have hx := abs_le.mp (x.reg m n)
    have hy := abs_le.mp (y.reg m n)
    rw [abs_le]
    constructor <;> linarith

/-- Equivalence relation on `RegPhaseSeq`: asymptotic convergence of the difference to $0$. -/
def cauchyEquiv (x y : RegPhaseSeq) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ N : ℕ, ∀ n ≥ N, |x.seq n - y.seq n| ≤ ε

theorem cauchyEquiv_refl (x : RegPhaseSeq) : cauchyEquiv x x := by
  intro ε hε
  refine ⟨0, fun n _ => ?_⟩
  simp only [sub_self, abs_zero]
  exact le_of_lt hε

theorem cauchyEquiv_symm {x y : RegPhaseSeq} (h : cauchyEquiv x y) : cauchyEquiv y x := by
  intro ε hε
  obtain ⟨N, hN⟩ := h ε hε
  refine ⟨N, fun n hn => ?_⟩
  rw [abs_sub_comm]
  exact hN n hn

theorem cauchyEquiv_trans {x y z : RegPhaseSeq}
    (hxy : cauchyEquiv x y) (hyz : cauchyEquiv y z) : cauchyEquiv x z := by
  intro ε hε
  have hε2 : 0 < ε / 2 := by linarith
  obtain ⟨N₁, hN₁⟩ := hxy (ε / 2) hε2
  obtain ⟨N₂, hN₂⟩ := hyz (ε / 2) hε2
  refine ⟨max N₁ N₂, fun n hn => ?_⟩
  have hn1 : n ≥ N₁ := le_trans (le_max_left N₁ N₂) hn
  have hn2 : n ≥ N₂ := le_trans (le_max_right N₁ N₂) hn
  have h1 := abs_le.mp (hN₁ n hn1)
  have h2 := abs_le.mp (hN₂ n hn2)
  rw [abs_le]
  constructor <;> linarith

/-! ## Section 3: Precompactness / Total Boundedness of $[0, 1]$ by Finite $N$-Torsion Grids -/

/-- Every rational phase $q \in [0, 1]$ lies within $1/N$ of a finite $N$-torsion grid point $k/N$ ($0 \le k \le N$). -/
theorem finite_torsion_grid_covers_unit_interval (q : ℚ) (hq0 : 0 ≤ q) (hq1 : q ≤ 1)
    (N : ℕ) (hN : 0 < N) :
    ∃ k : ℕ, k ≤ N ∧ |q - (k : ℚ) / (N : ℚ)| ≤ 1 / (N : ℚ) := by
  have hN_pos : (0 : ℚ) < (N : ℚ) := Nat.cast_pos.mpr hN
  have hN_nonneg : (0 : ℚ) ≤ (N : ℚ) := le_of_lt hN_pos
  have hNq_nonneg : (0 : ℚ) ≤ (N : ℚ) * q := mul_nonneg hN_nonneg hq0
  have hNq_le : (N : ℚ) * q ≤ (N : ℚ) := by
    calc (N : ℚ) * q ≤ (N : ℚ) * 1 := mul_le_mul_of_nonneg_left hq1 hN_nonneg
    _ = (N : ℚ) := mul_one (N : ℚ)
  let m : ℤ := ⌊(N : ℚ) * q⌋
  have hm_nonneg : 0 ≤ m := Int.floor_nonneg.mpr hNq_nonneg
  have hm_le_Nq : (m : ℚ) ≤ (N : ℚ) * q := Int.floor_le ((N : ℚ) * q)
  have hNq_lt_m1 : (N : ℚ) * q < (m : ℚ) + 1 := Int.lt_floor_add_one ((N : ℚ) * q)
  have hm_le_N_rat : (m : ℚ) ≤ ((N : ℤ) : ℚ) := by
    simpa using le_trans hm_le_Nq hNq_le
  have hm_le_N_int : m ≤ (N : ℤ) := Int.cast_le.mp hm_le_N_rat
  let k : ℕ := m.toNat
  have hk_int : (k : ℤ) = m := Int.toNat_of_nonneg hm_nonneg
  have hk_le_N : k ≤ N := by
    have h_int : (k : ℤ) ≤ (N : ℤ) := by omega
    exact Int.ofNat_le.mp h_int
  have hk_rat : (k : ℚ) = (m : ℚ) := by exact_mod_cast hk_int
  refine ⟨k, hk_le_N, ?_⟩
  have h_diff_nonneg : 0 ≤ (N : ℚ) * q - (k : ℚ) := by linarith
  have h_diff_le_one : (N : ℚ) * q - (k : ℚ) ≤ 1 := by linarith
  have h_div_nonneg : 0 ≤ ((N : ℚ) * q - (k : ℚ)) / (N : ℚ) :=
    div_nonneg h_diff_nonneg hN_nonneg
  have h_div_le : ((N : ℚ) * q - (k : ℚ)) / (N : ℚ) ≤ 1 / (N : ℚ) :=
    div_le_div_of_nonneg_right h_diff_le_one hN_nonneg
  have h_eq : q - (k : ℚ) / (N : ℚ) = ((N : ℚ) * q - (k : ℚ)) / (N : ℚ) := by
    have hN_ne : (N : ℚ) ≠ 0 := ne_of_gt hN_pos
    rw [sub_div, mul_div_cancel_left₀ q hN_ne]
  have h_inv_nonneg : (0 : ℚ) ≤ 1 / (N : ℚ) := div_nonneg zero_le_one hN_nonneg
  rw [h_eq, abs_le]
  constructor <;> linarith

/-- Combining finite $N$-torsion grid total boundedness with Cauchy regularity:
for any regular phase sequence $x$ taking values in $[0, 1]$ and any grid size $N \ge 1$,
there is an $N$-torsion point $k/N$ that approximates $x_N$ within $1/N$ and thus approximates
every tail term $x_m$ within $\frac{1}{N} + \frac{1}{N+1} + \frac{1}{m+1}$. -/
theorem regPhaseSeq_precompact_approx (x : RegPhaseSeq)
    (h0 : ∀ n, 0 ≤ x.seq n) (h1 : ∀ n, x.seq n ≤ 1) (N : ℕ) (hN : 0 < N) :
    ∃ k : ℕ, k ≤ N ∧ ∀ m : ℕ,
      |x.seq m - (k : ℚ) / (N : ℚ)| ≤
        1 / (N : ℚ) + 1 / ((N : ℚ) + 1) + 1 / ((m : ℚ) + 1) := by
  obtain ⟨k, hkN, hk_approx⟩ :=
    finite_torsion_grid_covers_unit_interval (x.seq N) (h0 N) (h1 N) N hN
  refine ⟨k, hkN, fun m => ?_⟩
  have hreg := abs_le.mp (x.reg m N)
  have hgrid := abs_le.mp hk_approx
  rw [abs_le]
  constructor <;> linarith

end U1Fable.CauchyCircleCompletion

#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.zero
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.one
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.ofRat
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.sqrt5
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.sub
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.neg
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.zero_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.zero_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.one_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.one_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.sub_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.sub_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.neg_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.neg_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul_a
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul_b
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add_assoc
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add_comm
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.zero_add
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.add_zero
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.neg_add_cancel
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul_assoc
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul_comm
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.one_mul
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.mul_one
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.left_distrib
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.right_distrib
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.sqrt5_sq
#print axioms U1Fable.CauchyCircleCompletion.QuadSqrt5.norm_sq_mul
#print axioms U1Fable.CauchyCircleCompletion.CircleQuadSqrt5.mul
#print axioms U1Fable.CauchyCircleCompletion.CircleQuadSqrt5.one
#print axioms U1Fable.CauchyCircleCompletion.CircleQuadSqrt5.inv
#print axioms U1Fable.CauchyCircleCompletion.u345Quad
#print axioms U1Fable.CauchyCircleCompletion.wHalf
#print axioms U1Fable.CauchyCircleCompletion.wHalf_sq_eq_u345
#print axioms U1Fable.CauchyCircleCompletion.wHalf_not_rational
#print axioms U1Fable.CauchyCircleCompletion.nested_lo_mono_add
#print axioms U1Fable.CauchyCircleCompletion.nested_hi_anti_add
#print axioms U1Fable.CauchyCircleCompletion.nested_lo_le_hi_of_le
#print axioms U1Fable.CauchyCircleCompletion.nested_cross_le
#print axioms U1Fable.CauchyCircleCompletion.nested_dyadic_cauchy
#print axioms U1Fable.CauchyCircleCompletion.unit_frac_nonneg
#print axioms U1Fable.CauchyCircleCompletion.ofRatSeq
#print axioms U1Fable.CauchyCircleCompletion.ofRatSeq_approx
#print axioms U1Fable.CauchyCircleCompletion.negSeq
#print axioms U1Fable.CauchyCircleCompletion.avgSeq
#print axioms U1Fable.CauchyCircleCompletion.cauchyEquiv
#print axioms U1Fable.CauchyCircleCompletion.cauchyEquiv_refl
#print axioms U1Fable.CauchyCircleCompletion.cauchyEquiv_symm
#print axioms U1Fable.CauchyCircleCompletion.cauchyEquiv_trans
#print axioms U1Fable.CauchyCircleCompletion.finite_torsion_grid_covers_unit_interval
#print axioms U1Fable.CauchyCircleCompletion.regPhaseSeq_precompact_approx
