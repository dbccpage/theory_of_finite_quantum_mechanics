# FQ-GLEASON-QI3-FRAME-FUNCTIONS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E4**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let V = Q(i)^3 with the standard Hermitian form. Decide whether every function f from the nonzero vectors of V to Q with f(u) + f(v) + f(w) = 1 for every orthogonal triple of nonzero vectors has the form f(v) = \<v, rho v\>/\<v, v\> for a Hermitian trace-one 3 x 3 matrix rho over Q(i), or exhibit one that does not; state separately the signed, nonnegative and {0,1}-valued variants, and whether the non-quadratic Q^3 frame function extends to Q(i)^3.

## Grade

Evidence grade **E4** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 13
- cited Lean, Rust or Python symbols found in their in-repo files: 61
- distinct cited Lean declarations covered by a current replay receipt: 54
- counted in-repo runnable tests: 8
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: none: all E4 conditions hold

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The {0,1}-valued variant is excluded by a finite real-ray obstruction. The specific exotic Q^3 frame function has no signed extension, by an exact finite linear certificate. Nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, the signed and bounded nonnegative residual-reduction equivalences, the (1+i)-adic norm-parity characterization on primitive Gaussian-integer vectors, and the explicit global {-1, 0, +1}-valued 3-adic zero-weight residual s3 and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame function exoticQi3 = (1 + s3) / 3 (settling both signed and nonnegative quadratic rigidity on Q(i)^3 in the negative) are formalized in lean4/BornGaussianTomographyReduction.lean. Complete classification of the space of all non-quadratic residuals across every inert prime p == 3 (mod 4) and the additional regularity hypothesis needed to eliminate them for FQ-GAP-BORN-UNIQUENESS-GLEASON remain open.

## Source status

Finite obstructions, nine-ray reductions, and global 3-adic non-quadratic residual: no {0,1}-valued frame function on Q(i)^3, no signed extension of the specified exotic Q^3 function, and in BornGaussianTomographyReduction.lean exact nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, signed and bounded nonnegative residual-reduction equivalences, (1+i)-adic norm-parity characterization on primitive Gaussian-integer vectors, and the explicit global {-1, 0, +1}-valued 3-adic zero-weight residual s3 and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame function exoticQi3 = (1 + s3) / 3 settling both signed and nonnegative quadratic rigidity on Q(i)^3 in the negative. Exact independent checks, runnable pytest suite, and scoped Lean declarations are linked; see the replay receipt for build evidence.

## Review

