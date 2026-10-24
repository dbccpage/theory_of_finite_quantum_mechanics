# FSP-PACHNER-INVARIANCE-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a discrete topological partition function on 4D triangulations is invariant under the 1-5, 2-4 and 3-3 Pachner moves; the source names no state-sum model, and the Regge action itself is not Pachner invariant.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fix a state-sum model (for example a Crane-Yetter type sum) and check its move invariance; nothing here bears on fermion signs. Narrowed in lean4/CampaignFspPachnerInvarianceClaim.lean and checks/independent/fsp-pachner-invariance-claim.py while keeping status OPEN to: (1) Euler-Poincare characteristic chi = N_0 - N_1 + N_2 - N_3 + N_4 invariance, move invertibility, and codimension-1 Dehn-Sommerville invariance 2 N_3 - 5 N_4 = 0 across all 4D bistellar Pachner moves (1\<-\>5, 2\<-\>4, 3\<-\>3); (2) exact surgical face-vector trajectory (6, 15, 20, 15, 6) -\> (7, 20, 30, 25, 10) -\> (7, 21, 34, 30, 12) -\> (7, 21, 34, 30, 12) on partial Delta^5 = S^4 matching Simplicial4DManifold in code/python/src/fsp/regge_pachner_wdw.py; (3) exact counterterm characterization w_0 = 10 w_2 + 15 w_3 + 6 w_4 and w_1 = -4 w_2 - 5 w_3 - 2 w_4 for linear state-sum invariance and vertex normalization invariance G^{-N_0} |Flat| for finite-group flat gauge bundles; and (4) non-invariance of the curved Regge action and curved WDW defect mass 3 N_1 (45 \< 60 \< 63), plus scope fences for signed rational hinge deficit cancellation, unnormalized 4-simplex weight failure, and fermion-sign independence.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-050 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspPachnerInvarianceClaim.lean`

- file: [lean4/CampaignFspPachnerInvarianceClaim.lean](../../../lean4/CampaignFspPachnerInvarianceClaim.lean)
- sha256 (`bytes`): `b9803f5c9fbf45b32716f9232722785f104440bbd27b79ce5423f2be040407bb`
- cited in: node.lean, receipt dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json (CampaignFspPachnerInvarianceClaim), record TFQ-1214
- replay: `verified`
  - receipt [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json) (module `CampaignFspPachnerInvarianceClaim`): recorded sha256 `b9803f5c9fbf45b32716f9232722785f104440bbd27b79ce5423f2be040407bb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspPachnerInvarianceClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspPachnerInvarianceClaim.curved_wdw_defect_mass_shifts_under_pachner_moves` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.curved_wdw_defect_mass_shifts_under_pachner_moves` |
| `CampaignFspPachnerInvarianceClaim.dehn_sommerville_codim1_invariant_under_pachner_moves` | yes | yes | yes | propext | `#print axioms CampaignFspPachnerInvarianceClaim.dehn_sommerville_codim1_invariant_under_pachner_moves` |
| `CampaignFspPachnerInvarianceClaim.linear_topological_state_sum_pachner_invariance_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.linear_topological_state_sum_pachner_invariance_iff` |
| `CampaignFspPachnerInvarianceClaim.pachner_moves_independent_of_fermion_sign_fence` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.pachner_moves_independent_of_fermion_sign_fence` |
| `CampaignFspPachnerInvarianceClaim.pachner_moves_preserve_euler_characteristic` | yes | yes | yes | propext | `#print axioms CampaignFspPachnerInvarianceClaim.pachner_moves_preserve_euler_characteristic` |
| `CampaignFspPachnerInvarianceClaim.regge_action_non_invariant_under_curved_pachner_subdivision` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.regge_action_non_invariant_under_curved_pachner_subdivision` |
| `CampaignFspPachnerInvarianceClaim.s4_seed_surgical_sequence_face_vectors_and_chi` | yes | yes | yes | none | `#print axioms CampaignFspPachnerInvarianceClaim.s4_seed_surgical_sequence_face_vectors_and_chi` |
| `CampaignFspPachnerInvarianceClaim.signed_hinge_deficits_can_cancel_under_pachner_move_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.signed_hinge_deficits_can_cancel_under_pachner_move_fence` |
| `CampaignFspPachnerInvarianceClaim.unnormalized_simplex_weight_fails_pachner_invariance_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.unnormalized_simplex_weight_fails_pachner_invariance_fence` |
| `CampaignFspPachnerInvarianceClaim.z2_gauge_state_sum_vertex_normalization_invariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspPachnerInvarianceClaim.z2_gauge_state_sum_vertex_normalization_invariance` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md`

- file: [dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md](../../../dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md)
- sha256 (`lf-normalised`): `42380cb36169d415858344b8ec08c171f8e448ec08334c16c05ae5724eca9421`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1214
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-pachner-invariance-claim.md`

- file: [dag/derivations/independent/fsp-pachner-invariance-claim.md](../../../dag/derivations/independent/fsp-pachner-invariance-claim.md)
- sha256 (`lf-normalised`): `d3715e8c1f627c11ccf35a5c5d4e94e6f9b58f9895cf7e15cb41fef65cf33446`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-pachner-invariance-claim_independent.json`

- file: [dag/research/campaign_fsp-pachner-invariance-claim_independent.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_independent.json)
- sha256 (`lf-normalised`): `41a932013778086f134e4f4bfeb9283ecbc555bd9ead66fe18e2c652143c768f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-pachner-invariance-claim_lean_mutation.json`

- file: [dag/research/campaign_fsp-pachner-invariance-claim_lean_mutation.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_mutation.json)
- sha256 (`lf-normalised`): `32dbd2e24ad9d43fc73dd2f541548b7a3a5befb4cc3ded55408ee8f79cb8a59f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json)
- sha256 (`lf-normalised`): `ddeb60b14042ddc326e980c0cade45a0f9dbb1087a5bb3e711d51b8dca20bfab`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `GAP_NO_DERIVATION`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
