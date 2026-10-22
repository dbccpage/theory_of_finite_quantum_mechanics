# MAJ-KITAEV-EDGE-INDEX-DISJOINT

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every bond (u, v) = (2j, 2j+1) with 1 \<= j \< L, u and v differ from 1 and from 2L.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Index-level statement only; operator commutation \[H, gamma_1\] = 0 is the exact instance MAJ-KITAEV-SWEETSPOT-EXACT.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-KITAEV-EDGE-INDEX claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaGinCore.lean`

- file: [papers/core/majorana/lean4/MajoranaGinCore.lean](../../../papers/core/majorana/lean4/MajoranaGinCore.lean)
- sha256 (`bytes`): `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102`
- cited in: node.lean, record TFQ-1168
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaGinCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `edge_mode_1_not_in_bulk` | yes | yes | yes | - | `#print axioms edge_mode_1_not_in_bulk` |
| `edge_mode_2L_not_in_bulk` | yes | yes | yes | - | `#print axioms edge_mode_2L_not_in_bulk` |
| `is_bulk_kitaev_bond` | yes | yes | yes | - | `#print axioms is_bulk_kitaev_bond` |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py`

- file: [papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py](../../../papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py)
- sha256 (`bytes`): `613eb90331749cead532af34aa06a1d61ff5c01a8cc6fd4bdce4bdb9923f7e32`
- cited in: record TFQ-1168
- check: `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_kitaev_sweet_spot_boundary_isolation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_kitaev_sweet_spot_boundary_isolation` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_kitaev_sweet_spot_boundary_isolation` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md`

- file: [dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md](../../../dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md)
- sha256 (`lf-normalised`): `64f76908cd75ea563e3c0998f55144b2610bd5a10a2ff234df7058ebfd09d013`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1168
- counts toward the grade: no

### Documents and data: `papers/core/majorana/lean4/axiom_report.txt`

- file: [papers/core/majorana/lean4/axiom_report.txt](../../../papers/core/majorana/lean4/axiom_report.txt)
- sha256 (`lf-normalised`): `ec4465011fdd2b18f2c9df263004e9050f8c394dece1841835ff0bcd1e00df79`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-KITAEV-EDGE-INDEX-DISJOINT` `DERIVED_LEAN`: [MAJ-IMPORT-KITAEV-CHAIN](MAJ-IMPORT-KITAEV-CHAIN.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

