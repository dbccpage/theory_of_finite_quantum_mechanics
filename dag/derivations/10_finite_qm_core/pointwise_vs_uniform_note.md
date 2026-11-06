# Pointwise versus uniform ray continuity for frame functions on Q(i)^3

Assessment updated 2026-11-03 after independent review of PR #500 at
`45b0b093921aa0281969f92da18694e2e89c3cc4`. AuthorityEffect: None.

Full findings, independent rebuild evidence, and the handoff to Claude are in
[the review](pr500_review/review.md) and [its manifest](pr500_review/manifest.json).

## Distinct questions and statuses

- **TFQ-1055 / FQ-GLEASON-QI3-FRAME-FUNCTIONS:** the original statement has **no continuity
  hypothesis**. Its unrestricted quadratic-rigidity assertion is REFUTED, even for nonnegative
  functions, by `exoticQi3_isNonnegFrameFunction` and `exoticQi3_not_quadratic`. The original
  decision question is retained verbatim; the zero-one and specified-extension alternatives
  have their separate negative answers. This is not an open pointwise-continuity statement.
- **TFQ-1056 / FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY:** CONDITIONAL on uniform ray continuity.
- **TFQ-1057 / FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM:** OPEN; signed and nonnegative cases separate.
- **TFQ-1058 / FQ-GLEASON-FRAME-CARRIERS:** the supplied carriers and frame definitions only.
- **TFQ-1059 / FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS:** the proved continuous signed C^3 theorem, CONDITIONAL on continuity away from zero.
- **TFQ-1060 / FQ-BORN-QI3-CONTINUUM-COMPLETION:** CONDITIONAL packaging in
  `lean4/GleasonBornCompletion.lean` of the existing extension lemmas into a unique complex
  density-matrix extension (`born_density_matrix_of_uniformlyRayContinuous`), Hermitian quadratic
  uniqueness (`eq_of_re_dotC_mulVec_self`), and the general quadratic converse
  (`isUniformlyRayContinuous_quadRay`, `uniformlyRayContinuous_frameFunction_iff`), conditional
  on uniform ray continuity.

TFQ-0307 remains CONDITIONAL. Its broad Born-uniqueness/operational target is not the literal
pointwise statement either. None of these results derives the Hilbert carrier or regularity
premise from finite operational data.

## What is proved

`BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` assumes:

- `IsFrameFunction f`: `f : GVec -> Q`, with sum one on every nonzero orthogonal triple in
  Q(i)^3. This is signed; no positivity is assumed.
- `IsUniformlyRayContinuous f`: for every rational epsilon > 0, a rational delta > 0 works
  for **all** nonzero u,v with `raySinSq u v < delta`, where
  `raySinSq u v = 1 - |<u,v>|^2 / (<u,u><v,v>)`.

It concludes `f v = quadRay (tomographyForm f) v` for every nonzero v. The tomography
trace-one and uniqueness results are already available separately. Nonnegative inputs are
a special case and imply nonnegativity of the rational quadratic numerator.

`raySinSq` is a squared ray distance; its square root is the metric on rays. The proof
extends f to a continuous frame function on C^3 and applies the continuous complex theorem.
The independent eight-module rebuild and 308-report axiom audit pass with only `propext`,
`Classical.choice`, and `Quot.sound`. Of the reports, 302 cover all named declarations in
the four new modules, four supporting results, and two review lemmas.

Uniform continuity is supplied, not derived. A finite instrument's resolution at one
tolerance gives one epsilon-delta pair, not the for-all-epsilon guarantee. The review
formally instantiates the hypothesis with the constant frame function 1/3. The general
instance for every Hermitian `quadRay rho` is kernel-checked in `GleasonBornCompletion`
(`isUniformlyRayContinuous_quadRay`): after phase-aligning unit representatives, the Rayleigh
quotient is uniformly continuous on the compact unit sphere of `C^3`, and the squared distance of
the aligned representatives is at most `2 raySinSq(u,v)`. The modulus obtained this way is
existential. On paper, the same alignment gives the quantitative bound
`|q_rho(u)-q_rho(v)| <= 2 ||rho|| sqrt(2 raySinSq(u,v))`, hence a rational delta from a
rational coefficient bound; that quantitative form is not formalized. The same module packages
the extension of a nonnegative uniformly ray-continuous frame function as a unique positive
semidefinite trace-one complex matrix (`born_density_matrix_of_uniformlyRayContinuous`) and
characterizes the uniformly ray-continuous frame functions on `Q(i)^3` as exactly the trace-one
rational Hermitian Rayleigh quotients (`uniformlyRayContinuous_frameFunction_iff`).

