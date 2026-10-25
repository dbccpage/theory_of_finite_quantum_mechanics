# QCV-QUBIT-BLOCH-DECAY-EXACT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For rational Bloch vectors, noisy steps r -\> (1-p)*R*r with rational rotations R (R^T R = 1) give sqDist(run r, run s) = (product of (1-p(i))^2)*sqDist(r, s), at most ((1-p)^2)^t*sqDist(r, s) when every p(i) in \[p,1\]; and (v.sigma)^2 = (v.v)*1 over the complex numbers, so the difference of two qubit states has both singular values |r-s|/2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- trace norm of a Hermitian matrix is the sum of absolute eigenvalues (cited)

## Bottleneck

The identification of the qubit trace norm with the Bloch distance uses the cited eigenvalue fact; Python and Rust replays are exact on declared instances only.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q4B claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcEntropySink.lean`

- file: [lean4/QcEntropySink.lean](../../../lean4/QcEntropySink.lean)
- sha256 (`bytes`): `361f4c3df7c3ef3ffa91793a3d1756a51a2c051ed83d2a3f86be65db06923bf2`
- cited in: node.lean, record TFQ-1323
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcEntropySink`): recorded sha256 `361f4c3df7c3ef3ffa91793a3d1756a51a2c051ed83d2a3f86be65db06923bf2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcEntropySink`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `blochMat_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms blochMat_sq` |
| `rot_dot` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms rot_dot` |
| `sqDist_runB` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sqDist_runB` |
| `sqDist_runB_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sqDist_runB_le` |
| `sqDist_stepB` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sqDist_stepB` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1323

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bloch_of_matrix` (rust_symbol) | yes | yes | yes | - | - |
| `bloch_run` (rust_symbol) | yes | yes | yes | - | - |
| `bloch_step` (rust_symbol) | yes | yes | yes | - | - |
| `decay_identity_holds` (rust_symbol) | yes | yes | yes | - | - |
| `pauli_part_squares_to_norm` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1323

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bloch_of_matrix` (python_symbol) | yes | yes | yes | - | - |
| `bloch_run` (python_symbol) | yes | yes | yes | - | - |
| `bloch_step` (python_symbol) | yes | yes | yes | - | - |
| `decay_identity_holds` (python_symbol) | yes | yes | yes | - | - |
| `pauli_part_squares_to_norm` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1323_qcv_qubit_bloch_decay_exact.md`

- file: [dag/derivations/29_computation/tfq_1323_qcv_qubit_bloch_decay_exact.md](../../../dag/derivations/29_computation/tfq_1323_qcv_qubit_bloch_decay_exact.md)
- sha256 (`lf-normalised`): `55d721d603760a0527de5e219b11eef271096e6b13bd7bee08ad4e0009f24ff6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1323
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

- `APP-R-QCV-QUBIT-BLOCH-DECAY-EXACT` `DERIVED_LEAN`: [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN)

Outgoing (0):

