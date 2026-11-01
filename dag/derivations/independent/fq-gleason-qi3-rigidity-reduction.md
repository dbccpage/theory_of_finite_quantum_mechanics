Status: AI-drafted, awaiting human review.

# Nine-ray reduction of the remaining Gaussian-rational frame-function problem

AuthorityEffect: None.

This derivation for `FQ-GLEASON-QI3-FRAME-FUNCTIONS` is formalized in
`lean4/BornGaussianTomographyReduction.lean` (`BornFinite.GaussianTomography`)
and checked by `checks/independent/fq-gleason-qi3-tomography.py` and
`code/python/tests/test_fq_gleason_qi3_frame_functions.py`. It reduces the
general signed and nonnegative classification problems to exact nine-ray
residual-vanishing statements, characterizes the `(1+i)`-adic norm-parity
obstruction on primitive vectors in `Z[i]^3`, and constructs an explicit
global `{-1, 0, +1}`-valued `3`-adic zero-weight residual frame function `s3`
(together with the `{0, 1/3, 2/3}`-valued nonnegative non-quadratic frame
function `exoticQi3 = (1 + s3) / 3`) that resolves both the signed and
nonnegative quadratic-rigidity questions on `Q(i)^3` in the negative.

## 1. Carrier and ray invariance

Put K = Q(i), V = K^3, and N(v) = v* v, using conjugate transpose `*`.
A weight-c function is a map f: V minus {0} -> Q satisfying
f(u) + f(v) + f(w) = c on every pairwise orthogonal nonzero triple.
No regularity, boundedness, positivity, or effect additivity is assumed.

Every nonzero v can be completed to such a frame over K without taking square
roots: choose a coordinate vector a outside K v, subtract
v (v* a)/N(v), and solve the two independent orthogonality equations for a
nonzero third vector. The coefficients remain in K. Positive definiteness
gives nonzero positive rational squared norms. Replacing v by lambda v in the
same completion, for any nonzero lambda in K, and subtracting the two frame
equations shows in this model that f(lambda v) = f(v). Thus the formulation on
vectors already implies that f is a function on rays.

## 2. Quadratic frame identity without unit-vector normalization

For any Hermitian matrix rho over K, define

    q_rho(v) = (v* rho v) / N(v).

The numerator is fixed by conjugation and hence lies in Q; its denominator is
a positive rational. For a frame, let U have columns u, v, w and let
D = diag(N(u), N(v), N(w)). Orthogonality says U* U = D. The columns are
linearly independent: taking the inner product with each column in a linear
relation kills the other two terms and leaves a nonzero squared norm. Thus U
is invertible and U D^(-1) U* = I. Consequently,

    q_rho(u) + q_rho(v) + q_rho(w)
      = tr(rho U D^(-1) U*) = tr(rho).

This identity applies to frames whose rays have no unit representative in K.

## 3. Unique candidate from nine specified rays

Let e_1, e_2, e_3 be the coordinate vectors, and use these nine rays:

    e_j (1 <= j <= 3),
    e_j + e_k and e_j + i e_k (1 <= j < k <= 3).

For any rational-valued f, set

    d_j = f(e_j),
    a_jk = f(e_j + e_k) - (d_j + d_k)/2,
    b_jk = (d_j + d_k)/2 - f(e_j + i e_k).

Define rho_f by diagonal entries d_j, upper entries a_jk + i b_jk, and lower
entries a_jk - i b_jk. This is a Hermitian matrix over K. Direct substitution
gives

    q_rho(e_j) = d_j,
    q_rho(e_j + e_k) = (d_j + d_k + 2 a_jk)/2,
    q_rho(e_j + i e_k) = (d_j + d_k - 2 b_jk)/2.

Therefore rho_f agrees with f on the nine rays, and these equations uniquely
determine it. If f has weight one, its coordinate frame equation gives
tr(rho_f) = d_1 + d_2 + d_3 = 1.

Define the residual g_f = f - q_rho_f. By Section 2, it is a weight-zero
function, and it vanishes on the nine rays. Conversely any weight-zero
rational-valued g vanishing on these rays gives a weight-one function
f = 1/3 + g. Its candidate is I/3. If g is nonzero, f is not quadratic:
uniqueness of the candidate would force f = q_(I/3) = 1/3.

It follows that **every signed weight-one frame function is quadratic if and
only if every weight-zero rational-valued frame function vanishing on these
nine rays is zero** (`signed_rigidity_iff_zero_residual`).

