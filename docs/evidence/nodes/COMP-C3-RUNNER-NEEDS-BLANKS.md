# COMP-C3-RUNNER-NEEDS-BLANKS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The one-state machine that moves right forever reaches words of every length under the TM0 encoding, so its bounded search is closed at no bound and the bounded decider returns boundExceeded at every bound; any regime that reaches arbitrarily long words is closed at no bound.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

One concrete machine; the general statement for every general-purpose regime is conditional (COMP-C3e).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C3d claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompTM.lean`

- file: [lean4/GenesisCompTM.lean](../../../lean4/GenesisCompTM.lean)
- sha256 (`bytes`): `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c`
- cited in: node.lean, node.source, record TFQ-1294
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompTM`): recorded sha256 `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompTM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `runner_not_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms runner_not_closed` |
| `runner_step` | yes | yes | yes | propext | `#print axioms runner_step` |
| `runner_unbounded` | yes | yes | yes | Quot.sound, propext | `#print axioms runner_unbounded` |
| `runner_unboundedSupply` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms runner_unboundedSupply` |
- counts toward the grade: yes

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1294
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closed_bounds_reach` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms closed_bounds_reach` |
| `not_closed_of_unbounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms not_closed_of_unbounded` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1294
- check: `cd code/rust && cargo test -p tfqm_wdp right_runner_is_refused_by_every_bounded_decider`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `right_runner` (rust_symbol) | yes | yes | yes | - | - |
| `right_runner_is_refused_by_every_bounded_decider` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp right_runner_is_refused_by_every_bounded_decider` |
- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1294

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `right_runner` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/tests/test_genesis_tm.py`

- file: [code/python/tests/test_genesis_tm.py](../../../code/python/tests/test_genesis_tm.py)
- sha256 (`bytes`): `6aefb990bc7d69e26cf22c1fe85301a5d07e73b85e2da39de613765242f30f60`
- cited in: record TFQ-1294
- check: `python -m pytest code/python/tests/test_genesis_tm.py::test_right_runner_needs_unbounded_blanks`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_right_runner_needs_unbounded_blanks` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_genesis_tm.py::test_right_runner_needs_unbounded_blanks` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1294_comp_c3_runner_needs_blanks.md`

- file: [dag/derivations/29_computation/tfq_1294_comp_c3_runner_needs_blanks.md](../../../dag/derivations/29_computation/tfq_1294_comp_c3_runner_needs_blanks.md)
- sha256 (`lf-normalised`): `1532bcf561e0af208403d732cc9dc296fb2688ecb619ca99dbef917095d77735`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1294
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C3-RUNNER-NEEDS-BLANKS` `DERIVED_LEAN`: [COMP-C3-VERDICT-SOUND](COMP-C3-VERDICT-SOUND.md) (PROVED_LEAN), [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C3-NO-FIXED-BOUND` `CONDITIONAL_ON_IMPORT`: [COMP-C3-NO-FIXED-BOUND](COMP-C3-NO-FIXED-BOUND.md) (CONDITIONAL)
