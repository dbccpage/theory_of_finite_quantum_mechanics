Status: AI-drafted, awaiting human review.

# FQ-GLEASON-QI3-FRAME-FUNCTIONS: finite obstructions, nine-ray reduction, and global `3`-adic non-quadratic residual

AuthorityEffect: None.

Baseline: `83667d6f0bd3a52898b915a0e68dcbadf443b6c1`. The original target retains
its `OPEN` DAG status (`AuthorityEffect: None`). All four existence and
quadratic-rigidity subquestions on `Q(i)^3` have kernel-checked Lean 4 theorems:
the `{0,1}`-valued and specified real-exotic extension questions have finite
obstruction certificates, and both the signed and nonnegative quadratic-rigidity
questions are settled in the negative by an explicit global `{-1, 0, +1}`-valued
`3`-adic zero-weight residual `s3` and the `{0, 1/3, 2/3}`-valued nonnegative
frame function `exoticQi3 = (1 + s3) / 3`.

## 1. Carrier and scope

Let \(K=\mathbb Q(i)\), with inner product
\(\langle u,v\rangle=\sum_j\overline{u_j}v_j\). A frame consists of three
nonzero pairwise orthogonal vectors. A frame function takes rational values and
sums to one on every frame. Positivity, continuity and dependence on residue
classes are not part of this definition.

The Lean carrier is `BornFinite.GaussianFrames.GVec`; `IsFrame` and
`IsFrameFunction` express these conditions. A total function on `GVec`
has an unconstrained value at zero, which plays no role on nonzero rays
(`GaussianTomography.normalizeAtZero_isFrameFunction`,
`GaussianTomography.eq_quadRay_all_of_zero_at_zero`). This is equivalent to
the target's function on nonzero vectors. Existing `frameFunction_smul` in
`BornGaussianFrameRays.lean` establishes constancy on nonzero scalar multiples.
Neither obstruction below needs to assume that property separately.

| Question in the original target | Result of this work | Evidence |
|---|---|---|
| Must every signed rational frame function be quadratic? | No (`s3` is a nonzero zero-weight residual vanishing on the 9 tomography rays) | `GaussianTomography.not_signed_quadratic_rigidity`, `GaussianTomography.exists_nonzero_bounded_zero_residual`, [Reduction note](fq-gleason-qi3-rigidity-reduction.md) |
| Must every nonnegative rational frame function be quadratic? | No (`exoticQi3 = (1 + s3) / 3` is a `{0, 1/3, 2/3}`-valued nonnegative non-quadratic frame function) | `GaussianTomography.not_nonneg_quadratic_rigidity`, `GaussianTomography.exoticQi3_isNonnegFrameFunction`, `GaussianTomography.exoticQi3_not_quadratic` |
| Does a \(\{0,1\}\)-valued frame function exist? | No | `NoColouring.no_zero_one_frame_function` |
| Does the repository's specified exotic \(\mathbb Q^3\) function extend? | No, even allowing signed values | `GaussianExtension.no_exotic_extension` |
| How does \((1+i)\)-adic norm-parity behave on primitive rays in \(\mathbb Z[i]^3\)? | Divisible by `4` iff two coordinates have odd norm and one has norm `2 (mod 4)` | `GaussianTomography.primitive_gaussian_norm_mod_four_iff`, `GaussianTomography.gaussian_norm_div_four_witness`, `GaussianTomography.gaussian_norm_eight_primitive_witness` |
| Which regularity, continuity, or field-extension hypotheses eliminate `s3`? | Archimedean continuity at `tomo_e1`, even-\(v_3\) extension to \(\mathbb Q(i,\sqrt{3})^3\), or operator-space projector linearity (`FactorsThroughRayProjLinear`) | `GaussianTomography.s3_oscillates_near_tomo_e1`, `GaussianTomography.s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`, `GaussianTomography.no_s3_even_v3_extension_to_sqrt3`, `GaussianTomography.quadratic_rigidity_iff_factorsThroughRayProjLinear` |

