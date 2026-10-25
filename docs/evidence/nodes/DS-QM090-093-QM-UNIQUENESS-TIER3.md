# DS-QM090-093-QM-UNIQUENESS-TIER3

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual context tables, global-assignment exclusion and spectator marginal recovery are exact; the odd-cycle and rational recovery statements are kernel checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM-093-C4/C5/C18/C20 survival theorem under finite descent, sealed_can_fail witness, Tier-4 ontological non-promotion, real-rebit local-tomography dimension failure (9 != 10), and 24-vertex (2,2,2) no-signaling PR-box counter-theory mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM090-093-QM-UNIQUENESS-TIER3/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM090-093-QM-UNIQUENESS-TIER3/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual context tables, global-assignment exclusion and spectator marginal recovery are exact; the odd-cycle and rational recovery statements are kernel checked.
  - does not support: Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted.
  - next test: Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0274
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion` |

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

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md)
- sha256 (`lf-normalised`): `efea6b419ae7b74a047883d974486edd4c3701cee1e73501da884e7fa000ac5d`
- generated view: listed, not counted
- cited in: record TFQ-0274
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-UNIQUENESS` `DERIVED_LEAN`: [DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY](DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY.md) (PROVED_LEAN)

Outgoing (0):

