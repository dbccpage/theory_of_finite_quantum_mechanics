# FSP-HINGE-LINEON-SIGN-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: lineons confined to 1D hinge lines cannot exchange without collision, so their worldlines carry no nontrivial permutations and foliated fracton models are sign free; no model, path expansion or sign computation exists in this checkout.

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

None recorded.

## Bottleneck

Give a fermionic fracton Hamiltonian, its declared representation and show all path weights nonnegative, including lineons on intersecting hinges; ledger GIN-C24 withdraws the fixture reading. Narrowed in lean4/CampaignFspHingeLineonSignClaim.lean and checks/independent/fsp-hinge-lineon-sign-claim.py while keeping status OPEN to: (1) on an isolated 1D open chain, non-colliding and non-crossing nearest-neighbor steps strictly preserve site ordering x1 \< x2, pass over (i+1) - i - 1 = 0 intermediate Jordan-Wigner sites (sign +1), and induce the identity permutation on closed loops (sign +1); (2) on a periodic 1D hinge ring, cyclic winding of N = 2 fermions induces Equiv.swap 0 1 with negative sign (-1)^(2-1) = -1; (3) on two intersecting 1D hinges meeting at a 4-vertex T-junction, two hardcore fermions exchange positions in 6 non-colliding steps with odd permutation sign -1; (4) turning a 1D lineon around a 90-degree hinge corner leaves a weight-2 orthogonal vertex defect and drops the foliated categorical projection trace from +4 to -2 \< 0; and (5) non-abelian 2-gauge sheet holonomy generators J = \[\[0,1\],\[-1,0\]\] and D = \[\[1,0\],\[0,-1\]\] have group commutator J D (-J) D = -I_2 with negative trace Tr(-I_2) = -2 \< 0 and defect mass Phi_1 = 2 \> 0 (GIN-C24).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-055 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspHingeLineonSignClaim.lean`

- file: [lean4/CampaignFspHingeLineonSignClaim.lean](../../../lean4/CampaignFspHingeLineonSignClaim.lean)
- sha256 (`bytes`): `43ff2487734337268f3af11efcc8106f02690576a8dc2a525ddcadab5b24ab8a`
- cited in: node.lean, receipt dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json (CampaignFspHingeLineonSignClaim), record TFQ-1219
- replay: `verified`
  - receipt [dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json) (module `CampaignFspHingeLineonSignClaim`): recorded sha256 `43ff2487734337268f3af11efcc8106f02690576a8dc2a525ddcadab5b24ab8a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspHingeLineonSignClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspHingeLineonSignClaim.corner_lineon_turn_leaves_residual_hinge_defect_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.corner_lineon_turn_leaves_residual_hinge_defect_fence` |
| `CampaignFspHingeLineonSignClaim.gin_c24_hinge_lineon_sign_claim_remains_open_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.gin_c24_hinge_lineon_sign_claim_remains_open_fence` |
| `CampaignFspHingeLineonSignClaim.nonabelian_2gauge_hinge_trace_and_defect_mass_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.nonabelian_2gauge_hinge_trace_and_defect_mass_fence` |
| `CampaignFspHingeLineonSignClaim.open_chain_closed_worldline_identity_permutation_sign_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.open_chain_closed_worldline_identity_permutation_sign_one` |
| `CampaignFspHingeLineonSignClaim.open_chain_jordan_wigner_nearest_neighbor_pass_count_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.open_chain_jordan_wigner_nearest_neighbor_pass_count_zero` |
| `CampaignFspHingeLineonSignClaim.open_chain_nearest_neighbor_order_preserved` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.open_chain_nearest_neighbor_order_preserved` |
| `CampaignFspHingeLineonSignClaim.periodic_ring_cyclic_winding_even_particle_negative_sign_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.periodic_ring_cyclic_winding_even_particle_negative_sign_fence` |
| `CampaignFspHingeLineonSignClaim.signed_partition_sum_cancellation_on_intersecting_hinges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.signed_partition_sum_cancellation_on_intersecting_hinges` |
| `CampaignFspHingeLineonSignClaim.su2_pauli_group_commutator_is_neg_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.su2_pauli_group_commutator_is_neg_identity` |
| `CampaignFspHingeLineonSignClaim.tjunction_intersecting_hinge_exchange_negative_sign_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspHingeLineonSignClaim.tjunction_intersecting_hinge_exchange_negative_sign_fence` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-hinge-lineon-sign-claim.py`

- file: [checks/independent/fsp-hinge-lineon-sign-claim.py](../../../checks/independent/fsp-hinge-lineon-sign-claim.py)
- sha256 (`bytes`): `c77877c19954179f4d625e2c5f955946b0c58ed5d56edc1d9dffc5e67b500b4d`
- cited in: record TFQ-1219

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/foliated_fracton_2gauge_defects.py`

- file: [code/python/src/fsp/foliated_fracton_2gauge_defects.py](../../../code/python/src/fsp/foliated_fracton_2gauge_defects.py)
- sha256 (`bytes`): `6c34ac89c96de95d234b1bbb9dbfeb98bd3ecae041f6163ed7e72addbb2aca66`
- cited in: record TFQ-1219

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FoliatedFractonEngine` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md`

- file: [dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md](../../../dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md)
- sha256 (`lf-normalised`): `4837d39383eb3ff72a30c0617c1b335081ebe3813d1466a6b4b87f7fbd58d7b6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1219
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-hinge-lineon-sign-claim.md`

- file: [dag/derivations/independent/fsp-hinge-lineon-sign-claim.md](../../../dag/derivations/independent/fsp-hinge-lineon-sign-claim.md)
- sha256 (`lf-normalised`): `07a70527a6a34b8f21d290d34dcbf5b79b6a9a9da653b41b6079ba27dc71f0e2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-hinge-lineon-sign-claim_independent.json`

- file: [dag/research/campaign_fsp-hinge-lineon-sign-claim_independent.json](../../../dag/research/campaign_fsp-hinge-lineon-sign-claim_independent.json)
- sha256 (`lf-normalised`): `da9ae5260ab4470add1fd3ea7fa468f8624663ebd66e2cbbd2b1c28188a65135`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_mutation.json`

- file: [dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_mutation.json](../../../dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_mutation.json)
- sha256 (`lf-normalised`): `4d02b7fe380a5e26973f8340581e86e59094d24b83b735339802955679136c6b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-hinge-lineon-sign-claim_lean_replay.json)
- sha256 (`lf-normalised`): `14de24ca04678c571f34f9dbd4a68574f603c018d82e7eb851b8f3fee3f52d00`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-HINGE-LINEON-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-FRACTON-MOBILITY](FSP-FRACTON-MOBILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
