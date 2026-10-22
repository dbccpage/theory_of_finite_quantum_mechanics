# DFM-TREE-MOMENTUM-ROUTING

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For external momenta q_v in Q^d with sum zero and a spanning tree T, p_T(e) is minus the total momentum on one side of e for e in T and 0 on chords; F_0(alpha; q) is the sum over spanning 2-forests (F, V_1, V_2) of prod_{e not in F} alpha_e times |sum_{v in V_1} q_v|^2.

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

None recorded.

## Bottleneck

Keep the metric on Q^d, the sign convention for p_T and the mass term of F_G explicit.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.3-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1107_dfm_tree_momentum_routing.md`

- file: [dag/derivations/24_dressing_field/tfq_1107_dfm_tree_momentum_routing.md](../../../dag/derivations/24_dressing_field/tfq_1107_dfm_tree_momentum_routing.md)
- sha256 (`lf-normalised`): `c94fa4e5c47861852ee762cfa5efbf27083474a9eadc43ab4515c82dcd93ca82`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1107
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-TREE-MOMENTUM-ROUTING` `DERIVED_PROSE`: [DFM-ABELIAN-TREE-PROJECTOR](DFM-ABELIAN-TREE-PROJECTOR.md) (DEFINITION)

Outgoing (2):

- `APP-R-DFM-BPHZ-SECTOR-KERNEL` `COMPUTED`: [DFM-BPHZ-SECTOR-KERNEL](DFM-BPHZ-SECTOR-KERNEL.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-TWO-FOREST-F0-DIAMOND` `COMPUTED`: [DFM-TWO-FOREST-F0-DIAMOND](DFM-TWO-FOREST-F0-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
