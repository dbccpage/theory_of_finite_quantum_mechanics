# DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If declared threshold hypotheses hold at the target workload and p_pair -\> 0, the projection-obstruction conditional no-go does not follow. The threshold theorem itself is cited as standard, not re-proved. The rate inequality mu_repair \>= lambda_proj at scale is open; physical scalability is not claimed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A conditional record citing the standard threshold theorem. The cited Lean evaluates a declared Boolean certificate; the rate inequality at scale is open.

## Source status

QM-101-C1..C10 threshold repair-image monotonicity (B subseteq B' implies uncorrectable fault indicator non-increasing), 5-obligation conditional no-go suppression equivalence, and sub-threshold vs super-threshold geometric scaling mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact finite backlog trajectories and declared gate controls are checked; lambda\<=mu implies non-increasing natural backlog in Lean.
  - does not support: Supply actual workload/noise/overhead assumptions, scaled repair rates and a p_pair convergence argument or the correctly cited threshold theorem. This toy queue is not a threshold theorem.
  - next test: Supply actual workload/noise/overhead assumptions, scaled repair rates and a p_pair convergence argument or the correctly cited threshold theorem. This toy queue is not a threshold theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary` |

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

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0269_threshold_theorems_read_as_repair_capacity_certificates.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0269_threshold_theorems_read_as_repair_capacity_certificates.md](../../../dag/derivations/13_finite_qm_information/tfq_0269_threshold_theorems_read_as_repair_capacity_certificates.md)
- sha256 (`lf-normalised`): `53ac8ebb78a7261620abd1462a51d2d63f4be89bb43a8105f6c07afb43175092`
- generated view: listed, not counted
- cited in: record TFQ-0269
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/101_threshold_theorems_as_repair_capacity_certificates/qm_101_threshold_theorems_as_repair_capacity_certificates_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/101_threshold_theorems_as_repair_capacity_certificates/qm_101_threshold_theorems_as_repair_capacity_certificates_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0269 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `DS-R-THRESHOLD` `GAP_NO_DERIVATION`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN)

Outgoing (6):

- `APP-R-QCV-IMPORT-NOISY-REVERSIBLE-LIMITS` `CONDITIONAL_ON_IMPORT`: [QCV-IMPORT-NOISY-REVERSIBLE-LIMITS](QCV-IMPORT-NOISY-REVERSIBLE-LIMITS.md) (IMPORTED_ASSUMPTION)
- `APP-R-QCV-IMPORT-THRESHOLD-THEOREM` `CONDITIONAL_ON_IMPORT`: [QCV-IMPORT-THRESHOLD-THEOREM](QCV-IMPORT-THRESHOLD-THEOREM.md) (IMPORTED_ASSUMPTION)
- `APP-R-QCV-QUESTION-SELF-LIMITING-REPAIR` `GAP_NO_DERIVATION`: [QCV-QUESTION-SELF-LIMITING-REPAIR](QCV-QUESTION-SELF-LIMITING-REPAIR.md) (OPEN)
- `APP-R-QCV-SELF-OBSTRUCTION-MODEL` `DERIVED_PROSE`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)
- `DS-R-CAPACITY` `COMPUTED`: [DS-QM102-SYNDROME-CAPACITY-BOUND](DS-QM102-SYNDROME-CAPACITY-BOUND.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PACKET` `DERIVED_LEAN`: [DS-QM103-SHOW-THE-PACKET-PROTOCOL](DS-QM103-SHOW-THE-PACKET-PROTOCOL.md) (DEFINITION)
