# DFM-SM-ANOMALY-NC-THREE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With Y_Q = 1/6, Y_u = 2/3, Y_d = -1/3, Y_L = -1/2, Y_e = -1 and rational N_c: N_c(2Y_Q - Y_u - Y_d) = 0, the gravitational trace is 0, N_c Y_Q + Y_L = (N_c - 3)/6 and the cubic trace is (3 - N_c)/4, so each of the last two vanishes iff N_c = 3.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

These are polynomial identities over Q, not triangle-diagram anomaly computations; the dossier prints the cubic trace as (3/4)(3 - N_c) and the change log as 6 A_grav = 6(N_c - 3), both inconsistent with Lean, which is retained.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.6-ANOMALY claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1121
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1` |
| `sm_anomaly_polynomials_general_nc` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sm_anomaly_polynomials_general_nc` |
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: record TFQ-1121

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar6_electroweak_doublet_dfm` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1121_dfm_sm_anomaly_nc_three.md`

- file: [dag/derivations/24_dressing_field/tfq_1121_dfm_sm_anomaly_nc_three.md](../../../dag/derivations/24_dressing_field/tfq_1121_dfm_sm_anomaly_nc_three.md)
- sha256 (`lf-normalised`): `c938aac611f6f1372630868c620e8417f270e903097fcfa4d0ec83143cd975e1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1121
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-SM-ANOMALY-NC-THREE` `DERIVED_LEAN`: [DFM-ELECTROWEAK-DOUBLET-DRESSING](DFM-ELECTROWEAK-DOUBLET-DRESSING.md) (DEFINITION)

Outgoing (0):

