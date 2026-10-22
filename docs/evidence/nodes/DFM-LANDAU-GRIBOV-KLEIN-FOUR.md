# DFM-LANDAU-GRIBOV-KLEIN-FOUR

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite graph with SU(3, Q(i)) links, the discrete Landau condition is the vanishing vertex divergence of the traceless anti-Hermitian parts of U^g; K_4 = {I, diag(1,-1,-1), diag(-1,1,-1), diag(-1,-1,1)}; the Hessian form along H^(23) = E_23 + E_32 is Tr(U (H^(23))^2).

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

The quadratic form along one generator is a stand-in for the Faddeev-Popov operator, not its spectrum.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.8-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1129_dfm_landau_gribov_klein_four.md`

- file: [dag/derivations/24_dressing_field/tfq_1129_dfm_landau_gribov_klein_four.md](../../../dag/derivations/24_dressing_field/tfq_1129_dfm_landau_gribov_klein_four.md)
- sha256 (`lf-normalised`): `59dd5e79eb56ae57832983876a963fc4bbbf746197c5be3b34826206608221bf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1129
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-LANDAU-GRIBOV-KLEIN-FOUR` `DERIVED_PROSE`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (2):

- `APP-R-DFM-SU3-GRIBOV-COPIES-DIAMOND` `COMPUTED`: [DFM-SU3-GRIBOV-COPIES-DIAMOND](DFM-SU3-GRIBOV-COPIES-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-SU3-TREE-DRESSING-DIAMOND` `COMPUTED`: [DFM-SU3-TREE-DRESSING-DIAMOND](DFM-SU3-TREE-DRESSING-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
