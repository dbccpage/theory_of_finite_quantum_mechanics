# OPS-SELF-CERTIFICATION-PACKET

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Read as a provenance packet, the sentence "I verified this and certify it" is (p, p, p): one identifier and one principal in the proposer, evaluator and authorizer roles. All three pairs of roles coincide. The gate returns REJECTED with the reasons SELF_AUTHORIZATION, EVALUATOR_IS_PROPOSER and EVALUATOR_IS_AUTHORIZER, in that order (fixture case i_verified_this_and_certify_it; test test_self_certification_sentence_is_rejected_on_three_counts). The note's reading of this as a single-patch gluing on the role cover with no descent data is prose, and is not computed.

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

The role policy is the authority note's PairwiseDistinct, principals included, which is declared by the regime and not derived from the evidence. A regime that permits self-attestation gives SELF_ATTESTED for the same packet.

## Source status

Ledger row L035-C6: proved + computed. The gate test runs here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/wdp/three_role_gate.py`

- file: [code/python/src/wdp/three_role_gate.py](../../../code/python/src/wdp/three_role_gate.py)
- sha256 (`bytes`): `8ab1e3557ac46b7ab6dcc17c77191482e53c484076760dc2476e8c4bde0adcf1`
- cited in: node.source, record TFQ-2522
- counts toward the grade: yes

### Python: `code/python/tests/test_three_role_gate.py`

- file: [code/python/tests/test_three_role_gate.py](../../../code/python/tests/test_three_role_gate.py)
- sha256 (`bytes`): `8b5716a7a80bebf130cc09d70df1ea159f8ca4c693c90ca3e4fd85125040dc3d`
- cited in: node.source, record TFQ-2522
- check: `python -m pytest code/python/tests/test_three_role_gate.py`
- counts toward the grade: yes

### Documents and data: `code/python/src/wdp/three_role_provenance_fixtures.json`

- file: [code/python/src/wdp/three_role_provenance_fixtures.json](../../../code/python/src/wdp/three_role_provenance_fixtures.json)
- sha256 (`lf-normalised`): `bea22cced6a7a851f67ecaab5e5adbe6472a9c35e88ccd937fd0be4936793287`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2522_ops_self_certification_packet.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2522_ops_self_certification_packet.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2522_ops_self_certification_packet.md)
- sha256 (`lf-normalised`): `1efb3a3e42173a57b8907271718feafaef0248541c13dc079a4d4d7e6e52845f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2522
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

- `OPS-R-SELF-CERTIFICATION-PACKET` `COMPUTED`: [OPS-THREE-ROLE-GATE](OPS-THREE-ROLE-GATE.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `OPS-R-AP-CARD-PROPOSAL` `RECORD_PARENT`: [OPS-AP-CARD-PROPOSAL](OPS-AP-CARD-PROPOSAL.md) (SOURCE_RECORD)
