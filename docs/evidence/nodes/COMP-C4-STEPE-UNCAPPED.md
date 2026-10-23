# COMP-C4-STEPE-UNCAPPED

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the byte copy of stepE, k copies of admitDatum replay to data = base.data + k, for every n a history reaches at least n data, and no event lowers the number of data; unbounded admission is permitted by the event semantics.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is a statement about the copied stepE; every admitDatum is a host event and nothing here generates them.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C4a claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, node.source, record TFQ-1296
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `genesis_unbounded_admission` | yes | yes | yes | propext | `#print axioms genesis_unbounded_admission` |
| `replay_admitDatum_replicate` | yes | yes | yes | propext | `#print axioms replay_admitDatum_replicate` |
| `stepE` | yes | yes | yes | module-level | `#print axioms stepE` |
| `stepE_data_mono` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms stepE_data_mono` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1296
- check: `cd code/rust && cargo test -p tfqm_wdp first_separation_replays_and_admission_is_uncapped`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `first_separation_replays_and_admission_is_uncapped` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_wdp first_separation_replays_and_admission_is_uncapped` |
| `step_e` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1296

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replay` (python_symbol) | yes | yes | yes | - | - |
| `step_e` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1296_comp_c4_stepe_uncapped.md`

- file: [dag/derivations/29_computation/tfq_1296_comp_c4_stepe_uncapped.md](../../../dag/derivations/29_computation/tfq_1296_comp_c4_stepe_uncapped.md)
- sha256 (`lf-normalised`): `ce75002557552695699573a30e589cfdb2d8b4eaa4b61815b18d24bd96fa50a2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1296
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C4-STEPE-UNCAPPED` `DERIVED_LEAN`: [COMP-C1-FIRST-SEPARATION-REPLAY](COMP-C1-FIRST-SEPARATION-REPLAY.md) (COMPUTATIONALLY_CHECKED), [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