## 4. The bounded residual is the exact nonnegative target

Every nonnegative weight-one function satisfies 0 <= f(v) <= 1: complete v
to a frame and use nonnegativity of its other two values.

For a fixed Hermitian rho with the coefficients above, the rational number

    C = sum_j |d_j| + sum_(j<k) (|a_jk| + |b_jk|)

bounds |q_rho(v)| for all nonzero v. Indeed each diagonal contribution is at
most |d_j| N(v). For each off-diagonal pair, its absolute contribution is at
most 2 (|a_jk| + |b_jk|) |v_j| |v_k|, which is at most
(|a_jk| + |b_jk|) N(v), by 2xy <= x^2 + y^2. Dividing their sum by N(v)
establishes the bound. Thus a nonnegative f has |g_f(v)| <= 1 + C, a rational
global bound.

In the other direction, suppose |g(v)| <= B for every ray, where B is a
nonnegative rational, and g is weight zero and zero on the nine rays. Put

    epsilon = 1 / (3 (B + 1)),   F(v) = 1/3 + epsilon g(v).

Then F has weight one, is rational-valued, and

    0 < 1 / (3 (B + 1)) <= F(v)
      <= (2 B + 1) / (3 (B + 1)) < 2/3.

These inequalities also cover B = 0; in that case g is zero and F is constant.
For any nonzero g, F is nonquadratic because its nine-ray candidate is I/3
and epsilon is nonzero. A real finite bound can always be enlarged to a
nonnegative rational bound, so the choice of a rational B loses nothing.

Therefore **every nonnegative weight-one frame function is quadratic if and
only if every bounded weight-zero rational-valued frame function vanishing
on the nine rays is zero** (`nonneg_rigidity_iff_bounded_zero_residual`).

For completeness, a weight-zero function bounded below by m is bounded above
by -2m, using g(v) = -g(u) - g(w) in a completion. A bound above by M similarly
gives a bound below by -2M. A one-sided global bound therefore suffices here.

## 5. Why a finite rank computation is not the global vanishing theorem

Let E be the free Q-vector space on all K-rays and an extra symbol t. Quotient
by the span of `[u] + [v] + [w] - t` for every frame, obtaining U. A linear
functional L: U -> Q with L(t) = 1 is a signed weight-one frame
function. The projector assignment

    T([v]) = v v* / N(v),   T(t) = I

is a well-defined surjection U -> Herm_3(K), by Section 2 and the nine-ray
reconstruction. Its target has Q-dimension nine.

The target operator space `HermForm3` is formalized in
`lean4/BornGaussianTomographyReduction.lean` with nondegenerate rational
Frobenius trace pairing `traceInner` (`traceInner_self_nonneg`,
`traceInner_self_eq_zero_iff`, `traceInner_ext`) and rank-1 ray projector map
`rayProj` satisfying `traceInner ρ (rayProj v) = quadRay ρ v`
(`traceInner_rayProj`), `rayProj_tr`, the orthogonal frame resolution of the
identity `rayProj u + rayProj v + rayProj w = HermForm3.id`
(`rayProj_frame_sum`), and explicit spanning of `HermForm3` by the nine
tomography ray projectors (`rayProj_nine_rays_span_hermForm3`).

If T were injective, the nondegenerate rational trace pairing would express
every L as tr(rho T(-)), giving the quadratic formula. Instead, `T` has a
nontrivial kernel that is separated constructively without basis extension: in
`HermForm3`, the projector of `witness_111 = (1, 1, 1)` decomposes as an exact
linear combination of the six real tomography projectors
(`rayProj_witness_111_decomp`):

    rayProj(1,1,1) = -(1/3) (rayProj(e_1) + rayProj(e_2) + rayProj(e_3))
                     + (2/3) (rayProj(e_1+e_2) + rayProj(e_1+e_3) + rayProj(e_2+e_3)),

so every quadratic Rayleigh function `quadRay ρ` satisfies the 7-ray linear
relation (`quadRay_witness_111_kernel_relation`)

    quadRay ρ (1,1,1) + (1/3) sum_j quadRay ρ e_j
                      - (2/3) sum_(j<k) quadRay ρ (e_j + e_k) = 0,

whereas the bounded `3`-adic zero-weight residual `s3` (and `exoticQi3`)
evaluates on the same 7-ray combination in `ker(T)` to `1 != 0` (and `1/3 != 0`,
`s3_witness_111_kernel_separation`).

## 6. `(1+i)`-Adic norm-parity structure on primitive vectors in `Z[i]^3`