Lean names in the table have prefix `BornFinite.GaussianFrames` for
`NoColouring`, and prefix `BornFinite` for `GaussianExtension` and
`GaussianTomography`. The
[replay receipt](../../research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json)
records the actual build and axiom audit; a table entry alone is not a replay.

## 2. Binary values are excluded

Take all primitive integer triples in \([-2,2]^3\), selecting the representative
whose first nonzero coordinate is positive. There are 49 such rays, 138
orthogonal pairs and 26 orthogonal triples entirely inside this set. The
[independent checker](../../../checks/independent/fq-gleason-qi3-frame-functions.py)
enumerates these sets using integer gcd and dot products.

Write \(c_j=f(v_j)\). Every internal triple imposes
\(c_a+c_b+c_c=1\). Every orthogonal pair also imposes
\(c_a+c_b\leq1\): the nonzero integer cross product
\(w=v_a\times v_b\) completes the pair to a frame, and \(f(w)\geq0\)
follows from the binary-value hypothesis. The completing vector need not be
inside the box. Omitting these additional pair constraints is an error:
the internal-triples-only system has a binary solution.

The resulting finite binary system is inconsistent. The checker shows this in
this finite setting by exhaustive branching with unit propagation. A value one
forces all orthogonal neighbours to zero; a triple with two zero values forces
its last value to one; a triple already containing one forces its other values
to zero. Conflicting assignments close a branch. Otherwise the algorithm
branches on both values of an unassigned variable, so each branch strictly
decreases the number of unassigned variables and all assignments are covered.
It also independently verifies satisfying assignments for the triples-only and
pairs-only negative controls and compares small instances with direct
exhaustive enumeration.

`BornGaussianRationalNoColouring.lean` checks the concrete nonzero vectors and
orthogonality equations, derives the pair inequalities from actual frame
equations, and replays a finite binary case split using rational linear
arithmetic. Its theorem quantifies over every frame function on \(K^3\).
All vectors used are real, so the same finite argument also rules out a binary
frame function on all rational real rays. This does not contradict results
about the smaller rational unit sphere: a rational ray need not have a rational
unit representative.

## 3. The specified real exotic has no signed extension

For a primitive real integer vector, the existing exotic is
\(E(v)=(1+s(v))/3\). If precisely two coordinates are odd, \(s(v)=-1\)
when those two are congruent modulo four and \(s(v)=1\) otherwise.
In every other parity pattern, \(s(v)=0\). This is the function defined in
`BornRationalRayObstruction.lean`, not an arbitrary nonquadratic real frame
function.

Suppose an extension \(f\) existed and set \(g(v)=3f(v)-1\). Every frame
then has \(g(u)+g(v)+g(w)=0\), and every real prescribed ray has
\(g(v)=s(v)\). The
[certificate](../../../checks/independent/data/fq_gleason_qi3_extension.json)
lists 277 nonzero Gaussian-integer vectors, 210 orthogonal frames, and 19 real
prescribed values, together with integer coefficients.

For each frame row \(t=(a,b,c)\), let its coefficient be \(\lambda_t\);
for each prescribed real ray \(j\), let its coefficient be \(\mu_j\).
The certificate has the exact identities

\[
 \sum_{t:\,k\in t}\lambda_t+\mu_k=0\quad\text{for every listed vector }k,
 \qquad \sum_j\mu_j s(v_j)=32,
\]

where \(\mu_k=0\) outside the prescribed real rows. Taking this linear
combination of the frame and value equations gives \(0=32\), a contradiction.
All cancellation uses the actual listed vectors; no identification of distinct
vectors or symmetry assumption about \(f\) is needed.

