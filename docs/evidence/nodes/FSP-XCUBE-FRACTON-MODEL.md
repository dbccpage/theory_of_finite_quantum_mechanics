# FSP-XCUBE-FRACTON-MODEL

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Vijay-Haah-Fu (2016): the X-cube model on an Lx x Ly x Lz periodic cubic lattice has pairwise commuting vertex and cube terms and ground-state degeneracy 2^(2Lx + 2Ly + 2Lz - 3).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- X-cube stabilizer model (Vijay, Haah, Fu 2016)

## Bottleneck

Imported literature result; the checkout has no X-cube stabilizer computation, and it has no fermion-sign consequence by itself. Narrowed in lean4/CampaignFspXcubeFractonModel.lean and checks/independent/fsp-xcube-fracton-model.py while keeping status IMPORTED_ASSUMPTION to: (1) periodic cubic lattice T^3(Lx, Ly, Lz) edge-qubit count 3 Lx Ly Lz and generator count 4 Lx Ly Lz; (2) pairwise commutativity \[A_v^(mu nu), B_c\] = 0 via even corner-edge overlap 2 % 2 = 0 and local vertex syzygy A_v^(xy) A_v^(yz) A_v^(zx) = I; (3) exact F_2 parity-check rank subtraction rank(H_X) = V - (Lx + Ly + Lz - 2) and rank(H_Z) = 2V - (Lx + Ly + Lz - 1) yielding logical qubit count k = 2 Lx + 2 Ly + 2 Lz - 3 and ground-state degeneracy GSD = 2^(2 Lx + 2 Ly + 2 Lz - 3), verified by exact F_2 Gaussian elimination across all 27 lattices (Lx, Ly, Lz) in {2, 3, 4}^3; and (4) explicit scope fences for 6-edge 3D star anti-commutation, bosonic CSS stoquasticity (no fermion-sign consequence), and non-abelian 2-gauge hinge negative trace.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-053 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspXcubeFractonModel.lean`

- file: [lean4/CampaignFspXcubeFractonModel.lean](../../../lean4/CampaignFspXcubeFractonModel.lean)
- sha256 (`bytes`): `7b5956a0c8a7df295e4ec834410351fb6c99e8733efd928596a3c6f802bd79c9`
- cited in: node.lean, receipt dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json (CampaignFspXcubeFractonModel), record TFQ-1217
- replay: `verified`
  - receipt [dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json](../../../dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json) (module `CampaignFspXcubeFractonModel`): recorded sha256 `7b5956a0c8a7df295e4ec834410351fb6c99e8733efd928596a3c6f802bd79c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspXcubeFractonModel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspXcubeFractonModel.nonabelian_hinge_holonomy_negative_trace_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.nonabelian_hinge_holonomy_negative_trace_fence` |
| `CampaignFspXcubeFractonModel.six_edge_3d_star_anticommutes_with_cube_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.six_edge_3d_star_anticommutes_with_cube_fence` |
| `CampaignFspXcubeFractonModel.xcube_css_bosonic_stoquasticity_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.xcube_css_bosonic_stoquasticity_fence` |
| `CampaignFspXcubeFractonModel.xcube_explicit_torus_degeneracy_table` | yes | yes | yes | propext | `#print axioms CampaignFspXcubeFractonModel.xcube_explicit_torus_degeneracy_table` |
| `CampaignFspXcubeFractonModel.xcube_local_vertex_triple_syzygy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.xcube_local_vertex_triple_syzygy` |
| `CampaignFspXcubeFractonModel.xcube_planar_subsystem_charge_conservation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.xcube_planar_subsystem_charge_conservation` |
| `CampaignFspXcubeFractonModel.xcube_stabilizer_rank_and_logical_qubit_identity` | yes | yes | yes | propext | `#print axioms CampaignFspXcubeFractonModel.xcube_stabilizer_rank_and_logical_qubit_identity` |
| `CampaignFspXcubeFractonModel.xcube_subextensive_linear_scaling_vs_toric_code` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.xcube_subextensive_linear_scaling_vs_toric_code` |
| `CampaignFspXcubeFractonModel.xcube_torus_cell_and_qubit_counts` | yes | yes | yes | propext | `#print axioms CampaignFspXcubeFractonModel.xcube_torus_cell_and_qubit_counts` |
| `CampaignFspXcubeFractonModel.xcube_vertex_cross_cube_intersection_even` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspXcubeFractonModel.xcube_vertex_cross_cube_intersection_even` |
- counts toward the grade: yes

### Python: `code/python/src/fsp/foliated_fracton_2gauge_defects.py`

- file: [code/python/src/fsp/foliated_fracton_2gauge_defects.py](../../../code/python/src/fsp/foliated_fracton_2gauge_defects.py)
- sha256 (`bytes`): `6c34ac89c96de95d234b1bbb9dbfeb98bd3ecae041f6163ed7e72addbb2aca66`
- cited in: record TFQ-1217

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FoliatedFractonEngine` (python_symbol) | yes | yes | yes | - | - |
| `SubsystemChargeRegistry` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md`

- file: [dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md](../../../dag/derivations/26_fsp/tfq_1217_fsp_xcube_fracton_model.md)
- sha256 (`lf-normalised`): `af56c4b744b3f77c567bc2024723e4c9be9d1ea87c659aaee0dfb51a01f5b5b3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1217
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-xcube-fracton-model.md`

- file: [dag/derivations/independent/fsp-xcube-fracton-model.md](../../../dag/derivations/independent/fsp-xcube-fracton-model.md)
- sha256 (`lf-normalised`): `6b3d26210b06c327552f9bccfa465193e5a2aff3b99dfcaf0159fdd4be51057d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-xcube-fracton-model_independent.json`

- file: [dag/research/campaign_fsp-xcube-fracton-model_independent.json](../../../dag/research/campaign_fsp-xcube-fracton-model_independent.json)
- sha256 (`lf-normalised`): `72813a6045f0834e8e0f1849a0d5fc89d8a9671db4debc919b7c45f1a20e748d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-xcube-fracton-model_lean_mutation.json`

- file: [dag/research/campaign_fsp-xcube-fracton-model_lean_mutation.json](../../../dag/research/campaign_fsp-xcube-fracton-model_lean_mutation.json)
- sha256 (`lf-normalised`): `9b8a7bee2d4713af3eb1e86f8d9ee3db62847df2ec7d59e2015b889fa5de03f4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json`

- file: [dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json](../../../dag/research/campaign_fsp-xcube-fracton-model_lean_replay.json)
- sha256 (`lf-normalised`): `7add97150c43c6e685d53a8588d60d54e81de07d6b60ae524d253de19a83361f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN), [FSP-DIRAC-KAHLER-SPINFOAM-CLAIM](FSP-DIRAC-KAHLER-SPINFOAM-CLAIM.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-FRACTON-MOBILITY` `CONDITIONAL_ON_IMPORT`: [FSP-FRACTON-MOBILITY](FSP-FRACTON-MOBILITY.md) (IMPORTED_ASSUMPTION)
