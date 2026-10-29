# L1-WDP-CH08-C01-REPLICA-L1

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> l1 appears when aggregation over independent replicas is required to be extensive. WDP 8.5 states that l2 is not excluded by this argument.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- distinct cited Lean declarations covered by a current replay receipt: 25
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No classification is formalised. Checked slice (L1ReplicaScale), Nat arithmetic only: For all natural numbers c, a, and b, c * a + c * b equals c * (a + b), and (c * a) * (c * a) + (c * b) * (c * b) equals (c * c) * (a * a + b * b). On a = 3 and b = 4, a + b = 7, a * a + b * b = 25, 5 * 5 = 25, (a + b) * (a + b) = 49, and 25 is not 49. On c = 2, c * (a + b) = 14, (c * a) * (c * a) + (c * b) * (c * b) = 100, c * (a * a + b * b) = 50, and 100 is not 50. Deriving l1 from replica extensivity, and a reading that l2 is excluded, stay outside this slice. The older citation wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation records finite-sum additivity and the closed facts (2*3)^2+(2*4)^2=100 and 3^2+4^2=5^2, and does not discharge the open reading.

## Source status

Replica extensivity of L1 and L2^2 (WDP 8.5 non-exclusion by extensivity alone), degree-1 homogeneity separation (100 != 50), and disjoint-support norm separation (5 != 3+4) mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-WDP-CH08-C01-REPLICA-L1/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-WDP-CH08-C01-REPLICA-L1/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact concatenated l1, squared energy and coherent scalar-scaling comparisons; general algebraic replication/scaling distinction in Lean.
  - does not support: Specify the source aggregation and independent-replica axioms and prove a classification under them. This does not derive physical replica independence or exclude l2.
  - next test: Specify the source aggregation and independent-replica axioms and prove a classification under them. This does not derive physical replica independence or exclude l2.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation` |

- counts toward the grade: yes

### Lean: `lean4/L1ReplicaScale.lean`

- file: [lean4/L1ReplicaScale.lean](../../../lean4/L1ReplicaScale.lean)
- sha256 (`bytes`): `1fc7062da653143a4f5b81116a49b532bcf8ee20efd72950f74bd5bdf0d79b82`
- cited in: node.lean, receipt dag/research/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json (L1ReplicaScale)
- replay: `verified`
  - receipt [dag/research/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json](../../../dag/research/campaign_l1-wdp-ch08-c01-replica-l1_lean_replay.json) (module `L1ReplicaScale`): recorded sha256 `1fc7062da653143a4f5b81116a49b532bcf8ee20efd72950f74bd5bdf0d79b82` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
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

### Rust: `code/rust/src/wdp/gauge_classification.rs`

- file: [code/rust/src/wdp/gauge_classification.rs](../../../code/rust/src/wdp/gauge_classification.rs)
- sha256 (`bytes`): `938dd12132fd41cdcdc3ebe3daa421dc174de67c1ecc1d9279ae0a05b2f17ef3`
- cited in: record TFQ-0357
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

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md](../../../dag/derivations/07_l1_emergence/tfq_0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md)
- sha256 (`lf-normalised`): `307d4e5f01bdf6e5fe541cbdf0450a4026ca9e48ea4586b223e2643fce6c23bd`
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

- `L1-R-REPLICA-L1` `GAP_NO_DERIVATION`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION)

Outgoing (0):

