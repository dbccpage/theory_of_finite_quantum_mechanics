# OPS-REFUTED-AXIS3-WIDE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `REFUTED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The earlier statement of Axis 3, "V(sigma(H)) = V(H) for any verdict V that is a function of internal receipts and conserved charges", is false. Countermodel: states a and b; sigma swaps them; the one transition swaps them, so hypothesis (i) holds; the only conserved charge is the constant 0, so (ii) holds; V(H) is "the first token of H is a". Then V((a)) = true and V(sigma((a))) = V((b)) = false. Recomputed by the independent check.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
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
- sha256 (`bytes`): `50f1a22baf6a42c8a7af57fdc1883fea1f4ad3fbf7679b7175fb513351dc11b4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2528_ops_refuted_axis3_wide.md)
- sha256 (`lf-normalised`): `999db6d56c040255dc448d899625932c46be29ffa14c3fbef6040fd2e299969d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2528
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

- `OPS-R-REFUTED-AXIS3-WIDE` `DERIVED_PROSE`: [OPS-AXIS3-RELABELING](OPS-AXIS3-RELABELING.md) (CONDITIONAL)

Outgoing (0):

