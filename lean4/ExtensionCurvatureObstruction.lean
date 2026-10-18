import Mathlib

/-!
# MUB extension curvature obstruction — mechanized cores

This module mechanizes the *cleanly-provable cores* of the encyclopedia entries
ENC-1131..1134 (MUB-extension GTFOC obstruction reframe, design spec
2026-06-19). It follows the established `MUB` contract-surface discipline: the
heavy analysis (compactness/attainment on `CP^{n-1}`, the full inner-product
Parseval identity, and the Invariant-Systems `max f = W` certificate) is carried
as *named hypotheses* — either explicit theorem hypotheses or fields of
`ExtensionObstruction` — while the genuinely finite/algebraic content is PROVED
outright. Nothing here proves a MUB(6)/MUB(N) no-go; it discharges the finite
logic that the entries reduce those questions to.

Proved content (real, not contract fields):
* `bianchi_closure_algebraic` / `bianchi_closure_zero` — ENC-1131: the discrete
  Bianchi closure `∑_{i} (g i − 1/n) = (∑ g) − 1`, hence `= 0` when `∑ g = 1`.
* `l1_sum_abs_eq_zero_iff` — ENC-1132: ℓ¹ positive-definiteness on a finite index.
* `ExtensionObstruction.phi_eq_zero_iff` / `.no_mu_vector_of_phi_pos` — ENC-1132:
  the characterization `Φ = 0 ⟺ ∃ MU vector` and the no-go `Φ > 0 ⟹ ¬∃ MU vector`
  (given attainment as a structure field — the honest stand-in for Weierstrass).
* `finite_cover_min_pos` — ENC-1133: a finite cover with per-patch bounds
  `ε_j > 0` yields a positive global bound `min_j ε_j > 0`.
* `W_lt_one`, `d6_floor_pos`, `no_mu_vector_at_d6_floor` — ENC-1134: `W < 1` for
  `W = (88+3√6)/100`, the positive d=6 floor, and the no-go it forces.
-/

namespace MUB
namespace ExtensionCurvatureObstruction

/-! ## ENC-1131 — the discrete Bianchi closure (real, proved) -/

/-- ENC-1131 Bianchi step (algebraic half): summing the deviation
`ω_i = g_i − 1/n` over a basis of size `n` collapses the constant tail to `1`. -/
theorem bianchi_closure_algebraic {n : ℕ} (hn : n ≠ 0) (g : Fin n → ℝ) :
    (∑ i, (g i - 1 / (n : ℝ))) = (∑ i, g i) - 1 := by
  have hnR : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn
  rw [Finset.sum_sub_distrib]
  have hconst : (∑ _i : Fin n, (1 / (n : ℝ))) = 1 := by
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
      mul_one_div, div_self hnR]
  rw [hconst]

/-- ENC-1131 Bianchi closure: with the per-basis Parseval/unit input `∑ g = 1`
(supplied as a hypothesis — its inner-product content is not formalized here), the
curvature closure mass vanishes. This is the `Γ₂ = 0` "closed survivor" fact. -/
theorem bianchi_closure_zero {n : ℕ} (hn : n ≠ 0) (g : Fin n → ℝ)
    (hParseval : (∑ i, g i) = 1) :
    (∑ i, (g i - 1 / (n : ℝ))) = 0 := by
  rw [bianchi_closure_algebraic hn g, hParseval]; ring

/-! ## ENC-1132 — ℓ¹ positive-definiteness (real, proved) -/

/-- ENC-1132 core: a finite ℓ¹ deviation sum is zero iff every coordinate is zero.
This is the definiteness used in `Φ = 0 ⟹ perfect unbiasedness`. -/
theorem l1_sum_abs_eq_zero_iff {ι : Type*} [Fintype ι] (ω : ι → ℝ) :
    (∑ i, |ω i| = 0) ↔ ∀ i, ω i = 0 := by
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => abs_nonneg (ω i))]
  simp [abs_eq_zero]

/-! ## ENC-1132 — the obstruction characterization and no-go (abstract, proved)

