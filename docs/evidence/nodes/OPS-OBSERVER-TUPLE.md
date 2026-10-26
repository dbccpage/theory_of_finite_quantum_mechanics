# OPS-OBSERVER-TUPLE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Definition A1 of the source note. Fix a finite set M of measurements with finite outcome sets and a cover C of M by maximal contexts, and write E(U) for the set of outcome assignments on U. An observer tuple is O = (K, Adm, norm, Term, L). K = (M, C, E). Adm is the convex hull conv(A) of the vectors (delta_g restricted to C) over all contexts C, for g in E(M). The norm is the l1 norm on the stacked context distributions. Term maps the defect and the claim to a status: defect 0 gives ExactRepair, defect above 0 with a support-level global section gives ClosedResidual, and otherwise OpenObstruction. L is the diagnostic layer. The defect of a claim e = (e_C), one distribution per context, is Delta_O(e) = min over p in Adm of the l1 norm of (e - p). The five components are a projection of the four packets of WDP chapter 10 (presentation, memory, evaluator, policy) and of the chapter 15 grade. The monograph defines no five-tuple of its own; the ledger row records a search for "5-tuple" that returned nothing.

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

A reading of WDP-CH10-D01 to D04, not a derivation. WDP chapter 15 has no node in this graph, so the layer component has no repository node to attach to. No source relates the L1 observer axioms H1 to H5 to this five-component tuple.

## Source status

Ledger row L035-A1, status cited: the row cites the repository's own chapter-10 definitions. This node records the tuple as a definition, which is what Definition A1 of the note is.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2500_ops_observer_tuple.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2500_ops_observer_tuple.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2500_ops_observer_tuple.md)
- sha256 (`lf-normalised`): `ec283667977ff0d640524e06734b11e6f708389726d3187d99ce7389686cdd32`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2500
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

Incoming (2):

- `OPS-R-OBSERVER-TUPLE` `RECORD_PARENT`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)
- `OPS-R-OBSERVER-TUPLE-2` `GAP_NO_DERIVATION`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (4):

- `OPS-R-NCF-LHV-EQUIVALENCE` `DERIVED_PROSE`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)
- `OPS-R-OBSERVER-DECLARATION-REFUSAL` `RECORD_PARENT`: [OPS-OBSERVER-DECLARATION-REFUSAL](OPS-OBSERVER-DECLARATION-REFUSAL.md) (CONDITIONAL)
- `OPS-R-THREE-ROLE-GATE` `COMPUTED`: [OPS-THREE-ROLE-GATE](OPS-THREE-ROLE-GATE.md) (COMPUTATIONALLY_CHECKED)
- `OPS-R-UNDERDETERMINATION` `DERIVED_PROSE`: [OPS-UNDERDETERMINATION](OPS-UNDERDETERMINATION.md) (PROVED_PROSE)
