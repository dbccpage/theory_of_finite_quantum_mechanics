# OPS-VOROBEV-THEOREM

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Assumed from Vorob'ev (Theory of Probability and its Applications 7 (1962) 147-163, doi:10.1137/1107014), as the note states it: if the hypergraph (M, C) is GYO-acyclic (it reduces to nothing by removing ears and absorbed vertices, equivalently it has a join tree), then every no-signalling model has a global section given on a join tree T by d(g) = (product over C of e_C(g|C)) / (product over the edges (C, C') of T of e_(C intersect C')(g|C intersect C')), with 0/0 = 0. The note gives an induction sketch, not a full proof. The converse (for every non-acyclic hypergraph some no-signalling family has no global section) is not implemented; the PR box on the 4-cycle is one instance.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Vorob'ev: a GYO-acyclic cover glues every no-signalling model by the join-tree product formula (assumption; cited)

## Bottleneck

Cited theorem with a proof sketch in the note only. Not formalised in Lean.

## Source status

Ledger row L035-B13: proved (sketch) + computed, with the theorem cited. The DOI was checked against the Crossref record (title, volume, pages, year). The computed instances are in nodes OPS-VOROBEV-PATH-INSTANCE and OPS-TEST-482-REPAIR.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2514_ops_vorobev_theorem.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2514_ops_vorobev_theorem.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2514_ops_vorobev_theorem.md)
- sha256 (`lf-normalised`): `6abe94d7e2bafe79f5b36482047981474f10b46433c9673e0ed3a97566d14aa0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2514
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

- `external:doi:10.1137/1107014`

## Routes

Incoming (1):

- `OPS-R-VOROBEV-THEOREM` `GAP_NO_DERIVATION`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (2):

- `OPS-R-TEST-482-REPAIR` `COMPUTED`: [OPS-TEST-482-REPAIR](OPS-TEST-482-REPAIR.md) (COMPUTATIONALLY_CHECKED)
- `OPS-R-VOROBEV-PATH-INSTANCE` `COMPUTED`: [OPS-VOROBEV-PATH-INSTANCE](OPS-VOROBEV-PATH-INSTANCE.md) (COMPUTATIONALLY_CHECKED)
