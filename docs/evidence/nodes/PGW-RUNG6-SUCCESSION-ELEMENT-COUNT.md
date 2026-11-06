# PGW-RUNG6-SUCCESSION-ELEMENT-COUNT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung six (pull request 259) takes Z-4, succession of accepted rounds through the element count, under three readings of a round: EVERY event, every ADMITTING event (not a supply) and every CHANGING event (the regime differs after it). In Lean, under CHANGING the count of any replayed history is the element count of the regime reached less the base's, so it is a function of base and regime, and counted from the empty regime a function of the regime alone; for every history CHANGING is at most ADMITTING, which is at most EVERY. Countermodels: EVERY and ADMITTING are not functions of base and regime, and CHANGING is not a function of the regime alone across bases (the Lean reading regime R2L is reached from the empty regime with count three and from itself with count zero).

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

- Lean declaration SecondSuccession.Count.changes_counted at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSuccession.Readings.every_not_given_base at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondSuccession.Readings.changing_not_of_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

The readings are of histories of the sealed step, not of an engine's run; class-level succession was OPEN at this rung and is closed for clean bases only by rung eight, and within continuation attempt two's runs one state is reached in five rounds and in six.

## Source status

continuation.txt section 3 definition 12, section 5.2 attempt 8 and section 6 rung six; run ledger SD-06-1 to SD-06-6; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean)
- sha256 (`bytes`): `e2d0c2ea1c49f613edb5efd542c1092ab43be08646f4e1d56662a44c9529bf64`
- cited in: node.lean, record TFQ-0469
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11.rung6_succession_element_count_and_countermodels` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.rung6_succession_element_count_and_countermodels` |
| `WitnessedDifference.WdpBatch11.stepRung_change_eq_elems_diff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.stepRung_change_eq_elems_diff` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean)
- sha256 (`bytes`): `fb93c9f5733e92d52e89df3da4ab8183ded4cf103514b6ba0d3141cfadc26165`
- cited in: node.lean, record TFQ-0469
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11Rep.rung6_succession_element_count_and_countermodels` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch11Rep.rung6_succession_element_count_and_countermodels` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md`

- file: [dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md](../../../dag/derivations/02_genesis/tfq_0469_rung6_succession_element_count.md)
- sha256 (`lf-normalised`): `b5ad11ec45907dd7b567ddad0ecb7e2d9049874ab22f7f90592f7b12c545e2b0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0469
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:195`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean::changes_counted`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean::changes_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::admitting_not_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::changing_not_of_regime`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean::every_not_given_base`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/succession.py::counts`

## Absences recorded by the TFQ records

- TFQ-0469 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG6-SUCCESSION-ELEMENT-COUNT` `DERIVED_LEAN`: [PGW-RUNG5-SYMMETRY-ALONG-HISTORY](PGW-RUNG5-SYMMETRY-ALONG-HISTORY.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-CAPABILITY-STAGE-COUNTER` `DERIVED_PROSE`: [PGW-CAPABILITY-STAGE-COUNTER](PGW-CAPABILITY-STAGE-COUNTER.md) (DEFINITION)
- `PGW-R-RUNG7-DURATION-UNDER-CHANGING` `DERIVED_LEAN`: [PGW-RUNG7-DURATION-UNDER-CHANGING](PGW-RUNG7-DURATION-UNDER-CHANGING.md) (PROVED_LEAN)
