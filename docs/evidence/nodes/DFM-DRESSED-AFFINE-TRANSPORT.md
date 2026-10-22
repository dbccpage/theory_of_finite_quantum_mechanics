# DFM-DRESSED-AFFINE-TRANSPORT

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For invertible rational tetrads and Omega in SO+(1,3; Q), Gamma = e_sigma^{-1} Omega e_sigma' is unchanged under independent frame changes (L_sigma, L_sigma') and satisfies Gamma^T g_sigma Gamma = g_sigma'.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Exact 4x4 checks exist for two fixed tetrads, one boost-rotation frame change and Omega = Lambda(1/2), with the group law at beta = 1/3, 1/2; no Lean witness in dimension 4.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.9-TRANSPORT claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/qm/campaigns/ravera_dfm.rs`

- file: [code/rust/src/qm/campaigns/ravera_dfm.rs](../../../code/rust/src/qm/campaigns/ravera_dfm.rs)
- sha256 (`bytes`): `000828b04ba50dedc39a4bd6cbf36734e50e36bc80cf05bfe5cb8f5b229ac477`
- cited in: node.rust, record TFQ-1135
- check: `cd code/rust && cargo test -p theory_of_finite_qm test_cartan_regge_lorentz_tetrad_dfm_control`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_cartan_regge_lorentz_tetrad_dfm_control` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p theory_of_finite_qm test_cartan_regge_lorentz_tetrad_dfm_control` |
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1135

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar9_cartan_regge_lorentz_tetrad_dfm` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/tests/test_ravera_dfm.py`

- file: [code/python/tests/test_ravera_dfm.py](../../../code/python/tests/test_ravera_dfm.py)
- sha256 (`bytes`): `d7498af3763b81e4cd1f5d26e651cf2a0772c5561ff3334f344db0b88993b590`
- cited in: record TFQ-1135
- check: `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar9_cartan_regge_lorentz_tetrad_dfm`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_pillar9_cartan_regge_lorentz_tetrad_dfm` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar9_cartan_regge_lorentz_tetrad_dfm` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1135_dfm_dressed_affine_transport.md`

- file: [dag/derivations/24_dressing_field/tfq_1135_dfm_dressed_affine_transport.md](../../../dag/derivations/24_dressing_field/tfq_1135_dfm_dressed_affine_transport.md)
- sha256 (`lf-normalised`): `94be2734270fc4e841b4fe80ab3843bb8259ff8398690236e33429ecd0492c3a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1135
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-DRESSED-AFFINE-TRANSPORT` `DERIVED_PROSE`: [DFM-CARTAN-REGGE-TETRAD](DFM-CARTAN-REGGE-TETRAD.md) (DEFINITION), [DFM-BOOST-PLANE-LEAN](DFM-BOOST-PLANE-LEAN.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-DFM-HINGE-HOLONOMY-WITNESS` `COMPUTED`: [DFM-HINGE-HOLONOMY-WITNESS](DFM-HINGE-HOLONOMY-WITNESS.md) (COMPUTATIONALLY_CHECKED)
