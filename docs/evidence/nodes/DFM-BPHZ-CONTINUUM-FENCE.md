# DFM-BPHZ-CONTINUUM-FENCE

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Algebraic cancellation of nested and overlapping UV boundary poles for actual Feynman-parametric integrands, and its use before continuum integration, is not established by the finite artifacts.

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

- Zimmermann forest formula
- continuum loop-momentum integration

## Bottleneck

State a forest formula for declared graph integrands with an explicit subtraction operator and a convergence statement before using the BPHZ language.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.3-FENCE claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md`

- file: [dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md](../../../dag/derivations/24_dressing_field/tfq_1110_dfm_bphz_continuum_fence.md)
- sha256 (`lf-normalised`): `f159decfb82a6929f7e0326d90c105de94f4c7253ee9fb7af37e5019646cfbd1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1110
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-BPHZ-CONTINUUM-FENCE` `GAP_NO_DERIVATION`: [DFM-BPHZ-SECTOR-KERNEL](DFM-BPHZ-SECTOR-KERNEL.md) (COMPUTATIONALLY_CHECKED), [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)

Outgoing (1):

- `APP-R-DFM-Z1-Z2-COUNTERTERM-FENCE` `GAP_NO_DERIVATION`: [DFM-Z1-Z2-COUNTERTERM-FENCE](DFM-Z1-Z2-COUNTERTERM-FENCE.md) (OPEN)
