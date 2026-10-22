# PGW-WDP-QUOTIENT-DEFECT-ROOT-P

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Root P, the evaluation layer: with V a finite-dimensional real space of defects, A a finite-dimensional space of repairs, d: A → V a linear repair map, δ ∈ V an exhibited defect and J a declared seminorm or cost, the quotient defect is Φ_J(\[δ\]) = inf_{α ∈ A} J(δ − dα), where \[δ\] is the coset of δ modulo im d. The expression is not primitive: it imports a linear carrier, a repair map and a cost, each declared rather than derived. Root P presupposes Root W, the admitted cut with its witnessed irreflexive relation, as carrier and never substitutes for it. This infimum over repairs is the quantity WDP later writes Φ₁.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared defect space V, repair space A, linear repair map d and cost J (assumption)

## Bottleneck

A declared construction, not a theorem; it derives none of the carrier, repair map or cost from the admitted cut, and Φ_J(\[δ\]) equals J(δ) or ‖d₀δ‖₁ only where that value is shown to be the infimum.

## Source status

WDP monograph §2.1 Root P quotient defect (declared construction)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md`

- file: [dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md](../../../dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md)
- sha256 (`lf-normalised`): `8cab19bb14a876a9bea48e975bc7ba207d4e9a5aa118c9cb9a7f63abf8ec59b4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0538
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::matrix_quotient_l1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Q1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Repair`

## Routes

Incoming (1):

- `PGW-R-WDP-QUOTIENT-DEFECT-ROOT-P` `DERIVED_PROSE`: [PGW-WDP-FAILED-SAMENESS](PGW-WDP-FAILED-SAMENESS.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
- `PGW-R-WDP-SEVEN-WITNESS-ROLES` `DERIVED_PROSE`: [PGW-WDP-SEVEN-WITNESS-ROLES](PGW-WDP-SEVEN-WITNESS-ROLES.md) (DEFINITION)
