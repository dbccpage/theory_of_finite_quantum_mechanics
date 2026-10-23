# FQ-GAP-BORN-UNIQUENESS-GLEASON

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Born uniqueness of the quadratic form needs imported Hilbert space, projection lattices and Gleason-type assumptions, with dimension n \>= 3; Gleason frame additivity at n \>= 3 is verified only over orthogonal frames of specific finite ray sets. The three-label cardinality surrogate (3 \<= |Q|) is false on Bool; the unit-effect contract already has two disagreeing pairings.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 15
- cited Lean, Rust or Python symbols found in their in-repo files: 36
- cited Lean declarations covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- rational matrix algebra with the quadratic-form preorder and unit identity (supplied carrier)
- effect additivity: v(E+F) = v(E)+v(F) whenever E, F and E+F are effects (assumption)
- Gleason theorem for d \>= 3 (assumption, projection-lattice route only)
- projection lattice (assumption, projection-lattice route only)
- Hilbert space (assumption)

## Bottleneck

The carrier (rational symmetric or Gaussian-rational Hermitian matrices with the Hermitian-form preorder) and effect additivity are supplied, not derived from primitives; the Gaussian-rational Hermitian case is kernel-checked in run 20261020T224000Z_gaussian_hermitian_carrier (BornGaussRat, BornHermitianCarrier with complex Cauchy-Schwarz and real-part trace representation, BornHermitianPsdDecomposition, BornHermitianTraceRepresentation: unique Hermitian rational-PSD trace-one rho with v(E) = re trace(rho E); exact twins code/python/src/qm/born_hermitian_valuation.py, code/rust/src/qm/born_hermitian_valuation.rs). Open: the operational justification of effect additivity and the projection-only frame-function route at n \>= 3; on rational rays the frame-function route is obstructed by the parity countermodel. Finite rational frame obstructions (Cabello 18-9, d=2 plane, d=3 rotated frame eliminating the quartic rival) remain mechanized. Gaussian-rational frame functions (Fable API run 20261022T193631Z, receipt dag/research/fable_gleason_run2_lean_replay.json): over Q(i)^3 a frame function on nonzero vectors is constant on rays (frameFunction_smul); and a frame function whose value on every Gaussian-integer vector with not all of a+b, c+d, e+g even depends only on ((a+b) mod 2, (c+d) mod 2, (e+g) mod 2) has the value 1/3 on all of those vectors (parity_class_function_is_third). That excludes only this (1+i)-parity-class ansatz: other parity-type constructions (for example residues modulo 2 in Z\[i\]) are not covered, the identification of the class with (1+i)-divisibility is not formalised, and the 1/3 is not stated outside those vectors. Existence of a non-quadratic frame function on Q(i)^3 rays and quadraticity of all of them both remain open.

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
- sha256 (`bytes`): `667f6f7a73ca630a4c395a424a68398c9daebfba404d5284abe56dfdbe2955cc`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornEffectValuation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.val_rat_smul` | yes | yes | yes | - | `#print axioms BornFable.val_rat_smul` |
- counts toward the grade: yes

### Lean: `lean4/BornGaussRat.lean`

- file: [lean4/BornGaussRat.lean](../../../lean4/BornGaussRat.lean)
- sha256 (`bytes`): `b3cd5a1f31afc2f074455cc29337108b57366739b707668448f2328d16c2c056`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornGaussRat`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.GaussRat.instStarRing` | yes | yes | yes | - | `#print axioms BornFable.GaussRat.instStarRing` |
- counts toward the grade: yes

### Lean: `lean4/BornGaussianFrameRays.lean`

- file: [lean4/BornGaussianFrameRays.lean](../../../lean4/BornGaussianFrameRays.lean)
- sha256 (`bytes`): `55b3b0911fa9d9081b70c2c388353163e02f4703cd79e78d5b33aa8cae7a73bf`
- cited in: node.lean, receipt dag/research/fable_gleason_run2_lean_replay.json (BornGaussianFrameRays)
- replay: `verified`
  - receipt [dag/research/fable_gleason_run2_lean_replay.json](../../../dag/research/fable_gleason_run2_lean_replay.json) (module `BornGaussianFrameRays`): recorded sha256 `55b3b0911fa9d9081b70c2c388353163e02f4703cd79e78d5b33aa8cae7a73bf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianFrameRays`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.GaussianFrames.exists_frame_completion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.exists_frame_completion` |
| `BornFable.GaussianFrames.frameFunction_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frameFunction_smul` |
| `BornFable.GaussianFrames.inner_smul_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.inner_smul_left` |
| `BornFable.GaussianFrames.nonZero_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.nonZero_smul` |
- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalFrameObstruction.lean`

