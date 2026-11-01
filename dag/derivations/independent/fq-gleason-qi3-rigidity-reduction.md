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
   `not_archimedeanContinuousAt_exoticQi3_tomo_e1`), whereas every Hermitian
   Rayleigh quotient `quadRay rho` is archimedean-continuous at `tomo_e1`
   (`archimedeanContinuousAt_quadRay_tomo_e1`), so any perturbation
   `f(v) = quadRay rho v + c * s3(v)` is archimedean-continuous at `tomo_e1`
   if and only if `c = 0` (`s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`,
   `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`). The independent
   Python checks verify the analogous local oscillation at `tomo_e1` for `p = 7`
   via `(7k, 1 + i, 2 + i)` and `(7k, 2 + i, 1 + i)` of norm `49k^2 + 7 = 7(7k^2 + 1)`.
2. **Quadratic Field Extension `Q(i, sqrt(p))^3` Obstruction (Suite 9B)**:
   Over `Q(i)^3`, no scalar multiple of `witness_111 = (1, 1, 1)` has unit
   squared norm (`no_unit_norm_smul_witness_111_in_qi3`), and every orthogonal
   frame has even `v_3`-sum (`frame_v3Rat_sum_even`). Over the biquadratic
   extension `Q(i, sqrt(p))^3` (`GaussRatSqrt3`, `GVecSqrt3`), scaling any vector
   `u` of squared norm `p != 0` by `1 / sqrt(p)` yields a unit-norm vector with
   even valuation `v_p(1) = 0` (`unit_norm_in_sqrtP_of_normSqVec_eq`,
   `witness_111_unit_sqrt3_normSq`), and the parameterized four-square SU(2)
   partner formula (`fourSquarePartner_ortho_and_normSqRatP`) completes `u`
   using `alpha, beta in Q(i)` with `|alpha|^2 + |beta|^2 = p` to orthogonal
   partners of rational squared norm `p^2 * N(v_0)` (shifting `v_p` from `1` to
   `2`). At `p = 3`, `witness_111_sqrt3 = (1, 1, 1)` completes to an exact
   orthogonal frame (`isFrameSqrt3_witness_111_even_norms`) with
   `frameSqrt3_p = (1 + i + sqrt(3), 1 + i - sqrt(3), -2 - 2i)` and
   `frameSqrt3_q = (-1 + (1 - i)sqrt(3), -1 - (1 - i)sqrt(3), 2)` of rational
   norms `(3, 18, 18)` (`v_3 = (1, 2, 2)`), forcing any zero-weight frame
   function on `Q(i, sqrt(3))^3` that vanishes on even-`v_3` rational norms to
   vanish on `witness_111` (`zero_on_witness_111_of_sqrt3_even_v3_vanishing`,
   `no_s3_even_v3_extension_to_sqrt3`). At `p = 7`, `witness_p7 = (1, 2, 1 + i)`
   completes to an exact orthogonal frame in `Q(i, sqrt(7))^3` with rational
   norms `(7, 245, 245)` and `7`-adic valuations `(1, 2, 2)`
   (`isFrameSqrt7_witness_p7_norms`).
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
4. **Multi-Prime `7`-Adic Residual `s7`, Linear Independence, and Joint Elimination (Suite 9D)**:
   Since `7 ≡ 3 (mod 4)` is inert in `Z[i]`, every nonzero `z in Q(i)^x` has
   even `7`-adic norm valuation (`v7Rat_normSq_even`), every orthogonal frame in
   `Q(i)^3` has even `v_7`-sum (`frame_v7Rat_sum_even`), and the Legendre
   character `u7Rat` mod `7` (`isQrMod7`, `chi7Nat`) defines a second global
   `{-1, 0, +1}`-valued bounded zero-weight residual `s7 : GVec -> Q`
   (`s7_orthogonal_odd_cancel`, `s7_isZeroWeightFrameFunction`, `s7_smul`,
   `s7_isBoundedOnRays`, `s7_vanishes_on_nine_rays`) and a second `{0, 1/3, 2/3}`-valued
   nonnegative non-quadratic frame function `exoticQi7(v) = (1 + s7(v)) / 3`
   (`exoticQi7_isNonnegFrameFunction`, `exoticQi7_not_quadratic`). On the
   `(1+i)`-primitive witnesses `witness_111 = (1, 1, 1)` (norm `3`) and
   `witness_p7 = (1, 2, 1 + i)` (norm `7`, `witness_p7_primitive`), `(s3, s7)`
   satisfies Kronecker-delta duality (`s3_s7_dual_on_witnesses`):
   `s3(witness_111) = 1, s7(witness_111) = 0` and
   `s3(witness_p7) = 0, s7(witness_p7) = 1`. Thus the two-parameter combination
   `combResidual37 c3 c7 v = c3 * s3 v + c7 * s7 v` spans a 2-dimensional
   subspace of bounded zero-weight residuals vanishing on the 9 tomography rays
   (`combResidual37_isZeroWeightFrameFunction`,
   `combResidual37_vanishes_on_nine_rays`, `combResidual37_isBoundedOnRays`,
   `s3_s7_linearIndependent`), and `exoticComb37 c3 c7 v = (1 + combResidual37 c3 c7 v) / 3`
   defines a 2-parameter rational diamond (`|c3| + |c7| <= 1`) of nonnegative
   frame functions bounded in `[0, 2/3]` that are quadratic iff `c3 = 0 ∧ c7 = 0`
   (`exoticComb37_isNonnegFrameFunction`, `exoticComb37_quadratic_iff`). Near
   `tomo_e1 = (1, 0, 0)`, the `3`-adic
   subsequence `perturbPosRay (7*k)` / `perturbNegRay (7*k)` has norm
   `9(7k)^2 + 3 ≡ 3 (mod 7)` (`v_7 = 0`), so `s3 = +/- 1` and `s7 = 0`
   (`s7_perturbPosRay_seven_mul`, `s7_perturbNegRay_seven_mul`), whereas the
   `7`-adic perturbation `perturb7PosRay k` / `perturb7NegRay k` from
   `(7k, 1 + i, 2 + i)` and `(7k, 2 + i, 1 + i)` has norm
   `49k^2 + 7 ≡ k^2 + 1 != 0 (mod 3)` (`v_3 = 0`, `v_7 = 1`), so `s3 = 0` and
   `s7 = +/- 1` (`s7_perturb7PosRay`, `s7_perturb7NegRay`, `s3_perturb7PosRay`,
   `s3_perturb7NegRay`, `distSqVec_perturb7PosRay_tomo_e1`,
   `distSqVec_perturb7NegRay_tomo_e1`). These four ray sequences selectively
   oscillate `s3` and `s7` in every archimedean neighborhood of `tomo_e1`
   (`s3_s7_selective_oscillation_near_tomo_e1`,
   `not_archimedeanContinuousAt_s7_tomo_e1`,
   `not_archimedeanContinuousAt_exoticQi7_tomo_e1`), so
   `quadRay rho + combResidual37 c3 c7` (and `exoticComb37 c3 c7`) is
   archimedean-continuous at `tomo_e1` if and only if `c3 = 0` and `c7 = 0`
   (`combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
   `quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff`,
   `exoticComb37_archimedeanContinuousAt_tomo_e1_iff`). Similarly,
   because the `Q(i, sqrt(3))^3` frame norms `(3, 18, 18)` have even `v_7` and the
   `Q(i, sqrt(7))^3` frame norms `(7, 245, 245)` have even `v_3`
   (`cross_prime_frame_partner_norm_valuations_even`), neither single quadratic
   extension alone eliminates the other prime's residual, whereas joint
   even-`{v_3, v_7}` extension to both biquadratic fields forces `c3 = 0` and
   `c7 = 0` (`no_unit_norm_smul_witness_p7_in_qi3`,
   `zero_on_witness_p7_of_sqrt7_even_v7_vanishing`,
   `no_s7_even_v7_extension_to_sqrt7`,
   `joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37`), as does
   operator-space projector linearity together with the constructive 9-ray
   projector expansion and kernel separation of `witness_p7`
   (`rayProj_witness_p7_decomp`, `quadRay_witness_p7_kernel_relation`,
   `s7_witness_p7_kernel_separation`, `not_factorsThroughRayProjLinear_s7`,
   `factorsThroughRayProjLinear_combResidual37_iff`).
5. **Uniform Prime-Indexed `s_p` Family, Third Inert Prime `p = 11 ≡ 3 (mod 4)`, and Finite-Family Elimination (Suite 9E)**:
   For any natural parameter `p : ℕ`, `vpNat` and `ppPartNat` extract the `p`-adic
   exponent and `p`-prime part of `n : ℕ`, `chiPNat p m` evaluates the Euler-criterion
   quadratic character `((m mod p)^((p-1)/2) mod p == 1 ? 1 : -1)`, and `vpRat p`,
   `upRat p`, `isLeadPCoord p`, `coordSignP p` define the uniform `{-1, 0, +1}`-valued
   ray function `sp p : GVec -> Q`, which agrees identically with `s3` at `p = 3`
   (`sp_three_eq_s3`) and `s7` at `p = 7` (`sp_seven_eq_s7`), is bounded by `1` on
   all vectors (`sp_values`, `sp_abs_le_one`, `sp_isBoundedOnRays`), and vanishes on
   all nine tomography rays for every `p >= 3` (`sp_vanishes_on_nine_rays`). At the
   third inert prime `p = 11 ≡ 3 (mod 4)`, the purely real `(1+i)`-primitive vector
   `witness_p11 = (1, 3, 1)` of norm `11` (`witness_p11_primitive`,
   `witness_p11_normSq`) yields exact `3 × 3` Kronecker-delta duality for
   `(s3, s7, sp 11)` on `(witness_111, witness_p7, witness_p11)`
   (`s3_s7_sp11_dual_on_three_witnesses`), establishing 3D `Q`-linear independence of
   `combResidual3_7_11` (`s3_s7_sp11_linearIndependent`,
   `factorsThroughRayProjLinear_combResidual3_7_11_iff`), an exact 7-ray projector
   decomposition and kernel separation over the 6 real tomography rays
   (`rayProj_witness_p11_decomp`, `quadRay_witness_p11_kernel_relation`,
   `sp11_witness_p11_kernel_separation`), and a `Q(i, sqrt(11))^3` four-square SU(2)
   orthogonal frame (`isFrameSqrt11_witness_p11_norms`) with partner norms
   `1210 = 10 * 11^2` (`v_3 = 0, v_7 = 0, v_11 = 2`,
   `three_prime_frame_partner_norm_valuations_even`). More generally, for any `m : ℕ`
   and any finite system `InertPrimeResidualSystem m` of zero-weight bounded
   nine-ray-vanishing residuals `R : Fin m -> GVec -> Q` equipped with dual witnesses
   and selective oscillation ray pairs near `tomo_e1`, the finite linear combination
   `finCombResidual m R c` and `m`-parameter `ell^1`-cross-polytope family
   `finExoticComb m R c v = (1 + finCombResidual m R c v) / 3` (`sum_i |c_i| <= 1`)
   satisfy:
   - `finExoticComb m R c` is a nonnegative frame function bounded in `[0, 2/3]`
     (`finExoticComb_isNonnegFrameFunction`);
   - `{R i}_{i < m}` is `Q`-linearly independent, and `finExoticComb m R c` is
     quadratic iff `forall i, c i = 0` (`inertPrimeResidualSystem_linearIndependent`,
     `finExoticComb_quadratic_iff`);
   - `quadRay rho + finCombResidual m S.R c` (and `finExoticComb m S.R c`) is
     archimedean-continuous at `tomo_e1` iff `forall i, c i = 0`
     (`finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
     `quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff`,
     `finExoticComb_archimedeanContinuousAt_tomo_e1_iff`);
   - `finCombResidual m S.R c` is simultaneously eliminated iff `forall i, c i = 0`
     under operator-space projector linearity
     (`factorsThroughRayProjLinear_finCombResidual_iff`) or joint quadratic field
     extension (`joint_field_extension_eliminates_finCombResidual`), with concrete
     instantiation `inertSystem37` (`finCombResidual_inertSystem37_eq_combResidual37`).
