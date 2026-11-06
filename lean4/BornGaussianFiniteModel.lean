import BornGaussianRationalNoColouring
import BornHermitianTraceRepresentation
import GleasonBornCompletion

/-!
# The Finite and Exact-Arithmetic Gleason Model over `ℚ(i)³`

AuthorityEffect: None.

This module completes the Phase 2 finite and exact-arithmetic Gleason development and its internal
mathematical interfaces across the existing modules (`BornGaussianRationalNoColouring`,
`BornHermitianTraceRepresentation`, `BornGaussianTomographyReduction`, `BornGaussianParallelogramRigidity`,
`GleasonGaussianBridge`, and `GleasonBornCompletion`):

1. **Five-Way Distinction of "Finite" (`FiniteFrameScenario` vs. `ℚ(i)³` vs. `nineAnchorsList`
   vs. `FixedAnchorBound` vs. `ApproachingAnchorFamily`)**:
   * (i) A genuinely finite measurement scenario (`FiniteFrameScenario`: a finite list of rays and
     orthogonal frames inside `ℚ(i)³`). We show that every global `IsFrameFunction` restricts to a
     scenario valuation (`global_frameFunction_restricts_to_scenario`), exhibit a concrete `{0, 1}`
     valuation on the 9-ray standard frame scenario (`nineAnchorSingleFrameScenario_admits_zero_one`),
     and contrast this with the 49-ray `NoColouring` obstruction (`no_zero_one_frame_function`) and
     the global `{0, 1/3, 2/3}`-valued nonquadratic counterexample `exoticQi3`
     (`finite_scenario_vs_global_frame_dichotomy`).
   * (ii) The 3-dimensional vector space `ℚ(i)³` over the infinite field `ℚ(i)`, which contains
     infinitely many pairwise non-collinear rays (`rayFamily_raySinSq_pos`) and infinitely many
     distinct orthogonal frames (`frameFamily_isFrame`).
   * (iii) The finite collection of 9 tomography anchors (`nineAnchorsList`) and their 6 completing
     axis-plane bisector partners (`sixBisectorPartnersList`), proving that any zero-weight frame
     residual vanishing on the 9 anchors automatically vanishes on all 15 anchor-bisector rays
     (`vanishes_on_six_bisector_partners`).
   * (iv) Finite presentations and fixed-anchor certificates (`FixedAnchorBound`).
   * (v) Directed families of finite rational approximations approaching the anchors
     (`ApproachingAnchorFamily`).

2. **Normalization and Boundedness Consequences**:
   * Zero-vector normalization (`normalizeAtZero`) preserves `IsFrameFunction`,
     `IsZeroWeightFrameFunction`, and `VanishesOnNineRays`.
   * Every nonnegative frame function satisfies `0 ≤ f v ≤ 1` (`nonneg_frameFunction_bounds`) and
     has residual bounded by `1 + (tomographyForm f).coeffNorm`
     (`abs_residual_le_one_add_coeffNorm_of_nonneg`), sharpening to `|residual f v| ≤ 1`
     whenever `0 ≤ quadRay (tomographyForm f) v ≤ 1`
     (`abs_residual_le_one_of_nonneg_and_quadRay_bounds`).

3. **Exact Bridge Between Operator-Level Effect Additivity and Ray-Level Quadratic Rigidity**:
   * Explicit bijection between `GVec` and `Fin 3 → GaussRat` (`vecOfGVec`, `gvecOfVec`) and between
     3×3 Hermitian Gaussian-rational matrices and `HermForm3` (`hermForm3OfGaussMatrix`,
     `gaussMatrixOfHermForm3`).
   * Every operator-level `EffectValuation (space 3)` restricts on rank-1 projectors `P (vecOfGVec v)`
     to `quadRay (hermForm3OfDensity W) v` (`effectValuation_rankOne_eq_quadRay`), inducing a
     nonnegative frame function satisfying `FactorsThroughRayProjLinear` with zero tomography
     residual (`rayValuationOfEffect_residual_eq_zero`).
   * Consequently, operator-level effect additivity unconditionally excludes `exoticQi3`, `s3`, `s7`,
     and every prime-indexed counterexample `(1 + sp p) / 3` without any topological continuity
     hypothesis (`no_effectValuation_induces_exoticQi3`, `no_effectValuation_induces_sp`).

4. **Exact Rational Equivalence of Vector-Level `IsArchimedeanContinuousAt` and Projective Ray-Level
   `IsPointwiseRayContinuousAt`**:
   * Purely rational proofs of `raySinSq u v₀ ≤ distSqVec u v₀ / normSqVec v₀`
     (`raySinSq_le_distSqVec_div`) and the exact orthogonal projection identity
     `distSqVec (GVec.smul (projScalar u v₀) u) v₀ = normSqVec v₀ * raySinSq u v₀`
     (`distSqVec_projScalar_smul`).
   * Equivalence theorem `isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt` for all
     scale-invariant functions on `ℚ(i)³ \ {0}` (including every `IsFrameFunction` and every
     `IsZeroWeightFrameFunction`).

5. **Fixed-Anchor Certificate Theory, Exact Meridian Pair Certificates, Prime-Valuation Obstructions,
   Coordinate-Refined Residuals, and Chinese Remainder Collisions (`TFQ-1057`)**:
   * Sufficiency of fixed-anchor certificate families with `r_k → 0` and fixed `A(x)` for proving
     `g x = 0` under pointwise ray continuity at the 9 anchors
     (`fixedAnchor_sufficiency_of_pointwiseRayContinuous_at_anchors`).
   * Exact 2-frame meridian antisymmetry `g witness_111 + g witness_neg211 = 0` and 0-remainder
     approaching-anchor certificate for the pair sum along `meridianApproachE1 t = (1 + t, 1, 1)`
     and `meridianApproachE23 t = (-2, 1 + t, 1 + t)` (`residual_witness111_add_neg211_eq_zero`,
     `meridian_pair_sum_eq_approaching_anchors`).
   * Necessary prime-valuation condition (`fixedAnchor_prime_valuation_obstruction`): any
     `FixedAnchorBound A r Y x` with `r < 1` and `sp p x ≠ 0` must contain a probe `y ∈ Y` with odd
     `p`-adic norm valuation `vpRat p (normSqVec y) % 2 ≠ 0`.
   * Coordinate-refined 3-adic residuals `s3_leadX` and `s3_leadAll`: both are bounded zero-weight
     anchor-vanishing residuals (`|·| ≤ 1`) equal to `1` at `witness_111`, while `s3_leadAll`
     vanishes on all vectors in the union of the three coordinate planes `u.x = 0 ∨ u.y = 0 ∨ u.z = 0`
     and on `perturbPosRay k` / `perturbNegRay k` for all `k`, forcing `1 ≤ r` for any certificate
     using only such probes (`fixedAnchor_obstruction_of_not_isLead3All`).
   * Chinese Remainder Archimedean/3-adic collision sequence `crtApproachE1 m = (1 + 9*(m+1), 1, 1)`
     satisfying `s3_leadAll (crtApproachE1 m) = 1` for all `m` while converging in projective ray
     distance `raySinSq` to `tomo_e1 = (1, 0, 0)` (`crtApproachE1_s3_leadAll_eq_one`,
     `crtApproachE1_raySinSq_tomo_e1_le`).

6. **Explicit Proof-Obligation Separations**:
   * Moving rational near-maximizers without a rational maximizing point
     (`moving_rational_near_maximizer_no_rational_maximizer`).
   * Linear accumulation `L * ε` of step-wise `ε` chain losses (`chain_step_error_accumulates`,
     `linearDriftChain_attains_bound`).
   * Scale-invariant `{0, 1}`-valued Dedekind ray cut `dedekindRayCut` on `ℚ(i)³ \ {0}` whose
     defining polynomial `3 * |u.y|⁴ - ‖u‖⁴` never vanishes on `ℚ(i)³ \ {0}` yet jumps by `1`
     between arbitrarily close rational rays (`dedekindRayCut_isScaleInvariantOnRays`,
     `dedekindRayCut_gap_ne_zero`, `dedekindRayCut_jump_on_pell_pair`).

7. **Track A (General-Value Rational Piron–Soler Chain & Polar–Equatorial Transfer) and Track B
   (Irrational-Locus / Dedekind-Cut Frame-Function Stress Tests) on `ℚ(i)³` (`TFQ-1057`)**:
   * Track A: General rational Piron orthogonal subadditivity (`rational_piron_subadditivity`,
     `nonneg_frameFunction_ortho_le_one_sub`), equatorial pole-deficiency frame decomposition
     (`isFrame_tomo_e1_eqOrtho`, `equatorial_pair_sum_eq_one_sub_pole`), general 2-frame
     meridian–Kelvin polar–equatorial transfer identities without assuming `f tomo_e1 = 1`
     (`meridian_kelvin_universal_bridge`, `meridian_kelvin_zeroWeight_bridge`), exact projective
     ray-distance duality `raySinSq (e₁ + y) e₁ = raySinSq (meridianOrtho y) y`
     (`meridianOrtho_raySinSq_eq`), and general-value 1-step, 2-step, 3-step Piron tangent chains
     and Pythagorean equatorial sandwich bounds with explicit pole-deficiency slack `1 - f tomo_e1`
     (`piron_general_one_step_le`, `piron_general_two_step_radial_le`,
     `piron_general_three_step_chain_le`, `pythagEqRot_general_sandwich`).
   * Track B: Local constancy and pointwise ray continuity of `dedekindRayCut` on explicit rational
     neighborhoods of `tomo_e1` (`raySinSq < 1 / 2`) and `tomo_e2` (`raySinSq < 1 / 3`) and at
     **every** nonzero vector `v₀ ∈ ℚ(i)³ \ {0}` (`dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt`,
     `dedekindRayCut_isPointwiseRayContinuousAt_tomo_e1`,
     `dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt`,
     `dedekindRayCut_isPointwiseRayContinuousAt_tomo_e2`,
     `dedekindRayCut_eventually_const`,
     `dedekindRayCut_isArchimedeanContinuousEverywhere`,
     `dedekindRayCut_isPointwiseRayContinuous`), general and `tomo_e1`-anchored orthogonal
     ray-distance Bessel bounds, `< 45°` polar-cap disjointness, and global vanishing of
     polar-cap-supported zero-weight residuals (`quadRay_rayProj_eq_one_sub_raySinSq`,
     `ortho_raySinSq_add_ge_one`, `not_both_raySinSq_lt_half_of_ortho`,
     `zero_of_zeroWeight_supported_in_polar_cap`, `ortho_raySinSq_tomo_e1_add_ge_one`,
     `not_both_raySinSq_tomo_e1_lt_half_of_ortho`),
     refutation of 3-frame additivity for `dedekindRayCut` and any `{0, 1}`-valued 1D latitude
     profile (`dedekindRayCut_not_isFrameFunction`, `yLatitudeFunction_std_and_bisector_constraints`,
     `no_zero_one_latitude_frameFunction`), and the two-frame Gaussian-norm latitude-halving identity
     `2 * f(a, b, a + b i) = f(a, b, 0) + f(0, 0, 1)` for coordinate-sign symmetric frame functions
     (`isFrame_gaussianHalving_base`, `isFrame_gaussianHalving_rot`,
     `coordSignSymmetric_gaussian_halving_identity`, `dedekindRayCut_isCoordSignSymmetric`,
     `dedekindRayCut_fails_gaussian_halving_at_1_2`).
   * Target 1 (`TFQ-1057` General-Anchor Meridian Coupling, Fixed-Anchor Isolation Obstruction, and
     Conditional Closures): general-anchor meridian partner `anchorMeridianOrtho a y` and zero-slack
     polar–equatorial transfer for any nonzero anchor `a ∈ ℚ(i)³` and orthogonal `y ∈ a⊥ \ {0}`
     (`inner_anchorMeridianStep_anchorMeridianOrtho`, `addVec_a_y_ne_zero_of_ortho`,
     `anchorMeridianOrtho_ne_zero_of_ortho`, `isFrame_anchor_meridian_base`,
     `isFrame_anchor_meridian_rot`, `anchor_meridian_kelvin_bridge`,
     `anchor_meridian_zeroWeight_bridge`, `anchorMeridianOrtho_raySinSq_eq`,
     `anchor_uniform_equatorial_continuity_of_anchor_continuous`,
     `multi_axis_uniform_equatorial_continuity_of_axes_continuous`,
     `nine_anchor_uniform_equatorial_continuity_of_anchors_continuous`), spherical 3-frame
     Pythagoras identity `raySinSq u a + raySinSq v a + raySinSq w a = 2`
     (`frame_raySinSq_sum_eq_two`, `anchor_frame_raySinSq_sum_eq_two`), two-frame cross-anchor
     proximity bound `raySinSq w a₃ ≤ raySinSq u a₁ + raySinSq v a₂` and fixed-anchor frame
     isolation obstruction (`frame_third_raySinSq_le_add_of_ortho_anchors`,
     `fixed_anchor_frame_isolation_obstruction`, `witness111_raySinSq_nineAnchors_le_two_thirds`,
     `ortho_witness111_raySinSq_nineAnchors_ge_one_third`,
     `frame_witness111_partners_isolated_from_nineAnchors`,
     `isFrame_witness_neg211_probe120_probe2m15`, `residual_witness111_eq_sum_in_fifth_ball`,
     `witness_neg211_isolation_one_eighth`, `perturbed_witness111_neg211_bounce_back`,
     `ortho_witness123_raySinSq_nine_and_six_ge`), genuine equivalence of uniform ray continuity and
     uniform meridian-step modulus (`HasUniformMeridianStepModulus`, `eq_of_raySinSq_eq_zero`,
     `isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus`), and conditional `TFQ-1057`
     closures, witness inhabitation, and necessary-and-sufficient characterizations from pointwise ray
     continuity and bounded anchor amplification (`HasBoundedAnchorAmplification`,
     `zero_of_pointwise_and_bounded_anchor_amplification`,
     `born_from_pointwise_and_bounded_anchor_amplification`,
     `born_density_matrix_of_pointwise_and_bounded_anchor_amplification`,
     `hasBoundedAnchorAmplificationOn_zero`,
     `hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous`,
     `uniformlyRayContinuous_iff_pointwise_and_bounded_anchor_amplification`,
     `hasDenseUniformModulusFromPointwise_quadRay`,
     `uniformlyRayContinuous_iff_pointwise_and_dense_uniform_modulus`).
-/

namespace BornFinite.GaussianFiniteModel

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open BornFinite.GaussianFrames.NoColouring BornFinite.GleasonBridge BornFinite.BornCompletion
open Matrix

/-! ### Section 1: The Five-Way Taxonomy of "Finite" in the Gleason Regime -/

/-- **(i) Genuinely finite measurement scenario**: a finite list of nonzero rays in `ℚ(i)³` together
with a finite list of orthogonal frames whose vectors belong to that ray list. -/
structure FiniteFrameScenario where
  rays : List GVec
  frames : List (GVec × GVec × GVec)
  rays_nonZero : ∀ v ∈ rays, v.NonZero
  frames_in_rays : ∀ fr ∈ frames, fr.1 ∈ rays ∧ fr.2.1 ∈ rays ∧ fr.2.2 ∈ rays
  frames_valid : ∀ fr ∈ frames, IsFrame fr.1 fr.2.1 fr.2.2

/-- A signed frame valuation on a finite measurement scenario `S`: sums to `1` on every frame in
`S.frames`. -/
def IsScenarioValuation (S : FiniteFrameScenario) (f : GVec → ℚ) : Prop :=
  ∀ fr ∈ S.frames, f fr.1 + f fr.2.1 + f fr.2.2 = 1

/-- A nonnegative frame valuation on a finite measurement scenario `S`. -/
def IsNonnegScenarioValuation (S : FiniteFrameScenario) (f : GVec → ℚ) : Prop :=
  IsScenarioValuation S f ∧ ∀ v ∈ S.rays, 0 ≤ f v

/-- A `{0, 1}`-valued (deterministic / noncontextual colouring) valuation on a finite scenario `S`. -/
def IsZeroOneScenarioValuation (S : FiniteFrameScenario) (f : GVec → ℚ) : Prop :=
  IsScenarioValuation S f ∧ ∀ v ∈ S.rays, f v = 0 ∨ f v = 1

/-- Every global frame function on `ℚ(i)³` restricts to a valid valuation on every finite scenario. -/
theorem global_frameFunction_restricts_to_scenario (S : FiniteFrameScenario) {f : GVec → ℚ}
    (hf : IsFrameFunction f) : IsScenarioValuation S f := by
  intro fr hfr
  exact hf fr.1 fr.2.1 fr.2.2 (S.frames_valid fr hfr)

/-- Every global nonnegative frame function restricts to a nonnegative valuation on every finite
scenario. -/
theorem global_nonneg_frameFunction_restricts_to_scenario (S : FiniteFrameScenario) {f : GVec → ℚ}
    (hf : IsFrameFunction f) (hnn : ∀ v : GVec, v.NonZero → 0 ≤ f v) :
    IsNonnegScenarioValuation S f :=
  ⟨global_frameFunction_restricts_to_scenario S hf,
   fun v hv => hnn v (S.rays_nonZero v hv)⟩

/-- The finite list of 9 tomography anchors in `ℚ(i)³`. -/
def nineAnchorsList : List GVec :=
  [tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23, tomo_e12i, tomo_e13i, tomo_e23i]

theorem nineAnchorsList_nonZero : ∀ v ∈ nineAnchorsList, v.NonZero := by
  intro v hv
  simp only [nineAnchorsList, List.mem_cons, List.not_mem_nil, or_false] at hv
  rcases hv with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact tomo_e1_nonZero
  · exact tomo_e2_nonZero
  · exact tomo_e3_nonZero
  · exact tomo_e12_nonZero
  · exact tomo_e13_nonZero
  · exact tomo_e23_nonZero
  · exact tomo_e12i_nonZero
  · exact tomo_e13i_nonZero
  · exact tomo_e23i_nonZero

/-- The finite measurement scenario consisting of the 9 tomography anchors and their internal
standard basis frame `(tomo_e1, tomo_e2, tomo_e3)`. -/
def nineAnchorSingleFrameScenario : FiniteFrameScenario where
  rays := nineAnchorsList
  frames := [(tomo_e1, tomo_e2, tomo_e3)]
  rays_nonZero := nineAnchorsList_nonZero
  frames_in_rays := by
    intro fr hfr
    simp only [List.mem_singleton] at hfr
    subst hfr
    simp [nineAnchorsList]
  frames_valid := by
    intro fr hfr
    simp only [List.mem_singleton] at hfr
    subst hfr
    exact frame_tomo_std

/-- Indicator valuation assigning `1` to vectors with `x ≠ 0 ∧ y = 0 ∧ z = 0` and `0` otherwise. -/
def indicatorXAxisVal (v : GVec) : ℚ :=
  if v.x ≠ 0 ∧ v.y = 0 ∧ v.z = 0 then 1 else 0

/-- The 9-anchor single-frame scenario admits an explicit `{0, 1}`-valued deterministic valuation. -/
theorem nineAnchorSingleFrameScenario_admits_zero_one :
    IsZeroOneScenarioValuation nineAnchorSingleFrameScenario indicatorXAxisVal := by
  refine ⟨?_, ?_⟩
  · intro fr hfr
    simp only [nineAnchorSingleFrameScenario, List.mem_singleton] at hfr
    subst hfr
    simp [indicatorXAxisVal, tomo_e1, tomo_e2, tomo_e3, gv, GaussRat.ext_iff]
  · intro v _hv
    by_cases h : v.x ≠ 0 ∧ v.y = 0 ∧ v.z = 0
    · right; simp [indicatorXAxisVal, h]
    · left; simp [indicatorXAxisVal, h]

/-- **Finite-Scenario vs. Global-Carrier Dichotomy.**
1. The finite 9-anchor single-frame scenario admits a `{0, 1}`-valued valuation.
2. Global `ℚ(i)³` (already on the 49-ray finite `CoordBox` of `BornGaussianRationalNoColouring`)
   admits **no** `{0, 1}`-valued frame function (`no_zero_one_frame_function`).
3. Global `ℚ(i)³` nevertheless admits the `{0, 1/3, 2/3}`-valued nonnegative frame function
   `exoticQi3` that is not the Rayleigh quotient of any `HermForm3`. -/
theorem finite_scenario_vs_global_frame_dichotomy :
    (∃ f : GVec → ℚ, IsZeroOneScenarioValuation nineAnchorSingleFrameScenario f) ∧
    (¬ ∃ f : GVec → ℚ, IsFrameFunction f ∧ ∀ v : GVec, v.NonZero → f v = 0 ∨ f v = 1) ∧
    (IsFrameFunction exoticQi3 ∧ (∀ v : GVec, v.NonZero → 0 ≤ exoticQi3 v) ∧
      ¬ ∃ ρ : HermForm3, ∀ v : GVec, v.NonZero → exoticQi3 v = quadRay ρ v) :=
  ⟨⟨indicatorXAxisVal, nineAnchorSingleFrameScenario_admits_zero_one⟩,
   fun ⟨f, hF, hB⟩ => no_zero_one_frame_function f hF hB,
   ⟨exoticQi3_isFrameFunction, fun v _ => (exoticQi3_bounds v).1, exoticQi3_not_quadratic⟩⟩

/-- **(ii) Infinite family of pairwise distinct rays and orthogonal frames in `ℚ(i)³`.** -/
def rayFamily (k : ℕ) : GVec := ⟨1, (k : GaussRat), 0⟩

def rayFamilyOrtho (k : ℕ) : GVec := ⟨-(k : GaussRat), 1, 0⟩

theorem rayFamily_nonZero (k : ℕ) : (rayFamily k).NonZero :=
  nonZero_of_x (by simp [rayFamily])

theorem rayFamilyOrtho_nonZero (k : ℕ) : (rayFamilyOrtho k).NonZero :=
  nonZero_of_y (by simp [rayFamilyOrtho])

/-- Every `k : ℕ` yields an exact orthogonal frame `(rayFamily k, rayFamilyOrtho k, tomo_e3)` in
`ℚ(i)³`. -/
theorem frameFamily_isFrame (k : ℕ) : IsFrame (rayFamily k) (rayFamilyOrtho k) tomo_e3 := by
  refine ⟨rayFamily_nonZero k, rayFamilyOrtho_nonZero k, tomo_e3_nonZero, ?_, ?_, ?_⟩
  · apply GaussRat.ext <;> simp [GVec.inner, rayFamily, rayFamilyOrtho]
  · apply GaussRat.ext <;> simp [GVec.inner, rayFamily, tomo_e3, gv]
  · apply GaussRat.ext <;> simp [GVec.inner, rayFamilyOrtho, tomo_e3, gv]

/-- Lagrange identity over `ℚ(i)³`: `‖u‖² ‖v‖² - |⟨u, v⟩|² = ‖cross u v‖²`. -/
theorem lagrange_normSqVec_cross (u v : GVec) :
    normSqVec u * normSqVec v - (GVec.inner u v).normSq = normSqVec (cross u v) := by
  exact (normSqVec_cross u v).symm

/-- `raySinSq u v = normSqVec (cross u v) / (normSqVec u * normSqVec v)` for nonzero `u, v`. -/
theorem raySinSq_eq_normSqVec_cross_div {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) :
    raySinSq u v = normSqVec (cross u v) / (normSqVec u * normSqVec v) := by
  have hnu : normSqVec u ≠ 0 := (normSqVec_pos_of_nonZero hu).ne'
  have hnv : normSqVec v ≠ 0 := (normSqVec_pos_of_nonZero hv).ne'
  unfold raySinSq
  rw [← lagrange_normSqVec_cross]
  field_simp

/-- Distinct indices `j ≠ k` produce distinct projective rays with `0 < raySinSq (rayFamily j) (rayFamily k)`. -/
theorem rayFamily_raySinSq_pos {j k : ℕ} (hjk : j ≠ k) :
    0 < raySinSq (rayFamily j) (rayFamily k) := by
  rw [raySinSq_eq_normSqVec_cross_div (rayFamily_nonZero j) (rayFamily_nonZero k)]
  apply div_pos
  · apply normSqVec_pos_of_nonZero
    right; right
    intro hz
    have hre := congrArg GaussRat.re hz
    simp only [cross, rayFamily, GaussRat.re_star, GaussRat.re_sub, GaussRat.re_mul,
      GaussRat.re_one, GaussRat.im_one, GaussRat.re_natCast,
      GaussRat.im_natCast, GaussRat.re_zero] at hre
    have hjkQ : (j : ℚ) ≠ (k : ℚ) := by exact_mod_cast hjk
    apply hjkQ
    linarith
  · exact mul_pos (normSqVec_pos_of_nonZero (rayFamily_nonZero j))
      (normSqVec_pos_of_nonZero (rayFamily_nonZero k))

/-- **(iii) The 6 completing axis-plane bisector partners of the 9 tomography anchors.** -/
def bisector_12_neg : GVec := ⟨1, -1, 0⟩
def bisector_12i_neg : GVec := ⟨1, -GaussRat.I, 0⟩
def bisector_13_neg : GVec := ⟨1, 0, -1⟩
def bisector_13i_neg : GVec := ⟨1, 0, -GaussRat.I⟩
def bisector_23_neg : GVec := ⟨0, 1, -1⟩
def bisector_23i_neg : GVec := ⟨0, 1, -GaussRat.I⟩

def sixBisectorPartnersList : List GVec :=
  [bisector_12_neg, bisector_12i_neg, bisector_13_neg,
   bisector_13i_neg, bisector_23_neg, bisector_23i_neg]

theorem isFrame_tomo_e3_e12_bisector : IsFrame tomo_e3 tomo_e12 bisector_12_neg := by
  refine ⟨tomo_e3_nonZero, tomo_e12_nonZero, nonZero_of_x (by simp [bisector_12_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e3, tomo_e12, bisector_12_neg, gv])

theorem isFrame_tomo_e3_e12i_bisector : IsFrame tomo_e3 tomo_e12i bisector_12i_neg := by
  refine ⟨tomo_e3_nonZero, tomo_e12i_nonZero, nonZero_of_x (by simp [bisector_12i_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e3, tomo_e12i, bisector_12i_neg, gv, GaussRat.I])

theorem isFrame_tomo_e2_e13_bisector : IsFrame tomo_e2 tomo_e13 bisector_13_neg := by
  refine ⟨tomo_e2_nonZero, tomo_e13_nonZero, nonZero_of_x (by simp [bisector_13_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e2, tomo_e13, bisector_13_neg, gv])

theorem isFrame_tomo_e2_e13i_bisector : IsFrame tomo_e2 tomo_e13i bisector_13i_neg := by
  refine ⟨tomo_e2_nonZero, tomo_e13i_nonZero, nonZero_of_x (by simp [bisector_13i_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e2, tomo_e13i, bisector_13i_neg, gv, GaussRat.I])

theorem isFrame_tomo_e1_e23_bisector : IsFrame tomo_e1 tomo_e23 bisector_23_neg := by
  refine ⟨tomo_e1_nonZero, tomo_e23_nonZero, nonZero_of_y (by simp [bisector_23_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e1, tomo_e23, bisector_23_neg, gv])

theorem isFrame_tomo_e1_e23i_bisector : IsFrame tomo_e1 tomo_e23i bisector_23i_neg := by
  refine ⟨tomo_e1_nonZero, tomo_e23i_nonZero, nonZero_of_y (by simp [bisector_23i_neg]), ?_, ?_, ?_⟩ <;>
    (ext <;> simp [GVec.inner, tomo_e1, tomo_e23i, bisector_23i_neg, gv, GaussRat.I])

/-- Any zero-weight frame residual vanishing on the 9 tomography anchors automatically vanishes on
all 6 completing axis-plane bisector partners (15 fixed rays in total). -/
theorem vanishes_on_six_bisector_partners {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g) :
    g bisector_12_neg = 0 ∧ g bisector_12i_neg = 0 ∧
    g bisector_13_neg = 0 ∧ g bisector_13i_neg = 0 ∧
    g bisector_23_neg = 0 ∧ g bisector_23i_neg = 0 := by
  obtain ⟨he1, he2, he3, he12, he13, he23, he12i, he13i, he23i⟩ := h9
  have h1 := hg _ _ _ isFrame_tomo_e3_e12_bisector
  have h2 := hg _ _ _ isFrame_tomo_e3_e12i_bisector
  have h3 := hg _ _ _ isFrame_tomo_e2_e13_bisector
  have h4 := hg _ _ _ isFrame_tomo_e2_e13i_bisector
  have h5 := hg _ _ _ isFrame_tomo_e1_e23_bisector
  have h6 := hg _ _ _ isFrame_tomo_e1_e23i_bisector
  refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith, by linarith⟩

/-! ### Section 2: Normalization and Boundedness Consequences -/

/-- Explicit ray-bound predicate `∀ v, v.NonZero → |g v| ≤ B` with a specified rational bound `B`. -/
def IsBoundedOnRaysBy (g : GVec → ℚ) (B : ℚ) : Prop :=
  ∀ v : GVec, v.NonZero → |g v| ≤ B

theorem isBoundedOnRays_of_isBoundedOnRaysBy {g : GVec → ℚ} {B : ℚ}
    (hB : 0 ≤ B) (h : IsBoundedOnRaysBy g B) : IsBoundedOnRays g :=
  ⟨B, hB, h⟩

/-- Canonical zero-normalization of a ray function at the origin `⟨0, 0, 0⟩`. -/
def normalizeAtZero (f : GVec → ℚ) (v : GVec) : ℚ :=
  if v.x = 0 ∧ v.y = 0 ∧ v.z = 0 then 0 else f v

@[simp] theorem normalizeAtZero_zero (f : GVec → ℚ) :
    normalizeAtZero f ⟨0, 0, 0⟩ = 0 := by
  simp [normalizeAtZero]

theorem normalizeAtZero_of_nonZero (f : GVec → ℚ) {v : GVec} (hv : v.NonZero) :
    normalizeAtZero f v = f v := by
  unfold normalizeAtZero
  have hnot : ¬ (v.x = 0 ∧ v.y = 0 ∧ v.z = 0) := by
    rintro ⟨hx, hy, hz⟩
    rcases hv with h | h | h <;> contradiction
  simp [hnot]

theorem normalizeAtZero_isFrameFunction {f : GVec → ℚ} (hf : IsFrameFunction f) :
    IsFrameFunction (normalizeAtZero f) := by
  intro u v w hfr
  rw [normalizeAtZero_of_nonZero f hfr.1,
      normalizeAtZero_of_nonZero f hfr.2.1,
      normalizeAtZero_of_nonZero f hfr.2.2.1]
  exact hf u v w hfr

theorem normalizeAtZero_isZeroWeightFrameFunction {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) :
    IsZeroWeightFrameFunction (normalizeAtZero g) := by
  intro u v w hfr
  rw [normalizeAtZero_of_nonZero g hfr.1,
      normalizeAtZero_of_nonZero g hfr.2.1,
      normalizeAtZero_of_nonZero g hfr.2.2.1]
  exact hg u v w hfr

/-- Unconditional explicit residual bound for any nonnegative frame function:
`|residual f v| ≤ 1 + (tomographyForm f).coeffNorm` on every nonzero ray. -/
theorem abs_residual_le_one_add_coeffNorm_of_nonneg {f : GVec → ℚ}
    (hf : IsNonnegFrameFunction f) :
    IsBoundedOnRaysBy (GaussianTomography.residual f) (1 + (tomographyForm f).coeffNorm) := by
  intro v hv
  unfold GaussianTomography.residual
  have hfb := nonneg_frameFunction_bounds hf hv
  have hfv_abs : |f v| ≤ 1 := abs_le.mpr ⟨by linarith [hfb.1], hfb.2⟩
  have hqb := abs_quadRay_le (tomographyForm f) hv
  have htri := abs_sub (f v) (quadRay (tomographyForm f) v)
  linarith

/-- Tight residual bound: whenever `0 ≤ f v ≤ 1` and `0 ≤ quadRay (tomographyForm f) v ≤ 1` (e.g.
when `tomographyForm f` is positive semidefinite of trace `1`), `|residual f v| ≤ 1`. -/
theorem abs_residual_le_one_of_nonneg_and_quadRay_bounds {f : GVec → ℚ}
    (hf : IsNonnegFrameFunction f)
    {v : GVec} (hv : v.NonZero)
    (hq0 : 0 ≤ quadRay (tomographyForm f) v)
    (hq1 : quadRay (tomographyForm f) v ≤ 1) :
    |GaussianTomography.residual f v| ≤ 1 := by
  obtain ⟨hf0, hf1⟩ := nonneg_frameFunction_bounds hf hv
  rw [abs_le]
  unfold GaussianTomography.residual
  constructor <;> linarith

/-! ### Section 3: Exact Bridge Between Operator-Level Effect Additivity and Ray-Level Rigidity -/

/-- Convert `v : GVec` to `Fin 3 → GaussRat`. -/
def vecOfGVec (v : GVec) : Fin 3 → GaussRat := ![v.x, v.y, v.z]

/-- Convert `x : Fin 3 → GaussRat` to `GVec`. -/
def gvecOfVec (x : Fin 3 → GaussRat) : GVec := ⟨x 0, x 1, x 2⟩

@[simp] theorem gvecOfVec_vecOfGVec (v : GVec) : gvecOfVec (vecOfGVec v) = v := by
  cases v; rfl

@[simp] theorem vecOfGVec_gvecOfVec (x : Fin 3 → GaussRat) : vecOfGVec (gvecOfVec x) = x := by
  funext i; fin_cases i <;> rfl

theorem vnorm_vecOfGVec (v : GVec) :
    HermitianCarrier.vnorm (vecOfGVec v) = normSqVec v := by
  simp [HermitianCarrier.vnorm, vecOfGVec, Fin.sum_univ_three, normSqVec]

theorem vecOfGVec_ne_zero_iff (v : GVec) :
    vecOfGVec v ≠ 0 ↔ v.NonZero := by
  constructor
  · intro h
    by_contra hnot
    simp only [GVec.NonZero, not_or, not_not] at hnot
    obtain ⟨hx, hy, hz⟩ := hnot
    apply h
    funext i; fin_cases i <;> simp [vecOfGVec, hx, hy, hz]
  · intro hv h0
    rcases hv with hx | hy | hz
    · exact hx (by simpa [vecOfGVec] using congrFun h0 0)
    · exact hy (by simpa [vecOfGVec] using congrFun h0 1)
    · exact hz (by simpa [vecOfGVec] using congrFun h0 2)

/-- Extract the 9 rational parameters of `HermForm3` from a 3×3 Gaussian-rational matrix. -/
def hermForm3OfGaussMatrix (M : Matrix (Fin 3) (Fin 3) GaussRat) : HermForm3 where
  d1 := (M 0 0).re
  d2 := (M 1 1).re
  d3 := (M 2 2).re
  a12 := (M 0 1).re
  a13 := (M 0 2).re
  a23 := (M 1 2).re
  b12 := (M 0 1).im
  b13 := (M 0 2).im
  b23 := (M 1 2).im

