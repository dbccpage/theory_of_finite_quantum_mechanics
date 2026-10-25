# PGW-MSSN-ROWS-1-TO-6-SPECIFIED

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Atlas rows MSS-1 to MSS-6 are specified targets whose lift status is unlicensed. MSS-1 introduces a single mark ⟨a⟩; MSS-2 specifies irreflexive pairings ⟨ab⟩ and obstructed cuts ⟨⟨ab⟩⟨⟩⟩ and refuses ⟨aa⟩; MSS-3 specifies abstract k-simplices for 0 ≤ k ≤ 3 with ∂² = 0; MSS-4 specifies 1-skeleton graph projections, a k-simplex decomposing into K_{k+1}; MSS-6 specifies stage packets with up-maps u_N and down-maps r_N satisfying r_N(u_N(x)) = x, with typed NON_DESCENT for new terms. MSS-0 is recorded in TFQ-0377, and MSS-5 is not part of this record.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- External MSS atlas row specifications MSS-1 to MSS-6 (assumption)

## Bottleneck

MSS-2 ≠ S(2): the levels README crosswalks MSS-2 post hoc to Genesis S(3) while the level_02 frontmatter names S(2), and either crosswalk is post hoc; each successor rationale is a declared obligation, and evaluator names and error labels are proposed interface labels, not running software.

## Source status

003_oemssn levels/README.md ledger rows 01-06 and level_01 to level_06 (specified, lift unlicensed)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0533_mssn_rows_1_to_6_specified.md`

- file: [dag/derivations/05_mssn_sn/tfq_0533_mssn_rows_1_to_6_specified.md](../../../dag/derivations/05_mssn_sn/tfq_0533_mssn_rows_1_to_6_specified.md)
- sha256 (`lf-normalised`): `a86868e4035c4692b6f50db44c3acaf0f19aa2cc2932658af780365a4ee6924f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0533
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/levels/README.md`

- file: `omega_engine_education/documentation/003_oemssn/levels/README.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/levels/level_03_abstract_simplices.md`

- file: `omega_engine_education/documentation/003_oemssn/levels/level_03_abstract_simplices.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/levels/level_06_tower_extension_retraction.md`

- file: `omega_engine_education/documentation/003_oemssn/levels/level_06_tower_extension_retraction.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0533 lean4: no Lean statement of rows MSS-1 to MSS-6 as specifications; the homology facts behind MSS-2 and MSS-3 are recorded under TFQ-0337
- TFQ-0533 python: no Python evaluator implements the MSS-1 to MSS-6 row obligations
- TFQ-0533 rust: no Rust evaluator implements the MSS-1 to MSS-6 row obligations

## Routes

Incoming (1):

- `PGW-R-MSSN-ROWS-1-TO-6-SPECIFIED` `DERIVED_PROSE`: [PGW-MSSN-SYNTAX-NOT-DECODING](PGW-MSSN-SYNTAX-NOT-DECODING.md) (DEFINITION), [PG-MSS0-ONLY-DIAMOND](PG-MSS0-ONLY-DIAMOND.md) (DEFINITION), [PG-CHAIN-RETRACTION](PG-CHAIN-RETRACTION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-MSSN-CIRCULATION-OBSTRUCTION` `DERIVED_LEAN`: [PGW-MSSN-CIRCULATION-OBSTRUCTION](PGW-MSSN-CIRCULATION-OBSTRUCTION.md) (PROVED_LEAN)
