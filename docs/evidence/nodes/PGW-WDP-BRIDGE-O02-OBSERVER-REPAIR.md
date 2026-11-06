# PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O02: connect each source transition and admission system to the WDP bridge by actual preservation and reflection maps covering costs, occurrences, and future questions.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

GEN-WDP-O02 remains open; scoped seed-15, seed-16, seed-22, and seed-25 replays do not establish faithful representation of every original executable run.

## Source status

GEN-WDP-O02 open refinement obligation in genesis_bridge_register.md

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
- sha256 (`lf-normalised`): `9009a8b34e288999cdad2100a4bed01469bcf3f2158dcbd021d447947e53e0b3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0567
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0567 rust: all-seed source transition preservation/reflection adapter is open

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O02-OBSERVER-REPAIR` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS](PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS.md) (OPEN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN), [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (PROVED_LEAN)

Outgoing (5):

- `PGW-R-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE](PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE.md) (OPEN)
- `PGW-R-WDP-MERON-M4-NATIVE-ADAPTERS` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M4-NATIVE-ADAPTERS](PGW-WDP-MERON-M4-NATIVE-ADAPTERS.md) (OPEN)
- `PGW-R-WDP-OUT-1-SHARP-OBSERVER-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION](PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION` `DERIVED_LEAN`: [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION` `DERIVED_LEAN`: [PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION](PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION.md) (PROVED_LEAN)
