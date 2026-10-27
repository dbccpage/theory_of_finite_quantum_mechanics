# PGW-CONTEXT-COUNT-FORMULA

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a regime with n admitted data, a form of arity a has (n+1)^a − n^a well-formed contexts: each slot is a hole or one of n data, less the n^a hole-free tuples, so |Ctx(R)| = Σ_f ((n+1)^{a_f} − n^{a_f}), with distinct form identifiers kept disjoint even when their arities coincide. The companion Lean module establishes the per-form count for the recursive word enumeration (contextWords_length), characterizes its members as exactly the well-formed words of that length containing a hole (contextWords_mem), and shows the enumeration has no repetitions (contextWords_nodup). The standalone replay checks the formula against the frozen Python enumeration in 35 cases (n from 0 to 4, arity 1 to 7), and Python and Rust enumerate the contexts independently.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is a companion result for the slot words of one form; the sum over forms is the written corollary of ledger row WDP-P000-015, which attributes it to no compiled source theorem, and large arities make profile enumeration expensive.

## Source status

paper.md section 6 counting corollary (ledger WDP-P000-015); companion Paper.lean contextWords theorems

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Paper.lean`

- file: [lean4/Imported/GenesisDerivation/Paper.lean](../../../lean4/Imported/GenesisDerivation/Paper.lean)
- sha256 (`bytes`): `028a885d67b4255d787dc087b2ef28a9f1b73ed45742ad55c0c66f08fcddc743`
- cited in: node.lean, record TFQ-0436
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Paper`): recorded sha256 `028a885d67b4255d787dc087b2ef28a9f1b73ed45742ad55c0c66f08fcddc743` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contextWords_length` | yes | yes | yes | Quot.sound, propext | `#print axioms contextWords_length` |
| `contextWords_mem` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms contextWords_mem` |
| `contextWords_nodup` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms contextWords_nodup` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs)
- sha256 (`bytes`): `f64df9adecf931d7b57907b47c03240742cd710230500c561b4ce14bba7c4d8f`
- cited in: node.rust, record TFQ-0436

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `a_binary_form_over_two_data_has_five_contexts` (rust_test) | yes | yes | yes | - | - |
| `contexts` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0436

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contexts` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py)
- sha256 (`bytes`): `60d4be592f4528fa5f40f3fa03179c84225daf914c79660f62cbd016fb649c71`
- cited in: record TFQ-0436

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `python_replay` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/code/fixtures/historical_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/fixtures/historical_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis/code/fixtures/historical_claim_ledger.md)
- sha256 (`lf-normalised`): `6d4beb7f0f2a00da850d837edb4c21e30deaf47422ddacff68966bc4220311c3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0436_context_count_formula.md`

- file: [dag/derivations/02_genesis/tfq_0436_context_count_formula.md](../../../dag/derivations/02_genesis/tfq_0436_context_count_formula.md)
- sha256 (`lf-normalised`): `6f60eb2ebaf67ec689ca7b6a96269a94efa6cb14151b8f85bea8360ec22ef139`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0436
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-CONTEXT-COUNT-FORMULA` `DERIVED_LEAN`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (1):

- `APP-R-COMP-C2-CONTEXT-COUNTS-CHECKED` `COMPUTED`: [COMP-C2-CONTEXT-COUNTS-CHECKED](COMP-C2-CONTEXT-COUNTS-CHECKED.md) (COMPUTATIONALLY_CHECKED)
