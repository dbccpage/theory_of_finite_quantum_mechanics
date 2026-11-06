# FQ-GLEASON-FRAME-CARRIERS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Fix the mathematical carriers Q(i)^3, R^3 and C^3 with their standard Hermitian or real inner products. A rational frame function has rational values summing to one on every nonzero orthogonal triple. The real/complex frame-function structures have real values, a supplied weight W, nonzero-scalar invariance, and the orthogonal-frame identity. These are definitions and supplied carriers, not a derivation of Hilbert geometry or of Born probabilities from finite operational rules.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No Born pairing, tensor product, dynamics or quantum operational reconstruction is supplied by this definition. Q(i)^3 is countably infinite despite having dimension three.

## Source status

Narrow hypothesis inventory for the Gleason proof chain, separating carrier and frame definitions from FQ-DECLARED-QUANTUM-INTERFACE, whose Born pairing is not used here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianRationalFrameObstruction.lean`

- file: [lean4/BornGaussianRationalFrameObstruction.lean](../../../lean4/BornGaussianRationalFrameObstruction.lean)
- sha256 (`bytes`): `5564b1a4dd947620281406208466d2df9792aedc5e7eeae3073b7ba52a8134c2`
- cited in: node.lean, node.source, record TFQ-1058
- replay: `verified`
  - receipt [evidence/lean_receipts/born_gaussian_frames_lean_replay.json](../../../evidence/lean_receipts/born_gaussian_frames_lean_replay.json) (module `BornGaussianRationalFrameObstruction`): recorded sha256 `5564b1a4dd947620281406208466d2df9792aedc5e7eeae3073b7ba52a8134c2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalFrameObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.GVec` | yes | yes | yes | module-level | `#print axioms BornFinite.GaussianFrames.GVec` |
| `BornFinite.GaussianFrames.IsFrameFunction` | yes | yes | yes | module-level | `#print axioms BornFinite.GaussianFrames.IsFrameFunction` |

- counts toward the grade: yes

### Lean: `lean4/GleasonComplexSphere.lean`

- file: [lean4/GleasonComplexSphere.lean](../../../lean4/GleasonComplexSphere.lean)
- sha256 (`bytes`): `72f3eaf6b95f5efaaca94bf90fb639b6849659b869c74ae6df03b3c912743ccc`
- cited in: node.lean, node.source, record TFQ-1058
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_fq-born-qi3-continuum-completion_lean_replay.json](../../../evidence/lean_receipts/campaign_fq-born-qi3-continuum-completion_lean_replay.json) (module `GleasonComplexSphere`): recorded sha256 `72f3eaf6b95f5efaaca94bf90fb639b6849659b869c74ae6df03b3c912743ccc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonComplexSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonComplex.IsFrameFunctionC` | yes | yes | yes | module-level | `#print axioms GleasonComplex.IsFrameFunctionC` |

- counts toward the grade: yes

### Lean: `lean4/GleasonRealSphere.lean`

- file: [lean4/GleasonRealSphere.lean](../../../lean4/GleasonRealSphere.lean)
- sha256 (`bytes`): `ecd7c942cfa705269182348b834edc16e89165c4c4a05aaba7368ae401f85efb`
- cited in: node.lean, node.source, record TFQ-1058
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_fq-born-qi3-continuum-completion_lean_replay.json](../../../evidence/lean_receipts/campaign_fq-born-qi3-continuum-completion_lean_replay.json) (module `GleasonRealSphere`): recorded sha256 `ecd7c942cfa705269182348b834edc16e89165c4c4a05aaba7368ae401f85efb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonRealSphere`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GleasonReal.IsFrameFunction` | yes | yes | yes | module-level | `#print axioms GleasonReal.IsFrameFunction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1058_fq_gleason_frame_carriers.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1058_fq_gleason_frame_carriers.md](../../../dag/derivations/10_finite_qm_core/tfq_1058_fq_gleason_frame_carriers.md)
- sha256 (`lf-normalised`): `4ea593121001a9451acdbafc22c528fa626fd59d8570f60c7ad911b712be1bce`
- generated view: listed, not counted
- cited in: record TFQ-1058
- counts toward the grade: no

### Documents and data: `evidence/reviews/pr500/manifest.json`

- file: [evidence/reviews/pr500/manifest.json](../../../evidence/reviews/pr500/manifest.json)
- sha256 (`lf-normalised`): `c32d8f516a5d51ea49c8a18535dc4423363527c2a7fcbe27681c2bf269ff2e5f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `evidence/reviews/pr500/review.md`

- file: [evidence/reviews/pr500/review.md](../../../evidence/reviews/pr500/review.md)
- sha256 (`lf-normalised`): `ba7c9cce9598da12b30e194be375b1c48bfd9df89ee5f3f7f95aed943d689e26`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (4):

- `FQ-R-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS](FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS.md) (CONDITIONAL)
- `FQ-R-GLEASON-QI3-FRAME-FUNCTIONS` `DERIVED_LEAN`: [FQ-GLEASON-QI3-FRAME-FUNCTIONS](FQ-GLEASON-QI3-FRAME-FUNCTIONS.md) (REFUTED)
- `FQ-R-GLEASON-QI3-POINTWISE-TO-UNIFORM` `GAP_NO_DERIVATION`: [FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM](FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM.md) (OPEN)
- `FQ-R-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY](FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY.md) (CONDITIONAL)

No incoming route.
