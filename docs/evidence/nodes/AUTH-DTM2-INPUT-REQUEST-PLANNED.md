# AUTH-DTM2-INPUT-REQUEST-PLANNED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On one closed request the header tag is 1, the fuel token is 2, the machine-code length is 1, the machine segment is the list 7, and the input word is the list 3, 4. Concatenating the header, the fuel, the length, the segment and the input word yields the list 1, 2, 1, 7, 3, 4. The list 0, 2, 1, 7, 3, 4 begins with 0, and 0 differs from the header tag.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An encoder and decoder for a request other than this closed list, the remaining named targets in the update packet, and result-level agreement with a bounded evaluator stay open. Configuration snapshots and step-by-step trace agreement stay open. No custody reading and no authorization reading are in this record.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-DTM2 claims planned in a producer-side update packet; absent from ledger, proof program, goals and Lean; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignAuthDtm2InputRequestPlanned.lean`

- file: [lean4/CampaignAuthDtm2InputRequestPlanned.lean](../../../lean4/CampaignAuthDtm2InputRequestPlanned.lean)
- sha256 (`bytes`): `070d8ae283532b1ad74a769395accb6f197e758859a540cf45a27aacefe852cd`
- cited in: node.lean, receipt dag/research/campaign_auth-dtm2-input-request-planned_lean_replay.json (CampaignAuthDtm2InputRequestPlanned), receipt dag/research/pr_371_review_replay.json (CampaignAuthDtm2InputRequestPlanned), record TFQ-1333
- replay: `verified`
  - receipt [dag/research/campaign_auth-dtm2-input-request-planned_lean_replay.json](../../../dag/research/campaign_auth-dtm2-input-request-planned_lean_replay.json) (module `CampaignAuthDtm2InputRequestPlanned`): recorded sha256 `070d8ae283532b1ad74a769395accb6f197e758859a540cf45a27aacefe852cd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_371_review_replay.json](../../../dag/research/pr_371_review_replay.json) (module `CampaignAuthDtm2InputRequestPlanned`): recorded sha256 `070d8ae283532b1ad74a769395accb6f197e758859a540cf45a27aacefe852cd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignAuthDtm2InputRequestPlanned`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignAuthDtm2InputRequestPlanned.oneRequestEncoding` | yes | yes | yes | none | `#print axioms CampaignAuthDtm2InputRequestPlanned.oneRequestEncoding` |
| `CampaignAuthDtm2InputRequestPlanned.zeroHeadDiffersFromHeader` | yes | yes | yes | none | `#print axioms CampaignAuthDtm2InputRequestPlanned.zeroHeadDiffersFromHeader` |
| `oneRequestEncoding` | yes | yes | yes | none | `#print axioms oneRequestEncoding` |
| `zeroHeadDiffersFromHeader` | yes | yes | yes | none | `#print axioms zeroHeadDiffersFromHeader` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md`

- file: [dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md](../../../dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md)
- sha256 (`lf-normalised`): `3cb9b84df8a6d64d49eda6344d7a29b7c93f18f661f385bf9dd22077baf16266`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1333
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md`

- file: [papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md](../../../papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md)
- sha256 (`lf-normalised`): `da69034cb8815cbc03629a322755b1ff7f35825f586ff3fefedc663082db0236`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_update_packet.md`

- file: [papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_update_packet.md](../../../papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm2_input_execution_update_packet.md)
- sha256 (`lf-normalised`): `4d392e64655a31fae0ff0602d9a7768b3ef21b02a869f12bd772f8cabd41c4cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-DTM2-INPUT-REQUEST-PLANNED` `GAP_NO_DERIVATION`: [AUTH-DTM1-TOKEN-CODE-ROUNDTRIP](AUTH-DTM1-TOKEN-CODE-ROUNDTRIP.md) (PROVED_LEAN)

Outgoing (0):

