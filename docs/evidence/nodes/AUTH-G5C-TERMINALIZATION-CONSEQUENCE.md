# AUTH-G5C-TERMINALIZATION-CONSEQUENCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given an allowed class with no total decider for a validity predicate, no terminalizer whose authorized bit lies in the class is both acceptance-sound and acceptance-complete, and none is acceptance-sound, rejection-sound and never unresolved; a two-valued Boolean fixture is closed, sound and complete.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- NoTotalDecider premise for the declared class
- class membership of the acceptance bit

## Bottleneck

The no-total-decider premise and the class membership of the acceptance bit are hypotheses that no program carrier supplies yet; the result does not say that every terminalizer must return unresolved, and it uses three terminal values where TFQ-0330 names five.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-G5c claims proved, rooted target; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean)
- sha256 (`bytes`): `a0ac0eec152cf48147a6294c3e4c84d933b71c3032e76e19ea51e10735d954d3`
- cited in: node.lean, record TFQ-1335
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `papers.foundations.authorization_incompleteness.evidence.original.formal.terminal_authorization_boundary_models`): recorded sha256 `a0ac0eec152cf48147a6294c3e4c84d933b71c3032e76e19ea51e10735d954d3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/terminal_authorization_boundary_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.acceptance_bit_decides_of_sound_complete` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.closed_two_sided_terminalization_is_acceptance_complete` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.finite_closed_terminalizer_remains_possible` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_closed_two_sided_terminalization` |
| `AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.TerminalAuthorizationBoundary.no_total_decider_blocks_sound_complete_authorization` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1335_auth_g5c_terminalization_consequence.md`

- file: [dag/derivations/29_computation/tfq_1335_auth_g5c_terminalization_consequence.md](../../../dag/derivations/29_computation/tfq_1335_auth_g5c_terminalization_consequence.md)
- sha256 (`lf-normalised`): `96fd2488724e35f0dbd77a5554baaed97b29ef182412d3de3d9bd135d4b063bc`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1335
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_g5c_terminalization_update_packet.md`

- file: [papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_g5c_terminalization_update_packet.md](../../../papers/foundations/authorization_incompleteness/_support/authorization_incompleteness_g5c_terminalization_update_packet.md)
- sha256 (`lf-normalised`): `9ae39a4781904d22596c7b649509fd34ac1ebee4709748180105049753445b2e`
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

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-G5C-TERMINALIZATION-CONSEQUENCE` `DERIVED_LEAN`: [TFQ-0330](TFQ-0330.md) (OPEN), [AUTH-G5A-CLASS-RELATIVE-TRANSPORT](AUTH-G5A-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN), [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

