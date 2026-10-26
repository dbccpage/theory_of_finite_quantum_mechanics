# OPS-MAXIMAL-COVER-DESCENT

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Proposition B4(1). Let S(U) be the set of assignments s on U whose restriction to every maximal context C inside U lies in the support of e_C; then S(M) = G(e). Over the cover of M by its maximal contexts, every matching family (s_C in S(C), agreeing on overlaps) glues to exactly one element of S(M). So a descent classifier on that cover reports no NoGlobalExtension, its fibers are in bijection with G(e), and strong contextuality appears as zero matching families, not as a failed gluing. Instances recomputed exactly: the PR box has 0 matching families; the noisy PR box at lam = 1/2 has 16, each with exactly one gluing.

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

The reading of the proposition as a statement about the Rust classifier is not checked here (not run here). Not formalised in Lean.

## Source status

Ledger row L035-B6: proved + computed. The statement here is about the set-level family S. The Rust classify_cover reading (the DescentOutcome variants read from finite_report_descent.rs) is not run here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2506_ops_maximal_cover_descent.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2506_ops_maximal_cover_descent.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2506_ops_maximal_cover_descent.md)
- sha256 (`lf-normalised`): `aed67ff30685eb3b5a5c387621696a89018513b56e7df3773b4e6ec6532431eb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2506
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

- `OPS-R-MAXIMAL-COVER-DESCENT` `DERIVED_PROSE`: [OPS-STRONG-CONTEXTUALITY-NCF-ZERO](OPS-STRONG-CONTEXTUALITY-NCF-ZERO.md) (PROVED_PROSE)

Outgoing (3):

- `OPS-R-ARC-COVER-NGE-WITNESS` `COMPUTED`: [OPS-ARC-COVER-NGE-WITNESS](OPS-ARC-COVER-NGE-WITNESS.md) (COMPUTATIONALLY_CHECKED)
- `OPS-R-NGE-NOT-CONTEXTUALITY` `DERIVED_PROSE`: [OPS-NGE-NOT-CONTEXTUALITY](OPS-NGE-NOT-CONTEXTUALITY.md) (PROVED_PROSE)
- `OPS-R-PARITY-CYCLE-DESCENT-NCF` `COMPUTED`: [OPS-PARITY-CYCLE-DESCENT-NCF](OPS-PARITY-CYCLE-DESCENT-NCF.md) (COMPUTATIONALLY_CHECKED)
