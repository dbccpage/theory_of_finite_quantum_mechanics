# DFM-CLIFFORD-WARD-TAKAHASHI

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In M_4(Q(i)), S_F^{-1}(p+q) - S_F^{-1}(p) = qslash, hence S_F(p+q) qslash S_F(p) = S_F(p) - S_F(p+q) at every rational (p, q, m) with both propagators non-singular.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The identity is checked by exact arithmetic only at p = (5,1,2,-1), q = (2,-1,1,3), m = 2 together with the Clifford relations of the Dirac basis; no Lean witness.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.4-WT claims COMPUTATIONALLY_CHECKED; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1113

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar4_dressed_dirac_and_ward_takahashi` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1113_dfm_clifford_ward_takahashi.md`

- file: [dag/derivations/24_dressing_field/tfq_1113_dfm_clifford_ward_takahashi.md](../../../dag/derivations/24_dressing_field/tfq_1113_dfm_clifford_ward_takahashi.md)
- sha256 (`lf-normalised`): `995ecad27b30f224869341703f78caf9d1f7583cfe73e882bb6da2fbde7ae606`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1113
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CLIFFORD-WARD-TAKAHASHI` `DERIVED_PROSE`: [DFM-DRESSED-DIRAC-PROPAGATOR](DFM-DRESSED-DIRAC-PROPAGATOR.md) (DEFINITION)

Outgoing (1):

- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-Z1-Z2-COUNTERTERM-FENCE](DFM-Z1-Z2-COUNTERTERM-FENCE.md) (OPEN)
