# IMPL-THYMUS-SCREENING-SOUNDNESS

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Complete finite panel/predicate controls and mismatch witnesses are exact; zero in-panel false positives under the actual screened predicate is kernel checked.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed. The broader source statement is kept in pfp_review.prior_statement.

## Source status

MECHANIZED in ThymusScreening.lean (empty axiom report) with Rust witness

## Review

- PFP review: [dag/results/IMPL-THYMUS-SCREENING-SOUNDNESS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/IMPL-THYMUS-SCREENING-SOUNDNESS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete finite panel/predicate controls and mismatch witnesses are exact; zero in-panel false positives under the actual screened predicate is kernel checked.
  - does not support: Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed.
  - next test: Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_education/documentation/004_oepfp/lean4/ThymusScreening.lean`

- file: `omega_engine_education/documentation/004_oepfp/lean4/ThymusScreening.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source, record TFQ-1045
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1045
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md`

- file: [dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md](../../../dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md)
- sha256 (`lf-normalised`): `06afafd2c94638f9b4f720c747b4680b27bbd4bb41bca63ef1227e68f977120c`
- generated view: listed, not counted
- cited in: record TFQ-1045
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `IMPL-R-THYMUS-SCREENING` `DERIVED_LEAN`: [PG-PREGEN-CONSTRUCTIVE-SUMMARY](PG-PREGEN-CONSTRUCTIVE-SUMMARY.md) (PROVED_LEAN)

Outgoing (0):

