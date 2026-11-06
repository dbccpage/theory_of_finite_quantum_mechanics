# PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung nine (pull request 264) takes X-6 for two-ness and observational classes: a regime holds two when some two admitted data are separable, and a representative list holds pairwise separable admitted data with every admitted datum collapsed with an entry. In Lean separability, collapse, holding two and representative lists are carried by the isomorphism with no hypothesis, collapse is reflexive, symmetric and transitive, and holding two needs two data, a form and an instance, so its first stage is four events from the empty regime and two from each Lean reading regime, both attained. Supply, datum, form and requirement admissions keep separable pairs, while an instance or a rule admission can end holding two. That two representative lists of one regime have one length, the class count as a number, is OPEN in Lean (T-1).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Lean declaration SecondProfile.Classes.holdsTwo_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondProfile.Stage.twoness_needs_four at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondProfile.Carry.separable_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)

## Bottleneck

separable_iso and collapsed_iso are stated forward only, the reverse being their application to the exchanged structure, which is not stated as a theorem; the class count as a number waits on a decision for collapse (X-1) and is a finite computation on the rectangle.

## Source status

continuation.txt section 5.2 attempt 11 and section 6 rung nine; run ledger SD-09-1 to SD-09-6; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean)
- sha256 (`bytes`): `e2d0c2ea1c49f613edb5efd542c1092ab43be08646f4e1d56662a44c9529bf64`
- cited in: node.lean, record TFQ-0472
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11.collapsedRung_equivalence` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.collapsedRung_equivalence` |
| `WitnessedDifference.WdpBatch11.rung9_twoness_observational_classes_and_stage_bounds` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch11.rung9_twoness_observational_classes_and_stage_bounds` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean)
- sha256 (`bytes`): `fb93c9f5733e92d52e89df3da4ab8183ded4cf103514b6ba0d3141cfadc26165`
- cited in: node.lean, record TFQ-0472
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch11Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch11Rep.rung9_twoness_observational_classes_and_stage_bounds` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch11Rep.rung9_twoness_observational_classes_and_stage_bounds` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0472_rung9_two_ness_observational_classes.md`

- file: [dag/derivations/02_genesis/tfq_0472_rung9_two_ness_observational_classes.md](../../../dag/derivations/02_genesis/tfq_0472_rung9_two_ness_observational_classes.md)
- sha256 (`lf-normalised`): `1624202c440cd260ef36ca1dfdaee22b7431cfce5c4d3f7db129e895bd36b20c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0472
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Carry.lean::collapsed_iso`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Carry.lean::separable_iso`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Classes.lean::holdsTwo_iso`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Stage.lean::twoness_needs_four`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Stage.lean::twoness_needs_two_L`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/profile_rows.py::class_count`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/profile_rows.py::holds_two`

## Absences recorded by the TFQ records

- TFQ-0472 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES` `DERIVED_LEAN`: [PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO](PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-RUNG10-RESPONDER-ADJACENCY-REACH` `DERIVED_LEAN`: [PGW-RUNG10-RESPONDER-ADJACENCY-REACH](PGW-RUNG10-RESPONDER-ADJACENCY-REACH.md) (PROVED_LEAN)
