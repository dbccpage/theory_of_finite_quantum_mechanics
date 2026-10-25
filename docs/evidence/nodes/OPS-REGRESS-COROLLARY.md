# OPS-REGRESS-COROLLARY

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH14-C01 (an unhosted token predictor cannot issue self-authorizing certificates) follows from Axes 2 and 3 for a process whose only outputs are receipt-free presentations and whose self-evaluation, if any, factors through its internal exports (premise (iii) of Axis 3). The nonclaim WDP-CH14-N03 is kept: a process coupled to a receipt-emitting oracle, as in WDP-CH15-D02, is outside the statement.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Conditional on nodes OPS-AXIS2-META-CARRIER (cited, not re-run) and OPS-AXIS3-RELABELING. Not formalised in Lean.

## Source status

Ledger row L035-C5: proved (conditional on (iii)), narrowed together with row C3.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2527_ops_regress_corollary.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2527_ops_regress_corollary.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2527_ops_regress_corollary.md)
- sha256 (`lf-normalised`): `a6e6b18d8fb9d50e84cecc91aa1a63c81deb1c07a69edc9d61812eb0569ca3cf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2527
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

- `OPS-R-REGRESS-COROLLARY` `CONDITIONAL_ON_IMPORT`: [OPS-AXIS2-META-CARRIER](OPS-AXIS2-META-CARRIER.md) (IMPORTED_ASSUMPTION), [OPS-AXIS3-RELABELING](OPS-AXIS3-RELABELING.md) (CONDITIONAL)

Outgoing (0):

