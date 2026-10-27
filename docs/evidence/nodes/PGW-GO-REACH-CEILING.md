# PGW-GO-REACH-CEILING

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the base genesis-ongoing seed (terms a and b, arb asserted, xrx forbidden; the changes are identification, removal, adding a term and adding an assertion), ledger row D9 says every finite legal state with at least one term, names anywhere, is a result under either beginning. The Lean edit path reach_by_edits reaches a legal well-formed goal that contains the start's terms and keeps its names, by removing what the goal does not assert, adding the missing terms and adding the missing assertions, in that many changes; givenA_to_oneTerm and givenB_to_oneTerm reach the one-term result in two and three changes. Row N5 is the expressive ceiling that follows from D9: no statement about the asserting that holds in one finite legal state and fails in another follows from the seed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared exploration bound C8 (at most 5 terms FREE, 4 terms ANCHORED) for the computed half of D9 (assumption)

## Bottleneck

The Lean witnesses fix the names at a = 0, b = 1 or a = b = 0; names elsewhere rest on the rewriting step that ledger row O3 tracks (TFQ-0390), and the computed half of D9 stops at the declared term bound.

## Source status

genesis_ongoing paper/claim_ledger.md rows D9 and N5; lean4/H3V7N5QF/Paths.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean`

- file: [lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean)
- sha256 (`bytes`): `637d60e38cc3585a31b011fee1b9fcfd5b3cc262ddb614d57617dbf169a86d96`
- cited in: node.lean, record TFQ-0477
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.H3V7N5QF.Paths`): recorded sha256 `637d60e38cc3585a31b011fee1b9fcfd5b3cc262ddb614d57617dbf169a86d96` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `givenA_to_oneTerm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms givenA_to_oneTerm` |
| `givenB_to_oneTerm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms givenB_to_oneTerm` |
| `reach_by_edits` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach_by_edits` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/xry/explore.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/xry/explore.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/xry/explore.py)
- sha256 (`bytes`): `50c770826fcc2f730a7595059389f5a3c2caca3fe69877446c5c16a2d5d0fd5b`
- cited in: record TFQ-0477

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `explore` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md)
- sha256 (`lf-normalised`): `34530ca3f714274f7f03a1cd5dffcdd1fb76e50ec20749a03a72956e5f93fd1c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md`

- file: [dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md](../../../dag/derivations/02_genesis/tfq_0477_go_reach_ceiling.md)
- sha256 (`lf-normalised`): `79be81339e7a654524f2c4b9d3d7c30340f94130e6aa90d462b05c14104eec82`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0477
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:e9980870b3fbf4a10e6edee3b299b40d21596bee9bdc3d22a5c5e9cd871589c7:33`

## Absences recorded by the TFQ records

- TFQ-0477 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-REACH-CEILING` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-CONTRACTION-STEP2-STEP3` `DERIVED_LEAN`: [PGW-GO-CONTRACTION-STEP2-STEP3](PGW-GO-CONTRACTION-STEP2-STEP3.md) (PROVED_LEAN)
