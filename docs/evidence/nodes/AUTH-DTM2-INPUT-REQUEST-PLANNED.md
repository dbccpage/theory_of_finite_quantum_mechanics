# AUTH-DTM2-INPUT-REQUEST-PLANNED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The update packet plans a request code made of a fuel token, a machine-code length, one machine segment and an input word, whose code-level evaluator decodes the request and calls the bounded evaluator on the declared initial input, with seven named target theorems.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Write the module and prove the request round trip and the result-level agreement; configuration snapshots and step-by-step trace agreement remain separate obligations.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-DTM2 claims planned in a producer-side update packet; absent from ledger, proof program, goals and Lean; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md`

- file: [dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md](../../../dag/derivations/29_computation/tfq_1333_auth_dtm2_input_request_planned.md)
- sha256 (`lf-normalised`): `8f0d253d4630ee216dff1d24abc9d5b118740c81b6cbd8ece037e029d4b68f4f`
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

