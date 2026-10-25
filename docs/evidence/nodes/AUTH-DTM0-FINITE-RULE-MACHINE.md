# AUTH-DTM0-FINITE-RULE-MACHINE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A machine is a designated halt state with an ordered finite rule list over natural-number states, the symbols blank and marked, and the moves left, right and stay; a step returns halted exactly when the state is the halt state, stuck when no rule matches, and otherwise applies the first matching rule; execute iterates at most the given fuel and returns halted, stuck or fuel exhausted with the last configuration.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declaration references covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- tape as a function from the integers to symbols, which includes tapes of infinite support
- natural-number state labels without a finiteness bound
- first-match lookup as the determinism convention

## Bottleneck

Relate the model to Mathlib Turing.TM0 by restricting initial tapes to finite support, splitting write-and-move rules into two steps and merging halted with stuck, then prove step simulation; no universality, extensional property or reduction is established here.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-DTM0 claims proved; partial carrier only; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean)
- sha256 (`bytes`): `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9`
- cited in: node.lean, record TFQ-1330
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `papers.foundations.authorization_incompleteness.evidence.original.formal.direct_turing_machine_models`): recorded sha256 `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/direct_turing_machine_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.empty_rule_fixture_is_stuck` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.execute` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.execute` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.execute_halted_of_declared_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.looping_fixture_exhausts_bounded_fuel` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.step` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.step` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.step_halted_iff_declared_halt` |
| `AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_executes_to_syntactic_halt` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.write_and_halt_executes_to_syntactic_halt` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1330_auth_dtm0_finite_rule_machine.md`

- file: [dag/derivations/29_computation/tfq_1330_auth_dtm0_finite_rule_machine.md](../../../dag/derivations/29_computation/tfq_1330_auth_dtm0_finite_rule_machine.md)
- sha256 (`lf-normalised`): `aea8f8ecc8f2f8f8d5480b77c12b5e05040ac39586039ecce9a5db0dc020c42f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1330
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

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-DTM0-FINITE-RULE-MACHINE` `DERIVED_PROSE`: [AUTH-TC2-FINITE-TRANSITION-CONTRACT](AUTH-TC2-FINITE-TRANSITION-CONTRACT.md) (COMPUTATIONALLY_CHECKED), [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-AUTH-DTM1-TOKEN-CODE-ROUNDTRIP` `DERIVED_LEAN`: [AUTH-DTM1-TOKEN-CODE-ROUNDTRIP](AUTH-DTM1-TOKEN-CODE-ROUNDTRIP.md) (PROVED_LEAN)
- `APP-R-AUTH-FUEL-EXHAUSTION-TYPED-STOP` `DERIVED_PROSE`: [AUTH-FUEL-EXHAUSTION-TYPED-STOP](AUTH-FUEL-EXHAUSTION-TYPED-STOP.md) (DEFINITION)
