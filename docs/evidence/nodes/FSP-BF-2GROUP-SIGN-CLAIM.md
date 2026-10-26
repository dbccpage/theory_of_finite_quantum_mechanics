# FSP-BF-2GROUP-SIGN-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- distinct cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The result concerns the explicitly defined Z2 cochain model and normalized rephasings. It constructs no BF state sum, 2-group gauge dynamics, knotted-worldsheet amplitude or three-loop braiding observable. No general cancellation or sign-free theorem follows. Original target retained as an obligation: Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout. Prior boundary: Define the finite BF or 2-group gauge model, compute the 3-loop braiding phases and state exactly which weights become nonnegative; ledger GIN-C19 to GIN-C21 withdraw the fixture readings.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-046 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignBfCocycleObstruction.lean`

- file: [lean4/CampaignBfCocycleObstruction.lean](../../../lean4/CampaignBfCocycleObstruction.lean)
- sha256 (`bytes`): `882c2767c327fb2be146c2069898bea71eac43e6c1adf5b61c044475feb4eddc`
- cited in: node.lean, receipt dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json (CampaignBfCocycleObstruction), record TFQ-1210
- replay: `verified`
  - receipt [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json) (module `CampaignBfCocycleObstruction`): recorded sha256 `882c2767c327fb2be146c2069898bea71eac43e6c1adf5b61c044475feb4eddc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignBfCocycleObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignBfCocycleObstruction.Normalized` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.Normalized` |
| `CampaignBfCocycleObstruction.coboundary` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.coboundary` |
| `CampaignBfCocycleObstruction.cocycle` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.cocycle` |
| `CampaignBfCocycleObstruction.cocycle_identity` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.cocycle_identity` |
| `CampaignBfCocycleObstruction.generator_sign_survives_rephasing` | yes | yes | yes | propext | `#print axioms CampaignBfCocycleObstruction.generator_sign_survives_rephasing` |
| `CampaignBfCocycleObstruction.no_normalized_rephasing_makes_all_signs_positive` | yes | yes | yes | propext | `#print axioms CampaignBfCocycleObstruction.no_normalized_rephasing_makes_all_signs_positive` |
| `CampaignBfCocycleObstruction.normalized_coboundary_at_generator` | yes | yes | yes | propext | `#print axioms CampaignBfCocycleObstruction.normalized_coboundary_at_generator` |
| `CampaignBfCocycleObstruction.normalized_cocycle` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.normalized_cocycle` |
| `CampaignBfCocycleObstruction.not_a_normalized_coboundary` | yes | yes | yes | propext | `#print axioms CampaignBfCocycleObstruction.not_a_normalized_coboundary` |
| `CampaignBfCocycleObstruction.rephase` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.rephase` |
| `CampaignBfCocycleObstruction.sign` | yes | yes | yes | none | `#print axioms CampaignBfCocycleObstruction.sign` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-bf-2group-sign-claim.py`

- file: [checks/independent/fsp-bf-2group-sign-claim.py](../../../checks/independent/fsp-bf-2group-sign-claim.py)
- sha256 (`bytes`): `9b1b7c5b3a3ba2735ff1e5bfa6bcd9e918f84c2281b0fa8d1c214e1fc1cf84dc`
- cited in: record TFQ-1210
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md`

- file: [dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md](../../../dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md)
- sha256 (`lf-normalised`): `0c807dcd6c58902afd7202e7d1105255616a76fe8a5fb2bf13599338fd4a9b66`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1210
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-bf-2group-sign-claim.md`

- file: [dag/derivations/independent/fsp-bf-2group-sign-claim.md](../../../dag/derivations/independent/fsp-bf-2group-sign-claim.md)
- sha256 (`lf-normalised`): `83f3aa9c7567ceab60d50adec7af32f9fdbb0dc6b69afebb759bbfe4ea0827fe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json)
- sha256 (`lf-normalised`): `32863477287110540a374428dee4ee40cd271e0bfb3d087180df26adc18931c1`
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
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-BF-2GROUP-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-COBORDISM-INTRINSIC-SIGN` `GAP_NO_DERIVATION`: [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)
- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)
