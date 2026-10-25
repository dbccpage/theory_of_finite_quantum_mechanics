# AUTH-TC0-TAPE-CONTROL-TYPING

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the fixed carrier of two halting presentations that differ only in the scanned cell (blank or marked), a control-only report does not determine the supplied content contract, an unread report does not determine it either, one read token admits two supplied semantic adapters, and one halt outcome admits two supplied terminal policies.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- supplied content contract
- supplied semantic adapters
- supplied terminal policies

## Bottleneck

State the same four facts for a general tape alphabet and head position; the content contract is chosen to separate the two presentations, so the result exhibits a split fiber and does not derive one.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-TC0 claims proved (Lean finite model, all axiom-free); audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/foundations/authorization_incompleteness/evidence/original/formal/tape_control_authorization_models.lean`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal/tape_control_authorization_models.lean](../../../papers/foundations/authorization_incompleteness/evidence/original/formal/tape_control_authorization_models.lean)
- sha256 (`bytes`): `c6d4e136cd5e0c8f696383518cee4657bd58e3354b07960f5525216b28af87df`
- cited in: node.lean, record TFQ-1328
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `papers.foundations.authorization_incompleteness.evidence.original.formal.tape_control_authorization_models`): recorded sha256 `c6d4e136cd5e0c8f696383518cee4657bd58e3354b07960f5525216b28af87df` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/foundations/authorization_incompleteness/evidence/original/formal/tape_control_authorization_models.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeControlModels.same_halt_control_blocks_control_only_decider` |
| `AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeControlModels.same_read_token_allows_distinct_semantic_adapters` |
| `AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy` |
| `AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeControlModels.unread_report_blocks_content_decider` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1328_auth_tc0_tape_control_typing.md`

- file: [dag/derivations/29_computation/tfq_1328_auth_tc0_tape_control_typing.md](../../../dag/derivations/29_computation/tfq_1328_auth_tc0_tape_control_typing.md)
- sha256 (`lf-normalised`): `ef820c2be5590d9bd08ef2d16f0a9e584ed7051144bcf6e57e4f2b79dff2e108`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1328
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

- `APP-R-AUTH-TC0-TAPE-CONTROL-TYPING` `COMPUTED`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION), [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL), [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-AUTH-TC2-FINITE-TRANSITION-CONTRACT` `COMPUTED`: [AUTH-TC2-FINITE-TRANSITION-CONTRACT](AUTH-TC2-FINITE-TRANSITION-CONTRACT.md) (COMPUTATIONALLY_CHECKED)
