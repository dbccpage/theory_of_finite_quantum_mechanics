# FSP-CDT-FOLIATION-POSITIVITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a global proper-time foliation in CDT forbids spatial branching, removes Lorentzian cancellations, yields a sign-free positive transfer matrix and a 4D de Sitter universe; the de Sitter phase is numerical literature and the checkout has no transfer-matrix or positivity computation.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Positivity in CDT uses a Wick rotation of a declared action; derive it for a declared finite model and keep numerical phase results as external evidence. Narrowed in lean4/CampaignFspCdtFoliationPositivity.lean and checks/independent/fsp-cdt-foliation-positivity.py while keeping status OPEN to: (1) proper-time foliation tau : V -\> Nat strict causal ordering and absence of causal 2-cycles and 3-cycles; (2) 4D CDT causal 4-simplex slice-partition classification (4,1), (3,2), (2,3), (1,4), exclusion of purely spatial (5,0) and (0,5) simplices, boundary tetrahedra matching, and rejection of disconnected spatial branching; (3) exact rational Wick-rotated Boltzmann weight positivity and reflection positivity \<psi, T psi\> = sum_k d_k (B psi)_k^2 \>= 0 of the symmetric slice transfer matrix T = B^T D B, with explicit 2-state witness T_cdt = \[\[5, 3\], \[3, 2\]\] traces Z_1 = 7, Z_2 = 47, Z_3 = 322; and (4) BQNF sign-reversing involution pair cancellation vs the frustrated chiral 3-configuration ensemble (\[2, 3, 5\], \[+1, +1, -1\]) obstruction, plus explicit scope fences for Lorentzian phase cancellation prior to Wick rotation, finite-complex stationary return probability saturation (asymptotic spectral dimension 0 != 4 vs external 4D de Sitter Monte Carlo literature), and fermionic Grassmann determinant signs.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-051 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspCdtFoliationPositivity.lean`

- file: [lean4/CampaignFspCdtFoliationPositivity.lean](../../../lean4/CampaignFspCdtFoliationPositivity.lean)
- sha256 (`bytes`): `5ed25f7689fb24bba7bc99521183c8f1c41cea9bc4ed074175014a286ea66cdf`
- cited in: node.lean, receipt dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json (CampaignFspCdtFoliationPositivity), record TFQ-1215
- replay: `verified`
  - receipt [dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json](../../../dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json) (module `CampaignFspCdtFoliationPositivity`): recorded sha256 `5ed25f7689fb24bba7bc99521183c8f1c41cea9bc4ed074175014a286ea66cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspCdtFoliationPositivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspCdtFoliationPositivity.bosonic_cdt_positivity_independent_of_fermion_determinant_sign_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.bosonic_cdt_positivity_independent_of_fermion_determinant_sign_fence` |
| `CampaignFspCdtFoliationPositivity.bqnf_involution_cancels_pairs_vs_chiral_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.bqnf_involution_cancels_pairs_vs_chiral_obstruction` |
| `CampaignFspCdtFoliationPositivity.cdt_4simplex_slice_partition_classification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.cdt_4simplex_slice_partition_classification` |
| `CampaignFspCdtFoliationPositivity.cdt_boundary_tetrahedra_and_no_spatial_branching` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.cdt_boundary_tetrahedra_and_no_spatial_branching` |
| `CampaignFspCdtFoliationPositivity.finite_complex_stationary_return_probability_saturates_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.finite_complex_stationary_return_probability_saturates_fence` |
| `CampaignFspCdtFoliationPositivity.lorentzian_vs_euclidean_wick_rotation_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.lorentzian_vs_euclidean_wick_rotation_fence` |
| `CampaignFspCdtFoliationPositivity.proper_time_foliation_strict_order_and_no_cycles` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.proper_time_foliation_strict_order_and_no_cycles` |
| `CampaignFspCdtFoliationPositivity.reflection_positive_transfer_matrix_symm_and_psd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.reflection_positive_transfer_matrix_symm_and_psd` |
| `CampaignFspCdtFoliationPositivity.two_state_cdt_transfer_matrix_trace_and_det_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.two_state_cdt_transfer_matrix_trace_and_det_pos` |
| `CampaignFspCdtFoliationPositivity.wick_rotated_cdt_boltzmann_weight_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspCdtFoliationPositivity.wick_rotated_cdt_boltzmann_weight_positivity` |
- counts toward the grade: yes

### Python: `code/python/src/fsp/cdt_fermion_sign_evaluator.py`

- file: [code/python/src/fsp/cdt_fermion_sign_evaluator.py](../../../code/python/src/fsp/cdt_fermion_sign_evaluator.py)
- sha256 (`bytes`): `bb756d8f519cff0f0929436f4166acf65886d4d78024887cdaec3dafe64f4e8e`
- cited in: record TFQ-1215

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CdtFermionSignEvaluator` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md`

- file: [dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md](../../../dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md)
- sha256 (`lf-normalised`): `ce4bd86569e4fbe8079e6c9508f3fc9331d6be99281f9a681c5147d296dbba0f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1215
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-cdt-foliation-positivity.md`

- file: [dag/derivations/independent/fsp-cdt-foliation-positivity.md](../../../dag/derivations/independent/fsp-cdt-foliation-positivity.md)
- sha256 (`lf-normalised`): `7b2f4cd137b530ad2c9dab03adef3d042389220c9cfeec5a3cfa06c92f00efa3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cdt-foliation-positivity_independent.json`

- file: [dag/research/campaign_fsp-cdt-foliation-positivity_independent.json](../../../dag/research/campaign_fsp-cdt-foliation-positivity_independent.json)
- sha256 (`lf-normalised`): `190a4a472745d2d36d33542e040c4d918ada0cfd9c13972606b0e356aaa67580`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cdt-foliation-positivity_lean_mutation.json`

- file: [dag/research/campaign_fsp-cdt-foliation-positivity_lean_mutation.json](../../../dag/research/campaign_fsp-cdt-foliation-positivity_lean_mutation.json)
- sha256 (`lf-normalised`): `45d42e21c105f31129cf2af771fa6cc6237935371ce3ab67d4d2e74dc12fc7ee`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json`

- file: [dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json](../../../dag/research/campaign_fsp-cdt-foliation-positivity_lean_replay.json)
- sha256 (`lf-normalised`): `c93da2f17665c9d67249686631a115e7531f5208da0bd9b231c4b840aa6d520a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN), [FSP-PACHNER-INVARIANCE-CLAIM](FSP-PACHNER-INVARIANCE-CLAIM.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` `GAP_NO_DERIVATION`: [FSP-DIRAC-KAHLER-SPINFOAM-CLAIM](FSP-DIRAC-KAHLER-SPINFOAM-CLAIM.md) (OPEN)
