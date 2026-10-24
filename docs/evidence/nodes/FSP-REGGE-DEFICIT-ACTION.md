# FSP-REGGE-DEFICIT-ACTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a 4D triangulation with squared edge lengths, the deficit angle at a hinge h is epsilon_h = 2 pi - sum of dihedral angles at h and the Regge action is S = sum_h A_h epsilon_h; its convergence to the Einstein-Hilbert action under refinement is a literature result imported here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Regge calculus (Regge 1961; Cheeger-Mueller-Schrader convergence)

## Bottleneck

Narrowed algebraic checks only. The declared rational Heron polynomial is symmetric and has the displayed evaluations; a supplied rational dot product is bilinear and an additive four-step telescoping sum is zero. Schlaefli cancellation is an explicit hypothesis, not derived geometry. The face vector and its interpretation as a sphere are supplied. No edge-length geometry, noncommutative Bianchi identity, continuum refinement theorem or actual Lorentzian exponential is constructed. The -I matrix and w-w identity do not identify a gravitational phase or resolve fermion signs. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-048 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspReggeDeficitAction.lean`

- file: [lean4/CampaignFspReggeDeficitAction.lean](../../../lean4/CampaignFspReggeDeficitAction.lean)
- sha256 (`bytes`): `37bbdca7459fc734d959bd223bdd3655f253e32800e9d50712c37c3241c6d91e`
- cited in: node.lean, record TFQ-1212
- replay: `verified`
  - receipt [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json) (module `CampaignFspReggeDeficitAction`): recorded sha256 `37bbdca7459fc734d959bd223bdd3655f253e32800e9d50712c37c3241c6d91e` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspReggeDeficitAction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspReggeDeficitAction.defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.defectBoundHolds_exact_rust_witnesses_and_zero_scale_limit` |
| `CampaignFspReggeDeficitAction.discrete_bianchi_cyclic_holonomy_telescoping` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.discrete_bianchi_cyclic_holonomy_telescoping` |
| `CampaignFspReggeDeficitAction.euclidean_vs_lorentzian_regge_phase_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.euclidean_vs_lorentzian_regge_phase_fence` |
| `CampaignFspReggeDeficitAction.flat_vertex_sum_vs_signed_cancellation_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.flat_vertex_sum_vs_signed_cancellation_fence` |
| `CampaignFspReggeDeficitAction.heronAreaSq_symmetric_and_orthogonal_pentatope_hinges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.heronAreaSq_symmetric_and_orthogonal_pentatope_hinges` |
| `CampaignFspReggeDeficitAction.hingeDeficit_flat_sum_zero_and_reggeAction_bilinear` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.hingeDeficit_flat_sum_zero_and_reggeAction_bilinear` |
| `CampaignFspReggeDeficitAction.reggeAction_positive_vs_mixed_deficit_sign` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.reggeAction_positive_vs_mixed_deficit_sign` |
| `CampaignFspReggeDeficitAction.regge_action_independent_of_fermion_occupation_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.regge_action_independent_of_fermion_occupation_fence` |
| `CampaignFspReggeDeficitAction.s4_boundary_delta5_face_counts_and_euler_characteristic` | yes | yes | yes | propext | `#print axioms CampaignFspReggeDeficitAction.s4_boundary_delta5_face_counts_and_euler_characteristic` |
| `CampaignFspReggeDeficitAction.schlaefli_variation_reduces_regge_variation_to_area_term` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspReggeDeficitAction.schlaefli_variation_reduces_regge_variation_to_area_term` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md`

- file: [dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md](../../../dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md)
- sha256 (`lf-normalised`): `ce941d33c5f62e277a4ebfca055c4734a5e6f2ebc8648476bd816cfaee336ddb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1212
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-regge-deficit-action.md`

- file: [dag/derivations/independent/fsp-regge-deficit-action.md](../../../dag/derivations/independent/fsp-regge-deficit-action.md)
- sha256 (`lf-normalised`): `e8fda0d8fdd12038635d238f713e3c679c654f5187592980593cbfcae36bb704`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-regge-deficit-action_independent.json`

- file: [dag/research/campaign_fsp-regge-deficit-action_independent.json](../../../dag/research/campaign_fsp-regge-deficit-action_independent.json)
- sha256 (`lf-normalised`): `050e689b7f1d04b97da73d6425f793e333e1f6cdaa558c2d265936a465420316`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-regge-deficit-action_lean_mutation.json`

- file: [dag/research/campaign_fsp-regge-deficit-action_lean_mutation.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_mutation.json)
- sha256 (`lf-normalised`): `390fa9b55e2299d1e9d3c5676bdb0f028388ba8df754aab53c0ae5f5f9757a9b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-regge-deficit-action_lean_replay.json`

- file: [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json)
- sha256 (`lf-normalised`): `6a40012e5319cb3f5e047652effd7b0c48e7526f575e5e8c8470901b2e99c159`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-DEGREE-K-TORSION-BALANCE](PGW-WDP-DEGREE-K-TORSION-BALANCE.md) (PROVED_PROSE), [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN)
- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `GAP_NO_DERIVATION`: [FSP-PACHNER-INVARIANCE-CLAIM](FSP-PACHNER-INVARIANCE-CLAIM.md) (OPEN)
