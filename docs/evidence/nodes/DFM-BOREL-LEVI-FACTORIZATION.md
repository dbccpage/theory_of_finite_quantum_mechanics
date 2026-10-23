# DFM-BOREL-LEVI-FACTORIZATION

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> B_2(Q) is the group of invertible upper-triangular rational 2x2 matrices, N its unipotent normal subgroup and T_2(Q) the diagonal torus; a tree holonomy \[\[a,b\],\[0,d\]\] factors as \[\[1,b/d\],\[0,1\]\] diag(a,d), giving the stage-1 dressing u_N and stage-2 dressing t.

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

Uniqueness of the factorization and quotient preservation for a supplied rooted tree are recorded at TFQ-0400. Extracting a spanning tree from an arbitrary graph is outside that record.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.2-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1105_dfm_borel_levi_factorization.md`

- file: [dag/derivations/24_dressing_field/tfq_1105_dfm_borel_levi_factorization.md](../../../dag/derivations/24_dressing_field/tfq_1105_dfm_borel_levi_factorization.md)
- sha256 (`lf-normalised`): `a85608891ddffe71ae9aa61ae898f8f5de39bd85b966391ae7f3f98f89500c16`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1105
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-BOREL-LEVI-FACTORIZATION` `DERIVED_PROSE`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN), [DFM-HIERARCHICAL-BOREL](DFM-HIERARCHICAL-BOREL.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-DFM-BOREL-TWO-STAGE-DIAMOND` `COMPUTED`: [DFM-BOREL-TWO-STAGE-DIAMOND](DFM-BOREL-TWO-STAGE-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
