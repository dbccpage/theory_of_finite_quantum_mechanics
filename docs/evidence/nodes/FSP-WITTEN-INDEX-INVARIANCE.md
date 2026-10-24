# FSP-WITTEN-INDEX-INVARIANCE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite-dimensional graded Hilbert space with an exact supercharge Q and H = {Q, Q^dagger}, positive-energy levels pair bosons with fermions, so W = Tr\[(-1)^F exp(-beta H)\] = n_B(E=0) - n_F(E=0) for every beta, and unbroken supersymmetry has ground energy 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- exact supercharge with H = {Q, Q^dagger} on a finite graded space (assumption)

## Bottleneck

Standard result imported; it presupposes an exact lattice supercharge, which FSP-DERIV-040 leaves open, and gives no sign-free sampling of Z itself. Narrowed in lean4/CampaignFspWittenIndexInvariance.lean and checks/independent/fsp-witten-index-invariance.py to exact block power intertwining (BA)^(k+1) = B(AB)^k A, vanishing supertrace Tr(Gamma_F H(A,B)^(k+1)) = 0 for all k, beta-independence of truncated Boltzmann polynomials and paired positive-energy doublet sums W(beta) = n_B(0) - n_F(0), forced zero-energy ground states when W != 0, rectangular (2, 1) forced bosonic zero modes, and explicit fences separating W(beta) from the beta-dependent partition function Z(beta) and showing that lattice SUSY breaking Delta shifts Tr(Gamma_F H_broken) by -Tr(Delta).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-042 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspWittenIndexInvariance.lean`

- file: [lean4/CampaignFspWittenIndexInvariance.lean](../../../lean4/CampaignFspWittenIndexInvariance.lean)
- sha256 (`bytes`): `d3d542d8c8d79ec7ec1aba98407ee71a913c7639b390bda963b6731dcd08ea84`
- cited in: node.lean, receipt dag/research/campaign_fsp-witten-index-invariance_lean_replay.json (CampaignFspWittenIndexInvariance), record TFQ-1206
- replay: `verified`
  - receipt [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json) (module `CampaignFspWittenIndexInvariance`): recorded sha256 `d3d542d8c8d79ec7ec1aba98407ee71a913c7639b390bda963b6731dcd08ea84` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspWittenIndexInvariance`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspWittenIndexInvariance.boson_eq_fermion_pow_succ_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.boson_eq_fermion_pow_succ_trace` |
| `CampaignFspWittenIndexInvariance.boson_fermion_block_pow_intertwine` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.boson_fermion_block_pow_intertwine` |
| `CampaignFspWittenIndexInvariance.broken_lattice_susy_destroys_supertrace_cancellation_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.broken_lattice_susy_destroys_supertrace_cancellation_fence` |
| `CampaignFspWittenIndexInvariance.nonzero_witten_index_implies_zero_mode_ground_state` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.nonzero_witten_index_implies_zero_mode_ground_state` |
| `CampaignFspWittenIndexInvariance.rectangular_2x1_supercharge_forced_zero_mode_and_index_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.rectangular_2x1_supercharge_forced_zero_mode_and_index_one` |
| `CampaignFspWittenIndexInvariance.supertrace_cubic_boltzmann_poly_independent_of_beta` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.supertrace_cubic_boltzmann_poly_independent_of_beta` |
| `CampaignFspWittenIndexInvariance.supertrace_fermionParity_fin_eq_sub` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.supertrace_fermionParity_fin_eq_sub` |
| `CampaignFspWittenIndexInvariance.supertrace_susyHamiltonian_pow_succ_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.supertrace_susyHamiltonian_pow_succ_eq_zero` |
| `CampaignFspWittenIndexInvariance.susyHamiltonian_eq_fromBlocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.susyHamiltonian_eq_fromBlocks` |
| `CampaignFspWittenIndexInvariance.susyHamiltonian_pow_eq_fromBlocks` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.susyHamiltonian_pow_eq_fromBlocks` |
| `CampaignFspWittenIndexInvariance.wittenIndexPaired_eq_zero_mode_diff_for_all_weights` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.wittenIndexPaired_eq_zero_mode_diff_for_all_weights` |
| `CampaignFspWittenIndexInvariance.witten_index_vs_partition_function_and_average_sign_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWittenIndexInvariance.witten_index_vs_partition_function_and_average_sign_fence` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-witten-index-invariance.py`

- file: [checks/independent/fsp-witten-index-invariance.py](../../../checks/independent/fsp-witten-index-invariance.py)
- sha256 (`bytes`): `0d5f2cf47efa219f9ced88a7017b96a461b633dd66218a70d8fc2284bc1cb96c`
- cited in: record TFQ-1206

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md`

- file: [dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md](../../../dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md)
- sha256 (`lf-normalised`): `b035181c9c24963dbff36b8b76153e38793706bca37dc0c0b87023a37eeb1633`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1206
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-witten-index-invariance.md`

- file: [dag/derivations/independent/fsp-witten-index-invariance.md](../../../dag/derivations/independent/fsp-witten-index-invariance.md)
- sha256 (`lf-normalised`): `40b54510c7c2f4d1da4586c07f62f99ac5791e7db0bb3cc37345a586234068de`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_independent.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_independent.json](../../../dag/research/campaign_fsp-witten-index-invariance_independent.json)
- sha256 (`lf-normalised`): `129a233a599208923aaa59daa6aadeed6a4905cff092cca93e25447a0c4a38ba`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json)
- sha256 (`lf-normalised`): `58339bbc9da6416c679575ee6ec15793c801110faf2184da823f607bcca2ef9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_lean_replay.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json)
- sha256 (`lf-normalised`): `fc66155f9af9f435ed039e2dd37057fd4d2c2d8c372bd882ada983c353542473`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-WITTEN-INDEX-INVARIANCE` `CONDITIONAL_ON_IMPORT`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
