import BornHermitianCarrier
import BornHermitianPsdDecomposition
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination

/-
Kernel of the finite exact Wigner theorem over ℚ(i)ⁿ.  AuthorityEffect: None.

Carrier.  `Fin n → GaussRat`, the Gaussian-rational sector carrier of `BornHermitianCarrier`, with the
inner product `ip x y = star x ⬝ᵥ y`, the squared norm `vnorm x = re (ip x x)` (the readout `hf 1 x`
selected up to scale by the sector-form run) and the transition probability
`tp x y = normSq (ip x y) / (vnorm x * vnorm y)`, which is the Born readout of the rank-one effect
`P x` in the state `y`, normalised (`tp_eq_born`).

Contents.  Algebra of `ip`, `vnorm`, `tp` (`ip_self_eq`, `tp_smul_left`, `tp_self`, `tp_le_one`,
`tp_eq_zero_iff`); the equality case of Cauchy–Schwarz over ℚ(i) (`eq_smul_of_normSq_ip_eq`,
`tp_eq_one_iff`); the involution `twist ε` (`ε = 1`: identity, `ε = -1`: componentwise conjugation)
and its compatibility with `tp` (`tp_twist`); similarities `Fᴴ * F = d • 1` (`Similarity`) and the
exact transport `ip (F x) (F y) = d • ip x y`, `tp (F x) (F y) = tp x y` (`tp_mulVec`); the
column matrix `colMatrix f` of a family `f` and the orthogonal expansion
`y = colMatrix f *ᵥ coords f y` of every vector in a pairwise orthogonal family of `n` nonzero vectors
(`expansion`, via `mul_eq_one_comm`: a left inverse of a square matrix over ℚ(i) is a right inverse).

Nothing physical is claimed: the carrier, the scalar field ℚ(i) and the quadratic readout are
supplied.  Exact arithmetic throughout; no real or complex numbers, no limits, no continuity.
-/

namespace WignerFinite.Kernel

open Matrix BornFinite BornFinite.HermitianCarrier BornFinite.HermitianPsd

variable {n : ℕ}

/-! ### Gaussian-rational scalars -/

theorem normSq_star (z : GaussRat) : GaussRat.normSq (star z) = GaussRat.normSq z := by
  simp only [GaussRat.normSq, GaussRat.re_star, GaussRat.im_star]
  ring

theorem normSq_smul (q : ℚ) (z : GaussRat) : GaussRat.normSq (q • z) = q ^ 2 * GaussRat.normSq z := by
  simp only [GaussRat.normSq, GaussRat.re_smul, GaussRat.im_smul]
  ring

theorem normSq_ratCast (q : ℚ) : GaussRat.normSq (q : GaussRat) = q ^ 2 := by
  simp only [GaussRat.normSq, GaussRat.re_ratCast, GaussRat.im_ratCast]
  ring

theorem normSq_I : GaussRat.normSq GaussRat.I = 1 := by
  simp [GaussRat.normSq]

theorem normSq_one_add (u : GaussRat) :
    GaussRat.normSq (1 + u) = 1 + 2 * u.re + GaussRat.normSq u := by
  simp only [GaussRat.normSq, GaussRat.re_add, GaussRat.im_add, GaussRat.re_one, GaussRat.im_one]
  ring

theorem ratCast_mul (q : ℚ) (z : GaussRat) : (q : GaussRat) * z = q • z := by
  ext <;> simp

theorem ratCast_ne_zero {q : ℚ} (hq : q ≠ 0) : (q : GaussRat) ≠ 0 := by
  intro h
  exact hq (congrArg GaussRat.re h)

theorem re_mul_star_self (z : GaussRat) : (z * star z).re = GaussRat.normSq z := by
  rw [mul_comm, GaussRat.re_star_mul_self]

theorem mul_self_eq_one_iff' {q : ℚ} : q * q = 1 ↔ q = 1 ∨ q = -1 := mul_self_eq_one_iff

/-! ### The inner product -/

/-- The Gaussian-rational inner product `x* y`. -/
def ip (x y : Fin n → GaussRat) : GaussRat := star x ⬝ᵥ y

theorem ip_def (x y : Fin n → GaussRat) : ip x y = star x ⬝ᵥ y := rfl

theorem ip_eq_sum (x y : Fin n → GaussRat) : ip x y = ∑ i, star (x i) * y i := by
  simp only [ip, dotProduct, Pi.star_apply]

theorem star_ip (x y : Fin n → GaussRat) : star (ip x y) = ip y x := by
  unfold ip
  rw [star_dotProduct, star_star]

theorem ip_add_left (x y z : Fin n → GaussRat) : ip (x + y) z = ip x z + ip y z := by
  unfold ip
  rw [star_add, add_dotProduct]

theorem ip_add_right (x y z : Fin n → GaussRat) : ip x (y + z) = ip x y + ip x z := by
  unfold ip
  rw [dotProduct_add]

theorem ip_smul_right (c : GaussRat) (x y : Fin n → GaussRat) : ip x (c • y) = c * ip x y := by
  unfold ip
  rw [dotProduct_smul, smul_eq_mul]

