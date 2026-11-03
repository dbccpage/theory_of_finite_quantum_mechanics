# FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let f : GVec -\> Q be a signed frame function on Q(i)^3 (IsFrameFunction f: f(u) + f(v) + f(w) = 1 for every triple of nonzero pairwise orthogonal vectors; no sign condition). Suppose f is uniformly continuous on rays (IsUniformlyRayContinuous f): for every rational epsilon \> 0 there is a rational delta \> 0 such that |f(u) - f(v)| \< epsilon whenever u, v are nonzero and raySinSq u v = 1 - |\<u,v\>|^2/(\<u,u\>\<v,v\>) \< delta, where raySinSq is a squared ray distance (phase and scale invariant) whose square root is the corresponding metric on rays. Then f(v) = quadRay (tomographyForm f) v = \<v, rho v\>/\<v, v\> for every nonzero v, with rho the Hermitian trace-one matrix reconstructed from the nine tomography rays. The nonnegative version (IsNonnegFrameFunction f) is the special case of a nonnegative f.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- uniform continuity of f on rays (IsUniformlyRayContinuous f): declared input, not derived

## Bottleneck

The result is conditional on the declared hypothesis IsUniformlyRayContinuous f. Whether Archimedean continuity at every nonzero rational vector (IsArchimedeanContinuousEverywhere, the pointwise notion used by the existing BornGaussianTomographyReduction results) implies it for frame functions is FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM (OPEN); until that is settled the pointwise targets remain unresolved. A finite instrument's resolution at one tolerance supplies one (epsilon, delta) pair, not the for-all-epsilon-exists-delta guarantee. This node changes no status of FQ-GLEASON-QI3-FRAME-FUNCTIONS or FQ-GAP-BORN-UNIQUENESS-GLEASON.

## Source status

Kernel-checked implication born_of_uniformlyRayContinuous in lean4/GleasonGaussianBridge.lean (0 sorry; axioms propext, Classical.choice, Quot.sound), built on Gleason's theorem for frame functions continuous away from the origin on the real sphere (lean4/GleasonRealSphere.lean) and on the complex sphere (lean4/GleasonComplexSphere.lean) and on the orthogonal parallelogram rigidity of lean4/BornGaussianParallelogramRigidity.lean. The hypothesis IsUniformlyRayContinuous f is declared, not derived: it is a mathematical input that requires justification before the theorem applies to a given f. Replay receipt: dag/research/campaign_fq-gleason-qi3-frame-functions_analytic_lean_replay.json. Recorded 2026-11-03 as a separate conditional result; the pointwise-continuity targets of FQ-GLEASON-QI3-FRAME-FUNCTIONS and FQ-GAP-BORN-UNIQUENESS-GLEASON keep their statements and statuses.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianParallelogramRigidity.lean`

- file: [lean4/BornGaussianParallelogramRigidity.lean](../../../lean4/BornGaussianParallelogramRigidity.lean)
- sha256 (`bytes`): `c384e1993ba8ecc2e9abbe75503b71b6e563c2ebd98f6a42d06310a23644733c`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build BornGaussianParallelogramRigidity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.signed_rigidity_of_orthoParallelogramZero_residual` | yes | yes | yes | - | `#print axioms BornFinite.GaussianTomography.signed_rigidity_of_orthoParallelogramZero_residual` |

- counts toward the grade: yes

### Lean: `lean4/GleasonComplexSphere.lean`

- file: [lean4/GleasonComplexSphere.lean](../../../lean4/GleasonComplexSphere.lean)
- sha256 (`bytes`): `72f3eaf6b95f5efaaca94bf90fb639b6849659b869c74ae6df03b3c912743ccc`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build GleasonComplexSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonComplex.gleason_complex` | yes | yes | yes | - | `#print axioms GleasonComplex.gleason_complex` |

- counts toward the grade: yes

### Lean: `lean4/GleasonGaussianBridge.lean`

- file: [lean4/GleasonGaussianBridge.lean](../../../lean4/GleasonGaussianBridge.lean)
- sha256 (`bytes`): `14f8dcb078c889c6acd220703697eea784d9d65b95c442972b63476f7c17e55f`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build GleasonGaussianBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GleasonBridge.IsUniformlyRayContinuous` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.IsUniformlyRayContinuous` |
| `BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` |
| `BornFinite.GleasonBridge.isFrameFunctionC_F` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.isFrameFunctionC_F` |
| `BornFinite.GleasonBridge.raySinSq` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.raySinSq` |
| `BornFinite.GleasonBridge.residual_orthoParallelogram` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.residual_orthoParallelogram` |

- counts toward the grade: yes

### Lean: `lean4/GleasonRealSphere.lean`

- file: [lean4/GleasonRealSphere.lean](../../../lean4/GleasonRealSphere.lean)
- sha256 (`bytes`): `ecd7c942cfa705269182348b834edc16e89165c4c4a05aaba7368ae401f85efb`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build GleasonRealSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonReal.gleason_real` | yes | yes | yes | - | `#print axioms GleasonReal.gleason_real` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1056_fq_gleason_qi3_uniform_ray_continuity.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1056_fq_gleason_qi3_uniform_ray_continuity.md](../../../dag/derivations/10_finite_qm_core/tfq_1056_fq_gleason_qi3_uniform_ray_continuity.md)
- sha256 (`lf-normalised`): `094a178fa9350272c5f887ad8f391924b914b220447980616f649a35776cfbaf`
- generated view: listed, not counted
- cited in: record TFQ-1056
- counts toward the grade: no

### Documents and data: `dag/research/campaign_fq-gleason-qi3-frame-functions_analytic_lean_replay.json`

- file: [dag/research/campaign_fq-gleason-qi3-frame-functions_analytic_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_analytic_lean_replay.json)
- sha256 (`lf-normalised`): `d9c75240cb29d1d523acdaf6f0876935dc36014c2967f73994b68c89470cd78c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pointwise_vs_uniform_note.md`

- file: [dag/research/pointwise_vs_uniform_note.md](../../../dag/research/pointwise_vs_uniform_note.md)
- sha256 (`lf-normalised`): `c8316ac1e62c6d8dc9ab90112a33bea973294dd4d3e85f257729e8d6500e7b7e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