Over `Z^3`, an odd-primitive integer vector `(a, c, e)` has `a^2 + c^2 + e^2`
 congruent to `1, 2, 3 (mod 4)` and never `0 (mod 4)` because each odd square is
`1 (mod 4)` and each even square is `0 (mod 4)`. Over `Z[i]^3`, a coordinate
`x + y i` has norm `x^2 + y^2 ≡ (x mod 2) + (y mod 2) (mod 4)`, taking values in
`{0, 1, 2}` modulo `4` (`gaussian_coord_norm_mod_four`). In particular, when both
`x` and `y` are odd, `x + y i` has `(1+i)`-valuation `1` (`(x + y) % 2 = 0`) and
norm `x^2 + y^2 ≡ 2 (mod 4)`.

Consequently (`primitive_gaussian_norm_mod_four_iff`), a `(1+i)`-primitive
vector `(a + b i, c + d i, e + g i) ∈ Z[i]^3` has total Hermitian norm divisible
by `4` if and only if two coordinates are `(1+i)`-odd (`norm % 2 = 1`) and the
remaining coordinate has `(1+i)`-valuation `1` (`norm % 4 = 2`). Explicit
witnesses formalized in `BornGaussianTomographyReduction.lean` are:

- `(1, 1, 1 + i)` with Hermitian norm `4` (`gaussian_norm_div_four_witness`),
- `(1 + 2 i, 1, 1 + i)` with Hermitian norm `8` (`gaussian_norm_eight_primitive_witness`).

## 7. Global bounded `3`-adic zero-weight residual `s3` and non-quadratic frame function `exoticQi3`

Although `2` ramifies in `Z[i]` as `-i (1+i)^2`—blocking any extension of the
`2`-adic real exotic frame function to `Q(i)^3` (`no_exotic_extension`)—the odd
prime `3 ≡ 3 (mod 4)` is **inert** in `Z[i]`. Every nonzero Gaussian rational
`z = x + i y ∈ Q(i)^×` therefore has **even** `3`-adic squared-norm valuation
(`v3Rat_normSq_even`):

    v_3(|z|^2) = v_3(x^2 + y^2) ≡ 0 (mod 2).

For any orthogonal frame `(u, v, w)` in `Q(i)^3`, the `3 × 3` determinant
identity (`detGVec_normSq_of_frame`) gives

    |det[u, v, w]|^2 = N(u) N(v) N(w),

so the sum of the `3`-adic norm valuations across any orthogonal frame is even
(`frame_v3Rat_sum_even`):

    v_3(N(u)) + v_3(N(v)) + v_3(N(w)) = v_3(|det[u, v, w]|^2) ≡ 0 (mod 2).

Every orthogonal frame in `Q(i)^3` therefore contains either `0` or `2` vectors
with odd `v_3(N(·))`.

Moreover, for any orthogonal pair `u ⊥ v` in `Q(i)^3`, the Lagrange-Gram
coordinate identity (`ortho_coord_identity_x`) holds:

    |u_x|^2 N(v) + |v_x|^2 N(u) + |u_y v_z - v_y u_z|^2 = N(u) N(v).

When both `v_3(N(u))` and `v_3(N(v))` are odd, `v_3(N(u) N(v))` and
`v_3(|u_y v_z - v_y u_z|^2)` are both even, whereas any nonzero term among
`|u_x|^2 N(v)` and `|v_x|^2 N(u)` has odd `3`-adic valuation. By ultrametric
cancellation (`four_term_v3Rat_cancel`, `lead3Coord_x_ortho_imp`), `u_x` is
`3`-leading in `u` (`v_3(|u_x|^2) < v_3(N(u))`) if and only if `v_x` is
`3`-leading in `v`, and their `3`-adic unit residue signs (`u3Rat`) cancel:

    u_3(|u_x|^2) u_3(N(u)) + u_3(|v_x|^2) u_3(N(v)) = 0.

The same equivalence and sign cancellation hold on the `y` and `z` coordinates
by cyclic coordinate rotation (`lead3Coord_y_ortho_imp`, `lead3Coord_z_ortho_imp`).
Defining `s3 : GVec → Q` (`s3`) by `0` when `v_3(N(u))` is even and by the
first `3`-leading coordinate's sign `u_3(|u_c|^2) u_3(N(u)) ∈ {-1, +1}` when
`v_3(N(u))` is odd yields:

1. Pair cancellation `s3(u) + s3(v) = 0` for any orthogonal pair with odd
   `v_3(N(u))` and `v_3(N(v))` (`s3_orthogonal_odd_cancel`), and therefore
   `s3(u) + s3(v) + s3(w) = 0` on every orthogonal frame in `Q(i)^3`
   (`s3_isZeroWeightFrameFunction`).
2. Scale invariance `s3(l • u) = s3(u)` for all `l ≠ 0` (`s3_smul`) and global
   boundedness `|s3(u)| ≤ 1` (`s3_isBoundedOnRays`).
3. Vanishing on all nine tomography rays (`s3_vanishes_on_nine_rays`), since
   those nine rays have norms `1` or `2` with `v_3(1) = v_3(2) = 0`.
4. Nonzero evaluation across `(1+i)`-primitive rays in distinct `(1+i)`-adic
   norm shells (`witness_111_primitive`, `witness_div_four_shell_primitive`,
   `witness_div_eight_shell_primitive`, `exists_nonzero_bounded_zero_residual`):
   `witness_111 = (1, 1, 1)` of norm `3` (`s3 = +1`),
   `witness_div_four_shell = (1+2i, 1+2i, 1+i)` of norm `12 = 4 · 3` (`s3 = -1`),
   and `witness_div_eight_shell = (1+4i, 1+2i, 1+i)` of norm `24 = 8 · 3`
   (`s3 = +1`).

Combining `exists_nonzero_bounded_zero_residual` with the reduction equivalences
`signed_rigidity_iff_zero_residual` and `nonneg_rigidity_iff_bounded_zero_residual`
establishes both `not_signed_quadratic_rigidity` and
`not_nonneg_quadratic_rigidity`, and gives the explicit `{0, 1/3, 2/3}`-valued
nonnegative non-quadratic frame function `exoticQi3(v) = (1 + s3(v)) / 3`
(`exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`).

## 8. Regularity, Continuity, and Field-Extension Hypotheses Eliminating `3`-Adic Residuals

Section 9 of `lean4/BornGaussianTomographyReduction.lean` formalizes three
complementary regularity and field-extension mechanisms that eliminate `s3`
(and, for projector linearity, every zero-weight residual vanishing on the nine
tomography rays):

1. **Archimedean Discontinuity / Local Oscillation at `tomo_e1 = (1, 0, 0)` (Suite 9A)**:
   For every integer `k >= 1`, the Gaussian-integer vectors
   `perturbPosInt k = (3k, 1, 1 + i)` and `perturbNegInt k = (3k, 1 + i, 1)`
   have squared norm `9k^2 + 3 = 3(3k^2 + 1)` (`v_3 = 1`, `u_3 = +1`), while
   their first `3`-leading coordinate `y` has norm `1` (`u_3 = +1`) and `2`
   (`u_3 = -1`) respectively (`s3_perturbPosInt`, `s3_perturbNegInt`). Their
   rescaled rays `perturbPosRay k = (1, 1/(3k), (1+i)/(3k))` and
   `perturbNegRay k = (1, (1+i)/(3k), 1/(3k))` have squared Euclidean/Hermitian
   distance `distSqVec (perturbPosRay k) tomo_e1 = 1 / (3k^2)` from
   `tomo_e1 = (1, 0, 0)` (`distSqVec_perturbPosRay_tomo_e1`,
   `distSqVec_perturbNegRay_tomo_e1`), yet evaluate to `s3 = +1` and `s3 = -1`
   (`s3_perturbPosRay`, `s3_perturbNegRay`) while `s3(tomo_e1) = 0`. Thus in
   every archimedean neighborhood `distSqVec v tomo_e1 < delta` (`delta > 0`),
   `s3` oscillates between `+1` and `-1` and `exoticQi3` oscillates between
   `2/3` and `0` (`s3_oscillates_near_tomo_e1`). Consequently neither `s3` nor
   `exoticQi3` is archimedean-continuous at `tomo_e1`
   (`not_archimedeanContinuousAt_s3_tomo_e1`,
   `not_archimedeanContinuousAt_exoticQi3_tomo_e1`), and any archimedean-continuous
   perturbation `f(v) = q_rho(v) + c * s3(v)` at `tomo_e1` forces `c = 0`
   (`s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`). The independent Python
   checks verify the analogous local oscillation at `tomo_e1` for `p = 7` via
   `(7k, 1 + i, 2 + i)` and `(7k, 2 + i, 1 + i)` of norm `49k^2 + 7 = 7(7k^2 + 1)`.
