# FQ-GLEASON-QI3-FRAME-FUNCTIONS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E4**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let V = Q(i)^3 with the standard Hermitian form. Decide whether every function f from the nonzero vectors of V to Q with f(u) + f(v) + f(w) = 1 for every orthogonal triple of nonzero vectors has the form f(v) = \<v, rho v\>/\<v, v\> for a Hermitian trace-one 3 x 3 matrix rho over Q(i), or exhibit one that does not; state separately the signed, nonnegative and {0,1}-valued variants, and whether the non-quadratic Q^3 frame function extends to Q(i)^3.

## Grade

Evidence grade **E4** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 13
- cited Lean, Rust or Python symbols found in their in-repo files: 186
- distinct cited Lean declarations covered by a current replay receipt: 174
- counted in-repo runnable tests: 13
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: none: all E4 conditions hold

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The {0,1}-valued variant is excluded by a finite real-ray obstruction. The specific exotic Q^3 frame function has no signed extension, by an exact finite linear certificate. Nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, the signed and bounded nonnegative residual-reduction equivalences, the (1+i)-adic norm-parity characterization on primitive Gaussian-integer vectors, the explicit global {-1, 0, +1}-valued 3-adic and 7-adic zero-weight residuals s3 and s7 and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame functions exoticQi3 = (1 + s3) / 3 and exoticQi7 = (1 + s7) / 3 (settling both signed and nonnegative quadratic rigidity on Q(i)^3 in the negative), their dual Kronecker-delta evaluation on (witness_111, witness_p7) and 2D linear independence (combResidual37), the uniform prime-indexed inert residual family sp p (with InertPrimeSpec p, p = 11 instance sp11, 3D subspace combResidual3_7_11, and arbitrary finite m-prime InertPrimeResidualSystem m), Section 9 elimination theorems (selective cross-prime archimedean discontinuity at tomo_e1, joint Q(i, sqrt(p))^3 even-valuation frame obstruction, and operator-space projector linearity quadratic_rigidity_iff_factorsThroughRayProjLinear / factorsThroughRayProjLinear_finCombResidual_iff), and Subsection 9F planar frame-rotation identities, the orthogonal parallelogram law SatisfiesOrthoParallelogramZero (refuted on s3, s7, sp11 and eliminating all coordinate-sign-symmetric zero-weight residuals), Piron's meridian-descent inequality and dense Pythagorean rational circle step (exists_pironStep_within_delta), and the nonnegativity/continuity bridge (nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual) are formalized in lean4/BornGaussianTomographyReduction.lean. Unconditional vanishing of all archimedean-continuous bounded zero-weight residuals on Q(i)^3 without coordinate-sign symmetry or projector linearity and closure of FQ-GAP-BORN-UNIQUENESS-GLEASON remain open.

## Source status

Finite obstructions, nine-ray reductions, global 3-adic and 7-adic non-quadratic residuals (s3, s7), 2D linear independence (combResidual37), uniform prime-indexed inert residual family sp p (with InertPrimeSpec p, p = 11 instance sp11, 3D subspace combResidual3_7_11, and arbitrary finite m-prime InertPrimeResidualSystem m), and Section 9 regularity/extension/projector-linearity/parallelogram/Piron elimination: no {0,1}-valued frame function on Q(i)^3, no signed extension of the specified exotic Q^3 function, and in BornGaussianTomographyReduction.lean exact nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, signed and bounded nonnegative residual-reduction equivalences, (1+i)-adic norm-parity characterization on primitive Gaussian-integer vectors, the explicit global {-1, 0, +1}-valued 3-adic, 7-adic, and uniform p-adic zero-weight residuals s3, s7, sp p and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame functions exoticQi3 = (1 + s3) / 3 and exoticQi7 = (1 + s7) / 3 (settling both signed and nonnegative quadratic rigidity on Q(i)^3 in the negative), Kronecker-delta evaluation and linear independence across arbitrary finite m-prime systems (inertPrimeResidualSystem_linearIndependent), joint elimination mechanisms (selective cross-prime archimedean oscillation and discontinuity at tomo_e1, joint Q(i, sqrt(p))^3 even-valuation frame obstruction, and operator-space projector linearity quadratic_rigidity_iff_factorsThroughRayProjLinear / factorsThroughRayProjLinear_finCombResidual_iff), and Subsection 9F planar frame-rotation identities, orthogonal parallelogram law SatisfiesOrthoParallelogramZero (refuted on s3, s7, sp11 and eliminating all coordinate-sign-symmetric zero-weight residuals), Piron's meridian-descent inequality and dense Pythagorean rational circle step (exists_pironStep_within_delta), and the nonnegativity/continuity bridge (nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual). Exact independent checks, runnable pytest suite, and scoped Lean declarations are linked; see the replay receipt for build evidence.

