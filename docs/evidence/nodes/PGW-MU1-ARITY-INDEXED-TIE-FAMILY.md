# PGW-MU1-ARITY-INDEXED-TIE-FAMILY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every arity k ≥ 1 the k-ary mark, one k-ary form and one instance (1, ..., 1), is a valid two-item response to Challenge 3 on R2L (deltaK_valid, deltaK_length), since the all-hole context separates the two required data. Distinct arities give non-isomorphic results because an isomorphism preserves form arity (markK_pairwise_noniso), so the mu1 tie class in reading L is countably infinite. A concrete enumeration is therefore complete only relative to an arity bound, and the arity-at-most-two census is one slice of this family.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared item grammar, measure mu1 and the implemented isomorphism relation (assumption)

## Bottleneck

Stated over R2L only: no reading-F analogue of the k-ary family is formalized, and the family leaves the mu2 minimum (2, 1) unique up to isomorphism.

## Source status

genesis_source.txt section 7.3 \[theorem, reading L\] (CL-3-INFINITE-TIES); Minimality.lean markK family

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- sha256 (`bytes`): `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925`
- cited in: node.lean, node.source, record TFQ-0441
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Minimality`): recorded sha256 `7aa1197717f6c6e839c33f603ed4e30a7185fdfeb6b6c81cefef8c7eb220d925` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `deltaK_length` | yes | yes | yes | none | `#print axioms deltaK_length` |
| `deltaK_valid` | yes | yes | yes | Quot.sound, propext | `#print axioms deltaK_valid` |
| `markK_pairwise_noniso` | yes | yes | yes | propext | `#print axioms markK_pairwise_noniso` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md`

- file: [dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md](../../../dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md)
- sha256 (`lf-normalised`): `b4ab36521981d022c58f8f9ae20e0ef2ed8a2e252257e1cb516ced9f18cd1861`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0441
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

## Absences recorded by the TFQ records

- TFQ-0441 python: no Python check of the unbounded arity family; the Python census enumerates form arity at most two
- TFQ-0441 rust: no Rust check of the unbounded arity family; the Rust census enumerates form arity at most two

## Routes

Incoming (1):

- `PGW-R-MU1-ARITY-INDEXED-TIE-FAMILY` `DERIVED_LEAN`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)

Outgoing (0):

