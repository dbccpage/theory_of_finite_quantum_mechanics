# PGW-CANDIDATE-EXTENSION-GENERATOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the map from an unresolved residual, a demand given as source node, target pair, measure and bounds, to a legal proposal space, in the Alpha harness's three phases. Propose: a Proposal is Supply-shaped and no offering is ever executed. Evaluate: evaluate enumerates the sealed min_responses, groups them by canonical key and returns an EvalResult that is evidence only and is recomputed on the admission path. License: an authorization is bound to the source history digest, the target, the measure and the bounds, reuse with any field changed is refused, and uniqueness is not authorization (M3, M4). Endogenous demand generation stays OPEN (AE-DEMAND-OPEN): the generator answers a host-supplied demand and chooses none.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

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

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md`

- file: [dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md](../../../dag/derivations/02_genesis/tfq_0492_candidate_extension_generator.md)
- sha256 (`lf-normalised`): `8f674d07e588c04026ae0c4985872abb32d256a901226edc0e6193393d41fc7e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0492
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
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

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/driver_a.py::apply_licensed`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/evaluate.py::evaluate`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs::Proposal`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean::two_rule`

## Routes

Incoming (1):

- `PGW-R-CANDIDATE-EXTENSION-GENERATOR` `DERIVED_PROSE`: [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)

Outgoing (2):

- `PGW-R-ALPHA-LICENSE-BINDING-M1-M8` `COMPUTED`: [PGW-ALPHA-LICENSE-BINDING-M1-M8](PGW-ALPHA-LICENSE-BINDING-M1-M8.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-FOUR-GATE-ACTIVE-OBSTRUCTION` `DERIVED_PROSE`: [PGW-FOUR-GATE-ACTIVE-OBSTRUCTION](PGW-FOUR-GATE-ACTIVE-OBSTRUCTION.md) (DEFINITION)
