import FiniteWignerKernel

/-
The finite exact Wigner theorem over ℚ(i)ⁿ.  AuthorityEffect: None.

Statement (`finite_wigner`).  Let `T` map the Gaussian-rational carrier `Fin n → ℚ(i)` to itself,
send nonzero vectors to nonzero vectors, and preserve the transition probability
`tp x y = |⟨x, y⟩|² / (‖x‖² ‖y‖²)` between nonzero vectors (`TpPreserving`).  Fix a sector `i₀`.
Then there are a similarity `F` (`Fᴴ F = d • 1`, `d > 0` rational) and a sign `ε ∈ {1, −1}` such
that for every nonzero `x` there is a nonzero scalar `μ` with `T x = μ • (F *ᵥ twist ε x)`:
`T` is induced on rays by a ℚ(i)-linear similarity (`ε = 1`) or by componentwise conjugation
followed by a ℚ(i)-linear similarity (`ε = −1`, `finite_wigner_cases`).  No continuity hypothesis
appears: the dichotomy `z = x` or `z = star x` for the coordinates is forced coordinatewise by two
modulus equations (`coord_rigidity`), and consistency of the sign across coordinates by one more
probe (`sgn_consistent`).  Conversely every such map preserves `tp` (`tpPreserving_of_similarity`).

Proof (Bargmann-type, exact).  Images of the sector basis are nonzero and pairwise orthogonal
(`ip_g_g`); the images of the probes `e i₀ + e j` align the phases and norms of the basis images
(`f`, `vnorm_f`, `T_p_eq`); the images of the probes `e i₀ + i e j` carry a sign `sgn j ∈ {±1}`
(`sgn_spec`); the probe `e i₀ + i e j + i e k` forces all signs equal (`sgn_consistent`); vectors
with `x i₀ ≠ 0` are handled by coordinate rigidity against the three probe families (`stage1`),
vectors with `x i₀ = 0` by the probe `e i₀ + x` and the equality case of Cauchy–Schwarz (`stage2`).

Not claimed: that the scale `d` is a norm from ℚ(i) (so that `F` rescales to a unitary); see
`FiniteWignerSimilarity` for the exact statement and the countermodel `d = 3`.  The carrier, the
scalar field and the transition probability (the Born readout of rank-one effects) are supplied.
-/

namespace WignerFable.Theorem

open Matrix BornFable BornFable.HermitianCarrier BornFable.HermitianPsd WignerFable.Kernel

variable {n : ℕ}

/-- A map preserving transition probabilities between nonzero vectors (and nonvanishing). -/
structure TpPreserving (T : (Fin n → GaussRat) → (Fin n → GaussRat)) : Prop where
  ne_zero : ∀ x, x ≠ 0 → T x ≠ 0
  tp_eq : ∀ x y, x ≠ 0 → y ≠ 0 → tp (T x) (T y) = tp x y

/-! ### Probe vectors -/

/-- The probe `e i₀ + e j`. -/
def p (i₀ j : Fin n) : Fin n → GaussRat := e i₀ + e j

/-- The probe `e i₀ + (s i) e j`. -/
def qs (i₀ : Fin n) (s : ℚ) (j : Fin n) : Fin n → GaussRat := e i₀ + (s • GaussRat.I) • e j

theorem star_smul_I (s : ℚ) : star (s • GaussRat.I) = -(s • GaussRat.I) := by
  ext <;> simp

theorem normSq_smul_I {s : ℚ} (hs : s = 1 ∨ s = -1) : GaussRat.normSq (s • GaussRat.I) = 1 := by
  rw [normSq_smul, normSq_I]
  rcases hs with rfl | rfl <;> norm_num

theorem ip_p_left (i₀ j : Fin n) (y : Fin n → GaussRat) : ip (p i₀ j) y = y i₀ + y j := by
  rw [p, ip_add_left, ip_e_left, ip_e_left]

theorem ip_qs_left (i₀ : Fin n) (s : ℚ) (j : Fin n) (y : Fin n → GaussRat) :
    ip (qs i₀ s j) y = y i₀ - (s • GaussRat.I) * y j := by
  rw [qs, ip_add_left, ip_smul_left, ip_e_left, ip_e_left, star_smul_I, neg_mul, sub_eq_add_neg]

theorem p_apply (i₀ j m : Fin n) : p i₀ j m = e i₀ m + e j m := rfl

theorem qs_apply (i₀ : Fin n) (s : ℚ) (j m : Fin n) :
    qs i₀ s j m = e i₀ m + (s • GaussRat.I) * e j m := rfl

theorem vnorm_p {i₀ j : Fin n} (h : j ≠ i₀) : vnorm (p i₀ j) = 2 := by
  rw [p, vnorm_add, vnorm_e, vnorm_e, ip_e_e_of_ne (Ne.symm h), GaussRat.re_zero]
  norm_num

theorem vnorm_qs {i₀ j : Fin n} (h : j ≠ i₀) {s : ℚ} (hs : s = 1 ∨ s = -1) :
    vnorm (qs i₀ s j) = 2 := by
  rw [qs, vnorm_add, vnorm_e, vnorm_smul, vnorm_e, ip_smul_right, ip_e_e_of_ne (Ne.symm h),
    mul_zero, GaussRat.re_zero, normSq_smul_I hs]
  norm_num

theorem p_ne_zero {i₀ j : Fin n} (h : j ≠ i₀) : p i₀ j ≠ 0 :=
  ne_zero_of_vnorm_ne_zero (by rw [vnorm_p h]; norm_num)

theorem qs_ne_zero {i₀ j : Fin n} (h : j ≠ i₀) {s : ℚ} (hs : s = 1 ∨ s = -1) : qs i₀ s j ≠ 0 :=
  ne_zero_of_vnorm_ne_zero (by rw [vnorm_qs h hs]; norm_num)

theorem p_apply_i₀ {i₀ j : Fin n} (h : j ≠ i₀) : p i₀ j i₀ = 1 := by
  rw [p_apply, e_apply_self, e_apply_ne (Ne.symm h), add_zero]

theorem p_apply_j {i₀ j : Fin n} (h : j ≠ i₀) : p i₀ j j = 1 := by
  rw [p_apply, e_apply_self, e_apply_ne h, zero_add]

theorem p_apply_other {i₀ j m : Fin n} (h₀ : m ≠ i₀) (h₁ : m ≠ j) : p i₀ j m = 0 := by
  rw [p_apply, e_apply_ne h₀, e_apply_ne h₁, add_zero]

theorem qs_apply_i₀ {i₀ j : Fin n} (h : j ≠ i₀) (s : ℚ) : qs i₀ s j i₀ = 1 := by
  rw [qs_apply, e_apply_self, e_apply_ne (Ne.symm h), mul_zero, add_zero]

theorem qs_apply_j {i₀ j : Fin n} (h : j ≠ i₀) (s : ℚ) : qs i₀ s j j = s • GaussRat.I := by
  rw [qs_apply, e_apply_self, e_apply_ne h, mul_one, zero_add]

theorem qs_apply_other {i₀ j m : Fin n} (h₀ : m ≠ i₀) (h₁ : m ≠ j) (s : ℚ) : qs i₀ s j m = 0 := by
  rw [qs_apply, e_apply_ne h₀, e_apply_ne h₁, mul_zero, add_zero]

theorem tp_e_left (m : Fin n) (y : Fin n → GaussRat) :
    tp (e m) y = GaussRat.normSq (y m) / vnorm y := by
  unfold tp
  rw [ip_e_left, vnorm_e, one_mul]

