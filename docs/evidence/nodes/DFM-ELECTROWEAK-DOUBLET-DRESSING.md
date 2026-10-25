# DFM-ELECTROWEAK-DOUBLET-DRESSING

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a doublet Phi = (phi_1, phi_2) over Q(i) with Phi^dagger Phi = v^2, v in Q_{\>0}, u(Phi) = (1/v)\[\[conj phi_2, phi_1\], \[-conj phi_1, phi_2\]\]; for rational (g, g') the neutral mass matrix is (v^2/4)\[\[g^2, -g g'\], \[-g g', g'^2\]\] with projectors P_gamma, P_Z.

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

Keep v rational and nonzero, and keep the hypercharge normalization (dossier Q = T_3 + Y, documentation Q = T_3 + Y/2) stated.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.6-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1118_dfm_electroweak_doublet_dressing.md`

- file: [dag/derivations/24_dressing_field/tfq_1118_dfm_electroweak_doublet_dressing.md](../../../dag/derivations/24_dressing_field/tfq_1118_dfm_electroweak_doublet_dressing.md)
- sha256 (`lf-normalised`): `c26c394ea7138c3de7836676047b4bb9d4774e724e4ebd5492a9ad64dbdd3fe1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1118
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-ELECTROWEAK-DOUBLET-DRESSING` `DERIVED_PROSE`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (3):

- `APP-R-DFM-EW-DOUBLET-REDUCTION` `DERIVED_LEAN`: [DFM-EW-DOUBLET-REDUCTION](DFM-EW-DOUBLET-REDUCTION.md) (PROVED_LEAN)
- `APP-R-DFM-SM-ANOMALY-NC-THREE` `DERIVED_LEAN`: [DFM-SM-ANOMALY-NC-THREE](DFM-SM-ANOMALY-NC-THREE.md) (PROVED_LEAN)
- `APP-R-DFM-WEINBERG-PROJECTORS-RHO` `DERIVED_LEAN`: [DFM-WEINBERG-PROJECTORS-RHO](DFM-WEINBERG-PROJECTORS-RHO.md) (PROVED_LEAN)
