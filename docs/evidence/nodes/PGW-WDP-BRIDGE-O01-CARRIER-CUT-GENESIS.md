# PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O01: an observation-separated irreflexive cut exists on a seed carrier if and only if at least one admitted test separates two states, whereas an inert seed with constant test profiles cannot generate an irreflexive cut.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Mechanized in Lean 4 (carrier_cut_challenge_floor_iff, inert_seed_cannot_generate_irreflexive_cut, and seed_round1_cut_and_residual_collapse in WdpBatch6.lean alongside endpoints_apart in PrimitiveAdmissionFloor.lean); autonomous demand generation beyond the declared seed tests remains fenced.

## Source status

GEN-WDP-O01 finite challenge-generation floor and inert-seed falsifier mechanized in PrimitiveAdmissionFloor.lean and WdpBatch6.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean)
- sha256 (`bytes`): `df9d149bbd06124fd7b6226656f0588be037bbbf121f12c99ec35ea4b123ae15`
- cited in: node.lean, record TFQ-0566
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `endpoints_apart` | yes | yes | yes | - | `#print axioms endpoints_apart` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `e1d9e23ed4bf94ba2f05b141cb8eecadcbd8e867ed8f2c1ca7ef86eedc82cfe1`
- cited in: node.lean, record TFQ-0566
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.carrier_cut_challenge_floor_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.carrier_cut_challenge_floor_iff` |
| `WitnessedDifference.WdpBatch6.inert_seed_cannot_generate_irreflexive_cut` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.inert_seed_cannot_generate_irreflexive_cut` |
| `WitnessedDifference.WdpBatch6.seed_round1_cut_and_residual_collapse` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.seed_round1_cut_and_residual_collapse` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py)
- sha256 (`bytes`): `8a955655b74671c6599df32e839bbaef8357e8d789869b009b63e063bc15bcbb`
- cited in: record TFQ-0566

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `apartness_witness` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0566_wdp_bridge_o01_carrier_cut_genesis.md`

- file: [dag/derivations/06_wdp/tfq_0566_wdp_bridge_o01_carrier_cut_genesis.md](../../../dag/derivations/06_wdp/tfq_0566_wdp_bridge_o01_carrier_cut_genesis.md)
- sha256 (`lf-normalised`): `796a3d813b04d7f60c28d4e26ffecbd9c8725d6d554e3e271b2d83d5012452e1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0566
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0566 rust: checked in Lean 4 and Python foundational bridge witnesses

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS` `DERIVED_LEAN`: [PGW-WD2-MINIMAL-DETERMINISTIC-QUOTIENT](PGW-WD2-MINIMAL-DETERMINISTIC-QUOTIENT.md) (PROVED_LEAN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (PROVED_LEAN), [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION)

Outgoing (1):

- `PGW-R-WDP-BRIDGE-O02-OBSERVER-REPAIR` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (PROVED_LEAN)