/-- Rescaling `x` to `x i₀ = 1`. -/
theorem smul_inv_apply_self {x : Fin n → GaussRat} {i₀ : Fin n} (hx : x i₀ ≠ 0) :
    ((x i₀)⁻¹ • x) i₀ = 1 := by
  rw [Pi.smul_apply, smul_eq_mul, inv_mul_cancel₀ hx]

/-! ### Scalar and probe lemmas (no map involved) -/

theorem normSq_inv (a : GaussRat) : GaussRat.normSq a⁻¹ = (GaussRat.normSq a)⁻¹ := by
  have : a⁻¹ = (GaussRat.normSq a)⁻¹ • star a := rfl
  rw [this, normSq_smul, normSq_star]
  by_cases ha : GaussRat.normSq a = 0
  · rw [ha]
    simp
  · field_simp

theorem normSq_div (a b : GaussRat) : GaussRat.normSq (a / b) = GaussRat.normSq a / GaussRat.normSq b := by
  rw [div_eq_mul_inv, GaussRat.normSq_mul, normSq_inv, div_eq_mul_inv]

theorem vnorm_add_of_ip_zero {x y : Fin n → GaussRat} (h : ip x y = 0) :
    vnorm (x + y) = vnorm x + vnorm y := by
  rw [vnorm_add, h, GaussRat.re_zero, mul_zero, add_zero]

theorem tp_e_qs {i₀ j : Fin n} (hj : j ≠ i₀) : tp (e i₀) (qs i₀ 1 j) = 1 / 2 := by
  rw [tp_e_left, qs_apply_i₀ hj, normSq_one, vnorm_qs hj (Or.inl rfl)]

theorem tp_ej_qs {i₀ j : Fin n} (hj : j ≠ i₀) : tp (e j) (qs i₀ 1 j) = 1 / 2 := by
  rw [tp_e_left, qs_apply_j hj, normSq_smul_I (Or.inl rfl), vnorm_qs hj (Or.inl rfl)]

theorem tp_p_qs {i₀ j : Fin n} (hj : j ≠ i₀) : tp (p i₀ j) (qs i₀ 1 j) = 1 / 2 := by
  unfold tp
  rw [ip_p_left, qs_apply_i₀ hj, qs_apply_j hj, vnorm_p hj, vnorm_qs hj (Or.inl rfl), one_smul]
  simp [GaussRat.normSq]
  norm_num

/-- From `|u|² = 1` and `|1 + u|² = 2`: `u = ± i`. -/
theorem eq_smul_I_of_normSq {u : GaussRat} (h1 : GaussRat.normSq u = 1)
    (h2 : GaussRat.normSq (1 + u) = 2) : u = u.im • GaussRat.I ∧ (u.im = 1 ∨ u.im = -1) := by
  rw [normSq_one_add, h1] at h2
  have hre : u.re = 0 := by linarith
  have him : u.im * u.im = 1 := by
    have := h1
    simp only [GaussRat.normSq, hre] at this
    nlinarith
  refine ⟨?_, mul_self_eq_one_iff.mp him⟩
  ext <;> simp [hre]

/-! ### Coordinate rigidity -/

theorem normSq_ip_qs {i₀ : Fin n} (j : Fin n) (s : ℚ) {x : Fin n → GaussRat} (hx : x i₀ = 1) :
    GaussRat.normSq (ip (qs i₀ s j) x) = (1 + s * (x j).im) ^ 2 + (s * (x j).re) ^ 2 := by
  rw [ip_qs_left, hx]
  simp only [GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub, GaussRat.re_mul, GaussRat.im_mul,
    GaussRat.re_smul, GaussRat.im_smul, GaussRat.re_I, GaussRat.im_I, GaussRat.re_one, GaussRat.im_one]
  ring

theorem normSq_ip_p {i₀ j : Fin n} {x : Fin n → GaussRat} (hx : x i₀ = 1) :
    GaussRat.normSq (ip (p i₀ j) x) = (1 + (x j).re) ^ 2 + (x j).im ^ 2 := by
  rw [ip_p_left, hx]
  simp only [GaussRat.normSq, GaussRat.re_add, GaussRat.im_add, GaussRat.re_one, GaussRat.im_one]
  ring

/-- Against the three probe families, the coordinate `m` of a normalised vector is determined up to
the sign `s`: `z m = tw s (x m)`. -/
theorem coord_rigidity {x z : Fin n → GaussRat} {i₀ m : Fin n} (hm : m ≠ i₀) (hx0 : x i₀ = 1)
    (hz0 : z i₀ = 1) (hN : vnorm z = vnorm x) {s : ℚ} (hs : s = 1 ∨ s = -1)
    (ha : tp (e m) x = tp (e m) z) (hb : tp (p i₀ m) x = tp (p i₀ m) z)
    (hc : tp (qs i₀ 1 m) x = tp (qs i₀ s m) z) : z m = tw s (x m) := by
  have hxN : vnorm x ≠ 0 := vnorm_ne_zero (fun h0 => by
    have := congrFun h0 i₀
    rw [hx0, Pi.zero_apply] at this
    exact one_ne_zero this)
  rw [tp_e_left, tp_e_left, hN] at ha
  have E1 : GaussRat.normSq (z m) = GaussRat.normSq (x m) := by
    have := ha
    field_simp at this
    linear_combination -this
  unfold tp at hb hc
  rw [vnorm_p hm, hN, normSq_ip_p hx0, normSq_ip_p hz0] at hb
  rw [vnorm_qs hm (Or.inl rfl), vnorm_qs hm hs, hN, normSq_ip_qs m 1 hx0, normSq_ip_qs m s hz0] at hc
  have E2 : (1 + (z m).re) ^ 2 + (z m).im ^ 2 = (1 + (x m).re) ^ 2 + (x m).im ^ 2 := by
    field_simp at hb
    linear_combination -hb
  have E3 : (1 + s * (z m).im) ^ 2 + (s * (z m).re) ^ 2 = (1 + 1 * (x m).im) ^ 2 + (1 * (x m).re) ^ 2 := by
    field_simp at hc
    linear_combination -hc
  have hss : s * s = 1 := by rcases hs with rfl | rfl <;> norm_num
  simp only [GaussRat.normSq] at E1
  have hre : (z m).re = (x m).re := by linear_combination (E2 - E1) / 2
  have him : (z m).im = s * (x m).im := by
    have h3 : s * (z m).im = (x m).im := by
      linear_combination (E3 - s ^ 2 * E1 - ((x m).re ^ 2 + (x m).im ^ 2) * hss) / 2
    linear_combination s * h3 - (z m).im * hss
  ext
  · rw [tw_re, hre]
  · rw [tw_im, him]

/-- A coordinate of a normalised `z` vanishes where `x` vanishes. -/
theorem coord_zero {x z : Fin n → GaussRat} {m : Fin n} (hN : vnorm z = vnorm x) (hxN : vnorm x ≠ 0)
    (ha : tp (e m) x = tp (e m) z) (hxm : x m = 0) : z m = 0 := by
  rw [tp_e_left, tp_e_left, hN, hxm, (GaussRat.normSq_eq_zero_iff 0).mpr rfl, zero_div] at ha
  rcases div_eq_zero_iff.mp ha.symm with h | h
  · exact (GaussRat.normSq_eq_zero_iff _).mp h
  · exact absurd h hxN

/-! ### Images of the sector basis -/

section Construction

variable (T : (Fin n → GaussRat) → (Fin n → GaussRat)) (i₀ : Fin n)

/-- The image of the sector basis. -/
def g (i : Fin n) : Fin n → GaussRat := T (e i)

/-- The alignment scalars: `1` at `i₀`, otherwise the ratio of the two coordinates of
`T (e i₀ + e k)` in the basis `g`. -/
def align (k : Fin n) : GaussRat :=
  if k = i₀ then 1 else coords (g T) (T (p i₀ k)) k / coords (g T) (T (p i₀ k)) i₀

