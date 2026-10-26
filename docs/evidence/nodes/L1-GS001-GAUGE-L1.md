# L1-GS001-GAUGE-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On two integer coordinates, for all integers x, y, and k and every coordinate swap and pair of coordinate signs, the aggregate |x| + |y| is unchanged by that signed permutation, equals |x| + |0| plus |0| + |y|, and after scaling both coordinates by k equals |k| times (|x| + |y|). The eight signed permutations send (1, 2) to (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), and (-2, -1), and these eight pairs are distinct, so equal images of (1, 2) force equal bit choices. For natural weights w1 and w2, w1 |x| + w2 |y| is unchanged by swapping the two coordinates for every integer pair if and only if w1 = w2, and in that case it equals w1 times (|x| + |y|). The weights 1 and 2 give 1 on (1, 0) and 2 on (0, 1). The pairs (3, 4) and (5, 0) both have squared length 25, and their aggregates are 7 and 5.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- distinct cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Two integer coordinates only. A faithful, edge-additive, maximal bounded-linear symmetry on a general gauge presentation is not derived, and weighted l1 is not obtained as that symmetry outer aggregation. Route L1-R-GS001 from L1-OBSERVER-AXIOMS-H1-H5 stays GAP_NO_DERIVATION. The conditional norming package in gs001_maximal_symmetry_direction_independence_and_gauge_proportionality remains a hypothesis package.

## Source status

Tier-1 direction independence (Lemma 4.1), gauge proportionality (Corollary 2), single-orbit uniform collapse (Theorem 4.2), and ENC-0523 drop-one counterexamples mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-GS001-GAUGE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-GS001-GAUGE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All eight signed-permutation gauge values, swap anisotropy, and equal-length direction countercontrol; exact sign/swap laws in Lean.
  - does not support: Establish the actual maximal bounded-linear symmetry and faithful edge-additive hypotheses; do not infer them from an eight-element test.
  - next test: Establish the actual maximal bounded-linear symmetry and faithful edge-additive hypotheses; do not infer them from an eight-element test.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignL1Gs001GaugeL1.lean`

- file: [lean4/CampaignL1Gs001GaugeL1.lean](../../../lean4/CampaignL1Gs001GaugeL1.lean)
- sha256 (`bytes`): `bf153360fcc3e39bfd6804c81ec821e576b85dbc4bd3cceab98f8835e55df7d7`
- cited in: node.lean, receipt dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json (CampaignL1Gs001GaugeL1)
- replay: `verified`
  - receipt [dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json](../../../dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json) (module `CampaignL1Gs001GaugeL1`): recorded sha256 `bf153360fcc3e39bfd6804c81ec821e576b85dbc4bd3cceab98f8835e55df7d7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignL1Gs001GaugeL1`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignL1Gs001GaugeL1.absolutely_homogeneous` | yes | yes | yes | propext | `#print axioms CampaignL1Gs001GaugeL1.absolutely_homogeneous` |
| `CampaignL1Gs001GaugeL1.edge_additive` | yes | yes | yes | propext | `#print axioms CampaignL1Gs001GaugeL1.edge_additive` |
| `CampaignL1Gs001GaugeL1.eight_images_of_one_two` | yes | yes | yes | none | `#print axioms CampaignL1Gs001GaugeL1.eight_images_of_one_two` |
| `CampaignL1Gs001GaugeL1.equal_squared_length_splits_l1` | yes | yes | yes | none | `#print axioms CampaignL1Gs001GaugeL1.equal_squared_length_splits_l1` |
| `CampaignL1Gs001GaugeL1.equal_weight_is_scaled_l1` | yes | yes | yes | propext | `#print axioms CampaignL1Gs001GaugeL1.equal_weight_is_scaled_l1` |
| `CampaignL1Gs001GaugeL1.faithful_on_one_two` | yes | yes | yes | propext | `#print axioms CampaignL1Gs001GaugeL1.faithful_on_one_two` |
| `CampaignL1Gs001GaugeL1.signed_permutation_gauge_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignL1Gs001GaugeL1.signed_permutation_gauge_shadow` |
| `CampaignL1Gs001GaugeL1.signed_permutation_preserves_l1` | yes | yes | yes | propext | `#print axioms CampaignL1Gs001GaugeL1.signed_permutation_preserves_l1` |
| `CampaignL1Gs001GaugeL1.swap_invariant_weighted_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignL1Gs001GaugeL1.swap_invariant_weighted_iff` |
| `CampaignL1Gs001GaugeL1.unequal_weights_separate_axes` | yes | yes | yes | none | `#print axioms CampaignL1Gs001GaugeL1.unequal_weights_separate_axes` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `bc047a1c21f261ec1a8240d4dc42e455608ed060c0a1719a8e37a492d6d51591`
- cited in: record TFQ-0356
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/gauge_classification.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/gauge_classification.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/projection_obstruction/m_compatible_gauge_classification`

- file: [atlas/papers/projection_obstruction/m_compatible_gauge_classification](../../../atlas/papers/projection_obstruction/m_compatible_gauge_classification)
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0356_keep_the_m_compatible_gauge_route_to_weighted_l1_on_its_own_hypothesis.md`

- file: [dag/derivations/07_l1_emergence/tfq_0356_keep_the_m_compatible_gauge_route_to_weighted_l1_on_its_own_hypothesis.md](../../../dag/derivations/07_l1_emergence/tfq_0356_keep_the_m_compatible_gauge_route_to_weighted_l1_on_its_own_hypothesis.md)
- sha256 (`lf-normalised`): `5825aea62937e055e1b3686055c0ede7cabf845f58e78b41f0c2c6b724163bf9`
- generated view: listed, not counted
- cited in: record TFQ-0356
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0356 python: no local python twin located for omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/tests_unit/test_m_compatible_gauge.py

## Routes

Incoming (1):

- `L1-R-GS001` `GAP_NO_DERIVATION`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (0):

