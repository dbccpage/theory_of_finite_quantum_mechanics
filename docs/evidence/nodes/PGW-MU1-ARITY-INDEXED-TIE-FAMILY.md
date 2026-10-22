# PGW-MU1-ARITY-INDEXED-TIE-FAMILY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every arity k ≥ 1 the k-ary mark, one k-ary form and one instance (1, ..., 1), is a valid two-item response to Challenge 3 on R2L (deltaK_valid, deltaK_length), since the all-hole context separates the two required data. Distinct arities give non-isomorphic results because an isomorphism preserves form arity (markK_pairwise_noniso), so the mu1 tie class in reading L is countably infinite. A concrete enumeration is therefore complete only relative to an arity bound, and the arity-at-most-two census is one slice of this family.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

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

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md`

- file: [dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md](../../../dag/derivations/02_genesis/tfq_0441_mu1_arity_indexed_tie_family.md)
- sha256 (`lf-normalised`): `f9c3278597bbbac34a749462ab86b6ebfaf75b81adc6c2f175f647e6eb10612f`
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::deltaK_length`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::deltaK_valid`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Minimality.lean::markK_pairwise_noniso`

## Absences recorded by the TFQ records

- TFQ-0441 python: no Python check of the unbounded arity family; the Python census enumerates form arity at most two
- TFQ-0441 rust: no Rust check of the unbounded arity family; the Rust census enumerates form arity at most two

## Routes

Incoming (1):

- `PGW-R-MU1-ARITY-INDEXED-TIE-FAMILY` `DERIVED_LEAN`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)

Outgoing (0):