/-- The aligned orthogonal basis `f k = align k • g k`. -/
def f (k : Fin n) : Fin n → GaussRat := align T i₀ k • g T k

/-- The reconstructed similarity: the column matrix of `f`. -/
def F : Matrix (Fin n) (Fin n) GaussRat := colMatrix (f T i₀)

/-- The scale `d = ‖T (e i₀)‖²`. -/
def d : ℚ := vnorm (g T i₀)

/-- The sign carried by the probe `e i₀ + i e j`. -/
def sgn (j : Fin n) : ℚ :=
  (coords (f T i₀) (T (qs i₀ 1 j)) j / coords (f T i₀) (T (qs i₀ 1 j)) i₀).im

theorem align_i₀ : align T i₀ i₀ = 1 := by
  simp [align]

theorem align_of_ne {k : Fin n} (h : k ≠ i₀) :
    align T i₀ k = coords (g T) (T (p i₀ k)) k / coords (g T) (T (p i₀ k)) i₀ := by
  simp [align, h]

theorem f_i₀ : f T i₀ i₀ = g T i₀ := by
  rw [f, align_i₀, one_smul]

theorem F_mulVec_e (k : Fin n) : F T i₀ *ᵥ e k = f T i₀ k := colMatrix_mulVec_e _ k

end Construction

section Proof

variable {T : (Fin n → GaussRat) → (Fin n → GaussRat)} (hT : TpPreserving T) {i₀ : Fin n}
include hT

theorem g_ne_zero (i : Fin n) : g T i ≠ 0 := hT.ne_zero _ (e_ne_zero i)

theorem ip_g_g {i j : Fin n} (h : i ≠ j) : ip (g T i) (g T j) = 0 := by
  have := hT.tp_eq (e i) (e j) (e_ne_zero i) (e_ne_zero j)
  rw [tp_e_e, ite_eq_right_iff.mpr (fun h' => absurd h' h)] at this
  exact (tp_eq_zero_iff (g_ne_zero hT i) (g_ne_zero hT j)).mp this

theorem d_pos : 0 < d T i₀ := vnorm_pos (g_ne_zero hT i₀)

theorem d_ne_zero : d T i₀ ≠ 0 := (d_pos hT).ne'

theorem expansion_g (y : Fin n → GaussRat) : y = colMatrix (g T) *ᵥ coords (g T) y :=
  expansion (g_ne_zero hT) (fun _ _ h => ip_g_g hT h) y

theorem ip_g_eq (y : Fin n → GaussRat) (k : Fin n) :
    ip (g T k) y = ((vnorm (g T k) : ℚ) : GaussRat) * coords (g T) y k :=
  ip_f_eq_vnorm_mul_coords (g_ne_zero hT) y k

/-- Transition probability of a basis image against the image of `x`: `tp (e m) x`. -/
theorem tp_g_T (m : Fin n) {x : Fin n → GaussRat} (hx : x ≠ 0) : tp (g T m) (T x) = tp (e m) x :=
  hT.tp_eq (e m) x (e_ne_zero m) hx

/-- A coordinate of `T x` in the basis `g` vanishes when `x m = 0`. -/
theorem coords_g_eq_zero {x : Fin n → GaussRat} (hx : x ≠ 0) {m : Fin n} (hm : x m = 0) :
    coords (g T) (T x) m = 0 := by
  rw [coords_eq_zero_iff (g_ne_zero hT)]
  rw [← tp_eq_zero_iff (g_ne_zero hT m) (hT.ne_zero x hx), tp_g_T hT m hx, tp_e_left, hm]
  simp [GaussRat.normSq]

/-! ### Alignment of the basis images by the probes `e i₀ + e j` -/

/-- `2 ‖g i₀‖² |a|² = ‖T (p i₀ j)‖²` and `2 ‖g j‖² |b|² = ‖T (p i₀ j)‖²` for the two coordinates. -/
theorem p_coord_eq {j : Fin n} (hj : j ≠ i₀) (k : Fin n) (hk : p i₀ j k = 1) :
    2 * vnorm (g T k) * GaussRat.normSq (coords (g T) (T (p i₀ j)) k) = vnorm (T (p i₀ j)) := by
  have h := tp_g_T hT k (p_ne_zero hj)
  rw [tp_e_left, hk, normSq_one, vnorm_p hj] at h
  unfold tp at h
  rw [ip_g_eq hT, GaussRat.normSq_mul, normSq_ratCast] at h
  have hgk := vnorm_pos (g_ne_zero hT k)
  have hTp := vnorm_pos (hT.ne_zero _ (p_ne_zero hj))
  field_simp at h
  linear_combination h

theorem p_coord_ne_zero {j : Fin n} (hj : j ≠ i₀) (k : Fin n) (hk : p i₀ j k = 1) :
    coords (g T) (T (p i₀ j)) k ≠ 0 := by
  intro h0
  have h := p_coord_eq hT hj k hk
  rw [h0, (GaussRat.normSq_eq_zero_iff 0).mpr rfl, mul_zero] at h
  exact (vnorm_pos (hT.ne_zero _ (p_ne_zero hj))).ne h

theorem align_ne_zero (k : Fin n) : align T i₀ k ≠ 0 := by
  unfold align
  split_ifs with h
  · exact one_ne_zero
  · exact div_ne_zero (p_coord_ne_zero hT h k (p_apply_j h)) (p_coord_ne_zero hT h i₀ (p_apply_i₀ h))

theorem f_ne_zero (k : Fin n) : f T i₀ k ≠ 0 :=
  smul_ne_zero (align_ne_zero hT k) (g_ne_zero hT k)

theorem ip_f_f {i j : Fin n} (h : i ≠ j) : ip (f T i₀ i) (f T i₀ j) = 0 := by
  unfold f
  rw [ip_smul_left, ip_smul_right, ip_g_g hT h, mul_zero, mul_zero]

theorem vnorm_f (k : Fin n) : vnorm (f T i₀ k) = d T i₀ := by
  unfold f d
  by_cases h : k = i₀
  · subst h
    rw [align_i₀, one_smul]
  · rw [align_of_ne T i₀ h, vnorm_smul, normSq_div]
    have h1 := p_coord_eq hT h k (p_apply_j h)
    have h2 := p_coord_eq hT h i₀ (p_apply_i₀ h)
    have hk0 : GaussRat.normSq (coords (g T) (T (p i₀ k)) i₀) ≠ 0 :=
      fun h0 => p_coord_ne_zero hT h i₀ (p_apply_i₀ h) ((GaussRat.normSq_eq_zero_iff _).mp h0)
    have key : GaussRat.normSq (coords (g T) (T (p i₀ k)) k) * vnorm (g T k) =
        vnorm (g T i₀) * GaussRat.normSq (coords (g T) (T (p i₀ k)) i₀) := by
      linear_combination (h1 - h2) / 2
    rw [div_mul_eq_mul_div, div_eq_iff hk0, key]

theorem similarity_F : Similarity (F T i₀) (d T i₀) :=
  similarity_colMatrix (fun _ _ h => ip_f_f hT h) (vnorm_f hT (i₀ := i₀))

theorem expansion_f (y : Fin n → GaussRat) : y = F T i₀ *ᵥ coords (f T i₀) y :=
  expansion (f_ne_zero hT) (fun _ _ h => ip_f_f hT h) y

theorem T_e_eq (k : Fin n) : T (e k) = (align T i₀ k)⁻¹ • (F T i₀ *ᵥ e k) := by
  rw [F_mulVec_e, f, smul_smul, inv_mul_cancel₀ (align_ne_zero hT k), one_smul]
  rfl

