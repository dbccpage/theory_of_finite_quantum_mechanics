# FSP-DIRAC-KAHLER-SPINFOAM-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: Dirac-Kaehler fermions on simplicial lattices give 2^(D/2) flavors and EPRL-FK boundary contractions yield nonnegative spin-network weights; the only local content is the count 1+4+6+4+1 = 16 = 4 x 4 in D = 4, and no spinfoam amplitude is evaluated.

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

None recorded.

## Bottleneck

Evaluate EPRL-FK boundary contractions on a declared finite complex and determine their signs; the taste count is standard and carries no positivity. Narrowed in lean4/CampaignFspDiracKahlerSpinfoamClaim.lean and checks/independent/fsp-dirac-kahler-spinfoam-claim.py while keeping status OPEN to: (1) 4D exterior-algebra binomial taste decomposition sum_{p=0}^4 C(4, p) = 1+4+6+4+1 = 16 = 4 * 2^(4/2), orientifold involution omega(p)^2 = 1, Hodge 2-form chirality split 3(1) + 3(-1) = 0, and single-taste spinor projector idempotence P^2 = P with Tr(P) = 4 and Tr(I - P) = 12; (2) simplicial coboundary nilpotence d_1 d_0 = 0, flat vs curved Dirac-projector commutator \[D_curved(c), P_0\] != 0 for c != 0 (Frobenius norm squared 2 c^2 \> 0), and S^4 Euler-vs-Ahat index mismatch chi(S^4) - 4 A_hat(S^4) = 2 != 0; (3) finite spin-network boundary contraction sign dichotomy showing that mirror-glued two-vertex contractions \<psi | V^T V | psi\> = sum_k (V psi)_k^2 \>= 0 are nonnegative whereas the single-vertex spin-1 tetrahedral Racah 6j recoupling kernel W_6j = \[\[1/6, -1/3\], \[-1/3, 1/6\]\] takes both negative (-1/3 \< 0 on psi_+ = (1, 1)) and positive (+1 \> 0 on psi_- = (1, -1)) values; and (4) explicit scope fences for 16-component negative determinants, Euclidean EPRL simplicity sublattice integrality, and odd-simplex Berezin orientation-reversal signs.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-052 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspDiracKahlerSpinfoamClaim.lean`

- file: [lean4/CampaignFspDiracKahlerSpinfoamClaim.lean](../../../lean4/CampaignFspDiracKahlerSpinfoamClaim.lean)
- sha256 (`bytes`): `eac20fb43c492827945a9a062592bb5d4b0386b8d46de6cf9387a1f185bc7842`
- cited in: node.lean, receipt dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json (CampaignFspDiracKahlerSpinfoamClaim), record TFQ-1216
- replay: `verified`
  - receipt [dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json](../../../dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json) (module `CampaignFspDiracKahlerSpinfoamClaim`): recorded sha256 `eac20fb43c492827945a9a062592bb5d4b0386b8d46de6cf9387a1f185bc7842` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspDiracKahlerSpinfoamClaim`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspDiracKahlerSpinfoamClaim.dirac_kahler_4d_exterior_taste_decomposition` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.dirac_kahler_4d_exterior_taste_decomposition` |
| `CampaignFspDiracKahlerSpinfoamClaim.dirac_kahler_projector_commutator_flat_vs_curved` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.dirac_kahler_projector_commutator_flat_vs_curved` |
| `CampaignFspDiracKahlerSpinfoamClaim.eprl_simplicity_spin_embedding_sublattice_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.eprl_simplicity_spin_embedding_sublattice_fence` |
| `CampaignFspDiracKahlerSpinfoamClaim.fermionic_cochain_orientation_reversal_sign_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.fermionic_cochain_orientation_reversal_sign_fence` |
| `CampaignFspDiracKahlerSpinfoamClaim.finite_spin_network_boundary_contraction_sign_dichotomy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.finite_spin_network_boundary_contraction_sign_dichotomy` |
| `CampaignFspDiracKahlerSpinfoamClaim.kahler_dirac_euler_vs_spinor_ahat_mismatch_on_s4` | yes | yes | yes | none | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.kahler_dirac_euler_vs_spinor_ahat_mismatch_on_s4` |
| `CampaignFspDiracKahlerSpinfoamClaim.minimal_spinor_projector_idempotent_and_trace_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.minimal_spinor_projector_idempotent_and_trace_four` |
| `CampaignFspDiracKahlerSpinfoamClaim.orientifold_involution_and_hodge_chirality_grading` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.orientifold_involution_and_hodge_chirality_grading` |
| `CampaignFspDiracKahlerSpinfoamClaim.simplicial_coboundary_nilpotence_on_4simplex` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.simplicial_coboundary_nilpotence_on_4simplex` |
| `CampaignFspDiracKahlerSpinfoamClaim.taste_count_carries_no_positivity_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspDiracKahlerSpinfoamClaim.taste_count_carries_no_positivity_fence` |
- counts toward the grade: yes

### Python: `code/python/src/fsp/cdt_kd_doubling_evaluator.py`

- file: [code/python/src/fsp/cdt_kd_doubling_evaluator.py](../../../code/python/src/fsp/cdt_kd_doubling_evaluator.py)
- sha256 (`bytes`): `34a304afd7e9d9bba51124bf1dfbf2c53f81e50ef37cb776c4da17f5f2e545e3`
- cited in: record TFQ-1216

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CdtKahlerDiracEvaluator` (python_symbol) | yes | yes | yes | - | - |
| `KahlerDiracAlgebra` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md`

- file: [dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md](../../../dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md)
- sha256 (`lf-normalised`): `5333736bfb52d4d6b19427dcf5c7cfb42a9576ddd4d220f04e0a5ad95cc03ef8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1216
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-dirac-kahler-spinfoam-claim.md`

- file: [dag/derivations/independent/fsp-dirac-kahler-spinfoam-claim.md](../../../dag/derivations/independent/fsp-dirac-kahler-spinfoam-claim.md)
- sha256 (`lf-normalised`): `94a95cddcf008bff91bb63837fd9cb96cafb7fc378e04c594460d52d04f0b0c6`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_independent.json`

- file: [dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_independent.json](../../../dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_independent.json)
- sha256 (`lf-normalised`): `184bc7374562a9bcc61b6c0498b12cfd605d8f3a3d04c542e7dd56e4a423317b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_mutation.json`

- file: [dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_mutation.json](../../../dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_mutation.json)
- sha256 (`lf-normalised`): `5aec7defa5f817553e708bad79103adc16dac8da0ec372a56512f6a3c7af80dc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json](../../../dag/research/campaign_fsp-dirac-kahler-spinfoam-claim_lean_replay.json)
- sha256 (`lf-normalised`): `cf0b1955e585eda7038086c6a3c585a2f949bf80eee3feadd9028dcb5b26cbbe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)