/-- Construct the 3×3 Hermitian Gaussian-rational matrix of `ρ : HermForm3`. -/
def gaussMatrixOfHermForm3 (ρ : HermForm3) : Matrix (Fin 3) (Fin 3) GaussRat :=
  !![⟨ρ.d1, 0⟩, ⟨ρ.a12, ρ.b12⟩, ⟨ρ.a13, ρ.b13⟩;
     star ⟨ρ.a12, ρ.b12⟩, ⟨ρ.d2, 0⟩, ⟨ρ.a23, ρ.b23⟩;
     star ⟨ρ.a13, ρ.b13⟩, star ⟨ρ.a23, ρ.b23⟩, ⟨ρ.d3, 0⟩]

/-- For any Hermitian 3×3 Gaussian-rational matrix `M` (`Mᴴ = M`), its Hermitian quadratic form
`HermitianCarrier.hf M (vecOfGVec v)` equals `quadNum (hermForm3OfGaussMatrix M) v`. -/
theorem hf_eq_quadNum_hermForm3OfGaussMatrix {M : Matrix (Fin 3) (Fin 3) GaussRat}
    (hM : Mᴴ = M) (v : GVec) :
    HermitianCarrier.hf M (vecOfGVec v) = quadNum (hermForm3OfGaussMatrix M) v := by
  have h10 : M 1 0 = star (M 0 1) := by
    have := congrFun (congrFun hM 1) 0
    simpa [Matrix.conjTranspose_apply] using this.symm
  have h20 : M 2 0 = star (M 0 2) := by
    have := congrFun (congrFun hM 2) 0
    simpa [Matrix.conjTranspose_apply] using this.symm
  have h21 : M 2 1 = star (M 1 2) := by
    have := congrFun (congrFun hM 2) 1
    simpa [Matrix.conjTranspose_apply] using this.symm
  have h00 : (M 0 0).im = 0 := by
    have := congrArg GaussRat.im (congrFun (congrFun hM 0) 0)
    simp only [Matrix.conjTranspose_apply, GaussRat.im_star] at this
    linarith
  have h11 : (M 1 1).im = 0 := by
    have := congrArg GaussRat.im (congrFun (congrFun hM 1) 1)
    simp only [Matrix.conjTranspose_apply, GaussRat.im_star] at this
    linarith
  have h22 : (M 2 2).im = 0 := by
    have := congrArg GaussRat.im (congrFun (congrFun hM 2) 2)
    simp only [Matrix.conjTranspose_apply, GaussRat.im_star] at this
    linarith
  rw [HermitianCarrier.hf_eq_sum_sum]
  simp [Fin.sum_univ_three, vecOfGVec, h10, h20, h21, quadNum, hermForm3OfGaussMatrix,
    GaussRat.normSq, h00, h11, h22]
  ring

/-- The `HermForm3` extracted from the representing density matrix of a 3D effect valuation `W`. -/
noncomputable def hermForm3OfDensity
    (W : EffectValuation (HermitianCarrier.space 3)) : HermForm3 :=
  hermForm3OfGaussMatrix (HermitianCarrier.density W)

theorem hermForm3OfDensity_tr (W : EffectValuation (HermitianCarrier.space 3)) :
    (hermForm3OfDensity W).tr = 1 := by
  have htr := HermitianCarrier.density_re_trace W
  simpa [HermForm3.tr, hermForm3OfDensity, hermForm3OfGaussMatrix, Matrix.trace,
    Fin.sum_univ_three, GaussRat.re_add] using htr

/-- **Exact Bridge Theorem (`EffectValuation (space 3)` → `quadRay`).**
For every 3D Gaussian-rational effect valuation `W : EffectValuation (space 3)` and every nonzero
vector `v : GVec`, the valuation on the rank-1 effect `P (vecOfGVec v)` equals the Rayleigh quotient
`quadRay (hermForm3OfDensity W) v`. -/
theorem effectValuation_rankOne_eq_quadRay
    (W : EffectValuation (HermitianCarrier.space 3)) {v : GVec} (hv : v.NonZero) :
    W.v (HermitianCarrier.P (vecOfGVec v)) = quadRay (hermForm3OfDensity W) v := by
  have hx : vecOfGVec v ≠ 0 := (vecOfGVec_ne_zero_iff v).mpr hv
  rw [HermitianCarrier.born_rule W hx, vnorm_vecOfGVec,
      hf_eq_quadNum_hermForm3OfGaussMatrix (HermitianCarrier.density_hermitian W) v]
  rfl

/-- The ray function on `GVec` induced by an operator-level effect valuation `W`. -/
noncomputable def rayValuationOfEffect
    (W : EffectValuation (HermitianCarrier.space 3)) (v : GVec) : ℚ :=
  quadRay (hermForm3OfDensity W) v

theorem rayValuationOfEffect_eq_on_nonZero
    (W : EffectValuation (HermitianCarrier.space 3)) {v : GVec} (hv : v.NonZero) :
    rayValuationOfEffect W v = W.v (HermitianCarrier.P (vecOfGVec v)) :=
  (effectValuation_rankOne_eq_quadRay W hv).symm

theorem rayValuationOfEffect_isFrameFunction
    (W : EffectValuation (HermitianCarrier.space 3)) :
    IsFrameFunction (rayValuationOfEffect W) :=
  quadRay_isFrameFunction (hermForm3OfDensity W) (hermForm3OfDensity_tr W)

theorem rayValuationOfEffect_nonneg
    (W : EffectValuation (HermitianCarrier.space 3)) {v : GVec} (hv : v.NonZero) :
    0 ≤ rayValuationOfEffect W v := by
  rw [rayValuationOfEffect_eq_on_nonZero W hv]
  exact W.nonneg _ (HermitianCarrier.rankOne_effect ((vecOfGVec_ne_zero_iff v).mpr hv))

theorem rayValuationOfEffect_factorsThroughRayProjLinear
    (W : EffectValuation (HermitianCarrier.space 3)) :
    FactorsThroughRayProjLinear (rayValuationOfEffect W) :=
  quadRay_factorsThroughRayProjLinear (hermForm3OfDensity W)

theorem rayValuationOfEffect_residual_eq_zero
    (W : EffectValuation (HermitianCarrier.space 3)) (v : GVec) :
    GaussianTomography.residual (rayValuationOfEffect W) v = 0 := by
  have htomo : tomographyForm (rayValuationOfEffect W) = hermForm3OfDensity W :=
    tomographyForm_quadRay (hermForm3OfDensity W)
  unfold GaussianTomography.residual
  rw [htomo, rayValuationOfEffect]
  ring

/-- Operator-level effect additivity (`EffectValuation (space 3)`) unconditionally excludes
`exoticQi3` without any topological continuity hypothesis. -/
theorem no_effectValuation_induces_exoticQi3 :
    ¬ ∃ W : EffectValuation (HermitianCarrier.space 3),
      ∀ v : GVec, v.NonZero → W.v (HermitianCarrier.P (vecOfGVec v)) = exoticQi3 v := by
  rintro ⟨W, hW⟩
  have hquad : ∀ v : GVec, v.NonZero → exoticQi3 v = quadRay (hermForm3OfDensity W) v := by
    intro v hv
    rw [← hW v hv, effectValuation_rankOne_eq_quadRay W hv]
  exact exoticQi3_not_quadratic ⟨hermForm3OfDensity W, hquad⟩

/-- Operator-level effect additivity unconditionally excludes `(1 + sp p) / 3` for every inert prime
`p` (`InertPrimeSpec p`) admitting a nonzero witness `v₀` with `sp p v₀ ≠ 0`. -/
theorem no_effectValuation_induces_sp {p : ℕ} (hP : InertPrimeSpec p)
    {v₀ : GVec} (hv₀ : v₀.NonZero) (hne : sp p v₀ ≠ 0) :
    ¬ ∃ W : EffectValuation (HermitianCarrier.space 3),
      ∀ v : GVec, v.NonZero →
        W.v (HermitianCarrier.P (vecOfGVec v)) = (1 + sp p v) / 3 := by
  rintro ⟨W, hW⟩
  let f : GVec → ℚ := fun v => (1 + sp p v) / 3
  have hf_eq : ∀ v : GVec, v.NonZero → f v = quadRay (hermForm3OfDensity W) v := by
    intro v hv
    show (1 + sp p v) / 3 = quadRay (hermForm3OfDensity W) v
    rw [← hW v hv, effectValuation_rankOne_eq_quadRay W hv]
  obtain ⟨h1, h2, h3, h12, h13, h23, h12i, h13i, h23i⟩ := sp_vanishes_on_nine_rays hP.ge_three
  have hm : tomographyForm f = hermForm3OfDensity W := by
    apply tomography_unique (tomographyForm f) (hermForm3OfDensity W)
    · rw [(tomography_matches_nine_rays f).1, hf_eq tomo_e1 tomo_e1_nonZero]
    · rw [(tomography_matches_nine_rays f).2.1, hf_eq tomo_e2 tomo_e2_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.1, hf_eq tomo_e3 tomo_e3_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.1, hf_eq tomo_e12 tomo_e12_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.2.1, hf_eq tomo_e13 tomo_e13_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.2.2.1, hf_eq tomo_e23 tomo_e23_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.1, hf_eq tomo_e12i tomo_e12i_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.1, hf_eq tomo_e13i tomo_e13i_nonZero]
    · rw [(tomography_matches_nine_rays f).2.2.2.2.2.2.2.2, hf_eq tomo_e23i tomo_e23i_nonZero]
  have hρ_id : hermForm3OfDensity W = ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ := by
    rw [← hm]
    ext <;> simp [tomographyForm, f, h1, h2, h3, h12, h13, h23, h12i, h13i, h23i]
  have hq_third : quadRay ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v₀ = 1 / 3 := by
    have hnz := normSqVec_ne_zero_of_nonZero hv₀
    have hnum : quadNum ⟨1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0, 0, 0⟩ v₀ = (1 / 3) * normSqVec v₀ := by
      simp only [quadNum, normSqVec]
      ring
    rw [quadRay, hnum, mul_div_cancel_right₀ (1 / 3) hnz]
  have hv₀_val := hf_eq v₀ hv₀
  rw [hρ_id, hq_third] at hv₀_val
  change (1 + sp p v₀) / 3 = 1 / 3 at hv₀_val
  apply hne
  linarith

/-! ### Section 4: Equivalence of Vector-Level and Projective Ray-Level Pointwise Continuity -/

/-- Projective ray-level pointwise continuity at `v₀ : GVec` with respect to `raySinSq`. -/
def IsPointwiseRayContinuousAt (g : GVec → ℚ) (v₀ : GVec) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
    ∀ v : GVec, v.NonZero → raySinSq v v₀ < δ → |g v - g v₀| < ε

/-- Projective ray-level pointwise continuity at every nonzero vector of `ℚ(i)³`. -/
def IsPointwiseRayContinuous (g : GVec → ℚ) : Prop :=
  ∀ v₀ : GVec, v₀.NonZero → IsPointwiseRayContinuousAt g v₀

/-- Scale invariance on rays of `ℚ(i)³ \ {0}`. -/
def IsScaleInvariantOnRays (g : GVec → ℚ) : Prop :=
  ∀ v : GVec, v.NonZero → ∀ c : GaussRat, c ≠ 0 → g (GVec.smul c v) = g v

theorem isScaleInvariantOnRays_of_isFrameFunction {f : GVec → ℚ} (hf : IsFrameFunction f) :
    IsScaleInvariantOnRays f :=
  fun _v hv _c hc => GaussianFrames.frameFunction_smul hf hv hc

theorem isScaleInvariantOnRays_of_isZeroWeightFrameFunction {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) : IsScaleInvariantOnRays g :=
  fun _v hv _c hc => zeroWeightFrameFunction_smul hg hv hc

/-- Purely algebraic identity over `ℚ(i)³`:
`‖u‖² ‖u - v₀‖² - (‖u‖² ‖v₀‖² - |⟨u, v₀⟩|²) = |⟨u, u - v₀⟩|²`. -/
theorem normSqVec_mul_distSqVec_sub_lagrange (u v₀ : GVec) :
    normSqVec u * distSqVec u v₀ - (normSqVec u * normSqVec v₀ - (GVec.inner u v₀).normSq) =
      (GVec.inner u (GVec.sub u v₀)).normSq := by
  simp only [normSqVec, distSqVec, GVec.inner, GVec.sub, GaussRat.normSq,
    GaussRat.re_add, GaussRat.im_add, GaussRat.re_sub, GaussRat.im_sub,
    GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star]
  ring

/-- Purely rational estimate: `raySinSq u v₀ ≤ distSqVec u v₀ / normSqVec v₀` for nonzero `u, v₀`. -/
theorem raySinSq_le_distSqVec_div {u v₀ : GVec} (hu : u.NonZero) (hv₀ : v₀.NonZero) :
    raySinSq u v₀ ≤ distSqVec u v₀ / normSqVec v₀ := by
  have hnu : 0 < normSqVec u := normSqVec_pos_of_nonZero hu
  have hnv : 0 < normSqVec v₀ := normSqVec_pos_of_nonZero hv₀
  have hid := normSqVec_mul_distSqVec_sub_lagrange u v₀
  have hnn : 0 ≤ (GVec.inner u (GVec.sub u v₀)).normSq := GaussRat.normSq_nonneg _
  have hle : normSqVec u * normSqVec v₀ - (GVec.inner u v₀).normSq ≤
      normSqVec u * distSqVec u v₀ := by linarith
  have hray : raySinSq u v₀ =
      (normSqVec u * normSqVec v₀ - (GVec.inner u v₀).normSq) / (normSqVec u * normSqVec v₀) := by
    unfold raySinSq
    field_simp
  rw [hray, div_le_div_iff₀ (mul_pos hnu hnv) hnv]
  nlinarith

/-- Gaussian-rational orthogonal projection scalar `c = ⟨u, v₀⟩ / ‖u‖²` projecting `v₀` onto `u`. -/
def projScalar (u v₀ : GVec) : GaussRat :=
  ⟨(GVec.inner u v₀).re / normSqVec u, (GVec.inner u v₀).im / normSqVec u⟩

theorem projScalar_normSq (u v₀ : GVec) :
    (projScalar u v₀).normSq = (GVec.inner u v₀).normSq / (normSqVec u) ^ 2 := by
  simp only [projScalar, GaussRat.normSq]
  ring

theorem projScalar_ne_zero_of_raySinSq_lt_one {u v₀ : GVec}
    (hu : u.NonZero) (hv₀ : v₀.NonZero) (h : raySinSq u v₀ < 1) :
    projScalar u v₀ ≠ 0 := by
  have hnu : 0 < normSqVec u := normSqVec_pos_of_nonZero hu
  have hnv : 0 < normSqVec v₀ := normSqVec_pos_of_nonZero hv₀
  unfold raySinSq at h
  have hpos_div : 0 < (GVec.inner u v₀).normSq / (normSqVec u * normSqVec v₀) := by linarith
  have hpos_ip : 0 < (GVec.inner u v₀).normSq := by
    by_contra hle
    have h0 : (GVec.inner u v₀).normSq ≤ 0 := not_lt.mp hle
    have : (GVec.inner u v₀).normSq / (normSqVec u * normSqVec v₀) ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg h0 (mul_pos hnu hnv).le
    linarith
  intro hc0
  have hns0 : (projScalar u v₀).normSq = 0 := by rw [hc0]; simp [GaussRat.normSq]
  rw [projScalar_normSq] at hns0
  have : (GVec.inner u v₀).normSq / (normSqVec u) ^ 2 > 0 := div_pos hpos_ip (pow_pos hnu 2)
  linarith

theorem distSqVec_eq_normSqVec_sub_two_re_inner (w v₀ : GVec) :
    distSqVec w v₀ = normSqVec w - 2 * (GVec.inner w v₀).re + normSqVec v₀ := by
  simp only [distSqVec, normSqVec, GVec.inner, GaussRat.normSq,
    GaussRat.re_add, GaussRat.re_sub, GaussRat.im_sub,
    GaussRat.re_mul, GaussRat.re_star, GaussRat.im_star]
  ring

theorem inner_projScalar_smul_re (u v₀ : GVec) :
    (GVec.inner (GVec.smul (projScalar u v₀) u) v₀).re =
      (GVec.inner u v₀).normSq / normSqVec u := by
  rw [inner_smul_left]
  simp only [projScalar, GaussRat.normSq, GaussRat.re_mul, GaussRat.re_star, GaussRat.im_star]
  ring

/-- **Exact Rational Projection Identity.**
For every nonzero `u : GVec` and every `v₀ : GVec`, the Euclidean squared distance from the
projected vector `GVec.smul (projScalar u v₀) u` on the ray of `u` to `v₀` is literally
`normSqVec v₀ * raySinSq u v₀`. -/
theorem distSqVec_projScalar_smul {u : GVec} (hu : u.NonZero) (v₀ : GVec) :
    distSqVec (GVec.smul (projScalar u v₀) u) v₀ = normSqVec v₀ * raySinSq u v₀ := by
  have hnu : normSqVec u ≠ 0 := (normSqVec_pos_of_nonZero hu).ne'
  rw [distSqVec_eq_normSqVec_sub_two_re_inner, normSqVec_smul, projScalar_normSq,
      inner_projScalar_smul_re, raySinSq]
  by_cases hnv₀ : normSqVec v₀ = 0
  · have hip0 : (GVec.inner u v₀).normSq = 0 := by
      have hle : (GVec.inner u v₀).normSq ≤ normSqVec u * normSqVec v₀ := by
        have := lagrange_normSqVec_cross u v₀
        have := normSqVec_nonneg (cross u v₀)
        linarith
      rw [hnv₀, mul_zero] at hle
      exact le_antisymm hle (GaussRat.normSq_nonneg _)
    simp [hnv₀, hip0]
  · field_simp
    ring

/-- Projective ray continuity at `v₀` implies vector-level Archimedean continuity at `v₀`. -/
theorem isArchimedeanContinuousAt_of_isPointwiseRayContinuousAt {g : GVec → ℚ} {v₀ : GVec}
    (hv₀ : v₀.NonZero) (hray : IsPointwiseRayContinuousAt g v₀) :
    IsArchimedeanContinuousAt g v₀ := by
  intro ε hε
  obtain ⟨δ, hδ, h⟩ := hray ε hε
  have hnv₀ : 0 < normSqVec v₀ := normSqVec_pos_of_nonZero hv₀
  refine ⟨δ * normSqVec v₀, mul_pos hδ hnv₀, ?_⟩
  intro v hv hdist
  apply h v hv
  calc raySinSq v v₀ ≤ distSqVec v v₀ / normSqVec v₀ := raySinSq_le_distSqVec_div hv hv₀
    _ < (δ * normSqVec v₀) / normSqVec v₀ := (div_lt_div_iff_of_pos_right hnv₀).mpr hdist
    _ = δ := mul_div_cancel_right₀ δ hnv₀.ne'

/-- For any scale-invariant function `g` on rays, vector-level Archimedean continuity at `v₀`
implies projective ray continuity at `v₀`. -/
theorem isPointwiseRayContinuousAt_of_isArchimedeanContinuousAt {g : GVec → ℚ} {v₀ : GVec}
    (hv₀ : v₀.NonZero) (hscale : IsScaleInvariantOnRays g)
    (hvec : IsArchimedeanContinuousAt g v₀) :
    IsPointwiseRayContinuousAt g v₀ := by
  intro ε hε
  obtain ⟨δ, hδ, h⟩ := hvec ε hε
  have hnv₀ : 0 < normSqVec v₀ := normSqVec_pos_of_nonZero hv₀
  let δ_ray : ℚ := min 1 (δ / normSqVec v₀)
  have hδ_ray_pos : 0 < δ_ray := lt_min one_pos (div_pos hδ hnv₀)
  refine ⟨δ_ray, hδ_ray_pos, ?_⟩
  intro u hu hsin
  have hsin1 : raySinSq u v₀ < 1 := lt_of_lt_of_le hsin (min_le_left _ _)
  have hsin_div : raySinSq u v₀ < δ / normSqVec v₀ := lt_of_lt_of_le hsin (min_le_right _ _)
  let c := projScalar u v₀
  have hc : c ≠ 0 := projScalar_ne_zero_of_raySinSq_lt_one hu hv₀ hsin1
  have hcu_nz : (GVec.smul c u).NonZero := nonZero_smul hc hu
  have hdist : distSqVec (GVec.smul c u) v₀ < δ := by
    rw [distSqVec_projScalar_smul hu v₀]
    calc normSqVec v₀ * raySinSq u v₀ < normSqVec v₀ * (δ / normSqVec v₀) :=
          mul_lt_mul_of_pos_left hsin_div hnv₀
      _ = δ := mul_div_cancel₀ δ hnv₀.ne'
  rw [← hscale u hu c hc]
  exact h (GVec.smul c u) hcu_nz hdist

/-- **Equivalence Theorem.** For every scale-invariant function `g` on `ℚ(i)³ \ {0}`, projective
ray-level pointwise continuity at `v₀` is equivalent to vector-level Archimedean continuity at `v₀`. -/
theorem isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt {g : GVec → ℚ} {v₀ : GVec}
    (hv₀ : v₀.NonZero) (hscale : IsScaleInvariantOnRays g) :
    IsPointwiseRayContinuousAt g v₀ ↔ IsArchimedeanContinuousAt g v₀ :=
  ⟨isArchimedeanContinuousAt_of_isPointwiseRayContinuousAt hv₀,
   isPointwiseRayContinuousAt_of_isArchimedeanContinuousAt hv₀ hscale⟩

/-- Global equivalence between `IsPointwiseRayContinuous` and `IsArchimedeanContinuousEverywhere`
for scale-invariant functions on `ℚ(i)³ \ {0}`. -/
theorem isPointwiseRayContinuous_iff_isArchimedeanContinuousEverywhere {g : GVec → ℚ}
    (hscale : IsScaleInvariantOnRays g) :
    IsPointwiseRayContinuous g ↔ IsArchimedeanContinuousEverywhere g :=
  ⟨fun h v₀ hv₀ => (isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt hv₀ hscale).mp (h v₀ hv₀),
   fun h v₀ hv₀ => (isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt hv₀ hscale).mpr (h v₀ hv₀)⟩

/-- Uniform ray continuity implies pointwise ray continuity at every nonzero vector. -/
theorem isPointwiseRayContinuous_of_isUniformlyRayContinuous {f : GVec → ℚ}
    (hu : IsUniformlyRayContinuous f) : IsPointwiseRayContinuous f := by
  intro v₀ hv₀ ε hε
  obtain ⟨δ, hδ, h⟩ := hu ε hε
  exact ⟨δ, hδ, fun v hv hsin => h v v₀ hv hv₀ hsin⟩

/-- The 3-adic residual `s3` fails projective pointwise ray continuity at `tomo_e1 = (1, 0, 0)`. -/
theorem not_isPointwiseRayContinuousAt_s3_tomo_e1 :
    ¬ IsPointwiseRayContinuousAt s3 tomo_e1 := by
  intro hray
  exact not_archimedeanContinuousAt_s3_tomo_e1
    (isArchimedeanContinuousAt_of_isPointwiseRayContinuousAt tomo_e1_nonZero hray)

/-- The 7-adic residual `s7` fails projective pointwise ray continuity at `tomo_e1 = (1, 0, 0)`. -/
theorem not_isPointwiseRayContinuousAt_s7_tomo_e1 :
    ¬ IsPointwiseRayContinuousAt s7 tomo_e1 := by
  intro hray
  exact not_archimedeanContinuousAt_s7_tomo_e1
    (isArchimedeanContinuousAt_of_isPointwiseRayContinuousAt tomo_e1_nonZero hray)

/-- `exoticQi3` fails projective pointwise ray continuity at `tomo_e1 = (1, 0, 0)`. -/
theorem not_isPointwiseRayContinuousAt_exoticQi3_tomo_e1 :
    ¬ IsPointwiseRayContinuousAt exoticQi3 tomo_e1 := by
  intro hray
  exact not_archimedeanContinuousAt_exoticQi3_tomo_e1
    (isArchimedeanContinuousAt_of_isPointwiseRayContinuousAt tomo_e1_nonZero hray)

/-! ### Section 5: Fixed-Anchor Certificates, Meridian Pair Identities, and Obstructions -/

/-- Maximum of `|g y|` over a finite list of probe vectors `Y : List GVec` (`0` on `[]`). -/
def maxAbsOnList (g : GVec → ℚ) (Y : List GVec) : ℚ :=
  Y.foldr (fun y acc => max |g y| acc) 0

theorem maxAbsOnList_nonneg (g : GVec → ℚ) (Y : List GVec) :
    0 ≤ maxAbsOnList g Y := by
  induction Y with
  | nil => rfl
  | cons y ys ih => exact le_max_of_le_right ih

theorem abs_le_maxAbsOnList (g : GVec → ℚ) {Y : List GVec} {y : GVec} (hy : y ∈ Y) :
    |g y| ≤ maxAbsOnList g Y := by
  induction Y with
  | nil => contradiction
  | cons z zs ih =>
    simp only [List.mem_cons] at hy
    rcases hy with rfl | hmem
    · exact le_max_left _ _
    · exact le_trans (ih hmem) (le_max_right _ _)

theorem maxAbsOnList_le_of_forall {g : GVec → ℚ} {Y : List GVec} {M : ℚ} (hM : 0 ≤ M)
    (h : ∀ y ∈ Y, |g y| ≤ M) : maxAbsOnList g Y ≤ M := by
  induction Y with
  | nil => exact hM
  | cons y ys ih =>
    simp only [maxAbsOnList, List.foldr_cons, max_le_iff]
    exact ⟨h y (List.mem_cons.mpr (Or.inl rfl)),
           ih (fun z hz => h z (List.mem_cons.mpr (Or.inr hz)))⟩

theorem maxAbsOnList_eq_zero_of_forall_zero {g : GVec → ℚ} {Y : List GVec}
    (h : ∀ y ∈ Y, g y = 0) : maxAbsOnList g Y = 0 := by
  apply le_antisymm
  · apply maxAbsOnList_le_of_forall le_rfl
    intro y hy
    rw [h y hy, abs_zero]
  · exact maxAbsOnList_nonneg g Y

/-- **(iv) Fixed-Anchor Certificate Bound (`FixedAnchorBound A r Y x`).**
States that for every bounded zero-weight residual `g` vanishing at the 9 tomography anchors with
`|g| ≤ B`, `|g x| ≤ A * max_{y ∈ Y} |g y| + B * r`. -/
def FixedAnchorBound (A r : ℚ) (Y : List GVec) (x : GVec) : Prop :=
  ∀ (g : GVec → ℚ) (B : ℚ), 0 ≤ B →
    IsZeroWeightFrameFunction g → VanishesOnNineRays g → IsBoundedOnRaysBy g B →
    |g x| ≤ A * maxAbsOnList g Y + B * r

/-- Vanishing on `nineAnchorsList` is equivalent to `VanishesOnNineRays`. -/
theorem vanishesOnNineRays_iff_forall_nineAnchorsList (g : GVec → ℚ) :
    VanishesOnNineRays g ↔ ∀ a ∈ nineAnchorsList, g a = 0 := by
  constructor
  · rintro ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ a ha
    simp only [nineAnchorsList, List.mem_cons, List.not_mem_nil, or_false] at ha
    rcases ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> assumption
  · intro h
    refine ⟨h _ (by simp [nineAnchorsList]), h _ (by simp [nineAnchorsList]),
      h _ (by simp [nineAnchorsList]), h _ (by simp [nineAnchorsList]),
      h _ (by simp [nineAnchorsList]), h _ (by simp [nineAnchorsList]),
      h _ (by simp [nineAnchorsList]), h _ (by simp [nineAnchorsList]),
      h _ (by simp [nineAnchorsList])⟩

/-- **Fixed-Anchor Certificate Sufficiency Theorem.**
Suppose `x : GVec` admits a coefficient `0 ≤ A` such that for every rational `η > 0` there is a
finite probe list `Y` and remainder `r < η` satisfying `FixedAnchorBound A r Y x` where every
probe `y ∈ Y` lies within `raySinSq y a < δ` of one of the 9 tomography anchors `a` for any chosen
`δ > 0`. Then every bounded zero-weight anchor-vanishing residual `g` that is pointwise ray-continuous
at the 9 anchors satisfies `g x = 0`. -/
theorem fixedAnchor_sufficiency_of_pointwiseRayContinuous_at_anchors
    {x : GVec} {A : ℚ} (hA : 0 ≤ A)
    (hcert : ∀ (δ η : ℚ), 0 < δ → 0 < η →
      ∃ (Y : List GVec) (r : ℚ), r ≤ η ∧ FixedAnchorBound A r Y x ∧
        ∀ y ∈ Y, y.NonZero ∧ ∃ a ∈ nineAnchorsList, raySinSq y a < δ)
    {g : GVec → ℚ} {B : ℚ} (hB : 0 ≤ B)
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g)
    (hb : IsBoundedOnRaysBy g B)
    (hcont : ∀ a ∈ nineAnchorsList, IsPointwiseRayContinuousAt g a) :
    g x = 0 := by
  by_contra hne
  have hpos : 0 < |g x| := abs_pos.mpr hne
  let ε₁ : ℚ := |g x| / (2 * (A + 1))
  have hA1 : 0 < A + 1 := by linarith
  have hε₁ : 0 < ε₁ := div_pos hpos (by positivity)
  -- Obtain continuity moduli at each of the 9 anchors
  obtain ⟨δ1, hδ1, hc1⟩ := hcont tomo_e1 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ2, hδ2, hc2⟩ := hcont tomo_e2 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ3, hδ3, hc3⟩ := hcont tomo_e3 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ4, hδ4, hc4⟩ := hcont tomo_e12 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ5, hδ5, hc5⟩ := hcont tomo_e13 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ6, hδ6, hc6⟩ := hcont tomo_e23 (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ7, hδ7, hc7⟩ := hcont tomo_e12i (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ8, hδ8, hc8⟩ := hcont tomo_e13i (by simp [nineAnchorsList]) ε₁ hε₁
  obtain ⟨δ9, hδ9, hc9⟩ := hcont tomo_e23i (by simp [nineAnchorsList]) ε₁ hε₁
  let δ := min δ1 (min δ2 (min δ3 (min δ4 (min δ5 (min δ6 (min δ7 (min δ8 δ9)))))))
  have hδ : 0 < δ := by
    refine lt_min hδ1 (lt_min hδ2 (lt_min hδ3 (lt_min hδ4 (lt_min hδ5 (lt_min hδ6 (lt_min hδ7 (lt_min hδ8 hδ9)))))))
  let η : ℚ := |g x| / (4 * (B + 1))
  have hB1 : 0 < B + 1 := by linarith
  have hη : 0 < η := div_pos hpos (by positivity)
  obtain ⟨Y, r, hr_le, hbound, hY⟩ := hcert δ η hδ hη
  have hmax_le : maxAbsOnList g Y ≤ ε₁ := by
    apply maxAbsOnList_le_of_forall hε₁.le
    intro y hy
    obtain ⟨hy_nz, a, ha_mem, hsin⟩ := hY y hy
    have ha0 : g a = 0 := (vanishesOnNineRays_iff_forall_nineAnchorsList g).mp h9 a ha_mem
    have hlt_ε₁ : |g y - g a| < ε₁ := by
      simp only [nineAnchorsList, List.mem_cons, List.not_mem_nil, or_false] at ha_mem
      rcases ha_mem with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · exact hc1 y hy_nz (lt_of_lt_of_le hsin (min_le_left _ _))
      · exact hc2 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (min_le_left _ _)))
      · exact hc3 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _))))
      · exact hc4 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _)))))
      · exact hc5 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _))))))
      · exact hc6 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _)))))))
      · exact hc7 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _))))))))
      · exact hc8 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_left _ _)))))))))
      · exact hc9 y hy_nz (lt_of_lt_of_le hsin (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (le_trans (min_le_right _ _) (min_le_right _ _)))))))))
    rw [ha0, sub_zero] at hlt_ε₁
    exact hlt_ε₁.le
  have hgx_le := hbound g B hB hg h9 hb
  have hA_term : A * maxAbsOnList g Y ≤ |g x| / 2 := by
    calc A * maxAbsOnList g Y ≤ A * ε₁ := mul_le_mul_of_nonneg_left hmax_le hA
      _ ≤ (A + 1) * ε₁ := by nlinarith
      _ = |g x| / 2 := by
        simp only [ε₁]
        field_simp
  have hB_term : B * r ≤ |g x| / 4 := by
    calc B * r ≤ B * η := mul_le_mul_of_nonneg_left hr_le hB
      _ ≤ (B + 1) * η := by nlinarith
      _ = |g x| / 4 := by
        simp only [η]
        field_simp
  linarith

/-- **Exact 2-Frame Meridian Antisymmetry at `witness_111 = (1, 1, 1)`.**
The meridian partner of `witness_111 = (1, 1, 1)` in the plane `(0, 1, -1)⊥` is
`witness_neg211 = (-2, 1, 1)`. -/
def witness_neg211 : GVec := ⟨-2, 1, 1⟩

theorem witness_neg211_nonZero : witness_neg211.NonZero :=
  nonZero_of_x (by simp [witness_neg211])

theorem isFrame_witness111_neg211_bisector :
    IsFrame witness_111 witness_neg211 bisector_23_neg := by
  refine ⟨witness_111_nonZero, witness_neg211_nonZero, nonZero_of_y (by simp [bisector_23_neg]), ?_, ?_, ?_⟩
  · (apply GaussRat.ext <;> simp [GVec.inner, witness_111, witness_neg211, gv]); norm_num
  · apply GaussRat.ext <;> simp [GVec.inner, witness_111, bisector_23_neg, gv]
  · apply GaussRat.ext <;> simp [GVec.inner, witness_neg211, bisector_23_neg]

/-- For **every** zero-weight frame residual `g` vanishing on the 9 tomography anchors (without any
continuity or boundedness assumption), `g witness_111 + g witness_neg211 = 0`. -/
theorem residual_witness111_add_neg211_eq_zero {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g) :
    g witness_111 + g witness_neg211 = 0 := by
  have hbis : g bisector_23_neg = 0 := (vanishes_on_six_bisector_partners hg h9).2.2.2.2.1
  have hfr := hg _ _ _ isFrame_witness111_neg211_bisector
  linarith

/-- Parametric meridian family `meridianApproachE1 t = (1 + t, 1, 1)` approaching `tomo_e1 = (1,0,0)`
as `t → ∞`, paired with `meridianApproachE23 t = (-2, 1 + t, 1 + t)` approaching `tomo_e23 = (0,1,1)`. -/
def meridianApproachE1 (t : ℚ) : GVec := ⟨⟨1 + t, 0⟩, 1, 1⟩

