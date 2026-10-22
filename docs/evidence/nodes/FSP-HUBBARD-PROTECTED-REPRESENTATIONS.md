# FSP-HUBBARD-PROTECTED-REPRESENTATIONS

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hubbard determinant positivity is restricted to the package stated half-filled bipartite or attractive spin-balanced hypotheses; exact negative fields outside those protections remain distinct witnesses.

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

- stated Hubbard model and protected symmetry hypotheses

## Bottleneck

Prove the required determinant pairing and Hamiltonian-to-representation equality for each stated model, including boundary cases.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md`

- file: [dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md](../../../dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md)
- sha256 (`lf-normalised`): `9a23cc13f78442d23b4852e3edb6c06ceb20dc6a9699025192a1cf57d0b1968c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0408
- counts toward the grade: no

### Documents and data: `papers/core/fsp/README.md`

- file: [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- sha256 (`lf-normalised`): `49bf9e23ec5b96cfd3fbd8bfff74f2a03d0151e20c497589d4233136dc24ca5b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/docs/sql_meron_hubbard.md`

- file: [papers/core/fsp/docs/sql_meron_hubbard.md](../../../papers/core/fsp/docs/sql_meron_hubbard.md)
- sha256 (`lf-normalised`): `88c5febb35077085c1e428eb5a75dc2d85357afd66bc2faff916abd8bf1a74de`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-HUBBARD-PROTECTED-REPRESENTATIONS` `CONDITIONAL_ON_IMPORT`: [FSP-SWITCHING-NORMAL-FORM](FSP-SWITCHING-NORMAL-FORM.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `GAP_NO_DERIVATION`: [FSP-EFFICIENT-SAMPLING-OBLIGATIONS](FSP-EFFICIENT-SAMPLING-OBLIGATIONS.md) (OPEN)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-U1-WILSON-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (IMPORTED_ASSUMPTION)
