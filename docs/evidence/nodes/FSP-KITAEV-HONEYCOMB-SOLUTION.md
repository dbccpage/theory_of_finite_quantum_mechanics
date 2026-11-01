# FSP-KITAEV-HONEYCOMB-SOLUTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Kitaev (2006): in the four-Majorana representation of the honeycomb model, the plaquette fluxes W_p commute with H and with each other, and in each flux sector H is quadratic in the c Majoranas with a static Z2 gauge field (after projection to the physical subspace).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Kitaev honeycomb spin model and its Majorana representation (Kitaev 2006)

## Bottleneck

This is one exact gauge-controlled hopping block. No honeycomb lattice, all plaquette operators, physical gauge projection, global flux-sector sum or sign-free sampling theorem is constructed. Original target retained as an obligation: Kitaev (2006): in the four-Majorana representation of the honeycomb model, the plaquette fluxes W_p commute with H and with each other, and in each flux sector H is quadratic in the c Majoranas with a static Z2 gauge field (after projection to the physical subspace). Prior boundary: A sign-free sampling claim for this representation is not made or checked here; the gauge projection and flux-sector sum must be kept explicit.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-043 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/KitaevSectorBlock.lean`

- file: [lean4/KitaevSectorBlock.lean](../../../lean4/KitaevSectorBlock.lean)
- sha256 (`bytes`): `5de45b17a7ae6cf93a2455172086d10e846b1f2ea0ed9d69ea973f79daa6abcf`
- cited in: node.lean, receipt dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json (KitaevSectorBlock), receipt dag/research/pr_378_round2_replay.json (KitaevSectorBlock), record TFQ-1207
- replay: `verified`
  - receipt [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json) (module `KitaevSectorBlock`): recorded sha256 `5de45b17a7ae6cf93a2455172086d10e846b1f2ea0ed9d69ea973f79daa6abcf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_378_round2_replay.json](../../../dag/research/pr_378_round2_replay.json) (module `KitaevSectorBlock`): recorded sha256 `5de45b17a7ae6cf93a2455172086d10e846b1f2ea0ed9d69ea973f79daa6abcf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build KitaevSectorBlock`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `KitaevSectorBlock.State` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.State` |
| `KitaevSectorBlock.flux` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.flux` |
| `KitaevSectorBlock.flux_commutes_hopping` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.flux_commutes_hopping` |
| `KitaevSectorBlock.flux_involution` | yes | yes | yes | Quot.sound, propext | `#print axioms KitaevSectorBlock.flux_involution` |
| `KitaevSectorBlock.hopping` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.hopping` |
| `KitaevSectorBlock.hopping_involution` | yes | yes | yes | Quot.sound, propext | `#print axioms KitaevSectorBlock.hopping_involution` |
| `KitaevSectorBlock.project` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.project` |
| `KitaevSectorBlock.project_commutes_hopping` | yes | yes | yes | Quot.sound, propext | `#print axioms KitaevSectorBlock.project_commutes_hopping` |
| `KitaevSectorBlock.restricted_hopping` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.restricted_hopping` |
| `KitaevSectorBlock.sector_decomposition` | yes | yes | yes | propext | `#print axioms KitaevSectorBlock.sector_decomposition` |
| `KitaevSectorBlock.sectors_distinct` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.sectors_distinct` |
| `KitaevSectorBlock.sign` | yes | yes | yes | none | `#print axioms KitaevSectorBlock.sign` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-kitaev-honeycomb-solution.py`

- file: [checks/independent/fsp-kitaev-honeycomb-solution.py](../../../checks/independent/fsp-kitaev-honeycomb-solution.py)
- sha256 (`bytes`): `4c408cb7ee24109ba524c4bfa03b01b825b2e700e820a240821978590584478f`
- cited in: record TFQ-1207
- counts toward the grade: yes

### Python: `code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py`

- file: [code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py](../../../code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py)
- sha256 (`bytes`): `83c7a6bc2b6e24b75bbcd469a3d1c0fcd9ce88ea8fa6ee820a9bc2a554603eeb`
- cited in: record TFQ-1207
- counts toward the grade: yes

### Python: `code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py`

- file: [code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py](../../../code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py)
- sha256 (`bytes`): `26a6d1c85e7e8e1170c0e563369604cd0fdc10d44a203d847d33cbedc9b91571`
- cited in: record TFQ-1207
- check: `python -m pytest code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py::test_vortex_free_ground_state`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_vortex_free_ground_state` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py::test_vortex_free_ground_state` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md`

- file: [dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md](../../../dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md)
- sha256 (`lf-normalised`): `7e8eef9aa3ecb713b32490306bf2054d2ebe3fbbc728fc84882b8c5f1f68c3eb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1207
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-kitaev-honeycomb-solution.md`

- file: [dag/derivations/independent/fsp-kitaev-honeycomb-solution.md](../../../dag/derivations/independent/fsp-kitaev-honeycomb-solution.md)
- sha256 (`lf-normalised`): `7afef1c8863452e4a33ff959edf51fb2a4adcbaf6f5b67b18bd1d2c697bf1d23`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json`

- file: [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json)
- sha256 (`lf-normalised`): `ede952607daf57ff1891a402fcdb893fc8c306a96f70cc2be4ad113ae1b5a267`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-MAJORANA-CLIFFORD-PARITY](FSP-MAJORANA-CLIFFORD-PARITY.md) (IMPORTED_ASSUMPTION), [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-LAUGHLIN-EXCHANGE-PHASE` `CONDITIONAL_ON_IMPORT`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)
