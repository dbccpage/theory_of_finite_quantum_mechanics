# DS-QM064-074-083-ANNEX-REDIRECT-ROWS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Triangle identities, retained stochastic outputs and contextual marginal residuals are recomputed exactly; generic finite rational contraction is kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Coboundary, triangle holonomy gauge invariance, and stochastic L1 contraction mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM064-074-083-ANNEX-REDIRECT-ROWS/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM064-074-083-ANNEX-REDIRECT-ROWS/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Triangle identities, retained stochastic outputs and contextual marginal residuals are recomputed exactly; generic finite rational contraction is kernel checked.
  - does not support: Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations.
  - next test: Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations.

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
| `QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant` |
| `QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md)
- sha256 (`lf-normalised`): `d9550d315f9a93fdeacf37fbcf43979ad633bc9c83d8a57913b54d2d6c468d88`
- generated view: listed, not counted
- cited in: record TFQ-0255
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md](../../../dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md)
- sha256 (`lf-normalised`): `d15381a243e254164c16e1eafedefccb868275f35a792b8564ec7f910f8138f5`
- generated view: listed, not counted
- cited in: record TFQ-0267 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-REDIRECT` `DERIVED_LEAN`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (PROVED_LEAN)

Outgoing (0):

