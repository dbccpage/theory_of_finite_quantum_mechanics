# DFM-DRESSED-CORRELATOR-DIAMOND

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the diamond graph with five fixed unit Gaussian-rational edge phases, one unit vertex gauge and one-component Q(i) vertex fields, the bare product conj(psi_3) psi_1 changes under the gauge while the tree-dressed product is unchanged for each of the 8 spanning trees.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Four-component spinors with gamma^0, the tree-change holonomy factor and arbitrary graphs are not checked; the general U(1) case is a specialization of TFQ-0398 and TFQ-0399.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.4-CORRELATOR claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1112

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar4_dressed_dirac_and_ward_takahashi` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_ravera_dfm.py`

- file: [code/python/tests/test_ravera_dfm.py](../../../code/python/tests/test_ravera_dfm.py)
- sha256 (`bytes`): `d7498af3763b81e4cd1f5d26e651cf2a0772c5561ff3334f344db0b88993b590`
- cited in: record TFQ-1112
- check: `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar4_dressed_dirac_and_ward_takahashi`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_pillar4_dressed_dirac_and_ward_takahashi` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar4_dressed_dirac_and_ward_takahashi` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1112_dfm_dressed_correlator_diamond.md`

- file: [dag/derivations/24_dressing_field/tfq_1112_dfm_dressed_correlator_diamond.md](../../../dag/derivations/24_dressing_field/tfq_1112_dfm_dressed_correlator_diamond.md)
- sha256 (`lf-normalised`): `b24df26ade6c74e2a2d6763cdbe7ab2434aa0132ef774e1692ba2205d8c15fd1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1112
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-DRESSED-CORRELATOR-DIAMOND` `COMPUTED`: [DFM-DRESSED-DIRAC-PROPAGATOR](DFM-DRESSED-DIRAC-PROPAGATOR.md) (DEFINITION), [DFM-ABELIAN-RETRACTION-DIAMOND](DFM-ABELIAN-RETRACTION-DIAMOND.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

