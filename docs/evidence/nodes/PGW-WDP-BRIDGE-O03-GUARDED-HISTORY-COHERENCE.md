# PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O03: on the 3-dimensional commuting swap cube {0,1}^3, the 3-cell boundary of the six square 2-face holonomies vanishes identically (d_2 d_1 = 0), so five coherent square faces force all six permutation schedules to have equal holonomy, whereas puncturing a 2-face obstructs path coherence.

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

Mechanized in Lean 4 (guarded_3cube_boundary_d2_d1_zero, guarded_3cube_all_six_paths_equal, and punctured_2face_holonomy_obstruction in WdpBatch6.lean alongside replay_iff_prefixSafe in GuardedScheduleTopology.lean); arbitrary infinite-dimensional CW complexes remain outside the finite cube model.

## Source status

GEN-WDP-O03 finite 3-cube filler coherence and punctured-face obstruction mechanized in GuardedScheduleTopology.lean and WdpBatch6.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean)
- sha256 (`bytes`): `1c868acd20086e2a9825cde8ad0f7ce88613dc161197d79466385fdb5098f39d`
- cited in: node.lean, record TFQ-0568
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replay_iff_prefixSafe` | yes | yes | yes | - | `#print axioms replay_iff_prefixSafe` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `e1d9e23ed4bf94ba2f05b141cb8eecadcbd8e867ed8f2c1ca7ef86eedc82cfe1`
- cited in: node.lean, record TFQ-0568
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.guarded_3cube_all_six_paths_equal` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.guarded_3cube_all_six_paths_equal` |
| `WitnessedDifference.WdpBatch6.guarded_3cube_boundary_d2_d1_zero` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.guarded_3cube_boundary_d2_d1_zero` |
| `WitnessedDifference.WdpBatch6.punctured_2face_holonomy_obstruction` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.punctured_2face_holonomy_obstruction` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0568

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0568_wdp_bridge_o03_guarded_history_coherence.md`

- file: [dag/derivations/06_wdp/tfq_0568_wdp_bridge_o03_guarded_history_coherence.md](../../../dag/derivations/06_wdp/tfq_0568_wdp_bridge_o03_guarded_history_coherence.md)
- sha256 (`lf-normalised`): `a52f25f9f1db3f1273de6a026629f2d4c41cb5528afe40ccb3be8c57082b9777`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0568
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0568 rust: checked in Lean 4 and Python obstruction signature witnesses

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (OPEN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN)

Outgoing (2):

- `PGW-R-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION](PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION.md) (OPEN)
- `PGW-R-WDP-OUT-2-GUARDED-SWAP-COHERENCE` `DERIVED_LEAN`: [PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE](PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE.md) (PROVED_LEAN)
