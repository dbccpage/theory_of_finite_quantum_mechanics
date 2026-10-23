# PGW-PYTHON-LEAN-CARRIER-BRIDGE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No refinement proof joins any Python computation to any Lean statement. The sealed Lean is a token-erased abstraction connected to the sealed Python by executable checks only (CL-TOKEN-ERASURE); the Alpha harness's Lean is about harness datatypes, python_driver_refinement is NOT_PROVED and it does not model the new license binding (D4); attempt two's Lean speaks of every history of sealed events and switch markers, and that each edge of a Python run is such a history is read, not proved. Rung two track one's represented state is not bridged to the sealed regime (L-1, which needs an amendment of the seal that is the author's act), and the reading regimes differ: R2L and R2F in Lean, the sealed genesis histories that stop before the requirement in Python.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open; agreement between Python and Lean is evidenced by executable checks on the inputs checked, which is not a refinement proof.

## Source status

closeout.txt §1 carriers and §9.1 D4; continuation.txt §13 carrier bridges (L-1)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/SecondRun/Kernel.lean`

- file: [lean4/Imported/Genesis19l57g1/SecondRun/Kernel.lean](../../../lean4/Imported/Genesis19l57g1/SecondRun/Kernel.lean)
- sha256 (`bytes`): `c88243985ee7dc438aa644b70a3259fd192647a25ee9ce4f3699ab44c130b1b4`
- cited in: node.lean, record TFQ-0499
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/SecondRun/Kernel.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replayE` | yes | yes | yes | - | `#print axioms replayE` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md`

- file: [dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md](../../../dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md)
- sha256 (`lf-normalised`): `0c923809aaa33743bc4892d81d9fa0057c39b179cca9faf31ca7a3edcab25c72`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0499
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::replay`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs::replay`

## Routes

Incoming (1):

- `PGW-R-PYTHON-LEAN-CARRIER-BRIDGE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

