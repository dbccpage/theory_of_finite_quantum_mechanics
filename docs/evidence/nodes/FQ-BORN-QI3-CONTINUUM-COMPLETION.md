# FQ-BORN-QI3-CONTINUUM-COMPLETION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Package a unique continuous extension of a uniformly ray-continuous nonnegative rational frame function on Q(i)^3 to all complex rays, represented by the embedded tomography matrix with Hermitian symmetry, trace one and complex positive semidefiniteness. Also prove the general converse instance IsUniformlyRayContinuous (quadRay rho). This target retains uniform continuity; it is not the pointwise-to-uniform problem.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- uniform ray continuity
- nonnegativity
- complex completion and rational density

## Bottleneck

Formalize the matrix embedding, PSD by density, equality and uniqueness of the continuous extension, and a quantitative modulus for quadRay. Rational-valued data reconstruct only Gaussian-rational coefficients: covering arbitrary complex density matrices needs real-valued data or a separate approximation theorem. Higher dimensions require compatible three-dimensional gluing; infinite dimensions additionally need suitable normality/countable additivity and control of trace in limits.

## Source status

Existing extension, scale-invariance, continuity, frame, rational Born, trace and uniqueness lemmas supply the main ingredients. The independent review checks constant-function nonvacuity and nonnegativity of the rational quadratic numerator; no complete complex PSD/unique-extension wrapper is claimed.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianTomographyReduction.lean`

- file: [lean4/BornGaussianTomographyReduction.lean](../../../lean4/BornGaussianTomographyReduction.lean)
- sha256 (`bytes`): `745cd957f5d93e9bcb10f2f28154d779a152f9718caf4fcc788d7a714c3a371a`
- cited in: node.lean, node.source, record TFQ-1060
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianTomographyReduction`): recorded sha256 `745cd957f5d93e9bcb10f2f28154d779a152f9718caf4fcc788d7a714c3a371a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianTomographyReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianTomography.tomography_trace_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_trace_one` |
| `BornFinite.GaussianTomography.tomography_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianTomography.tomography_unique` |

- counts toward the grade: yes

### Lean: `lean4/GleasonGaussianBridge.lean`

- file: [lean4/GleasonGaussianBridge.lean](../../../lean4/GleasonGaussianBridge.lean)
- sha256 (`bytes`): `14f8dcb078c889c6acd220703697eea784d9d65b95c442972b63476f7c17e55f`
- cited in: node.lean, node.source, record TFQ-1060
- replay: `none`
- check: `cd lean4 && lake build GleasonGaussianBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GleasonBridge.F_ι` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.F_ι` |
| `BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` |
| `BornFinite.GleasonBridge.continuousOn_F` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.continuousOn_F` |
| `BornFinite.GleasonBridge.isFrameFunctionC_F` | yes | yes | yes | - | `#print axioms BornFinite.GleasonBridge.isFrameFunctionC_F` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1060_fq_born_qi3_continuum_completion.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1060_fq_born_qi3_continuum_completion.md](../../../dag/derivations/10_finite_qm_core/tfq_1060_fq_born_qi3_continuum_completion.md)
- sha256 (`lf-normalised`): `85de6f465fe6b2556943ab3aff3187d6c1105c6ab6a9aaa66ab6ebfd8d5b6a57`
- generated view: listed, not counted
- cited in: record TFQ-1060
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

- `FQ-R-BORN-QI3-CONTINUUM-COMPLETION` `GAP_NO_DERIVATION`: [FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY](FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY.md) (CONDITIONAL), [FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS](FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS.md) (CONDITIONAL)

Outgoing (0):

