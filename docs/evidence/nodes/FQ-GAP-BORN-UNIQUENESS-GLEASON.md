# FQ-GAP-BORN-UNIQUENESS-GLEASON

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E4**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Born uniqueness of the quadratic form needs imported Hilbert space, projection lattices and Gleason-type assumptions, with dimension n \>= 3; Gleason frame additivity at n \>= 3 is verified only over orthogonal frames of specific finite ray sets. The three-label cardinality surrogate (3 \<= |Q|) is false on Bool; the unit-effect contract already has two disagreeing pairings.

## Grade

Evidence grade **E4** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 21
- cited Lean, Rust or Python symbols found in their in-repo files: 45
- distinct cited Lean declarations covered by a current replay receipt: 45
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: none: all E4 conditions hold

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- rational matrix algebra with the quadratic-form preorder and unit identity (supplied carrier)
- effect additivity: v(E+F) = v(E)+v(F) whenever E, F and E+F are effects (assumption)
- Gleason theorem for d \>= 3 (assumption, projection-lattice route only)
- projection lattice (assumption, projection-lattice route only)
- Hilbert space (assumption)

## Bottleneck

The carrier (rational symmetric or Gaussian-rational Hermitian matrices with the Hermitian-form preorder) and effect additivity are supplied, not derived from primitives; the Gaussian-rational Hermitian case is kernel-checked in run 20261020T224000Z_gaussian_hermitian_carrier (BornGaussRat, BornHermitianCarrier with complex Cauchy-Schwarz and real-part trace representation, BornHermitianPsdDecomposition, BornHermitianTraceRepresentation: unique Hermitian rational-PSD trace-one rho with v(E) = re trace(rho E); exact twins code/python/src/qm/born_hermitian_valuation.py, code/rust/src/qm/born_hermitian_valuation.rs). Open: the operational justification of effect additivity and the projection-only frame-function route at n \>= 3; on rational rays the frame-function route is obstructed by the parity countermodel. Finite rational frame obstructions (Cabello 18-9, d=2 plane, d=3 rotated frame eliminating the quartic rival) remain mechanized. Gaussian-rational frame functions (Fable API run 20261022T193631Z, receipt dag/research/fable_gleason_run2_lean_replay.json): over Q(i)^3 a frame function on nonzero vectors is constant on rays (frameFunction_smul); and a frame function whose value on every Gaussian-integer vector with not all of a+b, c+d, e+g even depends only on ((a+b) mod 2, (c+d) mod 2, (e+g) mod 2) has the value 1/3 on all of those vectors (parity_class_function_is_third). That excludes only this (1+i)-parity-class ansatz: other parity-type constructions (for example residues modulo 2 in Z\[i\]) are not covered, the identification of the class with (1+i)-divisibility is not formalised, and the 1/3 is not stated outside those vectors. Campaign run (receipt dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json): over Q^3 the mod-4 function exotic(v) = (1 + sgn v)/3 on integer vectors not all even is a frame function on all rational rays, takes the values 0, 1/3, 2/3, and is not quadratic (BornRationalRayObstruction: exotic_frame_function, exotic_not_quadratic), so on the rational carrier frame additivity on all orthogonal triples does not select the Born form even among nonnegative frame functions; and over Q(i)^3 a frame function that is a residue-modulo-2 class function on (1+i)-primitive Gaussian-integer vectors is 1/3 there (BornGaussianMod2ClassRigidity: mod2_class_function_is_third, 56 explicit frames). Existence of a non-quadratic frame function on Q(i)^3 rays and quadraticity of all of them both remain open, as does whether the Q^3 function extends to Q(i)^3.

## Source status

Effect-additive (Busch-type) route kernel-checked over Q in dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean: every positive normalized effect-additive valuation on rational n x n matrices is E -\> trace(rho E) for a unique symmetric rational-PSD trace-one rho (born_representation, density_is_state, born_rule, state_valuation_correspondence); the eight frozen targets of runs/20261020T004525Z_fable51_born (val_zero .. val_sandwich) are discharged; the rational-sphere parity frame function (parity_frame_function, parity_not_quadratic) shows that additivity on orthogonal triples of rational rays in d=3 does not select the quadratic form. Continuum Gleason on S^{n-1} is not used; it remains an external import only for the projection-lattice route. Exact replays: code/python/src/qm/born_effect_valuation.py, code/rust/src/qm/born_effect_valuation.rs. Earlier: Born vs quartic rival separation on (3,4) and d=3 orthogonal frame additivity eliminating the quartic rival mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Concrete weak-contract and quartic-frame countermodels with exact normalized values and literal kernel scope.
  - does not support: general Born/Gleason uniqueness from one rejected rival, or necessity/regularity assumptions inferred from flags.
  - next test: Challenge actual coordinates/dimension/readout values and refuse uniqueness promotion.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornEffectValuation.lean`

- file: [lean4/BornEffectValuation.lean](../../../lean4/BornEffectValuation.lean)
- sha256 (`bytes`): `c0c6c946120523644c5a8bb8a66bd72ace71c0c16ea3d1871e8f54670ec3395a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornEffectValuation`): recorded sha256 `c0c6c946120523644c5a8bb8a66bd72ace71c0c16ea3d1871e8f54670ec3395a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornEffectValuation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.val_rat_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.val_rat_smul` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussRat.lean`

