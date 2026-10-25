# PGW-TYPED-REQUIREMENT-KINDS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the requirement kinds a challenge import may introduce beyond the sealed one, an ordered pair of admitted data to be separated (a regime with n data has n(n-1)/2 such pairs, allPairs_length). The second derivation's declared stake is the typed extension it ran: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once; a pair is honoured when apart pairs are separable and same pairs collapsed, so its two demand kinds are a held apart pair that is collapsed and a held same pair that is separable. In rung two's menu of nine rules E4 alone generates both demand kinds (continuation §4), and stake invariance for E3, E4 and E6 is OPEN at target-regime transport replay, with no Lean statement about any menu rule (G-3 asks for the other five rules in Lean and E6's invariance). The education audit cites the Desc 64-toggle and KindDesc 1024-member families; in the sealed Lean these count guard toggles (Constitution.allDescs_length) and event-kind enable bits (ControllerCategory.allKinds_length), not requirement kinds.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared stake of the second derivation, an input declared once (continuation.txt §3 definition 7) (assumption)

## Bottleneck

No requirement-kind grammar is derived: the stake is a declared input, its invariance for E3, E4 and E6 is OPEN, and the Desc and KindDesc families are guard and event-kind toggles, not requirement-kind families.

## Source status

declared here; continuation.txt §3 definition 7, §4 row 2 and §13; education archive §6 item 2

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Constitution.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Constitution.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Constitution.lean)
- sha256 (`bytes`): `8546b1f70ffcdeb9da17f847a85d7d7aef39f5d2081acbac17f447a48f1118e8`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Constitution`): recorded sha256 `8546b1f70ffcdeb9da17f847a85d7d7aef39f5d2081acbac17f447a48f1118e8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Constitution.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allDescs_length` | yes | yes | yes | none | `#print axioms allDescs_length` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/ControllerCategory.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/ControllerCategory.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/ControllerCategory.lean)
- sha256 (`bytes`): `b7c9fa985aef2755770062af3d350b9e86efddebaacfb51befe25b6b57d01259`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.ControllerCategory`): recorded sha256 `b7c9fa985aef2755770062af3d350b9e86efddebaacfb51befe25b6b57d01259` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/ControllerCategory.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allKinds_length` | yes | yes | yes | none | `#print axioms allKinds_length` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Counting.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Counting.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Counting.lean)
- sha256 (`bytes`): `bd44a2b1eeec1da668413e098c2f11c65fb1062bd8c47b09ea031227cde66f8e`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Counting`): recorded sha256 `bd44a2b1eeec1da668413e098c2f11c65fb1062bd8c47b09ea031227cde66f8e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Counting.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allPairs_length` | yes | yes | yes | Quot.sound, propext | `#print axioms allPairs_length` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md`

- file: [dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md](../../../dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md)
- sha256 (`lf-normalised`): `268bc83294ac5d6efea7775dca00ec6121c1be49e459c06654ad1e62232672c6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0489
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::StakeRule`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::demands`

## Absences recorded by the TFQ records

- TFQ-0489 rust: no Rust port of the stake menu

## Routes

Incoming (1):

- `PGW-R-TYPED-REQUIREMENT-KINDS` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION), [PGW-RUNG2B-STAKE-MENU](PGW-RUNG2B-STAKE-MENU.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
