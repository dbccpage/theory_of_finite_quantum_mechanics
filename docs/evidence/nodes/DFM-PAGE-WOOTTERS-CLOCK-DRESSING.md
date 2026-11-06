# DFM-PAGE-WOOTTERS-CLOCK-DRESSING

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On Q(i)^N tensor Q(i)^d with cyclic clock shift S_C and a unitary step U_S with U_S^N = I_d, W = S_C tensor U_S and D = sum_t |t\>\<t| tensor U_S^t; the discrete time shift is treated as the gauge action.

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

None recorded.

## Bottleneck

Keep the finite clock period N and the hypothesis U_S^N = I_d explicit.

## Source status

dag/derivations/24_dressing_field/ravera_dfm_dossier.md record DFM-P3.5-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/ravera_dfm_dossier.md`

- file: [dag/derivations/24_dressing_field/ravera_dfm_dossier.md](../../../dag/derivations/24_dressing_field/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `a41d66a41925e1236c1c506bfb4e3fa7222de96f7211faa6981d14b677cbe36b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1115_dfm_page_wootters_clock_dressing.md`

- file: [dag/derivations/24_dressing_field/tfq_1115_dfm_page_wootters_clock_dressing.md](../../../dag/derivations/24_dressing_field/tfq_1115_dfm_page_wootters_clock_dressing.md)
- sha256 (`lf-normalised`): `8f8e66cc108d9ab76a923259e814223360cc4b19854d6aadee4e0f9922478385`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1115
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-DFM-PAGE-WOOTTERS-CLOCK-DRESSING` `DERIVED_PROSE`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (1):

- `APP-R-DFM-CLOCK-DRESSING-INTERTWINER` `DERIVED_PROSE`: [DFM-CLOCK-DRESSING-INTERTWINER](DFM-CLOCK-DRESSING-INTERTWINER.md) (PROVED_PROSE)
