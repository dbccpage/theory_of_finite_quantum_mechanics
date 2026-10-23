# AUTHF-DTM0-RULE-MACHINE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A DTM0 machine is a designated halt state with a finite, left-biased list of rows (state, scanned symbol, next state, written symbol, move) over the two-symbol alphabet blank and marked; a configuration is a state, an integer head and a total tape Int to symbol; execute runs at most the stated fuel and returns halted, stuck or fuelExhausted.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- two-symbol alphabet fixed
- rule-list order as the operational semantics
- fuel as an externally supplied bound

## Bottleneck

The definition carries no input encoding, no unbounded-run semantics, no halting predicate and no comparison with Mathlib Turing.TM0; fuel exhaustion is a bounded-evaluator result and not non-halting.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-1 claims PROVED_LEAN; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/DirectTM.lean`

- file: [lean4/AuthIncompleteness/DirectTM.lean](../../../lean4/AuthIncompleteness/DirectTM.lean)
- sha256 (`bytes`): `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a`
- cited in: node.lean, node.source, record TFQ-1340
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.DirectTM`): recorded sha256 `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/DirectTM.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.Configuration` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.Configuration` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.Machine` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.Machine` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.Rule` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.Rule` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.StepResult` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.StepResult` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.execute` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.execute` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.isDeclaredHalt` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.isDeclaredHalt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.lookup` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.lookup` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.step` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.step` |
- counts toward the grade: yes

### Python: `code/python/src/qm/auth_incompleteness/finite_models.py`

- file: [code/python/src/qm/auth_incompleteness/finite_models.py](../../../code/python/src/qm/auth_incompleteness/finite_models.py)
- sha256 (`bytes`): `ff6008a75c55f6fa8b55fb5889835109ea58f61355d9b09702e701cdf92ced97`
- cited in: record TFQ-1340

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `apply_rule` (python_symbol) | yes | yes | yes | - | - |
| `execute` (python_symbol) | yes | yes | yes | - | - |
| `lookup` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1340_authf_dtm0_rule_machine.md`

- file: [dag/derivations/29_computation/tfq_1340_authf_dtm0_rule_machine.md](../../../dag/derivations/29_computation/tfq_1340_authf_dtm0_rule_machine.md)
- sha256 (`lf-normalised`): `f5632fc9c0f7f77c8a95054b16c4ff6a23627efc4758122ae44e6c537934547c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1340
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM0-RULE-MACHINE` `DERIVED_PROSE`: [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN), [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (7):

- `APP-R-AUTHF-DTM0-FIXTURES` `COMPUTED`: [AUTHF-DTM0-FIXTURES](AUTHF-DTM0-FIXTURES.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-AUTHF-DTM0-HALT-IFF-STATE` `DERIVED_LEAN`: [AUTHF-DTM0-HALT-IFF-STATE](AUTHF-DTM0-HALT-IFF-STATE.md) (PROVED_LEAN)
- `APP-R-AUTHF-DTM0-SIMULATION-OPEN` `GAP_NO_DERIVATION`: [AUTHF-DTM0-SIMULATION-OPEN](AUTHF-DTM0-SIMULATION-OPEN.md) (OPEN)
- `APP-R-AUTHF-DTM1-TOKEN-GRAMMAR` `DERIVED_PROSE`: [AUTHF-DTM1-TOKEN-GRAMMAR](AUTHF-DTM1-TOKEN-GRAMMAR.md) (DEFINITION)
- `APP-R-AUTHF-HALT-NOT-POLICY` `DERIVED_LEAN`: [AUTHF-HALT-NOT-POLICY](AUTHF-HALT-NOT-POLICY.md) (PROVED_LEAN)
- `APP-R-AUTHF-TAPE-CONTROL-REPORTS` `DERIVED_LEAN`: [AUTHF-TAPE-CONTROL-REPORTS](AUTHF-TAPE-CONTROL-REPORTS.md) (PROVED_LEAN)
- `APP-R-AUTHF-TRANSITION-INVARIANTS` `DERIVED_LEAN`: [AUTHF-TRANSITION-INVARIANTS](AUTHF-TRANSITION-INVARIANTS.md) (PROVED_LEAN)
