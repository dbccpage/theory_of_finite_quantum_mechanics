# PGW-CONTEXTS-PLUGGING-PROFILES

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A context is an admitted form with a slot tuple of its arity in which every filled slot names an admitted datum and at least one slot is a hole; plugging a datum fills every hole with that same datum. Derivability is membership in the admitted instances or coverage by a uniform all-tuples rule, and no other inference exists. The profile of a datum is the set of well-formed contexts whose plugging is derivable. Two data are collapsed when their profiles are equal and separable when some well-formed context is derivable for one and not the other; that is the declared sense used for every separation requirement.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared derivability: admitted-instance membership or a uniform all-tuples rule, with no other inference (assumption)

## Bottleneck

These are declared definitions: separability means a difference in positive derivability only, and an imposed requirement records a demand for separation without making it hold.

## Source status

genesis_source.txt sections 3.3-3.5 and paper.md section 6 \[definition\]; Basic.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Basic.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Basic.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Basic.lean)
- sha256 (`bytes`): `ce682dc25fcdace62a9fef8a71019bf65b5a94e260c53748ea615e447ff3bed6`
- cited in: node.lean, record TFQ-0433
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Basic`): recorded sha256 `ce682dc25fcdace62a9fef8a71019bf65b5a94e260c53748ea615e447ff3bed6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Basic.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed` | yes | yes | yes | propext | `#print axioms collapsed` |
| `derivable` | yes | yes | yes | none | `#print axioms derivable` |
| `plug` | yes | yes | yes | none | `#print axioms plug` |
| `separable` | yes | yes | yes | propext | `#print axioms separable` |
| `wfCtx` | yes | yes | yes | propext | `#print axioms wfCtx` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/context.rs)
- sha256 (`bytes`): `f64df9adecf931d7b57907b47c03240742cd710230500c561b4ce14bba7c4d8f`
- cited in: node.rust, record TFQ-0433

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contexts` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs)
- sha256 (`bytes`): `225f3353d8ac938355ca451d7e50cb3ceeb0570f5247bd83d396f2d007b90450`
- cited in: node.rust, record TFQ-0433

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `profile` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0433

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `contexts` (python_symbol) | yes | yes | yes | - | - |
| `profile` (python_symbol) | yes | yes | yes | - | - |
| `separable` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0433_contexts_plugging_profiles.md`

- file: [dag/derivations/02_genesis/tfq_0433_contexts_plugging_profiles.md](../../../dag/derivations/02_genesis/tfq_0433_contexts_plugging_profiles.md)
- sha256 (`lf-normalised`): `03d144ab788bad849afa4e69dde7b190375e0e2fbf0866325fddc2f1f37cc651`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0433
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:ad3ab47c05abcec0f914042f034960d1143a7d7f023e1b4cedbfc0efd6023a3a:15`

## Routes

Incoming (1):

- `PGW-R-CONTEXTS-PLUGGING-PROFILES` `DERIVED_PROSE`: [PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS](PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md) (DEFINITION)

Outgoing (8):

- `APP-R-AUTH-TC0-TAPE-CONTROL-TYPING` `COMPUTED`: [AUTH-TC0-TAPE-CONTROL-TYPING](AUTH-TC0-TAPE-CONTROL-TYPING.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-AUTHF-DTM0-RULE-MACHINE` `DERIVED_PROSE`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION)
- `APP-R-AUTHF-DTM1-TOKEN-GRAMMAR` `DERIVED_PROSE`: [AUTHF-DTM1-TOKEN-GRAMMAR](AUTHF-DTM1-TOKEN-GRAMMAR.md) (DEFINITION)
- `APP-R-COMP-C2-ONE-HOLE-CONTEXTS` `DERIVED_LEAN`: [COMP-C2-ONE-HOLE-CONTEXTS](COMP-C2-ONE-HOLE-CONTEXTS.md) (PROVED_LEAN)
- `PGW-R-COLLAPSE-WITHOUT-INSTANCES` `DERIVED_LEAN`: [PGW-COLLAPSE-WITHOUT-INSTANCES](PGW-COLLAPSE-WITHOUT-INSTANCES.md) (PROVED_LEAN)
- `PGW-R-COLLECTION-EXTENSIONALITY` `DERIVED_LEAN`: [PGW-COLLECTION-EXTENSIONALITY](PGW-COLLECTION-EXTENSIONALITY.md) (PROVED_LEAN)
- `PGW-R-CONTEXT-COUNT-FORMULA` `DERIVED_LEAN`: [PGW-CONTEXT-COUNT-FORMULA](PGW-CONTEXT-COUNT-FORMULA.md) (PROVED_LEAN)
- `PGW-R-RESPONSES-COSTS-MU1-MU2` `DERIVED_PROSE`: [PGW-RESPONSES-COSTS-MU1-MU2](PGW-RESPONSES-COSTS-MU1-MU2.md) (DEFINITION)