6. **Dense-frame Piron / Cooke–Keane–Moran frame-rotation approximation, planar
   parallelogram law, and Nonnegativity + Archimedean Continuity Bridge (Subsection 9F)**:
   On `Q(i)^3`, any orthogonal pair `u ⊥ v` in a frame `(u, v, w)` generates a
   two-parameter family of rotated orthogonal frames `(rotPairU u v α β, rotPairV u v α β, w)`
   (`inner_rotPairU_rotPairV_eq_zero`, `normSqVec_rotPairU`, `normSqVec_rotPairV`,
   `isFrame_rotPair`) along which every frame function and zero-weight residual has
   invariant 2D subspace sum (`frameFunction_rotPair_sum`, `zeroWeight_rotPair_sum`).
   In operator space `HermForm3`, rank-1 ray projectors satisfy the exact two-point
   orthogonal parallelogram / convex-combination identity
   `T(u + v) + T(u - v) = (2 N(u) / (N(u) + N(v))) T(u) + (2 N(v) / (N(u) + N(v))) T(v)`
   (`rayProj_ortho_add_sub`, `factorsThroughRayProjLinear_ortho_add_sub`,
   `satisfiesOrthoParallelogramZero_of_factorsThroughRayProjLinear`). Every prime-indexed
   residual `sp p` is coordinate-sign symmetric (`sp_isCoordSignSymmetric`) and vanishes
   on all coordinate axes (`sp_vanishes_on_coord_axes`), whereas any coordinate-sign
   symmetric function vanishing on coordinate axes that also satisfies the orthogonal
   parallelogram zero law `SatisfiesOrthoParallelogramZero` vanishes on all of `Q(i)^3`
   in three steps (`zero_of_coordSignSymmetric_and_orthoParallelogram`); consequently
   `s3`, `s7`, and `sp 11` each explicitly violate `SatisfiesOrthoParallelogramZero`
   (`s3_not_satisfiesOrthoParallelogramZero`, `s7_not_satisfiesOrthoParallelogramZero`,
   `sp11_not_satisfiesOrthoParallelogramZero`). At a pure north-pole state (`f tomo_e1 = 1`),
   nonnegativity alone forces `f = 0` on the equatorial plane `e₁⊥`
   (`isFrame_hermCross`, `nonneg_eq_zero_on_perp_of_pole_one`), eliminating all
   `combResidual3_7_11 c3 c7 c11` perturbations of `quadRay (rayProj tomo_e1)` without
   continuity (`pure_pole_e1_nonneg_eliminates_combResidual3_7_11`), and yields the
   constructive Piron frame-rotation sum identity (`piron_frame_sum_identity`),
   Piron monotone descent `f(pironStep y lam) ≤ f(e₁ + y)` (`piron_descent_le_of_pole_one`),
   meridian complement `f(e₁ + y) + f(meridianOrtho y) = 1` (`meridian_complement_of_pole_one`),
   Pythagorean equatorial rotation norm and Born-weight invariance (`normSqVec_pythagEqRot`,
   `quadRay_rayProj_e1_pythagEqRot`), and Archimedean step density (`distSqVec_pironStep_inv_nat`,
   `exists_pironStep_within_delta`). Finally, every nonnegative zero-weight frame residual
   vanishes identically (`zero_of_nonneg_zeroWeightFrameFunction`), and nonnegative
   Archimedean-continuous frame rigidity to `FactorsThroughRayProjLinear` is equivalent to
   vanishing of bounded Archimedean-continuous nine-ray-vanishing zero-weight residuals
   (`nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual`).
