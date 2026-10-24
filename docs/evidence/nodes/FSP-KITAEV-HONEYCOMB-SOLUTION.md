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

Narrowed algebraic checks only. Explicit integer matrices obey Clifford identities; one anticommutation hypothesis gives bond factorization; a six-factor commutative-ring flux is gauge invariant; a product of all supplied involutions squared equals one; and a 4x4 skew matrix has determinant equal to the squared explicit Pfaffian polynomial. No cellular surface incidence map is built, so the product-square lemma is not a theorem about all plaquettes on closed tori. The independent diagonal parity matrix is not identified with the supplied Majorana gauge operator. No physical Hilbert-space projection or thermal partition function is constructed. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-043 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspKitaevHoneycombSolution.lean`

- file: [lean4/CampaignFspKitaevHoneycombSolution.lean](../../../lean4/CampaignFspKitaevHoneycombSolution.lean)
- sha256 (`bytes`): `b73b461fe2757d85dcdb6efb82fbd0e30aa98b76d3e0ed9425d67abce8508b52`
- cited in: node.lean, record TFQ-1207
- replay: `verified`
  - receipt [dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json](../../../dag/research/campaign_fsp-kitaev-honeycomb-solution_lean_replay.json) (module `CampaignFspKitaevHoneycombSolution`): recorded sha256 `b73b461fe2757d85dcdb6efb82fbd0e30aa98b76d3e0ed9425d67abce8508b52` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspKitaevHoneycombSolution`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspKitaevHoneycombSolution.abstract_bond_spin_product_factorization` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.abstract_bond_spin_product_factorization` |
| `CampaignFspKitaevHoneycombSolution.closed_surface_total_plaquette_flux_eq_one` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.closed_surface_total_plaquette_flux_eq_one` |
| `CampaignFspKitaevHoneycombSolution.hexPlaquetteFlux_sq_eq_one` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.hexPlaquetteFlux_sq_eq_one` |
| `CampaignFspKitaevHoneycombSolution.kitaev_spin_operators_pauli_algebra_and_gauge_commutation` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.kitaev_spin_operators_pauli_algebra_and_gauge_commutation` |
| `CampaignFspKitaevHoneycombSolution.link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.link_flip_flips_matter_pfaffian_sign_while_det_stays_positive_fence` |
| `CampaignFspKitaevHoneycombSolution.majorana_site_clifford_relations` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.majorana_site_clifford_relations` |
| `CampaignFspKitaevHoneycombSolution.physical_parity_projection_excludes_mismatched_sector_states_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.physical_parity_projection_excludes_mismatched_sector_states_fence` |
| `CampaignFspKitaevHoneycombSolution.plaquette_flux_local_z2_gauge_invariance` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.plaquette_flux_local_z2_gauge_invariance` |
| `CampaignFspKitaevHoneycombSolution.quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.quadratic_matter_matrix_skew_symmetric_and_pfaffian_sq_eq_det` |
| `CampaignFspKitaevHoneycombSolution.single_link_flip_inverts_two_incident_plaquettes` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.single_link_flip_inverts_two_incident_plaquettes` |
| `CampaignFspKitaevHoneycombSolution.unprojected_majorana_fock_overcounts_physical_spin_space_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspKitaevHoneycombSolution.unprojected_majorana_fock_overcounts_physical_spin_space_fence` |
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
- sha256 (`lf-normalised`): `ea360507fd4b16d04383aca06eef0db0c708e005c6d58f6637171da4ca7d5d84`
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
- sha256 (`lf-normalised`): `2a75eafbeded976e16ce3d08f0647a760ccae75dc349afc82d479fa8bc53152c`
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