The [independent checker](../../../checks/independent/fq-gleason-qi3-extension.py)
recomputes Hermitian orthogonality, nonzero-ness, the real parity values, and
every coefficient sum using integers. It uses no search solver or repository
imports. The Lean theorem `no_prescribed_frame_function` checks those actual
frame equations and combines them with the prescribed values.
`no_exotic_extension` derives the required real values directly from the
repository's `exotic` definition. No nonnegativity hypothesis occurs, so the
conclusion excludes both signed and nonnegative extensions of this example.

This certificate was discovered using permutation and conjugation orbits,
then expanded and reduced to equations on individual vectors. Discovery
symmetries are absent from the final proof. A finite consistent system, such
as the earlier smaller-box probe, never implied that an extension existed.

## 4. Nine-ray reduction, the global `3`-adic non-quadratic residual `s3`, and regularity/extension elimination

The [supplemental derivation](fq-gleason-qi3-rigidity-reduction.md) and its
Lean 4 formalization `lean4/BornGaussianTomographyReduction.lean` construct
the unique Hermitian trace-one candidate from the values on
\(e_j\), \(e_j+e_k\), and \(e_j+i e_k\) (`tomography_matches_nine_rays`,
`tomography_trace_one`, `tomography_unique`, `tomographyForm_quadRay`),
together with the operator-space Frobenius trace pairing, rank-1 ray
projector duality, and constructive 7-ray projector kernel decomposition and
separation (`traceInner_self_eq_zero_iff`, `traceInner_ext`,
`traceInner_rayProj`, `rayProj_frame_sum`, `rayProj_nine_rays_span_hermForm3`,
`rayProj_witness_111_decomp`, `quadRay_witness_111_kernel_relation`,
`s3_witness_111_kernel_separation`).
Subtracting its quadratic frame function (`quadRay_frame_sum`,
`quadRay_isFrameFunction`) leaves a zero-weight frame function vanishing on
those nine rays (`residual_is_zero_weight`, `residual_vanishes_on_nine_rays`).
Signed rigidity is equivalent to vanishing of every such residual
(`signed_rigidity_iff_zero_residual`); nonnegative rigidity is equivalent to
vanishing of every bounded residual (`nonneg_rigidity_iff_bounded_zero_residual`,
`nonneg_residual_is_bounded`, `one_sided_lower_bound_implies_upper_bound`).

Whereas \(2\) ramifies in \(\mathbb Z[i]\), the odd prime \(3\equiv 3\pmod 4\)
is inert in \(\mathbb Z[i]\), so every nonzero Gaussian rational \(z\in K^\times\)
has even \(3\)-adic squared-norm valuation \(v_3(|z|^2)\equiv 0\pmod 2\)
(`v3Rat_normSq_even`). On any orthogonal frame \((u,v,w)\),
\(|\det[u,v,w]|^2=N(u)N(v)N(w)\) (`detGVec_normSq_of_frame`), so
\(v_3(N(u))+v_3(N(v))+v_3(N(w))\) is even (`frame_v3Rat_sum_even`) and either
\(0\) or \(2\) vectors in the frame have odd \(v_3(N(\cdot))\). Using the
Lagrange-Gram coordinate identity (`ortho_coord_identity_x`), when two
orthogonal vectors \(u\perp v\) both have odd \(v_3(N(\cdot))\), they share the
same \(3\)-leading coordinates and opposite \(3\)-adic unit residue signs
(`lead3Coord_x_ortho_imp`, `s3_orthogonal_odd_cancel`). Consequently:

- `s3` is a global \(\{-1,0,+1\}\)-valued zero-weight frame function on \(K^3\)
  (`s3_isZeroWeightFrameFunction`, `s3_smul`, `s3_isBoundedOnRays`) that
  vanishes on all nine tomography rays (`s3_vanishes_on_nine_rays`) and takes
  nonzero values across \((1+i)\)-primitive rays in distinct \((1+i)\)-adic norm
  shells (`witness_111_primitive`, `witness_div_four_shell_primitive`,
  `witness_div_eight_shell_primitive`, `exists_nonzero_bounded_zero_residual`):
  \((1,1,1)\) (norm \(3\), \(s_3=+1\)), \((1+2i,1+2i,1+i)\) (norm \(12\),
  \(s_3=-1\)), and \((1+4i,1+2i,1+i)\) (norm \(24\), \(s_3=+1\)).
