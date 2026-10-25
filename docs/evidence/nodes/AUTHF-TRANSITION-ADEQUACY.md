# AUTHF-TRANSITION-ADEQUACY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the four configurations the identity report is adequate for markedCellContract, whereas the control-outcome report is not, because haltedBlank and haltedMarked both report stay and the contract separates them, so no function of the control outcome decides the contract.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A finite adequacy example; whether any report is adequate for a semantic property of arbitrary programs is not addressed.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record full_configuration_report_adequate_for_marked_cell_contract claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/TapeTransition.lean`

- file: [lean4/AuthIncompleteness/TapeTransition.lean](../../../lean4/AuthIncompleteness/TapeTransition.lean)
- sha256 (`bytes`): `107069b58a46297b84b5eb2bd7366a5bdc16ce6a4564a444b80f1b69feb87ebd`
- cited in: node.lean, node.source, record TFQ-1355
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TapeTransition`): recorded sha256 `107069b58a46297b84b5eb2bd7366a5bdc16ce6a4564a444b80f1b69feb87ebd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TapeTransition.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.control_report_not_adequate_for_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_adequate_for_marked_cell_contract` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_admits_marked_cell_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.full_configuration_report_admits_marked_cell_decider` |
| `AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeTransitionInvariantModels.shared_stay_control_blocks_control_only_contract_decider` |

- counts toward the grade: yes

### Python: `code/python/src/qm/auth_incompleteness/replay_packet.py`

- file: [code/python/src/qm/auth_incompleteness/replay_packet.py](../../../code/python/src/qm/auth_incompleteness/replay_packet.py)
- sha256 (`bytes`): `3d2bb1abdeeff00a6c3c7c5deb7e26f4fcacf8a7594916273587c759fcbb3196`
- cited in: record TFQ-1355

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `transition_evaluation` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1355_authf_transition_adequacy.md`

- file: [dag/derivations/29_computation/tfq_1355_authf_transition_adequacy.md](../../../dag/derivations/29_computation/tfq_1355_authf_transition_adequacy.md)
- sha256 (`lf-normalised`): `fe769f13f590b8508c5a365fe727c30ebe56b52d5ed9674290bc1cd035e10bdf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1355
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-TRANSITION-ADEQUACY` `DERIVED_LEAN`: [AUTHF-TRANSITION-INVARIANTS](AUTHF-TRANSITION-INVARIANTS.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-AUTHF-REPLAY-PACKET-PYTHON` `COMPUTED`: [AUTHF-REPLAY-PACKET-PYTHON](AUTHF-REPLAY-PACKET-PYTHON.md) (COMPUTATIONALLY_CHECKED)
