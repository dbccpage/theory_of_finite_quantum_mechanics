# AUTHF-DTM0-HALT-IFF-STATE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every DTM0 machine and configuration, step returns halted exactly when the configuration's state equals the machine's halt state, and execute then returns halted at every fuel budget.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This fixes what a declared halt means in DTM0; it is not a statement about halting of runs and selects no terminal policy.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record step_halted_iff_declared_halt claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/DirectTM.lean`

- file: [lean4/AuthIncompleteness/DirectTM.lean](../../../lean4/AuthIncompleteness/DirectTM.lean)
- sha256 (`bytes`): `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a`
- cited in: node.lean, node.source, record TFQ-1341
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.DirectTM`): recorded sha256 `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/DirectTM.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt` |

- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_finite_models.py`

- file: [code/python/tests/test_auth_incompleteness_finite_models.py](../../../code/python/tests/test_auth_incompleteness_finite_models.py)
- sha256 (`bytes`): `aaacae53160c7c35d0e874aa162ae7a7cca09a4925914df8dc21da3a2c22cc9a`
- cited in: record TFQ-1341
- check: `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_declared_halt_is_reported_at_any_fuel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_declared_halt_is_reported_at_any_fuel` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_declared_halt_is_reported_at_any_fuel` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1341_authf_dtm0_halt_iff_state.md`

- file: [dag/derivations/29_computation/tfq_1341_authf_dtm0_halt_iff_state.md](../../../dag/derivations/29_computation/tfq_1341_authf_dtm0_halt_iff_state.md)
- sha256 (`lf-normalised`): `926b7e3985854cd18435a91cd005a2fa44e0911c8da2d15a28591c8173b9a632`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1341
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM0-HALT-IFF-STATE` `DERIVED_LEAN`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)

Outgoing (0):

