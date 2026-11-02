# FSP-HINGE-LINEON-SIGN-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: lineons confined to 1D hinge lines cannot exchange without collision, so their worldlines carry no nontrivial permutations and foliated fracton models are sign free; no model, path expansion or sign computation exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Give a fermionic fracton Hamiltonian, its declared representation and show all path weights nonnegative, including lineons on intersecting hinges; ledger GIN-C24 withdraws the fixture reading.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-055 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FoliatedFracton2Gauge.lean`

- file: [lean4/FoliatedFracton2Gauge.lean](../../../lean4/FoliatedFracton2Gauge.lean)
- sha256 (`bytes`): `94233fe48aa785080384879d7b92735fd6a03e7f4b90973f853c0a04b41c0bc9`
- cited in: node.lean, receipt dag/research/campaign_tfq-1219_lean_replay.json (FoliatedFracton2Gauge), record TFQ-1219
- replay: `verified`
  - receipt [dag/research/campaign_tfq-1219_lean_replay.json](../../../dag/research/campaign_tfq-1219_lean_replay.json) (module `FoliatedFracton2Gauge`): recorded sha256 `94233fe48aa785080384879d7b92735fd6a03e7f4b90973f853c0a04b41c0bc9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FoliatedFracton2Gauge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FoliatedFracton2Gauge.anticommuting_mat2x2_commutator_trace_neg_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FoliatedFracton2Gauge.anticommuting_mat2x2_commutator_trace_neg_two` |
| `FoliatedFracton2Gauge.decoupled_foliated_lineon_sign_free` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.decoupled_foliated_lineon_sign_free` |
| `FoliatedFracton2Gauge.discrete_ivt_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms FoliatedFracton2Gauge.discrete_ivt_zero` |
| `FoliatedFracton2Gauge.foliated_lineon_axis_conservation_forbids_branch_exchange` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.foliated_lineon_axis_conservation_forbids_branch_exchange` |
| `FoliatedFracton2Gauge.hinge_lineon_exchange_collision_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms FoliatedFracton2Gauge.hinge_lineon_exchange_collision_obstruction` |
| `FoliatedFracton2Gauge.hinge_lineon_worldline_permutation_sign_trivial` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.hinge_lineon_worldline_permutation_sign_trivial` |
| `FoliatedFracton2Gauge.hinge_path_exchange_impossible` | yes | yes | yes | Quot.sound, propext | `#print axioms FoliatedFracton2Gauge.hinge_path_exchange_impossible` |
| `FoliatedFracton2Gauge.hinge_path_preserves_relative_order` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.hinge_path_preserves_relative_order` |
| `FoliatedFracton2Gauge.nonabelian_hinge_commutator_curvature_obstruction` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.nonabelian_hinge_commutator_curvature_obstruction` |
| `FoliatedFracton2Gauge.noncommuting_su2_positive_commutator_trace_counterexample` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FoliatedFracton2Gauge.noncommuting_su2_positive_commutator_trace_counterexample` |
| `FoliatedFracton2Gauge.y_junction_collision_free_exchange_exists` | yes | yes | yes | propext | `#print axioms FoliatedFracton2Gauge.y_junction_collision_free_exchange_exists` |
| `FoliatedFracton2Gauge.y_junction_exchange_induces_negative_sign` | yes | yes | yes | none | `#print axioms FoliatedFracton2Gauge.y_junction_exchange_induces_negative_sign` |

- counts toward the grade: yes

### Rust: `code/rust/src/fsp/foliated_fracton_lineon.rs`

- file: [code/rust/src/fsp/foliated_fracton_lineon.rs](../../../code/rust/src/fsp/foliated_fracton_lineon.rs)
- sha256 (`bytes`): `5b8f5f87c2457c6d89219d61ef5d4ea6530288dff25fae5f5898e746cff69ea6`
- cited in: node.rust, record TFQ-1219
- note: no test is cited for this symbol; its crate is tfqm_fsp
- counts toward the grade: yes

### Rust: `code/rust/tests/foliated_fracton_lineon_test.rs`

- file: [code/rust/tests/foliated_fracton_lineon_test.rs](../../../code/rust/tests/foliated_fracton_lineon_test.rs)
- sha256 (`bytes`): `cf260ce2a81817a2348a91cc5c0caa2b56a292436f129d9a67a4dcf3b0d8f700`
- cited in: node.rust, record TFQ-1219
- check: `cd code/rust && cargo test -p theory_of_finite_qm --test foliated_fracton_lineon_test`
- counts toward the grade: yes

### Python: `checks/independent/check_tfq_1219_fsp_hinge_lineon_sign_claim.py`

- file: [checks/independent/check_tfq_1219_fsp_hinge_lineon_sign_claim.py](../../../checks/independent/check_tfq_1219_fsp_hinge_lineon_sign_claim.py)
- sha256 (`bytes`): `d13536813242beff678ef462534b95a1c0f8e3b6b9fa7bac7de552a924cdcf39`
- cited in: node.source, record TFQ-1219
- counts toward the grade: yes

### Python: `code/python/src/fsp/foliated_fracton_2gauge_defects.py`

- file: [code/python/src/fsp/foliated_fracton_2gauge_defects.py](../../../code/python/src/fsp/foliated_fracton_2gauge_defects.py)
- sha256 (`bytes`): `abd511110e7415901937b8bb33cc543fa8df3b62dc732753b0bfbc522391bce4`
- cited in: record TFQ-1219
- counts toward the grade: yes

### Python: `code/python/tests/fsp/integration/test_foliated_fracton_2gauge_defects.py`

- file: [code/python/tests/fsp/integration/test_foliated_fracton_2gauge_defects.py](../../../code/python/tests/fsp/integration/test_foliated_fracton_2gauge_defects.py)
- sha256 (`bytes`): `869bb79dfd49cb430b8158b648e631a1909cd64927b787fcaf4b614a10f4c3a7`
- cited in: record TFQ-1219
- check: `python -m pytest code/python/tests/fsp/integration/test_foliated_fracton_2gauge_defects.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md`

- file: [dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md](../../../dag/derivations/26_fsp/tfq_1219_fsp_hinge_lineon_sign_claim.md)
- sha256 (`lf-normalised`): `de652e3c873f6fda84c9295e2c3f9c8e2d831f963e5d725566859c020da86119`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1219
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `d3b0b4deaf2b1c09ac29ba3e3206a2f6f832b7525b092992c8a6f72ed8a62dfb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-HINGE-LINEON-SIGN-CLAIM` `COMPUTED`: [FSP-FRACTON-MOBILITY](FSP-FRACTON-MOBILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