/-- The image of the probe `e i₀ + e j` is a multiple of `f i₀ + f j = F (p i₀ j)`. -/
theorem T_p_eq {j : Fin n} (hj : j ≠ i₀) :
    T (p i₀ j) = coords (g T) (T (p i₀ j)) i₀ • (F T i₀ *ᵥ p i₀ j) := by
  set a := coords (g T) (T (p i₀ j)) i₀ with ha
  set b := coords (g T) (T (p i₀ j)) j with hb
  have ha0 : a ≠ 0 := p_coord_ne_zero hT hj i₀ (p_apply_i₀ hj)
  have hz : coords (g T) (T (p i₀ j)) = Pi.single i₀ a + Pi.single j b := by
    funext m
    rw [Pi.add_apply]
    by_cases hm₀ : m = i₀
    · subst hm₀
      rw [Pi.single_eq_same, Pi.single_eq_of_ne (Ne.symm hj), add_zero]
    by_cases hmj : m = j
    · subst hmj
      rw [Pi.single_eq_same, Pi.single_eq_of_ne hj, zero_add]
    rw [Pi.single_eq_of_ne hm₀, Pi.single_eq_of_ne hmj, add_zero]
    exact coords_g_eq_zero hT (p_ne_zero hj) (p_apply_other hm₀ hmj)
  have hexp := expansion_g hT (T (p i₀ j))
  rw [hz, mulVec_add, colMatrix_mulVec_single, colMatrix_mulVec_single] at hexp
  rw [hexp, F, p, mulVec_add, colMatrix_mulVec_e, colMatrix_mulVec_e, smul_add, f, f, align_i₀,
    one_smul]
  congr 1
  rw [align_of_ne T i₀ hj, ← hb, ← ha, smul_smul, mul_div_cancel₀ _ ha0]

/-! ### Transport of transition probabilities through the reconstruction -/

theorem tp_transport {v x : Fin n → GaussRat} (hv : v ≠ 0) (hx : x ≠ 0) {a : Fin n → GaussRat}
    {μ : GaussRat} (hμ : μ ≠ 0) (hTv : T v = μ • (F T i₀ *ᵥ a)) :
    tp v x = tp a (coords (f T i₀) (T x)) := by
  calc tp v x = tp (T v) (T x) := (hT.tp_eq v x hv hx).symm
    _ = tp (F T i₀ *ᵥ a) (F T i₀ *ᵥ coords (f T i₀) (T x)) := by
        rw [hTv, tp_smul_left hμ]
        congr 1
        exact expansion_f hT (T x)
    _ = tp a (coords (f T i₀) (T x)) :=
        (similarity_F hT (i₀ := i₀)).tp_mulVec (d_ne_zero hT (i₀ := i₀)) _ _

theorem tp_e_transport (m : Fin n) {x : Fin n → GaussRat} (hx : x ≠ 0) :
    tp (e m) x = tp (e m) (coords (f T i₀) (T x)) :=
  tp_transport hT (e_ne_zero m) hx (inv_ne_zero (align_ne_zero hT m)) (T_e_eq hT m)

theorem tp_p_transport {j : Fin n} (hj : j ≠ i₀) {x : Fin n → GaussRat} (hx : x ≠ 0) :
    tp (p i₀ j) x = tp (p i₀ j) (coords (f T i₀) (T x)) :=
  tp_transport hT (p_ne_zero hj) hx (p_coord_ne_zero hT hj i₀ (p_apply_i₀ hj)) (T_p_eq hT hj)

/-- The coordinates of `T x` in `f` have the same squared norm profile as `x`, after matching the
total norms. -/
theorem vnorm_coords_eq {x : Fin n → GaussRat} (hx : x ≠ 0) {m : Fin n}
    (hzm : coords (f T i₀) (T x) m ≠ 0) :
    vnorm (coords (f T i₀) (T x)) * GaussRat.normSq (x m) =
      vnorm x * GaussRat.normSq (coords (f T i₀) (T x) m) := by
  have h := tp_e_transport hT (i₀ := i₀) m hx
  rw [tp_e_left, tp_e_left] at h
  have hz : coords (f T i₀) (T x) ≠ 0 := fun h0 => hzm (by rw [h0]; rfl)
  have hvx := vnorm_ne_zero hx
  have hvz := vnorm_ne_zero hz
  field_simp at h
  linear_combination h

theorem coords_f_eq_zero {x : Fin n → GaussRat} (hx : x ≠ 0) {m : Fin n} (hm : x m = 0) :
    coords (f T i₀) (T x) m = 0 := by
  have h := tp_e_transport hT (i₀ := i₀) m hx
  rw [tp_e_left, tp_e_left, hm, (GaussRat.normSq_eq_zero_iff 0).mpr rfl, zero_div] at h
  rcases div_eq_zero_iff.mp h.symm with h0 | h0
  · exact (GaussRat.normSq_eq_zero_iff _).mp h0
  · exfalso
    have hz : coords (f T i₀) (T x) = 0 := (vnorm_eq_zero_iff _).mp h0
    have := expansion_f hT (i₀ := i₀) (T x)
    rw [hz, mulVec_zero] at this
    exact hT.ne_zero x hx this

theorem coords_f_ne_zero {x : Fin n → GaussRat} (hx : x ≠ 0) {m : Fin n} (hm : x m ≠ 0) :
    coords (f T i₀) (T x) m ≠ 0 := by
  intro h0
  have h := tp_e_transport hT (i₀ := i₀) m hx
  rw [tp_e_left, tp_e_left, h0, (GaussRat.normSq_eq_zero_iff 0).mpr rfl, zero_div] at h
  rcases div_eq_zero_iff.mp h with h1 | h1
  · exact hm ((GaussRat.normSq_eq_zero_iff _).mp h1)
  · exact vnorm_ne_zero hx h1

/-! ### The sign carried by the probes `e i₀ + i e j` -/

