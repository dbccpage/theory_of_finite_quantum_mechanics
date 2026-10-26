# PGW-PRUNING-LEMMAS-COST-TWO

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A separation witness never inhabits a uniformly ruled form, so shrinking the final rule set preserves every separation (separable_of_subrules). With the item-level bridge applyDelta_dropRules, a delta containing a uniform-rule item is never minimal: dropping its rule items leaves a valid, strictly shorter delta with the same new-form arity sum (rule_item_never_minimal). The mention lemma shows that appending instances that mention neither datum of a pair leaves that pair's collapse unchanged (collapsed_append_unmentioning), and under the well-formedness conjuncts a fresh unreferenced datum or form leaves the collapse of every existing pair unchanged (collapsed_fresh_datum, collapsed_fresh_form).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The three irrelevance inputs and the rule bridge are theorems, but the enclosing claim that the pruned cost-2 enumeration contains every minimum (CL-PRUNE-STRUCTURAL) stays a bounded theorem on computational evidence over the declared grammar slice.

## Source status

genesis_source.txt section 8.3 \[theorem\] (R1-R4) with CL-PRUNE-STRUCTURAL \[bounded theorem\]; Progress, RuleBridge, Mention .lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Mention.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Mention.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- sha256 (`bytes`): `73f4b5ee8c91290124be0c39541217256f2ec47e26d23b887fa40f8ba9b97f38`
- cited in: node.lean, node.source, record TFQ-0446
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Mention`): recorded sha256 `73f4b5ee8c91290124be0c39541217256f2ec47e26d23b887fa40f8ba9b97f38` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Mention.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_append_unmentioning` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_append_unmentioning` |
| `collapsed_fresh_datum` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_fresh_datum` |
| `collapsed_fresh_form` | yes | yes | yes | propext | `#print axioms collapsed_fresh_form` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Progress.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Progress.lean)
- sha256 (`bytes`): `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce`
- cited in: node.lean, record TFQ-0446
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Progress`): recorded sha256 `1a6864314f6909227f3b41d3af68bcbca5b1c286e8a2c1e889381d302e8a92ce` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Progress.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separable_of_subrules` | yes | yes | yes | propext | `#print axioms separable_of_subrules` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean)
- sha256 (`bytes`): `2f5e9cbd5fa01227b953951195d39129ad389ccad6d9098a99ac78920356f467`
- cited in: node.lean, record TFQ-0446
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.RuleBridge`): recorded sha256 `2f5e9cbd5fa01227b953951195d39129ad389ccad6d9098a99ac78920356f467` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rule_item_never_minimal` | yes | yes | yes | propext | `#print axioms rule_item_never_minimal` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/enumeration.rs)
- sha256 (`bytes`): `a829a2a7ef365ce27b07cbd4d2fc3069f7b0653ce7a2a82fd3e5cd437407708a`
- cited in: node.rust, record TFQ-0446

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `iter_cost2_deltas` (rust_symbol) | yes | yes | yes | - | - |
| `pruned_and_unpruned_agree_on_valid_deltas` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0446

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `iter_cost2_deltas` (python_symbol) | yes | yes | yes | - | - |
| `iter_full_deltas` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0446_pruning_lemmas_cost_two.md`

- file: [dag/derivations/02_genesis/tfq_0446_pruning_lemmas_cost_two.md](../../../dag/derivations/02_genesis/tfq_0446_pruning_lemmas_cost_two.md)
- sha256 (`lf-normalised`): `23f5188cbc3fd45baffdc85574a710648d1d6cf3bcfabee089f47b8792ab6cae`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0446
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-PRUNING-LEMMAS-COST-TWO` `DERIVED_LEAN`: [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-BRANCH-TREES-AND-ROLES` `COMPUTED`: [PGW-BRANCH-TREES-AND-ROLES](PGW-BRANCH-TREES-AND-ROLES.md) (COMPUTATIONALLY_CHECKED)
