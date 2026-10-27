# PGW-COLLAPSE-WITHOUT-INSTANCES

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With no admitted instances, the derivability of a plugged context depends only on its form, so every pair of data is observationally collapsed (collapsed_of_no_insts). Uniform rules do not change this: a ruled form makes every plugging derivable alike. Retaining another datum alone therefore need not increase expressive power.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The statement covers instance-free regimes only; once an instance is admitted collapse is decided by the profiles, and a later uniform rule can again erase a separation (TFQ-0385).

## Source status

genesis_source.txt section 5 and paper.md section 6 \[theorem\]; Inertia.lean collapsed_of_no_insts

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Inertia.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Inertia.lean)
- sha256 (`bytes`): `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67`
- cited in: node.lean, record TFQ-0434
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Inertia`): recorded sha256 `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_of_no_insts` | yes | yes | yes | propext | `#print axioms collapsed_of_no_insts` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/profile.rs)
- sha256 (`bytes`): `225f3353d8ac938355ca451d7e50cb3ceeb0570f5247bd83d396f2d007b90450`
- cited in: node.rust, record TFQ-0434

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `coverage_is_constant_across_data_at_a_fixed_context` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0434

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_pairs` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0434_collapse_without_instances.md`

- file: [dag/derivations/02_genesis/tfq_0434_collapse_without_instances.md](../../../dag/derivations/02_genesis/tfq_0434_collapse_without_instances.md)
- sha256 (`lf-normalised`): `e46e4aad29e1b8f5624c616ab76ffe746f3bb4849cc96806ec9e67298a19b6f8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0434
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-COLLAPSE-WITHOUT-INSTANCES` `DERIVED_LEAN`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (1):

- `PGW-R-CHALLENGE2-ADMITTED-BUT-COLLAPSED` `DERIVED_LEAN`: [PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED](PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md) (PROVED_LEAN)
