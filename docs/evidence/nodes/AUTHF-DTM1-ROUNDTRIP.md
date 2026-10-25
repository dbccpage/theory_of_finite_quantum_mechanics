# AUTHF-DTM1-ROUNDTRIP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every DTM0 machine m, decodeMachine (encodeMachine m) = some m, supported by the tag round trips decodeTapeSymbol_encodeTapeSymbol and decodeMove_encodeMove and the rule-list round trip decodeRules_encodeRules.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Only decode after encode is stated; injectivity of decode on arbitrary lists and encode after decode are not stated.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record decodeMachine_encodeMachine claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TokenCode.lean`

- file: [lean4/AuthIncompleteness/TokenCode.lean](../../../lean4/AuthIncompleteness/TokenCode.lean)
- sha256 (`bytes`): `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a`
- cited in: node.lean, node.source, record TFQ-1344
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TokenCode`): recorded sha256 `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TokenCode.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMachine_encodeMachine` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMove_encodeMove` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeMove_encodeMove` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeRules_encodeRules` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeTapeSymbol_encodeTapeSymbol` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.decodeTapeSymbol_encodeTapeSymbol` |

- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_finite_models.py`

- file: [code/python/tests/test_auth_incompleteness_finite_models.py](../../../code/python/tests/test_auth_incompleteness_finite_models.py)
- sha256 (`bytes`): `aaacae53160c7c35d0e874aa162ae7a7cca09a4925914df8dc21da3a2c22cc9a`
- cited in: record TFQ-1344
- check: `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_token_code_round_trip_exhaustive_small_space`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_token_code_round_trip_exhaustive_small_space` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_token_code_round_trip_exhaustive_small_space` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1344_authf_dtm1_roundtrip.md`

- file: [dag/derivations/29_computation/tfq_1344_authf_dtm1_roundtrip.md](../../../dag/derivations/29_computation/tfq_1344_authf_dtm1_roundtrip.md)
- sha256 (`lf-normalised`): `54c64e07cd588c90b01016d3c29c5fcbad5fcd81affd5b176abdee99eebac9d3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1344
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM1-ROUNDTRIP` `DERIVED_LEAN`: [AUTHF-DTM1-TOKEN-GRAMMAR](AUTHF-DTM1-TOKEN-GRAMMAR.md) (DEFINITION)

Outgoing (0):

