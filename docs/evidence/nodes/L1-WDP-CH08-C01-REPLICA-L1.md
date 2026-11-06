# L1-WDP-CH08-C01-REPLICA-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> l1 appears when aggregation over independent replicas is required to be extensive. WDP 8.5 states that l2 is not excluded by this argument.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 30
- distinct cited Lean declarations covered by a current replay receipt: 25
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Finite replica additivity and degree-1 positive homogeneity mechanized over Q in WdpBatch5.lean; continuum Banach space characterizations remain outside finite scope.

## Source status

Replica extensivity of L1 and L2^2, degree-1 homogeneity of L1 vs L2^2, and un-squared L2 non-additivity mechanized in WdpBatch5.lean and DerivationDagQMClosure.lean

## Review

- PFP review: [evidence/results/L1-WDP-CH08-C01-REPLICA-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../evidence/results/L1-WDP-CH08-C01-REPLICA-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact concatenated l1, squared energy and coherent scalar-scaling comparisons; general algebraic replication/scaling distinction in Lean.
  - does not support: Specify the source aggregation and independent-replica axioms and prove a classification under them. This does not derive physical replica independence or exclude l2.
  - next test: Specify the source aggregation and independent-replica axioms and prove a classification under them. This does not derive physical replica independence or exclude l2.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch5.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch5.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch5.lean)
- sha256 (`bytes`): `dcfbb2733e10b50e5582e2c8f7b3d9ce8220a199280cd4a2db35b573940f0b99`
- cited in: node.lean, record TFQ-0357
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch5.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch5.l1_and_l2sq_disjoint_replica_additive` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch5.l1_and_l2sq_disjoint_replica_additive` |
| `WitnessedDifference.WdpBatch5.l1_degree_one_homogeneous` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch5.l1_degree_one_homogeneous` |
| `WitnessedDifference.WdpBatch5.l2sq_fails_degree_one_homogeneity` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch5.l2sq_fails_degree_one_homogeneity` |
| `WitnessedDifference.WdpBatch5.unsquared_l2_fails_disjoint_additivity` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch5.unsquared_l2_fails_disjoint_additivity` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_finite_qm_structure.json](../../../evidence/lean_receipts/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation` |

- counts toward the grade: yes

### Lean: `lean4/L1ReplicaScale.lean`

- file: [lean4/L1ReplicaScale.lean](../../../lean4/L1ReplicaScale.lean)
- sha256 (`bytes`): `1fc7062da653143a4f5b81116a49b532bcf8ee20efd72950f74bd5bdf0d79b82`
- cited in: node.lean, receipt evidence/lean_receipts/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json (L1ReplicaScale)
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json](../../../evidence/lean_receipts/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json) (module `L1ReplicaScale`): recorded sha256 `1fc7062da653143a4f5b81116a49b532bcf8ee20efd72950f74bd5bdf0d79b82` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build L1ReplicaScale`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `L1ReplicaScale.sampleFive` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleFive` |
| `L1ReplicaScale.sampleLinearScale` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleLinearScale` |
| `L1ReplicaScale.sampleScaledNeLinear` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleScaledNeLinear` |
| `L1ReplicaScale.sampleScaledSquares` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleScaledSquares` |
| `L1ReplicaScale.sampleScaledSum` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleScaledSum` |
| `L1ReplicaScale.sampleSquares` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleSquares` |
| `L1ReplicaScale.sampleSquaresNeSumSquare` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleSquaresNeSumSquare` |
| `L1ReplicaScale.sampleSum` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleSum` |
| `L1ReplicaScale.sampleSumSquare` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.sampleSumSquare` |
| `L1ReplicaScale.scaleSquares` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.scaleSquares` |
| `L1ReplicaScale.scaleSum` | yes | yes | yes | module-level | `#print axioms L1ReplicaScale.scaleSum` |
| `sampleFive` | yes | yes | yes | none | `#print axioms sampleFive` |
| `sampleLinearScale` | yes | yes | yes | none | `#print axioms sampleLinearScale` |
| `sampleScaledNeLinear` | yes | yes | yes | none | `#print axioms sampleScaledNeLinear` |
| `sampleScaledSquares` | yes | yes | yes | none | `#print axioms sampleScaledSquares` |
| `sampleScaledSum` | yes | yes | yes | none | `#print axioms sampleScaledSum` |
| `sampleSquares` | yes | yes | yes | none | `#print axioms sampleSquares` |
| `sampleSquaresNeSumSquare` | yes | yes | yes | none | `#print axioms sampleSquaresNeSumSquare` |
| `sampleSum` | yes | yes | yes | none | `#print axioms sampleSum` |
| `sampleSumSquare` | yes | yes | yes | none | `#print axioms sampleSumSquare` |
| `scaleSquares` | yes | yes | yes | propext | `#print axioms scaleSquares` |
| `scaleSum` | yes | yes | yes | none | `#print axioms scaleSum` |

- counts toward the grade: yes

### Rust: `atlas/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [atlas/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../atlas/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `938dd12132fd41cdcdc3ebe3daa421dc174de67c1ecc1d9279ae0a05b2f17ef3`
- cited in: record TFQ-0357
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md](../../../dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md)
- sha256 (`lf-normalised`): `7b50af7f039b3f11dd94fbfae93523dc43bf8c665ab5375ce27b7d7757b04be7`
- generated view: listed, not counted
- cited in: record TFQ-0357
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`

## Routes

Incoming (1):

- `L1-R-REPLICA-L1` `DERIVED_LEAN`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION)

Outgoing (0):

