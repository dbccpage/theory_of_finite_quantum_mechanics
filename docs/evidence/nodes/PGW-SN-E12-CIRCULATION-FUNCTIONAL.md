# PGW-SN-E12-CIRCULATION-FUNCTIONAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E12 takes the oriented triangle a→b→c→a with C₀ = C₁ = ℤ³, coboundary d₀ and supplied edge record x = (1,0,0). On the open path a→b→c the potential g = (0,1,1) realizes the first two records but predicts −1 on ca. The circulation I(x) = x_ab + x_bc + x_ca vanishes on every d₀g and I(x) = 1, so no integer or rational potential realizes all three records; conversely I(x) = 0 gives the potential (0, x_ab, x_ab + x_bc), so im d₀ = ker I and C¹/im d₀ ≅ ℤ. The combined paper states the same criterion over ℤ, and Cochain.lean establishes it as triangle_repair_invariant and triangle_repair_exact_iff.

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

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared oriented incidence of the triangle graph adapter, not the intrinsic meaning of \<ab\> (assumption)

## Bottleneck

Lean covers the criterion over ℤ; the rational case is the same written argument. With edge evidence fixed the result is a certificate, not a repair, changing one entry is a separately priced response, and the example is not a Genesis stage.

## Source status

000_pre_genesis_to_mssn paper.md section 17.2 and lean4/Cochain.lean; 002_oesn levels/level_12 (E12)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Cochain.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Cochain.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md`

- file: [dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md](../../../dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md)
- sha256 (`lf-normalised`): `9ee7cb23edb686052b38adef8a16d4c9566beaba8d85f3a96373ab5a3a32d377`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0523
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_12_observer_stack_dda.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_12_observer_stack_dda.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Cochain.lean::triangle_repair_exact_iff`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Cochain.lean::triangle_repair_invariant`

## Absences recorded by the TFQ records

- TFQ-0523 python: no Python check of E12 in the S(n) strand
- TFQ-0523 rust: no Rust check of the converse potential (0, x_ab, x_ab + x_bc); the MSS-N circulation audit is recorded under TFQ-0534

## Routes

Incoming (1):

- `PGW-R-SN-E12-CIRCULATION-FUNCTIONAL` `DERIVED_LEAN`: [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (CONDITIONAL)

Outgoing (4):

- `PGW-R-MSSN-CIRCULATION-OBSTRUCTION` `DERIVED_LEAN`: [PGW-MSSN-CIRCULATION-OBSTRUCTION](PGW-MSSN-CIRCULATION-OBSTRUCTION.md) (PROVED_LEAN)
- `PGW-R-SN-E19-TORSION-ERASED-OVER-Q` `DERIVED_PROSE`: [PGW-SN-E19-TORSION-ERASED-OVER-Q](PGW-SN-E19-TORSION-ERASED-OVER-Q.md) (PROVED_PROSE)
- `PGW-R-SN-E20-OBSERVER-COMPLETION` `DERIVED_PROSE`: [PGW-SN-E20-OBSERVER-COMPLETION](PGW-SN-E20-OBSERVER-COMPLETION.md) (PROVED_PROSE)
- `PGW-R-SN-E21-REPAIR-RANK` `DERIVED_PROSE`: [PGW-SN-E21-REPAIR-RANK](PGW-SN-E21-REPAIR-RANK.md) (PROVED_PROSE)
