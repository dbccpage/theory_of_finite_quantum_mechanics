# PGW-SN-REPRESENTATION-QUOTIENT

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In a supplied complex model with one coordinate at each of two sites, the balance map T sends the ordinary tensor coefficients (rr, ri, ir, ii) to (rr − ii, ri + ir), so for m = n = 1 its rows are (1,0,0,−1) and (0,1,1,0). With u = Tᵗ/2 and r = T, r u = I₂ while u r = P = TᵗT/2 is a rank-2 idempotent, and the vector (1,0,0,1) lies in ker T, so P ≠ I₄. The exact kernel of T is the complex balancing relation. The reading guide uses this as a representation quotient: it names the declared questions that survive and the information quotiented away, and it supplies no native S(n) obstruction.

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared complex scalars and tensor coordinates of the WDP realification supplement (assumption)

## Bottleneck

Lean states integer coefficient laws (balance after section is doubling, and the kernel test rr = ii, ri = −ir); division by 2 and positivity are written separately. A lawful representation of the selected quantum composite gives neither a new native S(n) obstruction nor permission to advance beyond S(6).

## Source status

WDP docs/complex_tensor_balancing.md Theorem 1; 002_oesn reading_guide.md representation quotient; Lean ComplexTensorBalancing

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ComplexTensorBalancing.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ComplexTensorBalancing.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs`

- file: `omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md`

- file: [dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md](../../../dag/derivations/05_mssn_sn/tfq_0521_sn_representation_quotient.md)
- sha256 (`lf-normalised`): `81d940b16ad12e46ece76d74e8e5e8390af0ed45b872ba516c59212a068a75bc`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0521
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/complex_tensor_balancing.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/reading_guide.md`

- file: `omega_engine_education/documentation/002_oesn/reading_guide.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_map_with_limits`
- `external:the_symbol_game/omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs::balance_projector_with_limits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ComplexTensorBalancing.lean::balance_kernel_iff`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ComplexTensorBalancing.lean::balance_section`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ComplexTensorBalancing.lean::twice_project_square`

## Absences recorded by the TFQ records

- TFQ-0521 python: no Python check of the balance map in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-REPRESENTATION-QUOTIENT` `DERIVED_LEAN`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)

Outgoing (0):