def meridianApproachE23 (t : ℚ) : GVec := ⟨-2, ⟨1 + t, 0⟩, ⟨1 + t, 0⟩⟩

theorem isFrame_meridianApproach {t : ℚ} (ht : 0 ≤ t) :
    IsFrame (meridianApproachE1 t) (meridianApproachE23 t) bisector_23_neg := by
  have h1t : (⟨1 + t, 0⟩ : GaussRat) ≠ 0 := by
    intro h
    have hre := congrArg GaussRat.re h
    simp at hre
    linarith
  refine ⟨Or.inl h1t, nonZero_of_x (by simp [meridianApproachE23]),
    nonZero_of_y (by simp [bisector_23_neg]), ?_, ?_, ?_⟩
  · (apply GaussRat.ext <;> simp [GVec.inner, meridianApproachE1, meridianApproachE23]); ring
  · apply GaussRat.ext <;> simp [GVec.inner, meridianApproachE1, bisector_23_neg]
  · apply GaussRat.ext <;> simp [GVec.inner, meridianApproachE23, bisector_23_neg]

/-- Exact 0-remainder 2-frame identity: for every zero-weight frame function `g` and every `t ≥ 0`,
`g witness_111 + g witness_neg211 = g (meridianApproachE1 t) + g (meridianApproachE23 t)`. -/
theorem meridian_pair_sum_eq_approaching_anchors {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) {t : ℚ} (ht : 0 ≤ t) :
    g witness_111 + g witness_neg211 =
      g (meridianApproachE1 t) + g (meridianApproachE23 t) := by
  have h1 := hg _ _ _ isFrame_witness111_neg211_bisector
  have h2 := hg _ _ _ (isFrame_meridianApproach ht)
  linarith

theorem sp_isBoundedOnRaysBy (p : ℕ) : IsBoundedOnRaysBy (sp p) 1 :=
  fun v _ => sp_abs_le_one p v

/-- **Prime-Valuation Necessary Condition / Obstruction for Fixed-Anchor Certificates.**
If `FixedAnchorBound A r Y x` holds with `0 ≤ A` and `r < 1`, and `p` is any inert prime
(`InertPrimeSpec p`) for which `sp p x ≠ 0`, then `Y` **must** contain at least one probe vector
`y ∈ Y` with `sp p y ≠ 0` (and hence odd `p`-adic norm valuation `vpRat p (normSqVec y) % 2 ≠ 0`). -/
theorem fixedAnchor_prime_valuation_obstruction
    {A r : ℚ} {Y : List GVec} {x : GVec}
    (_hA : 0 ≤ A) (hr : r < 1) (hcert : FixedAnchorBound A r Y x)
    {p : ℕ} (hP : InertPrimeSpec p) (hx : sp p x ≠ 0) :
    ∃ y ∈ Y, sp p y ≠ 0 ∧ vpRat p (normSqVec y) % 2 ≠ 0 := by
  have hsp_abs_one : |sp p x| = 1 := by
    rcases sp_values p x with h0 | h1 | hn1
    · exact absurd h0 hx
    · rw [h1, abs_one]
    · rw [hn1, abs_neg, abs_one]
  by_contra hnone
  have hall_zero : ∀ y ∈ Y, sp p y = 0 := by
    intro y hy
    by_contra hy_ne
    apply hnone
    refine ⟨y, hy, hy_ne, ?_⟩
    intro heven
    exact hy_ne (sp_eq_zero_of_even heven)
  have hmax0 : maxAbsOnList (sp p) Y = 0 := maxAbsOnList_eq_zero_of_forall_zero hall_zero
  have hbound := hcert (sp p) 1 zero_le_one
    (sp_isZeroWeightFrameFunction hP)
    (sp_vanishes_on_nine_rays hP.ge_three)
    (sp_isBoundedOnRaysBy p)
  rw [hsp_abs_one, hmax0, mul_zero, zero_add, one_mul] at hbound
  linarith

/-- Corollary: if every probe vector `y ∈ Y` has even `p`-adic squared-norm valuation for an inert
prime `p` with `sp p x ≠ 0`, then any `FixedAnchorBound A r Y x` (`0 ≤ A`) has remainder `1 ≤ r`. -/
theorem fixedAnchor_remainder_ge_one_of_even_vpRat
    {A r : ℚ} {Y : List GVec} {x : GVec}
    (hA : 0 ≤ A) (hcert : FixedAnchorBound A r Y x)
    {p : ℕ} (hP : InertPrimeSpec p) (hx : sp p x ≠ 0)
    (heven : ∀ y ∈ Y, vpRat p (normSqVec y) % 2 = 0) :
    1 ≤ r := by
  by_contra hlt
  have hr : r < 1 := not_le.mp hlt
  obtain ⟨y, hy, _, hodd⟩ := fixedAnchor_prime_valuation_obstruction hA hr hcert hP hx
  exact hodd (heven y hy)

/-- **Coordinate-Refined 3-Adic Residuals (`s3_leadX` and `s3_leadAll`).**
Because `isLead3Coord u.x u`, `isLead3Coord u.y u`, and `isLead3Coord u.z u` are each invariant
across orthogonal pairs in `S_{odd, 3}` (`lead3Coord_x_ortho_iff`, `lead3Coord_y_ortho_iff`,
`lead3Coord_z_ortho_iff`), restricting `s3` to rays where `x` is 3-leading (`s3_leadX`) or where
all three coordinates `x, y, z` are simultaneously 3-leading (`s3_leadAll`) produces valid
zero-weight frame residuals! -/
def isLead3All (u : GVec) : Prop :=
  isLead3Coord u.x u ∧ isLead3Coord u.y u ∧ isLead3Coord u.z u

instance instDecidableIsLead3All (u : GVec) : Decidable (isLead3All u) :=
  inferInstanceAs (Decidable (isLead3Coord u.x u ∧ isLead3Coord u.y u ∧ isLead3Coord u.z u))

def s3_leadX (u : GVec) : ℚ :=
  if v3Rat (normSqVec u) % 2 = 0 then 0
  else if isLead3Coord u.x u then coordSign3 u.x u
  else 0

def s3_leadAll (u : GVec) : ℚ :=
  if v3Rat (normSqVec u) % 2 = 0 then 0
  else if isLead3All u then coordSign3 u.x u
  else 0

theorem lead3Coord_z_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    isLead3Coord u.z u ↔ isLead3Coord v.z v :=
  ⟨fun h => (lead3Coord_z_ortho_imp huv hu_odd hv_odd h).1,
   fun h => (lead3Coord_z_ortho_imp (inner_eq_zero_symm huv) hv_odd hu_odd h).1⟩

theorem isLead3All_ortho_iff {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    isLead3All u ↔ isLead3All v := by
  unfold isLead3All
  rw [lead3Coord_x_ortho_iff huv hu_odd hv_odd,
      lead3Coord_y_ortho_iff huv hu_odd hv_odd,
      lead3Coord_z_ortho_iff huv hu_odd hv_odd]

theorem s3_leadX_pair_cancel {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    s3_leadX u + s3_leadX v = 0 := by
  simp only [s3_leadX, hu_odd, hv_odd, ↓reduceIte]
  by_cases hx : isLead3Coord u.x u
  · obtain ⟨hvx, hsum⟩ := lead3Coord_x_ortho_imp huv hu_odd hv_odd hx
    simp only [hx, hvx, ↓reduceIte]
    exact hsum
  · have hvx : ¬ isLead3Coord v.x v :=
      fun h => hx ((lead3Coord_x_ortho_iff huv hu_odd hv_odd).mpr h)
    simp only [hx, hvx, ↓reduceIte, add_zero]

theorem s3_leadAll_pair_cancel {u v : GVec}
    (huv : GVec.inner u v = 0)
    (hu_odd : v3Rat (normSqVec u) % 2 ≠ 0)
    (hv_odd : v3Rat (normSqVec v) % 2 ≠ 0) :
    s3_leadAll u + s3_leadAll v = 0 := by
  simp only [s3_leadAll, hu_odd, hv_odd, ↓reduceIte]
  by_cases hall : isLead3All u
  · have hv_all : isLead3All v := (isLead3All_ortho_iff huv hu_odd hv_odd).mp hall
    obtain ⟨_, hsum⟩ := lead3Coord_x_ortho_imp huv hu_odd hv_odd hall.1
    simp only [hall, hv_all, ↓reduceIte]
    exact hsum
  · have hv_all : ¬ isLead3All v :=
      fun h => hall ((isLead3All_ortho_iff huv hu_odd hv_odd).mpr h)
    simp only [hall, hv_all, ↓reduceIte, add_zero]

theorem s3_leadX_isZeroWeightFrameFunction : IsZeroWeightFrameFunction s3_leadX := by
  intro u v w hf
  have heven := frame_v3Rat_sum_even hf
  obtain ⟨_, _, _, huv, huw, hvw⟩ := hf
  by_cases hu : v3Rat (normSqVec u) % 2 = 0
  · by_cases hv : v3Rat (normSqVec v) % 2 = 0
    · have hw : v3Rat (normSqVec w) % 2 = 0 := by omega
      simp [s3_leadX, hu, hv, hw]
    · have hw : v3Rat (normSqVec w) % 2 ≠ 0 := by omega
      have hvw_sum := s3_leadX_pair_cancel hvw hv hw
      have hu_zero : s3_leadX u = 0 := by simp [s3_leadX, hu]
      linarith
  · by_cases hv : v3Rat (normSqVec v) % 2 = 0
    · have hw : v3Rat (normSqVec w) % 2 ≠ 0 := by omega
      have huw_sum := s3_leadX_pair_cancel huw hu hw
      have hv_zero : s3_leadX v = 0 := by simp [s3_leadX, hv]
      linarith
    · have hw : v3Rat (normSqVec w) % 2 = 0 := by omega
      have huv_sum := s3_leadX_pair_cancel huv hu hv
      have hw_zero : s3_leadX w = 0 := by simp [s3_leadX, hw]
      linarith

theorem s3_leadAll_isZeroWeightFrameFunction : IsZeroWeightFrameFunction s3_leadAll := by
  intro u v w hf
  have heven := frame_v3Rat_sum_even hf
  obtain ⟨_, _, _, huv, huw, hvw⟩ := hf
  by_cases hu : v3Rat (normSqVec u) % 2 = 0
  · by_cases hv : v3Rat (normSqVec v) % 2 = 0
    · have hw : v3Rat (normSqVec w) % 2 = 0 := by omega
      simp [s3_leadAll, hu, hv, hw]
    · have hw : v3Rat (normSqVec w) % 2 ≠ 0 := by omega
      have hvw_sum := s3_leadAll_pair_cancel hvw hv hw
      have hu_zero : s3_leadAll u = 0 := by simp [s3_leadAll, hu]
      linarith
  · by_cases hv : v3Rat (normSqVec v) % 2 = 0
    · have hw : v3Rat (normSqVec w) % 2 ≠ 0 := by omega
      have huw_sum := s3_leadAll_pair_cancel huw hu hw
      have hv_zero : s3_leadAll v = 0 := by simp [s3_leadAll, hv]
      linarith
    · have hw : v3Rat (normSqVec w) % 2 = 0 := by omega
      have huv_sum := s3_leadAll_pair_cancel huv hu hv
      have hw_zero : s3_leadAll w = 0 := by simp [s3_leadAll, hw]
      linarith

/-- `s3_leadAll` vanishes on any vector where `¬ isLead3All u`. -/
theorem s3_leadAll_eq_zero_of_not_isLead3All {u : GVec} (h : ¬ isLead3All u) :
    s3_leadAll u = 0 := by
  simp [s3_leadAll, h]

/-- `s3_leadAll` vanishes identically on the union of the three coordinate planes
`u.x = 0 ∨ u.y = 0 ∨ u.z = 0`. -/
theorem s3_leadAll_eq_zero_of_coord_zero {u : GVec}
    (hcoord : u.x = 0 ∨ u.y = 0 ∨ u.z = 0) : s3_leadAll u = 0 := by
  apply s3_leadAll_eq_zero_of_not_isLead3All
  rintro ⟨⟨hx, _⟩, ⟨hy, _⟩, ⟨hz, _⟩⟩
  rcases hcoord with h0 | h0 | h0
  · rw [h0] at hx; simp [GaussRat.normSq] at hx
  · rw [h0] at hy; simp [GaussRat.normSq] at hy
  · rw [h0] at hz; simp [GaussRat.normSq] at hz

theorem s3_leadAll_vanishes_on_nine_rays : VanishesOnNineRays s3_leadAll := by
  refine ⟨s3_leadAll_eq_zero_of_coord_zero (Or.inr (Or.inl (by ext <;> simp [tomo_e1, gv]))),
          s3_leadAll_eq_zero_of_coord_zero (Or.inl (by ext <;> simp [tomo_e2, gv])),
          s3_leadAll_eq_zero_of_coord_zero (Or.inl (by ext <;> simp [tomo_e3, gv])),
          s3_leadAll_eq_zero_of_coord_zero (Or.inr (Or.inr (by ext <;> simp [tomo_e12, gv]))),
          s3_leadAll_eq_zero_of_coord_zero (Or.inr (Or.inl (by ext <;> simp [tomo_e13, gv]))),
          s3_leadAll_eq_zero_of_coord_zero (Or.inl (by ext <;> simp [tomo_e23, gv])),
          s3_leadAll_eq_zero_of_coord_zero (Or.inr (Or.inr (by ext <;> simp [tomo_e12i, gv]))),
          s3_leadAll_eq_zero_of_coord_zero (Or.inr (Or.inl (by ext <;> simp [tomo_e13i, gv]))),
          s3_leadAll_eq_zero_of_coord_zero (Or.inl (by ext <;> simp [tomo_e23i, gv]))⟩

theorem s3_leadAll_values (u : GVec) :
    s3_leadAll u = 0 ∨ s3_leadAll u = 1 ∨ s3_leadAll u = -1 := by
  unfold s3_leadAll
  by_cases heven : v3Rat (normSqVec u) % 2 = 0
  · left; simp [heven]
  · simp only [heven, ↓reduceIte]
    by_cases hall : isLead3All u
    · simp only [hall, ↓reduceIte]
      have hnu : 0 < normSqVec u := pos_of_v3Rat_mod_two_ne_zero heven
      right; exact coordSign3_values hall.1.1 hnu
    · left; simp [hall]

theorem s3_leadAll_isBoundedOnRaysBy : IsBoundedOnRaysBy s3_leadAll 1 := by
  intro u _
  rcases s3_leadAll_values u with h0 | h1 | hn1
  · rw [h0, abs_zero]; exact zero_le_one
  · rw [h1, abs_one]
  · rw [hn1, abs_neg, abs_one]

theorem s3_leadAll_isBoundedOnRays : IsBoundedOnRays s3_leadAll :=
  isBoundedOnRays_of_isBoundedOnRaysBy zero_le_one s3_leadAll_isBoundedOnRaysBy

theorem s3_leadAll_eq_s3_of_isLead3All {u : GVec} (h : isLead3All u) :
    s3_leadAll u = s3 u := by
  simp [s3_leadAll, s3, h, h.1]

theorem isLead3All_witness_111 : isLead3All witness_111 := by
  have hnorm : normSqVec witness_111 = (3 : ℕ) := by
    simp [normSqVec, GaussRat.normSq, witness_111, gv]; norm_num
  have hvn : v3Rat (normSqVec witness_111) = 1 := by
    rw [hnorm, v3Rat_natCast (by decide : 0 < 3)]; rfl
  have hx : witness_111.x.normSq = (1 : ℕ) := by simp [GaussRat.normSq, witness_111, gv]
  have hy : witness_111.y.normSq = (1 : ℕ) := by simp [GaussRat.normSq, witness_111, gv]
  have hz : witness_111.z.normSq = (1 : ℕ) := by simp [GaussRat.normSq, witness_111, gv]
  have hv1 : v3Rat ((1 : ℕ) : ℚ) = 0 := by
    rw [v3Rat_natCast (by decide : 0 < 1)]; rfl
  refine ⟨⟨by rw [hx]; norm_num, by rw [hx, hv1, hvn]; decide⟩,
          ⟨by rw [hy]; norm_num, by rw [hy, hv1, hvn]; decide⟩,
          ⟨by rw [hz]; norm_num, by rw [hz, hv1, hvn]; decide⟩⟩

theorem s3_leadAll_witness_111 : s3_leadAll witness_111 = 1 := by
  rw [s3_leadAll_eq_s3_of_isLead3All isLead3All_witness_111, s3_witness_111]

/-- **Coordinate-Plane / Non-All-Leading Certificate Obstruction.**
Any `FixedAnchorBound A r Y witness_111` (`0 ≤ A`) whose probe vectors `y ∈ Y` satisfy
`¬ isLead3All y` (which includes all vectors in the three coordinate planes `y.x = 0 ∨ y.y = 0 ∨ y.z = 0`
and all `perturbPosRay k` / `perturbNegRay k`) must have remainder `1 ≤ r`. -/
theorem fixedAnchor_obstruction_of_not_isLead3All
    {A r : ℚ} {Y : List GVec}
    (_hA : 0 ≤ A) (hcert : FixedAnchorBound A r Y witness_111)
    (hY : ∀ y ∈ Y, ¬ isLead3All y) :
    1 ≤ r := by
  have hmax0 : maxAbsOnList s3_leadAll Y = 0 := by
    apply maxAbsOnList_eq_zero_of_forall_zero
    intro y hy
    exact s3_leadAll_eq_zero_of_not_isLead3All (hY y hy)
  have hbound := hcert s3_leadAll 1 zero_le_one
    s3_leadAll_isZeroWeightFrameFunction
    s3_leadAll_vanishes_on_nine_rays
    s3_leadAll_isBoundedOnRaysBy
  rw [s3_leadAll_witness_111, abs_one, hmax0, mul_zero, zero_add, one_mul] at hbound
  exact hbound

/-- **Chinese Remainder Archimedean / 3-Adic Collision Sequence.**
The sequence `crtApproachE1 m = (1 + 9*(m+1), 1, 1)` is congruent to `witness_111 = (1, 1, 1)`
modulo `9` (hence maintains `isLead3All (crtApproachE1 m)` and `s3_leadAll (crtApproachE1 m) = 1`
for every `m : ℕ`) while converging in projective ray distance `raySinSq` to `tomo_e1 = (1, 0, 0)`
as `m → ∞`. -/
def crtApproachE1 (m : ℕ) : GVec :=
  ⟨⟨(1 + 9 * (m + 1) : ℕ), 0⟩, 1, 1⟩

theorem crtApproachE1_nonZero (m : ℕ) : (crtApproachE1 m).NonZero :=
  nonZero_of_x (by simp [crtApproachE1]; positivity)

theorem crtApproachE1_s3_leadAll_eq_one (m : ℕ) : s3_leadAll (crtApproachE1 m) = 1 := by
  let N : ℕ := 1 + 9 * (m + 1)
  let q : ℕ := 1 + 6 * (m + 1) + 27 * (m + 1) ^ 2
  have hN2_pos : 0 < N ^ 2 := by dsimp [N]; positivity
  have hn_pos : 0 < N ^ 2 + 2 := by positivity
  have hN2_mod : N ^ 2 % 3 = 1 := by
    have : N ^ 2 = 1 + 3 * (6 * (m + 1) + 27 * (m + 1) ^ 2) := by dsimp [N]; ring
    omega
  have hq_mod : q % 3 = 1 := by
    have : q = 1 + 3 * (2 * (m + 1) + 9 * (m + 1) ^ 2) := by dsimp [q]; ring
    omega
  obtain ⟨hv_nx, hp_nx⟩ : v3Nat (N ^ 2) = 0 ∧ p3PartNat (N ^ 2) = N ^ 2 := by
    apply v3Nat_p3PartNat_eq_of_pow_mul (a := 0) (m := N ^ 2)
    · omega
    · ring
  obtain ⟨hv_n, hp_n⟩ : v3Nat (N ^ 2 + 2) = 1 ∧ p3PartNat (N ^ 2 + 2) = q := by
    apply v3Nat_p3PartNat_eq_of_pow_mul (a := 1) (m := q)
    · omega
    · dsimp [N, q]; ring
  have hnorm : normSqVec (crtApproachE1 m) = ((N ^ 2 + 2 : ℕ) : ℚ) := by
    simp [normSqVec, GaussRat.normSq, crtApproachE1, N]
    ring
  have hx : (crtApproachE1 m).x.normSq = ((N ^ 2 : ℕ) : ℚ) := by
    simp [GaussRat.normSq, crtApproachE1, N]
  have hy : (crtApproachE1 m).y.normSq = ((1 : ℕ) : ℚ) := by
    simp [GaussRat.normSq, crtApproachE1]
  have hz : (crtApproachE1 m).z.normSq = ((1 : ℕ) : ℚ) := by
    simp [GaussRat.normSq, crtApproachE1]
  have hvn : v3Rat (normSqVec (crtApproachE1 m)) = 1 := by
    rw [hnorm, v3Rat_natCast hn_pos, hv_n]; rfl
  have hvx : v3Rat (crtApproachE1 m).x.normSq = 0 := by
    rw [hx, v3Rat_natCast hN2_pos, hv_nx]; rfl
  have hv1 : v3Rat ((1 : ℕ) : ℚ) = 0 := by
    rw [v3Rat_natCast (by decide : 0 < 1)]; rfl
  have hall : isLead3All (crtApproachE1 m) := by
    refine ⟨⟨by rw [hx]; exact_mod_cast hN2_pos, by rw [hvx, hvn]; decide⟩,
            ⟨by rw [hy]; norm_num, by rw [hy, hv1, hvn]; decide⟩,
            ⟨by rw [hz]; norm_num, by rw [hz, hv1, hvn]; decide⟩⟩
  rw [s3_leadAll_eq_s3_of_isLead3All hall]
  rw [s3_eq_of_lead3Coord_x (n := N ^ 2 + 2) (nx := N ^ 2) hn_pos hN2_pos hnorm hx
    (by rw [hv_n]; decide) (by rw [hv_nx, hv_n]; decide)]
  rw [hp_nx, hp_n, hN2_mod, hq_mod]
  norm_num

theorem crtApproachE1_raySinSq_tomo_e1_le (m : ℕ) :
    raySinSq (crtApproachE1 m) tomo_e1 ≤ 2 / ((1 + 9 * (m + 1) : ℕ) : ℚ) ^ 2 := by
  let N : ℕ := 1 + 9 * (m + 1)
  have hN_pos : (0 : ℚ) < (N : ℚ) := by exact_mod_cast (show 0 < N by omega)
  have hnorm_pos : (0 : ℚ) < (N : ℚ) ^ 2 + 2 := by positivity
  have hsin_eq : raySinSq (crtApproachE1 m) tomo_e1 = 2 / ((N : ℚ) ^ 2 + 2) := by
    simp only [raySinSq, crtApproachE1, tomo_e1, gv, GVec.inner, normSqVec, GaussRat.normSq]
    dsimp [N]
    field_simp
    ring
  rw [hsin_eq]
  exact div_le_div_of_nonneg_left (by norm_num) (pow_pos hN_pos 2) (by linarith)

/-! ### Section 6: Explicit Proof-Obligation Separations -/

/-- **Proof Obligation 1 (`moving_rational_near_maximizer_no_rational_maximizer`).**
For the rational objective `irrationalSupObjective q = - (3 * q ^ 2 - 1) ^ 2`, rational
near-maximizers approach the supremum `0` (as `q → 1 / √3`), yet **no** rational `q : ℚ` achieves
`irrationalSupObjective q = 0` because `3 * q ^ 2 ≠ 1` for every `q : ℚ`. -/
def irrationalSupObjective (q : ℚ) : ℚ := - (3 * q ^ 2 - 1) ^ 2

theorem three_mul_sq_ne_sq {a b : ℚ} (hb : 0 < b) : 3 * a ^ 2 ≠ b ^ 2 := by
  by_cases ha : a = 0
  · subst ha
    have : (0 : ℚ) < b ^ 2 := pow_pos hb 2
    linarith
  · have ha2 : 0 < a ^ 2 := sq_pos_of_ne_zero ha
    have h3 : (0 : ℚ) < 3 := by norm_num
    intro heq
    have heven_a : v3Rat (a ^ 2) % 2 = 0 := by
      have hns : (⟨a, 0⟩ : GaussRat).normSq = a ^ 2 := by simp [GaussRat.normSq]
      rw [← hns]
      exact v3Rat_normSq_even ⟨a, 0⟩
    have heven_b : v3Rat (b ^ 2) % 2 = 0 := by
      have hns : (⟨b, 0⟩ : GaussRat).normSq = b ^ 2 := by simp [GaussRat.normSq]
      rw [← hns]
      exact v3Rat_normSq_even ⟨b, 0⟩
    have hv3 : v3Rat (3 : ℚ) = 1 := by
      have h3v := v3Rat_natCast (n := 3) (by decide)
      have hv3_nat : v3Nat 3 = 1 := rfl
      simpa [hv3_nat] using h3v
    have hmul : v3Rat (3 * a ^ 2) = 1 + v3Rat (a ^ 2) := by
      rw [v3Rat_mul h3 ha2, hv3]
    have h_eq_v : v3Rat (3 * a ^ 2) = v3Rat (b ^ 2) := congrArg v3Rat heq
    omega

theorem moving_rational_near_maximizer_no_rational_maximizer :
    (∀ q : ℚ, irrationalSupObjective q < 0) ∧
    irrationalSupObjective (15 / 26) > - (1 / 1000 : ℚ) := by
  refine ⟨fun q => ?_, by norm_num [irrationalSupObjective]⟩
  unfold irrationalSupObjective
  have hne : 3 * q ^ 2 - 1 ≠ 0 := by
    intro h0
    have heq : 3 * q ^ 2 = 1 ^ 2 := by linarith
    exact three_mul_sq_ne_sq one_pos heq
  have hpos : 0 < (3 * q ^ 2 - 1) ^ 2 := sq_pos_of_ne_zero hne
  linarith

/-- **Proof Obligation 2 (`chain_step_error_accumulates` & `linearDriftChain_attains_bound`).**
An `ε` loss per step along a chain of length `L` accumulates to `L * ε`, and this `L * ε` growth is
attained by `linearDriftChain ε k = k * ε`. -/
theorem chain_step_error_accumulates (c : ℕ → ℚ) {ε : ℚ}
    (hstep : ∀ k : ℕ, |c (k + 1) - c k| ≤ ε) (L : ℕ) :
    |c L - c 0| ≤ (L : ℚ) * ε := by
  induction L with
  | zero => simp
  | succ k ih =>
    have htri : |c (k + 1) - c 0| ≤ |c (k + 1) - c k| + |c k - c 0| := by
      have e : c (k + 1) - c 0 = (c (k + 1) - c k) + (c k - c 0) := by ring
      rw [e]
      exact abs_add_le _ _
    have hk := hstep k
    push_cast
    linarith

def linearDriftChain (ε : ℚ) (k : ℕ) : ℚ := (k : ℚ) * ε

theorem linearDriftChain_attains_bound {ε : ℚ} (hε : 0 ≤ ε) (L : ℕ) :
    (∀ k : ℕ, |linearDriftChain ε (k + 1) - linearDriftChain ε k| ≤ ε) ∧
    |linearDriftChain ε L - linearDriftChain ε 0| = (L : ℚ) * ε := by
  refine ⟨fun k => ?_, ?_⟩
  · unfold linearDriftChain
    push_cast
    have e : ((k : ℚ) + 1) * ε - (k : ℚ) * ε = ε := by ring
    rw [e, abs_of_nonneg hε]
  · unfold linearDriftChain
    simp [abs_of_nonneg (mul_nonneg (Nat.cast_nonneg L) hε)]

/-- **Proof Obligation 4 (`dedekindRayCut`): Scale-Invariant `{0, 1}` Ray Cut Jumping Across an
Irrational Cone.**
Define `dedekindRayCut u := if (normSqVec u) ^ 2 < 3 * (u.y.normSq) ^ 2 then 1 else 0`.
Because `3 * a ^ 2 ≠ b ^ 2` for every `b > 0`, `3 * (u.y.normSq) ^ 2 ≠ (normSqVec u) ^ 2` for every
nonzero `u ∈ ℚ(i)³`. Nevertheless, across the irrational cone `3 * |u.y|⁴ = ‖u‖⁴`, `dedekindRayCut`
jumps by `1` between arbitrarily close rational rays. -/
def dedekindRayCut (u : GVec) : ℚ :=
  if (normSqVec u) ^ 2 < 3 * (u.y.normSq) ^ 2 then 1 else 0

theorem dedekindRayCut_isScaleInvariantOnRays : IsScaleInvariantOnRays dedekindRayCut := by
  intro u _ c hc
  unfold dedekindRayCut
  have hns_c : 0 < c.normSq := by
    rcases (GaussRat.normSq_nonneg c).lt_or_eq with h | h
    · exact h
    · exact absurd ((GaussRat.normSq_eq_zero_iff c).mp h.symm) hc
  have hns_c2 : 0 < (c.normSq) ^ 2 := pow_pos hns_c 2
  have huy : (GVec.smul c u).y.normSq = c.normSq * u.y.normSq := by
    simp [GVec.smul, GaussRat.normSq_mul]
  have hu : normSqVec (GVec.smul c u) = c.normSq * normSqVec u := normSqVec_smul c u
  rw [huy, hu]
  have hiff : (c.normSq * normSqVec u) ^ 2 < 3 * (c.normSq * u.y.normSq) ^ 2 ↔
      (normSqVec u) ^ 2 < 3 * (u.y.normSq) ^ 2 := by
    have e1 : (c.normSq * normSqVec u) ^ 2 = c.normSq ^ 2 * (normSqVec u) ^ 2 := by ring
    have e2 : 3 * (c.normSq * u.y.normSq) ^ 2 = c.normSq ^ 2 * (3 * (u.y.normSq) ^ 2) := by ring
    rw [e1, e2]
    exact ⟨fun h => by nlinarith, fun h => mul_lt_mul_of_pos_left h hns_c2⟩
  by_cases h : (normSqVec u) ^ 2 < 3 * (u.y.normSq) ^ 2
  · have h' : (c.normSq * normSqVec u) ^ 2 < 3 * (c.normSq * u.y.normSq) ^ 2 := hiff.mpr h
    simp [h, h']
  · have h' : ¬ (c.normSq * normSqVec u) ^ 2 < 3 * (c.normSq * u.y.normSq) ^ 2 := mt hiff.mp h
    simp [h, h']

theorem dedekindRayCut_gap_ne_zero {u : GVec} (hu : u.NonZero) :
    3 * (u.y.normSq) ^ 2 ≠ (normSqVec u) ^ 2 :=
  three_mul_sq_ne_sq (normSqVec_pos_of_nonZero hu)

/-- Explicit rational ray pair `u_hi = (85, 100, 0)` and `u_lo = (86, 100, 0)` straddling the
irrational cone `3 * |u.y|⁴ = ‖u‖⁴` within `raySinSq < 1 / 10000` where `dedekindRayCut` jumps by `1`. -/
def pellHiRay : GVec := ⟨85, 100, 0⟩
def pellLoRay : GVec := ⟨86, 100, 0⟩

theorem dedekindRayCut_jump_on_pell_pair :
    pellHiRay.NonZero ∧ pellLoRay.NonZero ∧
    raySinSq pellHiRay pellLoRay < 1 / 10000 ∧
    |dedekindRayCut pellHiRay - dedekindRayCut pellLoRay| = 1 := by
  refine ⟨nonZero_of_x (by simp [pellHiRay]), nonZero_of_x (by simp [pellLoRay]), ?_, ?_⟩
  · norm_num [pellHiRay, pellLoRay, raySinSq, normSqVec, GVec.inner, GaussRat.normSq]
  · norm_num [pellHiRay, pellLoRay, dedekindRayCut, normSqVec, GaussRat.normSq]

/-! ### Section 7: Track A (Rational Piron–Soler Chain & Polar–Equatorial Transfer) and Track B (Irrational-Locus / Dedekind-Cut Frame Stress Tests) on `ℚ(i)³` (`TFQ-1057`) -/

/-! #### 7A. Track A: General-Value Rational Piron–Soler Chain & Polar–Equatorial Transfer -/

/-- **General Rational Piron Orthogonal Subadditivity (`rational_piron_subadditivity`)**:
for any nonnegative frame function `f` on `ℚ(i)³` and any two nonzero orthogonal vectors
`u, v ∈ ℚ(i)³` (`GVec.inner u v = 0`), completing `(u, v)` to the orthogonal 3-frame
`(u, v, hermCross u v)` forces `0 ≤ f u + f v ≤ 1`. -/
theorem rational_piron_subadditivity {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) (huv : GVec.inner u v = 0) :
    0 ≤ f u + f v ∧ f u + f v ≤ 1 := by
  have hfr := isFrame_hermCross hu hv huv
  have hsum := hf.1 u v (hermCross u v) hfr
  have hfu := hf.2 u hu
  have hfv := hf.2 v hv
  have hfw := hf.2 (hermCross u v) hfr.2.2.1
  exact ⟨by linarith, by linarith⟩

/-- **Orthogonal Pole-Deficiency Bound (`nonneg_frameFunction_ortho_le_one_sub`)**:
for any nonnegative frame function `f` on `ℚ(i)³` and any nonzero `v` orthogonal to a nonzero
pole `u`, `0 ≤ f v ≤ 1 - f u`. -/
theorem nonneg_frameFunction_ortho_le_one_sub {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) (huv : GVec.inner u v = 0) :
    0 ≤ f v ∧ f v ≤ 1 - f u := by
  have hsub := rational_piron_subadditivity hf hu hv huv
  exact ⟨hf.2 v hv, by linarith⟩

/-- Every nonzero equatorial vector `y ∈ e₁⊥` (`y.x = 0`) and its canonical equatorial partner
`eqOrtho y` complete `tomo_e1` to an exact orthogonal frame `(tomo_e1, y, eqOrtho y)` in `ℚ(i)³`. -/
theorem isFrame_tomo_e1_eqOrtho {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) :
    IsFrame tomo_e1 y (eqOrtho y) := by
  have hy_pos := normSqVec_pos_of_nonZero hy
  have heq_pos : 0 < normSqVec (eqOrtho y) := by
    rw [normSqVec_eqOrtho_of_x_zero hyx]
    exact hy_pos
  exact ⟨tomo_e1_nonZero, hy, nonZero_of_normSqVec_pos heq_pos,
    inner_tomo_e1_of_x_zero hyx,
    inner_tomo_e1_of_x_zero rfl,
    inner_eqOrtho_self y⟩

/-- **Equatorial Pole-Deficiency Decomposition (`equatorial_pair_sum_eq_one_sub_pole`)**:
for any nonnegative frame function `f` on `ℚ(i)³` and any nonzero `y ∈ e₁⊥`,
`f y + f (eqOrtho y) = 1 - f tomo_e1`, so both `f y ≤ 1 - f tomo_e1` and
`f (eqOrtho y) ≤ 1 - f tomo_e1`. -/
theorem equatorial_pair_sum_eq_one_sub_pole {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) :
    f y + f (eqOrtho y) = 1 - f tomo_e1 ∧
    f y ≤ 1 - f tomo_e1 ∧
    f (eqOrtho y) ≤ 1 - f tomo_e1 := by
  have hfr := isFrame_tomo_e1_eqOrtho hyx hy
  have hsum := hf.1 tomo_e1 y (eqOrtho y) hfr
  have hfy := hf.2 y hy
  have hfeq := hf.2 (eqOrtho y) hfr.2.2.1
  exact ⟨by linarith, by linarith, by linarith⟩

/-- **General Two-Frame Meridian–Kelvin Polar–Equatorial Bridge (`meridian_kelvin_universal_bridge`)**:
for **every** frame function `f` on `ℚ(i)³` (without assuming `f tomo_e1 = 1` or nonnegativity)
and every nonzero `y ∈ e₁⊥`, subtracting the equatorial frame `(tomo_e1, y, eqOrtho y)` from the
meridian frame `(e₁ + y, eqOrtho y, meridianOrtho y)` eliminates `f (eqOrtho y)` and yields:
1. `f (e₁ + y) + f (meridianOrtho y) = f tomo_e1 + f y`,
2. `f (e₁ + y) + f (e₁ + kelvinEq y) = f tomo_e1 + f y`,
3. `f (e₁ + y) - f tomo_e1 = f y - f (meridianOrtho y)` (polar variation equals equatorial variation). -/
theorem meridian_kelvin_universal_bridge {f : GVec → ℚ} (hf : IsFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) :
    f (GVec.add tomo_e1 y) + f (meridianOrtho y) = f tomo_e1 + f y ∧
    f (GVec.add tomo_e1 y) + f (GVec.add tomo_e1 (kelvinEq y)) = f tomo_e1 + f y ∧
    f (GVec.add tomo_e1 y) - f tomo_e1 = f y - f (meridianOrtho y) := by
  have hfr_eq := isFrame_tomo_e1_eqOrtho hyx hy
  have hsum_eq := hf tomo_e1 y (eqOrtho y) hfr_eq
  have hfr_mer := isFrame_piron_base hyx hy one_ne_zero
  have hsmul1 : GVec.smul 1 (eqOrtho y) = eqOrtho y := by
    ext <;> simp [GVec.smul]
  have hsum_mer := hf (GVec.add tomo_e1 y) (GVec.smul 1 (eqOrtho y)) (meridianOrtho y) hfr_mer
  rw [hsmul1] at hsum_mer
  have hm_nz : (meridianOrtho y).NonZero := hfr_mer.2.2.1
  have hy_pos := normSqVec_pos_of_nonZero hy
  have hl_ne : (⟨-(1 / normSqVec y), 0⟩ : GaussRat) ≠ 0 := by
    intro h
    have hre := congrArg GaussRat.re h
    dsimp at hre
    have hpos : 0 < 1 / normSqVec y := div_pos one_pos hy_pos
    linarith
  have hsmul_kelvin := GaussianTomography.frameFunction_smul hf hm_nz hl_ne
  rw [smul_meridianOrtho_eq_add_kelvinEq hy] at hsmul_kelvin
  exact ⟨by linarith, by linarith, by linarith⟩

/-- **Zero-Weight Meridian–Kelvin Polar–Equatorial Bridge (`meridian_kelvin_zeroWeight_bridge`)**:
for every zero-weight frame residual `g` on `ℚ(i)³` and every nonzero `y ∈ e₁⊥`,
`g (e₁ + y) + g (meridianOrtho y) = g tomo_e1 + g y` and
`g (e₁ + y) - g tomo_e1 = g y - g (meridianOrtho y)`. -/
theorem meridian_kelvin_zeroWeight_bridge {g : GVec → ℚ} (hg : IsZeroWeightFrameFunction g)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) :
    g (GVec.add tomo_e1 y) + g (meridianOrtho y) = g tomo_e1 + g y ∧
    g (GVec.add tomo_e1 y) - g tomo_e1 = g y - g (meridianOrtho y) := by
  have hfr_eq := isFrame_tomo_e1_eqOrtho hyx hy
  have hsum_eq := hg tomo_e1 y (eqOrtho y) hfr_eq
  have hfr_mer := isFrame_piron_base hyx hy one_ne_zero
  have hsmul1 : GVec.smul 1 (eqOrtho y) = eqOrtho y := by
    ext <;> simp [GVec.smul]
  have hsum_mer := hg (GVec.add tomo_e1 y) (GVec.smul 1 (eqOrtho y)) (meridianOrtho y) hfr_mer
  rw [hsmul1] at hsum_mer
  exact ⟨by linarith, by linarith⟩

/-- **Exact Polar–Equatorial Projective Ray-Distance Duality (`meridianOrtho_raySinSq_eq`)**:
for every nonzero `y ∈ e₁⊥`, the projective ray distance `raySinSq (e₁ + y) tomo_e1` near the pole
`tomo_e1` and the projective ray distance `raySinSq (meridianOrtho y) y` near the equatorial ray `y`
are both identically equal to `normSqVec y / (1 + normSqVec y)`. -/
theorem meridianOrtho_raySinSq_eq {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) :
    raySinSq (GVec.add tomo_e1 y) tomo_e1 = normSqVec y / (1 + normSqVec y) ∧
    raySinSq (meridianOrtho y) y = normSqVec y / (1 + normSqVec y) := by
  have hy_pos := normSqVec_pos_of_nonZero hy
  have hy_ne : normSqVec y ≠ 0 := ne_of_gt hy_pos
  have h1y_pos : 0 < 1 + normSqVec y := by linarith
  have h1y_ne : 1 + normSqVec y ≠ 0 := ne_of_gt h1y_pos
  have he1_norm : normSqVec tomo_e1 = 1 := by
    simp [normSqVec, GaussRat.normSq, tomo_e1, gv]
  have he1y_norm : normSqVec (GVec.add tomo_e1 y) = 1 + normSqVec y :=
    normSqVec_add_tomo_e1_of_x_zero hyx
  have he1y_inner : (GVec.inner (GVec.add tomo_e1 y) tomo_e1).normSq = 1 := by
    simp [GVec.inner, GVec.add, tomo_e1, gv, hyx, GaussRat.normSq]
  have h_ortho_mer : GVec.inner (GVec.smul ⟨-normSqVec y, 0⟩ tomo_e1) y = 0 := by
    rw [inner_smul_left, inner_tomo_e1_of_x_zero hyx, mul_zero]
  have hmer_norm : normSqVec (meridianOrtho y) = normSqVec y * (1 + normSqVec y) := by
    rw [meridianOrtho, (normSqVec_add_eq_normSqVec_sub_of_ortho h_ortho_mer).1,
        normSqVec_smul, he1_norm]
    simp only [GaussRat.normSq]
    ring
  have hmer_inner : (GVec.inner (meridianOrtho y) y).normSq = (normSqVec y) ^ 2 := by
    rw [meridianOrtho, inner_add_left, h_ortho_mer, zero_add, inner_self_eq_normSqVec y]
    simp only [GaussRat.normSq]
    ring
  refine ⟨?_, ?_⟩
  · unfold raySinSq
    rw [he1y_inner, he1y_norm, he1_norm]
    field_simp
    ring
  · unfold raySinSq
    rw [hmer_inner, hmer_norm]
    field_simp
    ring

/-- **Uniform Equatorial Meridian Continuity from Single-Pole Pointwise Continuity
(`meridian_uniform_equatorial_continuity_of_pole_continuous`)**:
if a frame function `f` on `ℚ(i)³` is pointwise ray-continuous at the single pole `tomo_e1`
(`IsPointwiseRayContinuousAt f tomo_e1`), then for every `ε > 0` there exists a single modulus
`δ > 0` (uniform across all equatorial directions `y ∈ e₁⊥ \ {0}`) such that whenever
`raySinSq (meridianOrtho y) y < δ`, `|f (meridianOrtho y) - f y| < ε`. -/
theorem meridian_uniform_equatorial_continuity_of_pole_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f) (hcont : IsPointwiseRayContinuousAt f tomo_e1) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ y : GVec, y.x = 0 → y.NonZero →
        raySinSq (meridianOrtho y) y < δ → |f (meridianOrtho y) - f y| < ε := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := hcont ε hε
  refine ⟨δ, hδ, ?_⟩
  intro y hyx hy hsin
  have h_e1y_nz : (GVec.add tomo_e1 y).NonZero :=
    (isFrame_piron_base hyx hy one_ne_zero).1
  have hsin_eq := meridianOrtho_raySinSq_eq hyx hy
  have hsin_pole : raySinSq (GVec.add tomo_e1 y) tomo_e1 < δ := by
    rw [hsin_eq.1, ← hsin_eq.2]
    exact hsin
  have h_pole_lt := hb (GVec.add tomo_e1 y) h_e1y_nz hsin_pole
  have hbridge := (meridian_kelvin_universal_bridge hf hyx hy).2.2
  have h_abs : |f (meridianOrtho y) - f y| = |f (GVec.add tomo_e1 y) - f tomo_e1| := by
    rw [← abs_neg (f (meridianOrtho y) - f y)]
    congr 1
    linarith
  rw [h_abs]
  exact h_pole_lt

/-- **Exact Zero-Slack Piron Step–Partner Bridge (`piron_zero_slack_step_partner_bridge`)**:
for every frame function `f` on `ℚ(i)³` (without assuming `f tomo_e1 = 1` or nonnegativity),
every nonzero `y ∈ e₁⊥`, and every `lam ≠ 0`,
1. `f (pironStep y lam) + f (pironPartner y lam) = f (e₁ + y) + f (eqOrtho y)`,
2. `f (pironStep y lam) - f (e₁ + y) = f (eqOrtho y) - f (pironPartner y lam)`,
3. `|f (pironStep y lam) - f (e₁ + y)| = |f (pironPartner y lam) - f (eqOrtho y)|`. -/
theorem piron_zero_slack_step_partner_bridge {f : GVec → ℚ} (hf : IsFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) {lam : GaussRat} (hlam : lam ≠ 0) :
    f (pironStep y lam) + f (pironPartner y lam) =
      f (GVec.add tomo_e1 y) + f (eqOrtho y) ∧
    f (pironStep y lam) - f (GVec.add tomo_e1 y) =
      f (eqOrtho y) - f (pironPartner y lam) ∧
    |f (pironStep y lam) - f (GVec.add tomo_e1 y)| =
      |f (pironPartner y lam) - f (eqOrtho y)| := by
  have hsum := (piron_frame_sum_identity hf hyx hy hlam).2
  have heq_nz : (eqOrtho y).NonZero := (isFrame_tomo_e1_eqOrtho hyx hy).2.2.1
  have hsmul_eq := GaussianTomography.frameFunction_smul hf heq_nz hlam
  have h1 : f (pironStep y lam) + f (pironPartner y lam) =
      f (GVec.add tomo_e1 y) + f (eqOrtho y) := by linarith
  have h2 : f (pironStep y lam) - f (GVec.add tomo_e1 y) =
      f (eqOrtho y) - f (pironPartner y lam) := by linarith
  refine ⟨h1, h2, ?_⟩
  rw [h2, ← abs_neg (f (eqOrtho y) - f (pironPartner y lam))]
  congr 1
  ring

/-- **Symmetric Opposite-Step Piron Partner Balance (`piron_symmetric_step_partner_balance`)**:
for every frame function `f` on `ℚ(i)³`, every nonzero `y ∈ e₁⊥`, and every `lam ≠ 0`,
subtracting the Piron rotated frames at `+lam` and `-lam` cancels `f (e₁ + y)`, `f (eqOrtho y)`,
and `f (meridianOrtho y)` simultaneously with zero pole-deficiency slack:
`f (pironStep y lam) + f (pironPartner y lam) = f (pironStep y (-lam)) + f (pironPartner y (-lam))`
and `f (pironStep y lam) - f (pironStep y (-lam)) = f (pironPartner y (-lam)) - f (pironPartner y lam)`. -/
theorem piron_symmetric_step_partner_balance {f : GVec → ℚ} (hf : IsFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) {lam : GaussRat} (hlam : lam ≠ 0) :
    f (pironStep y lam) + f (pironPartner y lam) =
      f (pironStep y (-lam)) + f (pironPartner y (-lam)) ∧
    f (pironStep y lam) - f (pironStep y (-lam)) =
      f (pironPartner y (-lam)) - f (pironPartner y lam) := by
  have hlam_neg : -lam ≠ 0 := neg_ne_zero.mpr hlam
  have hpos := (piron_zero_slack_step_partner_bridge hf hyx hy hlam).1
  have hneg := (piron_zero_slack_step_partner_bridge hf hyx hy hlam_neg).1
  exact ⟨by linarith, by linarith⟩

/-- **Exact Piron Step–Partner Projective Ray-Distance Duality (`pironStep_pironPartner_raySinSq_eq`)**:
for every nonzero `y ∈ e₁⊥` and every `lam ≠ 0`, the projective ray distance
`raySinSq (pironStep y lam) (e₁ + y)` and the partner projective ray distance
`raySinSq (pironPartner y lam) (eqOrtho y)` are both identically equal to
`(lam.normSq * normSqVec y) / (1 + normSqVec y + lam.normSq * normSqVec y)`. -/
theorem pironStep_pironPartner_raySinSq_eq {y : GVec} (hyx : y.x = 0) (hy : y.NonZero)
    {lam : GaussRat} (hlam : lam ≠ 0) :
    raySinSq (pironStep y lam) (GVec.add tomo_e1 y) =
      (lam.normSq * normSqVec y) / (1 + normSqVec y + lam.normSq * normSqVec y) ∧
    raySinSq (pironPartner y lam) (eqOrtho y) =
      (lam.normSq * normSqVec y) / (1 + normSqVec y + lam.normSq * normSqVec y) := by
  let u := GVec.add tomo_e1 y
  let v := eqOrtho y
  have hy_pos := normSqVec_pos_of_nonZero hy
  have hy_ne : normSqVec y ≠ 0 := ne_of_gt hy_pos
  have hlam_pos := gaussRat_normSq_pos_of_ne_zero hlam
  have hlam_ne : lam.normSq ≠ 0 := ne_of_gt hlam_pos
  have hu_norm : normSqVec u = 1 + normSqVec y := normSqVec_add_tomo_e1_of_x_zero hyx
  have hv_norm : normSqVec v = normSqVec y := normSqVec_eqOrtho_of_x_zero hyx
  have hu_pos : 0 < 1 + normSqVec y := by linarith
  have hu_ne : 1 + normSqVec y ≠ 0 := ne_of_gt hu_pos
  have htot_pos : 0 < 1 + normSqVec y + lam.normSq * normSqVec y := by
    have : 0 < lam.normSq * normSqVec y := mul_pos hlam_pos hy_pos
    linarith
  have htot_ne : 1 + normSqVec y + lam.normSq * normSqVec y ≠ 0 := ne_of_gt htot_pos
  have huv : GVec.inner u v = 0 := by
    dsimp [u, v]
    rw [inner_add_left, inner_tomo_e1_of_x_zero rfl, inner_eqOrtho_self, add_zero]
  have hvu : GVec.inner v u = 0 := inner_eq_zero_symm huv
  have huv_lam : GVec.inner u (GVec.smul lam v) = 0 := by
    rw [GaussianTomography.inner_smul_right, huv, mul_zero]
  have hstep_norm : normSqVec (pironStep y lam) = 1 + normSqVec y + lam.normSq * normSqVec y := by
    change normSqVec (GVec.add u (GVec.smul lam v)) = _
    rw [(normSqVec_add_eq_normSqVec_sub_of_ortho huv_lam).1,
        hu_norm, normSqVec_smul, hv_norm]
  have hstep_inner : (GVec.inner (pironStep y lam) u).normSq = (1 + normSqVec y) ^ 2 := by
    change (GVec.inner (GVec.add u (GVec.smul lam v)) u).normSq = _
    rw [inner_add_left, inner_smul_left, hvu, mul_zero, add_zero,
        inner_self_eq_normSqVec u, hu_norm]
    simp only [GaussRat.normSq]
    ring
  have hpart_norm :
      normSqVec (pironPartner y lam) =
        (1 + normSqVec y) * (lam.normSq * normSqVec y) *
          (1 + normSqVec y + lam.normSq * normSqVec y) := by
    rw [pironPartner_eq_rotPairV hyx lam,
        normSqVec_rotPairV huv_lam 1 1,
        ← pironStep_eq_rotPairU y lam,
        hstep_norm, hu_norm, normSqVec_smul, hv_norm]
  have hpart_inner :
      (GVec.inner (pironPartner y lam) v).normSq =
        (1 + normSqVec y) ^ 2 * lam.normSq * (normSqVec y) ^ 2 := by
    change (GVec.inner
      (GVec.add
        (GVec.smul (-(star lam * lam * ⟨normSqVec y, 0⟩)) u)
        (GVec.smul (⟨1 + normSqVec y, 0⟩ * lam) v)) v).normSq = _
    rw [inner_add_left, inner_smul_left, huv, mul_zero, zero_add,
        inner_smul_left, inner_self_eq_normSqVec v, hv_norm]
    simp only [GaussRat.normSq, GaussRat.re_mul, GaussRat.im_mul,
      GaussRat.re_star, GaussRat.im_star]
    ring
  refine ⟨?_, ?_⟩
  · unfold raySinSq
    change 1 - (GVec.inner (pironStep y lam) u).normSq /
      (normSqVec (pironStep y lam) * normSqVec u) = _
    rw [hstep_inner, hstep_norm, hu_norm]
    field_simp
    ring
  · unfold raySinSq
    change 1 - (GVec.inner (pironPartner y lam) v).normSq /
      (normSqVec (pironPartner y lam) * normSqVec v) = _
    rw [hpart_inner, hpart_norm, hv_norm]
    field_simp
    ring

/-- **Zero-Slack Piron Tangent Continuity from Equatorial Partner Continuity
(`piron_step_continuous_of_eqOrtho_continuous`)**:
for any frame function `f` on `ℚ(i)³` (without assuming `f tomo_e1 = 1` or nonnegativity) and any
nonzero `y ∈ e₁⊥`, if `f` is pointwise ray-continuous at `eqOrtho y`
(`IsPointwiseRayContinuousAt f (eqOrtho y)`), then for every `ε > 0` there exists `δ > 0` such that
every Piron tangent step `pironStep y lam` (`lam ≠ 0`) with
`raySinSq (pironStep y lam) (e₁ + y) < δ` satisfies `|f (pironStep y lam) - f (e₁ + y)| < ε`
with **zero pole-deficiency slack**. -/
theorem piron_step_continuous_of_eqOrtho_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f) {y : GVec} (hyx : y.x = 0) (hy : y.NonZero)
    (hcont : IsPointwiseRayContinuousAt f (eqOrtho y)) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ lam : GaussRat, lam ≠ 0 →
        raySinSq (pironStep y lam) (GVec.add tomo_e1 y) < δ →
          |f (pironStep y lam) - f (GVec.add tomo_e1 y)| < ε := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := hcont ε hε
  refine ⟨δ, hδ, ?_⟩
  intro lam hlam hsin
  have hfr := isFrame_piron_base hyx hy hlam
  have hpart_nz : (pironPartner y lam).NonZero := by
    rw [pironPartner_eq_rotPairV hyx]
    exact (isFrame_rotPair hfr (Or.inl one_ne_zero)).2.1
  have hsin_eq := pironStep_pironPartner_raySinSq_eq hyx hy hlam
  have hsin_part : raySinSq (pironPartner y lam) (eqOrtho y) < δ := by
    rw [hsin_eq.2, ← hsin_eq.1]
    exact hsin
  have h_part_lt := hb (pironPartner y lam) hpart_nz hsin_part
  rw [(piron_zero_slack_step_partner_bridge hf hyx hy hlam).2.2]
  exact h_part_lt

/-- **Zero-Slack 3-Step Rational Piron Chain Oscillation Bound
(`piron_three_step_zero_slack_chain_abs_le`)**:
along any three successive nonzero equatorial tangent steps `y₁ = eqTangentStep y t₁`,
`y₂ = eqTangentStep y₁ t₂`, `y₃ = eqTangentStep y₂ t₃` from `y ∈ e₁⊥ \ {0}`, every frame function
`f` on `ℚ(i)³` satisfies the exact identity and triangle-inequality bound with zero pole-deficiency
slack:
`f (e₁ + y₃) - f (e₁ + y) = (f (eqOrtho y) - f (pironPartner y t₁)) + (f (eqOrtho y₁) - f (pironPartner y₁ t₂)) + (f (eqOrtho y₂) - f (pironPartner y₂ t₃))`
and
`|f (e₁ + y₃) - f (e₁ + y)| ≤ |f (pironPartner y t₁) - f (eqOrtho y)| + |f (pironPartner y₁ t₂) - f (eqOrtho y₁)| + |f (pironPartner y₂ t₃) - f (eqOrtho y₂)|`. -/
theorem piron_three_step_zero_slack_chain_abs_le {f : GVec → ℚ} (hf : IsFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero)
    {t₁ t₂ t₃ : ℚ} (ht₁ : t₁ ≠ 0) (ht₂ : t₂ ≠ 0) (ht₃ : t₃ ≠ 0) :
    let y₁ := eqTangentStep y t₁
    let y₂ := eqTangentStep y₁ t₂
    let y₃ := eqTangentStep y₂ t₃
    f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y) =
      (f (eqOrtho y) - f (pironPartner y ⟨t₁, 0⟩)) +
      (f (eqOrtho y₁) - f (pironPartner y₁ ⟨t₂, 0⟩)) +
      (f (eqOrtho y₂) - f (pironPartner y₂ ⟨t₃, 0⟩)) ∧
    |f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y)| ≤
      |f (pironPartner y ⟨t₁, 0⟩) - f (eqOrtho y)| +
      |f (pironPartner y₁ ⟨t₂, 0⟩) - f (eqOrtho y₁)| +
      |f (pironPartner y₂ ⟨t₃, 0⟩) - f (eqOrtho y₂)| := by
  dsimp only
  let y₁ := eqTangentStep y t₁
  let y₂ := eqTangentStep y₁ t₂
  let y₃ := eqTangentStep y₂ t₃
  have hy₁x : y₁.x = 0 := eqTangentStep_x_zero hyx t₁
  have hy₁ : y₁.NonZero := eqTangentStep_nonZero_of_x_zero hyx hy t₁
  have hy₂x : y₂.x = 0 := eqTangentStep_x_zero hy₁x t₂
  have hy₂ : y₂.NonZero := eqTangentStep_nonZero_of_x_zero hy₁x hy₁ t₂
  have hlam₁ : (⟨t₁, 0⟩ : GaussRat) ≠ 0 := fun h => ht₁ (congrArg GaussRat.re h)
  have hlam₂ : (⟨t₂, 0⟩ : GaussRat) ≠ 0 := fun h => ht₂ (congrArg GaussRat.re h)
  have hlam₃ : (⟨t₃, 0⟩ : GaussRat) ≠ 0 := fun h => ht₃ (congrArg GaussRat.re h)
  obtain ⟨_, hd1, ha1⟩ := piron_zero_slack_step_partner_bridge hf hyx hy hlam₁
  obtain ⟨_, hd2, ha2⟩ := piron_zero_slack_step_partner_bridge hf hy₁x hy₁ hlam₂
  obtain ⟨_, hd3, ha3⟩ := piron_zero_slack_step_partner_bridge hf hy₂x hy₂ hlam₃
  rw [pironStep_eq_add_eqTangentStep y t₁] at hd1 ha1
  rw [pironStep_eq_add_eqTangentStep y₁ t₂] at hd2 ha2
  rw [pironStep_eq_add_eqTangentStep y₂ t₃] at hd3 ha3
  have htel :
      f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y) =
        (f (GVec.add tomo_e1 y₁) - f (GVec.add tomo_e1 y)) +
        (f (GVec.add tomo_e1 y₂) - f (GVec.add tomo_e1 y₁)) +
        (f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y₂)) := by ring
  refine ⟨by linarith, ?_⟩
  have htri1 := abs_add_le
    ((f (GVec.add tomo_e1 y₁) - f (GVec.add tomo_e1 y)) +
     (f (GVec.add tomo_e1 y₂) - f (GVec.add tomo_e1 y₁)))
    (f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y₂))
  have htri2 := abs_add_le
    (f (GVec.add tomo_e1 y₁) - f (GVec.add tomo_e1 y))
    (f (GVec.add tomo_e1 y₂) - f (GVec.add tomo_e1 y₁))
  rw [htel]
  linarith

