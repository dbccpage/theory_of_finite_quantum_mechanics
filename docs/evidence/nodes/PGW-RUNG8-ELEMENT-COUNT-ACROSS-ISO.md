# PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung eight (pull request 262) takes Z-1, the element count across the sealed isomorphism. In Lean every inhabitant of the isomorphism keeps the numbers of data and forms with no hypothesis, and two clean regimes (well-formed, no list holding an entry twice) that it relates have all five component counts equal; six exhibited pairs show neither hypothesis can be dropped for instances, rules or requirements. Every event keeps cleanness and the empty and both Lean reading regimes are clean; from a clean base no class left is reached again, a class revisited is the very regime reached by unchanging events, so recurrence is only a stutter, and the counts of a history are functions of the class it reaches. Across two bases the class does not carry the count.

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

- Lean declaration SecondClass.Count.size_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondClass.Recur.no_return_class at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondClass.Recur.recurrence_is_stutter at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

Clean regimes and bases only: recurrence from an unclean base (U-1) and the Lean form of a history recurring exactly when it holds an unchanging event (U-2) are OPEN, and the Lean countermodel's two sides lie in two Python classes because Python reading L holds no requirement (P-13 missed).

## Source status

continuation.txt section 5.2 attempt 10 and section 6 rung eight; run ledger SD-08-1 to SD-08-6; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md`

- file: [dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md](../../../dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md)
- sha256 (`lf-normalised`): `d363d400ea976b9e8b3141726497236088b8809e4e23565517aeb23bb4e38358`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0471
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/class_count.py::recurrences`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Count.lean::size_iso`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Counter.lean::counts_not_of_class`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean::no_return_class`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean::recurrence_is_stutter`

## Absences recorded by the TFQ records

- TFQ-0471 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG8-ELEMENT-COUNT-ACROSS-ISO` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG7-DURATION-UNDER-CHANGING](PGW-RUNG7-DURATION-UNDER-CHANGING.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES](PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES.md) (CONDITIONAL)
