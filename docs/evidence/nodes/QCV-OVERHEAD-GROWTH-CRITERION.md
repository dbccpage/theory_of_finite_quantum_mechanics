# QCV-OVERHEAD-GROWTH-CRITERION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For p(k+1) = c(k)*p(k)^2 with c(k) \>= 0, p(k) = p(0)^(2^k)*amp(k) with amp(0) = 1, amp(k+1) = c(k)*amp(k)^2, and some p(0) \> 0 has p(k) tending to zero iff some M \> 0 has amp(k) \<= M^(2^k) for all k; the criterion holds for c(k) \<= C, for c(k) \<= A*B^(k+1) with A, B \>= 1, for c(k) = (k+1)^2, and for c(k) \<= a*b^N(k) with block size N(k+1) \<= s*N(k), s \< 2; it fails for c(k) \>= a*b^(2^k) with a \> 0, b \> 1, and for c(k) \>= a*b^N(k) with 2^k \<= N(k), b \> 1, where no positive p(0) has p(k) tending to zero.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 29
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 13 Lean reference(s) cited, 13 in this checkout (replay: none 13). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The families are exact illustrations of the criterion, not claims that any physical overhead has such a form; correlated-noise strength as an exponential of block size is a declared toy.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q3 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/QcConcatenation.lean`

- file: [lean4/QcConcatenation.lean](../../../lean4/QcConcatenation.lean)
- sha256 (`bytes`): `5fea043a891ddf38414c7d169710a95f54e3f28b7b94fc11bd96ecef69541c63`
- cited in: node.lean, record TFQ-1320
- replay: `none`
- check: `cd lean4 && lake build QcConcatenation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ampBounded_of_bounded` | yes | yes | yes | - | `#print axioms ampBounded_of_bounded` |
| `ampBounded_of_geom` | yes | yes | yes | - | `#print axioms ampBounded_of_geom` |
| `ampBounded_of_sizes` | yes | yes | yes | - | `#print axioms ampBounded_of_sizes` |
| `ampBounded_poly` | yes | yes | yes | - | `#print axioms ampBounded_poly` |
| `amp_dexp_sq` | yes | yes | yes | - | `#print axioms amp_dexp_sq` |
| `blockExp_le` | yes | yes | yes | - | `#print axioms blockExp_le` |
| `bounded_overhead_goesToZero` | yes | yes | yes | - | `#print axioms bounded_overhead_goesToZero` |
| `concv_eq_amp` | yes | yes | yes | - | `#print axioms concv_eq_amp` |
| `dexp_not_ampBounded` | yes | yes | yes | - | `#print axioms dexp_not_ampBounded` |
| `dexp_region_empty` | yes | yes | yes | - | `#print axioms dexp_region_empty` |
| `region_empty_iff` | yes | yes | yes | - | `#print axioms region_empty_iff` |
| `sizes_not_ampBounded` | yes | yes | yes | - | `#print axioms sizes_not_ampBounded` |
| `threshold_region_iff` | yes | yes | yes | - | `#print axioms threshold_region_iff` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs`

- file: [code/rust/src/qm/campaigns/qc_self_obstruction.rs](../../../code/rust/src/qm/campaigns/qc_self_obstruction.rs)
- sha256 (`bytes`): `7ec8808a14754317eca2df6528a90985a6cbbaaddbf17c611cd236cd45eef4e3`
- cited in: node.rust, record TFQ-1320

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `amp` (rust_symbol) | yes | yes | yes | - | - |
| `amp_bound_holds` (rust_symbol) | yes | yes | yes | - | - |
| `amp_escape_level` (rust_symbol) | yes | yes | yes | - | - |
| `block_exp_bound_holds` (rust_symbol) | yes | yes | yes | - | - |
| `concv` (rust_symbol) | yes | yes | yes | - | - |
| `dexp_square_identity_holds` (rust_symbol) | yes | yes | yes | - | - |
| `geom_invariant_holds` (rust_symbol) | yes | yes | yes | - | - |
| `size_family` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/qc_self_obstruction.py`

- file: [code/python/src/qm/qc_self_obstruction.py](../../../code/python/src/qm/qc_self_obstruction.py)
- sha256 (`bytes`): `bfc41c6def8f655c61bde3475189a299d276bae04e1f8c75f09f1d35a6d89d66`
- cited in: record TFQ-1320

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `amp` (python_symbol) | yes | yes | yes | - | - |
| `amp_bound_holds` (python_symbol) | yes | yes | yes | - | - |
| `amp_escape_level` (python_symbol) | yes | yes | yes | - | - |
| `block_exp_bound_holds` (python_symbol) | yes | yes | yes | - | - |
| `concv` (python_symbol) | yes | yes | yes | - | - |
| `dexp_square_identity_holds` (python_symbol) | yes | yes | yes | - | - |
| `geom_invariant_holds` (python_symbol) | yes | yes | yes | - | - |
| `size_family` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1320_qcv_overhead_growth_criterion.md`

- file: [dag/derivations/29_computation/tfq_1320_qcv_overhead_growth_criterion.md](../../../dag/derivations/29_computation/tfq_1320_qcv_overhead_growth_criterion.md)
- sha256 (`lf-normalised`): `d3fc380988251f78ddec1b1291472a05f9f8a8ffb3ffaf02d8422c1c6ad412a4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1320
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

- `APP-R-QCV-OVERHEAD-GROWTH-CRITERION` `DERIVED_LEAN`: [QCV-CONCATENATION-THRESHOLD-DICHOTOMY](QCV-CONCATENATION-THRESHOLD-DICHOTOMY.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-QCV-CONDITIONAL-VIABILITY-CERTIFICATE` `CONDITIONAL_ON_IMPORT`: [QCV-CONDITIONAL-VIABILITY-CERTIFICATE](QCV-CONDITIONAL-VIABILITY-CERTIFICATE.md) (CONDITIONAL)