theorem ip_smul_left (c : GaussRat) (x y : Fin n → GaussRat) : ip (c • x) y = star c * ip x y := by
  simp only [ip_eq_sum, Pi.smul_apply, smul_eq_mul, star_mul', Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  ring

theorem ip_star_star (x y : Fin n → GaussRat) : ip (star x) (star y) = star (ip x y) := by
  rw [star_ip]
  unfold ip
  rw [star_star, dotProduct_comm]

theorem ip_self_re (x : Fin n → GaussRat) : (ip x x).re = vnorm x := by
  have h := hf_one x
  unfold hf at h
  rw [one_mulVec] at h
  exact h

theorem ip_self_im (x : Fin n → GaussRat) : (ip x x).im = 0 := by
  rw [ip_eq_sum, GaussRat.im_sum]
  exact Finset.sum_eq_zero fun i _ => GaussRat.im_star_mul_self (x i)

theorem ip_self_eq (x : Fin n → GaussRat) : ip x x = ((vnorm x : ℚ) : GaussRat) := by
  ext
  · rw [ip_self_re, GaussRat.re_ratCast]
  · rw [ip_self_im, GaussRat.im_ratCast]

theorem normSq_ip_self (x : Fin n → GaussRat) : GaussRat.normSq (ip x x) = vnorm x ^ 2 := by
  rw [ip_self_eq, normSq_ratCast]

theorem vnorm_add (x y : Fin n → GaussRat) :
    vnorm (x + y) = vnorm x + 2 * (ip x y).re + vnorm y := by
  rw [← ip_self_re, ip_add_left, ip_add_right, ip_add_right, GaussRat.re_add, GaussRat.re_add,
    GaussRat.re_add, ip_self_re, ip_self_re, ← star_ip x y, GaussRat.re_star]
  ring

theorem vnorm_smul (c : GaussRat) (x : Fin n → GaussRat) :
    vnorm (c • x) = GaussRat.normSq c * vnorm x := by
  unfold vnorm
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Pi.smul_apply, smul_eq_mul, GaussRat.normSq_mul]

theorem vnorm_star (x : Fin n → GaussRat) : vnorm (star x) = vnorm x := by
  unfold vnorm
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Pi.star_apply, normSq_star]

theorem vnorm_ne_zero {x : Fin n → GaussRat} (hx : x ≠ 0) : vnorm x ≠ 0 := (vnorm_pos hx).ne'

theorem ne_zero_of_vnorm_ne_zero {x : Fin n → GaussRat} (hx : vnorm x ≠ 0) : x ≠ 0 := by
  intro h
  exact hx (by rw [h, vnorm_zero])

theorem ip_ne_zero_left {x y : Fin n → GaussRat} (h : ip x y ≠ 0) : x ≠ 0 := by
  intro hx
  apply h
  rw [hx, ip_def, star_zero, zero_dotProduct]

theorem ip_ne_zero_right {x y : Fin n → GaussRat} (h : ip x y ≠ 0) : y ≠ 0 := by
  intro hy
  apply h
  rw [hy, ip_def, dotProduct_zero]

/-! ### Unit vectors -/

/-- The sector unit vector `e i`. -/
def e (i : Fin n) : Fin n → GaussRat := Pi.single i 1

theorem e_apply (i j : Fin n) : e i j = if j = i then 1 else 0 := by
  rw [e, Pi.single_apply]

theorem e_apply_self (i : Fin n) : e i i = 1 := by
  rw [e, Pi.single_eq_same]

theorem e_apply_ne {i j : Fin n} (h : j ≠ i) : e i j = 0 := by
  rw [e, Pi.single_eq_of_ne h]

theorem ip_e_left (i : Fin n) (y : Fin n → GaussRat) : ip (e i) y = y i := by
  unfold ip e
  rw [Pi.star_single, single_dotProduct, star_one, one_mul]

theorem ip_e_right (x : Fin n → GaussRat) (i : Fin n) : ip x (e i) = star (x i) := by
  rw [← star_ip, ip_e_left]

theorem vnorm_e (i : Fin n) : vnorm (e i) = 1 := by
  rw [← ip_self_re, ip_e_left, e_apply_self, GaussRat.re_one]

theorem e_ne_zero (i : Fin n) : e i ≠ 0 := by
  intro h
  have := congrFun h i
  rw [e_apply_self, Pi.zero_apply] at this
  exact one_ne_zero this

theorem ip_e_e (i j : Fin n) : ip (e i) (e j) = if i = j then 1 else 0 := by
  rw [ip_e_left, e_apply]

theorem ip_e_e_of_ne {i j : Fin n} (h : i ≠ j) : ip (e i) (e j) = 0 := by
  rw [ip_e_left, e_apply_ne h]

/-- `x = ∑ i, x i • e i`: coordinates in the sector basis. -/
theorem eq_sum_smul_e (x : Fin n → GaussRat) : x = ∑ i, x i • e i := by
  funext j
  rw [Finset.sum_apply]
  simp only [Pi.smul_apply, e_apply, smul_eq_mul, mul_ite, mul_one, mul_zero]
  rw [Finset.sum_ite_eq Finset.univ j (fun i => x i)]
  simp

/-! ### The transition probability -/

/-- The transition probability `|⟨x, y⟩|² / (‖x‖² ‖y‖²)`, a rational number. -/
def tp (x y : Fin n → GaussRat) : ℚ := GaussRat.normSq (ip x y) / (vnorm x * vnorm y)

theorem tp_def (x y : Fin n → GaussRat) : tp x y = GaussRat.normSq (ip x y) / (vnorm x * vnorm y) :=
  rfl

theorem tp_comm (x y : Fin n → GaussRat) : tp x y = tp y x := by
  unfold tp
  rw [← star_ip, normSq_star, mul_comm]

