# FQ-BORN-QI3-CONTINUUM-COMPLETION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Package a unique continuous extension of a uniformly ray-continuous nonnegative rational frame function on Q(i)^3 to all complex rays, represented by the embedded tomography matrix with Hermitian symmetry, trace one and complex positive semidefiniteness. Also prove the general converse instance IsUniformlyRayContinuous (quadRay rho). This target retains uniform continuity; it is not the pointwise-to-uniform problem.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 16
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

The modulus in isUniformlyRayContinuous_quadRay is existential (Heine-Cantor on the compact unit sphere), not a quantitative delta in the coefficient norm; the paper estimate |q(u) - q(v)| \<= 2 ||rho|| sqrt(2 raySinSq u v) is not formalized. Rational-valued data reconstruct only Gaussian-rational coefficients: covering arbitrary complex density matrices needs real-valued data or a separate approximation theorem. Higher dimensions require compatible three-dimensional gluing; infinite dimensions additionally need suitable normality/countable additivity and control of trace in limits. Pointwise-to-uniform remains FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM (OPEN).

## Source status

Kernel-checked in lean4/GleasonBornCompletion.lean. born_density_matrix_of_uniformlyRayContinuous packages the extension F f of a nonnegative frame function that is uniformly continuous on rays as Re \<v, rhoC v\>/\<v, v\> on every nonzero v in C^3 (and f g = Re \<g, rhoC g\>/\<g, g\> on every nonzero g in Q(i)^3) for the positive semidefinite trace-one complex matrix rhoC = toMatrix (tomographyForm f), unique among Hermitian matrices with that property (eq_of_re_dotC_mulVec_self, polarization). F_eq_QcRay is the signed version without positivity. isUniformlyRayContinuous_quadRay is the general converse instance for every rational Hermitian form by compactness of the unit sphere of C^3 after phase alignment of unit representatives; uniformlyRayContinuous_frameFunction_iff then characterizes the uniformly ray-continuous frame functions on Q(i)^3 as exactly the trace-one rational Hermitian Rayleigh quotients. All 339 named declarations of the five Gleason modules carry #print axioms reports with only propext, Classical.choice and Quot.sound (dag/research/gleason_lean_audit.json, verified fail-closed by scripts/gleason_lean_audit.py and the hosted workflow lean-gleason). The declared uniform premise is retained, so the node is CONDITIONAL.

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

### Lean: `lean4/GleasonBornCompletion.lean`

- file: [lean4/GleasonBornCompletion.lean](../../../lean4/GleasonBornCompletion.lean)
- sha256 (`bytes`): `e5cf793ba4626826123d8d8b0207b01dcca765e316e0c602985769c07b971646`
- cited in: node.lean, node.source, record TFQ-1060
- replay: `none`
- check: `cd lean4 && lake build GleasonBornCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.BornCompletion.F_eq_QcRay` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.F_eq_QcRay` |
| `BornFinite.BornCompletion.born_density_matrix_of_uniformlyRayContinuous` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.born_density_matrix_of_uniformlyRayContinuous` |
| `BornFinite.BornCompletion.eq_of_re_dotC_mulVec_self` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.eq_of_re_dotC_mulVec_self` |
| `BornFinite.BornCompletion.eq_on_nonzero_of_eq_on_ι` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.eq_on_nonzero_of_eq_on_ι` |
| `BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.isUniformlyRayContinuous_quadRay` |
| `BornFinite.BornCompletion.toMatrix` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.toMatrix` |
| `BornFinite.BornCompletion.toMatrix_isHermitian` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.toMatrix_isHermitian` |
| `BornFinite.BornCompletion.toMatrix_posSemidef` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.toMatrix_posSemidef` |
| `BornFinite.BornCompletion.trace_toMatrix` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.trace_toMatrix` |
| `BornFinite.BornCompletion.uniformlyRayContinuous_frameFunction_iff` | yes | yes | yes | - | `#print axioms BornFinite.BornCompletion.uniformlyRayContinuous_frameFunction_iff` |

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
- sha256 (`lf-normalised`): `5803aa1490d88b1d8aa1a1529031c4c1af96a840e2a730435977134af50e7846`
- generated view: listed, not counted
- cited in: record TFQ-1060
- counts toward the grade: no

### Documents and data: `dag/research/campaign_fq-born-qi3-continuum-completion_lean_replay.json`

- file: [dag/research/campaign_fq-born-qi3-continuum-completion_lean_replay.json](../../../dag/research/campaign_fq-born-qi3-continuum-completion_lean_replay.json)
- sha256 (`lf-normalised`): `19d35178275f5e0444413be2cd519840a3111d5b8bc5b7d03c46d2272e050e0b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/gleason_lean_audit.json`

- file: [dag/research/gleason_lean_audit.json](../../../dag/research/gleason_lean_audit.json)
- sha256 (`lf-normalised`): `e4d40511530afe7735d1fa2a73fca294366d08de1634f7cb5e4dab41c2ded7ab`
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

- `FQ-R-BORN-QI3-CONTINUUM-COMPLETION` `CONDITIONAL_ON_IMPORT`: [FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY](FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY.md) (CONDITIONAL), [FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS](FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS.md) (CONDITIONAL)

Outgoing (0):

