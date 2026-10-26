# PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A regime isomorphism is a pair of bijections on datum and form indices that preserves form arities, ordered instance arguments, uniform-rule membership and the separation requirements read as unordered pairs; mapped requirement endpoints are sorted before comparison, and presentation tokens are erased first. Because requirements are unordered, exchanging the endpoints of a requirement can identify two responses; a relation preserving directed requirements would be a different convention. The Lean structure Iso states these fields over the admitted index ranges, and sortPair is shown to equal (min, max) and to be symmetric.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared isomorphism convention with unordered requirement pairs, genesis_source.txt section 3.8 (assumption)

## Bottleneck

The convention is declared: Iso is a membership relation, so it also identifies list representations such as \[p\] and \[p, p\], and an isomorphism preserving directed requirements would give different tie classes.

## Source status

paper.md section 6 and genesis_source.txt section 3.8 \[definition\]; Minimality.lean Iso

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean)
- sha256 (`bytes`): `eeff121b3e27349e2bd6172b8cfc325f4f8d7d5234b320e92b0c5e7548c92a18`
- cited in: node.lean, node.source, record TFQ-0431
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.IsoCanon`): recorded sha256 `eeff121b3e27349e2bd6172b8cfc325f4f8d7d5234b320e92b0c5e7548c92a18` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sortPair_comm` | yes | yes | yes | propext | `#print axioms sortPair_comm` |
| `sortPair_eq_minmax` | yes | yes | yes | propext | `#print axioms sortPair_eq_minmax` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean, record TFQ-0431
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Iso` | yes | yes | yes | propext | `#print axioms Iso` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md`

- file: [dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md](../../../dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md)
- sha256 (`lf-normalised`): `33dcfc68663860ed53e3fc857084e7a890e6dcaca4926d243c0043056d1de3e9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0431
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
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

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::find_iso`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::find_iso`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/tests/test_mathematics.py::test_unordered_requirement_identifies_unary_endpoint_responses`

## Routes

Incoming (1):

- `PGW-R-REGIME-ISOMORPHISM-UNORDERED-PAIRS` `DERIVED_PROSE`: [PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT](PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md) (DEFINITION), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CANONICAL-KEY-CLASSIFICATION` `DERIVED_LEAN`: [PGW-CANONICAL-KEY-CLASSIFICATION](PGW-CANONICAL-KEY-CLASSIFICATION.md) (PROVED_LEAN)
- `PGW-R-CONTEXTS-PLUGGING-PROFILES` `DERIVED_PROSE`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)
