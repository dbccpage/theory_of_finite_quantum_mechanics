# DFM-BOREL-TWO-STAGE-DIAMOND

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the diamond graph with one fixed tree, a pure-gauge B_2(Q) connection built from one rational vertex map is dressed to the identity on all 5 edges, and a connection with one chord multiplied by \[\[2,1\],\[0,3\]\] is dressed to the identity on tree edges and to a non-identity chord; stage-1 fields lie in N, stage-1 tree links are diagonal, and stage 2 reproduces the one-shot dressing.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Rooted-tree two-stage identities and the specified incidence operators are recorded at TFQ-0400. A 2-plaquette prism, and a criterion for a graph that does not supply a parent and a depth, stay outside TFQ-0400 and outside TFQ-0016.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.2-TWO-STAGE claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, record TFQ-1106
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `spanning_tree_nonabelian_mat2_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms spanning_tree_nonabelian_mat2_factorization` |

- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: node.source, record TFQ-1106

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar2_nonabelian_borel_two_stage_dfm` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_ravera_dfm.py`

- file: [code/python/tests/test_ravera_dfm.py](../../../code/python/tests/test_ravera_dfm.py)
- sha256 (`bytes`): `d7498af3763b81e4cd1f5d26e651cf2a0772c5561ff3334f344db0b88993b590`
- cited in: record TFQ-1106
- check: `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar2_nonabelian_borel_two_stage_dfm`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_pillar2_nonabelian_borel_two_stage_dfm` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_ravera_dfm.py::test_pillar2_nonabelian_borel_two_stage_dfm` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1106_dfm_borel_two_stage_diamond.md`

- file: [dag/derivations/24_dressing_field/tfq_1106_dfm_borel_two_stage_diamond.md](../../../dag/derivations/24_dressing_field/tfq_1106_dfm_borel_two_stage_diamond.md)
- sha256 (`lf-normalised`): `bbfb9d3e6f9972c5dcd20dc6136c3f748f18d96dfb31381da102b802b3cd4f07`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1106
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-BOREL-TWO-STAGE-DIAMOND` `COMPUTED`: [DFM-BOREL-LEVI-FACTORIZATION](DFM-BOREL-LEVI-FACTORIZATION.md) (DEFINITION), [DFM-HIERARCHICAL-BOREL](DFM-HIERARCHICAL-BOREL.md) (PROVED_LEAN)

Outgoing (0):