## The remaining pointwise question

Does `IsArchimedeanContinuousEverywhere f` (pointwise epsilon-delta continuity at each
nonzero rational vector, using `distSqVec`) imply uniform ray continuity for a frame
function? The signed version implies the nonnegative version, which is enough for the
probability-valued target. Neither is settled by this review.

For arbitrary functions on a dense noncompact domain, no: on Q intersected with [0,1],
take h(q)=1 above sqrt(2)/2 and h(q)=0 below it. It is locally constant at every rational
point but not uniformly continuous. This is a topological illustration, not a frame function.

## What the near-maximum argument does and does not show

First restrict to a bounded-above frame function before choosing a rational p with
`f(p) > sup f - epsilon`. Nonnegative frame functions satisfy 0 <= f <= 1 by completion
of each ray to a frame. Such boundedness is not supplied for the general signed,
pointwise-continuous rational case.

The known near-maximum descent gives an epsilon loss per step. The constructed chains
lengthen near equal latitudes, and no argument controls the accumulated loss while the
rational near-maximizing pole changes with epsilon. This is a failure of the attempted
proof, not a lower bound on every possible argument. The uniform bridge avoids it by
extension and compactness: an actual maximum exists on the complex sphere and may be at
an irrational ray. Uniform continuity does not make a fixed rational pole a maximizer.

Two-step products `(1+ti)(1+si)=a+bi` obey `b^2+4(a-1)=(t-s)^2 >= 0`, even with real
parameters, so they are not dense in C. The earlier two-step density claim remains withdrawn.
However, this is not a new obstruction to arbitrary finite-chain approximation:
`GleasonReal.exists_chain_eq` expresses every m with |m|>1 as a finite real-parameter
product. For that fixed length N, the product is continuous in R^N and Q^N is dense, so
rational products approximate m. All factors have modulus >=1, and approximation from
outside reaches the unit circle in the closure. Thus the closure of **all finite** rational
products is exactly {|m|>=1}, not C. This paragraph is a paper deduction from the checked
real theorem, not a new Lean declaration. It gives neither a uniform length bound nor
the required accumulated-error control.

## Counterexamples and a constructive search target

A zero-weight residual supported in an angular cap of radius <45 degrees vanishes if
each ray completes to an admissible rational orthogonal frame: a frame can meet that cap
in at most one ray, and the frame identity forces its value to zero. This excludes that
support construction only. It shows in this model neither that a counterexample must be a Zorn/Hamel
object nor that a finite description or finite search could never discover one.

The existing selective-oscillation results at `tomo_e1` rule out continuity everywhere
for the cited nonzero finite valuation combinations under their explicit prime/system
hypotheses. The cited declarations do not prove that every `sp` is discontinuous at every
ray; “nowhere continuous” is therefore not used as a formal result here.

For the nonnegative case, try fixed-ray oscillation propagation or exact rational frame
certificates which bound a residual value at x by values near the fixed tomography anchors
with coefficients bounded independently of the approximation tolerance. The full review
states a sufficient certificate inequality. Finite exact search can suggest and verify
individual certificates; a global theorem needs a symbolic family with the coefficient
bound proved. Projector linearity must not be silently assumed, since it already implies
the desired rigidity. The review also gives a separate effect-additive route and the
additional obligations for arbitrary complex states, higher finite dimensions, and
infinite-dimensional trace-class states.

## Phase 2 finite and exact-arithmetic Gleason model (`lean4/BornGaussianFiniteModel.lean`)