theorem tp_smul_left {c : GaussRat} (hc : c ≠ 0) (x y : Fin n → GaussRat) :
    tp (c • x) y = tp x y := by
  unfold tp
  rw [ip_smul_left, GaussRat.normSq_mul, normSq_star, vnorm_smul, mul_assoc]
  exact mul_div_mul_left _ _ (fun h => hc ((GaussRat.normSq_eq_zero_iff c).mp h))

theorem tp_smul_right {c : GaussRat} (hc : c ≠ 0) (x y : Fin n → GaussRat) :
    tp x (c • y) = tp x y := by
  rw [tp_comm, tp_smul_left hc, tp_comm]

theorem tp_self {x : Fin n → GaussRat} (hx : x ≠ 0) : tp x x = 1 := by
  unfold tp
  rw [normSq_ip_self, sq]
  exact div_self (mul_ne_zero (vnorm_ne_zero hx) (vnorm_ne_zero hx))

theorem tp_nonneg (x y : Fin n → GaussRat) : 0 ≤ tp x y :=
  div_nonneg (GaussRat.normSq_nonneg _) (mul_nonneg (vnorm_nonneg x) (vnorm_nonneg y))

theorem tp_le_one (x y : Fin n → GaussRat) : tp x y ≤ 1 := by
  unfold tp
  rcases (mul_nonneg (vnorm_nonneg x) (vnorm_nonneg y)).lt_or_eq with h | h
  · rw [div_le_one h]
    exact normSq_dot_le x y
  · rw [← h, div_zero]
    exact zero_le_one

theorem tp_eq_zero_iff {x y : Fin n → GaussRat} (hx : x ≠ 0) (hy : y ≠ 0) :
    tp x y = 0 ↔ ip x y = 0 := by
  unfold tp
  rw [div_eq_zero_iff, GaussRat.normSq_eq_zero_iff]
  constructor
  · rintro (h | h)
    · exact h
    · exact absurd h (mul_ne_zero (vnorm_ne_zero hx) (vnorm_ne_zero hy))
  · exact Or.inl

theorem tp_star_star (x y : Fin n → GaussRat) : tp (star x) (star y) = tp x y := by
  unfold tp
  rw [ip_star_star, normSq_star, vnorm_star, vnorm_star]

theorem tp_e_e (i j : Fin n) : tp (e i) (e j) = if i = j then 1 else 0 := by
  unfold tp
  rw [ip_e_e, vnorm_e, vnorm_e]
  by_cases h : i = j
  · simp [h, normSq_one]
  · simp [h, GaussRat.normSq]

/-! ### Equality in Cauchy–Schwarz -/