`ExtensionObstruction V` packages the configuration deviation `mass : V → ℝ`
(`mass v = ‖ω(v)‖₁`, the pointwise curvature mass) together with the obstruction
value `phi` and the two facts that make it a *minimum*: it is a lower bound and it
is attained. Attainment is the honest stand-in for the Weierstrass step
(ENC-1132(1)) — the only analytic input, surfaced as a field rather than proved. -/

structure ExtensionObstruction (V : Type*) where
  /-- pointwise deviation mass `‖ω(v)‖₁` -/
  mass : V → ℝ
  /-- the deviation mass is nonnegative (it is an ℓ¹ norm) -/
  mass_nonneg : ∀ v, 0 ≤ mass v
  /-- the obstruction value `Φ` -/
  phi : ℝ
  /-- `Φ` is the minimum: a lower bound, and attained (Weierstrass — ENC-1132(1)) -/
  phi_is_min : (∀ v, phi ≤ mass v) ∧ (∃ v, phi = mass v)

namespace ExtensionObstruction

variable {V : Type*} (O : ExtensionObstruction V)

theorem phi_le_mass (v : V) : O.phi ≤ O.mass v := O.phi_is_min.1 v

theorem phi_nonneg : 0 ≤ O.phi := by
  obtain ⟨v, hv⟩ := O.phi_is_min.2
  rw [hv]; exact O.mass_nonneg v

/-- ENC-1132(2): `Φ = 0` iff a mutually-unbiased vector (zero deviation) exists. -/
theorem phi_eq_zero_iff : O.phi = 0 ↔ ∃ v, O.mass v = 0 := by
  constructor
  · intro h
    obtain ⟨v, hv⟩ := O.phi_is_min.2
    exact ⟨v, by rw [← hv]; exact h⟩
  · rintro ⟨v, hv⟩
    have h1 : O.phi ≤ 0 := by have := O.phi_le_mass v; rwa [hv] at this
    exact le_antisymm h1 O.phi_nonneg

/-- ENC-1132(3) / ENC-1134: the no-go direction. A strictly positive obstruction
mass rules out any mutually-unbiased vector (hence any `(k+1)`-th MU basis, whose
first vector would be one). The geometric `(k+1)`-th-basis step is in the prose
entry; here it is the clean `Φ > 0 ⟹ ¬∃ MU vector`. -/
theorem no_mu_vector_of_phi_pos (hpos : 0 < O.phi) : ¬ ∃ v, O.mass v = 0 := by
  rw [← O.phi_eq_zero_iff]; exact hpos.ne'

end ExtensionObstruction

/-- A concrete inhabitant (constant unit deviation, `Φ = 1`) exhibiting the no-go
firing — the abstract analogue of "the d=6 wall makes `Φ > 0`, so no MU vector". -/
def constUnitObstruction : ExtensionObstruction Unit where
  mass := fun _ => 1
  mass_nonneg := fun _ => by norm_num
  phi := 1
  phi_is_min := ⟨fun _ => le_refl 1, ⟨(), rfl⟩⟩

theorem constUnit_no_mu_vector : ¬ ∃ v, constUnitObstruction.mass v = 0 :=
  constUnitObstruction.no_mu_vector_of_phi_pos (by show (0 : ℝ) < 1; norm_num)

/-! ## ENC-1133 — the finite-cover lower bound (real, proved) -/