/-- **General 1-Step Rational Piron Bound with Pole-Deficiency Slack (`piron_general_one_step_le`)**:
for any nonnegative frame function `f` on `ℚ(i)³`, any nonzero `y ∈ e₁⊥`, and any `lam ≠ 0`,
`f (pironStep y lam) ≤ f (e₁ + y) + f (eqOrtho y) ≤ f (e₁ + y) + (1 - f tomo_e1)`. -/
theorem piron_general_one_step_le {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) {lam : GaussRat} (hlam : lam ≠ 0) :
    f (pironStep y lam) ≤ f (GVec.add tomo_e1 y) + f (eqOrtho y) ∧
    f (pironStep y lam) ≤ f (GVec.add tomo_e1 y) + (1 - f tomo_e1) := by
  have hfr := isFrame_piron_base hyx hy hlam
  have hsum := (piron_frame_sum_identity hf.1 hyx hy hlam).2
  have heq_nz : (eqOrtho y).NonZero := (isFrame_tomo_e1_eqOrtho hyx hy).2.2.1
  have hsmul_eq := GaussianTomography.frameFunction_smul hf.1 heq_nz hlam
  have hpart_nz : (pironPartner y lam).NonZero := by
    rw [pironPartner_eq_rotPairV hyx]
    exact (isFrame_rotPair hfr (Or.inl one_ne_zero)).2.1
  have hpart_nn := hf.2 (pironPartner y lam) hpart_nz
  have heq_le := (equatorial_pair_sum_eq_one_sub_pole hf hyx hy).2.2
  exact ⟨by linarith, by linarith⟩

/-- **General 2-Step Opposite-Tangent Rational Piron Radial Bound (`piron_general_two_step_radial_le`)**:
for any nonnegative frame function `f` on `ℚ(i)³`, any nonzero `y ∈ e₁⊥`, and any `t ≠ 0`,
`f (e₁ + (1 + t²) • y) ≤ f (pironStep y ⟨t, 0⟩) + (1 - f tomo_e1) ≤ f (e₁ + y) + 2 * (1 - f tomo_e1)`. -/
theorem piron_general_two_step_radial_le {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) {t : ℚ} (ht : t ≠ 0) :
    f (GVec.add tomo_e1 (GVec.smul ⟨1 + t ^ 2, 0⟩ y)) ≤
      f (pironStep y ⟨t, 0⟩) + (1 - f tomo_e1) ∧
    f (GVec.add tomo_e1 (GVec.smul ⟨1 + t ^ 2, 0⟩ y)) ≤
      f (GVec.add tomo_e1 y) + 2 * (1 - f tomo_e1) := by
  have hlam : (⟨t, 0⟩ : GaussRat) ≠ 0 := fun h => ht (congrArg GaussRat.re h)
  have hlam_neg : (⟨-t, 0⟩ : GaussRat) ≠ 0 :=
    fun h => (neg_ne_zero.mpr ht) (congrArg GaussRat.re h)
  have hstep1 := (piron_general_one_step_le hf hyx hy hlam).2
  have hstep2 :=
    (piron_general_one_step_le hf
      (eqTangentStep_x_zero hyx t)
      (eqTangentStep_nonZero_of_x_zero hyx hy t)
      hlam_neg).2
  rw [pironStep_eq_add_eqTangentStep (eqTangentStep y t) (-t),
      eqTangentStep_cancel_of_x_zero hyx t,
      ← pironStep_eq_add_eqTangentStep y t] at hstep2
  exact ⟨hstep2, by linarith⟩

/-- **General 3-Step Rational Piron Tangent Chain Bound (`piron_general_three_step_chain_le`)**:
along any three successive nonzero equatorial tangent steps `y₁ = eqTangentStep y t₁`,
`y₂ = eqTangentStep y₁ t₂`, `y₃ = eqTangentStep y₂ t₃` from `y ∈ e₁⊥ \ {0}`, every nonnegative
frame function `f` satisfies:
`f (e₁ + y₃) - f (e₁ + y) ≤ f (eqOrtho y) + f (eqOrtho y₁) + f (eqOrtho y₂) ≤ 3 * (1 - f tomo_e1)`. -/
theorem piron_general_three_step_chain_le {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero)
    {t₁ t₂ t₃ : ℚ} (ht₁ : t₁ ≠ 0) (ht₂ : t₂ ≠ 0) (ht₃ : t₃ ≠ 0) :
    let y₁ := eqTangentStep y t₁
    let y₂ := eqTangentStep y₁ t₂
    let y₃ := eqTangentStep y₂ t₃
    f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y) ≤
      f (eqOrtho y) + f (eqOrtho y₁) + f (eqOrtho y₂) ∧
    f (GVec.add tomo_e1 y₃) - f (GVec.add tomo_e1 y) ≤ 3 * (1 - f tomo_e1) := by
  dsimp only
  let y₁ := eqTangentStep y t₁
  let y₂ := eqTangentStep y₁ t₂
  let y₃ := eqTangentStep y₂ t₃
  have hy₁x : y₁.x = 0 := eqTangentStep_x_zero hyx t₁
  have hy₁ : y₁.NonZero := eqTangentStep_nonZero_of_x_zero hyx hy t₁
  have hy₂x : y₂.x = 0 := eqTangentStep_x_zero hy₁x t₂
  have hy₂ : y₂.NonZero := eqTangentStep_nonZero_of_x_zero hy₁x hy₁ t₂
  have hlam₁ : (⟨t₁, 0⟩ : GaussRat) ≠ 0 := fun h => ht₁ (congrArg GaussRat.re h)
  have hlam₂ : (⟨t₂, 0⟩ : GaussRat) ≠ 0 := fun h => ht₂ (congrArg GaussRat.re h)
  have hlam₃ : (⟨t₃, 0⟩ : GaussRat) ≠ 0 := fun h => ht₃ (congrArg GaussRat.re h)
  obtain ⟨hs1_eq, hs1_pole⟩ := piron_general_one_step_le hf hyx hy hlam₁
  obtain ⟨hs2_eq, hs2_pole⟩ := piron_general_one_step_le hf hy₁x hy₁ hlam₂
  obtain ⟨hs3_eq, hs3_pole⟩ := piron_general_one_step_le hf hy₂x hy₂ hlam₃
  rw [pironStep_eq_add_eqTangentStep y t₁] at hs1_eq hs1_pole
  rw [pironStep_eq_add_eqTangentStep y₁ t₂] at hs2_eq hs2_pole
  rw [pironStep_eq_add_eqTangentStep y₂ t₃] at hs3_eq hs3_pole
  exact ⟨by linarith, by linarith⟩

/-- **General Piron–Pythagorean Two-Sided Sandwich with Pole-Deficiency Slack (`pythagEqRot_general_sandwich`)**:
for every nonnegative frame function `f` on `ℚ(i)³`, every nonzero `y ∈ e₁⊥`, and every `k ≥ 2`,
the Pythagorean rotated value `f (e₁ + pythagEqRot y k)` is sandwiched between the two radial
meridian perturbations up to the pole-deficiency slack `1 - f tomo_e1`:
`f (e₁ + ((k²+1)/(k²-1)) y) - (1 - f tomo_e1) ≤ f (e₁ + pythagEqRot y k)` and
`f (e₁ + pythagEqRot y k) ≤ f (e₁ + ((k²-1)/(k²+1)) y) + (1 - f tomo_e1)`. -/
theorem pythagEqRot_general_sandwich {f : GVec → ℚ} (hf : IsNonnegFrameFunction f)
    {y : GVec} (hyx : y.x = 0) (hy : y.NonZero) {k : ℕ} (hk : 2 ≤ k) :
    f (GVec.add tomo_e1 (GVec.smul ⟨((k : ℚ) ^ 2 + 1) / ((k : ℚ) ^ 2 - 1), 0⟩ y)) -
      (1 - f tomo_e1) ≤ f (GVec.add tomo_e1 (pythagEqRot y k)) ∧
    f (GVec.add tomo_e1 (pythagEqRot y k)) ≤
      f (GVec.add tomo_e1 (GVec.smul ⟨((k : ℚ) ^ 2 - 1) / ((k : ℚ) ^ 2 + 1), 0⟩ y)) +
        (1 - f tomo_e1) := by
  let a : ℚ := ((k : ℚ) ^ 2 - 1) / ((k : ℚ) ^ 2 + 1)
  let t : ℚ := (2 * (k : ℚ)) / ((k : ℚ) ^ 2 - 1)
  let y_lo : GVec := GVec.smul ⟨a, 0⟩ y
  have hk_q : (2 : ℚ) ≤ (k : ℚ) := by exact_mod_cast hk
  have hkm1_pos : 0 < (k : ℚ) ^ 2 - 1 := by nlinarith
  have hkp1_pos : 0 < (k : ℚ) ^ 2 + 1 := by positivity
  have ha_pos : 0 < a := div_pos hkm1_pos hkp1_pos
  have ht_pos : 0 < t := div_pos (by linarith) hkm1_pos
  have ha_ne : (⟨a, 0⟩ : GaussRat) ≠ 0 := by
    intro h
    have hre := congrArg GaussRat.re h
    dsimp at hre
    linarith
  have hy_lo_x : y_lo.x = 0 := by simp [y_lo, GVec.smul, hyx]
  have hy_lo_nz : y_lo.NonZero := nonZero_smul ha_ne hy
  obtain ⟨h1, _⟩ :=
    piron_general_two_step_radial_le hf hy_lo_x hy_lo_nz (ne_of_gt ht_pos)
  have hlam : (⟨t, 0⟩ : GaussRat) ≠ 0 :=
    fun h => (ne_of_gt ht_pos) (congrArg GaussRat.re h)
  have h2 := (piron_general_one_step_le hf hy_lo_x hy_lo_nz hlam).2
  have hpiron_rot : pironStep y_lo ⟨t, 0⟩ = GVec.add tomo_e1 (pythagEqRot y k) := by
    rw [pironStep_eq_add_eqTangentStep, ← pythagEqRot_eq_eqTangentStep_of_two_le hk]
  have hneg_t : -t = -(2 * (k : ℚ)) / ((k : ℚ) ^ 2 - 1) := by dsimp [t]; ring
  have hhi_eq :
      GVec.smul ⟨1 + t ^ 2, 0⟩ y_lo =
        GVec.smul ⟨((k : ℚ) ^ 2 + 1) / ((k : ℚ) ^ 2 - 1), 0⟩ y := by
    rw [← eqTangentStep_cancel_of_x_zero hy_lo_x t,
        ← pythagEqRot_eq_eqTangentStep_of_two_le hk,
        hneg_t,
        eqTangentStep_pythagEqRot_neg_of_x_zero hyx hk]
  rw [hpiron_rot, hhi_eq] at h1
  rw [hpiron_rot] at h2
  exact ⟨by linarith, h2⟩

