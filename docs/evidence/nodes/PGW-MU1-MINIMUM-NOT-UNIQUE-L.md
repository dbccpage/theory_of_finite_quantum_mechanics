# PGW-MU1-MINIMUM-NOT-UNIQUE-L

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under mu1 in reading L the minimum corrective augmentation is not unique. The unary mark deltaU0 and the binary link deltaBL are both valid two-item responses to Challenge 3 on R2L, no response of at most one item is valid, and their results U0 and BL are non-isomorphic because form arity is an isomorphism invariant (mu1_minimum_not_unique, U0_not_iso_BL). The theorem is stated over R2L only.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared item grammar, measure mu1 and the implemented isomorphism relation (assumption)

## Bottleneck

Reading L only: reading-F non-uniqueness is the bounded engine enumeration of five classes (TFQ-0442), and under mu2 the minimum is unique up to isomorphism (TFQ-0382).

## Source status

genesis_source.txt section 7.3 \[theorem, reading L\]; Minimality.lean mu1_minimum_not_unique

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Minimality.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Minimality.lean)
- sha256 (`bytes`): `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c`
- cited in: node.lean, node.source, record TFQ-0440
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Minimality`): recorded sha256 `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U0_not_iso_BL` | yes | yes | yes | Quot.sound, propext | `#print axioms U0_not_iso_BL` |
| `mu1_minimum_not_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms mu1_minimum_not_unique` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)
- sha256 (`bytes`): `1ce7119c17f0bac2b7f0a81487da586024d0d4e38a5004197e9765ebe96def98`
- cited in: node.rust, record TFQ-0440

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nothing_below_two_items_separates_the_target` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0440

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `min_responses` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md`

- file: [dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md](../../../dag/derivations/02_genesis/tfq_0440_mu1_minimum_not_unique_l.md)
- sha256 (`lf-normalised`): `8062d51d0ffdf1c0400619c21c8b6427dac24172939cd890f322fce2a2ae6113`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0440
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-MU1-MINIMUM-NOT-UNIQUE-L` `DERIVED_LEAN`: [PGW-CHALLENGE3-CURRENT-REGIME-FAILS](PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md) (PROVED_LEAN), [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `PGW-R-BOUNDED-TIE-CENSUS` `COMPUTED`: [PGW-BOUNDED-TIE-CENSUS](PGW-BOUNDED-TIE-CENSUS.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-MU1-ARITY-INDEXED-TIE-FAMILY` `DERIVED_LEAN`: [PGW-MU1-ARITY-INDEXED-TIE-FAMILY](PGW-MU1-ARITY-INDEXED-TIE-FAMILY.md) (PROVED_LEAN)
