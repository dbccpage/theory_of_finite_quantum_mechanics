# PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed manuscript declares two levels. The metatheory holds presentation tokens (strings), event sequences, indices, finite data structures and arithmetic; the object language holds only what a regime admits. Token glyphs, component counts, order, concatenation, multiplicity, substring structure, matching and string equality live in the metatheory unless an admitted judgment internalizes a distinction. Presentation identity (token equality) is metatheory only, internal identity is the datum index, and no semantic interpretation is ever assigned.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared two-level metatheory/object-language split of genesis_source.txt section 2 (assumption)

## Bottleneck

A declared split, not a theorem: the Lean model has no tokens by construction, so token-blindness is structural there and is checked in Python and Rust by renaming tests; admission order is visible to the token-aware metatheory and erased at the object level.

## Source status

genesis_source.txt section 2 \[declared metatheory\]; Bridge.lean admission-order theorems

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)
- sha256 (`bytes`): `c6608bb88c7fcaf7c5d05e087c812033db60a3b3ee88fe28d209531279900f03`
- cited in: node.lean, record TFQ-0430
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Bridge`): recorded sha256 `c6608bb88c7fcaf7c5d05e087c812033db60a3b3ee88fe28d209531279900f03` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `order_erased_at_object_level` | yes | yes | yes | Quot.sound, propext | `#print axioms order_erased_at_object_level` |
| `order_visible_to_metatheory` | yes | yes | yes | Quot.sound, propext | `#print axioms order_visible_to_metatheory` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md`

- file: [dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md](../../../dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md)
- sha256 (`lf-normalised`): `f3a4b3738ec59809c0da5793b08997ecb4868774018dd33f9ef82a7a038e64f9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0430
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/genesis.md`

- file: `omega_engine_education/documentation/001_oegen/genesis.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::serialize`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs::tokens_are_forgotten_by_the_key`

## Routes

Incoming (1):

- `PGW-R-METATHEORY-OBJECT-LANGUAGE-SPLIT` `DERIVED_PROSE`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CHALLENGE0-INERTIA-SECOND-TOKEN` `DERIVED_LEAN`: [PGW-CHALLENGE0-INERTIA-SECOND-TOKEN](PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md) (PROVED_LEAN)
- `PGW-R-REGIME-ISOMORPHISM-UNORDERED-PAIRS` `DERIVED_PROSE`: [PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS](PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md) (DEFINITION)
