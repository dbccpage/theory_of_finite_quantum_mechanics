# FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let f : GVec -\> Q be a frame function on Q(i)^3 (IsFrameFunction f). Decide whether Archimedean continuity of f at every nonzero vector (IsArchimedeanContinuousEverywhere f: pointwise epsilon-delta continuity in the Euclidean squared distance distSqVec) implies uniform continuity on rays (IsUniformlyRayContinuous f: one rational delta per rational epsilon in the squared ray distance raySinSq). State separately the signed version (all frame functions) and the nonnegative version (IsNonnegFrameFunction f) needed by the original targets; the signed version implies the nonnegative one.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

For arbitrary functions on a dense non-compact domain the implication fails (h(q) = 1 for q \> sqrt(2)/2 and 0 otherwise, on Q intersected with \[0,1\], is continuous at every point of its domain and not uniformly continuous; a topological illustration only, not a frame function). Known: a zero-weight residual supported in a cap of angular radius below 45 degrees vanishes on the cap, assuming each ray of the cap completes to an admissible rational orthogonal frame, so that particular localized construction is ruled out; the valuation-defined residuals s3, s7, sp are nowhere Archimedean continuous and are not candidates. Not known: whether a counterexample must be global, whether one exists at all, or an epsilon-free rigidity argument that fixes a pole. A positive answer would make FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY apply to every pointwise-continuous frame function; a negative answer would be a pointwise-continuous non-quadratic frame function. Neither the unsuccessful attempts nor the conditional theorem settle the pointwise targets.

## Source status

Named open sub-question recorded 2026-11-03 after a bounded-time attempt (dag/research/pointwise_vs_uniform_note.md): the epsilon-version of the Cooke-Keane-Moran descent from a rational near-maximiser did not close because the per-step loss accumulates over unboundedly many Piron steps near equal latitudes; the two-step Piron multiplier products (1 + ti)(1 + si) are not dense in C; no counterexample is established. Proof exploration paused by the maintainer.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianTomographyReduction.lean`

- file: [lean4/BornGaussianTomographyReduction.lean](../../../lean4/BornGaussianTomographyReduction.lean)
- sha256 (`bytes`): `745cd957f5d93e9bcb10f2f28154d779a152f9718caf4fcc788d7a714c3a371a`
- cited in: node.lean, node.source, record TFQ-1057
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianTomographyReduction`): recorded sha256 `745cd957f5d93e9bcb10f2f28154d779a152f9718caf4fcc788d7a714c3a371a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianTomographyReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.IsArchimedeanContinuousAt` | yes | yes | yes | module-level | `#print axioms BornFinite.GaussianTomography.IsArchimedeanContinuousAt` |
| `BornFinite.GaussianTomography.IsArchimedeanContinuousEverywhere` | yes | yes | yes | module-level | `#print axioms BornFinite.GaussianTomography.IsArchimedeanContinuousEverywhere` |

- counts toward the grade: yes

### Lean: `lean4/GleasonGaussianBridge.lean`

- file: [lean4/GleasonGaussianBridge.lean](../../../lean4/GleasonGaussianBridge.lean)
- sha256 (`bytes`): `14f8dcb078c889c6acd220703697eea784d9d65b95c442972b63476f7c17e55f`
- cited in: node.lean, node.source, record TFQ-1057
- replay: `none`
- check: `cd lean4 && lake build GleasonGaussianBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GleasonBridge.IsUniformlyRayContinuous` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.IsUniformlyRayContinuous` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1057_fq_gleason_qi3_pointwise_to_uniform.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1057_fq_gleason_qi3_pointwise_to_uniform.md](../../../dag/derivations/10_finite_qm_core/tfq_1057_fq_gleason_qi3_pointwise_to_uniform.md)
- sha256 (`lf-normalised`): `ef6afcb339fc2f3716ceb15906d982b5c766a336901a97f3ef87d8ca945b24a8`
- generated view: listed, not counted
- cited in: record TFQ-1057
- counts toward the grade: no

### Documents and data: `dag/research/pointwise_vs_uniform_note.md`

- file: [dag/research/pointwise_vs_uniform_note.md](../../../dag/research/pointwise_vs_uniform_note.md)
- sha256 (`lf-normalised`): `c8316ac1e62c6d8dc9ab90112a33bea973294dd4d3e85f257729e8d6500e7b7e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (0):


No incoming route.
