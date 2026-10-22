# DFM-CLOCK-DRESSING-INTERTWINER

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If U_S is unitary with U_S^N = I_d, then D^dagger W D = S_C tensor I_d, and D^dagger sends each history state sum_t |t\> tensor U_S^t psi_0 in ker(I - W) to (sum_t |t\>) tensor psi_0.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Exact checks exist only for N = 4, d = 2, U_S = \[\[0,-1\],\[1,0\]\] and psi_0 = (3/5, 4/5); no Lean witness.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.5-INTERTWINER claims COMPUTATIONALLY_CHECKED; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1116

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar5_page_wootters_clock_dressing` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/tests/test_ravera_dfm.py`

- file: [code/python/tests/test_ravera_dfm.py](../../../code/python/tests/test_ravera_dfm.py)
- sha256 (`bytes`): `d7498af3763b81e4cd1f5d26e651cf2a0772c5561ff3334f344db0b88993b590`
- cited in: record TFQ-1116
- check: `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar5_page_wootters_clock_dressing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_pillar5_page_wootters_clock_dressing` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar5_page_wootters_clock_dressing` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1116_dfm_clock_dressing_intertwiner.md`

- file: [dag/derivations/24_dressing_field/tfq_1116_dfm_clock_dressing_intertwiner.md](../../../dag/derivations/24_dressing_field/tfq_1116_dfm_clock_dressing_intertwiner.md)
- sha256 (`lf-normalised`): `2cc3960e9fa7799e90fc7ba8eca0a045c63d2ce61c1796e2cacbfa995c02c8f7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1116
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CLOCK-DRESSING-INTERTWINER` `DERIVED_PROSE`: [DFM-PAGE-WOOTTERS-CLOCK-DRESSING](DFM-PAGE-WOOTTERS-CLOCK-DRESSING.md) (DEFINITION)

Outgoing (1):

- `APP-R-DFM-RELATIONAL-TIME-FENCE` `GAP_NO_DERIVATION`: [DFM-RELATIONAL-TIME-FENCE](DFM-RELATIONAL-TIME-FENCE.md) (OPEN)
