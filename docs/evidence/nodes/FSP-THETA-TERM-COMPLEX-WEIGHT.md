# FSP-THETA-TERM-COMPLEX-WEIGHT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Adding S_theta = i theta Q_top with real lattice charge Q_top multiplies the Boltzmann weight by exp(-i theta Q_top), which is nonreal unless theta Q_top lies in pi Z for every configuration, so positive-weight importance sampling is lost for generic theta != 0.

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

- lattice topological charge Q_top and theta vacuum term (standard)

## Bottleneck

Severity of the resulting sign problem is phenomenology from the literature; the checkout has no theta-term model. Narrowed in lean4/CampaignFspThetaTermComplexWeight.lean and checks/independent/fsp-theta-term-complex-weight.py while keeping status IMPORTED_ASSUMPTION to: (1) integer lattice chiral index Q_top = n_+ - n_- CP antisymmetry Q_top(n_-, n_+) = -Q_top(n_+, n_-) and Q_top(n, n) = 0; (2) rational vacuum angle theta = (p/q) pi divisibility criterion theta Q_top in pi Z iff q | p Q_top, CP-conjugate pair sine cancellation leaving 2 w cos(theta Q_top), and negative paired real weight 2 w c \< 0 whenever w \> 0 and c \< 0; (3) at theta = pi, real parity character sigma_pi(Q) = (-1)^Q homomorphism sigma_pi(Q_1 + Q_2) = sigma_pi(Q_1) sigma_pi(Q_2), two-sector partition sum cancellation Z(pi) = w_0 - w_1 \< Z_pq = w_0 + w_1, action-gap weight separation, and CP-symmetric 3-sector instanton susceptibility second moment sum_Q Q^2 w_Q = 2 w_1 \> 0; and (4) explicit GIN-C9 scope fences for the historical Nat arithmetic inequality w_0 != w_0 + delta_S and against extrapolating finite phase algebra to continuum theta-vacuum phenomenology.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-034 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspThetaTermComplexWeight.lean`

- file: [lean4/CampaignFspThetaTermComplexWeight.lean](../../../lean4/CampaignFspThetaTermComplexWeight.lean)
- sha256 (`bytes`): `b4dd2aa963f7a33c4964b9782da2918d380e12e178abfe0bf507581570e12ade`
- cited in: node.lean, receipt dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json (CampaignFspThetaTermComplexWeight), record TFQ-1198
- replay: `verified`
  - receipt [dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json) (module `CampaignFspThetaTermComplexWeight`): recorded sha256 `b4dd2aa963f7a33c4964b9782da2918d380e12e178abfe0bf507581570e12ade` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspThetaTermComplexWeight`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspThetaTermComplexWeight.cp_conjugate_pair_cancels_imaginary_boltzmann_phase` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.cp_conjugate_pair_cancels_imaginary_boltzmann_phase` |
| `CampaignFspThetaTermComplexWeight.cp_conjugate_pair_negative_real_weight_at_obtuse_phase` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.cp_conjugate_pair_negative_real_weight_at_obtuse_phase` |
| `CampaignFspThetaTermComplexWeight.gin_c9_su2_action_gap_fixture_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.gin_c9_su2_action_gap_fixture_scope_fence` |
| `CampaignFspThetaTermComplexWeight.lattice_chiral_index_cp_antisymmetry` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.lattice_chiral_index_cp_antisymmetry` |
| `CampaignFspThetaTermComplexWeight.rational_pi_theta_real_weight_iff_divisible` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.rational_pi_theta_real_weight_iff_divisible` |
| `CampaignFspThetaTermComplexWeight.su2_vortex_action_gap_sector_weight_ordering` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.su2_vortex_action_gap_sector_weight_ordering` |
| `CampaignFspThetaTermComplexWeight.theta_pi_alternating_sector_sign_homomorphism` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.theta_pi_alternating_sector_sign_homomorphism` |
| `CampaignFspThetaTermComplexWeight.theta_term_phenomenology_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.theta_term_phenomenology_scope_fence` |
| `CampaignFspThetaTermComplexWeight.topological_susceptibility_second_moment_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.topological_susceptibility_second_moment_positivity` |
| `CampaignFspThetaTermComplexWeight.two_sector_theta_pi_partition_cancellation_and_average_sign` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.two_sector_theta_pi_partition_cancellation_and_average_sign` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-theta-term-complex-weight.py`

- file: [checks/independent/fsp-theta-term-complex-weight.py](../../../checks/independent/fsp-theta-term-complex-weight.py)
- sha256 (`bytes`): `a16b2b3ce02cb6c4ca1b58b08b8114057ed61ead9a126ffd29f8ce0984d6f2af`
- cited in: record TFQ-1198

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/cdt_topological_charge_evaluator.py`

- file: [code/python/src/fsp/cdt_topological_charge_evaluator.py](../../../code/python/src/fsp/cdt_topological_charge_evaluator.py)
- sha256 (`bytes`): `5a305f4b2f43f2455242c887840729f7751604f28a5f82147b29964927ce2229`
- cited in: record TFQ-1198

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CdtTopologicalChargeEvaluator` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md`

- file: [dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md](../../../dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md)
- sha256 (`lf-normalised`): `ccc9edec15a5df1a5a76d7a02f15fc66cfa447ed970851b23f94a841b88fa6d1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1198
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-theta-term-complex-weight.md`

- file: [dag/derivations/independent/fsp-theta-term-complex-weight.md](../../../dag/derivations/independent/fsp-theta-term-complex-weight.md)
- sha256 (`lf-normalised`): `32b73bf654690f884c1974c8f30c5d44124ea57aa96fb11a26dc5f055fff5428`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-theta-term-complex-weight_independent.json`

- file: [dag/research/campaign_fsp-theta-term-complex-weight_independent.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_independent.json)
- sha256 (`lf-normalised`): `fff841dc7f04e6f2a7c659d9e30776e4d1ff560e601940cf0c93c184b45a2214`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-theta-term-complex-weight_lean_mutation.json`

- file: [dag/research/campaign_fsp-theta-term-complex-weight_lean_mutation.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_lean_mutation.json)
- sha256 (`lf-normalised`): `a7f6701f2209274da931cee635900e3a51787b49f4787a4b1fbf955577a981f8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json`

- file: [dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json)
- sha256 (`lf-normalised`): `10c4a2f5f4c756ecb003d7d748984fe6485ac21fc2ca16652bf1ca8f91ae49ac`
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

- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)

Outgoing (0):

