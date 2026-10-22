# QCV-FRESH-MARK-SUPPLY-BRIDGE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A fresh-mark supply is a stream of distinguished marks each usable once; a process consuming at least rmin \> 0 marks per round completes at most B/rmin rounds from a total supply B, and a positive per-round consumption exhausts every finite supply; reliable quantum computation of unbounded length (QCV-Q1B, QCV-Q4) and Turing-complete computation in the parallel UTM branch each need such an unbounded supply.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A bridge definition only: no common theorem is proved, no map between the entropy-sink supply and the blank-tape supply of the UTM branch is defined, and that branch is not part of this checkout.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q6 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcRepairQueue.lean`

- file: [lean4/QcRepairQueue.lean](../../../lean4/QcRepairQueue.lean)
- sha256 (`bytes`): `8dfb92005317d793979869da1eb38b11ac86a4bb1cdd0b44cef0c435cacd1267`
- cited in: node.lean, record TFQ-1327
- replay: `none`
- check: `cd lean4 && lake build QcRepairQueue`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `budget_exhausted` | yes | yes | yes | - | `#print axioms budget_exhausted` |
| `rounds_le_budget` | yes | yes | yes | - | `#print axioms rounds_le_budget` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1327

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rounds_upper_bound` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1327

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rounds_upper_bound` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1327_qcv_fresh_mark_supply_bridge.md`

- file: [dag/derivations/29_computation/tfq_1327_qcv_fresh_mark_supply_bridge.md](../../../dag/derivations/29_computation/tfq_1327_qcv_fresh_mark_supply_bridge.md)
- sha256 (`lf-normalised`): `b4f45e8040fefcc82c0f83c861a18a84136e4d4da5c1af36535f8f8f22c5f1d8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1327
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/quantum_computation_self_obstruction_axioms.txt`

- file: [dag/research/quantum_computation_self_obstruction_axioms.txt](../../../dag/research/quantum_computation_self_obstruction_axioms.txt)
- sha256 (`lf-normalised`): `b4c803ee2b1a4fe8af1d9d92a351fb11c61d2791bea01a5b7cd3dd7c1623af81`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-FRESH-MARK-SUPPLY-BRIDGE` `DERIVED_PROSE`: [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN), [QCV-NET-RATE-BACKLOG-DICHOTOMY](QCV-NET-RATE-BACKLOG-DICHOTOMY.md) (PROVED_LEAN)

Outgoing (0):

