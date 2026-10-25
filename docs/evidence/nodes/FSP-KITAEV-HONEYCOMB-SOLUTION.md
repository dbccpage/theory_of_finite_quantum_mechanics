# FSP-KITAEV-HONEYCOMB-SOLUTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On integer amplitudes indexed by a gauge bit and a matter bit, define W(v)(g,b)=sign(g)*v(g,b) and H(v)(g,b)=sign(g)*v(g,not b). Both square to the identity and commute. The two gauge-sector projectors commute with H and sum to the identity; the restricted hopping blocks are X and -X.

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

### Lean: `lean4/CampaignKitaevSectorBlock.lean`

- file: [lean4/CampaignKitaevSectorBlock.lean](../../../lean4/CampaignKitaevSectorBlock.lean)
- sha256 (`bytes`): `d9bd9073f6b684cfddfae8bc545d3002950a50d7bf1165a8e30091ed89503329`
- cited in: node.lean, receipt dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json (CampaignKitaevSectorBlock), record TFQ-1207
- replay: `verified`
  - receipt [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json) (module `CampaignKitaevSectorBlock`): recorded sha256 `d9bd9073f6b684cfddfae8bc545d3002950a50d7bf1165a8e30091ed89503329` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignKitaevSectorBlock`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignKitaevSectorBlock.State` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.State` |
| `CampaignKitaevSectorBlock.flux` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.flux` |
| `CampaignKitaevSectorBlock.flux_commutes_hopping` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.flux_commutes_hopping` |
| `CampaignKitaevSectorBlock.flux_involution` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignKitaevSectorBlock.flux_involution` |
| `CampaignKitaevSectorBlock.hopping` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.hopping` |
| `CampaignKitaevSectorBlock.hopping_involution` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignKitaevSectorBlock.hopping_involution` |
| `CampaignKitaevSectorBlock.project` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.project` |
| `CampaignKitaevSectorBlock.project_commutes_hopping` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignKitaevSectorBlock.project_commutes_hopping` |
| `CampaignKitaevSectorBlock.restricted_hopping` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.restricted_hopping` |
| `CampaignKitaevSectorBlock.sector_decomposition` | yes | yes | yes | propext | `#print axioms CampaignKitaevSectorBlock.sector_decomposition` |
| `CampaignKitaevSectorBlock.sectors_distinct` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.sectors_distinct` |
| `CampaignKitaevSectorBlock.sign` | yes | yes | yes | none | `#print axioms CampaignKitaevSectorBlock.sign` |

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
- sha256 (`lf-normalised`): `f560415332b14d38ef65230f61315565536c06e1a3fc9ba2cb58bfc8355ddd17`
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
- sha256 (`lf-normalised`): `c317032459f2e9c3331e7f3e1feb6abd5b4882810c8f4ee18bcf79d2f5e629f5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-MAJORANA-CLIFFORD-PARITY](FSP-MAJORANA-CLIFFORD-PARITY.md) (IMPORTED_ASSUMPTION), [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-LAUGHLIN-EXCHANGE-PHASE` `CONDITIONAL_ON_IMPORT`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)
