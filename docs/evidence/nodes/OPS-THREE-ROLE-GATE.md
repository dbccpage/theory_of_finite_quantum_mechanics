# OPS-THREE-ROLE-GATE

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> ThreeRoleGate(scope, admitted_roots) reads a packet (claim_id, scope, proposer, evaluator, authorizer, observer, authority_root, policy); each role binding is (identifier, principal) and the observer is the five-component declaration. Run here (code/python/tests/test_three_role_gate.py, 15 tests, 33 subtests, with a fixture of 17 cases): every fixture case yields its recorded verdict and reasons; every RefusalReason is reached by some fixture case; every verdict carries authority_effect None and GateVerdict refuses any other value; a missing field, an empty identifier, an unknown field or policy, a non-string value, and a missing or blank observer component are typed refusals, never a default; two identifiers on one principal give SHARED_PRINCIPAL, including the case (id-A/p1, id-B/p1, id-A/p2) that a count rule misses; a non-string mapping key at the top level, in a role binding or in the observer is a MALFORMED_PACKET refusal and is never coerced to a string; a self_attested_permitted policy gives SELF_ATTESTED, never ADMITTED_FOR_AUTHORIZATION.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A shape and separation check on one fixture. It does not evaluate the claim, compute a defect or promote anything, and it is not connected to the Rust evaluator: the observer strings in the fixture are copies of the evaluator's constants, compared as text. No node for WDP chapter 15 exists, so the link to the authority packet is a gap route.

## Source status

Ledger rows L035-C8, L035-C9 and L035-C10: computed. The Python tests run in this repository under pytest. The expected verdicts are data in the JSON fixture.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/wdp/three_role_gate.py`

- file: [code/python/src/wdp/three_role_gate.py](../../../code/python/src/wdp/three_role_gate.py)
- sha256 (`bytes`): `8ab1e3557ac46b7ab6dcc17c77191482e53c484076760dc2476e8c4bde0adcf1`
- cited in: node.source, record TFQ-2521
- counts toward the grade: yes

### Python: `code/python/tests/test_three_role_gate.py`

- file: [code/python/tests/test_three_role_gate.py](../../../code/python/tests/test_three_role_gate.py)
- sha256 (`bytes`): `8b5716a7a80bebf130cc09d70df1ea159f8ca4c693c90ca3e4fd85125040dc3d`
- cited in: node.source, record TFQ-2521
- check: `python -m pytest code/python/tests/test_three_role_gate.py`
- counts toward the grade: yes

### Documents and data: `code/python/src/wdp/three_role_provenance_fixtures.json`

- file: [code/python/src/wdp/three_role_provenance_fixtures.json](../../../code/python/src/wdp/three_role_provenance_fixtures.json)
- sha256 (`lf-normalised`): `bea22cced6a7a851f67ecaab5e5adbe6472a9c35e88ccd937fd0be4936793287`
- cited in: node.source, record TFQ-2521
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2521_ops_three_role_gate.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2521_ops_three_role_gate.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2521_ops_three_role_gate.md)
- sha256 (`lf-normalised`): `0e64b8b5070246b537f59395de249d85850e62e5cab209910e55a7af21f1f893`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2521
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

- `OPS-R-THREE-ROLE-GATE` `COMPUTED`: [OPS-OBSERVER-TUPLE](OPS-OBSERVER-TUPLE.md) (DEFINITION)
- `OPS-R-THREE-ROLE-GATE-2` `GAP_NO_DERIVATION`: [TFQ-0329](TFQ-0329.md) (OPEN)

Outgoing (2):

- `OPS-R-REFUTED-EARLIER-GATE` `COMPUTED`: [OPS-REFUTED-EARLIER-GATE](OPS-REFUTED-EARLIER-GATE.md) (REFUTED)
- `OPS-R-SELF-CERTIFICATION-PACKET` `COMPUTED`: [OPS-SELF-CERTIFICATION-PACKET](OPS-SELF-CERTIFICATION-PACKET.md) (COMPUTATIONALLY_CHECKED)