/-! #### 7B. Track B: Irrational-Locus / Dedekind-Cut Frame-Function Stress Tests on `ℚ(i)³` -/

/-- **Local Constancy of `dedekindRayCut` Near `tomo_e1` (`dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt`)**:
for every nonzero `u ∈ ℚ(i)³` with `raySinSq u tomo_e1 < 1 / 2`, `|u.y|² < (1 / 2) ‖u‖²`, so
`3 |u.y|⁴ < (3 / 4) ‖u‖⁴ < ‖u‖⁴` and `dedekindRayCut u = 0`. -/
theorem dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt {u : GVec} (hu : u.NonZero)
    (hsin : raySinSq u tomo_e1 < 1 / 2) :
    dedekindRayCut u = 0 := by
  have hnu_pos : 0 < normSqVec u := normSqVec_pos_of_nonZero hu
  have hnu_ne : normSqVec u ≠ 0 := ne_of_gt hnu_pos
  have he1_norm : normSqVec tomo_e1 = 1 := by
    simp [normSqVec, GaussRat.normSq, tomo_e1, gv]
  have hinner : (GVec.inner u tomo_e1).normSq = u.x.normSq := by
    simp [GVec.inner, tomo_e1, gv, GaussRat.normSq]
  have hsin_eq : normSqVec u * raySinSq u tomo_e1 = u.y.normSq + u.z.normSq := by
    unfold raySinSq
    rw [hinner, he1_norm, mul_one, mul_sub, mul_one, mul_div_cancel₀ _ hnu_ne]
    simp only [normSqVec]
    ring
  have huz_nn : 0 ≤ u.z.normSq := GaussRat.normSq_nonneg u.z
  have huy_nn : 0 ≤ u.y.normSq := GaussRat.normSq_nonneg u.y
  have huy_lt : u.y.normSq < (1 / 2) * normSqVec u := by
    have hmul : normSqVec u * raySinSq u tomo_e1 < normSqVec u * (1 / 2) :=
      mul_lt_mul_of_pos_left hsin hnu_pos
    linarith
  have h3_lt : 3 * (u.y.normSq) ^ 2 < (normSqVec u) ^ 2 := by
    nlinarith
  unfold dedekindRayCut
  exact ite_eq_right_iff.mpr (fun h => absurd h (not_lt.mpr (le_of_lt h3_lt)))

/-- **Pointwise Ray Continuity of `dedekindRayCut` at `tomo_e1` (`dedekindRayCut_isPointwiseRayContinuousAt_tomo_e1`)**:
despite jumping by `1` across the irrational cone `3 |u.y|⁴ = ‖u‖⁴`, `dedekindRayCut` is locally
constant (and hence pointwise ray-continuous) on the rational ray neighborhood
`raySinSq u tomo_e1 < 1 / 2` of `tomo_e1`. -/
theorem dedekindRayCut_isPointwiseRayContinuousAt_tomo_e1 :
    IsPointwiseRayContinuousAt dedekindRayCut tomo_e1 := by
  intro ε hε
  refine ⟨1 / 2, by norm_num, ?_⟩
  intro u hu hsin
  have hu0 := dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt hu hsin
  have he1 : dedekindRayCut tomo_e1 = 0 := by
    norm_num [dedekindRayCut, tomo_e1, gv, normSqVec, GaussRat.normSq]
  rw [hu0, he1, sub_self, abs_zero]
  exact hε

/-- **Local Constancy of `dedekindRayCut` Near `tomo_e2` (`dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt`)**:
for every nonzero `u ∈ ℚ(i)³` with `raySinSq u tomo_e2 < 1 / 3`, `|u.y|² > (2 / 3) ‖u‖²`, so
`3 |u.y|⁴ > (4 / 3) ‖u‖⁴ > ‖u‖⁴` and `dedekindRayCut u = 1`. -/
theorem dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt {u : GVec} (hu : u.NonZero)
    (hsin : raySinSq u tomo_e2 < 1 / 3) :
    dedekindRayCut u = 1 := by
  have hnu_pos : 0 < normSqVec u := normSqVec_pos_of_nonZero hu
  have hnu_ne : normSqVec u ≠ 0 := ne_of_gt hnu_pos
  have he2_norm : normSqVec tomo_e2 = 1 := by
    simp [normSqVec, GaussRat.normSq, tomo_e2, gv]
  have hinner : (GVec.inner u tomo_e2).normSq = u.y.normSq := by
    simp [GVec.inner, tomo_e2, gv, GaussRat.normSq]
  have hsin_eq : normSqVec u * raySinSq u tomo_e2 = normSqVec u - u.y.normSq := by
    unfold raySinSq
    rw [hinner, he2_norm, mul_one, mul_sub, mul_one, mul_div_cancel₀ _ hnu_ne]
  have huy_gt : (2 / 3) * normSqVec u < u.y.normSq := by
    have hmul : normSqVec u * raySinSq u tomo_e2 < normSqVec u * (1 / 3) :=
      mul_lt_mul_of_pos_left hsin hnu_pos
    linarith
  have h3_gt : (normSqVec u) ^ 2 < 3 * (u.y.normSq) ^ 2 := by
    nlinarith
  unfold dedekindRayCut
  exact ite_eq_left_iff.mpr (fun h => absurd h3_gt h)

/-- **Pointwise Ray Continuity of `dedekindRayCut` at `tomo_e2` (`dedekindRayCut_isPointwiseRayContinuousAt_tomo_e2`)**:
`dedekindRayCut` is locally constant (`= 1`) and hence pointwise ray-continuous on the rational ray
neighborhood `raySinSq u tomo_e2 < 1 / 3` of `tomo_e2`. -/
theorem dedekindRayCut_isPointwiseRayContinuousAt_tomo_e2 :
    IsPointwiseRayContinuousAt dedekindRayCut tomo_e2 := by
  intro ε hε
  refine ⟨1 / 3, by norm_num, ?_⟩
  intro u hu hsin
  have hu1 := dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt hu hsin
  have he2 : dedekindRayCut tomo_e2 = 1 := by
    norm_num [dedekindRayCut, tomo_e2, gv, normSqVec, GaussRat.normSq]
  rw [hu1, he2, sub_self, abs_zero]
  exact hε

/-- **Refutation of 3-Frame Additivity for `dedekindRayCut` (`dedekindRayCut_not_isFrameFunction`)**:
on the rational anchor-bisector frame `(tomo_e3, tomo_e12, bisector_12_neg)`, the `y`-latitudes are
`0, 1 / 2, 1 / 2` (all below `1 / √3`), so `dedekindRayCut` evaluates to `0 + 0 + 0 = 0 ≠ 1`. -/
theorem dedekindRayCut_not_isFrameFunction : ¬ IsFrameFunction dedekindRayCut := by
  intro hf
  have hsum := hf tomo_e3 tomo_e12 bisector_12_neg isFrame_tomo_e3_e12_bisector
  have h0 : dedekindRayCut tomo_e3 + dedekindRayCut tomo_e12 + dedekindRayCut bisector_12_neg = 0 := by
    norm_num [dedekindRayCut, tomo_e3, tomo_e12, bisector_12_neg, gv, normSqVec, GaussRat.normSq]
  linarith

/-- Ray function `u ↦ h (|u.y|² / ‖u‖²)` depending only on the single coordinate latitude
`u.y.normSq / normSqVec u`. -/
def yLatitudeFunction (h : ℚ → ℚ) (u : GVec) : ℚ :=
  h (u.y.normSq / normSqVec u)

/-- **Two-Frame Latitude Constraints (`yLatitudeFunction_std_and_bisector_constraints`)**:
if a single-coordinate latitude function `yLatitudeFunction h` is a frame function on `ℚ(i)³`,
evaluating it on the standard basis frame `(tomo_e1, tomo_e2, tomo_e3)` and the bisector frame
`(tomo_e3, tomo_e12, bisector_12_neg)` forces `2 * h 0 + h 1 = 1` and `h 0 + 2 * h (1 / 2) = 1`. -/
theorem yLatitudeFunction_std_and_bisector_constraints {h : ℚ → ℚ}
    (hf : IsFrameFunction (yLatitudeFunction h)) :
    2 * h 0 + h 1 = 1 ∧ h 0 + 2 * h (1 / 2) = 1 := by
  have hstd := hf tomo_e1 tomo_e2 tomo_e3 frame_tomo_std
  have hbis := hf tomo_e3 tomo_e12 bisector_12_neg isFrame_tomo_e3_e12_bisector
  have he1 : yLatitudeFunction h tomo_e1 = h 0 := by
    norm_num [yLatitudeFunction, tomo_e1, gv, normSqVec, GaussRat.normSq]
  have he2 : yLatitudeFunction h tomo_e2 = h 1 := by
    norm_num [yLatitudeFunction, tomo_e2, gv, normSqVec, GaussRat.normSq]
  have he3 : yLatitudeFunction h tomo_e3 = h 0 := by
    norm_num [yLatitudeFunction, tomo_e3, gv, normSqVec, GaussRat.normSq]
  have he12 : yLatitudeFunction h tomo_e12 = h (1 / 2) := by
    norm_num [yLatitudeFunction, tomo_e12, gv, normSqVec, GaussRat.normSq]
  have h12n : yLatitudeFunction h bisector_12_neg = h (1 / 2) := by
    norm_num [yLatitudeFunction, bisector_12_neg, normSqVec, GaussRat.normSq]
  rw [he1, he2, he3] at hstd
  rw [he3, he12, h12n] at hbis
  exact ⟨by linarith, by linarith⟩

/-- **No `{0, 1}`-Valued 1D Latitude Cut Is a Frame Function (`no_zero_one_latitude_frameFunction`)**:
no profile `h : ℚ → ℚ` taking values in `{0, 1}` at the three rational latitudes `{0, 1 / 2, 1}`
(at any irrational or rational threshold) can satisfy `IsFrameFunction (yLatitudeFunction h)`. -/
theorem no_zero_one_latitude_frameFunction (h : ℚ → ℚ)
    (h0 : h 0 = 0 ∨ h 0 = 1)
    (h12 : h (1 / 2) = 0 ∨ h (1 / 2) = 1)
    (h1 : h 1 = 0 ∨ h 1 = 1) :
    ¬ IsFrameFunction (yLatitudeFunction h) := by
  intro hf
  obtain ⟨hstd, hbis⟩ := yLatitudeFunction_std_and_bisector_constraints hf
  rcases h0 with h0_0 | h0_1 <;> rcases h12 with h12_0 | h12_1 <;> rcases h1 with h1_0 | h1_1 <;>
    linarith

/-- Equatorial vector `(a, b, 0)` and its planar orthogonal partner `(-b, a, 0)` together with
their Gaussian-norm `45°` polar lifts `(a, b, a + b i)` and `(a, b, -(a + b i))` in `ℚ(i)³`. -/
def gaussianHalvingBase (a b : ℚ) : GVec := ⟨⟨a, 0⟩, ⟨b, 0⟩, 0⟩
def gaussianHalvingOrtho (a b : ℚ) : GVec := ⟨⟨-b, 0⟩, ⟨a, 0⟩, 0⟩
def gaussianHalvingPos (a b : ℚ) : GVec := ⟨⟨a, 0⟩, ⟨b, 0⟩, ⟨a, b⟩⟩
def gaussianHalvingNeg (a b : ℚ) : GVec := ⟨⟨a, 0⟩, ⟨b, 0⟩, -⟨a, b⟩⟩