2. **Quadratic Field Extension `Q(i, sqrt(3))^3` Obstruction (Suite 9B)**:
   Over `Q(i)^3`, no scalar multiple of `witness_111 = (1, 1, 1)` has unit
   squared norm (`no_unit_norm_smul_witness_111_in_qi3`), and every orthogonal
   frame has even `v_3`-sum (`frame_v3Rat_sum_even`). Over the biquadratic
   extension `Q(i, sqrt(3))^3` (`GaussRatSqrt3`, `GVecSqrt3`), scaling
   `witness_111` by `1 / sqrt(3)` yields a unit-norm vector with even valuation
   `v_3(1) = 0` (`witness_111_unit_sqrt3_normSq`), and the embedded ray
   `witness_111_sqrt3 = (1, 1, 1)` (norm `3`, `v_3 = 1` odd) completes to an
   exact orthogonal frame (`isFrameSqrt3_witness_111_even_norms`) with
   `frameSqrt3_p = (1 + i + sqrt(3), 1 + i - sqrt(3), -2 - 2i)` (rational norm
   `18`, `v_3(18) = 2` even) and
   `frameSqrt3_q = (-1 + (1 - i)sqrt(3), -1 - (1 - i)sqrt(3), 2)` (rational norm
   `18`, `v_3(18) = 2` even), whose `v_3`-sum is `1 + 2 + 2 = 5` (odd). Hence
   any zero-weight frame function on `Q(i, sqrt(3))^3` that vanishes on vectors
   whose rational squared norm has even `v_3` must vanish on `witness_111`
   (`zero_on_witness_111_of_sqrt3_even_v3_vanishing`), and `s3` admits no such
   extension to `Q(i, sqrt(3))^3` (`no_s3_even_v3_extension_to_sqrt3`). The
   independent Python checks also verify the analogous `Q(i, sqrt(7))^3`
   orthogonal frame around `(1, 2, 1 + i)` with rational norms `(7, 245, 245)`
   and `7`-adic valuations `(1, 2, 2)`.
3. **General Operator-Space Projector-Linearity Criterion (Suite 9C)**:
   A ray function `f : GVec -> Q` factors linearly through the rank-1 projector
   map `rayProj : GVec -> HermForm3` (`FactorsThroughRayProjLinear`) if
   `f(v) = L(rayProj v)` for a `Q`-linear functional `L : HermForm3 -> Q`
   (`IsLinearOnHermForm3`). Since the nine tomography ray projectors span
   `HermForm3` (`rayProj_nine_rays_span_hermForm3`), every residual that vanishes
   on the nine tomography rays and factors linearly through `rayProj` vanishes
   identically on all nonzero vectors in `Q(i)^3`
   (`zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear`,
   `not_factorsThroughRayProjLinear_s3`), and a frame function on `Q(i)^3` has
   the quadratic Born form `quadRay rho` (`tr rho = 1`) if and only if it factors
   linearly through `rayProj` (`quadratic_rigidity_iff_factorsThroughRayProjLinear`).

## What is established (What this artifact supports)

- Nine-ray Hermitian tomography reconstruction (`tomography_matches_nine_rays`,
  `tomography_trace_one`), uniqueness (`tomography_unique`,
  `tomographyForm_quadRay`), zero-vector normalization (`quadRay_zero`,
  `normalizeAtZero_isFrameFunction`, `eq_quadRay_all_of_zero_at_zero`), and the
  non-unit orthogonal frame identity (`quadNum_orthogonal_weighted_sum`,
  `quadRay_frame_sum`, `quadRay_isFrameFunction`) are kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.
- The signed and nonnegative residual-reduction equivalences
  (`signed_rigidity_iff_zero_residual`,
  `nonneg_rigidity_iff_bounded_zero_residual`) together with the global
  quadratic ray bound (`abs_quadRay_le`, `nonneg_residual_is_bounded`) and
  one-sided-to-two-sided bound (`one_sided_lower_bound_implies_upper_bound`)
  are kernel-checked in `lean4/BornGaussianTomographyReduction.lean`.
- The operator-space Frobenius trace pairing (`traceInner`,
  `traceInner_self_nonneg`, `traceInner_self_eq_zero_iff`, `traceInner_ext`),
  rank-1 ray projectors (`rayProj`, `traceInner_rayProj`, `rayProj_tr`), frame
  resolution of the identity (`rayProj_frame_sum`), nine-ray projector
  spanning of `HermForm3` (`rayProj_nine_rays_span_hermForm3`), and constructive
  7-ray projector kernel decomposition and separation
  (`rayProj_witness_111_decomp`, `quadRay_witness_111_kernel_relation`,
  `s3_witness_111_kernel_separation`) are kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.
