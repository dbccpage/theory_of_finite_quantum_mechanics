# PGW-IDENTITY-IS-INDEX-NOT-PROFILE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Internal identity in the model is the datum index, never the profile (CL-IDENTITY-NOT-PROFILE). In reading F the first-round mu2 minimum admits one unary form with an instance marking datum 1; its only context is that form with one hole, so data 0 and 2 keep distinct indices with identical empty profiles while datum 1 is separated from both. A valid response separates the challenged pair by profiles, and other distinct data may stay observationally equivalent. The earlier sentence that from Challenge 3 round 1 onward each datum's internal identity is exactly its profile is false in the model and was withdrawn on 2026-09-08.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Question 11 itself stays unanswered by instruction, because naming external structures is withheld; the two surviving discrimination styles, attribute-like unary marks and relation-like binary links, are internal descriptions only.

## Source status

CL-IDENTITY-NOT-PROFILE and U0F empty-profile pair coincidence mechanized in MinimalityF.lean and WdpBatch7.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean)
- sha256 (`bytes`): `325cb7b3dd05bf6b4c4f5081935af36bbddc9493b7404f2bb3cce46bc0e32fc5`
- cited in: node.lean, record TFQ-0452
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch7.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch7.distinct_indices_can_share_profile` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch7.distinct_indices_can_share_profile` |
| `WitnessedDifference.WdpBatch7.identity_is_index_not_profile_u0f` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch7.identity_is_index_not_profile_u0f` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean](../../../lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean)
- sha256 (`bytes`): `d70d5131314c35edb40ce737ca0d1a796944c8d3bc15705436466313294f5214`
- cited in: node.lean, record TFQ-0452
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_mssn_sn.json](../../../evidence/lean_receipts/lean_replay_campaign_mssn_sn.json) (module `Imported.GenesisDerivation.Derivation.MinimalityF`): recorded sha256 `d70d5131314c35edb40ce737ca0d1a796944c8d3bc15705436466313294f5214` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U0F` | yes | yes | yes | module-level | `#print axioms U0F` |

- counts toward the grade: yes

### Rust: `atlas/finite_obstruction_calculus/genesis/code/rust/src/profile.rs`

- file: [atlas/finite_obstruction_calculus/genesis/code/rust/src/profile.rs](../../../atlas/finite_obstruction_calculus/genesis/code/rust/src/profile.rs)
- sha256 (`bytes`): `225f3353d8ac938355ca451d7e50cb3ceeb0570f5247bd83d396f2d007b90450`
- cited in: node.rust, record TFQ-0452

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `profiles` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/genesis/code/derivation/observe.py`

- file: [atlas/finite_obstruction_calculus/genesis/code/derivation/observe.py](../../../atlas/finite_obstruction_calculus/genesis/code/derivation/observe.py)
- sha256 (`bytes`): `78443d67e613d9cc9924538fe2e0a5acaf81f4654440bfe8586e16652f0317ba`
- cited in: record TFQ-0452

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `profiles` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md`

- file: [dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md](../../../dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md)
- sha256 (`lf-normalised`): `5b0f79245c51831577454e99553b1ee71aa5da40db6524d29fc3102ba1e8d09c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0452
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-IDENTITY-IS-INDEX-NOT-PROFILE` `DERIVED_LEAN`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_LEAN`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_LEAN)
