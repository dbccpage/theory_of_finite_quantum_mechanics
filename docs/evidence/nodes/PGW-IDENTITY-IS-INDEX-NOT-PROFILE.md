# PGW-IDENTITY-IS-INDEX-NOT-PROFILE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Internal identity in the model is the datum index, never the profile (CL-IDENTITY-NOT-PROFILE). In reading F the first-round mu2 minimum admits one unary form with an instance marking datum 1; its only context is that form with one hole, so data 0 and 2 keep distinct indices with identical empty profiles while datum 1 is separated from both. A valid response separates the challenged pair by profiles, and other distinct data may stay observationally equivalent. The earlier sentence that from Challenge 3 round 1 onward each datum's internal identity is exactly its profile is false in the model and was withdrawn on 2026-09-08.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

None recorded.

## Bottleneck

Question 11 itself stays unanswered by instruction, because naming external structures is withheld; the two surviving discrimination styles, attribute-like unary marks and relation-like binary links, are internal descriptions only.

## Source status

genesis_source.txt question 11 internal statement (CL-IDENTITY-NOT-PROFILE) and withdrawal of 2026-09-08

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean)
- sha256 (`bytes`): `d9886a5c94b65a96b4f3364c3bb6cd63064a843e57d2afff536035ced039242f`
- cited in: node.lean, record TFQ-0452
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.Genesis19l57g1.Derivation.MinimalityF`): recorded sha256 `d9886a5c94b65a96b4f3364c3bb6cd63064a843e57d2afff536035ced039242f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/MinimalityF.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U0F` | yes | yes | yes | module-level | `#print axioms U0F` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md`

- file: [dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md](../../../dag/derivations/02_genesis/tfq_0452_identity_is_index_not_profile.md)
- sha256 (`lf-normalised`): `28000bdb0b720cea505ee79cbf3c2e65f19a431007c0fb47ce710d9059d72fc4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0452
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::profiles`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs::profiles`

## Routes

Incoming (1):

- `PGW-R-IDENTITY-IS-INDEX-NOT-PROFILE` `DERIVED_PROSE`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)

Outgoing (1):

- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_PROSE`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)
