# PGW-CHALLENGE0-INERTIA-SECOND-TOKEN

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At Challenge 0 the only object-language inscription is the opaque whole \<\>. In the token-erased Lean model nothing is derivable at genesis (genesis_underivable), and nothing is derivable in any regime with no instances and no rules (underivable_of_empty); the Challenge 0 computation records zero contexts and an empty derivable set in both readings. That no successor is internally forced is a property of the declared grammar, whose only state changes are external-event-indexed admissions, not a theorem about a forcing predicate. In the token-aware model a history whose datum admissions all carry one token leaves at most one admitted datum (single_token_carrier_bound), so a state with two data needs the admission of a second, different token (second_token_required).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

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

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs)
- sha256 (`bytes`): `0e3a65e8050ce25cab79310ab655dbae54e8c6bc1dbdbdbd130d8cc65dff4452`
- cited in: node.rust, record TFQ-0432

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `challenge0_generates_nothing` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0432

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `challenge0_report` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md`

- file: [dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md](../../../dag/derivations/02_genesis/tfq_0432_challenge0_inertia_second_token.md)
- sha256 (`lf-normalised`): `b3abe415a2304923c55d04de4715c5e9c036b57ef4826d212955d6739ccb5a63`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0432
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-CHALLENGE0-INERTIA-SECOND-TOKEN` `DERIVED_LEAN`: [PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT](PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md) (DEFINITION), [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)

Outgoing (0):