- file: [lean4/BornGaussianRationalFrameObstruction.lean](../../../lean4/BornGaussianRationalFrameObstruction.lean)
- sha256 (`bytes`): `bffddd6e1bc2877e30d830212fa2a4e6ed4b1af5135f421a43aeb4079a8480a3`
- cited in: node.lean, receipt dag/research/fable_gleason_run2_lean_replay.json (BornGaussianRationalFrameObstruction)
- replay: `verified`
  - receipt [dag/research/fable_gleason_run2_lean_replay.json](../../../dag/research/fable_gleason_run2_lean_replay.json) (module `BornGaussianRationalFrameObstruction`): recorded sha256 `bffddd6e1bc2877e30d830212fa2a4e6ed4b1af5135f421a43aeb4079a8480a3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalFrameObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.GaussianFrames.class_value` | yes | yes | yes | Quot.sound, propext | `#print axioms BornFable.GaussianFrames.class_value` |
| `BornFable.GaussianFrames.frame_111_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_111_110` |
| `BornFable.GaussianFrames.frame_e1_011` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_e1_011` |
| `BornFable.GaussianFrames.frame_e2_101` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_e2_101` |
| `BornFable.GaussianFrames.frame_e3_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_e3_110` |
| `BornFable.GaussianFrames.frame_tri_011` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_tri_011` |
| `BornFable.GaussianFrames.frame_tri_101` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_tri_101` |
| `BornFable.GaussianFrames.frame_tri_110` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.frame_tri_110` |
| `BornFable.GaussianFrames.parity_class_function_is_third` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.GaussianFrames.parity_class_function_is_third` |
- counts toward the grade: yes

### Lean: `lean4/BornHermitianCarrier.lean`

- file: [lean4/BornHermitianCarrier.lean](../../../lean4/BornHermitianCarrier.lean)
- sha256 (`bytes`): `ce59c8f922be95483f8e6c6319d92dfcca15244f23067af62a2564419e388336`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornHermitianCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.HermitianCarrier.normSq_dot_le` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.normSq_dot_le` |
| `BornFable.HermitianCarrier.trace_rep` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.trace_rep` |
- counts toward the grade: yes

### Lean: `lean4/BornHermitianPsdDecomposition.lean`

- file: [lean4/BornHermitianPsdDecomposition.lean](../../../lean4/BornHermitianPsdDecomposition.lean)
- sha256 (`bytes`): `35fe7beaeab4e29cc2c0b710a911d403aa1a573db5634e9c92af9618ce16eb32`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornHermitianPsdDecomposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.HermitianPsd.gram_of_psd` | yes | yes | yes | - | `#print axioms BornFable.HermitianPsd.gram_of_psd` |
- counts toward the grade: yes

### Lean: `lean4/BornHermitianTraceRepresentation.lean`

- file: [lean4/BornHermitianTraceRepresentation.lean](../../../lean4/BornHermitianTraceRepresentation.lean)
- sha256 (`bytes`): `3e1bcb60f82cef30c92e2cf350ffb080ab56d8155d92aa50481c893d92b1b68e`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornHermitianTraceRepresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.HermitianCarrier.born_representation` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.born_representation` |
| `BornFable.HermitianCarrier.born_rule` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.born_rule` |
| `BornFable.HermitianCarrier.density_is_state` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.density_is_state` |
| `BornFable.HermitianCarrier.state_valuation_correspondence` | yes | yes | yes | - | `#print axioms BornFable.HermitianCarrier.state_valuation_correspondence` |
- counts toward the grade: yes

### Lean: `lean4/BornLinearExtension.lean`

- file: [lean4/BornLinearExtension.lean](../../../lean4/BornLinearExtension.lean)
- sha256 (`bytes`): `3ad866318f95fd58021e70a95dd2d0197e565e8375645d236a45eca99424b332`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornLinearExtension`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.OrderedQUnit.linear_extension` | yes | yes | yes | - | `#print axioms BornFable.OrderedQUnit.linear_extension` |
- counts toward the grade: yes

### Lean: `lean4/BornMatrixCarrier.lean`

