# PGW-RUNG3-FIRST-DEMAND-INDEX

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung three (pull request 239) takes leftover L-2, the first-demand index over an arbitrary run: a first count is a prefix length at which a demand stands with no shorter prefix carrying one. In Lean the first count is unique with no decidability hypothesis, every event preserves well-formedness, a successor first count never consumes a demand-inert event last, and from the empty base no count below two is a first count. Existence is proved only given a decision for a demand at a regime (X-1, OPEN). Countermodels: the first count is not a function of the reached regime (two datum admissions, and a supply followed by the same two, give counts two and three under the all-apart stake), and a demand can cease.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Lean declaration SecondIndex.Index.first_demand_unique at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIndex.Index.first_demand_exists_when_a_demand_is_decidable at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIndex.Countermodel.index_is_not_a_function_of_the_reached_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Declared two-sided stake of rung two track one (assumption)

## Bottleneck

Existence of a first count waits on a decision procedure over contexts (X-1), which no rung built; the rectangle results (577, 3928 and 14293 sequences) stop at four events, and nothing here concerns a run driven by a responder (I-X PENDING).

## Source status

continuation.txt section 5.2 attempt 5 and section 6 rung three; run ledger SD-03-1 to SD-03-8; Lean at 19L57G1 only; mechanized in WitnessedDifference/WdpBatch10.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean)
- sha256 (`bytes`): `1a5147b5528c55fd4e346eb77a9ee79f7078baf2270b0cb8b2e05c9686a4319a`
- cited in: node.lean, record TFQ-0466
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10.demand_can_cease` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.demand_can_cease` |
| `WitnessedDifference.WdpBatch10.first_demand_unique` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.first_demand_unique` |
| `WitnessedDifference.WdpBatch10.index_is_not_a_function_of_the_reached_regime` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.index_is_not_a_function_of_the_reached_regime` |
| `WitnessedDifference.WdpBatch10.rung3_first_demand_index_uniqueness_and_countermodels` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.rung3_first_demand_index_uniqueness_and_countermodels` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean)
- sha256 (`bytes`): `32ea7319ad7905fe4ed84601af3d18f0448f22eadfde420530af6a3971251b9b`
- cited in: node.lean, record TFQ-0466
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10Rep.rep_rung3_first_demand_index` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung3_first_demand_index` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md`

- file: [dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md](../../../dag/derivations/02_genesis/tfq_0466_rung3_first_demand_index.md)
- sha256 (`lf-normalised`): `e5ec5cee3081f07b96b50e0363ccb22b73a2043b9b38113a3df1a79671cf67b9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0466
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:161`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/index.py::first_index_forward`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean::demand_can_cease`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Countermodel.lean::index_is_not_a_function_of_the_reached_regime`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean::first_demand_exists_when_a_demand_is_decidable`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_index/lean/SecondIndex/Index.lean::first_demand_unique`

## Absences recorded by the TFQ records

- TFQ-0466 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG3-FIRST-DEMAND-INDEX` `DERIVED_LEAN`: [PGW-RUNG2A-STAKE-DECLARED-LABEL](PGW-RUNG2A-STAKE-DECLARED-LABEL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-RUNG4-INDEX-UP-TO-ISOMORPHISM` `DERIVED_LEAN`: [PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM](PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM.md) (PROVED_LEAN)
