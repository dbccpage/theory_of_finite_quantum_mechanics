# L1-GS000-EDGEWISE-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under H1-H5 the aggregate seminorm is an edgewise weighted l1 sum (Thm 1), with orbit-constant weights under graph symmetry (Thm 2); with edge-transitivity the weights collapse to unweighted l1 (Thm 3). Counterexamples CE1-CE5 show each axiom is used.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 2 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Lean states only fixed small cases: a two-edge weighted l1 sum, a three-coordinate seminorm that is additive and homogeneous by hypothesis, and the l-infinity counterexample on two coordinates. Theorems 1 to 3 under H1-H5 on a general edge set, and the counterexamples CE1-CE5, are not in Lean.

## Source status

Thm 1 coordinatewise weighted L1 decomposition, Thm 2 symmetry orbit-constancy, Thm 3 edge-transitive collapse, and CE1-CE5 drop-one countermodels mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-GS000-EDGEWISE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-GS000-EDGEWISE-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Weighted two-edge l1 decomposition, exact transposition defect and l-infinity disjoint-additivity countercontrols; general transposition algebra under positive coordinates.
  - does not support: Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness.
  - next test: Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/Imported/CoordinateWiseAdditivity/gs003_coordinate_l1.lean`

- file: [lean4/Imported/CoordinateWiseAdditivity/gs003_coordinate_l1.lean](../../../lean4/Imported/CoordinateWiseAdditivity/gs003_coordinate_l1.lean)
- sha256 (`bytes`): `07ccbbad40edfdf33388fed09c701273fb3ef1e3ce3ae4ab7557d038dd17a42a`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_emergence.json](../../../dag/research/lean_replay_campaign_l1_emergence.json) (module `Imported.CoordinateWiseAdditivity.gs003_coordinate_l1`): recorded sha256 `07ccbbad40edfdf33388fed09c701273fb3ef1e3ce3ae4ab7557d038dd17a42a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/CoordinateWiseAdditivity/gs003_coordinate_l1.lean`
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `938dd12132fd41cdcdc3ebe3daa421dc174de67c1ecc1d9279ae0a05b2f17ef3`
- cited in: record TFQ-0353
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `30b2b590d0fb59ab9f01eb5f5ee924651ae5c2d391628a48ec57b88f3620fc29`
- cited in: record TFQ-0354 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

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

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md`

- file: [dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md](../../../dag/derivations/07_l1_emergence/tfq_0353_under_admitted_h1_h5_record_an_edgewise_weighted_l1_aggregate_orbit_constant_weights_and.md)
- sha256 (`lf-normalised`): `50e79d3778e964374a776a2588c86b6498ff2b32ed5cdd5bd59ac1865ab85833`
- generated view: listed, not counted
- cited in: record TFQ-0353
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md](../../../dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)
- sha256 (`lf-normalised`): `d4531de0213a9426dd4e3025c034634a7373aed0a94d9b8eb21bcf4f662e1e65`
- generated view: listed, not counted
- cited in: record TFQ-0354 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:97b89a12d973cc3fa80d33c83b782f78b54982645db2d58ab9c4ac58c98aed40::standard_l1`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`

## Absences recorded by the TFQ records

- TFQ-0353 python: no local python twin located for external:sha256:63fe87b0f4001f63e4cf817c382c38036c636bef507dc306d07320cdf814f817

## Routes

Incoming (1):

- `L1-R-OBSERVER-TO-GS000` `COMPUTED`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (4):

- `L1-R-INNER-PRODUCT-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)
- `L1-R-ORTHOGONAL-ADDITIVITY-GAP` `GAP_NO_DERIVATION`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-ORTHOGONAL-ADDITIVITY-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)
- `L1-R-RESIDUAL-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
