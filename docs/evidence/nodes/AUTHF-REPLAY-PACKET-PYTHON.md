# AUTHF-REPLAY-PACKET-PYTHON

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A manifest binding eight artifacts by SHA-256 together with a four-row transition proposal, a contract and a leave-open policy verifies under the Python port; it finds the clean-terminal contract preserved, the marked-cell contract violated at runningMarked and haltedMarked, the control-outcome report inadequate (haltedBlank and haltedMarked share stay), the route open_due_to_inadequate_report and the terminal open, and refuses 21 tamper mutations.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Evaluator correspondence to the Lean model, SHA-256 collision resistance, runtime integrity and custody remain assumptions; the PowerShell runtime pin is not reproduced and the formal replay uses Lean v4.35.0 instead of the recorded v4.32.2.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-23 claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/auth_incompleteness/replay_packet.py`

- file: [code/python/src/qm/auth_incompleteness/replay_packet.py](../../../code/python/src/qm/auth_incompleteness/replay_packet.py)
- sha256 (`bytes`): `3d2bb1abdeeff00a6c3c7c5deb7e26f4fcacf8a7594916273587c759fcbb3196`
- cited in: node.source, record TFQ-1361

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check_packet` (python_symbol) | yes | yes | yes | - | - |
| `invoke_replay_packet` (python_symbol) | yes | yes | yes | - | - |
| `transition_evaluation` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_replay_packet.py`

- file: [code/python/tests/test_auth_incompleteness_replay_packet.py](../../../code/python/tests/test_auth_incompleteness_replay_packet.py)
- sha256 (`bytes`): `8d881e902654a1e0f9294c8f7df915f1591772f35827af2950f741c1f0330087`
- cited in: record TFQ-1361
- check: `python -m pytest code/python/tests/test_auth_incompleteness_replay_packet.py::test_case_01_good_packet_verifies`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_case_01_good_packet_verifies` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_replay_packet.py::test_case_01_good_packet_verifies` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1361_authf_replay_packet_python.md`

- file: [dag/derivations/29_computation/tfq_1361_authf_replay_packet_python.md](../../../dag/derivations/29_computation/tfq_1361_authf_replay_packet_python.md)
- sha256 (`lf-normalised`): `0b8139913b4b2c961f179fb2f1eaaf558fdd73b12487278f0cb2296742353e2d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1361
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-REPLAY-PACKET-PYTHON` `COMPUTED`: [AUTHF-TRANSITION-ADEQUACY](AUTHF-TRANSITION-ADEQUACY.md) (PROVED_LEAN), [TFQ-0331](TFQ-0331.md) (SOURCE_RECORD)

Outgoing (0):

