# DFM-TREE-CHANGE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For any two dressings u and u prime, the change field C(v)=u prime(v)u(v) inverse intertwines the residual connections. In particular this describes two spanning-forest choices without commuting group elements.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Use the same multiplication convention in all three languages; distinguish edge residuals from conjugacy-invariant closed-loop observables.

## Source status

New theorem checked in Lean 4.33.1; axioms printed separately; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FiniteGraphDressing.lean`

- file: [lean4/FiniteGraphDressing.lean](../../../lean4/FiniteGraphDressing.lean)
- sha256 (`bytes`): `23bed260d85f626312bcebf0d1b6052711591450af1cad3a3300d744038e3e7d`
- cited in: node.lean, record TFQ-0399
- replay: `verified`
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `FiniteGraphDressing`): recorded sha256 `23bed260d85f626312bcebf0d1b6052711591450af1cad3a3300d744038e3e7d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteGraphDressing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `change_dressing` | yes | yes | yes | propext | `#print axioms change_dressing` |

- counts toward the grade: yes

### Rust: `dag/research/finite_graph_dressing.rs`

- file: [dag/research/finite_graph_dressing.rs](../../../dag/research/finite_graph_dressing.rs)
- sha256 (`bytes`): `e712f48dcd6dfc980b43b6c3962349ea2d22f92d4854548dcef60561b1705324`
- cited in: node.rust, node.source, record TFQ-0399

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `forest_dressing` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `dag/research/finite_graph_dressing.py`

- file: [dag/research/finite_graph_dressing.py](../../../dag/research/finite_graph_dressing.py)
- sha256 (`bytes`): `bc0c027d037cac345a2602fa0d6acb1446ac262328b868844c20994cce7479c6`
- cited in: node.source, record TFQ-0399
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_0399_dfm_tree_change.md`

- file: [dag/derivations/24_dressing_field/tfq_0399_dfm_tree_change.md](../../../dag/derivations/24_dressing_field/tfq_0399_dfm_tree_change.md)
- sha256 (`lf-normalised`): `075660d7fd2591335d28fa43c620f541ac56838207ad1b355ebf8e38903cf9b7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0399
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-DFM-TREE-CHANGE` `DERIVED_LEAN`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-DFM-HIERARCHICAL-BOREL` `DERIVED_LEAN`: [DFM-HIERARCHICAL-BOREL](DFM-HIERARCHICAL-BOREL.md) (PROVED_LEAN)
- `APP-R-DFM-SU3-TREE-DRESSING-DIAMOND` `COMPUTED`: [DFM-SU3-TREE-DRESSING-DIAMOND](DFM-SU3-TREE-DRESSING-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-TREE-CHANGE-GLZ-SYMANZIK-U` `COMPUTED`: [DFM-TREE-CHANGE-GLZ-SYMANZIK-U](DFM-TREE-CHANGE-GLZ-SYMANZIK-U.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-TREE-CHORD-COORDINATES` `DERIVED_LEAN`: [DFM-TREE-CHORD-COORDINATES](DFM-TREE-CHORD-COORDINATES.md) (PROVED_LEAN)
