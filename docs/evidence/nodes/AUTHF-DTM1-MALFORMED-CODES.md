# AUTHF-DTM1-MALFORMED-CODES

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> decodeMachine returns none on the four named lists \[\], \[0,0,0,1\], \[0,0,2,1,0,0\] and \[0,0,0,1,0,3\].

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Four named inputs only; no theorem characterizes the full domain of decodeMachine.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record invalid_symbol_tag_is_rejected claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TokenCode.lean`

- file: [lean4/AuthIncompleteness/TokenCode.lean](../../../lean4/AuthIncompleteness/TokenCode.lean)
- sha256 (`bytes`): `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a`
- cited in: node.lean, node.source, record TFQ-1345
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TokenCode`): recorded sha256 `462875c362c83b192c5e491df86655258c973a13ea740d4e1cee06360f88240a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TokenCode.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.empty_machine_code_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_move_tag_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.invalid_symbol_tag_is_rejected` |
| `AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineTokenCodeModels.truncated_rule_code_is_rejected` |
- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_finite_models.py`

- file: [code/python/tests/test_auth_incompleteness_finite_models.py](../../../code/python/tests/test_auth_incompleteness_finite_models.py)
- sha256 (`bytes`): `aaacae53160c7c35d0e874aa162ae7a7cca09a4925914df8dc21da3a2c22cc9a`
- cited in: record TFQ-1345
- check: `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_malformed_codes_are_rejected`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_malformed_codes_are_rejected` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_malformed_codes_are_rejected` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1345_authf_dtm1_malformed_codes.md`

- file: [dag/derivations/29_computation/tfq_1345_authf_dtm1_malformed_codes.md](../../../dag/derivations/29_computation/tfq_1345_authf_dtm1_malformed_codes.md)
- sha256 (`lf-normalised`): `58a523083e9e5d521ae963e64e00e2fe3eb289e484446cfbe7eec65ed16c97e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1345
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM1-MALFORMED-CODES` `COMPUTED`: [AUTHF-DTM1-TOKEN-GRAMMAR](AUTHF-DTM1-TOKEN-GRAMMAR.md) (DEFINITION)

Outgoing (0):