7. **Two-Step Piron Tangent Algebra, Kelvin-Inverted Meridian Duality, Piron–Pythagorean
   Two-Sided Sandwich Squeeze, and Equatorial-Invariance vs. Parallelogram Separation
   (Subsection 9G)**:
   On the equatorial plane `e₁⊥` (`y.x = 0`), `eqOrtho(eqOrtho y) = -y`
   (`eqOrtho_eqOrtho_of_x_zero`), `pythagEqRot y 1 = eqOrtho y`
   (`pythagEqRot_one_eq_eqOrtho`, `pythagEqRot_one_twice_of_x_zero`), and the equatorial
   tangent step `eqTangentStep y t = y + t eqOrtho y` satisfies
   `pironStep y ⟨t, 0⟩ = e₁ + eqTangentStep y t` (`pironStep_eq_add_eqTangentStep`),
   `eqTangentStep_x_zero`, `normSqVec (eqTangentStep y t) = (1 + t^2) N(y)`
   (`normSqVec_eqTangentStep_of_x_zero`, `eqTangentStep_nonZero_of_x_zero`),
   `eqOrtho (eqTangentStep y t) = -t y + eqOrtho y` (`eqOrtho_eqTangentStep_of_x_zero`),
   and the exact two-step composition law
   `eqTangentStep (eqTangentStep y t) s = (1 - t s) y + (t + s) eqOrtho y`
   (`eqTangentStep_comp_of_x_zero`). Taking `s = -t` cancels the orthogonal component to
   `eqTangentStep (eqTangentStep y t) (-t) = (1 + t^2) y` (`eqTangentStep_cancel_of_x_zero`),
   yielding outward radial monotonicity
   `f(e₁ + (1 + t^2) y) ≤ f(e₁ + eqTangentStep y t) ≤ f(e₁ + y)`
   (`piron_radial_scale_le_of_pole_one`), while `t = s = 1` gives the `90°` step
   `eqTangentStep (eqTangentStep y 1) 1 = 2 eqOrtho y` (`eqTangentStep_one_one_of_x_zero`,
   `piron_two_step_eqOrtho_le_of_pole_one`). Using ray scale invariance (`frameFunction_smul`),
   the meridian partner `meridianOrtho y = -N(y) e₁ + y` rescales by `-1 / N(y)` to
   `e₁ + kelvinEq y` where `kelvinEq y = -(1 / N(y)) y` has inverted norm `1 / N(y)`
   (`kelvinEq_x_zero`, `normSqVec_kelvinEq`, `kelvinEq_nonZero`,
   `smul_meridianOrtho_eq_add_kelvinEq`), converting the meridian complement into the
   Kelvin-inversion duality `f(e₁ + y) + f(e₁ + kelvinEq y) = 1`
   (`meridian_kelvin_complement_of_pole_one`) and dualizing outward radial descent on
   `kelvinEq y` into upward inward radial monotonicity
   `f(e₁ + y) ≤ f(e₁ + (1 / (1 + t^2)) y)` (`piron_radial_inv_scale_ge_of_pole_one`).
   For every `k ≥ 2`, `pythagEqRot y k` is reached from the inward radial vector
   `((k^2 - 1) / (k^2 + 1)) y` by tangent step `t = 2k / (k^2 - 1)`
   (`pythagEqRot_eq_eqTangentStep_of_two_le`), and taking the opposite step `-t` from
   `pythagEqRot y k` lands on the outward radial vector `((k^2 + 1) / (k^2 - 1)) y`
   (`eqTangentStep_pythagEqRot_neg_of_x_zero`), sandwiching the rotated value between two
   purely radial scalings along the same equatorial direction `y`:
   `f(e₁ + ((k^2 + 1) / (k^2 - 1)) y) ≤ f(e₁ + pythagEqRot y k) ≤ f(e₁ + ((k^2 - 1) / (k^2 + 1)) y)`
   (`pythagEqRot_sandwich_of_pole_one`). Since both radial factors converge to `1` at rate
   `O(1 / k^2)` (`distSqVec_radial_scale`, `exists_pythagEqRot_radial_within_delta`),
   Archimedean continuity at `e₁ + y` squeezes both radial bounds to `f(e₁ + y)`
   (`pythagEqRot_archimedean_squeeze_of_pole_one`). Finally, `sp p (e₁ + y)` depends only
   on `N(y)` for `y ∈ e₁⊥` (`sp_e1_add_eq_of_normSqVec_eq`) and is invariant under all
   Pythagorean equatorial rotations (`sp_e1_add_pythagEqRot_eq`,
   `s3_pythagEqRot_invariant_tomo_e23`, `s7_pythagEqRot_invariant_v7`,
   `sp11_pythagEqRot_invariant_v11`), whereas `90°` rotational invariance (`k = 1`, whose
   square maps `e₁ + y` to `e₁ - y`) together with `SatisfiesOrthoParallelogramZero`
   forces `2 g(e₁ + y) = 0` (`orthoParallelogram_at_e1_iff_zero_of_pythagEqRot_one_invariant`,
   `nonneg_pole_perturbation_vanishes_on_equator`), explaining why equatorial rotational
   invariance around `e₁` alone does not eliminate `sp p` on `e₁ + y`.

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
  7-ray and 9-ray projector kernel decompositions and separations for
  `witness_111`, `witness_p7`, and `witness_p11`
  (`rayProj_witness_111_decomp`, `quadRay_witness_111_kernel_relation`,
  `s3_witness_111_kernel_separation`, `rayProj_witness_p7_decomp`,
  `quadRay_witness_p7_kernel_relation`, `s7_witness_p7_kernel_separation`,
  `rayProj_witness_p11_decomp`, `quadRay_witness_p11_kernel_relation`,
  `sp11_witness_p11_kernel_separation`) are kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.
