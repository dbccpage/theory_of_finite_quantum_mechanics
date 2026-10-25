# FSP-NICOLAI-MAP-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: on an off-shell supersymmetric lattice model the map xi = -partial^2 phi + W'(phi) has Jacobian equal to the fermion determinant and turns the partition function into a Gaussian with no sign problem; nothing in this checkout constructs the map or the Jacobian identity.

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

Give the lattice model, prove det(d xi / d phi) = det D_F, and treat the sign of det D_F and the multiplicity of the map; Nicolai-map results are model specific in the literature. Narrowed in lean4/CampaignFspNicolaiMapClaim.lean and checks/independent/fsp-nicolai-map-claim.py while keeping status OPEN to: (1) explicit 2-site and 3-site periodic skew-plus-diagonal lattice Nicolai map Jacobian identities J = D_kin(kappa) + diag(w_i) = D_F with det J_2 = w_0 w_1 + kappa^2 and det J_3 = w_0 w_1 w_2 + kappa^2 (w_0 + w_1 + w_2); (2) strict positivity det J_2 \>= m^2 + kappa^2 \> 0 and det J_3 \> 0 under convex quartic superpotentials W''(phi_i) = m + c phi_i^2 \>= m \> 0 (m \> 0, c \>= 0); (3) change-of-variables branch sign decomposition J = sgn(J) * |J|, opposite-sign branch cancellation sgn(+2 phi_0) + sgn(-2 phi_0) = 0 on the non-convex fold map xi(phi) = phi^2 - c, negative inner-branch Jacobian J(0) = -3 \< 0 on the cubic map xi(phi) = phi^3 - 3 phi, and negative determinant flip under supersymmetry-breaking perturbations delta * w_1 \> w_0 w_1 + kappa^2; and (4) explicit scope fences against the historical regge_wdw_core.lean::NicolaiMapSignSuppressionPredicate t t (t = t) placeholder and against generalizing model-specific 1D convex Nicolai maps to arbitrary lattice fermion theories.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-041 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspNicolaiMapClaim.lean`

- file: [lean4/CampaignFspNicolaiMapClaim.lean](../../../lean4/CampaignFspNicolaiMapClaim.lean)
- sha256 (`bytes`): `f8e55a83e4e7d330dfb4cd86ac210d2b499eee4400f944289150cc480f77fa1d`
- cited in: node.lean, receipt dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json (CampaignFspNicolaiMapClaim), record TFQ-1205
- replay: `verified`
  - receipt [dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json](../../../dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json) (module `CampaignFspNicolaiMapClaim`): recorded sha256 `f8e55a83e4e7d330dfb4cd86ac210d2b499eee4400f944289150cc480f77fa1d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspNicolaiMapClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspNicolaiMapClaim.nicolai_2site_skew_plus_positive_diag_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_2site_skew_plus_positive_diag_det_pos` |
| `CampaignFspNicolaiMapClaim.nicolai_3site_periodic_skew_plus_diag_det_formula` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_3site_periodic_skew_plus_diag_det_formula` |
| `CampaignFspNicolaiMapClaim.nicolai_change_of_variables_branch_sign_decomposition` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_change_of_variables_branch_sign_decomposition` |
| `CampaignFspNicolaiMapClaim.nicolai_map_2site_jacobian_equals_fermion_matrix` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_map_2site_jacobian_equals_fermion_matrix` |
| `CampaignFspNicolaiMapClaim.nicolai_map_model_specificity_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_map_model_specificity_scope_fence` |
| `CampaignFspNicolaiMapClaim.nicolai_quadratic_superpotential_hessian_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.nicolai_quadratic_superpotential_hessian_lower_bound` |
| `CampaignFspNicolaiMapClaim.non_convex_double_well_nicolai_branch_cancellation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.non_convex_double_well_nicolai_branch_cancellation` |
| `CampaignFspNicolaiMapClaim.non_monotonic_cubic_nicolai_three_branch_sign_defect` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.non_monotonic_cubic_nicolai_three_branch_sign_defect` |
| `CampaignFspNicolaiMapClaim.susy_breaking_perturbation_induces_negative_determinant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.susy_breaking_perturbation_induces_negative_determinant` |
| `CampaignFspNicolaiMapClaim.withdrawn_regge_wdw_core_tautology_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspNicolaiMapClaim.withdrawn_regge_wdw_core_tautology_fence` |
- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/regge_wdw_core.lean`

- file: [papers/core/fsp/lean4/regge_wdw_core.lean](../../../papers/core/fsp/lean4/regge_wdw_core.lean)
- sha256 (`bytes`): `8f20ead1eb7c40441e6ccee48c7b5c828d0d93319928ea2df7ec322226e164b9`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/regge_wdw_core.lean`
- counts toward the grade: yes

### Python: `checks/independent/fsp-nicolai-map-claim.py`

- file: [checks/independent/fsp-nicolai-map-claim.py](../../../checks/independent/fsp-nicolai-map-claim.py)
- sha256 (`bytes`): `b52113e30aa126c7b92d01efe2951d86d81c1a400dd9ddebba57fdc32c1e9f97`
- cited in: record TFQ-1205

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/cdt_susy_witten_evaluator.py`

- file: [code/python/src/fsp/cdt_susy_witten_evaluator.py](../../../code/python/src/fsp/cdt_susy_witten_evaluator.py)
- sha256 (`bytes`): `b20f9906a48e848bbb69d35bb00ec3fcbbaccae2de6f202e82e2866277131736`
- cited in: record TFQ-1205

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CdtSusyWittenEvaluator` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md`

- file: [dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md](../../../dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md)
- sha256 (`lf-normalised`): `eced2892ee847ce0c041f678571115d500f3c221589a7b6200ee0b577dad4e12`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1205
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-nicolai-map-claim.md`

- file: [dag/derivations/independent/fsp-nicolai-map-claim.md](../../../dag/derivations/independent/fsp-nicolai-map-claim.md)
- sha256 (`lf-normalised`): `ba56c28d778f98c6058cc3de90425cec2aca3ede1e50e58df8ce8f082e4f99fe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-nicolai-map-claim_independent.json`

- file: [dag/research/campaign_fsp-nicolai-map-claim_independent.json](../../../dag/research/campaign_fsp-nicolai-map-claim_independent.json)
- sha256 (`lf-normalised`): `a1eae5652b31685f46894964c853e3cdb8d72cda9dd668149055ce71da090653`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-nicolai-map-claim_lean_mutation.json`

- file: [dag/research/campaign_fsp-nicolai-map-claim_lean_mutation.json](../../../dag/research/campaign_fsp-nicolai-map-claim_lean_mutation.json)
- sha256 (`lf-normalised`): `971d3581200c5e5e85fa7bb371ce76907301ca3b6074831492b75bc0c2ccb15d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json](../../../dag/research/campaign_fsp-nicolai-map-claim_lean_replay.json)
- sha256 (`lf-normalised`): `5a8a7c86111d243ee471fe94fd0dfa744214b508471204d0ad8184787719676e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-NICOLAI-MAP-CLAIM` `GAP_NO_DERIVATION`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)

Outgoing (0):