## Review

- PFP review: [dag/research/fq_gleason_qi3_assessment.json](../../../dag/research/fq_gleason_qi3_assessment.json); file present and sha256 matches the node's record: yes; verdict `scoped_obstructions_and_tomography_reduction_reviewed`; scope effect `consistent`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: No {0,1}-valued frame function exists on all Q(i)^3 rays; the specified exotic Q^3 frame function has no signed extension to Q(i)^3; nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, signed and bounded nonnegative residual-reduction equivalences, (1+i)-adic norm-parity characterization, the explicit global {-1, 0, +1}-valued 3-adic and 7-adic zero-weight residuals s3 and s7 and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame functions exoticQi3 = (1 + s3) / 3 and exoticQi7 = (1 + s7) / 3, their dual witness evaluation and 2D linear independence (combResidual37), the uniform prime-indexed inert residual family sp p (with InertPrimeSpec p, p = 11 instance sp11, 3D subspace combResidual3_7_11, and finite m-prime InertPrimeResidualSystem m), Section 9 elimination mechanisms (selective cross-prime archimedean discontinuity at tomo_e1, joint Q(i, sqrt(p))^3 even-valuation frame obstruction, and operator-space projector linearity), and Subsection 9F planar frame-rotation identities, orthogonal parallelogram law SatisfiesOrthoParallelogramZero (refuted on s3, s7, sp11 and eliminating all coordinate-sign-symmetric zero-weight residuals), Piron's meridian-descent inequality and dense Pythagorean rational circle step (exists_pironStep_within_delta), and the nonnegativity/continuity bridge (nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual) are kernel-checked in Lean 4.
  - does not support: Unconditional vanishing of all archimedean-continuous bounded zero-weight residuals on Q(i)^3 without coordinate-sign symmetry or projector linearity, continuum Gleason, or closure of FQ-GAP-BORN-UNIQUENESS-GLEASON.
  - next test: Test whether archimedean continuity and boundedness on Q(i)^3 (or dense-frame Piron/Cooke-Keane-Moran meridian descent along rational unit spheres) force every bounded zero-weight residual on Q(i)^3 to satisfy the orthogonal parallelogram law or vanish identically without assuming coordinate-sign symmetry or projector linearity.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianMod2ClassRigidity.lean`

- file: [lean4/BornGaussianMod2ClassRigidity.lean](../../../lean4/BornGaussianMod2ClassRigidity.lean)
- sha256 (`bytes`): `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornGaussianMod2ClassRigidity`): recorded sha256 `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianMod2ClassRigidity`
- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalExtensionObstruction.lean`

- file: [lean4/BornGaussianRationalExtensionObstruction.lean](../../../lean4/BornGaussianRationalExtensionObstruction.lean)
- sha256 (`bytes`): `aa68f3cdf925dcbe35b7aa2d23f51bc9bf1171963f060c8540988e5c77b1fb33`
- cited in: node.lean, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianRationalExtensionObstruction), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianRationalExtensionObstruction`): recorded sha256 `aa68f3cdf925dcbe35b7aa2d23f51bc9bf1171963f060c8540988e5c77b1fb33` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalExtensionObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianExtension.no_exotic_extension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianExtension.no_exotic_extension` |
| `BornFinite.GaussianExtension.no_prescribed_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianExtension.no_prescribed_frame_function` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalNoColouring.lean`

- file: [lean4/BornGaussianRationalNoColouring.lean](../../../lean4/BornGaussianRationalNoColouring.lean)
- sha256 (`bytes`): `fffb58fbf26650d8e27fcabb2935937eda3d919dee03d9b481a21b67ea0ac778`
- cited in: node.lean, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianRationalNoColouring), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianRationalNoColouring`): recorded sha256 `fffb58fbf26650d8e27fcabb2935937eda3d919dee03d9b481a21b67ea0ac778` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalNoColouring`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianTomographyReduction.lean`