theorem sgn_spec {j : Fin n} (hj : j ≠ i₀) :
    (sgn T i₀ j = 1 ∨ sgn T i₀ j = -1) ∧
      T (qs i₀ 1 j) = coords (f T i₀) (T (qs i₀ 1 j)) i₀ • (F T i₀ *ᵥ qs i₀ (sgn T i₀ j) j) := by
  have hq : qs i₀ 1 j ≠ 0 := qs_ne_zero hj (Or.inl rfl)
  set w := coords (f T i₀) (T (qs i₀ 1 j)) with hw
  have hw₀ : w i₀ ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) hq (by rw [qs_apply_i₀ hj]; exact one_ne_zero)
  have hwj : w j ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) hq (by
    rw [qs_apply_j hj]
    intro h0
    have := congrArg GaussRat.im h0
    simp at this)
  -- |w i₀|² = |w j|² and |w i₀ + w j|² = 2 |w i₀|²
  have e1 := vnorm_coords_eq hT (i₀ := i₀) hq (m := i₀) hw₀
  have e2 := vnorm_coords_eq hT (i₀ := i₀) hq (m := j) hwj
  rw [qs_apply_i₀ hj, normSq_one, mul_one] at e1
  rw [qs_apply_j hj, normSq_smul_I (Or.inl rfl), mul_one] at e2
  rw [← hw] at e1 e2
  have e3 := tp_p_transport hT hj hq
  rw [tp_p_qs hj] at e3
  unfold tp at e3
  rw [ip_p_left, vnorm_p hj, ← hw] at e3
  have hvq := vnorm_qs hj (Or.inl rfl)
  have hvw : vnorm w ≠ 0 := fun h0 => hw₀ (by
    have := (vnorm_eq_zero_iff w).mp h0
    rw [this]; rfl)
  have hsum : GaussRat.normSq (w i₀ + w j) = vnorm w := by
    rw [eq_div_iff (mul_ne_zero two_ne_zero hvw)] at e3
    linarith
  -- the ratio u = w j / w i₀
  set u := w j / w i₀ with hu
  have hu1 : GaussRat.normSq u = 1 := by
    rw [hu, normSq_div, div_eq_one_iff_eq (fun h0 => hw₀ ((GaussRat.normSq_eq_zero_iff _).mp h0))]
    have hvx : vnorm (qs i₀ 1 j) ≠ 0 := by rw [hvq]; norm_num
    have := e1.symm.trans e2
    exact (mul_left_cancel₀ hvx this).symm
  have hu2 : GaussRat.normSq (1 + u) = 2 := by
    have hwsum : w i₀ + w j = w i₀ * (1 + u) := by
      rw [hu, mul_add, mul_one, mul_div_cancel₀ _ hw₀]
    have hvw2 : vnorm w = 2 * GaussRat.normSq (w i₀) := by
      have hvx : vnorm (qs i₀ 1 j) = 2 := hvq
      have := e1
      rw [hvx] at this
      linarith
    rw [hwsum, GaussRat.normSq_mul] at hsum
    rw [hvw2] at hsum
    have hn0 : GaussRat.normSq (w i₀) ≠ 0 := fun h0 => hw₀ ((GaussRat.normSq_eq_zero_iff _).mp h0)
    have := mul_left_cancel₀ hn0 (hsum.trans (mul_comm _ _))
    exact this
  obtain ⟨hu_eq, hs⟩ := eq_smul_I_of_normSq hu1 hu2
  have hsgn : sgn T i₀ j = u.im := rfl
  refine ⟨by rw [hsgn]; exact hs, ?_⟩
  -- w = w i₀ • qs i₀ s j
  have hw_eq : w = w i₀ • qs i₀ (sgn T i₀ j) j := by
    funext m
    rw [Pi.smul_apply, smul_eq_mul]
    by_cases hm₀ : m = i₀
    · subst hm₀
      rw [qs_apply_i₀ hj, mul_one]
    by_cases hmj : m = j
    · subst hmj
      rw [qs_apply_j hj, hsgn, ← hu_eq, hu, mul_div_cancel₀ _ hw₀]
    rw [qs_apply_other hm₀ hmj, mul_zero]
    exact coords_f_eq_zero hT (i₀ := i₀) hq (qs_apply_other hm₀ hmj 1)
  have hexp := expansion_f hT (i₀ := i₀) (T (qs i₀ 1 j))
  rw [← hw, hw_eq, mulVec_smul] at hexp
  exact hexp

theorem tp_qs_transport {j : Fin n} (hj : j ≠ i₀) {x : Fin n → GaussRat} (hx : x ≠ 0) :
    tp (qs i₀ 1 j) x = tp (qs i₀ (sgn T i₀ j) j) (coords (f T i₀) (T x)) :=
  tp_transport hT (qs_ne_zero hj (Or.inl rfl)) hx
    (coords_f_ne_zero hT (i₀ := i₀) (qs_ne_zero hj (Or.inl rfl)) (by rw [qs_apply_i₀ hj]; exact one_ne_zero))
    (sgn_spec hT hj).2

/-! ### Stage 1: vectors with `x i₀ ≠ 0` -/

