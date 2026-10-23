# OPS-Z2-WITNESS-FALSE-NEGATIVES

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Assumed from Abramsky, Mansfield and Barbosa (EPTCS 95 (2012) 1-14, arXiv:1111.3620), as the note cites it: the Z2 holonomy witness of parity constraints can be silent where the linear-programming witness is not, that is, it has false negatives on other families of scenarios. The note does not compute such a family and does not claim the behaviour away.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Abramsky-Mansfield-Barbosa: the Z2 holonomy witness has false negatives on other families (assumption; cited)

## Bottleneck

Cited, not re-run. No family with a silent Z2 witness is exhibited in this repository.

## Source status

Ledger row L035-B12: cited. The external identifier was checked against the arXiv record. Not computed here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2513_ops_z2_witness_false_negatives.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2513_ops_z2_witness_false_negatives.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2513_ops_z2_witness_false_negatives.md)
- sha256 (`lf-normalised`): `7788af92754a97292d47637dd8121523caa4b3695a7dbb2d547df1fe1ebcb2ec`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2513
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1111.3620`

## Routes

Incoming (1):

- `OPS-R-Z2-WITNESS-FALSE-NEGATIVES` `GAP_NO_DERIVATION`: [OPS-PARITY-CYCLE-DESCENT-NCF](OPS-PARITY-CYCLE-DESCENT-NCF.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

