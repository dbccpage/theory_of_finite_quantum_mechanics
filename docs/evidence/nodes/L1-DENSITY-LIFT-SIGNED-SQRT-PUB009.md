# L1-DENSITY-LIFT-SIGNED-SQRT-PUB009

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact signed-square density projectors, overlap/Xi², zero-mass refusal, saturation and positive-support controls; general normalized Cauchy algebra and zero-weight strictness counterexample in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- real square roots (real field): lift
- trace norm on real symmetric matrices: lift

## Bottleneck

Unmet after the PFP review: Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi\<1 is admitted. The broader source statement is kept in pfp_review.prior_statement.

## Source status

PUB-009 signed-sqrt lift and Cauchy-Schwarz Xi bound mechanized in DerivationDagQMClosure.lean and Rust BigRational witness

## Review

- PFP review: [dag/results/L1-DENSITY-LIFT-SIGNED-SQRT-PUB009/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-DENSITY-LIFT-SIGNED-SQRT-PUB009/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact signed-square density projectors, overlap/Xi², zero-mass refusal, saturation and positive-support controls; general normalized Cauchy algebra and zero-weight strictness counterexample in Lean.
  - does not support: Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi\<1 is admitted.
  - next test: Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi\<1 is admitted.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/lean4/Xi.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/lean4/Xi.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_functional/src/xi.rs`

- file: `omega_engine/crates_rs/omega_functional/src/xi.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md`

- file: [dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md](../../../dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md)
- sha256 (`lf-normalised`): `afafc9b824245cd2b19b9f248fe02687da0b8782d2f01dd84904020ef321fe45`
- generated view: listed, not counted
- cited in: record TFQ-0355 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/density_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/density_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-DENSITY-LIFT-PUB009` `DERIVED_LEAN`: [L1-QM002-O022A-PHI1-QUOTIENT](L1-QM002-O022A-PHI1-QUOTIENT.md) (PROVED_LEAN), [L1-FRAMEWORK-KKT-CERT](L1-FRAMEWORK-KKT-CERT.md) (PROVED_LEAN), [L1-IMP-SQRT-FIELD](L1-IMP-SQRT-FIELD.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `L1-R-QM003-C17-FACTORIZATION` `DERIVED_LEAN`: [L1-QM003-C17-COMPOSABLE-FACTORIZATION](L1-QM003-C17-COMPOSABLE-FACTORIZATION.md) (PROVED_LEAN)
