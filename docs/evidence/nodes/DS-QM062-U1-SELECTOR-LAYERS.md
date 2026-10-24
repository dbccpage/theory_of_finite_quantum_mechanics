# DS-QM062-U1-SELECTOR-LAYERS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual rational matrix products, Gaussian coefficients and norm-multiplicativity/conjugation polynomials are checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove the full ring homomorphism/embedding and the R/C/H selection hypotheses, continuity and global uniqueness separately; algebraic controls do not exclude H by themselves. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Layers 1-3 U(1) selector finite algebra (conjugation involution S^2=I2, Frobenius exclusion of split-real zero divisors and non-abelian Pauli pairs X2*Z2 != Z2*X2, and Gaussian-integer cx ring homomorphism/injectivity) mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM062-U1-SELECTOR-LAYERS/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM062-U1-SELECTOR-LAYERS/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual rational matrix products, Gaussian coefficients and norm-multiplicativity/conjugation polynomials are checked.
  - does not support: Prove the full ring homomorphism/embedding and the R/C/H selection hypotheses, continuity and global uniqueness separately; algebraic controls do not exclude H by themselves.
  - next test: Prove the full ring homomorphism/embedding and the R/C/H selection hypotheses, continuity and global uniqueness separately; algebraic controls do not exclude H by themselves.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0253 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` |
| `QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` |
- counts toward the grade: yes

### Lean: `lean4/H011U1SelectorBoundary.lean`

- file: [lean4/H011U1SelectorBoundary.lean](../../../lean4/H011U1SelectorBoundary.lean)
- sha256 (`bytes`): `214f187afdfc0ee196021aa3ce2ab96875b1c13de9b3a560ef1eaf0359622912`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H011U1SelectorBoundary`): recorded sha256 `214f187afdfc0ee196021aa3ce2ab96875b1c13de9b3a560ef1eaf0359622912` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H011U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `u1_selector_boundary` | yes | yes | yes | none | `#print axioms u1_selector_boundary` |
- counts toward the grade: yes

### Lean: `lean4/U1AngleAddition.lean`

- file: [lean4/U1AngleAddition.lean](../../../lean4/U1AngleAddition.lean)
- sha256 (`bytes`): `04d6fa729f320b810a16f1cea8b5f337ac394ab72ec4320fb4498c87f0ae9efc`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1AngleAddition`): recorded sha256 `04d6fa729f320b810a16f1cea8b5f337ac394ab72ec4320fb4498c87f0ae9efc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build U1AngleAddition`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `J_squared_eq_neg_id` | yes | yes | yes | Quot.sound, propext | `#print axioms J_squared_eq_neg_id` |
| `one_parameter_group_law` | yes | yes | yes | Quot.sound, propext | `#print axioms one_parameter_group_law` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
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

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md](../../../dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md)
- sha256 (`lf-normalised`): `156cf03a6e2efbe4a97922fe7e41bc0342db70068c5c46b2a82d79eb6b94f6cc`
- generated view: listed, not counted
- cited in: record TFQ-0253 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/028_the_u1_selector/qm_028_the_u1_selector_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/028_the_u1_selector/qm_028_the_u1_selector_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/062_the_u1_selector/qm_062_the_u1_selector_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/062_the_u1_selector/qm_062_the_u1_selector_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-U1-SELECTOR-LAYERS` `COMPUTED`: [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `DS-R-U1-SELECTOR` `DERIVED_LEAN`: [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) (PROVED_LEAN)
- `L1-R-U1-SELECTOR-LAYERS` `GAP_NO_DERIVATION`: [L1-U1-SELECTOR-OTHER-SEGMENT](L1-U1-SELECTOR-OTHER-SEGMENT.md) (OPEN)
