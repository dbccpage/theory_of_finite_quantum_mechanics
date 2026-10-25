# FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact integer population descent iff every row is sparse is rechecked generally. The all-ones zero-cancellation control is explicit; native cross-term differences are 4abxy and 4cdxy.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- sector basis and quadratic readout (assumption)

## Bottleneck

Unmet after the PFP review: Prove the advertised normalized/projective characterization, with its exact carrier and retained-zero convention, separately; do not promote the stronger-looking target wording from the integer theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

General-n row-sparsity characterization and projective-zero counterexample mechanized in DerivationDagQMClosure.lean and BornRedundancy.lean

## Review

- PFP review: [dag/results/FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact integer population descent iff every row is sparse is rechecked generally. The all-ones zero-cancellation control is explicit; native cross-term differences are 4abxy and 4cdxy.
  - does not support: Prove the advertised normalized/projective characterization, with its exact carrier and retained-zero convention, separately; do not promote the stronger-looking target wording from the integer theorem.
  - next test: Prove the advertised normalized/projective characterization, with its exact carrier and retained-zero convention, separately; do not promote the stronger-looking target wording from the integer theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0300 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `descent_compatible_iff_row_sparse` | yes | yes | yes | Quot.sound, propext | `#print axioms descent_compatible_iff_row_sparse` |
| `ray_quotient_classification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ray_quotient_classification` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md](../../../dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md)
- sha256 (`lf-normalised`): `1711cef9f69d5cafbf72d2e3c1a12bb8ce47f6773b96bab5491aec0055e0ca38`
- generated view: listed, not counted
- cited in: record TFQ-0300 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0300 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `FQ-R-DESCENT` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)

Outgoing (0):

