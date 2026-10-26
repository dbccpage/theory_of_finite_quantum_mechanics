# FSP-DISCRETE-WDW-CONSTRAINT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a discrete Wheeler-DeWitt operator H_perp on spatial triangulations is nonnegative and acts as a projection on diffeomorphism-invariant states; no such operator is constructed here, and the DeWitt supermetric of the continuum constraint is indefinite.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is a declared finite-dimensional integer model; its set of integer triples is infinite. It constructs no discrete Wheeler-DeWitt operator, triangulation dynamics, diffeomorphism action, physical state space or continuum limit. Its counterexample concerns an inference from symmetry and a nonzero kernel to positivity or idempotence, not a specified gravitational model. Original target retained as an obligation: Claimed: a discrete Wheeler-DeWitt operator H_perp on spatial triangulations is nonnegative and acts as a projection on diffeomorphism-invariant states; no such operator is constructed here, and the DeWitt supermetric of the continuum constraint is indefinite. Prior boundary: Construct H_perp on a declared finite state space and determine its spectrum; the manuscript separates the constraint H_perp Psi = 0 from thermal Hamiltonians (Section 2.5).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-049 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignConstraintKernelProjector.lean`

- file: [lean4/CampaignConstraintKernelProjector.lean](../../../lean4/CampaignConstraintKernelProjector.lean)
- sha256 (`bytes`): `4a01928ee24ba7b0f5432ede8b95a1c974f09ba942a596f849a6df520946b0d6`
- cited in: node.lean, receipt dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json (CampaignConstraintKernelProjector), record TFQ-1213
- replay: `verified`
  - receipt [dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json) (module `CampaignConstraintKernelProjector`): recorded sha256 `4a01928ee24ba7b0f5432ede8b95a1c974f09ba942a596f849a6df520946b0d6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignConstraintKernelProjector`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignConstraintKernelProjector.Vec` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.Vec` |
| `CampaignConstraintKernelProjector.constraint` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.constraint` |
| `CampaignConstraintKernelProjector.constraint_is_indefinite` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.constraint_is_indefinite` |
| `CampaignConstraintKernelProjector.constraint_is_not_projector` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.constraint_is_not_projector` |
| `CampaignConstraintKernelProjector.constraint_symmetric` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignConstraintKernelProjector.constraint_symmetric` |
| `CampaignConstraintKernelProjector.dot` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.dot` |
| `CampaignConstraintKernelProjector.kernel_characterization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignConstraintKernelProjector.kernel_characterization` |
| `CampaignConstraintKernelProjector.nontrivial_kernel` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.nontrivial_kernel` |
| `CampaignConstraintKernelProjector.project` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.project` |
| `CampaignConstraintKernelProjector.projected_vector_satisfies_constraint` | yes | yes | yes | propext | `#print axioms CampaignConstraintKernelProjector.projected_vector_satisfies_constraint` |
| `CampaignConstraintKernelProjector.projection_residual_orthogonal_to_kernel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignConstraintKernelProjector.projection_residual_orthogonal_to_kernel` |
| `CampaignConstraintKernelProjector.projector_fixes_exactly_kernel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignConstraintKernelProjector.projector_fixes_exactly_kernel` |
| `CampaignConstraintKernelProjector.projector_idempotent` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.projector_idempotent` |
| `CampaignConstraintKernelProjector.subtract` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.subtract` |
| `CampaignConstraintKernelProjector.zero` | yes | yes | yes | none | `#print axioms CampaignConstraintKernelProjector.zero` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-discrete-wdw-constraint.py`

- file: [checks/independent/fsp-discrete-wdw-constraint.py](../../../checks/independent/fsp-discrete-wdw-constraint.py)
- sha256 (`bytes`): `02ffa1ea9c9499c659e38294266fd328ef7227cce9975b28b837ceac8ecf2790`
- cited in: record TFQ-1213
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md`

- file: [dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md](../../../dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md)
- sha256 (`lf-normalised`): `10bd8dd266745158896eb4090925b2e6183b1ff622f713c1f7ab9ad86401b9a4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1213
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-discrete-wdw-constraint.md`

- file: [dag/derivations/independent/fsp-discrete-wdw-constraint.md](../../../dag/derivations/independent/fsp-discrete-wdw-constraint.md)
- sha256 (`lf-normalised`): `9009d23304505e8486c5423f1d9dc88d99036f17379f457fae9e8e9e6129c153`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json`

- file: [dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json)
- sha256 (`lf-normalised`): `039fd027ed60fb98aa3d5adcf76c6328fc8982740f3cd34ad3d9166881ab7156`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
