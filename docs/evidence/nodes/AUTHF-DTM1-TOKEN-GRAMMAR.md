# AUTHF-DTM1-TOKEN-GRAMMAR

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A machine code is the halt-state token followed by complete five-token frames (state, scanned tag, next state, written tag, move tag) with tags 0 and 1 for symbols and 0, 1, 2 for moves; decodeMachine consumes the whole list and returns none on an empty list, a truncated frame or an invalid tag.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Tokens are natural numbers, not bytes; there is no configuration or input encoding and no parser-to-execution agreement.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-4 claims PROVED_LEAN; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TokenCode.lean`

- file: [lean4/AuthIncompleteness/TokenCode.lean](../../../lean4/AuthIncompleteness/TokenCode.lean)
- sha256 (`bytes`): `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a`
- cited in: node.lean, node.source, record TFQ-1343
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TokenCode`): recorded sha256 `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TokenCode.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeMachine` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeMachine` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeRule` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeRule` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeRules` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.encodeRules` |
- counts toward the grade: yes

### Python: `code/python/src/qm/auth_incompleteness/finite_models.py`

- file: [code/python/src/qm/auth_incompleteness/finite_models.py](../../../code/python/src/qm/auth_incompleteness/finite_models.py)
- sha256 (`bytes`): `ff6008a75c55f6fa8b55fb5889835109ea58f61355d9b09702e701cdf92ced97`
- cited in: record TFQ-1343

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decode_machine` (python_symbol) | yes | yes | yes | - | - |
| `encode_machine` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1343_authf_dtm1_token_grammar.md`

- file: [dag/derivations/29_computation/tfq_1343_authf_dtm1_token_grammar.md](../../../dag/derivations/29_computation/tfq_1343_authf_dtm1_token_grammar.md)
- sha256 (`lf-normalised`): `66b71d48c4e3987d6633baff6553cb9d8e4ec5866269dd908e216a570fa690a6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1343
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM1-TOKEN-GRAMMAR` `DERIVED_PROSE`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION), [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (2):

- `APP-R-AUTHF-DTM1-MALFORMED-CODES` `COMPUTED`: [AUTHF-DTM1-MALFORMED-CODES](AUTHF-DTM1-MALFORMED-CODES.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-AUTHF-DTM1-ROUNDTRIP` `DERIVED_LEAN`: [AUTHF-DTM1-ROUNDTRIP](AUTHF-DTM1-ROUNDTRIP.md) (PROVED_LEAN)
