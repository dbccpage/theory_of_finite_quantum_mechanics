# MAJ-PARITY-SECTOR-SPLIT-EXACT

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the exact 2-mode Fock carrier the parity operator restricts to 2-dimensional even and odd sectors, and restricting gamma_1 to a sector is refused because it mixes sectors.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed 2-mode instance; the paper code's ParityAlgebraModel check is floating point.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-PARITY-SECTOR-EXACT claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/majorana_fock_algebra.rs`

- file: [code/rust/src/majorana/majorana_fock_algebra.rs](../../../code/rust/src/majorana/majorana_fock_algebra.rs)
- sha256 (`bytes`): `5da71d117706660f313b3ab162cf2155ed9b852878651667e066d564a5ba9602`
- cited in: node.rust, record TFQ-1174
- check: `cd code/rust && cargo test -p tfqm_majorana test_sector_restriction_and_refusals`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_sector_restriction_and_refusals` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana test_sector_restriction_and_refusals` |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_gf2_trichotomy.py`

- file: [code/python/src/majorana/test_gf2_trichotomy.py](../../../code/python/src/majorana/test_gf2_trichotomy.py)
- sha256 (`bytes`): `ef02fedf569c136afcde5946b0a5b597fa108fd48c981f60494aa3d9f517ec75`
- cited in: record TFQ-1174
- check: `python -m pytest code/python/src/majorana/test_gf2_trichotomy.py::test_parity_observable_algebra_and_sector_splitting`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_parity_observable_algebra_and_sector_splitting` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_gf2_trichotomy.py::test_parity_observable_algebra_and_sector_splitting` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md`

- file: [dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md](../../../dag/derivations/28_majorana/tfq_1174_maj_parity_sector_split_exact.md)
- sha256 (`lf-normalised`): `746eee1c7c375aec1d5a869661db7fdaa98c55249d99ae539c9d8eeb66d463d5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1174
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-PARITY-SECTOR-SPLIT-EXACT` `COMPUTED`: [MAJ-PARITY-OBSERVABLE-FENCE](MAJ-PARITY-OBSERVABLE-FENCE.md) (DEFINITION)

Outgoing (0):

