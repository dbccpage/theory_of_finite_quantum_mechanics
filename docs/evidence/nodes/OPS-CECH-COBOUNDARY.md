# OPS-CECH-COBOUNDARY

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Proposition B5. Let N be the nerve of the maximal-context cover and take cochains valued in the presheaf U -\> Q^E(U), with (delta0 alpha)_(C,C') the restriction of alpha_C to the overlap minus the restriction of alpha_C', and delta1 the alternating sum of restrictions on triples. Then delta1 delta0 = 0; for an empirical model e read as a 0-cochain, delta0 e = 0 if and only if e is no-signalling; and Phi_1(\[omega\]) = min over alpha of the l1 norm of (omega - delta0 alpha) is unchanged by omega -\> omega - delta0 beta. Instances recomputed exactly: the Bell nerve has four edges (a 4-cycle) and no triple, so delta1 delta0 = 0 is vacuous there; on the cover {0,1}, {0,2}, {0,3} (one nerve triple, overlap {0}) delta1 delta0 alpha = 0 for a non-constant alpha while a 1-cochain supported on one pair has delta1 beta = \[1, 0\]; delta0 e = 0 for the PR box and is nonzero at the pair (0,1) for a model whose a-marginal differs between the contexts ab and ab'; the unit cochain (1, 1) on the first edge of the Bell nerve has Phi_1 = 2, by the value 2 at alpha = 0 and a dual witness of sup norm 1 that annihilates delta0, and Phi_1 is again 2 after adding delta0 of a coboundary.

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

Phi_1 is the quotient value of the WDP degree-1 window; no source in this graph identifies the Cech-cochain Phi_1 with PG-WDP-DEGREE1-WINDOW with J the l1 norm, so that route is a gap. Not formalised in Lean.

## Source status

Ledger row L035-B9: proved + computed. The instance values are recomputed here by an exact script. The Rust tests, including the shape checks of the ledger row, are not run here (node OPS-RUST-RECEIPTS-AND-LIMITS).

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `3d90a2037dad209ecb4d24638a9c362056cc9b5c6c402859e653b22bdc9f6d9d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2509_ops_cech_coboundary.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2509_ops_cech_coboundary.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2509_ops_cech_coboundary.md)
- sha256 (`lf-normalised`): `184ad6613b5b504cbcfe3cbae4bda3e681735d234afda32c712cfed03f02ed2d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2509
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

- `OPS-R-CECH-COBOUNDARY` `DERIVED_PROSE`: [OPS-PUSHFORWARD-FUNCTOR-LEAN](OPS-PUSHFORWARD-FUNCTOR-LEAN.md) (PROVED_LEAN)
- `OPS-R-CECH-COBOUNDARY-2` `GAP_NO_DERIVATION`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (2):

- `OPS-R-RUST-RECEIPTS-AND-LIMITS` `RECORD_PARENT`: [OPS-RUST-RECEIPTS-AND-LIMITS](OPS-RUST-RECEIPTS-AND-LIMITS.md) (CONDITIONAL)
- `OPS-R-ZERO-COCYCLE-BLIND` `DERIVED_PROSE`: [OPS-ZERO-COCYCLE-BLIND](OPS-ZERO-COCYCLE-BLIND.md) (PROVED_PROSE)
