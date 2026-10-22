# DFM-DRESSED-DIRAC-PROPAGATOR

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> gamma^mu in M_4(Q(i)) satisfy {gamma^mu, gamma^nu} = 2 eta^{mu nu} I_4 with eta = diag(1,-1,-1,-1); S_F(p) = (pslash - m)^{-1} = (pslash + m)/(p^2 - m^2) for p^2 != m^2; a vertex field is dressed by psi^(T)_v = u_T(v)^{-1} psi_v.

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

Keep the gamma family admission and the non-singularity condition p^2 != m^2 explicit.

## Source status

papers/ravera_dfm_dossier.md record DFM-P3.4-DEF claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/24_dressing_field/tfq_1111_dfm_dressed_dirac_propagator.md`

- file: [dag/derivations/24_dressing_field/tfq_1111_dfm_dressed_dirac_propagator.md](../../../dag/derivations/24_dressing_field/tfq_1111_dfm_dressed_dirac_propagator.md)
- sha256 (`lf-normalised`): `25dffb83eb547d721cc2450a1156ff35fca13063c939be8fdfe51114c6c1b188`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1111
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-DRESSED-DIRAC-PROPAGATOR` `DERIVED_PROSE`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-DFM-CLIFFORD-WARD-TAKAHASHI` `DERIVED_PROSE`: [DFM-CLIFFORD-WARD-TAKAHASHI](DFM-CLIFFORD-WARD-TAKAHASHI.md) (PROVED_PROSE)
- `APP-R-DFM-DRESSED-CORRELATOR-DIAMOND` `COMPUTED`: [DFM-DRESSED-CORRELATOR-DIAMOND](DFM-DRESSED-CORRELATOR-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