- file: [lean4/BornGaussRat.lean](../../../lean4/BornGaussRat.lean)
- sha256 (`bytes`): `5e44685120e200cf66416fe13f3fe762da0cb072157b62b92454dc9f4089665b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornGaussRat`): recorded sha256 `5e44685120e200cf66416fe13f3fe762da0cb072157b62b92454dc9f4089665b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussRat`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussRat.instStarRing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussRat.instStarRing` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianFrameRays.lean`

- file: [lean4/BornGaussianFrameRays.lean](../../../lean4/BornGaussianFrameRays.lean)
- sha256 (`bytes`): `978b7e33c3accef4513c5d5151ee92bcd2612caf16b5bc084e095b764fadc7e6`
- cited in: node.lean, receipt dag/research/born_gaussian_frames_lean_replay.json (BornGaussianFrameRays)
- replay: `verified`
  - receipt [dag/research/born_gaussian_frames_lean_replay.json](../../../dag/research/born_gaussian_frames_lean_replay.json) (module `BornGaussianFrameRays`): recorded sha256 `978b7e33c3accef4513c5d5151ee92bcd2612caf16b5bc084e095b764fadc7e6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianFrameRays`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.exists_frame_completion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.exists_frame_completion` |
| `BornFinite.GaussianFrames.frameFunction_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frameFunction_smul` |
| `BornFinite.GaussianFrames.inner_smul_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.inner_smul_left` |
| `BornFinite.GaussianFrames.nonZero_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.nonZero_smul` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianMod2ClassRigidity.lean`

- file: [lean4/BornGaussianMod2ClassRigidity.lean](../../../lean4/BornGaussianMod2ClassRigidity.lean)
- sha256 (`bytes`): `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d`
- cited in: node.lean, receipt dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json (BornGaussianMod2ClassRigidity)
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornGaussianMod2ClassRigidity`): recorded sha256 `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianMod2ClassRigidity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.class_value2` | yes | yes | yes | Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.class_value2` |
| `BornFinite.GaussianFrames.mod2_class_function_is_third` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.mod2_class_function_is_third` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalFrameObstruction.lean`

- file: [lean4/BornGaussianRationalFrameObstruction.lean](../../../lean4/BornGaussianRationalFrameObstruction.lean)
- sha256 (`bytes`): `5564b1a4dd947620281406208466d2df9792aedc5e7eeae3073b7ba52a8134c2`
- cited in: node.lean, receipt dag/research/born_gaussian_frames_lean_replay.json (BornGaussianRationalFrameObstruction)
- replay: `verified`
  - receipt [dag/research/born_gaussian_frames_lean_replay.json](../../../dag/research/born_gaussian_frames_lean_replay.json) (module `BornGaussianRationalFrameObstruction`): recorded sha256 `5564b1a4dd947620281406208466d2df9792aedc5e7eeae3073b7ba52a8134c2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalFrameObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.class_value` | yes | yes | yes | Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.class_value` |
| `BornFinite.GaussianFrames.frame_111_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_111_110` |
| `BornFinite.GaussianFrames.frame_e1_011` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_e1_011` |
| `BornFinite.GaussianFrames.frame_e2_101` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_e2_101` |
| `BornFinite.GaussianFrames.frame_e3_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_e3_110` |
| `BornFinite.GaussianFrames.frame_tri_011` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_tri_011` |
| `BornFinite.GaussianFrames.frame_tri_101` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_tri_101` |
| `BornFinite.GaussianFrames.frame_tri_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.frame_tri_110` |
| `BornFinite.GaussianFrames.parity_class_function_is_third` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.parity_class_function_is_third` |

- counts toward the grade: yes

### Lean: `lean4/BornHermitianCarrier.lean`

- file: [lean4/BornHermitianCarrier.lean](../../../lean4/BornHermitianCarrier.lean)
- sha256 (`bytes`): `7fdb683ab5515376014639d26f6709f2409bec1d13631f8c3f38dadf4e4017d5`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornHermitianCarrier`): recorded sha256 `7fdb683ab5515376014639d26f6709f2409bec1d13631f8c3f38dadf4e4017d5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornHermitianCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.HermitianCarrier.normSq_dot_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.normSq_dot_le` |
| `BornFinite.HermitianCarrier.trace_rep` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.trace_rep` |

