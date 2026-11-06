# QI-CLASSICAL-CHANNEL-LIFT

Stage: [FINITE_QM_INFORMATION](../stages/FINITE_QM_INFORMATION.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the admitted complex matrix model every column-stochastic kernel K has a CPTP map with Kraus operators sqrt(K(j|i)) times |j\>\<i|, sending diagonal probabilities p to diagonal probabilities Kp.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex square roots of nonnegative entries
- standard basis
- K(j|i) nonnegative with each column summing to one

## Bottleneck

Summing A_ji adjoint times A_ji gives the identity by column normalization. The operator-sum formula is completely positive and its output on a diagonal state is diag(Kp). It erases off-diagonal entries. Thus it is one lift, not a unique coherence-preserving reconstruction of K. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/13_finite_qm_information/quantum_information.md`

- file: [dag/derivations/13_finite_qm_information/quantum_information.md](../../../dag/derivations/13_finite_qm_information/quantum_information.md)
- sha256 (`lf-normalised`): `8ee593efc75d4739338be886916654c69e07b4143c7c622d3924c25f910b32d7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_2611_qi_classical_channel_lift.md`

- file: [dag/derivations/13_finite_qm_information/tfq_2611_qi_classical_channel_lift.md](../../../dag/derivations/13_finite_qm_information/tfq_2611_qi_classical_channel_lift.md)
- sha256 (`lf-normalised`): `d83505f6e2a9d91ae776b463b03bae92cc1ace127aba2d7a01f37b1b122cd8b9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2611
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-QI-CLASSICAL-CHANNEL-LIFT` `DERIVED_PROSE`: [QI-MODEL-ADMISSION](QI-MODEL-ADMISSION.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

