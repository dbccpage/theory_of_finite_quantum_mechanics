# DFM-Z1-Z2-COUNTERTERM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The contraction q_mu I_Lambda^mu = I_Sigma(p) - I_Sigma(p+q) of the one-loop vertex integrand and the resulting counterterm equality Z_1/Z_2 = 1 are not computed by the cited replay.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- gauge-invariant BPHZ subtraction scheme
- continuum loop integration

## Bottleneck

Check the integrand contraction in M_4(Q(i)) at stated loop momenta and keep Z_1 = Z_2 conditional on a declared gauge-invariant subtraction scheme.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.4-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1114

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar4_dressed_dirac_and_ward_takahashi` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md](../../../dag/derivations/24_dressing_field/tfq_1114_dfm_z1_z2_counterterm_fence.md)
- sha256 (`lf-normalised`): `d89b48b5b6a5d7e6c24e87b83b14595a315f2f3434148f28de08114271e4e5d3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1114
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-CLIFFORD-WARD-TAKAHASHI](DFM-CLIFFORD-WARD-TAKAHASHI.md) (PROVED_PROSE), [DFM-BPHZ-CONTINUUM-FENCE](DFM-BPHZ-CONTINUUM-FENCE.md) (OPEN), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (0):