- counts toward the grade: yes

### Lean: `lean4/BornHermitianPsdDecomposition.lean`

- file: [lean4/BornHermitianPsdDecomposition.lean](../../../lean4/BornHermitianPsdDecomposition.lean)
- sha256 (`bytes`): `21f92d44fe846b08783f3641a47aec5a9b211a453faf4f4cd5c54d1421a06e5f`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornHermitianPsdDecomposition`): recorded sha256 `21f92d44fe846b08783f3641a47aec5a9b211a453faf4f4cd5c54d1421a06e5f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornHermitianPsdDecomposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.HermitianPsd.gram_of_psd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianPsd.gram_of_psd` |

- counts toward the grade: yes

### Lean: `lean4/BornHermitianTraceRepresentation.lean`

- file: [lean4/BornHermitianTraceRepresentation.lean](../../../lean4/BornHermitianTraceRepresentation.lean)
- sha256 (`bytes`): `06463b9a757cf3b567ecdc07cee15df0dde4cad5cf2f214e2b3fcb8b304bad3d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornHermitianTraceRepresentation`): recorded sha256 `06463b9a757cf3b567ecdc07cee15df0dde4cad5cf2f214e2b3fcb8b304bad3d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornHermitianTraceRepresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.HermitianCarrier.born_representation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.born_representation` |
| `BornFinite.HermitianCarrier.born_rule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.born_rule` |
| `BornFinite.HermitianCarrier.density_is_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.density_is_state` |
| `BornFinite.HermitianCarrier.state_valuation_correspondence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.HermitianCarrier.state_valuation_correspondence` |

- counts toward the grade: yes

### Lean: `lean4/BornLinearExtension.lean`

- file: [lean4/BornLinearExtension.lean](../../../lean4/BornLinearExtension.lean)
- sha256 (`bytes`): `9d76112b91323c8481b5a25597337e2922b6987bf34b460f22d5a23019968d17`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornLinearExtension`): recorded sha256 `9d76112b91323c8481b5a25597337e2922b6987bf34b460f22d5a23019968d17` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornLinearExtension`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.OrderedQUnit.linear_extension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.OrderedQUnit.linear_extension` |

- counts toward the grade: yes

### Lean: `lean4/BornMatrixCarrier.lean`

- file: [lean4/BornMatrixCarrier.lean](../../../lean4/BornMatrixCarrier.lean)
- sha256 (`bytes`): `9637035fc88ea1e974d73efe00457798ad48c28f5d27061fe89c2dbc384ba4df`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornMatrixCarrier`): recorded sha256 `9637035fc88ea1e974d73efe00457798ad48c28f5d27061fe89c2dbc384ba4df` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornMatrixCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.MatrixCarrier.order_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.MatrixCarrier.order_unit` |

- counts toward the grade: yes

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: record TFQ-0307 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornNormalization`): recorded sha256 `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornNormalization`
- counts toward the grade: no

### Lean: `lean4/BornPsdDecomposition.lean`

- file: [lean4/BornPsdDecomposition.lean](../../../lean4/BornPsdDecomposition.lean)
- sha256 (`bytes`): `6e51927474e64564df8d05ddc75f7c8ac474dc382d0667e3d9a749ac4c5f6aa9`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornPsdDecomposition`): recorded sha256 `6e51927474e64564df8d05ddc75f7c8ac474dc382d0667e3d9a749ac4c5f6aa9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornPsdDecomposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.PsdDecomposition.gram_of_psd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.PsdDecomposition.gram_of_psd` |

- counts toward the grade: yes

### Lean: `lean4/BornRationalRayObstruction.lean`

- file: [lean4/BornRationalRayObstruction.lean](../../../lean4/BornRationalRayObstruction.lean)
- sha256 (`bytes`): `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0`
- cited in: node.lean, receipt dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json (BornRationalRayObstruction)
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornRationalRayObstruction`): recorded sha256 `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRationalRayObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.RationalRays.exotic_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_frame_function` |
| `BornFinite.RationalRays.exotic_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_neg` |
| `BornFinite.RationalRays.exotic_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_nonneg` |
| `BornFinite.RationalRays.exotic_not_quadratic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_not_quadratic` |
| `BornFinite.RationalRays.exotic_odd_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_odd_smul` |
| `BornFinite.RationalRays.exotic_values` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.exotic_values` |
| `BornFinite.RationalRays.pairSign_add_eq_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms BornFinite.RationalRays.pairSign_add_eq_zero` |
| `BornFinite.RationalRays.sgn_frame_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalRays.sgn_frame_sum` |

- counts toward the grade: yes

### Lean: `lean4/BornRationalSphereObstruction.lean`

