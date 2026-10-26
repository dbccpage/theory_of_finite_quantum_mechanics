# PGW-RESPONSE-EXISTENCE-MARK-PROGRESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On any well-formed regime whose imposed requirements are all separated, for any two distinct admitted data i and j, the two-item delta of one fresh unary form and one instance of it at datum j is a valid response to Separate(i, j) and keeps every imposed requirement separated (mark_progress). Derivability of instances of the old forms is unchanged by this extension, so old witnesses survive (derivable_extend). The standalone replay checks fresh-mark preservation for 3,996 targets across 1,436 regimes, and no terminal_no_response node occurs in any exported run.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is response existence for a supplied demand only; it does not establish autonomous demand generation or an unbounded tower, and the preserved conjunct ranges over the requirement store, not over all separable pairs.

## Source status

genesis_source.txt section 8.2 \[theorem\] (CL-PROGRESS); Progress.lean mark_progress

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Progress.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Progress.lean)
- sha256 (`bytes`): `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce`
- cited in: node.lean, record TFQ-0445
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Progress`): recorded sha256 `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `derivable_extend` | yes | yes | yes | propext | `#print axioms derivable_extend` |
| `mark_progress` | yes | yes | yes | Quot.sound, propext | `#print axioms mark_progress` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md`

- file: [dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md](../../../dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md)
- sha256 (`lf-normalised`): `c71680fc99c4e78c0d8feecc720716bdf5bee2ece47022713663ed0b11b9e10e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0445
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`

## Absences recorded by the TFQ records

- TFQ-0445 rust: no Rust check of fresh-mark progress; the standalone replay checks it against the frozen Python model

## Routes

Incoming (1):

- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN), [PGW-RESPONSES-COSTS-MU1-MU2](PGW-RESPONSES-COSTS-MU1-MU2.md) (DEFINITION)

Outgoing (1):

- `PGW-R-PRUNING-LEMMAS-COST-TWO` `DERIVED_LEAN`: [PGW-PRUNING-LEMMAS-COST-TWO](PGW-PRUNING-LEMMAS-COST-TWO.md) (PROVED_LEAN)
