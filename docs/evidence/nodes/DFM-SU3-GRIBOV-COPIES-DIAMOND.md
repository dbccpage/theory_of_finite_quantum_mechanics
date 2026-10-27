# DFM-SU3-GRIBOV-COPIES-DIAMOND

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the diamond graph, the 64 anchored maps V -\> K_4 applied to the trivial connection give 64 configurations (63 nontrivial) with Hermitian links, hence zero discrete Landau divergence; some link has trace -1 and Tr(U (H^(23))^2) = -2 versus +2 at the identity; dressing along one fixed tree sends all 64 to the trivial configuration.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The collapse holds because every copy is pure gauge; the check does not compare dressing with Landau gauge on configurations with nonzero curvature.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.8-GRIBOV claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1130
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `su3_diagonal_klein_four_landau_gribov_copies` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms su3_diagonal_klein_four_landau_gribov_copies` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/ravera_dfm.rs`

- file: [code/rust/src/qm/campaigns/ravera_dfm.rs](../../../code/rust/src/qm/campaigns/ravera_dfm.rs)
- sha256 (`bytes`): `000828b04ba50dedc39a4bd6cbf36734e50e36bc80cf05bfe5cb8f5b229ac477`
- cited in: node.rust, record TFQ-1130
- check: `cd code/rust && cargo test -p theory_of_finite_qm test_su3_spanning_tree_vs_landau_gribov_control`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_su3_spanning_tree_vs_landau_gribov_control` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p theory_of_finite_qm test_su3_spanning_tree_vs_landau_gribov_control` |

- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1130

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar8_su3_spanning_tree_vs_landau_gribov` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_ravera_dfm.py`

- file: [code/python/tests/test_ravera_dfm.py](../../../code/python/tests/test_ravera_dfm.py)
- sha256 (`bytes`): `d7498af3763b81e4cd1f5d26e651cf2a0772c5561ff3334f344db0b88993b590`
- cited in: record TFQ-1130
- check: `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar8_su3_spanning_tree_vs_landau_gribov`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_pillar8_su3_spanning_tree_vs_landau_gribov` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar8_su3_spanning_tree_vs_landau_gribov` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1130_dfm_su3_gribov_copies_diamond.md`

- file: [dag/derivations/24_dressing_field/tfq_1130_dfm_su3_gribov_copies_diamond.md](../../../dag/derivations/24_dressing_field/tfq_1130_dfm_su3_gribov_copies_diamond.md)
- sha256 (`lf-normalised`): `f93bfd9df958184049a19d5d15915d9d13cd09f45957627ce3ed53753eb3e356`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1130
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-SU3-GRIBOV-COPIES-DIAMOND` `COMPUTED`: [DFM-LANDAU-GRIBOV-KLEIN-FOUR](DFM-LANDAU-GRIBOV-KLEIN-FOUR.md) (DEFINITION), [DFM-SU3-TREE-DRESSING-DIAMOND](DFM-SU3-TREE-DRESSING-DIAMOND.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `APP-R-DFM-GRIBOV-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-GRIBOV-CONTINUUM-FENCE](DFM-GRIBOV-CONTINUUM-FENCE.md) (OPEN)