/-- ENC-1133 core `(3) ⟹ (2)`: a finite (nonempty) cover with per-patch positive
mass bounds `ε_j > 0` yields a uniform positive lower bound `min_j ε_j > 0`. The
compactness that guarantees the cover is finite (ENC-1133 `(1) ⟹ (3)`) is the
analytic step abstracted away; the finite-min arithmetic is proved here. -/
theorem finite_cover_min_pos {ι : Type*} (s : Finset ι) (hs : s.Nonempty)
    (ε : ι → ℝ) (hpos : ∀ j ∈ s, 0 < ε j) :
    0 < s.inf' hs ε := by
  rw [Finset.lt_inf'_iff]
  exact hpos

/-! ## ENC-1134 — `W < 1`, the d=6 floor, and the no-go it forces (real, proved) -/

/-- The Invariant-Systems d=6 wall value `W = (88 + 3√6)/100` (cited; not derived). -/
noncomputable def W : ℝ := (88 + 3 * Real.sqrt 6) / 100

/-- `W < 1`, proved unconditionally from `√6 < 4` (i.e. `6 < 16`). This is the
strictness that turns the cited bound `max f = W` into "no perfect-unbiased vector"
(ENC-1134 step 1). -/
theorem W_lt_one : W < 1 := by
  have h1 : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have h2 : (0 : ℝ) ≤ Real.sqrt 6 := Real.sqrt_nonneg 6
  have h3 : Real.sqrt 6 < 4 := by nlinarith [h1, h2, sq_nonneg (Real.sqrt 6 - 4)]
  unfold W; linarith [h3]

/-- The d=6 quantitative floor `√((1−W)·5/6)` is strictly positive (it is the
panel-verified curvature floor `Φ₁^MUB(T0) ≥ √((1−W)·5/6) ≈ 0.197` of ENC-1134,
valid for the upstream functional `f = 1 − (6/5)‖ω‖₂²`). -/
theorem d6_floor_pos : 0 < Real.sqrt ((1 - W) * (5 / 6)) := by
  apply Real.sqrt_pos.mpr
  have h : (0 : ℝ) < 1 - W := by linarith [W_lt_one]
  exact mul_pos h (by norm_num)

/-- ENC-1134 capstone: any extension obstruction whose mass meets the d=6 floor
has no mutually-unbiased vector — chaining `W < 1 ⟹ floor > 0 ⟹ Φ > 0 ⟹ no MU
vector`. (Instantiated for the canonical triple `T0` once the `omega_mub`
cross-check discharges the `Φ₁(T0) ≥ floor` input.) -/
theorem no_mu_vector_at_d6_floor {V : Type*} (O : ExtensionObstruction V)
    (hfloor : Real.sqrt ((1 - W) * (5 / 6)) ≤ O.phi) :
    ¬ ∃ v, O.mass v = 0 :=
  O.no_mu_vector_of_phi_pos (lt_of_lt_of_le d6_floor_pos hfloor)

/-! ## Next rung — lifting two contract-surface hypotheses to real Mathlib proofs

The cores above abstracted the analysis (Weierstrass attainment, the `f=1⟺ω=0`
identification) into hypotheses/structure fields. Here those two are *proved*. -/

/-- **ENC-1134 H2, proved (ℓ² feasibility identity).** For the normalized upstream
feasibility functional `f(v) = 1 − c·∑ᵢ ωᵢ²` with any positive normalization
`c > 0`, `f = 1 ⟺ every ωᵢ = 0` — i.e. the maximal feasible value is attained
*exactly* at perfect unbiasedness. The d=6 wall functional is the instance
`c = 1/(1−1/6) = 6/5` (so `f = 1 − (6/5)‖ω‖₂²`), turning the omega_mub
cross-check's numerically-corroborated H2 into a proved identity. -/
theorem feasibility_eq_one_iff {ι : Type*} [Fintype ι] (c : ℝ) (hc : 0 < c)
    (ω : ι → ℝ) :
    1 - c * (∑ i, (ω i) ^ 2) = 1 ↔ ∀ i, ω i = 0 := by
  rw [sub_eq_self, mul_eq_zero]
  constructor
  · rintro (hc0 | hsum)
    · exact absurd hc0 hc.ne'
    · intro i
      have h2 : (ω i) ^ 2 = 0 :=
        (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg (ω j))).mp hsum i
          (Finset.mem_univ i)
      rw [pow_two] at h2
      exact mul_self_eq_zero.mp h2
  · intro h
    right
    exact Finset.sum_eq_zero (fun i _ => by rw [h i]; ring)

