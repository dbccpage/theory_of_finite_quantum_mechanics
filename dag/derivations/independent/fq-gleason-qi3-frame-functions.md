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
  4. **Multi-prime `7`-adic residual `s7`, linear independence, and joint elimination (Subsection 9D)**:
     the second inert prime \(p=7\equiv 3\pmod 4\) yields a second global
     \(\{-1,0,+1\}\)-valued bounded zero-weight residual `s7` on \(K^3\) via
     `v7Rat` and the Legendre character `u7Rat` mod \(7\)
     (`v7Rat_normSq_even`, `frame_v7Rat_sum_even`, `s7_orthogonal_odd_cancel`,
     `s7_isZeroWeightFrameFunction`, `s7_smul`, `s7_isBoundedOnRays`,
     `s7_vanishes_on_nine_rays`) and a second `{0, 1/3, 2/3}`-valued nonnegative
     non-quadratic frame function `exoticQi7 = (1 + s7) / 3`
     (`exoticQi7_isNonnegFrameFunction`, `exoticQi7_not_quadratic`). The pair
     \((s_3, s_7)\) satisfies Kronecker-delta duality on
     \(\operatorname{witness\_111}=(1,1,1)\) and
     \(\operatorname{witness\_p7}=(1,2,1+i)\) (`s3_s7_dual_on_witnesses`), so
     \(\operatorname{combResidual37} c_3 c_7 = c_3 s_3 + c_7 s_7\) spans a
     2-dimensional subspace of bounded zero-weight residuals vanishing on the 9
     tomography rays (`combResidual37_isZeroWeightFrameFunction`,
     `combResidual37_vanishes_on_nine_rays`, `combResidual37_isBoundedOnRays`,
     `s3_s7_linearIndependent`), inducing the 2-parameter rational polytope
     `exoticComb37 c3 c7 v = (1 + combResidual37 c3 c7 v) / 3` (\(|c_3|+|c_7|\le 1\))
     of nonnegative frame functions bounded in \([0,2/3]\) that are quadratic iff
     \(c_3=0\wedge c_7=0\) (`exoticComb37_isNonnegFrameFunction`,
     `exoticComb37_quadratic_iff`). Near `tomo_e1 = (1, 0, 0)`, the subsequence rays
     \(\operatorname{perturbPosRay}(7k)\), \(\operatorname{perturbNegRay}(7k)\)
     (with \(s_3=\pm 1, s_7=0\)) and the \(7\)-adic perturbation rays
     \(\operatorname{perturb7PosRay} k\), \(\operatorname{perturb7NegRay} k\)
     (with \(s_3=0, s_7=\pm 1\)) selectively oscillate \(s_3\) and \(s_7\)
     independently (`s3_s7_selective_oscillation_near_tomo_e1`), so
     `quadRay ρ + combResidual37 c3 c7` (and `exoticComb37 c3 c7`) is
     archimedean-continuous at `tomo_e1` if and only if \(c_3=0\wedge c_7=0\)
     (`combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
     `quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff`,
     `exoticComb37_archimedeanContinuousAt_tomo_e1_iff`). Likewise, because the
     \(\mathbb Q(i,\sqrt{3})^3\) and \(\mathbb Q(i,\sqrt{7})^3\) frame partner
     norms \((3, 18, 18)\) and \((7, 245, 245)\) have even cross-prime valuations
     (`cross_prime_frame_partner_norm_valuations_even`), neither single quadratic
     extension alone eliminates the other prime's residual, whereas joint
     even-\(\{v_3,v_7\}\) extension to both biquadratic fields forces
     \(c_3=0\wedge c_7=0\) (`zero_on_witness_p7_of_sqrt7_even_v7_vanishing`,
     `no_s7_even_v7_extension_to_sqrt7`,
     `joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37`), as does
     operator-space projector linearity together with the constructive 9-ray
     projector decomposition and kernel separation of \(\operatorname{witness\_p7}\)
     (`rayProj_witness_p7_decomp`, `quadRay_witness_p7_kernel_relation`,
     `s7_witness_p7_kernel_separation`, `not_factorsThroughRayProjLinear_s7`,
     `factorsThroughRayProjLinear_combResidual37_iff`).
  5. **Uniform prime-indexed `s_p` family, third inert prime `p = 11 ≡ 3 (mod 4)`, and finite-family elimination (Subsection 9E)**:
     `vpRat p`, `upRat p` (via Euler's criterion `chiPNat p`), `isLeadPCoord p`, and
     `coordSignP p` define the uniform \(\{-1,0,+1\}\)-valued family `sp p : GVec → ℚ`,
     which agrees identically with `s3` at \(p=3\) (`sp_three_eq_s3`) and `s7` at
     \(p=7\) (`sp_seven_eq_s7`), is bounded by \(1\) on all vectors (`sp_isBoundedOnRays`),
     and vanishes on the 9 tomography rays for all \(p\ge 3\) (`sp_vanishes_on_nine_rays`).
     At the third inert prime \(p=11\equiv 3\pmod 4\), the purely real
     \((1+i)\)-primitive vector \(\operatorname{witness\_p11}=(1,3,1)\) of norm \(11\)
     (`witness_p11_primitive`) yields \(3\times 3\) Kronecker-delta duality for
     \((s_3, s_7, s_{11})\) on \((\operatorname{witness\_111}, \operatorname{witness\_p7}, \operatorname{witness\_p11})\)
     (`s3_s7_sp11_dual_on_three_witnesses`), establishing 3D \(\mathbb Q\)-linear
     independence (`s3_s7_sp11_linearIndependent`,
     `factorsThroughRayProjLinear_combResidual3_7_11_iff`), an exact 7-ray
     projector decomposition and kernel separation over the 6 real tomography rays
     (`rayProj_witness_p11_decomp`, `quadRay_witness_p11_kernel_relation`,
     `sp11_witness_p11_kernel_separation`), and a \(\mathbb Q(i,\sqrt{11})^3\)
     four-square SU(2) orthogonal frame (`isFrameSqrt11_witness_p11_norms`) with
     partner norms \(1210=10\cdot 11^2\) (`three_prime_frame_partner_norm_valuations_even`).
     More generally, for any \(m\in\mathbb N\) and any `InertPrimeResidualSystem m`,
     the finite linear combination `finCombResidual m R c` and \(m\)-parameter
     \(\ell^1\)-cross-polytope family `finExoticComb m R c` (\(\sum_i |c_i|\le 1\))
     are nonnegative frame functions bounded in \([0,2/3]\) that are quadratic iff
     \(\forall i, c_i=0\) (`finExoticComb_isNonnegFrameFunction`,
     `inertPrimeResidualSystem_linearIndependent`, `finExoticComb_quadratic_iff`),
     and are simultaneously eliminated (\(\forall i, c_i=0\)) by archimedean
     continuity at `tomo_e1`
     (`finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
     `quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff`,
     `finExoticComb_archimedeanContinuousAt_tomo_e1_iff`), by operator-space
     projector linearity (`factorsThroughRayProjLinear_finCombResidual_iff`), or
     by joint quadratic field extension
     (`joint_field_extension_eliminates_finCombResidual`,
     `finCombResidual_inertSystem37_eq_combResidual37`).

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
  characterization on primitive Gaussian-integer vectors, the uniform
  prime-indexed residual family `sp p` and its decidable modular specification
  `InertPrimeSpec p` (`sp_three_eq_s3`, `sp_seven_eq_s7`, `sp_isBoundedOnRays`,
  `sp_vanishes_on_nine_rays`, `inertPrimeSpec_eleven`, `vpRat_normSq_even`,
  `frame_vpRat_sum_even`, `sp_orthogonal_odd_cancel`,
  `sp_isZeroWeightFrameFunction`, `sp_smul`, `sp11_isZeroWeightFrameFunction`,
  `combResidual3_7_11_isZeroWeightFrameFunction`), the explicit global
  `3`-adic, `7`-adic, and `11`-adic zero-weight residuals `s3`, `s7`, `sp 11`
  and nonnegative non-quadratic frame functions `exoticQi3`, `exoticQi7`, the
  third inert prime \(p=11\equiv 3\pmod 4\) witness `witness_p11 = (1, 3, 1)`
  (`witness_p11_primitive`, `s3_s7_sp11_dual_on_three_witnesses`,
  `s3_s7_sp11_linearIndependent`, `rayProj_witness_p11_decomp`,
  `quadRay_witness_p11_kernel_relation`, `sp11_witness_p11_kernel_separation`,
  `isFrameSqrt11_witness_p11_norms`,
  `three_prime_frame_partner_norm_valuations_even`), the 2-dimensional and
  arbitrary-\(m\) finite combinations `combResidual37 c3 c7`,
  `finCombResidual m R c` and \(\ell^1\)-cross-polytope families
  `exoticComb37 c3 c7`, `finExoticComb m R c` (`s3_s7_dual_on_witnesses`,
  `s3_s7_linearIndependent`, `exoticComb37_isNonnegFrameFunction`,
  `exoticComb37_quadratic_iff`, `finExoticComb_isNonnegFrameFunction`,
  `inertPrimeResidualSystem_linearIndependent`, `finExoticComb_quadratic_iff`),
  and the Section 9 single-prime, two-prime, three-prime, and \(m\)-prime
  elimination theorems (`s3_oscillates_near_tomo_e1`,
  `s3_s7_selective_oscillation_near_tomo_e1`,
  `archimedeanContinuousAt_quadRay_tomo_e1`,
  `quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff`,
  `quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff`,
  `exoticComb37_archimedeanContinuousAt_tomo_e1_iff`,
  `finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1`,
  `quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff`,
  `finExoticComb_archimedeanContinuousAt_tomo_e1_iff`,
  `no_s3_even_v3_extension_to_sqrt3`, `no_s7_even_v7_extension_to_sqrt7`,
  `cross_prime_frame_partner_norm_valuations_even`,
  `joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37`,
  `joint_field_extension_eliminates_finCombResidual`,
  `unit_norm_in_sqrtP_of_normSqVec_eq`,
  `fourSquarePartner_ortho_and_normSqRatP`, `isFrameSqrt7_witness_p7_norms`,
  `rayProj_witness_p7_decomp`, `quadRay_witness_p7_kernel_relation`,
  `s7_witness_p7_kernel_separation`,
  `quadratic_rigidity_iff_factorsThroughRayProjLinear`,
  `factorsThroughRayProjLinear_combResidual37_iff`,
  `factorsThroughRayProjLinear_combResidual3_7_11_iff`,
  `factorsThroughRayProjLinear_finCombResidual_iff`) are formalized in
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

