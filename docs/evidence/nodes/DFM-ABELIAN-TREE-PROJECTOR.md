# DFM-ABELIAN-TREE-PROJECTOR

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite connected graph with coboundary (d_0 lambda)_(u,v) = lambda(v) - lambda(u) and a rooted spanning tree T, u_T\[A\](v) is the signed sum of A along the tree path from the root, and Pi_T(A) = A - d_0 u_T\[A\] on C^1(G; Q).

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

Keep the root, the tree, the edge orientations and the additive group (Q, +) explicit; this is the additive case of TFQ-0397.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.1-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1101_dfm_abelian_tree_projector.md`

- file: [dag/derivations/24_dressing_field/tfq_1101_dfm_abelian_tree_projector.md](../../../dag/derivations/24_dressing_field/tfq_1101_dfm_abelian_tree_projector.md)
- sha256 (`lf-normalised`): `3adcdb8b2a43ece73ca1e70f6710394a25b8a7120bc7227977434380ef791cf7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1101
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-ABELIAN-TREE-PROJECTOR` `DERIVED_PROSE`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-DFM-ABELIAN-RETRACTION-DIAMOND` `COMPUTED`: [DFM-ABELIAN-RETRACTION-DIAMOND](DFM-ABELIAN-RETRACTION-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-CKM-BIPARTITE-REPHASING` `DERIVED_PROSE`: [DFM-CKM-BIPARTITE-REPHASING](DFM-CKM-BIPARTITE-REPHASING.md) (DEFINITION)
- `APP-R-DFM-TREE-MOMENTUM-ROUTING` `DERIVED_PROSE`: [DFM-TREE-MOMENTUM-ROUTING](DFM-TREE-MOMENTUM-ROUTING.md) (DEFINITION)
