# FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let f : GVec -\> Q be a frame function on Q(i)^3 (IsFrameFunction f). Decide whether Archimedean continuity of f at every nonzero vector (IsArchimedeanContinuousEverywhere f: pointwise epsilon-delta continuity in the Euclidean squared distance distSqVec) implies uniform continuity on rays (IsUniformlyRayContinuous f: one rational delta per rational epsilon in the squared ray distance raySinSq). State separately the signed version (all frame functions) and the nonnegative version (IsNonnegFrameFunction f) needed for probability-valued Born reconstruction; the signed version implies the nonnegative one.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
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

Prove pointwise-to-uniform for signed or, first, nonnegative rational frame functions, or give a counterexample satisfying the full frame identity and continuity everywhere. Nonnegative functions are bounded by frame completion; boundedness for the general signed pointwise case is not supplied. Existing selective-oscillation theorems exclude the cited nonzero finite valuation combinations by discontinuity at tomo_e1 under their stated hypotheses; they do not certify nowhere continuity of every sp. The small-cap argument rules out only that support construction. Suggested research: fixed-ray oscillation propagation or exact finite frame certificates with coefficients uniformly bounded as auxiliary rays approach fixed tomography anchors. Neither finite search failure nor arbitrary-chain approximation settles this node.

## Source status

Open regularity question in this repository. The bounded/nonnegative near-supremum descent attempt has no controlled accumulated-error argument when the pole varies and chains lengthen. Two-step products are not dense, but arbitrary finite rational Piron products approximate every complex multiplier of modulus greater than one by the real-chain theorem and finite-product continuity (paper argument in the review, not a new Lean theorem). This does not close the regularity argument. No pointwise-continuous non-quadratic counterexample is established by this review.

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
- sha256 (`lf-normalised`): `282b75846f6ae84ccbbecb2ace3e8c64a6c618d2b44f536d5254d6e6ca65bd48`
- generated view: listed, not counted
- cited in: record TFQ-1057
- counts toward the grade: no

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

- `FQ-R-GLEASON-QI3-POINTWISE-TO-UNIFORM` `GAP_NO_DERIVATION`: [FQ-GLEASON-FRAME-CARRIERS](FQ-GLEASON-FRAME-CARRIERS.md) (DEFINITION)

Outgoing (0):

