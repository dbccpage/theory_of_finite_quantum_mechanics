# L1-GS001-GAUGE-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A faithful, edge-additive, maximal bounded-linear symmetry on the gauge presentation gives weighted l1 as the outer aggregation. Alternative route to l1 to L1-GS000-EDGEWISE-L1, with a different hypothesis set.

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

Checked slice (L1SignedPermutationGauge), two integer coordinates only: On two integer coordinates, for all integers x, y, and k and every coordinate swap and pair of coordinate signs, the aggregate |x| + |y| is unchanged by that signed permutation, equals |x| + |0| plus |0| + |y|, and after scaling both coordinates by k equals |k| times (|x| + |y|). The eight signed permutations send (1, 2) to (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), and (-2, -1), and these eight pairs are distinct, so equal images of (1, 2) force equal bit choices. For natural weights w1 and w2, w1 |x| + w2 |y| is unchanged by swapping the two coordinates for every integer pair if and only if w1 = w2, and in that case it equals w1 times (|x| + |y|). The weights 1 and 2 give 1 on (1, 0) and 2 on (0, 1). The pairs (3, 4) and (5, 0) both have squared length 25, and their aggregates are 7 and 5. A faithful, edge-additive, maximal bounded-linear symmetry on a general gauge presentation is not derived, and weighted l1 is not obtained as that symmetry outer aggregation. Route L1-R-GS001 from L1-OBSERVER-AXIOMS-H1-H5 stays GAP_NO_DERIVATION. The conditional norming package in gs001_maximal_symmetry_direction_independence_and_gauge_proportionality remains a hypothesis package.

## Source status

Tier-1 direction independence (Lemma 4.1), gauge proportionality (Corollary 2), single-orbit uniform collapse (Theorem 4.2), and ENC-0523 drop-one counterexamples mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-GS001-GAUGE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-GS001-GAUGE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All eight signed-permutation gauge values, swap anisotropy, and equal-length direction countercontrol; exact sign/swap laws in Lean.
  - does not support: Establish the actual maximal bounded-linear symmetry and faithful edge-additive hypotheses; do not infer them from an eight-element test.
  - next test: Establish the actual maximal bounded-linear symmetry and faithful edge-additive hypotheses; do not infer them from an eight-element test.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/L1SignedPermutationGauge.lean`

- file: [lean4/L1SignedPermutationGauge.lean](../../../lean4/L1SignedPermutationGauge.lean)
- sha256 (`bytes`): `e4a66a1f3bbbeab211980d213bcfb68daf75ed2a9927e690730c4bb448a2ba65`
- cited in: node.lean, receipt dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json (L1SignedPermutationGauge)
- replay: `verified`
  - receipt [dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json](../../../dag/research/campaign_l1-gs001-gauge-l1_lean_replay.json) (module `L1SignedPermutationGauge`): recorded sha256 `e4a66a1f3bbbeab211980d213bcfb68daf75ed2a9927e690730c4bb448a2ba65` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build L1SignedPermutationGauge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1SignedPermutationGauge.absolutely_homogeneous` | yes | yes | yes | propext | `#print axioms L1SignedPermutationGauge.absolutely_homogeneous` |
| `L1SignedPermutationGauge.edge_additive` | yes | yes | yes | propext | `#print axioms L1SignedPermutationGauge.edge_additive` |
| `L1SignedPermutationGauge.eight_images_of_one_two` | yes | yes | yes | none | `#print axioms L1SignedPermutationGauge.eight_images_of_one_two` |
| `L1SignedPermutationGauge.equal_squared_length_splits_l1` | yes | yes | yes | none | `#print axioms L1SignedPermutationGauge.equal_squared_length_splits_l1` |
| `L1SignedPermutationGauge.equal_weight_is_scaled_l1` | yes | yes | yes | propext | `#print axioms L1SignedPermutationGauge.equal_weight_is_scaled_l1` |
| `L1SignedPermutationGauge.faithful_on_one_two` | yes | yes | yes | propext | `#print axioms L1SignedPermutationGauge.faithful_on_one_two` |
| `L1SignedPermutationGauge.signed_permutation_gauge_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms L1SignedPermutationGauge.signed_permutation_gauge_shadow` |
| `L1SignedPermutationGauge.signed_permutation_preserves_l1` | yes | yes | yes | propext | `#print axioms L1SignedPermutationGauge.signed_permutation_preserves_l1` |
| `L1SignedPermutationGauge.swap_invariant_weighted_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms L1SignedPermutationGauge.swap_invariant_weighted_iff` |
| `L1SignedPermutationGauge.unequal_weights_separate_axes` | yes | yes | yes | none | `#print axioms L1SignedPermutationGauge.unequal_weights_separate_axes` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `938dd12132fd41cdcdc3ebe3daa421dc174de67c1ecc1d9279ae0a05b2f17ef3`
- cited in: record TFQ-0356
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

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
- sha256 (`lf-normalised`): `8273cf40e3c9e3da7c4a8b88e01c641b5672367ea2a3d539532bfc9063826508`
- generated view: listed, not counted
- cited in: record TFQ-0356
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`
- `external:sha256:97b89a12d973cc3fa80d33c83b782f78b54982645db2d58ab9c4ac58c98aed40::standard_l1`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`

## Absences recorded by the TFQ records

- TFQ-0356 python: no local python twin located for external:sha256:d962d12328cc1c600be34fe639ca170247c351ec5cafdf48ea450d608d3d4e15

## Routes

Incoming (1):

- `L1-R-GS001` `GAP_NO_DERIVATION`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (0):

