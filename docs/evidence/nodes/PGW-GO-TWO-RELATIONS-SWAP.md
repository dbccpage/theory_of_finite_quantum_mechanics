# PGW-GO-TWO-RELATIONS-SWAP

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The eighth derivation adds a second relation s beside r, and the ninth combines two relations with an empty beginning: a state has terms and a multiplicity table per relation. The two relations interact through the terms alone: an assertion of one leaves the other part as it is, a term or an identification acts on both, and a sequence projects to a sequence on either part. The seventh derivation's one-relation states embed with nothing in s (proj_ofR9_false, proj_ofR9_true), and the exchange of the two relations is an involution (swap9_swap) and a symmetry of the results, the cost and reachability (ledger D16, with Reach9.swap and reach9_swap).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

proj_ofR9_false and proj_ofR9_true hold by rfl, so the embedding statements are definitional; the exchange symmetry is stated for the ninth seed's states, and later seeds that change the sameness re-prove it for their own (22:D10).

## Source status

genesis_ongoing paper/ninth/claim_ledger.md D16 and D17; lean4/Ninth/State.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Ninth/Reach.lean`

- file: [lean4/Imported/GenesisOngoing/Ninth/Reach.lean](../../../lean4/Imported/GenesisOngoing/Ninth/Reach.lean)
- sha256 (`bytes`): `f9b1fba535c2105546c6abb89577903e1e0e59cb065c8681c6da0905d4e2a72c`
- cited in: node.lean, record TFQ-0480
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Ninth.Reach`): recorded sha256 `f9b1fba535c2105546c6abb89577903e1e0e59cb065c8681c6da0905d4e2a72c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Ninth/Reach.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `reach9_swap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach9_swap` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Ninth/State.lean`

- file: [lean4/Imported/GenesisOngoing/Ninth/State.lean](../../../lean4/Imported/GenesisOngoing/Ninth/State.lean)
- sha256 (`bytes`): `4ec0bf99da08f7babb46c74cd94421591ae577b648d5bcb40fe6201acb793f55`
- cited in: node.lean, record TFQ-0480
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Ninth.State`): recorded sha256 `4ec0bf99da08f7babb46c74cd94421591ae577b648d5bcb40fe6201acb793f55` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Ninth/State.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `proj_ofR9_false` | yes | yes | yes | Quot.sound, propext | `#print axioms proj_ofR9_false` |
| `proj_ofR9_true` | yes | yes | yes | Quot.sound, propext | `#print axioms proj_ofR9_true` |
| `swap9_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms swap9_swap` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/ninth/state.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/ninth/state.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/ninth/state.py)
- sha256 (`bytes`): `9d9d54ab7b8a81bcb2e47472bccce13c61e6d7dd09268053cbaecc0ea821e3fc`
- cited in: record TFQ-0480

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `of_s` (python_symbol) | yes | yes | yes | - | - |
| `swap` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/claim_ledger.md)
- sha256 (`lf-normalised`): `24295ce3672d36f7ef252a5424d183eda4a8b13949bb3df5f5ee4ad1fc6d789c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md`

- file: [dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md](../../../dag/derivations/02_genesis/tfq_0480_go_two_relations_swap.md)
- sha256 (`lf-normalised`): `e63fca8bd326324ccc0fa3c75f9e4ca188ab51d63910d7f1f028ce5ca3b98e11`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0480
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:064fb17780045efefd70ca5b5e60edcdc3df7c7caf4cc260e251d77fd0e5aa64:108-110`

## Absences recorded by the TFQ records

- TFQ-0480 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-TWO-RELATIONS-SWAP` `DERIVED_LEAN`: [PGW-GO-MULTIPLICITY-MONOTONE](PGW-GO-MULTIPLICITY-MONOTONE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-ADMISSION-GATE` `DERIVED_PROSE`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)
