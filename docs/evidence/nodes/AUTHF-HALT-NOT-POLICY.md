# AUTHF-HALT-NOT-POLICY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the DTM0 model, the tape-control model and the replay model, a halted or verified outcome receives different terminal values from two supplied policies: acceptHalted versus leaveAllOpen, acceptHalt versus rejectAll, and authorizeOnVerified versus leaveVerifiedOpen.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Existence of two policies only; no policy is selected or justified.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record syntactic_halt_does_not_select_terminal_policy claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/DirectTM.lean`

- file: [lean4/AuthIncompleteness/DirectTM.lean](../../../lean4/AuthIncompleteness/DirectTM.lean)
- sha256 (`bytes`): `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a`
- cited in: node.lean, node.source, record TFQ-1353
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.DirectTM`): recorded sha256 `7a64ee188f1fbfc2b593571eee43b0996021cd68eb694a4e48b3cb384e20310a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/DirectTM.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.DirectTuringMachineModels.syntactic_halt_does_not_select_direct_machine_policy` | yes | yes | yes | propext | `#print axioms AuthorizationIncompleteness.DirectTuringMachineModels.syntactic_halt_does_not_select_direct_machine_policy` |

- counts toward the grade: yes

### Lean: `lean4/AuthIncompleteness/Replay.lean`

- file: [lean4/AuthIncompleteness/Replay.lean](../../../lean4/AuthIncompleteness/Replay.lean)
- sha256 (`bytes`): `5d1411fd9a1b692f18bbe037dc42532911d7468415ea5ae0bcd91d64f7463362`
- cited in: node.lean, node.source, record TFQ-1353
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.Replay`): recorded sha256 `5d1411fd9a1b692f18bbe037dc42532911d7468415ea5ae0bcd91d64f7463362` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Replay.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.ReplayPacketBindingModels.terminal_policy_is_not_selected_by_verification` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.ReplayPacketBindingModels.terminal_policy_is_not_selected_by_verification` |

- counts toward the grade: yes

### Lean: `lean4/AuthIncompleteness/TapeControl.lean`

- file: [lean4/AuthIncompleteness/TapeControl.lean](../../../lean4/AuthIncompleteness/TapeControl.lean)
- sha256 (`bytes`): `88462fe7ef09d03d0250de9aaf91c0f43a86a17166a07e0bf3639981f3a584a8`
- cited in: node.lean, node.source, record TFQ-1353
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.TapeControl`): recorded sha256 `88462fe7ef09d03d0250de9aaf91c0f43a86a17166a07e0bf3639981f3a584a8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/TapeControl.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.TapeControlModels.syntactic_halt_does_not_select_terminal_policy` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1353_authf_halt_not_policy.md`

- file: [dag/derivations/29_computation/tfq_1353_authf_halt_not_policy.md](../../../dag/derivations/29_computation/tfq_1353_authf_halt_not_policy.md)
- sha256 (`lf-normalised`): `a2c244b8bec4a2594abfefcb73ac0cf399aa0c698d8ee8b4e0e7b0626140cc18`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1353
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-HALT-NOT-POLICY` `DERIVED_LEAN`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)

Outgoing (0):