`lean4/BornGaussianFiniteModel.lean` (checked by the nine-module Gleason audit in
`evidence/lean_receipts/gleason_lean_audit.json` across 807 declarations using only `propext`,
`Classical.choice`, and `Quot.sound`, with companion exact rational certificate checks in
`scripts/verify_gleason_finite_certificates.py` and
`evidence/lean_receipts/gleason_finite_model_receipt.json`) formalizes the finite and exact-arithmetic
Gleason model over $\mathbb{Q}(i)^3$:

1. **Five-way distinction of "finite":**
   - **(i) Genuinely finite measurement scenario (`FiniteFrameScenario`):** a finite list of
     nonzero rays and admissible orthogonal frames. Every global `IsFrameFunction` restricts
     to a scenario valuation (`global_frameFunction_restricts_to_scenario`). The 9-ray
     single-frame scenario (`nineAnchorSingleFrameScenario`) admits a $\{0,1\}$-valued
     deterministic valuation (`nineAnchorSingleFrameScenario_admits_zero_one`), whereas the
     49-ray `NoColouring` scenario excludes $\{0,1\}$ valuations (`no_zero_one_frame_function`)
     while global $\mathbb{Q}(i)^3$ still admits the $\{0, 1/3, 2/3\}$-valued nonquadratic frame
     function `exoticQi3` (`finite_scenario_vs_global_frame_dichotomy`).
   - **(ii) Finite-dimensional vector space over an infinite field ($\mathbb{Q}(i)^3$):**
     exhibits an infinite family of pairwise non-collinear rays (`rayFamily_raySinSq_pos`) and
     orthogonal frames (`frameFamily_isFrame`).
   - **(iii) Finite collection of fixed tomography anchors and completing partners:** any
     zero-weight residual vanishing on the 9 tomography anchors (`nineAnchorsList`) also
     vanishes on all 6 completing axis-plane bisector partners (`sixBisectorPartnersList`,
     `vanishes_on_six_bisector_partners`), yielding 15 fixed zero rays in total.
   - **(iv) Finite presentation or certificate (`FixedAnchorBound`):** formalizes the
     fixed-anchor bound $|g(x)| \le A \max_{y \in Y} |g(y)| + B r$ over all bounded zero-weight
     anchor-vanishing residuals $g$ (`|g| \le B`).
   - **(v) Directed family of finite approximations:** formalizes the sufficiency theorem
     (`fixedAnchor_sufficiency_of_pointwiseRayContinuous_at_anchors`) showing that if a target
     ray $x$ admits a fixed $A \ge 0$ and finite probe lists $Y$ approaching `nineAnchorsList`
     in `raySinSq` with $r \to 0$, then every bounded zero-weight anchor-vanishing residual
     that is pointwise ray-continuous at the 9 anchors vanishes at $x$.

2. **Normalization and boundedness consequences:**
   - Origin normalization (`normalizeAtZero`) preserves `IsFrameFunction` and
     `IsZeroWeightFrameFunction` (`normalizeAtZero_isFrameFunction`,
     `normalizeAtZero_isZeroWeightFrameFunction`).
   - Nonnegative frame functions satisfy $|f(v) - \text{quadRay}(\text{tomographyForm}(f), v)|
     \le 1 + \text{coeffNorm}(\text{tomographyForm}(f))$ on every nonzero ray
     (`abs_residual_le_one_add_coeffNorm_of_nonneg`), and $\le 1$ whenever
     $0 \le \text{quadRay}(\text{tomographyForm}(f), v) \le 1$
     (`abs_residual_le_one_of_nonneg_and_quadRay_bounds`).

3. **Exact bridge from operator-level effect additivity to ray-level quadratic rigidity:**
   - Establishes the explicit bijection between `GVec` and `Fin 3 -> GaussRat` (`vecOfGVec`,
     `gvecOfVec`) and between $3 \times 3$ Hermitian Gaussian-rational matrices and `HermForm3`
     (`hermForm3OfGaussMatrix`, `gaussMatrixOfHermForm3`, `hf_eq_quadNum_hermForm3OfGaussMatrix`).
   - Shows that every operator-level `EffectValuation (HermitianCarrier.space 3)` restricts on
     rank-1 projectors `P (vecOfGVec v)` to `quadRay (hermForm3OfDensity W) v`
     (`effectValuation_rankOne_eq_quadRay`), inducing a nonnegative frame function that factors
     linearly through `rayProj` (`rayValuationOfEffect_factorsThroughRayProjLinear`) with zero
     tomography residual (`rayValuationOfEffect_residual_eq_zero`).
   - Shows that operator-level effect additivity excludes `exoticQi3` and every prime-indexed
     counterexample $(1 + \text{sp}_p)/3$ without any topological continuity hypothesis
     (`no_effectValuation_induces_exoticQi3`, `no_effectValuation_induces_sp`).

