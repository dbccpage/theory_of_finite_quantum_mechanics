# OPS-LEAN-GAP

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Not formalised in Lean: the equivalences between global sections, conv(A) and the noncontextual fraction, and between strong contextuality and NCF 0 (nodes OPS-NCF-LHV-EQUIVALENCE and OPS-STRONG-CONTEXTUALITY-NCF-ZERO); Vorob'ev sufficiency and its converse (node OPS-VOROBEV-THEOREM); delta0 e = 0 if and only if e is no-signalling; rational normalisation of weights; and any link from the Lean model of natural-number-weighted lists to the Rust Scenario type or to the Rust and Python gates.

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

Missing: a Lean proof of any item listed in the statement. The Lean file lean4/LggrFiniteResults.lean covers only the statements of nodes OPS-PUSHFORWARD-FUNCTOR-LEAN and OPS-PARITY-HOLONOMY-LEAN among these rows.

## Source status

Ledger row L035-L1, status open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md)
- sha256 (`lf-normalised`): `3b4fcf95cec2f1601d5d2427d57b2028d251703685b29b8750ac04a13aac76d6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2520
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

- `OPS-R-LEAN-GAP` `GAP_NO_DERIVATION`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)
- `OPS-R-LEAN-GAP-2` `GAP_NO_DERIVATION`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (0):

