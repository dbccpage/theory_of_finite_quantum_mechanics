# QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For complex matrices of any size d and the variational trace norm tn(X) = sup over unitaries U of |tr(UX)|, the global depolarizing channel satisfies tn(Delta_p(rho) - Delta_p(sigma)) = (1-p)*tn(rho - sigma) for equal-trace rho, sigma and p \<= 1; along any history of unitaries V(i) with depolarizing rates p(i) in \[0,1\], tn(run rho - run sigma) = (product of (1-p(i)))*tn(rho - sigma), which is at most (1-p)^t*tn(rho - sigma) when every p(i) \>= p, and (1-p)^t \<= 1/(1+p*t).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- variational trace norm equals the Schatten-1 norm (Ky Fan, cited)
- global depolarizing noise at a declared rate after every step

## Bottleneck

The trace norm is the variational form, whose equality with the sum of singular values is cited; the noise is global depolarizing with a declared rate per step, not independent per-qubit noise, and the statement is about histories without fresh resets.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q4 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcEntropySink.lean`

- file: [lean4/QcEntropySink.lean](../../../lean4/QcEntropySink.lean)
- sha256 (`bytes`): `361f4c3df7c3ef3ffa91793a3d1756a51a2c051ed83d2a3f86be65db06923bf2`
- cited in: node.lean, record TFQ-1322
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `QcEntropySink`): recorded sha256 `361f4c3df7c3ef3ffa91793a3d1756a51a2c051ed83d2a3f86be65db06923bf2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build QcEntropySink`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decay_below` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms decay_below` |
| `decay_le_inv` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms decay_le_inv` |
| `depol_dist` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms depol_dist` |
| `noisyStep_dist` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms noisyStep_dist` |
| `pairingSet_bddAbove` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pairingSet_bddAbove` |
| `run_dist` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms run_dist` |
| `run_dist_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms run_dist_le` |
| `tn` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tn` |
| `tn_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tn_conj` |
| `tn_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tn_smul` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1322

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decay_le_inv_holds` (rust_symbol) | yes | yes | yes | - | - |
| `depolarize_matrix` (rust_symbol) | yes | yes | yes | - | - |
| `depth_until_below` (rust_symbol) | yes | yes | yes | - | - |
| `matrix_step` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1322

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decay_le_inv_holds` (python_symbol) | yes | yes | yes | - | - |
| `depolarize_matrix` (python_symbol) | yes | yes | yes | - | - |
| `depth_until_below` (python_symbol) | yes | yes | yes | - | - |
| `matrix_step` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1322_qcv_noisy_history_trace_distance_decay.md`

- file: [dag/derivations/29_computation/tfq_1322_qcv_noisy_history_trace_distance_decay.md](../../../dag/derivations/29_computation/tfq_1322_qcv_noisy_history_trace_distance_decay.md)
- sha256 (`lf-normalised`): `e806ef87fd15d67692848a5c0a0036f8986114d8f07cc69b8d4d0acd65723b23`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1322
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

- `APP-R-QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY` `DERIVED_LEAN`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION), [QCV-IMPORT-NOISY-REVERSIBLE-LIMITS](QCV-IMPORT-NOISY-REVERSIBLE-LIMITS.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `APP-R-QCV-CONDITIONAL-VIABILITY-CERTIFICATE` `CONDITIONAL_ON_IMPORT`: [QCV-CONDITIONAL-VIABILITY-CERTIFICATE](QCV-CONDITIONAL-VIABILITY-CERTIFICATE.md) (CONDITIONAL)
- `APP-R-QCV-FRESH-MARK-SUPPLY-BRIDGE` `DERIVED_PROSE`: [QCV-FRESH-MARK-SUPPLY-BRIDGE](QCV-FRESH-MARK-SUPPLY-BRIDGE.md) (DEFINITION)
- `APP-R-QCV-QUBIT-BLOCH-DECAY-EXACT` `DERIVED_LEAN`: [QCV-QUBIT-BLOCH-DECAY-EXACT](QCV-QUBIT-BLOCH-DECAY-EXACT.md) (PROVED_LEAN)
