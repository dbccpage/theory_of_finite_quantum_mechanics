# FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For F : C^3 -\> R and W : R, assume GleasonComplex.IsFrameFunctionC F W (complex nonzero-scalar invariance and weight W on each nonzero orthogonal triple) and ContinuousOn F {v | v != 0}. Then there is a complex orthonormal frame p,q,r and real coefficients M,alpha,m with F(v) = (M |\<p,v\>|^2 + alpha |\<q,v\>|^2 + m |\<r,v\>|^2)/||v||^2 for every nonzero v. Signed functions are allowed.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real/complex carriers, completeness and compactness
- frame identity and scalar invariance
- continuity away from zero

## Bottleneck

Automatic continuity from nonnegativity, arbitrary finite dimension, and an infinite-dimensional trace-class theorem are not conclusions of this declaration.

## Source status

gleason_complex and its real three-dimensional backend were independently rebuilt and all named declarations axiom-audited in PR #500. This is already a continuum-coordinate theorem under continuity, not the full nonnegative Gleason theorem without a regularity hypothesis.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GleasonComplexSphere.lean`

- file: [lean4/GleasonComplexSphere.lean](../../../lean4/GleasonComplexSphere.lean)
- sha256 (`bytes`): `72f3eaf6b95f5efaaca94bf90fb639b6849659b869c74ae6df03b3c912743ccc`
- cited in: node.lean, node.source, record TFQ-1059
- replay: `none`
- check: `cd lean4 && lake build GleasonComplexSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonComplex.gleason_complex` | yes | yes | yes | - | `#print axioms GleasonComplex.gleason_complex` |

- counts toward the grade: yes

### Lean: `lean4/GleasonRealSphere.lean`

- file: [lean4/GleasonRealSphere.lean](../../../lean4/GleasonRealSphere.lean)
- sha256 (`bytes`): `ecd7c942cfa705269182348b834edc16e89165c4c4a05aaba7368ae401f85efb`
- cited in: node.lean, node.source, record TFQ-1059
- replay: `none`
- check: `cd lean4 && lake build GleasonRealSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonReal.gleason_real` | yes | yes | yes | - | `#print axioms GleasonReal.gleason_real` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1059_fq_gleason_c3_continuous_frame_functions.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1059_fq_gleason_c3_continuous_frame_functions.md](../../../dag/derivations/10_finite_qm_core/tfq_1059_fq_gleason_c3_continuous_frame_functions.md)
- sha256 (`lf-normalised`): `0033f91250cb32d200df6d7cb501fddd28ad2d4f1e0decdc1dc3d7ea6f7835ce`
- generated view: listed, not counted
- cited in: record TFQ-1059
- counts toward the grade: no

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

- `FQ-R-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-FRAME-CARRIERS](FQ-GLEASON-FRAME-CARRIERS.md) (DEFINITION)

Outgoing (2):

- `FQ-R-BORN-QI3-CONTINUUM-COMPLETION` `CONDITIONAL_ON_IMPORT`: [FQ-BORN-QI3-CONTINUUM-COMPLETION](FQ-BORN-QI3-CONTINUUM-COMPLETION.md) (CONDITIONAL)
- `FQ-R-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY](FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY.md) (CONDITIONAL)
