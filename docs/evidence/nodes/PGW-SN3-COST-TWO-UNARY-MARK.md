# PGW-SN3-COST-TWO-UNARY-MARK

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(3) requires the admitted opaque data \<a\> and \<ab\> to be separated, starting from a form-less, instance-less regime and counting each admitted item once. No response of at most one item separates the pair (cost1_insufficient_general), and one new unary form with one instance at a demanded endpoint does, so the minimum item count is 2 in both readings. Under item count the minima tie: at max_items 2 and max_arity 2 reading L has 6 valid deltas in 3 classes (unary mark, binary link, binary self-loop) and reading F has 10 in 5, and in reading L the tie class over all arities is countably infinite. Under the lexicographic cost mu2 = (items, new-form arity sum) the unique minimum up to source isomorphism is the unary mark (2,1), in reading L (mu2_unique) and reading F (mu2_unique_F).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared response grammar NewDatum, NewForm, NewInst, NewRuleAll and the costs mu1 and mu2 of the sealed Genesis account (assumption)

## Bottleneck

The mu2 minimizer is a unary mark, not a binary edge: a binary link is one of the tied mu1 responses and an edge reading is an additional interpretation. S3Separation.cost_floor in sn_core.py is a fixture parameter, and testing that it equals 2 does not reprove minimality; the cost belongs to this item grammar only.

## Source status

genesis_source.txt section 7 (Challenge 3, mu1 ties, mu2 uniqueness); Lean Derivation/Minimality and MinimalityF

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Minimality.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Minimality.lean)
- sha256 (`bytes`): `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c`
- cited in: node.lean, record TFQ-0514
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Minimality`): recorded sha256 `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cost1_insufficient_general` | yes | yes | yes | propext | `#print axioms cost1_insufficient_general` |
| `mu2_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms mu2_unique` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean](../../../lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean)
- sha256 (`bytes`): `d70d5131314c35edb40ce737ca0d1a796944c8d3bc15705436466313294f5214`
- cited in: node.lean, record TFQ-0514
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.GenesisDerivation.Derivation.MinimalityF`): recorded sha256 `d70d5131314c35edb40ce737ca0d1a796944c8d3bc15705436466313294f5214` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mu2_unique_F` | yes | yes | yes | Quot.sound, propext | `#print axioms mu2_unique_F` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)
- sha256 (`bytes`): `1ce7119c17f0bac2b7f0a81487da586024d0d4e38a5004197e9765ebe96def98`
- cited in: node.rust, record TFQ-0514

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `min_responses` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0514

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `iter_cost2_deltas` (python_symbol) | yes | yes | yes | - | - |
| `mu2` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md`

- file: [dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md](../../../dag/derivations/05_mssn_sn/tfq_0514_sn3_cost_two_unary_mark.md)
- sha256 (`lf-normalised`): `4e165a664d50fd273ba4c425932e0b2b350f2068c4db7be39095cb4a4190cfba`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0514
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:217d5f5c9cdc03ec3787cd9e1c38bfca51fa068ca55f96b61ce4c1c61d34b3fb:28-36`

## Routes

Incoming (1):

- `PGW-R-SN3-COST-TWO-UNARY-MARK` `DERIVED_LEAN`: [PGW-SN2-OPAQUE-COLLAPSE](PGW-SN2-OPAQUE-COLLAPSE.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-SN-ENDPOINT-LEMMA` `DERIVED_LEAN`: [PGW-SN-ENDPOINT-LEMMA](PGW-SN-ENDPOINT-LEMMA.md) (PROVED_LEAN)
- `PGW-R-SN4-POLICY-CLOSURE-CYCLE-SPACE` `DERIVED_PROSE`: [PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE](PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md) (PROVED_PROSE)
