import BornEffectValuation
import BornGaussRat
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Basis
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.Star.Pi
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.Ring.Unbundled.Basic
import Mathlib.Algebra.Order.Floor.Semiring
import Mathlib.Data.Rat.Floor
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel

/-
Gaussian-rational Hermitian carrier for the effect-valuation interface `BornFable.OrderedQUnit`.
AuthorityEffect: None.

Carrier.  V := Matrix (Fin n) (Fin n) GaussRat, all n×n matrices over ℚ(i) (Hermitianity is NOT
imposed on the carrier).  Hermitian form hf A x := re (x* A x) with x* the componentwise
conjugate.  Order: le A B := ∀ x, 0 ≤ hf (B - A) x, i.e. B - A is positive semidefinite on
Gaussian-rational points (`PsdH`).  Unit: u := 1.

The order is a preorder (reflexive, transitive, translation- and scaling-compatible) but NOT a
partial order: a skew-Hermitian matrix A (Aᴴ = -A) has hf A x = 0 for every x, hence A ≤ 0 and
0 ≤ A while A ≠ 0 in general (`skew_le_zero_and_ge`).  `OrderedQUnit` asks only for reflexivity
and transitivity, so `space n` is an honest instance of that interface.  The form only sees the
Hermitian part of a matrix (`hf_conjTranspose`), and a Hermitian density matrix only sees the
Hermitian part of an effect (`re_trace_mul_conjTranspose`).

Nothing physical is claimed.  The matrix algebra over ℚ(i), its order, the order-unit bound, the
rank-one effects, and the real-trace representation of ℚ-linear functionals are supplied
(standard finite linear algebra over ℚ(i)), not derived from any physical postulate.  No Born
rule and no Gleason-type uniqueness is proved here.  Everything is exact over ℚ; no real or
complex numbers, limits, or continuity.
-/

namespace BornFable.HermitianCarrier

open Matrix BornFable

variable {n : ℕ}

/-! ### The squared norm of a Gaussian-rational vector -/

/-- The squared Euclidean norm `∑ i, |x i|²`, a rational number. -/
def vnorm (x : Fin n → GaussRat) : ℚ := ∑ i, GaussRat.normSq (x i)

theorem vnorm_nonneg (x : Fin n → GaussRat) : 0 ≤ vnorm x :=
  Finset.sum_nonneg fun i _ => GaussRat.normSq_nonneg (x i)

theorem vnorm_eq_zero_iff (x : Fin n → GaussRat) : vnorm x = 0 ↔ x = 0 := by
  unfold vnorm
  rw [Finset.sum_eq_zero_iff_of_nonneg fun i _ => GaussRat.normSq_nonneg (x i)]
  constructor
  · intro h
    funext i
    exact (GaussRat.normSq_eq_zero_iff (x i)).mp (h i (Finset.mem_univ i))
  · intro h i _
    rw [h, Pi.zero_apply]
    exact (GaussRat.normSq_eq_zero_iff 0).mpr rfl

theorem vnorm_zero : vnorm (0 : Fin n → GaussRat) = 0 := (vnorm_eq_zero_iff 0).mpr rfl

theorem vnorm_pos {x : Fin n → GaussRat} (hx : x ≠ 0) : 0 < vnorm x := by
  rcases (vnorm_nonneg x).lt_or_eq with h | h
  · exact h
  · exact absurd ((vnorm_eq_zero_iff x).mp h.symm) hx

theorem normSq_le_vnorm (x : Fin n → GaussRat) (i : Fin n) : GaussRat.normSq (x i) ≤ vnorm x := by
  unfold vnorm
  exact Finset.single_le_sum (f := fun j => GaussRat.normSq (x j))
    (fun j _ => GaussRat.normSq_nonneg (x j)) (Finset.mem_univ i)

/-! ### The Hermitian form and its algebraic rules -/

/-- The real part of the Hermitian form `x* A x` at the Gaussian-rational vector `x`. -/
def hf (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) : ℚ :=
  (star x ⬝ᵥ (A *ᵥ x)).re