- The `(1+i)`-adic norm-parity characterization on primitive Gaussian-integer
  vectors (`gaussian_coord_norm_mod_four`,
  `primitive_gaussian_norm_mod_four_iff`, `gaussian_norm_div_four_witness`,
  `gaussian_norm_eight_primitive_witness`) is kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.
- The uniform prime-indexed residual family `sp p` and its decidable modular
  specification `InertPrimeSpec p` (`sp_three_eq_s3`, `sp_seven_eq_s7`,
  `sp_isBoundedOnRays`, `sp_vanishes_on_nine_rays`, `inertPrimeSpec_eleven`,
  `vpRat_normSq_even`, `frame_vpRat_sum_even`, `sp_orthogonal_odd_cancel`,
  `sp_isZeroWeightFrameFunction`, `sp_smul`, `sp11_isZeroWeightFrameFunction`,
  `combResidual3_7_11_isZeroWeightFrameFunction`), the global bounded
  `{-1, 0, +1}`-valued `3`-adic, `7`-adic, and `11`-adic zero-weight residuals
  `s3`, `s7`, and `sp 11` (`v3Rat_normSq_even`, `v7Rat_normSq_even`,
  `detGVec_normSq_of_frame`, `frame_v3Rat_sum_even`, `frame_v7Rat_sum_even`,
  `ortho_coord_identity_x`, `s3_orthogonal_odd_cancel`,
  `s7_orthogonal_odd_cancel`, `s3_isZeroWeightFrameFunction`,
  `s7_isZeroWeightFrameFunction`, `s3_smul`, `s7_smul`, `s3_isBoundedOnRays`,
  `s7_isBoundedOnRays`, `s3_vanishes_on_nine_rays`, `s7_vanishes_on_nine_rays`,
  `witness_111_primitive`, `witness_p7_primitive`, `witness_p11_primitive`,
  `witness_div_four_shell_primitive`, `witness_div_eight_shell_primitive`,
  `exists_nonzero_bounded_zero_residual`, `s3_s7_dual_on_witnesses`,
  `s3_s7_sp11_dual_on_three_witnesses`, `s3_s7_linearIndependent`,
  `s3_s7_sp11_linearIndependent`), their 2D and 3D spans `combResidual37` and
  `combResidual3_7_11`, the arbitrary-`m` finite combination `finCombResidual m R c`
  and `ell^1`-cross-polytope family `finExoticComb m R c`
  (`finExoticComb_isNonnegFrameFunction`, `inertPrimeResidualSystem_linearIndependent`,
  `finExoticComb_quadratic_iff`), and the explicit `{0, 1/3, 2/3}`-valued
  nonnegative non-quadratic frame functions `exoticQi3`, `exoticQi7`, and
  `exoticComb37 c3 c7` (`exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`,
  `exoticQi7_isNonnegFrameFunction`, `exoticQi7_not_quadratic`,
  `exoticComb37_isNonnegFrameFunction`, `exoticComb37_quadratic_iff`,
  `not_signed_quadratic_rigidity`, `not_nonneg_quadratic_rigidity`) are
  kernel-checked in `lean4/BornGaussianTomographyReduction.lean`.
