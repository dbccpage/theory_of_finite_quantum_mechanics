# OPS-NO-SIGNALLING-SIGNED-SECTION

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Assumed from Abramsky and Brandenburger (New Journal of Physics 13 (2011) 113036, arXiv:1102.0264), as the note cites it and does not prove it: an empirical model is no-signalling if and only if it has a signed global section, a function d on E(M) with values in Q, sum 1 and the given marginals. Instance recomputed exactly: the PR box, which is no-signalling, has a signed global section found by exact linear algebra, with sum 1, all 16 marginal equations satisfied and at least one negative entry.

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

- Abramsky-Brandenburger: no-signalling iff a signed global section exists (assumption; cited, not proved here)

## Bottleneck

The equivalence is cited, not derived here. The instance covers one no-signalling model and says nothing about the converse direction or about other models.

## Source status

Ledger row L035-B3: cited + computed. The external identifier was checked against the arXiv record (title and journal reference). The instance is recomputed by an exact script; the equivalence itself is not re-proved.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2512_ops_no_signalling_signed_section.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2512_ops_no_signalling_signed_section.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2512_ops_no_signalling_signed_section.md)
- sha256 (`lf-normalised`): `6a45e1054ca26dad0ad62da27914e123dfe9aff93879c4b877114e80e037b995`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2512
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

- `external:arXiv:1102.0264`

## Routes

Incoming (1):

- `OPS-R-NO-SIGNALLING-SIGNED-SECTION` `GAP_NO_DERIVATION`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (0):

