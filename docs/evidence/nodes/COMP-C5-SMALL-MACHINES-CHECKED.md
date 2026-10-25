# COMP-C5-SMALL-MACHINES-CHECKED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rust: a binary incrementer on inputs 0 to 40 with 0 to 2 padding cells (steps 2c+1, value n+1), the two-state busy beaver in the TM0 form (12 steps, 4 ones), step simulation on all 3150 small configurations of that machine; Python: all 6561 two-state two-symbol TM0 machines for 20 steps from the blank tape with a different tape representation; Lean: one write-and-halt machine.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 4
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite instances; they are not a proof for other machines.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C5d claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompTM.lean`

- file: [lean4/GenesisCompTM.lean](../../../lean4/GenesisCompTM.lean)
- sha256 (`bytes`): `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c`
- cited in: node.lean, record TFQ-1302
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompTM`): recorded sha256 `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompTM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `writeOne_halts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms writeOne_halts` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, node.source, record TFQ-1302

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `busy_beaver_2` (rust_symbol) | yes | yes | yes | - | - |
| `busy_beaver_2_matches_machine` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp busy_beaver_2_matches_machine` |
| `incrementer` (rust_symbol) | yes | yes | yes | - | - |
| `incrementer_matches_machine_for_all_small_inputs` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp incrementer_matches_machine_for_all_small_inputs` |
| `step_simulation_holds_on_every_small_configuration` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp step_simulation_holds_on_every_small_configuration` |

- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1302

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `all_two_state_machines` (python_symbol) | yes | yes | yes | - | - |
| `busy_beaver_2` (python_symbol) | yes | yes | yes | - | - |
| `incrementer` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_genesis_tm.py`

- file: [code/python/tests/test_genesis_tm.py](../../../code/python/tests/test_genesis_tm.py)
- sha256 (`bytes`): `6aefb990bc7d69e26cf22c1fe85301a5d07e73b85e2da39de613765242f30f60`
- cited in: record TFQ-1302
- check: `python -m pytest code/python/tests/test_genesis_tm.py::test_all_two_state_two_symbol_machines_step_simulation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_all_two_state_two_symbol_machines_step_simulation` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_genesis_tm.py::test_all_two_state_two_symbol_machines_step_simulation` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1302_comp_c5_small_machines_checked.md`

- file: [dag/derivations/29_computation/tfq_1302_comp_c5_small_machines_checked.md](../../../dag/derivations/29_computation/tfq_1302_comp_c5_small_machines_checked.md)
- sha256 (`lf-normalised`): `130a3316f341a83bf8a45d1f51b6b0c77848a221d22cce61bb3ca4e12334d812`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1302
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C5-SMALL-MACHINES-CHECKED` `COMPUTED`: [COMP-C5-CLOSURES-HALTING](COMP-C5-CLOSURES-HALTING.md) (PROVED_LEAN)

Outgoing (0):

