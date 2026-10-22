# PGW-RUNG5-SYMMETRY-ALONG-HISTORY

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung five (pull request 258) takes Y-3, symmetry along a history. In Lean a supply keeps every automorphism, datum and form admissions at a well-formed regime lose none, and an instance, rule or requirement admission keeps exactly the automorphisms fixing the added element. Each of the three adding kinds loses automorphisms at some regime and gains them at another, so the automorphism count moves both ways; on the rectangle the largest rise is five, at datum edges, and the largest fall 24, at instance edges. Every event keeps the regime or raises the element count by exactly one, so no history returns to a regime it left after a changing event.

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

- Lean declaration SecondSymmetry.Aut.inst_meet at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSymmetry.Aut.kinds_move_both_ways at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSymmetry.Aut.size_counts_changes at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

Which automorphisms survive is proved, never how many: no theorem counts an automorphism set, the numeric fixer and multiplication laws (Z-2, Z-3) are finite computation only, and that isomorphic regimes share an element count is left to rung eight for clean regimes.

## Source status

continuation.txt section 5.2 attempt 7 and section 6 rung five; run ledger SD-05-1 to SD-05-7; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md`

- file: [dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md](../../../dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md)
- sha256 (`lf-normalised`): `4d1633b59e7e70c2c553f4fe8b758c4b1a9fa6efb00a7d24df3e61b4a96b5740`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0468
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Grow.lean::no_return`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Grow.lean::size_counts_changes`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Meet.lean::inst_meet`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/lean/SecondSymmetry/Witness.lean::kinds_move_both_ways`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/symmetry.py::brute_automorphisms`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_symmetry/symmetry.py::edge_report`

## Absences recorded by the TFQ records

- TFQ-0468 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG5-SYMMETRY-ALONG-HISTORY` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM](PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-RUNG6-SUCCESSION-ELEMENT-COUNT` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG6-SUCCESSION-ELEMENT-COUNT](PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md) (CONDITIONAL)