/-- **Weierstrass attainment, proved.** A continuous real function on a nonempty
compact space attains its minimum. This is the analytic step (ENC-1132(1)) that
`ExtensionObstruction.phi_is_min` previously took as a field. -/
theorem exists_min_on_compact {V : Type*} [TopologicalSpace V] [CompactSpace V]
    [Nonempty V] (φ : V → ℝ) (hcont : Continuous φ) :
    ∃ v₀ : V, ∀ v : V, φ v₀ ≤ φ v := by
  obtain ⟨v₀, -, hv₀⟩ := isCompact_univ.exists_isMinOn Set.univ_nonempty hcont.continuousOn
  exact ⟨v₀, fun v => isMinOn_iff.mp hv₀ v (Set.mem_univ v)⟩

/-- Build an `ExtensionObstruction` from a continuous nonnegative mass on a
nonempty compact configuration space — **discharging the attainment half of
`phi_is_min` by Weierstrass** rather than assuming it. Instantiating this at
`V = CP^{n-1}` (a compact space) with `mass = ‖ω(·)‖₁` continuous is the remaining
geometric setup; the attainment principle itself is now proved. -/
noncomputable def ExtensionObstruction.ofCompact {V : Type*} [TopologicalSpace V]
    [CompactSpace V] [Nonempty V] (mass : V → ℝ) (hmass : ∀ v, 0 ≤ mass v)
    (hcont : Continuous mass) : ExtensionObstruction V where
  mass := mass
  mass_nonneg := hmass
  phi := mass (exists_min_on_compact mass hcont).choose
  phi_is_min :=
    ⟨(exists_min_on_compact mass hcont).choose_spec,
     (exists_min_on_compact mass hcont).choose, rfl⟩

