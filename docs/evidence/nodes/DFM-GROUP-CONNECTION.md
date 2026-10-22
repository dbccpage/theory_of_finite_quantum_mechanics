# DFM-GROUP-CONNECTION

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite multigraph with oriented edge representatives carries labels in a supplied group G; reverse traversal carries the inverse label. This admits the group and connection rather than selecting them from primitive difference.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- finite multigraph
- supplied group G and group axioms

## Bottleneck

Keep the graph, group axioms, inverse-edge convention and multiplication order explicit.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `dag/research/finite_graph_dressing.py`

- file: [dag/research/finite_graph_dressing.py](../../../dag/research/finite_graph_dressing.py)
- sha256 (`bytes`): `bc0c027d037cac345a2602fa0d6acb1446ac262328b868844c20994cce7479c6`
- cited in: record TFQ-0397
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_0397_dfm_group_connection.md`

- file: [dag/derivations/24_dressing_field/tfq_0397_dfm_group_connection.md](../../../dag/derivations/24_dressing_field/tfq_0397_dfm_group_connection.md)
- sha256 (`lf-normalised`): `df4865f34200afa63bacecf4b1bba5d0a0dbbfb8c7ab59e83f90b61b7308354d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0397
- counts toward the grade: no

### Documents and data: `dag/research/hierarchical_nonabelian_dfm_finite_map.md`

- file: [dag/research/hierarchical_nonabelian_dfm_finite_map.md](../../../dag/research/hierarchical_nonabelian_dfm_finite_map.md)
- sha256 (`lf-normalised`): `2124e198921c1a9978f94866a6777e623ef8cee8a175fef1326be2b5eafe6cf8`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-GROUP-CONNECTION` `CONDITIONAL_ON_IMPORT`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (6):

- `APP-R-DFM-CARTAN-REGGE-TETRAD` `DERIVED_PROSE`: [DFM-CARTAN-REGGE-TETRAD](DFM-CARTAN-REGGE-TETRAD.md) (DEFINITION)
- `APP-R-DFM-CKM-BIPARTITE-REPHASING` `DERIVED_PROSE`: [DFM-CKM-BIPARTITE-REPHASING](DFM-CKM-BIPARTITE-REPHASING.md) (DEFINITION)
- `APP-R-DFM-ELECTROWEAK-DOUBLET-DRESSING` `DERIVED_PROSE`: [DFM-ELECTROWEAK-DOUBLET-DRESSING](DFM-ELECTROWEAK-DOUBLET-DRESSING.md) (DEFINITION)
- `APP-R-DFM-GENERAL-GRAPH-DRESSING` `DERIVED_LEAN`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN)
- `APP-R-DFM-LANDAU-GRIBOV-KLEIN-FOUR` `DERIVED_PROSE`: [DFM-LANDAU-GRIBOV-KLEIN-FOUR](DFM-LANDAU-GRIBOV-KLEIN-FOUR.md) (DEFINITION)
- `APP-R-DFM-PAGE-WOOTTERS-CLOCK-DRESSING` `DERIVED_PROSE`: [DFM-PAGE-WOOTTERS-CLOCK-DRESSING](DFM-PAGE-WOOTTERS-CLOCK-DRESSING.md) (DEFINITION)
