# PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung four (pull request 255) takes leftover X-3, the first-demand index up to the sealed isomorphism. In Lean separability and honour transport across the isomorphism, a label-preserving isomorphism carries a demand, and under a uniform stake (one label on every distinct pair) carrying a demand is class-invariant and class-matched histories have one first count; renaming supply tokens moves no first count. Under the three index readers parity, chain and residueThree the index escapes: isomorphic regimes of three or four data differ in carrying a demand, and class-matched histories of eight and eleven events have first counts eight or eleven against none. On the rectangle (2316 regimes in 402 classes, automorphism counts one to 240) the first count is constant on every trajectory class inside four events, which the Lean witnesses show is the bound's doing.

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

- Lean declaration SecondIso.Transport.hasDemand_iff_of_uniform at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIso.Trajectory.first_demand_matched_of_uniform at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondIso.Countermodel.first_count_not_trajectory_invariant at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

Necessity of uniformity (Y-2) and the shortest class-matched witnesses (Y-1) are OPEN; the countermodel checks are proved sound with no converse, and the four-event rectangle hides the non-constancy that the longer Lean witnesses exhibit.

## Source status

continuation.txt section 5.2 attempt 6, section 6 rung four and section 13; run ledger SD-04-1 to SD-04-7; Lean at 19L57G1 only; mechanized in WitnessedDifference/WdpBatch10.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean)
- sha256 (`bytes`): `c11c08954dc32c9203e93e7615edd4b6e7ec6320d02543c4617226256a7964d7`
- cited in: node.lean, record TFQ-0467
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10.rung4_uniform_transport_and_nonuniform_escape` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.rung4_uniform_transport_and_nonuniform_escape` |
| `WitnessedDifference.WdpBatch10.uniform_stake_transports_demand_pair` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.uniform_stake_transports_demand_pair` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean)
- sha256 (`bytes`): `bc49f2f3c659583494e3e796ac38a509874bcc8931aeb04542aff9e5b68aab24`
- cited in: node.lean, record TFQ-0467
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10Rep.rep_rung4_index_up_to_isomorphism` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung4_index_up_to_isomorphism` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0467_rung4_index_up_to_isomorphism.md`

- file: [dag/derivations/02_genesis/tfq_0467_rung4_index_up_to_isomorphism.md](../../../dag/derivations/02_genesis/tfq_0467_rung4_index_up_to_isomorphism.md)
- sha256 (`lf-normalised`): `f13f067887ea2f199c2b4b04d87de640c54aa28eb88549dd523e501d05d9ac8e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0467
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:170`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/iso_index.py::trajectory_report`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Countermodel.lean::demand_not_class_invariant`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Countermodel.lean::first_count_not_trajectory_invariant`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Trajectory.lean::first_demand_matched_of_uniform`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Transport.lean::hasDemand_iff_of_uniform`

## Absences recorded by the TFQ records

- TFQ-0467 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG4-INDEX-UP-TO-ISOMORPHISM` `DERIVED_LEAN`: [PGW-RUNG3-FIRST-DEMAND-INDEX](PGW-RUNG3-FIRST-DEMAND-INDEX.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-RUNG5-SYMMETRY-ALONG-HISTORY` `DERIVED_LEAN`: [PGW-RUNG5-SYMMETRY-ALONG-HISTORY](PGW-RUNG5-SYMMETRY-ALONG-HISTORY.md) (PROVED_LEAN)
