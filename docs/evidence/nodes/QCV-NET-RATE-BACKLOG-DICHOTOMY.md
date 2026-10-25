# QCV-NET-RATE-BACKLOG-DICHOTOMY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the QCV-Q1 model with q0 \>= 0, the backlog is bounded iff lam \<= (1-g)*mu; for g \>= 1 and lam \> 0 no mu \>= 0 bounds it; for g \< 1 and mu = kappa*r, with kappa \> 0, it is bounded iff r \>= lam/((1-g)*kappa); with r = 0 and lam \> 0 it equals q0 + t*lam.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A statement inside the declared model; it does not say any code has g \< 1 or that any supply r is available.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q1B claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcRepairQueue.lean`

- file: [lean4/QcRepairQueue.lean](../../../lean4/QcRepairQueue.lean)
- sha256 (`bytes`): `8dfb92005317d793979869da1eb38b11ac86a4bb1cdd0b44cef0c435cacd1267`
- cited in: node.lean, record TFQ-1316
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcRepairQueue`): recorded sha256 `8dfb92005317d793979869da1eb38b11ac86a4bb1cdd0b44cef0c435cacd1267` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcRepairQueue`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog_bounded_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms backlog_bounded_iff` |
| `backlog_le_initial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms backlog_le_initial` |
| `backlog_linear` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms backlog_linear` |
| `fresh_supply_threshold` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fresh_supply_threshold` |
| `no_bounded_backlog_if_unit_gain` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_bounded_backlog_if_unit_gain` |
| `no_supply_linear_growth` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_supply_linear_growth` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1316

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog` (rust_symbol) | yes | yes | yes | - | - |
| `backlog_bounded_decision` (rust_symbol) | yes | yes | yes | - | - |
| `supply_threshold` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1316

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog` (python_symbol) | yes | yes | yes | - | - |
| `backlog_bounded_decision` (python_symbol) | yes | yes | yes | - | - |
| `supply_threshold` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1316_qcv_net_rate_backlog_dichotomy.md`

- file: [dag/derivations/29_computation/tfq_1316_qcv_net_rate_backlog_dichotomy.md](../../../dag/derivations/29_computation/tfq_1316_qcv_net_rate_backlog_dichotomy.md)
- sha256 (`lf-normalised`): `b1bea1575d51ca9c7bddb5bee7ab5eae63399cdca2198bafd7a64a20da91e52b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1316
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

- `APP-R-QCV-NET-RATE-BACKLOG-DICHOTOMY` `DERIVED_LEAN`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)

Outgoing (2):

- `APP-R-QCV-CONDITIONAL-VIABILITY-CERTIFICATE` `CONDITIONAL_ON_IMPORT`: [QCV-CONDITIONAL-VIABILITY-CERTIFICATE](QCV-CONDITIONAL-VIABILITY-CERTIFICATE.md) (CONDITIONAL)
- `APP-R-QCV-FRESH-MARK-SUPPLY-BRIDGE` `DERIVED_PROSE`: [QCV-FRESH-MARK-SUPPLY-BRIDGE](QCV-FRESH-MARK-SUPPLY-BRIDGE.md) (DEFINITION)
