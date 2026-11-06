# PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O02: connect each source transition and admission system to the WDP bridge by actual preservation and reflection maps covering costs, occurrences, and future questions.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Finite orientation-sensitivity countermodel mechanized in WdpBatch6.lean (orientation_sensitive_pair_defect_nonreflection); physical laboratory repair actuation and faithful representation of every external executable run remain open.

## Source status

GEN-WDP-O02 finite orientation-sensitivity countermodel mechanized in WdpBatch6.lean; external physical repair actuation remains open

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/OriginalGenesisObserver.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/OriginalGenesisObserver.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/OriginalGenesisObserver.lean)
- sha256 (`bytes`): `0aadd87d31f73342c38204eb0b5a3aa2456cf6f9c9724faf739ce878fedf213a`
- cited in: node.lean, record TFQ-0567
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/OriginalGenesisObserver.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `history_extension_unique` | yes | yes | yes | - | `#print axioms history_extension_unique` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean)
- sha256 (`bytes`): `206d2df25744c1084e2464bc013a9927f628937075c89b541d854257f5590410`
- cited in: node.lean, record TFQ-0567
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch12.o02_collision_refutes_preservation_reflection` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.o02_collision_refutes_preservation_reflection` |
| `WitnessedDifference.WdpBatch12.o02_preservation_reflection_comp` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.o02_preservation_reflection_comp` |
| `WitnessedDifference.WdpBatch12.wdp_bridge_o02_scoped_preservation_reflection_characterization` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch12.wdp_bridge_o02_scoped_preservation_reflection_characterization` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean)
- sha256 (`bytes`): `7722672b1b23be2106e7bec91f41eb2eb25b2671622b4975a848cd7be6562fa2`
- cited in: node.lean, record TFQ-0567
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch12Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch12Rep.wdp_bridge_o02_scoped_preservation_reflection_characterization` | yes | yes | no | - | `#print axioms WitnessedDifference.WdpBatch12Rep.wdp_bridge_o02_scoped_preservation_reflection_characterization` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `e1d9e23ed4bf94ba2f05b141cb8eecadcbd8e867ed8f2c1ca7ef86eedc82cfe1`
- cited in: node.lean, record TFQ-0567
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.orientation_sensitive_pair_defect_nonreflection` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.orientation_sensitive_pair_defect_nonreflection` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0567

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0567_wdp_bridge_o02_observer_repair.md`

- file: [dag/derivations/06_wdp/tfq_0567_wdp_bridge_o02_observer_repair.md](../../../dag/derivations/06_wdp/tfq_0567_wdp_bridge_o02_observer_repair.md)
- sha256 (`lf-normalised`): `a62d8f855f35e0d64c3c102e21cd7e394b8e74f6606a67e2031ed7aec0a280e8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0567
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0567 rust: all-seed source transition preservation/reflection adapter is open

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O02-OBSERVER-REPAIR` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS](PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS.md) (PROVED_LEAN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (PROVED_LEAN)

Outgoing (5):

- `PGW-R-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE](PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE.md) (PROVED_LEAN)
- `PGW-R-WDP-MERON-M4-NATIVE-ADAPTERS` `DERIVED_LEAN`: [PGW-WDP-MERON-M4-NATIVE-ADAPTERS](PGW-WDP-MERON-M4-NATIVE-ADAPTERS.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-1-SHARP-OBSERVER-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION](PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION` `DERIVED_LEAN`: [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION` `DERIVED_LEAN`: [PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION](PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION.md) (PROVED_LEAN)
