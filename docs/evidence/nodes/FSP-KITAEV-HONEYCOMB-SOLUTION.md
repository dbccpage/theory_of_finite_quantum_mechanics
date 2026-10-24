# FSP-KITAEV-HONEYCOMB-SOLUTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Kitaev (2006): in the four-Majorana representation of the honeycomb model, the plaquette fluxes W_p commute with H and with each other, and in each flux sector H is quadratic in the c Majoranas with a static Z2 gauge field (after projection to the physical subspace).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Kitaev honeycomb spin model and its Majorana representation (Kitaev 2006)

## Bottleneck

A sign-free sampling claim for this representation is not made or checked here; the gauge projection and flux-sector sum must be kept explicit. Narrowed in lean4/CampaignFspKitaevHoneycombSolution.lean and checks/independent/fsp-kitaev-honeycomb-solution.py to the single-site 4x4 Majorana Clifford and Pauli spin algebra, bond spin-product factorization (bj cj)(bk ck) = -(bj bk)(cj ck), hexagonal plaquette local Z2 gauge invariance, closed-surface even vortex parity prod_p W_p = 1, quadratic matter skew-symmetry det(A(u)) = Pf_4(A(u))^2, and explicit fences for 4^N = 2^N * 2^N gauge redundancy, link-flip Pfaffian sign reversal Pf(A(-u_e)) = -Pf(A(u_e)), and physical parity projection filtering (1 + P_matter * P_gauge).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-043 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspKitaevHoneycombSolution.lean`

- file: [lean4/CampaignFspKitaevHoneycombSolution.lean](../../../lean4/CampaignFspKitaevHoneycombSolution.lean)
- sha256 (`bytes`): `def191c845e345ab0745b9f3c769de207113b8826417a55adc54223fca4aa78a`
- cited in: node.lean, receipt dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json (CampaignFspKitaevHoneycombSolution), record TFQ-1207
- replay: `verified`
  - receipt [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json) (module `CampaignFspKitaevHoneycombSolution`): recorded sha256 `def191c845e345ab0745b9f3c769de207113b8826417a55adc54223fca4aa78a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspKitaevHoneycombSolution`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspKitaevHoneycombSolution.abstract_bond_spin_product_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.abstract_bond_spin_product_factorization` |
| `CampaignFspKitaevHoneycombSolution.closed_surface_total_plaquette_flux_eq_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.closed_surface_total_plaquette_flux_eq_one` |
| `CampaignFspKitaevHoneycombSolution.hexPlaquetteFlux_sq_eq_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.hexPlaquetteFlux_sq_eq_one` |
| `CampaignFspKitaevHoneycombSolution.kitaev_spin_operators_pauli_algebra_and_gauge_commutation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.kitaev_spin_operators_pauli_algebra_and_gauge_commutation` |
| `CampaignFspKitaevHoneycombSolution.link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence` |
| `CampaignFspKitaevHoneycombSolution.majorana_site_clifford_relations` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.majorana_site_clifford_relations` |
| `CampaignFspKitaevHoneycombSolution.physical_parity_projection_excludes_mismatched_sector_states_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.physical_parity_projection_excludes_mismatched_sector_states_fence` |
| `CampaignFspKitaevHoneycombSolution.plaquette_flux_local_z2_gauge_invariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.plaquette_flux_local_z2_gauge_invariance` |
| `CampaignFspKitaevHoneycombSolution.quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det` |
| `CampaignFspKitaevHoneycombSolution.single_link_flip_inverts_two_incident_plaquettes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.single_link_flip_inverts_two_incident_plaquettes` |
| `CampaignFspKitaevHoneycombSolution.unprojected_majorana_fock_overcounts_physical_spin_space_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspKitaevHoneycombSolution.unprojected_majorana_fock_overcounts_physical_spin_space_fence` |
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
- sha256 (`lf-normalised`): `76edc3a55e959f3ef6658e493d977132c3e6fcbe9818d4c390a55b3e93d4a18e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1207
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-kitaev-honeycomb-solution.md`

- file: [dag/derivations/independent/fsp-kitaev-honeycomb-solution.md](../../../dag/derivations/independent/fsp-kitaev-honeycomb-solution.md)
- sha256 (`lf-normalised`): `51571f5975294e4d4640495652f137c8917afa5833280e1b0eae71092b3000a3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-kitaev-honeycomb-solution_independent.json`

- file: [dag/research/campaign_fsp-kitaev-honeycomb-solution_independent.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_independent.json)
- sha256 (`lf-normalised`): `df17b0c448f81f04a69b8524774196ad7e62ea852131076143190bf3dd54d5af`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_mutation.json`

- file: [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_mutation.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_mutation.json)
- sha256 (`lf-normalised`): `7f151adca99357ff2f55d2cf1c01371a6197ebfea67912940d852a38d57552ff`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json`

- file: [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json)
- sha256 (`lf-normalised`): `dbf34fcab7ef807219cb9b053615ff662bbb19217775abea7b9ba9a7ec0c9928`
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
