# OPS-REFUTED-AXIS3-WIDE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `REFUTED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The earlier statement of Axis 3, "V(sigma(H)) = V(H) for any verdict V that is a function of internal receipts and conserved charges", is false. Countermodel: states a and b; sigma swaps them; the one transition swaps them, so hypothesis (i) holds; the only conserved charge is the constant 0, so (ii) holds; V(H) is "the first token of H is a". Then V((a)) = true and V(sigma((a))) = V((b)) = false. Recomputed by the independent check.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Refutes the unconditional form only; the form with the declared-export premise (iii) is node OPS-AXIS3-RELABELING.

## Source status

Ledger row L035-N3: refuted (the note's own earlier statement), found in the review of PR 1080 of the source repository. The countermodel is recomputed here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md)
- sha256 (`lf-normalised`): `4da2d48d94bd95cafbb6363295801f04d95404e34820b99816ea5dd0fbe1151a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2528
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-REFUTED-AXIS3-WIDE` `DERIVED_PROSE`: [OPS-AXIS3-RELABELING](OPS-AXIS3-RELABELING.md) (CONDITIONAL)

Outgoing (0):

