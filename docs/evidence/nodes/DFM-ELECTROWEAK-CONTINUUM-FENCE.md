# DFM-ELECTROWEAK-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The residual U(1)_Y covariance u(e^{i alpha/2} Phi) = u(Phi) diag(e^{-i alpha/2}, e^{i alpha/2}), the dressed gauge field with derivative term, and the reading as an electroweak model without spontaneous symmetry breaking are not established by the finite artifacts.

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

- continuum gauge fields W_mu and derivatives
- U(1)_Y phases outside Q(i)

## Bottleneck

Generic phases e^{i alpha/2} are not in Q(i); keep the residual covariance on declared rational phases and keep the continuum Standard Model and Elitzur reading as interfaces.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.6-FENCE claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1122_dfm_electroweak_continuum_fence.md)
- sha256 (`lf-normalised`): `27e43b224abb4af5cf579dfa83a30c4f1dacf5044cd9eacf5936040c68061e07`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1122
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-ELECTROWEAK-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-EW-DOUBLET-REDUCTION](DFM-EW-DOUBLET-REDUCTION.md) (PROVED_LEAN), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (1):

- `APP-R-DFM-CKM-PHYSICS-FENCE` `GAP_NO_DERIVATION`: [DFM-CKM-PHYSICS-FENCE](DFM-CKM-PHYSICS-FENCE.md) (OPEN)