/-- The normalised coordinates `z' = (z i₀)⁻¹ • coords f (T x)` and `x' = (x i₀)⁻¹ • x` have the same
norm, and the rescaled probe equations hold. -/
theorem normalised_data {x : Fin n → GaussRat} (hx0 : x i₀ ≠ 0) :
    let z := coords (f T i₀) (T x)
    let x' := (x i₀)⁻¹ • x
    let z' := (z i₀)⁻¹ • z
    x' i₀ = 1 ∧ z' i₀ = 1 ∧ vnorm z' = vnorm x' ∧
      (∀ m, tp (e m) x' = tp (e m) z') ∧
      (∀ j, j ≠ i₀ → tp (p i₀ j) x' = tp (p i₀ j) z') ∧
      (∀ j, j ≠ i₀ → tp (qs i₀ 1 j) x' = tp (qs i₀ (sgn T i₀ j) j) z') := by
  intro z x' z'
  have hx : x ≠ 0 := fun h0 => hx0 (by rw [h0]; rfl)
  have hz0 : z i₀ ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) hx hx0
  have hx'0 : x' i₀ = 1 := smul_inv_apply_self hx0
  have hz'0 : z' i₀ = 1 := smul_inv_apply_self hz0
  have hx'ne : x' ≠ 0 := fun h0 => by
    have := congrFun h0 i₀
    rw [hx'0, Pi.zero_apply] at this
    exact one_ne_zero this
  have hz'ne : z' ≠ 0 := fun h0 => by
    have := congrFun h0 i₀
    rw [hz'0, Pi.zero_apply] at this
    exact one_ne_zero this
  have he : ∀ m, tp (e m) x' = tp (e m) z' := fun m => by
    show tp (e m) ((x i₀)⁻¹ • x) = tp (e m) ((z i₀)⁻¹ • z)
    rw [tp_smul_right (inv_ne_zero hx0), tp_smul_right (inv_ne_zero hz0)]
    exact tp_e_transport hT m hx
  have hN : vnorm z' = vnorm x' := by
    have h := he i₀
    rw [tp_e_left, tp_e_left, hx'0, hz'0, normSq_one] at h
    have := vnorm_ne_zero hx'ne
    have := vnorm_ne_zero hz'ne
    field_simp at h
    linarith
  refine ⟨hx'0, hz'0, hN, he, fun j hj => ?_, fun j hj => ?_⟩
  · show tp (p i₀ j) ((x i₀)⁻¹ • x) = tp (p i₀ j) ((z i₀)⁻¹ • z)
    rw [tp_smul_right (inv_ne_zero hx0), tp_smul_right (inv_ne_zero hz0)]
    exact tp_p_transport hT hj hx
  · show tp (qs i₀ 1 j) ((x i₀)⁻¹ • x) = tp (qs i₀ (sgn T i₀ j) j) ((z i₀)⁻¹ • z)
    rw [tp_smul_right (inv_ne_zero hx0), tp_smul_right (inv_ne_zero hz0)]
    exact tp_qs_transport hT hj hx

theorem stage1 {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (hsgn : ∀ j, j ≠ i₀ → sgn T i₀ j = ε)
    {x : Fin n → GaussRat} (hx0 : x i₀ ≠ 0) :
    ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F T i₀ *ᵥ twist ε x) := by
  obtain ⟨hx'0, hz'0, hN, he, hp, hq⟩ := normalised_data hT hx0
  set z := coords (f T i₀) (T x) with hz
  have hx : x ≠ 0 := fun h0 => hx0 (by rw [h0]; rfl)
  have hz0 : z i₀ ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) hx hx0
  have hz' : (z i₀)⁻¹ • z = twist ε ((x i₀)⁻¹ • x) := by
    funext m
    by_cases hm : m = i₀
    · subst hm
      rw [twist_apply, hz'0, hx'0, tw_one']
    · rw [twist_apply]
      have hq' := hq m hm
      rw [hsgn m hm] at hq'
      exact coord_rigidity hm hx'0 hz'0 hN hε (he m) (hp m hm) hq'
  have hzz : z = (z i₀ * tw ε (x i₀)⁻¹) • twist ε x := by
    rw [twist_smul hε] at hz'
    calc z = z i₀ • ((z i₀)⁻¹ • z) := by rw [smul_smul, mul_inv_cancel₀ hz0, one_smul]
      _ = (z i₀ * tw ε (x i₀)⁻¹) • twist ε x := by rw [hz', smul_smul]
  refine ⟨z i₀ * tw ε (x i₀)⁻¹, mul_ne_zero hz0 (tw_ne_zero hε (inv_ne_zero hx0)), ?_⟩
  have hexp := expansion_f hT (i₀ := i₀) (T x)
  rw [← hz, hzz, mulVec_smul] at hexp
  exact hexp

/-! ### Consistency of the sign across coordinates -/

/-- The probe `e i₀ + e j + e k` is mapped to a multiple of its own image under `F`. -/
theorem T_r_eq {j k : Fin n} (hj : j ≠ i₀) (hk : k ≠ i₀) (hjk : j ≠ k) :
    ∃ μ : GaussRat, μ ≠ 0 ∧ T (e i₀ + e j + e k) = μ • (F T i₀ *ᵥ (e i₀ + e j + e k)) := by
  set r : Fin n → GaussRat := e i₀ + e j + e k with hr
  have hr0 : r i₀ = 1 := by
    simp only [hr, Pi.add_apply, e_apply_self, e_apply_ne (Ne.symm hj), e_apply_ne (Ne.symm hk)]
    norm_num
  have hri : r i₀ ≠ 0 := by rw [hr0]; exact one_ne_zero
  obtain ⟨hx'0, hz'0, hN, he, hp, hq⟩ := normalised_data hT hri
  set z := coords (f T i₀) (T r) with hz
  have hr' : (r i₀)⁻¹ • r = r := by rw [hr0, inv_one, one_smul]
  rw [hr'] at hx'0 hN he hp hq
  have hz0 : z i₀ ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) (fun h0 => hri (by rw [h0]; rfl)) hri
  have hz' : (z i₀)⁻¹ • z = r := by
    funext m
    by_cases hm₀ : m = i₀
    · subst hm₀
      rw [hz'0, hr0]
    have hxN : vnorm r ≠ 0 := vnorm_ne_zero (fun h0 => hri (by rw [h0]; rfl))
    by_cases hmj : m = j
    · subst hmj
      have := coord_rigidity hm₀ hx'0 hz'0 hN (sgn_spec hT hm₀).1 (he m) (hp m hm₀) (hq m hm₀)
      rw [this]
      have hrm : r m = 1 := by
        simp only [hr, Pi.add_apply, e_apply_self, e_apply_ne hj, e_apply_ne hjk]
        norm_num
      rw [hrm, tw_one']
    by_cases hmk : m = k
    · subst hmk
      have := coord_rigidity hm₀ hx'0 hz'0 hN (sgn_spec hT hm₀).1 (he m) (hp m hm₀) (hq m hm₀)
      rw [this]
      have hrm : r m = 1 := by
        simp only [hr, Pi.add_apply, e_apply_self, e_apply_ne hk, e_apply_ne (Ne.symm hjk)]
        norm_num
      rw [hrm, tw_one']
    have hrm : r m = 0 := by
      simp only [hr, Pi.add_apply, e_apply_ne hm₀, e_apply_ne hmj, e_apply_ne hmk]
      norm_num
    rw [hrm]
    exact coord_zero hN hxN (he m) hrm
  refine ⟨z i₀, hz0, ?_⟩
  have hzz : z = z i₀ • r := by
    rw [← hz']
    rw [smul_smul, mul_inv_cancel₀ hz0, one_smul]
  have hexp := expansion_f hT (i₀ := i₀) (T r)
  rw [← hz, hzz, mulVec_smul] at hexp
  exact hexp

theorem sgn_consistent {j k : Fin n} (hj : j ≠ i₀) (hk : k ≠ i₀) (hjk : j ≠ k) :
    sgn T i₀ j = sgn T i₀ k := by
  set x : Fin n → GaussRat := e i₀ + GaussRat.I • e j + GaussRat.I • e k with hxdef
  set r : Fin n → GaussRat := e i₀ + e j + e k with hrdef
  have hx0 : x i₀ = 1 := by
    simp only [hxdef, Pi.add_apply, Pi.smul_apply, e_apply_self, e_apply_ne (Ne.symm hj),
      e_apply_ne (Ne.symm hk), smul_eq_mul, mul_zero]
    norm_num
  have hxj : x j = GaussRat.I := by
    simp only [hxdef, Pi.add_apply, Pi.smul_apply, e_apply_self, e_apply_ne hj, e_apply_ne hjk,
      smul_eq_mul, mul_zero, mul_one]
    norm_num
  have hxk : x k = GaussRat.I := by
    simp only [hxdef, Pi.add_apply, Pi.smul_apply, e_apply_self, e_apply_ne hk,
      e_apply_ne (Ne.symm hjk), smul_eq_mul, mul_zero, mul_one]
    norm_num
  have hxi : x i₀ ≠ 0 := by rw [hx0]; exact one_ne_zero
  have hx : x ≠ 0 := fun h0 => hxi (by rw [h0]; rfl)
  have hvx : vnorm x = 3 := by
    have h1 : ip (e i₀) (GaussRat.I • e j) = 0 := by
      rw [ip_smul_right, ip_e_e_of_ne (Ne.symm hj), mul_zero]
    have h2 : ip (e i₀ + GaussRat.I • e j) (GaussRat.I • e k) = 0 := by
      rw [ip_add_left, ip_smul_right, ip_smul_left, ip_smul_right, ip_e_e_of_ne (Ne.symm hk),
        ip_e_e_of_ne hjk]
      simp
    rw [hxdef, vnorm_add_of_ip_zero h2, vnorm_add_of_ip_zero h1, vnorm_smul, vnorm_smul, vnorm_e,
      vnorm_e, vnorm_e, normSq_I]
    norm_num
  have hvr : vnorm r = 3 := by
    have h1 : ip (e i₀) (e j) = 0 := ip_e_e_of_ne (Ne.symm hj)
    have h2 : ip (e i₀ + e j) (e k) = 0 := by
      rw [ip_add_left, ip_e_e_of_ne (Ne.symm hk), ip_e_e_of_ne hjk, add_zero]
    rw [hrdef, vnorm_add_of_ip_zero h2, vnorm_add_of_ip_zero h1, vnorm_e, vnorm_e, vnorm_e]
    norm_num
  have hr : r ≠ 0 := ne_zero_of_vnorm_ne_zero (by rw [hvr]; norm_num)
  obtain ⟨hx'0, hz'0, hN, he, hp, hq⟩ := normalised_data hT hxi
  set z := coords (f T i₀) (T x) with hz
  have hx' : (x i₀)⁻¹ • x = x := by rw [hx0, inv_one, one_smul]
  rw [hx'] at hx'0 hN he hp hq
  have hz0 : z i₀ ≠ 0 := coords_f_ne_zero hT (i₀ := i₀) hx hxi
  set z' := (z i₀)⁻¹ • z with hz'def
  have hsj := (sgn_spec hT hj).1
  have hsk := (sgn_spec hT hk).1
  have hzj : z' j = sgn T i₀ j • GaussRat.I := by
    have := coord_rigidity hj hx'0 hz'0 hN hsj (he j) (hp j hj) (hq j hj)
    rw [this, hxj]
    ext <;> simp [tw]
  have hzk : z' k = sgn T i₀ k • GaussRat.I := by
    have := coord_rigidity hk hx'0 hz'0 hN hsk (he k) (hp k hk) (hq k hk)
    rw [this, hxk]
    ext <;> simp [tw]
  -- the probe r against x and against z'
  obtain ⟨μ, hμ, hTr⟩ := T_r_eq hT hj hk hjk
  have htr : tp r x = tp r z := tp_transport hT hr hx hμ hTr
  have htr' : tp r x = tp r z' := by
    rw [htr, hz'def, tp_smul_right (inv_ne_zero hz0)]
  have hipx : ip r x = 1 + GaussRat.I + GaussRat.I := by
    rw [hrdef, ip_add_left, ip_add_left, ip_e_left, ip_e_left, ip_e_left, hx0, hxj, hxk]
  have hipz : ip r z' = 1 + sgn T i₀ j • GaussRat.I + sgn T i₀ k • GaussRat.I := by
    rw [hrdef, ip_add_left, ip_add_left, ip_e_left, ip_e_left, ip_e_left, hz'0, hzj, hzk]
  have hvz : vnorm z' = 3 := by rw [hN, hvx]
  unfold tp at htr'
  rw [hipx, hipz, hvx, hvz, hvr] at htr'
  have hnum : GaussRat.normSq (1 + GaussRat.I + GaussRat.I) = 5 := by
    simp only [GaussRat.normSq, GaussRat.re_add, GaussRat.im_add, GaussRat.re_I, GaussRat.im_I,
      GaussRat.re_one, GaussRat.im_one]
    norm_num
  have hnum' : GaussRat.normSq (1 + sgn T i₀ j • GaussRat.I + sgn T i₀ k • GaussRat.I) =
      1 + (sgn T i₀ j + sgn T i₀ k) ^ 2 := by
    simp only [GaussRat.normSq, GaussRat.re_add, GaussRat.im_add, GaussRat.re_smul, GaussRat.im_smul,
      GaussRat.re_I, GaussRat.im_I, GaussRat.re_one, GaussRat.im_one]
    ring
  rw [hnum, hnum'] at htr'
  have h4 : (sgn T i₀ j + sgn T i₀ k) ^ 2 = 4 := by
    field_simp at htr'
    linarith
  rcases hsj with h1 | h1 <;> rcases hsk with h2 | h2
  · rw [h1, h2]
  · exfalso
    rw [h1, h2] at h4
    norm_num at h4
  · exfalso
    rw [h1, h2] at h4
    norm_num at h4
  · rw [h1, h2]

/-! ### Stage 2: vectors with `x i₀ = 0` -/

theorem stage2 {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (hsgn : ∀ j, j ≠ i₀ → sgn T i₀ j = ε)
    {x : Fin n → GaussRat} (hx : x ≠ 0) (hx0 : x i₀ = 0) :
    ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F T i₀ *ᵥ twist ε x) := by
  set v : Fin n → GaussRat := e i₀ + x with hvdef
  have hv0 : v i₀ ≠ 0 := by
    rw [hvdef, Pi.add_apply, e_apply_self, hx0, add_zero]
    exact one_ne_zero
  have hv : v ≠ 0 := fun h0 => hv0 (by rw [h0]; rfl)
  obtain ⟨μ, hμ, hTv⟩ := stage1 hT hε hsgn hv0
  set z := coords (f T i₀) (T x) with hz
  set w := twist ε z with hwdef
  have hz0 : z i₀ = 0 := coords_f_eq_zero hT (i₀ := i₀) hx hx0
  have hw0 : w i₀ = 0 := by
    rw [hwdef, twist_apply, hz0]
    ext <;> simp [tw]
  -- tp v x = tp v w
  have h1 : tp v x = tp (twist ε v) z := tp_transport hT hv hx hμ hTv
  have h2 : tp (twist ε v) z = tp v w := by
    rw [← tp_twist hε, twist_twist hε, ← hwdef]
  have hipvx : ip v x = ((vnorm x : ℚ) : GaussRat) := by
    rw [hvdef, ip_add_left, ip_e_left, hx0, zero_add, ip_self_eq]
  have hipvw : ip v w = ip x w := by
    rw [hvdef, ip_add_left, ip_e_left, hw0, zero_add]
  have hvv : vnorm v = 1 + vnorm x := by
    rw [hvdef, vnorm_add, vnorm_e, ip_e_left, hx0, GaussRat.re_zero]
    ring
  have hzne : z ≠ 0 := fun h0 => hT.ne_zero x hx (by
    have := expansion_f hT (i₀ := i₀) (T x)
    rw [← hz, h0, mulVec_zero] at this
    exact this)
  have hwne : w ≠ 0 := fun h0 => hzne ((twist_eq_zero_iff hε z).mp h0)
  have hvx := vnorm_pos hx
  have hvw := vnorm_pos hwne
  have hcs : GaussRat.normSq (ip x w) = vnorm x * vnorm w := by
    have h := h1.trans h2
    unfold tp at h
    rw [hipvx, hipvw, normSq_ratCast, hvv] at h
    field_simp at h
    nlinarith [h, hvx, hvw]
  have hw_eq := eq_smul_of_normSq_ip_eq hx hcs
  set c := ip x w / ((vnorm x : ℚ) : GaussRat) with hc
  have hz_eq : z = tw ε c • twist ε x := by
    rw [← twist_twist hε z, ← hwdef, hw_eq, twist_smul hε]
  have hc0 : tw ε c ≠ 0 := by
    intro h0
    rw [h0, zero_smul] at hz_eq
    exact hzne hz_eq
  refine ⟨tw ε c, hc0, ?_⟩
  have hexp := expansion_f hT (i₀ := i₀) (T x)
  rw [← hz, hz_eq, mulVec_smul] at hexp
  exact hexp

/-! ### Assembly -/

theorem induced_of_sign {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (hsgn : ∀ j, j ≠ i₀ → sgn T i₀ j = ε)
    {x : Fin n → GaussRat} (hx : x ≠ 0) :
    ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F T i₀ *ᵥ twist ε x) := by
  by_cases hx0 : x i₀ = 0
  · exact stage2 hT hε hsgn hx hx0
  · exact stage1 hT hε hsgn hx0

/-- A sign `ε ∈ {1, −1}` agreeing with every `sgn j`, `j ≠ i₀`. -/
theorem exists_sign : ∃ ε : ℚ, (ε = 1 ∨ ε = -1) ∧ ∀ j, j ≠ i₀ → sgn T i₀ j = ε := by
  by_cases hex : ∃ j : Fin n, j ≠ i₀
  · obtain ⟨j₁, hj₁⟩ := hex
    refine ⟨sgn T i₀ j₁, (sgn_spec hT hj₁).1, fun j hj => ?_⟩
    by_cases hjj : j = j₁
    · rw [hjj]
    · exact sgn_consistent hT hj hj₁ hjj
  · refine ⟨1, Or.inl rfl, fun j hj => absurd ⟨j, hj⟩ hex⟩

end Proof

/-- **Finite exact Wigner theorem over ℚ(i)ⁿ.**  A map preserving transition probabilities between
nonzero vectors is induced on rays by a ℚ(i)-linear similarity composed with the identity or with
componentwise conjugation. -/
theorem finite_wigner (i₀ : Fin n) {T : (Fin n → GaussRat) → (Fin n → GaussRat)}
    (hT : TpPreserving T) :
    ∃ (F : Matrix (Fin n) (Fin n) GaussRat) (d ε : ℚ), 0 < d ∧ Similarity F d ∧ (ε = 1 ∨ ε = -1) ∧
      ∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F *ᵥ twist ε x) := by
  obtain ⟨ε, hε, hsgn⟩ := exists_sign hT (i₀ := i₀)
  exact ⟨F T i₀, d T i₀, ε, d_pos hT (i₀ := i₀), similarity_F hT (i₀ := i₀), hε,
    fun x hx => induced_of_sign hT hε hsgn hx⟩

/-- The two cases: linear similarity, or conjugation followed by a linear similarity. -/
theorem finite_wigner_cases (i₀ : Fin n) {T : (Fin n → GaussRat) → (Fin n → GaussRat)}
    (hT : TpPreserving T) :
    ∃ (F : Matrix (Fin n) (Fin n) GaussRat) (d : ℚ), 0 < d ∧ Similarity F d ∧
      ((∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F *ᵥ x)) ∨
       (∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F *ᵥ star x))) := by
  obtain ⟨F, d, ε, hd, hF, hε, h⟩ := finite_wigner i₀ hT
  refine ⟨F, d, hd, hF, ?_⟩
  rcases hε with rfl | rfl
  · left
    intro x hx
    obtain ⟨μ, hμ, hx'⟩ := h x hx
    rw [twist_one] at hx'
    exact ⟨μ, hμ, hx'⟩
  · right
    intro x hx
    obtain ⟨μ, hμ, hx'⟩ := h x hx
    rw [twist_neg_one] at hx'
    exact ⟨μ, hμ, hx'⟩

/-- Converse: every ray map of the form `x ↦ c x • (F *ᵥ twist ε x)` with `F` a similarity of
nonzero scale and `c x ≠ 0` preserves transition probabilities. -/
theorem tpPreserving_of_similarity {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (hF : Similarity F d)
    (hd : d ≠ 0) {ε : ℚ} (hε : ε = 1 ∨ ε = -1) (c : (Fin n → GaussRat) → GaussRat)
    (hc : ∀ x, c x ≠ 0) : TpPreserving (fun x => c x • (F *ᵥ twist ε x)) where
  ne_zero x hx := smul_ne_zero (hc x) (hF.mulVec_ne_zero hd (fun h0 => hx ((twist_eq_zero_iff hε x).mp h0)))
  tp_eq x y _ _ := by
    show tp (c x • (F *ᵥ twist ε x)) (c y • (F *ᵥ twist ε y)) = tp x y
    rw [tp_smul_left (hc x), tp_smul_right (hc y), hF.tp_mulVec hd, tp_twist hε]

/-- The induced map on rays is reversible: `F` has the two-sided inverse `(1 / d) • Fᴴ`, itself a
similarity, so `x ↦ F *ᵥ twist ε x` is a bijection of the carrier. -/
theorem similarity_bijective {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (hF : Similarity F d)
    (hd : d ≠ 0) {ε : ℚ} (hε : ε = 1 ∨ ε = -1) :
    Function.Bijective (fun x : Fin n → GaussRat => F *ᵥ twist ε x) := by
  refine ⟨fun x y hxy => ?_, fun y => ⟨twist ε (((1 / d) • Fᴴ) *ᵥ y), ?_⟩⟩
  · have hxy' : F *ᵥ twist ε x = F *ᵥ twist ε y := hxy
    have h : ((1 / d) • Fᴴ) *ᵥ (F *ᵥ twist ε x) = ((1 / d) • Fᴴ) *ᵥ (F *ᵥ twist ε y) := by
      rw [hxy']
    rw [mulVec_mulVec, mulVec_mulVec, hF.left_inverse hd, one_mulVec, one_mulVec] at h
    rw [← twist_twist hε x, h, twist_twist hε]
  · show F *ᵥ twist ε (twist ε (((1 / d) • Fᴴ) *ᵥ y)) = y
    rw [twist_twist hε, mulVec_mulVec, hF.right_inverse hd, one_mulVec]

end WignerFable.Theorem

#print axioms WignerFable.Theorem.TpPreserving
#print axioms WignerFable.Theorem.p
#print axioms WignerFable.Theorem.qs
#print axioms WignerFable.Theorem.star_smul_I
#print axioms WignerFable.Theorem.normSq_smul_I
#print axioms WignerFable.Theorem.ip_p_left
#print axioms WignerFable.Theorem.ip_qs_left
#print axioms WignerFable.Theorem.p_apply
#print axioms WignerFable.Theorem.qs_apply
#print axioms WignerFable.Theorem.vnorm_p
#print axioms WignerFable.Theorem.vnorm_qs
#print axioms WignerFable.Theorem.p_ne_zero
#print axioms WignerFable.Theorem.qs_ne_zero
#print axioms WignerFable.Theorem.p_apply_i₀
#print axioms WignerFable.Theorem.p_apply_j
#print axioms WignerFable.Theorem.p_apply_other
#print axioms WignerFable.Theorem.qs_apply_i₀
#print axioms WignerFable.Theorem.qs_apply_j
#print axioms WignerFable.Theorem.qs_apply_other
#print axioms WignerFable.Theorem.tp_e_left
#print axioms WignerFable.Theorem.smul_inv_apply_self
#print axioms WignerFable.Theorem.normSq_inv
#print axioms WignerFable.Theorem.normSq_div
#print axioms WignerFable.Theorem.vnorm_add_of_ip_zero
#print axioms WignerFable.Theorem.tp_e_qs
#print axioms WignerFable.Theorem.tp_ej_qs
#print axioms WignerFable.Theorem.tp_p_qs
#print axioms WignerFable.Theorem.eq_smul_I_of_normSq
#print axioms WignerFable.Theorem.normSq_ip_qs
#print axioms WignerFable.Theorem.normSq_ip_p
#print axioms WignerFable.Theorem.coord_rigidity
#print axioms WignerFable.Theorem.coord_zero
#print axioms WignerFable.Theorem.g
#print axioms WignerFable.Theorem.align
#print axioms WignerFable.Theorem.f
#print axioms WignerFable.Theorem.F
#print axioms WignerFable.Theorem.d
#print axioms WignerFable.Theorem.sgn
#print axioms WignerFable.Theorem.align_i₀
#print axioms WignerFable.Theorem.align_of_ne
#print axioms WignerFable.Theorem.f_i₀
#print axioms WignerFable.Theorem.F_mulVec_e
#print axioms WignerFable.Theorem.g_ne_zero
#print axioms WignerFable.Theorem.ip_g_g
#print axioms WignerFable.Theorem.d_pos
#print axioms WignerFable.Theorem.d_ne_zero
#print axioms WignerFable.Theorem.expansion_g
#print axioms WignerFable.Theorem.ip_g_eq
#print axioms WignerFable.Theorem.tp_g_T
#print axioms WignerFable.Theorem.coords_g_eq_zero
#print axioms WignerFable.Theorem.p_coord_eq
#print axioms WignerFable.Theorem.p_coord_ne_zero
#print axioms WignerFable.Theorem.align_ne_zero
#print axioms WignerFable.Theorem.f_ne_zero
#print axioms WignerFable.Theorem.ip_f_f
#print axioms WignerFable.Theorem.vnorm_f
#print axioms WignerFable.Theorem.similarity_F
#print axioms WignerFable.Theorem.expansion_f
#print axioms WignerFable.Theorem.T_e_eq
#print axioms WignerFable.Theorem.T_p_eq
#print axioms WignerFable.Theorem.tp_transport
#print axioms WignerFable.Theorem.tp_e_transport
#print axioms WignerFable.Theorem.tp_p_transport
#print axioms WignerFable.Theorem.vnorm_coords_eq
#print axioms WignerFable.Theorem.coords_f_eq_zero
#print axioms WignerFable.Theorem.coords_f_ne_zero
#print axioms WignerFable.Theorem.sgn_spec
#print axioms WignerFable.Theorem.tp_qs_transport
#print axioms WignerFable.Theorem.normalised_data
#print axioms WignerFable.Theorem.stage1
#print axioms WignerFable.Theorem.T_r_eq
#print axioms WignerFable.Theorem.sgn_consistent
#print axioms WignerFable.Theorem.stage2
#print axioms WignerFable.Theorem.induced_of_sign
#print axioms WignerFable.Theorem.exists_sign
#print axioms WignerFable.Theorem.finite_wigner
#print axioms WignerFable.Theorem.finite_wigner_cases
#print axioms WignerFable.Theorem.tpPreserving_of_similarity
#print axioms WignerFable.Theorem.similarity_bijective
