# DS-QM062-U1-SELECTOR-LAYERS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual rational matrix products, Gaussian coefficients and norm-multiplicativity/conjugation polynomials are checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 6
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

Layers 1-3 U(1) selector finite algebra (conjugation involution S^2=I2, Frobenius exclusion of split-real zero divisors and non-abelian Pauli pairs X2*Z2 != Z2*X2, and Gaussian-integer cx ring homomorphism/injectivity) mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM062-U1-SELECTOR-LAYERS/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM062-U1-SELECTOR-LAYERS/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
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

### Lean: `lean4/U1SelectorBoundary.lean`

- file: [lean4/U1SelectorBoundary.lean](../../../lean4/U1SelectorBoundary.lean)
- sha256 (`bytes`): `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1SelectorBoundary`): recorded sha256 `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `u1_selector_boundary` | yes | yes | yes | none | `#print axioms u1_selector_boundary` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`
- `external:sha256:7c9f367207a364a50dbd6f9d9c97a1c30b7dc1fd5499990bb770aa8135344b6a#DUAL-QM_028-C0`
- `external:sha256:80736e21321aa43e6bf1cf97fb3deb2e07039345a223d53af7c36162b2e4cae7#QM-062-C2`
- `external:sha256:80736e21321aa43e6bf1cf97fb3deb2e07039345a223d53af7c36162b2e4cae7#QM-062-C3`
- `external:sha256:80736e21321aa43e6bf1cf97fb3deb2e07039345a223d53af7c36162b2e4cae7#QM-062-C5`
- `external:sha256:80736e21321aa43e6bf1cf97fb3deb2e07039345a223d53af7c36162b2e4cae7#QM-062-C8`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- `external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e::PairingInvolution`

## Routes

Incoming (1):

- `DS-R-U1-SELECTOR-LAYERS` `COMPUTED`: [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `DS-R-U1-SELECTOR` `DERIVED_LEAN`: [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) (PROVED_LEAN)
- `L1-R-U1-SELECTOR-LAYERS` `GAP_NO_DERIVATION`: [L1-U1-SELECTOR-OTHER-SEGMENT](L1-U1-SELECTOR-OTHER-SEGMENT.md) (OPEN)
