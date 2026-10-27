# PGW-TYPED-REQUIREMENT-KINDS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the requirement kinds a challenge import may introduce beyond the sealed one, an ordered pair of admitted data to be separated (a regime with n data has n(n-1)/2 such pairs, allPairs_length). The second derivation's declared stake is the typed extension it ran: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once; a pair is honoured when apart pairs are separable and same pairs collapsed, so its two demand kinds are a held apart pair that is collapsed and a held same pair that is separable. In rung two's menu of nine rules E4 alone generates both demand kinds (continuation §4), and stake invariance for E3, E4 and E6 is OPEN at target-regime transport replay, with no Lean statement about any menu rule (G-3 asks for the other five rules in Lean and E6's invariance). The education audit cites the Desc 64-toggle and KindDesc 1024-member families; in the sealed Lean these count guard toggles (Constitution.allDescs_length) and event-kind enable bits (ControllerCategory.allKinds_length), not requirement kinds.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Constitution.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Constitution.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Constitution.lean)
- sha256 (`bytes`): `a87b5a2aedce427c13fd33ba073d94c968ef6272afbf636e5610d194af53e882`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Constitution`): recorded sha256 `a87b5a2aedce427c13fd33ba073d94c968ef6272afbf636e5610d194af53e882` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Constitution.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allDescs_length` | yes | yes | yes | none | `#print axioms allDescs_length` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean](../../../lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean)
- sha256 (`bytes`): `e8dbba159ba6dbdff72117487457490b97a238808cfa1f1bc60557c873888bd5`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.ControllerCategory`): recorded sha256 `e8dbba159ba6dbdff72117487457490b97a238808cfa1f1bc60557c873888bd5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allKinds_length` | yes | yes | yes | none | `#print axioms allKinds_length` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Counting.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Counting.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Counting.lean)
- sha256 (`bytes`): `695d808307ea84d4e98ebd4bd63d1c570e8a93d5a8553f0db21af56093f3f996`
- cited in: node.lean, record TFQ-0489
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Counting`): recorded sha256 `695d808307ea84d4e98ebd4bd63d1c570e8a93d5a8553f0db21af56093f3f996` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Counting.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allPairs_length` | yes | yes | yes | Quot.sound, propext | `#print axioms allPairs_length` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md`

- file: [dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md](../../../dag/derivations/02_genesis/tfq_0489_typed_requirement_kinds.md)
- sha256 (`lf-normalised`): `f1e641148537e86f70794ec9adbb1e023e6e6eb3f6bcb753de765e1069028eae`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0489
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::StakeRule`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::demands`
- `external:sha256:0d098004a566c40656af6035d6e66ff13f7e873b11966677df080686a1b29cf9:1100`

## Absences recorded by the TFQ records

- TFQ-0489 rust: no Rust port of the stake menu

## Routes

Incoming (1):

- `PGW-R-TYPED-REQUIREMENT-KINDS` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION), [PGW-RUNG2B-STAKE-MENU](PGW-RUNG2B-STAKE-MENU.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
