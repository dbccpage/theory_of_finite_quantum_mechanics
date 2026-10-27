# PGW-PYTHON-LEAN-CARRIER-BRIDGE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No refinement proof joins any Python computation to any Lean statement. The sealed Lean is a token-erased abstraction connected to the sealed Python by executable checks only (CL-TOKEN-ERASURE); the Alpha harness's Lean is about harness datatypes, python_driver_refinement is NOT_PROVED and it does not model the new license binding (D4); attempt two's Lean speaks of every history of sealed events and switch markers, and that each edge of a Python run is such a history is read, not proved. Rung two track one's represented state is not bridged to the sealed regime (L-1, which needs an amendment of the seal that is the author's act), and the reading regimes differ: R2L and R2F in Lean, the sealed genesis histories that stop before the requirement in Python.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- distinct cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

These two replays are sealed Lean histories. They are not a refinement from a Python computation to a Lean statement. Token erasure, the license binding, rung-two track one, and the Python histories that stop before the requirement stay open. Status stays OPEN.

## Source status

closeout.txt §1 carriers and §9.1 D4; continuation.txt §13 carrier bridges (L-1)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/PregenesisPythonLeanCarrierBridge.lean`

- file: [lean4/PregenesisPythonLeanCarrierBridge.lean](../../../lean4/PregenesisPythonLeanCarrierBridge.lean)
- sha256 (`bytes`): `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3`
- cited in: node.lean, receipt dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json (PregenesisPythonLeanCarrierBridge), receipt dag/research/pr_320_current_lean_replay.json (PregenesisPythonLeanCarrierBridge), record TFQ-0499
- replay: `verified`
  - receipt [dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json](../../../dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json) (module `PregenesisPythonLeanCarrierBridge`): recorded sha256 `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_320_current_lean_replay.json](../../../dag/research/pr_320_current_lean_replay.json) (module `PregenesisPythonLeanCarrierBridge`): recorded sha256 `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisPythonLeanCarrierBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwData_counts` | yes | yes | yes | none | `#print axioms pgwData_counts` |
| `pgwEmpty_carriers` | yes | yes | yes | none | `#print axioms pgwEmpty_carriers` |
| `pgwHistoryF_replays` | yes | yes | yes | propext | `#print axioms pgwHistoryF_replays` |
| `pgwHistoryL_replays` | yes | yes | yes | propext | `#print axioms pgwHistoryL_replays` |
| `pgwHistory_lengths` | yes | yes | yes | none | `#print axioms pgwHistory_lengths` |
| `pgwR2L_ne_R2F` | yes | yes | yes | none | `#print axioms pgwR2L_ne_R2F` |
| `pgwReplay_ne` | yes | yes | yes | propext | `#print axioms pgwReplay_ne` |
| `pgwReqs` | yes | yes | yes | none | `#print axioms pgwReqs` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs)
- sha256 (`bytes`): `867338d50212fc47d60491a47f12c0538343f146d389588f8b480cb34764d23e`
- cited in: node.rust, record TFQ-0499

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replay` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py)
- sha256 (`bytes`): `6a7fd2ba9688d47e9291514c623a811cde3c6b9e8fda1d12a608dc9bb0b1f3c2`
- cited in: record TFQ-0499

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replay` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-python-lean-carrier-bridge.py`

- file: [checks/independent/pgw-python-lean-carrier-bridge.py](../../../checks/independent/pgw-python-lean-carrier-bridge.py)
- sha256 (`bytes`): `537eda034fc19d0d6adc3e874a12ede9e09e27b8888fc3788b74d8e1f3464788`
- cited in: record TFQ-0499

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md`

- file: [dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md](../../../dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md)
- sha256 (`lf-normalised`): `5acaa41c6e0b52d3d3aa007d5a9860f1fcb4c49a2f4e7c25d64300c87de45316`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0499
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-python-lean-carrier-bridge.md`

- file: [dag/derivations/independent/pgw-python-lean-carrier-bridge.md](../../../dag/derivations/independent/pgw-python-lean-carrier-bridge.md)
- sha256 (`lf-normalised`): `0f8dcc31634fe521f22e51cb1519572293b62282e9b56bbb324f1d777409bfe7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json`

- file: [dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json](../../../dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json)
- sha256 (`lf-normalised`): `39dc4682d9f3dbe249fdced747303a743a328d6a2ac01ea67166c9d8f497fed9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `PGW-R-PYTHON-LEAN-CARRIER-BRIDGE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

