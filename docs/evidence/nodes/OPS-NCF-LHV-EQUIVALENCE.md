# OPS-NCF-LHV-EQUIVALENCE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Proposition B3(1). For an empirical model e = (e_C) on a finite scenario, let A be the matrix whose column g, for g in E(M), is the stacked vector of the point masses of g restricted to each context, and let NCF(e) = max of the sum of lambda_g over lambda \>= 0 with A lambda \<= e. Then these are equivalent: e has a global section (a probability vector d on E(M) with marginal e_C on every context C); e lies in conv(A); NCF(e) = 1. This is the local-hidden-variable condition. Instances recomputed exactly: the mixture (1/2)(delta_g1 + delta_g2), with g1 = (0,0,0,0) and g2 = (1,0,0,1) on (a, a', b, b'), has NCF 1; the noisy PR box (1 - lam) PR + lam U at lam = 1/2 has NCF 1 and a distribution as a global section.

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

Not formalised in Lean (ledger row L035-L1, node OPS-LEAN-GAP). The proof is in the note and is not machine-checked.

## Source status

Ledger row L035-B2: proved + computed. The note gives a direct proof of the clause; the equivalence with the local-hidden-variable condition is the statement of Abramsky and Brandenburger, whose publisher record was not checked by the note. The instance values are recomputed here by an exact script, not by the Rust tests.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2503_ops_ncf_lhv_equivalence.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2503_ops_ncf_lhv_equivalence.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2503_ops_ncf_lhv_equivalence.md)
- sha256 (`lf-normalised`): `a089c41e413ea326fb66efc61071ae8a403ddad529ac5b53db0059ff146a6c50`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2503
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1102.0264`
- `external:arXiv:1705.07918`

## Routes

Incoming (1):

- `OPS-R-NCF-LHV-EQUIVALENCE` `DERIVED_PROSE`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)

Outgoing (5):

- `OPS-R-LEAN-GAP-2` `GAP_NO_DERIVATION`: [OPS-LEAN-GAP](OPS-LEAN-GAP.md) (OPEN)
- `OPS-R-NO-SIGNALLING-SIGNED-SECTION` `GAP_NO_DERIVATION`: [OPS-NO-SIGNALLING-SIGNED-SECTION](OPS-NO-SIGNALLING-SIGNED-SECTION.md) (IMPORTED_ASSUMPTION)
- `OPS-R-NOISY-PR-NCF` `COMPUTED`: [OPS-NOISY-PR-NCF](OPS-NOISY-PR-NCF.md) (COMPUTATIONALLY_CHECKED)
- `OPS-R-STRONG-CONTEXTUALITY-NCF-ZERO` `DERIVED_PROSE`: [OPS-STRONG-CONTEXTUALITY-NCF-ZERO](OPS-STRONG-CONTEXTUALITY-NCF-ZERO.md) (PROVED_PROSE)
- `OPS-R-VOROBEV-THEOREM` `GAP_NO_DERIVATION`: [OPS-VOROBEV-THEOREM](OPS-VOROBEV-THEOREM.md) (IMPORTED_ASSUMPTION)
