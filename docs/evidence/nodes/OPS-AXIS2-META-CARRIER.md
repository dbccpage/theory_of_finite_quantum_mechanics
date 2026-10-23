# OPS-AXIS2-META-CARRIER

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Axis 2. Let eval_n be the evaluator of a process on carrier K_n. The statement "eval_n is sound" relates eval_n to a standard of correctness for K_n; that standard is not an element of K_n, so the statement is a sentence of a carrier K_(n+1), and the output PASS of eval_n on it has no standing at K_(n+1) (ENC-0195, AuthorityEffect None). The level statement holds by construction of the carrier hierarchy. Imported: the strengthening by Tarski's undefinability theorem, which applies only when K_n interprets enough arithmetic, and the Genesis identifiers ENC-0118 and ENC-0195, cited by name.

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

- Tarski undefinability, conditional on a carrier that interprets arithmetic (assumption)
- Genesis identifiers ENC-0118 and ENC-0195 (assumption; cited by name, not re-run)

## Bottleneck

Cited by name, not re-run. The level statement is a typing remark and not a theorem; the Tarski clause is conditional on the arithmetic hypothesis.

## Source status

Ledger row L035-C2: by construction + cited. Lemma D, named in the monograph, has no statement in the source repository and nothing here rests on it.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2525_ops_axis2_meta_carrier.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2525_ops_axis2_meta_carrier.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2525_ops_axis2_meta_carrier.md)
- sha256 (`lf-normalised`): `47288efde8aad7dc980f77ef432c4c3e4a8d38e9c28bbb1ed6f95ff2dc08575c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2525
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

- `OPS-R-AXIS2-META-CARRIER` `GAP_NO_DERIVATION`: [GTH-LANG-LIMITS](GTH-LANG-LIMITS.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-REGRESS-COROLLARY` `CONDITIONAL_ON_IMPORT`: [OPS-REGRESS-COROLLARY](OPS-REGRESS-COROLLARY.md) (CONDITIONAL)