- PFP review: [dag/research/fq_gleason_qi3_assessment.json](../../../dag/research/fq_gleason_qi3_assessment.json); file present and sha256 matches the node's record: yes; verdict `scoped_obstructions_and_tomography_reduction_reviewed`; scope effect `consistent`; prior status `OPEN`; qualifies for E4: yes.
  - narrowest claim: No {0,1}-valued frame function exists on all Q(i)^3 rays; the specified exotic Q^3 frame function has no signed extension to Q(i)^3; nine-ray Hermitian tomography reconstruction, operator-space ray projector duality and nine-ray spanning of HermForm3, non-unit orthogonal frame sums, zero-vector normalization, signed and bounded nonnegative residual-reduction equivalences, (1+i)-adic norm-parity characterization, and the explicit global {-1, 0, +1}-valued 3-adic zero-weight residual s3 and {0, 1/3, 2/3}-valued nonnegative non-quadratic frame function exoticQi3 = (1 + s3) / 3 (settling both signed and nonnegative quadratic rigidity on Q(i)^3 in the negative) are kernel-checked in Lean 4.
  - does not support: Complete classification of the space of all non-quadratic residuals across every inert prime p == 3 (mod 4), continuum Gleason, or closure of FQ-GAP-BORN-UNIQUENESS-GLEASON.
  - next test: Determine which additional regularity or field-extension positivity hypothesis eliminates all inert-prime p-adic zero-weight residuals on Q(i)^3 for FQ-GAP-BORN-UNIQUENESS-GLEASON.

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
- sha256 (`bytes`): `9c3e48586cf5f004a4cfa8ca1fe00eef793debac1da236a4487d4a3cc344545d`
- cited in: node.lean, node.source, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianTomographyReduction), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianTomographyReduction`): recorded sha256 `9c3e48586cf5f004a4cfa8ca1fe00eef793debac1da236a4487d4a3cc344545d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianTomographyReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.abs_quadRay_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.abs_quadRay_le` |
| `BornFinite.GaussianTomography.detGVec_normSq_of_frame` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.detGVec_normSq_of_frame` |
| `BornFinite.GaussianTomography.eq_quadRay_all_of_zero_at_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.eq_quadRay_all_of_zero_at_zero` |
| `BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exists_nonzero_bounded_zero_residual` |
| `BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi3_isNonnegFrameFunction` |
| `BornFinite.GaussianTomography.exoticQi3_not_quadratic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.exoticQi3_not_quadratic` |
| `BornFinite.GaussianTomography.frame_v3Rat_sum_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.frame_v3Rat_sum_even` |
| `BornFinite.GaussianTomography.gaussian_coord_norm_mod_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_coord_norm_mod_four` |
| `BornFinite.GaussianTomography.gaussian_norm_div_four_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_norm_div_four_witness` |
| `BornFinite.GaussianTomography.gaussian_norm_eight_primitive_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.gaussian_norm_eight_primitive_witness` |
| `BornFinite.GaussianTomography.inner_applyVec_im_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inner_applyVec_im_zero` |
| `BornFinite.GaussianTomography.inner_applyVec_re_eq_quadNum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.inner_applyVec_re_eq_quadNum` |
| `BornFinite.GaussianTomography.nonneg_frameFunction_bounds` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_frameFunction_bounds` |
| `BornFinite.GaussianTomography.nonneg_residual_is_bounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_residual_is_bounded` |
| `BornFinite.GaussianTomography.nonneg_rigidity_iff_bounded_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.nonneg_rigidity_iff_bounded_zero_residual` |
| `BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_nonneg_quadratic_rigidity` |
| `BornFinite.GaussianTomography.not_signed_quadratic_rigidity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.not_signed_quadratic_rigidity` |
| `BornFinite.GaussianTomography.one_sided_lower_bound_implies_upper_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.one_sided_lower_bound_implies_upper_bound` |
| `BornFinite.GaussianTomography.ortho_coord_identity_x` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.ortho_coord_identity_x` |
| `BornFinite.GaussianTomography.primitive_gaussian_norm_mod_four_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.primitive_gaussian_norm_mod_four_iff` |
| `BornFinite.GaussianTomography.quadNum_orthogonal_weighted_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadNum_orthogonal_weighted_sum` |
| `BornFinite.GaussianTomography.quadRay_frame_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_frame_sum` |
| `BornFinite.GaussianTomography.quadRay_isFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_isFrameFunction` |
| `BornFinite.GaussianTomography.quadRay_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_smul` |
| `BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.quadRay_witness_111_kernel_relation` |
| `BornFinite.GaussianTomography.rayProj_frame_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_frame_sum` |
| `BornFinite.GaussianTomography.rayProj_nine_rays_span_hermForm3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_nine_rays_span_hermForm3` |
| `BornFinite.GaussianTomography.rayProj_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_smul` |
| `BornFinite.GaussianTomography.rayProj_tr` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_tr` |
| `BornFinite.GaussianTomography.rayProj_witness_111_decomp` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.rayProj_witness_111_decomp` |
| `BornFinite.GaussianTomography.residual_is_zero_weight` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.residual_is_zero_weight` |
| `BornFinite.GaussianTomography.residual_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.residual_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.s3_isBoundedOnRays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_isBoundedOnRays` |
| `BornFinite.GaussianTomography.s3_isZeroWeightFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_isZeroWeightFrameFunction` |
| `BornFinite.GaussianTomography.s3_orthogonal_odd_cancel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_orthogonal_odd_cancel` |
| `BornFinite.GaussianTomography.s3_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_smul` |
| `BornFinite.GaussianTomography.s3_vanishes_on_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_vanishes_on_nine_rays` |
| `BornFinite.GaussianTomography.s3_witness_111_kernel_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.s3_witness_111_kernel_separation` |
| `BornFinite.GaussianTomography.signed_rigidity_iff_zero_residual` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.signed_rigidity_iff_zero_residual` |
| `BornFinite.GaussianTomography.tomographyForm_quadRay` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomographyForm_quadRay` |
| `BornFinite.GaussianTomography.tomography_isFrameFunction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_isFrameFunction` |
| `BornFinite.GaussianTomography.tomography_matches_nine_rays` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_matches_nine_rays` |
| `BornFinite.GaussianTomography.tomography_trace_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_trace_one` |
| `BornFinite.GaussianTomography.tomography_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_unique` |
| `BornFinite.GaussianTomography.traceInner_ext` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_ext` |
| `BornFinite.GaussianTomography.traceInner_rayProj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_rayProj` |
| `BornFinite.GaussianTomography.traceInner_self_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.traceInner_self_eq_zero_iff` |
| `BornFinite.GaussianTomography.v3Rat_normSq_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.v3Rat_normSq_even` |
| `BornFinite.GaussianTomography.witness_111_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_111_primitive` |
| `BornFinite.GaussianTomography.witness_div_eight_shell_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_div_eight_shell_primitive` |
| `BornFinite.GaussianTomography.witness_div_four_shell_primitive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.witness_div_four_shell_primitive` |

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
- sha256 (`bytes`): `3e01aa6b00d08ba5389bd16afb7513e792fbc54d209439bf2719cb7e9e03fbe3`
- cited in: node.source
- counts toward the grade: yes

### Python: `code/python/tests/test_fq_gleason_qi3_frame_functions.py`

- file: [code/python/tests/test_fq_gleason_qi3_frame_functions.py](../../../code/python/tests/test_fq_gleason_qi3_frame_functions.py)
- sha256 (`bytes`): `ebaa82946274762a57870c9429d6e2c26ee7fa2c9bd71ea1e5a17c6493ae5134`
- cited in: node.source, record TFQ-1055

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_fq_gleason_qi3_frame_functions_end_to_end` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_fq_gleason_qi3_frame_functions_end_to_end` |
| `test_nine_ray_tomography_reconstruction_and_uniqueness` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_nine_ray_tomography_reconstruction_and_uniqueness` |
| `test_one_plus_i_adic_norm_parity_witnesses_and_mod_four_iff` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_one_plus_i_adic_norm_parity_witnesses_and_mod_four_iff` |
| `test_operator_space_ray_projector_duality_and_zero_normalization` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_operator_space_ray_projector_duality_and_zero_normalization` |
| `test_quadray_frame_sum_on_non_unit_orthogonal_frames` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_quadray_frame_sum_on_non_unit_orthogonal_frames` |
| `test_s3_global_bounded_zero_weight_residual_and_exotic_qi3` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_s3_global_bounded_zero_weight_residual_and_exotic_qi3` |
| `test_signed_and_nonnegative_residual_reduction_equivalences` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py::test_signed_and_nonnegative_residual_reduction_equivalences` |

- counts toward the grade: yes

### Documents and data: `checks/independent/data/fq_gleason_qi3_extension.json`

- file: [checks/independent/data/fq_gleason_qi3_extension.json](../../../checks/independent/data/fq_gleason_qi3_extension.json)
- sha256 (`lf-normalised`): `fd0fd770fd92f7cb60203c2b813936717db74707e9e3ac5954fab3eaed0f226b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md](../../../dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md)
- sha256 (`lf-normalised`): `b84c08d0668b681d3fdc3371571035b52be90c628ee083f771d6dd9268bbc43e`
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
- sha256 (`lf-normalised`): `c5d95e03644e6033ab24f68cdf164048026d4bd3cf3221539d201aef8e6969cb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md`

- file: [dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md](../../../dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md)
- sha256 (`lf-normalised`): `fb1a4e802342a4a82b67af06675a09cadd412eaa44bbbc95a55bc40012cb9129`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-QI3-FRAME-FUNCTIONS` `GAP_NO_DERIVATION`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)

Outgoing (0):

