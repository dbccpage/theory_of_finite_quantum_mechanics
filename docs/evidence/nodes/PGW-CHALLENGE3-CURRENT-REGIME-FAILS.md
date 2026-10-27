# PGW-CHALLENGE3-CURRENT-REGIME-FAILS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Challenge 3 requires \<a\> and \<ab\> to be internally separable in the declared sense of positive derivability. Instantiating R2L_collapsed and R2F_collapsed, the current regime fails this: no witness context exists. The quotient barrier then applies: every function out of a quotient by a relation is constant on related elements (quotient_barrier, quot_barrier), and on the collapse classes of R2L any operation takes equal values on data 0 and 1 (barrier_R2L). An operation defined only on the current abstraction therefore cannot recover the required distinction, and a response has to change the regime.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The barrier concerns operations defined on the given quotient; it puts no bound on what an admitted augmentation of the regime can separate, which is the subject of the cost results (TFQ-0381).

## Source status

genesis_source.txt section 7.1 and question 5 \[theorem\]; Quot.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Quot.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Quot.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Quot.lean)
- sha256 (`bytes`): `8336fd5a34d1c54d909f648f7f528dc24c17696f9376c05610e0c80f3da564de`
- cited in: node.lean, node.source, record TFQ-0439
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Quot`): recorded sha256 `8336fd5a34d1c54d909f648f7f528dc24c17696f9376c05610e0c80f3da564de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Quot.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `barrier_R2L` | yes | yes | yes | Quot.sound, propext | `#print axioms barrier_R2L` |
| `quot_barrier` | yes | yes | yes | Quot.sound | `#print axioms quot_barrier` |
| `quotient_barrier` | yes | yes | yes | Quot.sound | `#print axioms quotient_barrier` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/separability.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/separability.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/separability.rs)
- sha256 (`bytes`): `2682476247f2d37a2af6afd02449d47bd3968765f2ddce116c3279445371841a`
- cited in: node.rust, record TFQ-0439

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `challenge2_collapse_is_total_in_both_readings` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0439

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separable` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0439_challenge3_current_regime_fails.md`

- file: [dag/derivations/02_genesis/tfq_0439_challenge3_current_regime_fails.md](../../../dag/derivations/02_genesis/tfq_0439_challenge3_current_regime_fails.md)
- sha256 (`lf-normalised`): `0018b94053a9d5a2a54ca9f83220258808329a4a926994f85262ba24cbd535c7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0439
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-CHALLENGE3-CURRENT-REGIME-FAILS` `DERIVED_LEAN`: [PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED](PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md) (PROVED_LEAN), [PGW-RESPONSES-COSTS-MU1-MU2](PGW-RESPONSES-COSTS-MU1-MU2.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MU1-MINIMUM-NOT-UNIQUE-L` `DERIVED_LEAN`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)
