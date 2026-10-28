# FQCD-FINITE-GROUP-FREEZING-FENCE

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `SOURCE_RECORD`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Source record: lattice gauge theories whose gauge group is a finite subgroup of SU(2) or SU(3) follow the Lie-group theory at small beta and undergo a freezing transition at larger beta (Petcher-Weingarten 1980 for subgroups of SU(2); Bhanot-Rebbi 1981 for the 1080-element subgroup of SU(3)).

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

Fence: a fixed finite gauge group is not a route to the asymptotically free continuum limit, which needs beta to go to infinity; a finite route must enlarge the group, or pass to a quantum-group truncation, together with the lattice. The cited results are numerical; no rigorous freezing theorem is recorded here.

## Source status

Added 2026-10-27 with maintainer approval as a record of published or announced work; it carries no derivation status in this graph.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1053_fqcd_finite_group_freezing_fence.md`

- file: [dag/derivations/17_finite_qcd/tfq_1053_fqcd_finite_group_freezing_fence.md](../../../dag/derivations/17_finite_qcd/tfq_1053_fqcd_finite_group_freezing_fence.md)
- sha256 (`lf-normalised`): `d2e8d702d927d042b9c84c2d14ece2e71ba2fa286d2145efce6b8f4ccd0a4e13`
- generated view: listed, not counted
- cited in: record TFQ-1053
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `23dbe23bf9913bed6b5ea2428aae9f15b82a0e260a1a8894a23aa1d3d301475f`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:D. Petcher, D. H. Weingarten, Phys. Rev. D 22 (1980) 2465`
- `external:G. Bhanot, C. Rebbi, Phys. Rev. D 24 (1981) 3319`

## Routes

Incoming (1):

- `FQCD-R-FINITE-GROUP-FREEZING-FENCE` `RECORD_PARENT`: [TFQ-0031](TFQ-0031.md) (OPEN), [TFQ-0012](TFQ-0012.md) (OPEN)

Outgoing (0):