open scoped InnerProductSpace in
/-- **ENC-1131 Bianchi closure, proved from Parseval (real orthonormal basis).**
For an orthonormal basis `b` of a finite-dimensional `𝕜`-inner-product space and a
unit vector `v`, the curvature deviations `ωᵢ = ‖⟪bᵢ, v⟫‖² − 1/n` sum to zero.
This upgrades `bianchi_closure_zero` (which assumed the input `∑ g = 1`) to a real
geometric proof: `∑ᵢ‖⟪bᵢ,v⟫‖² = ‖v‖²` is Parseval (`OrthonormalBasis.sum_sq_norm_inner_right`),
and `‖v‖ = 1` closes it. The `Γ₂ = 0` "closed survivor" fact is now derived, not
assumed. -/
theorem parseval_bianchi {n : ℕ} {𝕜 E : Type*} [RCLike 𝕜]
    [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
    (b : OrthonormalBasis (Fin n) 𝕜 E) (v : E) (hv : ‖v‖ = 1) (hn : n ≠ 0) :
    (∑ i, (‖⟪b i, v⟫_𝕜‖ ^ 2 - 1 / (n : ℝ))) = 0 := by
  rw [bianchi_closure_algebraic hn (fun i => ‖⟪b i, v⟫_𝕜‖ ^ 2)]
  rw [b.sum_sq_norm_inner_right v, hv]
  norm_num

open scoped InnerProductSpace in
/-- **The curvature-mass objective is continuous** (ENC-1132(1) input). The map
`v ↦ ∑ᵢ |‖⟪eᵢ,v⟫‖² − c|` is continuous — a finite sum of compositions of the
continuous inner product, norm, square, subtraction, and `|·|`. -/
theorem continuous_curvature_mass {n : ℕ} {𝕜 E : Type*} [RCLike 𝕜]
    [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
    (e : Fin n → E) (c : ℝ) :
    Continuous (fun v => ∑ i, |‖⟪e i, v⟫_𝕜‖ ^ 2 - c|) := by
  refine continuous_finsetSum _ (fun i _ => ?_)
  exact (((continuous_const.inner continuous_id).norm.pow 2).sub continuous_const).abs

open scoped InnerProductSpace in
/-- **Concrete attainment of the obstruction on the unit sphere** (ENC-1132(1),
Weierstrass made concrete). On the unit sphere of a finite-dimensional (proper)
inner-product space, the *actual* curvature objective `∑ᵢ|‖⟪eᵢ,v⟫‖²−c|` attains
its minimum — promoting the abstract `exists_min_on_compact` to the real geometry.
The MUB instance is `c = 1/n`, `e =` the fixed MU-set vectors, `E = ℂⁿ`. -/
theorem curvature_mass_attains_min_on_sphere {n : ℕ} {𝕜 E : Type*} [RCLike 𝕜]
    [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [ProperSpace E]
    (e : Fin n → E) (c : ℝ) (hne : (Metric.sphere (0 : E) 1).Nonempty) :
    ∃ v₀ ∈ Metric.sphere (0 : E) 1, ∀ v ∈ Metric.sphere (0 : E) 1,
      (∑ i, |‖⟪e i, v₀⟫_𝕜‖ ^ 2 - c|) ≤ (∑ i, |‖⟪e i, v⟫_𝕜‖ ^ 2 - c|) := by
  obtain ⟨v₀, hv₀, hmin⟩ :=
    (isCompact_sphere (0 : E) 1).exists_isMinOn hne
      (continuous_curvature_mass (𝕜 := 𝕜) e c).continuousOn
  exact ⟨v₀, hv₀, fun v hv => isMinOn_iff.mp hmin v hv⟩

/-! ## Goal 1 — the no-go reduction, conditional only on the cited wall -/

open scoped InnerProductSpace in
/-- **The no-go reduction (keystone).** Given the cited feasibility wall
`f(v) = 1 − c·∑ᵢ(‖⟪eᵢ,v⟫‖² − target)² ≤ W < 1` for every unit vector (the
Invariant-Systems result `max f = W`), NO unit vector is mutually unbiased to the
fixed set `e` (`∀i, ‖⟪eᵢ,v⟫‖² = target`). A mutually-unbiased `v` makes every
`ωᵢ = 0`, so `feasibility_eq_one_iff` forces `f(v) = 1 > W` — contradiction. The
entire chain is machine-checked; the only input is the cited wall. -/
theorem no_mu_vector_of_wall {N : ℕ} {𝕜 E : Type*} [RCLike 𝕜]
    [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
    (e : Fin N → E) (target W c : ℝ) (hc : 0 < c) (hW : W < 1)
    (H1 : ∀ v : E, ‖v‖ = 1 →
      1 - c * (∑ i, (‖⟪e i, v⟫_𝕜‖ ^ 2 - target) ^ 2) ≤ W) :
    ∀ v : E, ‖v‖ = 1 → ¬ (∀ i, ‖⟪e i, v⟫_𝕜‖ ^ 2 = target) := by
  intro v hv hMU
  have hf1 : 1 - c * (∑ i, (‖⟪e i, v⟫_𝕜‖ ^ 2 - target) ^ 2) = 1 := by
    rw [feasibility_eq_one_iff c hc (fun i => ‖⟪e i, v⟫_𝕜‖ ^ 2 - target)]
    intro i; rw [hMU i]; ring
  have h2 := H1 v hv
  rw [hf1] at h2
  linarith

open scoped InnerProductSpace in
/-- **d=6 instance (ENC-1134), conditional ONLY on the cited wall.** No unit vector
of a `ℂ`-inner-product space is mutually unbiased to the 18 fixed vectors `e` of the
canonical triple `T0`, given the Invariant-Systems wall in its verified upstream
form `f = 1 − (6/5)·∑ᵢωᵢ² ≤ W = (88+3√6)/100`. (A fourth mutually-unbiased basis's
first vector would be such a `v`, so none extends `T0`.) Every step but the cited
wall `H1` is now machine-checked — `W < 1` is `W_lt_one`, the contradiction is the
keystone above. -/
theorem no_fourth_mu_vector_T0 {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E)
    (H1 : ∀ v : E, ‖v‖ = 1 →
      1 - (6 / 5) * (∑ i, (‖⟪e i, v⟫_ℂ‖ ^ 2 - 1 / 6) ^ 2) ≤ W) :
    ∀ v : E, ‖v‖ = 1 → ¬ (∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6) :=
  no_mu_vector_of_wall e (1 / 6) W (6 / 5) (by norm_num) W_lt_one H1

/-! ## Goal 2 (2a) — the finite-cover class no-go (Thm B / ENC-1133, computational) -/

/-- **Compactness half of Thm B.** A continuous, pointwise-positive obstruction on
a compact configuration class is *uniformly* positive (`∃ ε > 0, ε ≤ Φ`). -/
theorem uniform_pos_of_pointwise_pos {V : Type*} [TopologicalSpace V] [CompactSpace V]
    [Nonempty V] (Φ : V → ℝ) (hcont : Continuous Φ) (hpos : ∀ v, 0 < Φ v) :
    ∃ ε, 0 < ε ∧ ∀ v, ε ≤ Φ v := by
  obtain ⟨v₀, hv₀⟩ := exists_min_on_compact Φ hcont
  exact ⟨Φ v₀, hpos v₀, hv₀⟩

/-- **Computational half of Thm B — the class no-go.** If a configuration class `K`
is covered by finitely many patches `Uⱼ` (`j ∈ s`), each carrying a *certified*
positive lower bound `εⱼ ≤ Φ` on it, then `Φ > 0` on all of `K` — no member of `K`
is feasible (`Φ = 0`). This is precisely how finitely many local certificates (e.g.
the friend's interval / PSD certificates) certify a whole-class no-go. -/
theorem finite_cover_no_feasible {V ι : Type*} (s : Finset ι) (U : ι → Set V)
    (Φ : V → ℝ) (K : Set V)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ Φ v) (hpos : ∀ j ∈ s, 0 < ε j) :
    ∀ v ∈ K, 0 < Φ v := by
  intro v hv
  obtain ⟨j, hj, hvj⟩ := hcover v hv
  exact lt_of_lt_of_le (hpos j hj) (hbound j hj v hvj)

end ExtensionCurvatureObstruction
end MUB

-- Axiom hygiene: every proved core should rest only on the standard kernel axioms.
#print axioms MUB.ExtensionCurvatureObstruction.bianchi_closure_algebraic
#print axioms MUB.ExtensionCurvatureObstruction.bianchi_closure_zero
#print axioms MUB.ExtensionCurvatureObstruction.l1_sum_abs_eq_zero_iff
#print axioms MUB.ExtensionCurvatureObstruction.ExtensionObstruction.phi_eq_zero_iff
#print axioms MUB.ExtensionCurvatureObstruction.ExtensionObstruction.no_mu_vector_of_phi_pos
#print axioms MUB.ExtensionCurvatureObstruction.constUnit_no_mu_vector
#print axioms MUB.ExtensionCurvatureObstruction.finite_cover_min_pos
#print axioms MUB.ExtensionCurvatureObstruction.W_lt_one
#print axioms MUB.ExtensionCurvatureObstruction.d6_floor_pos
#print axioms MUB.ExtensionCurvatureObstruction.no_mu_vector_at_d6_floor
#print axioms MUB.ExtensionCurvatureObstruction.feasibility_eq_one_iff
#print axioms MUB.ExtensionCurvatureObstruction.exists_min_on_compact
#print axioms MUB.ExtensionCurvatureObstruction.ExtensionObstruction.ofCompact
#print axioms MUB.ExtensionCurvatureObstruction.parseval_bianchi
#print axioms MUB.ExtensionCurvatureObstruction.continuous_curvature_mass
#print axioms MUB.ExtensionCurvatureObstruction.curvature_mass_attains_min_on_sphere
#print axioms MUB.ExtensionCurvatureObstruction.no_mu_vector_of_wall
#print axioms MUB.ExtensionCurvatureObstruction.no_fourth_mu_vector_T0
#print axioms MUB.ExtensionCurvatureObstruction.uniform_pos_of_pointwise_pos
#print axioms MUB.ExtensionCurvatureObstruction.finite_cover_no_feasible
