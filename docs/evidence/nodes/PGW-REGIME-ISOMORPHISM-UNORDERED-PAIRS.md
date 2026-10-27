# PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A regime isomorphism is a pair of bijections on datum and form indices that preserves form arities, ordered instance arguments, uniform-rule membership and the separation requirements read as unordered pairs; mapped requirement endpoints are sorted before comparison, and presentation tokens are erased first. Because requirements are unordered, exchanging the endpoints of a requirement can identify two responses; a relation preserving directed requirements would be a different convention. The Lean structure Iso states these fields over the admitted index ranges, and sortPair is shown to equal (min, max) and to be symmetric.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/IsoCanon.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/IsoCanon.lean](../../../lean4/Imported/GenesisDerivation/Derivation/IsoCanon.lean)
- sha256 (`bytes`): `ef2570898eaff1d2b4bdf68d5d82f81ba249e1559627c16e713fc124d0a9d78e`
- cited in: node.lean, node.source, record TFQ-0431
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.IsoCanon`): recorded sha256 `ef2570898eaff1d2b4bdf68d5d82f81ba249e1559627c16e713fc124d0a9d78e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/IsoCanon.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sortPair_comm` | yes | yes | yes | propext | `#print axioms sortPair_comm` |
| `sortPair_eq_minmax` | yes | yes | yes | propext | `#print axioms sortPair_eq_minmax` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Minimality.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Minimality.lean)
- sha256 (`bytes`): `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c`
- cited in: node.lean, record TFQ-0431
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Minimality`): recorded sha256 `96894c39bed9b2e9661deabbbb9a2f75d85603e0ccdf3e9d505be2a0175e362c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Iso` | yes | yes | yes | propext | `#print axioms Iso` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)
- sha256 (`bytes`): `bd91e864bb54ade9ed3890a65d89f57500cef2fb66e060eb5e18359d6c6187ea`
- cited in: node.rust, record TFQ-0431

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `find_iso` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py)
- sha256 (`bytes`): `b0f1f3bcf05126111a07706f4388a9fff5e30455d4b8f127966cf99ab0d0886e`
- cited in: record TFQ-0431

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `find_iso` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py)
- sha256 (`bytes`): `a2b7a7b6452e649b40a4c36803dd498e3444499643455c35a5c625a72f3062cf`
- cited in: record TFQ-0431
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py::test_unordered_requirement_identifies_unary_endpoint_responses`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_unordered_requirement_identifies_unary_endpoint_responses` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py::test_unordered_requirement_identifies_unary_endpoint_responses` |

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

### Documents and data: `dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md`

- file: [dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md](../../../dag/derivations/02_genesis/tfq_0431_regime_isomorphism_unordered_pairs.md)
- sha256 (`lf-normalised`): `72387517d1fd957ab34ddc24122602a7931b1402215afd501036004c201386d1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0431
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-REGIME-ISOMORPHISM-UNORDERED-PAIRS` `DERIVED_PROSE`: [PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT](PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md) (DEFINITION), [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CANONICAL-KEY-CLASSIFICATION` `DERIVED_LEAN`: [PGW-CANONICAL-KEY-CLASSIFICATION](PGW-CANONICAL-KEY-CLASSIFICATION.md) (PROVED_LEAN)
- `PGW-R-CONTEXTS-PLUGGING-PROFILES` `DERIVED_PROSE`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)
