# AUTHF-TRANSITION-INVARIANTS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The four-configuration transition table maps every configuration to one that cleanTerminalContract accepts, so it preserves that contract, and it does not preserve markedCellContract because runningMarked is accepted while its successor runningBlank is not.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
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

Two supplied Boolean contracts on one finite table; nothing is said about transition systems in general.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record transition_preserves_clean_terminal_contract claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TapeTransition.lean`

- file: [lean4/AuthIncompleteness/TapeTransition.lean](../../../lean4/AuthIncompleteness/TapeTransition.lean)
- sha256 (`bytes`): `107069b58a46297b84b5eb2bd7366a5bdc16ce6a4564a444b80f1b69feb87ebd`
- cited in: node.lean, node.source, record TFQ-1354
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TapeTransition`): recorded sha256 `107069b58a46297b84b5eb2bd7366a5bdc16ce6a4564a444b80f1b69feb87ebd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TapeTransition.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_output_satisfies_clean_terminal_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_output_satisfies_clean_terminal_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract` |
- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_finite_models.py`

- file: [code/python/tests/test_auth_incompleteness_finite_models.py](../../../code/python/tests/test_auth_incompleteness_finite_models.py)
- sha256 (`bytes`): `aaacae53160c7c35d0e874aa162ae7a7cca09a4925914df8dc21da3a2c22cc9a`
- cited in: record TFQ-1354
- check: `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_contracts_and_adequacy_match_lean_theorems`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_contracts_and_adequacy_match_lean_theorems` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_contracts_and_adequacy_match_lean_theorems` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1354_authf_transition_invariants.md`

- file: [dag/derivations/29_computation/tfq_1354_authf_transition_invariants.md](../../../dag/derivations/29_computation/tfq_1354_authf_transition_invariants.md)
- sha256 (`lf-normalised`): `a863685e4fa53aa6e8417395343092685bc7567352e132c6f3f9808d022c0a10`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1354
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-TRANSITION-INVARIANTS` `DERIVED_LEAN`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)

Outgoing (1):

- `APP-R-AUTHF-TRANSITION-ADEQUACY` `DERIVED_LEAN`: [AUTHF-TRANSITION-ADEQUACY](AUTHF-TRANSITION-ADEQUACY.md) (PROVED_LEAN)
