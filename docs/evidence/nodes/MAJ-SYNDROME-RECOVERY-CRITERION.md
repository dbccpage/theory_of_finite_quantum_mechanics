# MAJ-SYNDROME-RECOVERY-CRITERION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For B = im d0, Q = d1 and an admitted error set E in C1, a syndrome-only recovery succeeds for every e in E if and only if (E + E) intersected with ker Q is contained in B.

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

- recovery model: deterministic syndrome-only decoder applying a C1 correction; success means the residual error lies in B

## Bottleneck

Lean or exact-code witness of the criterion is absent; the recovery model (deterministic decoder seeing only Qe, success meaning the residual lies in B) is declared in the proof.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-THM-SYNDROME-RECOVERY claims PROVED_PROSE; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/28_majorana/tfq_1147_maj_syndrome_recovery_criterion.md`

- file: [dag/derivations/28_majorana/tfq_1147_maj_syndrome_recovery_criterion.md](../../../dag/derivations/28_majorana/tfq_1147_maj_syndrome_recovery_criterion.md)
- sha256 (`lf-normalised`): `687055fa64aaf65662cb2ce2a3c7e36b98130c9683a5ac888fc2edb5cc8e0a61`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1147
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-SYNDROME-RECOVERY-CRITERION` `DERIVED_PROSE`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION), [DS-QM102-SYNDROME-CAPACITY-BOUND](DS-QM102-SYNDROME-CAPACITY-BOUND.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MAJ-DISTANCE-WEIGHT-CORRECTION` `GAP_NO_DERIVATION`: [MAJ-DISTANCE-WEIGHT-CORRECTION](MAJ-DISTANCE-WEIGHT-CORRECTION.md) (OPEN)
- `APP-R-MAJ-OPEN-LIEB-ROBINSON-LOCALITY` `GAP_NO_DERIVATION`: [MAJ-OPEN-LIEB-ROBINSON-LOCALITY](MAJ-OPEN-LIEB-ROBINSON-LOCALITY.md) (OPEN)
