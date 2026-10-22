# PG-GEN-ONGOING-FEWEST-CHANGES

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fewest changes to reach a result is the first derivation's size-plus-twice-destroyed-givens formula, with matching lower and upper bounds (fewest_changes_A/B).

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem.

## Source status

Fewest-changes formula (D8-D10)

## Review

- PFP review: [dag/results/PG-GEN-ONGOING-FEWEST-CHANGES/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-ONGOING-FEWEST-CHANGES/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete 68-state shortest-path tables for both apart seeds and exact edit-cost identities are retained; scalar lower-bound algebra is kernel checked.
  - does not support: Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem.
  - next test: Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Cost.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Cost.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md`

- file: [dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md](../../../dag/derivations/02_genesis/tfq_0389_fewest_changes_formula.md)
- sha256 (`lf-normalised`): `a104cc78b841b7e7c5f927f96ff593a4cd3b2fe5195e5869f7e8d839d5646e70`
- generated view: listed, not counted
- cited in: record TFQ-0389
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0389 lean4: declaration obligation: fewest_changes_A for one legal well-formed writing
- TFQ-0389 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean
- TFQ-0389 python: missing obligation: a cost column under 001_genesis_ongoing_h3v7n5qf/evidence that is checked only inside the declared term bound
- TFQ-0389 rust: missing obligation: no Rust cost module was listed for the ongoing package; the formula still needs an explicit finite checker or a stated absence

## Routes

Incoming (1):

- `PG-R-ONGOING-COST` `DERIVED_LEAN`: [PG-GEN-ONGOING-OBSTRUCTION](PG-GEN-ONGOING-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (3):

- `PG-R-REWRITING` `DERIVED_LEAN`: [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN)
- `PG-R-SAMENESS` `COMPUTED`: [PG-GEN-SAMENESS-REFINEMENTS](PG-GEN-SAMENESS-REFINEMENTS.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-GO-REACH-CEILING` `DERIVED_LEAN`: [PGW-GO-REACH-CEILING](PGW-GO-REACH-CEILING.md) (PROVED_LEAN)