4. **Exact rational equivalence of vector-level and projective ray-level pointwise continuity:**
   - Establishes the rational inequality `raySinSq u v₀ <= distSqVec u v₀ / normSqVec v₀`
     (`raySinSq_le_distSqVec_div`) and the exact orthogonal projection identity
     `distSqVec (GVec.smul (projScalar u v₀) u) v₀ = normSqVec v₀ * raySinSq u v₀`
     (`distSqVec_projScalar_smul`).
   - Concludes `IsPointwiseRayContinuousAt g v₀ <-> IsArchimedeanContinuousAt g v₀` and
     `IsPointwiseRayContinuous g <-> IsArchimedeanContinuousEverywhere g` for all
     scale-invariant ray functions (`isPointwiseRayContinuousAt_iff_isArchimedeanContinuousAt`,
     `isPointwiseRayContinuous_iff_isArchimedeanContinuousEverywhere`).

5. **Fixed-anchor certificate structure, meridian pair antisymmetry, prime-valuation and
   coordinate-plane obstructions, and Chinese Remainder collisions (`TFQ-1057`):**
   - **Exact 2-frame meridian antisymmetry:** for every zero-weight residual $g$ vanishing on
     the 9 anchors, $g(1,1,1) + g(-2,1,1) = 0$ (`residual_witness111_add_neg211_eq_zero`), and
     for every $t \ge 0$, $g(1,1,1) + g(-2,1,1) = g(1+t, 1, 1) + g(-2, 1+t, 1+t)$ with
     $(1+t,1,1) \to e_1$ and $(-2,1+t,1+t) \to e_{23}$
     (`meridian_pair_sum_eq_approaching_anchors`).
   - **Prime-valuation obstruction (`fixedAnchor_prime_valuation_obstruction`,
     `fixedAnchor_remainder_ge_one_of_even_vpRat`):** any `FixedAnchorBound A r Y x` with
     $A \ge 0$, $r < 1$, and $\text{sp}_p(x) \ne 0$ for an inert prime $p$ must include a probe
     $y \in Y$ with odd $p$-adic norm valuation `vpRat p (normSqVec y) % 2 != 0`.
   - **Coordinate-refined 3-adic residuals (`s3_leadX`, `s3_leadAll`) and coordinate-plane
     obstruction (`fixedAnchor_obstruction_of_not_isLead3All`):** `s3_leadAll` is a bounded
     zero-weight anchor-vanishing residual (`|s3_leadAll| <= 1`) with
     `s3_leadAll witness_111 = 1` that vanishes on the union of the three coordinate planes
     `u.x = 0 \/ u.y = 0 \/ u.z = 0` (`s3_leadAll_eq_zero_of_coord_zero`), forcing $r \ge 1$
     whenever all probes satisfy `~ isLead3All y`.
   - **Chinese Remainder Archimedean/3-adic collision sequence (`crtApproachE1`):**
     `crtApproachE1 m = (1 + 9*(m+1), 1, 1)` satisfies `s3_leadAll (crtApproachE1 m) = 1` for
     every $m \in \mathbb{N}$ (`crtApproachE1_s3_leadAll_eq_one`) while converging in projective
     ray distance `raySinSq` to `tomo_e1 = (1, 0, 0)` at rate $\le 2 / (1 + 9(m+1))^2$
     (`crtApproachE1_raySinSq_tomo_e1_le`).

