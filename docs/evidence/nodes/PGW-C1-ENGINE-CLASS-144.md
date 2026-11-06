# PGW-C1-ENGINE-CLASS-144

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuation attempt one (pull request 267), authorized by the author after the original twelve attempts, takes Challenge 3, the engine: a generator (one of the nine stake rules, read in a plain or flipped mode), a responder (one sealed measure and one of rung one's two validity members, answering a demand by every tied minimum), a continuation (a subset of growth and switch fired only at a demand-free state, the empty subset named HALT) and the sealed replay extended by the switch marker. The class has 144 members, 108 of them without HALT, with capability counts from six to ten, so no member is one declaration. Probed to depth two from both readings (288 probes), 64 members are LIVE and 16 TWO-KINDED; a count-minimal and inclusion-minimal member exists in every declared subclass, none of the minima is unique up to probe-isomorphism, and no member is initial under inclusions of declarations. No engine is run forward.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Lean declaration SecondEngine.Census.class_size at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondEngine.Census.no_initial at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondEngine.EngineDef.run_named at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Author ruling of 2026-09-25 authorizing at most two continuation attempts outside the original budget (assumption)

## Bottleneck

The Lean response relation is not constrained to be a minimum and no theorem ties the finite list of declarations to the Engine structure; minima_differ_at_genL states only that E4 demands and E1 does not at reading L's genesis, the non-isomorphism going through the Python probe; no census row is decided, and initiality is refused for inclusion morphisms only.

## Source status

continuation.txt section 3 definition 17, section 4 row 3 and section 12 attempt one; run ledger SD-E-1 to SD-E-18; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean)
- sha256 (`bytes`): `979e9edd791cdf8a6915e6dba2d07174693f66dd5b6006fa81f355f7d016864d`
- cited in: node.lean, record TFQ-0474
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch12.c1_engine_class_144_and_no_initial` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.c1_engine_class_144_and_no_initial` |
| `WitnessedDifference.WdpBatch12.engineCapCount1_bounds` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.engineCapCount1_bounds` |
| `WitnessedDifference.WdpBatch12.engine_not_subset_opposite_measure` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.engine_not_subset_opposite_measure` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean)
- sha256 (`bytes`): `55e6b24863699434b12724fe74d3738c98943ab98b03683f7cc12dd87d2a45d7`
- cited in: node.lean, record TFQ-0474
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch12Rep.c1_engine_class_144_and_no_initial` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12Rep.c1_engine_class_144_and_no_initial` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0474_c1_engine_class_144.md`

- file: [dag/derivations/02_genesis/tfq_0474_c1_engine_class_144.md](../../../dag/derivations/02_genesis/tfq_0474_c1_engine_class_144.md)
- sha256 (`lf-normalised`): `75659f08707e73e209052ba2e61e348d3c2c92a1d27ad017854498aa9eba5d45`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0474
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_decl.py::count_minimal`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_decl.py::engine_class`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/engine_probe.py::build_probe`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean::class_size`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean::literal_size`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Census.lean::no_initial`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Engine.lean::run_named`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_engine/lean/SecondEngine/Genesis.lean::minima_differ_at_genL`

## Absences recorded by the TFQ records

- TFQ-0474 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-C1-ENGINE-CLASS-144` `DERIVED_LEAN`: [PGW-RUNG10-RESPONDER-ADJACENCY-REACH](PGW-RUNG10-RESPONDER-ADJACENCY-REACH.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-C2-RUN-FORWARD-EVERY-HISTORY` `DERIVED_LEAN`: [PGW-C2-RUN-FORWARD-EVERY-HISTORY](PGW-C2-RUN-FORWARD-EVERY-HISTORY.md) (PROVED_LEAN)
