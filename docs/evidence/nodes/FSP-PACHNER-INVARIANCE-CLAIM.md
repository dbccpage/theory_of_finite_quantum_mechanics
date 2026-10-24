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

Narrowed algebraic checks only. Five-integer face-vector translations preserve the displayed linear functionals; solving two rational linear equations characterizes invariant count weights. In Lean no simplicial complex, move admissibility, topology, or flat-connection extension count is constructed. The independent checker performs additional finite simplex-set examples, not a general refinement proof. normalizedFlatGaugeSum declares inverse-G cancellation for delta 0 and 1 and returns zero otherwise; it proves no gauge-bundle counting theorem. The Regge shift and WDW mass are supplied scalar formulas, not geometric action differences or constraint solutions. The stated face-count trajectories and arithmetic remain exact. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-050 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspPachnerInvarianceClaim.lean`

- file: [lean4/CampaignFspPachnerInvarianceClaim.lean](../../../lean4/CampaignFspPachnerInvarianceClaim.lean)
- sha256 (`bytes`): `3675c610049324080f9f9ed57539909efe180f959cebc77fff1c49f6ce6efec1`
- cited in: node.lean, record TFQ-1214
- replay: `verified`
  - receipt [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json) (module `CampaignFspPachnerInvarianceClaim`): recorded sha256 `3675c610049324080f9f9ed57539909efe180f959cebc77fff1c49f6ce6efec1` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspPachnerInvarianceClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspPachnerInvarianceClaim.curved_wdw_defect_mass_shifts_under_pachner_moves` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.curved_wdw_defect_mass_shifts_under_pachner_moves` |
| `CampaignFspPachnerInvarianceClaim.dehn_sommerville_codim1_invariant_under_pachner_moves` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.dehn_sommerville_codim1_invariant_under_pachner_moves` |
| `CampaignFspPachnerInvarianceClaim.linear_topological_state_sum_pachner_invariance_iff` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.linear_topological_state_sum_pachner_invariance_iff` |
| `CampaignFspPachnerInvarianceClaim.pachner_moves_independent_of_fermion_sign_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.pachner_moves_independent_of_fermion_sign_fence` |
| `CampaignFspPachnerInvarianceClaim.pachner_moves_preserve_euler_characteristic` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.pachner_moves_preserve_euler_characteristic` |
| `CampaignFspPachnerInvarianceClaim.regge_action_non_invariant_under_curved_pachner_subdivision` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.regge_action_non_invariant_under_curved_pachner_subdivision` |
| `CampaignFspPachnerInvarianceClaim.s4_seed_surgical_sequence_face_vectors_and_chi` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.s4_seed_surgical_sequence_face_vectors_and_chi` |
| `CampaignFspPachnerInvarianceClaim.signed_hinge_deficits_can_cancel_under_pachner_move_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.signed_hinge_deficits_can_cancel_under_pachner_move_fence` |
| `CampaignFspPachnerInvarianceClaim.unnormalized_simplex_weight_fails_pachner_invariance_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.unnormalized_simplex_weight_fails_pachner_invariance_fence` |
| `CampaignFspPachnerInvarianceClaim.z2_gauge_state_sum_vertex_normalization_invariance` | yes | yes | yes | module-level | `#print axioms CampaignFspPachnerInvarianceClaim.z2_gauge_state_sum_vertex_normalization_invariance` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md`

- file: [dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md](../../../dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md)
- sha256 (`lf-normalised`): `42380cb36169d415858344b8ec08c171f8e448ec08334c16c05ae5724eca9421`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1214
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-pachner-invariance-claim.md`

- file: [dag/derivations/independent/fsp-pachner-invariance-claim.md](../../../dag/derivations/independent/fsp-pachner-invariance-claim.md)
- sha256 (`lf-normalised`): `a1e19125518ed3c42912d678e42378c93f6380c99232f93392b52e709f2a7ecb`
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
- sha256 (`lf-normalised`): `dc534f2081828c92447eb58bdccb6cab258c268cbaeef426d1f3aedc81703595`
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
