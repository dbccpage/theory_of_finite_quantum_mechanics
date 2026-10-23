# AUTHF-DTM0-FIXTURES

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the three named fixtures, writeAndHaltMachine writes a mark and reaches its halt state in one transition, the empty-rule machine is stuck at its first step, and the one-row self-loop machine returns fuelExhausted with the looped configuration after one unit of fuel.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The self-loop result is exhaustion of one unit of fuel; no theorem says the loop never halts, and no fixture exceeds three rows.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-3 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/DirectTM.lean`

- file: [lean4/AuthIncompleteness/DirectTM.lean](../../../lean4/AuthIncompleteness/DirectTM.lean)
- sha256 (`bytes`): `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a`
- cited in: node.lean, node.source, record TFQ-1342
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.DirectTM`): recorded sha256 `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/DirectTM.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_executes_to_syntactic_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_executes_to_syntactic_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_reaches_declared_halt` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_reaches_declared_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_writes_mark` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_transition_writes_mark` |
- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_finite_models.py`

- file: [code/python/tests/test_auth_incompleteness_finite_models.py](../../../code/python/tests/test_auth_incompleteness_finite_models.py)
- sha256 (`bytes`): `aaacae53160c7c35d0e874aa162ae7a7cca09a4925914df8dc21da3a2c22cc9a`
- cited in: record TFQ-1342

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_stuck_and_looping_fixtures_are_distinct_outcomes` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_stuck_and_looping_fixtures_are_distinct_outcomes` |
| `test_write_and_halt_fixture` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_finite_models.py::test_write_and_halt_fixture` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1342_authf_dtm0_fixtures.md`

- file: [dag/derivations/29_computation/tfq_1342_authf_dtm0_fixtures.md](../../../dag/derivations/29_computation/tfq_1342_authf_dtm0_fixtures.md)
- sha256 (`lf-normalised`): `7910849197fef2104083d598b9d2dc6f03d9b671f09ead32d21117908e659ddf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1342
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM0-FIXTURES` `COMPUTED`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION), [PGW-RUNS-PAST-DECLARED-BOUNDS](PGW-RUNS-PAST-DECLARED-BOUNDS.md) (OPEN)

Outgoing (0):

