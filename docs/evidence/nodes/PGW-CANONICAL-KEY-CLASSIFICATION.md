# PGW-CANONICAL-KEY-CLASSIFICATION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If a representative map C lies in each regime's isomorphism orbit and is constant on orbits, then C(R) = C(S) exactly when R ≅ S, and an injective serialization of the representatives gives the same criterion for keys (key_classification, conditional on both hypotheses). Companion results remove those hypotheses for the concrete search: equal sorted five-field tuples after relabeling by supplied bijections imply isomorphism (serializedRelabel_sound), and the length-prefixed unsigned 64-bit wire encoding is injective on words below 2^64 (portableBytes_injective). Exhaustive search over all datum and form permutations attains a least structural key (canonicalKey_attained), and for well-formed regimes with duplicate-free collections the keys, and under the word bounds their byte encodings, are equal exactly when the regimes are isomorphic (canonicalKey_classification, canonicalBytes_classification).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The abstract key_classification needs an in-orbit, orbit-invariant choice; the concrete search results assume no orbit oracle but cover the Lean search only, and refinement of the optimized Python and Rust programs remains a separate engineering obligation, checked by finite agreement on 1,436 labelled regimes.

## Source status

paper.md section 10 canonicalization (ledger WDP-P000-022); CanonicalMinimizer.lean and companion PaperCanonical, PaperWire, PaperSearch .lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean`

- file: [lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean](../../../lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean)
- sha256 (`bytes`): `ee3e086e5d280fadd1c2cbd4dd729e429dd7ca157f996c5c83e8d970d8b31f4c`
- cited in: node.lean, record TFQ-0459
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.CanonicalMinimizer`): recorded sha256 `ee3e086e5d280fadd1c2cbd4dd729e429dd7ca157f996c5c83e8d970d8b31f4c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `key_classification` | yes | yes | yes | Quot.sound | `#print axioms key_classification` |
- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/PaperCanonical.lean`

- file: [lean4/Imported/Genesis19l57g1/PaperCanonical.lean](../../../lean4/Imported/Genesis19l57g1/PaperCanonical.lean)
- sha256 (`bytes`): `e7bf20a70e6f11904670da6e366667cbafd353ed85627ceb53cef17f44128ebf`
- cited in: node.lean, record TFQ-0459
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.PaperCanonical`): recorded sha256 `e7bf20a70e6f11904670da6e366667cbafd353ed85627ceb53cef17f44128ebf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/PaperCanonical.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `serializedRelabel_sound` | yes | yes | yes | Quot.sound, propext | `#print axioms serializedRelabel_sound` |
- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/PaperSearch.lean`

- file: [lean4/Imported/Genesis19l57g1/PaperSearch.lean](../../../lean4/Imported/Genesis19l57g1/PaperSearch.lean)
- sha256 (`bytes`): `1d94300a7e6a83f10e75499f7971510d03b57e45c8f67fbb8740c60cbb880cd9`
- cited in: node.lean, record TFQ-0459
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.PaperSearch`): recorded sha256 `1d94300a7e6a83f10e75499f7971510d03b57e45c8f67fbb8740c60cbb880cd9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/PaperSearch.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonicalBytes_classification` | yes | yes | yes | Quot.sound, propext | `#print axioms canonicalBytes_classification` |
| `canonicalKey_attained` | yes | yes | yes | Quot.sound, propext | `#print axioms canonicalKey_attained` |
- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/PaperWire.lean`

- file: [lean4/Imported/Genesis19l57g1/PaperWire.lean](../../../lean4/Imported/Genesis19l57g1/PaperWire.lean)
- sha256 (`bytes`): `97b1332123a359a360b5faa69da16024009e6f62a8c55eb393624dd04949a1be`
- cited in: node.lean, record TFQ-0459
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.PaperWire`): recorded sha256 `97b1332123a359a360b5faa69da16024009e6f62a8c55eb393624dd04949a1be` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/PaperWire.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `portableBytes_injective` | yes | yes | yes | Quot.sound, propext | `#print axioms portableBytes_injective` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0459_canonical_key_classification.md`

- file: [dag/derivations/02_genesis/tfq_0459_canonical_key_classification.md](../../../dag/derivations/02_genesis/tfq_0459_canonical_key_classification.md)
- sha256 (`lf-normalised`): `1e18965fe0ca720a9f6f0334287e89f1d115e9c14051bf81afda588a62b9c0e8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0459
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/portable_key.py::portable_key_v1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::portable_key_v1`

## Routes

Incoming (1):

- `PGW-R-CANONICAL-KEY-CLASSIFICATION` `DERIVED_LEAN`: [PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS](PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md) (DEFINITION)

Outgoing (0):

