# L1-QM002-O022A-PHI1-QUOTIENT

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact rational triangle primal construction, minimum weighted cost and gauge-shift invariance, plus general telescoping and lower-bound assumptions in Lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Banach quotient construction on finite-dim packet: lift

## Bottleneck

Unmet after the PFP review: Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Exact coboundary quotient invariance of edgewise residual mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM002-O022A-PHI1-QUOTIENT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-QM002-O022A-PHI1-QUOTIENT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact rational triangle primal construction, minimum weighted cost and gauge-shift invariance, plus general telescoping and lower-bound assumptions in Lean.
  - does not support: Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement.
  - next test: Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/cochain_repair_code.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/cochain_repair_code.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md`

- file: [dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md](../../../dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md)
- sha256 (`lf-normalised`): `46d73c193145815e5df5a3d4f71fa4ed65d54955e322ef115b622a1fa3b8bb27`
- generated view: listed, not counted
- cited in: record TFQ-0359
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/002_cofiber_to_banach_quotient_bridge/qm_002_cofiber_to_banach_quotient_bridge_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/002_cofiber_to_banach_quotient_bridge/qm_002_cofiber_to_banach_quotient_bridge_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-PHI1-QUOTIENT` `DERIVED_LEAN`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `L1-R-DENSITY-LIFT-PUB009` `DERIVED_LEAN`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (PROVED_LEAN)
