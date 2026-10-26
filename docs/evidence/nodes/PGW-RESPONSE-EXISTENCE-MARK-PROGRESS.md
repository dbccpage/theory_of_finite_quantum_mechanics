# PGW-RESPONSE-EXISTENCE-MARK-PROGRESS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On any well-formed regime whose imposed requirements are all separated, for any two distinct admitted data i and j, the two-item delta of one fresh unary form and one instance of it at datum j is a valid response to Separate(i, j) and keeps every imposed requirement separated (mark_progress). Derivability of instances of the old forms is unchanged by this extension, so old witnesses survive (derivable_extend). The standalone replay checks fresh-mark preservation for 3,996 targets across 1,436 regimes, and no terminal_no_response node occurs in any exported run.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py)
- sha256 (`bytes`): `60d4be592f4528fa5f40f3fa03179c84225daf914c79660f62cbd016fb649c71`
- cited in: record TFQ-0445

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `python_replay` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md`

- file: [dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md](../../../dag/derivations/02_genesis/tfq_0445_response_existence_mark_progress.md)
- sha256 (`lf-normalised`): `c750ac583b5524f1ec46695312659a8927f2b1090006b60ac761353d07a6337a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0445
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0445 rust: no Rust check of fresh-mark progress; the standalone replay checks it against the frozen Python model

## Routes

Incoming (1):

- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN), [PGW-RESPONSES-COSTS-MU1-MU2](PGW-RESPONSES-COSTS-MU1-MU2.md) (DEFINITION)

Outgoing (1):

- `PGW-R-PRUNING-LEMMAS-COST-TWO` `DERIVED_LEAN`: [PGW-PRUNING-LEMMAS-COST-TWO](PGW-PRUNING-LEMMAS-COST-TWO.md) (PROVED_LEAN)