- The single-prime, two-prime, three-prime, and general `m`-prime elimination
  mechanisms in Section 9—selective archimedean oscillation and discontinuity at
  `tomo_e1` together with positive-control continuity of `quadRay rho`
  (`s3_oscillates_near_tomo_e1`, `s3_s7_selective_oscillation_near_tomo_e1`,
  `not_archimedeanContinuousAt_s3_tomo_e1`,
  `not_archimedeanContinuousAt_exoticQi3_tomo_e1`,
  `not_archimedeanContinuousAt_s7_tomo_e1`,
  `not_archimedeanContinuousAt_exoticQi7_tomo_e1`,
  `s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`,
  `combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
  `finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
  `archimedeanContinuousAt_quadRay_tomo_e1`,
  `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`,
  `quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff`,
  `quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff`,
  `exoticComb37_archimedeanContinuousAt_tomo_e1_iff`,
  `finExoticComb_archimedeanContinuousAt_tomo_e1_iff`), the biquadratic field
  extension `Q(i, sqrt(p))^3` even-valuation frame obstruction
  (`no_unit_norm_smul_witness_111_in_qi3`, `no_unit_norm_smul_witness_p7_in_qi3`,
  `witness_111_unit_sqrt3_normSq`, `isFrameSqrt3_witness_111_even_norms`,
  `zero_on_witness_111_of_sqrt3_even_v3_vanishing`,
  `no_s3_even_v3_extension_to_sqrt3`,
  `zero_on_witness_p7_of_sqrt7_even_v7_vanishing`,
  `no_s7_even_v7_extension_to_sqrt7`,
  `cross_prime_frame_partner_norm_valuations_even`,
  `three_prime_frame_partner_norm_valuations_even`,
  `joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37`,
  `joint_field_extension_eliminates_finCombResidual`,
  `unit_norm_in_sqrtP_of_normSqVec_eq`,
  `fourSquarePartner_ortho_and_normSqRatP`, `isFrameSqrt7_witness_p7_norms`,
  `isFrameSqrt11_witness_p11_norms`), general operator-space projector
  linearity (`zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear`,
  `not_factorsThroughRayProjLinear_s3`, `not_factorsThroughRayProjLinear_s7`,
  `factorsThroughRayProjLinear_combResidual37_iff`,
  `factorsThroughRayProjLinear_combResidual3_7_11_iff`,
  `factorsThroughRayProjLinear_finCombResidual_iff`,
  `quadratic_rigidity_iff_factorsThroughRayProjLinear`), the Subsection 9F
  planar frame-rotation pairs, operator-space parallelogram identity,
  coordinate-sign symmetry vs. orthogonal parallelogram zero propagation,
  pure-pole equatorial elimination, Piron monotone descent, Pythagorean
  equatorial rotations, and Nonnegativity + Archimedean Continuity Bridge
  (`inner_rotPairU_rotPairV_eq_zero`, `normSqVec_add_eq_normSqVec_sub_of_ortho`,
  `normSqVec_rotPairU`, `normSqVec_rotPairV`, `isFrame_rotPair`,
  `frameFunction_rotPair_sum`, `zeroWeight_rotPair_sum`,
  `rayProj_ortho_add_sub`, `factorsThroughRayProjLinear_ortho_add_sub`,
  `satisfiesOrthoParallelogramZero_of_factorsThroughRayProjLinear`,
  `sp_isCoordSignSymmetric`, `sp_vanishes_on_coord_axes`,
  `zero_of_coordSignSymmetric_and_orthoParallelogram`,
  `s3_not_satisfiesOrthoParallelogramZero`,
  `s7_not_satisfiesOrthoParallelogramZero`,
  `sp11_not_satisfiesOrthoParallelogramZero`, `isFrame_hermCross`,
  `nonneg_eq_zero_on_perp_of_pole_one`,
  `pure_pole_e1_nonneg_eliminates_combResidual3_7_11`,
  `piron_frame_sum_identity`, `piron_descent_le_of_pole_one`,
  `meridian_complement_of_pole_one`, `normSqVec_pythagEqRot`,
  `quadRay_rayProj_e1_pythagEqRot`, `distSqVec_pironStep_inv_nat`,
  `exists_pironStep_within_delta`, `zero_of_nonneg_zeroWeightFrameFunction`,
  `nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual`), and the
  Subsection 9G two-step Piron tangent algebra, Kelvin-inverted meridian
  duality, Piron–Pythagorean two-sided sandwich squeeze, and
  equatorial-invariance vs. orthogonal parallelogram separation
  (`eqOrtho_eqOrtho_of_x_zero`, `pythagEqRot_one_eq_eqOrtho`,
  `pythagEqRot_one_twice_of_x_zero`, `pironStep_eq_add_eqTangentStep`,
  `eqTangentStep_x_zero`, `normSqVec_eqTangentStep_of_x_zero`,
  `eqTangentStep_nonZero_of_x_zero`, `eqOrtho_eqTangentStep_of_x_zero`,
  `eqTangentStep_comp_of_x_zero`, `eqTangentStep_cancel_of_x_zero`,
  `eqTangentStep_one_one_of_x_zero`, `piron_radial_scale_le_of_pole_one`,
  `piron_two_step_eqOrtho_le_of_pole_one`, `frameFunction_smul`,
  `kelvinEq_x_zero`, `normSqVec_kelvinEq`, `kelvinEq_nonZero`,
  `smul_meridianOrtho_eq_add_kelvinEq`, `meridian_kelvin_complement_of_pole_one`,
  `piron_radial_inv_scale_ge_of_pole_one`,
  `pythagEqRot_eq_eqTangentStep_of_two_le`,
  `eqTangentStep_pythagEqRot_neg_of_x_zero`,
  `pythagEqRot_sandwich_of_pole_one`, `distSqVec_radial_scale`,
  `exists_pythagEqRot_radial_within_delta`,
  `pythagEqRot_archimedean_squeeze_of_pole_one`, `sp_e1_add_eq_of_normSqVec_eq`,
  `sp_e1_add_pythagEqRot_eq`, `s3_pythagEqRot_invariant_tomo_e23`,
  `s7_pythagEqRot_invariant_v7`, `sp11_pythagEqRot_invariant_v11`,
  `orthoParallelogram_at_e1_iff_zero_of_pythagEqRot_one_invariant`,
  `nonneg_pole_perturbation_vanishes_on_equator`)—are kernel-checked in
  `lean4/BornGaussianTomographyReduction.lean`.

