# PGW-COUNT-INVARIANCE-TRANSPORT

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Observational collapse is invariant under a renaming of datum indices with forms fixed: the renamed regime collapses the renamed pair exactly when the original regime collapses the original pair (collapsed_rename). For any caller-supplied candidate pair list with deciders that track collapse, the collapsed-pair counts before and after renaming agree (collapsedCount_rename). Collapse also transports across a full two-bijection regime isomorphism (collapsed_transport) and under the combined datum-and-form action (collapsed_renameDataForm). Requirements never enter collapse, so the renaming action leaves them alone.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The count transport acts on datum indices with forms fixed and takes the pair list and decider as parameters; token renaming is inexpressible in the token-erased Lean model, and the executable count and the identification of the mapped list with the engine's pair enumeration stay computational.

## Source status

genesis_source.txt question 8 and register row R6 \[theorem\]; CountTransport.lean, IsoCollapse.lean, FormTransport.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/CountTransport.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/CountTransport.lean](../../../lean4/Imported/GenesisDerivation/Derivation/CountTransport.lean)
- sha256 (`bytes`): `bf4dd5b01b66a1b131204d91edca721599668ac2b38952753097126601358fb2`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.CountTransport`): recorded sha256 `bf4dd5b01b66a1b131204d91edca721599668ac2b38952753097126601358fb2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/CountTransport.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsedCount_rename` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsedCount_rename` |
| `collapsed_rename` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_rename` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/FormTransport.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/FormTransport.lean](../../../lean4/Imported/GenesisDerivation/Derivation/FormTransport.lean)
- sha256 (`bytes`): `c3be3c53567869fea4057ac05b7968d9f670c92cd97f7bd98ac8606aec62b076`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.FormTransport`): recorded sha256 `c3be3c53567869fea4057ac05b7968d9f670c92cd97f7bd98ac8606aec62b076` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/FormTransport.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_renameDataForm` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_renameDataForm` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/IsoCollapse.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/IsoCollapse.lean](../../../lean4/Imported/GenesisDerivation/Derivation/IsoCollapse.lean)
- sha256 (`bytes`): `1a6cdbcf5dd4b25dd865c368203265446d95d2a2d55c110c296ea2f33d3b72b6`
- cited in: node.lean, record TFQ-0447
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.IsoCollapse`): recorded sha256 `1a6cdbcf5dd4b25dd865c368203265446d95d2a2d55c110c296ea2f33d3b72b6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/IsoCollapse.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_transport` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_transport` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)
- sha256 (`bytes`): `bd91e864bb54ade9ed3890a65d89f57500cef2fb66e060eb5e18359d6c6187ea`
- cited in: node.rust, record TFQ-0447

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `the_key_is_invariant_under_every_renaming` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs)
- sha256 (`bytes`): `f9de5073d9258eac42c4e875a0c61f35f8ae2470dc4695097195387f270ec21a`
- cited in: node.rust, record TFQ-0447

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `a_single_collapsed_pair_transports_under_renaming` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py)
- sha256 (`bytes`): `b0f1f3bcf05126111a07706f4388a9fff5e30455d4b8f127966cf99ab0d0886e`
- cited in: record TFQ-0447

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `rename` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0447

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_pairs` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md`

- file: [dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md](../../../dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md)
- sha256 (`lf-normalised`): `538971c895c4c15b8e2cc40cd6ef94c2de69831e601cbfdfae79f15e36ca1ea8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0447
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-COUNT-INVARIANCE-TRANSPORT` `DERIVED_LEAN`: [PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR](PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-BRANCH-TREES-AND-ROLES` `COMPUTED`: [PGW-BRANCH-TREES-AND-ROLES](PGW-BRANCH-TREES-AND-ROLES.md) (COMPUTATIONALLY_CHECKED)
