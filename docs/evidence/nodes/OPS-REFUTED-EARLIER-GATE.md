# OPS-REFUTED-EARLIER-GATE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `REFUTED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Two earlier designs of the Python gate failed. (N1) The count rule "the number of principals is below the number of identifiers" missed the case evaluator_also_proposer (identical bindings) and the case (id-A/p1, id-B/p1, id-A/p2), where two identifiers share a principal and a third principal exists; for both, the principals and the identifiers are 2 in number, so the rule does not fire. It was replaced by a pairwise check. (N8) A non-string key in a packet mapping reached the string join in _reject_unknown and escaped evaluate_mapping as a TypeError; it is now a MALFORMED_PACKET refusal at every level. The counts are recomputed by the independent check; the earlier code is not in this repository.

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

Records two superseded designs. The current gate is node OPS-THREE-ROLE-GATE.

## Source status

Ledger rows L035-N1 and L035-N8: refuted (the note's own earlier design and code). The failing run before the fix (2 failures) is recorded in the source repository and is not reproducible here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `50f1a22baf6a42c8a7af57fdc1883fea1f4ad3fbf7679b7175fb513351dc11b4`
- cited in: node.source
- counts toward the grade: yes

### Python: `code/python/tests/test_three_role_gate.py`

- file: [code/python/tests/test_three_role_gate.py](../../../code/python/tests/test_three_role_gate.py)
- sha256 (`bytes`): `8b5716a7a80bebf130cc09d70df1ea159f8ca4c693c90ca3e4fd85125040dc3d`
- cited in: node.source
- check: `python -m pytest code/python/tests/test_three_role_gate.py`
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2530_ops_refuted_earlier_gate.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2530_ops_refuted_earlier_gate.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2530_ops_refuted_earlier_gate.md)
- sha256 (`lf-normalised`): `fb388352ae414a3506881d4f0638e7225e875f0fdae88db201b6dfe6b0fe7aa3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2530
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

- `OPS-R-REFUTED-EARLIER-GATE` `COMPUTED`: [OPS-THREE-ROLE-GATE](OPS-THREE-ROLE-GATE.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

