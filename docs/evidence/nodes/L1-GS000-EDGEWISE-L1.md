# L1-GS000-EDGEWISE-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Weighted two-edge l1 decomposition, exact transposition defect and l-infinity disjoint-additivity countercontrols; general transposition algebra under positive coordinates.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Thm 1 coordinatewise weighted L1 decomposition, Thm 2 symmetry orbit-constancy, Thm 3 edge-transitive collapse, and CE1-CE5 drop-one countermodels mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/L1-GS000-EDGEWISE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-GS000-EDGEWISE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Weighted two-edge l1 decomposition, exact transposition defect and l-infinity disjoint-additivity countercontrols; general transposition algebra under positive coordinates.
  - does not support: Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness.
  - next test: Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels` |
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity/lean4/gs003_coordinate_l1.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity/lean4/gs003_coordinate_l1.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Lean: `sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: [sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean](../../../sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `a2ec0a203277c5c7b4bd71067351c574509c655c18bf0e08fe3c05a8005fc497`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `bc047a1c21f261ec1a8240d4dc42e455608ed060c0a1719a8e37a492d6d51591`
- cited in: record TFQ-0353
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0354 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

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

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md`

- file: [dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md](../../../dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md)
- sha256 (`lf-normalised`): `728346e31e7df2e97cc5cc1c296f42bfec0931ae5bc86fa107641dc40ce8193e`
- generated view: listed, not counted
- cited in: record TFQ-0353
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md](../../../dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)
- sha256 (`lf-normalised`): `18700eae8449b13f08c61fadbbcd7fb803c6f31ab445adda49326decd63e389b`
- generated view: listed, not counted
- cited in: record TFQ-0354 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity/coordinate_wise_additivity_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity/coordinate_wise_additivity_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0353 python: no local python twin located for omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/tests_unit/test_so_k_gauge.py

## Routes

Incoming (1):

- `L1-R-OBSERVER-TO-GS000` `DERIVED_LEAN`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (4):

- `L1-R-INNER-PRODUCT-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)
- `L1-R-ORTHOGONAL-ADDITIVITY-GAP` `GAP_NO_DERIVATION`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-RESIDUAL-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
