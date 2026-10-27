# PGW-NO-ENDOGENOUS-DEMAND-GENERATOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The continuation question asks whether the admitted structure can generate its next unresolved requirement without inspecting token glyphs, supplying a fresh datum, importing a new goal or assuming the continuation. The sealed answer is that no object-language endogenous demand generator was derived: a collapsed pair is not an active obstruction by itself, and the declared closure policy only reissues the admitted requirement pattern. Under that policy the fixed finite datum set reaches the all-pairs-separated fixpoint within n(n−1)/2 rounds, the size of the requirement language (allPairs_length). At the fixpoint no unresolved requirement exists in that language, so any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared pair-separation closure policy, genesis_source.txt section 3.9 (assumption)

## Bottleneck

This reports that no generator was derived, not that none exists in an extended language; raw rule admission can still erase a separation (TFQ-0385), and no longer or infinite tower is forced.

## Source status

genesis_source.txt section 9 written result with \[theorem\] and \[bounded theorem\] parts; Counting.lean allPairs_length

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Counting.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Counting.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Counting.lean)
- sha256 (`bytes`): `695d808307ea84d4e98ebd4bd63d1c570e8a93d5a8553f0db21af56093f3f996`
- cited in: node.lean, record TFQ-0451
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Counting`): recorded sha256 `695d808307ea84d4e98ebd4bd63d1c570e8a93d5a8553f0db21af56093f3f996` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Counting.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `allPairs_length` | yes | yes | yes | Quot.sound, propext | `#print axioms allPairs_length` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Rounds.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Rounds.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Rounds.lean)
- sha256 (`bytes`): `4b99ab31fc2a384709450f7d9a664d6aa35026a69599d98524802846f2e25b2d`
- cited in: node.lean, record TFQ-0451
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Rounds`): recorded sha256 `4b99ab31fc2a384709450f7d9a664d6aa35026a69599d98524802846f2e25b2d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Rounds.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closedRun_round_bound_from_empty` | yes | yes | yes | Quot.sound, propext | `#print axioms closedRun_round_bound_from_empty` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs)
- sha256 (`bytes`): `f9de5073d9258eac42c4e875a0c61f35f8ae2470dc4695097195387f270ec21a`
- cited in: node.rust, record TFQ-0451

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_round_bound` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0451

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_challenge_orbits` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md`

- file: [dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md](../../../dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md)
- sha256 (`lf-normalised`): `623f619de1578db6e990a309b9cfcd3f65f55c5a2293d9bf2a11dc898d285f90`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0451
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-NO-ENDOGENOUS-DEMAND-GENERATOR` `DERIVED_PROSE`: [PGW-POLICY-ENDPOINT-ALL-SEPARATED](PGW-POLICY-ENDPOINT-ALL-SEPARATED.md) (PROVED_LEAN), [TFQ-0385](TFQ-0385.md) (OPEN)

Outgoing (5):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS` `DERIVED_LEAN`: [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) (PROVED_LEAN)
- `PGW-R-IDENTITY-IS-INDEX-NOT-PROFILE` `DERIVED_PROSE`: [PGW-IDENTITY-IS-INDEX-NOT-PROFILE](PGW-IDENTITY-IS-INDEX-NOT-PROFILE.md) (PROVED_PROSE)
- `PGW-R-MINIMAL-OR-INITIAL-REFUSED` `DERIVED_PROSE`: [PGW-MINIMAL-OR-INITIAL-REFUSED](PGW-MINIMAL-OR-INITIAL-REFUSED.md) (PROVED_PROSE)
- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_PROSE`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)
