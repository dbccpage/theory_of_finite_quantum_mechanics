# OPS-UNDERDETERMINATION

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Lemma A2. Let O' leave one of K, Adm, norm, Term undeclared, and require that an evaluation's receipt for a claim agree across every admissible completion of the undeclared component. Then no evaluation of O' meets that requirement: for each of the four components there are two admissible completions, agreeing elsewhere, whose receipts for one claim differ. Witnesses on the PR box (Bell scenario, parity targets 0, 0, 0, 1): K, the Bell cover gives defect 2 and the acyclic sub-cover {ab, ab'} gives defect 0; Adm, the noncontextual polytope gives 2 and the no-signalling polytope gives 0, because the PR box is no-signalling; norm, the l1 norm gives 2 and twice the l1 norm gives 4; Term, with defect 2 and empty global support the rule of the note gives OpenObstruction and the rule "defect below 3 gives ExactRepair" gives ExactRepair. The lemma does not say that no function from claims to receipts exists; any one completion defines a function. The layer has no row, because Definition A1 fixes it to diagnostic.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The norm and Term rows are arithmetic on the defect 2, not receipts of a configurable evaluator: the Rust evaluator implements one norm and one terminal rule. The second receipt of the Adm row is proved, not computed by the Rust code. Not formalised in Lean.

## Source status

Ledger row L035-A2: computed (K row; first receipt of the Adm row) + proved (second receipt of the Adm row) + derived by hand (norm and Term rows). The Rust receipts are not run here; the defects 2 and 0 are recomputed by the independent check.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `50f1a22baf6a42c8a7af57fdc1883fea1f4ad3fbf7679b7175fb513351dc11b4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2517_ops_underdetermination.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2517_ops_underdetermination.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2517_ops_underdetermination.md)
- sha256 (`lf-normalised`): `4c6297d8f93ecf375aab5c2153ade5c5d7f1f52e429703b6325912e24f61ffd4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2517
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

- `OPS-R-UNDERDETERMINATION` `DERIVED_PROSE`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION), [OPS-STRONG-CONTEXTUALITY-NCF-ZERO](OPS-STRONG-CONTEXTUALITY-NCF-ZERO.md) (PROVED_PROSE)

Outgoing (0):

