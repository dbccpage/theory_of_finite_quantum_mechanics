# MAJ-KITAEV-EDGE-INDEX-DISJOINT

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every bond (u, v) = (2j, 2j+1) with 1 \<= j \< L, u and v differ from 1 and from 2L.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaGinCore`): recorded sha256 `33ca2d4ec9a96398a74c96207caf0aa46d91b15ff4f10d245f394440a5102102` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaGinCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `edge_mode_1_not_in_bulk` | yes | yes | yes | Quot.sound, propext | `#print axioms edge_mode_1_not_in_bulk` |
| `edge_mode_2L_not_in_bulk` | yes | yes | yes | Quot.sound, propext | `#print axioms edge_mode_2L_not_in_bulk` |
| `is_bulk_kitaev_bond` | yes | yes | yes | none | `#print axioms is_bulk_kitaev_bond` |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1168
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_kitaev_sweet_spot_boundary_isolation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_kitaev_sweet_spot_boundary_isolation` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_kitaev_sweet_spot_boundary_isolation` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md`

- file: [dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md](../../../dag/derivations/28_majorana/tfq_1168_maj_kitaev_edge_index_disjoint.md)
- sha256 (`lf-normalised`): `85fb78e9560c162d822bdf7ce5bf37fcc11367592caf5344d77e466f6cc77544`
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
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-KITAEV-EDGE-INDEX-DISJOINT` `DERIVED_LEAN`: [MAJ-IMPORT-KITAEV-CHAIN](MAJ-IMPORT-KITAEV-CHAIN.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