## What is assumed

The stated field, Hermitian form, and all-frame equations are supplied by the
target. The Lean 4 theorems use rational linear, polynomial, biquadratic
(`Q(i, sqrt(p))`), and `p`-adic valuation arithmetic over `Q` and `Q(i)`.
Constructive separation of the projector kernel in Sections 5, 9D, and 9E uses
the explicit bounded `p`-adic functionals `s3`, `s7`, and `sp 11`
(`s3_witness_111_kernel_separation`, `s7_witness_p7_kernel_separation`,
`sp11_witness_p11_kernel_separation`), requiring no infinite-dimensional basis
extension. No continuum Gleason theorem is used.

## What this artifact does not support and what remains open

- **What it does not support**: This artifact does not classify the full
  infinite-dimensional vector space of all non-quadratic zero-weight residuals
  across every inert prime `p ≡ 3 (mod 4)` simultaneously without projector
  linearity, nor does it establish that every bounded Archimedean-continuous
  nine-ray-vanishing zero-weight residual on `Q(i)^3` vanishes identically
  without an additional regularity or parallelogram hypothesis, nor does it
  close `FQ-GAP-BORN-UNIQUENESS-GLEASON`.
- **Narrowest defensible claim**: On `Q(i)^3`, the uniform prime-indexed family
  `sp p` recovers `s3` and `s7` (`sp_three_eq_s3`, `sp_seven_eq_s7`), is a
  global `{-1, 0, +1}`-valued zero-weight frame residual vanishing on the 9
  tomography rays for every `p` satisfying `InertPrimeSpec p`
  (`sp_isZeroWeightFrameFunction`, `sp_smul`, `sp_isBoundedOnRays`,
  `sp_vanishes_on_nine_rays`, instantiated at `p ∈ {3, 7, 11}` via
  `inertPrimeSpec_eleven` and `sp11_isZeroWeightFrameFunction`), is coordinate-sign
  symmetric (`sp_isCoordSignSymmetric`) and invariant under all Pythagorean
  equatorial rotations on `e₁ + y` (`sp_e1_add_pythagEqRot_eq`,
  `s3_pythagEqRot_invariant_tomo_e23`, `s7_pythagEqRot_invariant_v7`,
  `sp11_pythagEqRot_invariant_v11`) while violating the operator-space
  orthogonal parallelogram zero law `SatisfiesOrthoParallelogramZero` that follows
  from `rayProj_ortho_add_sub` (`zero_of_coordSignSymmetric_and_orthoParallelogram`,
  `s3_not_satisfiesOrthoParallelogramZero`, `s7_not_satisfiesOrthoParallelogramZero`,
  `sp11_not_satisfiesOrthoParallelogramZero`,
  `orthoParallelogram_at_e1_iff_zero_of_pythagEqRot_one_invariant`), is eliminated
  at a pure pole `quadRay (rayProj tomo_e1)` by nonnegativity alone on the equator
  (`pure_pole_e1_nonneg_eliminates_combResidual3_7_11`,
  `nonneg_pole_perturbation_vanishes_on_equator`), and for any finite
  `InertPrimeResidualSystem m` is simultaneously eliminated (`forall i, c i = 0`)
  by archimedean continuity at `tomo_e1`, operator-space projector linearity, or
  joint quadratic field extension; moreover, general nonnegative
  Archimedean-continuous rigidity to `FactorsThroughRayProjLinear` is equivalent
  to vanishing of bounded Archimedean-continuous nine-ray-vanishing zero-weight
  residuals (`nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual`),
  with two-step Piron tangent composition (`eqTangentStep_comp_of_x_zero`,
  `eqTangentStep_cancel_of_x_zero`), Kelvin-inverted meridian duality
  (`meridian_kelvin_complement_of_pole_one`), outward and inward radial
  monotonicity (`piron_radial_scale_le_of_pole_one`,
  `piron_radial_inv_scale_ge_of_pole_one`), and the exact two-sided
  Piron–Pythagorean sandwich squeeze (`pythagEqRot_sandwich_of_pole_one`,
  `pythagEqRot_archimedean_squeeze_of_pole_one`) established in `Q(i)^3`.
- **Next test needed**: Combine equatorial rotational invariance around each of
  the three coordinate axes `e_1, e_2, e_3` (via `pythagEqRot_archimedean_squeeze_of_pole_one`
  and coordinate permutations) to test whether multi-axis Piron–Pythagorean
  invariance forces radial dependence `f(v) = F(|v_x|^2, |v_y|^2, |v_z|^2)` and
  vanishing of `sp p` on non-equatorial rays.




