# QCV-SELF-OBSTRUCTION-MODEL

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Backlog q(t+1) = max(0, q(t) + lam + g*mu - mu) in units of the Phi_1 repair cost, where lam is the residual generated per round by the computation, mu = kappa*r the repair rate from r fresh ancillas per round at kappa units each, and g the residual generated per unit of repair; with g = 0 this is the DS-QM101 queue; a distance-three level with a fault locations has constant c = a(a-1)/2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- declared generation rate lam
- declared self-generated fraction g of repair
- declared capacity kappa per fresh ancilla
- declared fresh supply r per round

## Bottleneck

lam, g, kappa and r are declared inputs; no value is derived or measured for any code, and Phi_1 of a residual is not computed here.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q1 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcConcatenation.lean`

- file: [lean4/QcConcatenation.lean](../../../lean4/QcConcatenation.lean)
- sha256 (`bytes`): `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63`
- cited in: node.lean, record TFQ-1315
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcConcatenation`): recorded sha256 `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcConcatenation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pairCount` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pairCount` |
- counts toward the grade: yes

### Lean: `lean4/QcRepairQueue.lean`

- file: [lean4/QcRepairQueue.lean](../../../lean4/QcRepairQueue.lean)
- sha256 (`bytes`): `8dfb92005317d793979869da1eb38b11ac86a4bb1cdd0b44cef0c435cacd1267`
- cited in: node.lean, record TFQ-1315
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcRepairQueue`): recorded sha256 `8dfb92005317d793979869da1eb38b11ac86a4bb1cdd0b44cef0c435cacd1267` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcRepairQueue`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms backlog` |
| `drift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms drift` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1315

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog` (rust_symbol) | yes | yes | yes | - | - |
| `pair_count` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1315

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `backlog` (python_symbol) | yes | yes | yes | - | - |
| `pair_count` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivation_dag.json`

- file: [dag/derivation_dag.json](../../../dag/derivation_dag.json)
- sha256 (`lf-normalised`): `fc072fb495b2f38db8888efe620005e6a741cc13372d672fe7e67505e6cb053c`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/29_computation/tfq_1315_qcv_self_obstruction_model.md`

- file: [dag/derivations/29_computation/tfq_1315_qcv_self_obstruction_model.md](../../../dag/derivations/29_computation/tfq_1315_qcv_self_obstruction_model.md)
- sha256 (`lf-normalised`): `041e6e718533e0a7a8b64c12abc77e0c6582379dbec1c1b29c56a6129e88b845`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1315
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

- `APP-R-QCV-SELF-OBSTRUCTION-MODEL` `DERIVED_PROSE`: [QCV-QUESTION-SELF-LIMITING-REPAIR](QCV-QUESTION-SELF-LIMITING-REPAIR.md) (OPEN), [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (PROVED_LEAN), [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [DS-QM061-BUILDABILITY-SET-S](DS-QM061-BUILDABILITY-SET-S.md) (COMPUTATIONALLY_CHECKED)

Outgoing (4):

- `APP-R-QCV-CONCATENATION-THRESHOLD-DICHOTOMY` `DERIVED_LEAN`: [QCV-CONCATENATION-THRESHOLD-DICHOTOMY](QCV-CONCATENATION-THRESHOLD-DICHOTOMY.md) (PROVED_LEAN)
- `APP-R-QCV-NET-RATE-BACKLOG-DICHOTOMY` `DERIVED_LEAN`: [QCV-NET-RATE-BACKLOG-DICHOTOMY](QCV-NET-RATE-BACKLOG-DICHOTOMY.md) (PROVED_LEAN)
- `APP-R-QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY` `DERIVED_LEAN`: [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN)
- `APP-R-QCV-REPAIR-NEEDED-BUT-COSTLY` `DERIVED_LEAN`: [QCV-REPAIR-NEEDED-BUT-COSTLY](QCV-REPAIR-NEEDED-BUT-COSTLY.md) (PROVED_LEAN)
