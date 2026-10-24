# FSP-BF-2GROUP-SIGN-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Narrowed algebraic checks only. Explicit low-degree simplicial coboundaries on Fin 5 compose to zero and preserve the displayed curvatures under exact shifts. The ZMod 2 product cocycle is not any displayed 2-coboundary, as detected by the explicit three-term functional. Two supplied integer involutions have commutator -I. Crossed-module identity formulas reduce to reflexivity and do not construct an arbitrary crossed module. There is no identification with Wang-Levin braiding, a path integral, or a unique physical cancellation mechanism. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-046 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspBf2GroupSignClaim.lean`

- file: [lean4/CampaignFspBf2GroupSignClaim.lean](../../../lean4/CampaignFspBf2GroupSignClaim.lean)
- sha256 (`bytes`): `2ecf83152cc14542336d294520b8d3e727d8b134273e05fa2421a3d5acd66843`
- cited in: node.lean, record TFQ-1210
- replay: `verified`
  - receipt [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json) (module `CampaignFspBf2GroupSignClaim`): recorded sha256 `2ecf83152cc14542336d294520b8d3e727d8b134273e05fa2421a3d5acd66843` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspBf2GroupSignClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspBf2GroupSignClaim.bf_cochain_gauge_invariance` | yes | yes | yes | propext | `#print axioms CampaignFspBf2GroupSignClaim.bf_cochain_gauge_invariance` |
| `CampaignFspBf2GroupSignClaim.bf_z2_level_hopf_link_sign_and_weight_trichotomy` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.bf_z2_level_hopf_link_sign_and_weight_trichotomy` |
| `CampaignFspBf2GroupSignClaim.bf_z3_level_non_involution_and_cos_sum_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.bf_z3_level_non_involution_and_cos_sum_fence` |
| `CampaignFspBf2GroupSignClaim.crossed_module_conjugation_peiffer_and_identity` | yes | yes | yes | propext | `#print axioms CampaignFspBf2GroupSignClaim.crossed_module_conjugation_peiffer_and_identity` |
| `CampaignFspBf2GroupSignClaim.doubled_partition_function_changes_target_model_fence` | yes | yes | yes | propext | `#print axioms CampaignFspBf2GroupSignClaim.doubled_partition_function_changes_target_model_fence` |
| `CampaignFspBf2GroupSignClaim.one_form_double_vs_conjugate_two_group_postnikov_cancellation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.one_form_double_vs_conjugate_two_group_postnikov_cancellation` |
| `CampaignFspBf2GroupSignClaim.postnikov_cup3_is_3cocycle_on_zmod2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.postnikov_cup3_is_3cocycle_on_zmod2` |
| `CampaignFspBf2GroupSignClaim.postnikov_cup3_not_coboundary_in_H3_zmod2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.postnikov_cup3_not_coboundary_in_H3_zmod2` |
| `CampaignFspBf2GroupSignClaim.simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2` | yes | yes | yes | propext | `#print axioms CampaignFspBf2GroupSignClaim.simplicial_coboundary_nilpotence_d1d0_d2d1_d3d2` |
| `CampaignFspBf2GroupSignClaim.two_connection_postnikov_3curvature_bianchi` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.two_connection_postnikov_3curvature_bianchi` |
| `CampaignFspBf2GroupSignClaim.wang_levin_ising_commutator_negative_trace_and_abelian_commutation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspBf2GroupSignClaim.wang_levin_ising_commutator_negative_trace_and_abelian_commutation` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md`

- file: [dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md](../../../dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md)
- sha256 (`lf-normalised`): `2ed355d7c52e7dfd643bd49a79e9cf140110e6ddcf2598529eb28d10fb276279`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1210
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-bf-2group-sign-claim.md`

- file: [dag/derivations/independent/fsp-bf-2group-sign-claim.md](../../../dag/derivations/independent/fsp-bf-2group-sign-claim.md)
- sha256 (`lf-normalised`): `68f306da33ac4d99ab0c3e272f52cf67edbb99d8eb4833f57edae127ebd5df82`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-bf-2group-sign-claim_independent.json`

- file: [dag/research/campaign_fsp-bf-2group-sign-claim_independent.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_independent.json)
- sha256 (`lf-normalised`): `948cc9e0747f006b091eb7ea22c17fbec09198f5873694e8105d78f8516996dd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-bf-2group-sign-claim_lean_mutation.json`

- file: [dag/research/campaign_fsp-bf-2group-sign-claim_lean_mutation.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_mutation.json)
- sha256 (`lf-normalised`): `fa4c3dc6b0d0de062e9a6a5be9fa240ee224665c66717d8f774ad36102296e25`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json)
- sha256 (`lf-normalised`): `73d02deedd5d0276d19ba3c4781dbf89be68c3c6282ec606ffd0d7e323213654`
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

- `APP-R-FSP-BF-2GROUP-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-COBORDISM-INTRINSIC-SIGN` `GAP_NO_DERIVATION`: [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)
- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)