- file: [lean4/BornGaussianTomographyReduction.lean](../../../lean4/BornGaussianTomographyReduction.lean)
- sha256 (`bytes`): `2a42834c901ade5f1a8831ff0c4339a109d08f5af8dc0132c24f79fab734321f`
- cited in: node.lean, node.source, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianTomographyReduction), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianTomographyReduction`): recorded sha256 `2a42834c901ade5f1a8831ff0c4339a109d08f5af8dc0132c24f79fab734321f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianTomographyReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.abs_quadRay_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.abs_quadRay_le` |
| `BornFinite.GaussianTomography.archimedeanContinuousAt_quadRay_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.archimedeanContinuousAt_quadRay_tomo_e1` |
| `BornFinite.GaussianTomography.combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1` |
| `BornFinite.GaussianTomography.combResidual37_isBoundedOnRays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.combResidual37_isBoundedOnRays` |
| `BornFinite.GaussianTomography.combResidual37_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.combResidual37_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.combResidual37_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.combResidual37_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.combResidual3_7_11_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.combResidual3_7_11_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.cross_prime_frame_partner_norm_valuations_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.cross_prime_frame_partner_norm_valuations_even` |
| `BornFinite.GaussianTomography.detGVec_normSq_of_frame` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.detGVec_normSq_of_frame` |
| `BornFinite.GaussianTomography.distSqVec_perturb7NegRay_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.distSqVec_perturb7NegRay_tomo_e1` |
| `BornFinite.GaussianTomography.distSqVec_perturb7PosRay_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.distSqVec_perturb7PosRay_tomo_e1` |
| `BornFinite.GaussianTomography.distSqVec_perturbNegRay_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.distSqVec_perturbNegRay_tomo_e1` |
| `BornFinite.GaussianTomography.distSqVec_perturbPosRay_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.distSqVec_perturbPosRay_tomo_e1` |
| `BornFinite.GaussianTomography.distSqVec_pironStep_inv_nat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.distSqVec_pironStep_inv_nat` |
| `BornFinite.GaussianTomography.eq_quadRay_all_of_zero_at_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.eq_quadRay_all_of_zero_at_zero` |
| `BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual` |
| `BornFinite.GaussianTomography.exists_pironStep_within_delta` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exists_pironStep_within_delta` |
| `BornFinite.GaussianTomography.exoticComb37_archimedeanContinuousAt_tomo_e1_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticComb37_archimedeanContinuousAt_tomo_e1_iff` |
| `BornFinite.GaussianTomography.exoticComb37_isNonnegFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticComb37_isNonnegFrameFunction` |
| `BornFinite.GaussianTomography.exoticComb37_quadratic_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticComb37_quadratic_iff` |
| `BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction` |
| `BornFinite.GaussianTomography.exoticQi3_not_quadratic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi3_not_quadratic` |
| `BornFinite.GaussianTomography.exoticQi7_isNonnegFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi7_isNonnegFrameFunction` |
| `BornFinite.GaussianTomography.exoticQi7_not_quadratic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi7_not_quadratic` |
| `BornFinite.GaussianTomography.factorsThroughRayProjLinear_combResidual37_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.factorsThroughRayProjLinear_combResidual37_iff` |
| `BornFinite.GaussianTomography.factorsThroughRayProjLinear_combResidual3_7_11_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.factorsThroughRayProjLinear_combResidual3_7_11_iff` |
| `BornFinite.GaussianTomography.factorsThroughRayProjLinear_finCombResidual_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.factorsThroughRayProjLinear_finCombResidual_iff` |
| `BornFinite.GaussianTomography.factorsThroughRayProjLinear_ortho_add_sub` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.factorsThroughRayProjLinear_ortho_add_sub` |
| `BornFinite.GaussianTomography.finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1` |
| `BornFinite.GaussianTomography.finCombResidual_inertSystem37_eq_combResidual37` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.finCombResidual_inertSystem37_eq_combResidual37` |
| `BornFinite.GaussianTomography.finExoticComb_archimedeanContinuousAt_tomo_e1_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.finExoticComb_archimedeanContinuousAt_tomo_e1_iff` |
| `BornFinite.GaussianTomography.finExoticComb_isNonnegFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.finExoticComb_isNonnegFrameFunction` |
| `BornFinite.GaussianTomography.finExoticComb_quadratic_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.finExoticComb_quadratic_iff` |
| `BornFinite.GaussianTomography.fourSquarePartner_ortho_and_normSqRatP` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.fourSquarePartner_ortho_and_normSqRatP` |
| `BornFinite.GaussianTomography.frameFunction_rotPair_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.frameFunction_rotPair_sum` |
| `BornFinite.GaussianTomography.frame_v3Rat_sum_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.frame_v3Rat_sum_even` |
| `BornFinite.GaussianTomography.frame_v7Rat_sum_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.frame_v7Rat_sum_even` |
| `BornFinite.GaussianTomography.frame_vpRat_sum_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.frame_vpRat_sum_even` |
| `BornFinite.GaussianTomography.gaussian_coord_norm_mod_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_coord_norm_mod_four` |
| `BornFinite.GaussianTomography.gaussian_norm_div_four_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_norm_div_four_witness` |
| `BornFinite.GaussianTomography.gaussian_norm_eight_primitive_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_norm_eight_primitive_witness` |
| `BornFinite.GaussianTomography.inertPrimeResidualSystem_linearIndependent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inertPrimeResidualSystem_linearIndependent` |
| `BornFinite.GaussianTomography.inertPrimeSpec_eleven` | yes | yes | yes | propext | `#print axioms BornFinite.GaussianTomography.inertPrimeSpec_eleven` |
| `BornFinite.GaussianTomography.inner_applyVec_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inner_applyVec_im_zero` |
| `BornFinite.GaussianTomography.inner_applyVec_re_eq_quadNum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inner_applyVec_re_eq_quadNum` |
| `BornFinite.GaussianTomography.inner_rotPairU_rotPairV_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inner_rotPairU_rotPairV_eq_zero` |
| `BornFinite.GaussianTomography.isFrameSqrt11_witness_p11_norms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.isFrameSqrt11_witness_p11_norms` |
| `BornFinite.GaussianTomography.isFrameSqrt3_witness_111_even_norms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.isFrameSqrt3_witness_111_even_norms` |
| `BornFinite.GaussianTomography.isFrameSqrt7_witness_p7_norms` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.isFrameSqrt7_witness_p7_norms` |
| `BornFinite.GaussianTomography.isFrame_hermCross` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.isFrame_hermCross` |
| `BornFinite.GaussianTomography.isFrame_rotPair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.isFrame_rotPair` |
| `BornFinite.GaussianTomography.joint_field_extension_eliminates_finCombResidual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.joint_field_extension_eliminates_finCombResidual` |
| `BornFinite.GaussianTomography.joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37` |
| `BornFinite.GaussianTomography.meridian_complement_of_pole_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.meridian_complement_of_pole_one` |
| `BornFinite.GaussianTomography.no_s3_even_v3_extension_to_sqrt3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.no_s3_even_v3_extension_to_sqrt3` |
| `BornFinite.GaussianTomography.no_s7_even_v7_extension_to_sqrt7` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.no_s7_even_v7_extension_to_sqrt7` |
| `BornFinite.GaussianTomography.no_unit_norm_smul_witness_111_in_qi3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.no_unit_norm_smul_witness_111_in_qi3` |
| `BornFinite.GaussianTomography.no_unit_norm_smul_witness_p7_in_qi3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.no_unit_norm_smul_witness_p7_in_qi3` |
| `BornFinite.GaussianTomography.nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_continuous_rigidity_iff_continuous_bounded_zero_residual` |
| `BornFinite.GaussianTomography.nonneg_eq_zero_on_perp_of_pole_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_eq_zero_on_perp_of_pole_one` |
| `BornFinite.GaussianTomography.nonneg_frameFunction_bounds` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_frameFunction_bounds` |
| `BornFinite.GaussianTomography.nonneg_residual_is_bounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_residual_is_bounded` |
| `BornFinite.GaussianTomography.nonneg_rigidity_iff_bounded_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_rigidity_iff_bounded_zero_residual` |
| `BornFinite.GaussianTomography.normSqVec_add_eq_normSqVec_sub_of_ortho` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.normSqVec_add_eq_normSqVec_sub_of_ortho` |
| `BornFinite.GaussianTomography.normSqVec_pythagEqRot` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.normSqVec_pythagEqRot` |
| `BornFinite.GaussianTomography.normSqVec_rotPairU` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.normSqVec_rotPairU` |
| `BornFinite.GaussianTomography.normSqVec_rotPairV` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.normSqVec_rotPairV` |
| `BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi3_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi3_tomo_e1` |
| `BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi7_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_exoticQi7_tomo_e1` |
| `BornFinite.GaussianTomography.not_archimedeanContinuousAt_s3_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_s3_tomo_e1` |
| `BornFinite.GaussianTomography.not_archimedeanContinuousAt_s7_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_archimedeanContinuousAt_s7_tomo_e1` |
| `BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s3` |
| `BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s7` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_factorsThroughRayProjLinear_s7` |
| `BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity` |
| `BornFinite.GaussianTomography.not_signed_quadratic_rigidity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_signed_quadratic_rigidity` |
| `BornFinite.GaussianTomography.one_sided_lower_bound_implies_upper_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.one_sided_lower_bound_implies_upper_bound` |
| `BornFinite.GaussianTomography.ortho_coord_identity_x` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.ortho_coord_identity_x` |
| `BornFinite.GaussianTomography.piron_descent_le_of_pole_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.piron_descent_le_of_pole_one` |
| `BornFinite.GaussianTomography.piron_frame_sum_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.piron_frame_sum_identity` |
| `BornFinite.GaussianTomography.primitive_gaussian_norm_mod_four_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.primitive_gaussian_norm_mod_four_iff` |
| `BornFinite.GaussianTomography.pure_pole_e1_nonneg_eliminates_combResidual3_7_11` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.pure_pole_e1_nonneg_eliminates_combResidual3_7_11` |
| `BornFinite.GaussianTomography.quadNum_orthogonal_weighted_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadNum_orthogonal_weighted_sum` |
| `BornFinite.GaussianTomography.quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff` |
| `BornFinite.GaussianTomography.quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff` |
| `BornFinite.GaussianTomography.quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff` |
| `BornFinite.GaussianTomography.quadRay_frame_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_frame_sum` |
| `BornFinite.GaussianTomography.quadRay_isFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_isFrameFunction` |
| `BornFinite.GaussianTomography.quadRay_rayProj_e1_pythagEqRot` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_rayProj_e1_pythagEqRot` |
| `BornFinite.GaussianTomography.quadRay_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_smul` |
| `BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation` |
| `BornFinite.GaussianTomography.quadRay_witness_p11_kernel_relation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_witness_p11_kernel_relation` |
| `BornFinite.GaussianTomography.quadRay_witness_p7_kernel_relation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_witness_p7_kernel_relation` |
| `BornFinite.GaussianTomography.quadratic_rigidity_iff_factorsThroughRayProjLinear` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadratic_rigidity_iff_factorsThroughRayProjLinear` |
| `BornFinite.GaussianTomography.rayProj_frame_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_frame_sum` |
| `BornFinite.GaussianTomography.rayProj_nine_rays_span_hermForm3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_nine_rays_span_hermForm3` |
| `BornFinite.GaussianTomography.rayProj_ortho_add_sub` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_ortho_add_sub` |
| `BornFinite.GaussianTomography.rayProj_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_smul` |
| `BornFinite.GaussianTomography.rayProj_tr` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_tr` |
| `BornFinite.GaussianTomography.rayProj_witness_111_decomp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_witness_111_decomp` |
| `BornFinite.GaussianTomography.rayProj_witness_p11_decomp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_witness_p11_decomp` |
| `BornFinite.GaussianTomography.rayProj_witness_p7_decomp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_witness_p7_decomp` |
| `BornFinite.GaussianTomography.residual_is_zero_weight` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.residual_is_zero_weight` |
| `BornFinite.GaussianTomography.residual_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.residual_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1` |
| `BornFinite.GaussianTomography.s3_isBoundedOnRays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_isBoundedOnRays` |
| `BornFinite.GaussianTomography.s3_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.s3_not_satisfiesOrthoParallelogramZero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_not_satisfiesOrthoParallelogramZero` |
| `BornFinite.GaussianTomography.s3_orthogonal_odd_cancel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_orthogonal_odd_cancel` |
| `BornFinite.GaussianTomography.s3_oscillates_near_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_oscillates_near_tomo_e1` |
| `BornFinite.GaussianTomography.s3_perturb7NegRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_perturb7NegRay` |
| `BornFinite.GaussianTomography.s3_perturb7PosRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_perturb7PosRay` |
| `BornFinite.GaussianTomography.s3_perturbNegRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_perturbNegRay` |
| `BornFinite.GaussianTomography.s3_perturbPosRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_perturbPosRay` |
| `BornFinite.GaussianTomography.s3_s7_dual_on_witnesses` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_s7_dual_on_witnesses` |
| `BornFinite.GaussianTomography.s3_s7_linearIndependent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_s7_linearIndependent` |
| `BornFinite.GaussianTomography.s3_s7_selective_oscillation_near_tomo_e1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_s7_selective_oscillation_near_tomo_e1` |
| `BornFinite.GaussianTomography.s3_s7_sp11_dual_on_three_witnesses` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_s7_sp11_dual_on_three_witnesses` |
| `BornFinite.GaussianTomography.s3_s7_sp11_linearIndependent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_s7_sp11_linearIndependent` |
| `BornFinite.GaussianTomography.s3_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_smul` |
| `BornFinite.GaussianTomography.s3_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.s3_witness_111_kernel_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_witness_111_kernel_separation` |
| `BornFinite.GaussianTomography.s7_isBoundedOnRays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_isBoundedOnRays` |
| `BornFinite.GaussianTomography.s7_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.s7_not_satisfiesOrthoParallelogramZero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_not_satisfiesOrthoParallelogramZero` |
| `BornFinite.GaussianTomography.s7_orthogonal_odd_cancel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_orthogonal_odd_cancel` |
| `BornFinite.GaussianTomography.s7_perturb7NegRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_perturb7NegRay` |
| `BornFinite.GaussianTomography.s7_perturb7PosRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_perturb7PosRay` |
| `BornFinite.GaussianTomography.s7_perturbNegRay_seven_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_perturbNegRay_seven_mul` |
| `BornFinite.GaussianTomography.s7_perturbPosRay_seven_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_perturbPosRay_seven_mul` |
| `BornFinite.GaussianTomography.s7_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_smul` |
| `BornFinite.GaussianTomography.s7_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.s7_witness_p7_kernel_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s7_witness_p7_kernel_separation` |
| `BornFinite.GaussianTomography.satisfiesOrthoParallelogramZero_of_factorsThroughRayProjLinear` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.satisfiesOrthoParallelogramZero_of_factorsThroughRayProjLinear` |
| `BornFinite.GaussianTomography.signed_rigidity_iff_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.signed_rigidity_iff_zero_residual` |
| `BornFinite.GaussianTomography.sp11_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp11_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.sp11_not_satisfiesOrthoParallelogramZero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp11_not_satisfiesOrthoParallelogramZero` |
| `BornFinite.GaussianTomography.sp11_witness_p11_kernel_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp11_witness_p11_kernel_separation` |
| `BornFinite.GaussianTomography.sp_isBoundedOnRays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_isBoundedOnRays` |
| `BornFinite.GaussianTomography.sp_isCoordSignSymmetric` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_isCoordSignSymmetric` |
| `BornFinite.GaussianTomography.sp_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.sp_orthogonal_odd_cancel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_orthogonal_odd_cancel` |
| `BornFinite.GaussianTomography.sp_seven_eq_s7` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_seven_eq_s7` |
| `BornFinite.GaussianTomography.sp_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_smul` |
| `BornFinite.GaussianTomography.sp_three_eq_s3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_three_eq_s3` |
| `BornFinite.GaussianTomography.sp_vanishes_on_coord_axes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_vanishes_on_coord_axes` |
| `BornFinite.GaussianTomography.sp_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.sp_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.three_prime_frame_partner_norm_valuations_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.three_prime_frame_partner_norm_valuations_even` |
| `BornFinite.GaussianTomography.tomographyForm_quadRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomographyForm_quadRay` |
| `BornFinite.GaussianTomography.tomography_isFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_isFrameFunction` |
| `BornFinite.GaussianTomography.tomography_matches_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_matches_nine_rays` |
| `BornFinite.GaussianTomography.tomography_trace_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_trace_one` |
| `BornFinite.GaussianTomography.tomography_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_unique` |
| `BornFinite.GaussianTomography.traceInner_ext` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_ext` |
| `BornFinite.GaussianTomography.traceInner_rayProj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_rayProj` |
| `BornFinite.GaussianTomography.traceInner_self_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_self_eq_zero_iff` |
| `BornFinite.GaussianTomography.unit_norm_in_sqrtP_of_normSqVec_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.unit_norm_in_sqrtP_of_normSqVec_eq` |
| `BornFinite.GaussianTomography.v3Rat_normSq_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.v3Rat_normSq_even` |
| `BornFinite.GaussianTomography.v7Rat_normSq_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.v7Rat_normSq_even` |
| `BornFinite.GaussianTomography.vpRat_normSq_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.vpRat_normSq_even` |
| `BornFinite.GaussianTomography.witness_111_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_111_primitive` |
| `BornFinite.GaussianTomography.witness_111_unit_sqrt3_normSq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_111_unit_sqrt3_normSq` |
| `BornFinite.GaussianTomography.witness_div_eight_shell_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_div_eight_shell_primitive` |
| `BornFinite.GaussianTomography.witness_div_four_shell_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_div_four_shell_primitive` |
| `BornFinite.GaussianTomography.witness_p11_primitive` | yes | yes | yes | none | `#print axioms BornFinite.GaussianTomography.witness_p11_primitive` |
| `BornFinite.GaussianTomography.witness_p7_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_p7_primitive` |
| `BornFinite.GaussianTomography.zeroWeight_rotPair_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zeroWeight_rotPair_sum` |
| `BornFinite.GaussianTomography.zero_of_coordSignSymmetric_and_orthoParallelogram` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zero_of_coordSignSymmetric_and_orthoParallelogram` |
| `BornFinite.GaussianTomography.zero_of_nonneg_zeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zero_of_nonneg_zeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear` |
| `BornFinite.GaussianTomography.zero_on_witness_111_of_sqrt3_even_v3_vanishing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zero_on_witness_111_of_sqrt3_even_v3_vanishing` |
| `BornFinite.GaussianTomography.zero_on_witness_p7_of_sqrt7_even_v7_vanishing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.zero_on_witness_p7_of_sqrt7_even_v7_vanishing` |

- counts toward the grade: yes

### Lean: `lean4/BornRationalRayObstruction.lean`

- file: [lean4/BornRationalRayObstruction.lean](../../../lean4/BornRationalRayObstruction.lean)
- sha256 (`bytes`): `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornRationalRayObstruction`): recorded sha256 `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRationalRayObstruction`
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-extension.py`

