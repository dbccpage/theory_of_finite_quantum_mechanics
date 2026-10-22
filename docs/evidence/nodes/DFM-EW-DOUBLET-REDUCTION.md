# DFM-EW-DOUBLET-REDUCTION

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For rational a, b, c, d, r with r != 0 and a^2 + b^2 + c^2 + d^2 = r^2, the four real component identities of u(Phi)^dagger Phi = (0, r) hold; for a real doublet (phi_+, phi_0) on the circle of radius r the real dressing matrix has determinant 1, is orthogonal and maps the doublet to (0, r).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unitarity and det = 1 of the complex u(Phi), the covariance u(g_L Phi) = g_L u(Phi), and SU(2)_L invariance of the dressed W are not in Lean or Python.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.6-DOUBLET claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1119
- replay: `none`
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ew_dfm_goldstone_elimination_on_sphere` | yes | yes | yes | - | `#print axioms ew_dfm_goldstone_elimination_on_sphere` |
| `ew_gaussian_4d_goldstone_elimination` | yes | yes | yes | - | `#print axioms ew_gaussian_4d_goldstone_elimination` |
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1119

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar6_electroweak_doublet_dfm` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1119_dfm_ew_doublet_reduction.md`

- file: [dag/derivations/24_dressing_field/tfq_1119_dfm_ew_doublet_reduction.md](../../../dag/derivations/24_dressing_field/tfq_1119_dfm_ew_doublet_reduction.md)
- sha256 (`lf-normalised`): `d250c63111fa554ff156a544f1576c9c3e5c68a4764e3490f3296549bfcc2958`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1119
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-EW-DOUBLET-REDUCTION` `DERIVED_LEAN`: [DFM-ELECTROWEAK-DOUBLET-DRESSING](DFM-ELECTROWEAK-DOUBLET-DRESSING.md) (DEFINITION)

Outgoing (1):

- `APP-R-DFM-ELECTROWEAK-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-ELECTROWEAK-CONTINUUM-FENCE](DFM-ELECTROWEAK-CONTINUUM-FENCE.md) (OPEN)
