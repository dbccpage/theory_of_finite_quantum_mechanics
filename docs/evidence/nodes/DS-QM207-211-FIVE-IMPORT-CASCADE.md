# DS-QM207-211-FIVE-IMPORT-CASCADE

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Exact phase/readout and noncommutative matrix controls are retained, and the cross-term and quartic-gap polynomials are exact identities over the rationals. They do not derive the five imports (U(1) phase fiber, quadratic readout, operator algebra, Born uniqueness, continuous dynamics) or establish that those imports are independent.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM207-C1 phase-blindness of L1 weights, QM208-C3 quadratic cross-term interference, QM209-C2 non-commutative operator algebra, QM210-C3 Lp power-rule separation, and QM211-C1..C3 five-import drop-one independence mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM207-211-FIVE-IMPORT-CASCADE/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM207-211-FIVE-IMPORT-CASCADE/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact phase/readout and noncommutative matrix controls are retained; cross-term and quartic-gap polynomials are general rational kernel identities.
  - does not support: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports.
  - next test: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornPairingBoundary.lean`

- file: [lean4/BornPairingBoundary.lean](../../../lean4/BornPairingBoundary.lean)
- sha256 (`bytes`): `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29`
- cited in: node.lean, record TFQ-1042
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornPairingBoundary`): recorded sha256 `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quartic_not_proportional` | yes | yes | yes | Quot.sound, propext | `#print axioms quartic_not_proportional` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1042
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` |

- counts toward the grade: yes

### Lean: `lean4/OperatorAlgebraShadow.lean`

- file: [lean4/OperatorAlgebraShadow.lean](../../../lean4/OperatorAlgebraShadow.lean)
- sha256 (`bytes`): `de5afdd4f30362f888b675aec2108d2c5829d3b672f9cf16ead20ee3ace415cc`
- cited in: node.lean, record TFQ-1042
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `OperatorAlgebraShadow`): recorded sha256 `de5afdd4f30362f888b675aec2108d2c5829d3b672f9cf16ead20ee3ace415cc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build OperatorAlgebraShadow`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `operator_algebra_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms operator_algebra_shadow` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1042

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md](../../../dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md)
- sha256 (`lf-normalised`): `5dc229bd9a171299153ccbefc50d1b96ab3c42cf714a570a3f6705e9e003f6d6`
- generated view: listed, not counted
- cited in: record TFQ-1042
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0ec245a80fd1f767b054bf2e08a4d4675786360f28e9c91c05bf47a04d4d02cc#QM209-C2`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche6_conditional_and_open_boundary_certificates_witness`
- `external:sha256:679e96859aa828d9063d94ad24f73a041996618602d4bb23baf393330b4fb740#QM207-C1`
- `external:sha256:83253e68b167f6b49b8ec5a08c51481a26d0e3390d6a9fb9f814d2b8983ca1e5#QM211-C1`
- `external:sha256:83253e68b167f6b49b8ec5a08c51481a26d0e3390d6a9fb9f814d2b8983ca1e5#QM211-C3`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:e6b742bc0e4edbe6c24d0da1183c1ce72cf4bbfd0b5f3b48d900e9ccee7b2375#QM208-C3`
- `external:sha256:f9b815a51e8e2748a89001239a63f49274febcad5e3e958f9a01c13f0ec6b96a#QM210-C3`

## Routes

Incoming (2):

- `DS-R-DYNAMICS-FROM-L1` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION), [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN), [DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY](DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY.md) (IMPORTED_ASSUMPTION), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