- file: [checks/independent/fq-gleason-qi3-extension.py](../../../checks/independent/fq-gleason-qi3-extension.py)
- sha256 (`bytes`): `e54fbb9b4babc7324cf22aa43cab27a89b72208ba1f482c893cbf18128a99d0d`
- cited in: node.source
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-frame-functions.py`

- file: [checks/independent/fq-gleason-qi3-frame-functions.py](../../../checks/independent/fq-gleason-qi3-frame-functions.py)
- sha256 (`bytes`): `79b9d9fac2eea13b1e5a498c6aefa6017c787e3f5a8c9224e503c7d71e1c939d`
- cited in: node.source
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-tomography.py`

- file: [checks/independent/fq-gleason-qi3-tomography.py](../../../checks/independent/fq-gleason-qi3-tomography.py)
- sha256 (`bytes`): `ea6bb44906c6aba0a946800dde5012b854cd34abec6fc68c45084d824e8c8633`
- cited in: node.source
- counts toward the grade: yes

### Python: `code/python/tests/test_fq_gleason_qi3_frame_functions.py`

- file: [code/python/tests/test_fq_gleason_qi3_frame_functions.py](../../../code/python/tests/test_fq_gleason_qi3_frame_functions.py)
- sha256 (`bytes`): `8066a3a38a3114dd40132a827ab0cc50d5e28fa3e91c96511d44bb6b603591a1`
- cited in: node.source, record TFQ-1055

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_archimedean_discontinuity_and_field_extension_elimination` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_archimedean_discontinuity_and_field_extension_elimination` |
| `test_fq_gleason_qi3_frame_functions_end_to_end` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_fq_gleason_qi3_frame_functions_end_to_end` |
| `test_independent_check_scripts_pass` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_independent_check_scripts_pass` |
| `test_multi_prime_s3_s7_linear_independence_and_joint_elimination` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_multi_prime_s3_s7_linear_independence_and_joint_elimination` |
| `test_nine_ray_tomography_reconstruction_and_uniqueness` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_nine_ray_tomography_reconstruction_and_uniqueness` |
| `test_one_plus_i_adic_norm_parity_witnesses_and_mod_four_iff` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_one_plus_i_adic_norm_parity_witnesses_and_mod_four_iff` |
| `test_operator_space_ray_projector_duality_and_zero_normalization` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_operator_space_ray_projector_duality_and_zero_normalization` |
| `test_piron_frame_rotation_parallelogram_and_continuity_bridge` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_piron_frame_rotation_parallelogram_and_continuity_bridge` |
| `test_quadray_frame_sum_on_non_unit_orthogonal_frames` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_quadray_frame_sum_on_non_unit_orthogonal_frames` |
| `test_s3_global_bounded_zero_weight_residual_and_exotic_qi3` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_s3_global_bounded_zero_weight_residual_and_exotic_qi3` |
| `test_signed_and_nonnegative_residual_reduction_equivalences` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_signed_and_nonnegative_residual_reduction_equivalences` |
| `test_uniform_sp_family_p11_and_finite_inert_residual_system` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_uniform_sp_family_p11_and_finite_inert_residual_system` |

- counts toward the grade: yes

### Documents and data: `checks/independent/data/fq_gleason_qi3_extension.json`

- file: [checks/independent/data/fq_gleason_qi3_extension.json](../../../checks/independent/data/fq_gleason_qi3_extension.json)
- sha256 (`lf-normalised`): `fd0fd770fd92f7cb60203c2b813936717db74707e9e3ac5954fab3eaed0f226b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md](../../../dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md)
- sha256 (`lf-normalised`): `71a7487fa7b44950d07c6b6bdea5608cdc9e3f7d70e0c593b13a2f5205b25303`
- generated view: listed, not counted
- cited in: record TFQ-1055
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md`

- file: [dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md](../../../dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md)
- sha256 (`lf-normalised`): `117b3b26afb3b5286eb706c59b1b4427e6aecc82d15289a90045cf78fd762132`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/fq-gleason-qi3-frame-functions.md`

- file: [dag/derivations/independent/fq-gleason-qi3-frame-functions.md](../../../dag/derivations/independent/fq-gleason-qi3-frame-functions.md)
- sha256 (`lf-normalised`): `bdaa18902d61e8c5b9d133dec1cc539130f6ace10d576940a9a5be13b010413f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md`

- file: [dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md](../../../dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md)
- sha256 (`lf-normalised`): `05ab2358bed5d27932a7be17d9e5639fae4871e075734b7f3c9b01a07884117e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-QI3-FRAME-FUNCTIONS` `GAP_NO_DERIVATION`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)

Outgoing (0):

