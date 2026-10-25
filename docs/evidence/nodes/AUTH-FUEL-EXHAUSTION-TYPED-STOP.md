# AUTH-FUEL-EXHAUSTION-TYPED-STOP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A bounded evaluator has three terminal outcomes, halted, stuck and fuel exhausted; the fuel-exhausted outcome records only that the budget ended and is never read as divergence, and a looping fixture exhausts a budget of one step without any claim about whether it halts.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Apply the same three-way typing to the declared-bound runs of the Genesis continuation: a run stopped at the guard or the bound stays unresolved, neither closed nor diverging, until a longer run or a proof decides it.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AUTH-PAPER-1 claims stated in prose and by a closed fixture (no separate claim id); audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean)
- sha256 (`bytes`): `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9`
- cited in: node.lean, record TFQ-1331
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `papers.foundations.authorization_incompleteness.evidence.original.formal.direct_turing_machine_models`): recorded sha256 `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1331_auth_fuel_exhaustion_typed_stop.md`

- file: [dag/derivations/29_computation/tfq_1331_auth_fuel_exhaustion_typed_stop.md](../../../dag/derivations/29_computation/tfq_1331_auth_fuel_exhaustion_typed_stop.md)
- sha256 (`lf-normalised`): `71d48336c845d4913920263dbf49ca41b55093e9e5196b689193510d86f0c69f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1331
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_theory_red_team_dialogue_raw.md`

- file: [papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_theory_red_team_dialogue_raw.md](../../../papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_theory_red_team_dialogue_raw.md)
- sha256 (`lf-normalised`): `d82040ae365722831a28a1b09e8571c6bccdfc925edf8faeb7343d8a7fb3ae04`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md)
- sha256 (`lf-normalised`): `4ca81b6ae8e724b54c7abf43ea951c119c2cff31a375e45cd7d79299adc7f70c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-FUEL-EXHAUSTION-TYPED-STOP` `DERIVED_PROSE`: [PGW-RUNS-PAST-DECLARED-BOUNDS](PGW-RUNS-PAST-DECLARED-BOUNDS.md) (OPEN), [AUTH-DTM0-FINITE-RULE-MACHINE](AUTH-DTM0-FINITE-RULE-MACHINE.md) (DEFINITION)

Outgoing (0):

