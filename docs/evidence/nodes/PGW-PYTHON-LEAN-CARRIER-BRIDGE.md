# PGW-PYTHON-LEAN-CARRIER-BRIDGE

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No refinement proof joins any Python computation to any Lean statement. The sealed Lean is a token-erased abstraction connected to the sealed Python by executable checks only (CL-TOKEN-ERASURE); the Alpha harness's Lean is about harness datatypes, python_driver_refinement is NOT_PROVED and it does not model the new license binding (D4); attempt two's Lean speaks of every history of sealed events and switch markers, and that each edge of a Python run is such a history is read, not proved. Rung two track one's represented state is not bridged to the sealed regime (L-1, which needs an amendment of the seal that is the author's act), and the reading regimes differ: R2L and R2F in Lean, the sealed genesis histories that stop before the requirement in Python.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Lean: `lean4/CampaignPgwPythonLeanCarrierBridge.lean`

- file: [lean4/CampaignPgwPythonLeanCarrierBridge.lean](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- sha256 (`bytes`): `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3`
- cited in: node.lean, receipt dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json (CampaignPgwPythonLeanCarrierBridge), receipt dag/research/pr_320_current_lean_replay.json (CampaignPgwPythonLeanCarrierBridge), record TFQ-0499
- replay: `verified`
  - receipt [dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json](../../../dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json) (module `CampaignPgwPythonLeanCarrierBridge`): recorded sha256 `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_320_current_lean_replay.json](../../../dag/research/pr_320_current_lean_replay.json) (module `CampaignPgwPythonLeanCarrierBridge`): recorded sha256 `096d8f363f7190fcf8f5d9cb4058b440307229794ae2507c1d7bf87d827740f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwPythonLeanCarrierBridge`

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

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-python-lean-carrier-bridge.py`

- file: [checks/independent/pgw-python-lean-carrier-bridge.py](../../../checks/independent/pgw-python-lean-carrier-bridge.py)
- sha256 (`bytes`): `9a1eab0f6a57e471781b2885f4e388bee921a86d22b615040c7f95d7598ed16a`
- cited in: record TFQ-0499

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md`

- file: [dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md](../../../dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md)
- sha256 (`lf-normalised`): `904afe91e471d24d6daee6002bfcb03806805c0c609f9278bb97da76a83d022a`
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
- sha256 (`lf-normalised`): `38c3772b98208d02c0eb882af95a681ad1cf2c61d62dd55b6a8bb7feedf12cc2`
- cited in: node.source
- counts toward the grade: yes

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

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::replay`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs::replay`

## Routes

Incoming (1):

- `PGW-R-PYTHON-LEAN-CARRIER-BRIDGE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

