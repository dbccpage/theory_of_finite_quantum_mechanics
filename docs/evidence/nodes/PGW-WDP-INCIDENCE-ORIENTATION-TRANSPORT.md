# PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the one triangle with vertices 0, 1, 2, swapping Genesis edge slots (01, 02, 12) into WDP slots (01, 12, 02) is an involution; the admitted face column (1, -1, 1) becomes (1, 1, -1), matching triD1Row, and negating the 02 component sends that triple to (1, 1, 1). The swapped column has vertex boundary 0 at each vertex, triD1 of triD0 is 0 for every rational vertex triple, and triD1 of the swapped face row is 3.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Neither file states a general transport of window quantities, and monograph invariance under reorientation stays open. boundary_boundary_filled is a chain-level fact in the incidence edge order (01, 02, 12); the incidence construction (TFQ-0460) does not derive the WDP window from Genesis admission (TFQ-0344); the Python orientation test stays inside the WDP convention. The vertex cycle of the swapped face column is separate from triD1 of that row, which equals 3. A declared map for a general cochain, and a theorem that d0 and d1 of the whole WDP window are the transposes of the Genesis boundary maps, stay open.

## Source status

006_oewdp lean4/GenesisIncidence.lean (boundary order 01,02,12) vs WDP monograph §4.7 orientation convention; transport owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpIncidenceOrientationTransport.lean`

- file: [lean4/CampaignPgwWdpIncidenceOrientationTransport.lean](../../../lean4/CampaignPgwWdpIncidenceOrientationTransport.lean)
- sha256 (`bytes`): `11af3b7cdcea7ff3ab3e9ad6b506163824fe4a4c590b0a0babb03e7725fed794`
- cited in: node.lean, node.source, receipt dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json (CampaignPgwWdpIncidenceOrientationTransport), record TFQ-0543
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json](../../../dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json) (module `CampaignPgwWdpIncidenceOrientationTransport`): recorded sha256 `11af3b7cdcea7ff3ab3e9ad6b506163824fe4a4c590b0a0babb03e7725fed794` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpIncidenceOrientationTransport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwInc_d1_d0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwInc_d1_d0` |
| `pgwInc_dot_matches_order` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwInc_dot_matches_order` |
| `pgwInc_face_cyclic` | yes | yes | yes | propext | `#print axioms pgwInc_face_cyclic` |
| `pgwInc_face_is_row` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwInc_face_is_row` |
| `pgwInc_face_swapped` | yes | yes | yes | propext | `#print axioms pgwInc_face_swapped` |
| `pgwInc_face_tri` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwInc_face_tri` |
| `pgwInc_int_d1_d0` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwInc_int_d1_d0` |
| `pgwInc_rat_telescope` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwInc_rat_telescope` |
| `pgwInc_row` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwInc_row` |
| `pgwInc_swap_involutive` | yes | yes | yes | none | `#print axioms pgwInc_swap_involutive` |
| `pgwInc_swapped_coord_is_tri` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwInc_swapped_coord_is_tri` |
| `pgwInc_transported_cycle` | yes | yes | yes | propext | `#print axioms pgwInc_transported_cycle` |
- counts toward the grade: yes

### Lean: `lean4/Imported/OeWdp/GenesisIncidence.lean`

- file: [lean4/Imported/OeWdp/GenesisIncidence.lean](../../../lean4/Imported/OeWdp/GenesisIncidence.lean)
- sha256 (`bytes`): `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9`
- cited in: node.lean, node.source, record TFQ-0543
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.OeWdp.GenesisIncidence`): recorded sha256 `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeWdp/GenesisIncidence.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `boundary_boundary_filled` | yes | yes | yes | module-level | `#print axioms boundary_boundary_filled` |
- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, node.source, record TFQ-0543
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `triD1` | yes | yes | yes | module-level | `#print axioms triD1` |
- counts toward the grade: yes

### Python: `checks/independent/pgw-wdp-incidence-orientation-transport.py`

- file: [checks/independent/pgw-wdp-incidence-orientation-transport.py](../../../checks/independent/pgw-wdp-incidence-orientation-transport.py)
- sha256 (`bytes`): `b0fdf0d2e634bacb58af36135fe6803c2fc8abc13ba67646627b6cc18e366531`
- cited in: record TFQ-0543

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md`

- file: [dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md](../../../dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md)
- sha256 (`lf-normalised`): `b75a2abb113977b04d0cf23ce1e2857eddd19504e5422bc3087828b544e33727`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0543
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md`

- file: [dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md](../../../dag/derivations/independent/pgw-wdp-incidence-orientation-transport.md)
- sha256 (`lf-normalised`): `80b68e665ec5e8d08cf83a5e374432fb987635321661d30637062d0636e95155`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json](../../../dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json)
- sha256 (`lf-normalised`): `619976a3f85936100239dbc2c1735cee4d8f1ec4ec109ce7fbe3ef63a30155e7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature`

## Absences recorded by the TFQ records

- TFQ-0543 rust: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window

## Routes

Incoming (1):

- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-INCIDENCE-CONSTRUCTION-BETTI](PGW-INCIDENCE-CONSTRUCTION-BETTI.md) (PROVED_LEAN)

Outgoing (0):

