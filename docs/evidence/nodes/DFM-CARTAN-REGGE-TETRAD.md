# DFM-CARTAN-REGGE-TETRAD

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Lambda(beta) for rational beta in (-1, 1) is the boost with entries (1+beta^2)/(1-beta^2) and 2 beta/(1-beta^2); each 4-simplex carries e_sigma in GL(4, Q), each shared tetrahedron Omega in SO+(1,3; Q); g_sigma = e^T eta e, Gamma = e_sigma^{-1} Omega e_sigma', and H_h is the ordered product of Gamma around a hinge.

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

Keep the frame action e -\> L e and Omega -\> L Omega L'^{-1} explicit.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.9-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1133_dfm_cartan_regge_tetrad.md`

- file: [dag/derivations/24_dressing_field/tfq_1133_dfm_cartan_regge_tetrad.md](../../../dag/derivations/24_dressing_field/tfq_1133_dfm_cartan_regge_tetrad.md)
- sha256 (`lf-normalised`): `829304672f6b6166d164a40f3585b68048741fe0ed15cf79c63a5cfa07b02f72`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1133
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-CARTAN-REGGE-TETRAD` `DERIVED_PROSE`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (2):

- `APP-R-DFM-BOOST-PLANE-LEAN` `DERIVED_LEAN`: [DFM-BOOST-PLANE-LEAN](DFM-BOOST-PLANE-LEAN.md) (PROVED_LEAN)
- `APP-R-DFM-DRESSED-AFFINE-TRANSPORT` `DERIVED_PROSE`: [DFM-DRESSED-AFFINE-TRANSPORT](DFM-DRESSED-AFFINE-TRANSPORT.md) (PROVED_PROSE)
