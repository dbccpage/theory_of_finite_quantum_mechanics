# DFM-TREE-CHANGE-GLZ-SYMANZIK-U

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the diamond graph, the 2x2 chord-coordinate matrix from a fixed tree T_0 to each of the 8 trees has determinant +1 or -1, and det(C_T diag(alpha) C_T^T) = U_G(alpha) = 247 for every tree at alpha = (2,3,5,7,11), with U_G(1,...,1) = 8.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 3 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Kirchhoff matrix-tree theorem for the general graph statement

## Bottleneck

The general claims (tree change acts by GL(b_1, Z); det L_T(alpha) = U_G(alpha) for every graph and positive alpha) are the classical matrix-tree theorem and are cited, not proved here.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.1-SYMANZIK claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1103

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar1_abelian_tree_dfm_and_symanzik_u` (python_symbol) | yes | yes | yes | - | - |
| `verify_pillar3_symanzik_two_forest_and_bphz` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1103_dfm_tree_change_glz_symanzik_u.md`

- file: [dag/derivations/24_dressing_field/tfq_1103_dfm_tree_change_glz_symanzik_u.md](../../../dag/derivations/24_dressing_field/tfq_1103_dfm_tree_change_glz_symanzik_u.md)
- sha256 (`lf-normalised`): `16f3dcb6c0f5e07c714de304c52de99e892c07ed87cde6f9a5967681618acdf3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1103
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-TREE-CHANGE-GLZ-SYMANZIK-U` `COMPUTED`: [DFM-ABELIAN-RETRACTION-DIAMOND](DFM-ABELIAN-RETRACTION-DIAMOND.md) (COMPUTATIONALLY_CHECKED), [DFM-TREE-CHANGE](DFM-TREE-CHANGE.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-DFM-SYMANZIK-QED-AE-FENCE` `GAP_NO_DERIVATION`: [DFM-SYMANZIK-QED-AE-FENCE](DFM-SYMANZIK-QED-AE-FENCE.md) (OPEN)
- `APP-R-DFM-TWO-FOREST-F0-DIAMOND` `COMPUTED`: [DFM-TWO-FOREST-F0-DIAMOND](DFM-TWO-FOREST-F0-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
