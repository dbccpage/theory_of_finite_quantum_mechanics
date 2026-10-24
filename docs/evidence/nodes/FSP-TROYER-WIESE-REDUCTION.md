# FSP-TROYER-WIESE-REDUCTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Troyer-Wiese (2005): the NP-complete decision whether a 3D +-J Ising spin glass has ground energy below a threshold reduces in polynomial time to estimating the thermal energy of the frustrated quantum model -sum J_ij sigma^x_i sigma^x_j at beta J \>= N ln 2 + ln(12N); a deterministic polynomial estimator for that family would give P = NP, a randomized one NP subset of BPP.

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

- Troyer and Wiese, PRL 94, 170201 (2005), cond-mat/0408370, equations (10)-(11) and footnote 9
- NP-completeness of the 3D Ising spin-glass ground-state decision problem (Barahona)

## Bottleneck

This is a worst-case statement about a model family under a precision promise; it is not formalized here, is not a reduction to the Hubbard model, and does not make any fixed finite system or every fermionic Hamiltonian intractable. Narrowed in lean4/CampaignFspTroyerWieseReduction.lean and checks/independent/fsp-troyer-wiese-reduction.py while keeping status IMPORTED_ASSUMPTION to: (1) integer +/-J Ising spin-flip bond parity (-s)*s' - s*s' = -2*(s*s') and frustrated antiferromagnetic triangle ground energy -J vs excited +3J (gap 4J \> 0); (2) Troyer-Wiese (2005) Eqs. (10)-(11) Boltzmann excited-state tail bound (3*N*J*2^N)/(1 + W) \< J/4 when W \>= 12*N*2^N (corresponding to beta*J \>= N ln 2 + ln(12 N)) and disjoint YES/NO threshold decision windows separated at E_th + J/2 under estimator precision |E_hat - E_therm| \<= J/4; (3) 2x2 Hadamard conjugation U_H sigma_z U_H = 2 sigma_x mapping the diagonal Ising spin glass to the off-diagonal -sum J_ij sigma_i^x sigma_j^x model with negative length-3 closed-walk weight (-J)^3 = -J^3 \< 0 on frustrated triangles; (4) sign-estimator relative variance 1/s^2 - 1 strict growth as average sign s decreases; and (5) explicit scope fences for basis dependence (purely diagonal in the sigma_x eigenbasis), non-applicability to fixed N or bipartite half-filled Hubbard models, and withdrawn HaltingQuotient / GenesisFspBridge fixtures.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-026 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspTroyerWieseReduction.lean`

- file: [lean4/CampaignFspTroyerWieseReduction.lean](../../../lean4/CampaignFspTroyerWieseReduction.lean)
- sha256 (`bytes`): `0d22e9ca5374f2a63da32e3f58adb1394f7aa2f8b6500b5d40c5e88e6b4e81bb`
- cited in: node.lean, receipt dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json (CampaignFspTroyerWieseReduction), record TFQ-1192
- replay: `verified`
  - receipt [dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json](../../../dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json) (module `CampaignFspTroyerWieseReduction`): recorded sha256 `0d22e9ca5374f2a63da32e3f58adb1394f7aa2f8b6500b5d40c5e88e6b4e81bb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspTroyerWieseReduction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspTroyerWieseReduction.frustrated_triangle_minimum_energy_and_degeneracy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.frustrated_triangle_minimum_energy_and_degeneracy` |
| `CampaignFspTroyerWieseReduction.frustrated_triangle_sigma_x_closed_walk_negative_weight` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.frustrated_triangle_sigma_x_closed_walk_negative_weight` |
| `CampaignFspTroyerWieseReduction.ground_energy_threshold_decision_window_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.ground_energy_threshold_decision_window_separation` |
| `CampaignFspTroyerWieseReduction.hadamard_basis_rotation_maps_sigma_z_glass_to_off_diagonal_sigma_x` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.hadamard_basis_rotation_maps_sigma_z_glass_to_off_diagonal_sigma_x` |
| `CampaignFspTroyerWieseReduction.ising_energy_integer_gap_ge_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.ising_energy_integer_gap_ge_two` |
| `CampaignFspTroyerWieseReduction.sign_estimator_variance_amplification_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.sign_estimator_variance_amplification_identity` |
| `CampaignFspTroyerWieseReduction.thermal_excited_state_boltzmann_tail_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.thermal_excited_state_boltzmann_tail_bound` |
| `CampaignFspTroyerWieseReduction.troyer_wiese_does_not_reduce_to_hubbard_or_fixed_N_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.troyer_wiese_does_not_reduce_to_hubbard_or_fixed_N_fence` |
| `CampaignFspTroyerWieseReduction.troyer_wiese_is_basis_dependent_not_intrinsic_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.troyer_wiese_is_basis_dependent_not_intrinsic_fence` |
| `CampaignFspTroyerWieseReduction.withdrawn_halting_and_cochain_arity_fixtures_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTroyerWieseReduction.withdrawn_halting_and_cochain_arity_fixtures_fence` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-troyer-wiese-reduction.py`

- file: [checks/independent/fsp-troyer-wiese-reduction.py](../../../checks/independent/fsp-troyer-wiese-reduction.py)
- sha256 (`bytes`): `da18a8df9fb37ca23305eda95bd43863924ec71108f4b98d866ee94b656469ef`
- cited in: record TFQ-1192

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/bqnf_sign_evaluator.py`

- file: [code/python/src/fsp/bqnf_sign_evaluator.py](../../../code/python/src/fsp/bqnf_sign_evaluator.py)
- sha256 (`bytes`): `6bbc7a71841797e537bf4f62308124325c6f39848c08ee914dfb96187f892f92`
- cited in: record TFQ-1192

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalize_sign_cochain` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md`

- file: [dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md](../../../dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md)
- sha256 (`lf-normalised`): `ebd705859ee77512a2032df4ab4f9c9e8070648f88f0bb11088767c52d182bc9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1192
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-troyer-wiese-reduction.md`

- file: [dag/derivations/independent/fsp-troyer-wiese-reduction.md](../../../dag/derivations/independent/fsp-troyer-wiese-reduction.md)
- sha256 (`lf-normalised`): `e279b1354be9ccfa038163bed10a5e89d485d3e11becbd0ab458cbb7c9bb6daf`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-troyer-wiese-reduction_independent.json`

- file: [dag/research/campaign_fsp-troyer-wiese-reduction_independent.json](../../../dag/research/campaign_fsp-troyer-wiese-reduction_independent.json)
- sha256 (`lf-normalised`): `632ab1f005f8b64fe327b6e229752be932e1b5ca741b2f3acd0df437919f0bf8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-troyer-wiese-reduction_lean_mutation.json`

- file: [dag/research/campaign_fsp-troyer-wiese-reduction_lean_mutation.json](../../../dag/research/campaign_fsp-troyer-wiese-reduction_lean_mutation.json)
- sha256 (`lf-normalised`): `402e5e2cd01e4071a85b8c84b7d6a7ae54ae1ce31cf265e503df2050db8fea1e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json`

- file: [dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json](../../../dag/research/campaign_fsp-troyer-wiese-reduction_lean_replay.json)
- sha256 (`lf-normalised`): `9be46346165a390fa94872b6957a75fd4e44d4833742a648c76c8c7a52a5f804`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-TROYER-WIESE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [FSP-SIGN-ESTIMATOR-VARIANCE](FSP-SIGN-ESTIMATOR-VARIANCE.md) (PROVED_PROSE), [FSP-FREE-TRIANGLE-REPRESENTATION](FSP-FREE-TRIANGLE-REPRESENTATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
