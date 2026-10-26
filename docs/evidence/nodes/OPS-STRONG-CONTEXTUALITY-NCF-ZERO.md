# OPS-STRONG-CONTEXTUALITY-NCF-ZERO

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Proposition B3(3). Write G(e) for the set of g in E(M) with e_C(g restricted to C) \> 0 for every context C. Then e is strongly contextual (G(e) is empty) if and only if NCF(e) = 0: if lambda_g \> 0 is feasible then e_C(g|C) \>= lambda_g \> 0 for every C, so g is in G(e); conversely g in G(e) makes lambda = (min over C of e_C(g|C)) delta_g feasible with positive weight. Instance recomputed exactly: the PR box on the Bell scenario (contexts ab, ab', a'b, a'b', each uniform on the two outcome pairs with parity 0, 0, 0, 1) has |G| = 0 and NCF 0. The four parity constraints x_a + x_b = 0, x_a + x_b' = 0, x_a' + x_b = 0 and x_a' + x_b' = 1 sum to 0 = 1 modulo 2, so none of the 16 assignments satisfies all.

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

Not formalised in Lean (ledger row L035-L1, node OPS-LEAN-GAP).

## Source status

Ledger row L035-B4: proved + computed. The instance values are recomputed here by an exact script.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2504_ops_strong_contextuality_ncf_zero.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2504_ops_strong_contextuality_ncf_zero.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2504_ops_strong_contextuality_ncf_zero.md)
- sha256 (`lf-normalised`): `fc99842addce846400fc7d90c690524235a01e08224329407be41d0f12f0c36c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2504
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

- `OPS-R-STRONG-CONTEXTUALITY-NCF-ZERO` `DERIVED_PROSE`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (3):

- `OPS-R-MAXIMAL-COVER-DESCENT` `DERIVED_PROSE`: [OPS-MAXIMAL-COVER-DESCENT](OPS-MAXIMAL-COVER-DESCENT.md) (PROVED_PROSE)
- `OPS-R-UNDERDETERMINATION` `DERIVED_PROSE`: [OPS-UNDERDETERMINATION](OPS-UNDERDETERMINATION.md) (PROVED_PROSE)
- `OPS-R-ZERO-COCYCLE-BLIND` `DERIVED_PROSE`: [OPS-ZERO-COCYCLE-BLIND](OPS-ZERO-COCYCLE-BLIND.md) (PROVED_PROSE)
