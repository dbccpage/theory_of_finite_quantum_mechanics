# COMP-C1-FIRST-SEPARATION-REPLAY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the byte copy of the sealed event semantics, the history of two admitted data, one unary form, one instance on datum 0 and the demand (0,1) replays from the empty regime to a regime in which datum 0 and datum 1 are told apart by a unary instance, giving the alphabet {mark0, mark1}; a fixed instance.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 6 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Labelling mark0 := \<\> and mark1 := its first separated successor (declared)
- Byte copy of the sealed Regime, Event, stepE, replayE from the staged SupplyErasure.lean

## Bottleneck

The cost-two minimum (TFQ-0381) and the external definition of separable are not re-proved here; mark0 as \<\> and mark1 as its first separated successor is a declared labelling.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C1a claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean`

- file: [dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean](../../../dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean)
- sha256 (`bytes`): `cdc8d4cea4febffc6c3cb9be455c0b51c476383dc537577199021328d5ef0682`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean`
- counts toward the grade: yes

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1283
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Mark2.toDatum_bijective` | yes | yes | yes | Quot.sound, propext | `#print axioms Mark2.toDatum_bijective` |
| `firstSeparationHistory` | yes | yes | yes | none | `#print axioms firstSeparationHistory` |
| `first_separation_pairwise` | yes | yes | yes | Quot.sound, propext | `#print axioms first_separation_pairwise` |
| `first_separation_replay` | yes | yes | yes | propext | `#print axioms first_separation_replay` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/genesis_tm.rs`

- file: [code/rust/src/wdp/genesis_tm.rs](../../../code/rust/src/wdp/genesis_tm.rs)
- sha256 (`bytes`): `5ac31a360716dd646e3aa897a7a1fe2e73d74246e262aa4bc93fd9e8df720cb4`
- cited in: node.rust, record TFQ-1283

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `first_separation_history` (rust_symbol) | yes | yes | yes | - | - |
| `replay_e` (rust_symbol) | yes | yes | yes | - | - |
| `step_e` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/qm/genesis_tm.py`

- file: [code/python/src/qm/genesis_tm.py](../../../code/python/src/qm/genesis_tm.py)
- sha256 (`bytes`): `121faeefcc3cc65024c1b305989ed3bf5bd224a2af7e7217df7465ea4a5c64d5`
- cited in: record TFQ-1283

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FIRST_SEPARATION` (python_symbol) | yes | yes | yes | - | - |
| `replay` (python_symbol) | yes | yes | yes | - | - |
| `step_e` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1283_comp_c1_first_separation_replay.md`

- file: [dag/derivations/29_computation/tfq_1283_comp_c1_first_separation_replay.md](../../../dag/derivations/29_computation/tfq_1283_comp_c1_first_separation_replay.md)
- sha256 (`lf-normalised`): `27a7d05796c4abb6c46ab7354d94ffd64432114851edc754e2c0f00e000f4a49`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1283
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C1-FIRST-SEPARATION-REPLAY` `COMPUTED`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION), [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED), [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (3):

- `APP-R-COMP-C1-CANONICAL-SEPARATED-ALPHABET` `DERIVED_LEAN`: [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)
- `APP-R-COMP-C1-IDENTITY-CONVENTION-INPUT` `CONDITIONAL_ON_IMPORT`: [COMP-C1-IDENTITY-CONVENTION-INPUT](COMP-C1-IDENTITY-CONVENTION-INPUT.md) (IMPORTED_ASSUMPTION)
- `APP-R-COMP-C4-STEPE-UNCAPPED` `DERIVED_LEAN`: [COMP-C4-STEPE-UNCAPPED](COMP-C4-STEPE-UNCAPPED.md) (PROVED_LEAN)
