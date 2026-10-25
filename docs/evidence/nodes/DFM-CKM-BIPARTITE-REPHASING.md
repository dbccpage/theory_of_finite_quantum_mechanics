# DFM-CKM-BIPARTITE-REPHASING

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> K_{N_g,N_g} has N_g up and N_g down vertices and N_g^2 edges carrying V_{alpha j}; rephasing V_{alpha j} -\> e^{i phi_alpha} V_{alpha j} e^{-i phi_j} is a U(1) vertex coboundary, and the plaquette is Q_{alpha beta j k}(V) = V_{alpha j} V_{beta k} conj(V_{alpha k}) conj(V_{beta j}).

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Keep the phases in the unit circle of Q(i) or declare the larger field.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.7-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1123_dfm_ckm_bipartite_rephasing.md`

- file: [dag/derivations/24_dressing_field/tfq_1123_dfm_ckm_bipartite_rephasing.md](../../../dag/derivations/24_dressing_field/tfq_1123_dfm_ckm_bipartite_rephasing.md)
- sha256 (`lf-normalised`): `f2be511cdf98ec6282269b75647efbda3cb11c1cf9941bca52de3ca3e9d420f2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1123
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CKM-BIPARTITE-REPHASING` `DERIVED_PROSE`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION), [DFM-ABELIAN-TREE-PROJECTOR](DFM-ABELIAN-TREE-PROJECTOR.md) (DEFINITION)

Outgoing (2):

- `APP-R-DFM-CKM-CYCLE-COUNT` `DERIVED_LEAN`: [DFM-CKM-CYCLE-COUNT](DFM-CKM-CYCLE-COUNT.md) (PROVED_LEAN)
- `APP-R-DFM-JARLSKOG-QUARTET-INVARIANCE` `DERIVED_LEAN`: [DFM-JARLSKOG-QUARTET-INVARIANCE](DFM-JARLSKOG-QUARTET-INVARIANCE.md) (PROVED_LEAN)
