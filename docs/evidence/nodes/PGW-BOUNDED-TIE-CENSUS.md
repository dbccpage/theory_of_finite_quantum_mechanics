# PGW-BOUNDED-TIE-CENSUS

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Within the declared bounds of at most two items and form arity at most two, exhaustive enumeration under mu1, cross-checked against the unpruned space, finds at (2,2) six valid deltas in three isomorphism classes for reading L (unary mark, binary link, binary self-loop) and ten valid deltas in five classes for reading F. Reading F's two extra classes link to and from the never-required genesis datum, and they are non-isomorphic to each other because the bijection must preserve the requirement pair. Under mu2 each reading has two minimal deltas in one class. The standalone replay reproduces all four counts.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared resource bounds max_items 2 and max_arity 2 and the implemented isomorphism relation (assumption)

## Bottleneck

A bounded census: it is the max_arity = 2 slice of the infinite mu1 tie family of reading L (TFQ-0441), and no reading-F Lean non-uniqueness statement exists.

## Source status

genesis_source.txt section 7.3 \[bounded theorem\] engine enumeration at (2,2); reproduce.py minimum census

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)
- sha256 (`bytes`): `1ce7119c17f0bac2b7f0a81487da586024d0d4e38a5004197e9765ebe96def98`
- cited in: node.rust, record TFQ-0442

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sealed_challenge3_reading_f` (rust_test) | yes | yes | yes | - | - |
| `sealed_challenge3_reading_l` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- sha256 (`bytes`): `856ce42faba2dc2ae1217207ecc8af893eac29b50ae8a374dc06d2ba22c957bb`
- cited in: record TFQ-0442

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `min_responses` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/reproduce.py)
- sha256 (`bytes`): `60d4be592f4528fa5f40f3fa03179c84225daf914c79660f62cbd016fb649c71`
- cited in: record TFQ-0442

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `python_replay` (python_symbol) | yes | yes | yes | - | - |

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

### Documents and data: `dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md`

- file: [dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md](../../../dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md)
- sha256 (`lf-normalised`): `27d7dd0b3fd87282e3b4899308621b75e79d2710205c38c75b27d090eb66a943`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0442
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/genesis.md`

- file: `omega_engine_education/documentation/001_oegen/genesis.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0442 lean4: no Lean census of the bounded tie classes; reading-F non-uniqueness has no Lean statement

## Routes

Incoming (1):

- `PGW-R-BOUNDED-TIE-CENSUS` `COMPUTED`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)

Outgoing (0):