/-- For any `(a, b) ∈ ℚ²` with `a² + b² ≠ 0`, `(gaussianHalvingBase a b, tomo_e3, gaussianHalvingOrtho a b)`
is an orthogonal 3-frame in `ℚ(i)³`. -/
theorem isFrame_gaussianHalving_base {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    IsFrame (gaussianHalvingBase a b) tomo_e3 (gaussianHalvingOrtho a b) := by
  have hpos : 0 < a ^ 2 + b ^ 2 := by
    rcases (add_nonneg (sq_nonneg a) (sq_nonneg b)).lt_or_eq with h | h
    · exact h
    · exact absurd h.symm hab
  have hu_eq : normSqVec (gaussianHalvingBase a b) = a ^ 2 + b ^ 2 := by
    simp [gaussianHalvingBase, normSqVec, GaussRat.normSq]
  have hw_eq : normSqVec (gaussianHalvingOrtho a b) = a ^ 2 + b ^ 2 := by
    simp [gaussianHalvingOrtho, normSqVec, GaussRat.normSq]
    ring
  have hu_pos : 0 < normSqVec (gaussianHalvingBase a b) := by linarith
  have hw_pos : 0 < normSqVec (gaussianHalvingOrtho a b) := by linarith
  refine ⟨nonZero_of_normSqVec_pos hu_pos, tomo_e3_nonZero, nonZero_of_normSqVec_pos hw_pos,
    ?_, ?_, ?_⟩
  · ext <;> simp [GVec.inner, gaussianHalvingBase, tomo_e3, gv]
  · ext <;> (simp [GVec.inner, gaussianHalvingBase, gaussianHalvingOrtho]; try ring)
  · ext <;> simp [GVec.inner, tomo_e3, gaussianHalvingOrtho, gv]

/-- Because `|a + b i|² = a² + b² = ‖(a, b, 0)‖²`, the rotated pair
`(gaussianHalvingPos a b, gaussianHalvingNeg a b, gaussianHalvingOrtho a b)` is also an exact
orthogonal 3-frame in `ℚ(i)³` whenever `a² + b² ≠ 0`, and halves the `(x, y)` coordinate latitudes
from `(a²/(a²+b²), b²/(a²+b²))` to `(a²/(2(a²+b²)), b²/(2(a²+b²)))`. -/
theorem isFrame_gaussianHalving_rot {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    IsFrame (gaussianHalvingPos a b) (gaussianHalvingNeg a b) (gaussianHalvingOrtho a b) := by
  have hpos : 0 < a ^ 2 + b ^ 2 := by
    rcases (add_nonneg (sq_nonneg a) (sq_nonneg b)).lt_or_eq with h | h
    · exact h
    · exact absurd h.symm hab
  have hu_eq : normSqVec (gaussianHalvingPos a b) = 2 * (a ^ 2 + b ^ 2) := by
    simp [gaussianHalvingPos, normSqVec, GaussRat.normSq]
    ring
  have hv_eq : normSqVec (gaussianHalvingNeg a b) = 2 * (a ^ 2 + b ^ 2) := by
    simp [gaussianHalvingNeg, normSqVec, GaussRat.normSq]
    ring
  have hw_eq : normSqVec (gaussianHalvingOrtho a b) = a ^ 2 + b ^ 2 := by
    simp [gaussianHalvingOrtho, normSqVec, GaussRat.normSq]
    ring
  have hu_pos : 0 < normSqVec (gaussianHalvingPos a b) := by linarith
  have hv_pos : 0 < normSqVec (gaussianHalvingNeg a b) := by linarith
  have hw_pos : 0 < normSqVec (gaussianHalvingOrtho a b) := by linarith
  refine ⟨nonZero_of_normSqVec_pos hu_pos, nonZero_of_normSqVec_pos hv_pos,
    nonZero_of_normSqVec_pos hw_pos, ?_, ?_, ?_⟩
  · ext <;> (simp [GVec.inner, gaussianHalvingPos, gaussianHalvingNeg]; try ring)
  · ext <;> (simp [GVec.inner, gaussianHalvingPos, gaussianHalvingOrtho]; try ring)
  · ext <;> (simp [GVec.inner, gaussianHalvingNeg, gaussianHalvingOrtho]; try ring)

/-- **Two-Frame Gaussian-Norm Latitude-Halving Identity (`coordSignSymmetric_gaussian_halving_identity`)**:
for any frame function `f` on `ℚ(i)³` that is coordinate-sign symmetric (`IsCoordSignSymmetric f`,
satisfied by every function of the coordinate norms `(|x|², |y|², |z|²)`) and any `(a, b) ∈ ℚ²`
with `a² + b² ≠ 0`, subtracting the two frames `(gaussianHalvingBase a b, tomo_e3, gaussianHalvingOrtho a b)`
and `(gaussianHalvingPos a b, gaussianHalvingNeg a b, gaussianHalvingOrtho a b)` forces the exact
latitude-halving equation `2 * f (gaussianHalvingPos a b) = f (gaussianHalvingBase a b) + f tomo_e3`. -/
theorem coordSignSymmetric_gaussian_halving_identity {f : GVec → ℚ}
    (hf : IsFrameFunction f) (hsym : IsCoordSignSymmetric f)
    {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    2 * f (gaussianHalvingPos a b) = f (gaussianHalvingBase a b) + f tomo_e3 := by
  have hbase := hf _ _ _ (isFrame_gaussianHalving_base hab)
  have hrot := hf _ _ _ (isFrame_gaussianHalving_rot hab)
  have hneg_eq : f (gaussianHalvingNeg a b) = f (gaussianHalvingPos a b) :=
    (hsym ⟨a, 0⟩ ⟨b, 0⟩ ⟨a, b⟩).2
  linarith

/-- **Zero-Weight Gaussian-Norm Latitude-Halving Identity
(`zeroWeight_coordSignSymmetric_gaussian_halving_identity`)**:
for any coordinate-sign symmetric zero-weight frame residual `g` on `ℚ(i)³` and any `(a, b) ∈ ℚ²`
with `a² + b² ≠ 0`, `2 * g (gaussianHalvingPos a b) = g (gaussianHalvingBase a b) + g tomo_e3`. -/
theorem zeroWeight_coordSignSymmetric_gaussian_halving_identity {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hsym : IsCoordSignSymmetric g)
    {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    2 * g (gaussianHalvingPos a b) = g (gaussianHalvingBase a b) + g tomo_e3 := by
  have hbase := hg _ _ _ (isFrame_gaussianHalving_base hab)
  have hrot := hg _ _ _ (isFrame_gaussianHalving_rot hab)
  have hneg_eq : g (gaussianHalvingNeg a b) = g (gaussianHalvingPos a b) :=
    (hsym ⟨a, 0⟩ ⟨b, 0⟩ ⟨a, b⟩).2
  linarith

/-- **General Gaussian-Halving Irrational-Cone Exit Theorem
(`gaussianHalvingPos_exits_irrational_cone`)**:
for **every** `(a, b) ∈ ℚ²` with `a² + b² ≠ 0`, the Gaussian-norm `45°` lift
`gaussianHalvingPos a b = (a, b, a + b i)` has `y`-latitude `b² / (2(a² + b²)) ≤ 1 / 2 < 1 / √3`,
so `3 |y|⁴ = 3 b⁴ < 4 (a² + b²)² = ‖gaussianHalvingPos a b‖⁴` and `gaussianHalvingPos a b` exits
the irrational cone `3 |u.y|⁴ > ‖u‖⁴`. -/
theorem gaussianHalvingPos_exits_irrational_cone {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    3 * ((gaussianHalvingPos a b).y.normSq) ^ 2 < (normSqVec (gaussianHalvingPos a b)) ^ 2 := by
  have hpos : 0 < a ^ 2 + b ^ 2 := by
    rcases (add_nonneg (sq_nonneg a) (sq_nonneg b)).lt_or_eq with h | h
    · exact h
    · exact absurd h.symm hab
  have hy_eq : (gaussianHalvingPos a b).y.normSq = b ^ 2 := by
    simp [gaussianHalvingPos, GaussRat.normSq]
  have hn_eq : normSqVec (gaussianHalvingPos a b) = 2 * (a ^ 2 + b ^ 2) := by
    simp [gaussianHalvingPos, normSqVec, GaussRat.normSq]
    ring
  rw [hy_eq, hn_eq]
  have ha2 : 0 ≤ a ^ 2 := sq_nonneg a
  have hb2 : 0 ≤ b ^ 2 := sq_nonneg b
  have hsq_pos : 0 < (a ^ 2 + b ^ 2) ^ 2 := sq_pos_of_pos hpos
  nlinarith

/-- For **every** `a, b : ℚ`, `dedekindRayCut (gaussianHalvingPos a b) = 0`. -/
theorem dedekindRayCut_gaussianHalvingPos_eq_zero (a b : ℚ) :
    dedekindRayCut (gaussianHalvingPos a b) = 0 := by
  by_cases hab : a ^ 2 + b ^ 2 = 0
  · have ha0 : a = 0 := by nlinarith [sq_nonneg a, sq_nonneg b]
    have hb0 : b = 0 := by nlinarith [sq_nonneg a, sq_nonneg b]
    subst ha0 hb0
    norm_num [dedekindRayCut, gaussianHalvingPos, normSqVec, GaussRat.normSq]
  · have hexit := gaussianHalvingPos_exits_irrational_cone hab
    unfold dedekindRayCut
    exact ite_eq_right_iff.mpr (fun h => absurd h (not_lt.mpr (le_of_lt hexit)))

/-- **General Vanishing of Irrational-Cone-Supported Symmetric Residuals on the `(x, y)`-Plane
(`zero_on_xy_plane_of_subcone_zero_and_coordSignSymmetric`)**:
if `g : GVec → ℚ` is any coordinate-sign symmetric zero-weight frame residual that vanishes on the
sub-cone `3 |u.y|⁴ < ‖u‖⁴` (i.e., `g` is supported inside the irrational cone `3 |u.y|⁴ > ‖u‖⁴`
around `tomo_e2`), then `g (gaussianHalvingBase a b) = 0` for **every** `(a, b) ∈ ℚ²` with
`a² + b² ≠ 0` (including `tomo_e2 = gaussianHalvingBase 0 1` and every ray in the `(x, y)`-plane
inside the irrational cone). -/
theorem zero_on_xy_plane_of_subcone_zero_and_coordSignSymmetric {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hsym : IsCoordSignSymmetric g)
    (hsub : ∀ u : GVec, u.NonZero → 3 * (u.y.normSq) ^ 2 < (normSqVec u) ^ 2 → g u = 0)
    {a b : ℚ} (hab : a ^ 2 + b ^ 2 ≠ 0) :
    g (gaussianHalvingBase a b) = 0 := by
  have hhalve := zeroWeight_coordSignSymmetric_gaussian_halving_identity hg hsym hab
  have hpos_nz : (gaussianHalvingPos a b).NonZero := (isFrame_gaussianHalving_rot hab).1
  have hpos_zero : g (gaussianHalvingPos a b) = 0 :=
    hsub (gaussianHalvingPos a b) hpos_nz (gaussianHalvingPos_exits_irrational_cone hab)
  have he3_lt : 3 * (tomo_e3.y.normSq) ^ 2 < (normSqVec tomo_e3) ^ 2 := by
    norm_num [tomo_e3, gv, normSqVec, GaussRat.normSq]
  have he3_zero : g tomo_e3 = 0 := hsub tomo_e3 tomo_e3_nonZero he3_lt
  linarith

theorem dedekindRayCut_eq_of_normSq_eq {u v : GVec}
    (hn : normSqVec u = normSqVec v) (hy : u.y.normSq = v.y.normSq) :
    dedekindRayCut u = dedekindRayCut v := by
  unfold dedekindRayCut
  rw [hn, hy]

theorem dedekindRayCut_isCoordSignSymmetric : IsCoordSignSymmetric dedekindRayCut :=
  fun x y z =>
    ⟨dedekindRayCut_eq_of_normSq_eq (by simp [normSqVec, gaussRat_normSq_neg]) (gaussRat_normSq_neg y),
     dedekindRayCut_eq_of_normSq_eq (by simp [normSqVec, gaussRat_normSq_neg]) rfl⟩

/-- **Explicit Gaussian-Halving Obstruction for `dedekindRayCut` at `(a, b) = (1, 2)`
(`dedekindRayCut_fails_gaussian_halving_at_1_2`)**:
at `(a, b) = (1, 2)`, the `y`-latitude of `gaussianHalvingBase 1 2 = (1, 2, 0)` is `4 / 5 > 1 / √3`
(`dedekindRayCut = 1`), whereas the halved `y`-latitude of `gaussianHalvingPos 1 2 = (1, 2, 1 + 2i)`
is `2 / 5 < 1 / √3` (`dedekindRayCut = 0`), violating the 2-frame Gaussian-halving identity
`2 * f (gaussianHalvingPos 1 2) = f (gaussianHalvingBase 1 2) + f tomo_e3`. -/
theorem dedekindRayCut_fails_gaussian_halving_at_1_2 :
    dedekindRayCut (gaussianHalvingBase 1 2) = 1 ∧
    dedekindRayCut tomo_e3 = 0 ∧
    dedekindRayCut (gaussianHalvingPos 1 2) = 0 ∧
    2 * dedekindRayCut (gaussianHalvingPos 1 2) ≠
      dedekindRayCut (gaussianHalvingBase 1 2) + dedekindRayCut tomo_e3 := by
  refine ⟨?_, ?_, dedekindRayCut_gaussianHalvingPos_eq_zero 1 2, ?_⟩
  · norm_num [dedekindRayCut, gaussianHalvingBase, normSqVec, GaussRat.normSq]
  · norm_num [dedekindRayCut, tomo_e3, gv, normSqVec, GaussRat.normSq]
  · norm_num [dedekindRayCut, gaussianHalvingBase, gaussianHalvingPos, tomo_e3, gv,
      normSqVec, GaussRat.normSq]

/-- For any `a b : GaussRat` and any rational `0 < θ ≤ 1`, if `(a - b).normSq ≤ θ ^ 2`, then
`|a.normSq - b.normSq| ≤ (2 * b.normSq + 2) * θ`. -/
theorem abs_normSq_sub_le_of_normSq_sub_le {a b : GaussRat} {θ : ℚ}
    (hθ_pos : 0 < θ) (hθ_le : θ ≤ 1) (hd : (a - b).normSq ≤ θ ^ 2) :
    |a.normSq - b.normSq| ≤ (2 * b.normSq + 2) * θ := by
  let d : GaussRat := a - b
  have hd_nn : 0 ≤ d.normSq := GaussRat.normSq_nonneg d
  have hb_nn : 0 ≤ b.normSq := GaussRat.normSq_nonneg b
  have hid : a.normSq - b.normSq = d.normSq + 2 * (b.re * d.re + b.im * d.im) := by
    simp only [d, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
    ring
  have htri : |a.normSq - b.normSq| ≤ |d.normSq| + |2 * (b.re * d.re + b.im * d.im)| := by
    rw [hid]
    exact abs_add_le _ _
  rw [abs_of_nonneg hd_nn] at htri
  have hw := mul_abs_two_re_inner_le_weighted θ (le_of_lt hθ_pos) b d
  have hθ2 : θ ^ 2 ≤ θ := by nlinarith
  have hd_le : d.normSq ≤ θ ^ 2 := hd
  nlinarith

/-- For any `v v₀ : GVec` and `0 < θ ≤ 1` with `distSqVec v v₀ < θ ^ 2`, both
`|normSqVec v - normSqVec v₀|` and `|v.y.normSq - v₀.y.normSq|` are at most
`(2 * normSqVec v₀ + 6) * θ`. -/
theorem abs_normSqVec_and_y_sub_le_of_distSqVec_lt {v v₀ : GVec} {θ : ℚ}
    (hθ_pos : 0 < θ) (hθ_le : θ ≤ 1) (hdist : distSqVec v v₀ < θ ^ 2) :
    |normSqVec v - normSqVec v₀| ≤ (2 * normSqVec v₀ + 6) * θ ∧
    |v.y.normSq - v₀.y.normSq| ≤ (2 * normSqVec v₀ + 6) * θ := by
  have hdx_nn : 0 ≤ (v.x - v₀.x).normSq := GaussRat.normSq_nonneg _
  have hdy_nn : 0 ≤ (v.y - v₀.y).normSq := GaussRat.normSq_nonneg _
  have hdz_nn : 0 ≤ (v.z - v₀.z).normSq := GaussRat.normSq_nonneg _
  have hdist_eq :
      distSqVec v v₀ = (v.x - v₀.x).normSq + (v.y - v₀.y).normSq + (v.z - v₀.z).normSq := rfl
  have hdx : (v.x - v₀.x).normSq ≤ θ ^ 2 := by linarith
  have hdy : (v.y - v₀.y).normSq ≤ θ ^ 2 := by linarith
  have hdz : (v.z - v₀.z).normSq ≤ θ ^ 2 := by linarith
  have hx := abs_normSq_sub_le_of_normSq_sub_le hθ_pos hθ_le hdx
  have hy := abs_normSq_sub_le_of_normSq_sub_le hθ_pos hθ_le hdy
  have hz := abs_normSq_sub_le_of_normSq_sub_le hθ_pos hθ_le hdz
  have hdiff :
      normSqVec v - normSqVec v₀ =
        (v.x.normSq - v₀.x.normSq) + (v.y.normSq - v₀.y.normSq) + (v.z.normSq - v₀.z.normSq) := by
    simp only [normSqVec]
    ring
  have htri1 := abs_add_le
    ((v.x.normSq - v₀.x.normSq) + (v.y.normSq - v₀.y.normSq))
    (v.z.normSq - v₀.z.normSq)
  have htri2 := abs_add_le (v.x.normSq - v₀.x.normSq) (v.y.normSq - v₀.y.normSq)
  have hv₀x_nn : 0 ≤ v₀.x.normSq := GaussRat.normSq_nonneg _
  have hv₀z_nn : 0 ≤ v₀.z.normSq := GaussRat.normSq_nonneg _
  have hnorm_sum : v₀.x.normSq + v₀.y.normSq + v₀.z.normSq = normSqVec v₀ := rfl
  refine ⟨by rw [hdiff]; nlinarith, by nlinarith⟩

/-- For nonnegative rationals `a, b ≥ 0` and `0 ≤ η ≤ 1`, `|a - b| ≤ η` implies
`|a ^ 2 - b ^ 2| ≤ (2 * b + 1) * η`. -/
theorem abs_sq_sub_sq_le_of_abs_sub_le {a b η : ℚ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hη_nn : 0 ≤ η) (hη_le : η ≤ 1) (hab : |a - b| ≤ η) :
    |a ^ 2 - b ^ 2| ≤ (2 * b + 1) * η := by
  obtain ⟨hl, hu⟩ := abs_le.mp hab
  have hsum_nn : 0 ≤ a + b := by linarith
  have hsum_le : a + b ≤ 2 * b + 1 := by linarith
  have hfac : a ^ 2 - b ^ 2 = (a - b) * (a + b) := by ring
  rw [hfac]
  exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩

/-- **Local Constancy of `dedekindRayCut` at Every Nonzero Vector (`dedekindRayCut_eventually_const`)**:
for every nonzero vector `v₀ ∈ ℚ(i)³ \ {0}`, the irrational cone `3 |u.y|⁴ = ‖u‖⁴` has a strictly
positive rational gap `|3 (v₀.y.normSq)² - (normSqVec v₀)²| > 0`, so there exists a rational radius
`δ > 0` on which `dedekindRayCut v = dedekindRayCut v₀` whenever `distSqVec v v₀ < δ`. -/
theorem dedekindRayCut_eventually_const {v₀ : GVec} (hv₀ : v₀.NonZero) :
    ∃ δ : ℚ, 0 < δ ∧ ∀ v : GVec, distSqVec v v₀ < δ → dedekindRayCut v = dedekindRayCut v₀ := by
  let P : GVec → ℚ := fun u => 3 * (u.y.normSq) ^ 2 - (normSqVec u) ^ 2
  have hP_ne : P v₀ ≠ 0 := sub_ne_zero.mpr (dedekindRayCut_gap_ne_zero hv₀)
  let gap : ℚ := |P v₀|
  have hgap_pos : 0 < gap := abs_pos.mpr hP_ne
  have hnv₀_pos : 0 < normSqVec v₀ := normSqVec_pos_of_nonZero hv₀
  have hnv₀_nn : 0 ≤ normSqVec v₀ := le_of_lt hnv₀_pos
  let C : ℚ := 4 * (2 * normSqVec v₀ + 1) + 1
  have hC_pos : 0 < C := by dsimp [C]; linarith
  let η : ℚ := min 1 (gap / C)
  have hη_pos : 0 < η := lt_min one_pos (div_pos hgap_pos hC_pos)
  have hη_nn : 0 ≤ η := le_of_lt hη_pos
  have hη_le_one : η ≤ 1 := min_le_left _ _
  have hη_le_div : η ≤ gap / C := min_le_right _ _
  have hC_η_le : C * η ≤ gap := by
    have h1 := (le_div_iff₀ hC_pos).mp hη_le_div
    linarith
  have h4_η_lt : 4 * (2 * normSqVec v₀ + 1) * η < gap := by
    have : 4 * (2 * normSqVec v₀ + 1) * η + η = C * η := by dsimp [C]; ring
    linarith
  let M : ℚ := 2 * normSqVec v₀ + 6
  have hM_pos : 0 < M := by dsimp [M]; linarith
  have hM_ne : M ≠ 0 := ne_of_gt hM_pos
  let θ : ℚ := η / M
  have hθ_pos : 0 < θ := div_pos hη_pos hM_pos
  have hθ_le_one : θ ≤ 1 := by
    have hη_le_M : η ≤ M := by dsimp [M]; linarith
    exact (div_le_one hM_pos).mpr hη_le_M
  have hM_θ : M * θ = η := mul_div_cancel₀ η hM_ne
  refine ⟨θ ^ 2, sq_pos_of_pos hθ_pos, ?_⟩
  intro v hdist
  obtain ⟨hn_diff, hy_diff⟩ := abs_normSqVec_and_y_sub_le_of_distSqVec_lt hθ_pos hθ_le_one hdist
  change |normSqVec v - normSqVec v₀| ≤ M * θ at hn_diff
  change |v.y.normSq - v₀.y.normSq| ≤ M * θ at hy_diff
  rw [hM_θ] at hn_diff hy_diff
  have hnv_nn : 0 ≤ normSqVec v := normSqVec_nonneg v
  have hvy_nn : 0 ≤ v.y.normSq := GaussRat.normSq_nonneg v.y
  have hv₀y_nn : 0 ≤ v₀.y.normSq := GaussRat.normSq_nonneg v₀.y
  have hv₀y_le_n : v₀.y.normSq ≤ normSqVec v₀ := by
    have hx_nn := GaussRat.normSq_nonneg v₀.x
    have hz_nn := GaussRat.normSq_nonneg v₀.z
    unfold normSqVec
    linarith
  have hn_sq := abs_sq_sub_sq_le_of_abs_sub_le hnv_nn hnv₀_nn hη_nn hη_le_one hn_diff
  have hy_sq := abs_sq_sub_sq_le_of_abs_sub_le hvy_nn hv₀y_nn hη_nn hη_le_one hy_diff
  have hy_sq' : |(v.y.normSq) ^ 2 - (v₀.y.normSq) ^ 2| ≤ (2 * normSqVec v₀ + 1) * η := by
    nlinarith
  have hP_diff_eq :
      P v - P v₀ =
        3 * ((v.y.normSq) ^ 2 - (v₀.y.normSq) ^ 2) + (-((normSqVec v) ^ 2 - (normSqVec v₀) ^ 2)) := by
    dsimp [P]
    ring
  have htriP := abs_add_le
    (3 * ((v.y.normSq) ^ 2 - (v₀.y.normSq) ^ 2))
    (-((normSqVec v) ^ 2 - (normSqVec v₀) ^ 2))
  rw [abs_neg, abs_mul, abs_of_pos (by norm_num : (0 : ℚ) < 3)] at htriP
  have hP_lt_gap : |P v - P v₀| < gap := by
    rw [hP_diff_eq]
    linarith
  obtain ⟨hP_lo, hP_hi⟩ := abs_lt.mp hP_lt_gap
  unfold dedekindRayCut
  by_cases hlt₀ : (normSqVec v₀) ^ 2 < 3 * (v₀.y.normSq) ^ 2
  · have hP₀_pos : 0 < P v₀ := by dsimp [P]; linarith
    have hgap_eq : gap = P v₀ := abs_of_pos hP₀_pos
    have hlt_v : (normSqVec v) ^ 2 < 3 * (v.y.normSq) ^ 2 := by
      dsimp [P] at hP_lo hgap_eq
      linarith
    simp [hlt₀, hlt_v]
  · have hP₀_neg : P v₀ < 0 := by
      rcases lt_trichotomy (P v₀) 0 with hneg | hzero | hpos
      · exact hneg
      · exact absurd hzero hP_ne
      · dsimp [P] at hpos; exact absurd (by linarith) hlt₀
    have hgap_eq : gap = -P v₀ := abs_of_neg hP₀_neg
    have hnot_v : ¬ ((normSqVec v) ^ 2 < 3 * (v.y.normSq) ^ 2) := by
      dsimp [P] at hP_hi hgap_eq
      linarith
    simp [hlt₀, hnot_v]

/-- **Global Vector-Level Archimedean Continuity of `dedekindRayCut` on `ℚ(i)³ \ {0}`
(`dedekindRayCut_isArchimedeanContinuousEverywhere`)**:
because the irrational cone `3 |u.y|⁴ = ‖u‖⁴` misses `ℚ(i)³ \ {0}` entirely, `dedekindRayCut` is
locally constant—and therefore Archimedean-continuous—at **every** nonzero vector `v₀ ∈ ℚ(i)³ \ {0}`. -/
theorem dedekindRayCut_isArchimedeanContinuousEverywhere :
    IsArchimedeanContinuousEverywhere dedekindRayCut := by
  intro v₀ hv₀ ε hε
  obtain ⟨δ, hδ, hconst⟩ := dedekindRayCut_eventually_const hv₀
  refine ⟨δ, hδ, ?_⟩
  intro v _hv hdist
  rw [hconst v hdist, sub_self, abs_zero]
  exact hε

/-- **Global Pointwise Ray Continuity of `dedekindRayCut` on `ℚ(i)³ \ {0}`
(`dedekindRayCut_isPointwiseRayContinuous`)**:
`dedekindRayCut` is pointwise ray-continuous (`IsPointwiseRayContinuous`) at **every** nonzero ray
of `ℚ(i)³`, while failing both uniform ray continuity (`dedekindRayCut_jump_on_pell_pair`) and
3-frame additivity (`dedekindRayCut_not_isFrameFunction`). -/
theorem dedekindRayCut_isPointwiseRayContinuous :
    IsPointwiseRayContinuous dedekindRayCut :=
  (isPointwiseRayContinuous_iff_isArchimedeanContinuousEverywhere
    dedekindRayCut_isScaleInvariantOnRays).mpr
    dedekindRayCut_isArchimedeanContinuousEverywhere

/-- For any vectors `u, w : GVec`, the rank-1 projector Rayleigh quotient `quadRay (rayProj w) u`
equals `1 - raySinSq u w`. -/
theorem quadRay_rayProj_eq_one_sub_raySinSq (u w : GVec) :
    quadRay (rayProj w) u = 1 - raySinSq u w := by
  simp only [quadRay, quadNum, rayProj, raySinSq, GVec.inner,
    GaussRat.normSq, re_add, im_add, re_mul, im_mul, re_star, im_star]
  ring

/-- For every nonzero anchor `w ∈ ℚ(i)³ \ {0}`, `quadRay (rayProj w)` is a nonnegative frame
function on `ℚ(i)³`. -/
theorem quadRay_rayProj_isNonnegFrameFunction {w : GVec} (hw : w.NonZero) :
    IsNonnegFrameFunction (quadRay (rayProj w)) := by
  refine ⟨quadRay_isFrameFunction (rayProj w) (rayProj_tr hw), ?_⟩
  intro u _hu
  rw [quadRay_rayProj_eq_one_sub_raySinSq u w]
  unfold raySinSq
  have h1 :
      1 - (1 - (GVec.inner u w).normSq / (normSqVec u * normSqVec w)) =
        (GVec.inner u w).normSq / (normSqVec u * normSqVec w) := by ring
  rw [h1]
  exact div_nonneg (GaussRat.normSq_nonneg _)
    (mul_nonneg (normSqVec_nonneg u) (normSqVec_nonneg w))

/-- **General Orthogonal Ray-Distance Bessel Bound (`ortho_raySinSq_add_ge_one`)**:
for any two nonzero orthogonal vectors `u, v ∈ ℚ(i)³` (`GVec.inner u v = 0`) and any nonzero
anchor `w ∈ ℚ(i)³ \ {0}`, completing `(u, v)` with `hermCross u v` and applying
`rational_piron_subadditivity` to `quadRay (rayProj w) = 1 - raySinSq · w` yields
`1 ≤ raySinSq u w + raySinSq v w`. -/
theorem ortho_raySinSq_add_ge_one {u v w : GVec}
    (hu : u.NonZero) (hv : v.NonZero) (hw : w.NonZero) (huv : GVec.inner u v = 0) :
    1 ≤ raySinSq u w + raySinSq v w := by
  have hsub :=
    (rational_piron_subadditivity (quadRay_rayProj_isNonnegFrameFunction hw) hu hv huv).2
  rw [quadRay_rayProj_eq_one_sub_raySinSq u w,
      quadRay_rayProj_eq_one_sub_raySinSq v w] at hsub
  linarith

/-- **General Orthogonal Polar-Cap Disjointness (`not_both_raySinSq_lt_half_of_ortho`)**:
for any nonzero anchor `w ∈ ℚ(i)³ \ {0}`, no two nonzero orthogonal vectors `u, v ∈ ℚ(i)³`
(`GVec.inner u v = 0`) can simultaneously lie inside the polar cap `raySinSq · w < 1 / 2`. -/
theorem not_both_raySinSq_lt_half_of_ortho {u v w : GVec}
    (hu : u.NonZero) (hv : v.NonZero) (hw : w.NonZero) (huv : GVec.inner u v = 0) :
    ¬ (raySinSq u w < 1 / 2 ∧ raySinSq v w < 1 / 2) := by
  rintro ⟨hu_lt, hv_lt⟩
  have hge := ortho_raySinSq_add_ge_one hu hv hw huv
  linarith

/-- **Global Vanishing of Zero-Weight Residuals Supported in a `< 45°` Polar Cap
(`zero_of_zeroWeight_supported_in_polar_cap`)**:
if `g : GVec → ℚ` is a zero-weight frame function on `ℚ(i)³` supported inside the `< 45°` polar cap
`raySinSq · w < 1 / 2` around any nonzero ray `w ∈ ℚ(i)³ \ {0}` (meaning `g u = 0` whenever
`u.NonZero` and `1 / 2 ≤ raySinSq u w`), then `g x = 0` for every nonzero `x ∈ ℚ(i)³ \ {0}`:
any ray `x` inside the cap completes to an orthogonal frame `(x, u, v)`, both orthogonal partners
`u, v` are forced outside the cap by `not_both_raySinSq_lt_half_of_ortho`, and `g x + g u + g v = 0`
forces `g x = 0`. -/
theorem zero_of_zeroWeight_supported_in_polar_cap {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) {w : GVec} (hw : w.NonZero)
    (hcap : ∀ u : GVec, u.NonZero → 1 / 2 ≤ raySinSq u w → g u = 0)
    {x : GVec} (hx : x.NonZero) :
    g x = 0 := by
  by_cases hx_cap : 1 / 2 ≤ raySinSq x w
  · exact hcap x hx hx_cap
  · push_neg at hx_cap
    obtain ⟨u, v, hfr, _⟩ := exists_frame_completion hx
    have hu : u.NonZero := hfr.2.1
    have hv : v.NonZero := hfr.2.2.1
    have hxu : GVec.inner x u = 0 := hfr.2.2.2.1
    have hxv : GVec.inner x v = 0 := hfr.2.2.2.2.1
    have hu_out : 1 / 2 ≤ raySinSq u w := by
      by_contra hu_in
      push_neg at hu_in
      exact not_both_raySinSq_lt_half_of_ortho hx hu hw hxu ⟨hx_cap, hu_in⟩
    have hv_out : 1 / 2 ≤ raySinSq v w := by
      by_contra hv_in
      push_neg at hv_in
      exact not_both_raySinSq_lt_half_of_ortho hx hv hw hxv ⟨hx_cap, hv_in⟩
    have hgu : g u = 0 := hcap u hu hu_out
    have hgv : g v = 0 := hcap v hv hv_out
    have hsum := hg x u v hfr
    linarith

/-- For every vector `u : GVec`, the pure-pole Rayleigh quotient `quadRay (rayProj tomo_e1) u`
equals `1 - raySinSq u tomo_e1`. -/
theorem quadRay_rayProj_tomo_e1_eq_one_sub_raySinSq (u : GVec) :
    quadRay (rayProj tomo_e1) u = 1 - raySinSq u tomo_e1 :=
  quadRay_rayProj_eq_one_sub_raySinSq u tomo_e1

/-- **Orthogonal Ray-Distance Bessel Bound Relative to `tomo_e1`
(`ortho_raySinSq_tomo_e1_add_ge_one`)**:
for any two nonzero orthogonal vectors `u, v ∈ ℚ(i)³` (`GVec.inner u v = 0`),
`1 ≤ raySinSq u tomo_e1 + raySinSq v tomo_e1`. -/
theorem ortho_raySinSq_tomo_e1_add_ge_one {u v : GVec}
    (hu : u.NonZero) (hv : v.NonZero) (huv : GVec.inner u v = 0) :
    1 ≤ raySinSq u tomo_e1 + raySinSq v tomo_e1 :=
  ortho_raySinSq_add_ge_one hu hv tomo_e1_nonZero huv

/-- **Orthogonal Polar-Cap Disjointness (`not_both_raySinSq_tomo_e1_lt_half_of_ortho`)**:
no two nonzero orthogonal vectors `u, v ∈ ℚ(i)³` (`GVec.inner u v = 0`) can simultaneously lie
inside the polar cap `raySinSq · tomo_e1 < 1 / 2`. -/
theorem not_both_raySinSq_tomo_e1_lt_half_of_ortho {u v : GVec}
    (hu : u.NonZero) (hv : v.NonZero) (huv : GVec.inner u v = 0) :
    ¬ (raySinSq u tomo_e1 < 1 / 2 ∧ raySinSq v tomo_e1 < 1 / 2) :=
  not_both_raySinSq_lt_half_of_ortho hu hv tomo_e1_nonZero huv

/-! #### 7C. Target 1 (`TFQ-1057`): General-Anchor Meridian Coupling, Fixed-Anchor Isolation Obstruction, and Conditional Closures -/

/-- **General-Anchor Meridian Step (`anchorMeridianStep`)**:
for any anchor `a ∈ ℚ(i)³` and orthogonal tangent vector `y ∈ a⊥`, the meridian step is `a + y`. -/
def anchorMeridianStep (a y : GVec) : GVec :=
  GVec.add a y

/-- **General-Anchor Meridian Orthogonal Partner (`anchorMeridianOrtho`)**:
for any anchor `a ∈ ℚ(i)³` and orthogonal vector `y ∈ a⊥`, the planar orthogonal partner of `a + y`
in `span(a, y)` is `-‖y‖² a + ‖a‖² y`. -/
def anchorMeridianOrtho (a y : GVec) : GVec :=
  GVec.add (GVec.smul ⟨-normSqVec y, 0⟩ a) (GVec.smul ⟨normSqVec a, 0⟩ y)

/-- **General-Anchor Kelvin Equatorial Partner (`anchorKelvinEq`)**:
for any anchor `a ∈ ℚ(i)³` and nonzero `y ∈ a⊥`, `anchorKelvinEq a y = -(‖a‖² / ‖y‖²) y` satisfies
`-(1 / ‖y‖²) • anchorMeridianOrtho a y = a + anchorKelvinEq a y`. -/
def anchorKelvinEq (a y : GVec) : GVec :=
  GVec.smul ⟨-(normSqVec a / normSqVec y), 0⟩ y

theorem add_eq_rotPairU (a y : GVec) :
    GVec.add a y = rotPairU a y 1 1 := by
  ext <;> simp [rotPairU, GVec.add, GVec.smul]

theorem anchorMeridianStep_eq_rotPairU (a y : GVec) :
    anchorMeridianStep a y = rotPairU a y 1 1 :=
  add_eq_rotPairU a y

theorem anchorMeridianOrtho_eq_rotPairV (a y : GVec) :
    anchorMeridianOrtho a y = rotPairV a y 1 1 := by
  ext <;> simp [anchorMeridianOrtho, rotPairV, GVec.add, GVec.smul]

theorem anchorMeridianOrtho_tomo_e1 (y : GVec) :
    anchorMeridianOrtho tomo_e1 y = meridianOrtho y := by
  have he1 : normSqVec tomo_e1 = 1 := by
    simp [normSqVec, GaussRat.normSq, tomo_e1, gv]
  ext <;> simp [anchorMeridianOrtho, meridianOrtho, he1, GVec.add, GVec.smul]

theorem smul_anchorMeridianOrtho_eq_add_anchorKelvinEq {a y : GVec} (hy : y.NonZero) :
    GVec.smul ⟨-(1 / normSqVec y), 0⟩ (anchorMeridianOrtho a y) =
      GVec.add a (anchorKelvinEq a y) := by
  have hy_ne : normSqVec y ≠ 0 := normSqVec_ne_zero_of_nonZero hy
  ext <;>
    simp only [anchorMeridianOrtho, anchorKelvinEq, GVec.add, GVec.smul,
      GaussRat.re_add, GaussRat.im_add, GaussRat.re_mul, GaussRat.im_mul] <;>
    field_simp [hy_ne] <;>
    ring

/-- For any anchor `a` and any `y` orthogonal to `a` (`GVec.inner a y = 0`), the meridian step
`a + y` and the meridian partner `anchorMeridianOrtho a y` are orthogonal. -/
theorem inner_anchorMeridianStep_anchorMeridianOrtho (a y : GVec) (hay : GVec.inner a y = 0) :
    GVec.inner (GVec.add a y) (anchorMeridianOrtho a y) = 0 := by
  rw [add_eq_rotPairU a y, anchorMeridianOrtho_eq_rotPairV a y]
  exact inner_rotPairU_rotPairV_eq_zero hay 1 1

/-- If `a` is nonzero and `GVec.inner a y = 0`, then `a + y` is nonzero. -/
theorem addVec_a_y_ne_zero_of_ortho (a y : GVec) (ha : a.NonZero) (hay : GVec.inner a y = 0) :
    (GVec.add a y).NonZero := by
  have ha_pos := normSqVec_pos_of_nonZero ha
  have hy_nn := normSqVec_nonneg y
  have hnorm : normSqVec (GVec.add a y) = normSqVec a + normSqVec y :=
    (normSqVec_add_eq_normSqVec_sub_of_ortho hay).1
  apply nonZero_of_normSqVec_pos
  linarith

/-- If `a` and `y` are nonzero and `GVec.inner a y = 0`, then `anchorMeridianOrtho a y` is nonzero. -/
theorem anchorMeridianOrtho_ne_zero_of_ortho (a y : GVec)
    (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    (anchorMeridianOrtho a y).NonZero := by
  rw [anchorMeridianOrtho_eq_rotPairV a y]
  exact (isFrame_rotPair (isFrame_hermCross ha hy hay) (Or.inl one_ne_zero)).2.1

/-- For any nonzero orthogonal pair `(a, y)` in `ℚ(i)³`, `(a, y, hermCross a y)` is an orthogonal
3-frame. -/
theorem isFrame_anchor_meridian_base (a y : GVec)
    (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    IsFrame a y (hermCross a y) :=
  isFrame_hermCross ha hy hay

/-- For any nonzero orthogonal pair `(a, y)` in `ℚ(i)³`, rotating `(a, y)` inside `span(a, y)` yields
the meridian orthogonal 3-frame `(a + y, anchorMeridianOrtho a y, hermCross a y)` sharing the third
axis `hermCross a y`. -/
theorem isFrame_anchor_meridian_rot (a y : GVec)
    (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    IsFrame (GVec.add a y) (anchorMeridianOrtho a y) (hermCross a y) := by
  rw [add_eq_rotPairU a y, anchorMeridianOrtho_eq_rotPairV a y]
  exact isFrame_rotPair (isFrame_hermCross ha hy hay) (Or.inl one_ne_zero)

/-- **General-Anchor Two-Frame Meridian–Kelvin Bridge (`anchor_meridian_kelvin_bridge`)**:
for every frame function `f` on `ℚ(i)³`, every nonzero anchor `a`, and every nonzero `y ∈ a⊥`,
comparing `(a, y, hermCross a y)` and `(a + y, anchorMeridianOrtho a y, hermCross a y)` cancels
`f (hermCross a y)` and yields:
1. `f (a + y) + f (anchorMeridianOrtho a y) = f a + f y`,
2. `f (a + y) + f (a + anchorKelvinEq a y) = f a + f y`,
3. `f (a + y) - f a = f y - f (anchorMeridianOrtho a y)`,
4. `|f y - f (anchorMeridianOrtho a y)| = |f (a + y) - f a|`. -/
theorem anchor_meridian_kelvin_bridge {f : GVec → ℚ} (hf : IsFrameFunction f)
    {a y : GVec} (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    f (GVec.add a y) + f (anchorMeridianOrtho a y) = f a + f y ∧
    f (GVec.add a y) + f (GVec.add a (anchorKelvinEq a y)) = f a + f y ∧
    f (GVec.add a y) - f a = f y - f (anchorMeridianOrtho a y) ∧
    |f y - f (anchorMeridianOrtho a y)| = |f (GVec.add a y) - f a| := by
  have hsum : f (GVec.add a y) + f (anchorMeridianOrtho a y) = f a + f y := by
    rw [add_eq_rotPairU a y, anchorMeridianOrtho_eq_rotPairV a y]
    exact frameFunction_rotPair_sum hf (isFrame_hermCross ha hy hay) (Or.inl one_ne_zero)
  have hm_nz : (anchorMeridianOrtho a y).NonZero :=
    anchorMeridianOrtho_ne_zero_of_ortho a y ha hy hay
  have hy_pos := normSqVec_pos_of_nonZero hy
  have hl_ne : (⟨-(1 / normSqVec y), 0⟩ : GaussRat) ≠ 0 := by
    intro h
    have hre := congrArg GaussRat.re h
    dsimp at hre
    have hpos : 0 < 1 / normSqVec y := div_pos one_pos hy_pos
    linarith
  have hsmul_kelvin := GaussianTomography.frameFunction_smul hf hm_nz hl_ne
  rw [smul_anchorMeridianOrtho_eq_add_anchorKelvinEq hy] at hsmul_kelvin
  have hdiff : f (GVec.add a y) - f a = f y - f (anchorMeridianOrtho a y) := by linarith
  exact ⟨hsum, by linarith, hdiff, by rw [hdiff]⟩

/-- **General-Anchor Zero-Weight Meridian Bridge (`anchor_meridian_zeroWeight_bridge`)**:
for every zero-weight frame residual `g` on `ℚ(i)³`, every nonzero anchor `a`, and every nonzero
`y ∈ a⊥`,
1. `g (a + y) + g (anchorMeridianOrtho a y) = g a + g y`,
2. `g (a + y) - g a = g y - g (anchorMeridianOrtho a y)`,
3. `|g y - g (anchorMeridianOrtho a y)| = |g (a + y) - g a|`. -/
theorem anchor_meridian_zeroWeight_bridge {g : GVec → ℚ} (hg : IsZeroWeightFrameFunction g)
    {a y : GVec} (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    g (GVec.add a y) + g (anchorMeridianOrtho a y) = g a + g y ∧
    g (GVec.add a y) - g a = g y - g (anchorMeridianOrtho a y) ∧
    |g y - g (anchorMeridianOrtho a y)| = |g (GVec.add a y) - g a| := by
  have hsum : g (GVec.add a y) + g (anchorMeridianOrtho a y) = g a + g y := by
    rw [add_eq_rotPairU a y, anchorMeridianOrtho_eq_rotPairV a y]
    exact zeroWeight_rotPair_sum hg (isFrame_hermCross ha hy hay) (Or.inl one_ne_zero)
  have hdiff : g (GVec.add a y) - g a = g y - g (anchorMeridianOrtho a y) := by linarith
  exact ⟨hsum, hdiff, by rw [hdiff]⟩

/-- **General-Anchor Polar–Equatorial Projective Ray-Distance Duality
(`anchorMeridianOrtho_raySinSq_eq`)**:
for every nonzero anchor `a ∈ ℚ(i)³` and every nonzero `y ∈ a⊥`, both `raySinSq (a + y) a` and
`raySinSq (anchorMeridianOrtho a y) y` equal `normSqVec y / (normSqVec a + normSqVec y)`. -/
theorem anchorMeridianOrtho_raySinSq_eq {a y : GVec}
    (ha : a.NonZero) (hy : y.NonZero) (hay : GVec.inner a y = 0) :
    raySinSq (GVec.add a y) a = normSqVec y / (normSqVec a + normSqVec y) ∧
    raySinSq (anchorMeridianOrtho a y) y = normSqVec y / (normSqVec a + normSqVec y) := by
  have ha_pos := normSqVec_pos_of_nonZero ha
  have ha_ne : normSqVec a ≠ 0 := ne_of_gt ha_pos
  have hy_pos := normSqVec_pos_of_nonZero hy
  have hy_ne : normSqVec y ≠ 0 := ne_of_gt hy_pos
  have hsum_pos : 0 < normSqVec a + normSqVec y := add_pos ha_pos hy_pos
  have hsum_ne : normSqVec a + normSqVec y ≠ 0 := ne_of_gt hsum_pos
  have hya : GVec.inner y a = 0 := inner_eq_zero_symm hay
  have hay_norm : normSqVec (GVec.add a y) = normSqVec a + normSqVec y :=
    (normSqVec_add_eq_normSqVec_sub_of_ortho hay).1
  have hay_inner : (GVec.inner (GVec.add a y) a).normSq = (normSqVec a) ^ 2 := by
    rw [inner_add_left, hya, add_zero, inner_self_eq_normSqVec a]
    simp only [GaussRat.normSq]
    ring
  have hmer_norm :
      normSqVec (anchorMeridianOrtho a y) =
        normSqVec a * normSqVec y * (normSqVec a + normSqVec y) := by
    rw [anchorMeridianOrtho_eq_rotPairV a y,
        normSqVec_rotPairV hay 1 1,
        ← add_eq_rotPairU a y,
        hay_norm]
  have h_ortho_mer : GVec.inner (GVec.smul ⟨-normSqVec y, 0⟩ a) y = 0 := by
    rw [inner_smul_left, hay, mul_zero]
  have hmer_inner :
      (GVec.inner (anchorMeridianOrtho a y) y).normSq =
        (normSqVec a) ^ 2 * (normSqVec y) ^ 2 := by
    rw [anchorMeridianOrtho, inner_add_left, h_ortho_mer, zero_add,
        inner_smul_left, inner_self_eq_normSqVec y]
    simp only [GaussRat.normSq, GaussRat.re_mul, GaussRat.im_mul,
      GaussRat.re_star, GaussRat.im_star]
    ring
  refine ⟨?_, ?_⟩
  · unfold raySinSq
    rw [hay_inner, hay_norm]
    field_simp
    ring
  · unfold raySinSq
    rw [hmer_inner, hmer_norm]
    field_simp
    ring

/-- **Uniform Equatorial Meridian Continuity from Single-Anchor Pointwise Continuity
(`anchor_uniform_equatorial_continuity_of_anchor_continuous`)**:
if `f` is a frame function on `ℚ(i)³` that is pointwise ray-continuous at a nonzero anchor `a`,
then for every `ε > 0` there exists `δ > 0` (the pointwise modulus at `a`) such that for all
nonzero `y ∈ a⊥` with `normSqVec y / (normSqVec a + normSqVec y) < δ`, both
`|f y - f (anchorMeridianOrtho a y)| < ε` and `|f (a + y) - f a| < ε`. -/
theorem anchor_uniform_equatorial_continuity_of_anchor_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f) {a : GVec} (ha : a.NonZero)
    (hcont : IsPointwiseRayContinuousAt f a) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ y : GVec, y.NonZero → GVec.inner a y = 0 →
        normSqVec y / (normSqVec a + normSqVec y) < δ →
          |f y - f (anchorMeridianOrtho a y)| < ε ∧
          |f (GVec.add a y) - f a| < ε := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := hcont ε hε
  refine ⟨δ, hδ, ?_⟩
  intro y hy hay hquo
  have hay_nz : (GVec.add a y).NonZero := addVec_a_y_ne_zero_of_ortho a y ha hay
  have hsin_eq := anchorMeridianOrtho_raySinSq_eq ha hy hay
  have hsin_a : raySinSq (GVec.add a y) a < δ := by
    rw [hsin_eq.1]
    exact hquo
  have h_lt := hb (GVec.add a y) hay_nz hsin_a
  have hbridge := (anchor_meridian_kelvin_bridge hf ha hy hay).2.2.2
  exact ⟨by rw [hbridge]; exact h_lt, h_lt⟩

/-- **Shared Pointwise Modulus Across Any Finite Anchor List
(`finite_anchors_pointwiseRayContinuous_common_delta`)**:
if `g : GVec → ℚ` is pointwise ray-continuous at every anchor `a` in a finite list `anchors`, then
for every `ε > 0` there exists a single shared modulus `δ > 0` working simultaneously across all
`a ∈ anchors`. -/
theorem finite_anchors_pointwiseRayContinuous_common_delta {g : GVec → ℚ}
    (anchors : List GVec) (hcont : ∀ a ∈ anchors, IsPointwiseRayContinuousAt g a) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ a ∈ anchors, ∀ v : GVec, v.NonZero → raySinSq v a < δ → |g v - g a| < ε := by
  intro ε hε
  induction anchors with
  | nil =>
    exact ⟨1, one_pos, fun a ha => False.elim (List.not_mem_nil ha)⟩
  | cons a as ih =>
    obtain ⟨δ₁, hδ₁, hb₁⟩ := hcont a (List.mem_cons.mpr (Or.inl rfl)) ε hε
    obtain ⟨δ₂, hδ₂, hb₂⟩ := ih (fun b hb => hcont b (List.mem_cons.mpr (Or.inr hb)))
    refine ⟨min δ₁ δ₂, lt_min hδ₁ hδ₂, ?_⟩
    intro b hb v hv hsin
    simp only [List.mem_cons] at hb
    rcases hb with rfl | hmem
    · exact hb₁ v hv (lt_of_lt_of_le hsin (min_le_left δ₁ δ₂))
    · exact hb₂ b hmem v hv (lt_of_lt_of_le hsin (min_le_right δ₁ δ₂))

/-- **Multi-Anchor Uniform Equatorial Meridian Continuity Across Any Finite Anchor List
(`finite_anchors_uniform_equatorial_continuity_of_anchors_continuous`)**:
if `f` is a frame function on `ℚ(i)³` and `anchors : List GVec` is any finite list of nonzero
anchors at each of which `f` is pointwise ray-continuous, then for every `ε > 0` there exists a
single shared modulus `δ > 0` governing meridian steps on every equator `a⊥` (`a ∈ anchors`). -/
theorem finite_anchors_uniform_equatorial_continuity_of_anchors_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f) (anchors : List GVec)
    (hanz : ∀ a ∈ anchors, a.NonZero)
    (hcont : ∀ a ∈ anchors, IsPointwiseRayContinuousAt f a) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ a ∈ anchors, ∀ y : GVec, y.NonZero → GVec.inner a y = 0 →
        normSqVec y / (normSqVec a + normSqVec y) < δ →
          |f y - f (anchorMeridianOrtho a y)| < ε ∧
          |f (GVec.add a y) - f a| < ε := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := finite_anchors_pointwiseRayContinuous_common_delta anchors hcont ε hε
  refine ⟨δ, hδ, ?_⟩
  intro a ha_mem y hy hay hquo
  have ha : a.NonZero := hanz a ha_mem
  have hay_nz : (GVec.add a y).NonZero := addVec_a_y_ne_zero_of_ortho a y ha hay
  have hsin_eq := anchorMeridianOrtho_raySinSq_eq ha hy hay
  have hsin_a : raySinSq (GVec.add a y) a < δ := by
    rw [hsin_eq.1]
    exact hquo
  have h_lt := hb a ha_mem (GVec.add a y) hay_nz hsin_a
  have hbridge := (anchor_meridian_kelvin_bridge hf ha hy hay).2.2.2
  exact ⟨by rw [hbridge]; exact h_lt, h_lt⟩

/-- **Multi-Axis Uniform Equatorial Meridian Continuity Across `{tomo_e1, tomo_e2, tomo_e3}`
(`multi_axis_uniform_equatorial_continuity_of_axes_continuous`)**:
pointwise ray continuity of a frame function `f` at the three coordinate axes `tomo_e1`, `tomo_e2`,
`tomo_e3` yields a single shared modulus `δ > 0` simultaneously governing meridian steps on all
three coordinate equators `e₁⊥`, `e₂⊥`, `e₃⊥`. -/
theorem multi_axis_uniform_equatorial_continuity_of_axes_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f)
    (h1 : IsPointwiseRayContinuousAt f tomo_e1)
    (h2 : IsPointwiseRayContinuousAt f tomo_e2)
    (h3 : IsPointwiseRayContinuousAt f tomo_e3) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ a ∈ [tomo_e1, tomo_e2, tomo_e3], ∀ y : GVec, y.NonZero → GVec.inner a y = 0 →
        normSqVec y / (normSqVec a + normSqVec y) < δ →
          |f y - f (anchorMeridianOrtho a y)| < ε ∧
          |f (GVec.add a y) - f a| < ε := by
  apply finite_anchors_uniform_equatorial_continuity_of_anchors_continuous hf [tomo_e1, tomo_e2, tomo_e3]
  · intro a ha
    simp only [List.mem_cons, List.not_mem_nil, or_false] at ha
    rcases ha with rfl | rfl | rfl
    · exact tomo_e1_nonZero
    · exact tomo_e2_nonZero
    · exact tomo_e3_nonZero
  · intro a ha
    simp only [List.mem_cons, List.not_mem_nil, or_false] at ha
    rcases ha with rfl | rfl | rfl
    · exact h1
    · exact h2
    · exact h3

/-- **Nine-Anchor Uniform Equatorial Meridian Continuity Across `nineAnchorsList`
(`nine_anchor_uniform_equatorial_continuity_of_anchors_continuous`)**:
pointwise ray continuity of a frame function `f` at the 9 tomography anchors yields a single shared
modulus `δ > 0` simultaneously governing meridian steps on all 9 anchor equators `a⊥`
(`a ∈ nineAnchorsList`). -/
theorem nine_anchor_uniform_equatorial_continuity_of_anchors_continuous {f : GVec → ℚ}
    (hf : IsFrameFunction f)
    (hcont : ∀ a ∈ nineAnchorsList, IsPointwiseRayContinuousAt f a) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ a ∈ nineAnchorsList, ∀ y : GVec, y.NonZero → GVec.inner a y = 0 →
        normSqVec y / (normSqVec a + normSqVec y) < δ →
          |f y - f (anchorMeridianOrtho a y)| < ε ∧
          |f (GVec.add a y) - f a| < ε :=
  finite_anchors_uniform_equatorial_continuity_of_anchors_continuous
    hf nineAnchorsList nineAnchorsList_nonZero hcont

/-- Symmetry of projective ray distance `raySinSq u v = raySinSq v u`. -/
theorem raySinSq_comm (u v : GVec) :
    raySinSq u v = raySinSq v u := by
  have h_inner : (GVec.inner u v).normSq = (GVec.inner v u).normSq := by
    simp only [GVec.inner, GaussRat.normSq, re_add, im_add, re_mul, im_mul, re_star, im_star]
    ring
  have h_mul : normSqVec u * normSqVec v = normSqVec v * normSqVec u :=
    mul_comm (normSqVec u) (normSqVec v)
  unfold raySinSq
  rw [h_inner, h_mul]

/-- Upper bound `raySinSq u w ≤ 1` for all `u, w : GVec`. -/
theorem raySinSq_le_one (u w : GVec) :
    raySinSq u w ≤ 1 := by
  unfold raySinSq
  have hnn : 0 ≤ (GVec.inner u w).normSq / (normSqVec u * normSqVec w) :=
    div_nonneg (GaussRat.normSq_nonneg _)
      (mul_nonneg (normSqVec_nonneg u) (normSqVec_nonneg w))
  linarith

/-- Nonnegativity `0 ≤ raySinSq u w` for nonzero `u, w : GVec`. -/
theorem raySinSq_nonneg {u w : GVec} (hu : u.NonZero) (hw : w.NonZero) :
    0 ≤ raySinSq u w := by
  rw [raySinSq_eq_normSqVec_cross_div hu hw]
  exact div_nonneg (normSqVec_nonneg (cross u w))
    (mul_nonneg (normSqVec_nonneg u) (normSqVec_nonneg w))

/-- **Exact Spherical 3-Frame Pythagoras Identity (`frame_raySinSq_sum_eq_two`)**:
for any orthogonal 3-frame `IsFrame u v w` and any nonzero ray `a ∈ ℚ(i)³ \ {0}`, evaluating the
Born rank-1 projector frame function `quadRay (rayProj a) = 1 - raySinSq · a` on `(u, v, w)` yields
`raySinSq u a + raySinSq v a + raySinSq w a = 2`. -/
theorem frame_raySinSq_sum_eq_two {u v w a : GVec}
    (hfr : IsFrame u v w) (ha : a.NonZero) :
    raySinSq u a + raySinSq v a + raySinSq w a = 2 := by
  have hsum := (quadRay_rayProj_isNonnegFrameFunction ha).1 u v w hfr
  rw [quadRay_rayProj_eq_one_sub_raySinSq u a,
      quadRay_rayProj_eq_one_sub_raySinSq v a,
      quadRay_rayProj_eq_one_sub_raySinSq w a] at hsum
  linarith

/-- **Symmetric Spherical Anchor-Frame Pythagoras Identity (`anchor_frame_raySinSq_sum_eq_two`)**:
for any orthogonal anchor 3-frame `IsFrame a₁ a₂ a₃` and any nonzero ray `x ∈ ℚ(i)³ \ {0}`,
`raySinSq x a₁ + raySinSq x a₂ + raySinSq x a₃ = 2`. -/
theorem anchor_frame_raySinSq_sum_eq_two {a₁ a₂ a₃ x : GVec}
    (ha : IsFrame a₁ a₂ a₃) (hx : x.NonZero) :
    raySinSq x a₁ + raySinSq x a₂ + raySinSq x a₃ = 2 := by
  rw [raySinSq_comm x a₁, raySinSq_comm x a₂, raySinSq_comm x a₃]
  exact frame_raySinSq_sum_eq_two ha hx

/-- **Two-Frame Cross-Anchor Proximity Bound (`frame_third_raySinSq_le_add_of_ortho_anchors`)**:
for any two orthogonal 3-frames `IsFrame u v w` and `IsFrame a₁ a₂ a₃` in `ℚ(i)³`, the projective
ray distance from `w` to `a₃` is bounded above by the sum of the projective ray distances from `u`
to `a₁` and from `v` to `a₂`:
`raySinSq w a₃ ≤ raySinSq u a₁ + raySinSq v a₂`. -/
theorem frame_third_raySinSq_le_add_of_ortho_anchors {u v w a₁ a₂ a₃ : GVec}
    (hfr : IsFrame u v w) (ha : IsFrame a₁ a₂ a₃) :
    raySinSq w a₃ ≤ raySinSq u a₁ + raySinSq v a₂ := by
  have hu : u.NonZero := hfr.1
  have hv : v.NonZero := hfr.2.1
  have hw : w.NonZero := hfr.2.2.1
  have huw : GVec.inner u w = 0 := hfr.2.2.2.2.1
  have hvw : GVec.inner v w = 0 := hfr.2.2.2.2.2
  have ha₁ : a₁.NonZero := ha.1
  have ha₂ : a₂.NonZero := ha.2.1
  have h1 := ortho_raySinSq_add_ge_one hu hw ha₁ huw
  have h2 := ortho_raySinSq_add_ge_one hv hw ha₂ hvw
  have hsum := anchor_frame_raySinSq_sum_eq_two ha hw
  linarith

/-- **Fixed-Anchor Frame Isolation Obstruction (`fixed_anchor_frame_isolation_obstruction`)**:
if `IsFrame u v w` is an orthogonal 3-frame, `IsFrame a₁ a₂ a₃` is an orthogonal anchor 3-frame,
and `w` lies at projective distance `η ≤ raySinSq w a₃` from `a₃`, then:
1. `η ≤ raySinSq u a₁ + raySinSq v a₂`, and
2. `u` and `v` cannot simultaneously lie within `< η / 2` of `a₁` and `a₂`. -/
theorem fixed_anchor_frame_isolation_obstruction {u v w a₁ a₂ a₃ : GVec} {η : ℚ}
    (hfr : IsFrame u v w) (ha : IsFrame a₁ a₂ a₃) (hη : η ≤ raySinSq w a₃) :
    η ≤ raySinSq u a₁ + raySinSq v a₂ ∧
    ¬ (raySinSq u a₁ < η / 2 ∧ raySinSq v a₂ < η / 2) := by
  have hle := le_trans hη (frame_third_raySinSq_le_add_of_ortho_anchors hfr ha)
  refine ⟨hle, ?_⟩
  rintro ⟨hu_lt, hv_lt⟩
  linarith

/-- Every anchor `a ∈ nineAnchorsList` lies at projective distance `raySinSq witness_111 a ≤ 2 / 3`
from `witness_111 = (1, 1, 1)` (specifically `2 / 3` for the 3 axes and 3 complex bisectors, and
`1 / 3` for the 3 real bisectors). -/
theorem witness111_raySinSq_nineAnchors_le_two_thirds :
    ∀ a ∈ nineAnchorsList, raySinSq witness_111 a ≤ 2 / 3 := by
  intro a ha
  simp only [nineAnchorsList, List.mem_cons, List.not_mem_nil, or_false] at ha
  rcases ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [witness_111, tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23,
      tomo_e12i, tomo_e13i, tomo_e23i, gv, GaussRat.I, raySinSq, normSqVec,
      GVec.inner, GaussRat.normSq]

/-- **Nine-Anchor Isolation of `witness_111⊥` (`ortho_witness111_raySinSq_nineAnchors_ge_one_third`)**:
every nonzero vector `u ∈ ℚ(i)³` orthogonal to `witness_111 = (1, 1, 1)` stays at projective ray
distance `1 / 3 ≤ raySinSq u a` from all 9 tomography anchors `a ∈ nineAnchorsList`. -/
theorem ortho_witness111_raySinSq_nineAnchors_ge_one_third {u : GVec}
    (hu : u.NonZero) (huw : GVec.inner u witness_111 = 0) :
    ∀ a ∈ nineAnchorsList, 1 / 3 ≤ raySinSq u a := by
  intro a ha_mem
  have ha_nz : a.NonZero := nineAnchorsList_nonZero a ha_mem
  have hge := ortho_raySinSq_add_ge_one hu witness_111_nonZero ha_nz huw
  have hle := witness111_raySinSq_nineAnchors_le_two_thirds a ha_mem
  linarith

/-- **Single-Frame Nine-Anchor Isolation for `witness_111`
(`frame_witness111_partners_isolated_from_nineAnchors`)**:
in any orthogonal 3-frame `IsFrame witness_111 u v` containing `witness_111 = (1, 1, 1)`, both
orthogonal partners `u` and `v` are bounded away from all 9 tomography anchors by
`1 / 3 ≤ raySinSq u a` and `1 / 3 ≤ raySinSq v a`. -/
theorem frame_witness111_partners_isolated_from_nineAnchors {u v : GVec}
    (hfr : IsFrame witness_111 u v) :
    (∀ a ∈ nineAnchorsList, 1 / 3 ≤ raySinSq u a) ∧
    (∀ a ∈ nineAnchorsList, 1 / 3 ≤ raySinSq v a) := by
  have hu : u.NonZero := hfr.2.1
  have hv : v.NonZero := hfr.2.2.1
  have huw : GVec.inner u witness_111 = 0 := inner_eq_zero_symm hfr.2.2.2.1
  have hvw : GVec.inner v witness_111 = 0 := inner_eq_zero_symm hfr.2.2.2.2.1
  exact ⟨ortho_witness111_raySinSq_nineAnchors_ge_one_third hu huw,
         ortho_witness111_raySinSq_nineAnchors_ge_one_third hv hvw⟩

/-- **First `B_{1/5}(T₉)` Probe Partner of `witness_neg211` (`probe_120`)**:
`probe_120 = (1, 2, 0)` lies at projective ray distance `raySinSq probe_120 tomo_e12 = 1 / 10 < 1 / 5`
from `tomo_e12 = (1, 1, 0)`. -/
def probe_120 : GVec := ⟨1, 2, 0⟩

/-- **Second `B_{1/5}(T₉)` Probe Partner of `witness_neg211` (`probe_2m15`)**:
`probe_2m15 = (2, -1, 5)` lies at projective ray distance `raySinSq probe_2m15 tomo_e3 = 1 / 6 < 1 / 5`
from `tomo_e3 = (0, 0, 1)`. -/
def probe_2m15 : GVec := ⟨2, -1, 5⟩

theorem probe_120_nonZero : probe_120.NonZero :=
  nonZero_of_x (by simp [probe_120])

theorem probe_2m15_nonZero : probe_2m15.NonZero :=
  nonZero_of_x (by simp [probe_2m15])

/-- **Orthogonal 3-Frame `(witness_neg211, probe_120, probe_2m15)`
(`isFrame_witness_neg211_probe120_probe2m15`)**:
`witness_neg211 = (-2, 1, 1)`, `probe_120 = (1, 2, 0)`, and `probe_2m15 = (2, -1, 5)` form an
exact orthogonal 3-frame in `ℚ(i)³`. -/
theorem isFrame_witness_neg211_probe120_probe2m15 :
    IsFrame witness_neg211 probe_120 probe_2m15 := by
  refine ⟨witness_neg211_nonZero, probe_120_nonZero, probe_2m15_nonZero, ?_, ?_, ?_⟩
  · apply GaussRat.ext <;> simp [GVec.inner, witness_neg211, probe_120]
  · (apply GaussRat.ext <;> simp [GVec.inner, witness_neg211, probe_2m15]); norm_num
  · apply GaussRat.ext <;> simp [GVec.inner, probe_120, probe_2m15]

/-- **Exact 2-Frame `B_{1/5}(T₉)` Determination of `witness_111`
(`residual_witness111_eq_sum_in_fifth_ball`)**:
although any single orthogonal frame containing `witness_111 = (1, 1, 1)` has both partners at
distance `≥ 1 / 3` from `T₉`, chaining the 2-frame meridian antisymmetry
`g witness_111 = -g witness_neg211` with `isFrame_witness_neg211_probe120_probe2m15` expresses
`g witness_111 = g probe_120 + g probe_2m15` where `raySinSq probe_120 tomo_e12 = 1 / 10 < 1 / 5`
and `raySinSq probe_2m15 tomo_e3 = 1 / 6 < 1 / 5`. -/
theorem residual_witness111_eq_sum_in_fifth_ball {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g) :
    g witness_111 = g probe_120 + g probe_2m15 ∧
    raySinSq probe_120 tomo_e12 = 1 / 10 ∧
    raySinSq probe_2m15 tomo_e3 = 1 / 6 := by
  have hanti := residual_witness111_add_neg211_eq_zero hg h9
  have hfr := hg _ _ _ isFrame_witness_neg211_probe120_probe2m15
  refine ⟨by linarith, ?_, ?_⟩
  · norm_num [probe_120, tomo_e12, gv, raySinSq, normSqVec, GVec.inner, GaussRat.normSq]
  · norm_num [probe_2m15, tomo_e3, gv, raySinSq, normSqVec, GVec.inner, GaussRat.normSq]

/-- **Quantitative 2-Step `B_{1/5}(T₉)` Amplification Bound at `witness_111` and `witness_neg211`
(`residual_witness111_abs_le_two_eps_of_fifth_ball`)**:
if a zero-weight frame residual `g` vanishing on `T₉` satisfies `|g z| ≤ ε` on the `1 / 5`-ball
`B_{1/5}(T₉)`, then `|g witness_111| ≤ 2 * ε` and `|g witness_neg211| ≤ 2 * ε`. -/
theorem residual_witness111_abs_le_two_eps_of_fifth_ball {g : GVec → ℚ} {ε : ℚ}
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g)
    (hb : ∀ z : GVec, z.NonZero → (∃ a ∈ nineAnchorsList, raySinSq z a < 1 / 5) → |g z| ≤ ε) :
    |g witness_111| ≤ 2 * ε ∧ |g witness_neg211| ≤ 2 * ε := by
  obtain ⟨hsum, hsin120, hsin2m15⟩ := residual_witness111_eq_sum_in_fifth_ball hg h9
  have hanti := residual_witness111_add_neg211_eq_zero hg h9
  have he12_mem : tomo_e12 ∈ nineAnchorsList := by simp [nineAnchorsList]
  have he3_mem : tomo_e3 ∈ nineAnchorsList := by simp [nineAnchorsList]
  have h120_le : |g probe_120| ≤ ε :=
    hb probe_120 probe_120_nonZero ⟨tomo_e12, he12_mem, by rw [hsin120]; norm_num⟩
  have h2m15_le : |g probe_2m15| ≤ ε :=
    hb probe_2m15 probe_2m15_nonZero ⟨tomo_e3, he3_mem, by rw [hsin2m15]; norm_num⟩
  have htri := abs_add_le (g probe_120) (g probe_2m15)
  have hw1 : |g witness_111| ≤ 2 * ε := by rw [hsum]; linarith
  have hneg_eq : g witness_neg211 = -g witness_111 := by linarith
  have hw2 : |g witness_neg211| ≤ 2 * ε := by rw [hneg_eq, abs_neg]; exact hw1
  exact ⟨hw1, hw2⟩

/-- **Unique 2-Step `B_{1/5}(T₉)` Vanishing of `witness_111` and `witness_neg211`
(`residual_witness111_eq_zero_of_fifth_ball`)**:
any zero-weight frame residual `g` vanishing on `T₉` that vanishes on `B_{1/5}(T₉)` is forced in
2 frame steps to satisfy `g witness_111 = 0` and `g witness_neg211 = 0`. -/
theorem residual_witness111_eq_zero_of_fifth_ball {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (h9 : VanishesOnNineRays g)
    (hz : ∀ z : GVec, z.NonZero → (∃ a ∈ nineAnchorsList, raySinSq z a < 1 / 5) → g z = 0) :
    g witness_111 = 0 ∧ g witness_neg211 = 0 := by
  have hb : ∀ z : GVec, z.NonZero → (∃ a ∈ nineAnchorsList, raySinSq z a < 1 / 5) → |g z| ≤ 0 := by
    intro z hznz hmem
    rw [hz z hznz hmem, abs_zero]
  obtain ⟨hw1, hw2⟩ := residual_witness111_abs_le_two_eps_of_fifth_ball hg h9 hb
  rw [mul_zero] at hw1 hw2
  exact ⟨abs_nonpos_iff.mp hw1, abs_nonpos_iff.mp hw2⟩

theorem isFrame_tomo_e12_e3_bisector : IsFrame tomo_e12 tomo_e3 bisector_12_neg := by
  obtain ⟨he3, he12, hbis, h3_12, h3_bis, h12_bis⟩ := isFrame_tomo_e3_e12_bisector
  exact ⟨he12, he3, hbis, inner_eq_zero_symm h3_12, h12_bis, h3_bis⟩

theorem witness_neg211_raySinSq_bisector_12_neg :
    raySinSq witness_neg211 bisector_12_neg = 1 / 4 := by
  norm_num [witness_neg211, bisector_12_neg, raySinSq, normSqVec, GVec.inner, GaussRat.normSq]

/-- **Sharp `< 1 / 8` Isolation Obstruction at `witness_neg211` Relative to `(tomo_e12, tomo_e3)`
(`witness_neg211_isolation_one_eighth`)**:
because `raySinSq witness_neg211 bisector_12_neg = 1 / 4` and
`IsFrame tomo_e12 tomo_e3 bisector_12_neg`, every orthogonal 3-frame `IsFrame u v witness_neg211`
satisfies `1 / 4 ≤ raySinSq u tomo_e12 + raySinSq v tomo_e3` and cannot have both
`raySinSq u tomo_e12 < 1 / 8` and `raySinSq v tomo_e3 < 1 / 8` (showing that the 2-step probes
`probe_120` and `probe_2m15` with `1 / 10 + 1 / 6 = 4 / 15` nearly saturate the `1 / 4` lower bound). -/
theorem witness_neg211_isolation_one_eighth {u v : GVec}
    (hfr : IsFrame u v witness_neg211) :
    1 / 4 ≤ raySinSq u tomo_e12 + raySinSq v tomo_e3 ∧
    ¬ (raySinSq u tomo_e12 < 1 / 8 ∧ raySinSq v tomo_e3 < 1 / 8) := by
  have hge : (1 : ℚ) / 4 ≤ raySinSq witness_neg211 bisector_12_neg := by
    rw [witness_neg211_raySinSq_bisector_12_neg]
  have hiso := fixed_anchor_frame_isolation_obstruction hfr isFrame_tomo_e12_e3_bisector hge
  refine ⟨hiso.1, ?_⟩
  rintro ⟨hu_lt, hv_lt⟩
  linarith [hiso.1]

/-- Projective ray distance from any nonzero vector `u` to itself is `0`. -/
theorem raySinSq_self {u : GVec} (hu : u.NonZero) : raySinSq u u = 0 := by
  have hnu : normSqVec u ≠ 0 := normSqVec_ne_zero_of_nonZero hu
  have hip : (GVec.inner u u).normSq = (normSqVec u) ^ 2 := by
    rw [inner_self_eq_normSqVec]
    simp [GaussRat.normSq]
  unfold raySinSq
  rw [hip]
  field_simp
  ring

theorem isFrame_witness111_bisector_neg211 :
    IsFrame witness_111 bisector_23_neg witness_neg211 := by
  obtain ⟨hw1, hw2, hbis, h12, h1b, h2b⟩ := isFrame_witness111_neg211_bisector
  exact ⟨hw1, hbis, hw2, h1b, h12, inner_eq_zero_symm h2b⟩

theorem isFrame_neg211_bisector_witness111 :
    IsFrame witness_neg211 bisector_23_neg witness_111 := by
  obtain ⟨hw1, hw2, hbis, h12, h1b, h2b⟩ := isFrame_witness111_neg211_bisector
  exact ⟨hw2, hbis, hw1, h2b, inner_eq_zero_symm h12, inner_eq_zero_symm h1b⟩

/-- **Perturbed Two-Frame Bisector Bounce-Back (`perturbed_witness111_neg211_bounce_back`)**:
for any perturbed frame `IsFrame witness_111 u v` and second-step frame `IsFrame v u' v'`, keeping
`u` and `u'` close to `bisector_23_neg = (0, 1, -1)` forces `v` close to `witness_neg211` and
forces `v'` to bounce back toward `witness_111`:
`raySinSq v witness_neg211 ≤ raySinSq u bisector_23_neg` and
`raySinSq v' witness_111 ≤ raySinSq u bisector_23_neg + raySinSq u' bisector_23_neg`. -/
theorem perturbed_witness111_neg211_bounce_back {u v u' v' : GVec}
    (hfr1 : IsFrame witness_111 u v) (hfr2 : IsFrame v u' v') :
    raySinSq v witness_neg211 ≤ raySinSq u bisector_23_neg ∧
    raySinSq v' witness_111 ≤ raySinSq u bisector_23_neg + raySinSq u' bisector_23_neg := by
  have hstep1 :=
    frame_third_raySinSq_le_add_of_ortho_anchors hfr1 isFrame_witness111_bisector_neg211
  rw [raySinSq_self witness_111_nonZero, zero_add] at hstep1
  have hstep2 :=
    frame_third_raySinSq_le_add_of_ortho_anchors hfr2 isFrame_neg211_bisector_witness111
  exact ⟨hstep1, by linarith⟩

/-- **Generic Non-Symmetric Ray `witness_123 = (1, 2, 3)` (`witness_123`)**:
a generic ray in `ℚ(i)³` outside all coordinate and bisector symmetry planes (`‖witness_123‖² = 14`). -/
def witness_123 : GVec := ⟨1, 2, 3⟩

theorem witness_123_nonZero : witness_123.NonZero :=
  nonZero_of_x (by simp [witness_123])

theorem sixBisectorPartnersList_nonZero : ∀ b ∈ sixBisectorPartnersList, b.NonZero := by
  intro b hb
  simp only [sixBisectorPartnersList, List.mem_cons, List.not_mem_nil, or_false] at hb
  rcases hb with rfl | rfl | rfl | rfl | rfl | rfl
  · exact nonZero_of_x (by simp [bisector_12_neg])
  · exact nonZero_of_x (by simp [bisector_12i_neg])
  · exact nonZero_of_x (by simp [bisector_13_neg])
  · exact nonZero_of_x (by simp [bisector_13i_neg])
  · exact nonZero_of_y (by simp [bisector_23_neg])
  · exact nonZero_of_y (by simp [bisector_23i_neg])

theorem witness123_raySinSq_nineAnchors_le :
    ∀ a ∈ nineAnchorsList, raySinSq witness_123 a ≤ 13 / 14 := by
  intro a ha
  simp only [nineAnchorsList, List.mem_cons, List.not_mem_nil, or_false] at ha
  rcases ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [witness_123, tomo_e1, tomo_e2, tomo_e3, tomo_e12, tomo_e13, tomo_e23,
      tomo_e12i, tomo_e13i, tomo_e23i, gv, GaussRat.I, raySinSq, normSqVec,
      GVec.inner, GaussRat.normSq]

theorem witness123_raySinSq_sixBisectors_le :
    ∀ b ∈ sixBisectorPartnersList, raySinSq witness_123 b ≤ 27 / 28 := by
  intro b hb
  simp only [sixBisectorPartnersList, List.mem_cons, List.not_mem_nil, or_false] at hb
  rcases hb with rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [witness_123, bisector_12_neg, bisector_12i_neg, bisector_13_neg,
      bisector_13i_neg, bisector_23_neg, bisector_23i_neg, GaussRat.I,
      raySinSq, normSqVec, GVec.inner, GaussRat.normSq]

/-- **Simultaneous 9-Anchor and 6-Bisector Isolation of `witness_123⊥`
(`ortho_witness123_raySinSq_nine_and_six_ge`)**:
because `witness_123 = (1, 2, 3)` is non-orthogonal to all 15 rays in `T₉ ∪ B₆`, every nonzero
vector `u ∈ witness_123⊥` stays bounded away from all 9 tomography anchors by
`1 / 14 ≤ raySinSq u a` and from all 6 completing bisectors by `1 / 28 ≤ raySinSq u b`. -/
theorem ortho_witness123_raySinSq_nine_and_six_ge {u : GVec}
    (hu : u.NonZero) (huw : GVec.inner u witness_123 = 0) :
    (∀ a ∈ nineAnchorsList, 1 / 14 ≤ raySinSq u a) ∧
    (∀ b ∈ sixBisectorPartnersList, 1 / 28 ≤ raySinSq u b) := by
  refine ⟨?_, ?_⟩
  · intro a ha_mem
    have ha_nz : a.NonZero := nineAnchorsList_nonZero a ha_mem
    have hge := ortho_raySinSq_add_ge_one hu witness_123_nonZero ha_nz huw
    have hle := witness123_raySinSq_nineAnchors_le a ha_mem
    linarith
  · intro b hb_mem
    have hb_nz : b.NonZero := sixBisectorPartnersList_nonZero b hb_mem
    have hge := ortho_raySinSq_add_ge_one hu witness_123_nonZero hb_nz huw
    have hle := witness123_raySinSq_sixBisectors_le b hb_mem
    linarith

/-- **Single-Frame 15-Ray Partner Isolation for `witness_123`
(`frame_witness123_partners_isolated_from_nine_and_six`)**:
in any orthogonal 3-frame `IsFrame witness_123 u v` containing `witness_123 = (1, 2, 3)`, both
orthogonal partners `u` and `v` are bounded away from all 9 tomography anchors by `≥ 1 / 14` and
from all 6 completing bisectors by `≥ 1 / 28`. -/
theorem frame_witness123_partners_isolated_from_nine_and_six {u v : GVec}
    (hfr : IsFrame witness_123 u v) :
    ((∀ a ∈ nineAnchorsList, 1 / 14 ≤ raySinSq u a) ∧
     (∀ b ∈ sixBisectorPartnersList, 1 / 28 ≤ raySinSq u b)) ∧
    ((∀ a ∈ nineAnchorsList, 1 / 14 ≤ raySinSq v a) ∧
     (∀ b ∈ sixBisectorPartnersList, 1 / 28 ≤ raySinSq v b)) := by
  have hu : u.NonZero := hfr.2.1
  have hv : v.NonZero := hfr.2.2.1
  have huw : GVec.inner u witness_123 = 0 := inner_eq_zero_symm hfr.2.2.2.1
  have hvw : GVec.inner v witness_123 = 0 := inner_eq_zero_symm hfr.2.2.2.2.1
  exact ⟨ortho_witness123_raySinSq_nine_and_six_ge hu huw,
         ortho_witness123_raySinSq_nine_and_six_ge hv hvw⟩

/-- **Explicit-Anchor Bounded Amplification Hypothesis (`HasBoundedAnchorAmplificationOn`)**:
`g : GVec → ℚ` has bounded anchor amplification relative to a finite anchor list `anchors` with
amplification factor `A ≥ 0` if every `a ∈ anchors` is nonzero with `g a = 0`, and for every
`ε > 0` and `δ > 0`, bounding `|g z| < ε` on the `δ`-neighborhood of `anchors` forces
`|g x| ≤ A * ε` for all nonzero `x ∈ ℚ(i)³`. -/
def HasBoundedAnchorAmplificationOn (anchors : List GVec) (A : ℚ) (g : GVec → ℚ) : Prop :=
  0 ≤ A ∧
  (∀ a ∈ anchors, a.NonZero) ∧
  (∀ a ∈ anchors, g a = 0) ∧
  ∀ (ε δ : ℚ), 0 < ε → 0 < δ →
    (∀ z : GVec, z.NonZero → (∃ a ∈ anchors, raySinSq z a < δ) → |g z| < ε) →
    ∀ x : GVec, x.NonZero → |g x| ≤ A * ε

/-- **Existential Bounded Anchor Amplification (`HasBoundedAnchorAmplification`)**:
there exist a finite list `anchors : List GVec` and `A : ℚ` such that
`HasBoundedAnchorAmplificationOn anchors A g` holds. -/
def HasBoundedAnchorAmplification (g : GVec → ℚ) : Prop :=
  ∃ (anchors : List GVec) (A : ℚ), HasBoundedAnchorAmplificationOn anchors A g

/-- **Uniform Meridian-Step Modulus (`HasUniformMeridianStepModulus`)**:
for every rational `ε > 0`, there exists a single rational `δ > 0` working uniformly across all
nonzero anchors `a ∈ ℚ(i)³ \ {0}` and all nonzero orthogonal tangent steps `y ∈ a⊥ \ {0}` such that
`normSqVec y / (normSqVec a + normSqVec y) < δ` implies `|f (GVec.add a y) - f a| < ε`. -/
def HasUniformMeridianStepModulus (f : GVec → ℚ) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
    ∀ a y : GVec, a.NonZero → y.NonZero → GVec.inner a y = 0 →
      normSqVec y / (normSqVec a + normSqVec y) < δ →
        |f (GVec.add a y) - f a| < ε

/-- **Dense Uniform Meridian-Step Modulus Upgrade (`HasDenseUniformModulusFromPointwise`)**:
states that pointwise ray continuity on `ℚ(i)³ \ {0}` upgrades to a uniform meridian-step modulus
(`HasUniformMeridianStepModulus f`) across all nonzero anchors `a ∈ ℚ(i)³ \ {0}` and orthogonal
tangent steps `y ∈ a⊥ \ {0}`. -/
def HasDenseUniformModulusFromPointwise (f : GVec → ℚ) : Prop :=
  IsPointwiseRayContinuous f → HasUniformMeridianStepModulus f

/-- Two vectors in `ℚ(i)³` with zero squared Euclidean distance are equal. -/
theorem eq_of_distSqVec_eq_zero {u v : GVec} (h : distSqVec u v = 0) : u = v := by
  unfold distSqVec normSqVec at h
  have hx0 : (u.x - v.x).normSq = 0 := by
    linarith [GaussRat.normSq_nonneg (u.x - v.x), GaussRat.normSq_nonneg (u.y - v.y),
      GaussRat.normSq_nonneg (u.z - v.z)]
  have hy0 : (u.y - v.y).normSq = 0 := by
    linarith [GaussRat.normSq_nonneg (u.x - v.x), GaussRat.normSq_nonneg (u.y - v.y),
      GaussRat.normSq_nonneg (u.z - v.z)]
  have hz0 : (u.z - v.z).normSq = 0 := by
    linarith [GaussRat.normSq_nonneg (u.x - v.x), GaussRat.normSq_nonneg (u.y - v.y),
      GaussRat.normSq_nonneg (u.z - v.z)]
  have hx := sub_eq_zero.mp ((GaussRat.normSq_eq_zero_iff (u.x - v.x)).mp hx0)
  have hy := sub_eq_zero.mp ((GaussRat.normSq_eq_zero_iff (u.y - v.y)).mp hy0)
  have hz := sub_eq_zero.mp ((GaussRat.normSq_eq_zero_iff (u.z - v.z)).mp hz0)
  cases u; cases v; simp_all

/-- **Collinear Ray Projection Identity (`eq_of_raySinSq_eq_zero`)**:
if `u` is nonzero and `raySinSq u v = 0`, then `GVec.smul (projScalar u v) u = v`. -/
theorem eq_of_raySinSq_eq_zero {u v : GVec} (hu : u.NonZero) (hsin : raySinSq u v = 0) :
    GVec.smul (projScalar u v) u = v := by
  apply eq_of_distSqVec_eq_zero
  rw [distSqVec_projScalar_smul hu v, hsin, mul_zero]

theorem distSqVec_symm (u v : GVec) : distSqVec u v = distSqVec v u := by
  simp only [distSqVec, normSqVec, GaussRat.normSq, GaussRat.re_sub, GaussRat.im_sub]
  ring

theorem addVec_sub_cancel (a v : GVec) : GVec.add a (GVec.sub v a) = v := by
  ext <;> simp [GVec.add, GVec.sub]

theorem inner_projScalar_smul_right {u : GVec} (hu : u.NonZero) (v : GVec) :
    GVec.inner u (GVec.smul (projScalar u v) u) = GVec.inner u v := by
  have hnu : normSqVec u ≠ 0 := normSqVec_ne_zero_of_nonZero hu
  rw [GaussianTomography.inner_smul_right, inner_self_eq_normSqVec]
  ext
  · simp only [projScalar, GaussRat.re_mul]
    field_simp [hnu]
    ring
  · simp only [projScalar, GaussRat.im_mul]
    field_simp [hnu]
    ring

/-- Orthogonal projection residual orthogonality: `a = (projScalar u v) • u` is orthogonal to
`y = v - a`. -/
theorem inner_projScalar_smul_sub_eq_zero {u : GVec} (hu : u.NonZero) (v : GVec) :
    GVec.inner (GVec.smul (projScalar u v) u) (GVec.sub v (GVec.smul (projScalar u v) u)) = 0 := by
  rw [inner_smul_left, GaussianTomography.inner_sub_right,
      inner_projScalar_smul_right hu v, sub_self, mul_zero]

/-- Uniform ray continuity implies a uniform meridian-step modulus across all nonzero anchors and
orthogonal tangent steps. -/
theorem hasUniformMeridianStepModulus_of_isUniformlyRayContinuous {f : GVec → ℚ}
    (hu : IsUniformlyRayContinuous f) : HasUniformMeridianStepModulus f := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := hu ε hε
  refine ⟨δ, hδ, ?_⟩
  intro a y ha hy hay hquo
  have hay_nz : (GVec.add a y).NonZero := addVec_a_y_ne_zero_of_ortho a y ha hay
  have hsin : raySinSq (GVec.add a y) a < δ := by
    rw [(anchorMeridianOrtho_raySinSq_eq ha hy hay).1]
    exact hquo
  exact hb (GVec.add a y) a hay_nz ha hsin

/-- For any scale-invariant function `f` on `ℚ(i)³ \ {0}`, a uniform meridian-step modulus
implies uniform projective ray continuity `IsUniformlyRayContinuous f` (handling collinear rays
`raySinSq u v = 0` via `eq_of_raySinSq_eq_zero` and non-collinear rays via the orthogonal
projection decomposition `v = a + y` with `a = (projScalar u v) • u` and `y = v - a ⊥ a`). -/
theorem isUniformlyRayContinuous_of_hasUniformMeridianStepModulus {f : GVec → ℚ}
    (hscale : IsScaleInvariantOnRays f) (hmer : HasUniformMeridianStepModulus f) :
    IsUniformlyRayContinuous f := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := hmer ε hε
  refine ⟨min 1 δ, lt_min one_pos hδ, ?_⟩
  intro u v hu hv hsin
  have hsin1 : raySinSq u v < 1 := lt_of_lt_of_le hsin (min_le_left 1 δ)
  have hsin_δ : raySinSq u v < δ := lt_of_lt_of_le hsin (min_le_right 1 δ)
  let c := projScalar u v
  have hc : c ≠ 0 := projScalar_ne_zero_of_raySinSq_lt_one hu hv hsin1
  let a := GVec.smul c u
  have ha : a.NonZero := nonZero_smul hc hu
  have hfa : f a = f u := hscale u hu c hc
  by_cases h0 : raySinSq u v = 0
  · have hav : a = v := eq_of_raySinSq_eq_zero hu h0
    have hfuv : f u = f v := by rw [← hfa, hav]
    rw [hfuv, sub_self, abs_zero]
    exact hε
  · have hsin_pos : 0 < raySinSq u v :=
      lt_of_le_of_ne (raySinSq_nonneg hu hv) (Ne.symm h0)
    let y := GVec.sub v a
    have hay : GVec.inner a y = 0 := inner_projScalar_smul_sub_eq_zero hu v
    have hadd : GVec.add a y = v := addVec_sub_cancel a v
    have hnv_pos : 0 < normSqVec v := normSqVec_pos_of_nonZero hv
    have hny_eq : normSqVec y = normSqVec v * raySinSq u v := by
      change distSqVec v a = normSqVec v * raySinSq u v
      rw [distSqVec_symm v a, distSqVec_projScalar_smul hu v]
    have hy : y.NonZero := by
      apply nonZero_of_normSqVec_pos
      rw [hny_eq]
      exact mul_pos hnv_pos hsin_pos
    have hsum_eq : normSqVec a + normSqVec y = normSqVec v := by
      rw [← (normSqVec_add_eq_normSqVec_sub_of_ortho hay).1, hadd]
    have hquo : normSqVec y / (normSqVec a + normSqVec y) < δ := by
      rw [hsum_eq, hny_eq, mul_div_cancel_left₀ (raySinSq u v) (ne_of_gt hnv_pos)]
      exact hsin_δ
    have hlt := hb a y ha hy hay hquo
    rw [hadd, hfa, abs_sub_comm] at hlt
    exact hlt

/-- **Genuine Meridian-Step Characterization of Uniform Ray Continuity
(`isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus`)**:
for any scale-invariant ray function `f` on `ℚ(i)³ \ {0}` (including every frame function and
every zero-weight frame residual), uniform projective ray continuity `IsUniformlyRayContinuous f`
is equivalent to having a uniform meridian-step modulus `HasUniformMeridianStepModulus f`. -/
theorem isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus {f : GVec → ℚ}
    (hscale : IsScaleInvariantOnRays f) :
    IsUniformlyRayContinuous f ↔ HasUniformMeridianStepModulus f :=
  ⟨hasUniformMeridianStepModulus_of_isUniformlyRayContinuous,
   isUniformlyRayContinuous_of_hasUniformMeridianStepModulus hscale⟩

/-- **Equatorial Kelvin-Partner Characterization of `HasUniformMeridianStepModulus`
(`hasUniformMeridianStepModulus_iff_equatorial_kelvin_modulus`)**:
for any frame function `f` on `ℚ(i)³`, having a uniform meridian-step modulus
`HasUniformMeridianStepModulus f` (`|f (a + y) - f a| < ε`) is equivalent to having a uniform
equatorial Kelvin-partner modulus `|f y - f (anchorMeridianOrtho a y)| < ε` across all nonzero
anchors `a ∈ ℚ(i)³ \ {0}` and orthogonal tangent steps `y ∈ a⊥ \ {0}`. -/
theorem hasUniformMeridianStepModulus_iff_equatorial_kelvin_modulus {f : GVec → ℚ}
    (hf : IsFrameFunction f) :
    HasUniformMeridianStepModulus f ↔
      (∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
        ∀ a y : GVec, a.NonZero → y.NonZero → GVec.inner a y = 0 →
          normSqVec y / (normSqVec a + normSqVec y) < δ →
            |f y - f (anchorMeridianOrtho a y)| < ε) := by
  constructor
  · intro hmer ε hε
    obtain ⟨δ, hδ, hb⟩ := hmer ε hε
    refine ⟨δ, hδ, ?_⟩
    intro a y ha hy hay hquo
    have hlt := hb a y ha hy hay hquo
    have hbridge := (anchor_meridian_kelvin_bridge hf ha hy hay).2.2.2
    rw [hbridge]
    exact hlt
  · intro hkel ε hε
    obtain ⟨δ, hδ, hb⟩ := hkel ε hε
    refine ⟨δ, hδ, ?_⟩
    intro a y ha hy hay hquo
    have hlt := hb a y ha hy hay hquo
    have hbridge := (anchor_meridian_kelvin_bridge hf ha hy hay).2.2.2
    rw [← hbridge]
    exact hlt

/-- Pointwise ray continuity of `g` at a finite list of anchors where `g` vanishes implies that for
every `ε > 0` there exists `δ > 0` such that `|g z| < ε` for every nonzero `z` within `raySinSq z a < δ`
of some `a ∈ anchors`. -/
theorem exists_anchor_neighborhood_bound_of_pointwiseRayContinuous {g : GVec → ℚ}
    (anchors : List GVec)
    (hzero : ∀ a ∈ anchors, g a = 0)
    (hcont : ∀ a ∈ anchors, IsPointwiseRayContinuousAt g a) :
    ∀ ε : ℚ, 0 < ε → ∃ δ : ℚ, 0 < δ ∧
      ∀ z : GVec, z.NonZero → (∃ a ∈ anchors, raySinSq z a < δ) → |g z| < ε := by
  intro ε hε
  obtain ⟨δ, hδ, hb⟩ := finite_anchors_pointwiseRayContinuous_common_delta anchors hcont ε hε
  refine ⟨δ, hδ, ?_⟩
  intro z hz ⟨a, ha_mem, hsin⟩
  have hlt := hb a ha_mem z hz hsin
  rw [hzero a ha_mem, sub_zero] at hlt
  exact hlt

/-- **Global Vanishing from Finite-Anchor Pointwise Continuity and Bounded Amplification
(`zero_of_pointwise_and_bounded_anchor_amplification_on`)**:
if `g : GVec → ℚ` satisfies `HasBoundedAnchorAmplificationOn anchors A g` and is pointwise
ray-continuous at each `a ∈ anchors`, then `g x = 0` for every nonzero `x ∈ ℚ(i)³ \ {0}`. -/
theorem zero_of_pointwise_and_bounded_anchor_amplification_on {g : GVec → ℚ}
    {anchors : List GVec} {A : ℚ}
    (hamp : HasBoundedAnchorAmplificationOn anchors A g)
    (hcont : ∀ a ∈ anchors, IsPointwiseRayContinuousAt g a) :
    ∀ x : GVec, x.NonZero → g x = 0 := by
  obtain ⟨hA, _hanz, hzero, hbound⟩ := hamp
  intro x hx
  by_contra hne
  have hpos : 0 < |g x| := abs_pos.mpr hne
  have hA1 : 0 < A + 1 := by linarith
  let ε : ℚ := |g x| / (2 * (A + 1))
  have hε : 0 < ε := div_pos hpos (by positivity)
  obtain ⟨δ, hδ, hnbhd⟩ :=
    exists_anchor_neighborhood_bound_of_pointwiseRayContinuous anchors hzero hcont ε hε
  have hgx_le : |g x| ≤ A * ε := hbound ε δ hε hδ hnbhd x hx
  have hA_eps : A * ε ≤ |g x| / 2 := by
    calc A * ε ≤ (A + 1) * ε := by nlinarith
      _ = |g x| / 2 := by
        simp only [ε]
        field_simp
  linarith

/-- **Global Vanishing from Pointwise Ray Continuity and Bounded Anchor Amplification
(`zero_of_pointwise_and_bounded_anchor_amplification`)**:
if `g : GVec → ℚ` satisfies `HasBoundedAnchorAmplification g` and `IsPointwiseRayContinuous g`,
then `g x = 0` for every nonzero `x ∈ ℚ(i)³ \ {0}`. -/
theorem zero_of_pointwise_and_bounded_anchor_amplification {g : GVec → ℚ}
    (hamp : HasBoundedAnchorAmplification g)
    (hcont : IsPointwiseRayContinuous g) :
    ∀ x : GVec, x.NonZero → g x = 0 := by
  obtain ⟨anchors, A, hamp_on⟩ := hamp
  exact zero_of_pointwise_and_bounded_anchor_amplification_on hamp_on
    (fun a ha => hcont a (hamp_on.2.1 a ha))

/-- Every rational Hermitian Rayleigh quotient `quadRay ρ` is pointwise ray-continuous at every
nonzero vector `v₀ ∈ ℚ(i)³ \ {0}`. -/
theorem isPointwiseRayContinuousAt_quadRay (ρ : HermForm3) {v₀ : GVec} (hv₀ : v₀.NonZero) :
    IsPointwiseRayContinuousAt (quadRay ρ) v₀ :=
  isPointwiseRayContinuous_of_isUniformlyRayContinuous (isUniformlyRayContinuous_quadRay ρ) v₀ hv₀

/-- Pointwise ray continuity at `v₀` is preserved under subtraction of functions. -/
theorem isPointwiseRayContinuousAt_sub {f₁ f₂ : GVec → ℚ} {v₀ : GVec}
    (h₁ : IsPointwiseRayContinuousAt f₁ v₀) (h₂ : IsPointwiseRayContinuousAt f₂ v₀) :
    IsPointwiseRayContinuousAt (fun v => f₁ v - f₂ v) v₀ := by
  intro ε hε
  have hε2 : 0 < ε / 2 := half_pos hε
  obtain ⟨δ₁, hδ₁, hb₁⟩ := h₁ (ε / 2) hε2
  obtain ⟨δ₂, hδ₂, hb₂⟩ := h₂ (ε / 2) hε2
  refine ⟨min δ₁ δ₂, lt_min hδ₁ hδ₂, ?_⟩
  intro v hv hsin
  have hlt₁ := hb₁ v hv (lt_of_lt_of_le hsin (min_le_left δ₁ δ₂))
  have hlt₂ := hb₂ v hv (lt_of_lt_of_le hsin (min_le_right δ₁ δ₂))
  have hsplit :
      (f₁ v - f₂ v) - (f₁ v₀ - f₂ v₀) = (f₁ v - f₁ v₀) + (-(f₂ v - f₂ v₀)) := by ring
  have htri := abs_add_le (f₁ v - f₁ v₀) (-(f₂ v - f₂ v₀))
  rw [abs_neg] at htri
  rw [hsplit]
  linarith

/-- If `f` is pointwise ray-continuous at a nonzero vector `v₀`, then its tomography residual
`GaussianTomography.residual f` is also pointwise ray-continuous at `v₀`. -/
theorem isPointwiseRayContinuousAt_residual {f : GVec → ℚ} {v₀ : GVec}
    (hv₀ : v₀.NonZero) (hf : IsPointwiseRayContinuousAt f v₀) :
    IsPointwiseRayContinuousAt (GaussianTomography.residual f) v₀ :=
  isPointwiseRayContinuousAt_sub hf (isPointwiseRayContinuousAt_quadRay (tomographyForm f) hv₀)

/-- If `f` is globally pointwise ray-continuous on `ℚ(i)³ \ {0}`, then its tomography residual
`GaussianTomography.residual f` is also globally pointwise ray-continuous on `ℚ(i)³ \ {0}`. -/
theorem isPointwiseRayContinuous_residual {f : GVec → ℚ}
    (hf : IsPointwiseRayContinuous f) :
    IsPointwiseRayContinuous (GaussianTomography.residual f) :=
  fun v₀ hv₀ => isPointwiseRayContinuousAt_residual hv₀ (hf v₀ hv₀)

/-- **Conditional `TFQ-1057` Quadratic Rigidity on an Explicit Anchor List
(`born_from_pointwise_and_bounded_anchor_amplification_on`)**:
if `f` is a frame function on `ℚ(i)³` that is pointwise ray-continuous at each anchor in `anchors`
and whose tomography residual `GaussianTomography.residual f` satisfies
`HasBoundedAnchorAmplificationOn anchors A (GaussianTomography.residual f)`, then `f` coincides with
`quadRay (tomographyForm f)` on all nonzero rays and is uniformly ray-continuous. -/
theorem born_from_pointwise_and_bounded_anchor_amplification_on {f : GVec → ℚ}
    {anchors : List GVec} {A : ℚ}
    (hf : IsFrameFunction f)
    (hcont : ∀ a ∈ anchors, IsPointwiseRayContinuousAt f a)
    (hamp : HasBoundedAnchorAmplificationOn anchors A (GaussianTomography.residual f)) :
    (∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v) ∧
    IsUniformlyRayContinuous f := by
  have hcont_res : ∀ a ∈ anchors, IsPointwiseRayContinuousAt (GaussianTomography.residual f) a :=
    fun a ha => isPointwiseRayContinuousAt_residual (hamp.2.1 a ha) (hcont a ha)
  have hzero := zero_of_pointwise_and_bounded_anchor_amplification_on hamp hcont_res
  have heq : ∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v := by
    intro v hv
    have hr := hzero v hv
    unfold GaussianTomography.residual at hr
    linarith
  have hu : IsUniformlyRayContinuous f :=
    ((uniformlyRayContinuous_frameFunction_iff f).mpr
      ⟨tomographyForm f, tomography_trace_one hf, heq⟩).2
  exact ⟨heq, hu⟩

/-- **Sharp Conditional `TFQ-1057` Closure Theorem
(`born_from_pointwise_and_bounded_anchor_amplification`)**:
if `f` is a frame function on `ℚ(i)³` that is pointwise ray-continuous (`IsPointwiseRayContinuous f`)
and whose tomography residual satisfies `HasBoundedAnchorAmplification (GaussianTomography.residual f)`,
then `f` equals the Born Rayleigh quotient `quadRay (tomographyForm f)` on all nonzero vectors and is
uniformly ray-continuous on `ℚ(i)³ \ {0}`. -/
theorem born_from_pointwise_and_bounded_anchor_amplification {f : GVec → ℚ}
    (hf : IsFrameFunction f)
    (hcont : IsPointwiseRayContinuous f)
    (hamp : HasBoundedAnchorAmplification (GaussianTomography.residual f)) :
    (∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v) ∧
    IsUniformlyRayContinuous f := by
  obtain ⟨anchors, A, hamp_on⟩ := hamp
  exact born_from_pointwise_and_bounded_anchor_amplification_on hf
    (fun a ha => hcont a (hamp_on.2.1 a ha)) hamp_on

open GleasonComplex in
open scoped ComplexOrder in
/-- **Conditional `TFQ-1057` Density-Matrix Completion
(`born_density_matrix_of_pointwise_and_bounded_anchor_amplification`)**:
if `f` is a nonnegative frame function on `ℚ(i)³` that is pointwise ray-continuous and whose
tomography residual satisfies `HasBoundedAnchorAmplification (GaussianTomography.residual f)`, then
`f` is the Born rule of a unique positive semidefinite trace-one density matrix on `ℂ³`. -/
theorem born_density_matrix_of_pointwise_and_bounded_anchor_amplification {f : GVec → ℚ}
    (hf : IsNonnegFrameFunction f)
    (hcont : IsPointwiseRayContinuous f)
    (hamp : HasBoundedAnchorAmplification (GaussianTomography.residual f)) :
    ∃ ρC : Matrix (Fin 3) (Fin 3) ℂ, ρC.PosSemidef ∧ ρC.trace = 1 ∧
      (∀ v : Fin 3 → ℂ, v ≠ 0 → F f v = (star v ⬝ᵥ (ρC *ᵥ v)).re / nsq v) ∧
      (∀ g : GVec, g.NonZero → (f g : ℝ) = (star (ι g) ⬝ᵥ (ρC *ᵥ ι g)).re / nsq (ι g)) ∧
      (∀ σC : Matrix (Fin 3) (Fin 3) ℂ, σC.IsHermitian →
        (∀ v : Fin 3 → ℂ, v ≠ 0 → F f v = (star v ⬝ᵥ (σC *ᵥ v)).re / nsq v) → σC = ρC) := by
  have hu := (born_from_pointwise_and_bounded_anchor_amplification hf.1 hcont hamp).2
  exact born_density_matrix_of_uniformlyRayContinuous hf hu

/-- **Conditional `TFQ-1057` Closure from Dense Uniform Meridian-Step Modulus Upgrade
(`born_from_pointwise_and_dense_uniform_modulus`)**:
if `f` is a frame function on `ℚ(i)³` satisfying `IsPointwiseRayContinuous f` and
`HasDenseUniformModulusFromPointwise f`, then `f` equals `quadRay (tomographyForm f)` on all
nonzero rays and is uniformly ray-continuous. -/
theorem born_from_pointwise_and_dense_uniform_modulus {f : GVec → ℚ}
    (hf : IsFrameFunction f)
    (hcont : IsPointwiseRayContinuous f)
    (hdense : HasDenseUniformModulusFromPointwise f) :
    (∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v) ∧
    IsUniformlyRayContinuous f := by
  have hmer : HasUniformMeridianStepModulus f := hdense hcont
  have hu : IsUniformlyRayContinuous f :=
    (isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus
      (isScaleInvariantOnRays_of_isFrameFunction hf)).mpr hmer
  exact ⟨born_of_uniformlyRayContinuous hf hu, hu⟩

/-- **Inhabitation of `HasBoundedAnchorAmplificationOn` by the Zero Function
(`hasBoundedAnchorAmplificationOn_zero`)**:
for any finite list `anchors : List GVec` of nonzero rays, the identically zero function
`fun _ => 0` satisfies `HasBoundedAnchorAmplificationOn anchors 0 (fun _ => 0)`. -/
theorem hasBoundedAnchorAmplificationOn_zero (anchors : List GVec)
    (hanz : ∀ a ∈ anchors, a.NonZero) :
    HasBoundedAnchorAmplificationOn anchors 0 (fun _ => 0) := by
  refine ⟨le_rfl, hanz, fun _ _ => rfl, ?_⟩
  intro ε _δ _hε _hδ _hnbhd x _hx
  simp

/-- **Inhabitation of `HasBoundedAnchorAmplificationOn` by Uniformly Ray-Continuous Frame Functions
(`hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous`)**:
if `f` is a uniformly ray-continuous frame function on `ℚ(i)³`, then its tomography residual
`GaussianTomography.residual f` vanishes on all nonzero vectors and satisfies
`HasBoundedAnchorAmplificationOn nineAnchorsList 0 (GaussianTomography.residual f)` (and hence
`HasBoundedAnchorAmplification (GaussianTomography.residual f)`). -/
theorem hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous {f : GVec → ℚ}
    (hf : IsFrameFunction f) (hu : IsUniformlyRayContinuous f) :
    HasBoundedAnchorAmplificationOn nineAnchorsList 0 (GaussianTomography.residual f) ∧
    HasBoundedAnchorAmplification (GaussianTomography.residual f) := by
  have hborn := born_of_uniformlyRayContinuous hf hu
  have h9 := (vanishesOnNineRays_iff_forall_nineAnchorsList (GaussianTomography.residual f)).mp
    (residual_vanishes_on_nine_rays f)
  have hamp_on : HasBoundedAnchorAmplificationOn nineAnchorsList 0 (GaussianTomography.residual f) := by
    refine ⟨le_rfl, nineAnchorsList_nonZero, h9, ?_⟩
    intro ε _δ _hε _hδ _hnbhd x hx
    have hfx := hborn x hx
    have hres : GaussianTomography.residual f x = 0 := by
      unfold GaussianTomography.residual
      linarith
    rw [hres, abs_zero, zero_mul]
  exact ⟨hamp_on, ⟨nineAnchorsList, 0, hamp_on⟩⟩

/-- **Necessary and Sufficient Characterization of Uniform Ray Continuity via Bounded Anchor
Amplification (`uniformlyRayContinuous_iff_pointwise_and_bounded_anchor_amplification`)**:
for any frame function `f` on `ℚ(i)³`, `IsUniformlyRayContinuous f` is equivalent to the
conjunction of `IsPointwiseRayContinuous f` and
`HasBoundedAnchorAmplification (GaussianTomography.residual f)`. -/
theorem uniformlyRayContinuous_iff_pointwise_and_bounded_anchor_amplification {f : GVec → ℚ}
    (hf : IsFrameFunction f) :
    IsUniformlyRayContinuous f ↔
      (IsPointwiseRayContinuous f ∧
       HasBoundedAnchorAmplification (GaussianTomography.residual f)) := by
  constructor
  · intro hu
    exact ⟨isPointwiseRayContinuous_of_isUniformlyRayContinuous hu,
           (hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous hf hu).2⟩
  · rintro ⟨hcont, hamp⟩
    exact (born_from_pointwise_and_bounded_anchor_amplification hf hcont hamp).2

/-- **Inhabitation of `HasDenseUniformModulusFromPointwise` by Rational Hermitian Rayleigh Quotients
(`hasDenseUniformModulusFromPointwise_quadRay`)**:
every rational Hermitian Rayleigh quotient `quadRay ρ` satisfies
`HasDenseUniformModulusFromPointwise (quadRay ρ)`. -/
theorem hasDenseUniformModulusFromPointwise_quadRay (ρ : HermForm3) :
    HasDenseUniformModulusFromPointwise (quadRay ρ) :=
  fun _ => hasUniformMeridianStepModulus_of_isUniformlyRayContinuous
    (isUniformlyRayContinuous_quadRay ρ)

/-- **Necessary and Sufficient Characterization of Uniform Ray Continuity via Dense Uniform
Meridian-Step Modulus Upgrade (`uniformlyRayContinuous_iff_pointwise_and_dense_uniform_modulus`)**:
for any frame function `f` on `ℚ(i)³`, `IsUniformlyRayContinuous f` is equivalent to the
conjunction of `IsPointwiseRayContinuous f` and `HasDenseUniformModulusFromPointwise f`. -/
theorem uniformlyRayContinuous_iff_pointwise_and_dense_uniform_modulus {f : GVec → ℚ}
    (hf : IsFrameFunction f) :
    IsUniformlyRayContinuous f ↔
      (IsPointwiseRayContinuous f ∧ HasDenseUniformModulusFromPointwise f) := by
  constructor
  · intro hu
    exact ⟨isPointwiseRayContinuous_of_isUniformlyRayContinuous hu,
           fun _ => hasUniformMeridianStepModulus_of_isUniformlyRayContinuous hu⟩
  · rintro ⟨hcont, hdense⟩
    exact (born_from_pointwise_and_dense_uniform_modulus hf hcont hdense).2

end BornFinite.GaussianFiniteModel

#print axioms BornFinite.GaussianFiniteModel.global_frameFunction_restricts_to_scenario
#print axioms BornFinite.GaussianFiniteModel.global_nonneg_frameFunction_restricts_to_scenario
#print axioms BornFinite.GaussianFiniteModel.nineAnchorSingleFrameScenario_admits_zero_one
#print axioms BornFinite.GaussianFiniteModel.finite_scenario_vs_global_frame_dichotomy
#print axioms BornFinite.GaussianFiniteModel.frameFamily_isFrame
#print axioms BornFinite.GaussianFiniteModel.rayFamily_raySinSq_pos
#print axioms BornFinite.GaussianFiniteModel.vanishes_on_six_bisector_partners
#print axioms BornFinite.GaussianFiniteModel.normalizeAtZero_isFrameFunction
#print axioms BornFinite.GaussianFiniteModel.normalizeAtZero_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianFiniteModel.abs_residual_le_one_add_coeffNorm_of_nonneg
#print axioms BornFinite.GaussianFiniteModel.abs_residual_le_one_of_nonneg_and_quadRay_bounds
#print axioms BornFinite.GaussianFiniteModel.hf_eq_quadNum_hermForm3OfGaussMatrix
#print axioms BornFinite.GaussianFiniteModel.hermForm3OfDensity_tr
#print axioms BornFinite.GaussianFiniteModel.effectValuation_rankOne_eq_quadRay
#print axioms BornFinite.GaussianFiniteModel.rayValuationOfEffect_isFrameFunction
#print axioms BornFinite.GaussianFiniteModel.rayValuationOfEffect_nonneg
#print axioms BornFinite.GaussianFiniteModel.rayValuationOfEffect_factorsThroughRayProjLinear
#print axioms BornFinite.GaussianFiniteModel.rayValuationOfEffect_residual_eq_zero
#print axioms BornFinite.GaussianFiniteModel.no_effectValuation_induces_exoticQi3
#print axioms BornFinite.GaussianFiniteModel.no_effectValuation_induces_sp
#print axioms BornFinite.GaussianFiniteModel.raySinSq_le_distSqVec_div
#print axioms BornFinite.GaussianFiniteModel.distSqVec_projScalar_smul
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuous_iff_isArchimedeanContinuousEverywhere
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuous_of_isUniformlyRayContinuous
#print axioms BornFinite.GaussianFiniteModel.not_isPointwiseRayContinuousAt_s3_tomo_e1
#print axioms BornFinite.GaussianFiniteModel.not_isPointwiseRayContinuousAt_s7_tomo_e1
#print axioms BornFinite.GaussianFiniteModel.not_isPointwiseRayContinuousAt_exoticQi3_tomo_e1
#print axioms BornFinite.GaussianFiniteModel.fixedAnchor_sufficiency_of_pointwiseRayContinuous_at_anchors
#print axioms BornFinite.GaussianFiniteModel.residual_witness111_add_neg211_eq_zero
#print axioms BornFinite.GaussianFiniteModel.meridian_pair_sum_eq_approaching_anchors
#print axioms BornFinite.GaussianFiniteModel.fixedAnchor_prime_valuation_obstruction
#print axioms BornFinite.GaussianFiniteModel.fixedAnchor_remainder_ge_one_of_even_vpRat
#print axioms BornFinite.GaussianFiniteModel.s3_leadX_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianFiniteModel.s3_leadAll_isZeroWeightFrameFunction
#print axioms BornFinite.GaussianFiniteModel.s3_leadAll_vanishes_on_nine_rays
#print axioms BornFinite.GaussianFiniteModel.s3_leadAll_isBoundedOnRays
#print axioms BornFinite.GaussianFiniteModel.s3_leadAll_eq_zero_of_coord_zero
#print axioms BornFinite.GaussianFiniteModel.fixedAnchor_obstruction_of_not_isLead3All
#print axioms BornFinite.GaussianFiniteModel.crtApproachE1_s3_leadAll_eq_one
#print axioms BornFinite.GaussianFiniteModel.crtApproachE1_raySinSq_tomo_e1_le
#print axioms BornFinite.GaussianFiniteModel.three_mul_sq_ne_sq
#print axioms BornFinite.GaussianFiniteModel.moving_rational_near_maximizer_no_rational_maximizer
#print axioms BornFinite.GaussianFiniteModel.chain_step_error_accumulates
#print axioms BornFinite.GaussianFiniteModel.linearDriftChain_attains_bound
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isScaleInvariantOnRays
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_gap_ne_zero
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_jump_on_pell_pair
#print axioms BornFinite.GaussianFiniteModel.rational_piron_subadditivity
#print axioms BornFinite.GaussianFiniteModel.nonneg_frameFunction_ortho_le_one_sub
#print axioms BornFinite.GaussianFiniteModel.isFrame_tomo_e1_eqOrtho
#print axioms BornFinite.GaussianFiniteModel.equatorial_pair_sum_eq_one_sub_pole
#print axioms BornFinite.GaussianFiniteModel.meridian_kelvin_universal_bridge
#print axioms BornFinite.GaussianFiniteModel.meridian_kelvin_zeroWeight_bridge
#print axioms BornFinite.GaussianFiniteModel.meridianOrtho_raySinSq_eq
#print axioms BornFinite.GaussianFiniteModel.meridian_uniform_equatorial_continuity_of_pole_continuous
#print axioms BornFinite.GaussianFiniteModel.piron_zero_slack_step_partner_bridge
#print axioms BornFinite.GaussianFiniteModel.piron_symmetric_step_partner_balance
#print axioms BornFinite.GaussianFiniteModel.pironStep_pironPartner_raySinSq_eq
#print axioms BornFinite.GaussianFiniteModel.piron_step_continuous_of_eqOrtho_continuous
#print axioms BornFinite.GaussianFiniteModel.piron_three_step_zero_slack_chain_abs_le
#print axioms BornFinite.GaussianFiniteModel.piron_general_one_step_le
#print axioms BornFinite.GaussianFiniteModel.piron_general_two_step_radial_le
#print axioms BornFinite.GaussianFiniteModel.piron_general_three_step_chain_le
#print axioms BornFinite.GaussianFiniteModel.pythagEqRot_general_sandwich
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isPointwiseRayContinuousAt_tomo_e1
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isPointwiseRayContinuousAt_tomo_e2
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_not_isFrameFunction
#print axioms BornFinite.GaussianFiniteModel.yLatitudeFunction_std_and_bisector_constraints
#print axioms BornFinite.GaussianFiniteModel.no_zero_one_latitude_frameFunction
#print axioms BornFinite.GaussianFiniteModel.isFrame_gaussianHalving_base
#print axioms BornFinite.GaussianFiniteModel.isFrame_gaussianHalving_rot
#print axioms BornFinite.GaussianFiniteModel.coordSignSymmetric_gaussian_halving_identity
#print axioms BornFinite.GaussianFiniteModel.zeroWeight_coordSignSymmetric_gaussian_halving_identity
#print axioms BornFinite.GaussianFiniteModel.gaussianHalvingPos_exits_irrational_cone
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_gaussianHalvingPos_eq_zero
#print axioms BornFinite.GaussianFiniteModel.zero_on_xy_plane_of_subcone_zero_and_coordSignSymmetric
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_eq_of_normSq_eq
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isCoordSignSymmetric
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_fails_gaussian_halving_at_1_2
#print axioms BornFinite.GaussianFiniteModel.abs_normSq_sub_le_of_normSq_sub_le
#print axioms BornFinite.GaussianFiniteModel.abs_normSqVec_and_y_sub_le_of_distSqVec_lt
#print axioms BornFinite.GaussianFiniteModel.abs_sq_sub_sq_le_of_abs_sub_le
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_eventually_const
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isArchimedeanContinuousEverywhere
#print axioms BornFinite.GaussianFiniteModel.dedekindRayCut_isPointwiseRayContinuous
#print axioms BornFinite.GaussianFiniteModel.quadRay_rayProj_eq_one_sub_raySinSq
#print axioms BornFinite.GaussianFiniteModel.quadRay_rayProj_isNonnegFrameFunction
#print axioms BornFinite.GaussianFiniteModel.ortho_raySinSq_add_ge_one
#print axioms BornFinite.GaussianFiniteModel.not_both_raySinSq_lt_half_of_ortho
#print axioms BornFinite.GaussianFiniteModel.zero_of_zeroWeight_supported_in_polar_cap
#print axioms BornFinite.GaussianFiniteModel.quadRay_rayProj_tomo_e1_eq_one_sub_raySinSq
#print axioms BornFinite.GaussianFiniteModel.ortho_raySinSq_tomo_e1_add_ge_one
#print axioms BornFinite.GaussianFiniteModel.not_both_raySinSq_tomo_e1_lt_half_of_ortho
#print axioms BornFinite.GaussianFiniteModel.inner_anchorMeridianStep_anchorMeridianOrtho
#print axioms BornFinite.GaussianFiniteModel.addVec_a_y_ne_zero_of_ortho
#print axioms BornFinite.GaussianFiniteModel.anchorMeridianOrtho_ne_zero_of_ortho
#print axioms BornFinite.GaussianFiniteModel.isFrame_anchor_meridian_base
#print axioms BornFinite.GaussianFiniteModel.isFrame_anchor_meridian_rot
#print axioms BornFinite.GaussianFiniteModel.anchor_meridian_kelvin_bridge
#print axioms BornFinite.GaussianFiniteModel.anchor_meridian_zeroWeight_bridge
#print axioms BornFinite.GaussianFiniteModel.anchorMeridianOrtho_raySinSq_eq
#print axioms BornFinite.GaussianFiniteModel.anchor_uniform_equatorial_continuity_of_anchor_continuous
#print axioms BornFinite.GaussianFiniteModel.finite_anchors_pointwiseRayContinuous_common_delta
#print axioms BornFinite.GaussianFiniteModel.finite_anchors_uniform_equatorial_continuity_of_anchors_continuous
#print axioms BornFinite.GaussianFiniteModel.multi_axis_uniform_equatorial_continuity_of_axes_continuous
#print axioms BornFinite.GaussianFiniteModel.nine_anchor_uniform_equatorial_continuity_of_anchors_continuous
#print axioms BornFinite.GaussianFiniteModel.raySinSq_comm
#print axioms BornFinite.GaussianFiniteModel.raySinSq_le_one
#print axioms BornFinite.GaussianFiniteModel.raySinSq_nonneg
#print axioms BornFinite.GaussianFiniteModel.frame_raySinSq_sum_eq_two
#print axioms BornFinite.GaussianFiniteModel.anchor_frame_raySinSq_sum_eq_two
#print axioms BornFinite.GaussianFiniteModel.frame_third_raySinSq_le_add_of_ortho_anchors
#print axioms BornFinite.GaussianFiniteModel.fixed_anchor_frame_isolation_obstruction
#print axioms BornFinite.GaussianFiniteModel.witness111_raySinSq_nineAnchors_le_two_thirds
#print axioms BornFinite.GaussianFiniteModel.ortho_witness111_raySinSq_nineAnchors_ge_one_third
#print axioms BornFinite.GaussianFiniteModel.frame_witness111_partners_isolated_from_nineAnchors
#print axioms BornFinite.GaussianFiniteModel.probe_120_nonZero
#print axioms BornFinite.GaussianFiniteModel.probe_2m15_nonZero
#print axioms BornFinite.GaussianFiniteModel.isFrame_witness_neg211_probe120_probe2m15
#print axioms BornFinite.GaussianFiniteModel.residual_witness111_eq_sum_in_fifth_ball
#print axioms BornFinite.GaussianFiniteModel.residual_witness111_abs_le_two_eps_of_fifth_ball
#print axioms BornFinite.GaussianFiniteModel.residual_witness111_eq_zero_of_fifth_ball
#print axioms BornFinite.GaussianFiniteModel.isFrame_tomo_e12_e3_bisector
#print axioms BornFinite.GaussianFiniteModel.witness_neg211_raySinSq_bisector_12_neg
#print axioms BornFinite.GaussianFiniteModel.witness_neg211_isolation_one_eighth
#print axioms BornFinite.GaussianFiniteModel.raySinSq_self
#print axioms BornFinite.GaussianFiniteModel.isFrame_witness111_bisector_neg211
#print axioms BornFinite.GaussianFiniteModel.isFrame_neg211_bisector_witness111
#print axioms BornFinite.GaussianFiniteModel.perturbed_witness111_neg211_bounce_back
#print axioms BornFinite.GaussianFiniteModel.witness_123_nonZero
#print axioms BornFinite.GaussianFiniteModel.sixBisectorPartnersList_nonZero
#print axioms BornFinite.GaussianFiniteModel.witness123_raySinSq_nineAnchors_le
#print axioms BornFinite.GaussianFiniteModel.witness123_raySinSq_sixBisectors_le
#print axioms BornFinite.GaussianFiniteModel.ortho_witness123_raySinSq_nine_and_six_ge
#print axioms BornFinite.GaussianFiniteModel.frame_witness123_partners_isolated_from_nine_and_six
#print axioms BornFinite.GaussianFiniteModel.eq_of_distSqVec_eq_zero
#print axioms BornFinite.GaussianFiniteModel.eq_of_raySinSq_eq_zero
#print axioms BornFinite.GaussianFiniteModel.distSqVec_symm
#print axioms BornFinite.GaussianFiniteModel.addVec_sub_cancel
#print axioms BornFinite.GaussianFiniteModel.inner_projScalar_smul_right
#print axioms BornFinite.GaussianFiniteModel.inner_projScalar_smul_sub_eq_zero
#print axioms BornFinite.GaussianFiniteModel.hasUniformMeridianStepModulus_of_isUniformlyRayContinuous
#print axioms BornFinite.GaussianFiniteModel.isUniformlyRayContinuous_of_hasUniformMeridianStepModulus
#print axioms BornFinite.GaussianFiniteModel.isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus
#print axioms BornFinite.GaussianFiniteModel.hasUniformMeridianStepModulus_iff_equatorial_kelvin_modulus
#print axioms BornFinite.GaussianFiniteModel.exists_anchor_neighborhood_bound_of_pointwiseRayContinuous
#print axioms BornFinite.GaussianFiniteModel.zero_of_pointwise_and_bounded_anchor_amplification_on
#print axioms BornFinite.GaussianFiniteModel.zero_of_pointwise_and_bounded_anchor_amplification
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuousAt_quadRay
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuousAt_sub
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuousAt_residual
#print axioms BornFinite.GaussianFiniteModel.isPointwiseRayContinuous_residual
#print axioms BornFinite.GaussianFiniteModel.born_from_pointwise_and_bounded_anchor_amplification_on
#print axioms BornFinite.GaussianFiniteModel.born_from_pointwise_and_bounded_anchor_amplification
#print axioms BornFinite.GaussianFiniteModel.born_density_matrix_of_pointwise_and_bounded_anchor_amplification
#print axioms BornFinite.GaussianFiniteModel.born_from_pointwise_and_dense_uniform_modulus
#print axioms BornFinite.GaussianFiniteModel.hasBoundedAnchorAmplificationOn_zero
#print axioms BornFinite.GaussianFiniteModel.hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous
#print axioms BornFinite.GaussianFiniteModel.uniformlyRayContinuous_iff_pointwise_and_bounded_anchor_amplification
#print axioms BornFinite.GaussianFiniteModel.hasDenseUniformModulusFromPointwise_quadRay
#print axioms BornFinite.GaussianFiniteModel.uniformlyRayContinuous_iff_pointwise_and_dense_uniform_modulus