theorem hf_add (A B : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf (A + B) x = hf A x + hf B x := by
  unfold hf
  rw [Matrix.add_mulVec, dotProduct_add, GaussRat.re_add]

theorem hf_sub (A B : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf (A - B) x = hf A x - hf B x := by
  unfold hf
  rw [Matrix.sub_mulVec, dotProduct_sub, GaussRat.re_sub]

theorem hf_neg (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf (-A) x = -hf A x := by
  unfold hf
  rw [Matrix.neg_mulVec, dotProduct_neg, GaussRat.re_neg]

theorem hf_smul (q : ℚ) (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf (q • A) x = q * hf A x := by
  unfold hf
  rw [Matrix.smul_mulVec, dotProduct_smul, GaussRat.re_smul]

theorem hf_zero (x : Fin n → GaussRat) : hf (0 : Matrix (Fin n) (Fin n) GaussRat) x = 0 := by
  unfold hf
  rw [Matrix.zero_mulVec, dotProduct_zero, GaussRat.re_zero]

theorem hf_one (x : Fin n → GaussRat) : hf (1 : Matrix (Fin n) (Fin n) GaussRat) x = vnorm x := by
  unfold hf vnorm
  rw [Matrix.one_mulVec]
  unfold dotProduct
  rw [GaussRat.re_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Pi.star_apply, GaussRat.re_star_mul_self]

theorem hf_eq_sum_sum (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf A x = ∑ i, ∑ j, (star (x i) * (A i j * x j)).re := by
  unfold hf
  simp only [dotProduct, Matrix.mulVec_apply_eq_sum, Finset.mul_sum, GaussRat.re_sum,
    Pi.star_apply]

/-! ### Positive semidefiniteness over Gaussian-rational points, and the ordered unit space -/

/-- Positive semidefinite on Gaussian-rational vectors: the exact finite notion used throughout. -/
def PsdH (A : Matrix (Fin n) (Fin n) GaussRat) : Prop := ∀ x, 0 ≤ hf A x

/-- The Gaussian-rational matrix carrier as an `OrderedQUnit`: `le A B` iff `B - A` is `PsdH`,
unit `1`. -/
def space (n : ℕ) : OrderedQUnit (Matrix (Fin n) (Fin n) GaussRat) where
  le A B := PsdH (B - A)
  le_refl A := by
    intro x
    rw [sub_self, hf_zero]
  le_trans A B C hAB hBC := by
    intro x
    have e : C - A = (C - B) + (B - A) := by abel
    rw [e, hf_add]
    exact add_nonneg (hBC x) (hAB x)
  add_le_add_right A B C h := by
    intro x
    have e : B + C - (A + C) = B - A := by abel
    rw [e]
    exact h x
  smul_nonneg q A hq hA := by
    intro x
    rw [sub_zero, hf_smul]
    have h := hA x
    rw [sub_zero] at h
    exact mul_nonneg hq h
  u := 1
  u_nonneg := by
    intro x
    rw [sub_zero, hf_one]
    exact vnorm_nonneg x

theorem space_le (A B : Matrix (Fin n) (Fin n) GaussRat) :
    (space n).le A B ↔ PsdH (B - A) := Iff.rfl

theorem space_u : (space n).u = 1 := rfl

theorem effect_iff (E : Matrix (Fin n) (Fin n) GaussRat) :
    (space n).Effect E ↔ PsdH E ∧ PsdH (1 - E) := by
  show PsdH (E - 0) ∧ PsdH (1 - E) ↔ PsdH E ∧ PsdH (1 - E)
  rw [sub_zero]

theorem effect_iff' (E : Matrix (Fin n) (Fin n) GaussRat) :
    (space n).Effect E ↔ ∀ x, 0 ≤ hf E x ∧ hf E x ≤ vnorm x := by
  rw [effect_iff]
  constructor
  · rintro ⟨h1, h2⟩ x
    refine ⟨h1 x, ?_⟩
    have h := h2 x
    rw [hf_sub, hf_one] at h
    linarith
  · intro h
    refine ⟨fun x => (h x).1, fun x => ?_⟩
    rw [hf_sub, hf_one]
    linarith [(h x).2]

/-! ### Order-unit bound: every matrix lies between `-k • 1` and `k • 1` -/

theorem re_star_mul_mul_le (a c b : GaussRat) :
    |(star a * (c * b)).re| ≤
      (|c.re| + |c.im|) * ((GaussRat.normSq a + GaussRat.normSq b) / 2) := by
  have e : (star a * (c * b)).re =
      c.re * (a.re * b.re + a.im * b.im) + c.im * (a.im * b.re - a.re * b.im) := by
    simp only [GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star]
    ring
  have h1 : |a.re * b.re + a.im * b.im| ≤ (GaussRat.normSq a + GaussRat.normSq b) / 2 := by
    rw [abs_le]
    unfold GaussRat.normSq
    constructor
    · nlinarith [sq_nonneg (a.re + b.re), sq_nonneg (a.im + b.im)]
    · nlinarith [sq_nonneg (a.re - b.re), sq_nonneg (a.im - b.im)]
  have h2 : |a.im * b.re - a.re * b.im| ≤ (GaussRat.normSq a + GaussRat.normSq b) / 2 := by
    rw [abs_le]
    unfold GaussRat.normSq
    constructor
    · nlinarith [sq_nonneg (a.im + b.re), sq_nonneg (a.re - b.im)]
    · nlinarith [sq_nonneg (a.im - b.re), sq_nonneg (a.re + b.im)]
  rw [e]
  calc |c.re * (a.re * b.re + a.im * b.im) + c.im * (a.im * b.re - a.re * b.im)|
      ≤ |c.re * (a.re * b.re + a.im * b.im)| + |c.im * (a.im * b.re - a.re * b.im)| :=
        abs_add_le _ _
    _ = |c.re| * |a.re * b.re + a.im * b.im| + |c.im| * |a.im * b.re - a.re * b.im| := by
        rw [abs_mul, abs_mul]
    _ ≤ |c.re| * ((GaussRat.normSq a + GaussRat.normSq b) / 2)
          + |c.im| * ((GaussRat.normSq a + GaussRat.normSq b) / 2) :=
        add_le_add (mul_le_mul_of_nonneg_left h1 (abs_nonneg _))
          (mul_le_mul_of_nonneg_left h2 (abs_nonneg _))
    _ = (|c.re| + |c.im|) * ((GaussRat.normSq a + GaussRat.normSq b) / 2) := by ring

theorem abs_hf_le (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    |hf A x| ≤ (∑ i, ∑ j, (|(A i j).re| + |(A i j).im|)) * vnorm x := by
  rw [hf_eq_sum_sum, Finset.sum_mul]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun i _ => ?_)
  rw [Finset.sum_mul]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun j _ => ?_)
  calc |(star (x i) * (A i j * x j)).re|
      ≤ (|(A i j).re| + |(A i j).im|) * ((GaussRat.normSq (x i) + GaussRat.normSq (x j)) / 2) :=
        re_star_mul_mul_le _ _ _
    _ ≤ (|(A i j).re| + |(A i j).im|) * vnorm x := by
        apply mul_le_mul_of_nonneg_left _ (add_nonneg (abs_nonneg _) (abs_nonneg _))
        have h1 := normSq_le_vnorm x i
        have h2 := normSq_le_vnorm x j
        linarith

theorem order_unit (A : Matrix (Fin n) (Fin n) GaussRat) :
    ∃ k : ℕ, (space n).le (-((k : ℚ) • (1 : Matrix (Fin n) (Fin n) GaussRat))) A ∧
      (space n).le A ((k : ℚ) • (1 : Matrix (Fin n) (Fin n) GaussRat)) := by
  obtain ⟨c, hc⟩ : ∃ c : ℚ, c = ∑ i, ∑ j, (|(A i j).re| + |(A i j).im|) := ⟨_, rfl⟩
  have hk : c ≤ (⌈c⌉₊ : ℚ) := Nat.le_ceil c
  refine ⟨⌈c⌉₊, ?_, ?_⟩
  · intro x
    have h := abs_hf_le A x
    rw [← hc] at h
    have hS := vnorm_nonneg x
    have hcS : c * vnorm x ≤ (⌈c⌉₊ : ℚ) * vnorm x := mul_le_mul_of_nonneg_right hk hS
    rw [sub_neg_eq_add, hf_add, hf_smul, hf_one]
    linarith [(abs_le.mp h).1]
  · intro x
    have h := abs_hf_le A x
    rw [← hc] at h
    have hS := vnorm_nonneg x
    have hcS : c * vnorm x ≤ (⌈c⌉₊ : ℚ) * vnorm x := mul_le_mul_of_nonneg_right hk hS
    rw [hf_sub, hf_smul, hf_one]
    linarith [(abs_le.mp h).2]

/-! ### Rank-one effects -/

theorem star_dot_eq_sum (x y : Fin n → GaussRat) :
    star (star x ⬝ᵥ y) = ∑ i, star (y i) * x i := by
  simp only [dotProduct, star_sum, star_mul, star_star, Pi.star_apply]

theorem dot_vecMulVec_star (x y : Fin n → GaussRat) :
    star y ⬝ᵥ (vecMulVec x (star x) *ᵥ y) = star (star x ⬝ᵥ y) * (star x ⬝ᵥ y) := by
  rw [star_dot_eq_sum]
  simp only [dotProduct, Matrix.mulVec_apply_eq_sum, vecMulVec_apply, Pi.star_apply]
  rw [Finset.sum_mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  ring

theorem hf_vecMulVec_star (x y : Fin n → GaussRat) :
    hf (vecMulVec x (star x)) y = GaussRat.normSq (star x ⬝ᵥ y) := by
  unfold hf
  rw [dot_vecMulVec_star, GaussRat.re_star_mul_self]

/-- Cauchy–Schwarz over ℚ(i): `|x* y|² ≤ ‖x‖² ‖y‖²`, proved by expanding
`0 ≤ ‖(‖x‖²) y - (x* y) x‖²`. -/
theorem normSq_dot_le (x y : Fin n → GaussRat) :
    GaussRat.normSq (star x ⬝ᵥ y) ≤ vnorm x * vnorm y := by
  by_cases hx : x = 0
  · subst hx
    calc GaussRat.normSq (star (0 : Fin n → GaussRat) ⬝ᵥ y) = 0 := by
          rw [star_zero, zero_dotProduct]
          exact (GaussRat.normSq_eq_zero_iff 0).mpr rfl
      _ ≤ vnorm 0 * vnorm y := mul_nonneg (vnorm_nonneg 0) (vnorm_nonneg y)
  · obtain ⟨c, hc⟩ : ∃ c : GaussRat, c = star x ⬝ᵥ y := ⟨_, rfl⟩
    obtain ⟨N, hN⟩ : ∃ N : ℚ, N = vnorm x := ⟨_, rfl⟩
    have hNpos : 0 < N := by
      rw [hN]
      exact vnorm_pos hx
    have hstar : star c = ∑ i, star (y i) * x i := by
      rw [hc]
      exact star_dot_eq_sum x y
    have hre : ∑ i, (star (y i) * (c * x i)).re = GaussRat.normSq c := by
      have hsum : ∑ i, star (y i) * (c * x i) = c * star c := by
        rw [hstar, Finset.mul_sum]
        refine Finset.sum_congr rfl fun i _ => ?_
        ring
      rw [← GaussRat.re_sum, hsum, mul_comm, GaussRat.re_star_mul_self]
    have hterm : ∀ i, GaussRat.normSq (N • y i - c * x i) =
        N ^ 2 * GaussRat.normSq (y i) + GaussRat.normSq c * GaussRat.normSq (x i)
          - 2 * N * (star (y i) * (c * x i)).re := by
      intro i
      simp only [GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub, GaussRat.re_smul,
        GaussRat.im_smul, GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star]
      ring
    have hz : 0 ≤ vnorm (fun i => N • y i - c * x i) := vnorm_nonneg _
    have hexp : vnorm (fun i => N • y i - c * x i) = N * (N * vnorm y - GaussRat.normSq c) := by
      have h1 : vnorm (fun i => N • y i - c * x i) =
          ∑ i, (N ^ 2 * GaussRat.normSq (y i) + GaussRat.normSq c * GaussRat.normSq (x i)
            - 2 * N * (star (y i) * (c * x i)).re) := by
        unfold vnorm
        exact Finset.sum_congr rfl fun i _ => hterm i
      rw [h1, Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
        ← Finset.mul_sum, hre]
      unfold vnorm at hN ⊢
      rw [← hN]
      ring
    rw [hexp] at hz
    have h2 : 0 ≤ N * vnorm y - GaussRat.normSq c := (mul_nonneg_iff_of_pos_left hNpos).mp hz
    rw [← hc, ← hN]
    linarith

/-- The rank-one matrix `(1 / ‖x‖²) • x x*` (a projector when `x ≠ 0`). -/
def P (x : Fin n → GaussRat) : Matrix (Fin n) (Fin n) GaussRat :=
  (1 / vnorm x) • vecMulVec x (star x)

theorem hf_rankOne (x y : Fin n → GaussRat) :
    hf (P x) y = GaussRat.normSq (star x ⬝ᵥ y) / vnorm x := by
  unfold P
  rw [hf_smul, hf_vecMulVec_star, one_div_mul_eq_div]

theorem rankOne_effect {x : Fin n → GaussRat} (hx : x ≠ 0) : (space n).Effect (P x) := by
  rw [effect_iff']
  intro y
  rw [hf_rankOne]
  have hpos := vnorm_pos hx
  constructor
  · exact div_nonneg (GaussRat.normSq_nonneg _) hpos.le
  · rw [div_le_iff₀ hpos]
    calc GaussRat.normSq (star x ⬝ᵥ y) ≤ vnorm x * vnorm y := normSq_dot_le x y
      _ = vnorm y * vnorm x := mul_comm _ _

/-! ### Real-trace representation of ℚ-linear functionals -/

/-- The matrix representing a ℚ-linear functional `L` (real-valued, not ℚ(i)-linear):
`repMatrix L i j = ⟨L (single j i 1), -L (single j i I)⟩`. -/
def repMatrix (L : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ) : Matrix (Fin n) (Fin n) GaussRat :=
  Matrix.of fun i j =>
    (⟨L (Matrix.single j i 1), -L (Matrix.single j i GaussRat.I)⟩ : GaussRat)

theorem repMatrix_apply (L : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ) (i j : Fin n) :
    repMatrix L i j = ⟨L (Matrix.single j i 1), -L (Matrix.single j i GaussRat.I)⟩ := rfl

theorem repMatrix_re (L : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ) (i j : Fin n) :
    (repMatrix L i j).re = L (Matrix.single j i 1) := rfl

theorem repMatrix_im (L : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ) (i j : Fin n) :
    (repMatrix L i j).im = -L (Matrix.single j i GaussRat.I) := rfl

theorem trace_mul_eq_sum (ρ A : Matrix (Fin n) (Fin n) GaussRat) :
    Matrix.trace (ρ * A) = ∑ i, ∑ j, ρ i j * A j i := by
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply]

theorem re_trace_mul (ρ A : Matrix (Fin n) (Fin n) GaussRat) :
    (Matrix.trace (ρ * A)).re =
      ∑ i, ∑ j, ((ρ i j).re * (A j i).re - (ρ i j).im * (A j i).im) := by
  rw [trace_mul_eq_sum]
  simp only [GaussRat.re_sum, GaussRat.re_mul]

theorem single_eq_smul_add_smul (i j : Fin n) (z : GaussRat) :
    Matrix.single i j z =
      z.re • Matrix.single i j (1 : GaussRat) + z.im • Matrix.single i j GaussRat.I := by
  rw [Matrix.smul_single, Matrix.smul_single, ← Matrix.single_add]
  exact congrArg (Matrix.single i j) (by ext <;> simp)

theorem trace_rep (L : Matrix (Fin n) (Fin n) GaussRat →ₗ[ℚ] ℚ)
    (A : Matrix (Fin n) (Fin n) GaussRat) :
    L A = (Matrix.trace (repMatrix L * A)).re := by
  calc L A = L (∑ i, ∑ j, Matrix.single i j (A i j)) :=
        congrArg L (Matrix.matrix_eq_sum_single A)
    _ = ∑ i, ∑ j, ((A i j).re * L (Matrix.single i j (1 : GaussRat))
          + (A i j).im * L (Matrix.single i j GaussRat.I)) := by
        rw [map_sum]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [map_sum]
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [single_eq_smul_add_smul, map_add, LinearMap.map_smul, LinearMap.map_smul,
          smul_eq_mul, smul_eq_mul]
    _ = ∑ i, ∑ j, ((repMatrix L j i).re * (A i j).re - (repMatrix L j i).im * (A i j).im) := by
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        rw [repMatrix_re, repMatrix_im]
        ring
    _ = ∑ j, ∑ i, ((repMatrix L j i).re * (A i j).re - (repMatrix L j i).im * (A i j).im) :=
        Finset.sum_comm
    _ = (Matrix.trace (repMatrix L * A)).re := (re_trace_mul _ _).symm

theorem re_trace_mul_single_one (ρ : Matrix (Fin n) (Fin n) GaussRat) (i j : Fin n) :
    (Matrix.trace (ρ * Matrix.single j i (1 : GaussRat))).re = (ρ i j).re := by
  rw [Matrix.trace_mul_single, op_smul_eq_mul, mul_one]

theorem re_trace_mul_single_I (ρ : Matrix (Fin n) (Fin n) GaussRat) (i j : Fin n) :
    (Matrix.trace (ρ * Matrix.single j i GaussRat.I)).re = -(ρ i j).im := by
  rw [Matrix.trace_mul_single, op_smul_eq_mul, GaussRat.re_mul, GaussRat.re_I, GaussRat.im_I]
  ring

theorem rep_unique (ρ ρ' : Matrix (Fin n) (Fin n) GaussRat)
    (h : ∀ A, (Matrix.trace (ρ * A)).re = (Matrix.trace (ρ' * A)).re) : ρ = ρ' := by
  refine Matrix.ext fun i j => GaussRat.ext ?_ ?_
  · have h1 := h (Matrix.single j i 1)
    rwa [re_trace_mul_single_one, re_trace_mul_single_one] at h1
  · have h2 := h (Matrix.single j i GaussRat.I)
    rw [re_trace_mul_single_I, re_trace_mul_single_I] at h2
    exact neg_inj.mp h2

theorem dot_eq_trace (ρ : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    star x ⬝ᵥ (ρ *ᵥ x) = Matrix.trace (ρ * vecMulVec x (star x)) := by
  rw [Matrix.mul_vecMulVec, Matrix.trace_vecMulVec, dotProduct_comm]

theorem hf_eq_re_trace (ρ : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf ρ x = (Matrix.trace (ρ * vecMulVec x (star x))).re :=
  congrArg GaussRat.re (dot_eq_trace ρ x)

/-! ### Conjugate transpose: the form sees only the Hermitian part -/

theorem star_dot_mulVec (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    star (star x ⬝ᵥ (A *ᵥ x)) = star x ⬝ᵥ (Aᴴ *ᵥ x) := by
  rw [star_dotProduct x (A *ᵥ x), star_star, Matrix.star_mulVec, ← Matrix.dotProduct_mulVec]

theorem hf_conjTranspose (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) :
    hf Aᴴ x = hf A x := by
  unfold hf
  rw [← star_dot_mulVec, GaussRat.re_star]

theorem re_trace_mul_conjTranspose {ρ : Matrix (Fin n) (Fin n) GaussRat} (hρ : ρᴴ = ρ)
    (E : Matrix (Fin n) (Fin n) GaussRat) :
    (Matrix.trace (ρ * Eᴴ)).re = (Matrix.trace (ρ * E)).re := by
  have h : Matrix.trace (ρ * Eᴴ) = star (Matrix.trace (ρ * E)) := by
    calc Matrix.trace (ρ * Eᴴ) = Matrix.trace (ρᴴ * Eᴴ) := by rw [hρ]
      _ = Matrix.trace ((E * ρ)ᴴ) := by rw [Matrix.conjTranspose_mul]
      _ = star (Matrix.trace (E * ρ)) := Matrix.trace_conjTranspose _
      _ = star (Matrix.trace (ρ * E)) := by rw [Matrix.trace_mul_comm]
  rw [h, GaussRat.re_star]

/-! ### Non-antisymmetry: skew-Hermitian matrices are both `≤ 0` and `≥ 0` -/

theorem hf_eq_zero_of_skew {A : Matrix (Fin n) (Fin n) GaussRat} (hA : Aᴴ = -A)
    (x : Fin n → GaussRat) : hf A x = 0 := by
  have h : star (star x ⬝ᵥ (A *ᵥ x)) = -(star x ⬝ᵥ (A *ᵥ x)) := by
    rw [star_dot_mulVec, hA, Matrix.neg_mulVec, dotProduct_neg]
  have h' : (star (star x ⬝ᵥ (A *ᵥ x))).re = (-(star x ⬝ᵥ (A *ᵥ x))).re := congrArg GaussRat.re h
  rw [GaussRat.re_star, GaussRat.re_neg] at h'
  unfold hf
  linarith

theorem skew_le_zero_and_ge {A : Matrix (Fin n) (Fin n) GaussRat} (hA : Aᴴ = -A) :
    (space n).le A 0 ∧ (space n).le 0 A := by
  constructor
  · intro x
    rw [zero_sub, hf_neg, hf_eq_zero_of_skew hA, neg_zero]
  · intro x
    rw [sub_zero, hf_eq_zero_of_skew hA]

end BornFable.HermitianCarrier

#print axioms BornFable.HermitianCarrier.vnorm
#print axioms BornFable.HermitianCarrier.vnorm_nonneg
#print axioms BornFable.HermitianCarrier.vnorm_eq_zero_iff
#print axioms BornFable.HermitianCarrier.vnorm_zero
#print axioms BornFable.HermitianCarrier.vnorm_pos
#print axioms BornFable.HermitianCarrier.normSq_le_vnorm
#print axioms BornFable.HermitianCarrier.hf
#print axioms BornFable.HermitianCarrier.hf_add
#print axioms BornFable.HermitianCarrier.hf_sub
#print axioms BornFable.HermitianCarrier.hf_neg
#print axioms BornFable.HermitianCarrier.hf_smul
#print axioms BornFable.HermitianCarrier.hf_zero
#print axioms BornFable.HermitianCarrier.hf_one
#print axioms BornFable.HermitianCarrier.hf_eq_sum_sum
#print axioms BornFable.HermitianCarrier.PsdH
#print axioms BornFable.HermitianCarrier.space
#print axioms BornFable.HermitianCarrier.space_le
#print axioms BornFable.HermitianCarrier.space_u
#print axioms BornFable.HermitianCarrier.effect_iff
#print axioms BornFable.HermitianCarrier.effect_iff'
#print axioms BornFable.HermitianCarrier.re_star_mul_mul_le
#print axioms BornFable.HermitianCarrier.abs_hf_le
#print axioms BornFable.HermitianCarrier.order_unit
#print axioms BornFable.HermitianCarrier.star_dot_eq_sum
#print axioms BornFable.HermitianCarrier.dot_vecMulVec_star
#print axioms BornFable.HermitianCarrier.hf_vecMulVec_star
#print axioms BornFable.HermitianCarrier.normSq_dot_le
#print axioms BornFable.HermitianCarrier.P
#print axioms BornFable.HermitianCarrier.hf_rankOne
#print axioms BornFable.HermitianCarrier.rankOne_effect
#print axioms BornFable.HermitianCarrier.repMatrix
#print axioms BornFable.HermitianCarrier.repMatrix_apply
#print axioms BornFable.HermitianCarrier.repMatrix_re
#print axioms BornFable.HermitianCarrier.repMatrix_im
#print axioms BornFable.HermitianCarrier.trace_mul_eq_sum
#print axioms BornFable.HermitianCarrier.re_trace_mul
#print axioms BornFable.HermitianCarrier.single_eq_smul_add_smul
#print axioms BornFable.HermitianCarrier.trace_rep
#print axioms BornFable.HermitianCarrier.re_trace_mul_single_one
#print axioms BornFable.HermitianCarrier.re_trace_mul_single_I
#print axioms BornFable.HermitianCarrier.rep_unique
#print axioms BornFable.HermitianCarrier.dot_eq_trace
#print axioms BornFable.HermitianCarrier.hf_eq_re_trace
#print axioms BornFable.HermitianCarrier.star_dot_mulVec
#print axioms BornFable.HermitianCarrier.hf_conjTranspose
#print axioms BornFable.HermitianCarrier.re_trace_mul_conjTranspose
#print axioms BornFable.HermitianCarrier.hf_eq_zero_of_skew
#print axioms BornFable.HermitianCarrier.skew_le_zero_and_ge