- **What it does not support**: This artifact does not classify the entire
  infinite-dimensional space of non-quadratic residuals across all inert primes
  \(p\equiv 3\pmod 4\) simultaneously without projector linearity, nor does it
  bridge `Nat.Prime p ∧ p % 4 = 3` to the decidable finite modular specification
  `InertPrimeSpec p` for symbolic prime \(p\) without instantiating `p`, nor
  does it close the parent Born-rule uniqueness gap
  `FQ-GAP-BORN-UNIQUENESS-GLEASON`.
- **Narrowest defensible claim**: On \(K^3=\mathbb Q(i)^3\), no \(\{0,1\}\)-valued
  frame function exists, the prescribed \(2\)-adic real exotic on \(\mathbb Q^3\)
  has no signed extension to \(K^3\), the uniform prime-indexed family `sp p`
  recovers `s3` and `s7` (`sp_three_eq_s3`, `sp_seven_eq_s7`), is a global
  \(\{-1,0,+1\}\)-valued zero-weight frame residual vanishing on the 9 tomography
  rays for every `p` satisfying the decidable modular specification
  `InertPrimeSpec p` (`sp_isZeroWeightFrameFunction`, `sp_smul`,
  `sp_isBoundedOnRays`, `sp_vanishes_on_nine_rays`, instantiated at
  \(p\in\{3,7,11\}\) via `inertPrimeSpec_eleven` and
  `sp11_isZeroWeightFrameFunction`), yields \(3\times 3\) Kronecker-delta duality
  and 3D \(\mathbb Q\)-linear independence at \(p\in\{3,7,11\}\) via
  \(\operatorname{witness\_p11}=(1,3,1)\)
  (`s3_s7_sp11_dual_on_three_witnesses`, `s3_s7_sp11_linearIndependent`,
  `combResidual3_7_11_isZeroWeightFrameFunction`, `rayProj_witness_p11_decomp`,
  `isFrameSqrt11_witness_p11_norms`), and for any finite
  `InertPrimeResidualSystem m` of size \(m\), every finite combination
  `finCombResidual m S.R c` and \(m\)-parameter \(\ell^1\)-cross-polytope family
  `finExoticComb m S.R c` (`finExoticComb_isNonnegFrameFunction`,
  `inertPrimeResidualSystem_linearIndependent`, `finExoticComb_quadratic_iff`)
  is simultaneously eliminated (\(\forall i, c_i=0\)) by archimedean continuity
  at `tomo_e1` (`quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff`,
  `finExoticComb_archimedeanContinuousAt_tomo_e1_iff`), by operator-space
  projector linearity (`factorsThroughRayProjLinear_finCombResidual_iff`), or by
  joint quadratic field extension (`joint_field_extension_eliminates_finCombResidual`).
- **Next test needed**: Formalize the implication from symbolic primality
  `Nat.Prime p ∧ p % 4 = 3` to `InertPrimeSpec p` in Lean 4 (using Euler's
  criterion in `ZMod p`) and instantiate `inertSystem3_7_11 : InertPrimeResidualSystem 3`
  with product-scaled `231 * k` selective perturbation rays in Lean 4.

Consequently the full target and its incoming gap route retain their original
statuses (`AuthorityEffect: None`). No result here establishes continuum
Gleason or the whole Born-rule derivation.

