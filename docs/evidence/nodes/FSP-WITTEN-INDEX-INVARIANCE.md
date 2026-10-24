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

Narrowed algebraic checks only. For arbitrary finite rectangular matrix blocks over a commutative ring, positive-power block traces agree and the graded supertrace vanishes. The cubic polynomial follows. The paired-list model explicitly subtracts each weight from itself; it does not derive spectral pairing. B is independent of A and is not proved to be its adjoint. Zero-mode counts are supplied; the rectangular vector may be zero at a=b=0. There is no analytic exponential, ground-state existence proof, or sign-free sampler. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-042 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspWittenIndexInvariance.lean`

- file: [lean4/CampaignFspWittenIndexInvariance.lean](../../../lean4/CampaignFspWittenIndexInvariance.lean)
- sha256 (`bytes`): `6935af1b664bfdfcaebc654abe377c8b99414758b128c692e40c4902db40183b`
- cited in: node.lean, record TFQ-1206
- replay: `verified`
  - receipt [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json) (module `CampaignFspWittenIndexInvariance`): recorded sha256 `6935af1b664bfdfcaebc654abe377c8b99414758b128c692e40c4902db40183b` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspWittenIndexInvariance`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspWittenIndexInvariance.boson_eq_fermion_pow_succ_trace` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.boson_eq_fermion_pow_succ_trace` |
| `CampaignFspWittenIndexInvariance.boson_fermion_block_pow_intertwine` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.boson_fermion_block_pow_intertwine` |
| `CampaignFspWittenIndexInvariance.broken_lattice_susy_destroys_supertrace_cancellation_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.broken_lattice_susy_destroys_supertrace_cancellation_fence` |
| `CampaignFspWittenIndexInvariance.nonzero_witten_index_implies_zero_mode_ground_state` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.nonzero_witten_index_implies_zero_mode_ground_state` |
| `CampaignFspWittenIndexInvariance.rectangular_2x1_supercharge_forced_zero_mode_and_index_one` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.rectangular_2x1_supercharge_forced_zero_mode_and_index_one` |
| `CampaignFspWittenIndexInvariance.supertrace_cubic_boltzmann_poly_independent_of_beta` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.supertrace_cubic_boltzmann_poly_independent_of_beta` |
| `CampaignFspWittenIndexInvariance.supertrace_fermionParity_fin_eq_sub` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.supertrace_fermionParity_fin_eq_sub` |
| `CampaignFspWittenIndexInvariance.supertrace_susyHamiltonian_pow_succ_eq_zero` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.supertrace_susyHamiltonian_pow_succ_eq_zero` |
| `CampaignFspWittenIndexInvariance.susyHamiltonian_eq_fromBlocks` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.susyHamiltonian_eq_fromBlocks` |
| `CampaignFspWittenIndexInvariance.susyHamiltonian_pow_eq_fromBlocks` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.susyHamiltonian_pow_eq_fromBlocks` |
| `CampaignFspWittenIndexInvariance.wittenIndexPaired_eq_zero_mode_diff_for_all_weights` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.wittenIndexPaired_eq_zero_mode_diff_for_all_weights` |
| `CampaignFspWittenIndexInvariance.witten_index_vs_partition_function_and_average_sign_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspWittenIndexInvariance.witten_index_vs_partition_function_and_average_sign_fence` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-witten-index-invariance.py`

- file: [checks/independent/fsp-witten-index-invariance.py](../../../checks/independent/fsp-witten-index-invariance.py)
- sha256 (`bytes`): `cc583dcc76fbf1cb45da1acbea62f995d37920bf8077c747eae54dd8d167c265`
- cited in: record TFQ-1206

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md`

- file: [dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md](../../../dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md)
- sha256 (`lf-normalised`): `e9ec3c1a473956c447707f5651a48b3691d190486986fb22c9aff4b7d8126d0b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1206
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-witten-index-invariance.md`

- file: [dag/derivations/independent/fsp-witten-index-invariance.md](../../../dag/derivations/independent/fsp-witten-index-invariance.md)
- sha256 (`lf-normalised`): `6636c85679ecf789a0400d2fb985b75ce7eff5d260685c2260181faff4177da2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_independent.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_independent.json](../../../dag/research/campaign_fsp-witten-index-invariance_independent.json)
- sha256 (`lf-normalised`): `24b41a610981b2d8caed63ec4bfea341ffa3b9bdf305ac45bf23e01ad7f46d99`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_mutation.json)
- sha256 (`lf-normalised`): `58339bbc9da6416c679575ee6ec15793c801110faf2184da823f607bcca2ef9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_lean_replay.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json)
- sha256 (`lf-normalised`): `634ccad0d373af3ed03c698ab5bba00973d27f19253c6454aea2fca78b8d5bb9`
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
