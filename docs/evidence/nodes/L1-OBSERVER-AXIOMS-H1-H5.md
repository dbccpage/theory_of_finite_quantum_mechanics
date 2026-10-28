# L1-OBSERVER-AXIOMS-H1-H5

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `ADMITTED_PRIMITIVE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared observer axioms on a finite edge-indexed projection: H1 edge locality, H2 coordinate permutation symmetry, H3 disjoint-coordinate additivity, H4 graph-isomorphism invariance with an l1-isometric fiber action, H5 seminorm homogeneity. They are inputs to the l1 classification results, not consequences of Genesis.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- observer / role packet with finite local scope: assumption
- real-valued seminorm on edge fibers: assumption

## Bottleneck

No derivation of H1-H5 from Genesis / MSS-0 found in the sources read. Expect an observer node in the WDP fragment (see cross_refs).

## Source status

GS-000 declared axioms H1-H5

## Review

- PFP review: [dag/results/L1-OBSERVER-AXIOMS-H1-H5/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-OBSERVER-AXIOMS-H1-H5/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `ADMITTED_PRIMITIVE`; qualifies for E4: yes.
  - narrowest claim: Exact named rival defects and admitted weighted aggregate controls, with l-infinity and squared-energy counterexamples in Lean.
  - does not support: State and prove all observer axioms on the full finite projection and derive the conditional classification; these samples do not establish general axioms.
  - next test: State and prove all observer axioms on the full finite projection and derive the conditional classification; these samples do not establish general axioms.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` |
| `QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `938dd12132fd41cdcdc3ebe3daa421dc174de67c1ecc1d9279ae0a05b2f17ef3`
- cited in: record TFQ-0352
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

### Documents and data: `atlas/papers/projection_obstruction/coordinate_wise_additivity/coordinate_wise_additivity_claim_ledger.md`

- file: [atlas/papers/projection_obstruction/coordinate_wise_additivity/coordinate_wise_additivity_claim_ledger.md](../../../atlas/papers/projection_obstruction/coordinate_wise_additivity/coordinate_wise_additivity_claim_ledger.md)
- sha256 (`lf-normalised`): `8419cdbe706a67b721f246acc93e1875ec692fb3ce05329669221efda32afb29`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0352_admit_h1_through_h5_as_observer_hypotheses_on_a_finite_edge_projection.md`

- file: [dag/derivations/07_l1_emergence/tfq_0352_admit_h1_through_h5_as_observer_hypotheses_on_a_finite_edge_projection.md](../../../dag/derivations/07_l1_emergence/tfq_0352_admit_h1_through_h5_as_observer_hypotheses_on_a_finite_edge_projection.md)
- sha256 (`lf-normalised`): `e0fc4b5e256526f92bcd7823125ae8c7e8e764796655c9c132a7d89b86684213`
- generated view: listed, not counted
- cited in: record TFQ-0352
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:97b89a12d973cc3fa80d33c83b782f78b54982645db2d58ab9c4ac58c98aed40::standard_l1`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`

## Routes

Incoming (0):


Outgoing (5):

- `DS-R-AUTHORITY-FIREWALL` `COMPUTED`: [DS-QM090-092-AUTHORITY-FIREWALL](DS-QM090-092-AUTHORITY-FIREWALL.md) (COMPUTATIONALLY_CHECKED)
- `IMPL-R-LGGR-FINITE-RESULTS` `DERIVED_LEAN`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)
- `L1-R-GS001` `GAP_NO_DERIVATION`: [L1-GS001-GAUGE-L1](L1-GS001-GAUGE-L1.md) (OPEN)
- `L1-R-OBSERVER-TO-GS000` `COMPUTED`: [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (COMPUTATIONALLY_CHECKED)
- `OPS-R-OBSERVER-TUPLE-2` `GAP_NO_DERIVATION`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)

No incoming route.
