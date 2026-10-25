# FSP-FIBONACCI-ANYON-DATA

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Fibonacci category has fusion tau x tau = 1 + tau, quantum dimension d_tau = (1 + sqrt 5)/2 (irrational), F and R matrices solving the pentagon and hexagon equations, and three-anyon braids generate a dense subgroup of SU(2) (Freedman-Larsen-Wang).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Fibonacci modular tensor category data (literature)

## Bottleneck

The JSONL calls d_tau rational, which is false; the claim that braiding avoids sign degradation has no content here. Exact ribbon data are pinned elsewhere in the trunk (TFQ-0050), not in this package. Narrowed in lean4/CampaignFspFibonacciAnyonData.lean and checks/independent/fsp-fibonacci-anyon-data.py while keeping status IMPORTED_ASSUMPTION to: (1) exact Fibonacci fusion associativity sum_e N_{a,b}^e N_{e,c}^d = sum_f N_{a,f}^d N_{b,c}^f across all 16 quadruples (a,b,c,d) in {0,1}^4 and Fibonacci fusion channel growth fibSeq(n+2) = fibSeq(n+1) + fibSeq(n) with fibSeq(3) = 2; (2) exact golden-ratio ring Z\[phi\] (phi^2 = 1 + phi) identities for quantum dimensions d_1^2 + d_tau^2 = 2 + phi, inverse phi * phi^-1 = 1, F-matrix row normalization phi^-2 + phi^-1 = 1, and computational-basis state leakage phi^-3 * (2 + phi^-1) = phi^-1 = phi - 1; (3) 2x2 symmetric reflection F-matrix zero trace, orthogonality, and diagonal square (u^2 + v^2) I_2, plus involutive braid word reduction F(FR) = R under F^2 = I_2; (4) Mac Lane 5-term pentagon equation across all 512 4-anyon fusion trees and Artin braid relation sigma_1 sigma_2 sigma_1 == sigma_2 sigma_1 sigma_2; and (5) explicit GIN-C17 scope fences showing Pauli-Z involution non-commutativity (\[M, Xi\])_{01} = -2 M_{01} != 0, bounded non-square checks (2p - q)^2 != 5 q^2 for p,q in \[1..25\] refuting the source JSONL's rational d_tau wording, and non-injectivity of the 2D Fibonacci braid fixture with respect to microscopic fermion sign theorems.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-045 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspFibonacciAnyonData.lean`

- file: [lean4/CampaignFspFibonacciAnyonData.lean](../../../lean4/CampaignFspFibonacciAnyonData.lean)
- sha256 (`bytes`): `3568629c46eddde0416562784c300d42a8d7bbed9af8848edc7e13c9c26c4728`
- cited in: node.lean, receipt dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json (CampaignFspFibonacciAnyonData), record TFQ-1209
- replay: `verified`
  - receipt [dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json](../../../dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json) (module `CampaignFspFibonacciAnyonData`): recorded sha256 `3568629c46eddde0416562784c300d42a8d7bbed9af8848edc7e13c9c26c4728` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspFibonacciAnyonData`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspFibonacciAnyonData.artin_braid_word_involutive_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.artin_braid_word_involutive_reduction` |
| `CampaignFspFibonacciAnyonData.fib_f_matrix_orthogonality_and_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fib_f_matrix_orthogonality_and_involution` |
| `CampaignFspFibonacciAnyonData.fib_fusion_associativity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fib_fusion_associativity` |
| `CampaignFspFibonacciAnyonData.fib_fusion_dimension_recurrence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fib_fusion_dimension_recurrence` |
| `CampaignFspFibonacciAnyonData.fib_leakage_algebraic_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fib_leakage_algebraic_identity` |
| `CampaignFspFibonacciAnyonData.fib_phi_inverse_and_square_identities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fib_phi_inverse_and_square_identities` |
| `CampaignFspFibonacciAnyonData.fibonacci_fusion_space_growth` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.fibonacci_fusion_space_growth` |
| `CampaignFspFibonacciAnyonData.five_not_rational_square_bounded_grid` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.five_not_rational_square_bounded_grid` |
| `CampaignFspFibonacciAnyonData.gin_c17_historical_fixture_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.gin_c17_historical_fixture_scope_fence` |
| `CampaignFspFibonacciAnyonData.pauli_z_involution_commutator_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspFibonacciAnyonData.pauli_z_involution_commutator_obstruction` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-fibonacci-anyon-data.py`

- file: [checks/independent/fsp-fibonacci-anyon-data.py](../../../checks/independent/fsp-fibonacci-anyon-data.py)
- sha256 (`bytes`): `2b50ff1eace50824669ed4943fce22e9f63873beb7e33b2019dbaf5d25f28ad5`
- cited in: record TFQ-1209

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/fibonacci_anyon_braiding.py`

- file: [code/python/src/fsp/fibonacci_anyon_braiding.py](../../../code/python/src/fsp/fibonacci_anyon_braiding.py)
- sha256 (`bytes`): `056332892a8e42c5054d1692abdb00b093ec3cb7ecd19adb7d2b6add95f9f76a`
- cited in: record TFQ-1209

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FibonacciAnyonBraidingEngine` (python_symbol) | yes | yes | yes | - | - |
| `FibonacciAnyonModel` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1209_fsp_fibonacci_anyon_data.md`

- file: [dag/derivations/26_fsp/tfq_1209_fsp_fibonacci_anyon_data.md](../../../dag/derivations/26_fsp/tfq_1209_fsp_fibonacci_anyon_data.md)
- sha256 (`lf-normalised`): `4a3365896aa90cb091e83d991f410a47b94794d470905f5127ab363b8f0706d4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1209
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-fibonacci-anyon-data.md`

- file: [dag/derivations/independent/fsp-fibonacci-anyon-data.md](../../../dag/derivations/independent/fsp-fibonacci-anyon-data.md)
- sha256 (`lf-normalised`): `800d10c2134cfe7b194c285faddd4250cea3f83b2c9d714f1ca3f8ac5774044e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fibonacci-anyon-data_independent.json`

- file: [dag/research/campaign_fsp-fibonacci-anyon-data_independent.json](../../../dag/research/campaign_fsp-fibonacci-anyon-data_independent.json)
- sha256 (`lf-normalised`): `e97969b3cf32c4fb7f4e5a64b8eaaddb0a537148a7647f946b957d93dcf721fe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fibonacci-anyon-data_lean_mutation.json`

- file: [dag/research/campaign_fsp-fibonacci-anyon-data_lean_mutation.json](../../../dag/research/campaign_fsp-fibonacci-anyon-data_lean_mutation.json)
- sha256 (`lf-normalised`): `0062fac268a0898e4fb7225854664e851e16423d59c956f47755a3fef782b6e5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json`

- file: [dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json](../../../dag/research/campaign_fsp-fibonacci-anyon-data_lean_replay.json)
- sha256 (`lf-normalised`): `a5a04227cdf2b03dac54f8bc953bdc23163f59c30f04eb3aa788aa2f07fdbd8f`
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

- `APP-R-FSP-FIBONACCI-ANYON-DATA` `CONDITIONAL_ON_IMPORT`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

