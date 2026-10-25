# PGW-COUNT-INVARIANCE-TRANSPORT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Observational collapse is invariant under a renaming of datum indices with forms fixed: the renamed regime collapses the renamed pair exactly when the original regime collapses the original pair (collapsed_rename). For any caller-supplied candidate pair list with deciders that track collapse, the collapsed-pair counts before and after renaming agree (collapsedCount_rename). Collapse also transports across a full two-bijection regime isomorphism (collapsed_transport) and under the combined datum-and-form action (collapsed_renameDataForm). Requirements never enter collapse, so the renaming action leaves them alone.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
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

The count transport acts on datum indices with forms fixed and takes the pair list and decider as parameters; token renaming is inexpressible in the token-erased Lean model, and the executable count and the identification of the mapped list with the engine's pair enumeration stay computational.

## Source status

genesis_source.txt question 8 and register row R6 \[theorem\]; CountTransport.lean, IsoCollapse.lean, FormTransport.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean)
- sha256 (`bytes`): `e9975572e9e521c76a21cff3485f77bcf2bb18062045fc1c09ad375930540088`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.CountTransport`): recorded sha256 `e9975572e9e521c76a21cff3485f77bcf2bb18062045fc1c09ad375930540088` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsedCount_rename` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsedCount_rename` |
| `collapsed_rename` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_rename` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean)
- sha256 (`bytes`): `b3b430792e69cd8c64a10b71637d34bc3691b83ef0304362fa97f8919eda5b9f`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.FormTransport`): recorded sha256 `b3b430792e69cd8c64a10b71637d34bc3691b83ef0304362fa97f8919eda5b9f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_renameDataForm` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_renameDataForm` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean)
- sha256 (`bytes`): `1a269017cea3c5f1c1f6d8d37cedd29297ea73d38c6876cb7d2f660c70575d9c`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.IsoCollapse`): recorded sha256 `1a269017cea3c5f1c1f6d8d37cedd29297ea73d38c6876cb7d2f660c70575d9c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_transport` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_transport` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md`

- file: [dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md](../../../dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md)
- sha256 (`lf-normalised`): `b0109cd9f3a7813d8b940b692109e8f1f145dd2ffae493194a2054149edf843b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0447
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::rename`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::collapsed_pairs`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::the_key_is_invariant_under_every_renaming`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::a_single_collapsed_pair_transports_under_renaming`

## Routes

Incoming (1):

- `PGW-R-COUNT-INVARIANCE-TRANSPORT` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-BRANCH-TREES-AND-ROLES` `COMPUTED`: [PGW-BRANCH-TREES-AND-ROLES](PGW-BRANCH-TREES-AND-ROLES.md) (COMPUTATIONALLY_CHECKED)
