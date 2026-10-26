# PGW-CANDIDATE-EXTENSION-GENERATOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the map from an unresolved residual, a demand given as source node, target pair, measure and bounds, to a legal proposal space, in the Alpha harness's three phases. Propose: a Proposal is Supply-shaped and no offering is ever executed. Evaluate: evaluate enumerates the sealed min_responses, groups them by canonical key and returns an EvalResult that is evidence only and is recomputed on the admission path. License: an authorization is bound to the source history digest, the target, the measure and the bounds, reuse with any field changed is refused, and uniqueness is not authorization (M3, M4). Endogenous demand generation stays OPEN (AE-DEMAND-OPEN): the generator answers a host-supplied demand and chooses none.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Alpha harness trust boundary of closeout §7: the host builds each License with make_license and the host's call is the authorization (assumption)

## Bottleneck

The generator ranges over the sealed candidate space within declared bounds, where 'minimum' and 'iso class' are relative to those bounds; the passage system's extensionProposals is a separate carrier with no checked bridge to the harness (S7).

## Source status

declared here; closeout.txt §3 M1-M8; ALPHA_HANDOFF §5-§7; education archive §6 item 5

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean)
- sha256 (`bytes`): `02869440f9049c3a60bf5c3b1647a9f211d04370f2853718a6d2adaa82551612`
- cited in: node.lean, record TFQ-0492
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.PrimitivePassage`): recorded sha256 `02869440f9049c3a60bf5c3b1647a9f211d04370f2853718a6d2adaa82551612` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/PrimitivePassage.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_rule` | yes | yes | yes | Quot.sound, propext | `#print axioms two_rule` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs)
- sha256 (`bytes`): `79461000d78d732752daca76f68288e27be855dc36605c2de578e0478e1798d1`
- cited in: node.rust, record TFQ-0492

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Proposal` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md`

- file: [dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md](../../../dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md)
- sha256 (`lf-normalised`): `095de25c2a341dab167ea2519d97efe359b317c02a8939cc6b2d66a7cb054173`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0492
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:101-116`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/driver_a.py::apply_licensed`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/evaluate.py::evaluate`

## Routes

Incoming (1):

- `PGW-R-CANDIDATE-EXTENSION-GENERATOR` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)

Outgoing (2):

- `PGW-R-ALPHA-LICENSE-BINDING-M1-M8` `COMPUTED`: [PGW-ALPHA-LICENSE-BINDING-M1-M8](PGW-ALPHA-LICENSE-BINDING-M1-M8.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-FOUR-GATE-ACTIVE-OBSTRUCTION` `DERIVED_PROSE`: [PGW-FOUR-GATE-ACTIVE-OBSTRUCTION](PGW-FOUR-GATE-ACTIVE-OBSTRUCTION.md) (DEFINITION)
