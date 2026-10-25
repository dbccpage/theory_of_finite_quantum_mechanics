# OPS-ARC-COVER-NGE-WITNESS

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Existence witness. On the Bell scenario let e = (1/2)(delta_g1 + delta_g2) with g1 = (a, a', b, b') = (0,0,0,0) and g2 = (1,0,0,1). Then NCF(e) = 1 and G(e) has 2 elements. Over the arc cover {a, a', b}, {a', b, b'}, which omits the context {a, b'}, there are 4 matching families; 2 of them have exactly one gluing in S(M) and 2 have none. So a noncontextual model can have matching families without a global extension on a cover that omits a context.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An existence claim with one witness. The Rust classifier outcome names (Unique, NoGlobalExtension) are read as: exactly one gluing, no gluing. Not run here for the Rust code.

## Source status

Ledger row L035-B7: computed by the Rust test a_noncontextual_model_can_still_fail_descent_on_an_arc_cover, not run here. The counts are recomputed by checks/independent/foc035_observer_presheaf.py by enumerating the families and the gluings.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/descent.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/descent.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/descent.rs)
- sha256 (`bytes`): `f69c766a07bf1c4624808653855fc2fe99e962e17a35a9307bf57f7994f3f9f6`
- cited in: node.rust, record TFQ-2507

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `summarize_descent` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Python: `dag/test_foc035_observer_presheaf.py`

- file: [dag/test_foc035_observer_presheaf.py](../../../dag/test_foc035_observer_presheaf.py)
- sha256 (`bytes`): `17b962ed09fd6127e11d44e3bbc0524f076a9bd85a316992a4e2612ae66a15ee`
- cited in: node.source
- check: `python -m pytest dag/test_foc035_observer_presheaf.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2507_ops_arc_cover_nge_witness.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2507_ops_arc_cover_nge_witness.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2507_ops_arc_cover_nge_witness.md)
- sha256 (`lf-normalised`): `08038dce706b7b2599f19db34719f73af62d9bf1642d50571af1bc7c58cc3c08`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2507
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-ARC-COVER-NGE-WITNESS` `COMPUTED`: [OPS-MAXIMAL-COVER-DESCENT](OPS-MAXIMAL-COVER-DESCENT.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-NGE-NOT-CONTEXTUALITY` `DERIVED_PROSE`: [OPS-NGE-NOT-CONTEXTUALITY](OPS-NGE-NOT-CONTEXTUALITY.md) (PROVED_PROSE)