- Both signed and nonnegative quadratic rigidity on \(K^3\) fail
  (`not_signed_quadratic_rigidity`, `not_nonneg_quadratic_rigidity`), and
  `exoticQi3(v) = (1 + s3(v)) / 3` is an explicit global \(\{0,1/3,2/3\}\)-valued
  nonnegative non-quadratic frame function on \(K^3\)
  (`exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`).
- Section 9 of `lean4/BornGaussianTomographyReduction.lean` establishes three
  mechanisms that eliminate `s3` (and, under projector linearity, every
  nine-ray-vanishing residual):
  1. **Archimedean discontinuity at `tomo_e1 = (1, 0, 0)`**: the normalized
     rays \((1,\frac{1}{3k},\frac{1+i}{3k})\) and \((1,\frac{1+i}{3k},\frac{1}{3k})\)
     lie at squared distance \(\frac{1}{3k^2}\to 0\) from \(e_1\) while
     evaluating to \(s_3=+1\) and \(s_3=-1\) (`s3_oscillates_near_tomo_e1`), so
     neither `s3` nor `exoticQi3` is archimedean-continuous at `tomo_e1`
     (`not_archimedeanContinuousAt_s3_tomo_e1`,
     `not_archimedeanContinuousAt_exoticQi3_tomo_e1`), whereas every Hermitian
     Rayleigh quotient `quadRay ρ` is archimedean-continuous at `tomo_e1`
     (`archimedeanContinuousAt_quadRay_tomo_e1`), so `quadRay ρ + c • s3` is
     archimedean-continuous at `tomo_e1` if and only if \(c=0\)
     (`s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1`,
     `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`).
  2. **Biquadratic field extension \(\mathbb Q(i,\sqrt{p})^3\)**: adjoining
     \(\sqrt{p}\) rescales any vector \(u\in\mathbb Q(i)^3\) of norm \(p\neq 0\)
     to unit norm \(\frac{1}{\sqrt{p}}u\) (`unit_norm_in_sqrtP_of_normSqVec_eq`,
     `witness_111_unit_sqrt3_normSq`, excluded over \(\mathbb Q(i)^3\) at \(p=3\)
     by `no_unit_norm_smul_witness_111_in_qi3`) and completes \(u\) via the
     parameterized four-square SU(2) partner formula (`fourSquarePartner_ortho_and_normSqRatP`)
     to orthogonal partners of rational norm \(p^2 N(v_0)\) (`v_p = 2`). At
     \(p=3\), \((1,1,1)\) completes to partners of norm \(18=2\cdot 3^2\)
     (`isFrameSqrt3_witness_111_even_norms`), forcing any zero-weight frame
     function on \(\mathbb Q(i,\sqrt{3})^3\) that vanishes on even-\(v_3\) norm
     rays to vanish on \((1,1,1)\) (`zero_on_witness_111_of_sqrt3_even_v3_vanishing`,
     `no_s3_even_v3_extension_to_sqrt3`); at \(p=7\), \((1,2,1+i)\) completes to
     partners of norm \(245=5\cdot 7^2\) (`isFrameSqrt7_witness_p7_norms`).
  3. **Operator-space projector linearity**: a frame function on \(K^3\) has the
     quadratic Born form `quadRay ρ` (\(\operatorname{tr}\rho=1\)) if and only if
     it factors linearly through `rayProj : GVec → HermForm3`
     (`zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear`,
     `not_factorsThroughRayProjLinear_s3`,
     `quadratic_rigidity_iff_factorsThroughRayProjLinear`).

## What is established (What this artifact supports)

