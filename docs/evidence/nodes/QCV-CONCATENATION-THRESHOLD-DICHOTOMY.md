# QCV-CONCATENATION-THRESHOLD-DICHOTOMY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the recurrence p(k+1) = c*p(k)^2 over Q, c*p(k) = (c*p(0))^(2^k); for c \> 0 and p(0) \>= 0: if c*p(0) \< 1 then p(k) tends to zero with c*p(k) \<= (c*p(0))^(k+1) and, for c*p(0) \<= 1/2, p(k) \<= (1/2)^(2^k)/c; if c*p(0) = 1 then p(k) = 1/c for all k; if c*p(0) \> 1 then p(k) diverges; so p(k) tends to zero iff p(0) \< 1/c.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 9 Lean reference(s) cited, 9 in this checkout (replay: none 9). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The recurrence is the hypothesis; no noise model is shown to obey it and no constant c is computed for any code.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q2 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcConcatenation.lean`

- file: [lean4/QcConcatenation.lean](../../../lean4/QcConcatenation.lean)
- sha256 (`bytes`): `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63`
- cited in: node.lean, record TFQ-1319
- replay: `none`
- check: `cd lean4 && lake build QcConcatenation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conc_closed` | yes | yes | yes | - | `#print axioms conc_closed` |
| `conc_eq_div` | yes | yes | yes | - | `#print axioms conc_eq_div` |
| `fixed_point` | yes | yes | yes | - | `#print axioms fixed_point` |
| `goesToZero_iff_below_threshold` | yes | yes | yes | - | `#print axioms goesToZero_iff_below_threshold` |
| `sub_bound` | yes | yes | yes | - | `#print axioms sub_bound` |
| `sub_half_bound` | yes | yes | yes | - | `#print axioms sub_half_bound` |
| `super_bound` | yes | yes | yes | - | `#print axioms super_bound` |
| `super_diverges` | yes | yes | yes | - | `#print axioms super_diverges` |
| `threshold_trichotomy` | yes | yes | yes | - | `#print axioms threshold_trichotomy` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1319

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify` (rust_symbol) | yes | yes | yes | - | - |
| `conc` (rust_symbol) | yes | yes | yes | - | - |
| `conc_closed_holds` (rust_symbol) | yes | yes | yes | - | - |
| `first_level_above` (rust_symbol) | yes | yes | yes | - | - |
| `first_level_below` (rust_symbol) | yes | yes | yes | - | - |
| `half_bound_holds` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1319

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify` (python_symbol) | yes | yes | yes | - | - |
| `conc` (python_symbol) | yes | yes | yes | - | - |
| `conc_closed_holds` (python_symbol) | yes | yes | yes | - | - |
| `first_level_above` (python_symbol) | yes | yes | yes | - | - |
| `first_level_below` (python_symbol) | yes | yes | yes | - | - |
| `half_bound_holds` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1319_qcv_concatenation_threshold_dichotomy.md`

- file: [dag/derivations/29_computation/tfq_1319_qcv_concatenation_threshold_dichotomy.md](../../../dag/derivations/29_computation/tfq_1319_qcv_concatenation_threshold_dichotomy.md)
- sha256 (`lf-normalised`): `3d98a033f36992969e098f65f595cc567c98a64d3c9167fb8eb3fb2358c264df`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1319
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

- `APP-R-QCV-CONCATENATION-THRESHOLD-DICHOTOMY` `DERIVED_LEAN`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION), [QCV-IMPORT-THRESHOLD-THEOREM](QCV-IMPORT-THRESHOLD-THEOREM.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-QCV-OVERHEAD-GROWTH-CRITERION` `DERIVED_LEAN`: [QCV-OVERHEAD-GROWTH-CRITERION](QCV-OVERHEAD-GROWTH-CRITERION.md) (PROVED_LEAN)
