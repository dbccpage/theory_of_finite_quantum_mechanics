# PGW-RUNG5-SYMMETRY-ALONG-HISTORY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung five (pull request 258) takes Y-3, symmetry along a history. In Lean a supply keeps every automorphism, datum and form admissions at a well-formed regime lose none, and an instance, rule or requirement admission keeps exactly the automorphisms fixing the added element. Each of the three adding kinds loses automorphisms at some regime and gains them at another, so the automorphism count moves both ways; on the rectangle the largest rise is five, at datum edges, and the largest fall 24, at instance edges. Every event keeps the regime or raises the element count by exactly one, so no history returns to a regime it left after a changing event.

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

- Lean declaration SecondSymmetry.Aut.inst_meet at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSymmetry.Aut.kinds_move_both_ways at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSymmetry.Aut.size_counts_changes at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

Which automorphisms survive is proved, never how many: no theorem counts an automorphism set, the numeric fixer and multiplication laws (Z-2, Z-3) are finite computation only, and that isomorphic regimes share an element count is left to rung eight for clean regimes.

## Source status

continuation.txt section 5.2 attempt 7 and section 6 rung five; run ledger SD-05-1 to SD-05-7; Lean at 19L57G1 only; mechanized in WitnessedDifference/WdpBatch10.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean)
- sha256 (`bytes`): `c11c08954dc32c9203e93e7615edd4b6e7ec6320d02543c4617226256a7964d7`
- cited in: node.lean, record TFQ-0468
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10.rung5_symmetry_step_law_and_both_ways_witness` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.rung5_symmetry_step_law_and_both_ways_witness` |
| `WitnessedDifference.WdpBatch10.stepRung_eq_or_elems_succ` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.stepRung_eq_or_elems_succ` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean)
- sha256 (`bytes`): `bc49f2f3c659583494e3e796ac38a509874bcc8931aeb04542aff9e5b68aab24`
- cited in: node.lean, record TFQ-0468
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10Rep.rep_rung5_symmetry_along_history` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung5_symmetry_along_history` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md`

- file: [dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md](../../../dag/derivations/02_genesis/tfq_0468_rung5_symmetry_along_history.md)
- sha256 (`lf-normalised`): `60a75949501dc38503cff5847109b3b2860722b77120711c1c792ed8dbe57900`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0468
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:183`
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

- `PGW-R-RUNG5-SYMMETRY-ALONG-HISTORY` `DERIVED_LEAN`: [PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM](PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-RUNG6-SUCCESSION-ELEMENT-COUNT` `DERIVED_LEAN`: [PGW-RUNG6-SUCCESSION-ELEMENT-COUNT](PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md) (PROVED_LEAN)