- The exact finite binary obstruction excludes \(\{0,1\}\)-valued frame
  functions on all \(K^3\) rays, and the same real witness applies to
  \(\mathbb Q^3\) (`NoColouring.no_zero_one_frame_function`).
- The exact linear certificate excludes any signed extension of the specified
  real exotic to \(K^3\) (`GaussianExtension.no_exotic_extension`).
- Nine-ray Hermitian tomography reconstruction, operator-space ray projector
  duality and nine-ray spanning of `HermForm3`, non-unit orthogonal frame sums,
  zero-vector normalization, the signed and bounded nonnegative
  residual-reduction equivalences, the \((1+i)\)-adic norm-parity
  characterization on primitive Gaussian-integer vectors, the explicit global
  `3`-adic zero-weight residual `s3` and nonnegative non-quadratic frame
  function `exoticQi3` (`not_signed_quadratic_rigidity`,
  `not_nonneg_quadratic_rigidity`), and the three Section 9 elimination
  theorems (`s3_oscillates_near_tomo_e1`,
  `archimedeanContinuousAt_quadRay_tomo_e1`,
  `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`,
  `no_s3_even_v3_extension_to_sqrt3`, `unit_norm_in_sqrtP_of_normSqVec_eq`,
  `fourSquarePartner_ortho_and_normSqRatP`, `isFrameSqrt7_witness_p7_norms`,
  `quadratic_rigidity_iff_factorsThroughRayProjLinear`) are formalized in
  `lean4/BornGaussianTomographyReduction.lean` and tested in
  `code/python/tests/test_fq_gleason_qi3_frame_functions.py`.

## What is assumed

The supplied Gaussian-rational vector space, its standard Hermitian form,
and frame normalization are the setting. Binary values are assumed only for
the binary obstruction. Agreement with the specified exotic is assumed only
for the extension obstruction. In Section 9, archimedean continuity at
`tomo_e1`, even-\(v_p\) extension to \(\mathbb Q(i,\sqrt{p})^3\), and
operator-space projector linearity (`FactorsThroughRayProjLinear`) are
analyzed as explicit hypotheses. These results do not derive the carrier from
earlier DAG nodes.

## What this artifact does not support and what remains open

- **What it does not support**: This artifact does not classify the entire space
  of non-quadratic residuals across all inert primes \(p\equiv 3\pmod 4\)
  without projector linearity, nor does it establish that archimedean continuity
  alone (without projector linearity or continuum completeness) eliminates every
  infinite linear combination of inert-prime residuals, nor does it close the
  parent Born-rule uniqueness gap `FQ-GAP-BORN-UNIQUENESS-GLEASON`.
- **Narrowest defensible claim**: On \(K^3=\mathbb Q(i)^3\), no \(\{0,1\}\)-valued
  frame function exists, the prescribed \(2\)-adic real exotic on \(\mathbb Q^3\)
  has no signed extension to \(K^3\), the \(3\)-adic residual \(s_3\) gives an
  explicit \(\{0,1/3,2/3\}\)-valued nonnegative non-quadratic frame function
  \(\operatorname{exoticQi3}=(1+s_3)/3\) on \(K^3\), and \(s_3\) is eliminated by
  archimedean continuity at `tomo_e1`, by even-\(v_3\) extension to
  \(\mathbb Q(i,\sqrt{3})^3\), or generally (for all nine-ray-vanishing
  residuals) by operator-space projector linearity (`FactorsThroughRayProjLinear`).
- **Next test needed**: Formalize the parameterized inert-prime residual family
  \(s_p\) for general \(p\equiv 3\pmod 4\) in Lean 4 and test whether archimedean
  continuity on \(\mathbb Q(i)^3\) (without assuming `FactorsThroughRayProjLinear`
  a priori) suffices to force every bounded zero-weight residual on
  \(\mathbb Q(i)^3\) to vanish.

Consequently the full target and its incoming gap route retain their original
statuses (`AuthorityEffect: None`). No result here establishes continuum
Gleason or the whole Born-rule derivation.

