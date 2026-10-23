# FSP-MAJORANA-CLIFFORD-PARITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For N CAR modes, gamma_{2j-1} = c_j + c_j^dagger and gamma_{2j} = -i(c_j - c_j^dagger) are self-adjoint with {gamma_a, gamma_b} = 2 delta_ab, generate the Clifford algebra on 2N generators, and P = prod_j (-i gamma_{2j-1} gamma_{2j}) is the fermion parity (-1)^N_op.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Majorana operator decomposition of CAR modes (standard literature result)
- fermion parity superselection (physical postulate)

## Bottleneck

Standard algebra imported, not derived here; the trunk mechanizes only the two-generator case (DS-QM212-MAJORANA-PROBLEM). Parity superselection is a physical postulate, not a consequence of the algebra.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-020 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md`

- file: [dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md](../../../dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md)
- sha256 (`lf-normalised`): `dea1de965df82e4b16b90a7f726b990d1a873adf02610c15676d06b427a4eb97`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1186
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-MAJORANA-CLIFFORD-PARITY` `CONDITIONAL_ON_IMPORT`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