- file: [lean4/BornRationalSphereObstruction.lean](../../../lean4/BornRationalSphereObstruction.lean)
- sha256 (`bytes`): `50f87e37e9cc467a2b36332fc8e8307bfa71ec9a5b19ac0dc44e36ce3412f6ba`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornRationalSphereObstruction`): recorded sha256 `50f87e37e9cc467a2b36332fc8e8307bfa71ec9a5b19ac0dc44e36ce3412f6ba` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRationalSphereObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.RationalSphere.parity_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalSphere.parity_frame_function` |
| `BornFinite.RationalSphere.parity_not_quadratic` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.RationalSphere.parity_not_quadratic` |

- counts toward the grade: yes

### Lean: `lean4/BornTraceRepresentation.lean`

- file: [lean4/BornTraceRepresentation.lean](../../../lean4/BornTraceRepresentation.lean)
- sha256 (`bytes`): `04fc9c79e4fb5226c4427c81fea96bfaada1fe2ef3bb58863eddc73d48d779c7`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `BornTraceRepresentation`): recorded sha256 `04fc9c79e4fb5226c4427c81fea96bfaada1fe2ef3bb58863eddc73d48d779c7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornTraceRepresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.MatrixCarrier.born_representation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.MatrixCarrier.born_representation` |
| `BornFinite.MatrixCarrier.born_rule` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.MatrixCarrier.born_rule` |
| `BornFinite.MatrixCarrier.density_is_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.MatrixCarrier.density_is_state` |
| `BornFinite.MatrixCarrier.state_valuation_correspondence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.MatrixCarrier.state_valuation_correspondence` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0307 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/HilbertWalkGleason.lean`

- file: [lean4/HilbertWalkGleason.lean](../../../lean4/HilbertWalkGleason.lean)
- sha256 (`bytes`): `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleason`): recorded sha256 `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gleason_pack_uniqueness_still_imported` | yes | yes | yes | none | `#print axioms gleason_pack_uniqueness_still_imported` |

- counts toward the grade: yes

### Lean: `lean4/QuarticRivalSeparation.lean`

- file: [lean4/QuarticRivalSeparation.lean](../../../lean4/QuarticRivalSeparation.lean)
- sha256 (`bytes`): `17bb7bdba42a7ea9e389864cd6f5b6ab6537d525b4969b9e441f9db70a7f43e4`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `QuarticRivalSeparation`): recorded sha256 `17bb7bdba42a7ea9e389864cd6f5b6ab6537d525b4969b9e441f9db70a7f43e4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build QuarticRivalSeparation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `frames_equinorm` | yes | yes | yes | none | `#print axioms frames_equinorm` |

- counts toward the grade: yes

### Python: `code/python/tests/test_fq_gleason_qi3_frame_functions.py`

- file: [code/python/tests/test_fq_gleason_qi3_frame_functions.py](../../../code/python/tests/test_fq_gleason_qi3_frame_functions.py)
- sha256 (`bytes`): `aca7a111e7e2e5cc500ebe17467e5eca14701a8852ba36a9b18690b494ea7d6a`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_fq_gleason_qi3_frame_functions.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md](../../../dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md)
- sha256 (`lf-normalised`): `cbdaa44b0fba859fe8fe7dd5ada4b13dbeb9c1e39728690a396b044f7798a6ff`
- generated view: listed, not counted
- cited in: record TFQ-0307 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md`

- file: [dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md](../../../dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md)
- sha256 (`lf-normalised`): `117b3b26afb3b5286eb706c59b1b4427e6aecc82d15289a90045cf78fd762132`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json`

- file: [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json)
- sha256 (`lf-normalised`): `bb7224ff87e7c0de653fb381e4f0a4f8f154ab83d5d30cacfccc89a3f4f12fbd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`

## Routes

Incoming (2):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION](FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION.md) (PROVED_LEAN), [FQ-CABELLO-FRAME-POLYTOPE-146](FQ-CABELLO-FRAME-POLYTOPE-146.md) (COMPUTATIONALLY_CHECKED), [FQ-SORKIN-READOUT-CLASS-QM208](FQ-SORKIN-READOUT-CLASS-QM208.md) (COMPUTATIONALLY_CHECKED), [FQ-POWER-RULE-P2-SELECTION](FQ-POWER-RULE-P2-SELECTION.md) (COMPUTATIONALLY_CHECKED)
- `FRO-R-BACK-CT-PROBABILITY-TO-BORN` `GAP_NO_DERIVATION`: [CT-PROBABILITY-2016-SOURCE](CT-PROBABILITY-2016-SOURCE.md) (SOURCE_RECORD)

Outgoing (1):

- `FQ-R-GLEASON-QI3-FRAME-FUNCTIONS` `GAP_NO_DERIVATION`: [FQ-GLEASON-QI3-FRAME-FUNCTIONS](FQ-GLEASON-QI3-FRAME-FUNCTIONS.md) (OPEN)