6. **Explicit proof-obligation separations:**
   - Moving rational near-maximizers without a rational maximizer for $- (3q^2 - 1)^2$ on
     $\mathbb{Q}$ (`three_mul_sq_ne_sq`,
     `moving_rational_near_maximizer_no_rational_maximizer`).
   - Linear accumulation $L\varepsilon$ of step-wise $\varepsilon$ chain drift
     (`chain_step_error_accumulates`, `linearDriftChain_attains_bound`).
   - Scale-invariant $\{0,1\}$-valued Dedekind ray cut `dedekindRayCut` on
     $\mathbb{Q}(i)^3 \setminus \{0\}$ across the irrational cone $3|u_y|^4 = \|u\|^4$
     (`dedekindRayCut_isScaleInvariantOnRays`, `dedekindRayCut_gap_ne_zero`,
     `dedekindRayCut_jump_on_pell_pair`).

7. **Track A (General-Value Rational Piron–Soler Chain & Polar–Equatorial Transfer) and Track B
   (Irrational-Locus / Dedekind-Cut Frame Stress Tests) on $\mathbb{Q}(i)^3$ (`TFQ-1057`):**
   - **Track A (Rational Piron–Soler Chain & Polar–Equatorial Transfer):**
     - General rational Piron orthogonal subadditivity (`rational_piron_subadditivity`,
       `nonneg_frameFunction_ortho_le_one_sub`) and equatorial pole-deficiency decomposition
       `f(y) + f(\text{eqOrtho}(y)) = 1 - f(e_1)` (`isFrame_tomo_e1_eqOrtho`,
       `equatorial_pair_sum_eq_one_sub_pole`).
     - General two-frame meridian–Kelvin polar–equatorial bridge (`meridian_kelvin_universal_bridge`,
       `meridian_kelvin_zeroWeight_bridge`, `meridianOrtho_raySinSq_eq`): for any frame function $f$
       (without assuming $f(e_1) = 1$ or nonnegativity) and any $y \in e_1^\perp \setminus \{0\}$,
       subtracting the equatorial frame $(e_1, y, \text{eqOrtho}(y))$ from the meridian frame
       $(e_1 + y, \text{eqOrtho}(y), \text{meridianOrtho}(y))$ yields
       $f(e_1 + y) - f(e_1) = f(y) - f(\text{meridianOrtho}(y))$ with identical projective ray distances
       $\text{raySinSq}(e_1 + y, e_1) = \text{raySinSq}(\text{meridianOrtho}(y), y) = \|y\|^2 / (1 + \|y\|^2)$.
       Consequently, pointwise ray continuity at the single pole `tomo_e1` implies uniform meridian
       ray continuity across all equatorial directions $y \in e_1^\perp \setminus \{0\}$ with the
       same modulus $\delta(\varepsilon)$ (`meridian_uniform_equatorial_continuity_of_pole_continuous`).
     - Exact zero-slack Piron step–partner bridge and projective ray-distance duality
       (`piron_zero_slack_step_partner_bridge`, `piron_symmetric_step_partner_balance`,
       `pironStep_pironPartner_raySinSq_eq`, `piron_step_continuous_of_eqOrtho_continuous`,
       `piron_three_step_zero_slack_chain_abs_le`): for every frame function $f$, nonzero $y \in e_1^\perp$,
       and $\lambda \ne 0$, $f(\text{pironStep}(y, \lambda)) - f(e_1 + y) = f(\text{eqOrtho}(y)) - f(\text{pironPartner}(y, \lambda))$
       with $\text{raySinSq}(\text{pironStep}(y, \lambda), e_1 + y) = \text{raySinSq}(\text{pironPartner}(y, \lambda), \text{eqOrtho}(y)) = |\lambda|^2 \|y\|^2 / (1 + \|y\|^2 + |\lambda|^2 \|y\|^2)$,
       so pointwise ray continuity at $\text{eqOrtho}(y)$ propagates to Piron tangent steps at $e_1 + y$
       with zero pole-deficiency slack, and opposite tangent steps $\pm \lambda$ satisfy the symmetric
       balance $f(\text{pironStep}(y, \lambda)) + f(\text{pironPartner}(y, \lambda)) = f(\text{pironStep}(y, -\lambda)) + f(\text{pironPartner}(y, -\lambda))$.
     - General 1-step, 2-step, 3-step Piron tangent chains and Pythagorean equatorial sandwich bounds
       with explicit pole-deficiency slack $1 - f(e_1)$ (`piron_general_one_step_le`,
       `piron_general_two_step_radial_le`, `piron_general_three_step_chain_le`,
       `pythagEqRot_general_sandwich`).
   - **Track B (Irrational-Locus / Dedekind-Cut Frame Stress Tests):**
     - Local constancy and pointwise ray continuity of `dedekindRayCut` on explicit rational
       neighborhoods of `tomo_e1` ($\text{raySinSq} < 1/2$) and `tomo_e2` ($\text{raySinSq} < 1/3$)
       and at **every** nonzero vector $v_0 \in \mathbb{Q}(i)^3 \setminus \{0\}$
       (`dedekindRayCut_eq_zero_of_raySinSq_tomo_e1_lt`,
       `dedekindRayCut_isPointwiseRayContinuousAt_tomo_e1`,
       `dedekindRayCut_eq_one_of_raySinSq_tomo_e2_lt`,
       `dedekindRayCut_isPointwiseRayContinuousAt_tomo_e2`,
       `dedekindRayCut_eventually_const`,
       `dedekindRayCut_isArchimedeanContinuousEverywhere`,
       `dedekindRayCut_isPointwiseRayContinuous`), establishing an explicit scale-invariant ray
       function on $\mathbb{Q}(i)^3 \setminus \{0\}$ that is pointwise ray-continuous everywhere
       yet fails both uniform ray continuity (`dedekindRayCut_jump_on_pell_pair`) and 3-frame
       additivity (`dedekindRayCut_not_isFrameFunction`).
     - General and `tomo_e1`-anchored orthogonal ray-distance Bessel bounds, `< 45°` polar-cap
       disjointness, and global vanishing of polar-cap-supported zero-weight residuals
       (`quadRay_rayProj_eq_one_sub_raySinSq`, `quadRay_rayProj_isNonnegFrameFunction`,
       `ortho_raySinSq_add_ge_one`, `not_both_raySinSq_lt_half_of_ortho`,
       `zero_of_zeroWeight_supported_in_polar_cap`, `quadRay_rayProj_tomo_e1_eq_one_sub_raySinSq`,
       `ortho_raySinSq_tomo_e1_add_ge_one`, `not_both_raySinSq_tomo_e1_lt_half_of_ortho`): for any
       nonzero anchor $w \in \mathbb{Q}(i)^3 \setminus \{0\}$ and any two nonzero orthogonal vectors
       $u \perp v$ in $\mathbb{Q}(i)^3$, applying `rational_piron_subadditivity` to the rank-1
       projector Rayleigh quotient $\text{quadRay}(\text{rayProj}(w)) = 1 - \text{raySinSq}(\cdot, w)$
       gives $\text{raySinSq}(u, w) + \text{raySinSq}(v, w) \ge 1$, so no two orthogonal vectors can
       both lie in the polar cap $\text{raySinSq}(\cdot, w) < 1/2$, and any zero-weight frame
       residual supported inside $\text{raySinSq}(\cdot, w) < 1/2$ vanishes on all of
       $\mathbb{Q}(i)^3 \setminus \{0\}$.
     - Refutation of 3-frame additivity for `dedekindRayCut` on the rational bisector frame
       `(tomo_e3, tomo_e12, bisector_12_neg)` (`dedekindRayCut_not_isFrameFunction`) and for any
       $\{0, 1\}$-valued 1D latitude profile at `{0, 1/2, 1}`
       (`yLatitudeFunction_std_and_bisector_constraints`, `no_zero_one_latitude_frameFunction`).
     - Two-frame Gaussian-norm latitude-halving identity
       $2 f(a, b, a + bi) = f(a, b, 0) + f(0, 0, 1)$ for coordinate-sign symmetric frame functions
       and zero-weight residuals (`isFrame_gaussianHalving_base`, `isFrame_gaussianHalving_rot`,
       `coordSignSymmetric_gaussian_halving_identity`,
       `zeroWeight_coordSignSymmetric_gaussian_halving_identity`), exit of
       `gaussianHalvingPos a b = (a, b, a + bi)` from the irrational cone $3|u_y|^4 > \|u\|^4$ for
       every $(a, b) \in \mathbb{Q}^2 \setminus \{(0, 0)\}$ (`gaussianHalvingPos_exits_irrational_cone`,
       `dedekindRayCut_gaussianHalvingPos_eq_zero`), global vanishing on $(a, b, 0)$ of any
       coordinate-sign symmetric zero-weight residual supported inside the irrational cone
       (`zero_on_xy_plane_of_subcone_zero_and_coordSignSymmetric`), and explicit obstruction for
       `dedekindRayCut` at $(a, b) = (1, 2)$ (`dedekindRayCut_isCoordSignSymmetric`,
       `dedekindRayCut_fails_gaussian_halving_at_1_2`).
     - **Target 1 (`TFQ-1057` Section 7C of `lean4/BornGaussianFiniteModel.lean`) — General-anchor meridian coupling, spherical 3-frame Pythagoras identity, fixed-anchor frame isolation obstruction, and conditional `TFQ-1057` closures**:
       - **General-anchor meridian partner and zero-slack bridge**: For any anchor $a \in \mathbb{Q}(i)^3 \setminus \{0\}$ and any equatorial ray $y \neq 0$ with $\langle a, y \rangle = 0$, the meridian step `anchorMeridianStep a y = a + y` and orthogonal partner `anchorMeridianOrtho a y` $= -\|y\|^2 a + \|a\|^2 y$ satisfy $\langle a+y, w(a,y) \rangle = 0$ (`inner_anchorMeridianStep_anchorMeridianOrtho`), non-vanishing (`addVec_a_y_ne_zero_of_ortho`, `anchorMeridianOrtho_ne_zero_of_ortho`), and share cross-product axis $a \times y$ (`isFrame_anchor_meridian_base`, `isFrame_anchor_meridian_rot`), yielding the exact Kelvin bridge $f(a+y) - f(a) = f(y) - f(w(a,y))$ (`anchor_meridian_kelvin_bridge`, `anchor_meridian_zeroWeight_bridge`) with equal step distances $d_{\text{ray}}^2(a+y, a) = d_{\text{ray}}^2(w(a,y), y) = \|y\|^2/(\|a\|^2 + \|y\|^2)$ (`anchorMeridianOrtho_raySinSq_eq`). Pointwise continuity at any finite anchor list yields a single shared modulus $\delta = \min_i \delta_i > 0$ simultaneously governing meridian steps across all anchor equators (`finite_anchors_pointwiseRayContinuous_common_delta`, `finite_anchors_uniform_equatorial_continuity_of_anchors_continuous`, `multi_axis_uniform_equatorial_continuity_of_axes_continuous`, `nine_anchor_uniform_equatorial_continuity_of_anchors_continuous`).
       - **Spherical 3-frame Pythagoras identity, fixed-anchor frame isolation obstruction, and 2-step vs. $<1/8$ dichotomy**: Because $\text{quadRay}(\text{rayProj}(a))$ is a nonnegative frame function of weight $1$, every orthogonal 3-frame $\{u, v, w\}$ and non-zero ray $a$ satisfy $d_{\text{ray}}^2(u, a) + d_{\text{ray}}^2(v, a) + d_{\text{ray}}^2(w, a) = 2$ (`frame_raySinSq_sum_eq_two`, `anchor_frame_raySinSq_sum_eq_two`). Double-summing over two orthogonal 3-frames $\{u, v, w\}$ and $\{a_1, a_2, a_3\}$ yields the two-partner anchor proximity inequality $d_{\text{ray}}^2(w, a_3) \le d_{\text{ray}}^2(u, a_1) + d_{\text{ray}}^2(v, a_2)$ (`frame_third_raySinSq_le_add_of_ortho_anchors`) and the fixed-anchor frame isolation obstruction $\eta \le d_{\text{ray}}^2(u, a_1) + d_{\text{ray}}^2(v, a_2)$ whenever $d_{\text{ray}}^2(w, a_3) \ge \eta$ (`fixed_anchor_frame_isolation_obstruction`). For $w_{111} = (1, 1, 1)^T$, every single-frame partner $u \perp w_{111}$ has $d_{\text{ray}}^2(u, a) \ge 1/3$ from all 9 tomography anchors $a \in T_9$ (`witness111_raySinSq_nineAnchors_le_two_thirds`, `ortho_witness111_raySinSq_nineAnchors_ge_one_third`, `frame_witness111_partners_isolated_from_nineAnchors`), whereas chaining the 2-frame meridian antisymmetry $g(w_{111}) = -g(w_{-211})$ with the orthogonal 3-frame $(w_{-211}, p_{120}, p_{2,-1,5})$ (`probe_120`, `probe_2m15`, `isFrame_witness_neg211_probe120_probe2m15`) expresses $g(w_{111}) = g(p_{120}) + g(p_{2,-1,5})$ inside $B_{1/5}(T_9)$ with $d_{\text{ray}}^2(p_{120}, e_{12}) = 1/10$ and $d_{\text{ray}}^2(p_{2,-1,5}, e_3) = 1/6$ (`residual_witness111_eq_sum_in_fifth_ball`, `residual_witness111_abs_le_two_eps_of_fifth_ball`, `residual_witness111_eq_zero_of_fifth_ball`), while any single frame through $w_{-211}$ satisfies $1/4 \le d_{\text{ray}}^2(u, e_{12}) + d_{\text{ray}}^2(v, e_3)$ and cannot have both partners within $< 1/8$ (`witness_neg211_isolation_one_eighth`). Furthermore, perturbed two-frame chains through $w_{111}$ and $w_{-211}$ near `bisector_23_neg` bounce back toward $w_{111}$ (`perturbed_witness111_neg211_bounce_back`), and for the generic ray $w_{123} = (1, 2, 3)^T$ (`witness_123`), every $u \in w_{123}^\perp \setminus \{0\}$ and both partners in any frame through $w_{123}$ are isolated from all 9 anchors by $\ge 1/14$ and from all 6 bisectors by $\ge 1/28$ (`ortho_witness123_raySinSq_nine_and_six_ge`, `frame_witness123_partners_isolated_from_nine_and_six`).
       - **Meridian-step characterization of uniform ray continuity and conditional `TFQ-1057` closures**: Defining `HasUniformMeridianStepModulus` and `HasDenseUniformModulusFromPointwise f : Prop := IsPointwiseRayContinuous f → HasUniformMeridianStepModulus f`, uniform projective ray continuity `IsUniformlyRayContinuous f` for any scale-invariant ray function is equivalent to having a uniform meridian-step modulus across all anchors $a \in \mathbb{Q}(i)^3 \setminus \{0\}$ and orthogonal tangent steps $y \in a^\perp \setminus \{0\}$ (`eq_of_raySinSq_eq_zero`, `hasUniformMeridianStepModulus_of_isUniformlyRayContinuous`, `isUniformlyRayContinuous_of_hasUniformMeridianStepModulus`, `isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus`, `hasUniformMeridianStepModulus_iff_equatorial_kelvin_modulus`). Together with `HasBoundedAnchorAmplificationOn`, `HasBoundedAnchorAmplification`, and pointwise ray continuity of the Born residual (`isPointwiseRayContinuousAt_quadRay`, `isPointwiseRayContinuousAt_sub`, `isPointwiseRayContinuousAt_residual`, `isPointwiseRayContinuous_residual`), the conditional vanishing, Born uniqueness, witness inhabitation, and necessary-and-sufficient equivalence theorems (`exists_anchor_neighborhood_bound_of_pointwiseRayContinuous`, `zero_of_pointwise_and_bounded_anchor_amplification_on`, `zero_of_pointwise_and_bounded_anchor_amplification`, `born_from_pointwise_and_bounded_anchor_amplification_on`, `born_from_pointwise_and_bounded_anchor_amplification`, `born_density_matrix_of_pointwise_and_bounded_anchor_amplification`, `born_from_pointwise_and_dense_uniform_modulus`, `hasBoundedAnchorAmplificationOn_zero`, `hasBoundedAnchorAmplificationOn_residual_of_uniformlyRayContinuous`, `uniformlyRayContinuous_iff_pointwise_and_bounded_anchor_amplification`, `hasDenseUniformModulusFromPointwise_quadRay`, `uniformlyRayContinuous_iff_pointwise_and_dense_uniform_modulus`) isolate the exact amplification/meridian-step modulus bridge needed to close `TFQ-1057`.