theorem vnorm_smul_sub_smul (N : ℚ) (c : GaussRat) (x y : Fin n → GaussRat) :
    vnorm (N • y - c • x) =
      N ^ 2 * vnorm y + GaussRat.normSq c * vnorm x - 2 * N * (c * star (ip x y)).re := by
  have hterm : ∀ i, GaussRat.normSq ((N • y - c • x) i) =
      N ^ 2 * GaussRat.normSq (y i) + GaussRat.normSq c * GaussRat.normSq (x i)
        - 2 * N * (c * (x i * star (y i))).re := by
    intro i
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, GaussRat.normSq, GaussRat.re_sub,
      GaussRat.im_sub, GaussRat.re_smul, GaussRat.im_smul, GaussRat.re_mul, GaussRat.im_mul,
      GaussRat.re_star, GaussRat.im_star]
    ring
  have hsum : (c * star (ip x y)).re = ∑ i, (c * (x i * star (y i))).re := by
    rw [star_ip, ip_eq_sum, Finset.mul_sum, GaussRat.re_sum]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [mul_comm (star (y i))]
  unfold vnorm
  rw [hsum, Finset.mul_sum, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib,
    ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun i _ => hterm i

/-- Equality in Cauchy–Schwarz: `|⟨x, y⟩|² = ‖x‖² ‖y‖²` with `x ≠ 0` forces `y ∈ ℚ(i) x`. -/
theorem eq_smul_of_normSq_ip_eq {x y : Fin n → GaussRat} (hx : x ≠ 0)
    (h : GaussRat.normSq (ip x y) = vnorm x * vnorm y) :
    y = (ip x y / ((vnorm x : ℚ) : GaussRat)) • x := by
  have hN : vnorm x ≠ 0 := vnorm_ne_zero hx
  have hN' : ((vnorm x : ℚ) : GaussRat) ≠ 0 := ratCast_ne_zero hN
  have hz : vnorm ((vnorm x) • y - ip x y • x) = 0 := by
    rw [vnorm_smul_sub_smul, re_mul_star_self, h]
    ring
  have hv := (vnorm_eq_zero_iff _).mp hz
  funext i
  have hi := congrFun hv i
  simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hi
  have hi' : ((vnorm x : ℚ) : GaussRat) * y i = ip x y * x i := by
    rw [ratCast_mul]
    exact sub_eq_zero.mp hi
  rw [Pi.smul_apply, smul_eq_mul, div_mul_eq_mul_div, eq_div_iff hN', mul_comm (y i), hi']

theorem tp_eq_one_iff {x y : Fin n → GaussRat} (hx : x ≠ 0) (hy : y ≠ 0) :
    tp x y = 1 ↔ ∃ c : GaussRat, c ≠ 0 ∧ y = c • x := by
  constructor
  · intro h
    unfold tp at h
    rw [div_eq_one_iff_eq (mul_ne_zero (vnorm_ne_zero hx) (vnorm_ne_zero hy))] at h
    refine ⟨ip x y / ((vnorm x : ℚ) : GaussRat), ?_, eq_smul_of_normSq_ip_eq hx h⟩
    intro hc
    have hy' := eq_smul_of_normSq_ip_eq hx h
    rw [hc, zero_smul] at hy'
    exact hy hy'
  · rintro ⟨c, hc, rfl⟩
    rw [tp_smul_right hc, tp_self hx]

/-! ### The Born readout of a rank-one effect -/

/-- `tp x y` is the Born probability `hf (P x) y / vnorm y` of the rank-one effect `P x` in the
state `y` of `BornHermitianCarrier`. -/
theorem tp_eq_born (x y : Fin n → GaussRat) : tp x y = hf (P x) y / vnorm y := by
  unfold tp
  rw [hf_rankOne, div_div]
  rfl

/-! ### The twist `ε = ±1`: identity or componentwise conjugation -/

/-- The scalar twist `⟨a, b⟩ ↦ ⟨a, ε b⟩`. -/
def tw (ε : ℚ) (c : GaussRat) : GaussRat := ⟨c.re, ε * c.im⟩

/-- The vector twist, applied componentwise. -/
def twist (ε : ℚ) (x : Fin n → GaussRat) : Fin n → GaussRat := fun i => tw ε (x i)

theorem twist_apply (ε : ℚ) (x : Fin n → GaussRat) (i : Fin n) : twist ε x i = tw ε (x i) := rfl

@[simp] theorem tw_re (ε : ℚ) (c : GaussRat) : (tw ε c).re = c.re := rfl
@[simp] theorem tw_im (ε : ℚ) (c : GaussRat) : (tw ε c).im = ε * c.im := rfl

theorem tw_one (c : GaussRat) : tw 1 c = c := by
  ext <;> simp [tw]

theorem tw_neg_one (c : GaussRat) : tw (-1) c = star c := by
  ext <;> simp [tw]

theorem twist_one (x : Fin n → GaussRat) : twist 1 x = x := by
  funext i
  exact tw_one (x i)

theorem twist_neg_one (x : Fin n → GaussRat) : twist (-1) x = star x := by
  funext i
  exact tw_neg_one (x i)

theorem tw_tw {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (c : GaussRat) : tw ε (tw ε c) = c := by
  rcases hε with rfl | rfl
  · rw [tw_one, tw_one]
  · rw [tw_neg_one, tw_neg_one, star_star]

theorem twist_twist {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (x : Fin n → GaussRat) :
    twist ε (twist ε x) = x := by
  funext i
  exact tw_tw hε (x i)

theorem tw_mul {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (c d : GaussRat) : tw ε (c * d) = tw ε c * tw ε d := by
  rcases hε with rfl | rfl
  · rw [tw_one, tw_one, tw_one]
  · rw [tw_neg_one, tw_neg_one, tw_neg_one, star_mul']

theorem tw_one' (ε : ℚ) : tw ε 1 = 1 := by
  ext <;> simp [tw]

theorem tw_ratCast (ε : ℚ) (q : ℚ) : tw ε (q : GaussRat) = (q : GaussRat) := by
  ext <;> simp [tw]

theorem tw_eq_zero_iff (ε : ℚ) (hε : ε = 1 ∨ ε = -1) (c : GaussRat) : tw ε c = 0 ↔ c = 0 := by
  rcases hε with rfl | rfl
  · rw [tw_one]
  · rw [tw_neg_one, star_eq_zero]

theorem tw_ne_zero {ε : ℚ} (hε : ε = 1 ∨ ε = -1) {c : GaussRat} (hc : c ≠ 0) : tw ε c ≠ 0 :=
  fun h => hc ((tw_eq_zero_iff ε hε c).mp h)

theorem normSq_tw {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (c : GaussRat) :
    GaussRat.normSq (tw ε c) = GaussRat.normSq c := by
  rcases hε with rfl | rfl
  · rw [tw_one]
  · rw [tw_neg_one, normSq_star]

theorem twist_smul {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (c : GaussRat) (x : Fin n → GaussRat) :
    twist ε (c • x) = tw ε c • twist ε x := by
  funext i
  simp only [twist_apply, Pi.smul_apply, smul_eq_mul]
  exact tw_mul hε c (x i)

theorem twist_add (ε : ℚ) (x y : Fin n → GaussRat) : twist ε (x + y) = twist ε x + twist ε y := by
  funext i
  ext <;> simp [twist_apply, tw]
  ring

theorem twist_e (ε : ℚ) (i : Fin n) : twist ε (e i) = e i := by
  funext j
  rw [twist_apply, e_apply]
  split_ifs
  · exact tw_one' ε
  · ext <;> simp [tw]

theorem twist_eq_zero_iff {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (x : Fin n → GaussRat) :
    twist ε x = 0 ↔ x = 0 := by
  rcases hε with rfl | rfl
  · rw [twist_one]
  · rw [twist_neg_one, star_eq_zero]

theorem tp_twist {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (x y : Fin n → GaussRat) :
    tp (twist ε x) (twist ε y) = tp x y := by
  rcases hε with rfl | rfl
  · rw [twist_one, twist_one]
  · rw [twist_neg_one, twist_neg_one, tp_star_star]

theorem vnorm_twist {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (x : Fin n → GaussRat) :
    vnorm (twist ε x) = vnorm x := by
  rcases hε with rfl | rfl
  · rw [twist_one]
  · rw [twist_neg_one, vnorm_star]

/-! ### Similarities: `Fᴴ F = d • 1` -/

/-- `F` is a similarity with scale `d`: `Fᴴ * F = d • 1`. -/
def Similarity (F : Matrix (Fin n) (Fin n) GaussRat) (d : ℚ) : Prop :=
  Fᴴ * F = d • (1 : Matrix (Fin n) (Fin n) GaussRat)

theorem ip_mulVec_mulVec (F : Matrix (Fin n) (Fin n) GaussRat) (x y : Fin n → GaussRat) :
    ip (F *ᵥ x) (F *ᵥ y) = star x ⬝ᵥ ((Fᴴ * F) *ᵥ y) := by
  unfold ip
  rw [star_mulVec, ← dotProduct_mulVec, mulVec_mulVec]

theorem Similarity.ip_mulVec {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (x y : Fin n → GaussRat) : ip (F *ᵥ x) (F *ᵥ y) = d • ip x y := by
  rw [ip_mulVec_mulVec, h, smul_mulVec, one_mulVec, dotProduct_smul]
  rfl

theorem Similarity.vnorm_mulVec {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (x : Fin n → GaussRat) : vnorm (F *ᵥ x) = d * vnorm x := by
  rw [← ip_self_re, h.ip_mulVec, GaussRat.re_smul, ip_self_re]

theorem Similarity.tp_mulVec {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (hd : d ≠ 0) (x y : Fin n → GaussRat) : tp (F *ᵥ x) (F *ᵥ y) = tp x y := by
  unfold tp
  rw [h.ip_mulVec, h.vnorm_mulVec, h.vnorm_mulVec, normSq_smul]
  have : d * vnorm x * (d * vnorm y) = d ^ 2 * (vnorm x * vnorm y) := by ring
  rw [this]
  exact mul_div_mul_left _ _ (pow_ne_zero 2 hd)

theorem Similarity.mulVec_eq_zero_iff {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ}
    (h : Similarity F d) (hd : d ≠ 0) (x : Fin n → GaussRat) : F *ᵥ x = 0 ↔ x = 0 := by
  constructor
  · intro hx
    have := h.vnorm_mulVec x
    rw [hx, vnorm_zero] at this
    exact (vnorm_eq_zero_iff x).mp (by
      rcases mul_eq_zero.mp this.symm with h0 | h0
      · exact absurd h0 hd
      · exact h0)
  · intro hx
    rw [hx, mulVec_zero]

theorem Similarity.mulVec_ne_zero {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ}
    (h : Similarity F d) (hd : d ≠ 0) {x : Fin n → GaussRat} (hx : x ≠ 0) : F *ᵥ x ≠ 0 :=
  fun h0 => hx ((h.mulVec_eq_zero_iff hd x).mp h0)

/-- The scale of a similarity on a nonempty carrier is nonnegative; it is positive when `n ≥ 1`. -/
theorem Similarity.scale_pos {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (hd : d ≠ 0) (i : Fin n) : 0 < d := by
  have := h.vnorm_mulVec (e i)
  rw [vnorm_e, mul_one] at this
  rw [← this]
  exact vnorm_pos (h.mulVec_ne_zero hd (e_ne_zero i))

/-- A similarity is invertible: `F * ((1/d) • Fᴴ) = 1` and `((1/d) • Fᴴ) * F = 1`. -/
theorem Similarity.left_inverse {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (hd : d ≠ 0) : ((1 / d) • Fᴴ) * F = 1 := by
  rw [smul_mul, h, smul_smul, one_div_mul_cancel hd, one_smul]

theorem Similarity.right_inverse {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (hd : d ≠ 0) : F * ((1 / d) • Fᴴ) = 1 :=
  mul_eq_one_comm.mp (h.left_inverse hd)

theorem conjTranspose_qsmul (q : ℚ) (M : Matrix (Fin n) (Fin n) GaussRat) : (q • M)ᴴ = q • Mᴴ := by
  refine Matrix.ext fun i j => ?_
  rw [conjTranspose_apply, Matrix.smul_apply, Matrix.smul_apply, conjTranspose_apply]
  ext <;> simp

/-- `F * Fᴴ = d • 1` as well. -/
theorem Similarity.mul_conjTranspose {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ}
    (h : Similarity F d) (hd : d ≠ 0) : F * Fᴴ = d • (1 : Matrix (Fin n) (Fin n) GaussRat) := by
  have h1 := h.right_inverse hd
  rw [Matrix.mul_smul] at h1
  calc F * Fᴴ = d • ((1 / d) • (F * Fᴴ)) := by
        rw [smul_smul, mul_one_div_cancel hd, one_smul]
    _ = d • (1 : Matrix (Fin n) (Fin n) GaussRat) := by rw [h1]

/-- The inverse of a similarity with scale `d` is a similarity with scale `1 / d`. -/
theorem Similarity.inverse {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (h : Similarity F d)
    (hd : d ≠ 0) : Similarity ((1 / d) • Fᴴ) (1 / d) := by
  unfold Similarity
  rw [conjTranspose_qsmul, conjTranspose_conjTranspose, smul_mul, Matrix.mul_smul, smul_smul,
    h.mul_conjTranspose hd, smul_smul]
  congr 1
  field_simp

theorem Similarity.one : Similarity (1 : Matrix (Fin n) (Fin n) GaussRat) 1 := by
  unfold Similarity
  rw [conjTranspose_one, Matrix.mul_one, one_smul]

/-! ### Column matrices and the orthogonal expansion -/

/-- The matrix whose `i`-th column is `f i`. -/
def colMatrix (f : Fin n → Fin n → GaussRat) : Matrix (Fin n) (Fin n) GaussRat :=
  Matrix.of fun r i => f i r

theorem colMatrix_apply (f : Fin n → Fin n → GaussRat) (r i : Fin n) : colMatrix f r i = f i r := rfl

theorem colMatrix_mulVec_apply (f : Fin n → Fin n → GaussRat) (z : Fin n → GaussRat) (r : Fin n) :
    (colMatrix f *ᵥ z) r = ∑ i, f i r * z i := by
  rw [mulVec_apply_eq_sum]
  rfl

theorem colMatrix_mulVec (f : Fin n → Fin n → GaussRat) (z : Fin n → GaussRat) :
    colMatrix f *ᵥ z = ∑ i, z i • f i := by
  funext r
  rw [colMatrix_mulVec_apply, Finset.sum_apply]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Pi.smul_apply, smul_eq_mul, mul_comm]

theorem colMatrix_mulVec_e (f : Fin n → Fin n → GaussRat) (i : Fin n) : colMatrix f *ᵥ e i = f i := by
  rw [e, mulVec_single', one_smul]
  funext r
  rfl

theorem colMatrix_mulVec_single (f : Fin n → Fin n → GaussRat) (i : Fin n) (t : GaussRat) :
    colMatrix f *ᵥ Pi.single i t = t • f i := by
  rw [mulVec_single']
  rfl

theorem conjTranspose_colMatrix_mulVec_apply (f : Fin n → Fin n → GaussRat) (y : Fin n → GaussRat)
    (i : Fin n) : ((colMatrix f)ᴴ *ᵥ y) i = ip (f i) y := by
  rw [mulVec_apply_eq_sum, ip_eq_sum]
  rfl

theorem gram_colMatrix (f : Fin n → Fin n → GaussRat) (i j : Fin n) :
    ((colMatrix f)ᴴ * colMatrix f) i j = ip (f i) (f j) := by
  rw [Matrix.mul_apply, ip_eq_sum]
  rfl

/-- The Gram matrix of a pairwise orthogonal family is the diagonal of the squared norms. -/
theorem gram_eq_diagonal {f : Fin n → Fin n → GaussRat} (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0) :
    (colMatrix f)ᴴ * colMatrix f = Matrix.diagonal fun i => ((vnorm (f i) : ℚ) : GaussRat) := by
  refine Matrix.ext fun i j => ?_
  rw [gram_colMatrix]
  by_cases h : i = j
  · subst h
    rw [Matrix.diagonal_apply_eq, ip_self_eq]
  · rw [Matrix.diagonal_apply_ne _ h, horth i j h]

/-- The inner product of two expansions in an orthogonal family. -/
theorem ip_colMatrix_mulVec {f : Fin n → Fin n → GaussRat} (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0)
    (z w : Fin n → GaussRat) :
    ip (colMatrix f *ᵥ z) (colMatrix f *ᵥ w) = ∑ i, star (z i) * (((vnorm (f i) : ℚ) : GaussRat) * w i) := by
  rw [ip_mulVec_mulVec, gram_eq_diagonal horth]
  simp only [dotProduct, Pi.star_apply, mulVec_diagonal]

theorem vnorm_colMatrix_mulVec {f : Fin n → Fin n → GaussRat}
    (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0) (z : Fin n → GaussRat) :
    vnorm (colMatrix f *ᵥ z) = ∑ i, vnorm (f i) * GaussRat.normSq (z i) := by
  rw [← ip_self_re, ip_colMatrix_mulVec horth, GaussRat.re_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [ratCast_mul, mul_smul_comm, GaussRat.re_smul, GaussRat.re_star_mul_self]

theorem ip_f_colMatrix_mulVec {f : Fin n → Fin n → GaussRat}
    (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0) (k : Fin n) (z : Fin n → GaussRat) :
    ip (f k) (colMatrix f *ᵥ z) = ((vnorm (f k) : ℚ) : GaussRat) * z k := by
  have h1 : ip (f k) (colMatrix f *ᵥ z) = ip (colMatrix f *ᵥ e k) (colMatrix f *ᵥ z) := by
    rw [colMatrix_mulVec_e]
  rw [h1, ip_colMatrix_mulVec horth, Finset.sum_eq_single k]
  · rw [e_apply_self, star_one, one_mul]
  · intro i _ hi
    rw [e_apply_ne hi, star_zero, zero_mul]
  · intro h
    exact absurd (Finset.mem_univ k) h

/-- Coordinates of `y` in a pairwise orthogonal family: `(1 / ‖f i‖²) ⟨f i, y⟩`. -/
def coords (f : Fin n → Fin n → GaussRat) (y : Fin n → GaussRat) : Fin n → GaussRat :=
  fun i => (vnorm (f i))⁻¹ • ip (f i) y

theorem coords_apply (f : Fin n → Fin n → GaussRat) (y : Fin n → GaussRat) (i : Fin n) :
    coords f y i = (vnorm (f i))⁻¹ • ip (f i) y := rfl

theorem coords_eq (f : Fin n → Fin n → GaussRat) (y : Fin n → GaussRat) :
    coords f y = Matrix.diagonal (fun i => (((vnorm (f i))⁻¹ : ℚ) : GaussRat)) *ᵥ ((colMatrix f)ᴴ *ᵥ y) := by
  funext i
  rw [mulVec_diagonal, conjTranspose_colMatrix_mulVec_apply, coords_apply, ratCast_mul]

/-- Orthogonal expansion: every vector is the `colMatrix`-image of its coordinates in a pairwise
orthogonal family of `n` nonzero vectors. -/
theorem expansion {f : Fin n → Fin n → GaussRat} (hf : ∀ i, f i ≠ 0)
    (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0) (y : Fin n → GaussRat) :
    y = colMatrix f *ᵥ coords f y := by
  set D : Matrix (Fin n) (Fin n) GaussRat :=
    Matrix.diagonal (fun i => (((vnorm (f i))⁻¹ : ℚ) : GaussRat)) with hD
  have hleft : (D * (colMatrix f)ᴴ) * colMatrix f = 1 := by
    rw [Matrix.mul_assoc, gram_eq_diagonal horth, hD, diagonal_mul_diagonal]
    rw [← diagonal_one]
    congr 1
    funext i
    rw [← Rat.cast_mul, inv_mul_cancel₀ (vnorm_ne_zero (hf i)), Rat.cast_one]
  have hright : colMatrix f * (D * (colMatrix f)ᴴ) = 1 := mul_eq_one_comm.mp hleft
  rw [coords_eq, mulVec_mulVec, mulVec_mulVec, Matrix.mul_assoc, ← hD, hright, one_mulVec]

theorem ip_f_eq_vnorm_mul_coords {f : Fin n → Fin n → GaussRat} (hf : ∀ i, f i ≠ 0)
    (y : Fin n → GaussRat) (k : Fin n) : ip (f k) y = ((vnorm (f k) : ℚ) : GaussRat) * coords f y k := by
  rw [coords_apply, ratCast_mul, smul_smul, mul_inv_cancel₀ (vnorm_ne_zero (hf k)), one_smul]

theorem coords_eq_zero_iff {f : Fin n → Fin n → GaussRat} (hf : ∀ i, f i ≠ 0) (y : Fin n → GaussRat)
    (k : Fin n) : coords f y k = 0 ↔ ip (f k) y = 0 := by
  rw [ip_f_eq_vnorm_mul_coords hf, mul_eq_zero]
  constructor
  · exact Or.inr
  · rintro (h | h)
    · exact absurd h (ratCast_ne_zero (vnorm_ne_zero (hf k)))
    · exact h

/-- A pairwise orthogonal family of `n` vectors of common squared norm `d ≠ 0` has a similarity with
scale `d` as column matrix. -/
theorem similarity_colMatrix {f : Fin n → Fin n → GaussRat} {d : ℚ}
    (horth : ∀ i j, i ≠ j → ip (f i) (f j) = 0) (hnorm : ∀ i, vnorm (f i) = d) :
    Similarity (colMatrix f) d := by
  unfold Similarity
  rw [gram_eq_diagonal horth]
  refine Matrix.ext fun i j => ?_
  by_cases h : i = j
  · subst h
    rw [Matrix.diagonal_apply_eq, Matrix.smul_apply, Matrix.one_apply_eq, hnorm]
    ext <;> simp
  · rw [Matrix.diagonal_apply_ne _ h, Matrix.smul_apply, Matrix.one_apply_ne h, smul_zero]

theorem coords_of_similarity {f : Fin n → Fin n → GaussRat} {d : ℚ} (hnorm : ∀ i, vnorm (f i) = d)
    (y : Fin n → GaussRat) (k : Fin n) : coords f y k = d⁻¹ • ip (f k) y := by
  rw [coords_apply, hnorm]

end WignerFinite.Kernel

#print axioms WignerFinite.Kernel.normSq_star
#print axioms WignerFinite.Kernel.normSq_smul
#print axioms WignerFinite.Kernel.normSq_ratCast
#print axioms WignerFinite.Kernel.normSq_I
#print axioms WignerFinite.Kernel.normSq_one_add
#print axioms WignerFinite.Kernel.ratCast_mul
#print axioms WignerFinite.Kernel.ratCast_ne_zero
#print axioms WignerFinite.Kernel.re_mul_star_self
#print axioms WignerFinite.Kernel.mul_self_eq_one_iff'
#print axioms WignerFinite.Kernel.ip
#print axioms WignerFinite.Kernel.ip_def
#print axioms WignerFinite.Kernel.ip_eq_sum
#print axioms WignerFinite.Kernel.star_ip
#print axioms WignerFinite.Kernel.ip_add_left
#print axioms WignerFinite.Kernel.ip_add_right
#print axioms WignerFinite.Kernel.ip_smul_right
#print axioms WignerFinite.Kernel.ip_smul_left
#print axioms WignerFinite.Kernel.ip_star_star
#print axioms WignerFinite.Kernel.ip_self_re
#print axioms WignerFinite.Kernel.ip_self_im
#print axioms WignerFinite.Kernel.ip_self_eq
#print axioms WignerFinite.Kernel.normSq_ip_self
#print axioms WignerFinite.Kernel.vnorm_add
#print axioms WignerFinite.Kernel.vnorm_smul
#print axioms WignerFinite.Kernel.vnorm_star
#print axioms WignerFinite.Kernel.vnorm_ne_zero
#print axioms WignerFinite.Kernel.ne_zero_of_vnorm_ne_zero
#print axioms WignerFinite.Kernel.ip_ne_zero_left
#print axioms WignerFinite.Kernel.ip_ne_zero_right
#print axioms WignerFinite.Kernel.e
#print axioms WignerFinite.Kernel.e_apply
#print axioms WignerFinite.Kernel.e_apply_self
#print axioms WignerFinite.Kernel.e_apply_ne
#print axioms WignerFinite.Kernel.ip_e_left
#print axioms WignerFinite.Kernel.ip_e_right
#print axioms WignerFinite.Kernel.vnorm_e
#print axioms WignerFinite.Kernel.e_ne_zero
#print axioms WignerFinite.Kernel.ip_e_e
#print axioms WignerFinite.Kernel.ip_e_e_of_ne
#print axioms WignerFinite.Kernel.eq_sum_smul_e
#print axioms WignerFinite.Kernel.tp
#print axioms WignerFinite.Kernel.tp_def
#print axioms WignerFinite.Kernel.tp_comm
#print axioms WignerFinite.Kernel.tp_smul_left
#print axioms WignerFinite.Kernel.tp_smul_right
#print axioms WignerFinite.Kernel.tp_self
#print axioms WignerFinite.Kernel.tp_nonneg
#print axioms WignerFinite.Kernel.tp_le_one
#print axioms WignerFinite.Kernel.tp_eq_zero_iff
#print axioms WignerFinite.Kernel.tp_star_star
#print axioms WignerFinite.Kernel.tp_e_e
#print axioms WignerFinite.Kernel.vnorm_smul_sub_smul
#print axioms WignerFinite.Kernel.eq_smul_of_normSq_ip_eq
#print axioms WignerFinite.Kernel.tp_eq_one_iff
#print axioms WignerFinite.Kernel.tp_eq_born
#print axioms WignerFinite.Kernel.tw
#print axioms WignerFinite.Kernel.twist
#print axioms WignerFinite.Kernel.twist_apply
#print axioms WignerFinite.Kernel.tw_one
#print axioms WignerFinite.Kernel.tw_neg_one
#print axioms WignerFinite.Kernel.twist_one
#print axioms WignerFinite.Kernel.twist_neg_one
#print axioms WignerFinite.Kernel.tw_tw
#print axioms WignerFinite.Kernel.twist_twist
#print axioms WignerFinite.Kernel.tw_mul
#print axioms WignerFinite.Kernel.tw_one'
#print axioms WignerFinite.Kernel.tw_ratCast
#print axioms WignerFinite.Kernel.tw_eq_zero_iff
#print axioms WignerFinite.Kernel.tw_ne_zero
#print axioms WignerFinite.Kernel.normSq_tw
#print axioms WignerFinite.Kernel.twist_smul
#print axioms WignerFinite.Kernel.twist_add
#print axioms WignerFinite.Kernel.twist_e
#print axioms WignerFinite.Kernel.twist_eq_zero_iff
#print axioms WignerFinite.Kernel.tp_twist
#print axioms WignerFinite.Kernel.vnorm_twist
#print axioms WignerFinite.Kernel.Similarity
#print axioms WignerFinite.Kernel.ip_mulVec_mulVec
#print axioms WignerFinite.Kernel.Similarity.ip_mulVec
#print axioms WignerFinite.Kernel.Similarity.vnorm_mulVec
#print axioms WignerFinite.Kernel.Similarity.tp_mulVec
#print axioms WignerFinite.Kernel.Similarity.mulVec_eq_zero_iff
#print axioms WignerFinite.Kernel.Similarity.mulVec_ne_zero
#print axioms WignerFinite.Kernel.Similarity.scale_pos
#print axioms WignerFinite.Kernel.Similarity.left_inverse
#print axioms WignerFinite.Kernel.Similarity.right_inverse
#print axioms WignerFinite.Kernel.conjTranspose_qsmul
#print axioms WignerFinite.Kernel.Similarity.mul_conjTranspose
#print axioms WignerFinite.Kernel.Similarity.inverse
#print axioms WignerFinite.Kernel.Similarity.one
#print axioms WignerFinite.Kernel.colMatrix
#print axioms WignerFinite.Kernel.colMatrix_apply
#print axioms WignerFinite.Kernel.colMatrix_mulVec_apply
#print axioms WignerFinite.Kernel.colMatrix_mulVec
#print axioms WignerFinite.Kernel.colMatrix_mulVec_e
#print axioms WignerFinite.Kernel.colMatrix_mulVec_single
#print axioms WignerFinite.Kernel.conjTranspose_colMatrix_mulVec_apply
#print axioms WignerFinite.Kernel.gram_colMatrix
#print axioms WignerFinite.Kernel.gram_eq_diagonal
#print axioms WignerFinite.Kernel.ip_colMatrix_mulVec
#print axioms WignerFinite.Kernel.vnorm_colMatrix_mulVec
#print axioms WignerFinite.Kernel.ip_f_colMatrix_mulVec
#print axioms WignerFinite.Kernel.coords
#print axioms WignerFinite.Kernel.coords_apply
#print axioms WignerFinite.Kernel.coords_eq
#print axioms WignerFinite.Kernel.expansion
#print axioms WignerFinite.Kernel.ip_f_eq_vnorm_mul_coords
#print axioms WignerFinite.Kernel.coords_eq_zero_iff
#print axioms WignerFinite.Kernel.similarity_colMatrix
#print axioms WignerFinite.Kernel.coords_of_similarity
