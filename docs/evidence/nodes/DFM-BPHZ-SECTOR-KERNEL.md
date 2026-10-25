# DFM-BPHZ-SECTOR-KERNEL

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For K(z; lambda) = (1 + z lambda) / (lambda (1 + lambda)) at z = 3/5, the four-term sum K1(z)K2(z) - K1(z)K2(0) - K1(0)K2(z) + K1(0)K2(0) equals (z/(1+lambda_1))(z/(1+lambda_2)) at 9 rational (lambda_1, lambda_2) pairs, with formal value z^2 = 9/25 at (0, 0).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 2 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

The identity is distributivity on one declared toy kernel; it is not Zimmermann's forest formula on a Feynman integrand and fixes no renormalization scheme.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.3-BPHZ claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1109

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar3_symanzik_two_forest_and_bphz` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1109_dfm_bphz_sector_kernel.md`

- file: [dag/derivations/24_dressing_field/tfq_1109_dfm_bphz_sector_kernel.md](../../../dag/derivations/24_dressing_field/tfq_1109_dfm_bphz_sector_kernel.md)
- sha256 (`lf-normalised`): `b96a50078a1a4fd53c953ec332afdb23f874038d56a8686cd4e99062587cf44a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1109
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-BPHZ-SECTOR-KERNEL` `COMPUTED`: [DFM-TREE-MOMENTUM-ROUTING](DFM-TREE-MOMENTUM-ROUTING.md) (DEFINITION)

Outgoing (1):

- `APP-R-DFM-BPHZ-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-BPHZ-CONTINUUM-FENCE](DFM-BPHZ-CONTINUUM-FENCE.md) (OPEN)
