# DFM-HINGE-HOLONOMY-WITNESS

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A telescoping product of pure-gauge frame factors is I_4; Lambda(1/2) Lambda(1/3) Lambda(-1/3) has 4x4 trace 16/3 (boost-plane trace 10/3) and the same trace after tetrad conjugation; the product of three telescoping conjugated factors around a declared 3-cell is I_4.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No simplicial complex, edge lengths or deficit angles are constructed, and the Bianchi check is a telescoping identity, not curvature on actual 3-cell boundaries.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.9-HINGE claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1136
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cartan_regge_hinge_holonomy_and_bianchi_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cartan_regge_hinge_holonomy_and_bianchi_witness` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/ravera_dfm.rs`

- file: [code/rust/src/qm/campaigns/ravera_dfm.rs](../../../code/rust/src/qm/campaigns/ravera_dfm.rs)
- sha256 (`bytes`): `4b865159ebe5a6ab9cd60382784354719fe46dc71f3346e817fdaae8162f646f`
- cited in: node.rust, record TFQ-1136
- check: `cd code/rust && cargo test -p theory_of_finite_qm test_cartan_regge_lorentz_tetrad_dfm_control`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_cartan_regge_lorentz_tetrad_dfm_control` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p theory_of_finite_qm test_cartan_regge_lorentz_tetrad_dfm_control` |

- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1136

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar9_cartan_regge_lorentz_tetrad_dfm` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1136_dfm_hinge_holonomy_witness.md`

- file: [dag/derivations/24_dressing_field/tfq_1136_dfm_hinge_holonomy_witness.md](../../../dag/derivations/24_dressing_field/tfq_1136_dfm_hinge_holonomy_witness.md)
- sha256 (`lf-normalised`): `ff0e189db10c9ff547624aad991cf287e15624dac911490b27a9462536647826`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1136
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-HINGE-HOLONOMY-WITNESS` `COMPUTED`: [DFM-DRESSED-AFFINE-TRANSPORT](DFM-DRESSED-AFFINE-TRANSPORT.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-DFM-REGGE-GRAVITY-FENCE` `GAP_NO_DERIVATION`: [DFM-REGGE-GRAVITY-FENCE](DFM-REGGE-GRAVITY-FENCE.md) (OPEN)
