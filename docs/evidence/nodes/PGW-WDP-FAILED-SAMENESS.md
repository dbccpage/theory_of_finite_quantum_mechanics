# PGW-WDP-FAILED-SAMENESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P01: within a fixed comparison family K, a failed declared sameness comparison Same_K(p, q) = 0 exhibits that the two compared presentations are not interchangeable under that comparison. The statement is local: it does not say the presentations differ under every comparison, does not make the failure intrinsic to the tokens, and supplies no order. A failed comparison is a residual at the level of predicates; encoding it as p − q is a stronger step that presupposes subtraction, scalars and a zero.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Declared comparison family K and sameness predicate Same_K on presentations (assumption)

## Bottleneck

Local to the declared comparison; it orders nothing, says nothing about other comparisons, and the ledger binds it to prose plus the Python ground.py check with no Lean declaration.

## Source status

WDP monograph §1.2 WDP-CH01-P01 finite proposition (prose; Python ground.py)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `omega_engine/crates_rs/omega_wdp/src/difference.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/difference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md`

- file: [dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md](../../../dag/derivations/06_wdp/tfq_0536_wdp_failed_sameness.md)
- sha256 (`lf-normalised`): `da15b746b176bdcc97e6f115bbab8bc0052105121ac63b148c6f7647015b5032`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0536
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_00_admitted_cut.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_00_admitted_cut.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/difference.rs::primitive_difference`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_exact_ground_outcomes.py::test_primitive_difference_and_triangle_identity`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/ground.py::primitive_difference`

## Absences recorded by the TFQ records

- TFQ-0536 lean4: the claim map lists WDP-CH01-P01 as prose-only; no Lean declaration states it

## Routes

Incoming (1):

- `PGW-R-WDP-FAILED-SAMENESS` `DERIVED_PROSE`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-WDP-ASYMMETRY-INJECTION-LEDGER` `DERIVED_PROSE`: [PGW-WDP-ASYMMETRY-INJECTION-LEDGER](PGW-WDP-ASYMMETRY-INJECTION-LEDGER.md) (DEFINITION)
- `PGW-R-WDP-QUOTIENT-DEFECT-ROOT-P` `DERIVED_PROSE`: [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION)
