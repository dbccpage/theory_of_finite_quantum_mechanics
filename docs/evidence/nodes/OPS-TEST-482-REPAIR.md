# OPS-TEST-482-REPAIR

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The instances that the repaired Test 482 of the source repository checks: a GYO reduction accepts the path cover {ab, bc} and rejects the triangle cover {ab, bc, ac}; two rational tables on the path (p_ab with entries 1/2, 1/6, 1/12, 1/4 and p_bc with entries 1/3, 1/4, 1/6, 1/4) agree on the overlap and glue by the product formula p_ab p_bc / p_b to a joint of total mass 1 that reproduces both tables exactly; and the constraints a = b, b = c, a != c of the triangle parity cover have no compatible assignment among the eight. The earlier version of the source test assigned the literal True and asserted it, so it verified nothing. The source test itself is not imported (see the bottleneck).

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The source test was not imported: as one test with fixed inputs and no edge-case handling it would score L3 under SCORING.md, below the L4 floor this change set for code, so it was left out. The row's own caveat stands: other tests of the source file assert literals and are not repaired. The instances are two fixed covers and one pair of tables.

## Source status

Ledger row L035-B14: computed by the repaired test of the source repository (20 tests run there with unittest, exit 0). That test is not run here. The instances are recomputed by checks/independent/foc035_observer_presheaf.py, which restates the tables, the GYO reduction and the exhaustion.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `50f1a22baf6a42c8a7af57fdc1883fea1f4ad3fbf7679b7175fb513351dc11b4`
- cited in: node.source
- counts toward the grade: yes

### Python: `dag/test_foc035_observer_presheaf.py`

- file: [dag/test_foc035_observer_presheaf.py](../../../dag/test_foc035_observer_presheaf.py)
- sha256 (`bytes`): `27a52d7d08c7472387aa311df47c1974523addd994bc46191415e098b618ae1c`
- cited in: node.source
- check: `python -m pytest dag/test_foc035_observer_presheaf.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2516_ops_test_482_repair.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2516_ops_test_482_repair.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2516_ops_test_482_repair.md)
- sha256 (`lf-normalised`): `c8c29c9f9f61b29bfd1e1c47c6c4421cac75726ed54891ccfd6cb33a74de2490`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2516
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

- `OPS-R-TEST-482-REPAIR` `COMPUTED`: [OPS-VOROBEV-THEOREM](OPS-VOROBEV-THEOREM.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

