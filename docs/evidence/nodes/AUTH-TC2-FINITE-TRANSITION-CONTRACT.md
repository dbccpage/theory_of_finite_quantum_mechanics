# AUTH-TC2-FINITE-TRANSITION-CONTRACT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In a table over the four configurations running-blank, running-marked, halted-blank and halted-marked that exposes advance, stay and halt, the supplied clean-terminal contract is preserved, the supplied marked-cell contract fails from running-marked, the identity report is adequate for the marked-cell contract, and the control-only report is not.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- supplied clean-terminal contract
- supplied marked-cell contract

## Bottleneck

Replace the enumerated carrier by an actual tape and head, and replace the contracts, which were written to produce the countertrace, by contracts stated independently of the table.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-TC2 claims proved, rooted target (Lean finite model, axiom-free); audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/tape_transition_invariant_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/tape_transition_invariant_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/tape_transition_invariant_models.lean)
- sha256 (`bytes`): `5d6467c5b88a3955bd78f55a6629fe5c204a004bfe4e68c11b24e11544e1fab0`
- cited in: node.lean, record TFQ-1329
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `tape_transition_invariant_models`): recorded sha256 `5d6467c5b88a3955bd78f55a6629fe5c204a004bfe4e68c11b24e11544e1fab0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/tape_transition_invariant_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.marked_contract_countertrace` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_does_not_preserve_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.transition_preserves_clean_terminal_contract` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1329_auth_tc2_finite_transition_contract.md`

- file: [dag/derivations/29_computation/tfq_1329_auth_tc2_finite_transition_contract.md](../../../dag/derivations/29_computation/tfq_1329_auth_tc2_finite_transition_contract.md)
- sha256 (`lf-normalised`): `aca32faadec07fc27757648df8b973cd01313df3892d342b4855ab9ba7ffd0d8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1329
- counts toward the grade: no

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

- `APP-R-AUTH-TC2-FINITE-TRANSITION-CONTRACT` `COMPUTED`: [AUTH-TC0-TAPE-CONTROL-TYPING](AUTH-TC0-TAPE-CONTROL-TYPING.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `APP-R-AUTH-DTM0-FINITE-RULE-MACHINE` `DERIVED_PROSE`: [AUTH-DTM0-FINITE-RULE-MACHINE](AUTH-DTM0-FINITE-RULE-MACHINE.md) (DEFINITION)
