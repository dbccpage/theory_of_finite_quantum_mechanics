# PGW-CHALLENGE0-INERTIA-SECOND-TOKEN

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At Challenge 0 the only object-language inscription is the opaque whole \<\>. In the token-erased Lean model nothing is derivable at genesis (genesis_underivable), and nothing is derivable in any regime with no instances and no rules (underivable_of_empty); the Challenge 0 computation records zero contexts and an empty derivable set in both readings. That no successor is internally forced is a property of the declared grammar, whose only state changes are external-event-indexed admissions, not a theorem about a forcing predicate. In the token-aware model a history whose datum admissions all carry one token leaves at most one admitted datum (single_token_carrier_bound), so a state with two data needs the admission of a second, different token (second_token_required).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No forcing predicate is defined, so no forced successor is a model-scoped definition and not a theorem, and nothing here excludes a successor in an extension of the language; supply_no_op itself is recorded under TFQ-0379.

## Source status

genesis_source.txt section 4 \[theorem\] plus a \[definition\] for no forced successor; Inertia.lean, Bridge.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)
- sha256 (`bytes`): `c6608bb88c7fcaf7c5d05e087c812033db60a3b3ee88fe28d209531279900f03`
- cited in: node.lean, node.source, record TFQ-0432
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Bridge`): recorded sha256 `c6608bb88c7fcaf7c5d05e087c812033db60a3b3ee88fe28d209531279900f03` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `second_token_required` | yes | yes | yes | Quot.sound, propext | `#print axioms second_token_required` |
| `single_token_carrier_bound` | yes | yes | yes | Quot.sound, propext | `#print axioms single_token_carrier_bound` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean, record TFQ-0432
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `genesis_underivable` | yes | yes | yes | none | `#print axioms genesis_underivable` |
| `underivable_of_empty` | yes | yes | yes | none | `#print axioms underivable_of_empty` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md`

- file: [dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md](../../../dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md)
- sha256 (`lf-normalised`): `71ea4752e407e3949482d477f52fc75ecc26a8d512680fd067b6f9372aa08342`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0432
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::challenge0_report`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/reading.rs::challenge0_generates_nothing`

## Routes

Incoming (1):

- `PGW-R-CHALLENGE0-INERTIA-SECOND-TOKEN` `DERIVED_LEAN`: [PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT](PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md) (DEFINITION), [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (0):

