# FQ-GAP-REAL-EMBEDDING-CHOICE

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact quadratic-field Gram/conjugate coefficients, a mixed signature control and real-root inequalities are checked; the fake 9/4 root is explicitly rejected.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Formalize the coefficient-to-real embedding homomorphisms, full Gram PSD and cyclotomic fixed-field degree identification. A declared evaluation is not that embedding. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H060 2D pure-state Gram total positivity under every real embedding vs conductor-5 mixed witness W5 = diag(-2+sqrt(5), 3-sqrt(5)) Galois conjugate sign flip (evalAtS(9)=(1,3) \> 0 vs evalAtS(-9)=(-17,21)) and phi(120)/2 = 16 real embeddings mechanized in DerivationDagQMClosure.lean, H060EmbeddingRelativity.lean, and 006_finite_qm

## Review

- PFP review: [dag/results/FQ-GAP-REAL-EMBEDDING-CHOICE/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-GAP-REAL-EMBEDDING-CHOICE/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact quadratic-field Gram/conjugate coefficients, a mixed signature control and real-root inequalities are checked; the fake 9/4 root is explicitly rejected.
  - does not support: Formalize the coefficient-to-real embedding homomorphisms, full Gram PSD and cyclotomic fixed-field degree identification. A declared evaluation is not that embedding.
  - next test: Formalize the coefficient-to-real embedding homomorphisms, full Gram PSD and cyclotomic fixed-field degree identification. A declared evaluation is not that embedding.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1022
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_real_embedding_conductor5_mixed_witness_sign_flip` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_real_embedding_conductor5_mixed_witness_sign_flip` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_aliasing_and_real_embedding_conjugate` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_aliasing_and_real_embedding_conjugate` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1022
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `galois_conjugate_negativity_vs_sos_total_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms galois_conjugate_negativity_vs_sos_total_positivity` |

- counts toward the grade: yes

### Lean: `lean4/H060EmbeddingRelativity.lean`

- file: [lean4/H060EmbeddingRelativity.lean](../../../lean4/H060EmbeddingRelativity.lean)
- sha256 (`bytes`): `007106d36a4b1e5ff395a6c23d3c7eb970c5f74e0c884361c4655b7b4ffbd666`
- cited in: node.lean, record TFQ-1022
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `H060EmbeddingRelativity`): recorded sha256 `007106d36a4b1e5ff395a6c23d3c7eb970c5f74e0c884361c4655b7b4ffbd666` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H060EmbeddingRelativity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pure_state_totally_positive_2d` | yes | yes | yes | propext | `#print axioms pure_state_totally_positive_2d` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1022
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/embedding_relativity.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/embedding_relativity.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1022
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1022
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1022

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_1022_fq_gap_real_embedding_choice.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_1022_fq_gap_real_embedding_choice.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_1022_fq_gap_real_embedding_choice.md)
- sha256 (`lf-normalised`): `88ccf03fe39fe895df23b56dad6ff1c261e166abcabd4bc359f139816e162b4c`
- generated view: listed, not counted
- cited in: record TFQ-1022
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-EMBEDDING` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-BUSCH-EFFECT-FRAME](FQ-BUSCH-EFFECT-FRAME.md) (PROVED_LEAN)

Outgoing (0):

