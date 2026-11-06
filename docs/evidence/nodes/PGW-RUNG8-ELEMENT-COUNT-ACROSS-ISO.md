# PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung eight (pull request 262) takes Z-1, the element count across the sealed isomorphism. In Lean every inhabitant of the isomorphism keeps the numbers of data and forms with no hypothesis, and two clean regimes (well-formed, no list holding an entry twice) that it relates have all five component counts equal; six exhibited pairs show neither hypothesis can be dropped for instances, rules or requirements. Every event keeps cleanness and the empty and both Lean reading regimes are clean; from a clean base no class left is reached again, a class revisited is the very regime reached by unchanging events, so recurrence is only a stutter, and the counts of a history are functions of the class it reaches. Across two bases the class does not carry the count.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

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

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean)
- sha256 (`bytes`): `e2d0c2ea1c49f613edb5efd542c1092ab43be08646f4e1d56662a44c9529bf64`
- cited in: node.lean, record TFQ-0471
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11.no_return_class_and_recurrence_is_stutter` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.no_return_class_and_recurrence_is_stutter` |
| `WitnessedDifference.WdpBatch11.rung8_element_count_across_iso_and_clean_stutter` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.rung8_element_count_across_iso_and_clean_stutter` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean)
- sha256 (`bytes`): `fb93c9f5733e92d52e89df3da4ab8183ded4cf103514b6ba0d3141cfadc26165`
- cited in: node.lean, record TFQ-0471
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11Rep.rung8_element_count_across_iso_and_clean_stutter` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch11Rep.rung8_element_count_across_iso_and_clean_stutter` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md`

- file: [dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md](../../../dag/derivations/02_genesis/tfq_0471_rung8_element_count_across_iso.md)
- sha256 (`lf-normalised`): `df33eca26447fbc16fe3c9a41185d55ff8ca560aeda437fbf61767f4728e45e1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0471
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:218`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/class_count.py::recurrences`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Count.lean::size_iso`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Counter.lean::counts_not_of_class`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean::no_return_class`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean::recurrence_is_stutter`

## Absences recorded by the TFQ records

- TFQ-0471 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG8-ELEMENT-COUNT-ACROSS-ISO` `DERIVED_LEAN`: [PGW-RUNG7-DURATION-UNDER-CHANGING](PGW-RUNG7-DURATION-UNDER-CHANGING.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES` `DERIVED_LEAN`: [PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES](PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES.md) (PROVED_LEAN)
