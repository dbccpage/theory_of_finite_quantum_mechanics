# FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let f : GVec -\> Q be a signed frame function on Q(i)^3 (IsFrameFunction f: f(u) + f(v) + f(w) = 1 for every triple of nonzero pairwise orthogonal vectors; no sign condition). Suppose f is uniformly continuous on rays (IsUniformlyRayContinuous f): for every rational epsilon \> 0 there is a rational delta \> 0 such that |f(u) - f(v)| \< epsilon whenever u, v are nonzero and raySinSq u v = 1 - |\<u,v\>|^2/(\<u,u\>\<v,v\>) \< delta, where raySinSq is a squared ray distance (phase and scale invariant) whose square root is the corresponding metric on rays. Then f(v) = quadRay (tomographyForm f) v = \<v, rho v\>/\<v, v\> for every nonzero v, with rho the Hermitian trace-one matrix reconstructed from the nine tomography rays. The nonnegative version (IsNonnegFrameFunction f) is the special case of a nonnegative f.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Q(i)^3 with its standard Hermitian form and the normalized orthogonal-frame identity (signed values permitted)
- uniform continuity of f on rays (IsUniformlyRayContinuous f): declared input, not derived
- real/complex completeness and compactness in the continuous-C^3 proof backend; no Born pairing, dynamics or tensor axiom is an input

## Bottleneck

Uniform ray continuity remains a declared hypothesis. Pointwise-to-uniform for rational frame functions is TFQ-1057, with signed and nonnegative cases separate. A finite instrument at one tolerance supplies only one epsilon-delta pair. General uniform continuity of quadRay and the packaged unique complex PSD trace-one extension are kernel-checked in FQ-BORN-QI3-CONTINUUM-COMPLETION, which is CONDITIONAL on the same declared input. TFQ-1055 asks about unrestricted frame functions and its unrestricted assertion is REFUTED; TFQ-0307 remains CONDITIONAL.

## Source status

Kernel-checked signed implication born_of_uniformlyRayContinuous, with uniform ray continuity supplied as a hypothesis. Independently rebuilt the eight-module project import closure and audited all 302 named declarations in the four new modules at PR #500 head 45b0b093921aa0281969f92da18694e2e89c3cc4; only propext, Classical.choice and Quot.sound occur. The continuum backend is the continuous-C^3 theorem, not automatic continuity from positivity. A review lemma instantiates the uniform hypothesis with f = 1/3. Original analytic receipt retained; independent raw audit and dependency pins are recorded separately. GleasonBornCompletion (FQ-BORN-QI3-CONTINUUM-COMPLETION) adds the general converse isUniformlyRayContinuous_quadRay and the characterization uniformlyRayContinuous_frameFunction_iff: the hypothesis class is exactly the trace-one rational Hermitian Rayleigh quotients.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianParallelogramRigidity.lean`

- file: [lean4/BornGaussianParallelogramRigidity.lean](../../../lean4/BornGaussianParallelogramRigidity.lean)
- sha256 (`bytes`): `58d5caf7a34808fddd8abd67eee6c8ae659f942ccaa7febf1cfdcb0da24be6d2`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build BornGaussianParallelogramRigidity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.signed_rigidity_of_orthoParallelogramZero_residual` | yes | yes | yes | - | `#print axioms BornFinite.GaussianTomography.signed_rigidity_of_orthoParallelogramZero_residual` |

- counts toward the grade: yes

### Lean: `lean4/GleasonBornCompletion.lean`

- file: [lean4/GleasonBornCompletion.lean](../../../lean4/GleasonBornCompletion.lean)
- sha256 (`bytes`): `e5cf793ba4626826123d8d8b0207b01dcca765e316e0c602985769c07b971646`
- cited in: node.lean, node.source, record TFQ-1056
- replay: `none`
- check: `cd lean4 && lake build GleasonBornCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay` |

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
- sha256 (`lf-normalised`): `5a196e4b9b8c0713e97b4a7814bd8043954b8ff58ce80d00ff30b7f1136136be`
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
- sha256 (`lf-normalised`): `9794356d43b714c238d1a49b55e3e10b153e1baccfae11683b1c1891de99980f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr500_review/manifest.json`

- file: [dag/research/pr500_review/manifest.json](../../../dag/research/pr500_review/manifest.json)
- sha256 (`lf-normalised`): `c32d8f516a5d51ea49c8a18535dc4423363527c2a7fcbe27681c2bf269ff2e5f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr500_review/review.md`

- file: [dag/research/pr500_review/review.md](../../../dag/research/pr500_review/review.md)
- sha256 (`lf-normalised`): `ba7c9cce9598da12b30e194be375b1c48bfd9df89ee5f3f7f95aed943d689e26`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-FRAME-CARRIERS](FQ-GLEASON-FRAME-CARRIERS.md) (DEFINITION), [FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS](FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS.md) (CONDITIONAL)

Outgoing (1):

- `FQ-R-BORN-QI3-CONTINUUM-COMPLETION` `CONDITIONAL_ON_IMPORT`: [FQ-BORN-QI3-CONTINUUM-COMPLETION](FQ-BORN-QI3-CONTINUUM-COMPLETION.md) (CONDITIONAL)