- file: [lean4/BornMatrixCarrier.lean](../../../lean4/BornMatrixCarrier.lean)
- sha256 (`bytes`): `723ec7dad59f111be54b11096ac8de4040b7b0777a6be521a07ca6b09c1311eb`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornMatrixCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.MatrixCarrier.order_unit` | yes | yes | yes | - | `#print axioms BornFable.MatrixCarrier.order_unit` |
- counts toward the grade: yes

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: record TFQ-0307 (shared)
- replay: `none`
- check: `cd lean4 && lake build BornNormalization`
- counts toward the grade: no

### Lean: `lean4/BornPsdDecomposition.lean`

- file: [lean4/BornPsdDecomposition.lean](../../../lean4/BornPsdDecomposition.lean)
- sha256 (`bytes`): `fc4d54c9f1c4d0156843c89cf6de6aaad8149ee9aa9654366336ef7400ad8037`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornPsdDecomposition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.PsdDecomposition.gram_of_psd` | yes | yes | yes | - | `#print axioms BornFable.PsdDecomposition.gram_of_psd` |
- counts toward the grade: yes

### Lean: `lean4/BornRationalSphereObstruction.lean`

- file: [lean4/BornRationalSphereObstruction.lean](../../../lean4/BornRationalSphereObstruction.lean)
- sha256 (`bytes`): `bf329537287f4cc508d944ea0ce780096d36df81216728d03a192ea741457812`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornRationalSphereObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.RationalSphere.parity_frame_function` | yes | yes | yes | - | `#print axioms BornFable.RationalSphere.parity_frame_function` |
| `BornFable.RationalSphere.parity_not_quadratic` | yes | yes | yes | - | `#print axioms BornFable.RationalSphere.parity_not_quadratic` |
- counts toward the grade: yes

### Lean: `lean4/BornTraceRepresentation.lean`

- file: [lean4/BornTraceRepresentation.lean](../../../lean4/BornTraceRepresentation.lean)
- sha256 (`bytes`): `24bc62b14d2a6661c17202df9122a38ef9a3c7ae099e1549198b410ee52b1709`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build BornTraceRepresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.MatrixCarrier.born_representation` | yes | yes | yes | - | `#print axioms BornFable.MatrixCarrier.born_representation` |
| `BornFable.MatrixCarrier.born_rule` | yes | yes | yes | - | `#print axioms BornFable.MatrixCarrier.born_rule` |
| `BornFable.MatrixCarrier.density_is_state` | yes | yes | yes | - | `#print axioms BornFable.MatrixCarrier.density_is_state` |
| `BornFable.MatrixCarrier.state_valuation_correspondence` | yes | yes | yes | - | `#print axioms BornFable.MatrixCarrier.state_valuation_correspondence` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0307 (shared)
- replay: `none`
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/H013QuarticRivalSeparation.lean`

- file: [lean4/H013QuarticRivalSeparation.lean](../../../lean4/H013QuarticRivalSeparation.lean)
- sha256 (`bytes`): `249249d7a40e4f9e93ae816e9190e2ce3506ba883f8c95f134f6b9419c329bd5`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H013QuarticRivalSeparation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `frames_equinorm` | yes | yes | yes | - | `#print axioms frames_equinorm` |
- counts toward the grade: yes

### Lean: `lean4/H017Gleason.lean`

- file: [lean4/H017Gleason.lean](../../../lean4/H017Gleason.lean)
- sha256 (`bytes`): `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H017Gleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gleason_pack_uniqueness_still_imported` | yes | yes | yes | - | `#print axioms gleason_pack_uniqueness_still_imported` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md](../../../dag/derivations/09_finite_hilbert/tfq_0307_gleason_route_for_dimension_at_least_three.md)
- sha256 (`lf-normalised`): `7c6c2498ae3a8a9ca89f986289680fec7db4936bceccc852ebc20ab3cc2f76c5`
- generated view: listed, not counted
- cited in: record TFQ-0307 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION](FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION.md) (PROVED_LEAN), [FQ-CABELLO-FRAME-POLYTOPE-146](FQ-CABELLO-FRAME-POLYTOPE-146.md) (COMPUTATIONALLY_CHECKED), [FQ-SORKIN-READOUT-CLASS-QM208](FQ-SORKIN-READOUT-CLASS-QM208.md) (PROVED_LEAN), [FQ-POWER-RULE-P2-SELECTION](FQ-POWER-RULE-P2-SELECTION.md) (PROVED_LEAN)
- `FRO-R-BACK-CT-PROBABILITY-TO-BORN` `GAP_NO_DERIVATION`: [CT-PROBABILITY-2016-SOURCE](CT-PROBABILITY-2016-SOURCE.md) (SOURCE_RECORD)

Outgoing (0):

