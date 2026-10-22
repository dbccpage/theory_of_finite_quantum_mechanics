# DFM-CKM-CYCLE-COUNT

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every rational n, n^2 - (2n - 1) = (n - 1)^2, and (n - 1)(n - 2)/2 equals 0, 0, 1, 3 at n = 1, 2, 3, 4.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

That a spanning tree of K_{n,n} has 2n - 1 edges and that unitarity reduces the (n-1)^2 cycle phases to (n-1)(n-2)/2 CP phases are cited, not formalized.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.7-COUNT claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1124
- replay: `none`
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ckm_bipartite_dfm_parameter_count` | yes | yes | yes | - | `#print axioms ckm_bipartite_dfm_parameter_count` |
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: record TFQ-1124

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar7_ckm_jarlskog_bipartite_dfm` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1124_dfm_ckm_cycle_count.md`

- file: [dag/derivations/24_dressing_field/tfq_1124_dfm_ckm_cycle_count.md](../../../dag/derivations/24_dressing_field/tfq_1124_dfm_ckm_cycle_count.md)
- sha256 (`lf-normalised`): `d4f7b94289970747639b6c8b111e0dc4d8739351c78e816df6d85c647e664a01`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1124
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CKM-CYCLE-COUNT` `DERIVED_LEAN`: [DFM-CKM-BIPARTITE-REPHASING](DFM-CKM-BIPARTITE-REPHASING.md) (DEFINITION)

Outgoing (0):