- The `(1+i)`-adic norm-parity characterization on primitive Gaussian-integer
  vectors (`gaussian_coord_norm_mod_four`,
  `primitive_gaussian_norm_mod_four_iff`, `gaussian_norm_div_four_witness`,
  `gaussian_norm_eight_primitive_witness`) is kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.
- The global bounded `{-1, 0, +1}`-valued `3`-adic zero-weight residual `s3`
  (`v3Rat_normSq_even`, `detGVec_normSq_of_frame`, `frame_v3Rat_sum_even`,
  `ortho_coord_identity_x`, `s3_orthogonal_odd_cancel`,
  `s3_isZeroWeightFrameFunction`, `s3_smul`, `s3_isBoundedOnRays`,
  `s3_vanishes_on_nine_rays`, `witness_111_primitive`,
  `witness_div_four_shell_primitive`, `witness_div_eight_shell_primitive`,
  `exists_nonzero_bounded_zero_residual`) and the explicit `{0, 1/3, 2/3}`-valued
  nonnegative non-quadratic frame function `exoticQi3`
  (`exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`,
  `not_signed_quadratic_rigidity`, `not_nonneg_quadratic_rigidity`) are
  kernel-checked in `lean4/BornGaussianTomographyReduction.lean`.
- The three elimination mechanisms in Section 9—archimedean oscillation and
  discontinuity at `tomo_e1` (`s3_oscillates_near_tomo_e1`,
  `not_archimedeanContinuousAt_s3_tomo_e1`,
  `not_archimedeanContinuousAt_exoticQi3_tomo_e1`,
  `s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`), the biquadratic field
  extension `Q(i, sqrt(3))^3` even-valuation frame obstruction
  (`no_unit_norm_smul_witness_111_in_qi3`, `witness_111_unit_sqrt3_normSq`,
  `isFrameSqrt3_witness_111_even_norms`,
  `zero_on_witness_111_of_sqrt3_even_v3_vanishing`,
  `no_s3_even_v3_extension_to_sqrt3`), and general operator-space projector
  linearity (`zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear`,
  `not_factorsThroughRayProjLinear_s3`,
  `quadratic_rigidity_iff_factorsThroughRayProjLinear`)—are kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.

## What is assumed

The stated field, Hermitian form, and all-frame equations are supplied by the
target. The Lean 4 theorems use rational linear, polynomial, biquadratic
(`Q(i, sqrt(3))`), and `3`-adic valuation arithmetic over `Q` and `Q(i)`.
Constructive separation of the projector kernel in Section 5 uses the explicit
bounded `3`-adic functional `s3` (`s3_witness_111_kernel_separation`), requiring
no infinite-dimensional basis extension. No continuum Gleason theorem is used.

## What this artifact does not support and what remains open

- **What it does not support**: This artifact does not classify the full vector
  space of all non-quadratic zero-weight residuals across every inert prime
  `p ≡ 3 (mod 4)` simultaneously without projector linearity, nor does it
  establish that archimedean continuity alone (without projector linearity or
  continuum completeness) eliminates every infinite linear combination of
  inert-prime residuals, nor does it close `FQ-GAP-BORN-UNIQUENESS-GLEASON`.
- **Narrowest defensible claim**: On `Q(i)^3`, the `3`-adic residual `s3` and
  `exoticQi3 = (1 + s3) / 3` settle both signed and nonnegative pure-frame
  quadratic rigidity in the negative, while `s3` is eliminated at `p = 3` by
  archimedean continuity at `tomo_e1`
  (`s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`) or by even-`v_3`
  extension to `Q(i, sqrt(3))^3` (`no_s3_even_v3_extension_to_sqrt3`), and all
  nine-ray-vanishing residuals are eliminated iff the frame function factors
  linearly through `rayProj`
  (`quadratic_rigidity_iff_factorsThroughRayProjLinear`).
- **Next test needed**: Formalize the parameterized inert-prime residual family
  `s_p` for general `p ≡ 3 (mod 4)` in Lean 4 and test whether archimedean
  continuity on `Q(i)^3` (without assuming `FactorsThroughRayProjLinear` a
  priori) suffices to force every bounded zero-weight residual on `Q(i)^3` to
  vanish.

