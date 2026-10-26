# AUTH-DTM1-TOKEN-CODE-ROUNDTRIP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every finite-rule machine, decoding the token list that encodes it (the halt-state token followed by five-token frames of state, scanned tag, next state, written tag and move tag) returns that machine, and the all-consuming decoder returns none on the empty list, a truncated frame, an invalid symbol tag and an invalid move tag in the four named fixtures.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No converse (encoding after decoding), no source-byte format, no configuration or input encoding and no agreement between parsed code and execution is established; the token alphabet is the natural numbers, so passing to the two-symbol tape alphabet needs a prefix-code argument, since free monoids on alphabets of different sizes are not isomorphic.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-DTM1 claims proved; partial carrier only; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean)
- sha256 (`bytes`): `6d3aecf402c15951b53eccf49e1609180346bac425496f3cd85264e6ba527153`
- cited in: node.lean, record TFQ-1332
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `papers.foundations.authorization_incompleteness.evidence.original.formal.direct_turing_machine_token_code_models`): recorded sha256 `6d3aecf402c15951b53eccf49e1609180346bac425496f3cd85264e6ba527153` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_token_code_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1332_auth_dtm1_token_code_roundtrip.md`

- file: [dag/derivations/29_computation/tfq_1332_auth_dtm1_token_code_roundtrip.md](../../../dag/derivations/29_computation/tfq_1332_auth_dtm1_token_code_roundtrip.md)
- sha256 (`lf-normalised`): `c0b28167100a86a1fa47ee00c013f386f68440970547bc04c9d524c55c737268`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1332
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm1_token_code_update_packet.md`

- file: [papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm1_token_code_update_packet.md](../../../papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_dtm1_token_code_update_packet.md)
- sha256 (`lf-normalised`): `796b99650531f96d129b3db8a96e4984aabd03d9d9386e7ad5b86461d06ca7df`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md)
- sha256 (`lf-normalised`): `71cd507642cce8ef451189097acd333162642eeb85345ffa304bff305a620697`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md`

- file: [papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md](../../../papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md)
- sha256 (`lf-normalised`): `2573123162731ea63495b0ece777ae4b9e704e27b976fbc031df51c6f81c6f7b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-DTM1-TOKEN-CODE-ROUNDTRIP` `DERIVED_LEAN`: [AUTH-DTM0-FINITE-RULE-MACHINE](AUTH-DTM0-FINITE-RULE-MACHINE.md) (DEFINITION), [PG-FREE-MONOID-NONISO](PG-FREE-MONOID-NONISO.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-AUTH-DTM2-INPUT-REQUEST-PLANNED` `GAP_NO_DERIVATION`: [AUTH-DTM2-INPUT-REQUEST-PLANNED](AUTH-DTM2-INPUT-REQUEST-PLANNED.md) (OPEN)
- `APP-R-AUTH-G5B-CARRIER-ADMISSION-GATE` `DERIVED_PROSE`: [AUTH-G5B-CARRIER-ADMISSION-GATE](AUTH-G5B-CARRIER-ADMISSION-GATE.md) (DEFINITION)
