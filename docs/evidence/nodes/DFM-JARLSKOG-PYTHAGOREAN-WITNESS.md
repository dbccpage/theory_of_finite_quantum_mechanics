# DFM-JARLSKOG-PYTHAGOREAN-WITNESS

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the fixed 3x3 Gaussian-rational matrix with c_i = 3/5, s_i = 4/5 and e^{i delta} = i, the three rows have unit norm, rows 1 and 2 are orthogonal, and the plaquette imaginary parts are +-5184/78125, nonzero.

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

Full unitarity is not checked in Lean or Python (the external Rust asserts it); the instance is a chosen rational point, not measured CKM data.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.7-THREE-GEN claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1127
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `three_gen_ckm_substantial_jarlskog_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms three_gen_ckm_substantial_jarlskog_witness` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/ravera_dfm.rs`

- file: [code/rust/src/qm/campaigns/ravera_dfm.rs](../../../code/rust/src/qm/campaigns/ravera_dfm.rs)
- sha256 (`bytes`): `000828b04ba50dedc39a4bd6cbf36734e50e36bc80cf05bfe5cb8f5b229ac477`
- cited in: node.rust, record TFQ-1127
- check: `cd code/rust && cargo test -p theory_of_finite_qm test_ckm_jarlskog_bipartite_dfm_control`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_ckm_jarlskog_bipartite_dfm_control` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p theory_of_finite_qm test_ckm_jarlskog_bipartite_dfm_control` |

- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1127

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar7_ckm_jarlskog_bipartite_dfm` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1127_dfm_jarlskog_pythagorean_witness.md`

- file: [dag/derivations/24_dressing_field/tfq_1127_dfm_jarlskog_pythagorean_witness.md](../../../dag/derivations/24_dressing_field/tfq_1127_dfm_jarlskog_pythagorean_witness.md)
- sha256 (`lf-normalised`): `cef3fd2ebf072dc1ba7477e451844c0d4fe877b51804000d2e58687f25d2e558`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1127
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-JARLSKOG-PYTHAGOREAN-WITNESS` `COMPUTED`: [DFM-JARLSKOG-QUARTET-INVARIANCE](DFM-JARLSKOG-QUARTET-INVARIANCE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-DFM-CKM-PHYSICS-FENCE` `GAP_NO_DERIVATION`: [DFM-CKM-PHYSICS-FENCE](DFM-CKM-PHYSICS-FENCE.md) (OPEN)
