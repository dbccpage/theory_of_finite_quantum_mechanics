# FSP-FRACTON-MOBILITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the X-cube model isolated fractons are immobile, fracton dipoles move within planes (planons) and lineons move only along lattice axes.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- X-cube excitation mobility (literature)

## Bottleneck

Imported literature result; no local stabilizer or excitation-mobility proof exists, and mobility constraints do not by themselves establish fermion-sign freedom. Narrowed in lean4/CampaignFspFractonMobility.lean and checks/independent/fsp-fracton-mobility.py while keeping status IMPORTED_ASSUMPTION to: (1) single-edge Pauli Z_e flips all 4 adjacent cubes (weight 4), so a single-edge hop from an isolated 1-cube fracton produces syndrome weight 3 (creating 2 extra fractons, Delta_E = 4J \> 0) and no 1- or 2-edge Z operator can move an isolated fracton without creating additional excitations; (2) rectangular dual membranes excite only the 4 corner cubes while foliation-leaf separation penalty Delta_S = kappa * R grows strictly with R; (3) adjacent 2-cube fracton dipoles move freely in perpendicular 2D planes (Delta_E = 0, 2D planons); (4) single-edge Pauli X_e excites a pair of 1D lineons of vertex weight 2 that move along collinear strings with Delta_E = 0, whereas a 90-degree corner turn leaves an immobile weight-2 orthogonal lineon defect at the corner vertex (raising total vertex weight from 4 to 6, Delta_E = 2 J_A \> 0); and (5) explicit scope fences for 2D planon braiding, 1D T-junction 3-step exchange, and non-abelian 2-gauge hinge negative trace.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-054 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspFractonMobility.lean`

- file: [lean4/CampaignFspFractonMobility.lean](../../../lean4/CampaignFspFractonMobility.lean)
- sha256 (`bytes`): `12f968fba7e557982f04d6c55df24792e2081b6002ff17cf90d5d22b5c745faa`
- cited in: node.lean, receipt dag/research/campaign_fsp-fracton-mobility_lean_replay.json (CampaignFspFractonMobility), record TFQ-1218
- replay: `verified`
  - receipt [dag/research/campaign_fsp-fracton-mobility_lean_replay.json](../../../dag/research/campaign_fsp-fracton-mobility_lean_replay.json) (module `CampaignFspFractonMobility`): recorded sha256 `12f968fba7e557982f04d6c55df24792e2081b6002ff17cf90d5d22b5c745faa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspFractonMobility`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspFractonMobility.lineon_tjunction_three_step_exchange_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.lineon_tjunction_three_step_exchange_fence` |
| `CampaignFspFractonMobility.mobility_constraints_do_not_imply_fermion_sign_freedom_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.mobility_constraints_do_not_imply_fermion_sign_freedom_fence` |
| `CampaignFspFractonMobility.planon_dipole_2d_braiding_obstruction_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.planon_dipole_2d_braiding_obstruction_fence` |
| `CampaignFspFractonMobility.xcube_fracton_dipole_is_2d_planon` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_fracton_dipole_is_2d_planon` |
| `CampaignFspFractonMobility.xcube_isolated_fracton_hop_creates_two_extra_fractons` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_isolated_fracton_hop_creates_two_extra_fractons` |
| `CampaignFspFractonMobility.xcube_lineon_collinear_string_preserves_weight` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_lineon_collinear_string_preserves_weight` |
| `CampaignFspFractonMobility.xcube_lineon_corner_turn_creates_immobile_vertex_defect` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_lineon_corner_turn_creates_immobile_vertex_defect` |
| `CampaignFspFractonMobility.xcube_rectangular_membrane_corner_quadrupole_conservation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_rectangular_membrane_corner_quadrupole_conservation` |
| `CampaignFspFractonMobility.xcube_single_edge_pauli_x_excites_lineon_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_single_edge_pauli_x_excites_lineon_pair` |
| `CampaignFspFractonMobility.xcube_single_edge_pauli_z_excites_four_cubes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFractonMobility.xcube_single_edge_pauli_z_excites_four_cubes` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-fracton-mobility.py`

- file: [checks/independent/fsp-fracton-mobility.py](../../../checks/independent/fsp-fracton-mobility.py)
- sha256 (`bytes`): `e07bb5a8404ea6aa38cc297b8bc93b70c7f0cef55f4aef9e35cf6860539b51e6`
- cited in: record TFQ-1218

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/foliated_fracton_2gauge_defects.py`

- file: [code/python/src/fsp/foliated_fracton_2gauge_defects.py](../../../code/python/src/fsp/foliated_fracton_2gauge_defects.py)
- sha256 (`bytes`): `6c34ac89c96de95d234b1bbb9dbfeb98bd3ecae041f6163ed7e72addbb2aca66`
- cited in: record TFQ-1218

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FoliatedFractonEngine` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md`

- file: [dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md](../../../dag/derivations/26_fsp/tfq_1218_fsp_fracton_mobility.md)
- sha256 (`lf-normalised`): `9c6ed0e0a0111d6bf9c9fc55fb60a90f9077e5c0b03130557e82b58d157c10c1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1218
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-fracton-mobility.md`

- file: [dag/derivations/independent/fsp-fracton-mobility.md](../../../dag/derivations/independent/fsp-fracton-mobility.md)
- sha256 (`lf-normalised`): `57c8381893f189fafd2a30840f43f9eda7786a2f5f647297a2e653dd97c93807`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fracton-mobility_independent.json`

- file: [dag/research/campaign_fsp-fracton-mobility_independent.json](../../../dag/research/campaign_fsp-fracton-mobility_independent.json)
- sha256 (`lf-normalised`): `90d88505294edb371508641c1d8112c29bf771fd3d16c8c9ef9d220fdad02d83`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fracton-mobility_lean_mutation.json`

- file: [dag/research/campaign_fsp-fracton-mobility_lean_mutation.json](../../../dag/research/campaign_fsp-fracton-mobility_lean_mutation.json)
- sha256 (`lf-normalised`): `413874efdcfb506ed1726a841ddf2ba09287900e96232d74e17c4b9f4a976612`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fracton-mobility_lean_replay.json`

- file: [dag/research/campaign_fsp-fracton-mobility_lean_replay.json](../../../dag/research/campaign_fsp-fracton-mobility_lean_replay.json)
- sha256 (`lf-normalised`): `efbfe35d13872932503a1f7c1dcb62c39f8dfb19e844ba17b711cecd6549c36f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-FRACTON-MOBILITY` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-HINGE-LINEON-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-HINGE-LINEON-SIGN-CLAIM](FSP-HINGE-LINEON-SIGN-CLAIM.md) (OPEN)
