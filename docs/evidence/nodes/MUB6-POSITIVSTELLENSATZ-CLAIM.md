# MUB6-POSITIVSTELLENSATZ-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: an exact rational Positivstellensatz identity -1 = sum p_i s_i^2 + sum q_j g_j over the 180 residuals g_j refutes every fourth basis.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

No such certificate is in the checkout; the only Stengle identity present (singular Segre slice, residual R7) is NOT_A_CERTIFICATE because its separating polynomial equals -1/1000 on the slice by construction.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-073 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1241_mub6_positivstellensatz_claim.md`

- file: [dag/derivations/25_mub/tfq_1241_mub6_positivstellensatz_claim.md](../../../dag/derivations/25_mub/tfq_1241_mub6_positivstellensatz_claim.md)
- sha256 (`lf-normalised`): `b1a4e40fb6a05c19b8a279b71fdd808e01842a34bd47d8b076a2598d9f7c50ea`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1241
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6_change_log.md`

- file: [papers/core/mub6/mub6_change_log.md](../../../papers/core/mub6/mub6_change_log.md)
- sha256 (`lf-normalised`): `289562fee89b61899f12541494bd67401f95abfd5f45952610c1de80a121f556`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_global_proof_atlas.md`

- file: [papers/core/mub6/mub6_global_proof_atlas.md](../../../papers/core/mub6/mub6_global_proof_atlas.md)
- sha256 (`lf-normalised`): `94d599e65738f154ef0604e436b2e084b04c879c965f6015916781ef857a1209`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `b515bf981d6c3a339c2b0a7937d54d9deb05f3b53186c584b83f5fa3419dc902`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-POSITIVSTELLENSATZ-CLAIM` `GAP_NO_DERIVATION`: [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (1):

- `APP-R-MUB6-RATIONAL-LDL-CLAIM` `GAP_NO_DERIVATION`: [MUB6-RATIONAL-LDL-CLAIM](MUB6-RATIONAL-LDL-CLAIM.md) (OPEN)
